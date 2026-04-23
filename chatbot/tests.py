"""
Tests for chatbot app.
"""

import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import ChatSession, ChatMessage


class ChatAPITest(TestCase):
    """Test cases for Chat API."""
    
    def setUp(self):
        self.client = APIClient()
        self.chat_url = reverse('chatbot:chat')
    
    def test_chat_empty_message(self):
        """Test chat with empty message."""
        response = self.client.post(self.chat_url, {'message': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_chat_valid_message(self):
        """Test chat with valid message."""
        response = self.client.post(
            self.chat_url,
            {'message': 'Hello, tell me about the portfolio owner'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('response', response.data)
        self.assertIn('session_id', response.data)
    
    def test_chat_with_session_id(self):
        """Test chat with existing session ID."""
        session = ChatSession.objects.create()
        response = self.client.post(
            self.chat_url,
            {'message': 'Hello', 'session_id': str(session.session_id)},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['session_id'], str(session.session_id))
    
    def test_chat_saves_messages(self):
        """Test that chat messages are saved to database."""
        response = self.client.post(
            self.chat_url,
            {'message': 'Test message'},
            format='json'
        )
        session_id = uuid.UUID(response.data['session_id'])
        session = ChatSession.objects.get(session_id=session_id)
        
        self.assertEqual(session.messages.count(), 2)  # User + Assistant messages
        user_msg = session.messages.filter(role='user').first()
        self.assertEqual(user_msg.content, 'Test message')


class ChatSessionAPITest(TestCase):
    """Test cases for Chat Session API."""
    
    def setUp(self):
        self.client = APIClient()
        self.session = ChatSession.objects.create()
        self.session_url = reverse('chatbot:chat-session', args=[self.session.session_id])
    
    def test_get_session(self):
        """Test getting a chat session."""
        # Add some messages
        ChatMessage.objects.create(
            session=self.session,
            role='user',
            content='Hello'
        )
        ChatMessage.objects.create(
            session=self.session,
            role='assistant',
            content='Hi there!'
        )
        
        response = self.client.get(self.session_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['messages']), 2)
    
    def test_get_nonexistent_session(self):
        """Test getting a non-existent session."""
        fake_id = uuid.uuid4()
        url = reverse('chatbot:chat-session', args=[fake_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ChatSessionsListAPITest(TestCase):
    """Test cases for Chat Sessions List API."""
    
    def setUp(self):
        self.client = APIClient()
        self.sessions_url = reverse('chatbot:chat-sessions')
    
    def test_list_sessions_empty(self):
        """Test listing sessions when none exist."""
        response = self.client.get(self.sessions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_list_sessions(self):
        """Test listing sessions."""
        ChatSession.objects.create()
        ChatSession.objects.create()
        
        response = self.client.get(self.sessions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
