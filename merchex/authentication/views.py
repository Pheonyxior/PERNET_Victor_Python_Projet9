from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import login, logout, mixins, authenticate # import des fonctions login et authenticate
from django.views.generic import View
from django.conf import settings

from . import forms


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})