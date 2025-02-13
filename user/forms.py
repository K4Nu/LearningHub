from allauth.account.forms import SignupForm
from .models import CustomUser
from django import forms

class MyCustomSignupForm(SignupForm):

    field_order = ['email', 'password1', 'password2']

    def clean_email(self):
        email=self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email
