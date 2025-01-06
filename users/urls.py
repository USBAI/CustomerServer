from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('get_users_list/', views.get_all_users_emails, name='get_all_users_emails'),
    path('login_authorizer/', views.login_authorizer, name='register_user'),
    path('get-user-details/', views.get_user_details, name='get_user_details'),
    path('get-shipping-info/', views.get_shipping_info, name='get_shipping_info'),
    path('post-shipping-info/', views.post_shipping_info, name='post_shipping_info'),
    path('update-shipping-info/', views.update_shipping_info, name='update_shipping_info'),
]
