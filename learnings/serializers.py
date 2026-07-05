from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from learnings.models import Course, Lesson, Subscription
from learnings.validators import YoutubeOnlyValidator


class LessonSerializer(ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YoutubeOnlyValidator(field="link_to_video"), YoutubeOnlyValidator(field="description")]


class CourseSerializer(ModelSerializer):
    """Сериализатор для курсов"""

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        """Метод подсчитывает количество уроков в курсе"""
        return instance.lessons.all().count()

    def get_is_subscribed(self, instance):
        """Метод определяет, подписан ли текущий пользователь на данный курс"""

        request = self.context.get("request")

        if not request or not request.user or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(user=request.user, course=instance).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview_image",
            "description",
            "user",
            "lessons",
            "lessons_count",
            "is_subscribed",
        )
        read_only_fields = ("user",)
        validators = [YoutubeOnlyValidator(field="description")]


class SubscriptionSerializer(Serializer):
    """Сериализатор для управления подпиской"""

    class Meta:
        model = Subscription
        fields = ("course",)


class SubscriptionMessageSerializer(Serializer):
    """Вспомогательный сериализатор для корректного отображения
    JSON-ответа подписки в Swagger"""

    message = serializers.CharField(default="Подписка добавлена")
