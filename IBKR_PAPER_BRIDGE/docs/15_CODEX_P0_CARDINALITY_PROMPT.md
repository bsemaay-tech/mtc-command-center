# 15_CODEX_P0_CARDINALITY_PROMPT — positionTpsl response fix + final approved P0 attempt

Date: 2026-07-12. Author: Claude Opus 4.8 (auditor). Builder: Codex GPT-5 (fresh session — this
file is self-contained; you need no prior chat context).

## 0. Who you are and where you work

- Repo: `C:\LAB\Tradingview_LAB_CLEAN` (the LIVE repo; the sibling `C:\LAB\tradingview-lab` is
  frozen — never touch it). Read repo `AGENTS.md` if you have not.
- Project: `IBKR_PAPER_BRIDGE/` — the **Crypto Paper Bridge** on Hyperliquid (dir name is legacy).
- Branch: `feature/ibkr-bridge-final`. A repo hook flips HEAD back to master between tool calls —
  commit with inline `git checkout feature/ibkr-bridge-final && git add <exact paths> && git
  commit -m "..."` in ONE command, after EVERY task.
- Design is FINAL. Do not redesign. Binding docs, read before coding:
  `docs/01_ARCHITECTURE.md` §6.1, `docs/00_PREREG.md` §4 (P0 exit criteria),
  `docs/13_CODEX_P0_RETRY_PROMPT.md` §5 (smoke run procedure),
  `docs/14_P0_SMOKE_REPORT.md` (history of all three P0 attempts).
- Run everything with `PYTHONUTF8=1`. Pytest works from BOTH repo root
  (`python -m pytest IBKR_PAPER_BRIDGE/tests -q`) and from `IBKR_PAPER_BRIDGE/`. Current
  baseline: **72 passed, 1 warning**.

## 1. Situation (state as of 2026-07-12, all audited by Claude on real code)

P1 (mock runtime) passed audit. Three P0 testnet smoke attempts happened:

1. **Attempt 1:** failed pre-connect — env var held the wallet ADDRESS, not the key. Fixed:
   `HL_API_WALLET_KEY` now holds a valid 32-byte agent-wallet private key (verified length-only).
2. **Attempt 2:** connected, but (a) the account is **unifiedAccount** mode — balance authority is
   `spot_user_state` (999 mock USDC), not `user_state.marginSummary`; (b) the error parser crashed
   on a string-shaped response, masking the real rejection. Both fixed and audited.
3. **Attempt 3:** got furthest — connect ✓, unified equity 999 ✓, candles ✓, price-rule-compliant
   plan ✓ (entry 57600, SL 56448, 5-sig-fig rounding). Failed at response parsing:
   **the real `positionTpsl` bulk response contained FEWER status objects than the adapter's
   one-status-per-request assumption** → `HyperliquidOrderError("bulk order response did not
   contain every status")`. Post-checks: zero open orders, zero positions, clean WS disconnect.
   The raw exchange response was NOT persisted, so the true response shape is still unknown.

Working facts: credentials valid; unified balance reads correctly; price rounding compliant;
smoke script (`tools/smoke_p0.py`) covers key-precheck → connect → account → candles → plan →
atomic place → verify → modify → cancel → verify-cleanup → flatten-guard → disconnect, JSON log
at `docs/p0_smoke_log.json`.

## 2. Authorization record (Barış, 2026-07-12 — do not ask again)

Barış approved: the three LOCAL fixes below, then **exactly ONE** bounded P0 testnet smoke
attempt. One attempt means one run of the script; if it fails: stop, clean up, report. A further
attempt needs NEW approval. **P2 (unattended testnet ARM) is NOT approved — never ARM the engine.**

## 3. Hard rails (non-negotiable)

1. NEVER print, log, echo, or persist `HL_API_WALLET_KEY` or any private key. Length/existence
   checks only. Grep every changed file and log for `[0-9a-fA-F]{64,}` before committing — zero
   matches required (the account ADDRESS, 40 hex, is fine to log).
