from django.urls import path
from . import views

urlpatterns = [
    path('usbai_api/', views.usbai_django_get, name='usbai_django_get'),
]
