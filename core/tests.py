"""
Tests for core app.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Profile, Home, About, Project


class ProfileAPITest(TestCase):
    """Test cases for Profile API."""
    
    def setUp(self):
        self.client = APIClient()
        self.profile_url = reverse('core:profile')
        
    def test_get_profile_empty(self):
        """Test getting profile when none exists."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)
    
    def test_get_profile_exists(self):
        """Test getting profile when one exists."""
        Profile.objects.create(
            name="Test User",
            title="Developer",
            bio="Test bio"
        )
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test User")


class HomeAPITest(TestCase):
    """Test cases for Home API."""
    
    def setUp(self):
        self.client = APIClient()
        self.home_url = reverse('core:home')
        
    def test_get_home_empty(self):
        """Test getting home when none exists."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)
    
    def test_get_home_exists(self):
        """Test getting home when one exists."""
        Home.objects.create(
            headline="Test Headline",
            subheadline="Test Subheadline"
        )
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['headline'], "Test Headline")


class AboutAPITest(TestCase):
    """Test cases for About API."""
    
    def setUp(self):
        self.client = APIClient()
        self.about_url = reverse('core:about')
        
    def test_get_about_empty(self):
        """Test getting about when none exists."""
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)
    
    def test_get_about_exists(self):
        """Test getting about when one exists."""
        About.objects.create(
            title="About Me",
            description="Test description",
            skills="Python, Django"
        )
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "About Me")
        self.assertEqual(response.data['skills_list'], ["Python", "Django"])


class ProjectAPITest(TestCase):
    """Test cases for Project API."""
    
    def setUp(self):
        self.client = APIClient()
        self.projects_url = reverse('core:project-list')
        
    def test_get_projects_empty(self):
        """Test getting projects when none exist."""
        response = self.client.get(self.projects_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_get_projects_active_only(self):
        """Test that only active projects are returned."""
        Project.objects.create(
            title="Active Project",
            description="Test",
            is_active=True
        )
        Project.objects.create(
            title="Inactive Project",
            description="Test",
            is_active=False
        )
        response = self.client.get(self.projects_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Active Project")
    
    def test_get_projects_featured_filter(self):
        """Test filtering projects by featured status."""
        Project.objects.create(
            title="Featured Project",
            description="Test",
            is_active=True,
            is_featured=True
        )
        Project.objects.create(
            title="Regular Project",
            description="Test",
            is_active=True,
            is_featured=False
        )
        response = self.client.get(f"{self.projects_url}?featured=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Featured Project")
