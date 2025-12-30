# Pre-Deployment Checklist ✅

## Package Configuration
- ✅ Package name: `fx-sdk` (consistent in setup.py and pyproject.toml)
- ✅ Version: `0.1.0` (consistent across all files)
- ✅ Import name: `fx_sdk` (matches directory structure)
- ✅ Python requirement: `>=3.8`

## Dependencies
- ✅ `web3>=6.0.0`
- ✅ `eth-account>=0.5.0` (explicitly added)
- ✅ `eth-typing>=3.0.0`
- ✅ `eth-utils>=2.0.0`
- ✅ `python-dotenv>=1.0.0`

## Package Contents
- ✅ 19 ABI files in `fx_sdk/abis/`
- ✅ Core modules: client.py, constants.py, utils.py, exceptions.py
- ✅ All x tokens included: xETH, xCVX, xWBTC, xeETH, xezETH, xstETH, xfrxETH

## Documentation
- ✅ README.md (complete with authentication examples)
- ✅ features.md (complete feature list)
- ✅ LICENSE (MIT)
- ✅ All docstrings updated

## Testing
- ✅ All 11 tests passing
- ✅ No linter errors
- ✅ Package imports successfully

## Metadata
- ✅ Author: Christopher Stampar (@cstampar)
- ✅ Email: cstampar@me.com
- ✅ URL: https://fx.aladdin.club/
- ✅ License: MIT

## Deployment Steps

1. **Build the package:**
   ```bash
   pip install --upgrade build twine
   python3 -m build
   ```

2. **Test the build locally:**
   ```bash
   pip install dist/fx_sdk-0.1.0-py3-none-any.whl
   python3 -c "from fx_sdk import ProtocolClient; print('✓ Installed successfully')"
   ```

3. **Upload to TestPyPI (recommended first):**
   
   **Option A: Using environment variables (recommended):**
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-AgENdGVzdC5weXBpLm9yZwIkZTA0NzNjZGMtNDA4Ni00MTQwLWI5MTUtZjkxNTcwOWQwOTQwAAIqWzMsIjU1ZjJmM2UzLTI4YjUtNGEwYi05MTY5LTBmOGZiNzEzMGRjZSJdAAAGIHR8a653cdAoMnHjxarM-f5kqbEaytPm2hW-YSLEK1v5
   python3 -m twine upload --repository testpypi dist/*
   ```
   
   **Option B: Using .pypirc file:**
   Create `~/.pypirc`:
   ```ini
   [distutils]
   index-servers = testpypi pypi
   
   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-AgENdGVzdC5weXBpLm9yZwIkZTA0NzNjZGMtNDA4Ni00MTQwLWI5MTUtZjkxNTcwOWQwOTQwAAIqWzMsIjU1ZjJmM2UzLTI4YjUtNGEwYi05MTY5LTBmOGZiNzEzMGRjZSJdAAAGIHR8a653cdAoMnHjxarM-f5kqbEaytPm2hW-YSLEK1v5
   
   [pypi]
   username = __token__
   password = pypi-YourPyPIAPITokenHere
   ```
   Then run:
   ```bash
   python3 -m twine upload --repository testpypi dist/*
   ```
   
   **Get API tokens:**
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - PyPI: https://pypi.org/manage/account/token/
   
   **Note:** If you get a 403 error:
   - Verify the token starts with `pypi-`
   - Check the token has upload permissions
   - Ensure package name isn't already taken (TestPyPI allows re-uploads, PyPI doesn't)

4. **Test installation from TestPyPI:**
   ```bash
   # Correct: Use the simple API endpoint and specify package name
   pip install --index-url https://test.pypi.org/simple/ fx-sdk
   
   # Or install a specific version:
   pip install --index-url https://test.pypi.org/simple/ fx-sdk==0.1.0
   
   # Note: The --index-url must point to /simple/, not the project page URL
   ```

5. **Upload to PyPI:**
   
   **⚠️ IMPORTANT: PyPI does NOT allow re-uploads of the same version!**
   - Test thoroughly on TestPyPI first
   - If you need to fix something, bump the version (0.1.0 → 0.1.1)
   
   **Get PyPI API Token:**
   - Go to: https://pypi.org/manage/account/token/
   - Create a new token (starts with `pypi-`)
   - Copy it immediately (you won't see it again!)
   
   **Upload:**
   ```bash
   # Using environment variables (recommended):
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-YourPyPIAPITokenHere
   python3 -m twine upload dist/*
   
   # Or using .pypirc (if configured):
   python3 -m twine upload dist/*
   ```
   
   **Verify:**
   - Visit: https://pypi.org/project/fx-sdk/
   - Test install: `pip install fx-sdk`
   
   **See PYPI_UPLOAD.md for detailed step-by-step instructions.**

## Post-Deployment
- Update version number for future releases
- Tag the release in git
- Update changelog if maintained

