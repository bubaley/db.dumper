import datetime
import sys
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = env.bool('DEBUG', True)
TESTING = sys.argv[1:2] == ['test']
SETTINGS_MODULE = 'core.settings.dev' if DEBUG else 'core.settings.prod'
SECRET_KEY = env.str('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOST', default=['*'])
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=['http://localhost:5173'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'user',
    'config',
    'workflow',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

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

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

if env.str('SQL_ENGINE', None):
    DATABASES = {
        'default': {
            'ENGINE': env.str('SQL_ENGINE'),
            'NAME': env.str('SQL_DATABASE'),
            'USER': env.str('SQL_USER'),
            'PASSWORD': env.str('SQL_PASSWORD'),
            'HOST': env.str('SQL_HOST'),
            'PORT': env.str('SQL_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'data' / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False

STATICFILES_DIRS = [Path(BASE_DIR / 'data' / 'static')]
STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR / 'data' / 'media'
MEDIA_URL = 'media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_PAGINATION_CLASS': 'core.utils.base_pagination.BasePagination',
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'UPDATE_LAST_LOGIN': True,
}

AUTH_USER_MODEL = 'user.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'app_cache',
        'TIMEOUT': 604800,
    }
}

CELERY_BROKER_URL = env.str('BROKER_URL', None)
CELERY_BACKEND_URL = env.str('CELERY_BACKEND_URL', None)
CELERY_BEAT_ENABLED = env.str('CELERY_BEAT_ENABLED', False)

# --- CUSTOM_SETTINGS ---
CRYPTO_FIELD_KEY = env.str('CRYPTO_FIELD_KEY')
