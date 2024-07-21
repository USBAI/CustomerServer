import os
import django_heroku
import dj_database_url
from pathlib import Path

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# STRIPE_SECRET_KEY = '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'
# STRIPE_PUBLISHABLE_KEY = 'pk_live_51PRfSZCZLHzBAOdTZTnLqhcUrEIk9vWY9zfnlbh51HiHf3SnRfQ6gUSlZbqhF9BwLmM3QxPGwydIbwAllriqQ4OR00vOKxMn4g'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2j7)5+p0zz&d8#5bbg%&cj299)ovbcu%ba2zbtzumd&(tq-%l+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# CORS_ALLOW_ALL_ORIGINS = True

# account_sid = "ACe45bb8f68bb97440e3183def3e1d8f9d"
# auth_token = "c04ac813ef4d3d48e809237ebc748830"
# twilio_number = "+13343263823"
# openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"

# TWILIO_ACCOUNT_SID = 'ACe45bb8f68bb97440e3183def3e1d8f9d'
# TWILIO_AUTH_TOKEN = 'c04ac813ef4d3d48e809237ebc748830'
# TWILIO_PHONE_NUMBER = '+13343263823'
# openai.api_key = "sk-proj-Q1JLGoe7A3rRoZaqyUh9T3BlbkFJv7YuuWTvZccPiUAyp9Ji"

# Application definition

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
    'kluret_engine',
    'kluret_user_id',
    'UserCart',
    'Notify',
    'kluret_stripe',
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
#https://id.heroku.com/account/accept/15390462/4aefea38e7cca2eaadd9864420519135
#7m_VTuNH$zJx%GC
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://usbai.org",
    "https://webenginegptai-f6919d4667cb.herokuapp.com",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://usbai.org",
    "https://webenginegptai-f6919d4667cb.herokuapp.com",
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

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

django_heroku.settings(locals())
