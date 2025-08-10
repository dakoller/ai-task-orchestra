"""API router for v1 endpoints."""

from fastapi import APIRouter

from ai_task_orchestra.api.v1.endpoints import tasks, templates

# Create API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
