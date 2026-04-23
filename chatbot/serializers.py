"""
Serializers for chatbot app models.
"""

from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatMessage model.
    """
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class ChatSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatSession model.
    """
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = ['id', 'session_id', 'messages', 'message_count', 'created_at']
        read_only_fields = ['id', 'session_id', 'created_at']
    
    def get_message_count(self, obj):
        """Return the number of messages in this session."""
        return obj.get_message_count()


class ChatRequestSerializer(serializers.Serializer):
    """
    Serializer for chat request payload.
    """
    message = serializers.CharField(required=True, max_length=4000)
    session_id = serializers.UUIDField(required=False)
    
    def validate_message(self, value):
        """Validate that message is not empty or whitespace only."""
        if not value or not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value.strip()


class ChatResponseSerializer(serializers.Serializer):
    """
    Serializer for chat response.
    """
    response = serializers.CharField()
    session_id = serializers.UUIDField()
    message_id = serializers.IntegerField()
