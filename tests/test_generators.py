"""
Tests for the generator modules.
"""

import os
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from scaffold_fastapi.generators import (
    generate_app_files,
    generate_celery_tasks,
    generate_docker_files,
    generate_terraform_files,
    generate_env_files,
)


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary directory for project generation."""
    project_dir = tmp_path / "test-project"
    project_dir.mkdir()

    # Create required subdirectories
    (project_dir / "app").mkdir()
    (project_dir / "app" / "api").mkdir()
    (project_dir / "app" / "core").mkdir()
    (project_dir / "app" / "db").mkdir()
    (project_dir / "app" / "models").mkdir()
    (project_dir / "tasks").mkdir()
    (project_dir / "infra").mkdir()
    (project_dir / "infra" / "docker").mkdir()
    (project_dir / "infra" / "terraform").mkdir()

    return project_dir


def test_generate_env_files(temp_project_dir):
    """Test generating environment files."""
    generate_env_files(temp_project_dir, "postgresql", "redis")

    # Check that files were created
    assert (temp_project_dir / ".env").exists()
    assert (temp_project_dir / ".env.example").exists()

    # Check that .env contains the right variables
    with open(temp_project_dir / ".env") as f:
        content = f.read()
        assert "DATABASE_URL" in content
        assert "CELERY_BROKER_URL" in content
        assert "postgresql+asyncpg" in content
        assert "redis://redis:6379/0" in content


def test_generate_env_files_mongodb(temp_project_dir):
    """Test generating environment files with MongoDB."""
    generate_env_files(temp_project_dir, "mongodb", "redis")

    # Check that files were created
    assert (temp_project_dir / ".env").exists()
    assert (temp_project_dir / ".env.example").exists()

    # Check that .env contains the right variables
    with open(temp_project_dir / ".env") as f:
        content = f.read()
        assert "DATABASE_URL" in content
        assert "CELERY_BROKER_URL" in content
        assert "mongodb://" in content
        assert "redis://redis:6379/0" in content


def test_generate_env_files_rabbitmq(temp_project_dir):
    """Test generating environment files with RabbitMQ."""
    generate_env_files(temp_project_dir, "postgresql", "rabbitmq")

    # Check that files were created
    assert (temp_project_dir / ".env").exists()
    assert (temp_project_dir / ".env.example").exists()

    # Check that .env contains the right variables
    with open(temp_project_dir / ".env") as f:
        content = f.read()
        assert "DATABASE_URL" in content
        assert "CELERY_BROKER_URL" in content
        assert "postgresql+asyncpg" in content
        assert "amqp://" in content
