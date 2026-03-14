#!/usr/bin/env python3
"""
Recipe rewriter: uses Claude to clean up raw imported recipes.

Takes messy recipe data (from YouTube descriptions, Apple Notes, etc.) and
rewrites them with clean titles, proper ingredient lists, clear instructions,
and appropriate categories/tags. Removes YouTube cruft, social media links,
hashtags, and promotional text.

Marks processed recipes with 'rewritten: true' in frontmatter to avoid
re-processing.
"""

import os
import sys
import json
import time
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = REPO_ROOT / "content" / "recipes"

# All known categories and cuisines for consistency
CATEGORIES = [
    "Main Course", "Side Dish", "Appetizer", "Dessert", "Baking",
    "Breakfast", "Snack", "Soup", "Salad", "Sauce", "Condiment",
    "Drink", "Vegetarian", "Vegan",
]
CUISINES = [
    "Indian", "Chinese", "Italian", "Mexican", "Thai", "Japanese",
    "French", "American", "British", "Mediterranean", "Korean",
    "Middle Eastern", "Vietnamese",
]


def get_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        config_path = REPO_ROOT / "scripts" / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f) or {}
                key = config.get("anthropic_api_key", "")
    if not key:
        print("Error: No ANTHROPIC_API_KEY set.")
        print("Set it as an env var or add anthropic_api_key to scripts/config.yaml")
        sys.exit(1)
    return key


def load_recipe(path: Path) -> tuple[dict, str]:
    """Load a recipe MDX file, return (frontmatter_dict, raw_content)."""
    raw = path.read_text(encoding="utf-8")
    # Parse YAML frontmatter between --- markers
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                # Malformed YAML — return raw text as body so it can still be rewritten
                return {"title": path.stem.replace("-", " ").title()}, raw
            body = parts[2].strip()
            return fm, body
    return {}, raw


def save_recipe(path: Path, frontmatter: dict, body: str = ""):
    """Save a recipe MDX file."""
    yaml_str = yaml.dump(
        frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False
    )
    content = f"---\n{yaml_str}---\n"
    if body:
        content += f"\n{body}\n"
    path.write_text(content, encoding="utf-8")


def get_unprocessed_recipes() -> list[Path]:
    """Find all recipe MDX files that haven't been rewritten yet."""
    recipes = []
    for mdx_path in sorted(RECIPES_DIR.rglob("*.mdx")):
        fm, _ = load_recipe(mdx_path)
        if not fm.get("rewritten"):
            recipes.append(mdx_path)
    return recipes


