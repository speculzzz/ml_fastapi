# FastAPI ML Model Service with Keycloak Auth

A lightweight REST API for machine learning model inference built with FastAPI, Docker,  
JWT authentication via Keycloak and modern Python tooling.  
It is a part of Homeworks 9-10 for the OTUS course and is intended for educational purposes.

## Features

- 🚀 FastAPI-powered REST endpoints
- 🔑 JWT Authentication: Integrated with Keycloak
- 🧑‍💻 Role-Based Access:
  - `user` role → `/predict`
  - `admin` role → `/admin`
  - `admin` or `user` role → `/flexible`
- 📦 Docker containerization
- ✅ Pytest with coverage reporting
- 🔍 Pylint code quality checks
- 📊 Makefile for common tasks

## Quick Start

### Prerequisites

- Python 3.12+
- Docker 20.10+
- Keycloak server 26+

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

### Keycloak Configuration
1. Create realm test-realm
2. Create clients:
   ml-fastapi (confidential)
   admin-fastapi (confidential, for admin access)
3. Create roles: admin, user
4. Assign roles to users

## Authentication

### Protected Endpoints

| Endpoint | Role Required | Description         |
|----------|---------------|---------------------|
| /predict | user	        | Iris classification |
| /admin   | admin         | Admin dashboard     | 
| /login   | -             | Get JWT tokens      |

### API Endpoints

_Get Access Token_
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "pass1"}'
```

_Make Prediction (User)_
```bash
curl -X POST http://localhost:8000/predict \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

_Access Admin information_
```bash
curl -X GET http://localhost:8000/admin \
  -H "Authorization: Bearer $ADMIN_TOKEN"
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
