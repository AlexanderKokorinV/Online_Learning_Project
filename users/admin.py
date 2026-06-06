from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model

# Register your models here.
User = get_user_model()


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    """Регистрация кастомной модели пользователя в админке"""

    list_display = ["id", "email", "phone_number", "city", "is_staff", "is_active"]

    search_fields = ["email", "phone_number", "city"]

    list_filter = ["is_staff", "is_active", "is_superuser", "groups"]
