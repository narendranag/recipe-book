# Tasks — recipe-book

Resume: 2026-10-24 Later list done and merged; only the owner's two deletion questions remain (Vercel `nag.family` domain entry, merged `cloudflare-workers` branch).

## Now

## Next

## Later

- [ ] (owner) Remove the account-level `nag.family` domain entry on Vercel? Nothing on Vercel uses it now. Left in place because only the project deletion was asked for. Proposed default: remove it (it is a deletion, so it waits for your yes)
- [ ] (owner) Delete the merged `cloudflare-workers` branch (local and origin)? It's fully merged into `main`. Proposed default: delete both (a deletion; waits for your yes)

## Done

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
