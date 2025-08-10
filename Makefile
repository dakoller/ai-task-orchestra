.PHONY: help install dev run worker beat flower docker-build docker-up docker-down clean

# Default target
help:
	@echo "Available targets:"
	@echo "  help        - Show this help message"
	@echo "  install     - Install the package"
	@echo "  dev         - Install the package in development mode"
	@echo "  run         - Run the API server"
	@echo "  worker      - Run the Celery worker"
	@echo "  beat        - Run the Celery beat scheduler"
	@echo "  flower      - Run the Celery flower monitoring tool"
	@echo "  docker-build - Build the Docker images"
	@echo "  docker-up   - Start the Docker containers"
	@echo "  docker-down - Stop the Docker containers"
	@echo "  clean       - Clean up temporary files"

# Install the package
install:
	pip install -e .

# Install the package in development mode
dev:
	pip install -e ".[dev]"
	pre-commit install

# Run the API server
run:
	python run.py

# Run the Celery worker
worker:
	python run_worker.py

# Run the Celery beat scheduler
beat:
	python run_beat.py

# Run the Celery flower monitoring tool
flower:
	python run_flower.py

# Build the Docker images
docker-build:
	docker-compose build

# Start the Docker containers
docker-up:
	docker-compose up -d

# Stop the Docker containers
docker-down:
	docker-compose down

# Clean up temporary files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	rm -f celerybeat-schedule
