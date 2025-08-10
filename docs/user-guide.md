# AI Task Orchestra User Guide

This guide provides instructions for using AI Task Orchestra.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Creating Tasks](#creating-tasks)
- [Managing Tasks](#managing-tasks)
- [Using Templates](#using-templates)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Installation

### Using Docker (Recommended)

The easiest way to install AI Task Orchestra is using Docker Compose:

1. Clone the repository:
   ```bash
   git clone https://github.com/[username]/ai-task-orchestra.git
   cd ai-task-orchestra
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

This will start the following services:
- API server
- Celery worker
- Redis
- Ollama

### Manual Installation

If you prefer to install AI Task Orchestra manually:

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

3. Install the package:
   ```bash
   pip install -e .
   ```

4. Install Redis and Ollama separately.

## Configuration

AI Task Orchestra can be configured using environment variables or a `.env` file. The following configuration options are available:

### API Configuration

- `API_HOST`: Host to bind to (default: 0.0.0.0)
- `API_PORT`: Port to bind to (default: 8000)
- `API_DEBUG`: Enable debug mode (default: false)
- `API_RELOAD`: Enable auto-reload (default: false)

### Database Configuration

- `DATABASE_URL`: Database URL (default: sqlite:///./ai_task_orchestra.db)

### Redis Configuration

- `REDIS_URL`: Redis URL (default: redis://localhost:6379/0)

### Ollama Configuration

- `OLLAMA_API_BASE_URL`: Ollama API base URL (default: http://localhost:11434)

### Logging Configuration

- `LOG_LEVEL`: Log level (default: INFO)

### Security Configuration

- `API_KEY`: API key for authentication (default: none)

### Templates Configuration

- `TEMPLATES_DIR`: Directory containing template YAML files (default: templates)

### Example .env File

```
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
API_RELOAD=true
DATABASE_URL=sqlite:///./ai_task_orchestra.db
REDIS_URL=redis://redis:6379/0
OLLAMA_API_BASE_URL=http://ollama:11434
LOG_LEVEL=INFO
API_KEY=your-api-key-here
```

## Running the Application

### Using Docker Compose

```bash
docker-compose up -d
```

### Using the Makefile

```bash
# Run the API server
make run

# Run the Celery worker
make worker

# Run the Celery beat scheduler
make beat

# Run the Celery flower monitoring tool
make flower
```

### Using Python Directly

```bash
# Run the API server
python run.py

# Run the Celery worker
python run_worker.py

# Run the Celery beat scheduler
python run_beat.py

# Run the Celery flower monitoring tool
python run_flower.py
```

## Creating Tasks

Tasks can be created using the API. Here's an example using curl:

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "template": "ollama-inference",
    "parameters": {
      "model": "llama3.1:8b",
      "prompt": "Explain quantum computing in simple terms"
    },
    "priority": 5
  }'
```

This will create a new task using the `ollama-inference` template with the specified parameters.

### Task Parameters

- `template`: Name of the template to use (required)
- `parameters`: Parameters for the template (required)
- `priority`: Task priority (1-10, default: 5)
- `depends_on`: List of task IDs this task depends on (optional)

## Managing Tasks

### Listing Tasks

```bash
curl http://localhost:8000/api/v1/tasks
```

You can filter tasks by status and template:

```bash
curl "http://localhost:8000/api/v1/tasks?status=queued&template=ollama-inference"
```

### Getting Task Details

```bash
curl http://localhost:8000/api/v1/tasks/{task_id}
```

### Updating Task Priority

```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/{task_id}/priority?priority=8"
```

### Cancelling a Task

```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/{task_id}
```

## Using Templates

AI Task Orchestra comes with several built-in templates:

- `git-script-execution`: Clone repository, run script, store results
- `ollama-inference`: Run inference with specified model and prompt
- `file-processing`: Process files with AI analysis

### Listing Templates

```bash
curl http://localhost:8000/api/v1/templates
```

### Getting Template Details

```bash
curl http://localhost:8000/api/v1/templates/{template_name}
```

### Validating Template Parameters

```bash
curl -X POST "http://localhost:8000/api/v1/templates/validate?template_name=ollama-inference" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "Explain quantum computing in simple terms"
  }'
```

### Creating Custom Templates

You can create custom templates by adding YAML files to the `templates` directory. See the [Templates Documentation](templates.md) for more information.

## Monitoring

### API Documentation

The API documentation is available at:

```
http://localhost:8000/docs
```

### Celery Flower

Celery Flower provides a web interface for monitoring Celery tasks. It's available at:

```
http://localhost:5555
```

## Troubleshooting

### Common Issues

#### API Server Won't Start

- Check if the port is already in use
- Check if the database file is accessible
- Check the logs for error messages

#### Tasks Stuck in Queued State

- Check if the Celery worker is running
- Check if Redis is running
- Check if the task has dependencies that haven't completed

#### Ollama Integration Issues

- Check if Ollama is running
- Check if the Ollama API URL is correct
- Check if the model is available in Ollama

### Logs

Logs are written to the console by default. You can change the log level using the `LOG_LEVEL` environment variable.

### Getting Help

If you encounter issues not covered in this guide, please:

1. Check the [GitHub Issues](https://github.com/[username]/ai-task-orchestra/issues) to see if the issue has been reported
2. Create a new issue if necessary, providing detailed information about the problem
