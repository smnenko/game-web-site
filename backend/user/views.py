from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import LoginForm, SignUpForm
from .models import CustomUser


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return HttpResponseRedirect('/invalid')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('')

        return render(request, 'user/login.html', {'form': LoginForm()})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = CustomUser.objects.filter(username=form.cleaned_data['username'])
            if not username:
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    birth_date=form.cleaned_data['birth_date'],
                )
                return HttpResponseRedirect('/')
        return HttpResponseRedirect('/error')

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, 'user/signup.html', {'form': SignUpForm()})


def log_out(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect('/')


@login_required(login_url='/login')
def profile(request):
    user = CustomUser.objects.filter(username=request.user)[0]
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': timezone.now().year - user.birth_date.year
    }
    return render(request, 'user/profile.html', context=context)


def mymusts(request):
    pass
