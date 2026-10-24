---
id: overview
title: Overview
order: 1
summary: "What the recipe site is, how it is put together, and what is in and out of scope."
status: stable
updated: 2026-10-24
audience: [everyone]
depends_on: [index]
related: [recipes, deploy]
defines: []
answers:
  - "What is recipe-book for?"
  - How is the site built?
  - What is deliberately out of scope?
---

# Overview

## What it is

A public recipe site for the Nag family. The recipes come from two places the family already uses: a YouTube playlist of cooking videos and a "Recipes" folder in Apple Notes. Each one becomes a page with ingredients, steps, times and, for videos, the embedded video.

## How it is put together

```
YouTube playlist ──ingest_youtube.py──┐
                                      ├─▶ content/recipes/<source>/*.mdx ──rewrite_recipes.py──▶ cleaned .mdx
Apple Notes "Recipes" ─ingest_notes.py┘                                                              │
                                                                                                     ▼
                                   next build: src/lib/recipes.ts reads every .mdx with fs ──▶ static pages
                                                                                                     │
                                                                          OpenNext ──▶ Worker recipe-book
```

| Part        | Where                                                         |
| ----------- | ------------------------------------------------------------- |
| Framework   | Next.js 16 App Router, Tailwind 4, npm                        |
| Pages       | `/`, `/recipe/[slug]`, `/category/[category]`, all prerendered with `generateStaticParams` |
| Data        | `src/lib/recipes.ts`, reading `content/recipes/` at build time |
| Search      | Fuse.js in the browser (`src/components/SearchBar.tsx`)       |
| Images      | `public/images/recipes/`                                      |
| Structured data | JSON-LD on each recipe page                               |
| Hosting     | Cloudflare Workers via OpenNext; see [03 Deploy](03-deploy.md) |

## Scope

In scope: reading recipes, searching them, filtering by category, and adding recipes through the two syncs or by hand.

Out of scope: accounts, comments, editing in the browser, a database, and any runtime environment variable. Every change to a recipe is a commit and a rebuild.

## What stays hard

- Every push to `main` deploys, including the sync bots' commits, so a bad recipe file reaches production unless the build fails on it.
- Slugs are one namespace across all sources. Two recipes with the same title from different sources clash; see [Slugs](02-recipes.md#slugs).
