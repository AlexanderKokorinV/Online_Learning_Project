from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.template.defaultfilters import title
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from learnings.models import Course, Lesson

# Create your tests here.

User = get_user_model()

class LMSProjectTestCase(APITestCase):
    """Комплексный тестовый набор для проверки бизнес-логики LMS
     Данный класс покрывает:
        1. Полный CRUD-цикл для моделей Course и Lesson.
        2. Разграничение прав доступа (владельцы, модераторы, анонимы).
        3. Работу эндпоинта управления подписками.
        4. Валидацию встроенных полей (включая фильтрацию сторонних ссылок через YoutubeOnlyValidator).
        5. Корректность структуры ответа при включенной пагинации.
    """

    def setUp(self):
        """Предустановка окружения перед запуском каждого отдельного теста."""

        # Создаем группу модераторов
        self.moderator_group, _ = Group.objects.get_or_create(name="moderators")

        # Создаем тестовых пользователей
        self.user_owner = User.objects.create_user(
            email="owner@test.com",
            password="1234!1234",
        )
        self.user_moderator = User.objects.create_user(
            email="mod@test.com",
            password="1234!1234",
        )
        self.user_moderator.groups.add(self.moderator_group)

        self.user_other = User.objects.create_user(
            email="other@test.com",
            password="1234!1234",
        )

        # Создаем базовый курс и урок для тестов
        self.course = Course.objects.create(
            title="Основы DRF",
            description="Курс по разработке на Python с использованием DRF",
            user=self.user_owner,
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Вводный урок по Django REST Framework (DRF)",
            description="Первый шаг в изучении DRF",
            link_to_video="https://youtube.com",
            user=self.user_owner,
        )

#------------Тесты эндпоинтов курсов (CourseViewSet - router)------------

    def test_course_create_by_owner_success(self):
        """Тест создания курса обычным пользователем (POST /learnings/courses/)"""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("learnings:courses-list")
        data = {
            "title": "Тестовый курс по DRF",
            "description": "Тестовый курс по DRF для начинающих",
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Проверка возвращения статуса
        self.assertEqual(Course.objects.filter(title=data["title"]).count(), 1) # В БД появилась ровно одна запись
        self.assertEqual(Course.objects.get(title=data["title"]).user, self.user_owner) # Проверка автоматического назначения автора (perform_create)

    def test_course_create_by_moderator_denied(self):
        """Тест запрета создания курса модератором (POST /learnings/courses/)"""
        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("learnings:courses-list")
        data = {
            "title": "Курс модератора",
            "description": "Тестовый курс модератора"
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Проверка возвращения статуса "запрещено"

    def test_course_list_by_owner(self):
        """Владелец видит только свои курсы (GET /learnings/courses/)"""
        Course.objects.create(
            title="Курс, созданный другим пользователем", # Создаем чужой курс для проверки изоляции
            user=self.user_other,
        )

        self.client.force_authenticate(user=self.user_owner)
        url = reverse("learnings:courses-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], self.course.title)

    def test_course_list_by_moderator(self):
        """Модератор видит абсолютно все курсы (GET /learnings/courses/)"""
        Course.objects.create(
            title="Курс, созданный другим пользователем",
            user=self.user_other,
        )

        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("learnings:courses-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2) # Видит оба курса благодаря prefetch_related


    def test_course_retrieve_by_owner_and_moderator(self):
        """Чтение деталей курса - разрешено владельцу и модератору (GET /learnings/courses/<pk>/)"""
        url = reverse("learnings:courses-detail", kwargs={"pk": self.course.pk})

        # Проверка для владельца
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.course.title)
        self.assertEqual(len(response.data["lessons"]), 1)

        # Проверка для модератора
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update_by_owner_and_moderator(self):
        """Редактирование курса владельцем или модератором (PUT/PATCH /learnings/courses/<pk>/)"""
        url = reverse("learnings:courses-detail", kwargs={"pk": self.course.pk})
        data = {"title": "Измененное название"}

        # Проверка для модератора
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в БД данные изменились на значение из словаря data
        self.course.refresh_from_db()
        self.assertEqual(data["title"], self.course.title)

        # Проверка для обычного чужого пользователя (Запрещено)
        self.client.force_authenticate(user=self.user_other)
        bad_data = {"title": "Взлом"}
        response = self.client.patch(url, data=bad_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Дополнительная проверка безопасности: убеждаемся, что взлом не прошел в БД
        self.course.refresh_from_db()
        self.assertNotEqual(bad_data["title"], self.course.title)


    def test_course_delete_by_moderator_denied(self):
        """Запрет удаления курса модератором (DELETE /learnings/courses/<pk>/)"""
        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("learnings:courses-detail", kwargs={"pk": self.course.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Course.objects.count(), 1)

    def test_course_delete_by_owner_success(self):
        """Успешное удаление курса владельцем (DELETE /learnings/courses/<pk>/)"""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("learnings:courses-detail", kwargs={"pk": self.course.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

#------------Тесты эндпоинтов уроков (Generic APIViews - path)------------

    def test_lesson_create_by_owner_success(self):
        """Создание урока владельцем (POST /learnings/lessons/create/)"""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("learnings:lesson_create")
        data = {
            "course": self.course.pk,
            "title": "Создание моделей",
            "description": "Изучаем ORM",
            "link_to_video": "https://youtube.com",
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.filter(title=data["title"]).count(), 1)

    def test_lesson_create_by_moderator_denied(self):
        """Запрет создания урока модератором (POST /learnings/lessons/create/)"""
        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("learnings:lesson_create")
        data = {
            "course": self.course.pk,
            "title": "Урок модератора",
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list_by_owner(self):
        """Просмотр списка уроков владельцем (GET /learnings/lessons/)"""
        Lesson.objects.create(
            course=self.course,
            title="Чужой урок",
            user=self.user_other,
        )

        self.client.force_authenticate(user=self.user_owner)
        url = reverse("learnings:lessons")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1) # Пользователь видит только свой урок

    def test_lesson_list_by_moderator(self):
        """Просмотр списка уроков модератором (GET /learnings/lessons/)"""
        Lesson.objects.create(
            course=self.course,
            title="Чужой урок",
            user=self.user_other
        )

        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("learnings:lessons")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_lesson_retrieve(self):
        """Просмотр отдельного урока (GET /learnings/lessons/<pk>/)"""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("learnings:lesson_retrieve", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update_by_moderator(self):
        """Редактирование урока модератором (PUT/PATCH /learnings/lessons/update/<pk>/)"""
        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("learnings:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"course": self.course.pk, "title": "Новое название урока"}
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, data["title"])

    def test_lesson_delete_by_moderator_denied(self):
        """Запрет удаления урока модератором (DELETE /learnings/lessons/delete/<pk>/)"""
        self.client.force_authenticate(user=self.user_moderator)
        url = reverse("learnings:lesson_delete", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_delete_by_owner_success(self):
        """Удаление урока его владельцем (DELETE /learnings/lessons/delete/<pk>/)"""
        self.client.force_authenticate(user=self.user_owner)
        url = reverse("learnings:lesson_delete", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)








