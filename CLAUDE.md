# recipe-book

**What:** Nag Family Recipes: a NYT Cooking–style recipe site built from a YouTube playlist and Apple Notes.
**For:** family (public site, no login)
**Target:** web, live at [recipes.nag.family](https://recipes.nag.family)

## Context

- System and fleet: `~/claude-computer/docs/` (start with `FLEET.md`).
- How every project is built: `~/claude-computer/docs/DEV-GUIDELINES.md`. Deviations are listed below with the reason.
- Tasks: `TASKS.md` in this folder.

## What's here

- Next.js 16 App Router + Tailwind 4, npm (not pnpm). Pages: `/`, `/recipe/[slug]`, `/category/[category]`, all statically generated (`generateStaticParams`).
- Recipes are MDX front matter in `content/recipes/{youtube,notes}/` (54 as of 2026-10-20), read with `fs` in `src/lib/recipes.ts` at build time. Thumbnails live in `public/images/recipes/`. Search is client-side Fuse.js.
- No database, no runtime env vars, no auth.

## Run

`npm install` · `npm run dev` (http://localhost:3000) · `npm run build` · `npm run lint`

## Adding recipes

- **YouTube:** `make sync-youtube`, then `make rewrite` (Claude cleans titles, ingredients and steps). GitHub Action `sync-recipes.yml` does both weekly (Mon 06:00 UTC) and commits to `main`. Repo secrets: `YOUTUBE_PLAYLIST_URL`, `YOUTUBE_API_KEY`. `ANTHROPIC_API_KEY` is referenced by the workflow but **not set**, so the rewrite step can't run in CI.
- **Apple Notes:** `make sync-notes` (osascript export of the "Recipes" folder → MDX), or `scripts/sync-notes.sh` under launchd. It commits and pushes on its own.
- **By hand:** an MDX file in `content/recipes/manual/` (README has the front matter).

## Deploy

- **Now:** Vercel, auto-deploy on push to `main` (project `recipe-book`, domain recipes.nag.family).
- **Porting to:** Cloudflare Workers via OpenNext, on branch `cloudflare-workers`, following `~/claude-computer/docs/runbooks/vercel-to-cloudflare.md`. Staged on `workers.dev`. Main and production stay on Vercel until Narendra OKs the DNS cutover and the production deploy.

Every push to `main` deploys, including the bots' recipe commits, so a broken MDX file breaks production.
