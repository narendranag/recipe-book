# justfile — setup / test / lint / run are the contract every repo keeps (~/claude-computer/docs/DEV-GUIDELINES.md).

setup:
    npm ci

dev:
    npm run dev

run: dev

build:
    npm run build

# No unit tests: the build is the test. It prerenders every recipe and fails on a duplicate slug.
test: build

# Typecheck, ESLint, then the docs standard.
lint:
    npx tsc --noEmit
    npm run lint
    docs-build --check docs

# OpenNext build under workerd: the local Worker test (not `wrangler dev`).
preview:
    npm run preview

# OpenNext build + deploy to Workers. A push to main already does this (.github/workflows/deploy.yml).
deploy:
    npm run deploy
    just smoke

# Production's /api/health must answer ok (ops-check polls the same route). SMOKE_URL overrides it.
smoke url=env_var_or_default("SMOKE_URL", "https://recipes.nag.family"):
    curl -fsS --retry 6 --retry-delay 5 --retry-all-errors "{{ url }}/api/health" | tee /dev/stderr | jq -e '.ok == true' > /dev/null
