# Setting Environment Variables in Cursor

## Method 1: Inline with Command (Easiest for One-Time Use)

Set them directly in the command:

```bash
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-YourTokenHere python3 -m twine upload dist/*
```

## Method 2: Export in Terminal (Current Session Only)

In Cursor's integrated terminal:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YourTokenHere
python3 -m twine upload dist/*
```

**Note**: These only last for the current terminal session. If you close the terminal, you'll need to set them again.

## Method 3: Create a `.env` File (Recommended for Security)

1. Create a `.env` file in your project root:

```bash
# .env file (already in .gitignore)
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-YourTokenHere
```

2. Load it before running commands:

```bash
# Install python-dotenv if not already installed
pip install python-dotenv

# Load and run in one command
source <(cat .env | sed 's/^/export /') && python3 -m twine upload dist/*
```

Or use a simple script:

```bash
# upload_to_pypi.sh
#!/bin/bash
set -a
source .env
set +a
python3 -m twine upload dist/*
```

Then run:
```bash
chmod +x upload_to_pypi.sh
./upload_to_pypi.sh
```

## Method 4: Use a Shell Script

Create `upload_pypi.sh`:

```bash
#!/bin/bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YourTokenHere
python3 -m twine upload dist/*
```

Make it executable and run:
```bash
chmod +x upload_pypi.sh
./upload_pypi.sh
```

## Method 5: Cursor Settings (Persistent)

You can set environment variables in Cursor's settings:

1. Open Cursor Settings (Cmd+, or Ctrl+,)
2. Search for "terminal integrated env"
3. Add to `terminal.integrated.env.osx` (Mac) or `terminal.integrated.env.linux` (Linux):

```json
{
  "TWINE_USERNAME": "__token__",
  "TWINE_PASSWORD": "pypi-YourTokenHere"
}
```

**⚠️ Warning**: This stores the token in Cursor's settings file, which may not be ideal for security.

## Method 6: Using `~/.pypirc` File (Most Secure)

Create or edit `~/.pypirc`:

```ini
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = pypi-YourTokenHere
```

Then just run:
```bash
python3 -m twine upload dist/*
```

**Note**: Make sure `~/.pypirc` has proper permissions:
```bash
chmod 600 ~/.pypirc
```

## Recommended Approach

For PyPI uploads, I recommend **Method 6** (`.pypirc` file) because:
- ✅ Most secure (stored in home directory, not project)
- ✅ Persistent across sessions
- ✅ Works automatically with twine
- ✅ Easy to manage multiple PyPI accounts

## Quick Reference

**One-time upload (inline):**
```bash
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-YourTokenHere python3 -m twine upload dist/*
```

**Current session (export):**
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YourTokenHere
python3 -m twine upload dist/*
```

**Persistent (.pypirc):**
```bash
# Create ~/.pypirc once, then just:
python3 -m twine upload dist/*
```

