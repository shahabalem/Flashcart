import os

from core.django.base import *  # noqa
from core.django.base import env

# Development ENV
# BACKEND_ENVIRONMENT       development

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="change_me")
JWT_SECRET = env("JWT_SECRET", default="change_me")

ALLOWED_HOSTS = ["*"]

DEBUG = True
ADMIN_ENABLED = True


SECURE_SSL_REDIRECT = False

# Static files
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Select database engine based on env variable
if env.bool("USE_POSTGRES_FOR_DEVELOPMENT", default=0):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "5432",
            "OPTIONS": {"sslmode": "disable"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Debug Toolbar
from core.third.debug_toolbar.settings import *  # noqa
from core.third.debug_toolbar.setup import DebugToolbarSetup  # noqa

ENABLE_DEBUG_TOOLBAR = True
INTERNAL_IPS = ("127.0.0.1",)
INSTALLED_APPS, MIDDLEWARE = DebugToolbarSetup.do_settings(INSTALLED_APPS, MIDDLEWARE)

# Download Data Domain
SITE_DOMAIN = "localhost"

# Setting Unsubscribe URL
UNSUBSCRIBE_URL = f"{SITE_DOMAIN}/confirmation?type=unsubscribe"
