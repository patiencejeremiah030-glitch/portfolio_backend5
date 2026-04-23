"""
Test settings for portfolio_backend project.
Uses SQLite for faster test execution without requiring PostgreSQL.
"""

from .development import *

# Use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable password validation for faster tests
AUTH_PASSWORD_VALIDATORS = []

# Disable OpenAI API for tests
OPENAI_API_KEY = ''

# Disable rate limiting for tests
CHATBOT_RATE_LIMIT = 1000
CHATBOT_RATE_LIMIT_PERIOD = 1

# Disable debug for tests
DEBUG = False
