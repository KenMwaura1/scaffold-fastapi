# PyPI Publishing Instructions

To publish your package to PyPI, you need to set up an API token. Here's how:

## 1. Create a PyPI API Token

1. Create an account on [PyPI](https://pypi.org/) if you don't have one
2. Go to your account settings: https://pypi.org/manage/account/
3. Navigate to "API tokens"
4. Click "Add API token"
5. Give it a name (e.g., "GitHub Actions")
6. Choose the scope (either "Entire account" or limit it to the "scaffold-fastapi" project)
7. Click "Create token"
8. **Copy the token immediately** - you won't be able to see it again!

## 2. Add the Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste the API token you copied from PyPI
6. Click "Add secret"

## 3. Publishing Process

With the API token set up, your package will be automatically published to PyPI when:

- You push to the `main` branch
- You create a new tag starting with `v` (e.g., `v0.1.0`)

To create and push a new version tag:

```bash
# Update version in pyproject.toml first
git add pyproject.toml
git commit -m "Bump version to X.Y.Z"

# Create and push tag
git tag vX.Y.Z
git push origin vX.Y.Z
```

## 4. Manual Publishing

If you need to publish manually:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI
twine upload dist/* --api-token YOUR_API_TOKEN
```

## 5. Troubleshooting

If you encounter issues:

- Make sure your package name is unique on PyPI
- Ensure your version number is incremented (PyPI doesn't allow overwriting existing versions)
- Check that your API token has the correct permissions
- Try uploading to TestPyPI first: `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`