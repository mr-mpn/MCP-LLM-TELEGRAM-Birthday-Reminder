#!/bin/bash
# Build script for packaging Lambda functions and dependencies layer

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"

echo "=== Building Birthday Bot Lambda Package ==="

# Clean dist directory
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# --- Build dependencies layer ---
echo "Building dependencies layer..."
LAYER_DIR="$DIST_DIR/layer/python"
mkdir -p "$LAYER_DIR"

pip install -r "$PROJECT_ROOT/requirements.txt" -t "$LAYER_DIR" --quiet

cd "$DIST_DIR/layer"
zip -r "$DIST_DIR/dependencies_layer.zip" python/ -q
cd "$PROJECT_ROOT"
rm -rf "$DIST_DIR/layer"

echo "✓ Dependencies layer built: dist/dependencies_layer.zip"

# --- Build Lambda code package ---
echo "Building Lambda code package..."
cd "$PROJECT_ROOT/src"
zip -r "$DIST_DIR/chat_lambda.zip" . -q
cd "$PROJECT_ROOT"

echo "✓ Lambda code built: dist/chat_lambda.zip"
echo ""
echo "=== Build complete! ==="
echo "Next steps:"
echo "  1. cd terraform"
echo "  2. terraform init"
echo "  3. terraform plan"
echo "  4. terraform apply"
