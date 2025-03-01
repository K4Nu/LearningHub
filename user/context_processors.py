from .models import Profile

def get_theme(request):
    theme = "Default"
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        profile = Profile.objects.get(user=request.user)
        if profile.theme:
            theme = profile.theme
    return {'theme': theme}