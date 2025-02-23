from django.urls import path,include
from . import views


app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path("create-profile/",views.ProfileCreateView.as_view(), name='create-profile'),
    path("test/", views.TestView.as_view(), name='test'),
    path("profile_essa/",views.FormProfile.as_view(), name='form-profile'),
    path("profile-info/", views.ProfileInfoView.as_view(), name="profile-info"),
    path("profile-delete/",views.DeleteUserView.as_view(), name="delete-profile"),
    path("settings/",views.ProfileSettingsView.as_view(), name="profile-settings"),
    path("profile-theme/",views.ProfileThemeView.as_view(), name="profile-theme"),
    path("<slug:username>/", views.ProfileDashboardView.as_view(), name='profile-detail'),

]