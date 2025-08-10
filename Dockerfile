FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml /app/
COPY README.md /app/
COPY src/ /app/src/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create directory for templates
RUN mkdir -p /app/templates

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "ai_task_orchestra.main:app", "--host", "0.0.0.0", "--port", "8000"]
