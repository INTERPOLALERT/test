"""
KimiGPT - Cohere API Integration
Free tier available!
"""

import os
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)


class CohereAPI:
    """Wrapper for Cohere API - Has free tier!"""

    def __init__(self):
        """Initialize Cohere API client"""
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY not found in environment")

        self.base_url = "https://api.cohere.ai/v1"
        self.model = "command"  # Free tier model

    def generate(self, prompt: str,
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None,
                 **kwargs) -> str:
        """
        Generate response from Cohere

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
                "Content-Type": "application/json"
            }

            # Build full prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "temperature": temperature,
                "max_tokens": max_tokens or 2048
            }

            response = requests.post(
                f"{self.base_url}/generate",
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            # Extract generated text
            if "generations" in data and len(data["generations"]) > 0:
                return data["generations"][0]["text"]
            else:
                return data.get("text", "")

        except Exception as e:
            logger.error(f"Cohere API error: {e}")
            raise
