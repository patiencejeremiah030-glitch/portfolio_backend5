"""
URL configuration for core app.
"""

from django.urls import path
from . import views
from . import views_html


app_name = 'core'

urlpatterns = [
    # Public endpoints
    path('home/', views.HomeAPIView.as_view(), name='home'),
    path('about/', views.AboutAPIView.as_view(), name='about'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('projects/', views.ProjectListAPIView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='project-detail'),

    # HTML pages for projects
    path('projects/page/', views_html.projects_page, name='projects-page'),
    path('projects/page/<int:project_id>/', views_html.project_detail_page, name='project-detail-page'),

    # Admin endpoints
    path('admin/profile/', views.ProfileAdminAPIView.as_view(), name='admin-profile'),
    path('admin/home/', views.HomeAdminAPIView.as_view(), name='admin-home'),
    path('admin/about/', views.AboutAdminAPIView.as_view(), name='admin-about'),
    path('admin/projects/', views.ProjectAdminListCreateAPIView.as_view(), name='admin-project-list'),
    path('admin/projects/<int:pk>/', views.ProjectAdminDetailAPIView.as_view(), name='admin-project-detail'),
]
