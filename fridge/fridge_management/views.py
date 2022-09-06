from django.shortcuts import render
from django.contrib.auth import get_user_model, login, \
    authenticate, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView, ListView, RedirectView
from django.views.generic import FormView, CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserCreateForm, LoginForm

User = get_user_model()


class UserCreateView(FormView):
    template_name = 'fridge/user_create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        User.objects.create_user(
            username=cd['login'],
            password=cd['password1'],
            email=cd['email'],
        )
        return response


class LoginView(FormView):
    template_name = 'fridge/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['login'], password=cd['password'])
        login(self.request, user)
        return response


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
