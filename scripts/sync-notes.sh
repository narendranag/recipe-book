#!/bin/bash
# Sync recipes from Apple Notes to the recipe-book repo.
# Designed to run via launchd or manually.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

cd "$REPO_DIR"

echo "$(date): Starting Notes sync..."

# Step 1: Export notes from Apple Notes
echo "Exporting notes..."
osascript "$SCRIPT_DIR/export_notes.applescript"

# Step 2: Convert to MDX (using uv to manage Python deps)
echo "Converting to MDX..."
cd "$SCRIPT_DIR"
uv run --with pyyaml --with beautifulsoup4 --with html2text --with requests python ingest_notes.py

# Step 3: Check for changes and push
cd "$REPO_DIR"
git add content/recipes/notes/

if git diff --cached --quiet; then
    echo "No new recipes from Notes."
else
    git commit -m "chore: sync recipes from Apple Notes"
    git push
    echo "New recipes pushed to GitHub."
fi

echo "$(date): Notes sync complete."
