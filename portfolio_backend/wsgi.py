"""
WSGI config for portfolio_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Render sets RENDER=true; use production settings unless overridden explicitly.
_default = (
    'portfolio_backend.settings.production'
    if os.environ.get('RENDER')
    else 'portfolio_backend.settings.development'
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', _default)

application = get_wsgi_application()
