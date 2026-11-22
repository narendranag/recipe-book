import { execSync } from "node:child_process";
import type { NextConfig } from "next";

// The git commit, for /api/health. CI sets GITHUB_SHA; a local build asks git.
function gitSha(): string {
  if (process.env.GITHUB_SHA) return process.env.GITHUB_SHA;
  try {
    return execSync("git rev-parse HEAD", { encoding: "utf8" }).trim();
  } catch {
    return "dev";
  }
}

const nextConfig: NextConfig = {
  env: { GIT_SHA: gitSha() },
};

export default nextConfig;