2. TESTNET ONLY. `HL_LIVE_ACK` stays unset; no mainnet code path may execute.
3. Order scope = the bounded smoke exactly: one tiny resting entry (~$11–12 notional, limit far
   below market so it cannot fill) + native SL trigger, one modify, cancel all owned cloids,
   reduce-only flatten only if a position unexpectedly exists.
4. No LLM runtime calls, no backtests, no Pine/parity, no `MTC_COMMAND_CENTER/` edits (except the
   handoff files listed in task R). Preserve untracked dirs (`Youtube transcrip/` etc.).
5. No destructive git (no reset --hard, no checkout -- on tracked files, no stash).

## 4. Task C1 — real positionTpsl response cardinality (local)

The adapter (`bridge/broker/hyperliquid.py`) assumes one status object per submitted order in
`place_bracket` (and `reprotect_position`); the real exchange returned fewer for a positionTpsl
group. Rework:

1. Do NOT require `len(statuses) == len(requests)`. Map whatever statuses arrive to orders by
   position/known shape; a trigger order with no status of its own is treated as
   accepted-with-position (pending verification).
2. IMMEDIATELY after the bulk call, verify ground truth via `open_orders()` + `positions()`:
   every submitted cloid must be either visible as a resting/trigger order or explainable
   (filled). Build the returned result dict from that verification, not from status-count
   assumptions. If a cloid is missing AND unexplained → raise with detail, triggering cleanup.
3. Unit tests: response fixtures with cardinality 1, 2, and 3 for a 3-order group; an
   error-status mix; verification-driven result construction.

## 5. Task C2 — raw response capture on mismatch (local)

When response parsing fails or cardinality surprises us, persist the FULL raw exchange response
into the smoke log (and an `events` row when running under the engine), passed through the
existing secret-redaction helper (64+ hex → `[redacted]`). Raise the redaction cap to 4000 chars
for this diagnostic payload (the current 500 is too small). We must never again lose the
exchange's actual answer. Unit test: a surprising response shape ends up redacted-but-complete in
the log structure.

## 6. Task C3 — guaranteed owned-cloid cleanup (local)

Wrap the smoke's order phase so ANY exception after the bulk call triggers cleanup that does NOT
depend on parsed statuses: query `open_orders()` for our deterministic cloids and cancel each;
verify zero owned orders remain; flatten if a position exists. Unit test: bulk call raises
mid-parse → cleanup still cancels resting owned orders.

## 7. Gates before the network attempt

- Full suite green from BOTH repo root and `IBKR_PAPER_BRIDGE/` (expect >72).
- Secret grep (rail 1) on all changed files + logs: zero matches.
- All of C1–C3 committed.

## 8. The single approved P0 attempt

Run `PYTHONUTF8=1 python IBKR_PAPER_BRIDGE/tools/smoke_p0.py` from repo root under PowerShell (so
Windows user env is inherited). Expected to PASS now — credentials, unified balance, and price
rules are all validated; only the response-shape assumption remained. If it still fails: the log
now contains the full redacted raw response — stop, clean up (C3 guarantees it), report honestly.
No second run.

## 9. Task R — report for Claude's audit

Append to `docs/14_P0_SMOKE_REPORT.md` (keep all prior runs as history):
1. C1–C3: what changed, file:line, new tests, full pytest summaries pasted (both CWDs).
2. Complete new `p0_smoke_log.json` inline, incl. oids/cloids placed and cancelled.
3. The REAL positionTpsl response shape observed (redacted) — document it in
   `docs/01_ARCHITECTURE.md` §6.1 as a dated amendment note if it differs from the spec's
   assumption.
4. Secret-scan confirmation (exact grep command + result).
5. Honest remaining gaps. Update `docs/03_STATUS.md` and append a dated section to
   `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
   (format: `## [Codex GPT-5] 2026-07-12 — Bridge P0 attempt 4`).

P0 exit criteria (PREREG §4): connect + account + live candle + place entry & SL trigger group +
cancel, all steps in JSON log. If this run passes them all, state "P0 exit criteria MET, pending
Claude audit" — do not self-declare the gate closed.
