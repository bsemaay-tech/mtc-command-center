# P0-20 / P0-30 checker re-verification on the merged base — 2026-09-07

Independent re-run of the two checkers PR #161 landed, performed by the Claude Lead in the remote
Linux container **after** the merge, against `master` `fe35b7c`. The Lead's original record
(`C:\tmp\P020_P030_RECON_QA_20260907\LEAD_RECORD.md`) was produced on the Windows host in the
reconciliation worktree, before the merge; this record is a second, independent observation on a
different platform and a different base commit. It accepts nothing — both packages remain
unaccepted, exactly as PR #161 states.

## Environment

| | Lead record (Windows host) | This re-run (Linux container) |
|---|---|---|
| Base | reconciliation worktree, pre-merge | `master` `fe35b7c`, post-merge |
| Python | Windows host interpreter | `3.11.15` |
| Flag | `PYTHONDONTWRITEBYTECODE=1` | `PYTHONDONTWRITEBYTECODE=1` |

## Commands and exit codes

```
PYTHONDONTWRITEBYTECODE=1 python3 check_shared_risk_calculator.py   # exit 0
PYTHONDONTWRITEBYTECODE=1 python3 check_market_data_collector.py    # exit 0
```

## `check_shared_risk_calculator.py` — PASS

```
CLI EXTREME NAMED REFUSALS: PASS
CLI UNDERFLOW RISK BOUND AND EXACT SUBNORMAL CONTROL: PASS
MODIFIED COPY: DETECTED
ALL REFUSALS DROPPED: DETECTED
FLOAT ARITHMETIC: DETECTED
ROUND_HALF_UP: DETECTED
MULTIPLIER IGNORED: DETECTED
NONFINITE GUARD DROPPED: DETECTED
PADDED VERSION GUARD DROPPED: DETECTED
SETTINGS TYPE GUARD DROPPED: DETECTED
CALLER CONTEXT: DETECTED
OVERFLOW REFUSAL DROPPED: DETECTED
ZERO REFUSAL DROPPED: DETECTED
SHARED RISK CALCULATOR CHECK: PASS
```

All eleven mutation controls named in the PR body are `DETECTED`, matching the Lead's record
exactly. The check is self-confirming: each control asserts the pre-fix behaviour is still
detectable, so a `PASS` is not merely the absence of a failure.

## `check_market_data_collector.py` — PASS

```
COMPLETE PERSISTED RECORDS (21 fields, two bars): PASS
PERSISTED FENCE PROOF (open): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT
REINTRODUCTION MUTANT (persisted open corrupted): DETECTED
PERSISTED FENCE PROOF (env_lineage_id): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT
REINTRODUCTION MUTANT (persisted env_lineage_id corrupted): DETECTED
FOUR-INTERVAL ARCHIVE/GAP/ROLLOVER MATRIX: PASS
INTERVAL-STEP MUTANT (1h/4h swapped): DETECTED
GAP-REPORT CLI (gap + complete): PASS
OFFLINE COLLECTOR LIFECYCLE (success + wait error): PASS
LIFECYCLE MUTANT (close skipped after wait error): DETECTED
MODIFIED COPY (gap detection removed): DETECTED
CARRIED FENCE PROOF (forming bar): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT
CARRIED FENCE PROOF (refusal): OLD_FENCE_ACCEPTS_DEVIANT; NEW_FENCE_REJECTS_DEVIANT
REINTRODUCTION MUTANT (packet interpretation): DETECTED
REINTRODUCTION MUTANT (packet interpretation (static boundary)): DETECTED
REINTRODUCTION MUTANT (durable gap event): DETECTED
REINTRODUCTION MUTANT (concrete SDK import): DETECTED
REINTRODUCTION MUTANT (forming bar written): DETECTED
REINTRODUCTION MUTANT (eth_account import): DETECTED
REINTRODUCTION MUTANT (os.environ read): DETECTED
REINTRODUCTION MUTANT (order call): DETECTED
NETWORK ATTEMPTS: 0
MARKET DATA COLLECTOR CHECK: PASS
```

`NETWORK ATTEMPTS: 0` is asserted by the checker itself, which patches `socket` and fails on any
wait or close (`check_market_data_collector.py:146,153`) and asserts an empty attempt list at
`:508`, `:909` and `:930`. The container reproduces the offline claim rather than assuming it.

## Two counting corrections to the PR #161 body

Both are **under**-counts in the PR; the checker proves more than the PR claimed, so neither
weakens the evidence. Recorded so the numbers in the record match the tool's actual output.

1. The body says "three fence proofs". The run emits **four**: `PERSISTED FENCE PROOF (open)`,
   `PERSISTED FENCE PROOF (env_lineage_id)`, `CARRIED FENCE PROOF (forming bar)` and
   `CARRIED FENCE PROOF (refusal)`.
2. The body's reintroduction-mutant list omits `persisted open corrupted`. The run emits
   **thirteen** `DETECTED` mutants, not the twelve enumerated.

## What this does not establish

Nothing about acceptance. **P0-20 acceptance still requires caps, quantisation, import identity
into `simulate_slice`, and `UNSIMULATED_CONTROLS`**, and its own dependency `WP-P0-12` is stopped
by `OD-20260826-1` / `OD-20260826-8` with its in-flight work absent from this repository. P0-30
integration remains blocked behind P0-21 thresholds and P0-26 alerting. The four files' placement
at the repository root remains the open question PR #161 recorded and deliberately did not decide.
