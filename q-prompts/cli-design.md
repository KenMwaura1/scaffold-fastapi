# CLI Design Prompts 

**Goal**: Generate a Typer-based CLI with production-ready defaults  

## **Prompt 1** (10-5-2025)

1. **Core Features**:
   - Command: `scaffold-fastapi create <name> --db=<postgresql|mongodb|sqlite> --broker=<redis|rabbitmq> --stack=<minimal|full|serverless>`
   - Uses `uv` for dependency management (virtual envs + installations)
   - Interactive prompts for missing options

2. **Project Structure**:
   - `app/` (FastAPI core)
   - `tasks/` (Celery tasks)
   - `infra/` (Terraform/Docker files for the selected stack)

3. **Database Support**:
   - PostgreSQL: AsyncSQLAlchemy models + connection pool
   - MongoDB: Motor async driver setup

4. **Celery**:
   - Redis/RabbitMQ broker configuration
   - Sample task (e.g., `process_data`) with error handling

5. **Production-Ready**:
   - Dockerfile with multi-stage builds
   - Terraform AWS ECS module (for `--stack=full`)
   - Helm charts (for K8s)

6. **Validation**:
   - Verify environment variables (e.g., `DATABASE_URL`) are set
   - Generate `.env.example` with placeholder values


