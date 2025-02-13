from django.contrib import messages
from django.shortcuts import render,redirect
from allauth.account.views import ConfirmEmailView,SignupView,PasswordResetDoneView,EmailView
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from django.views.generic import View


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