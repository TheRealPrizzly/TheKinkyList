from django import forms

from .models import MAX_LEVELS, SPICE_CHOICES, Dare, Item, Level, Question, Truth
from .utils import split_categories, split_levels

MAX_LEVEL_TEXT = Level._meta.get_field("text").max_length


class ItemForm(forms.ModelForm):
    categories = forms.CharField(
        label="Categories",
        required=False,
        help_text="Separate several with commas.",
        widget=forms.TextInput(attrs={"placeholder": "Romance, Adventure…", "x-ref": "categories"}),
    )
    spice = forms.TypedChoiceField(
        label="Intensity", choices=SPICE_CHOICES, coerce=int, widget=forms.RadioSelect, initial=1
    )
    levels = forms.CharField(
        label="Levels (optional)",
        required=False,
        help_text=(
            "One per line, from a gentle start to the full thing. When you tap Done, you tick the levels "
            "you reached, and the wish keeps coming up in the games until the last one is done."
        ),
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Start gentle\nGo a little further\nThe full thing"}),
    )

    class Meta:
        model = Item
        fields = ["title", "description", "spice"]
        labels = {"title": "Action", "description": "Details (optional)"}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Slow dance in the kitchen at midnight"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Any details, ideas or boundaries"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial["categories"] = ", ".join(self.instance.category_names)
            self.initial["levels"] = "\n".join(level.text for level in self.instance.levels.all())

    def clean_categories(self):
        return split_categories(self.cleaned_data["categories"])

    def clean_levels(self):
        levels = split_levels(self.cleaned_data["levels"])
        if len(levels) > MAX_LEVELS:
            raise forms.ValidationError(f"A wish can have up to {MAX_LEVELS} levels. This has {len(levels)}.")
        for number, level in enumerate(levels, 1):
            if len(level) > MAX_LEVEL_TEXT:
                raise forms.ValidationError(
                    f"Keep each level to {MAX_LEVEL_TEXT} characters. Level {number} has {len(level)}."
                )
        return levels

    def save_levels(self, item):
        """Apply the levels from the form to a saved item."""
        item.set_levels(self.cleaned_data["levels"])


class ItemEditForm(ItemForm):
    """Editing a wish can also start its levels over, in case one was ticked by mistake."""

    reset_levels = forms.BooleanField(
        label="Start the levels over: mark them all as not done", required=False
    )

    def save_levels(self, item):
        super().save_levels(item)
        if self.cleaned_data.get("reset_levels"):
            item.reset_levels()


class BulkForm(forms.Form):
    lines = forms.CharField(
        label="Paste your list",
        help_text=(
            "One per line: <strong>Action | Categories | Intensity</strong>. Categories and intensity are optional. "
            "Separate several categories with commas. Intensity is Sweet, Spicy or Sizzling (or 1 to 3). "
            "Tabs work in place of | too, so you can paste straight from a spreadsheet."
        ),
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": "Candlelit bath | Romance, Relaxing | Sweet\nSkinny dip | Adventure | 3\nStargazing picnic",
            }
        ),
    )


def spice_field():
    return forms.TypedChoiceField(
        label="Intensity", choices=SPICE_CHOICES, coerce=int, widget=forms.RadioSelect, initial=1
    )


KIND_CHOICES = [("truth", "Truth"), ("dare", "Dare")]


class TruthOrDareForm(forms.Form):
    kind = forms.ChoiceField(label="It's a", choices=KIND_CHOICES, widget=forms.RadioSelect, initial="truth")
    text = forms.CharField(
        label="Truth or dare",
        max_length=Truth._meta.get_field("text").max_length,
        widget=forms.TextInput(attrs={"placeholder": "What's something you've never told me?"}),
    )
    spice = spice_field()

    def clean(self):
        data = super().clean()
        limit = Dare._meta.get_field("text").max_length
        if data.get("kind") == "dare" and len(" ".join(data.get("text", "").split())) > limit:
            self.add_error("text", f"Keep a dare to {limit} characters.")
        return data


class TruthOrDareImportForm(forms.Form):
    kind = forms.ChoiceField(label="Add them as", choices=KIND_CHOICES, widget=forms.RadioSelect, initial="truth")
    lines = forms.CharField(
        label="Paste your list",
        help_text=(
            "One per line: <strong>Text | Intensity</strong>. Intensity is optional: Sweet, Spicy or Sizzling "
            "(or 1 to 3). To mix both in one paste, start a line with Truth or Dare: "
            "<strong>Dare | Kiss my neck | Spicy</strong>."
        ),
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": "What's your wildest fantasy? | Spicy\nDare | Kiss my neck for a minute | 1",
            }
        ),
    )


class QuestionForm(forms.ModelForm):
    spice = spice_field()

    class Meta:
        model = Question
        fields = ["first", "second", "spice"]
        labels = {"first": "Would you rather…", "second": "…or"}
        widgets = {
            "first": forms.TextInput(attrs={"placeholder": "be tied up"}),
            "second": forms.TextInput(attrs={"placeholder": "do the tying"}),
        }


class QuestionImportForm(forms.Form):
    lines = forms.CharField(
        label="Paste your list",
        help_text=(
            "One per line: <strong>First choice | Second choice | Intensity</strong>, or write the question out: "
            "<strong>Would you rather kiss or cuddle? | Sweet</strong>. Intensity is optional."
        ),
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": "be tied up | do the tying | Spicy\nWould you rather kiss or cuddle?",
            }
        ),
    )
