"""
Views for core app.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Profile, Home, About, Project
from .serializers import (
    ProfileSerializer, HomeSerializer, AboutSerializer,
    ProjectSerializer, ProjectListSerializer
)


class ProfileAPIView(generics.RetrieveAPIView):
    """
    Get the portfolio profile.
    Returns the single profile entry.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """Return the first (and only) profile."""
        return Profile.objects.first()

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return None if no profile exists."""
        instance = self.get_object()
        if not instance:
            return Response(None, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_context(self):
        """Include request in serializer context for image URLs."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class HomeAPIView(generics.RetrieveAPIView):
    """
    Get the home page hero section content.
    Returns the single home entry.
    """
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """Return the first (and only) home entry."""
        return Home.objects.first()
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return None if no home exists."""
        instance = self.get_object()
        if not instance:
            return Response(None, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AboutAPIView(generics.RetrieveAPIView):
    """
    Get the about page content.
    Returns the single about entry.
    """
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        """Return the first (and only) about entry."""
        return About.objects.first()
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return None if no about exists."""
        instance = self.get_object()
        if not instance:
            return Response(None, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProjectListAPIView(generics.ListAPIView):
    """
    Get all active projects.
    Supports filtering by featured status.
    """
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Return active projects, optionally filtered."""
        queryset = Project.objects.filter(is_active=True)

        # Filter by featured if requested
        featured = self.request.query_params.get('featured', None)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)

        return queryset

    def get_serializer_context(self):
        """Include request in serializer context for image URLs."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ProjectDetailAPIView(generics.RetrieveAPIView):
    """
    Get a single project by ID.
    """
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def get_serializer_context(self):
        """Include request in serializer context for image URLs."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# Admin-only views for CRUD operations

class ProfileAdminAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin view for updating profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return Profile.objects.first()

    def get_serializer_context(self):
        """Include request in serializer context for image URLs."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class HomeAdminAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin view for updating home content.
    """
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        return Home.objects.first()


class AboutAdminAPIView(generics.RetrieveUpdateAPIView):
    """
    Admin view for updating about content.
    """
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        return About.objects.first()


class ProjectAdminListCreateAPIView(generics.ListCreateAPIView):
    """
    Admin view for listing and creating projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        """Include request in serializer context for image URLs."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ProjectAdminDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin view for project CRUD operations.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def get_serializer_context(self):
        """Include request in serializer context for image URLs."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
