# FastAPI ML Model Service

A lightweight REST API for machine learning model inference built with FastAPI, Docker, and modern Python tooling.  
It is a part of Homework 9 for the OTUS course and is intended for educational purposes.

## Features

- 🚀 FastAPI-powered REST endpoints
- 📦 Docker containerization
- ✅ Pytest with coverage reporting
- 🔍 Pylint code quality checks
- 📊 Makefile for common tasks

## Quick Start

### Prerequisites

- Python 3.12+
- Docker 20.10+

### Installation

```bash
# Clone repository
git clone https://github.com/speculzzz/ml_fastapi.git
cd ml_fastapi

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running the Service

```bash
# Development mode (auto-reload)
make run

# Production mode with Docker
make build && make up
```

## Project Structure

```
ml_fastapi/
├── app/               - Application code
│   ├── __init__.py
│   ├── main.py        - FastAPI app
│   ├── models.py      - ML model
│   └── schemas.py     - Pydantic models
├── tests/             - Test cases
├── Dockerfile         - Container configuration
├── docker-compose.yml - Service orchestration
├── Makefile           - Development commands
├── pyproject.toml     - Build configuration
└── setup.py           - Package metadata
```

## Available Commands

```bash
# Run tests with coverage
make coverage

# Generate HTML coverage report
make cov-report

# Lint code
make lint

# Clean project
make clean
```

## API Documentation

Access interactive docs when service is running:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

- **speculzzz** (speculzzz@gmail.com)

---

Feel free to use it!
