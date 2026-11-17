from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from .models import Device
from .views import SESSION_KEY


@receiver(user_logged_out)
def forget_device(sender, request, user, **kwargs):
    """Stop notifying this phone once its user logs out. Runs before the session is cleared."""
    token = request.session.get(SESSION_KEY) if request is not None else None
    if token:
        Device.objects.filter(token=token).delete()
