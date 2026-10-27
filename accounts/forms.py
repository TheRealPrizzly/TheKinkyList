from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import AVATAR_COLORS, Profile, profile_for


class SignupForm(UserCreationForm):
    display_name = forms.CharField(max_length=40, label="What should we call you?")
    adult_confirmed = forms.BooleanField(
        required=True,
        label="I am 18 or older and comfortable with adult content.",
    )

    class Meta(UserCreationForm.Meta):
        fields = ("username",)

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = profile_for(user)
            profile.display_name = self.cleaned_data["display_name"].strip()
            profile.adult_confirmed = True
            profile.save()
        return user


class ProfileForm(forms.ModelForm):
    avatar_color = forms.ChoiceField(choices=AVATAR_COLORS, widget=forms.RadioSelect)

    class Meta:
        model = Profile
        fields = ["display_name", "avatar_color"]
        labels = {"display_name": "Display name", "avatar_color": "Your color"}
