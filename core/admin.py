"""
Admin configuration for core app.
"""

from django.contrib import admin
from .models import Profile, Home, About, Project


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.
    """
    list_display = ('name', 'title', 'created_at', 'updated_at')
    search_fields = ('name', 'title', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio')
        }),
        ('Images', {
            'fields': ('profile_image', 'about_image')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter'),
            'description': 'Add your social media profile links'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Home model.
    """
    list_display = ('headline', 'subheadline', 'created_at', 'updated_at')
    search_fields = ('headline', 'subheadline')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Hero Section', {
            'fields': ('headline', 'subheadline')
        }),
        ('Media', {
            'fields': ('hero_image',)
        }),
        ('Resume', {
            'fields': ('resume_link',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """
    Admin configuration for About model.
    """
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'skills')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Experience', {
            'fields': ('experience',)
        }),
        ('Skills', {
            'fields': ('skills',),
            'description': 'Enter skills as comma-separated values (e.g., Python, Django, React)'
        }),
        ('Image', {
            'fields': ('about_image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for Project model.
    """
    list_display = ('title', 'order', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_featured', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Media & Links', {
            'fields': ('image', 'live_link', 'github_link')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
