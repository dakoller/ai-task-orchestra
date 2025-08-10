"""Templates API endpoints."""

from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ai_task_orchestra.services.template_service import Template, TemplateService, get_template_service

# Create router
router = APIRouter()


@router.get("/")
async def list_templates(
    template_service: TemplateService = Depends(get_template_service),
) -> List[Dict]:
    """
    List all available task templates.
    """
    templates = template_service.get_templates()
    return [template.model_dump() for template in templates]


@router.get("/{template_name}")
async def get_template(
    template_name: str,
    template_service: TemplateService = Depends(get_template_service),
) -> Dict:
    """
    Get template details by name.

    - **template_name**: Name of the template to retrieve
    """
    template = template_service.get_template(template_name)
    return template.model_dump()


@router.post("/validate")
async def validate_template_parameters(
    template_name: str,
    parameters: Dict,
    template_service: TemplateService = Depends(get_template_service),
) -> Dict:
    """
    Validate parameters for a template.

    - **template_name**: Name of the template to validate parameters for
    - **parameters**: Parameters to validate
    """
    return template_service.validate_parameters(template_name, parameters)
