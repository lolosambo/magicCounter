from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordChangeDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LoginView
from django.shortcuts import render, redirect
from datetime import datetime

from django.urls import reverse_lazy
from user.models import CustomUser
from user.forms import UserProfileForm
from django.contrib.auth.forms import UserCreationForm


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields


def signup(request):
    context = {}
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, 'magicCounteur/index.html', {"user": user})
        else:
            context["errors"] = form.errors
    form = CustomSignupForm()
    context["form"] = form

    return render(request, 'user/signup.html', context=context)


def profile(request):
    form = UserProfileForm()
    user = request.user
    if user.is_authenticated:
        form.fields['date_of_birth'].initial = user.date_of_birth.strftime("%Y-%m-%d")
        form.fields['email'].initial = user.email
    if request.method == "POST":
        user.email = request.POST.get('email')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.save()
        return redirect("profile")

    return render(request, 'account/profile.html', context={"user": user, "form": form})


class CustomPasswordChangeView(PasswordChangeView):
    model = CustomUser
    context_object_name = "user"
    template_name = "user/change_password.html"
    success_url = reverse_lazy("login")


class CustomPasswordResetView(PasswordResetView):
    template_name = "user/reset_password.html"
    success_url = reverse_lazy("user_password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "user/reset_password_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("user_password_reset_complete")
    template_name = "user/reset_password_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "user/reset_password_complete.html"

class CustomLoginResetView(LoginView):
    success_url = reverse_lazy("homepage")
