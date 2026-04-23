"""
OpenAI Service for AI chatbot integration.

This service handles communication with the OpenAI API,
including conversation memory and context injection.
"""

import logging
from typing import Dict, Any, Optional, List
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not available. Chatbot will not function.")


def _is_placeholder_api_key(api_key: str) -> bool:
    """True if the value is an example / unset key from .env templates."""
    if not api_key or not str(api_key).strip():
        return True
    normalized = str(api_key).strip().lower()
    if normalized in (
        'your-openai-api-key-here',
        'your-groq-api-key-here',
        'your-api-key-here',
    ):
        return True
    if normalized.startswith('your-') and normalized.endswith('here'):
        return True
    return False


def _looks_like_provider_api_key(api_key: str) -> bool:
    """Groq keys start with gsk_; OpenAI keys typically start with sk-."""
    key = str(api_key).strip()
    return key.startswith(('gsk_', 'sk-'))


class OpenAIService:
    """
    Service for interacting with OpenAI/Groq API.

    Handles:
    - API client initialization
    - Context-aware message generation
    - Conversation memory management
    - Error handling and fallbacks
    """

    def __init__(self):
        """Initialize the OpenAI/Groq client."""
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.client = None

        if (
            OPENAI_AVAILABLE
            and self.api_key
            and not _is_placeholder_api_key(self.api_key)
            and _looks_like_provider_api_key(self.api_key)
        ):
            try:
                # Use Groq API (compatible with OpenAI SDK)
                if self.api_key.strip().startswith('gsk_'):
                    self.client = OpenAI(
                        api_key=self.api_key,
                        base_url='https://api.groq.com/openai/v1'
                    )
                    logger.info("Groq API client initialized")
                else:
                    # Standard OpenAI (sk-...)
                    self.client = OpenAI(api_key=self.api_key)
                    logger.info("OpenAI API client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize API client: {e}")
        else:
            if self.api_key and not _is_placeholder_api_key(self.api_key) and not _looks_like_provider_api_key(self.api_key):
                logger.warning(
                    "OPENAI_API_KEY is set but does not look like a Groq (gsk_) or OpenAI (sk-) key; "
                    "using mock responses. Replace it with a real key from Groq or OpenAI."
                )
            else:
                logger.warning("API key not configured. Using mock responses.")
    
    def get_response(
        self,
        message: str,
        context: str,
        chat_session=None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Get AI response for a user message.
        
        Args:
            message: The user's message
            context: Portfolio context string
            chat_session: Optional ChatSession object for conversation history
            max_tokens: Maximum tokens in response
            temperature: Response creativity (0-1)
        
        Returns:
            Dict containing response content and metadata
        """
        # Build messages array
        messages = self._build_messages(message, context, chat_session)
        
        # If no valid client, return mock response
        if not self.client:
            return self._get_mock_response(message, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            
            choice = response.choices[0].message
            content = (choice.content or "").strip()
            if not content:
                content = (
                    "I do not have a text reply for that right now. "
                    "Please try rephrasing your question."
                )
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            logger.info(f"OpenAI response generated. Tokens used: {tokens_used}")
            
            return {
                'content': content,
                'tokens_used': tokens_used,
                'model_used': self.model,
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}", exc_info=True)
            return self._get_mock_response(message, context, error=str(e))
    
    def _build_messages(
        self,
        message: str,
        context: str,
        chat_session=None
    ) -> List[Dict[str, str]]:
        """
        Build the messages array for OpenAI API.
        
        Includes:
        - System prompt with portfolio context
        - Recent conversation history (if available)
        - Current user message
        """
        # System prompt with context
        system_prompt = self._get_system_prompt(context)
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history if available
        if chat_session:
            history = self._get_conversation_history(chat_session)
            messages.extend(history)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        return messages
    
    def _get_system_prompt(self, context: str) -> str:
        """
        Generate the system prompt with portfolio context.
        """
        return f"""You are an AI assistant for a developer portfolio website. Your role is to help visitors learn about the portfolio owner's skills, experience, and projects.

Use the following context about the portfolio to answer questions accurately:

{context}

Guidelines:
1. Be friendly, professional, and helpful
2. Answer questions based on the portfolio context provided
3. If asked about something not in the context, politely say you don't have that information
4. Keep responses concise but informative
5. Encourage visitors to check out the projects and contact the portfolio owner
6. Do not make up information that isn't in the context
7. If the context is empty or missing, introduce yourself as the portfolio assistant and explain that you're still being configured

Remember: You represent the portfolio owner, so maintain a professional tone."""
    
    def _get_conversation_history(self, chat_session, max_messages: int = 10) -> List[Dict[str, str]]:
        """
        Get recent conversation history for context.
        """
        history = []
        
        # Get recent messages (excluding the latest user message)
        recent_messages = chat_session.messages.order_by('-timestamp')[:max_messages]
        
        # Reverse to get chronological order
        for msg in reversed(recent_messages):
            history.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return history
    
    def _get_mock_response(
        self,
        message: str,
        context: str,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Return a mock response when OpenAI is not available.
        """
        if error:
            content = f"I apologize, but I'm experiencing technical difficulties ({error}). Please try again later or contact the portfolio owner directly."
        else:
            content = (
                "Hello! I'm the AI assistant for this portfolio. "
                "I'm currently running in demo mode because no valid Groq (gsk_…) or OpenAI (sk-…) "
                "API key is configured. Once configured, I'll be able to answer questions about the "
                "portfolio owner's skills, experience, and projects using the portfolio data."
            )
        
        logger.warning(f"Returning mock response for message: {message[:50]}...")
        
        return {
            'content': content,
            'tokens_used': 0,
            'model_used': 'mock',
        }
