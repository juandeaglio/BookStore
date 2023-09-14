"""
Inherits a lot of stuff from settings.py in the base project.
"""
import os

import BookStoreServer.settings

BASE_DIR = BookStoreServer.settings.BASE_DIR

SECRET_KEY = BookStoreServer.settings.SECRET_KEY

# Application definition

INSTALLED_APPS = BookStoreServer.settings.INSTALLED_APPS

MIDDLEWARE = BookStoreServer.settings.MIDDLEWARE

ROOT_URLCONF = BookStoreServer.settings.ROOT_URLCONF

TEMPLATES = BookStoreServer.settings.TEMPLATES

WSGI_APPLICATION = BookStoreServer.settings.WSGI_APPLICATION

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = BookStoreServer.settings.DATABASES

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = BookStoreServer.settings.AUTH_PASSWORD_VALIDATORS

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = BookStoreServer.settings.LANGUAGE_CODE

TIME_ZONE = BookStoreServer.settings.TIME_ZONE
USE_I18N = BookStoreServer.settings.USE_I18N
USE_TZ = BookStoreServer.settings.USE_TZ

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = BookStoreServer.settings.STATIC_URL

STATICFILES_DIRS = [
    BookStoreServer.settings.BASE_DIR, 'static'
]
CSRF_TRUSTED_ORIGINS = BookStoreServer.settings.CSRF_TRUSTED_ORIGINS

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = BookStoreServer.settings.DEFAULT_AUTO_FIELD

if os.environ.get("ENVIRONMENT") == "test":
    DEBUG = True
    CORS_ALLOW_ALL_ORIGINS = DEBUG
    CORS_ALLOW_HEADERS = (
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    )

    CORS_ORIGIN_WHITELIST = (
        'http://localhost:3000',  # for localhost (REACT Default)
    )
    # CORS_URLS_REGEX = r'^/catalog_service/fetchCatalog.*$'
    # CORS_ALLOW_METHODS = [
    #     'DELETE',
    #     'GET',
    #     'OPTIONS',
    #     'PATCH',
    #     'POST',
    #     'PUT',
    # ]
else:
    DEBUG = False
