from django.db import models

from config import settings


# Create your models here.


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=150, verbose_name="Курс", help_text="Введите название курса")
    preview_image = models.ImageField(
        upload_to="learnings/course_previews/",
        verbose_name="Превью",
        help_text="Подгрузите превью курса",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Описание", help_text="Добавьте описание курса", null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока"""

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс", help_text="Выберите курс"
    )
    title = models.CharField(max_length=150, verbose_name="Урок", help_text="Введите название урока")
    preview_image = models.ImageField(
        upload_to="learnings/lesson_previews/",
        verbose_name="Превью",
        help_text="Добавьте превью урока",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Описание", help_text="Добавьте описание урока", null=True, blank=True)
    link_to_video = models.URLField(
        max_length=500,
        verbose_name="Ссылка на видео урока",
        help_text="Добавьте ссылку на видео урока",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]

    def __str__(self):
        return self.title
