# W249 Kernel Ordered Equity Report

**Measured summary: 17/17 MATCH, 0/17 MISMATCH; 0 KERNEL-SHORT, 0 GOLDEN-OVER, 0 DESIGN-GAP.**

The two W246 KERNEL-SHORT rows were reproduced before editing and both now match their sealed
goldens. Frozen legacy replay remained byte-exact for 17/17 scenarios and 34/34 surfaces. The
legacy Python tests measured 142 passed, the corrected-vNext contract self-tests measured 221
passed, and the built-in verifier returned 18/18 expected check dispositions. W246's immediately
preceding state was 15/17 MATCH with the two named one-step binary64 differences
(`W246_GATE_RERUN_REPORT.md:5-15,124-144`).

Finding count after implementation: **0 remaining gate mismatches and 0 legacy-surface
mismatches**. This is implementer QA evidence, not an independent acceptance verdict.

## Scope and authority

Gate-1 classification is **T0** because this protected kernel edit changes an economic result node.
The exact authorized worktree and branch are `C:\WP012BUILD` and
`feature/wp-p0-12-corrected-vnext-20260831`; the lane grants this worktree's only write lane and the
specific `mtc_v2/core/**` exception under standing P0-12 authorization
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W249_KERNEL_ORDERED_EQUITY.md:4-7`).

Allowed writes were limited to:

- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py`;
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py`;
- `W249_KERNEL_ORDERED_EQUITY_REPORT.md`.

Every other kernel path and every golden, catalog, manifest, seal, input, baseline, design, Pine,
adapter, schema, parity, broker, venue, host, credential, deployment, and network surface was
forbidden. The lane expressly forbids golden/baseline/design changes and canonical baseline
regeneration (`C:\tmp\LANE_PROMPTS_20260828\LANE_W249_KERNEL_ORDERED_EQUITY.md:52-57`). No live or
scheduled dependency was used. No backtest, optimization, server, launcher, artifact generator,
baseline regeneration, skip flag, push, pull request, merge, or live-trading action was performed.
Local package tests and verifiers are expressly allowed (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:33-36`).

Parity risk is bounded but not claimed away: ordered binary64 association intentionally changes
corrected 2.0.0 equity endpoint nodes when order matters. No Pine byte changed and no TradingView
export was executed; TradingView parity is **NOT VERIFIED / not comparable**. The stage requires
unchanged goldens and RED/GREEN evidence for regression closure
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/AGENTS.md:8-10,27-28`).

## Pre-edit reproduction

The lane required the real corrected executor followed immediately by the scoped expected-value
comparator before any edit (`C:\tmp\LANE_PROMPTS_20260828\LANE_W249_KERNEL_ORDERED_EQUITY.md:29-31`).
W246 identifies these same functions as the canonical row measurement seam
(`W246_GATE_RERUN_REPORT.md:106-112`).

From `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`, this exact in-memory command was run before the
test or kernel was edited:

```powershell
@'
from pathlib import Path

from mtc_v2.tests.corrected_vnext.verify_bceg import (
    compare_scoped_expected,
    execute_corrected_scenario,
    load_json_exact,
)

root = Path("mtc_v2").resolve()
scenario_ids = {"RULE2-06-RED", "RULE2-06-EQUAL-PRICE-RED"}
catalog = load_json_exact(root / "tests/corrected_vnext/contracts/scenario_catalog.json")
rows = [row for row in catalog if row["scenario_id"] in scenario_ids]
if len(rows) != 2:
    raise SystemExit(f"expected 2 rows, found {len(rows)}")
for row in rows:
    golden = load_json_exact(root / row["expected_artifacts"]["2.0.0"]["path"])
    observed = execute_corrected_scenario(root, row)
    difference = compare_scoped_expected(golden, observed)
    print(f"{row['scenario_id']}|{difference[0]}|{difference[1]}|{difference[2]}")
'@ | python -
```

Exit code **0**; exact output:

```text
RULE2-06-RED|/RESULT_SURFACE/equity_curve/last|F:0x1.fb68189374bc6p+9|F:0x1.fb68189374bc7p+9
RULE2-06-EQUAL-PRICE-RED|/RESULT_SURFACE/equity_curve/last|F:0x1.f8e8624dd2f1ap+9|F:0x1.f8e8624dd2f1bp+9
```

This exactly reproduces the lane's two required pre-edit values
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W249_KERNEL_ORDERED_EQUITY.md:14-17`).

