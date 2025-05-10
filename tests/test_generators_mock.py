"""
Tests for the generator modules using mocks.
"""

import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

import pytest

from scaffold_fastapi.generators import (
    generate_app_files,
    generate_celery_tasks,
    generate_docker_files,
    generate_terraform_files,
    generate_env_files,
)


@pytest.fixture
def mock_path():
    """Create a mock Path object."""
    mock = MagicMock(spec=Path)
    mock.__truediv__.return_value = mock  # Make / operator return self
    return mock


def test_generate_app_files_calls_open(mock_path):
    """Test that generate_app_files calls open."""
    m = mock_open()
    with patch("builtins.open", m):
        generate_app_files(mock_path, "postgresql", "redis", "minimal")

    # Check that open was called multiple times
    assert m.call_count > 0


def test_generate_celery_tasks_calls_open(mock_path):
    """Test that generate_celery_tasks calls open."""
    m = mock_open()
    with patch("builtins.open", m):
        generate_celery_tasks(mock_path, "redis")

    # Check that open was called multiple times
    assert m.call_count > 0


def test_generate_docker_files_calls_open(mock_path):
    """Test that generate_docker_files calls open."""
    m = mock_open()
    with patch("builtins.open", m):
        with patch("os.chmod"):  # Mock chmod to avoid permission issues
            generate_docker_files(mock_path, "postgresql", "redis", "minimal")

    # Check that open was called multiple times
    assert m.call_count > 0


def test_generate_terraform_files_calls_open(mock_path):
    """Test that generate_terraform_files calls open."""
    m = mock_open()
    with patch("builtins.open", m):
        generate_terraform_files(mock_path, "full")

    # Check that open was called multiple times
    assert m.call_count > 0


def test_generate_env_files_calls_open(mock_path):
    """Test that generate_env_files calls open."""
    m = mock_open()
    with patch("builtins.open", m):
        generate_env_files(mock_path, "postgresql", "redis")

    # Check that open was called multiple times
    assert m.call_count > 0
