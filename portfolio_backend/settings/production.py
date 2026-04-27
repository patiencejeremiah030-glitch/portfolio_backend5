"""
Production settings for portfolio_backend project.
Optimized for cloud deployment (Render, Fly.io, Heroku, etc.).
"""

import os
from .base import *


# -----------------------------------------------------------------------------
# Environment helpers
# -----------------------------------------------------------------------------

def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f'{name} environment variable is required in production')
    return value


def _get_csv_env(name: str, default: str = '') -> list[str]:
    return [item.strip() for item in os.getenv(name, default).split(',') if item.strip()]


def _build_database_settings() -> dict:
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        import dj_database_url

        return {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }

    db_name = os.getenv('DB_NAME')
    if not db_name:
        raise ValueError(
            'Production requires DATABASE_URL or DB_NAME (with DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).'
        )

    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'CONN_MAX_AGE': 600,
            'OPTIONS': {
                'connect_timeout': 10,
            },
        }
    }


def _build_cors_allowed_origins(hosts: list[str]) -> list[str]:
    origins = _get_csv_env('FRONTEND_URL')
    for host in hosts:
        if host in ('localhost', '127.0.0.1'):
            continue
        origin = f'https://{host}'
        if origin not in origins:
            origins.append(origin)
    return origins


# -----------------------------------------------------------------------------
# Core settings
# -----------------------------------------------------------------------------

DEBUG = False
SECRET_KEY = _get_required_env('SECRET_KEY')

ALLOWED_HOSTS = [
    'portfolio-backend5-3.onrender.com',
    'localhost',
    '127.0.0.1',
]

DATABASES = _build_database_settings()
CORS_ALLOWED_ORIGINS = _build_cors_allowed_origins(ALLOWED_HOSTS)

CORS_ALLOW_CREDENTIALS = True

# -----------------------------------------------------------------------------
# CSRF / proxy / security
# -----------------------------------------------------------------------------

CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(
    ['https://portfolio-backend5-3.onrender.com'] + CORS_ALLOWED_ORIGINS
))

# Trust reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# HTTPS
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# -----------------------------------------------------------------------------
# REST and logging
# -----------------------------------------------------------------------------

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}