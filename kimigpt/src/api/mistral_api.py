"""
KimiGPT - Mistral AI API Integration
"""

import os
import logging
from typing import Optional
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

logger = logging.getLogger(__name__)


class MistralAPI:
    """Wrapper for Mistral AI API"""

    def __init__(self):
        """Initialize Mistral API client"""
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment")

        self.client = MistralClient(api_key=api_key)
        self.model = "mistral-small-latest"

    def generate(self, prompt: str,
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None,
                 **kwargs) -> str:
        """
        Generate response from Mistral

        Args:
            prompt: User prompt
            system_prompt: System instructions
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
        try:
            messages = []

            if system_prompt:
                messages.append(ChatMessage(
                    role="system",
                    content=system_prompt or "You are a helpful AI assistant specialized in web development."
                ))

            messages.append(ChatMessage(
                role="user",
                content=prompt
            ))

            response = self.client.chat(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Mistral API error: {e}")
            raise

    def stream_generate(self, prompt: str, **kwargs):
        """Generate response with streaming"""
        try:
            messages = [
                ChatMessage(role="system", content="You are a helpful AI assistant specialized in web development."),
                ChatMessage(role="user", content=prompt)
            ]

            for chunk in self.client.chat_stream(
                model=self.model,
                messages=messages
            ):
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Mistral API streaming error: {e}")
            raise
