# PyPI Verification Guide

**Goal:** Achieve "Verified" status on your PyPI project page  
**Status:** This guide covers all verification methods available on PyPI

---

## What is PyPI Verification?

PyPI verification shows users that your project is legitimate and maintained by the actual project owners. Verified projects display:
- ✅ Green checkmarks next to verified URLs
- 🔒 Trusted Publishing badges
- 📦 Digital Attestation indicators
- 🏷️ Verified repository links

---

## Verification Methods

### 1. **Domain Verification** (Recommended for Full Verification)

Verify ownership of your domain (e.g., `fx.aladdin.club`) to get green checkmarks on your project URLs.

#### Steps:

1. **Go to PyPI Account Settings:**
   - Visit: https://pypi.org/manage/account/
   - Scroll to "Verified domains" section

2. **Add Your Domain:**
   - Click "Add domain"
   - Enter your domain: `fx.aladdin.club` (or `aladdin.club` if you own the root)
   - PyPI will generate a DNS TXT record

3. **Add DNS TXT Record:**
   - Go to your domain's DNS settings
   - Add a TXT record with the value PyPI provides
   - Example:
     ```
     Type: TXT
     Name: @ (or _pypi-verification)
     Value: pypi-verification=abc123xyz...
     TTL: 3600
     ```

4. **Verify:**
   - Wait 5-60 minutes for DNS propagation
   - Click "Verify" in PyPI settings
   - Once verified, your homepage URL will show a ✅ checkmark

