import os
import django_heroku
import dj_database_url
from pathlib import Path

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2j7)5+p0zz&d8#5bbg%&cj299)ovbcu%ba2zbtzumd&(tq-%l+'
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'endpoints',
    'openai_image',
    'openai_voice',
    'image_host',
    'usbai_django_get',
    'chatbotapi',
    'corsheaders',
    'web_engine',
    'users',
    'kluret_user_id',
    'UserCart',
    'Notify',
    'kluret_stripe',
    'AddCart',
    'Users_Order',
    'Kluretworkflow',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "https://usbai.org",
    'https://www.kluret.se',
    "https://usbai.vercel.app",
    "https://webenginegptai-f6919d4667cb.herokuapp.com",
    "https://webnodes-1ac3b80d6a1c.herokuapp.com",
    "https://usbaiclient-8c59f2a693e9.herokuapp.com",
    "https://webnode-9662dc9a689b.herokuapp.com"
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://usbai.org",
    'https://www.kluret.se',
    "https://usbai.vercel.app",
    "https://webenginegptai-f6919d4667cb.herokuapp.com",
    "https://webnodes-1ac3b80d6a1c.herokuapp.com",
    "https://usbaiclient-8c59f2a693e9.herokuapp.com",
    "https://webnode-9662dc9a689b.herokuapp.com"
]

ROOT_URLCONF = 'usbai_client.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'usbai_client.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_heroku.settings(locals())
