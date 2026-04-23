"""
URL configuration for portfolio_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import admin_login
from core.views_html import projects_page

urlpatterns = [
    # Root endpoint - Admin Login
    path('', admin_login, name='admin_login'),

    # Projects HTML page
    path('projects/', projects_page, name='projects-page'),

    # Admin
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/core/', include('core.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/users/', include('users.urls'))
]

# Serve media files in development
# Always serve media for admin file uploads to work
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Still serve media files in admin for file uploads
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site customization
admin.site.site_header = 'Portfolio Admin Dashboard'
admin.site.site_title = 'Portfolio Admin'
admin.site.index_title = 'Welcome to Portfolio Content Management'
