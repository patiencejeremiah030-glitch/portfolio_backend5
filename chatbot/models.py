"""
Chatbot models for AI conversation management.
"""

import uuid
from django.db import models


class ChatSession(models.Model):
    """
    Represents a chat session for AI conversations.
    """
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Chat Session'
        verbose_name_plural = 'Chat Sessions'
        ordering = ['-created_at']
    
    def __str__(self):
        return str(self.session_id)
    
    def get_message_count(self):
        """Return the number of messages in this session."""
        return self.messages.count()


class ChatMessage(models.Model):
    """
    Individual chat messages within a session.
    """
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(
        ChatSession,
        related_name='messages',
        on_delete=models.CASCADE
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Metadata
    tokens_used = models.PositiveIntegerField(default=0, blank=True, null=True)
    model_used = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
