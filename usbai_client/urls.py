# main urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/', include('endpoints.urls')),
    path('api/', include('image_host.urls')),
    path('usbai_vision/', include('usbai_django_get.urls')),
    path('image_recognition/', include('openai_image.urls')),
    path('openai_image/', include('openai_image.urls')),
    path('api/', include('chatbotapi.urls')), 
    path('products/', include('web_engine.urls')),
    path('users/', include('users.urls')),
    path('api/', include('kluret_user_id.urls')),
    path('getcart/', include('UserCart.urls')),
    path('notify/', include('Notify.urls')),
    path('kluret_stripe/', include('kluret_stripe.urls')),
    path('addcart/', include('AddCart.urls')), 
    path('users_order/', include('Users_Order.urls')),
    path('kluretworkflow/', include('Kluretworkflow.urls')),
    path('searchengine_tracking/', include('searchengine_tracting.urls')),
    path('auth_google/', include('auth_google.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
