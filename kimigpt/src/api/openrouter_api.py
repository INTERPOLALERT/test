"""
KimiGPT - OpenRouter API Integration
"""

import os
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)


class OpenRouterAPI:
    """Wrapper for OpenRouter API"""

    def __init__(self):
        """Initialize OpenRouter API client"""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")

        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "openai/gpt-3.5-turbo"

    def generate(self, prompt: str,
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None,
                 **kwargs) -> str:
        """
        Generate response from OpenRouter

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
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://kimigpt.local",
                "X-Title": "KimiGPT"
            }

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

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
            }

            if max_tokens:
                payload["max_tokens"] = max_tokens

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"OpenRouter API error: {e}")
            raise
