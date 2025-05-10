"""
Tests for the CLI module.
"""

import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from scaffold_fastapi.cli import app, validate_option, DATABASES, BROKERS, STACKS

runner = CliRunner()


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary directory for project generation."""
    project_dir = tmp_path / "test-project"
    yield project_dir
    # Clean up
    if project_dir.exists():
        shutil.rmtree(project_dir)


def test_validate_option_valid():
    """Test validate_option with valid input."""
    result = validate_option("postgresql", DATABASES, "database")
    assert result == "postgresql"


def test_validate_option_invalid():
    """Test validate_option with invalid input."""
    with pytest.raises(SystemExit):
        validate_option("invalid-db", DATABASES, "database")


def test_databases_constants():
    """Test that the database constants are defined correctly."""
    assert "postgresql" in DATABASES
    assert "mongodb" in DATABASES
    assert "sqlite" in DATABASES
    assert len(DATABASES) == 3


def test_brokers_constants():
    """Test that the broker constants are defined correctly."""
    assert "redis" in BROKERS
    assert "rabbitmq" in BROKERS
    assert len(BROKERS) == 2


def test_stacks_constants():
    """Test that the stack constants are defined correctly."""
    assert "minimal" in STACKS
    assert "full" in STACKS
    assert "serverless" in STACKS
    assert len(STACKS) == 3


def test_create_command_help():
    """Test the create command help text."""
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0
    assert "Create a new FastAPI project scaffold" in result.stdout
    assert "--db" in result.stdout
    assert "--broker" in result.stdout
    assert "--stack" in result.stdout
