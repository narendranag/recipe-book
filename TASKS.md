# Tasks — recipe-book

## Now

- [ ] **Resume here:** nothing half done. Waiting on the owner's OK for the Epicure similar-recipes plan (`## Next`) and its two `(owner)` questions. On OK, run the spike in `~/projects/explore/epicure/epicure.md` §Spike (branch `later-2026-10-24` of `narendranag/explore`) in a scratch venv on mini, writing nothing into this repo

## Next

- [ ] "Similar recipes" and "swap this ingredient" on recipe pages, from Epicure ingredient embeddings computed at build time — plan ready, owner's OK. The owner asked for it on 2026-10-24 (their answer to Q1 of the Epicure explore). Background: `~/projects/explore/epicure/epicure.md` (branch `later-2026-10-24` of `narendranag/explore`), §Applicability and §Spike; read it there.
  - **What:** a "Similar recipes" row (top 5) on each `/recipe/[slug]` page, and per-ingredient swap hints. Both precomputed into static JSON; nothing runs per request, and the Worker and the site's runtime are unchanged.
  - **Step 1, spike (the note's §Spike, 5 h operator time, 0 USD):** Epicure core vs all-MiniLM-L6-v2 on the 51 recipes, in a scratch venv on mini, writing nothing into this repo. The owner judges 20 pairs blind (30 min). Kill it if coverage stays under 70 % after 60 min of mapping. The note's decision tree (adopt / trial / watch / skip) decides whether step 2 happens.
  - **Step 2, build (only on "adopt"):**
    - `scripts/similar_recipes.py`: normalises each `ingredients` line (lowercase, strip quantities and units, exact then fuzzy match to Epicure's 1,790 names, then `scripts/ingredient_aliases.yaml`). It averages each recipe's vectors, ranks by cosine and writes `src/data/similar.json` (slug → top 5, ingredient → nearest names), which is committed. It prints unmapped lines. `make similar`; `sync-recipes.yml` and `sync-notes.sh` run it after `rewrite_recipes.py`.
    - Epicure files are fetched into a git-ignored cache by the script, not committed. `similar.json` is the only artefact.
    - `src/lib/recipes.ts` reads `similar.json`; `src/app/recipe/[slug]/page.tsx` adds the row and a hint under each ingredient. The build fails if `similar.json` names a slug that doesn't exist, and warns on recipes missing from it.
    - A CC BY 4.0 attribution for Epicure in the site footer. `docs/02-recipes.md` gets a "Similar recipes" section; then `docs-build`.
  - **Size:** spike 5 h. Build about 1 day: similar recipes about 5 h, swap hints about 3 h. Upkeep is about 3 min per new recipe for alias mapping (the note's cost model: about 11 h in year 1).
  - **Risks:** free-text mapping is the real cost and recurs with each new recipe; Epicure neighbours show what *pairs* with an ingredient, not what *replaces* it, so swap hints ship only after a cook's review (a reviewed list in the alias file); core and chem draw on FlavorDB (academic use), fine for a family site, but the co-occurrence variant is the clean choice if it ever goes commercial; the bots push to `main`, so an unmapped line must warn, never fail the build.
- [ ] (owner) For the similar-recipes spike: is 30 minutes of blind judging (20 pairs) OK as its only call on your time? Proposed default: yes, scheduled once the spike's lists are ready
- [ ] (owner) Will recipe-book stay a family site? It decides whether Epicure core (FlavorDB, academic use) is acceptable or the co-occurrence variant is needed. Proposed default: family site, so core

## Later


## Done

- [x] 2026-10-24 justfile (setup, test, lint, run, build, preview, deploy) for the brains standard, round 3 (fleet session's request); setup, test, lint and run checked
- [x] 2026-10-24 Deleted the merged `cloudflare-workers` and `fix/duplicate-slugs` branches, local and origin (owner's OK; both 0 commits ahead of `main`)
- [x] 2026-10-22 Vercel's account-level `nag.family` domain entry removed by the fleet session (`vercel domains rm`, `~/claude-computer/TASKS.md`); `vercel domains ls` shows 0 domains on 2026-10-24
- [x] 2026-10-24 Merged `fix/duplicate-slugs` into `main` (fast-forward to b3f68fc) with the owner's OK; deploy.yml run 40088616018 green; 65/65 real routes 200 on recipes.nag.family
- [x] 2026-10-24 Duplicate slugs: the YouTube `butter-chicken` and `orange-posset` were shadowed by the notes copies. Renamed to `butter-chicken-your-food-lab` and `orange-posset-florency-dias`; `rewrite_recipes.py` now checks slugs across every folder, and the build fails on a duplicate (tested). 51 files, 51 pages. On `fix/duplicate-slugs` (5dd3743, 70c3a8d), not merged
- [x] 2026-10-24 Project docs in `docs/` per the documentation standard: index, overview, recipes, deploy; `docs-build` passes. On `fix/duplicate-slugs` (bf1ad4f)
- [x] 2026-10-21 Retired Vercel: project `recipe-book` deleted, with its deployments and its recipes.nag.family assignment. The account-level `nag.family` domain entry on Vercel was left alone

- [x] 2026-10-21 Cutover: recipes.nag.family serves from the Worker (custom domain). Vercel CNAME deleted and replaced in one script; 63/63 routes 200, immutable /_next/static, http→https, deploy.yml green (run 39545918994). TTFB from mini 0.51 s vs Vercel's 0.11 s (MRS routing)
- [x] 2026-10-21 Production deploy: `cloudflare-workers` merged into `main` (fast-forward) and pushed
- [x] 2026-10-21 Repo secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `ANTHROPIC_API_KEY` set from the store with `deploy-secrets` (fleet session)
- [x] 2026-10-21 Fix 404s on non-ASCII slugs and categories with spaces (decode route params; stop double-encoding category static params)
- [x] 2026-10-20 Port to OpenNext on `cloudflare-workers`: next 16.4.2, OpenNext 1.20.12, wrangler 4.151.3; staged on workers.dev, route-for-route parity with production
- [x] 2026-10-20 Env inventory: Vercel has no env vars or Marketplace storage; the app reads no env. Nothing to copy
- [x] 2026-10-20 Brain: CLAUDE.md + TASKS.md
