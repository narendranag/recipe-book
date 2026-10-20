import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

// OpenNext's Cloudflare adapter: how this Next.js app runs on Workers (`npm run deploy`).
// Pages read content/recipes with `fs` at build time, so the prerendered pages must be served
// from the static-assets incremental cache; without it they re-render per request and 500.
// That cache is read-only: no ISR, so new recipes need a rebuild and deploy.
export default defineCloudflareConfig({
  incrementalCache: staticAssetsIncrementalCache,
  enableCacheInterception: true,
});
