from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.register_user, name='register_user'),
    path('login_authorizer/', views.login_authorizer, name='register_user'),

    
    # Add more URLs as needed for your app
]
