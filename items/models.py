from django.conf import settings
from django.db import models

SPICE_CHOICES = [(1, "Sweet"), (2, "Spicy"), (3, "Sizzling")]


class Item(models.Model):
    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=40, blank=True)
    spice = models.PositiveSmallIntegerField(choices=SPICE_CHOICES, default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = " ".join(self.title.split())
        self.category = " ".join(self.category.split())
        super().save(*args, **kwargs)

    @property
    def category_label(self):
        return self.category or "Uncategorized"
