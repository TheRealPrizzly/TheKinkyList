import logging
import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_POST

from spaces.models import Membership

from . import google
from .forms import DeleteAccountForm, GoogleSignupForm, ProfileForm, SignupForm
from .models import Profile, profile_for

log = logging.getLogger(__name__)

# Session keys: the redirect round trip to Google, and a verified Google account waiting for the 18+ step.
GOOGLE_FLOW = "google_flow"
GOOGLE_SIGNUP = "google_signup"
MODEL_BACKEND = "django.contrib.auth.backends.ModelBackend"


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {profile_for(user).name}. Let's set up your space.")
        return redirect("spaces:index")
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=profile_for(request.user))
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile saved.")
        return redirect("home")
    return render(request, "accounts/profile.html", {"form": form, "profile": form.instance})


# ---------- Sign in with Google (see google.py) ----------


def _safe_next(request, url):
    if url and url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return url
    return ""


def _google_failed(request, text="Google sign-in didn't work. Please try again."):
    messages.error(request, text)
    return redirect("profile" if request.user.is_authenticated else "login")


@require_GET
def google_start(request):
    if not google.is_configured():
        raise Http404
    state, verifier = secrets.token_urlsafe(24), secrets.token_urlsafe(64)
    request.session[GOOGLE_FLOW] = {"state": state, "verifier": verifier, "next": _safe_next(request, request.GET.get("next"))}
    return redirect(google.authorization_url(request.build_absolute_uri(reverse("google_callback")), state, verifier))


@require_GET
def google_callback(request):
    flow = request.session.pop(GOOGLE_FLOW, None)
    if not google.is_configured() or not flow or request.GET.get("state") != flow["state"]:
        return _google_failed(request, "That Google sign-in expired. Please try again.")
    code = request.GET.get("code")
    if not code:
        # They cancelled on Google's page.
        return redirect("profile" if request.user.is_authenticated else "login")
    try:
        identity = google.exchange_code(code, request.build_absolute_uri(reverse("google_callback")), flow["verifier"])
    except google.InvalidCredential as error:
        log.warning("Google sign-in failed: %s", error)
        return _google_failed(request)
    return _signed_in_with_google(request, identity, flow["next"])


@require_POST
def google_token(request):
    """The Android app signs in natively and posts Google's ID token here."""
    if not google.is_configured():
        raise Http404
    try:
        identity = google.verify(request.POST.get("credential", ""))
    except google.InvalidCredential as error:
        log.warning("Google sign-in failed: %s", error)
        return _google_failed(request)
    return _signed_in_with_google(request, identity, _safe_next(request, request.POST.get("next")))


def _signed_in_with_google(request, identity, next_url):
    linked = Profile.objects.filter(google_id=identity.sub).select_related("user").first()
    if request.user.is_authenticated:
        # Connecting Google from the profile page.
        if linked and linked.user_id != request.user.pk:
            messages.error(request, "That Google account is already used by another Kinky List account.")
        else:
            profile = profile_for(request.user)
            profile.google_id = identity.sub
            profile.save(update_fields=["google_id"])
            messages.success(request, "Google connected. You can now log in with it.")
        return redirect("profile")
    if linked:
        if not linked.user.is_active:
            return _google_failed(request, "This account has been deactivated.")
        login(request, linked.user, backend=MODEL_BACKEND)
        return redirect(next_url or settings.LOGIN_REDIRECT_URL)
    request.session[GOOGLE_SIGNUP] = {"sub": identity.sub, "name": identity.name[:40], "next": next_url}
    return redirect("google_signup")


def google_signup(request):
    """New Google users still choose a display name and confirm they're 18 or older."""
    pending = request.session.get(GOOGLE_SIGNUP)
    if request.user.is_authenticated or not pending:
        return redirect("home" if request.user.is_authenticated else "signup")
    form = GoogleSignupForm(request.POST or None, initial={"display_name": pending["name"]})
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save(google_id=pending["sub"])
        except IntegrityError:
            # This Google account finished signing up in another tab meanwhile: log into that one.
            user = Profile.objects.select_related("user").get(google_id=pending["sub"]).user
        del request.session[GOOGLE_SIGNUP]
        login(request, user, backend=MODEL_BACKEND)
        messages.success(request, f"Welcome, {profile_for(user).name}. Let's set up your space.")
        return redirect(pending["next"] or "spaces:index")
    return render(request, "accounts/google_signup.html", {"form": form})


@login_required
@require_POST
def google_disconnect(request):
    if not request.user.has_usable_password():
        messages.error(request, "You log in with Google, so it can't be disconnected.")
        return redirect("profile")
    profile = profile_for(request.user)
    profile.google_id = None
    profile.save(update_fields=["google_id"])
    messages.success(request, "Google disconnected. Log in with your username and password.")
    return redirect("profile")


@login_required
def delete_account(request):
    """Permanently delete the account. Required by the App Store and Google Play for apps with sign-up."""
    form = DeleteAccountForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = request.user
        with transaction.atomic():
            # Leave each space the same way the Leave button does, so shared spaces keep an owner
            # and spaces nobody else is in are deleted with their lists.
            for membership in Membership.objects.filter(user=user).select_related("space"):
                membership.leave()
            logout(request)
            user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("home")
    sole_spaces = [
        m.space for m in Membership.objects.filter(user=request.user).select_related("space") if m.space.memberships.count() == 1
    ]
    return render(request, "accounts/delete.html", {"form": form, "sole_spaces": sole_spaces})


def privacy(request):
    return render(request, "privacy.html", {"contact_email": settings.CONTACT_EMAIL})
