from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import login, logout, mixins, authenticate # import des fonctions login et authenticate
from django.views.generic import View

# class LoginPageView(View, mixins.LoginRequiredMixin):
#     template_name = 'authentication/login.html'
#     form_class = forms.LoginForm

#     def get(self, request):
#         form = self.form_class()
#         message = ''
#         return render(request, self.template_name, 
#                       context={'form': form, 'message': message})

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#         message = 'Identifiants invalides.'
#         return render(request, self.template_name, 
#                       context={'form': form, 'message': message})

# def logout_user(request):
#     logout(request)
#     return redirect('login')