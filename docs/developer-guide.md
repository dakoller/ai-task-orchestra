# AI Task Orchestra Developer Guide

This guide provides information for developers contributing to the AI Task Orchestra project.

## Table of Contents

- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Development Environment

### Prerequisites

- Python 3.8 or higher
- Redis
- Ollama (optional, for AI model integration)
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/[username]/ai-task-orchestra.git
   cd ai-task-orchestra
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running the Application

1. Start Redis:
   ```bash
   # Using Docker
   docker run -d -p 6379:6379 redis:7-alpine
   ```

2. Start the API server:
   ```bash
   python run.py
   ```

3. Start the Celery worker:
   ```bash
   python run_worker.py
   ```

4. Start the Celery beat scheduler (optional):
   ```bash
   python run_beat.py
   ```

5. Start the Celery flower monitoring tool (optional):
   ```bash
   python run_flower.py
   ```

### Using Docker Compose

Alternatively, you can use Docker Compose to start all services:

```bash
docker-compose up -d
```

## Project Structure

The project is organized as follows:

```
ai-task-orchestra/
├── docs/                  # Documentation
├── src/                   # Source code
│   └── ai_task_orchestra/
│       ├── api/           # API endpoints
│       │   └── v1/        # API version 1
│       │       ├── endpoints/  # API endpoint modules
│       │       └── router.py   # API router
│       ├── integrations/  # External integrations (e.g., Ollama)
│       ├── services/      # Business logic services
│       ├── config.py      # Configuration
│       ├── main.py        # FastAPI application
│       └── worker.py      # Celery worker
├── templates/             # Task templates
├── tests/                 # Tests
├── .env.example           # Example environment variables
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker configuration
├── pyproject.toml         # Project metadata and dependencies
├── README.md              # Project README
└── run.py                 # Script to run the API server
```

### Key Modules

- **api**: Contains the API endpoints and routers.
- **integrations**: Contains integrations with external services (e.g., Ollama).
- **services**: Contains business logic services.
- **config.py**: Contains application configuration.
- **main.py**: Contains the FastAPI application.
- **worker.py**: Contains the Celery worker.

## Coding Standards

### Style Guide

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. We use the following tools to enforce coding standards:

- **Black**: Code formatter
- **isort**: Import sorter
- **Flake8**: Linter
- **mypy**: Static type checker

### Type Hints

We use type hints throughout the codebase. All functions and methods should have type hints for parameters and return values.

Example:

```python
def add_numbers(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of the two numbers
    """
    return a + b
```

### Docstrings

We use Google-style docstrings. All modules, classes, functions, and methods should have docstrings.

Example:

```python
def add_numbers(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of the two numbers
    """
    return a + b
```

## Testing

We use pytest for testing. Tests are located in the `tests` directory.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=ai_task_orchestra

# Run specific tests
pytest tests/test_api.py
```

### Writing Tests

Tests should be organized by module and functionality. Test files should be named `test_*.py`.

Example:

```python
# tests/test_services/test_template_service.py

import pytest

from ai_task_orchestra.services.template_service import TemplateService


def test_load_templates():
    """Test loading templates."""
    service = TemplateService(templates_dir="tests/fixtures/templates")
    templates = service.get_templates()
    assert len(templates) > 0
    assert templates[0].name == "test-template"
```

## Documentation

We use Markdown for documentation. Documentation is located in the `docs` directory.

### Building Documentation

We don't have a documentation build process yet. Documentation is written in Markdown and can be viewed directly on GitHub or in a Markdown viewer.

### Writing Documentation

Documentation should be clear, concise, and comprehensive. It should be written for both users and developers.

## Contributing

### Workflow

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Run tests to ensure your changes don't break existing functionality.
5. Submit a pull request.

### Pull Requests

Pull requests should include:

- A clear description of the changes.
- Any relevant issue numbers.
- Tests for new functionality.
- Documentation updates if necessary.

### Code Review

All pull requests will be reviewed by a maintainer. Feedback will be provided, and changes may be requested before the pull request is merged.

### Commit Messages

Commit messages should be clear and descriptive. They should explain what changes were made and why.

Example:

```
Add template validation

- Add validation for template parameters
- Add tests for template validation
- Update documentation
```

## Adding New Features

### Adding a New API Endpoint

1. Create a new file in `src/ai_task_orchestra/api/v1/endpoints/` for the endpoint.
2. Define the endpoint using FastAPI.
3. Add the endpoint to the router in `src/ai_task_orchestra/api/v1/router.py`.
4. Add tests for the endpoint.
5. Update documentation.

Example:

```python
# src/ai_task_orchestra/api/v1/endpoints/health.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

### Adding a New Service

1. Create a new file in `src/ai_task_orchestra/services/` for the service.
2. Define the service class.
3. Add tests for the service.
4. Update documentation.

Example:

```python
# src/ai_task_orchestra/services/health_service.py

class HealthService:
    """Service for health checks."""

    def check_health(self):
        """Check the health of the system.

        Returns:
            Health status
        """
        return {"status": "healthy"}
```

### Adding a New Template

1. Create a new YAML file in the `templates` directory.
2. Define the template according to the template format.
3. Add tests for the template.
4. Update documentation.

Example:

```yaml
# templates/custom-template.yaml
name: custom-template
description: Custom template description
parameters:
  - name: param1
    type: string
    required: true
    description: Parameter description
steps:
  - type: step_type
    param1: "{{param1}}"
```

## Troubleshooting

### Common Issues

#### Tests Failing

- Check that Redis is running.
- Check that the virtual environment is activated.
- Check that all dependencies are installed.

#### API Server Won't Start

- Check that the port is not already in use.
- Check that Redis is running.
- Check that the environment variables are set correctly.

#### Pre-commit Hooks Failing

- Run `black` and `isort` to format the code.
- Fix any issues reported by `flake8` and `mypy`.

### Getting Help

If you encounter issues not covered in this guide, please:

1. Check the [GitHub Issues](https://github.com/[username]/ai-task-orchestra/issues) to see if the issue has been reported.
2. Create a new issue if necessary, providing detailed information about the problem.
