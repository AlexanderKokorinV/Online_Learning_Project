from rest_framework.serializers import ModelSerializer

from learnings.models import Course, Lesson



class LessonSerializer(ModelSerializer):
    """Сериализатор для уроков"""
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор для курсов"""
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"