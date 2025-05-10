# FastAPI Project Scaffolder

[![Test](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/test.yml/badge.svg)](https://github.com/KenMwaura1/scaffold-fastapi/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/scaffold-fastapi.svg)](https://badge.fury.io/py/scaffold-fastapi)
[![Python Versions](https://img.shields.io/pypi/pyversions/scaffold-fastapi.svg)](https://pypi.org/project/scaffold-fastapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool to generate FastAPI project scaffolds with various database, message broker, and deployment options.

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
```

## Usage

```bash
# Basic usage
scaffold-fastapi create my-project --db=postgresql --broker=redis --stack=full

# Interactive mode (will prompt for missing options)
scaffold-fastapi create my-project
```

### Command Options

- `--db`: Database type (postgresql, mongodb, sqlite)
- `--broker`: Message broker (redis, rabbitmq)
- `--stack`: Deployment stack (minimal, full, serverless)

## Project Structure

The generated project will have the following structure:

```
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

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/scaffold-fastapi.git
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

- **Testing**: Runs tests on Python 3.9, 3.10, and 3.11 for both main and dev branches
- **Publishing**: Automatically publishes to PyPI when pushing to main or creating a tag
- **Dependencies**: Weekly checks and updates dependencies

## Publishing to PyPI

To publish this package to PyPI, you need to:

1. Create a PyPI API token (see [pypi_instructions.md](pypi_instructions.md))
2. Add the token to GitHub Secrets as `PYPI_API_TOKEN`
3. Push to main or create a tag starting with `v` (e.g., `v0.1.0`)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
