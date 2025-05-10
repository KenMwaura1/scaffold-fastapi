# Packaging Guide for scaffold-fastapi

This guide explains how to package and publish the scaffold-fastapi project to PyPI using uv.

## Prerequisites

1. Install uv:
```bash
pip install uv
```

2. Install build tools:
```bash
uv pip install build twine
```

## Building the Package

1. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Build the package:
```bash
python -m build
```

This will create both a source distribution (.tar.gz) and a wheel (.whl) in the `dist/` directory.

## Testing the Package Locally

Before publishing to PyPI, you can test the package locally:

```bash
# Install the package in development mode
uv pip install -e .

# Test the CLI
scaffold-fastapi --help
```

## Publishing to PyPI

1. Create an account on [PyPI](https://pypi.org/) if you don't have one.

2. Create an API token on PyPI:
   - Go to your account settings
   - Navigate to "API tokens"
   - Create a new token with scope "Entire account" or limited to this project

3. Configure your credentials:
```bash
# Create or edit ~/.pypirc
[pypi]
username = __token__
password = pypi-your-token-here
```

4. Upload to PyPI:
```bash
twine upload dist/*
```

5. Alternatively, you can use uv to upload:
```bash
uv pip publish
```

## Updating the Package

When you make changes and want to release a new version:

1. Update the version number in `pyproject.toml`
2. Rebuild the package:
```bash
python -m build
```
3. Upload the new version:
```bash
twine upload dist/*
```

## Installing from PyPI

Once published, users can install your package with:

```bash
# Using pip
pip install scaffold-fastapi

# Using uv
uv pip install scaffold-fastapi
```

## GitHub Actions for Automated Publishing

You can set up GitHub Actions to automatically build and publish your package when you create a new release:

1. Create a `.github/workflows/publish.yml` file:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python -m build
        twine upload dist/*
```

2. Add your PyPI token as a secret in your GitHub repository settings (Settings > Secrets > Actions > New repository secret) with the name `PYPI_PASSWORD` and set `PYPI_USERNAME` to `__token__`.