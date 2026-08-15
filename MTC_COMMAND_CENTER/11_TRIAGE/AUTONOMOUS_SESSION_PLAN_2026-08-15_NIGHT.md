# Autonomous session plan — 2026-08-15 19:20 → 2026-08-16 07:20 (+03)

Lead: Claude Opus 5, session `192dd112`, working in `C:\R7FINAL` on branch
`codex/rp7-r1-r4-repair-20260815`.

Owner authorizations in force for this session:

- One fresh Pathscope `gpt-5.6-sol` high execution-audit **retry** — CONSUMED,
  see block 1. Stop before any repair cycle if it finds required changes.
- Packet 10: run the Bridge test suite locally at a declared SHA.
- Packet 11: prepare an exact hours figure for the owner's signature.
- Fill idle time with both freeze-input preparation and Bridge deploy-readiness
  preparation, in parallel lanes.
- Deploy finish line for estimating: **bridge on KVM2, DISARMED, TESTNET-only,
  loopback-only.** Not the dashboard, not the AI lab.

Everything else stays gated: host contact, deployment, credentials, services,
broker/exchange, ARM, orders, TESTNET/mainnet execution, Pine, parity, MTC,
trading, merge to master, and any economic action.

## Preflight (completed before any write)

| check | result |
|---|---|
| Worktree | `C:\R7FINAL`, branch `codex/rp7-r1-r4-repair-20260815` |
| HEAD at start | `2d401822b1543e90721704d60b81b9b6b026db02` |
| `git status --porcelain` | empty |
| Active writer | none — no `codex.exe` process; the only Claude processes are this session |
| Lock | Pathscope and Audit-2 rows claimed in `SESSION_LOCK.md`, logged |
| Primary checkout | `C:\LAB\Tradingview_LAB_CLEAN` untouched, as instructed |

## Block plan

### Block 1 — 19:20-20:00 — Pathscope retry (DONE)

Dispatched the authorized retry with a corrected dual-form identity table after
finding that the 2026-08-14 table was unsatisfiable in either derivation mode.
Transport precondition held: `sandbox: danger-full-access` confirmed in the
session header before any work.

Result: **REQUEST_CHANGES**, three REQUIRED findings, no nits. Lane stopped at
the owner boundary exactly as instructed; no repair opened, no further audit
dispatched. Records committed at `ddc8a9c8`.

### Block 2 — 20:00-21:30 — four parallel lanes

| lane | worker | subject | writes |
|---|---|---|---|
| A | Lead (local) | Packet 10 provisional suite baseline, run twice for determinism | Packet 10 record |
| B | Codex `secondary`, sol medium | Packet 11 hours measurement | one new file |
| C | Codex `free`, sol high | Bridge VPS deploy-readiness refresh | one new file |
| D | Codex `fourth`, sol high | Freeze-blocker map reconciliation after RP7 | one new file |

Each lane works in its own detached worktree at `ddc8a9c8` and writes exactly
one new file. The Lead copies results into the branch and commits. No lane holds
a `SESSION_LOCK` row; each writes only its own new file.

### Block 3 — 21:30-23:30 — integrate and prepare the two suite repairs

Integrate lane output. Prepare — but do not merge — evidence-backed patches for
the two Bridge suite failures found in block 2, each on its own branch with a
repair report. One is environment-dependent and one is a stale expectation; both
sit on the deploy critical path through checklist item 9.

### Block 4 — 23:30-01:30 — Claude Pro audit window

Use the Claude Pro window (not Max) for the highest-value independent review
available: the two prepared suite repairs and the Bridge readiness roll-up.
Claude Max stays untouched unless a genuine T0 flagship slot needs it.

### Block 5 — 01:30-04:30 — freeze-input preparation

Documentation-only: Packet 9 skeleton fill, the authority-consolidation record
that `OPEN_QUESTIONS_FOR_DISPATCHER.md` section 7 requires, and the D026 map
carry-forward. Nothing here implies freeze or host authority.

### Block 6 — 04:30-06:30 — consolidation

Refresh `GLOBAL_HANDOFF.md`, the remaining-work dashboard, and the morning
handoff with real numbers rather than the provisional ones.

### Block 7 — 06:30-07:20 — clean stop

Verify the tree, commit and push everything, release the `SESSION_LOCK` rows,
write the memory hand-back, and leave the owner a short decision list.

## Standing rules for this session

1. No idling. If a lane blocks on an owner decision, pull the next item from the
   preparation backlog rather than waiting.
2. Heavy work goes to Codex; GLM and DeepSeek take mechanical work. Claude Pro is
   for audits, Claude Max only for a real T0 flagship slot.
3. Every claim in every record must be reproducible from a command printed in
   that record. No inferred statuses.
4. Any REQUIRED finding on any lane stops that lane at the owner boundary. It
   does not start a repair cycle.
