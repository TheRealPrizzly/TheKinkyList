import random

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AVATAR_COLORS, Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, defaults={"avatar_color": random.choice(AVATAR_COLORS)[0]})
