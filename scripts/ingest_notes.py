#!/usr/bin/env python3
"""
Apple Notes ingestion script.
Reads exported notes JSON (from export_notes.applescript) and converts to MDX files.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

from parse_recipe import parse_recipe_text, slugify

REPO_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = REPO_ROOT / "content" / "recipes" / "notes"
EXPORT_FILE = Path(__file__).resolve().parent / ".notes-export.json"


def html_to_text(html: str) -> str:
    """Convert HTML note body to plain text."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove style and script tags
    for tag in soup(["style", "script"]):
        tag.decompose()

    # Get text with newlines preserved
    text = soup.get_text(separator="\n")

    # Clean up excessive whitespace
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(lines)


def process_note(note: dict) -> bool:
    """
    Process a single note and write as MDX.
    Returns True if new file written.
    """
    title = note.get("title", "Untitled")
    slug = slugify(title)
    mdx_path = RECIPES_DIR / f"{slug}.mdx"

    if mdx_path.exists():
        return False

    body_html = note.get("body", "")
    body_text = html_to_text(body_html)
    date_modified = note.get("dateModified", datetime.now().strftime("%Y-%m-%d"))

    # Parse recipe from text
    parsed = parse_recipe_text(body_text, title)

    frontmatter = {
        "title": title,
        "slug": slug,
        "description": parsed.get("description", "")[:200],
        "source": "notes",
        "category": [],
        "author": "Family Recipe",
        "dateAdded": date_modified,
        "tags": [],
    }

    if parsed.get("prepTime"):
        frontmatter["prepTime"] = parsed["prepTime"]
    if parsed.get("cookTime"):
        frontmatter["cookTime"] = parsed["cookTime"]
    if parsed.get("totalTime"):
        frontmatter["totalTime"] = parsed["totalTime"]
    if parsed.get("servings"):
        frontmatter["servings"] = parsed["servings"]
    if parsed.get("ingredients"):
        frontmatter["ingredients"] = parsed["ingredients"]
    if parsed.get("instructions"):
        frontmatter["instructions"] = parsed["instructions"]

    RECIPES_DIR.mkdir(parents=True, exist_ok=True)
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    mdx_content = f"---\n{yaml_str}---\n"
    mdx_path.write_text(mdx_content, encoding="utf-8")
    return True


def main():
    if not EXPORT_FILE.exists():
        print("No notes export found. Run the AppleScript first:")
        print("  osascript scripts/export_notes.applescript")
        sys.exit(1)

    raw = EXPORT_FILE.read_text(encoding="utf-8")
    # AppleScript export may contain literal newlines inside JSON strings;
    # use strict=False to tolerate control characters.
    notes = json.loads(raw, strict=False)

    print(f"Found {len(notes)} notes in export.")

    new_count = 0
    for note in notes:
        title = note.get("title", "Untitled")
        if process_note(note):
            print(f"  + Added: {title}")
            new_count += 1
        else:
            print(f"  - Skipped (exists): {title}")

    print(f"\nDone. {new_count} new recipes added.")


if __name__ == "__main__":
    main()
