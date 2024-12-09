from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('add_user_info/', views.add_user_info, name='add_user_info'),
]
