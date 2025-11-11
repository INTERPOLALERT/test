"""
KimiGPT - Groq API Integration
"""

import os
import logging
from typing import Optional
from groq import Groq

logger = logging.getLogger(__name__)


class GroqAPI:
    """Wrapper for Groq API"""

    def __init__(self):
        """Initialize Groq API client"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-70b-versatile"

    def generate(self, prompt: str,
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None,
                 **kwargs) -> str:
        """
        Generate response from Groq

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
                messages.append({
                    "role": "system",
                    "content": system_prompt or "You are a helpful AI assistant specialized in web development."
                })

            messages.append({
                "role": "user",
                "content": prompt
            })

            chat_params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
            }

            if max_tokens:
                chat_params["max_tokens"] = max_tokens

            response = self.client.chat.completions.create(**chat_params)

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise

    def stream_generate(self, prompt: str, **kwargs):
        """Generate response with streaming"""
        try:
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant specialized in web development."},
                {"role": "user", "content": prompt}
            ]

            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Groq API streaming error: {e}")
            raise
