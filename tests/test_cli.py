"""
Tests for the CLI module.
"""
import os
import shutil
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

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
@patch("scaffold_fastapi.cli.validate_option", return_value="postgresql")
@patch("scaffold_fastapi.cli.Path.exists", return_value=False)
@patch("scaffold_fastapi.cli.Path.mkdir")
@patch("scaffold_fastapi.cli.create_project_structure")
@patch("scaffold_fastapi.cli.generate_app_files")
@patch("scaffold_fastapi.cli.generate_celery_tasks")
@patch("scaffold_fastapi.cli.generate_docker_files")
@patch("scaffold_fastapi.cli.generate_terraform_files")
@patch("scaffold_fastapi.cli.generate_env_files")
def test_create_command_with_options(
    mock_env_files,
    mock_terraform_files,
    mock_docker_files,
    mock_celery_tasks,
    mock_app_files,
    mock_create_structure,
    mock_mkdir,
    mock_exists,
    mock_validate,
    mock_install,
    mock_setup,
):
    """Test the create command with options."""
    # Mock sys.exit to prevent test from exiting
    with patch.object(sys, "exit") as mock_exit:
        result = runner.invoke(
            app,
            [
                "create",
                "test-project",
                "--db", "postgresql",
                "--broker", "redis",
                "--stack", "minimal",
            ],
        )
    
    # Check that sys.exit was not called
    mock_exit.assert_not_called()
    
    # Check that the output contains expected strings
    assert "Creating FastAPI project" in result.stdout
    assert "test-project" in result.stdout


@patch("scaffold_fastapi.cli.validate_option")
def test_create_command_invalid_option(mock_validate):
    """Test the create command with invalid option."""
    # Set up the mock to raise SystemExit with code 1
    mock_validate.side_effect = SystemExit(1)
    
    result = runner.invoke(
        app,
        [
            "create",
            "test-project",
            "--db", "invalid-db",
            "--broker", "redis",
            "--stack", "minimal",
        ],
    )
    
    # Check that the exit code is 1 (error)
    assert result.exit_code == 1


@patch("scaffold_fastapi.cli.setup_virtual_env")
@patch("scaffold_fastapi.cli.install_dependencies")
@patch("scaffold_fastapi.cli.validate_option", return_value="postgresql")
@patch("scaffold_fastapi.cli.Path.exists", return_value=True)
@patch("scaffold_fastapi.cli.Confirm.ask", return_value=True)
@patch("scaffold_fastapi.cli.shutil.rmtree")
@patch("scaffold_fastapi.cli.Path.mkdir")
@patch("scaffold_fastapi.cli.create_project_structure")
@patch("scaffold_fastapi.cli.generate_app_files")
@patch("scaffold_fastapi.cli.generate_celery_tasks")
@patch("scaffold_fastapi.cli.generate_docker_files")
@patch("scaffold_fastapi.cli.generate_terraform_files")
@patch("scaffold_fastapi.cli.generate_env_files")
def test_create_command_existing_directory(
    mock_env_files,
    mock_terraform_files,
    mock_docker_files,
    mock_celery_tasks,
    mock_app_files,
    mock_create_structure,
    mock_mkdir,
    mock_rmtree,
    mock_confirm,
    mock_exists,
    mock_validate,
    mock_install,
    mock_setup,
):
    """Test the create command with existing directory."""
    # Mock sys.exit to prevent test from exiting
    with patch.object(sys, "exit") as mock_exit:
        result = runner.invoke(
            app,
            [
                "create",
                "test-project",
                "--db", "postgresql",
                "--broker", "redis",
                "--stack", "minimal",
            ],
        )
    
    # Check that sys.exit was not called
    mock_exit.assert_not_called()
    
    # Check that rmtree was called (directory was removed)
    mock_rmtree.assert_called_once()
    
    # Check that the output contains expected strings
    assert "Creating FastAPI project" in result.stdout
    assert "test-project" in result.stdout