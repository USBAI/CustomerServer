from django.urls import path
from .views import add_to_cart, get_cart

urlpatterns = [
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('getcart/', get_cart, name='add-to-cart'),
]
