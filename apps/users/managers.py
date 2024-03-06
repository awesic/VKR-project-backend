from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where create user without username
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Почта должна быть заполнена"))
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("У superuser'a должно быть is_staff=True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("У superuser'a должно быть is_superuser=True"))
        return self.create_user(email, password, **extra_fields)
