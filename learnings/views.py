from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from learnings.models import Course, Lesson
from learnings.serializers import CourseSerializer, LessonSerializer

# Create your views here.


class CourseViewSet(ModelViewSet):
    """CRUD для модели курсов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateAPIView(CreateAPIView):
    """Создание урока (POST)"""

    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    """Просмотр списка уроков (GET)"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """Просмотр одного урока (GET)"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """Редактирование урока (PUT/PATCH)"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока (DELETE)"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
