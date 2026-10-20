# Decisions — recipe-book

- [mini] [2026-10-20] Move hosting from Vercel to Cloudflare Workers via OpenNext, staged on workers.dev first — fleet-wide port (`~/claude-computer/docs/runbooks/vercel-to-cloudflare.md`)
- [mini] [2026-10-20] Static-assets incremental cache, no ISR — pages read `fs` at build time; every recipe change is a rebuild, which push-to-main already gives
- [mini] [2026-10-20] Stay on npm, not pnpm — the repo and its lockfile are npm; switching buys nothing for the port
