from django.urls import path
from . import views
from .views import handle_post_request


urlpatterns = [
    path('imagerecognition/', views.image_recognition, name='image'),
    path('handle_post/', handle_post_request, name='handle_post'),
]
