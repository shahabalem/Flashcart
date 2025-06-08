from core.django.base import *  # noqa
from core.django.base import env

# Production ENV
# BACKEND_ENVIRONMENT       production
SECRET_KEY = env("SECRET_KEY")
JWT_SECRET = env("JWT_SECRET")

ALLOWED_HOSTS = [
    "www.flashcard.com",
]

DEBUG = False
ADMIN_ENABLED = True

# Web Configuration
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
DISABLE_COLLECTSTATIC = 1
CORS_ORIGIN_ALLOW_ALL = True

# CSRF Protection
CSRF_COOKIES_SECURE = True
SESSION_COOKIE_SECURE = True

# XSS Protection
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# disable debug toolbar
ENABLE_DEBUG_TOOLBAR = False

# Download Data Domain
SITE_DOMAIN = "https://flaslearn.com"

# Setting Unsubscribe URL
UNSUBSCRIBE_URL = f"{SITE_DOMAIN}/confirmation?type=unsubscribe"

# Primary database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "postgres",
        "PORT": "5432",
        "OPTIONS": {"sslmode": "disable"},
    }
}


# Logging:

FORMATTERS = {
    'trace': {
        'format': '{levelname} {asctime:s} {threadName} {thread:d} {module} {filename} {lineno:d} {name} {funcName} {process:d} {message}',
        'style': '{',
    }
}

HANDLERS = {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'trace',
    },
    'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': BASE_DIR / 'logs/webapp.log',
        'mode': 'a',
        'encoding': 'utf-8',
        'formatter': 'trace',
        'backupCount': 5,
        'maxBytes': 1024 * 1024 * 50,  # 50 MB
        'level': 'WARNING',
    },
}

LOGGERS = {
    'django': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
    },
    'django.request': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
        'propagate': False,
    },
}

ROOT = {
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': FORMATTERS,
    'handlers': HANDLERS,
    'loggers': LOGGERS,
    'root': ROOT,
}
