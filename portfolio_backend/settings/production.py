"""
Production settings for portfolio_backend project.
Optimized for cloud deployment (Render, Fly.io, Heroku, etc.).
"""

import logging
import os
from .base import *

logger = logging.getLogger(__name__)

# Security
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]

if not SECRET_KEY:
    raise ValueError('SECRET_KEY environment variable is required in production')

# Database - PostgreSQL (for platforms that provide it) or fallback to env vars
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

# CORS: prefer FRONTEND_URL (single or comma-separated); else use CORS_ALLOWED_ORIGINS from env
_cors_from_frontend = [o.strip() for o in os.getenv('FRONTEND_URL', '').split(',') if o.strip()]
_cors_from_env = [o.strip() for o in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if o.strip()]
CORS_ALLOWED_ORIGINS = list(dict.fromkeys(_cors_from_frontend or _cors_from_env))

for host in ALLOWED_HOSTS:
    host = host.strip()
    if not host or host in ('localhost', '127.0.0.1') or host.startswith('.'):
        continue
    origin = host if host.startswith('http') else f'https://{host}'
    if origin not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(origin)

CORS_ALLOW_CREDENTIALS = True

if not CORS_ALLOWED_ORIGINS:
    # Do not crash Gunicorn on first deploy (e.g. Blueprint env not filled yet). Browsers will
    # get CORS failures until FRONTEND_URL or CORS_ALLOWED_ORIGINS is set to your real frontend origin(s).
    logger.warning(
        'FRONTEND_URL and CORS_ALLOWED_ORIGINS are unset or empty. '
        'Set FRONTEND_URL (recommended) to your deployed frontend, e.g. https://your-app.vercel.app'
    )

# CSRF: merge explicit env list with CORS origins (SPA on another origin needs both)
_csrf_extra = [o.strip() for o in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]
_csrf = list(dict.fromkeys(list(CSRF_TRUSTED_ORIGINS) + _csrf_extra + CORS_ALLOWED_ORIGINS))
CSRF_TRUSTED_ORIGINS = _csrf

# Trust X-Forwarded-Proto from reverse proxies (Koyeb, Render, Railway, etc.)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# HTTPS settings (your hosting platform handles HTTPS termination)
SECURE_SSL_REDIRECT = False  # Platform handles HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# WhiteNoise + static storage are already configured in base.py (do not duplicate middleware).

# JSON API only in production (no browsable HTML renderer)
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
}

# Logging: console always; file only if the logs directory is writable (some containers are read-only)
logs_dir = BASE_DIR / 'logs'
handlers_config = {
    'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
    },
}
root_handlers = ['console']
django_handlers = ['console']

try:
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / 'django.log'
    log_path.touch(exist_ok=True)
    handlers_config['file'] = {
        'class': 'logging.FileHandler',
        'filename': str(log_path),
        'formatter': 'verbose',
    }
    root_handlers = ['console', 'file']
    django_handlers = ['console', 'file']
except OSError:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': handlers_config,
    'root': {
        'handlers': root_handlers,
        'level': 'INFO',
    },
    'django': {
        'handlers': django_handlers,
        'level': 'INFO',
        'propagate': False,
    },
}
