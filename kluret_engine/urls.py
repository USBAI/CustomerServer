from django.urls import path
from .views import zalando, update_pipeline

urlpatterns = [
    path('zalando/', zalando, name='zalando'),
    path('update_pipeline/', update_pipeline, name='update_pipeline'),
]
