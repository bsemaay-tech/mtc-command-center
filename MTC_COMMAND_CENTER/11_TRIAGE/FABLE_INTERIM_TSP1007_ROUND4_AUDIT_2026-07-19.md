# Fable independent audit — interim TS-P1-007 round-4 repair

Audit date: 2026-07-19
Auditor: Claude Fable 5 (independent; no shared context with the builder session)
Builder: Codex GPT-5
Worktree audited: `C:\P1IF`
Branch: `feature/interim-daily-loss-wiring`
Target commit: `acb83b5b1dc464bad0db28f8a104015e3c1aa864`
Parent: `b11a2e36f18287db347ce53f7379139b72aba940` (docs-only D017)
Handoff brief: `FABLE_INTERIM_TSP1007_ROUND4_AUDIT_HANDOFF_2026-07-19.md`
Round-3 BLOCK report: `CODEX_INTERIM_TSP1007_REAUDIT2_2026-07-18.md`

## VERDICT: PASS-WITH-NITS

No path was found that can rewrite canonical closed PnL, corrupt either risk-gate input,
duplicate terminal/partial accounting, or leave owned broker exposure unprotected or
misclassified as foreign. All round-3 BLOCK findings are verifiably repaired. Every
builder evidence claim was independently reproduced this session. Nits are listed below;
none is a deployment blocker.

## Scope identity — VERIFIED

- HEAD `acb83b5b`, parent `b11a2e36`, branch `feature/interim-daily-loss-wiring`, worktree
  clean before, during-restore-checked, and after the audit (`git status --porcelain` empty,
  `git diff --exit-code HEAD` clean on both production files after each restore).
- `git diff --stat HEAD~1 HEAD`: exactly 4 files, 417 insertions, 33 deletions —
  `bridge/store/db.py`, `bridge/engine/orders.py`, `tests/test_interim_risk_wiring.py`,
  `docs/20_INTERIM_TSP1007_RISK_WIRING.md`. No threshold, strategy, config, schema-version,
  Pine, parity, runtime, or deployment file in the diff.
- `update_trade_exit` (the old mutable close) now has **zero production callers** — only
  tests and a legacy build-plan doc reference it. The engine gate path still consumes
  `store.realized_pnl_today` + `store.consecutive_closed_losses`
  (`bridge/engine/engine.py:240-252`) — earlier-round wiring intact.

## Evidence reproduced this session (exact commands and results)

From `C:\P1IF\IBKR_PAPER_BRIDGE`:

```text
python -m pytest tests/test_interim_risk_wiring.py -q   -> 32 passed in 3.43s
python -m pytest tests -q                                -> 164 passed, 1 warning in 15.53s
```