## Kernel change

Design v1.10 defines `first` as initial realized equity after earlier cash events and `last` as
`first` plus each closed-window `signed_delta` in section-3/array order
(`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md:1070-1078`). The implementation now starts
from `state.initial_capital`, performs one addition per qualifying pre-window row, starts `last`
from `first`, and performs one addition per in-window row while preserving both existing predicates
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:790-809`).

Exact committed kernel diff:

```diff
@@ -795,19 +795,17 @@ def _realized_equity_window(
 ) -> tuple[float, float] | None:
     if observation_start is None:
         return None
-    first = state.initial_capital + sum(
-        float(row.signed_delta)
-        for row in state.cash_events
-        if row.event_timestamp < observation_start
-    )
-    last = first + sum(
-        float(row.signed_delta)
-        for row in _event_rows(
-            state.cash_events,
-            start=observation_start,
-            end=observation_end,
-        )
-    )
+    first = state.initial_capital
+    for row in state.cash_events:
+        if row.event_timestamp < observation_start:
+            first += float(row.signed_delta)
+    last = first
+    for row in _event_rows(
+        state.cash_events,
+        start=observation_start,
+        end=observation_end,
+    ):
+        last += float(row.signed_delta)
     return first, last
```

There is no `sum()`, `math.fsum`, reordering, or explicit rounding in the changed function. No
other kernel file is present in implementation commit `615438452c0958fb7123a441e0347e3eb9c2d9bb`.

## RED/GREEN regression evidence

The new self-test constructs the three ordered deltas `1e16`, `1.0`, and `-1e16`, proves that the
runtime's `sum()` result differs from explicit left-to-right addition, then asserts both endpoints
with `float.hex()` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py:153-186`).

Exact focused command from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py::test_realized_equity_window_adds_in_window_deltas_in_array_order -q
```

### RED against the pre-fix grouping

Exit code **1**. The exact failing assertion was:

```text
>       assert last.hex() == expected_last.hex()
E       AssertionError: assert '0x1.0000000000000p+1' == '0x0.0p+0'
E
E         - 0x0.0p+0
E         + 0x1.0000000000000p+1

mtc_v2\tests\corrected_vnext\contracts\selftests\test_results_corrected.py:186: AssertionError
=========================== short test summary info ===========================
FAILED mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py::test_realized_equity_window_adds_in_window_deltas_in_array_order
1 failed in 0.12s
```

### GREEN after ordered accumulation

Exit code **0**; exact output:

```text
.                                                                        [100%]
1 passed in 0.06s
```

This is the required D026 RED/GREEN form (`MTC_COMMAND_CENTER/01_MTC_PROJECT/TESTS.md:3-5`).

## Legacy verification

### Legacy Python self-tests

The first attempt from the nested `00_PYTHON` directory used:

```text
python -m pytest mtc_v2/tests --ignore=mtc_v2/tests/corrected_vnext -q
```

It exited **1 during collection** because `test_runner_metrics_api.py` imports the project-level
`tools.runner_metrics_adapter` package, which is not on `sys.path` from that directory:

```text
E   ModuleNotFoundError: No module named 'tools'
ERROR mtc_v2/tests/test_runner_metrics_api.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 1.34s
```

The corrected command was run from `MTC_COMMAND_CENTER/01_MTC_PROJECT`, keeping the project root as
the working directory and adding its Python package directory explicitly:

```powershell
$env:PYTHONPATH='00_PYTHON'; python -m pytest 00_PYTHON/mtc_v2/tests --ignore=00_PYTHON/mtc_v2/tests/corrected_vnext -q
```

Exit code **0**; exact summary:

```text
142 passed in 1.22s
```

### Frozen KERNEL_1 / LEGACY_P011_EXACT_V1 replay

W188 defines the available legacy check as loading the frozen driver's `prepare_scenario`,
`run_legacy`, and `canonical_bytes`, then comparing two in-memory surfaces per scenario directly
with `C:\tmp\P012_BASELINE_RUN\out` (`W188_KERNEL_RESUME_REPORT.md:131-142`). The frozen driver
imports the selected kernel's `config`, `runner`, and `types` modules and refuses an escaped import
(`C:\tmp\P012_BASELINE_RUN\run_baseline.py:554-570`).

This exact no-write replay was run from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```powershell
@'
import importlib.util
from pathlib import Path

