# 18_GOLDEN_REPORT — Real QuantLens golden parity fixture

Date: 2026-07-13. Branch: `feature/quantlens-keltner-golden`.
Approval: Barış I4 (recorded in `16_GO_LIVE_PLAN.md`) — MCC-engine touch approved 2026-07-13.
Unblocks: `12_GOLDEN_REGEN_ATTEMPT.md` (T12 BLOCKED item). Provisional golden RETIRED.

## What was done

1. **QuantLens registration** (`MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py`):
   strategy id `keltner_trail_ema8` added to `GRIDS` with a single pinned combo mirroring
   `config/strategies/keltner_trail_ema8.yaml` verbatim (`kc_length 20, kc_mult 2.0,
   atr_length 20, trail_ema 8`), plus a `build_signals` branch implementing the bridge rules
   exactly: prior-window bands (current bar excluded; SMA of closes, arithmetic mean of TR;
   first TR = high−low), two-sided close-confirmed breakout, consecutive same-direction
   breakouts collapsed (the bridge's last-signal-direction state machine). The two-sided event
   stream is stamped on the dataframe (`kte8_event`) for the golden exporter; the engine sim
   itself takes the LONG leg (engine is single-direction per config) with the bridge's initial
   stop (lower band). **Purely additive**: the new id lives in `BRIDGE_PARITY_STRATEGIES` and is
   excluded from default full runs, so default job lists, trial counts, DSR pools and the BH-FDR
   family stay byte-identical. No existing strategy, grid, or engine behavior modified.

2. **Signal-equivalence check** (pre-run): bridge port vs registry branch on the synthetic
   fixture — identical signal lists (1/1), identical stop levels. EQUIVALENT.

3. **QuantLens run** (read-only data):

   ```powershell
   $env:MEGA_BUNDLE_MANIFEST = "<repo>\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
   $env:MEGA_OUTPUT_DIR     = "<repo>\IBKR_PAPER_BRIDGE\data\golden_quantlens_20260713"
   $env:MEGA_EXIT_MODES     = "trail_ema8"
   $env:PYTHONUTF8          = "1"
   python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --strategy keltner_trail_ema8 --symbol BTCUSD --tf 1h
   ```

   Result: 1 job, 3.7 s. Dataset BTCUSD 1h, **48,077 bars**, 2021-01-01 06:00 → 2026-06-28
   00:00 UTC, engine `faz3b-exit-mode-v1`, exit_mode `trail_ema8`.
   Classification **FAIL** (lockbox 96 trades, −22.09% net) — expected and irrelevant here: this
   is the plumbing test subject, not a promotion claim (long-leg sim only). Artifacts in
   `IBKR_PAPER_BRIDGE/data/golden_quantlens_20260713/` (git-ignored).

   Codex independently reran the same explicit strategy/symbol/timeframe command with
   `MEGA_OUTPUT_DIR=C:\tmp\codex_keltner_audit_20260713`: **1 job in 2.6 s**. The audit output
   remained outside the repository.

4. **Golden generation** (`tools/generate_golden.py`, rewritten): imports the registered
   QuantLens signal function read-only (the engine file is the single source of the signal
   math — no reimplementation), runs it on the same manifest dataset, applies the documented
   bridge execution transform (close-confirmed signal bar → MKT-next semantics, UTC 1h 24/7
   alignment, runtime `Z` timestamps), refuses to emit if registry grid ≠ bridge YAML params:

   ```
   python IBKR_PAPER_BRIDGE/tools/generate_golden.py --manifest <manifest>
   ```

   Emitted:
   - `tests/fixtures/BTC_1h_real.csv` — the exact 48,077 bars QuantLens processed (3.5 MB)
   - `tests/fixtures/golden_signals.json` — **858 signals**, `provisional: false`
   - `golden_run_id` = **`QL_MEGA_KELTNER_TRAIL_EMA8_BTCUSD_1h_2026-06-28_01a3f1255e29`**
     (sha256 over data range + signal list, first 12 hex) — written into
     `config/strategies/keltner_trail_ema8.yaml` (replaces
     `PROVISIONAL_SYNTHETIC_REFERENCE_2026-07-06`).

   First signal `2021-01-02T12:00:00Z LONG @30649.71`; last `2026-06-23T04:00:00Z SHORT
   @63544.5195`. Both directions present. The synthetic `BTC_1h.csv` stays untouched — it
   serves MockBroker fill mechanics only (audit Opus F-21 split honored).

## Parity result — bridge port vs QuantLens

`tests/test_strategy.py` replays the bridge port (`bridge/engine/strategies/keltner_trail_ema8.py`,
untouched) over all 48,077 real bars and requires signal-for-signal equality (ts, symbol,
direction, reason, ref_price) with the golden:

**858/858 signals identical. Zero divergence.** No assertion weakened; the test additionally
asserts `provisional: false` and non-empty signal count. `test_golden_generation.py` now pins
real-golden invariants (source, YAML run-id sync, exact bridge params, well-formed two-sided
Z-timestamp signals, fixture/golden window consistency).

## Divergences and honest caveats

- **Entry signals: none.** 858/858 exact.
- **Exit path not covered by the golden.** The golden is an ENTRY-signal fixture (that is what
  `test_strategy.py` asserts). Exits differ between the two engines by design and are NOT
  parity-claimed: the bridge trails with the arithmetic mean (SMA) of the last 8 closes
  (`trail_level`), while QuantLens `trail_ema8` exit mode uses a true EMA(8) (`ema_8` column)
  with next-open exit fills. The bridge's name `trail_ema8` is therefore a misnomer for its
  SMA-8 implementation — flagged per build-plan guardrail ("when ambiguous, write it into
  docs"); the bridge port remains the source of truth for live behavior and was not modified.
- **QuantLens sim = long leg only.** The engine simulates one direction per config; the golden's
  two-sided event stream comes from the same registered signal math, but walk-forward metrics
  (FAIL, −22.09% lockbox) describe the long leg with QuantLens exit semantics. Plumbing
  evidence only; never promotion evidence.

## Test output

```
IBKR_PAPER_BRIDGE>  python -m pytest tests -q          ->  114 passed, 1 warning in 10.48s
repo root>          python -m pytest IBKR_PAPER_BRIDGE/tests -q  ->  114 passed, 1 warning in 10.38s
```

Baseline was 113; +1 = new fixture/golden consistency test in `test_golden_generation.py`
(one provisional-era test replaced by two strictly stronger ones). `PYTHONUTF8=1` both runs.

Codex verification rerun:

```
IBKR_PAPER_BRIDGE>  python -m pytest tests -q                       ->  114 passed, 1 warning in 15.83s
repo root>          python -m pytest IBKR_PAPER_BRIDGE/tests -q     ->  114 passed, 1 warning in 15.85s
python -m py_compile <changed Python files>                         ->  PASS
```

Regenerating through `generate_real_golden` produced a signal list exactly equal to the saved
fixture (`True`): **858 signals** and the same run id,
`QL_MEGA_KELTNER_TRAIL_EMA8_BTCUSD_1h_2026-06-28_01a3f1255e29`.

## Files touched

| File | Change |
|---|---|
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py` | +grid, +signals branch, +BRIDGE_PARITY_STRATEGIES (additive) |
| `IBKR_PAPER_BRIDGE/tools/generate_golden.py` | real QuantLens golden path (legacy synthetic kept unwired) |
| `IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h_real.csv` | NEW — real 48,077-bar fixture |
| `IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json` | REAL golden, 858 signals, provisional: false |
| `IBKR_PAPER_BRIDGE/config/strategies/keltner_trail_ema8.yaml` | real golden_run_id |
| `IBKR_PAPER_BRIDGE/tests/test_strategy.py`, `tests/test_golden_generation.py` | real-golden parity + invariants |

Bridge runtime code (`bridge/`) untouched. `*.pine`, parity dirs, `MTC_V2`, `06_SCHEMAS`
untouched. No exchange orders, no LLM calls.
