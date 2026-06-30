import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course_title):
    """Создание продукта в Stripe. Возвращает JSON-словарь."""
    product = stripe.Product.create(name=course_title)
    return {
        "id": product.id,
        "name": product.name
    }


def create_stripe_price(product_id, amount):
    """Создание цены в Stripe (цена умножается на 100)."""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100), # Цены при передаче в Strip указываются в копейках
        currency="usd",
    )
    return {
        "id": price.id,
        "unit_amount": price.unit_amount
    }

def retrieve_stripe_session(session_id):
    """Обращение к Session Retrieve для проверки статуса платежа"""
    session = stripe.Checkout.Session.retrieve(session_id)
    return {
        "id": session.id,
        "payment_status": session.payment_status, # 'paid', 'unpaid', 'no_payment_required'
        "status": session.status # 'open', 'complete', 'expired'
    }