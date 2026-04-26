"""
Production settings for portfolio_backend project.
Optimized for cloud deployment (Render, Fly.io, Heroku, etc.).
"""

import logging
import os
from .base import *

logger = logging.getLogger(__name__)

# Security
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')

# Hardcoded ALLOWED_HOSTS - no underscores in domain names!
ALLOWED_HOSTS = [
    'portfolio-backend5-2.onrender.com',
    'localhost',
    '127.0.0.1',
]

if not SECRET_KEY:
    raise ValueError('SECRET_KEY environment variable is required in production')

# Database
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    db_name = os.getenv('DB_NAME')
    if not db_name:
        raise ValueError(
            'Production requires DATABASE_URL or DB_NAME (with DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).'
        )
    DATABASES = {
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

# CORS
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv('FRONTEND_URL', '').split(',')
    if o.strip()
]

# Add backend itself to CORS
for host in ALLOWED_HOSTS:
    if host in ('localhost', '127.0.0.1'):
        continue
    origin = f'https://{host}'
    if origin not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(origin)

CORS_ALLOW_CREDENTIALS = True

# CSRF
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(
    ['https://portfolio-backend5-2.onrender.com'] + CORS_ALLOWED_ORIGINS
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

# REST Framework - JSON only in production
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