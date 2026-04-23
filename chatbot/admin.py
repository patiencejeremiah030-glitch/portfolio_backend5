"""
Admin configuration for chatbot app.
"""

from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    """
    Inline admin for ChatMessage within ChatSession.
    """
    model = ChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'timestamp', 'tokens_used', 'model_used')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """
    Admin configuration for ChatSession model.
    """
    list_display = ('session_id', 'get_message_count', 'ip_address', 'created_at', 'updated_at')
    list_filter = ('created_at', 'ip_address')
    search_fields = ('session_id', 'ip_address')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
    
    inlines = [ChatMessageInline]
    
    def get_message_count(self, obj):
        """Return the number of messages in this session."""
        return obj.get_message_count()
    get_message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for ChatMessage model.
    """
    list_display = ('session', 'role', 'content_preview', 'timestamp', 'model_used')
    list_filter = ('role', 'timestamp', 'model_used')
    search_fields = ('content', 'session__session_id')
    readonly_fields = ('session', 'role', 'content', 'timestamp', 'tokens_used', 'model_used')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def content_preview(self, obj):
        """Return a preview of the message content."""
        if obj.content:
            return f"{obj.content[:100]}..." if len(obj.content) > 100 else obj.content
        return ''
    content_preview.short_description = 'Content'
