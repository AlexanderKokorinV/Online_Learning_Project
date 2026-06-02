import decimal

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils import timezone

from learnings.models import Course, Lesson
from users.models import Payments

User = get_user_model()


class Command(BaseCommand):

    help = "Команда для добавления тестовых платежей в БД"

    def handle(self, *args, **kwargs):
        # Удаляем старые платежи
        Payments.objects.all().delete()

        # Берем существующих в БД пользователей и контент
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("Создайте хотя бы одного пользователя."))
            return

        # Платеж за курс (перевод на счет)
        if course:
            Payments.objects.create(
                user=user,
                payment_date=timezone.now().date(),
                paid_course=course,
                payment_amount=decimal.Decimal("10000.00"),
                payment_type="transfer",
            )
            self.stdout.write(self.style.SUCCESS(f"Создан платеж за курс: {course.title}"))

        if lesson:
            Payments.objects.create(
                user=user,
                payment_date=timezone.now().date(),
                paid_lesson=lesson,
                payment_amount=decimal.Decimal("1000.00"),
                payment_type="cash",
            )
            self.stdout.write(self.style.SUCCESS(f"Создан платеж за урок: {lesson.title}"))

        self.stdout.write(self.style.SUCCESS("База данных платежей успешно заполнена."))
