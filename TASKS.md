# Tasks — recipe-book

## Now

- [ ] Port Vercel → Cloudflare Workers (OpenNext), staged on workers.dev on branch `cloudflare-workers`

## Next

- [ ] Narendra: OK the DNS cutover of recipes.nag.family to the Worker (custom domain)
- [ ] Narendra: OK the production deploy (merge `cloudflare-workers` → `main`)
- [ ] Narendra: repo secrets `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` for the deploy workflow
- [ ] Retire the Vercel project once the custom domain serves from Cloudflare (ask first)

## Later

- [ ] `ANTHROPIC_API_KEY` repo secret for the weekly rewrite step (it's missing, so CI can't rewrite)
- [ ] Project docs in `docs/` per the documentation standard

## Done

- [x] 2026-10-20 Brain: CLAUDE.md + TASKS.md
