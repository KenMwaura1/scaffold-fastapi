#!/bin/bash
# Script to fix linting issues in the project

# Install required tools if not already installed
pip install ruff black isort

# Fix imports with isort
echo "Fixing imports with isort..."
isort .

# Fix formatting with black
echo "Fixing formatting with black..."
black .

# Fix linting issues with ruff
echo "Fixing linting issues with ruff..."
ruff check --fix .

echo "Linting fixes complete!"