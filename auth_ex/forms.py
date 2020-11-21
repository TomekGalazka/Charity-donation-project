from django import forms
from django.core.exceptions import ValidationError

from .models import User


class RegisterUserForm(forms.Form):
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.EmailField(widget=forms.EmailInput, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    repeat_password = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')

    first_name.widget.attrs.update({'class': 'form-group form-group--buttons'})
    last_name.widget.attrs.update({'class': 'form-group form-group--buttons'})
    email.widget.attrs.update({'class': 'form-group form-group--buttons'})
    password.widget.attrs.update({'class': 'form-group form-group--buttons'})
    repeat_password.widget.attrs.update({'class': 'form-group form-group--buttons'})

    def clean(self):
        """
        Overwrite clean method to check if there are any errors.
        :return: ValidationError, if there is any.
        """
        cleaned_data = super().clean()
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        email = cleaned_data['email']
        password = cleaned_data['password']
        repeat_password = cleaned_data['repeat_password']

        users = User.objects.all()

        if password != repeat_password:
            raise ValidationError('Your password does not match. Please repeat the password correctly.')

        for user in users:
            if email == user.email:
                raise ValidationError('This user already exists. Please choose another name.')

        if '@' and '.' not in email:
            raise ValidationError('Please provide a valid e-mail address.')

