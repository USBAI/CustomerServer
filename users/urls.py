from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('get_users_list/', views.get_all_users_emails, name='get_all_users_emails'),
    path('login_authorizer/', views.login_authorizer, name='register_user'),
    path('get-user-details/', views.get_user_details, name='get_user_details'),
]
