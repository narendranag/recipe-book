#!/bin/bash
# Sync recipes from Apple Notes to the recipe-book repo.
# Designed to run via launchd or manually.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
UV_RUN="uv run --with pyyaml --with beautifulsoup4 --with html2text --with requests --with httpx"

cd "$REPO_DIR"

echo "$(date): Starting Notes sync..."

# Step 1: Export notes from Apple Notes
echo "Exporting notes..."
osascript "$SCRIPT_DIR/export_notes.applescript"

# Step 2: Convert to MDX
echo "Converting to MDX..."
cd "$SCRIPT_DIR"
$UV_RUN python ingest_notes.py

# Step 3: Rewrite any unprocessed recipes
echo "Rewriting recipes..."
$UV_RUN python rewrite_recipes.py

# Step 4: Check for changes and push
cd "$REPO_DIR"
git add content/recipes/

if git diff --cached --quiet; then
    echo "No new recipes from Notes."
else
    git commit -m "chore: sync and rewrite recipes from Apple Notes"
    git push
    echo "New recipes pushed to GitHub."
fi

echo "$(date): Notes sync complete."
