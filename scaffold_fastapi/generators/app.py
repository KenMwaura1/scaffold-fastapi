"""
Generator for FastAPI application files.
"""

from pathlib import Path


def generate_app_files(project_path: Path, db: str, broker: str, stack: str):
    """Generate FastAPI application files."""
    app_dir = project_path / "app"

    # Create main.py
    main_py_path = app_dir / "main.py"
    with open(main_py_path, "w") as f:
        f.write(_get_main_py_content())

    # Create core files
    core_dir = app_dir / "core"

    # Create config.py
    config_py_path = core_dir / "config.py"
    with open(config_py_path, "w") as f:
        f.write(_get_config_py_content(db, broker))

    # Create database.py
    db_py_path = app_dir / "db" / "database.py"
    with open(db_py_path, "w") as f:
        f.write(_get_database_py_content(db))

    # Create models
    models_dir = app_dir / "models"
    base_model_path = models_dir / "base.py"
    with open(base_model_path, "w") as f:
        f.write(_get_base_model_content(db))

    # Create API router
    api_dir = app_dir / "api"
    api_init_path = api_dir / "__init__.py"
    with open(api_init_path, "w") as f:
        f.write(_get_api_init_content())

    # Create v1 API router
    v1_dir = api_dir / "v1"
    v1_dir.mkdir(exist_ok=True)
    v1_init_path = v1_dir / "__init__.py"
    with open(v1_init_path, "w") as f:
        f.write(_get_v1_init_content())

    # Create health endpoint
    health_path = v1_dir / "health.py"
    with open(health_path, "w") as f:
        f.write(_get_health_py_content())


def _get_main_py_content() -> str:
    """Get content for main.py."""
    return '''"""
FastAPI application entry point.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.db.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )
    
    # Set up CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_STR)
    
    @application.on_event("startup")
    async def startup_event():
        """Initialize resources on startup."""
        logger.info("Starting up application...")
        await init_db()
    
    @application.on_event("shutdown")
    async def shutdown_event():
        """Clean up resources on shutdown."""
        logger.info("Shutting down application...")
    
    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
'''


def _get_config_py_content(db: str, broker: str) -> str:
    """Get content for config.py."""
    db_url = {
        "postgresql": "postgresql+asyncpg://postgres:postgres@postgres:5432/app",
        "mongodb": "mongodb://mongo:mongo@mongodb:27017/app",
        "sqlite": "sqlite+aiosqlite:///./app.db",
    }[db]

    broker_url = {
        "redis": "redis://redis:6379/0",
        "rabbitmq": "amqp://guest:guest@rabbitmq:5672//",
    }[broker]

    return f'''"""
Application configuration settings.
"""
import os
import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    
    # CORS settings
    CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["http://localhost:8000", "http://localhost:3000"]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Project metadata
    PROJECT_NAME: str = "FastAPI App"
    PROJECT_DESCRIPTION: str = "FastAPI application with {db} and {broker}"
    VERSION: str = "0.1.0"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "{db_url}")
    
    # Celery settings
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "{broker_url}")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "{broker_url}")
    
    class Config:
        """Pydantic config."""
        
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()
'''


def _get_database_py_content(db: str) -> str:
    """Get content for database.py."""
    if db == "postgresql" or db == "sqlite":
        return '''"""
Database connection and session management.
"""
import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database connection."""
    try:
        # Test database connection
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None)
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
'''
    elif db == "mongodb":
        return '''"""
MongoDB connection and client management.
"""
import logging
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from app.core.config import settings

logger = logging.getLogger(__name__)

# MongoDB client
client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None


async def get_database() -> AsyncIOMotorDatabase:
    """
    Get database instance.
    
    Returns:
        AsyncIOMotorDatabase: MongoDB database instance
    """
    return db


async def init_db() -> None:
    """Initialize MongoDB connection."""
    global client, db
    
    try:
        # Parse database name from connection string
        db_name = settings.DATABASE_URL.split("/")[-1]
        
        # Create client
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        
        # Verify connection
        await client.admin.command("ping")
        
        # Get database
        db = client[db_name]
        
        logger.info("MongoDB connection established")
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error initializing MongoDB: {e}")
        raise
'''


def _get_base_model_content(db: str) -> str:
    """Get content for base model."""
    if db == "postgresql" or db == "sqlite":
        return '''"""
Base SQLAlchemy model.
"""
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for all SQLAlchemy models."""
    
    id: Any
    __name__: str
    
    # Create table name automatically
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        return cls.__name__.lower()
    
    # Add created_at and updated_at columns to all models
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
'''
    elif db == "mongodb":
        return '''"""
Base Pydantic model for MongoDB documents.
"""
from datetime import datetime
from typing import Any, Dict, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic models."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        """Validate ObjectId."""
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        """Get Pydantic core schema."""
        from pydantic_core import PydanticCustomError, core_schema
        
        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise PydanticCustomError("invalid_objectid", "Invalid ObjectId")
            return ObjectId(value)
        
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.string_schema(
                serialization=core_schema.to_string_ser_schema(),
                parsers=[validate_from_str],
            ),
        ])


class MongoBaseModel(BaseModel):
    """Base model for MongoDB documents."""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_serializer("id")
    def serialize_id(self, id: PyObjectId) -> str:
        """Serialize ObjectId to string."""
        return str(id)
    
    class Config:
        """Pydantic config."""
        
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
'''


def _get_api_init_content() -> str:
    """Get content for API __init__.py."""
    return '''"""
API routes.
"""
from fastapi import APIRouter

from app.api.v1 import api_router as api_v1_router

# Create API router
api_router = APIRouter()

# Include API v1 router
api_router.include_router(api_v1_router)
'''


def _get_v1_init_content() -> str:
    """Get content for v1 __init__.py."""
    return '''"""
API v1 routes.
"""
from fastapi import APIRouter

from app.api.v1.health import router as health_router

# Create API v1 router
api_router = APIRouter()

# Include health router
api_router.include_router(health_router, tags=["health"])
'''


def _get_health_py_content() -> str:
    """Get content for health.py."""
    return '''"""
Health check endpoints.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.db.database import get_db

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Health check response
    """
    return {
        "status": "ok",
        "version": "0.1.0",
    }


@router.get("/health/db", response_model=HealthResponse)
async def db_health_check(db=Depends(get_db)):
    """
    Database health check endpoint.
    
    Args:
        db: Database session
    
    Returns:
        HealthResponse: Health check response
    """
    return {
        "status": "ok",
        "version": "0.1.0",
    }
'''
