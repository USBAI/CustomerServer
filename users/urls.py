from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('login_authorizer/', views.login_authorizer, name='register_user'),
    path('get-user-details/', views.get_user_details, name='get_user_details'),
]
