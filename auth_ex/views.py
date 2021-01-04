from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import LoginUserForm, RegisterUserForm
from .models import User


class RegisterView(FormView):
    """
    View allows to register new user.
    """
    template_name = 'auth_ex/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('auth_ex:login')

    def form_valid(self, form):
        User.objects.create_user(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        return super().form_valid(form)


class LoginView(FormView):
    """
    View allows to log in existing user.
    """
    template_name = 'auth_ex/login.html'
    form_class = LoginUserForm

    def form_valid(self, form):
        """
        Authenticates user. If user is authenticated redirects to landing page.
        If not, redirects to register new user page.
        """
        request = self.request
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(request, user)
        else:
            return redirect(reverse_lazy('auth_ex:register'))
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('landing_page'))


class LogoutView(View):
    """
    Logs out current user. Redirects to main page.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('landing_page'))

