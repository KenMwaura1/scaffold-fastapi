"""
Tests for the generator modules.
"""

import pytest

from scaffold_fastapi.generators import (
    generate_app_files,
    generate_celery_tasks,
    generate_docker_files,
    generate_env_files,
    generate_terraform_files,
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


def test_generate_app_files(temp_project_dir):
    """Test generating app files."""
    generate_app_files(temp_project_dir, "postgresql", "redis", "minimal")

    # Check that files were created
    assert (temp_project_dir / "app" / "main.py").exists()
    assert (temp_project_dir / "app" / "core" / "config.py").exists()
    assert (temp_project_dir / "app" / "db" / "database.py").exists()
    assert (temp_project_dir / "app" / "models" / "base.py").exists()
    assert (temp_project_dir / "app" / "api" / "__init__.py").exists()
    assert (temp_project_dir / "app" / "api" / "v1" / "__init__.py").exists()
    assert (temp_project_dir / "app" / "api" / "v1" / "health.py").exists()


def test_generate_celery_tasks(temp_project_dir):
    """Test generating Celery task files."""
    generate_celery_tasks(temp_project_dir, "redis")

    # Check that files were created
    assert (temp_project_dir / "tasks" / "celery_app.py").exists()
    assert (temp_project_dir / "tasks" / "sample_tasks.py").exists()

    # Check that Redis is configured
    with open(temp_project_dir / "tasks" / "celery_app.py") as f:
        content = f.read()
        assert "redis://redis:6379/0" in content


def test_generate_docker_files(temp_project_dir):
    """Test generating Docker files."""
    generate_docker_files(temp_project_dir, "postgresql", "redis", "minimal")

    # Check that files were created
    assert (temp_project_dir / "Dockerfile").exists()
    assert (temp_project_dir / "docker-compose.yml").exists()
    assert (temp_project_dir / "infra" / "docker" / "docker-entrypoint.sh").exists()

    # Check that docker-compose.yml contains the right services
    with open(temp_project_dir / "docker-compose.yml") as f:
        content = f.read()
        assert "postgres" in content
        assert "redis" in content
        assert "app" in content
        assert "celery_worker" in content


def test_generate_terraform_files(temp_project_dir):
    """Test generating Terraform files."""
    generate_terraform_files(temp_project_dir, "full")

    # Check that files were created
    assert (temp_project_dir / "infra" / "terraform" / "main.tf").exists()
    assert (temp_project_dir / "infra" / "terraform" / "variables.tf").exists()
    assert (temp_project_dir / "infra" / "terraform" / "outputs.tf").exists()
    assert (
        temp_project_dir / "infra" / "terraform" / "modules" / "ecs" / "main.tf"
    ).exists()
    assert (
        temp_project_dir / "infra" / "terraform" / "modules" / "ecs" / "variables.tf"
    ).exists()
    assert (
        temp_project_dir / "infra" / "terraform" / "modules" / "ecs" / "outputs.tf"
    ).exists()


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
