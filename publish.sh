#!/bin/bash
# Publish the context-py package to PyPI
# This script builds and uploads the package to PyPI using twine

set -e  # Exit on any error

echo "==========================================="
echo "Publishing context-py package to PyPI"
echo "==========================================="
echo ""

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "Error: twine is not installed."
    echo "Install it with: pip install twine"
    exit 1
fi

# Check if we have credentials
echo "Checking PyPI credentials..."
if [ -z "$TWINE_USERNAME" ] && [ -z "$TWINE_PASSWORD" ] && [ ! -f ~/.pypirc ]; then
    echo "Warning: No PyPI credentials found."
    echo "You can set them via:"
    echo "  - Environment variables: TWINE_USERNAME and TWINE_PASSWORD"
    echo "  - Or configure ~/.pypirc file"
    echo ""
    read -p "Do you want to continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf src/*.egg-info
find . -name '*.pyc' -exec rm -f {} +
find . -name '__pycache__' -exec rm -fr {} +
echo "✓ Cleaned"
echo ""

# Build the package
echo "Building source distribution and wheel..."
python -m build
echo "✓ Built"
echo ""

# Show what will be uploaded
echo "Files to be uploaded:"
ls -lh dist/
echo ""

# Check the distribution
echo "Checking package with twine..."
twine check dist/*
echo "✓ Package check passed"
echo ""

# Ask for confirmation before uploading
read -p "Upload to PyPI? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Upload cancelled."
    exit 0
fi

# Upload to PyPI
echo "Uploading to PyPI..."
twine upload dist/*

echo ""
echo "==========================================="
echo "✓ Package published successfully!"
echo "==========================================="
echo ""
echo "You can now install it with: pip install context"
