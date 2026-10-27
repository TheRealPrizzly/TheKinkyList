from django import forms

from .models import CODE_LENGTH, Space


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ["name"]
        labels = {"name": "Name your space"}
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Us, forever"})}


class JoinForm(forms.Form):
    code = forms.CharField(
        max_length=CODE_LENGTH + 4,
        label="Invite code",
        widget=forms.TextInput(attrs={"placeholder": "ABC234", "autocomplete": "off", "autocapitalize": "characters"}),
    )

    def clean_code(self):
        code = "".join(self.cleaned_data["code"].split()).upper()
        try:
            self.space = Space.objects.get(invite_code=code)
        except Space.DoesNotExist:
            raise forms.ValidationError("We couldn't find a space with that code.")
        return code
