# SDK Project Structure

This document describes the organization of the fx-sdk project.

**Note:** This SDK project is located in the `sdk/` directory of the main workspace.

## 📁 Directory Structure

```
sdk/  (SDK project root)
├── fx_sdk/                    # Core SDK package (installed via pip)
│   ├── __init__.py
│   ├── client.py              # Main ProtocolClient class
│   ├── constants.py           # Contract addresses & configs
│   ├── utils.py               # Utility functions (conversions, etc.)
│   ├── exceptions.py          # Custom exception classes
│   └── abis/                  # Contract ABIs (JSON files)
│       ├── fxusd.json
│       ├── pool_manager.json
│       └── ...
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── tests.py               # Main unit tests
│   ├── test_sdk.py            # SDK integration tests
│   ├── test_address.py        # Address-specific tests
│   ├── test_installation.py   # Installation verification
│   ├── test_installed_package.py  # Post-install tests
│   ├── quick_test.py          # Quick functionality check
│   └── pre_upload_tests.py    # Pre-deployment tests
│
├── docs/                       # Documentation
│   ├── README.md              # Documentation index
│   ├── features.md            # Detailed feature list
│   ├── roadmap.md             # Development roadmap
│   ├── api_plan.md            # REST API implementation plan
│   ├── DEPLOYMENT_CHECKLIST.md    # PyPI deployment guide
│   ├── PRE_UPLOAD_CHECKLIST.md    # Pre-upload checklist
│   ├── PYPI_UPLOAD.md         # Upload instructions
│   └── SET_ENV_VARS.md        # Environment variables guide
│
├── scripts/                    # Utility scripts
│   └── upload_pypi.sh         # PyPI upload helper
│
├── dist/                       # Build artifacts (gitignored)
│   ├── fx_sdk-*.whl
│   └── fx_sdk-*.tar.gz
│
├── fx_sdk.egg-info/           # Package metadata (gitignored)
│
├── README.md                   # Main project README
├── LICENSE                     # MIT License
├── setup.py                   # Package setup script
├── pyproject.toml             # Modern Python project config
├── requirements.txt           # Python dependencies
├── MANIFEST.in                # Package file manifest
└── .gitignore                 # Git ignore rules
```

## 📦 Package Structure

The `fx_sdk/` directory is what gets installed when users run `pip install fx-sdk`.

## 🧪 Testing

All tests are in the `tests/` directory. Run tests with:
```bash
python -m pytest tests/
# or
python -m unittest discover tests
```

## 📚 Documentation

All documentation is in the `docs/` directory. The main README.md in the root provides a quick start guide.

## 🔧 Scripts

Utility scripts for development and deployment are in `scripts/`.

## 🚫 Ignored Files

The following are gitignored (build artifacts):
- `dist/` - Built packages
- `fx_sdk.egg-info/` - Package metadata
- `__pycache__/` - Python cache
- `.env` - Environment variables (never commit secrets!)

## 🎯 Best Practices

1. **Keep root clean**: Only essential files in root (README, setup.py, etc.)
2. **Organize by purpose**: Tests in `tests/`, docs in `docs/`, scripts in `scripts/`
3. **Package code only**: Only `fx_sdk/` should be in the installed package
4. **Documentation**: Keep all docs in `docs/` for easy reference

