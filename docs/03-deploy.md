---
id: deploy
title: Deploy
order: 3
summary: "How the site is hosted on Cloudflare Workers, how a push deploys it, and how to check a deploy."
status: stable
updated: 2026-10-24
audience: [developers]
depends_on: [index, overview]
related: [recipes]
defines: []
answers:
  - Where does the site run?
  - How does a change reach production?
  - How do I test the Worker locally?
  - How do I check that a deploy worked?
---

# Deploy

## Where it runs

The Worker `recipe-book`, built with OpenNext (`@opennextjs/cloudflare`), serves recipes.nag.family as a custom domain and https://recipe-book.narendranag-cd1.workers.dev. Vercel hosted the site until 2026-10-21; that project is deleted, so there is no fallback.

| File                  | What it sets                                                                              |
| --------------------- | ----------------------------------------------------------------------------------------- |
| `wrangler.jsonc`      | The Worker, its assets, and the custom domain (`routes`, `custom_domain: true`); no secrets |
| `open-next.config.ts` | The static-assets incremental cache: read-only, so no ISR                                 |
| `public/_headers`     | `/_next/static/*` immutable                                                               |

Pages read `fs` at build time and would fail if rendered per request, which is why the cache is the static-assets one. A new recipe needs a rebuild.

## How a change reaches production

`.github/workflows/deploy.yml` runs `npm run deploy` on every push to `main`, using the repo secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. The sync bots push to `main` too (see [The sources](02-recipes.md#the-sources)), so their recipes deploy without review. Work that isn't ready goes on a branch.

## Commands

| Command           | Does                                                     |
| ----------------- | -------------------------------------------------------- |
| `npm run dev`     | Next dev server at http://localhost:3000                 |
| `npm run build`   | Next build; fails on a duplicate slug                    |
| `npm run lint`    | ESLint                                                   |
| `npm run preview` | OpenNext build run under workerd, the local Worker test  |
| `npm run deploy`  | OpenNext build and deploy to Workers                     |

Test the Worker with `npm run preview`, not `wrangler dev` after a build: prerendered pages only reach `.open-next/assets` in OpenNext's populate-cache step, which preview and deploy run.

npm 11 gates install scripts. `allowScripts` in `package.json` pins `esbuild` and `workerd` by version, so after bumping either run `npm install-scripts approve esbuild workerd`.

## Checking a deploy

Request every route key in `.next/prerender-manifest.json` and expect 200. Keys can hold non-ASCII characters, so encode each once with `encodeURI(decodeURI(key))`. A badly formed URL such as `/recipe/%E0%A4` returns 500 from Next's router before page code runs; that is expected.

The custom domain attach is refused (code 100117) while a DNS record Cloudflare doesn't manage exists for the hostname, and `override_existing_dns_record` doesn't change that.
