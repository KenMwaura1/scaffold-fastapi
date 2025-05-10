#!/usr/bin/env python3
"""
FastAPI Project Scaffolder CLI

A command-line tool to generate FastAPI project scaffolds with various database,
message broker, and deployment options.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm

app = typer.Typer(help="FastAPI Project Scaffolder CLI")
console = Console()

# Supported options
DATABASES = ["postgresql", "mongodb", "sqlite"]
BROKERS = ["redis", "rabbitmq"]
STACKS = ["minimal", "full", "serverless"]

def validate_option(value: str, valid_options: List[str], option_type: str) -> str:
    """Validate and prompt for option if invalid or not provided."""
    if value is None:
        console.print(f"Select a {option_type}:")
        for i, option in enumerate(valid_options, 1):
            console.print(f"  {i}. {option}")
        
        selected = Prompt.ask(
            f"Enter your choice (1-{len(valid_options)})",
            choices=[str(i) for i in range(1, len(valid_options) + 1)]
        )
        return valid_options[int(selected) - 1]
    
    if value not in valid_options:
        console.print(f"[bold red]Error:[/] Invalid {option_type} '{value}'")
        console.print(f"Valid options: {', '.join(valid_options)}")
        sys.exit(1)
    
    return value

def create_project_structure(project_path: Path):
    """Create the basic project directory structure."""
    directories = [
        "app",
        "app/api",
        "app/core",
        "app/db",
        "app/models",
        "app/schemas",
        "tasks",
        "infra",
        "infra/docker",
        "infra/terraform",
        "infra/helm",
        "tests",
    ]
    
    for directory in directories:
        (project_path / directory).mkdir(parents=True, exist_ok=True)
        (project_path / directory / "__init__.py").touch()

def setup_virtual_env(project_path: Path):
    """Set up a virtual environment using uv."""
    console.print("Setting up virtual environment with uv...")
    try:
        subprocess.run(["uv", "venv", str(project_path / ".venv")], check=True)
        console.print("[green]Virtual environment created successfully![/]")
    except subprocess.CalledProcessError:
        console.print("[bold red]Failed to create virtual environment.[/]")
        console.print("Make sure 'uv' is installed: pip install uv")
        sys.exit(1)
    except FileNotFoundError:
        console.print("[bold red]Error:[/] 'uv' command not found.")
        console.print("Please install uv: pip install uv")
        sys.exit(1)

def install_dependencies(project_path: Path, db: str, broker: str, stack: str):
    """Install project dependencies using uv."""
    console.print("Installing dependencies...")
    
    # Base dependencies
    base_deps = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic[email]",
        "python-dotenv",
        "celery",
        "pytest",
        "httpx",
    ]
    
    # Database-specific dependencies
    db_deps = {
        "postgresql": ["sqlalchemy", "asyncpg", "alembic"],
        "mongodb": ["motor", "pymongo"],
        "sqlite": ["sqlalchemy", "aiosqlite", "alembic"],
    }
    
    # Broker-specific dependencies
    broker_deps = {
        "redis": ["redis", "hiredis"],
        "rabbitmq": ["pika", "aio-pika"],
    }
    
    # Stack-specific dependencies
    stack_deps = {
        "full": ["gunicorn", "prometheus-client", "python-json-logger"],
        "serverless": ["mangum"],
        "minimal": [],
    }
    
    all_deps = base_deps + db_deps[db] + broker_deps[broker] + stack_deps[stack]
    
    try:
        subprocess.run(
            ["uv", "pip", "install"] + all_deps,
            check=True,
            env={**os.environ, "VIRTUAL_ENV": str(project_path / ".venv")}
        )
        
        # Create requirements.txt
        subprocess.run(
            ["uv", "pip", "freeze"],
            check=True,
            env={**os.environ, "VIRTUAL_ENV": str(project_path / ".venv")},
            stdout=open(project_path / "requirements.txt", "w")
        )
        
        console.print("[green]Dependencies installed successfully![/]")
    except subprocess.CalledProcessError:
        console.print("[bold red]Failed to install dependencies.[/]")
        sys.exit(1)

@app.command()
def create(
    name: str = typer.Argument(..., help="Project name"),
    db: Optional[str] = typer.Option(None, help="Database type: postgresql, mongodb, or sqlite"),
    broker: Optional[str] = typer.Option(None, help="Message broker: redis or rabbitmq"),
    stack: Optional[str] = typer.Option(None, help="Deployment stack: minimal, full, or serverless"),
):
    """Create a new FastAPI project scaffold."""
    # Validate options or prompt for them
    db = validate_option(db, DATABASES, "database")
    broker = validate_option(broker, BROKERS, "message broker")
    stack = validate_option(stack, STACKS, "deployment stack")
    
    console.print(f"Creating FastAPI project: [bold green]{name}[/]")
    console.print(f"Database: [bold]{db}[/]")
    console.print(f"Message Broker: [bold]{broker}[/]")
    console.print(f"Deployment Stack: [bold]{stack}[/]")
    
    # Create project directory
    project_path = Path(name)
    if project_path.exists():
        overwrite = Confirm.ask(
            f"Directory '{name}' already exists. Overwrite?",
            default=False
        )
        if overwrite:
            shutil.rmtree(project_path)
        else:
            console.print("Aborted.")
            sys.exit(1)
    
    project_path.mkdir()
    
    # Create project structure
    create_project_structure(project_path)
    
    # Generate project files based on selected options
    from scaffold_fastapi.generators import (
        generate_app_files,
        generate_celery_tasks,
        generate_docker_files,
        generate_terraform_files,
        generate_env_files,
    )
    
    generate_app_files(project_path, db, broker, stack)
    generate_celery_tasks(project_path, broker)
    generate_docker_files(project_path, db, broker, stack)
    generate_terraform_files(project_path, stack)
    generate_env_files(project_path, db, broker)
    
    # Set up virtual environment and install dependencies
    setup_virtual_env(project_path)
    install_dependencies(project_path, db, broker, stack)
    
    console.print("\n[bold green]Project created successfully![/]")
    console.print(f"To get started, run:\n")
    console.print(f"  cd {name}")
    console.print(f"  source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
    console.print(f"  uvicorn app.main:app --reload")

if __name__ == "__main__":
    app()