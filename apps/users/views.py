import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import LoginForm, RegisterForm, SupportForm
from .models import User


class CustomLoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy("home"))
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(
                self.request,
                f"User credentials do not exist. Please double check and try again.",
            )
            return HttpResponseRedirect(reverse_lazy("login"))


class CustomLogoutView(LogoutView):
    def get_next_page(self):
        next_page = super().get_next_page()
        messages.success(self.request, "You have successfully logged out!")
        return next_page


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        username = email.split("@")[0] + str(random.randint(1, 999))
        password = form.cleaned_data["password1"]

        user = User.objects.create_user(
            email,
            username,
            password,
        )
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request,
            "You have successfully registered your account. Please login now to continue.",
        )
        return super().get_success_url()


class SupportView(CreateView):
    form_class = SupportForm
    template_name = "users/support.html"
    success_url = reverse_lazy("support")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_tab"] = "support"
        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            "We have received your support message and will respond as soon as possible.",
            extra_tags="success",
        )
        return super().form_valid(form)
