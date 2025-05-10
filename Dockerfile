FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY scaffold_fastapi ./scaffold_fastapi/

# Install the package
RUN pip install --no-cache-dir -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create a non-root user
RUN useradd -m scaffolder
USER scaffolder

ENTRYPOINT ["scaffold-fastapi"]
CMD ["--help"]