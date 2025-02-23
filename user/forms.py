from allauth.account.forms import SignupForm
from .models import CustomUser,Profile,StudySession
from django import forms
import os
from django.conf import settings


class MyCustomSignupForm(SignupForm):

    field_order = ['email', 'password1', 'password2']

    def clean_email(self):
        email=self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'bio', 'avatar']
        widgets = {
            "avatar": forms.FileInput(attrs={
                'class': 'file-input file-input-bordered',  # Base Daisy UI classes
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Use a case-insensitive filter
            qs = Profile.objects.filter(username__iexact=username)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Username already in use")
        return username

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            # Get file extension correctly
            extension = os.path.splitext(avatar.name)[-1].lower()

            if extension not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError("Not allowed file type. Only JPG, JPEG, and PNG are allowed.")

            # Validate file size
            if avatar.size > settings.MAX_IMAGE_SIZE:
                raise forms.ValidationError(
                    "The image is too large. Maximum allowed size is {} bytes.".format(settings.MAX_AVATAR_SIZE))
        else:
            raise forms.ValidationError("Avatar must be provided")
        return avatar

class EmailForm(forms.Form):
    email = forms.EmailField()
    email2 = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")

        if email and email2:
            if email != email2:
                raise forms.ValidationError("The two email addresses must match.")
            if CustomUser.objects.filter(email=email).exists():
                self.add_error("email", "Email already in use")
        return cleaned_data