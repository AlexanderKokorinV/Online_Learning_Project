from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from learnings.models import Course, Lesson, Subscription
from learnings.paginators import CoursePagination, LessonPagination
from learnings.permissions import IsNotModerator, IsOwnerOrModerator
from learnings.serializers import (CourseSerializer, LessonSerializer, SubscriptionMessageSerializer,
                                   SubscriptionSerializer)
from users.permissions import IsOwner

# Create your views here.

# ------Контроллеры курсов------


class CourseViewSet(ModelViewSet):
    """CRUD для модели курсов"""

    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        if user.is_staff or user.groups.filter(name="moderators").exists():
            return Course.objects.prefetch_related("lessons").all()
        return Course.objects.filter(user=user).prefetch_related("lessons")

    def get_permissions(self):

        # Создание курса (POST)
        if self.action == "create":
            # Авторизован и не модератор
            return [IsAuthenticated(), IsNotModerator()]

        # Просмотр списка курсов (GET)
        if self.action == "list":
            return [IsAuthenticated()]

        # Удаление курса (DELETE)
        if self.action == "destroy":
            # Удалять может только владелец
            return [IsAuthenticated(), IsOwner()]

        if self.action in ["update", "partial_update", "retrieve"]:
            return [IsAuthenticated(), IsOwnerOrModerator()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Автоматически назначает автора курса при создании"""
        serializer.save(user=self.request.user)


# ------Контроллеры уроков------


class LessonCreateAPIView(CreateAPIView):
    """Создание урока (POST). Недоступно модераторам"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        """Автоматически назначает автора урока при создании"""
        serializer.save(user=self.request.user)


class LessonListAPIView(ListAPIView):
    """Просмотр списка уроков (GET). Либо владелец, либо модератор"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPagination

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
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(UpdateAPIView):
    """Редактирование урока (PUT/PATCH). Авторизован и либо модератор, либо владелец"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(DestroyAPIView):
    """Удаление урока (DELETE). Доступ только владельцам"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionAPIView(APIView):
    """Эндпоинт для управления подпиской пользователя на курс"""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Управление подпиской на курс",
        description=("Позволяет авторизованному пользователю подписаться или отписаться от обновлений курса."),
        request=SubscriptionSerializer,  # Передаем сериализатор для валидации тела запроса (RequestBody)
        responses={
            200: OpenApiResponse(
                description="Успешное изменение статуса подписки (создание или удаление).",
                response=SubscriptionMessageSerializer,
            ),
            400: OpenApiResponse(description="Невалидные входящие данные."),
            401: OpenApiResponse(description="Пользователь не авторизован."),
            404: OpenApiResponse(description="Указанный курс не найден в базе данных."),
        },
    )
    def post(self, request):

        # Валидируем входящие данные через сериализатор
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user  # получаем пользователя
        course_id = request.data.get("course")  # получаем id курса

        course_item = get_object_or_404(Course, pk=course_id)  # получаем объект курса из базы

        subs_item = Subscription.objects.filter(
            user=user, course=course_item
        )  # получаем объекты подписок по текущему пользователю и курсу

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
            status_code = status.HTTP_200_OK

        # Если подписки нет - создаем ее
        else:
            subs_item = Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
            status_code = status.HTTP_201_CREATED

        # Возвращаем ответ в API
        return Response({"message": message}, status=status_code)
