DOCKER_COMPOSE = docker-compose
SERVICE_NAME = ml-api
PORT = 8000

.PHONY: install run build up down restart test lint clean logs help

# Install dependencies
install:
	pip install -e .

# Run locally (without Docker)
run:
	uvicorn app.main:app --reload --port $(PORT)

# Docker operations
build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart: down up

# Testing and quality
test:
	pytest tests/

coverage:
	pytest --cov=app --cov-report=term-missing tests/

cov-report:
	pytest --cov=app --cov-report=html tests/
	@echo "Coverage report: file://$(shell pwd)/htmlcov/index.html"

lint:
	pylint --rcfile=pyproject.toml app/

# Cleanup
clean:
	$(DOCKER_COMPOSE) down --volumes --rmi local
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf dist build *.egg-info .coverage htmlcov

# Monitoring
logs:
	$(DOCKER_COMPOSE) logs $(SERVICE_NAME)

# Help
help:
	@echo "Available commands:"
	@echo "  install  - Install project in development mode"
	@echo "  run      - Run locally without Docker"
	@echo "  build    - Build Docker images"
	@echo "  up       - Start containers"
	@echo "  down     - Stop containers"
	@echo "  restart  - Rebuild and restart service"
	@echo "  test     - Run tests"
	@echo "  coverage - Run tests with coverage report"
	@echo "  cov-report - Generate HTML coverage report"
	@echo "  lint     - Run pylint analysis"
	@echo "  clean    - Full cleanup"
	@echo "  logs     - View container logs"
	@echo "  help     - Show this help"
