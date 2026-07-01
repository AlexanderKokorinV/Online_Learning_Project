from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    """Регистрация кастомной модели пользователя в админке"""

    list_display = ["id", "email", "phone_number", "city", "is_staff", "is_active"]

    search_fields = ["email", "phone_number", "city"]

    list_filter = ["is_staff", "is_active", "is_superuser", "groups"]
