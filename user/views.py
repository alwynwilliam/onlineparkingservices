from django.shortcuts import render
from user import models as user_models


# Create your views here.
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import views as auth_views
from django.contrib import messages

from user import forms as user_form
from user import models

USER = get_user_model()

# UserCreateView
class UserCreateView(views.CreateView):
    template_name = "registration/signup.html"
    form_class = user_form.UserRegisterform
    success_url = reverse_lazy("user:user_login")


class UserLoginView(auth_views.LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class UserLogoutView(views.View):
    template_name = "registration/loggedout.html"

    def get(self, request):
        logout(request)
        messages.success(request, "Successfully Logged out")
        return render(request, self.template_name)


class ProfileCreateView(views.CreateView):
    template_name = "core/profile/profile_create.html"
    model = user_models.ProfileModel
    form_class = user_form.ProfileForm


# feedback updateview
class ProfileUpdateView(views.UpdateView):
    template_name = "core/profile/profile_update.html"
    model = user_models.ProfileModel
    form_class = user_form.ProfileForm


class ProfileDetailView(views.TemplateView):
    template_name = "core/profile/profile_detail.html"
    model = user_models.ProfileModel
    context_object_name = "profile"
