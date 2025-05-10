"""
Tests for the CLI module.
"""

import shutil
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from scaffold_fastapi.cli import app

runner = CliRunner()


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary directory for project generation."""
    project_dir = tmp_path / "test-project"
    yield project_dir
    # Clean up
    if project_dir.exists():
        shutil.rmtree(project_dir)


@patch("scaffold_fastapi.cli.setup_virtual_env")
@patch("scaffold_fastapi.cli.install_dependencies")
def test_create_command_help(mock_install, mock_setup):
    """Test the create command help text."""
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0
    assert "Create a new FastAPI project scaffold" in result.stdout


@patch("scaffold_fastapi.cli.setup_virtual_env")
@patch("scaffold_fastapi.cli.install_dependencies")
def test_create_command_with_options(mock_install, mock_setup, temp_project_dir):
    """Test the create command with options."""
    with patch("scaffold_fastapi.cli.Path.exists", return_value=False):
        with patch("scaffold_fastapi.cli.Path.mkdir"):
            result = runner.invoke(
                app,
                [
                    "create",
                    "test-project",
                    "--db",
                    "postgresql",
                    "--broker",
                    "redis",
                    "--stack",
                    "minimal",
                ],
            )

    assert result.exit_code == 0
    assert "Creating FastAPI project" in result.stdout
    assert "Database: postgresql" in result.stdout
    assert "Message Broker: redis" in result.stdout
    assert "Deployment Stack: minimal" in result.stdout


@patch("scaffold_fastapi.cli.setup_virtual_env")
@patch("scaffold_fastapi.cli.install_dependencies")
def test_create_command_invalid_option(mock_install, mock_setup):
    """Test the create command with invalid option."""
    result = runner.invoke(
        app,
        [
            "create",
            "test-project",
            "--db",
            "invalid-db",
            "--broker",
            "redis",
            "--stack",
            "minimal",
        ],
    )

    assert result.exit_code == 1
    assert "Invalid database" in result.stdout


@patch("scaffold_fastapi.cli.Confirm.ask", return_value=True)
@patch("scaffold_fastapi.cli.setup_virtual_env")
@patch("scaffold_fastapi.cli.install_dependencies")
def test_create_command_existing_directory(
    mock_install, mock_setup, mock_confirm, temp_project_dir
):
    """Test the create command with existing directory."""
    # Create the directory
    temp_project_dir.mkdir(parents=True, exist_ok=True)

    with patch("scaffold_fastapi.cli.Path.exists", return_value=True):
        with patch("scaffold_fastapi.cli.shutil.rmtree"):
            result = runner.invoke(
                app,
                [
                    "create",
                    str(temp_project_dir),
                    "--db",
                    "postgresql",
                    "--broker",
                    "redis",
                    "--stack",
                    "minimal",
                ],
            )

    assert result.exit_code == 0
    assert "Creating FastAPI project" in result.stdout
