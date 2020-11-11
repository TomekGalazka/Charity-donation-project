from django.shortcuts import render
from django.views import View


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'auth_ex/register.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'auth_ex/login.html')


