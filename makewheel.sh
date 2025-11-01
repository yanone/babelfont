#!/bin/bash
# Build a Python wheel compatible with Pyodide
# Uses build ~=1.2.0 for compatibility with pyodide-build 0.25.1

set -e

echo "Building context-py wheel for Pyodide..."

# Ensure we have the correct build version
pip install 'build~=1.2.0'

# Build the wheel
python -m build --wheel

# Get the most recent wheel file
WHEEL_FILE=$(ls -t dist/*.whl | head -1)

# Copy to font editor with fixed name
DEST_DIR="../context-font-editor/webapp/wheels"
DEST_FILE="$DEST_DIR/contextfonteditor.whl"

echo ""
echo "Copying wheel to font editor..."
mkdir -p "$DEST_DIR"
cp "$WHEEL_FILE" "$DEST_FILE"

echo ""
echo "Wheel built successfully!"
echo "Source: $WHEEL_FILE"
echo "Destination: $DEST_FILE"
ls -lh "$DEST_FILE"