From `C:\P1IF`:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q -> 32 passed in 3.56s
python -m pytest IBKR_PAPER_BRIDGE/tests -q                              -> 164 passed, 1 warning in 13.04s
```

The single warning is the pre-existing Starlette TestClient deprecation.

**Semantic red proof reproduced:** with committed tests unchanged, `git restore
--source=b11a2e36` on the two production files → **8 failed / 24 passed**, and the failing
set is exactly the eight cases the builder listed (late-TP rewrite, TP→SL rewrite,
SL→CLOSE rewrite, conflicting duplicate fill_id, partial-decision duplicate,
entry-remainder phantom close, cross-order overfill close, non-atomic close). Restored to
HEAD; blob equality and clean status verified.

**Half-exit old-code proof reproduced:** the half-exit engine-path test against `066b49cc`
production files → **1 failed** (old phantom full-qty close breached the daily boundary and
blocked engine submission). The builder's disclosure that this test passes against
`b11a2e36` (which already contains the round-2 cumulative-VWAP repair) is accurate — its
red target is `066b49cc`, and that is honestly recorded in the handoff. Restored clean.

## Independent adversarial probes (beyond the committed suite)

14 probes written and run this session against HEAD (scratchpad script, temp DBs, repo
untouched). All pass:

1. Per-order ENTRY overfill → `ORDER_OVERFILL` + DISARM, trade untouched.
2. Event role ≠ stored order role → `FILL_ROLE_CONFLICT` + DISARM, no fill row, no close.
3. `fill_id` reuse with mutated **fee / ts / qty / funding / px** (5 variants, fresh
   manager = post-restart) → `FILL_ID_CONFLICT` every time; first row byte-identical;
   canonical PnL −11 unchanged; single `TRADE_CLOSED`.
4. Loss streak at max−1 through the real engine path → still submits, stays ARMED
   (boundary complement to the committed at-limit trigger test).
5. CANCELED entry remainder → terminal close of the filled portion proceeds with
   fills-derived basis (correct PnL, one `TRADE_CLOSED`) — remainder guard applies only to
   live statuses `{OPEN, SUBMITTED, PENDING}`, consistent with the codebase's existing
   live-status definition (`find_live_orders_by_attributes`).
6. Float-dust exit (entry+1e-10, inside 1e-9 tolerance) → clean close, no quarantine.
7. Late ENTRY fill after canonical close → `POST_CLOSE_FILL` + DISARM; entry basis and PnL
   immutable (pre-repair this silently rewrote `entry_px` under a persisted PnL).
8. Exact redelivery of the closing fill on a closed trade → benign no-op (no quarantine,
   no duplicate decision) — the crash-recovery replay path.
9. Double `close_trade_once_with_decision` → second call refused; first PnL and single
   decision stand.
10. Trade-level dust overfill (entry+2e-9 via an SL order large enough to not trip the
    per-order check) → `TRADE_OVERFILL` + DISARM, trade left open. (An initial probe
    variant tripped `ORDER_OVERFILL` first — the earlier check masks the later one for
    same-size orders; both outcomes are fail-closed.)

## Round-3 findings — closure status

| Round-3 BLOCK finding | Status |
|---|---|
| Late/mixed exit fill rewrote closed PnL (−2000→0, +10→0, −10→−2.5) | CLOSED — post-close distinct fills quarantine; canonical row immutable (committed tests + probes) |
| `INSERT OR REPLACE` fill mutation (−11→+10) and partial-decision duplication | CLOSED — insert-once with INSERTED/EXACT_DUPLICATE/CONFLICT classification; decisions gated on INSERTED |
| Flat partial entry terminally closed with live entry remainder → later fill became foreign | CLOSED — `ENTRY_REMAINDER_LIVE` keeps trade open/owned across restart; reconcile reprotects or flattens (committed test verifies no `FOREIGN_POSITION_IGNORED`) |
| Non-atomic close + `TRADE_CLOSED` | CLOSED — single SQLite transaction; forced-abort rollback + exact-redelivery recovery proven by committed test |
| Half-exit test not semantic | CLOSED — qty 100 crosses the −2000 boundary on old code; 1F red vs `066b49cc` reproduced |

## Nits (non-blocking)

- **N-01:** No committed test exercises `ORDER_OVERFILL` (per-order overfill). Probe 1
  proves the behavior, but a regression would not be caught by the suite.
- **N-02:** No committed test exercises `FILL_ROLE_CONFLICT`. Same status (probe 2).
- **N-03:** `FILL_ROLE_CONFLICT` quarantines **before** persisting the fill, so the raw
  fill evidence lives only in the events row — asymmetric with `POST_CLOSE_FILL`, which
  retains the row. Fail-closed either way; worth aligning in the full TS-P1-007.
- **N-04:** Narrow crash window in the `ENTRY_REMAINDER_LIVE` path: if the process dies
  after the `TRADE_PARTIAL_EXIT` decision commits but before `set_meta(DISARMED)`, the
  exact redelivery on restart is an EXACT_DUPLICATE and skips the quarantine, so the
  bridge is not DISARMED although the flat-with-live-remainder condition persists. The
  trade correctly stays open and no gate input is corrupted — only the protective DISARM
  is missed. Comparable multi-commit crash windows pre-exist elsewhere; acceptable for the
  interim scope, should be folded into the full TS-P1-007 atomicity pass.
- **N-05:** Quarantined overfill fills remain in `fills` and therefore contribute to
  subsequent `order_fill_totals`/`trade_fill_totals` reads. Because every such path
  DISARMs and the trade is left open for manual reconciliation, this is fail-closed, but
  operators should know the totals include quarantined rows.
- **N-06 (cosmetic):** Stale comment at `tests/test_interim_risk_wiring.py:674` still says
  "INSERT OR REPLACE coalesces the row"; production is now INSERT OR IGNORE.

## Doc/D017 check — VERIFIED

Doc 20's round-4 addendum accurately describes the verified behavior (insert-once fill
identity, immutable canonical closes, remainder ownership, atomic terminal state, semantic
half-exit proof, 32/164 evidence). D017 scope unchanged: interim gate PnL remains gross
minus captured fees; funding attribution stays deferred to TS-P1-005. No
threshold/strategy/schema change anywhere in the diff.

## Safety confirmation for this audit session

Read-only audit plus local tests only. NO push, PR, merge, deploy, runtime start/restart,
scheduler, credential, exchange, testnet, paper, ARM, threshold, config, schema, strategy,
Pine, parity, or `C:\P2RT` action. `C:\P1IF` left clean at `acb83b5b` (verified after
every restore). Probe artifacts and DBs lived in the session scratchpad/temp only.

## What this verdict authorizes — and does not

- PASS-WITH-NITS clears the **independent-audit gate** for the round-4 repair.
- It does **not** authorize push, PR, merge, deploy, `C:\P2RT` changes, ARM, or a new
  monitoring window. Those remain a separate, explicit Barış approval (deploy gate
  unspent). No monitoring window may be cited as risk-control evidence until the fix is
  deployed to the runtime that produces that evidence.
- Recommended (non-blocking) follow-ups for the full TS-P1-007: add committed tests for
  N-01/N-02, align evidence retention (N-03), close the N-04 crash window, and fix the
  stale comment (N-06).
