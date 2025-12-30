# SDK Deployment Guide: GitHub, Read the Docs, and PyPI

Complete guide for uploading the SDK to GitHub, setting up Read the Docs, and publishing to PyPI v0.4.0.

## Task Overview

1. ✅ Upload SDK to new GitHub repository
2. ✅ Set up Read the Docs pointing to Documentation.md
3. ✅ Get Read the Docs URL and link to PyPI
4. ✅ Upload SDK to PyPI v0.4.0 with updated links

---

## Step 1: Upload SDK to GitHub

### 1.1 Create .gitignore for SDK

Create a `.gitignore` file in the `sdk/` directory:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/

# Virtual Environment
venv/
env/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/

# Distribution / Packaging
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Test files (optional - you may want to keep these)
# test_*.py
```

### 1.2 Initialize Git Repository

```bash
cd /Users/cstampar/Documents/built_with_cursor/fx_api/sdk
git init
git add .
git commit -m "Initial commit: fx-sdk v0.4.0"
```

### 1.3 Create GitHub Repository

1. Go to https://github.com and create a new repository
2. Name it: `fx-sdk` (or `fx-protocol-sdk`)
3. **DO NOT** initialize with README, .gitignore, or license
4. Copy the repository URL

### 1.4 Push to GitHub

```bash
cd /Users/cstampar/Documents/built_with_cursor/fx_api/sdk
git remote add origin https://github.com/chrisstampar/fx-sdk.git
git branch -M main
git push -u origin main
```

---

## Step 2: Set Up Read the Docs

### 2.1 Create Account

1. Go to https://readthedocs.org
2. Sign up / Sign in with GitHub (recommended)
3. Import your GitHub account

### 2.2 Import Project

1. Click "Import a Project"
2. Select your GitHub account
3. Find and select `fx-sdk` repository
4. Click "Next"

### 2.3 Configure Read the Docs

**Project Settings:**

1. **Name:** `fx-sdk` (or your preferred name)
2. **Repository URL:** `https://github.com/chrisstampar/fx-sdk`
3. **Default Branch:** `main`
4. **Documentation type:** Select "MkDocs"
5. **Configuration file:** `mkdocs.yml` (or leave empty - it will auto-detect)

**Note:** The repository already includes:
- `.readthedocs.yml` - Read the Docs configuration
- `mkdocs.yml` - MkDocs configuration
- `docs/index.md` - Homepage
- `docs/Documentation.md` - Main documentation

### 2.4 Build and Get URL

1. After configuration, Read the Docs will automatically build your docs
2. Go to the "Builds" tab to see the build progress
3. Once built successfully, your docs will be available at:
   ```
   https://fx-sdk.readthedocs.io/
   ```
   (The URL format is: `https://<project-name>.readthedocs.io/`)

4. **Copy this URL** - you'll need it for Step 3 (PyPI configuration)

---

## Step 3: Update PyPI Package for v0.4.0

### 3.1 Update Version Numbers

Update these files to v0.4.0:

**setup.py:**
```python
version="0.4.0",
```

**pyproject.toml:**
```toml
version = "0.4.0"
```

### 3.2 Update URLs in setup.py

**Note:** Files are already updated! Just verify the Read the Docs URL matches your actual URL.

The `setup.py` file already includes:
```python
url="https://github.com/chrisstampar/fx-sdk",
project_urls={
    "Homepage": "https://github.com/chrisstampar/fx-sdk",
    "Documentation": "https://fx-sdk.readthedocs.io/",  # Update if different
    "Source": "https://github.com/chrisstampar/fx-sdk",
    "Bug Tracker": "https://github.com/chrisstampar/fx-sdk/issues",
}
```

**If your Read the Docs URL is different**, update the `Documentation` URL in both `setup.py` and `pyproject.toml`.

### 3.3 Update URLs in pyproject.toml

**Note:** Files are already updated! Just verify the Read the Docs URL matches your actual URL.

The `pyproject.toml` file already includes:
```toml
[project.urls]
Homepage = "https://github.com/chrisstampar/fx-sdk"
Documentation = "https://fx-sdk.readthedocs.io/"  # Update if different
Source = "https://github.com/chrisstampar/fx-sdk"
"Bug Tracker" = "https://github.com/chrisstampar/fx-sdk/issues"
```

**If your Read the Docs URL is different**, update the `Documentation` URL in both files.

### 3.4 Build Package

```bash
cd /Users/cstampar/Documents/built_with_cursor/fx_api/sdk
python3 -m pip install --upgrade build twine
python3 -m build
```

### 3.5 Upload to PyPI

```bash
# Test first (optional but recommended)
python3 -m twine upload --repository testpypi dist/*

# Upload to real PyPI
python3 -m twine upload dist/*
```

You'll need your PyPI credentials (username and password/token).

---

## Quick Reference Checklist

### GitHub Setup
- [ ] Create `.gitignore` in SDK folder
- [ ] Initialize git: `git init`
- [ ] Create GitHub repository
- [ ] Push code: `git push -u origin main`

### Read the Docs Setup
- [ ] Sign up at readthedocs.org
- [ ] Import GitHub repository
- [ ] Configure build settings
- [ ] Create `.readthedocs.yml` (or use MkDocs config)
- [ ] Build documentation
- [ ] Get public URL: `https://fx-sdk.readthedocs.io/`

### PyPI Upload
- [ ] Update version to 0.4.0 in `setup.py` and `pyproject.toml`
- [ ] Update URLs to point to GitHub repo
- [ ] Update Documentation URL to Read the Docs
- [ ] Build package: `python3 -m build`
- [ ] Upload to PyPI: `python3 -m twine upload dist/*`

---

## Notes

- **Read the Docs URL format:** `https://your-project-name.readthedocs.io/`
- **GitHub repo URL:** `https://github.com/chrisstampar/fx-sdk`
- **PyPI package:** `fx-sdk` (already exists at v0.3.0)

---

**Next Steps:** Start with Step 1 (GitHub upload), then proceed to Read the Docs setup, and finally PyPI upload.

