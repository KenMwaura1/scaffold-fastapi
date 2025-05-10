"""
Generator for environment files.
"""
from pathlib import Path


def generate_env_files(project_path: Path, db: str, broker: str):
    """Generate environment files."""
    # Create .env.example file
    env_example_path = project_path / ".env.example"
    with open(env_example_path, "w") as f:
        f.write(_get_env_example_content(db, broker))
    
    # Create .env file
    env_path = project_path / ".env"
    with open(env_path, "w") as f:
        f.write(_get_env_content(db, broker))


def _get_env_example_content(db: str, broker: str) -> str:
    """Get content for .env.example file."""
    db_url = {
        "postgresql": "postgresql+asyncpg://postgres:postgres@postgres:5432/app",
        "mongodb": "mongodb://mongo:mongo@mongodb:27017/app",
        "sqlite": "sqlite+aiosqlite:///./app.db",
    }[db]
    
    broker_url = {
        "redis": "redis://redis:6379/0",
        "rabbitmq": "amqp://guest:guest@rabbitmq:5672//",
    }[broker]
    
    return f'''# Application settings
PROJECT_NAME=FastAPI App
SECRET_KEY=change-me-in-production

# API settings
API_V1_STR=/api/v1

# CORS settings
CORS_ORIGINS=http://localhost:8000,http://localhost:3000

# Database settings
DATABASE_URL={db_url}

# Celery settings
CELERY_BROKER_URL={broker_url}
CELERY_RESULT_BACKEND={broker_url}
'''


def _get_env_content(db: str, broker: str) -> str:
    """Get content for .env file."""
    import secrets
    
    db_url = {
        "postgresql": "postgresql+asyncpg://postgres:postgres@postgres:5432/app",
        "mongodb": "mongodb://mongo:mongo@mongodb:27017/app",
        "sqlite": "sqlite+aiosqlite:///./app.db",
    }[db]
    
    broker_url = {
        "redis": "redis://redis:6379/0",
        "rabbitmq": "amqp://guest:guest@rabbitmq:5672//",
    }[broker]
    
    return f'''# Application settings
PROJECT_NAME=FastAPI App
SECRET_KEY={secrets.token_urlsafe(32)}

# API settings
API_V1_STR=/api/v1

# CORS settings
CORS_ORIGINS=http://localhost:8000,http://localhost:3000

# Database settings
DATABASE_URL={db_url}

# Celery settings
CELERY_BROKER_URL={broker_url}
CELERY_RESULT_BACKEND={broker_url}
'''