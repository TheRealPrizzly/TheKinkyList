from datetime import timedelta

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone

from games.registry import GAME_CHOICES

# How long "Not for me" keeps an item from being given to that person again.
NOT_FOR_ME_PERIOD = timedelta(days=182)


class GameSession(models.Model):
    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="game_sessions")
    game_type = models.CharField(max_length=20, choices=GAME_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_game_type_display()} in {self.space}"


class Assignment(models.Model):
    ACTIVE = "active"
    COMPLETED = "completed"
    STATUS_CHOICES = [(ACTIVE, "Active"), (COMPLETED, "Completed")]

    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="assignments")
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE, related_name="assignments")
    session = models.ForeignKey(GameSession, null=True, on_delete=models.SET_NULL, related_name="assignments")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assignments")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item} ({self.status})"

    def is_assignee(self, user):
        return self.assignees.filter(pk=user.pk).exists()

    def complete(self, user, note=""):
        self.status = self.COMPLETED
        self.completed_by = user
        self.completed_at = timezone.now()
        self.note = note.strip()
        self.save(update_fields=["status", "completed_by", "completed_at", "note"])

    @transaction.atomic
    def reply(self, user, kind):
        """Record an assignee's answer. Anything but "Interested" takes them off the item,
        and once nobody is left on it the item goes back on the list."""
        details = {
            "space": self.space,
            "item": self.item,
            "requester": self.assigned_by,
            # Nobody to tell when you drew it for yourself.
            "seen": self.assigned_by_id in (None, user.id),
        }
        if kind == Reply.INTERESTED:
            Reply.objects.get_or_create(assignment=self, user=user, kind=kind, defaults=details)
            return
        self.replies.filter(user=user, kind=Reply.INTERESTED).delete()
        Reply.objects.create(assignment=self, user=user, kind=kind, **details)
        self.assignees.remove(user)
        if not self.assignees.exists():
            self.delete()


class Reply(models.Model):
    """An assignee's answer to something drawn for them, shown to whoever drew it."""

    INTERESTED = "interested"
    LATER = "later"
    NOT_FOR_ME = "not_for_me"
    KIND_CHOICES = [(INTERESTED, "Interested"), (LATER, "Maybe eventually"), (NOT_FOR_ME, "Not for me")]

    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="replies")
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE, related_name="replies")
    # Cleared once the assignment is gone, e.g. when the last assignee hands it back.
    assignment = models.ForeignKey(Assignment, null=True, blank=True, on_delete=models.SET_NULL, related_name="replies")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    kind = models.CharField(max_length=12, choices=KIND_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "replies"

    def __str__(self):
        return f"{self.user}: {self.get_kind_display()} ({self.item})"

    @property
    def blocked_until(self):
        return self.created_at + NOT_FOR_ME_PERIOD

    @classmethod
    def declines(cls, space):
        """The "Not for me" replies still in force."""
        return cls.objects.filter(space=space, kind=cls.NOT_FOR_ME, created_at__gte=timezone.now() - NOT_FOR_ME_PERIOD)

    @classmethod
    def blocked_until_by_person(cls, space):
        """{(item_id, user_id): when that person may be given the item again}."""
        blocked = {}
        for reply in cls.declines(space):
            key = (reply.item_id, reply.user_id)
            blocked[key] = max(blocked.get(key, reply.blocked_until), reply.blocked_until)
        return blocked
