# Parity Freeze -- MT CORE2 BTCUSDT.P 15m

**Frozen**: 2026-02-14
**Engine commit**: Do NOT modify `src/engine/` without re-running parity regression.

## Frozen Profile

- `execution_profile_id`: `base_close_intrabar_protective_v1`
- `profile semantics`: bar-close decisioning, intrabar protective fills, bar-close discretionary closes
- Any run using a different fill model must emit a different profile id and cannot be compared against this freeze as if it were the same contract.

## Fills / Execution Contract

### Order of Operations per Bar (9-step)

1. **SL check** -- `strategy.exit(stop=)` intrabar fill at exact price + slippage
2. **TP check** -- `strategy.exit(limit=)` intrabar fill at exact price + slippage
3. **Break-Even update** -- adjusts SL for *next* bar; no fill this bar
4. **Trailing activation** -- arms trail if price exceeds `start_r`; updates for *next* bar
5. **Trailing stop check** -- `strategy.exit(stop=trail)` intrabar fill
6. **Opposite-signal exit** -- `strategy.close()` bar-close fill
7. **Filter-block exit** -- `strategy.close()` bar-close fill
8. **Time-stop exit** -- `strategy.close()` bar-close fill
9. **Entry processing** -- new entry if signal + all gates pass

### Fill Categories

| Category | Pine Equivalent | Fill Price | Same-Bar Re-entry? |
|----------|----------------|------------|---------------------|
| A: Intrabar | `strategy.exit(stop/limit)` | exact level + slippage | YES |
| B: Bar-close | `strategy.close()` | bar close + slippage | NO (next bar), except `OPP_SIGNAL` flip |

**Intrabar exits** (SL, TP, BE, TRAIL): position closes at the exact stop/limit price.
**Bar-close exits** (`TRAIL-via-close`, `FILTER_BLOCK`, `TIME_STOP`, `MANUAL`): fill at bar close. Entry only on *next* bar.
`OPP_SIGNAL` also fills at bar close, but when `allow_flip=true` and `exit_on_opposite_signal=true`, the opposite-direction entry may reopen on that same bar.

### Same-Bar Re-entry Rule

When `allow_same_bar_reentry=true` and an intrabar exit fires:
- Signal-mode entry gate is re-evaluated WITHOUT the per-signal-cooldown quota.
- `_BAR_CLOSE_EXITS` (`TRAIL`, `FILTER_BLOCK`, `TIME_STOP`, `MANUAL`, `EVAL_START_FLATTEN`) block same-bar re-entry.
- `OPP_SIGNAL` is the only bar-close exception: same-bar reversal is allowed when `allow_flip=true` and `exit_on_opposite_signal=true`.

### Canonical Same-Bar Composite Chains

- `TP1 -> TP2`: allowed; `TP1` executes first, the remainder stays on the same lifecycle, then `TP2` may close the residual exposure.
- `TP1 -> SL/BE/TRAIL`: allowed; price-exit precedence is re-evaluated on the remainder before any discretionary close is considered.
- `TP1 -> OPP_SIGNAL`: allowed only as `partial + full close`; `allow_flip` is evaluated only if the remainder is fully closed by `OPP_SIGNAL`.
- `TP1 -> FILTER_BLOCK/TIME_STOP`: allowed as `partial + full close`; same-bar reopen remains blocked.
- `full price exit -> discretionary close`: not allowed as a second close mutation on the same lifecycle.

## Parity Artifact Minimums

Parity artifacts should carry the following fields whenever the source layer can emit them:

- `execution_profile_id`
- `lifecycle_id`
- `event_seq_in_bar`
- `exit_id`
- `working_exit_book_version`
- `effective_history_start`
- `warmup_bars`
- `warmup_seed_provenance`

These fields exist to reduce heuristic clustering in parity comparison. They do not replace normalized trade comparison; they narrow ambiguity.

## Warmup / History Contract

- Warmup is read-only seeding, not a skipped pipeline.
- `effective_history_start` and `warmup_bars` must be recorded with each parity run.
- `warmup_seed_provenance` should identify the active modules and effective warmup contributions used to seed the run.

## HTF Carry Regression Cases

Golden coverage for HTF alignment must include:

- weekend gap carry
- DST transition
- custom overnight session
- exchange half-day / holiday gap

### close_open_at_end Behavior

When `close_open_at_end=false` (default for parity): open positions at backtest end are **not** force-closed. TV reports these as signal="Open" with mark-to-market P&L. Python simply omits them from the trade list. Parity comparison uses `--clip-overlap` to exclude.

## Canonical Parity Case

```
configs/cases/full_jul2025_jan2026_parity.json
```

- **Data**: BTCUSDT.P 15m, Jun 30 2025 -- Feb 1 2026
- **TV timezone**: `Europe/London` (BST summer / GMT winter -- DST-aware)
- **TV reference CSV**: `debug/BTCUSDT/15m/MT_CORE2_BINANCE_BTCUSDT.P_2026-02-13_6e3fc.csv`
- **Preroll**: 365 days warmup-only

## Acceptance Criteria

| Metric | Threshold |
|--------|-----------|
| Closed trade count delta | **0** |
| Side + entry/exit time + reason mismatch | **0** |
| Absolute P&L delta | **<= 10 USDT** |

## How to Run

```bash
python scripts/parity_regression.py
```

Exit code 0 = PASS, non-zero = FAIL.
