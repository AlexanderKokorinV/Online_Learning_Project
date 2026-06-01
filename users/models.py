from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import CustomUserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя с email в качестве username"""

    username = None
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email", help_text="Укажите ваш email")
    phone_number = models.CharField(
        max_length=35, null=True, blank=True, verbose_name="Телефон", help_text="Укажите ваш номер телефона"
    )
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Город", help_text="Укажите ваш город")
    avatar = models.ImageField(
        upload_to="users/avatars/", null=True, blank=True, verbose_name="Аватар", help_text="Подгрузите ваш аватар"
    )

    is_staff = models.BooleanField(default=False, verbose_name="Статус персонала")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_superuser = models.BooleanField(default=False, verbose_name="Статус суперпользователя")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
