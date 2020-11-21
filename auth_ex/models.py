from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.db import models


class UserManager(UserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager".
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Email must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have 'is_staff'=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have 'is_superuser=True'.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    # first_name = models.CharField(blank=True, max_length=30, verbose_name='first name')
    # last_name = models.CharField(blank=True, max_length=150, verbose_name='last name')
    # is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this site.')
    # is_active = models.BooleanField(
    #     default=True,
    #     help_text='Designates whether this user should be treated as active.'
    #               'Unselect this instead of deleting accounts.'
    # )
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



