# FastAPI Project Scaffolder

[![Python Tests](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/python-test.yml/badge.svg)](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/python-test.yml)
[![Docker Compose Test](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/docker-compose-test.yml/badge.svg)](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/docker-compose-test.yml)
[![Publish to GHCR](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/ghcr-publish.yml/badge.svg)](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/ghcr-publish.yml)
[![Publish to PyPI](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/pypi-publish.yml)
[![PyPI version](https://badge.fury.io/py/sc affold-fastapi.svg)](https://badge.fury.io/py/scaffold-fastapi)
[![Python Versions](https://img.shields.io/pypi/pyversions/scaffold-fastapi.svg)](https://pypi.org/project/scaffold-fastapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/KenMwaura1/scaffold-fastapi.svg)](https://github.com/KenMwaura1/scaffold-fastapi/issues)

![Crushing the Command Line: How I Used Amazon Q to Build a Smarter FastAPI Scaffolder](media/Crushing%20the%20Command%20Line%3A%20How%20I%20Used%20Amazon%20Q%20to%20Build%20a%20Smarter%20FastAPI%20Scaffolder.png)

A command-line tool to generate FastAPI project scaffolds with various database, message broker, and deployment options.

### **Read the full article on [DEV](hhttps://dev.to/ken_mwaura1/crushing-the-command-line-how-i-used-amazon-q-to-build-a-smarter-fastapi-scaffolder-3c45).**

Link to the pyPI package: [scaffold-fastapi](https://pypi.org/project/scaffold-fastapi/)

## Features

- **Database Support**: PostgreSQL, MongoDB, SQLite
- **Message Broker**: Redis, RabbitMQ
- **Deployment Stacks**: Minimal, Full (AWS ECS), Serverless
- **Production-Ready**: Docker, Terraform, Helm charts
- **Dependency Management**: Uses `uv` for virtual environments and package installation

## Installation

```bash
# Install from PyPI
pip install scaffold-fastapi

# Or using uv
uv pip install scaffold-fastapi

# Or using Docker
docker run --rm -it ghcr.io/kenmwaura1/scaffold-fastapi:latest --help
```

![Crushing the Command Line: How I Used Amazon Q to Build a Smarter FastAPI Scaffolder](https://github.com/KenMwaura1/scaffold-fastapi/raw/main/media/2025-05-10_16-49.png)

## Usage

```bash
# Basic usage
scaffold-fastapi my-project --db=postgresql --broker=redis --stack=full

# Interactive mode (will prompt for missing options)
scaffold-fastapi my-project

# Using Docker with volume mount to create project in current directory
docker run --rm -it -v $(pwd):/workspace -w /workspace ghcr.io/kenmwaura1/scaffold-fastapi:latest my-project
```

### Command Options

- `--db`: Database type (postgresql, mongodb, sqlite)
- `--broker`: Message broker (redis, rabbitmq)
- `--stack`: Deployment stack (minimal, full, serverless)
  
![Crushing the Command Line: How I Used Amazon Q to Build a Smarter FastAPI Scaffolder](https://github.com/KenMwaura1/scaffold-fastapi/raw/main/media/2025-05-10_16-48.png)

## Project Structure

The generated project will have the following structure:

```shell
my-project/
├── app/
│   ├── api/
│   │   └── v1/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── main.py
├── tasks/
│   ├── celery_app.py
│   └── sample_tasks.py
├── infra/
│   ├── docker/
│   ├── terraform/
│   └── helm/
├── tests/
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

![Crushing the Command Line: How I Used Amazon Q to Build a Smarter FastAPI Scaffolder](https://github.com/KenMwaura1/scaffold-fastapi/raw/main/media/2025-05-10_16-51.png)

## Development

```bash
# Clone the repository
git clone https://github.com/KenMwaura1/scaffold-fastapi.git
cd scaffold-fastapi

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .
```

## CI/CD

This project uses GitHub Actions for:

- **Python Tests**: Runs tests on Python code, including formatting, linting, and unit tests
- **Docker Compose Testing**: Validates and tests the generated Docker Compose files
- **Container Publishing**: Builds and publishes Docker images to GitHub Container Registry
- **PyPI Publishing**: Automatically publishes to PyPI when pushing to main or creating a tag
- **Dependency Updates**: Weekly checks and updates dependencies

## Publishing to PyPI

To publish this package to PyPI, you need to:

1. Create a PyPI API token (see [pypi_instructions.md](pypi_instructions.md))
2. Add the token to GitHub Secrets as `PYPI_API_TOKEN`
3. Push to main or create a tag starting with `v` (e.g., `v0.1.0`)

## Using the Docker Image

The Docker image is published to GitHub Container Registry and can be used as follows:

```bash
# Pull the latest image
docker pull ghcr.io/kenmwaura1/scaffold-fastapi:latest

# Create a new project
docker run --rm -it -v $(pwd):/workspace -w /workspace ghcr.io/kenmwaura1/scaffold-fastapi:latest my-project
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
