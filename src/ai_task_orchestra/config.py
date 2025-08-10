"""Configuration module for AI Task Orchestra."""

import os
from typing import Any, Dict, List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    api_debug: bool = Field(False, env="API_DEBUG")
    api_reload: bool = Field(False, env="API_RELOAD")

    # Database Configuration
    database_url: str = Field("sqlite:///./ai_task_orchestra.db", env="DATABASE_URL")

    # Redis Configuration
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")

    # Ollama Configuration
    ollama_api_base_url: str = Field("http://localhost:11434", env="OLLAMA_API_BASE_URL")

    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # Security Configuration
    api_key: Optional[str] = Field(None, env="API_KEY")

    # Templates Configuration
    templates_dir: str = Field("templates", env="TEMPLATES_DIR")

    # CORS Configuration
    cors_origins: List[str] = Field(["*"], env="CORS_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def dict_for_celery(self) -> Dict[str, Any]:
        """Get Celery configuration dictionary.

        Returns:
            Celery configuration dictionary
        """
        return {
            "broker_url": self.redis_url,
            "result_backend": self.redis_url,
            "task_serializer": "json",
            "accept_content": ["json"],
            "result_serializer": "json",
            "timezone": "UTC",
            "enable_utc": True,
            "task_track_started": True,
            "task_time_limit": 3600,  # 1 hour
            "worker_prefetch_multiplier": 1,
            "worker_max_tasks_per_child": 100,
        }


# Create settings instance
settings = Settings()
