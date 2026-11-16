from django import forms

from .models import SPICE_CHOICES, Dare, Item, Question, Truth
from .utils import split_categories


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

    def clean_categories(self):
        return split_categories(self.cleaned_data["categories"])


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
