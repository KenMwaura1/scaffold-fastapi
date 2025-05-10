# FastAPI Project Scaffolder

A command-line tool to generate FastAPI project scaffolds with various database, message broker, and deployment options.

## Features

- **Database Support**: PostgreSQL, MongoDB, SQLite
- **Message Broker**: Redis, RabbitMQ
- **Deployment Stacks**: Minimal, Full (AWS ECS), Serverless
- **Production-Ready**: Docker, Terraform, Helm charts
- **Dependency Management**: Uses `uv` for virtual environments and package installation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/scaffold-fastapi.git
cd scaffold-fastapi

# Install the package
pip install -e .
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
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .
```

## License

MIT