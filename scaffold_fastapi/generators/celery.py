"""
Generator for Celery task files.
"""

from pathlib import Path


def generate_celery_tasks(project_path: Path, broker: str):
    """Generate Celery task files."""
    # Create celery app file
    celery_app_path = project_path / "tasks" / "celery_app.py"
    with open(celery_app_path, "w") as f:
        f.write(_get_celery_app_content(broker))

    # Create sample task file
    sample_task_path = project_path / "tasks" / "sample_tasks.py"
    with open(sample_task_path, "w") as f:
        f.write(_get_sample_task_content())


def _get_celery_app_content(broker: str) -> str:
    """Get content for celery_app.py file."""
    broker_url = {
        "redis": "redis://redis:6379/0",
        "rabbitmq": "amqp://guest:guest@rabbitmq:5672//",
    }[broker]

    return f'''"""
Celery application configuration.
"""
import os
from celery import Celery

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Use environment variables with defaults
broker_url = os.getenv("CELERY_BROKER_URL", "{broker_url}")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "{broker_url}")

# Create Celery app
celery_app = Celery(
    "tasks",
    broker=broker_url,
    backend=result_backend,
    include=["tasks.sample_tasks"]
)

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

if __name__ == "__main__":
    celery_app.start()
'''


def _get_sample_task_content() -> str:
    """Get content for sample_tasks.py file."""
    return '''"""
Sample Celery tasks with retry logic.
"""
import logging
import time
from typing import Dict, Any, Optional

from celery import Task
from celery.exceptions import SoftTimeLimitExceeded
from celery.utils.log import get_task_logger

from tasks.celery_app import celery_app

# Configure logger
logger = get_task_logger(__name__)


class BaseTask(Task):
    """Base task with error handling and retry logic."""
    
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 5}
    retry_backoff = True
    retry_backoff_max = 600  # 10 minutes
    retry_jitter = True
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure."""
        logger.error(
            f"Task {self.name}[{task_id}] failed: {exc}",
            exc_info=einfo
        )
        super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Handle task retry."""
        logger.warning(
            f"Task {self.name}[{task_id}] retrying: {exc}",
            exc_info=einfo
        )
        super().on_retry(exc, task_id, args, kwargs, einfo)
    
    def on_success(self, retval, task_id, args, kwargs):
        """Handle task success."""
        logger.info(f"Task {self.name}[{task_id}] completed successfully")
        super().on_success(retval, task_id, args, kwargs)


@celery_app.task(base=BaseTask, name="tasks.process_data")
def process_data(data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process data asynchronously.
    
    Args:
        data: The data to process
        options: Optional processing options
    
    Returns:
        Dict containing the processing results
    """
    logger.info(f"Processing data: {data}")
    
    try:
        # Simulate processing time
        time.sleep(2)
        
        # Simulate processing logic
        result = {
            "processed": True,
            "input_size": len(data),
            "timestamp": time.time(),
        }
        
        if options and options.get("raise_error"):
            # For testing error handling
            raise ValueError("Simulated error in task")
        
        return result
    
    except SoftTimeLimitExceeded:
        logger.error("Task exceeded time limit")
        raise
    except Exception as e:
        logger.exception(f"Error processing data: {e}")
        raise


@celery_app.task(base=BaseTask, name="tasks.cleanup")
def cleanup(task_id: str) -> bool:
    """
    Cleanup after task execution.
    
    Args:
        task_id: ID of the task to clean up after
    
    Returns:
        True if cleanup was successful
    """
    logger.info(f"Cleaning up after task {task_id}")
    
    # Simulate cleanup logic
    time.sleep(1)
    
    return True
'''
