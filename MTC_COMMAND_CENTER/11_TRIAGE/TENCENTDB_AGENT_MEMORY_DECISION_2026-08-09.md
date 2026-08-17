# TencentDB Agent Memory — Adoption Decision (2026-08-09)

**Decider:** Claude Fable 5 (Lead), on Barış's request to evaluate a ChatGPT report built from two YouTube transcripts.
**Subject:** [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) — 4-tier agent memory (L0–L3) + v2.0.0 "Team Memory" hub (Chat Memory / Skill / Wiki / CodeGraph), MIT, v2.0.0 released 2026-08-03.

## Decision

1. **Trading repo (`Tradingview_LAB_CLEAN`): DO NOT INSTALL.** Not as pilot either.
2. **Hermes sandbox: isolated pilot APPROVED IN PRINCIPLE, blocked on Docker.** v2 ships as 3 Docker images; this machine has no Docker (`docker: command not found`, verified 2026-08-09). Installing Docker Desktop is a system change → Barış decision.
3. **Two patterns adopted without the daemon:**
   - `_AI_MEMORY/TOOL_OUTPUT_OFFLOAD_PROTOCOL.md` (TOOL-OFFLOAD v1) — big tool outputs → file + compact index + ID-based return to raw evidence.
   - `_AI_MEMORY/REPO_MAP.md` — static module-level repo map, generated from mechanical inventory by DeepSeek, refreshed after structural merges. Never symbol-level (3–5M token cost, instant staleness).

## Why not in the trading repo

- **Governance conflict:** `_AI_MEMORY` is canonical, owner-ratified, git-versioned. LLM-auto-extracted memory = second source of truth without provenance; memory-poisoning surface in a repo carrying kill-switch/broker/TESTNET gates. Signed-skill attestation and ACL are still open discussions upstream.
- **Cache economics inverted for us:** upstream issue #120 (open): dynamic memory injection breaks prompt-prefix cache (reported hits 91→63%, 96→83%). Our costs are subscription-quota based (Claude Max, ChatGPT Pro) and DeepSeek's cheapness depends on cache hits — token-count savings can still cost MORE quota/money.
- **Integration mismatch:** most mature adapters = Hermes + OpenClaw. Our main implementer (Codex CLI) has no native support (upstream #833). Claude Code path = proxy, newest and least proven.
- **Maturity:** v2.0.0 six days old at decision time; default-branch architecture churned within weeks; OpenClaw integration patches compiled files (upstream #851 calls it fragile).
- Vendor benchmarks (221M→85.6M tokens, WideSearch 33→50%) have no independent reproduction; report itself found a ~33.09% vs ~31.6% arithmetic inconsistency in the SWE-bench claim.

## Hermes pilot conditions (when unblocked)

- Own workspace + own SQLite DB; never pointed at this repo; `_AI_MEMORY` stays canonical; retrieved memory ≠ trusted instruction.
- Pilot only on non-trading sandbox tasks (no broker/TESTNET/gate surfaces).
- Measure before/after: cache-hit rate, quota burn, task success — judge on the bill, not the token count.
- Install performed deterministically by Lead/Codex via CLI, **not** by Hermes itself (fresh agent + infra install = bad combo; Hermes smoke state as of 2026-08-09: CLI works, primary openai-codex backend returns no response — credential pool exhausted; DeepSeek provider responds).

## Revisit trigger (all required)

Upstream #120 closed (cache-friendly injection) + native Codex support + signed memory/ACL shipped + v2 API stable 2–3 months + at least one independent benchmark reproduction.
