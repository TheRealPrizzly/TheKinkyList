from django import forms

from .models import SPICE_CHOICES, Item
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
