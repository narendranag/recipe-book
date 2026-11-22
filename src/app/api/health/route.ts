// GET /api/health, polled hourly by ops-check: ok and version (the git commit, baked in at build).
// No database, no secrets and no runtime env, so there is nothing else to report.
export const dynamic = "force-dynamic";

export function GET() {
  return Response.json(
    { ok: true, version: process.env.GIT_SHA ?? "dev" },
    { headers: { "Cache-Control": "no-store" } },
  );
}
