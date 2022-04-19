from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.db.models import Value, IntegerField

from .forms import LoginForm, SignUpForm, UserSettingsForm

from user.forms import LoginForm
from user.forms import SignUpForm
from .models import CustomUser


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('games')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        messages.error(self.request, 'No user with the given username or password was found.')
        messages.error(self.request, 'Please enter correct username and password.')
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, *kwargs)


class SignupFormView(FormView):
    form_class = SignUpForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                birth_date=form.cleaned_data['birth_date'],
            )
            return super().form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    def form_invalid(self, form):
        if not form.errors:
            messages.error(
                self.request,
                'The user with this username or email already exists, please enter a different username or email'
            )
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        if request.method == 'GET' and request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))


class ProfileView(LoginRequiredMixin, DetailView, FormView):
    model = CustomUser
    template_name = 'user/profile.html'
    form_class = UserSettingsForm
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return super().get_queryset().annotate(age=Value(
            timezone.now().year - self.request.user.birth_date.year,
            output_field=IntegerField())
        )


class UpdateUserFormView(LoginRequiredMixin, FormView):
    form_class = UserSettingsForm
    success_url = '/profile'

    def form_valid(self, form):
        user = CustomUser.objects.filter(username=self.request.user).first()
        form.save()
        user.avatar = form.instance
        user.save()
        return HttpResponseRedirect(self.success_url)
