# kluret_stripe/urls.py
from django.urls import path
from .views import CollectDataView

urlpatterns = [
    path('collect-data/', CollectDataView.as_view(), name='collect-data'),
]
