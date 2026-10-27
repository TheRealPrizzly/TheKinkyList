from django.conf import settings
from django.db import models
from django.utils import timezone

from games.registry import GAME_CHOICES


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
