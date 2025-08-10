"""Ollama integration for AI Task Orchestra."""

import json
import logging
from typing import Any, Dict, List, Optional, Union

import httpx
from pydantic import BaseModel, Field

from ai_task_orchestra.config import settings

logger = logging.getLogger(__name__)


class OllamaGenerateRequest(BaseModel):
    """Request model for Ollama generate API."""

    model: str
    prompt: str
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    options: Optional[Dict[str, Any]] = None
    format: Optional[str] = None
    stream: bool = False


class OllamaGenerateResponse(BaseModel):
    """Response model for Ollama generate API."""

    model: str
    created_at: str = Field(..., alias="created_at")
    response: str
    context: Optional[List[int]] = None
    done: bool
    total_duration: Optional[int] = Field(None, alias="total_duration")
    load_duration: Optional[int] = Field(None, alias="load_duration")
    prompt_eval_duration: Optional[int] = Field(None, alias="prompt_eval_duration")
    eval_duration: Optional[int] = Field(None, alias="eval_duration")
    eval_count: Optional[int] = Field(None, alias="eval_count")


class OllamaModelInfo(BaseModel):
    """Model information from Ollama API."""

    name: str
    modified_at: str = Field(..., alias="modified_at")
    size: int
    digest: str
    details: Dict[str, Any]


class OllamaClient:
    """Client for interacting with the Ollama API."""

    def __init__(self, base_url: str = None):
        """Initialize the Ollama client.

        Args:
            base_url: Base URL for the Ollama API
        """
        self.base_url = base_url or settings.ollama_api_base_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=60.0)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    async def generate(
        self, request: Union[OllamaGenerateRequest, Dict[str, Any]]
    ) -> OllamaGenerateResponse:
        """Generate a response from Ollama.

        Args:
            request: Generate request parameters

        Returns:
            Generate response
        """
        if isinstance(request, dict):
            request = OllamaGenerateRequest(**request)

        logger.info(f"Generating response with model: {request.model}")
        response = await self.client.post("/api/generate", json=request.model_dump(exclude_none=True))
        response.raise_for_status()
        return OllamaGenerateResponse(**response.json())

    async def list_models(self) -> List[OllamaModelInfo]:
        """List available models.

        Returns:
            List of available models
        """
        logger.info("Listing available models")
        response = await self.client.get("/api/tags")
        response.raise_for_status()
        data = response.json()
        return [OllamaModelInfo(**model) for model in data.get("models", [])]

    async def get_model(self, model_name: str) -> Optional[OllamaModelInfo]:
        """Get information about a specific model.

        Args:
            model_name: Name of the model

        Returns:
            Model information if found, None otherwise
        """
        logger.info(f"Getting information for model: {model_name}")
        models = await self.list_models()
        for model in models:
            if model.name == model_name:
                return model
        return None

    async def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Pull a model from Ollama.

        Args:
            model_name: Name of the model to pull

        Returns:
            Pull response
        """
        logger.info(f"Pulling model: {model_name}")
        response = await self.client.post("/api/pull", json={"name": model_name})
        response.raise_for_status()
        return response.json()

    async def check_model_loaded(self, model_name: str) -> bool:
        """Check if a model is loaded.

        Args:
            model_name: Name of the model to check

        Returns:
            True if the model is loaded, False otherwise
        """
        model = await self.get_model(model_name)
        return model is not None

    async def ensure_model_loaded(self, model_name: str) -> bool:
        """Ensure a model is loaded, pulling it if necessary.

        Args:
            model_name: Name of the model to ensure is loaded

        Returns:
            True if the model is loaded, False otherwise
        """
        if await self.check_model_loaded(model_name):
            logger.info(f"Model {model_name} is already loaded")
            return True

        logger.info(f"Model {model_name} is not loaded, pulling...")
        try:
            await self.pull_model(model_name)
            return await self.check_model_loaded(model_name)
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False
