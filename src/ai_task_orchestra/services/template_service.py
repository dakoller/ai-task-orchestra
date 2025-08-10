"""Template service for AI Task Orchestra."""

import glob
import logging
import os
from typing import Any, Dict, List, Optional

import yaml
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, Field, ValidationError

from ai_task_orchestra.config import settings

logger = logging.getLogger(__name__)


class TemplateParameter(BaseModel):
    """Template parameter model."""

    name: str
    type: str
    required: bool = False
    description: Optional[str] = None


class TemplateStep(BaseModel):
    """Template step model."""

    type: str
    # Additional fields will be dynamically validated


class Template(BaseModel):
    """Template model."""

    name: str
    description: Optional[str] = None
    parameters: List[TemplateParameter]
    steps: List[Dict[str, Any]]


class TemplateService:
    """Service for managing templates."""

    def __init__(self, templates_dir: str = None):
        """Initialize the template service.

        Args:
            templates_dir: Directory containing template YAML files
        """
        self.templates_dir = templates_dir or settings.templates_dir
        self.templates: Dict[str, Template] = {}
        self.load_templates()

    def load_templates(self) -> None:
        """Load templates from YAML files."""
        logger.info(f"Loading templates from {self.templates_dir}")
        
        # Create templates directory if it doesn't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Find all YAML files in the templates directory
        template_files = glob.glob(os.path.join(self.templates_dir, "*.yaml"))
        template_files.extend(glob.glob(os.path.join(self.templates_dir, "*.yml")))
        
        # Load each template
        for template_file in template_files:
            try:
                with open(template_file, "r") as f:
                    template_data = yaml.safe_load(f)
                
                template = Template(**template_data)
                self.templates[template.name] = template
                logger.info(f"Loaded template: {template.name}")
            except (ValidationError, yaml.YAMLError) as e:
                logger.error(f"Error loading template {template_file}: {e}")

    def get_templates(self) -> List[Template]:
        """Get all templates.

        Returns:
            List of templates
        """
        return list(self.templates.values())

    def get_template(self, name: str) -> Template:
        """Get a template by name.

        Args:
            name: Name of the template

        Returns:
            Template

        Raises:
            HTTPException: If the template is not found
        """
        template = self.templates.get(name)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template '{name}' not found",
            )
        return template

    def validate_parameters(self, template_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for a template.

        Args:
            template_name: Name of the template
            parameters: Parameters to validate

        Returns:
            Validation result

        Raises:
            HTTPException: If the template is not found
        """
        template = self.get_template(template_name)
        
        # Check for missing required parameters
        missing_parameters = []
        for param in template.parameters:
            if param.required and param.name not in parameters:
                missing_parameters.append(param.name)
        
        # Check for invalid parameters
        invalid_parameters = []
        for param_name, param_value in parameters.items():
            # Find the parameter definition
            param_def = next((p for p in template.parameters if p.name == param_name), None)
            
            # If the parameter is not defined in the template, it's invalid
            if not param_def:
                invalid_parameters.append(param_name)
                continue
            
            # TODO: Add type validation based on param_def.type
        
        # Return validation result
        return {
            "valid": len(missing_parameters) == 0 and len(invalid_parameters) == 0,
            "missing_parameters": missing_parameters,
            "invalid_parameters": invalid_parameters,
        }


def get_template_service() -> TemplateService:
    """Get template service dependency.

    Returns:
        Template service
    """
    return TemplateService()
