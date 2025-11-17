"""
KimiGPT - Smart API Manager with Intelligent Rotation
Handles multiple AI providers with automatic failover and load balancing
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIManager:
    """
    Intelligent API Manager that handles:
    - Multi-provider rotation
    - Automatic failover
    - Rate limit management
    - Health monitoring
    - Response caching
    - Load balancing
    """

    def __init__(self, config_path: str = "config.json"):
        """Initialize API Manager with configuration"""
        self.config = self._load_config(config_path)
        self.providers = {}
        self.api_status = {}
        self.usage_stats = defaultdict(lambda: {"requests": 0, "failures": 0, "total_time": 0})
        self.rate_limits = {}
        self.last_request_time = {}
        self.cache = {}
        self.cache_ttl = int(os.getenv("API_CACHE_TTL", 3600))
        self.max_cache_size = 100  # Maximum number of cached responses

        # Initialize API providers
        self._initialize_providers()

        logger.info("API Manager initialized with {} providers".format(len(self.providers)))

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}

    def _initialize_providers(self):
        """Initialize all available API providers - 100% FREE ONLY!"""
        from .gemini_api import GeminiAPI
        from .groq_api import GroqAPI
        from .huggingface_api import HuggingFaceAPI
        from .cohere_api import CohereAPI

        # Only 100% free APIs (no trials, no credits, no payments!)

        if os.getenv("GROQ_API_KEY"):
            try:
                self.providers["groq"] = GroqAPI()
                self.api_status["groq"] = "available"
                logger.info("✓ Groq API initialized (FREE)")
            except Exception as e:
                logger.warning(f"✗ Groq API failed: {e}")
                self.api_status["groq"] = "unavailable"

        if os.getenv("GEMINI_API_KEY"):
            try:
                self.providers["gemini"] = GeminiAPI()
                self.api_status["gemini"] = "available"
                logger.info("✓ Google Gemini API initialized (FREE)")
            except Exception as e:
                logger.warning(f"✗ Google Gemini API failed: {e}")
                self.api_status["gemini"] = "unavailable"

        if os.getenv("HUGGINGFACE_API_KEY"):
            try:
                self.providers["huggingface"] = HuggingFaceAPI()
                self.api_status["huggingface"] = "available"
                logger.info("✓ Hugging Face API initialized (FREE)")
            except Exception as e:
                logger.warning(f"✗ Hugging Face API failed: {e}")
                self.api_status["huggingface"] = "unavailable"

        if os.getenv("COHERE_API_KEY"):
            try:
                self.providers["cohere"] = CohereAPI()
                self.api_status["cohere"] = "available"
                logger.info("✓ Cohere API initialized (FREE)")
            except Exception as e:
                logger.warning(f"✗ Cohere API failed: {e}")
                self.api_status["cohere"] = "unavailable"

        if not self.providers:
            logger.error("⚠️ No API providers configured! Please add API keys to .env file")

    def _get_cache_key(self, prompt: str, provider: str, **kwargs) -> str:
        """Generate cache key for request"""
        key_data = f"{provider}:{prompt}:{json.dumps(kwargs, sort_keys=True)}"
        return str(hash(key_data))

    def _check_cache(self, cache_key: str) -> Optional[Any]:
        """Check if response is in cache and not expired"""
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data["timestamp"] < self.cache_ttl:
                logger.info("✓ Cache hit")
                return cached_data["response"]
            else:
                # Cache expired
                del self.cache[cache_key]
        return None

    def _store_cache(self, cache_key: str, response: Any):
        """Store response in cache with size limit"""
        # Clean up expired entries first
        current_time = time.time()
        self.cache = {
            k: v for k, v in self.cache.items()
            if current_time - v["timestamp"] < self.cache_ttl
        }

        # If cache is still too large, remove oldest entries
        if len(self.cache) >= self.max_cache_size:
            # Sort by timestamp and keep only the newest entries
            sorted_cache = sorted(
                self.cache.items(),
                key=lambda x: x[1]["timestamp"],
                reverse=True
            )
            self.cache = dict(sorted_cache[:self.max_cache_size - 1])

        self.cache[cache_key] = {
            "response": response,
            "timestamp": time.time()
        }

    def _select_provider(self, preferred_provider: Optional[str] = None,
                        task_type: str = "text") -> Optional[str]:
        """
        Intelligently select best available API provider

        Selection criteria:
        1. Preferred provider (if specified and available)
        2. Provider that supports task type
        3. Lowest failure rate
        4. Fastest response time
        5. Not rate limited
        6. Priority from config
        """
        available_providers = [p for p, status in self.api_status.items()
                              if status == "available"]

        if not available_providers:
            logger.error("No API providers available!")
            return None

        # If preferred provider specified and available, try it first
        if preferred_provider and preferred_provider in available_providers:
            if not self._is_rate_limited(preferred_provider):
                return preferred_provider

        # Filter by task type support
        api_config = self.config.get("api_providers", {})
        suitable_providers = []

        for provider in available_providers:
            if provider in api_config:
                supported_types = api_config[provider].get("supports", [])
                if task_type in supported_types or "text" in supported_types:
                    suitable_providers.append(provider)

        if not suitable_providers:
            suitable_providers = available_providers

        # Score providers based on performance
        provider_scores = {}
        for provider in suitable_providers:
            if self._is_rate_limited(provider):
                continue

            stats = self.usage_stats[provider]
            requests = stats["requests"]
            failures = stats["failures"]

            # Calculate success rate
            success_rate = 1.0
            if requests > 0:
                success_rate = (requests - failures) / requests

            # Calculate average response time
            avg_time = 0
            if requests > 0:
                avg_time = stats["total_time"] / requests

            # Get priority from config
            priority = api_config.get(provider, {}).get("priority", 10)

            # Combined score (lower is better)
            score = priority * (1 / success_rate) * (avg_time + 1)
            provider_scores[provider] = score

        if not provider_scores:
            # All providers are rate limited, pick first available
            return suitable_providers[0] if suitable_providers else available_providers[0]

        # Select provider with best score
        best_provider = min(provider_scores, key=provider_scores.get)
        return best_provider

    def _is_rate_limited(self, provider: str) -> bool:
        """Check if provider is currently rate limited"""
        if provider not in self.last_request_time:
            return False

        api_config = self.config.get("api_providers", {}).get(provider, {})
        rate_limit = api_config.get("rate_limit", 60)

        # Calculate time since last request
        time_since_last = time.time() - self.last_request_time[provider]
        min_interval = 60.0 / rate_limit  # seconds between requests

        return time_since_last < min_interval

    def _update_rate_limit(self, provider: str):
        """Update last request time for rate limiting"""
        self.last_request_time[provider] = time.time()

    def generate(self, prompt: str,
                 preferred_provider: Optional[str] = None,
                 task_type: str = "text",
                 max_retries: int = 3,
                 use_cache: bool = True,
                 **kwargs) -> Dict[str, Any]:
        """
        Generate response using best available API

        Args:
            prompt: The prompt to send to the API
            preferred_provider: Preferred API provider (optional)
            task_type: Type of task (text, image, code, etc.)
            max_retries: Maximum number of retry attempts
            use_cache: Whether to use cached responses
            **kwargs: Additional parameters for the API

        Returns:
            Dict with response data and metadata
        """
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(prompt, preferred_provider or "auto", **kwargs)
            cached_response = self._check_cache(cache_key)
            if cached_response:
                return cached_response

        attempts = 0
        tried_providers = []

        while attempts < max_retries:
            # Select provider
            provider_name = self._select_provider(preferred_provider, task_type)

            if not provider_name or provider_name in tried_providers:
                # Try next best provider
                remaining = [p for p in self.providers.keys()
                           if p not in tried_providers and self.api_status[p] == "available"]
                if not remaining:
                    break
                provider_name = remaining[0]

            if provider_name not in self.providers:
                break

            provider = self.providers[provider_name]
            tried_providers.append(provider_name)

            try:
                logger.info(f"Attempting request with {provider_name} (attempt {attempts + 1})")

                # Update rate limit
                self._update_rate_limit(provider_name)

                # Make request
                start_time = time.time()
                response = provider.generate(prompt, **kwargs)
                end_time = time.time()

                # Update stats
                self.usage_stats[provider_name]["requests"] += 1
                self.usage_stats[provider_name]["total_time"] += (end_time - start_time)

                # Prepare result
                result = {
                    "success": True,
                    "provider": provider_name,
                    "response": response,
                    "time": end_time - start_time,
                    "attempts": attempts + 1
                }

                # Cache successful response
                if use_cache:
                    self._store_cache(cache_key, result)

                logger.info(f"✓ Success with {provider_name} in {end_time - start_time:.2f}s")
                return result

            except Exception as e:
                logger.warning(f"✗ {provider_name} failed: {e}")
                self.usage_stats[provider_name]["failures"] += 1
                attempts += 1

                # Mark provider as temporarily unavailable if too many failures
                if self.usage_stats[provider_name]["failures"] > 5:
                    self.api_status[provider_name] = "degraded"
                    logger.warning(f"⚠️ {provider_name} marked as degraded")

                # Wait before retry
                if attempts < max_retries:
                    wait_time = 2 ** attempts  # Exponential backoff
                    logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)

        # All attempts failed
        logger.error("All API providers failed!")
        return {
            "success": False,
            "error": "All API providers failed after {} attempts".format(max_retries),
            "tried_providers": tried_providers
        }

    def get_status(self) -> Dict[str, Any]:
        """Get current status of all API providers"""
        status_report = {
            "timestamp": datetime.now().isoformat(),
            "providers": {}
        }

        for provider_name in self.providers.keys():
            stats = self.usage_stats[provider_name]
            status_report["providers"][provider_name] = {
                "status": self.api_status.get(provider_name, "unknown"),
                "requests": stats["requests"],
                "failures": stats["failures"],
                "success_rate": (stats["requests"] - stats["failures"]) / stats["requests"]
                                if stats["requests"] > 0 else 0,
                "avg_response_time": stats["total_time"] / stats["requests"]
                                    if stats["requests"] > 0 else 0,
                "rate_limited": self._is_rate_limited(provider_name)
            }

        return status_report

    def test_apis(self) -> Dict[str, bool]:
        """Test all configured APIs"""
        results = {}
        test_prompt = "Hello, this is a test. Respond with 'OK'."

        for provider_name in self.providers.keys():
            try:
                logger.info(f"Testing {provider_name}...")
                response = self.generate(test_prompt, preferred_provider=provider_name,
                                       use_cache=False, max_retries=1)
                results[provider_name] = response.get("success", False)
                if results[provider_name]:
                    logger.info(f"✓ {provider_name} test passed")
                else:
                    logger.warning(f"✗ {provider_name} test failed")
            except Exception as e:
                logger.error(f"✗ {provider_name} test error: {e}")
                results[provider_name] = False

        return results


# Global instance
_api_manager_instance = None

def get_api_manager() -> APIManager:
    """Get global API manager instance"""
    global _api_manager_instance
    if _api_manager_instance is None:
        _api_manager_instance = APIManager()
    return _api_manager_instance
