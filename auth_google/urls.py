# urls.py
from django.urls import path
from .views import google_register

urlpatterns = [
    path('google_register/', google_register, name='google_register'),
]
