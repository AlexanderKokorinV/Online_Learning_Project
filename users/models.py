from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import UserManager

# Create your models here.


class User(AbstractBaseUser):
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
