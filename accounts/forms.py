import secrets

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import AVATAR_COLORS, Profile, profile_for

DISPLAY_NAME_LABEL = "What should we call you?"
ADULT_LABEL = "I am 18 or older and comfortable with adult content."


class SignupForm(UserCreationForm):
    display_name = forms.CharField(max_length=40, label=DISPLAY_NAME_LABEL)
    adult_confirmed = forms.BooleanField(required=True, label=ADULT_LABEL)

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


class GoogleSignupForm(forms.Form):
    """The last step of signing up with Google: the same display name and 18+ check as SignupForm."""

    display_name = forms.CharField(max_length=40, label=DISPLAY_NAME_LABEL)
    adult_confirmed = forms.BooleanField(required=True, label=ADULT_LABEL)

    def save(self, google_id):
        # Nobody types this username: they log in with Google, and the app shows the display name.
        User = get_user_model()
        username = f"google-{secrets.token_hex(5)}"
        while User.objects.filter(username=username).exists():
            username = f"google-{secrets.token_hex(5)}"
        user = User(username=username)
        user.set_unusable_password()
        user.save()
        profile = profile_for(user)
        profile.display_name = self.cleaned_data["display_name"].strip()
        profile.adult_confirmed = True
        profile.google_id = google_id
        profile.save()
        return user


class DeleteAccountForm(forms.Form):
    """Asks for the password, or, for accounts that only log in with Google, to type DELETE."""

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if user.has_usable_password():
            self.fields["password"] = forms.CharField(
                label="Your password", strip=False, widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
            )
        else:
            self.fields["confirm"] = forms.CharField(
                label="Type DELETE to confirm", widget=forms.TextInput(attrs={"autocomplete": "off"})
            )

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("That password isn't right.")
        return password

    def clean_confirm(self):
        confirm = self.cleaned_data["confirm"]
        if confirm.strip().upper() != "DELETE":
            raise forms.ValidationError("Type DELETE to confirm.")
        return confirm


class ProfileForm(forms.ModelForm):
    avatar_color = forms.ChoiceField(choices=AVATAR_COLORS, widget=forms.RadioSelect)

    class Meta:
        model = Profile
        fields = ["display_name", "avatar_color", "notification_previews"]
        labels = {
            "display_name": "Display name",
            "avatar_color": "Your color",
            "notification_previews": "Show wish titles in notifications",
        }
        help_texts = {
            "notification_previews": "When off, notifications only say who did something, so nothing private shows on your lock screen.",
        }
