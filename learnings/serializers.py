from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from learnings.models import Course, Lesson
from learnings.validators import YoutubeOnlyValidator


class LessonSerializer(ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            YoutubeOnlyValidator(field="link_to_video"),
            YoutubeOnlyValidator(field="description")
        ]


class CourseSerializer(ModelSerializer):
    """Сериализатор для курсов"""

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        return instance.lessons.all().count()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview_image",
            "description",
            "lessons",
            "lessons_count",
        )
        validators = [
            YoutubeOnlyValidator(field="description")
        ]
