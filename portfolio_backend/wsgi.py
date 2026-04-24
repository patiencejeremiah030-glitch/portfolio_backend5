"""
WSGI config for portfolio_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Literal default for hosts (Vercel, etc.) that read this file; manage.py uses the same pattern.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
# Render / Vercel: use production when the generic package settings are still selected.
if (os.environ.get('RENDER') or os.environ.get('VERCEL')) and os.environ.get(
    'DJANGO_SETTINGS_MODULE'
) == 'portfolio_backend.settings':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio_backend.settings.production'

application = get_wsgi_application()
