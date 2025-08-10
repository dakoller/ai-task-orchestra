# AI Task Orchestra Templates

This document provides information about task templates in AI Task Orchestra.

## What are Templates?

Templates are reusable task definitions that define a sequence of steps to be executed. They provide a way to standardize common workflows and make them easily reusable.

## Template Format

Templates are defined in YAML format. Here's the basic structure of a template:

```yaml
name: template-name
description: Template description
parameters:
  - name: parameter1
    type: string
    required: true
    description: Parameter description
  - name: parameter2
    type: integer
    required: false
    description: Parameter description
steps:
  - type: step_type
    param1: value1
    param2: "{{parameter1}}"
  - type: another_step_type
    param1: "{{parameter2}}"
```

### Template Fields

- `name`: The name of the template (required)
- `description`: A description of the template (optional)
- `parameters`: A list of parameters that the template accepts (required)
- `steps`: A list of steps to execute (required)

### Parameter Fields

- `name`: The name of the parameter (required)
- `type`: The type of the parameter (required, one of: string, integer, number, boolean, array, object)
- `required`: Whether the parameter is required (optional, default: false)
- `description`: A description of the parameter (optional)

### Step Fields

- `type`: The type of the step (required)
- Additional fields specific to the step type

## Parameter Substitution

Parameters can be referenced in steps using the `{{parameter_name}}` syntax. The parameter value will be substituted when the task is executed.

## Built-in Templates

AI Task Orchestra comes with several built-in templates:

### Git Script Execution

Clones a Git repository, runs a script, and stores the results.

```yaml
name: git-script-execution
description: Clone repository, run script, store results
parameters:
  - name: repo_url
    type: string
    required: true
    description: Git repository URL
  - name: script_path
    type: string
    required: true
    description: Path to script within repository
  - name: output_path
    type: string
    required: true
    description: Path to store output
steps:
  - type: git_clone
    repo: "{{repo_url}}"
  - type: execute_script
    script: "{{script_path}}"
  - type: store_result
    path: "{{output_path}}"
```

### Ollama Inference

Runs inference with a specified model and prompt.

```yaml
name: ollama-inference
description: Run inference with specified model and prompt
parameters:
  - name: model
    type: string
    required: true
    description: Ollama model name
  - name: prompt
    type: string
    required: true
    description: Prompt for the model
  - name: system_prompt
    type: string
    required: false
    description: Optional system prompt
steps:
  - type: ollama_generate
    model: "{{model}}"
    prompt: "{{prompt}}"
    system: "{{system_prompt}}"
```

### File Processing

Processes files with AI analysis.

```yaml
name: file-processing
description: Process files with AI analysis
parameters:
  - name: input_files
    type: array
    required: true
    description: List of files to process
  - name: analysis_model
    type: string
    required: true
    description: Model to use for analysis
  - name: output_format
    type: string
    required: true
    description: Format for the output (json, markdown, text)
steps:
  - type: read_files
    files: "{{input_files}}"
  - type: ollama_analyze
    model: "{{analysis_model}}"
  - type: format_output
    format: "{{output_format}}"
```

## Creating Custom Templates

You can create custom templates by adding YAML files to the `templates` directory. The file name should match the template name with a `.yaml` or `.yml` extension.

For example, to create a custom template named `custom-template`, create a file named `custom-template.yaml` in the `templates` directory:

```yaml
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

## Step Types

AI Task Orchestra supports the following step types:

### git_clone

Clones a Git repository.

**Parameters**:
- `repo`: Git repository URL

### execute_script

Executes a script.

**Parameters**:
- `script`: Path to the script to execute

### store_result

Stores the result of a task.

**Parameters**:
- `path`: Path to store the result

### ollama_generate

Generates text using Ollama.

**Parameters**:
- `model`: Ollama model name
- `prompt`: Prompt for the model
- `system`: Optional system prompt

### read_files

Reads files.

**Parameters**:
- `files`: List of files to read

### ollama_analyze

Analyzes text using Ollama.

**Parameters**:
- `model`: Ollama model name

### format_output

Formats the output.

**Parameters**:
- `format`: Format for the output (json, markdown, text)

## Template Validation

Templates are validated when they are loaded. The validation checks:

- The template has a name
- The template has parameters
- The template has steps
- Each parameter has a name and type
- Each step has a type

## Using Templates

Templates can be used to create tasks via the API:

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

You can also validate parameters for a template:

```bash
curl -X POST http://localhost:8000/api/v1/templates/validate?template_name=ollama-inference \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "Explain quantum computing in simple terms"
  }'
