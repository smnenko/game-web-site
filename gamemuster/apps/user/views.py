import os
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.core.files.uploadedfile import TemporaryUploadedFile
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

from core.views import MultipleFormsView
from user.models import Avatar, CustomUser
from user.forms import AvatarUpdateForm, LoginForm, SignUpForm, ProfileUpdateForm, UserUpdateForm


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


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user/profile.html'

    def get_queryset(self):
        return super().get_queryset().annotate(age=Value(
            timezone.now().year - self.request.user.birth_date.year,
            output_field=IntegerField())
        )


class UserUpdateFormView(LoginRequiredMixin, MultipleFormsView):
    forms_classes = [AvatarUpdateForm, ProfileUpdateForm, UserUpdateForm]
    template_name = 'user/profile_settings.html'

    def get_initial(self):
        return {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email
        }
    
    def form_valid(self, form):
        if isinstance(form, UserUpdateForm):
            if self.request.user.check_password(form.cleaned_data['password_confirm']):
                self.request.user.email = form.cleaned_data['email']
                self.request.user.save(update_fields=('email',))
                return super().form_valid(form)
            messages.error(self.request, 'Please enter valid password')
            return self.form_invalid(form)
        elif isinstance(form, AvatarUpdateForm):
            avatar_old = Avatar.objects.get(customuser=self.request.user)
            avatar = Avatar.objects.create(avatar=form.cleaned_data['avatar'])
            self.request.user.avatar = avatar
            self.request.user.save(update_fields=('avatar',))

            if avatar_old.id != 1:
                os.remove(Path().resolve().joinpath('deploy', 'media', str(avatar_old.avatar)))
                avatar_old.delete()
            return super().form_valid(form)
        elif isinstance(form, ProfileUpdateForm):
            fields = ('first_name', 'last_name')
            for field in fields:
                setattr(self.request.user, field, form.cleaned_data[field])
            self.request.user.save(update_fields=fields)
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})
