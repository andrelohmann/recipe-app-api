"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from os import getenv, environ, path
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Dotenv
dotenv_file = BASE_DIR / '.env.local'
if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_SECRET_KEY', get_random_secret_key())
# SECRET_KEY = 'django-insecure-5gyn98!dh1_)^hjt2%s_72@1w8e-81@%jm-#16f*aeu9iid^b+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # uncommented, when sessions will be stored in redis
    #'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'core',
    'rest_framework',
    # 'rest_framework.authtoken',
    'drf_spectacular',
    # 'user_auth_token',
    'djoser',
    'authentication',
    'django_bootstrap5',
    'web',
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

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DB_NAME'),
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PASS'),
        'HOST': environ.get('DB_HOST'),
        'PORT': environ.get('DB_PORT'),
        'CONN_MAX_AGE': 60,
    }
}

# REDIS CACHE
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": environ.get('REDIS_LOCATION'),
    }
}
SESSION_CACHE_ALIAS = "default"
# If data should be stored both in cache and db
#SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
# of course django.contrib.sessions needs to be added then
# Use Cache only
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

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

LANGUAGE_CODE = getenv('LANGUAGE_CODE', 'en-us')

TIME_ZONE = getenv('TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # We have overriden the JWTAuthentication class, to allow token in Cookie
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'authentication.authentication.CustomJWTAuthentication',
    ],
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.IsAuthenticated'
    ],
}

# from datetime import timedelta
SIMPLE_JWT = {
   # "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
   # "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
   'AUTH_HEADER_TYPES': ('JWT',),
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/{uid}/{token}',
    #'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activation/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    #'SERIALIZERS': {},
}

SITE_NAME = "DjangoBongo"

AUTH_COOKIE = 'access'  # name is fixed
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 5  # 5 Minutes, like default settings for token, look at SIMPLE_JWT
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24  # 24 hours, like default settings for token, look at SIMPLE_JWT
AUTH_COOKIE_SECURE = getenv('AUTH_COOKIE_SECURE', 'True') == 'True'  # https on prod, but http = False on dev
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAMESITE =  'None'  # Strict, Lax, None - strict origin must be on same domain - None irgnores origin

CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS', 'http://127.0.0.1:8000,http://localhost:8000').split(',')
CORS_ALLOW_CREDENTIALS = True

SPECTACULAR_SETTINGS = {
    'TITLE': 'BoatSpot API',
    'DESCRIPTION': 'BoatSpot Backend API',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': True,
    # OTHER SETTINGS
}

# MAILPIT Mailserver
if environ.get('EMAIL_HOST') is not None:
    EMAIL_HOST = environ.get('EMAIL_HOST')
if environ.get('EMAIL_PORT') is not None:
    EMAIL_PORT = environ.get('EMAIL_PORT')
if environ.get('EMAIL_HOST_USER') is not None:
    EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
if environ.get('EMAIL_HOST_PASSWORD') is not None:
    EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
if environ.get('EMAIL_USE_TLS') is not None:
    EMAIL_USE_TLS = environ.get('EMAIL_USE_TLS')
if environ.get('EMAIL_USE_SSL') is not None:
    EMAIL_USE_SSL = environ.get('EMAIL_USE_SSL')