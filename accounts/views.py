from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from spaces.models import Membership

from .forms import DeleteAccountForm, ProfileForm, SignupForm
from .models import profile_for


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
    return render(request, "accounts/profile.html", {"form": form})


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
