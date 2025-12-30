# Release Checklist for v0.3.0

**Release Date:** December 22, 2025  
**Version:** 0.3.0

## Pre-Release Steps

### 1. Version Updates
- [ ] Updated `setup.py` version to `0.3.0`
- [ ] Updated `pyproject.toml` version to `0.3.0`
- [ ] Updated `CHANGELOG.md` with v0.3.0 changes

### 2. Code Quality
- [ ] Run all tests: `python3 -m unittest discover tests -v`
- [ ] Verify no linter errors: Check all modified files
- [ ] Verify all new ABIs are included in `MANIFEST.in` (recursive-include handles this)
- [ ] Check that all new methods are documented

### 3. Documentation
- [x] CHANGELOG.md created with all new features
- [ ] Verify README.md is up-to-date
- [ ] Verify features.md includes Convex and Curve sections
- [ ] Check that all integration docs are complete

### 4. Package Contents
- [ ] Verify all ABI files are included (should be automatic via `recursive-include`)
- [ ] Check that no internal files are included (tests, deployment files, etc.)
- [ ] Verify LICENSE file is included

### 5. Build & Test
- [ ] Clean previous builds: `rm -rf build/ dist/ *.egg-info/`
- [ ] Build package: `python3 -m build`
- [ ] Verify build contents: `tar -tzf dist/fx_sdk-0.3.0.tar.gz | head -20`
- [ ] Test install locally: `pip install dist/fx_sdk-0.3.0-py3-none-any.whl`

### 6. TestPyPI Upload (Optional but Recommended)
- [ ] Upload to TestPyPI: `python3 -m twine upload --repository testpypi dist/*`
- [ ] Test install from TestPyPI: `pip install --index-url https://test.pypi.org/simple/ fx-sdk==0.3.0`
- [ ] Verify package works correctly from TestPyPI

### 7. Production Release
- [ ] Upload to PyPI: `python3 -m twine upload dist/*`
- [ ] Verify package on PyPI: https://pypi.org/project/fx-sdk/
- [ ] Test install from PyPI: `pip install fx-sdk==0.3.0`
- [ ] Verify upgrade works: `pip install --upgrade fx-sdk`

## Post-Release

- [ ] Create GitHub release (if applicable)
- [ ] Update any external documentation
- [ ] Announce release (if applicable)

## What's New in v0.3.0

### Removed
- **APY Calculation Methods**: All APY calculation methods have been removed due to complexity and accuracy issues. Users should refer to Convex/Curve websites for official APY values.

### Breaking Changes
- `get_convex_pool_statistics()` no longer includes APY data
- All APY-related methods removed (see CHANGELOG.md for full list)

## What's New in v0.2.0

### Major Features
- **Convex Finance Integration**: Complete vault management, staking, and rewards
- **Curve Finance Integration**: Pool operations, swaps, liquidity, and gauge staking
- **30+ Convex Pools**: Full registry of f(x) Protocol pools
- **cvxFXN Staking**: Dedicated staking mechanism
- **Batch Operations**: Efficient multi-vault/pool queries
- **Position Summaries**: Comprehensive user position tracking

### Statistics
- **22 new Convex methods** (vault management, staking, etc.)
- **22 new Curve methods** (pool operations, swaps, gauges, etc.)
- **14 new ABIs** (7 Convex, 7 Curve)
- **52 new tests** (26 Convex, 26 Curve)
- **3 new documentation files** (integration guides)

## Commands Reference

```bash
# Clean build
rm -rf build/ dist/ *.egg-info/

# Build package
cd sdk
python3 -m build

# Upload to TestPyPI
python3 -m twine upload --repository testpypi dist/*

# Upload to PyPI
python3 -m twine upload dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ fx-sdk==0.3.0
pip install fx-sdk==0.3.0
```

## Notes

- All new ABIs are automatically included via `recursive-include fx_sdk/abis *.json` in MANIFEST.in
- Test files are excluded from package (as intended)
- Deployment checklist is excluded from package (as intended)
- All new methods follow the same patterns as existing code for consistency

