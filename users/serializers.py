from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from learnings.serializers import CourseSerializer, LessonSerializer
from users.models import User, Payments


class UserRegisterSerializer(ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    password = serializers.CharField(write_only=True)  # пароль только для записи

    class Meta:
        model = User
        fields = ["id", "email", "password", "phone_number", "city", "avatar"]

    def create(self, validated_data):
        """Метод для хеширования пароля перед сохранением в БД"""
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data["phone_number"],
            city=validated_data["city"],
            avatar=validated_data.get("avatar", None),
        )
        return user


class UserProfileSerializer(ModelSerializer):
    """Сериализатор для профиля пользователя"""

    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "city", "avatar"]
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
