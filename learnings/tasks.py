from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from learnings.models import Course, Subscription


@shared_task
def send_course_update_emails(course_id):
    """Фоновая задача для отправки писем всем подписчикам обновленного курса"""
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return f"Курс с ID {course_id} не найден."

    # Находим все подписки на данный курс и оптимизируем запрос через select_related
    subscriptions = Subscription.objects.filter(course=course).select_related("user")

    # Собираем список email-адресов подписчиков
    recipient_list = [sub.user.email for sub in subscriptions if sub.user and sub.user.email]

    if not recipient_list:
        return f"У курса '{course.title}' нет активных подписчиков."

    subject = f"Обновление материалов курса: {course.title}"
    message = (
        f"Здравствуйте!\n\n"
        f"Материалы курса '{course.title}' обновлены. "
        f"Зайдите на платформу, чтобы изучить новые уроки!"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return f"Письмо об обновлении курса '{course.title}' успешно отправлено {len(recipient_list)} пользователям."
