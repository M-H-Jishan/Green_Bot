"""
LLM Provider abstraction layer.
Supports OpenAI and Anthropic Claude, switchable via LLM_PROVIDER env var.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def get_response(self, query: str, context: Optional[str] = None) -> dict:
        """
        Get a response from the LLM.

        Args:
            query: The user's question.
            context: Optional context data to inject into the prompt.

        Returns:
            dict with keys: 'response' (str), 'success' (bool), 'error' (str|None)
        """
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider using the openai>=1.0 SDK."""

    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def get_response(self, query: str, context: Optional[str] = None) -> dict:
        try:
            system_prompt = (
                "You are a helpful assistant. Answer the user's question accurately and concisely. "
                "If context data is provided, use it to inform your answer."
            )
            user_content = query
            if context:
                user_content = f"Context data:\n{context}\n\nQuestion: {query}"

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            answer = response.choices[0].message.content.strip()
            return {'response': answer, 'success': True, 'error': None}
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {'response': '', 'success': False, 'error': str(e)}


class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider using the anthropic SDK."""

    def __init__(self):
        from anthropic import Anthropic
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL

    def get_response(self, query: str, context: Optional[str] = None) -> dict:
        try:
            system_prompt = (
                "You are a helpful assistant. Answer the user's question accurately and concisely. "
                "If context data is provided, use it to inform your answer."
            )
            user_content = query
            if context:
                user_content = f"Context data:\n{context}\n\nQuestion: {query}"

            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_content},
                ],
            )
            answer = response.content[0].text.strip()
            return {'response': answer, 'success': True, 'error': None}
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return {'response': '', 'success': False, 'error': str(e)}


def get_llm_provider() -> Optional[LLMProvider]:
    """
    Factory function to get the configured LLM provider.
    Returns None if no API key is set (KB-only mode).
    """
    provider_name = settings.LLM_PROVIDER.lower()

    if provider_name == 'openai':
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set — LLM fallback disabled (KB-only mode)")
            return None
        return OpenAIProvider()

    elif provider_name == 'claude':
        if not settings.ANTHROPIC_API_KEY:
            logger.warning("ANTHROPIC_API_KEY not set — LLM fallback disabled (KB-only mode)")
            return None
        return ClaudeProvider()

    else:
        logger.error(f"Unknown LLM_PROVIDER: {provider_name}")
        return None
