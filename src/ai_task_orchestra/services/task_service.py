"""Task service for AI Task Orchestra."""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Depends, HTTPException, status

from ai_task_orchestra.services.template_service import TemplateService, get_template_service
from ai_task_orchestra.worker import celery_app

logger = logging.getLogger(__name__)


class TaskService:
    """Service for managing tasks."""

    def __init__(self, template_service: TemplateService = Depends(get_template_service)):
        """Initialize the task service.

        Args:
            template_service: Template service
        """
        self.template_service = template_service
        # In a real implementation, this would be stored in a database
        self.tasks: Dict[str, Dict[str, Any]] = {}

    async def create_task(
        self, template_name: str, parameters: Dict[str, Any], priority: int = 5, depends_on: List[str] = None
    ) -> Dict[str, Any]:
        """Create a new task.

        Args:
            template_name: Name of the template to use
            parameters: Parameters for the template
            priority: Task priority (1-10, default: 5)
            depends_on: List of task IDs this task depends on

        Returns:
            Created task

        Raises:
            HTTPException: If the template is not found or parameters are invalid
        """
        # Validate template and parameters
        template = self.template_service.get_template(template_name)
        validation_result = self.template_service.validate_parameters(template_name, parameters)
        
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Invalid parameters",
                    "missing_parameters": validation_result["missing_parameters"],
                    "invalid_parameters": validation_result["invalid_parameters"],
                },
            )
        
        # Create task
        task_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat() + "Z"
        
        task = {
            "id": task_id,
            "status": "queued",
            "priority": priority,
            "created_at": created_at,
            "template": template_name,
            "parameters": parameters,
            "depends_on": depends_on or [],
        }
        
        # Store task
        self.tasks[task_id] = task
        
        # Enqueue task if it has no dependencies
        if not depends_on:
            await self.enqueue_task(task_id)
        
        return task

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a task by ID.

        Args:
            task_id: ID of the task

        Returns:
            Task

        Raises:
            HTTPException: If the task is not found
        """
        task = self.tasks.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task '{task_id}' not found",
            )
        return task

    async def list_tasks(
        self, status: Optional[str] = None, template: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List tasks with optional filtering.

        Args:
            status: Filter by task status
            template: Filter by template name
            limit: Maximum number of tasks to return
            offset: Pagination offset

        Returns:
            List of tasks
        """
        tasks = list(self.tasks.values())
        
        # Apply filters
        if status:
            tasks = [task for task in tasks if task["status"] == status]
        
        if template:
            tasks = [task for task in tasks if task["template"] == template]
        
        # Sort by created_at (newest first)
        tasks.sort(key=lambda task: task["created_at"], reverse=True)
        
        # Apply pagination
        tasks = tasks[offset:offset + limit]
        
        return tasks

    async def update_task_priority(self, task_id: str, priority: int) -> Dict[str, Any]:
        """Update task priority.

        Args:
            task_id: ID of the task
            priority: New priority value (1-10)

        Returns:
            Updated task

        Raises:
            HTTPException: If the task is not found
        """
        task = await self.get_task(task_id)
        
        # Only allow updating priority for queued tasks
        if task["status"] != "queued":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot update priority for task with status '{task['status']}'",
            )
        
        # Update priority
        task["priority"] = priority
        
        return task

    async def cancel_task(self, task_id: str) -> None:
        """Cancel a task.

        Args:
            task_id: ID of the task

        Raises:
            HTTPException: If the task is not found
        """
        task = await self.get_task(task_id)
        
        # Only allow cancelling queued or running tasks
        if task["status"] not in ["queued", "running"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel task with status '{task['status']}'",
            )
        
        # Update status
        task["status"] = "cancelled"
        
        # TODO: Cancel Celery task if running

    async def enqueue_task(self, task_id: str) -> None:
        """Enqueue a task for execution.

        Args:
            task_id: ID of the task

        Raises:
            HTTPException: If the task is not found
        """
        task = await self.get_task(task_id)
        
        # Only allow enqueueing queued tasks
        if task["status"] != "queued":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot enqueue task with status '{task['status']}'",
            )
        
        # Update status
        task["status"] = "running"
        task["started_at"] = datetime.utcnow().isoformat() + "Z"
        
        # Enqueue task
        celery_app.send_task(
            "ai_task_orchestra.execute_task",
            args=[task_id, task["template"], task["parameters"]],
            kwargs={},
            priority=task["priority"],
        )


def get_task_service(
    template_service: TemplateService = Depends(get_template_service),
) -> TaskService:
    """Get task service dependency.

    Args:
        template_service: Template service

    Returns:
        Task service
    """
    return TaskService(template_service=template_service)
