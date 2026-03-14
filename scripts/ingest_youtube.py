#!/usr/bin/env python3
"""
YouTube playlist ingestion script.
Fetches video metadata from a YouTube playlist using yt-dlp,
parses recipe data from descriptions, and writes MDX files.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
import yaml
import yt_dlp

from parse_recipe import parse_recipe_text, slugify

# Paths relative to the repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = REPO_ROOT / "content" / "recipes" / "youtube"
IMAGES_DIR = REPO_ROOT / "public" / "images" / "recipes"


def get_playlist_url() -> str:
    """Get playlist URL from environment or config file."""
    url = os.environ.get("YOUTUBE_PLAYLIST_URL", "")
    if not url:
        config_path = REPO_ROOT / "scripts" / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
                url = config.get("youtube_playlist_url", "")
    if not url:
        print("Error: No YouTube playlist URL configured.")
        print("Set YOUTUBE_PLAYLIST_URL env var or add to scripts/config.yaml")
        sys.exit(1)
    return url


def download_thumbnail(url: str, slug: str) -> str | None:
    """Download a video thumbnail and return the public path."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    ext = "jpg"
    filename = f"{slug}.{ext}"
    filepath = IMAGES_DIR / filename

    if filepath.exists():
        return f"/images/recipes/{filename}"

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        filepath.write_bytes(resp.content)
        return f"/images/recipes/{filename}"
    except Exception as e:
        print(f"  Warning: Could not download thumbnail: {e}")
        return None


def write_recipe_mdx(video: dict) -> bool:
    """
    Write a single recipe MDX file from video metadata.
    Returns True if a new file was written, False if skipped.
    """
    title = video.get("title", "Untitled")
    slug = slugify(title)
    mdx_path = RECIPES_DIR / f"{slug}.mdx"

    if mdx_path.exists():
        return False

    video_id = video.get("id", "")
    description = video.get("description", "")
    channel = video.get("channel", video.get("uploader", ""))
    upload_date = video.get("upload_date", "")
    thumbnail = video.get("thumbnail", "")

    # Parse recipe from description
    parsed = parse_recipe_text(description, title)

    # Download thumbnail
    image_path = None
    if thumbnail:
        image_path = download_thumbnail(thumbnail, slug)

    # Format upload date
    date_published = ""
    if upload_date and len(upload_date) == 8:
        date_published = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    # Build frontmatter
    frontmatter = {
        "title": title,
        "slug": slug,
        "description": parsed.get("description", "")[:200],
        "source": "youtube",
        "sourceUrl": f"https://www.youtube.com/watch?v={video_id}",
        "youtubeVideoId": video_id,
        "category": [],
        "author": channel,
        "dateAdded": datetime.now().strftime("%Y-%m-%d"),
        "tags": [],
    }

    if image_path:
        frontmatter["image"] = image_path
    if date_published:
        frontmatter["datePublished"] = date_published
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

    # Write MDX file
    RECIPES_DIR.mkdir(parents=True, exist_ok=True)
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    mdx_content = f"---\n{yaml_str}---\n"
    mdx_path.write_text(mdx_content, encoding="utf-8")
    return True


def fetch_playlist(url: str) -> list[dict]:
    """Fetch all video metadata from a YouTube playlist."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "ignoreerrors": True,
        "no_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if not info:
        print("Error: Could not fetch playlist info.")
        return []

    entries = info.get("entries", [])
    return [e for e in entries if e is not None]


def main():
    url = get_playlist_url()
    print(f"Fetching playlist: {url}")

    videos = fetch_playlist(url)
    print(f"Found {len(videos)} videos in playlist.")

    new_count = 0
    for video in videos:
        title = video.get("title", "Untitled")
        if write_recipe_mdx(video):
            print(f"  + Added: {title}")
            new_count += 1
        else:
            print(f"  - Skipped (exists): {title}")

    print(f"\nDone. {new_count} new recipes added.")


if __name__ == "__main__":
    main()
