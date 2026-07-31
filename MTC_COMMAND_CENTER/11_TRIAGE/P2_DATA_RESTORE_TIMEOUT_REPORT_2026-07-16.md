# P2 Data-Restore Timeout Build Report — 2026-07-16

## Outcome

**BUILD + TESTS PASS; DEPLOYMENT LOCKED FOR FABLE AUDIT.** Approved commit `79976577`
raises the BridgeEngine/configured post-reconnect fresh-data deadline from 60 seconds to
300 seconds. `IBKR_PAPER_BRIDGE/bridge/engine/bars.py` is unchanged. No broker, testnet,
paper, backtest, optimization, download, server, deploy, restart, DISARM, or ARM action ran.

Branch/worktree: `feature/ibkr-bridge-final` in `C:\BTL2`.

## Exact implementation

- `IBKR_PAPER_BRIDGE/config/bridge.yaml:10` adds broker `data_restore_timeout_s: 300`.
- `IBKR_PAPER_BRIDGE/bridge/app.py:118` reads the broker value with a `300.0` fallback.
- `IBKR_PAPER_BRIDGE/bridge/engine/engine.py:47` defines
  `bar_data_restore_timeout_s: float = 300.0`.
- `IBKR_PAPER_BRIDGE/bridge/engine/engine.py:62` clamps the value to at least 30 seconds.
- `IBKR_PAPER_BRIDGE/bridge/engine/engine.py:94` passes the value into `BarFeed`.
- `IBKR_PAPER_BRIDGE/bridge/engine/bars.py` has no diff.

The implementation commit contains only these five paths:

```text
IBKR_PAPER_BRIDGE/bridge/app.py
IBKR_PAPER_BRIDGE/bridge/engine/engine.py
IBKR_PAPER_BRIDGE/config/bridge.yaml
IBKR_PAPER_BRIDGE/tests/test_bars.py
IBKR_PAPER_BRIDGE/tests/test_task11_polish.py
```

No notification, reconcile, strategy, Pine, parity, schema, or protected-scope logic changed.

## Test-first failure proof

Baseline before the edit, from both supported working directories:

```text
C:\BTL2> python -m pytest IBKR_PAPER_BRIDGE/tests -q
130 passed, 1 warning in 20.06s

C:\BTL2\IBKR_PAPER_BRIDGE> python -m pytest tests -q
130 passed, 1 warning in 17.56s
```

The final retained focused tests were run against exact pre-fix production files from
`8721bce0`, then the committed implementation was restored in the same command. Result:

```text
..F                                                                      [100%]
FAILED ...test_dry_run_app_snapshot_has_bars_and_trade_data
  AttributeError: 'BridgeEngine' object has no attribute 'bar_data_restore_timeout_s'
1 failed, 2 passed, 1 warning in 0.56s
```

This is the required pre-fix failure proof for the new default/config wiring. The two direct
`BarFeed` behavior tests explicitly supply 300 or legacy 60 because the approved scope requires
`bars.py` to remain unchanged; those behavior tests therefore pass on both code versions.

## Post-fix focused proofs

With `PYTHONUTF8=1`:

```text
python -m pytest \
  IBKR_PAPER_BRIDGE/tests/test_bars.py::test_reconnect_late_fresh_bar_respects_restore_timeout \
  IBKR_PAPER_BRIDGE/tests/test_bars.py::test_reconnect_default_restore_timeout_disarms_after_300_seconds \
  IBKR_PAPER_BRIDGE/tests/test_task11_polish.py::test_dry_run_app_snapshot_has_bars_and_trade_data -q

3 passed, 1 warning in 0.81s
```

The focused coverage proves:

1. A 300-second configured window does not stale/disarm at 239 seconds and accepts a first
   fresh bar at 240 seconds with `DATA_RESTORED`.
2. An explicit legacy 60-second window emits exact
   `DATA_STALE / reconnect_no_fresh_data` and disarms at the same late point.
3. With 300 seconds configured and no fresh data, 301 seconds emits the exact stale reason
   and disarms exactly once.
4. The YAML value reaches both `BridgeEngine` and its created `BarFeed` instance.

`BarFeed` keeps its low-level 60-second constructor default because the approved scope froze
`bars.py`; the application/engine default is the new 300-second policy and is passed explicitly.

## Full-suite evidence

Both required suites ran concurrently after the fix, with `PYTHONUTF8=1`:

```text
C:\BTL2> python -m pytest IBKR_PAPER_BRIDGE/tests -q
132 passed, 1 warning in 21.43s

C:\BTL2\IBKR_PAPER_BRIDGE> python -m pytest tests -q
132 passed, 1 warning in 21.47s
```

The sole warning in each run is the existing FastAPI/Starlette `httpx` deprecation warning.

## Safety and isolation evidence

- Staged implementation diff 64+-hex scan: `0` matches.
- `HL_API_WALLET_KEY` was never printed or read.
- Final read-only runtime identity check: `C:\P2RT` is clean and detached at `1465f8f0`.
- No write, checkout, test, process, API, deploy, restart, or ARM action occurred in `C:\P2RT`.
- ClinePass failed to establish a session; the guarded `_deepseek_driver` fallback hit its
  iteration limit after misresolving the worktree. Both checkouts were inspected immediately;
  neither fallback changed a file. Codex then made and independently audited the narrow edits.

## Stop gate

STOP. Fable must audit commit `79976577` against real code, independently rerun both suites,
and independently reproduce the pre-fix failure. Deployment remains prohibited until Fable
records PASS. Any later deploy must follow the existing one-window testnet runbook, including
fresh-bar verification and exactly one authorized ARM.
