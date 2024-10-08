from django.urls import path
from .views import product_search_tracking

urlpatterns = [
    path('track_search/', product_search_tracking, name='track_search'),
]
