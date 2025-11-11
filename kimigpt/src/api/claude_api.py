"""
KimiGPT - Anthropic Claude API Integration
"""

import os
import logging
from typing import Optional, Dict, Any, List
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeAPI:
    """Wrapper for Anthropic Claude API"""

    def __init__(self):
        """Initialize Claude API client"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 4096

    def generate(self, prompt: str,
                 system_prompt: Optional[str] = None,
                 max_tokens: Optional[int] = None,
                 temperature: float = 0.7,
                 **kwargs) -> str:
        """
        Generate response from Claude

        Args:
            prompt: User prompt
            system_prompt: System instructions
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
        try:
            messages = [{"role": "user", "content": prompt}]

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature,
                system=system_prompt or "You are a helpful AI assistant specialized in web development.",
                messages=messages
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    def generate_with_images(self, prompt: str,
                            images: List[bytes],
                            **kwargs) -> str:
        """
        Generate response with image inputs

        Args:
            prompt: Text prompt
            images: List of image data (bytes)
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
        try:
            # Convert images to base64
            import base64

            content = []

            # Add images
            for img_data in images:
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64.b64encode(img_data).decode()
                    }
                })

            # Add text prompt
            content.append({
                "type": "text",
                "text": prompt
            })

            messages = [{"role": "user", "content": content}]

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=messages
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude API error with images: {e}")
            raise

    def stream_generate(self, prompt: str, **kwargs):
        """Generate response with streaming"""
        try:
            messages = [{"role": "user", "content": prompt}]

            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Claude API streaming error: {e}")
            raise
