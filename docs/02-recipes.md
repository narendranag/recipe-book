---
id: recipes
title: Recipes
order: 2
summary: "The recipe file format, the three sources and their syncs, the slug rule, and the Claude rewrite."
status: stable
updated: 2026-10-24
audience: [developers]
depends_on: [index, overview]
related: [deploy]
defines: []
answers:
  - What goes in a recipe file?
  - How do recipes get from YouTube and Apple Notes into the site?
  - How are slugs chosen, and what happens when two recipes clash?
  - What does the rewrite step change?
---

# Recipes

## The file

A recipe is an `.mdx` file in `content/recipes/youtube/`, `content/recipes/notes/` or `content/recipes/manual/`. Everything is front matter; the body is unused. The fields are the `Recipe` type in `src/lib/types.ts`.

| Field          | Required | Meaning                                                    |
| -------------- | -------- | ---------------------------------------------------------- |
| `title`        | yes      | Display title                                              |
| `slug`         | no       | URL name; defaults to the file name without `.mdx`         |
| `description`  | yes      | One or two sentences under the title                       |
| `source`       | yes      | `youtube`, `notes` or `manual`                             |
| `category`     | yes      | List; each value becomes a `/category/<value>` page        |
| `ingredients`  | yes      | List of strings                                            |
| `instructions` | yes      | List of strings, one per step                              |
| `dateAdded`    | yes      | `YYYY-MM-DD`; the home page sorts by it, newest first      |
| `tags`         | no       | List; searched by Fuse.js                                  |
| `cuisine`, `prepTime`, `cookTime`, `totalTime`, `servings` | no | Shown on the page as given |
| `sourceUrl`, `youtubeVideoId`, `image`, `author`, `datePublished` | no | Set by the YouTube sync |
| `notes`        | no       | Free text shown after the steps                            |
| `rewritten`    | no       | `true` once the rewrite has run; the rewrite skips it then |

## The sources

| Source    | How a recipe arrives                                                                                       | Runs                                         |
| --------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `youtube` | `make sync-youtube` (`scripts/ingest_youtube.py`): one file per playlist video, parsed from its description, thumbnail saved | Weekly in `.github/workflows/sync-recipes.yml`, Monday 06:00 UTC, which also rewrites and commits to `main` |
| `notes`   | `make sync-notes`: `scripts/export_notes.applescript` exports the Apple Notes "Recipes" folder, `scripts/ingest_notes.py` writes the files | By hand, or `scripts/sync-notes.sh` under launchd, which also rewrites, commits and pushes |
| `manual`  | A file written by hand in `content/recipes/manual/`                                                        | By hand                                      |

The YouTube sync knows a video by its `youtubeVideoId`, so renaming a YouTube file is safe. It also deletes the file of any video that has left the playlist. The Notes sync knows a note by the file `notes/<slugified title>.mdx`, so renaming a Notes file makes the next sync add it again.

Repo secrets for the weekly sync: `YOUTUBE_PLAYLIST_URL`, `YOUTUBE_API_KEY`, `ANTHROPIC_API_KEY`.

## Slugs

A slug is unique across all three folders, because pages are routed by slug alone. Two guards keep it that way:

- `scripts/rewrite_recipes.py` checks every folder before it takes a slug. On a clash it appends the slugified `author` (or the source), then `-2`, `-3`… as needed.
- `getAllRecipes` in `src/lib/recipes.ts` throws on a duplicate slug, naming both files, so the build and the deploy fail instead of one page silently shadowing the other.

`generateStaticParams` returns raw slugs. Route params can arrive percent-encoded (slugs may hold Devanagari, categories may hold spaces), so pages decode them with `decodeParam`.

## The rewrite

`make rewrite` (`scripts/rewrite_recipes.py`) sends each recipe without `rewritten: true` to Claude (`claude-haiku-4-5-20251001`) with `ANTHROPIC_API_KEY`. Claude returns a clean title, description, category, cuisine, times, servings, ingredients, steps, notes and tags. The script keeps the source fields (`source`, `sourceUrl`, `youtubeVideoId`, `image`, `author`, `dateAdded`, `datePublished`), sets `rewritten: true`, and renames the file when the new title gives a new slug.
