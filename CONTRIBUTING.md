# Contributing to AI Task Orchestra

Thank you for your interest in contributing to AI Task Orchestra! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all contributors. Please be respectful and considerate of others when participating in the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Redis
- Ollama (optional, for AI model integration)
- Git

### Setup

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/[your-username]/ai-task-orchestra.git
   cd ai-task-orchestra
   ```
3. Add the original repository as a remote:
   ```bash
   git remote add upstream https://github.com/[username]/ai-task-orchestra.git
   ```
4. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
5. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```
6. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   or
   ```bash
   git checkout -b fix/your-bug-fix
   ```

2. Make your changes.

3. Run tests to ensure your changes don't break existing functionality:
   ```bash
   pytest
   ```

4. Commit your changes:
   ```bash
   git commit -m "Your descriptive commit message"
   ```

5. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a pull request from your fork to the original repository.

## Pull Request Process

1. Ensure your code follows the project's coding standards.
2. Update the documentation if necessary.
3. Add tests for new functionality.
4. Ensure all tests pass.
5. Submit the pull request.
6. Address any feedback from the code review.
7. Once approved, your pull request will be merged.

## Coding Standards

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. We use the following tools to enforce coding standards:

- **Black**: Code formatter
- **isort**: Import sorter
- **Flake8**: Linter
- **mypy**: Static type checker

### Type Hints

We use type hints throughout the codebase. All functions and methods should have type hints for parameters and return values.

### Docstrings

We use Google-style docstrings. All modules, classes, functions, and methods should have docstrings.

For more details, see the [Developer Guide](docs/developer-guide.md).

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

For more details, see the [Developer Guide](docs/developer-guide.md).

## Documentation

We use Markdown for documentation. Documentation is located in the `docs` directory.

### Building Documentation

We don't have a documentation build process yet. Documentation is written in Markdown and can be viewed directly on GitHub or in a Markdown viewer.

### Writing Documentation

Documentation should be clear, concise, and comprehensive. It should be written for both users and developers.

For more details, see the [Developer Guide](docs/developer-guide.md).

## Issue Reporting

If you encounter a bug or have a suggestion for improvement, please create an issue on GitHub.

### Bug Reports

When reporting a bug, please include:

- A clear and descriptive title
- A detailed description of the issue
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any relevant logs or error messages
- Your environment (OS, Python version, etc.)

### Feature Requests

When requesting a feature, please include:

- A clear and descriptive title
- A detailed description of the feature
- Why the feature would be useful
- Any relevant examples or use cases

## Feature Requests

We welcome feature requests! If you have an idea for a new feature, please create an issue on GitHub with the "feature request" label.

## License

By contributing to AI Task Orchestra, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## Questions?

If you have any questions, feel free to create an issue on GitHub or reach out to the maintainers.

Thank you for contributing to AI Task Orchestra!
