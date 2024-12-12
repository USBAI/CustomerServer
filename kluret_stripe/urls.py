from django.urls import path
from .views import create_payment_intent, confirm_payment

urlpatterns = [
    path('create-payment-intent/', create_payment_intent, name='create-payment-intent'),
    path('confirm-payment/', confirm_payment, name='confirm-payment'),
]
