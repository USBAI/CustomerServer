from django.urls import path
from .views import create_payment_and_poll_status

urlpatterns = [
    # No need for 'as_view()' here because it's a function-based view
    path('collect-data/', create_payment_and_poll_status, name='collect-data'),
]
