from django.urls import path,include
from . import views


app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path("create-profile/",views.ProfileCreateView.as_view(), name='create-profile'),
]