path = Path(r"C:\tmp\P012_BASELINE_RUN\run_baseline.py")
spec = importlib.util.spec_from_file_location("p012_frozen_baseline_driver", path)
if spec is None or spec.loader is None:
    raise SystemExit("could not load frozen baseline driver")
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)

catalog_path = Path(r"C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json").resolve(strict=True)
baseline_out = Path(r"C:\tmp\P012_BASELINE_RUN\out").resolve(strict=True)
kernel_root = Path.cwd().resolve(strict=True)
rows = driver.validate_catalog(driver.load_json(catalog_path))
modules = driver.import_kernel(kernel_root)
matched_surfaces = 0
for row in rows:
    prepared = driver.prepare_scenario(row, catalog_path.parent, modules)
    event_surface, result_surface, _resolved_config = driver.run_legacy(
        modules["runner"].Runner,
        prepared["config"],
        prepared["bars"],
        prepared["htf_data"],
        prepared["gate_overrides"],
        prepared["profile_id"],
    )
    scenario_id = prepared["scenario_id"]
    for name, value in (("event_surface.json", event_surface), ("result_surface.json", result_surface)):
        expected = (baseline_out / scenario_id / name).read_bytes()
        observed = driver.canonical_bytes(value)
        if observed != expected:
            raise SystemExit(f"LEGACY MISMATCH {scenario_id}/{name}")
        matched_surfaces += 1
    print(f"LEGACY MATCH {scenario_id} 2/2")
print(f"LEGACY SUMMARY scenarios={len(rows)}/{len(rows)} surfaces={matched_surfaces}/{2 * len(rows)} exact")
'@ | python -
```

Exit code **0**. All 17 scenario lines reported `LEGACY MATCH ... 2/2`; exact final summary:

```text
LEGACY SUMMARY scenarios=17/17 surfaces=34/34 exact
```

Therefore no KERNEL_1 / `LEGACY_P011_EXACT_V1` surface changed at any serialized node in the
available frozen replay.

## Seventeen-row direct measurement

The all-row measurement used the same real executor/comparator seam as W246
(`W246_GATE_RERUN_REPORT.md:106-122`). It ran in memory and wrote no observed artifact.

Exact command from `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```powershell
@'
from pathlib import Path

from mtc_v2.tests.corrected_vnext.verify_bceg import (
    compare_scoped_expected,
    execute_corrected_scenario,
    load_json_exact,
)

root = Path("mtc_v2").resolve()
catalog = load_json_exact(root / "tests/corrected_vnext/contracts/scenario_catalog.json")
rows = [row for row in catalog if row["role"] in {"RED", "GREEN"}]
match_count = 0
for row in rows:
    golden = load_json_exact(root / row["expected_artifacts"]["2.0.0"]["path"])
    observed = execute_corrected_scenario(root, row)
    difference = compare_scoped_expected(golden, observed)
    if difference is None:
        match_count += 1
        print(f"| {row['scenario_id']} | MATCH | - | - | - | MATCH |")
    else:
        print(
            f"| {row['scenario_id']} | MISMATCH | `{difference[0]}` | "
            f"`{difference[1]}` | `{difference[2]}` | NOT CLASSIFIED |"
        )
print(f"SUMMARY|{match_count}/{len(rows)} MATCH|{len(rows) - match_count}/{len(rows)} MISMATCH")
'@ | python -
```

Exit code **0**. Measured table:

| Scenario | Result | First differing pointer | Observed | Golden | Classification |
|---|---|---|---|---|---|
| RULE2-01-RED | MATCH | - | - | - | MATCH |
| RULE2-01-GREEN | MATCH | - | - | - | MATCH |
| RULE2-02-RED | MATCH | - | - | - | MATCH |
| RULE2-02-GREEN | MATCH | - | - | - | MATCH |
| RULE2-03-RED | MATCH | - | - | - | MATCH |
| RULE2-03-GREEN | MATCH | - | - | - | MATCH |
| RULE2-04-RED | MATCH | - | - | - | MATCH |
| RULE2-04-GREEN | MATCH | - | - | - | MATCH |
| RULE2-05-RED | MATCH | - | - | - | MATCH |
| RULE2-05-GREEN | MATCH | - | - | - | MATCH |
| RULE2-06-RED | MATCH | - | - | - | MATCH |
| RULE2-06-EQUAL-PRICE-RED | MATCH | - | - | - | MATCH |
| RULE2-06-GREEN | MATCH | - | - | - | MATCH |
| RULE2-07-RED | MATCH | - | - | - | MATCH |
| RULE2-07-GREEN | MATCH | - | - | - | MATCH |
| RULE2-08-RED | MATCH | - | - | - | MATCH |
| RULE2-08-GREEN | MATCH | - | - | - | MATCH |

