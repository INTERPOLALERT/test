"""
KimiGPT - Google Gemini API Integration
"""

import os
import logging
from typing import Optional, List
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiAPI:
    """Wrapper for Google Gemini API"""

    def __init__(self):
        """Initialize Gemini API client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        genai.configure(api_key=api_key)
        self.model_name = "gemini-1.5-flash"
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None,
                 **kwargs) -> str:
        """
        Generate response from Gemini

        Args:
            prompt: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
        try:
            generation_config = {
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 40,
            }

            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
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
            from PIL import Image
            import io

            # Convert bytes to PIL Images
            pil_images = []
            for img_data in images:
                img = Image.open(io.BytesIO(img_data))
                pil_images.append(img)

            # Create content with images and text
            content = pil_images + [prompt]

            response = self.model.generate_content(content)

            return response.text

        except Exception as e:
            logger.error(f"Gemini API error with images: {e}")
            raise

    def generate_with_video(self, prompt: str, video_path: str, **kwargs) -> str:
        """
        Generate response with video input

        Args:
            prompt: Text prompt
            video_path: Path to video file
            **kwargs: Additional parameters

        Returns:
            Generated text response
        """
        try:
            # Upload video file
            video_file = genai.upload_file(video_path)

            # Wait for processing
            import time
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)

            # Generate content with video
            response = self.model.generate_content([video_file, prompt])

            return response.text

        except Exception as e:
            logger.error(f"Gemini API error with video: {e}")
            raise

    def stream_generate(self, prompt: str, **kwargs):
        """Generate response with streaming"""
        try:
            response = self.model.generate_content(prompt, stream=True)

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Gemini API streaming error: {e}")
            raise
