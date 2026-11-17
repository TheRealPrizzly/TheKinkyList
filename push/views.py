from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from .models import Device

# The token this browser session registered, so logging out can forget just this phone.
SESSION_KEY = "push_token"


@login_required
@require_POST
def register_device(request):
    """Called by static/js/push.js inside the app with the phone's FCM token."""
    token = request.POST.get("token", "").strip()
    platform = request.POST.get("platform", "")
    if not token or len(token) > 255 or platform not in dict(Device.PLATFORM_CHOICES):
        return HttpResponseBadRequest("Missing or invalid token.")
    # A phone can change hands (log out, log in as someone else), so the token follows the current user.
    Device.objects.update_or_create(token=token, defaults={"user": request.user, "platform": platform})
    request.session[SESSION_KEY] = token
    return HttpResponse(status=204)
