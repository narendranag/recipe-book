# recipe-book

**What:** Nag Family Recipes: a NYT Cooking–style recipe site built from a YouTube playlist and Apple Notes.
**For:** family (public site, no login)
**Target:** web, live at [recipes.nag.family](https://recipes.nag.family)

## Context

- System and fleet: `~/claude-computer/docs/` (start with `FLEET.md`).
- How every project is built: `~/claude-computer/docs/DEV-GUIDELINES.md`. Deviations are listed below with the reason.
- Tasks: `TASKS.md` in this folder.
- Docs: `docs/` (read `docs/llms.txt` first); rebuild with `docs-build` after every change.

## What's here

- Next.js 16 App Router + Tailwind 4, npm (not pnpm). Pages: `/`, `/recipe/[slug]`, `/category/[category]`, all statically generated (`generateStaticParams`).
- Recipes are MDX front matter in `content/recipes/{youtube,notes}/` (51 files, 51 pages, as of 2026-10-24; a duplicate slug fails the build), read with `fs` in `src/lib/recipes.ts` at build time. Thumbnails live in `public/images/recipes/`. Search is client-side Fuse.js.
- No database, no runtime env vars, no auth.

## Run

`just setup|test|lint|run` (also `build`, `preview`, `deploy`) wrap the npm scripts: `npm install` · `npm run dev` (http://localhost:3000) · `npm run build` · `npm run lint` · `npm run preview` (OpenNext build under workerd) · `npm run deploy` (OpenNext build + deploy to Workers)

npm 11 gates install scripts: `allowScripts` in `package.json` pins `esbuild` and `workerd` by version, so after a bump run `npm install-scripts approve esbuild workerd`.

## Adding recipes

- **YouTube:** `make sync-youtube`, then `make rewrite` (Claude cleans titles, ingredients and steps). GitHub Action `sync-recipes.yml` does both weekly (Mon 06:00 UTC) and commits to `main`. Repo secrets: `YOUTUBE_PLAYLIST_URL`, `YOUTUBE_API_KEY`, `ANTHROPIC_API_KEY`.
- **Apple Notes:** `make sync-notes` (osascript export of the "Recipes" folder → MDX), or `scripts/sync-notes.sh` under launchd. It commits and pushes on its own.
- **By hand:** an MDX file in `content/recipes/manual/` (README has the front matter).

## Deploy

- Cloudflare Workers via OpenNext (`@opennextjs/cloudflare`), Worker `recipe-book`, serving recipes.nag.family as a custom domain since 2026-10-21 (also https://recipe-book.narendranag-cd1.workers.dev). Ported per `~/claude-computer/docs/runbooks/vercel-to-cloudflare.md`.
  - `open-next.config.ts` uses the static-assets incremental cache. Pages read `fs` at build time and would 500 if rendered per request. That cache is read-only, so there's no ISR: a new recipe needs a rebuild.
  - `public/_headers` marks `/_next/static/*` immutable. `wrangler.jsonc` has no secrets, because the site needs none.
  - `.github/workflows/deploy.yml` deploys on push to `main` (repo secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`).
- Vercel is retired: the `recipe-book` project was deleted on 2026-10-21, so there is no Vercel fallback.

Every push to `main` deploys, including the bots' recipe commits, so a broken MDX file breaks production.

## Gotchas

- `next dev` writes `AGENTS.md` at the root (Next's agent rules) and re-creates it if it is deleted; it is committed on purpose.
- Test the Worker locally with `npm run preview`, not `wrangler dev` after a build. The prerendered pages only reach `.open-next/assets` at preview/deploy time (OpenNext's populate-cache step).
- To check a deploy, request every route in `.next/prerender-manifest.json` and expect 200 (65 real routes as of 2026-10-24; `/_not-found` 404 and `/_global-error` 500 are Next's own and expected). Keys can hold non-ASCII characters, so encode them once: `encodeURI(decodeURI(key))`.
- Route params can arrive percent-encoded. Pages decode them with `decodeParam` (`src/lib/recipes.ts`), and `generateStaticParams` must return raw values, never pre-encoded ones.
- A badly formed URL (`/recipe/%E0%A4`) returns 500 from Next's router before page code runs. Vercel did the same.
- The custom domain is set in `wrangler.jsonc` (`routes`, `custom_domain: true`). Cloudflare refuses the attach (code 100117) while a DNS record it doesn't manage exists for the hostname, and `override_existing_dns_record` doesn't change that. The cutover deleted the old CNAME and attached in one script.
- TTFB from mini is about 0.5 s (connect 156 ms to the MRS colo) against Vercel's 0.11 s. That's network routing, not the Worker.
