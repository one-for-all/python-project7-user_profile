from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import models
from . import forms


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    try:
        profile = models.UserProfile.objects.get(user=request.user)
    except models.UserProfile.DoesNotExist:
        profile = models.UserProfile()
        profile.user = request.user
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    try:
        profile = models.UserProfile.objects.get(user=request.user)
    except models.UserProfile.DoesNotExist:
        profile = models.UserProfile()
        profile.user = request.user
    form = forms.UserProfileForm(instance=profile,
                                 initial={'email2': profile.email})
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES,
                                     instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated!")
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    form = forms.CustomPasswordChangeForm(request.user)
    if request.method == 'POST':
        form = forms.CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Password Updated!")
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/change_password.html', {'form': form})
