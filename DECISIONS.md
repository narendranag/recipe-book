# Decisions — recipe-book

- [mini] [2026-10-20] Move hosting from Vercel to Cloudflare Workers via OpenNext, staged on workers.dev first — fleet-wide port (`~/claude-computer/docs/runbooks/vercel-to-cloudflare.md`)
- [mini] [2026-10-20] Static-assets incremental cache, no ISR — pages read `fs` at build time; every recipe change is a rebuild, which push-to-main already gives
- [mini] [2026-10-20] Stay on npm, not pnpm — the repo and its lockfile are npm; switching buys nothing for the port
- [mini] [2026-10-21] Cut recipes.nag.family over to the Worker custom domain by deleting the Vercel CNAME and attaching in one script, with automatic restore on failure — Cloudflare refused the attach (100117) while the external CNAME existed, and `override_existing_dns_record` only replaces Worker-managed records; Narendra OK'd the delete
- [mini] [2026-10-21] Keep the Vercel project as a fallback for now — rollback is recreating the CNAME to f163c48bd91bc12e.vercel-dns-017.com (DNS-only, TTL 600); retiring it is a separate yes
- [mini] [2026-10-21] Retire Vercel: delete the `recipe-book` project — Narendra asked; the site has served from the Worker since the cutover, and the Vercel project held no env vars or storage
