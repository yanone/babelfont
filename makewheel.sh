#!/bin/bash
# Build a Python wheel compatible with Pyodide
# Uses build ~=1.2.0 for compatibility with pyodide-build 0.25.1

set -e

echo "Building context-py wheel for Pyodide..."

# Ensure we have the correct build version
pip install 'build~=1.2.0'

# Build the wheel
python -m build --wheel

echo ""
echo "Wheel built successfully!"
echo "Output location: dist/"
ls -lh dist/*.whl | tail -1
