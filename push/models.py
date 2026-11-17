from django.conf import settings
from django.db import models


class Device(models.Model):
    """A phone running the app, identified by its Firebase Cloud Messaging token."""

    ANDROID = "android"
    IOS = "ios"
    PLATFORM_CHOICES = [(ANDROID, "Android"), (IOS, "iOS")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="devices")
    # FCM tokens are about 160 characters; Firebase can rotate them, and a reinstall makes a new one.
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_platform_display()} device of {self.user}"
