#!/usr/bin/env python3
"""
YouTube playlist ingestion script.

Uses the YouTube Data API v3 for CI environments (reliable, no bot detection).
Falls back to yt-dlp for local use if no API key is set.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
import yaml

from parse_recipe import parse_recipe_text, slugify

# Paths relative to the repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = REPO_ROOT / "content" / "recipes" / "youtube"
IMAGES_DIR = REPO_ROOT / "public" / "images" / "recipes"


def get_config() -> dict:
    """Get playlist ID and API key from environment or config file."""
    config = {}
    config_path = REPO_ROOT / "scripts" / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}

    playlist_url = os.environ.get("YOUTUBE_PLAYLIST_URL", config.get("youtube_playlist_url", ""))
    api_key = os.environ.get("YOUTUBE_API_KEY", config.get("youtube_api_key", ""))

    if not playlist_url:
        print("Error: No YouTube playlist URL configured.")
        print("Set YOUTUBE_PLAYLIST_URL env var or add to scripts/config.yaml")
        sys.exit(1)

    # Extract playlist ID from URL
    playlist_id = playlist_url
    if "list=" in playlist_url:
        playlist_id = playlist_url.split("list=")[1].split("&")[0]

    return {"playlist_id": playlist_id, "api_key": api_key}


def download_thumbnail(url: str, slug: str) -> str | None:
    """Download a video thumbnail and return the public path."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{slug}.jpg"
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


def fetch_playlist_api(playlist_id: str, api_key: str) -> list[dict]:
    """Fetch video metadata using YouTube Data API v3."""
    videos = []
    page_token = ""
    base_url = "https://www.googleapis.com/youtube/v3"

    # Step 1: Get all video IDs from the playlist
    video_ids = []
    while True:
        url = (
            f"{base_url}/playlistItems?part=snippet&maxResults=50"
            f"&playlistId={playlist_id}&key={api_key}"
        )
        if page_token:
            url += f"&pageToken={page_token}"

        resp = requests.get(url, timeout=30)
        if resp.status_code != 200:
            print(f"Error fetching playlist: {resp.status_code} {resp.text[:200]}")
            return []

        data = resp.json()
        for item in data.get("items", []):
            snippet = item["snippet"]
            vid_id = snippet.get("resourceId", {}).get("videoId", "")
            if vid_id:
                video_ids.append(vid_id)

        page_token = data.get("nextPageToken", "")
        if not page_token:
            break

    # Step 2: Get full video details (including description) in batches of 50
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        ids_str = ",".join(batch)
        url = (
            f"{base_url}/videos?part=snippet,contentDetails"
            f"&id={ids_str}&key={api_key}"
        )
        resp = requests.get(url, timeout=30)
        if resp.status_code != 200:
            print(f"Error fetching video details: {resp.status_code}")
            continue

        data = resp.json()
        for item in data.get("items", []):
            snippet = item["snippet"]
            thumbnails = snippet.get("thumbnails", {})
            thumb_url = (
                thumbnails.get("maxres", {}).get("url")
                or thumbnails.get("high", {}).get("url")
                or thumbnails.get("medium", {}).get("url", "")
            )
            videos.append({
                "id": item["id"],
                "title": snippet.get("title", "Untitled"),
                "description": snippet.get("description", ""),
                "channel": snippet.get("channelTitle", ""),
                "publishedAt": snippet.get("publishedAt", ""),
                "thumbnail": thumb_url,
            })

    return videos


def fetch_playlist_ytdlp(playlist_url: str) -> list[dict]:
    """Fetch video metadata using yt-dlp (local fallback)."""
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not installed. Install with: pip install yt-dlp")
        return []

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "ignoreerrors": True,
        "no_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    if not info:
        return []

    videos = []
    for e in info.get("entries", []):
        if e is None:
            continue
        upload_date = e.get("upload_date", "")
        published = ""
        if upload_date and len(upload_date) == 8:
            published = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
        videos.append({
            "id": e.get("id", ""),
            "title": e.get("title", "Untitled"),
            "description": e.get("description", ""),
            "channel": e.get("channel", e.get("uploader", "")),
            "publishedAt": published,
            "thumbnail": e.get("thumbnail", ""),
        })

    return videos


def get_existing_video_ids() -> dict[str, Path]:
    """Scan all YouTube recipe MDX files and return a map of videoId -> file path."""
    video_ids = {}
    if not RECIPES_DIR.exists():
        return video_ids
    for mdx_path in RECIPES_DIR.glob("*.mdx"):
        raw = mdx_path.read_text(encoding="utf-8")
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) >= 3:
                try:
                    fm = yaml.safe_load(parts[1]) or {}
                except Exception:
                    continue
                vid = fm.get("youtubeVideoId", "")
                if vid:
                    video_ids[vid] = mdx_path
    return video_ids


def write_recipe_mdx(video: dict, existing_ids: dict[str, Path]) -> bool:
    """
    Write a single recipe MDX file from video metadata.
    Returns True if a new file was written, False if skipped.
    """
    title = video.get("title", "Untitled")
    slug = slugify(title)
    mdx_path = RECIPES_DIR / f"{slug}.mdx"

    video_id = video.get("id", "")
    if video_id in existing_ids or mdx_path.exists():
        return False

    description = video.get("description", "")
    channel = video.get("channel", "")
    published = video.get("publishedAt", "")
    thumbnail = video.get("thumbnail", "")

    # Parse recipe from description
    parsed = parse_recipe_text(description, title)

    # Download thumbnail
    image_path = None
    if thumbnail:
        image_path = download_thumbnail(thumbnail, slug)

    # Format publish date
    date_published = ""
    if published:
        date_published = published[:10]  # "2024-01-15T..." -> "2024-01-15"

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


def main():
    config = get_config()
    playlist_id = config["playlist_id"]
    api_key = config["api_key"]

    if api_key:
        print(f"Fetching playlist {playlist_id} via YouTube Data API...")
        videos = fetch_playlist_api(playlist_id, api_key)
    else:
        print("No YOUTUBE_API_KEY set, falling back to yt-dlp...")
        playlist_url = os.environ.get("YOUTUBE_PLAYLIST_URL", "")
        if not playlist_url:
            config_path = REPO_ROOT / "scripts" / "config.yaml"
            if config_path.exists():
                with open(config_path) as f:
                    cfg = yaml.safe_load(f) or {}
                    playlist_url = cfg.get("youtube_playlist_url", "")
        videos = fetch_playlist_ytdlp(playlist_url)

    print(f"Found {len(videos)} videos in playlist.")

    existing_ids = get_existing_video_ids()
    playlist_video_ids = {v.get("id", "") for v in videos if v.get("id")}

    # Add new videos
    new_count = 0
    for video in videos:
        title = video.get("title", "Untitled")
        if write_recipe_mdx(video, existing_ids):
            print(f"  + Added: {title}")
            new_count += 1
        else:
            print(f"  - Skipped (exists): {title}")

    # Remove recipes for videos no longer in the playlist
    removed_count = 0
    for vid_id, path in existing_ids.items():
        if vid_id not in playlist_video_ids:
            print(f"  x Removed (not in playlist): {path.stem}")
            path.unlink()
            # Also remove thumbnail if it exists
            thumb = IMAGES_DIR / f"{path.stem}.jpg"
            if thumb.exists():
                thumb.unlink()
            removed_count += 1

    print(f"\nDone. {new_count} new, {removed_count} removed.")


if __name__ == "__main__":
    main()
