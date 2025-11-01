#!/bin/bash
# Publish the context-py package to PyPI via GitHub Actions
# This script creates a version tag and pushes it to GitHub,
# which triggers the automated CI/CD pipeline with Trusted Publishing

set -e  # Exit on any error

echo "==========================================="
echo "Publishing context-py package to PyPI"
echo "==========================================="
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "Error: You have uncommitted changes. Please commit or stash them first."
    git status --short
    exit 1
fi

# Get version number from user
echo "Enter the version number (e.g., 1.0.0):"
read -r VERSION

# Validate version format (basic check)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$ ]]; then
    echo "Error: Invalid version format. Use semantic versioning (e.g., 1.0.0 or 1.0.0-beta.1)"
    exit 1
fi

TAG_NAME="v${VERSION}"

# Check if tag already exists
if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    echo "Error: Tag $TAG_NAME already exists"
    exit 1
fi

echo ""
echo "This will:"
echo "  1. Create git tag: $TAG_NAME"
echo "  2. Push tag to GitHub"
echo "  3. Trigger GitHub Actions to build and publish to PyPI"
echo ""
echo "Current branch: $(git branch --show-current)"
echo "Latest commit: $(git log -1 --oneline)"
echo ""

# Confirm
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Optional: Add release notes
echo ""
echo "Enter release notes (press Ctrl+D when done, or Ctrl+C to skip):"
RELEASE_NOTES=$(cat)

# Create annotated tag
if [ -z "$RELEASE_NOTES" ]; then
    git tag -a "$TAG_NAME" -m "Release $VERSION"
else
    git tag -a "$TAG_NAME" -m "$RELEASE_NOTES"
fi

echo ""
echo "✓ Tag $TAG_NAME created"

# Push the tag
echo "Pushing tag to GitHub..."
git push origin "$TAG_NAME"

echo ""
echo "==========================================="
echo "✓ Tag pushed successfully!"
echo "==========================================="
echo ""
echo "GitHub Actions will now:"
echo "  - Build the package"
echo "  - Create a GitHub release"
echo "  - Publish to PyPI using Trusted Publishing"
echo ""
echo "Monitor progress at:"
echo "https://github.com/yanone/context-py/actions"
echo ""
echo "Once published, install with: pip install context"
