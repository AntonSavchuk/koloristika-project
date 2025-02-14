from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth
from django.urls import reverse

from .forms import ProfileForm, UserLoginForm, UserRegistrationForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Home - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        form = ProfileForm(data=request.POST, instance=user, files=request.FILES)

        if 'image' in request.FILES:
            user.image = request.FILES['image']
            user.save()
            return HttpResponseRedirect(reverse('users:profile'))

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': f'Профиль - {request.user}',
        'form': form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))

