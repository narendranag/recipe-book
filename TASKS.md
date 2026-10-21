# Tasks — recipe-book

## Now

## Next

## Later

- [ ] 51 MDX files but 49 recipe pages: `butter-chicken` and `orange-posset` exist in both notes/ and youtube/, and one of each pair is shadowed
- [ ] Project docs in `docs/` per the documentation standard

## Done

- [x] 2026-10-21 Retired Vercel: project `recipe-book` deleted, with its deployments and its recipes.nag.family assignment. The account-level `nag.family` domain entry on Vercel was left alone

- [x] 2026-10-21 Cutover: recipes.nag.family serves from the Worker (custom domain). Vercel CNAME deleted and replaced in one script; 63/63 routes 200, immutable /_next/static, http→https, deploy.yml green (run 39545918994). TTFB from mini 0.51 s vs Vercel's 0.11 s (MRS routing)
- [x] 2026-10-21 Production deploy: `cloudflare-workers` merged into `main` (fast-forward) and pushed
- [x] 2026-10-21 Repo secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `ANTHROPIC_API_KEY` set from the store with `deploy-secrets` (fleet session)
- [x] 2026-10-21 Fix 404s on non-ASCII slugs and categories with spaces (decode route params; stop double-encoding category static params)
- [x] 2026-10-20 Port to OpenNext on `cloudflare-workers`: next 16.4.2, OpenNext 1.20.12, wrangler 4.151.3; staged on workers.dev, route-for-route parity with production
- [x] 2026-10-20 Env inventory: Vercel has no env vars or Marketplace storage; the app reads no env. Nothing to copy
- [x] 2026-10-20 Brain: CLAUDE.md + TASKS.md
