from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from learnings.models import Course, Lesson
from learnings.permissions import IsModerator
from learnings.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwnerOrStaff


# Create your views here.

# ------Контроллеры курсов------

class CourseViewSet(ModelViewSet):
    """CRUD для модели курсов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Разделение прав доступа для курсов"""

        user = self.request.user

        # Создание курса
        if self.action == "create":
            if (
                user.is_authenticated
                and user.groups.filter(name="moderators").exists()
            ):
                raise PermissionDenied(
                    "Модераторам запрещено создавать новые курсы."
                )
            return [IsAuthenticated()]

        # Просмотр списка курсов
        if self.action == "list":
            return [IsAuthenticated(), IsModerator()]

        # Просмотр/обновление/частичное обновление курса
        if self.action in ["retrieve", "update", "partial_update"]:

            user = self.request.user

            if (
                user.is_authenticated
                and user.groups.filter(name="moderators").exists()
            ):
                return [IsAuthenticated()]
            # Если это обычный пользователь - проверка на owner
            return [IsAuthenticated(), IsOwnerOrStaff()]

        # Удаление курса
        if self.action == "destroy":
            if (
                user.is_authenticated
                and user.groups.filter(name="moderators").exists()
            ):
                return PermissionDenied("Модераторам запрещено удалять курсы.")
            # Пользователь может удалять только свой курс
            return [IsAuthenticated(), IsOwnerOrStaff()]

        # По умолчанию
        return [IsAuthenticated()]

# ------Контроллеры уроков------

class LessonCreateAPIView(CreateAPIView):
    """Создание урока (POST)"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonListAPIView(ListAPIView):
    """Просмотр списка уроков (GET)"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsModerator]


class LessonRetrieveAPIView(RetrieveAPIView):
    """Просмотр одного урока (GET)"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff | IsModerator]


class LessonUpdateAPIView(UpdateAPIView):
    """Редактирование урока (PUT/PATCH)"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока (DELETE)"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
