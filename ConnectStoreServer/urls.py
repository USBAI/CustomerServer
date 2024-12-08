from django.urls import path
from . import views 

urlpatterns = [
    path('get_store_info/', views.get_store_info, name='get_store_info'),  # Map to get_store_info view
    path('save_store_info/', views.save_store_info, name='save_store_info'),  # Map to get_store_info view
    path('save_customer/', views.save_customer, name='save_customer'),  # Map to get_store_info view
    path('save_order/', views.save_order, name='save_order'),  # Map to get_store_info view
]