from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib import messages
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponseRedirect
from allauth.core.exceptions import ImmediateHttpResponse
from django.urls import reverse
User=get_user_model()

@receiver(pre_social_login)
def pre_social_login_handler(sender,request,sociallogin,**kwargs):
    if not request:
        return

    email=sociallogin.user.email
    existing_user=User.objects.filter(email=email).first()

    if existing_user and not SocialAccount.objects.filter(user=existing_user).exists():
        messages.error(request, "Account exists with this email. Please login with email/password.")
        raise ImmediateHttpResponse(HttpResponseRedirect(reverse('login')))

    return