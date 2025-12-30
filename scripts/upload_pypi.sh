#!/bin/bash
# Quick script to upload to PyPI
# Usage: ./upload_pypi.sh

echo "📦 Uploading fx-sdk to PyPI..."

# Check if .pypirc exists
if [ -f ~/.pypirc ]; then
    echo "✓ Using ~/.pypirc for credentials"
    python3 -m twine upload dist/*
else
    echo "⚠️  ~/.pypirc not found"
    echo "Please set environment variables:"
    echo "  export TWINE_USERNAME=__token__"
    echo "  export TWINE_PASSWORD=pypi-YourTokenHere"
    echo ""
    read -p "Press Enter to continue with current environment..."
    python3 -m twine upload dist/*
fi
