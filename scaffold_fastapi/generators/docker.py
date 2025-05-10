"""
Generator for Docker-related files.
"""
import os
from pathlib import Path


def generate_docker_files(project_path: Path, db: str, broker: str, stack: str):
    """Generate Docker-related files."""
    # Create Dockerfile
    dockerfile_path = project_path / "Dockerfile"
    with open(dockerfile_path, "w") as f:
        f.write(_get_dockerfile_content())
    
    # Create docker-compose.yml
    docker_compose_path = project_path / "docker-compose.yml"
    with open(docker_compose_path, "w") as f:
        f.write(_get_docker_compose_content(db, broker))
    
    # Create docker directory files
    docker_dir = project_path / "infra" / "docker"
    
    # Create docker-entrypoint.sh
    entrypoint_path = docker_dir / "docker-entrypoint.sh"
    with open(entrypoint_path, "w") as f:
        f.write(_get_docker_entrypoint_content())
    
    # Make entrypoint executable
    os.chmod(entrypoint_path, 0o755)


def _get_dockerfile_content() -> str:
    """Get content for Dockerfile."""
    return '''# Multi-stage build for FastAPI application
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Use custom entrypoint script
COPY infra/docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''


def _get_docker_compose_content(db: str, broker: str) -> str:
    """Get content for docker-compose.yml."""
    services = {
        "app": {
            "build": ".",
            "ports": ["8000:8000"],
            "volumes": ["./:/app"],
            "environment": [
                "DATABASE_URL=${DATABASE_URL}",
                "CELERY_BROKER_URL=${CELERY_BROKER_URL}",
                "CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND}",
            ],
            "depends_on": [],
        },
        "celery_worker": {
            "build": ".",
            "command": "celery -A tasks.celery_app worker --loglevel=info",
            "volumes": ["./:/app"],
            "environment": [
                "DATABASE_URL=${DATABASE_URL}",
                "CELERY_BROKER_URL=${CELERY_BROKER_URL}",
                "CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND}",
            ],
            "depends_on": [],
        },
    }
    
    # Add database service
    if db == "postgresql":
        services["postgres"] = {
            "image": "postgres:15",
            "ports": ["5432:5432"],
            "environment": [
                "POSTGRES_USER=postgres",
                "POSTGRES_PASSWORD=postgres",
                "POSTGRES_DB=app",
            ],
            "volumes": ["postgres_data:/var/lib/postgresql/data"],
        }
        services["app"]["depends_on"].append("postgres")
        services["celery_worker"]["depends_on"].append("postgres")
    
    elif db == "mongodb":
        services["mongodb"] = {
            "image": "mongo:6",
            "ports": ["27017:27017"],
            "environment": [
                "MONGO_INITDB_ROOT_USERNAME=mongo",
                "MONGO_INITDB_ROOT_PASSWORD=mongo",
                "MONGO_INITDB_DATABASE=app",
            ],
            "volumes": ["mongodb_data:/data/db"],
        }
        services["app"]["depends_on"].append("mongodb")
        services["celery_worker"]["depends_on"].append("mongodb")
    
    # Add broker service
    if broker == "redis":
        services["redis"] = {
            "image": "redis:7",
            "ports": ["6379:6379"],
        }
        services["app"]["depends_on"].append("redis")
        services["celery_worker"]["depends_on"].append("redis")
    
    elif broker == "rabbitmq":
        services["rabbitmq"] = {
            "image": "rabbitmq:3-management",
            "ports": ["5672:5672", "15672:15672"],
            "environment": [
                "RABBITMQ_DEFAULT_USER=guest",
                "RABBITMQ_DEFAULT_PASS=guest",
            ],
        }
        services["app"]["depends_on"].append("rabbitmq")
        services["celery_worker"]["depends_on"].append("rabbitmq")
    
    # Build docker-compose.yml content
    volumes = {}
    if db == "postgresql":
        volumes["postgres_data"] = {"driver": "local"}
    elif db == "mongodb":
        volumes["mongodb_data"] = {"driver": "local"}
    
    docker_compose = {
        "version": "3.8",
        "services": services,
        "volumes": volumes,
    }
    
    # Convert to YAML format
    import yaml
    return yaml.dump(docker_compose, sort_keys=False)


def _get_docker_entrypoint_content() -> str:
    """Get content for docker-entrypoint.sh."""
    return '''#!/bin/sh
set -e

# Function to wait for a service to be ready
wait_for_service() {
    host="$1"
    port="$2"
    service_name="$3"
    timeout="${4:-30}"
    
    echo "Waiting for $service_name to be ready..."
    for i in $(seq 1 $timeout); do
        if nc -z "$host" "$port"; then
            echo "$service_name is ready!"
            return 0
        fi
        echo "Waiting for $service_name... $i/$timeout"
        sleep 1
    done
    echo "Timeout reached waiting for $service_name"
    return 1
}

# Wait for dependent services based on environment variables
if [ -n "$DATABASE_URL" ] && echo "$DATABASE_URL" | grep -q "postgresql"; then
    # Extract host and port from DATABASE_URL
    db_host=$(echo "$DATABASE_URL" | sed -E 's/.*@([^:]+):.*/\\1/')
    db_port=$(echo "$DATABASE_URL" | sed -E 's/.*:([0-9]+).*/\\1/')
    wait_for_service "$db_host" "$db_port" "PostgreSQL"
fi

if [ -n "$DATABASE_URL" ] && echo "$DATABASE_URL" | grep -q "mongodb"; then
    # Extract host and port from DATABASE_URL
    db_host=$(echo "$DATABASE_URL" | sed -E 's/.*@([^:]+):.*/\\1/')
    db_port=$(echo "$DATABASE_URL" | sed -E 's/.*:([0-9]+).*/\\1/')
    wait_for_service "$db_host" "$db_port" "MongoDB"
fi

if [ -n "$CELERY_BROKER_URL" ] && echo "$CELERY_BROKER_URL" | grep -q "redis"; then
    # Extract host and port from CELERY_BROKER_URL
    redis_host=$(echo "$CELERY_BROKER_URL" | sed -E 's/.*@([^:]+):.*/\\1/')
    redis_port=$(echo "$CELERY_BROKER_URL" | sed -E 's/.*:([0-9]+).*/\\1/')
    wait_for_service "$redis_host" "$redis_port" "Redis"
fi

if [ -n "$CELERY_BROKER_URL" ] && echo "$CELERY_BROKER_URL" | grep -q "amqp"; then
    # Extract host and port from CELERY_BROKER_URL
    rabbitmq_host=$(echo "$CELERY_BROKER_URL" | sed -E 's/.*@([^:]+):.*/\\1/')
    rabbitmq_port=$(echo "$CELERY_BROKER_URL" | sed -E 's/.*:([0-9]+).*/\\1/')
    wait_for_service "$rabbitmq_host" "$rabbitmq_port" "RabbitMQ"
fi

# Run database migrations if needed
if [ "$1" = "uvicorn" ] || [ "$1" = "gunicorn" ]; then
    echo "Running database migrations..."
    if [ -f "/app/alembic.ini" ]; then
        alembic upgrade head
    fi
fi

# Execute the command
exec "$@"
'''