from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import RegisterUserForm
from .models import User


class RegisterView(FormView):
    template_name = 'auth_ex/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        User.objects.create_user(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        return super().form_valid(form)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'auth_ex/login.html')


