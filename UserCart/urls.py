from django.urls import path
from .views import *

urlpatterns = [
    path('user-cart/', UserCartView.as_view(), name='user-cart'),
    path('all_carts/', AdminCartView.as_view(), name='AdminCartView'),
]
