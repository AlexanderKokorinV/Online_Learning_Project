from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from config import settings
from learnings.models import Course, Lesson
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

class Payments(models.Model):
    """Модель платежей"""

    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )

    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")

    paid_course = models.ForeignKey(
        Course,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )

    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
        help_text="Сумма оплаты")

    payment_type = models.CharField(
        max_length=100,
        choices=PAYMENT_METHODS,
        verbose_name="Способ оплаты",
        help_text="Способ оплаты: наличные или перевод на счет.",
    )

    class Meta:
        verbose_name="Платеж"
        verbose_name_plural="Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Платеж от {self.user.email} на сумму {self.payment_amount}"