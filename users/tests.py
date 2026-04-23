"""
Tests for users app.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserRegistrationTest(TestCase):
    """Test cases for user registration."""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:register')
    
    def test_register_success(self):
        """Test successful user registration."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'testuser')
    
    def test_register_password_mismatch(self):
        """Test registration with mismatched passwords."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'DifferentPass123',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='SecurePass123'
        )
        data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_duplicate_username(self):
        """Test registration with duplicate username."""
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='SecurePass123'
        )
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(TestCase):
    """Test cases for user login."""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123'
        )
    
    def test_login_success(self):
        """Test successful login."""
        data = {
            'username': 'testuser',
            'password': 'SecurePass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserMeTest(TestCase):
    """Test cases for user me endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.me_url = reverse('users:user-me')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='SecurePass123'
        )
    
    def test_get_me_unauthenticated(self):
        """Test getting current user without authentication."""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_me_authenticated(self):
        """Test getting current user with authentication."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_update_me(self):
        """Test updating current user profile."""
        self.client.force_authenticate(user=self.user)
        data = {'first_name': 'Test', 'last_name': 'User'}
        response = self.client.patch(self.me_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