def rewrite_recipe(api_key: str, frontmatter: dict, body: str) -> dict:
    """Call Claude to rewrite a recipe into clean, structured format."""
    import httpx

    # Build the raw recipe text for Claude
    raw_parts = []
    raw_parts.append(f"Title: {frontmatter.get('title', 'Untitled')}")
    if frontmatter.get("description"):
        raw_parts.append(f"Description: {frontmatter['description']}")
    if frontmatter.get("ingredients"):
        raw_parts.append("Ingredients:")
        for ing in frontmatter["ingredients"]:
            raw_parts.append(f"  - {ing}")
    if frontmatter.get("instructions"):
        raw_parts.append("Instructions:")
        for i, step in enumerate(frontmatter["instructions"], 1):
            raw_parts.append(f"  {i}. {step}")
    if frontmatter.get("notes"):
        raw_parts.append(f"Notes: {frontmatter['notes']}")
    if body:
        raw_parts.append(f"Additional content:\n{body}")

    raw_text = "\n".join(raw_parts)

    prompt = f"""You are a recipe editor. Clean up this raw recipe data and return a properly structured recipe as JSON.

RAW RECIPE:
{raw_text}

RULES:
1. TITLE: Write a clean, appetizing title. Remove ALL CAPS, hashtags, channel names, "Recipe -", website names. Keep it simple (e.g. "Butter Chicken", "Chocolate Lava Cake").
2. DESCRIPTION: Write 1-2 sentences describing the dish. Make it appetizing and informative. Remove any YouTube/social media cruft, URLs, hashtags.
3. INGREDIENTS: Clean list. Each item should be a proper ingredient with quantity and preparation (e.g. "2 cups flour, sifted"). Remove section headers like "For the Gravy" — instead, organize ingredients in the natural order they're used. Remove non-Latin script duplicates (keep English only). If ingredients are mixed with instructions, separate them.
4. INSTRUCTIONS: Clear numbered steps. Each step should be a complete action. Remove promotional text, "subscribe" messages, social links. If the original has section headers like "For the Gravy" / "For the Chicken", incorporate that context into the steps naturally (e.g. "To make the gravy: ...").
5. CATEGORY: Pick 1-3 from: {json.dumps(CATEGORIES)}
6. CUISINE: Pick one from: {json.dumps(CUISINES)} or leave empty if unclear.
7. TAGS: 3-6 lowercase tags for searchability (e.g. "chicken", "quick", "spicy", "weeknight").
8. TIMES: Extract or estimate prep_time, cook_time, total_time as human-readable strings (e.g. "20 min", "1 hour"). Leave empty if you genuinely can't tell.
9. SERVINGS: Extract or estimate. Leave empty if you genuinely can't tell.

Return ONLY valid JSON with these exact keys:
{{
  "title": "...",
  "description": "...",
  "ingredients": ["...", "..."],
  "instructions": ["...", "..."],
  "category": ["...", "..."],
  "cuisine": "...",
  "tags": ["...", "..."],
  "prepTime": "...",
  "cookTime": "...",
  "totalTime": "...",
  "servings": "...",
  "notes": "..."
}}

Do NOT include any text outside the JSON object. The "notes" field should contain any useful cooking tips from the original, or be empty."""

    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )

    if resp.status_code != 200:
        print(f"    API error {resp.status_code}: {resp.text[:200]}")
        return {}

    data = resp.json()
    text = data["content"][0]["text"].strip()

    # Extract JSON from response (handle markdown code blocks)
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"    JSON parse error: {e}")
        print(f"    Raw response: {text[:300]}")
        return {}


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    import re
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def process_recipe(api_key: str, path: Path) -> bool:
    """Rewrite a single recipe file. Returns True if successful."""
    fm, body = load_recipe(path)
    title = fm.get("title", path.stem)
    print(f"  Rewriting: {title}")

    result = rewrite_recipe(api_key, fm, body)
    if not result:
        print(f"    FAILED — skipping")
        return False

    # Build updated frontmatter, preserving source metadata
    new_title = result.get("title", title)
    new_slug = slugify(new_title)

    updated = {
        "title": new_title,
        "slug": new_slug,
        "description": result.get("description", fm.get("description", "")),
        "source": fm.get("source", "manual"),
        "rewritten": True,
    }

    # Preserve source-specific fields
    if fm.get("sourceUrl"):
        updated["sourceUrl"] = fm["sourceUrl"]
    if fm.get("youtubeVideoId"):
        updated["youtubeVideoId"] = fm["youtubeVideoId"]
    if fm.get("image"):
        updated["image"] = fm["image"]

    updated["category"] = result.get("category", [])
    if result.get("cuisine"):
        updated["cuisine"] = result["cuisine"]
    if result.get("prepTime"):
        updated["prepTime"] = result["prepTime"]
    if result.get("cookTime"):
        updated["cookTime"] = result["cookTime"]
    if result.get("totalTime"):
        updated["totalTime"] = result["totalTime"]
    if result.get("servings"):
        updated["servings"] = result["servings"]
    updated["ingredients"] = result.get("ingredients", fm.get("ingredients", []))
    updated["instructions"] = result.get("instructions", fm.get("instructions", []))
    if result.get("notes"):
        updated["notes"] = result["notes"]
    updated["author"] = fm.get("author", "Family Recipe")
    updated["dateAdded"] = fm.get("dateAdded", "")
    if fm.get("datePublished"):
        updated["datePublished"] = fm["datePublished"]
    updated["tags"] = result.get("tags", [])

    # Rename file if slug changed
    new_path = path.parent / f"{new_slug}.mdx"
    if new_path != path:
        if new_path.exists():
            # Avoid overwriting — keep original filename
            new_path = path
            updated["slug"] = fm.get("slug", path.stem)
        else:
            path.unlink()

    save_recipe(new_path, updated)
    print(f"    -> {updated['title']}")
    return True


def main():
    api_key = get_api_key()
    recipes = get_unprocessed_recipes()

    if not recipes:
        print("No unprocessed recipes found.")
        return

    print(f"Found {len(recipes)} recipes to rewrite.\n")

    success = 0
    failed = 0
    for i, path in enumerate(recipes):
        ok = process_recipe(api_key, path)
        if ok:
            success += 1
        else:
            failed += 1
        # Rate limiting: small delay between API calls
        if i < len(recipes) - 1:
            time.sleep(0.5)

    print(f"\nDone. {success} rewritten, {failed} failed.")


if __name__ == "__main__":
    main()
