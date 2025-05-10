"""
FastAPI Project Scaffolder

A tool to generate FastAPI project scaffolds with various database,
message broker, and deployment options.
"""

__version__ = "0.1.0"

# Import main components for easier access
from scaffold_fastapi.generators import (
    generate_app_files,
    generate_celery_tasks,
    generate_docker_files,
    generate_env_files,
    generate_terraform_files,
)
