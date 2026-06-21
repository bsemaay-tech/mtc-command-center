# Pilot — CodeBurn (AI cost observability)

**Date:** 2026-06-21 · **By:** Claude Opus 4.8 · **Verdict:** ✅ KEEP / integrate as periodic cost check.

## What / install
Local CLI, reads AI-tool session logs on disk (`~/.claude/projects/...`, `~/.codex/sessions/...`, Cursor sqlite, 30+ tools). Pricing from LiteLLM, cached 24h at `~/.cache/codeburn/`. **No API key, no account, no proxy** — fully local, read-only.
- Install: `npm install -g codeburn` (Node 22.13+; have 24.13). Installed **v0.9.12**.
- Repo footprint: none (global npm). No venv, no files committed.

## Commands that work (v0.9.12)
`status` (compact today+month), `today`, `month`, `export --format json`, `models`, `optimize`, `compare`, `models`. NOTE: there is **no** `overview` subcommand (the backlog/earlier guess was wrong).

## Real result (this machine, 2026-06-21)
`codeburn status` → Today $0.00 / Month **$772.00, 7195 calls**.
`codeburn models` (all-time window, total **$1185.70 / 1496.5M tokens**):

| Provider | Model | Total tok | Cost |
|---|---|---|---|
| Claude | Opus 4.8 | 614.0M | **$563.50** |
| Codex | GPT-5.5 | 420.6M | $377.05 |
| Claude | Opus 4.7 | 142.0M | $140.25 |
| Claude | Sonnet 4.6 | 170.4M | $91.16 |
| Codex | GPT-5.4 Mini | 58.9M | $8.55 |
| OpenCode | **DeepSeek v4 Pro** | 84.6M | **$2.44** |
| … | (others) | | < $1 each |

## Why this matters for MTC (key finding)
Opus 4.8 + Codex GPT-5.5 = **~$940**. The cheap delegation harness (DeepSeek v4 Pro via OpenCode) = **$2.44**. The token-discipline policy (`AGENTS.md` + `_deepseek_driver`) exists but DeepSeek is barely used relative to the premium models — the exact "agents forget to delegate" problem the backlog named, now measured. CodeBurn turns that from a hunch into a number.

## Caveats
- Pricing accuracy depends on LiteLLM tables (Codex flagged this). Numbers here look plausible; spot-check before quoting to the dollar.
- `report` is an interactive dashboard — don't run it in a non-interactive agent shell; use `status`/`models`/`export`.

## Acceptance — PASS
Read-only, zero-risk, real data, actionable. Recommend running `codeburn status` / `codeburn models` at session boundaries and after big runs to track whether delegation is actually happening.

## Next (optional, approval-gated)
- `codeburn export --format json` into a dated file under `09_DOCS/AI_TOOLING/pilots/` for trend tracking.
- `codeburn mcp` exposes usage to agents over MCP — could let agents self-check spend. Evaluate later.
