"""Tasks API endpoints."""

import logging
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from ai_task_orchestra.services.task_service import TaskService, get_task_service

# Create router
router = APIRouter()


class TaskCreate(BaseModel):
    """Task creation model."""

    template: str = Field(..., description="Name of the task template to use")
    parameters: Dict = Field(..., description="Parameters for the task template")
    priority: int = Field(5, ge=1, le=10, description="Task priority (1-10, default: 5)")
    depends_on: Optional[List[str]] = Field(None, description="List of task IDs this task depends on")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
) -> Dict:
    """
    Create a new task.

    - **template**: Name of the task template to use
    - **parameters**: Parameters for the task template
    - **priority**: Task priority (1-10, default: 5)
    - **depends_on**: List of task IDs this task depends on
    """
    # Add diagnostic logging
    logger = logging.getLogger(__name__)
    logger.info(f"Creating task with template: {task.template}")
    logger.info(f"Task parameters: {task.parameters}")
    logger.info(f"Task priority: {task.priority}")
    logger.info(f"Task dependencies: {task.depends_on}")
    
    try:
        result = await task_service.create_task(
            template_name=task.template,
            parameters=task.parameters,
            priority=task.priority,
            depends_on=task.depends_on,
        )
        logger.info(f"Task created successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        logger.exception("Task creation failed")
        raise


@router.get("/")
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter by task status"),
    template: Optional[str] = Query(None, description="Filter by template name"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    task_service: TaskService = Depends(get_task_service),
) -> List[Dict]:
    """
    List tasks with optional filtering.

    - **status**: Filter by task status (queued, running, completed, failed, cancelled)
    - **template**: Filter by template name
    - **limit**: Maximum number of tasks to return
    - **offset**: Pagination offset
    """
    return await task_service.list_tasks(
        status=status,
        template=template,
        limit=limit,
        offset=offset,
    )


@router.get("/status", summary="Get current tasks with execution status")
async def get_tasks_status(
    task_service: TaskService = Depends(get_task_service),
) -> Dict[str, List[Dict]]:
    """
    Get current tasks grouped by execution status.

    Returns a dictionary with tasks grouped by their status:
    - queued: Tasks waiting to be executed
    - running: Tasks currently being executed
    - completed: Tasks that have been successfully completed
    - failed: Tasks that have failed
    - cancelled: Tasks that have been cancelled
    
    Each task includes its ID, template name, creation time, and other relevant details.
    """
    # Get all tasks
    all_tasks = await task_service.list_tasks(limit=1000)
    
    # Group tasks by status
    tasks_by_status = {
        "queued": [],
        "running": [],
        "completed": [],
        "failed": [],
        "cancelled": []
    }
    
    for task in all_tasks:
        status = task.get("status", "unknown")
        if status in tasks_by_status:
            tasks_by_status[status].append(task)
    
    return tasks_by_status


@router.get("/{task_id}")
async def get_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> Dict:
    """
    Get task details by ID.

    - **task_id**: ID of the task to retrieve
    """
    return await task_service.get_task(task_id)


@router.patch("/{task_id}/priority")
async def update_task_priority(
    task_id: str,
    priority: int = Query(..., ge=1, le=10, description="New priority value (1-10)"),
    task_service: TaskService = Depends(get_task_service),
) -> Dict:
    """
    Update task priority.

    - **task_id**: ID of the task to update
    - **priority**: New priority value (1-10)
    """
    return await task_service.update_task_priority(task_id, priority)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
) -> None:
    """
    Cancel a task.

    - **task_id**: ID of the task to cancel
    """
    await task_service.cancel_task(task_id)
