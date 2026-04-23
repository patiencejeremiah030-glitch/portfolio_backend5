"""
Views for chatbot app.
"""

import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatRequestSerializer, ChatResponseSerializer, ChatSessionSerializer
)
from .services.openai_service import OpenAIService
from .utils.context_engine import build_context_string

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ChatAPIView(APIView):
    """
    AI-powered chatbot endpoint.
    Accepts a message and returns an AI-generated response based on portfolio context.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle chat message and return AI response.
        """
        # Apply rate limiting in non-test environments
        if not getattr(settings, 'TESTING', False):
            try:
                from django_ratelimit.decorators import ratelimit
                from django_ratelimit.exceptions import Ratelimited

                # Use decorator for rate limiting
                @ratelimit(
                    key='ip',
                    rate=f'{settings.CHATBOT_RATE_LIMIT}/{settings.CHATBOT_RATE_LIMIT_PERIOD}s',
                    block=True
                )
                def rate_limited_post(req):
                    return self._process_chat_message(req)

                try:
                    return rate_limited_post(request)
                except Ratelimited:
                    return Response(
                        {'error': 'Rate limit exceeded. Please try again later.'},
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )
            except ImportError:
                # django-ratelimit not installed, skip rate limiting
                logger.warning("django-ratelimit not installed, skipping rate limiting")
                return self._process_chat_message(request)
        else:
            return self._process_chat_message(request)
    
    def _process_chat_message(self, request):
        """Process the chat message (called after rate limiting check)."""
        try:
            # Log incoming request for debugging
            logger.info(f"Received chat request: {request.content_type}")
            
            serializer = ChatRequestSerializer(data=request.data)

            if not serializer.is_valid():
                logger.warning(f"Invalid request data: {serializer.errors}")
                return Response(
                    {'error': 'Invalid request', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            message = serializer.validated_data['message']
            session_id = serializer.validated_data.get('session_id')

            # Get or create chat session
            session = self._get_or_create_session(session_id, request)

            # Build context from portfolio data
            context = build_context_string()

            # Generate reply before persisting this turn's user message so history
            # from the DB does not duplicate the current user message in the prompt.
            openai_service = OpenAIService()
            ai_response = openai_service.get_response(message, context, session)

            # Save user message, then assistant (same transaction semantics as before)
            ChatMessage.objects.create(
                session=session,
                role='user',
                content=message
            )

            # Save assistant message
            assistant_message = ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=ai_response['content'],
                tokens_used=ai_response.get('tokens_used', 0),
                model_used=ai_response.get('model_used', settings.OPENAI_MODEL)
            )

            # Return response
            response_serializer = ChatResponseSerializer({
                'response': ai_response['content'],
                'session_id': session.session_id,
                'message_id': assistant_message.id
            })

            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Chat error: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Failed to process message', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _get_or_create_session(self, session_id, request):
        """Get existing session or create a new one."""
        if session_id:
            session = ChatSession.objects.filter(session_id=session_id).first()
            if session:
                return session
        
        # Create new session
        return ChatSession.objects.create(
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            ip_address=self._get_client_ip(request)
        )
    
    def _get_client_ip(self, request):
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class ChatSessionAPIView(APIView):
    """
    View for retrieving chat session history.
    """
    permission_classes = [AllowAny]
    
    def get(self, request, session_id):
        """Get chat session with message history."""
        try:
            session = ChatSession.objects.get(session_id=session_id)
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ChatSessionsListAPIView(APIView):
    """
    View for listing all chat sessions (admin only).
    """
    permission_classes = [AllowAny]  # Can be changed to IsAdminUser
    
    def get(self, request):
        """List all chat sessions."""
        sessions = ChatSession.objects.all().order_by('-created_at')
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
