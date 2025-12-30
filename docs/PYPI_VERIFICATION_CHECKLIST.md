# PyPI Verification Checklist

**Status:** Pre-GitHub Setup

---

## ✅ Can Do Now (No GitHub Required)

### 1. Domain Verification ⭐ **RECOMMENDED - DO THIS FIRST**
- [ ] Go to: https://pypi.org/manage/account/
- [ ] Scroll to "Verified domains"
- [ ] Click "Add domain"
- [ ] Enter: `fx.aladdin.club`
- [ ] Copy the DNS TXT record value
- [ ] Add TXT record to your domain DNS settings
- [ ] Wait 5-60 minutes for DNS propagation
- [ ] Click "Verify" in PyPI settings
- [ ] ✅ Homepage URL will show green checkmark

**Time:** 10-15 minutes  
**Impact:** High (immediate visual verification badge)

---

## ⏳ Wait Until GitHub is Set Up

### 2. Repository Link
- [ ] Create GitHub repository
- [ ] Add repository URL to `pyproject.toml`
- [ ] Bump version (e.g., 0.3.0 → 0.3.1)
- [ ] Rebuild and upload to PyPI
- [ ] Repository link appears on project page

**Time:** 5 minutes (after GitHub setup)  
**Impact:** Medium

### 3. Trusted Publishing
- [ ] Set up GitHub account
- [ ] Create repository
- [ ] Configure Trusted Publishing in PyPI
- [ ] Create `.github/workflows/publish.yml`
- [ ] Future releases will be automatic and verified

**Time:** 30 minutes (after GitHub setup)  
**Impact:** High (security + automation)

### 4. Digital Attestations
- [ ] Automatically enabled once Trusted Publishing is set up
- [ ] No additional action needed

---

## Quick Reference

**Domain Verification (Do Now):**
- Guide: See `PYPI_VERIFICATION_GUIDE.md` → "Step-by-Step: Domain Verification"
- No GitHub account needed
- Immediate visual impact

**After GitHub Setup:**
- See `PYPI_VERIFICATION_GUIDE.md` for full instructions
- Repository link: Quick 5-minute update
- Trusted Publishing: 30-minute setup for long-term benefits

---

**Last Updated:** December 23, 2025

