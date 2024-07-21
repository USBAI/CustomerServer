from django.urls import path
from .views import handle_request

urlpatterns = [
    path('handle-request/', handle_request, name='handle_request'),
]