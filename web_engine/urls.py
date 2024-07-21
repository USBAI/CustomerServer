# products/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/product/', views.get_product, name='get_product'),
]
