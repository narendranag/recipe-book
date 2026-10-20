# Tasks — recipe-book

## Now

- [ ] Narendra: check staging at https://recipe-book.narendranag-cd1.workers.dev

## Next

- [ ] Narendra: repo secrets `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` (`gh secret set …`) for `deploy.yml`
- [ ] Narendra: OK the production deploy (merge `cloudflare-workers` → `main`). Vercel also builds `main` until it's disconnected
- [ ] Narendra: OK the DNS cutover: recipes.nag.family as a Worker custom domain (Always Use HTTPS is already on for the zone); then `https-check recipes.nag.family` and re-measure TTFB
- [ ] Retire the Vercel project once the custom domain serves from Cloudflare (ask first)

## Later

- [ ] Fix 404s on non-ASCII slugs and categories with spaces (`/category/Main Course`, `/recipe/béchamel-sauce-pasta`, the Hindi-titled butter chicken). Also broken on Vercel. Likely cause, unverified: params compared without `decodeURIComponent`
- [ ] 51 MDX files but 49 recipe pages: `butter-chicken` and `orange-posset` exist in both notes/ and youtube/, and one of each pair is shadowed
- [ ] `ANTHROPIC_API_KEY` repo secret for the weekly rewrite step (it's missing, so CI can't rewrite)
- [ ] Project docs in `docs/` per the documentation standard

## Done

- [x] 2026-10-20 Brain: CLAUDE.md + TASKS.md
- [x] 2026-10-20 Env inventory: Vercel has no env vars or Marketplace storage; the app reads no env. Nothing to copy
- [x] 2026-10-20 Port to OpenNext on `cloudflare-workers`: next 16.4.2, OpenNext 1.20.12, wrangler 4.151.3; staged on workers.dev, route-for-route parity with production
