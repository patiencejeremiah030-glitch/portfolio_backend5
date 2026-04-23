"""
Development settings for portfolio_backend project.
"""

from .base import *

# Security
DEBUG = os.getenv('DEBUG', 'True') == 'True'
# base.py already loads SECRET_KEY from .env via decouple; only override if set in the real environment
_env_secret_key = os.getenv('SECRET_KEY')
if _env_secret_key:
    SECRET_KEY = _env_secret_key
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is required for development. "
        "Add it to backend/.env (see .env.example) or export SECRET_KEY in your shell. "
        "Generate one with: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
    )
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database (SQLite for easy local testing, PostgreSQL for production)
if os.getenv('USE_POSTGRES', 'False') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'portfolio_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
    if not DATABASES['default']['PASSWORD']:
        raise ValueError(
            "DB_PASSWORD environment variable is required for PostgreSQL. "
            "Set it in your .env file."
        )
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    os.getenv('FRONTEND_URL', 'http://localhost:3000'),
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

CORS_ALLOW_CREDENTIALS = True

# CORS allow all for development (disable in production)
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
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
    'django': {
        'handlers': ['console'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        'propagate': False,
    },
}
