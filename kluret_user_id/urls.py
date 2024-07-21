from django.urls import path
from .views import UserProductView

urlpatterns = [
    path('user-product/', UserProductView.as_view(), name='user-product'),
]
