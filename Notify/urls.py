from django.urls import path
from .views import EmailListCreate, VisitorCreate

urlpatterns = [
    path('api/emails/', EmailListCreate.as_view(), name='email-list-create'),
    path('api/visitors/', VisitorCreate.as_view(), name='visitor-create'),
]
