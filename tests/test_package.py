"""
Tests for the package structure and metadata.
"""

import importlib.metadata
import importlib.util
import os
from pathlib import Path

import pytest


def test_package_importable():
    """Test that the package can be imported."""
    import scaffold_fastapi

    assert scaffold_fastapi.__version__ is not None


def test_generators_importable():
    """Test that the generators module can be imported."""
    from scaffold_fastapi import generators

    assert generators.generate_app_files is not None
    assert generators.generate_celery_tasks is not None
    assert generators.generate_docker_files is not None
    assert generators.generate_terraform_files is not None
    assert generators.generate_env_files is not None


def test_cli_importable():
    """Test that the CLI module can be imported."""
    from scaffold_fastapi import cli

    assert cli.app is not None
    assert cli.validate_option is not None
    assert cli.create_project_structure is not None


def test_package_structure():
    """Test that the package has the expected structure."""
    package_dir = Path(__file__).parent.parent / "scaffold_fastapi"
    assert package_dir.exists()
    assert (package_dir / "__init__.py").exists()
    assert (package_dir / "cli.py").exists()
    assert (package_dir / "generators").exists()
    assert (package_dir / "generators" / "__init__.py").exists()
    assert (package_dir / "generators" / "app.py").exists()
    assert (package_dir / "generators" / "celery.py").exists()
    assert (package_dir / "generators" / "docker.py").exists()
    assert (package_dir / "generators" / "env.py").exists()
    assert (package_dir / "generators" / "terraform.py").exists()


def test_pyproject_toml_exists():
    """Test that pyproject.toml exists."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    assert pyproject_path.exists()
    with open(pyproject_path) as f:
        content = f.read()
        assert "[build-system]" in content
        assert "[project]" in content
        assert "scaffold-fastapi" in content
