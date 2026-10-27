from django import forms

from .models import SPICE_CHOICES, Item


class ItemForm(forms.ModelForm):
    spice = forms.TypedChoiceField(choices=SPICE_CHOICES, coerce=int, widget=forms.RadioSelect, initial=1)

    class Meta:
        model = Item
        fields = ["title", "description", "category", "spice"]
        labels = {"title": "What's the dream?", "description": "Details (optional)", "category": "Category"}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Slow dance in the kitchen at midnight"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Any details, ideas or boundaries"}),
            "category": forms.TextInput(attrs={"list": "category-options", "placeholder": "Romance, Adventure…"}),
        }


class BulkForm(forms.Form):
    lines = forms.CharField(
        label="Paste your list",
        widget=forms.Textarea(
            attrs={"rows": 8, "placeholder": "One per line. Add a category with a colon:\nRomance: Candlelit bath\nStargazing picnic"}
        ),
    )
