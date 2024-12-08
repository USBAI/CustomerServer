from django.urls import path
from . import views  # Import views from the app

urlpatterns = [
    path('get_store_info/', views.get_store_info, name='get_store_info'),  # Map to get_store_info view
]
