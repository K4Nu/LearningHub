"""
URL configuration for Starter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import allauth.account.views as allauth_views
from user.views import ConfirmEmailView,SignupView,PasswordResetDoneView,EmailView,RedirectView,PasswordChangeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/register", SignupView.as_view(), name="account_signup"),
     path("accounts/confirm-email/",ConfirmEmailView.as_view(),name="account_confirm_email"),
    path("accounts/confirm-email/<str:key>/", ConfirmEmailView.as_view(), name="account_confirm_email"),
    path("accounts/password/reset/done/",PasswordResetDoneView.as_view(),name="account_password_reset_done"),
    path("accounts/password/reset/key/done/",PasswordResetDoneView.as_view(),name="account_password_reset_key"),
    path("accounts/password/change/",PasswordChangeView.as_view(),name="account_password_change"),
    path("accounts/email/",EmailView.as_view(),name="account_email"),
    path("accounts/reauthenticate/",RedirectView.as_view(),name="account_reauthenticate"),
    path("user/",include("user.urls")),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)