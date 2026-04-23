"""
Serializers for core app models.
"""

from rest_framework import serializers
from .models import Profile, Home, About, Project


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.
    """
    skills = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'title', 'bio', 'profile_image', 'image_url', 'about_image',
            'github', 'linkedin', 'twitter', 'skills', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_skills(self, obj):
        """Get skills from About model if available."""
        about = About.objects.first()
        if about:
            return about.get_skills_list()
        return []

    def get_image_url(self, obj):
        """Return the full URL for the profile image."""
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None


class HomeSerializer(serializers.ModelSerializer):
    """
    Serializer for Home model.
    """
    class Meta:
        model = Home
        fields = [
            'id', 'headline', 'subheadline', 'hero_description',
            'features_title', 'features_description', 'cta_title', 'cta_description',
            'hero_image', 'resume_link',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class AboutSerializer(serializers.ModelSerializer):
    """
    Serializer for About model.
    """
    skills_list = serializers.SerializerMethodField(method_name='get_skills_list')
    
    class Meta:
        model = About
        fields = [
            'id', 'title', 'description', 'experience', 'skills', 'skills_list',
            'about_image', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_skills_list(self, obj):
        """Return skills as a list."""
        return obj.get_skills_list()


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model.
    """
    image_url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'image', 'image_url', 'live_link', 'github_link',
            'order', 'is_featured', 'is_active', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'tags']

    def get_tags(self, obj):
        """Reserved for future tagging; empty list keeps the API stable for the frontend."""
        return []

    def get_image_url(self, obj):
        """Return the full URL for the image."""
        if not obj.image:
            return None
        try:
            url = obj.image.url
        except (ValueError, OSError):
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
        return url


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for project listings.
    """
    image_url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'image', 'image_url', 'live_link', 'github_link',
            'is_featured', 'is_active', 'tags'
        ]
        read_only_fields = ['tags']

    def get_tags(self, obj):
        return []

    def get_image_url(self, obj):
        """Return the full URL for the image."""
        if not obj.image:
            return None
        try:
            url = obj.image.url
        except (ValueError, OSError):
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
        return url
