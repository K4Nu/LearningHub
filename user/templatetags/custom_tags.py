from django import template
from django.forms import CheckboxInput
from allauth.socialaccount.models import SocialAccount

register = template.Library()

@register.filter(name="is_checkbox")
def is_checkbox(field):
    return isinstance(field.field.widget, CheckboxInput)

@register.filter(name="strip_last_char")
def strip_last_char(field):
    if isinstance(field,str):
        return field[:-1]
    return field

@register.filter(name="has_social_account")  # Fixed: No extra space
def has_social_account(user):  # Fixed: No extra space
    return SocialAccount.objects.filter(user=user).exists()