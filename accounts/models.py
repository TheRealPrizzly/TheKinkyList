from django.conf import settings
from django.db import models

AVATAR_COLORS = [
    ("#e11d48", "Rose"),
    ("#fb7185", "Coral"),
    ("#db2777", "Magenta"),
    ("#c084fc", "Lilac"),
    ("#8b5cf6", "Violet"),
    ("#fdba8c", "Peach"),
    ("#f5d7a1", "Champagne"),
    ("#f472b6", "Bubblegum"),
]


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=40, blank=True)
    avatar_color = models.CharField(max_length=7, choices=AVATAR_COLORS, default=AVATAR_COLORS[0][0])
    adult_confirmed = models.BooleanField(default=False)
    last_space = models.ForeignKey("spaces.Space", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.display_name or self.user.get_username()

    @property
    def initial(self):
        return self.name[:1].upper()


def profile_for(user):
    """Return the user's profile, creating one for users made outside signup (e.g. createsuperuser)."""
    try:
        return user.profile
    except Profile.DoesNotExist:
        return Profile.objects.create(user=user)
