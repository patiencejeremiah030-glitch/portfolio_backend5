"""
Views for portfolio_backend project.
"""

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


def health(request):
    """Liveness probe for Render and other platforms (no DB hit)."""
    return JsonResponse({'status': 'ok'})


def admin_login(request):
    """
    Admin login page that displays a login form for the portfolio CMS.
    """
    return render(request, 'admin_login.html')
