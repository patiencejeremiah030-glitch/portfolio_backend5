"""
Django views for rendering HTML pages with projects.
"""
from django.shortcuts import render
from .models import Project


def projects_page(request):
    """Render a beautiful projects showcase page."""
    projects = Project.objects.filter(is_active=True).order_by('order', '-created_at')
    return render(request, 'core/projects.html', {'projects': projects})


def project_detail_page(request, project_id):
    """Render a single project detail page."""
    project = Project.objects.get(id=project_id, is_active=True)
    return render(request, 'core/project_detail.html', {'project': project})
