"""
KimiGPT - Hugging Face Inference API Integration
Completely free for many models!
"""

import os
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)


class HuggingFaceAPI:
    """Wrapper for Hugging Face Inference API - 100% FREE!"""

    def __init__(self):
        """Initialize Hugging Face API client"""
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment")

        self.base_url = "https://api-inference.huggingface.co/models"
        # Using free models
        self.model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    def generate(self, prompt: str,
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None,
                 **kwargs) -> str:
        """
        Generate response from Hugging Face

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
                full_prompt = f"<s>[INST] {system_prompt}\n\n{prompt} [/INST]"

            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": max_tokens or 2048,
                    "return_full_text": False
                }
            }

            response = requests.post(
                f"{self.base_url}/{self.model}",
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            # Handle response format
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "")
            elif isinstance(data, dict):
                return data.get("generated_text", "")
            else:
                return str(data)

        except Exception as e:
            logger.error(f"Hugging Face API error: {e}")
            raise
