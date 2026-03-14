# Nag Family Recipes

**[recipes.nag.family](https://recipes.nag.family)**

A curated family recipe website inspired by NYT Cooking. Built with Next.js, deployed on Vercel.

## Features

- Recipes from YouTube playlists, Apple Notes, and manual entries
- Fuzzy search across titles, ingredients, tags, and categories
- Embedded YouTube videos for video recipes
- Interactive ingredient checklist
- Category filtering
- JSON-LD structured data for SEO
- Automated weekly sync from YouTube via GitHub Actions

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Adding Recipes

### Manually

Create an MDX file in `content/recipes/manual/`:

```yaml
---
title: "Recipe Name"
slug: "recipe-name"
description: "A short description"
source: "manual"
category: ["Category"]
ingredients:
  - "1 cup ingredient"
instructions:
  - "Step one."
dateAdded: "2026-03-13"
tags: ["tag1", "tag2"]
---
```

### From YouTube

1. Set your playlist URL in `scripts/config.yaml` or as `YOUTUBE_PLAYLIST_URL` env var
2. Install Python dependencies: `make install-scripts`
3. Run: `make sync-youtube`

### From Apple Notes

1. Create a "Recipes" folder in Apple Notes with your recipes
2. Run: `make sync-notes`

## Deployment

Deployed on Vercel with auto-deploy on push to `main`. A GitHub Action runs weekly to sync new YouTube recipes.

Add `YOUTUBE_PLAYLIST_URL` as a GitHub repo secret for automated syncing.
