"""
Django settings for mindfulminutes project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()

if ENV_FILE:
	load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Disable the Browsable API in production
if not DEBUG:
	REST_FRAMEWORK = {
		"DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)
	}

if not DEBUG:
	# Instruct web browser to remember the HSTS policy for 3600 secs (1
	# hour), in this time if the user tries to access the website using HTTP
	# the browser automatically converts it to HTTPS - mitigates the risk of
	# man-in-the-middle attacks that can intercept and modify HTTP requests.
	SECURE_HSTS_SECONDS = 3600
	# Prevents browsers from interpreting files as a different MIME type
	# than declared by the server
	SECURE_CONTENT_TYPE_NOSNIFF = True
	# Prevents Cross-Site-Scripting (XSS) protections, by using sanitising
	# and filtering user input
	SECURE_BROWSER_XSS_FILTER = True
	# Redirects HTTP to HTTPs. All communication between client and server
	# is encrypted and secure
	SECURE_SSL_REDIRECT = True
	# Only send cookie over HTTPS connection
	SESSION_COOKIE_SECURE = True
	# Only send Cross-Site-Request-Forgery (CSRF) over HTTPS connection
	CSRF_COOKIE_SECURE = True
	# Prevents the site from being embedded in any frame, protect from
	# clickjacking attacks
	X_FRAME_OPTIONS = "DENY"
	# Ensures the HSTS policy is applied to the main domain and its
	# subdomains - enhancing security
	SECURE_HSTS_INCLUDE_SUBDOMAINS = True
	# Allows the website to be included in the HSTS Preload list. Ensures
	# that the browser is always accessible via HTTPS (from first visit)
	SECURE_HSTS_PRELOAD = True
	# Allows the app to detect the original protocol used by the client
	# before it reached the proxy (useful when Django app is deployed behind
	# reverse proxy (e.g. Nginx / Apache)
	SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
	# `same-origin` ensures the referrer information is only sent when
	# navigating to the same origin, helping protect user privacy
	SECURE_REFERRER_POLICY = "same-origin"

# Application definition
INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"cloudinary_storage",
	"django.contrib.staticfiles",
	"allauth",
	"allauth.account",
	"allauth.socialaccount",
	'allauth.socialaccount.providers.google',
	"cloudinary",
	"ckeditor",
	"rest_framework",
	"drf_yasg",
	"journal",
]

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
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

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
	"default": {
		"ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
		"NAME": os.environ.get(
			"SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")
		),
		"USER": os.environ.get("SQL_USER", "user"),
		"PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
		"HOST": os.environ.get("SQL_HOST", "localhost"),
		"PORT": os.environ.get("SQL_PORT", "5432"),
	}
}

if not DEBUG:
	DATABASE_URL = os.environ.get("DATABASE_URL")
	
	if DATABASE_URL:
		db_from_env = dj_database_url.config(
			default=DATABASE_URL, conn_max_age=500
		)
		DATABASES["default"].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-uk"

TIME_ZONE = "Europe/Zurich"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
# Add compression support
STATICFILES_STORAGE = (
	"cloudinary_storage.storage.StaticHashedCloudinaryStorage"
)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# Configure the handling of static files
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Replace 'your_cloudinary_url_here' with your actual Cloudinary URL
CLOUDINARY_STORAGE = {
	"CLOUD_NAME": os.environ.get("CLOUD_NAME"),
	"API_KEY": os.environ.get("API_KEY"),
	"API_SECRET": os.environ.get("API_SECRET"),
}
# CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "journal.CustomUser"

AUTHENTICATION_BACKENDS = (
	"allauth.account.auth_backends.AuthenticationBackend",
	"django.contrib.auth.backends.ModelBackend",
)
# https://stackoverflow.com/questions/71636502/django-allauth-customuser
# -object-has-no-attribute-username
# https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-user
# -models
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

ACCOUNT_FORMS = {"signup": "journal.forms.CustomSignupForm"}

SOCIALACCOUNT_FORMS = {
	"disconnect": "allauth.socialaccount.forms.DisconnectForm",
	"signup": "allauth.socialaccount.forms.SignupForm",
}

SOCIALACCOUNT_PROVIDERS = {
	'google': {
		'APPS': [
			{
				'client_id': os.environ.get("GOOGLE_CLIENT_ID"),
				'secret': os.environ.get("GOOGLE_SECRET"),
				'key': ''
			},
		],
		'SCOPE': [
			'profile',
			'email',
		],
		'AUTH_PARAMS': {
			'access_type': 'online',
		}
	}
}
