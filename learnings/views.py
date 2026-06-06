from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from learnings.models import Course, Lesson
from learnings.permissions import IsModerator
from learnings.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner


# Create your views here.

# ------Контроллеры курсов------

class CourseViewSet(ModelViewSet):
    """CRUD для модели курсов"""

    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        if user.is_staff or user.groups.filter(name="moderators").exists():
            return Course.objects.prefetch_related("lessons").all()
        return Course.objects.filter(user=user).prefetch_related("lessons")

    def get_permissions(self):

        user = self.request.user

        # Создание курса (POST)
        if self.action == "create":
            # Авторизован и не модератор
            if user.is_authenticated and user.groups.filter(name="moderators").exists():
                raise PermissionDenied("Модераторам запрещено создавать новые курсы.")
            return [IsAuthenticated()]

        # Просмотр списка курсов (GET)
        if self.action == "list":
            return [IsAuthenticated()]

        # Удаление курса (DELETE)
        if self.action == "destroy":
            # Удалять может только владелец
            if user.is_authenticated and user.groups.filter(name="moderators").exists():
                raise PermissionDenied("Модераторам запрещено удалять курсы.")
            return [IsAuthenticated()]

        # По умолчанию (включает retrieve, update, partial_update)
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Автоматически назначает автора курса при создании"""
        serializer.save(user=self.request.user)


# ------Контроллеры уроков------

class LessonCreateAPIView(CreateAPIView):
    """Создание урока (POST). Недоступно модераторам"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonListAPIView(ListAPIView):
    """Просмотр списка уроков (GET). Либо владелец, либо модератор"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        """Модераторы видят все уроки, пользователи - только свои"""
        user = self.request.user

        if not user.is_authenticated:
            return Lesson.objects.none()

        if user.is_staff or user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(user=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """Просмотр одного урока (GET). Авторизован и модератор либо владелец"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    """Редактирование урока (PUT/PATCH). Авторизован и либо модератор, либо владелец"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока (DELETE). Доступ только владельцам"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]
