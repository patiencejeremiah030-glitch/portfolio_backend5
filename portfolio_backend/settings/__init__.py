"""
Settings package entry point.

When ``DJANGO_SETTINGS_MODULE`` is set to ``portfolio_backend.settings`` (no
``.development`` / ``.production`` suffix), Django loads this file. We default
to development settings so WSGI/ASGI do not run with an empty configuration.

For production, set explicitly::

    DJANGO_SETTINGS_MODULE=portfolio_backend.settings.production
"""

from .development import *  # noqa: F401, F403