Measured summary: **17/17 MATCH, 0/17 MISMATCH; 0 KERNEL-SHORT, 0 GOLDEN-OVER, 0 DESIGN-GAP.**

The lane calls 17/17 a prediction rather than a target and requires the measured table
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W249_KERNEL_ORDERED_EQUITY.md:46-48`); this run measured the
prediction exactly.

## Contract self-tests

Both commands ran after the kernel change from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

| Command | Exit | Measured result |
|---|---:|---|
| `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` | 0 | **221 passed** in 0.69 s |
| `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode selftest` | 0 | **18 checks:** 3 `PASS`, 14 `DETECTED`, 1 `DETECTED:/a/1` |

The built-in selftest is explicitly non-accepting and constructs the receipt at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1377-1429`.

## Git and guard evidence

The implementation was committed from the authorized branch after exact-path staging,
`git diff --cached --name-only`, `git diff --cached --check`, and the repository guard. The guard
reported `RESULT: PASS`, the branch merge-base one commit behind local `origin/master` (within its
30-commit limit), exactly two staged files, no protected-path match, no risky untracked file, and
`PINE_ALERT_GUARD PASS`. The guard's required invocation is documented at
`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md:47-50`.

Implementation commit:

```text
615438452c0958fb7123a441e0347e3eb9c2d9bb fix(mtc-v2): preserve ordered equity accumulation
```

Parent/base commit:

```text
4fe52abb042a9c517c692903887bf3acd960a424
```

The implementation commit contains exactly the kernel file and its one contract self-test. The
second commit contains only this report. Neither commit was pushed, as prohibited by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W249_KERNEL_ORDERED_EQUITY.md:49-50`).

Final guard-format handoff:

```text
branch:            feature/wp-p0-12-corrected-vnext-20260831
files changed:     mtc_v2/core/results.py; selftests/test_results_corrected.py; W249_KERNEL_ORDERED_EQUITY_REPORT.md
checks run:        focused RED/GREEN; 17-row executor/comparator; 142 legacy tests; 34-surface frozen legacy replay; 221 contract tests; 18-check verifier selftest; git diff --check; repo_guard.ps1
guard:             PASS
commit:            615438452c0958fb7123a441e0347e3eb9c2d9bb plus this report's containing commit
pushed:            no
remaining dirty:   none expected after report commit; verified after commit in chat close
next action:       independent Lead acceptance; no merge or push is authorized by this lane
```

## Discrepancies

1. **The local runbook does not publish a legacy pytest command.** The lane requires legacy
   self-tests but supplies no command (`C:\tmp\LANE_PROMPTS_20260828\LANE_W249_KERNEL_ORDERED_EQUITY.md:43-45`),
   while the current runbook publishes parity commands rather than a legacy pytest invocation
   (`MTC_COMMAND_CENTER/01_MTC_PROJECT/03_DOCS/RUNBOOK.md:19-35,41-79`). The naive nested-directory
   command therefore failed to import the project-level `tools` package. The corrected explicit
   `PYTHONPATH` command and its 142-pass result are reported above; the frozen legacy replay provides
   the separate KERNEL_1 / `LEGACY_P011_EXACT_V1` byte-exact check.
2. **A Git commit cannot embed its own SHA without changing that SHA.** The lane asks the committed
   report to contain commit hashes (`C:\tmp\LANE_PROMPTS_20260828\LANE_W249_KERNEL_ORDERED_EQUITY.md:61-64`).
   This report therefore records the full implementation and base hashes and identifies the report
   commit as its containing commit. Its exact measured SHA is necessarily reported after commit in
   the under-10-line chat close rather than inserted into its own bytes.

No discrepancy was found between the design, sealed goldens, and post-fix 17-row measurement.
