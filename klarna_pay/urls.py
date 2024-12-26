from django.urls import path
from . import views  # Assuming the views are in the same app

urlpatterns = [
    path('create-klarna-payment-intent/', views.create_klarna_payment_intent, name='create_klarna_payment_intent'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
]
