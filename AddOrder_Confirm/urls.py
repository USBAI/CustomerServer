from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.add_product_to_db, name='add_product_to_db'),
    path('process-payment/', views.process_payment, name='process_payment'),
]
