"""
Ollama Service - Integration with local Ollama instance
Uses your existing llama3.3:70b model
"""

import logging
from typing import Dict, List, Optional
import aiohttp
import os

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for communicating with Ollama LLM"""

    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.3:70b")
        self.embedding_model = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text:latest")

    def set_model(self, model_name: str) -> bool:
        """
        Switch the active LLM model

        Args:
            model_name: Name of the model to use

        Returns:
            True if model was changed
        """
        logger.info(f"Switching LLM model from {self.model} to {model_name}")
        self.model = model_name
        return True

    def set_embedding_model(self, model_name: str) -> bool:
        """
        Switch the active embedding model

        Args:
            model_name: Name of the embedding model to use

        Returns:
            True if model was changed
        """
        logger.info(f"Switching embedding model from {self.embedding_model} to {model_name}")
        self.embedding_model = model_name
        return True

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        stream: bool = False
    ) -> Dict:
        """
        Generate text using Ollama

        Args:
            prompt: User prompt
            system_prompt: System instruction
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            Dict with response and metadata
        """
        try:
            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            # Prepare request
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ollama error: {response.status} - {error_text}")
                        raise Exception(f"Ollama request failed: {response.status}")

                    result = await response.json()

                    return {
                        "response": result["message"]["content"],
                        "model": result.get("model", self.model),
                        "total_duration": result.get("total_duration", 0),
                        "prompt_eval_count": result.get("prompt_eval_count", 0),
                        "eval_count": result.get("eval_count", 0)
                    }

        except Exception as e:
            logger.error(f"Ollama generation error: {e}", exc_info=True)
            raise

    async def embed(self, text: str) -> List[float]:
        """
        Generate embeddings using Ollama

        Args:
            text: Text to embed

        Returns:
            List of embedding values
        """
        try:
            payload = {
                "model": self.embedding_model,
                "prompt": text
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/embeddings",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ollama embedding error: {response.status} - {error_text}")
                        raise Exception(f"Embedding request failed: {response.status}")

                    result = await response.json()
                    return result["embedding"]

        except Exception as e:
            logger.error(f"Ollama embedding error: {e}", exc_info=True)
            raise

    async def list_models(self) -> List[Dict]:
        """
        List available models in Ollama

        Returns:
            List of model info dicts
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to list models: {response.status}")

                    result = await response.json()
                    return result.get("models", [])

        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    async def health_check(self) -> Dict:
        """
        Check if Ollama service is healthy

        Returns:
            Dict with health status
        """
        try:
            models = await self.list_models()

            # Check if our models are available
            model_names = [m["name"] for m in models]
            has_llm = self.model in model_names
            has_embedding = self.embedding_model in model_names

            return {
                "status": "healthy" if (has_llm and has_embedding) else "degraded",
                "ollama_url": self.base_url,
                "llm_model": self.model,
                "llm_available": has_llm,
                "embedding_model": self.embedding_model,
                "embedding_available": has_embedding,
                "total_models": len(models)
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "ollama_url": self.base_url
            }
