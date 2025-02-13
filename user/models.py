from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
import os
from uuid import uuid4
from allauth.account.models import EmailAddress


class CustomUserManager(BaseUserManager):
    """
    Create and return a regular user with the given email and password.
    """
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(email, password, **extra_fields)
        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
        # Remove Profile.objects.create() from here since signal will handle it
        return user


class CustomUser(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects=CustomUserManager()

    def __str__(self):
        return self.email