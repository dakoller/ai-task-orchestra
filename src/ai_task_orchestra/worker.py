"""Celery worker for AI Task Orchestra."""

import logging
from typing import Any, Dict

from celery import Celery

from ai_task_orchestra.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create Celery app
celery_app = Celery("ai_task_orchestra", broker=settings.redis_url, backend=settings.redis_url)

# Configure Celery
celery_app.conf.update(**settings.dict_for_celery())


@celery_app.task(name="ai_task_orchestra.execute_task")
def execute_task(task_id: str, template_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a task.

    Args:
        task_id: ID of the task
        template_name: Name of the template to use
        parameters: Parameters for the template

    Returns:
        Task result
    """
    logger.info(f"Executing task {task_id} with template {template_name}")
    
    try:
        # TODO: Implement task execution logic
        # 1. Load template
        # 2. Validate parameters
        # 3. Execute steps
        # 4. Return result
        
        # Placeholder implementation
        return {
            "task_id": task_id,
            "status": "completed",
            "result": {
                "output": f"Executed task with template {template_name}",
            },
        }
    except Exception as e:
        logger.error(f"Error executing task {task_id}: {e}")
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(e),
        }


@celery_app.task(name="ai_task_orchestra.ollama_generate")
def ollama_generate(model: str, prompt: str, system: str = None) -> Dict[str, Any]:
    """Generate text using Ollama.

    Args:
        model: Name of the model to use
        prompt: Prompt for the model
        system: Optional system prompt

    Returns:
        Generation result
    """
    logger.info(f"Generating text with model {model}")
    
    try:
        # Import here to avoid circular imports
        import httpx
        
        # Create request payload
        payload = {
            "model": model,
            "prompt": prompt,
        }
        
        if system:
            payload["system"] = system
        
        # Send request to Ollama API
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{settings.ollama_api_base_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
        
        return {
            "model": model,
            "response": result.get("response", ""),
            "status": "completed",
        }
    except Exception as e:
        logger.error(f"Error generating text with model {model}: {e}")
        return {
            "model": model,
            "status": "failed",
            "error": str(e),
        }


if __name__ == "__main__":
    celery_app.start()
