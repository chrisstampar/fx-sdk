# Quick Start: SDK Deployment Checklist

Follow these steps in order to deploy your SDK to GitHub, Read the Docs, and PyPI.

## ✅ Pre-Flight Checklist

- [x] Version updated to 0.4.0 in `setup.py` and `pyproject.toml`
- [x] URLs updated to point to GitHub repository
- [x] `.gitignore` created
- [x] `.readthedocs.yml` configured
- [x] `mkdocs.yml` configured
- [x] `docs/index.md` and `docs/Documentation.md` ready

## Step 1: GitHub Upload (5 minutes)

```bash
cd /Users/cstampar/Documents/built_with_cursor/fx_api/sdk

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: fx-sdk v0.4.0"

# Create repository on GitHub first, then:
git remote add origin https://github.com/chrisstampar/fx-sdk.git
git branch -M main
git push -u origin main
```

**After pushing:** Note your GitHub repository URL: `https://github.com/chrisstampar/fx-sdk`

---

## Step 2: Read the Docs Setup (10 minutes)

1. Go to https://readthedocs.org
2. Sign in with GitHub
3. Click "Import a Project"
4. Select `fx-sdk` repository
5. Configure:
   - **Name:** `fx-sdk`
   - **Repository:** `chrisstampar/fx-sdk`
   - **Type:** MkDocs
   - **Config file:** `mkdocs.yml` (or leave empty)
6. Click "Next" → "Finish"
7. Wait for build to complete (check "Builds" tab)
8. **Copy your Read the Docs URL:** `https://fx-sdk.readthedocs.io/`

**Important:** If your Read the Docs URL is different from `https://fx-sdk.readthedocs.io/`, update it in:
- `setup.py` (line with `"Documentation":`)
- `pyproject.toml` (line with `Documentation =`)

---

## Step 3: Update PyPI URLs (2 minutes)

If your Read the Docs URL is different, update these files:

**setup.py:**
```python
"Documentation": "https://YOUR-ACTUAL-URL.readthedocs.io/",
```

**pyproject.toml:**
```toml
Documentation = "https://YOUR-ACTUAL-URL.readthedocs.io/"
```

Then commit and push:
```bash
git add setup.py pyproject.toml
git commit -m "Update documentation URL for Read the Docs"
git push
```

---

## Step 4: Upload to PyPI (5 minutes)

```bash
cd /Users/cstampar/Documents/built_with_cursor/fx_api/sdk

# Install build tools
python3 -m pip install --upgrade build twine

# Build package
python3 -m build

# Upload to PyPI (you'll need your PyPI credentials)
python3 -m twine upload dist/*
```

**PyPI Credentials:**
- Username: Your PyPI username
- Password: Your PyPI password or API token

**After upload:** Your package will be available at:
- PyPI: https://pypi.org/project/fx-sdk/
- Install: `pip install fx-sdk==0.4.0`

---

## Verification Checklist

After completing all steps, verify:

- [ ] GitHub repository is public and accessible
- [ ] Read the Docs is building and accessible
- [ ] PyPI package shows v0.4.0
- [ ] PyPI package shows correct Homepage and Documentation links
- [ ] Can install via: `pip install fx-sdk==0.4.0`

---

## Troubleshooting

### Read the Docs build fails
- Check build logs in Read the Docs dashboard
- Verify `mkdocs.yml` syntax is correct
- Ensure `docs/Documentation.md` exists

### PyPI upload fails
- Verify version 0.4.0 is higher than existing version (0.3.0)
- Check credentials are correct
- Ensure `dist/` folder contains new build files

### Documentation URL not working
- Verify Read the Docs project is public
- Check that build completed successfully
- Wait a few minutes for DNS propagation

---

**Need help?** See `SDK_DEPLOYMENT_GUIDE.md` for detailed instructions.

