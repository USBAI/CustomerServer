from django.urls import path
from .views import get_all_user_names, get_tasks_from_storage

urlpatterns = [
    path('getusernames/', get_all_user_names, name='get_all_user_names'),
    path('get_tasks/', get_tasks_from_storage, name='get_tasks_from_storage'),
]
