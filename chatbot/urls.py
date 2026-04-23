"""
URL configuration for chatbot app.
"""

from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # Chat endpoint
    path('chat/', views.ChatAPIView.as_view(), name='chat'),
    
    # Session management
    path('sessions/', views.ChatSessionsListAPIView.as_view(), name='chat-sessions'),
    path('sessions/<uuid:session_id>/', views.ChatSessionAPIView.as_view(), name='chat-session'),
]
