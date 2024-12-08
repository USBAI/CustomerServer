from django.urls import path
from .views import EmailListCreate, VisitorCreate, SiteTrafficList

urlpatterns = [
    path('api/emails/', EmailListCreate.as_view(), name='email-list-create'),
    path('api/visitors/', VisitorCreate.as_view(), name='visitor-create'),
    path('api/sitetraffic/', SiteTrafficList.as_view(), name='site-traffic-list'),
]
