from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def block_inactive_users():
    """Периодическая задача Celery-Beat:
    Находит пользователей, которые не заходили в систему более 1 месяца (30 дней),
    и блокирует их, выставляя флаг is_active = False.
    """
    now = timezone.now()
    one_month_ago = now - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        is_superuser=False,
        last_login__lt=one_month_ago,
    )

    count_inactive_users = inactive_users.count()

    if count_inactive_users > 0:
        # Обновляем флаг is_active
        inactive_users.update(is_active=False)
        return f"Успешно заблокировано неактивных пользователей: {count_inactive_users}."
