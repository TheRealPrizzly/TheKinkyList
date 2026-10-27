import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

# No 0/O or 1/I so codes are easy to read aloud and type.
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
CODE_LENGTH = 6


def generate_invite_code():
    while True:
        code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
        if not Space.objects.filter(invite_code=code).exists():
            return code


class Space(models.Model):
    name = models.CharField(max_length=60)
    invite_code = models.CharField(max_length=CODE_LENGTH, unique=True, default=generate_invite_code)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def member_users(self):
        return (
            get_user_model()
            .objects.filter(memberships__space=self)
            .select_related("profile")
            .order_by("memberships__joined_at")
        )

    def has_member(self, user):
        return user.is_authenticated and self.memberships.filter(user=user).exists()


class Membership(models.Model):
    OWNER = "owner"
    MEMBER = "member"
    ROLE_CHOICES = [(OWNER, "Owner"), (MEMBER, "Member")]

    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["space", "user"], name="unique_membership")]

    def __str__(self):
        return f"{self.user} in {self.space}"
