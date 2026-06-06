from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from learnings.serializers import CourseSerializer, LessonSerializer
from users.models import Payments, User

User = get_user_model()

class UserRegisterSerializer(ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    password = serializers.CharField(write_only=True, min_length=8)  # пароль только для записи

    class Meta:
        model = User
        fields = ["id", "email", "password", "phone_number", "city", "avatar"]
        extra_kwargs = {
            "email": {
                "error_messages": {
                    "unique": "Пользователь с таким Email уже зарегистрирован в системе."
                }
            }
        }


    def create(self, validated_data):
        """Метод создания с хешированием пароля перед сохранением в БД"""
        try:
            user = User.objects.create_user(
                email=validated_data.get("email"),
                password=validated_data.get("password"),
                phone_number=validated_data.get("phone_number", None),
                city=validated_data.get("city", None),
                avatar=validated_data.get("avatar", None),
            )
            return user

        except IntegrityError as e:
            raise ValidationError(
                {
                    "error": f"Не удалось завершить регистрацию из-за системной ошибки: {str(e)}"
                }
            )



class UserPaymentsHystorySerializer(ModelSerializer):
    """Сериализатор для истории платежей пользователя"""

    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payments
        fields = (
            "id",
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "payment_amount",
            "payment_type",
        )


class UserProfileSerializer(ModelSerializer):
    """Сериализатор для профиля пользователя"""

    payments_hystory = UserPaymentsHystorySerializer(source="payments", many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "city",
            "avatar",
            "payments_hystory",
        )
        read_only_fields = ["email"]  # email доступен только для чтения


class PaymentsSerializer(ModelSerializer):
    """Сериализатор для списка платежей"""

    user = UserProfileSerializer(read_only=True)
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payments
        fields = (
            "id",
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "payment_amount",
            "payment_type",
        )

class PaymentsCreateSerializer(ModelSerializer):
    """Сериализатор для создания платежей"""
    class Meta:
        model = Payments
        fields = "__all__"