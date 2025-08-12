# AI Task Orchestra API Reference

This document provides a reference for the AI Task Orchestra API endpoints.

## Base URL

The base URL for all API endpoints is:

```
http://localhost:8000/api/v1
```

## Authentication

API authentication is done using API keys. To authenticate, include the API key in the `X-API-Key` header:

```
X-API-Key: your-api-key-here
```

## Endpoints

### Tasks

#### Create a Task

```
POST /tasks
```

Create a new task.

**Request Body**:

```json
{
  "template": "ollama-inference",
  "parameters": {
    "model": "llama3.1:8b",
    "prompt": "Explain quantum computing in simple terms"
  },
  "priority": 5,
  "depends_on": ["task-id-1", "task-id-2"]
}
```

**Parameters**:

- `template` (string, required): Name of the task template to use
- `parameters` (object, required): Parameters for the task template
- `priority` (integer, optional, default: 5): Task priority (1-10)
- `depends_on` (array, optional): List of task IDs this task depends on

**Response**:

```json
{
  "id": "task-uuid",
  "status": "queued",
  "priority": 5,
  "created_at": "2025-08-09T10:30:00Z",
  "template": "ollama-inference",
  "parameters": {
    "model": "llama3.1:8b",
    "prompt": "Explain quantum computing in simple terms"
  },
  "depends_on": []
}
```

#### List Tasks

```
GET /tasks
```

List tasks with optional filtering.

**Query Parameters**:

- `status` (string, optional): Filter by task status (queued, running, completed, failed, cancelled)
- `template` (string, optional): Filter by template name
- `limit` (integer, optional, default: 100): Maximum number of tasks to return
- `offset` (integer, optional, default: 0): Pagination offset

**Response**:

```json
[
  {
    "id": "task-uuid-1",
    "status": "completed",
    "priority": 5,
    "created_at": "2025-08-09T10:30:00Z",
    "completed_at": "2025-08-09T10:45:00Z",
    "template": "ollama-inference"
  },
  {
    "id": "task-uuid-2",
    "status": "queued",
    "priority": 8,
    "created_at": "2025-08-09T10:40:00Z",
    "template": "git-script-execution"
  }
]
```

#### Get Tasks by Execution Status

```
GET /tasks/status
```

Get current tasks grouped by their execution status.

**Response**:

```json
{
  "queued": [
    {
      "id": "task-uuid-2",
      "status": "queued",
      "priority": 8,
      "created_at": "2025-08-09T10:40:00Z",
      "template": "git-script-execution"
    }
  ],
  "running": [
    {
      "id": "task-uuid-3",
      "status": "running",
      "priority": 5,
      "created_at": "2025-08-09T10:50:00Z",
      "started_at": "2025-08-09T10:51:00Z",
      "template": "ollama-inference"
    }
  ],
  "completed": [
    {
      "id": "task-uuid-1",
      "status": "completed",
      "priority": 5,
      "created_at": "2025-08-09T10:30:00Z",
      "started_at": "2025-08-09T10:32:00Z",
      "completed_at": "2025-08-09T10:45:00Z",
      "template": "ollama-inference"
    }
  ],
  "failed": [],
  "cancelled": []
}
```

#### Get Task

```
GET /tasks/{task_id}
```

Get task details by ID.

**Path Parameters**:

- `task_id` (string, required): ID of the task to retrieve

**Response**:

```json
{
  "id": "task-uuid",
  "status": "completed",
  "priority": 5,
  "created_at": "2025-08-09T10:30:00Z",
  "started_at": "2025-08-09T10:32:00Z",
  "completed_at": "2025-08-09T10:45:00Z",
  "template": "ollama-inference",
  "parameters": {
    "model": "llama3.1:8b",
    "prompt": "Example prompt"
  },
  "result": {
    "output": "Example output from the model"
  },
  "resource_usage": {
    "model_name": "llama3.1:8b",
    "inference_time_seconds": 45.2,
    "memory_used_gb": 8.1
  }
}
```

#### Update Task Priority

```
PATCH /tasks/{task_id}/priority
```

Update task priority.

**Path Parameters**:

- `task_id` (string, required): ID of the task to update

**Query Parameters**:

- `priority` (integer, required): New priority value (1-10)

**Response**:

```json
{
  "id": "task-uuid",
  "priority": 8,
  "status": "queued"
}
```

#### Cancel Task

```
DELETE /tasks/{task_id}
```

Cancel a task.

**Path Parameters**:

- `task_id` (string, required): ID of the task to cancel

**Response**:

No content (204)

### Templates

#### List Templates

```
GET /templates
```

List all available task templates.

**Response**:

```json
[
  {
    "name": "git-script-execution",
    "description": "Clone repository, run script, store results",
    "parameters": [
      {
        "name": "repo_url",
        "type": "string",
        "required": true,
        "description": "Git repository URL"
      },
      {
        "name": "script_path",
        "type": "string",
        "required": true,
        "description": "Path to script within repository"
      },
      {
        "name": "output_path",
        "type": "string",
        "required": true,
        "description": "Path to store output"
      }
    ]
  },
  {
    "name": "ollama-inference",
    "description": "Run inference with specified model and prompt",
    "parameters": [
      {
        "name": "model",
        "type": "string",
        "required": true,
        "description": "Ollama model name"
      },
      {
        "name": "prompt",
        "type": "string",
        "required": true,
        "description": "Prompt for the model"
      },
      {
        "name": "system_prompt",
        "type": "string",
        "required": false,
        "description": "Optional system prompt"
      }
    ]
  }
]
```

#### Get Template

```
GET /templates/{template_name}
```

Get template details by name.

**Path Parameters**:

- `template_name` (string, required): Name of the template to retrieve

**Response**:

```json
{
  "name": "ollama-inference",
  "description": "Run inference with specified model and prompt",
  "parameters": [
    {
      "name": "model",
      "type": "string",
      "required": true,
      "description": "Ollama model name"
    },
    {
      "name": "prompt",
      "type": "string",
      "required": true,
      "description": "Prompt for the model"
    },
    {
      "name": "system_prompt",
      "type": "string",
      "required": false,
      "description": "Optional system prompt"
    }
  ],
  "steps": [
    {
      "type": "ollama_generate",
      "model": "{{model}}",
      "prompt": "{{prompt}}",
      "system": "{{system_prompt}}"
    }
  ]
}
```

#### Validate Template Parameters

```
POST /templates/validate
```

Validate parameters for a template.

**Query Parameters**:

- `template_name` (string, required): Name of the template to validate parameters for

**Request Body**:

```json
{
  "model": "llama3.1:8b",
  "prompt": "Explain quantum computing in simple terms"
}
```

**Response**:

```json
{
  "valid": true,
  "missing_parameters": [],
  "invalid_parameters": []
}
```

## Error Responses

Error responses have the following format:

```json
{
  "detail": "Error message"
}
```

Common error status codes:

- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
