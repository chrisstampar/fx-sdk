# Pre-Upload Checklist ✅

Run these tests before uploading to PyPI to ensure everything works correctly.

## Quick Test Commands

```bash
# 1. Run comprehensive pre-upload tests
python3 pre_upload_tests.py

# 2. Test package installation simulation
python3 test_installed_package.py

# 3. Quick functionality test
python3 quick_test.py

# 4. Comprehensive functionality test
python3 test_sdk.py
```

## Test Coverage

### ✅ Pre-Upload Tests (`pre_upload_tests.py`)
- [x] Package structure (all required files present)
- [x] ABI files (19 ABIs included)
- [x] Import tests (all modules importable)
- [x] Constants validation
- [x] Utility functions
- [x] Client initialization
- [x] Package version
- [x] Common issues check
- [x] Build files verification
- [x] Dependencies check
- [x] Optional dependencies

### ✅ Installation Simulation (`test_installed_package.py`)
- [x] Wheel contents (all files included)
- [x] Package metadata (correct fields)
- [x] Current installation test
- [x] Sensitive data check
- [x] Documentation files
- [x] File sizes (no unexpectedly large files)

### ✅ Functionality Tests
- [x] Quick test (`quick_test.py`) - Basic functionality
- [x] Comprehensive test (`test_sdk.py`) - Full feature coverage

## Manual Checks

Before uploading, also verify:

- [ ] **Version number** is correct in:
  - `fx_sdk/__init__.py` (__version__)
  - `setup.py`
  - `pyproject.toml`

- [ ] **No sensitive data** in code:
  - No API tokens
  - No private keys
  - No hardcoded credentials

- [ ] **Documentation** is complete:
  - README.md is up to date
  - features.md is accurate
  - All docstrings are present

- [ ] **Dependencies** are correct:
  - All required packages listed
  - Version constraints are appropriate
  - No unnecessary dependencies

- [ ] **Package name** is available:
  - Check: https://pypi.org/project/fx-sdk/
  - If taken, you'll need a different name

## Final Verification

After all tests pass:

1. **Rebuild the package** (to ensure latest changes):
   ```bash
   rm -rf dist/ build/ *.egg-info
   python3 -m build
   ```

2. **Run final test**:
   ```bash
   python3 pre_upload_tests.py
   ```

3. **Upload to PyPI**:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-YourTokenHere
   python3 -m twine upload dist/*
   ```

## Test Results Summary

If all tests pass, you should see:
- ✅ All critical tests passed
- ✅ Package structure looks good
- ✅ No errors or critical warnings

## Common Issues & Solutions

**Issue**: Missing ABI files
- **Solution**: Ensure all `.json` files are in `fx_sdk/abis/` and `MANIFEST.in` includes them

**Issue**: Import errors
- **Solution**: Check that all `__init__.py` files export correctly

**Issue**: Version mismatch
- **Solution**: Update version in all three places: `__init__.py`, `setup.py`, `pyproject.toml`

**Issue**: Build files missing
- **Solution**: Run `python3 -m build` to create distribution files

## Ready to Upload? ✅

If all tests pass and manual checks are complete, you're ready to upload!

See `PYPI_UPLOAD.md` for detailed upload instructions.

