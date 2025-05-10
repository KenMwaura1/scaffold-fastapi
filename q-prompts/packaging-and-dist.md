# Packaging and Distribution 

## **Prompt** (2025-10-05)

```text
I want to package this project using uv and make it available on PyPI.
```

### **Amazon Q Response**:

I'll help you package your `scaffold-fastapi` project using `uv` and make it available on PyPI. Here's a step-by-step guide:

---

### **1. Update Your Project Structure**

Ensure your project structure is ready for packaging:

- **Update `pyproject.toml`**: Use `hatchling` for modern Python packaging.
- **Move CLI Code**: Relocate CLI code to the `scaffold_fastapi` package and update imports.
- **Add a LICENSE File**: Include a license file, as it's required for PyPI packages.
- **Add a `.gitignore` File**: Create a `.gitignore` file tailored for Python projects.

---

### **2. Summary of Changes**

#### **Packaging Your `scaffold-fastapi` Project with `uv` for PyPI**

Here's what has been done to prepare your project for packaging and distribution:

- **Updated Project Structure**:
	- Moved CLI code to `scaffold_fastapi/cli.py` to make it importable as a module.
	- Updated imports to reflect the new structure.
- **Added Necessary Packaging Files**:
	- Included `LICENSE`, `.gitignore`, and `MANIFEST.in`.
- **Updated `pyproject.toml`**:
	- Switched to using `hatchling` as the build backend.
	- Added proper metadata and classifiers.
	- Configured the entry point for the CLI command.
	- Added development dependencies for packaging.
- **Created Packaging Documentation**:
	- Added a comprehensive `packaging_guide.md` with step-by-step instructions.

---

### **3. Next Steps to Publish to PyPI**

Since `uv` isn't available in your environment, you can use standard Python packaging tools. Follow these steps:

1. **Install Build Tools**:
	 ```bash
	 pip install build twine
	 ```

2. **Build the Package**:
	 ```bash
	 python -m build
	 ```
	 This will create distribution files in the `dist/` directory.

3. **Test Locally** (optional but recommended):
	 ```bash
	 pip install -e .
	 scaffold-fastapi --help
	 ```

4. **Create a PyPI Account**:
	 Register at [PyPI](https://pypi.org/account/register/).

5. **Upload to PyPI**:
	 ```bash
	 twine upload dist/*
	 ```
	 You'll be prompted for your PyPI username and password.

---

### **Fix for PyPI Authentication in GitHub Actions**

To improve security, I've updated your project to use the modern PyPI API token approach instead of username/password authentication. Here's what has been done:

1. **Updated GitHub Actions Workflow**:
	 Replaced the manual `twine` upload with the official PyPI GitHub Action:

	 ```yaml
	 - name: Publish to PyPI
		 if: startsWith(github.ref, 'refs/tags/') || github.ref == 'refs/heads/main'
		 uses: pypa/gh-action-pypi-publish@release/v1
		 with:
			 password: ${{ secrets.PYPI_API_TOKEN }}
	 ```

2. **Created PyPI Instructions**:
	 Added a `pypi_instructions.md` file with detailed steps on:
	 - How to create a PyPI API token.
	 - How to add it to GitHub Secrets.
	 - How to publish new versions.
	 - Troubleshooting tips.

3. **Updated the README**:
	 Included a section on publishing to PyPI:

	 ```markdown
	 ## Publishing to PyPI

	 To publish this package to PyPI, you need to:

	 1. Create a PyPI API token (see [pypi_instructions.md](pypi_instructions.md)).
	 2. Add the token to GitHub Secrets as `PYPI_API_TOKEN`.
	 3. Push to `main` or create a tag starting with `v` (e.g., `v0.1.0`).
	 ```

---

### **Why This Approach Is Better**

- **Security**: API tokens are more secure than username/password authentication.
- **Scoped Access**: You can limit the token to just this package.
- **Revocable**: You can revoke the token at any time if needed.
- **Official Support**: Using the official PyPI GitHub Action ensures compatibility with PyPI's requirements.

Follow the instructions in `pypi_instructions.md` to create a PyPI API token and add it to your GitHub repository secrets as `PYPI_API_TOKEN`. Push to `main` or create a tag to trigger the publishing workflow.
