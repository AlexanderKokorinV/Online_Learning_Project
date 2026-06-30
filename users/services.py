import stripe
from django.conf import settings

stripe_client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)


def create_stripe_product(course_title):
    """Создание продукта в Stripe. Возвращает JSON-словарь."""

    product = stripe_client.products.create(
        params={
            "name": course_title,
        }
    )
    return {"id": product.id, "name": product.name}


def create_stripe_price(product_id, amount):
    """Создание цены в Stripe (цена умножается на 100)."""

    price = stripe_client.prices.create(
        params={
            "product": product_id,
            "unit_amount": int(amount * 100),  # Переводим в копейки/центы
            "currency": "usd",
        }
    )
    return {"id": price.id, "unit_amount": price.unit_amount}


def create_stripe_session(price_id):
    """Создание платежной сессии Checkout для получения ссылки на оплату."""
    session = stripe_client.checkout.sessions.create(
        params={
            "success_url": "http://127.0.0.1:8000/learnings/courses/",
            "line_items": [{"price": price_id, "quantity": 1}],
            "mode": "payment",
        }
    )
    return {"id": session.id, "url": session.url, "status": session.status}


def retrieve_stripe_session(session_id):
    """Обращение к Session Retrieve для проверки статуса платежа"""
    session = stripe_client.checkout.sessions.retrieve(session_id)
    return {"id": session.id, "payment_status": session.payment_status, "status": session.status}
