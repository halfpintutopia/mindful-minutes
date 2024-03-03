import os
from pathlib import Path

import dj_database_url
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

SECRET_KEY = os.environ.get("SECRET_KEY", "")

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "mindful-minutes-f992c8465405.herokuapp.com",
]

if not DEBUG:
    SECURE_HSTS_SECONDS = 3600
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_REFERRER_POLICY = "same-origin"

    REST_FRAMEWORK = {
        "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)
    }

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary",
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "rest_framework",
    "drf_yasg",
    "appointments",
    "emotions",
    "gratitude_entries",
    "ideas",
    "improvements",
    "knowledge_entries",
    "notes",
    "targets",
    "user_settings",
    "users",
    "wins",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mindfulminutes.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
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

WSGI_APPLICATION = "mindfulminutes.wsgi.application"

if not DEBUG:
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL is not None:
        DATABASES = {
            "default": dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            ),
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get(
                "SQL_ENGINE", "django.db.backends.sqlite3"
            ),
            "NAME": os.environ.get(
                "SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")
            ),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-uk"

TIME_ZONE = "Europe/Zurich"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_STORAGE = (
    "cloudinary_storage.storage.StaticHashedCloudinaryStorage"
)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUD_NAME"),
    "API_KEY": os.environ.get("API_KEY"),
    "API_SECRET": os.environ.get("API_SECRET"),
}

MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_FORMS = {"signup": "users.forms.CustomSignupForm"}

SOCIALACCOUNT_FORMS = {
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
    "signup": "allauth.socialaccount.forms.SignupForm",
}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [
            {
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "secret": os.environ.get("GOOGLE_SECRET"),
                "key": "",
            },
        ],
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

if DEBUG:
    SECURE_SSL_REDIRECT = False

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CSRF_TRUSTED_ORIGINS = ["https://mindful-minutes-f992c8465405.herokuapp.com"]
