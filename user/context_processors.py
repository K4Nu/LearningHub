from .models import Profile

def get_theme(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'theme': profile.theme}