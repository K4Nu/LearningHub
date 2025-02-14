from django.contrib import messages
from django.shortcuts import render,redirect
from allauth.account.views import ConfirmEmailView,SignupView,PasswordResetDoneView,EmailView
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from django.views.generic import View, FormView, CreateView, DetailView
from .forms import ProfileForm
from PIL import Image
import uuid
import os
from django.urls import reverse_lazy
from django.conf import settings
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import CustomUser,Profile,StudySession



class SignupView(SignupView):
    def form_valid(self, form):
        response=super().form_valid(form)
        storage=get_messages(self.request)
        for message in storage:
            pass
        messages.success(self.request, "Registration successful! Please check your email to verify your account.")
        return redirect("account_login")
class ConfirmEmailView(ConfirmEmailView,):
    def get(self, request, *args, **kwargs):
        try:
            # Get and confirm the email confirmation object
            self.object = self.get_object()
            self.object.confirm(self.request)

            # Clear any existing messages
            storage = get_messages(self.request)
            for message in storage:
                pass  # Clear existing messages

            # Add success message
            messages.success(request, "Email has been confirmed successfully.")

            return redirect("account_login")

        except Exception as e:
            return redirect("account_login")

def index(request):
    return render(request,"user/index.html")

class PasswordResetDoneView(PasswordResetDoneView):

    def get(self, request, *args, **kwargs):
        storage=get_messages(self.request)
        for message in storage:
            pass
        messages.success(self.request, "Password reset successful.")
        return redirect("account_login")

class EmailView(EmailView):

    def get(self, request, *args, **kwargs):
        if not  request.headers.get("HX-Request"):
            return redirect(reverse_lazy("user:index"))
        return super().get(request, *args, **kwargs)

class RedirectView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy("user:index"))


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("user:index")

    def get(self, request, *args, **kwargs):
        # If a GET request is made, immediately redirect.
        return redirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        # Redirect if the user already has a profile
        if request.user.is_authenticated and hasattr(request.user, "profile"):
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        profile = form.save(commit=False)
        avatar = form.cleaned_data.get("avatar")
        if avatar:
            extension = os.path.splitext(avatar.name)[1].lower()
            new_filename = f"{uuid.uuid4().hex}{extension}"
            img = Image.open(avatar)
            img.thumbnail((128, 128))
            output = BytesIO()
            # Map the extension to the correct PIL format
            if extension in ['.jpg', '.jpeg']:
                img_format = 'JPEG'
            elif extension == '.png':
                img_format = 'PNG'
            else:
                # Fallback to JPEG if somehow an unsupported extension gets through
                img_format = 'JPEG'

            img.save(output, format=img_format)
            output.seek(0)

            profile.avatar = InMemoryUploadedFile(
                output,
                "ImageField",
                new_filename,
                avatar.content_type,  # use the original content type
                output.getbuffer().nbytes,
                None
            )
        profile.user = self.request.user
        profile.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        self.request.session['profile_form_errors'] = form.errors.as_json()
        self.request.session['profile_form_data'] = form.data

        return redirect(self.success_url)

class ProfileDashboardView(DetailView):
    model = Profile
    template_name = "user/profile.html"

    def get_object(self):
        return self.request.user.profile