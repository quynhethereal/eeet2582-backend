"""
Django settings for eeet2582_backend project.

Generated by 'django-admin startproject' using Django 4.
For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path
import environ
import os

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c$)+36!u&6#6e9gs8^@8=lf$b6+i33dvon12vk7z8c113fb6d-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "eeet2582_backend.apps.Eeet2582Config",
    'corsheaders',
    'drf_yasg',
    'django_celery_results',
    'storages'
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email"
        ],
        "AUTH_PARAMS": {"access_type": "online"}
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

ROOT_URLCONF = 'eeet2582_backend.urls'

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

WSGI_APPLICATION = 'eeet2582_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'eeet2582_backend.authentication.authentication.GoogleOAuth2Authentication'
    ],

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'

}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
CONN_MAX_AGE=None
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_ON_GET = True

STRIPE_WEBHOOK_SECRET = "whsec_o46piscbkWXSeX0EOPkiEG2gbwjBeS3b"
STRIPE_SECRET_KEY = "sk_test_51OPyOTE2WWDOW84JHiEZ8gORgRhFci7J76jZMfTljyz9hRqutP06hvdSwAVwsrrX9ClBO3W8dil3Ur96g3NN3Lay00iQXUtx38"
STRIPE_3MONTH_PRICE_ID = "price_1OQTxQE2WWDOW84JhtZPjyp5"
FRONT_END_DOMAIN = "http://localhost:5173/"

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = 'django-db'


STATIC_URL = 'uploads/'
MEDIA_URL = 'uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploads')

AWS_LOCATION = 'uploads/'

#S3 BUCKETS CONFIG
AWS_ACCESS_KEY_ID = 'AKIASU7NEA7EYYKTRHNG'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'group1-bucket'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_URL_PROTOCOL = 'https'
AWS_S3_USE_SSL = True
AWS_S3_VERIFY = True
MEDIA_URL = f'{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/uploads/'
AWS_S3_FILE_OVERWRITE = False  # (optional: default is True) Set to False if you want to have extra characters appended.
AWS_DEFAULT_ACL = None  # (optional; default is None) which means the file will inherit the bucket’s permission
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'