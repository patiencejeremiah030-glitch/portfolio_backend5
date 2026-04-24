"""
ASGI config for portfolio_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

_default = (
    'portfolio_backend.settings.production'
    if os.environ.get('RENDER')
    else 'portfolio_backend.settings.development'
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', _default)

application = get_asgi_application()
