from django.conf import settings
from django.db import models
from django.db.models.functions import Lower

SPICE_CHOICES = [(1, "Sweet"), (2, "Spicy"), (3, "Sizzling")]


class Category(models.Model):
    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=40)

    class Meta:
        ordering = [Lower("name")]
        constraints = [models.UniqueConstraint(Lower("name"), "space", name="unique_category_name_per_space")]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    @classmethod
    def resolve(cls, space, names):
        """The space's categories for these names, created as needed and matched ignoring case."""
        existing = {category.name.lower(): category for category in space.categories.all()}
        categories = []
        for name in names:
            name = " ".join(name.split())
            if not name:
                continue
            category = existing.get(name.lower())
            if category is None:
                category = existing[name.lower()] = cls.objects.create(space=space, name=name)
            if category not in categories:
                categories.append(category)
        return categories


class Item(models.Model):
    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="items")
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
        super().save(*args, **kwargs)

    @property
    def category_names(self):
        # Uses the prefetch cache when the queryset has prefetch_related("categories").
        return [category.name for category in self.categories.all()]

    def set_categories(self, names):
        self.categories.set(Category.resolve(self.space, names))


def tidy(text):
    return " ".join(text.split())


class Truth(models.Model):
    """A question on the space's Truth or Dare list. "Generate a list" fills it from games/truths.py."""

    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="truths")
    text = models.CharField(max_length=200)
    spice = models.PositiveSmallIntegerField(choices=SPICE_CHOICES, default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["spice", Lower("text")]

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.text = tidy(self.text)
        super().save(*args, **kwargs)


class Dare(models.Model):
    """A dare on the space's Truth or Dare list. "Generate a list" fills it from games/dares.py.

    Capped like Item.title, because saving a dare for later puts it on The Kinky List.
    """

    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="dares")
    text = models.CharField(max_length=140)
    spice = models.PositiveSmallIntegerField(choices=SPICE_CHOICES, default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["spice", Lower("text")]

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.text = tidy(self.text)
        super().save(*args, **kwargs)


class Question(models.Model):
    """A question on the space's "Would you rather" list: "Would you rather <first> or <second>?"."""

    space = models.ForeignKey("spaces.Space", on_delete=models.CASCADE, related_name="questions")
    first = models.CharField(max_length=120)
    second = models.CharField(max_length=120)
    spice = models.PositiveSmallIntegerField(choices=SPICE_CHOICES, default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["spice", Lower("first")]

    def __str__(self):
        return self.text

    @property
    def text(self):
        return f"Would you rather {self.first} or {self.second}?"

    @property
    def key(self):
        """Matches the same question however it was written, e.g. when generating or importing."""
        return f"{self.first.lower()} | {self.second.lower()}"

    def save(self, *args, **kwargs):
        self.first, self.second = tidy(self.first), tidy(self.second)
        super().save(*args, **kwargs)
