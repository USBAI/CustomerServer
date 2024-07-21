from django.urls import path
from .views import UserCartView

urlpatterns = [
    path('user-cart/', UserCartView.as_view(), name='user-cart'),
]
