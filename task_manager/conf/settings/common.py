"""
Django settings for task_manager project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import sys
from typing import Callable

import environ
from django.conf import global_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Callable = environ.Path(__file__) - 4
# apps directory path override
APPS_DIR = os.path.join(BASE_DIR, "task_manager/apps")
sys.path.insert(0, APPS_DIR)

# env file injection
env_file = os.path.join(BASE_DIR, ".env")
env = environ.Env()
env.read_env(env_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=True)

IS_PRODUCTION = env.bool("IS_PRODUCTION", default=False)

ALLOWED_HOSTS = ["*"]

FRONTEND_HOST = env.str("FRONTEND_HOST", default="127.0.0.1/").rstrip("/")

# CORS settingss
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=["http://*.127.0.0.1"],
)
CORS_ORIGIN_ALLOW_ALL = True


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SITE_ID = 1


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

# 3rd party libraries
THIRD_PARTY_APPS = [
    "corsheaders",
    "djoser",
    "django_filters",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
]


LOCAL_APPS = [
    "task_manager.apps.login.apps.LoginConfig",
    "task_manager.apps.tasks.apps.TasksConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "task_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "task_manager.wsgi.application"
AUTH_USER_MODEL = "login.UserAccount"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if IS_PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": env.str("DB_ENGINE"),
            "NAME": env.str("DB_NAME"),  # change in prod
            "USER": env.str("DB_USER"),
            "PASSWORD": env.str("DB_PASSWORD"),
            "HOST": env.str("DB_HOST"),
            "PORT": env.int("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": env.str(
                "DEV_DB_ENGINE", default="django.db.backends.sqlite3"
            ),
            "NAME": env.str("DEV_DB_NAME", default="db.sqlite3"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGES = global_settings.LANGUAGES + [("en-us", "American English")]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"


# email configs
EMAIL_HOST = env.str("EMAIL_HOST", default=None)
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_PORT = env.int("EMAIL_PORT", default=None)
EMAIL_USE_TLS = env.bool("EMAIL_PORT", default=True)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default=None)
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="admin@task.com")


#  restframework
# disable browsable api in production
DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)
if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "task_manager.api.filters.ResultsPagination",
}
CSRF_COOKIE_HTTPONLY = False

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# api auth settings
DJOSER = {
    "SERIALIZERS": {
        "user_create": "task_manager.apps.login.api.v1.serializers.UserAccountCreateSerializer",
        "user": "task_manager.apps.login.api.v1.serializers.UserResponseSerializer",
        "current_user": "task_manager.apps.login.api.v1.serializers.UserResponseSerializer",
    },
    "LOGIN_FIELD": "email",
    "SEND_ACTIVATION_EMAIL": False,
    "PASSWORD_RESET_CONFIRM_URL": "auth/password/reset/{uid}/{token}",
}