#### Current Status:
- ✅ Homepage URL: `https://fx.aladdin.club/` (can be verified)
- ⚠️ Documentation URL: Currently points to PyPI page (can't verify)

**Recommendation:** Once you have documentation hosted, update the documentation URL and verify that domain too.

---

### 2. **Trusted Publishing** (Most Secure Method)

Use OpenID Connect (OIDC) to publish directly from GitHub/GitLab without API tokens.

#### Benefits:
- 🔒 No API tokens to manage
- ✅ Automatic verification badge
- 🛡️ More secure (no token leakage risk)
- 📦 Can publish from CI/CD automatically

#### Setup for GitHub:

1. **Go to PyPI Account Settings:**
   - Visit: https://pypi.org/manage/account/publishing/
   - Click "Add a pending publisher"

2. **Configure Trusted Publisher:**
   - **PyPI project name:** `fx-sdk`
   - **Owner:** Your GitHub username or organization
   - **Repository name:** `fx_api` (or your actual repo name)
   - **Workflow filename:** `publish.yml` (or your CI workflow name)
   - **Environment name:** (optional, leave blank for default)

3. **Create GitHub Workflow:**
   
   Create `.github/workflows/publish.yml`:
   ```yaml
   name: Publish to PyPI
   
   on:
     release:
       types: [published]
   
   permissions:
     id-token: write  # Required for OIDC
     contents: read
   
   jobs:
     publish:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Set up Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.9'
         
         - name: Install build dependencies
           run: |
             python -m pip install --upgrade pip
             pip install build twine
         
         - name: Build package
           run: python -m build
         
         - name: Publish to PyPI
           uses: pypa/gh-action-pypi-publish@release/v1
           with:
             packages-dir: dist/
   ```

4. **Verify:**
   - Push the workflow file to your repository
   - Create a GitHub release
   - The workflow will automatically publish to PyPI
   - Your project page will show "Trusted Publishing" badge

#### Setup for GitLab:

Similar process, but use GitLab CI/CD:
- Visit: https://pypi.org/manage/account/publishing/
- Select "GitLab" as the provider
- Configure repository and CI job name

---

### 3. **Digital Attestations** (Advanced Security)

Publish cryptographic proofs that your package was built in a trusted environment.

#### Requirements:
- Trusted Publishing must be set up first
- Requires `pypa/gh-action-pypi-publish@release/v1` or newer

#### How It Works:
- When you publish via Trusted Publishing, PyPI automatically generates attestations
- These prove the package came from your verified repository
- Users can verify package authenticity

#### Current Status:
- ⏳ Requires Trusted Publishing setup first
- 📦 Will be automatic once Trusted Publishing is configured

---

### 4. **Repository Verification** (GitHub/GitLab)

Link your GitHub or GitLab repository to your PyPI project.

#### Steps:

1. **Update Project Metadata:**
   
   In `pyproject.toml`, add repository URLs:
   ```toml
   [project.urls]
   Homepage = "https://fx.aladdin.club/"
   Documentation = "https://pypi.org/project/fx-sdk/"
   Repository = "https://github.com/yourusername/fx_api"
   "Bug Tracker" = "https://github.com/yourusername/fx_api/issues"
   ```

2. **Verify Repository:**
   - PyPI will automatically detect if the repository exists
   - If you use Trusted Publishing, the repository is automatically verified
   - Otherwise, you may need to add a verification token to your repository

3. **Re-upload Package:**
   - Update version number (can't re-upload same version)
   - Rebuild and upload: `python3 -m build && python3 -m twine upload dist/*`

---

## Current Project Status

### ✅ Already Configured:
- ✅ Project name: `fx-sdk`
- ✅ Homepage URL: `https://fx.aladdin.club/`
- ✅ Author information
- ✅ License (MIT)
- ✅ Python version requirements

### ⏳ Can Be Improved:
- ⚠️ Documentation URL: Points to PyPI (should point to actual docs)
- ⚠️ Repository URL: Not specified in metadata
- ⚠️ Trusted Publishing: Not set up
- ⚠️ Domain Verification: Not verified

---

## Recommended Action Plan

### Priority 1: Domain Verification (Easiest)
1. Add DNS TXT record for `fx.aladdin.club`
2. Verify domain in PyPI settings
3. Homepage URL will show ✅ checkmark

**Time:** 10-15 minutes  
**Difficulty:** Easy  
**Impact:** High (visible verification badge)

### Priority 2: Repository Link (Quick Win)
1. Add repository URL to `pyproject.toml`
2. Bump version (e.g., 0.3.0 → 0.3.1)
3. Rebuild and upload
4. Repository link will appear on project page

**Time:** 5 minutes  
**Difficulty:** Easy  
**Impact:** Medium (shows source code location)

### Priority 3: Trusted Publishing (Best Long-term)
1. Set up Trusted Publishing in PyPI
2. Create GitHub Actions workflow
3. Future releases will be automatic and verified

**Time:** 30 minutes  
**Difficulty:** Medium  
**Impact:** High (security + automation)

### Priority 4: Digital Attestations (Automatic)
- Will be enabled automatically once Trusted Publishing is set up
- No additional action needed

---

## Step-by-Step: Domain Verification

### Step 1: Get Verification Token
1. Go to: https://pypi.org/manage/account/
2. Scroll to "Verified domains"
3. Click "Add domain"
4. Enter: `fx.aladdin.club`
5. Copy the TXT record value (starts with `pypi-verification=`)

### Step 2: Add DNS Record
1. Log into your domain registrar (where you manage `aladdin.club`)
2. Go to DNS settings
3. Add new TXT record:
   - **Type:** TXT
   - **Name:** `_pypi-verification` (or `@` for root domain)
   - **Value:** `pypi-verification=abc123xyz...` (the value from PyPI)
   - **TTL:** 3600 (or default)

### Step 3: Verify
1. Wait 5-60 minutes for DNS propagation
2. Go back to PyPI account settings
3. Click "Verify" next to your domain
4. Once verified, your homepage URL will show ✅

### Step 4: Verify It Worked
1. Visit: https://pypi.org/project/fx-sdk/
2. Check that `https://fx.aladdin.club/` shows a green checkmark ✅

---

## Step-by-Step: Add Repository URL

### Step 1: Update pyproject.toml

```toml
[project.urls]
Homepage = "https://fx.aladdin.club/"
Documentation = "https://pypi.org/project/fx-sdk/"
Repository = "https://github.com/yourusername/fx_api"
"Bug Tracker" = "https://github.com/yourusername/fx_api/issues"
```

### Step 2: Update Version
In both `pyproject.toml` and `setup.py`:
```toml
version = "0.3.1"  # Bump from 0.3.0
```

### Step 3: Rebuild and Upload
```bash
cd sdk
rm -rf build/ dist/ *.egg-info/
python3 -m build
python3 -m twine upload dist/*
```

### Step 4: Verify
Visit: https://pypi.org/project/fx-sdk/  
You should see a "Repository" link in the sidebar.

---

## Troubleshooting

### Domain Verification Not Working?
- **Check DNS propagation:** Use `dig TXT _pypi-verification.fx.aladdin.club` or online DNS checker
- **Wait longer:** DNS can take up to 48 hours (usually 5-60 minutes)
- **Check record name:** Must be `_pypi-verification` subdomain or root domain
- **Verify format:** Value must start with `pypi-verification=`

### Trusted Publishing Not Working?
- **Check permissions:** GitHub workflow needs `id-token: write` permission
- **Verify workflow name:** Must match exactly what you configured in PyPI
- **Check repository:** Must be public or you must grant PyPI access
- **Review logs:** Check GitHub Actions logs for errors

### Repository Not Showing?
- **Check URL format:** Must be full URL (https://github.com/...)
- **Verify repository exists:** Make sure the repo is accessible
- **Re-upload package:** Repository URL only appears after re-uploading with new version

---

## Verification Checklist

- [ ] Domain verified (DNS TXT record added and verified)
- [ ] Repository URL added to `pyproject.toml`
- [ ] Repository URL visible on PyPI project page
- [ ] Trusted Publishing configured (optional but recommended)
- [ ] GitHub Actions workflow created (if using Trusted Publishing)
- [ ] Digital Attestations enabled (automatic with Trusted Publishing)
- [ ] All URLs show green checkmarks ✅

---

## Resources

- **PyPI Account Settings:** https://pypi.org/manage/account/
- **Trusted Publishing Docs:** https://docs.pypi.org/trusted-publishers/
- **Domain Verification:** https://pypi.org/manage/account/ (scroll to "Verified domains")
- **Project Metadata Guide:** https://docs.pypi.org/project_metadata/
- **Digital Attestations:** https://blog.pypi.org/posts/2024-11-14-pypi-now-supports-digital-attestations/

---

**Last Updated:** December 23, 2025

