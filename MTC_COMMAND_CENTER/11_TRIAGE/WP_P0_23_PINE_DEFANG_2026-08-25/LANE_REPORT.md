# WP-P0-23 Pine de-fang — Lane AC implementer report

**Date:** 2026-08-25
**Role:** Codex implementer, Gates 3–4 only
**Audit tier:** T0 — protected Pine / live order-path removal
**Branch:** feature/wp-p0-23-pine-defang-20260825
**Base:** ef380d1cc8f224bde302e087f038919f29a14204
**Final implementation commit SHA:** f25152abe4747c888734fcfed988cdad1af3a944
**Acceptance status:** NOT SELF-ACCEPTED. TradingView-dependent checks remain unverified and Gate 5 belongs to the Claude lead.

## 1. Authority, boundaries, and exact scope

The lane brief records Barış's exact G2 authorization dated 2026-08-25 against
PINE_DEFANG_T0_AUTHORIZATION_PACKAGE.md sections 2–9. I implemented the eleven authorized
table rows as seven unique implementation files:

1. MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine
2. MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py
3. MTC_COMMAND_CENTER/01_MTC_PROJECT/tools/optimization_parameter_mapper.py
4. MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py
5. MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
6. MTC_COMMAND_CENTER/tools/repo_guard.ps1
7. .github/workflows/pine-defang-guard.yml

This report is the additional path explicitly required by the lane brief. No Bridge, parity,
kernel, deployment, host, credential, broker, exchange, TradingView state, tag, or master
branch was touched.

SESSION_LOCK.md says an unlisted workstream normally adds a row before writing. The exact lane
contract simultaneously says no file outside its named package may change. The isolated prepared
worktree was clean and no conflicting owner was recorded; I did not add an unauthorized
SESSION_LOCK.md row. Gate 7 memory write-back remains Lead-owned after acceptance.

The design package's earlier “no push” boundary is superseded only for this feature branch by
the later lane brief's explicit “Push the branch” instruction. This does not widen deployment,
publication, host, venue, credential, testnet, live, or merge authority.

## 2. Freeze tag and protected before-state proof

First repository action, rerun cleanly for this report:

~~~
git ls-remote --tags origin "legacy/pine-controller/*"
3075bd66547f5ade903a570cb54a49e3ef197328  refs/tags/legacy/pine-controller/2026-08-25
77a10e6573d93f8aaf777010ea507bbec0a7668b  refs/tags/legacy/pine-controller/2026-08-25^{}

git rev-parse "legacy/pine-controller/2026-08-25^{}"
77a10e6573d93f8aaf777010ea507bbec0a7668b

git show "legacy/pine-controller/2026-08-25:MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine" | rg -c -F "alert("
2
EXIT_CODE=0
~~~

Protected blobs before editing:

~~~
tag pine blob:
96cb361eafc04cd7e57fe2e138696c2ffd4f46e1
HEAD pine blob:
96cb361eafc04cd7e57fe2e138696c2ffd4f46e1
tag config blob:
e472d0ac3e6df99c17e90195b620feae12acfd1f
HEAD config blob:
e472d0ac3e6df99c17e90195b620feae12acfd1f
tag-to-HEAD protected diff rc=0
~~~

The original contained 13 Pine wt_ declarations and 13 Python wt_ defaults. The clean,
fixed-SHA freeze proof above supersedes an initial PowerShell helper run that proved the same
tag and alert count but emitted filename-decoding errors while searching the tag tree.

## 3. Anchors actually used

These are pre-edit line numbers from candidate parent ef380d1c:

| Authorized anchor | Actual pre-edit line(s) used | Drift |
|---|---:|---|
| Insert after //@version=6 | line 1; comment inserted at new line 2 | none |
| strategy(...) declaration | line 7 before insertion; identical content at line 8 after insertion | content unchanged |
| 13 wt_ Pine inputs | 176–188 | none |
| Dispatch opening divider | 2007 | none |
| SECTION 9 - WUNDERTRADING ALERT DISPATCH (L25) heading | 2008 | heading was +1 if the printed range start was read as the heading |
| Complete dispatch deletion | original 2007–2028 inclusive | exact; original separator line 2029 retained |
| Python defaults heading + 13 defaults | 225–238 | none |
| Python validation heading/block | 568–584 | none; original separator line 585 retained |
| integrations_disabled dictionary | 48–57 | none |
| stale mapper note | 87 | none |
| validate_config(merged) insertion seam | line 55; assertion inserted immediately before it | none |
| repo_guard unpushed check | line 157; scanner inserted before it | none |

Line-for-line transformation checks:

~~~
PINE_EXACT_AUTHORIZED_TRANSFORM=True before_lines=2079 after_lines=2045 expected_lines=2045
STRATEGY_DECLARATION_BYTE_EXACT=True count_before=1 count_after=1
CONFIG_EXACT_AUTHORIZED_TRANSFORM=True before_lines=698 after_lines=667 expected_lines=667

git diff --numstat -- <config> <pine>
0  31  MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py
1  35  MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine
~~~

The Pine proof constructs the expected source from the freeze-identical parent by inserting
only the required header, removing original lines 176–188, and removing original lines
2007–2028. It compares every resulting line in order with the candidate.

## 4. D026 — empty-allowlist scanner

### 4.1 RED against exact pre-fix behavior

The new scanner was run before the Pine deletion:

~~~
COMMAND: python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
PINE_ALERT_GUARD VIOLATION path=MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine matches=2
PINE_ALERT_GUARD BLOCK files=21 matches=2 allowlist=0
EXIT_CODE=1
~~~

### 4.2 GREEN after the repair plus independent rg

~~~
COMMAND: python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0
EXIT_CODE=0

COMMAND: $hits = @(rg -l -F --glob '*.pine' 'alert(' .)
RG_EXIT_CODE=1
RG_HIT_COUNT=0
PINE_FILE_COUNT=21
~~~

rg exit 1 is its documented no-match result. The independent check treated only rc outside
0/1 as inability to evaluate.

### 4.3 RED against an arbitrary tree path

Exact mutation: create
MTC_COMMAND_CENTER/tools/WP P0 23 D026 Probe.pine with:

~~~
//@version=6
alert("D026 arbitrary-tree probe")
~~~

The path is outside 01_PINE and contains spaces.

~~~
COMMAND: python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
PINE_ALERT_GUARD VIOLATION path=MTC_COMMAND_CENTER/tools/WP P0 23 D026 Probe.pine matches=1
PINE_ALERT_GUARD BLOCK files=22 matches=1 allowlist=0
EXIT_CODE=1
~~~

After deleting the probe through apply_patch:

~~~
COMMAND: git status --short
 M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py
 M MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine
 M MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py
 M MTC_COMMAND_CENTER/01_MTC_PROJECT/tools/optimization_parameter_mapper.py
 M MTC_COMMAND_CENTER/tools/repo_guard.ps1
?? .github/
?? MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
PROBE_STATUS_RESIDUE_COUNT=0
COMMAND: python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0
EXIT_CODE=0
~~~

### 4.4 Additional fail-closed scanner arms

An alert-free temporary .pine file was held open with FileShare.None. The scanner named the
unevaluated path, returned 2, and did not print PASS:

~~~
COMMAND: python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py (probe held with FileShare.None)
PINE_ALERT_GUARD UNEVALUATED path=MTC_COMMAND_CENTER/tools/WP P0 23 Read Failure Probe.pine detail=[Errno 13] Permission denied: 'C:\WPP023_20260825\MTC_COMMAND_CENTER\tools\WP P0 23 Read Failure Probe.pine'
PINE_ALERT_GUARD BLOCK files=22 matches=0 allowlist=0 errors=1
EXIT_CODE=2
~~~

The probe was removed and READ_PROBE_STATUS_RESIDUE_COUNT=0.

Git-root resolution was falsified by invoking the absolute Python executable with PATH containing
no Git:

~~~
COMMAND: C:\Python314\python.exe MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py (PATH contains no git)
PINE_ALERT_GUARD BLOCK reason=git_root_unavailable detail=[WinError 2] Sistem belirtilen dosyayı bulamıyor
EXIT_CODE=2
~~~

The scanner also passed from MTC_COMMAND_CENTER/01_MTC_PROJECT, proving that it resolves the
repository rather than assuming the caller's current directory:

~~~
COMMAND: python ..\tools\check_no_pine_alerts.py
PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0
SCANNER_EXIT_CODE=0
~~~

The immutable allowlist is declared as frozenset() and every terminal line above reports
allowlist=0.

## 5. repo_guard fail-closed carrier proof

### 5.1 Scanner returns nonzero

This ran while the arbitrary-tree probe existed:

~~~
COMMAND: powershell -NoProfile -ExecutionPolicy Bypass -File MTC_COMMAND_CENTER/tools/repo_guard.ps1
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    feature/wp-p0-23-pine-defang-20260825
[freshness] local origin/master tip ef380d1cc8f224bde302e087f038919f29a14204 age=0 day(s) (commit timestamp; no fetch attempted)
[freshness] branch merge-base ef380d1cc8f224bde302e087f038919f29a14204 is 0 commit(s) behind local origin/master (limit 30)
[dirty]     8 entr(y/ies):
             M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py
             M MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine
             M MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py
             M MTC_COMMAND_CENTER/01_MTC_PROJECT/tools/optimization_parameter_mapper.py
             M MTC_COMMAND_CENTER/tools/repo_guard.ps1
            ?? .github/
            ?? "MTC_COMMAND_CENTER/tools/WP P0 23 D026 Probe.pine"
            ?? MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
[staged]    none
[protected] none
[untracked] no risky files
[pine-alert] PINE_ALERT_GUARD VIOLATION path=MTC_COMMAND_CENTER/tools/WP P0 23 D026 Probe.pine matches=1
[pine-alert] PINE_ALERT_GUARD BLOCK files=22 matches=1 allowlist=0
[unpushed]  no upstream set

WARN: no upstream tracking branch
BLOCK: Pine alert invariant scanner returned nonzero (rc=1)
RESULT: BLOCKED
REPO_GUARD_EXIT_CODE=1
~~~

### 5.2 Scanner cannot execute

Exact falsification: define a child-PowerShell function named python that throws
“D026 forced scanner command unavailable,” then invoke repo_guard.ps1.

~~~
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    feature/wp-p0-23-pine-defang-20260825
[freshness] local origin/master tip ef380d1cc8f224bde302e087f038919f29a14204 age=0 day(s) (commit timestamp; no fetch attempted)
[freshness] branch merge-base ef380d1cc8f224bde302e087f038919f29a14204 is 0 commit(s) behind local origin/master (limit 30)
[dirty]     7 entr(y/ies):
             M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py
             M MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine
             M MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py
             M MTC_COMMAND_CENTER/01_MTC_PROJECT/tools/optimization_parameter_mapper.py
             M MTC_COMMAND_CENTER/tools/repo_guard.ps1
            ?? .github/
            ?? MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
[staged]    none
[protected] none
[untracked] no risky files
[pine-alert] scanner could not execute: D026 forced scanner command unavailable
[unpushed]  no upstream set

WARN: no upstream tracking branch
BLOCK: Pine alert invariant scanner could not execute
RESULT: BLOCKED
REPO_GUARD_EXIT_CODE=1
~~~

## 6. wt_ 13-to-13 removal and config validation

All thirteen mappings are absent in both active sources:

| # | Pine input | Python default | Result |
|---:|---|---|---|
| 1 | wt_enter_long_code | wt_enter_long_code | removed / removed |
| 2 | wt_exit_long_code | wt_exit_long_code | removed / removed |
| 3 | wt_enter_short_code | wt_enter_short_code | removed / removed |
| 4 | wt_exit_short_code | wt_exit_short_code | removed / removed |
| 5 | wt_exit_all_code | wt_exit_all_code | removed / removed |
| 6 | wt_order_type | wt_order_type | removed / removed; validator removed |
| 7 | wt_amount_type | wt_amount_type | removed / removed; validator removed |
| 8 | wt_amount | wt_amount | removed / removed; validator removed |
| 9 | wt_leverage | wt_leverage | removed / removed; validator removed |
| 10 | wt_use_tp | wt_use_tp | removed / removed; validator removed |
| 11 | wt_use_sl | wt_use_sl | removed / removed; validator removed |
| 12 | wt_reduce_only | wt_reduce_only | removed / removed; validator removed |
| 13 | wt_place_cond_orders | wt_place_cond_orders | removed / removed; validator removed |

Live-source and repo-wide non-document producer sweeps:

~~~
rg -n '\bwt_[a-z0-9_]+' MTC_V2.pine config.py optimization_parameter_mapper.py
LIVE_SOURCE_WT_SWEEP_RC=1 HIT_COUNT=0

rg -n '\bwt_[a-z0-9_]+' . --glob '!*.md' --glob '!*.txt' --glob '!*.csv' --glob '!*.log' --glob '!*.html' --glob '!*.json'
NON_DOCUMENT_WT_SWEEP_RC=1 HIT_COUNT=0
~~~

The compatibility flag emits no keys and ordinary config validation succeeds:

~~~
INTEGRATIONS_DISABLED_OVERRIDES={}
DEFAULT_WT_KEY_COUNT=0
CONFIG_VALIDATION PASS
EXIT_CODE=0
~~~

### 6.1 D026 for the new wt_-absence assertion

Equivalent deliberate mutation:

~~~
"integrations_disabled": {"wt_enter_long_code": ""},
~~~

The exact new test then failed at the new assertion:

~~~
COMMAND: python -m pytest MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py::test_tp_mode_none_null_is_numeric_before_runner_validation
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\WPP023_20260825
plugins: anyio-4.12.1, cov-7.0.0
collected 1 item

MTC_COMMAND_CENTER\01_MTC_PROJECT\tests\test_optimizer_post_run_patches.py F [100%]

================================== FAILURES ===================================
_________ test_tp_mode_none_null_is_numeric_before_runner_validation __________

>       assert not any(key.startswith("wt_") for key in overrides)
E       assert not True
E        +  where True = any(<generator object test_tp_mode_none_null_is_numeric_before_runner_validation.<locals>.<genexpr> at 0x0000000006030040>)

MTC_COMMAND_CENTER\01_MTC_PROJECT\tests\test_optimizer_post_run_patches.py:55: AssertionError
=========================== short test summary info ===========================
FAILED MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py::test_tp_mode_none_null_is_numeric_before_runner_validation
============================== 1 failed in 0.35s ==============================
EXIT_CODE=1
~~~

After restoring the exact empty dictionary:

~~~
COMMAND: python -m pytest MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\WPP023_20260825
plugins: anyio-4.12.1, cov-7.0.0
collected 2 items

MTC_COMMAND_CENTER\01_MTC_PROJECT\tests\test_optimizer_post_run_patches.py . [ 50%]
.                                                                        [100%]

============================== 2 passed in 0.12s ==============================
EXIT_CODE=0
~~~

Full affected project test directory from its module root:

~~~
COMMAND: python -m pytest tests
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\WPP023_20260825\MTC_COMMAND_CENTER\01_MTC_PROJECT
plugins: anyio-4.12.1, cov-7.0.0
collected 7 items

tests\test_optimizer_dataset_usage.py .....                              [ 71%]
tests\test_optimizer_post_run_patches.py ..                              [100%]

============================== 7 passed in 0.23s ==============================
FIXED_SHA_TEST_EXIT_CODE=0
~~~

A broader run first invoked from the repository root collected the two post-run tests but
could not import tools for test_optimizer_dataset_usage.py. That was an invocation-root error
(ModuleNotFoundError: No module named 'tools'); the exact corrected module-root command and
complete GREEN output are above. A supplemental direct config probe likewise first omitted
00_PYTHON from sys.path, then passed with that canonical module path added. Neither failure
occurred in the required target test command.

## 7. tw_ exclusion

The candidate preserves all seven declarations and every line containing a tw_ declaration,
required-key check, validator, or consumer in config.py:

~~~
TW_LINES_BYTE_EXACT=True before_lines=24 after_lines=24
TW_DECLARATION_COUNT=7
~~~

The comparison used candidate-parent content versus candidate content with line numbers
excluded, so shifts caused by the authorized wt_ deletions cannot create a false mismatch.
No tw_ line appears in the candidate diff.

## 8. CI and Python static checks

The workflow was parsed using PyYAML BaseLoader and checked structurally:

~~~
WORKFLOW_CONTRACT PASS {"actions": ["actions/checkout@v4", "actions/setup-python@v5"], "permissions": {"contents": "read"}, "python-version": "3.11", "run-commands": ["python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py"], "timeout-minutes": "5", "triggers": ["pull_request", "push"]}
EXIT_CODE=0
~~~

There is one run command and it invokes the same scanner as repo_guard.ps1. There is no path
filter, secret, deployment step, or second scanner implementation.

~~~
python -m py_compile MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py MTC_COMMAND_CENTER/01_MTC_PROJECT/tools/optimization_parameter_mapper.py MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py
PY_COMPILE_EXIT_CODE=0

git diff --check
EXIT_CODE=0
~~~

No repo-root Ruff configuration or installed Ruff module was found. No Python lint verdict is
claimed beyond compilation, executed scanner behavior, and pytest.

## 9. Fixed render dataset identity and render-identity criteria

Read-only fixed dataset proof:

~~~
git ls-files --stage -- "MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv"
100644 fc5bf84369bc163a3d51bef0993bcfb9a64a2fa7 0  MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv

git hash-object -- <dataset>
fc5bf84369bc163a3d51bef0993bcfb9a64a2fa7

Get-FileHash -Algorithm SHA256
0e6c540065690ba1ce00f4d03ad65881569d974d50e02bdd305f1048604d9a99

physical_lines=24525 data_rows=24524
first=1685314800,28079.4,28252.8,28042.3,28055.7
last=1773597600,71787.9,71856.0,71275.0,71346.8
~~~

Source identities:

- freeze Pine blob: 96cb361eafc04cd7e57fe2e138696c2ffd4f46e1
- candidate Pine blob: 0075483d58a2a82cb1ec63b86392cfcf4318fc47
- candidate config blob: 0738f2ff2c44a83e896209b83063c9a0c0f2b6ec
- exact static Pine transform: TRUE
- strategy(...) declaration content: byte-identical
- calculation/order-simulation/plot/table/label/render lines outside the authorized deletions:
  line-for-line identical by the constructed expected-source comparison

Criterion-by-criterion:

1. **Both versions compile and load the fixed interval:** UNVERIFIED. This lane did not open
   TradingView or touch TradingView state. No Pine v6 compiler is available locally.
2. **Exported chart timestamps and every emitted series are byte-equivalent:** UNVERIFIED.
   Dataset identity is proven, but no before/after TradingView exports were produced.
3. **Strategy Tester order/trade count and every order field are identical:** UNVERIFIED.
   Static strategy/order-simulation source identity is proven; runtime Strategy Tester output is not.
4. **Before/after screenshots are identical:** UNVERIFIED. No chart or screenshot was opened.
5. **Machine-readable comparison has zero differing cells/series:** UNVERIFIED because the
   required TradingView exports do not exist in this lane.
6. **No 13 WunderTrading inputs and no alert() call:** source-level VERIFIED. The active Pine has
   no wt_ identifier and the repository scanner/independent rg are GREEN. The UI absence itself
   was not visually verified.

No visual, compile, export, or simulated-order identity claim is made.

## 10. Rollback rehearsal

The first attempt used the normal user TEMP path and Git checkout stopped at 41% with
“Filename too long” before any restore command ran. The exact path did not exist afterward
and had no worktree registration. The successful rehearsal used short validated path
C:\tmp\R23_6b07fdb0.

Initial state and restore:

~~~
HEAD is now at f25152ab feat(mtc): de-fang Pine controller

git rev-parse "refs/tags/legacy/pine-controller/2026-08-25^{commit}"
77a10e6573d93f8aaf777010ea507bbec0a7668b

git status --short
<empty>

git restore --source=legacy/pine-controller/2026-08-25 --worktree -- <pine> <config>

git diff -- <pine> <config>
~~~

The complete diff was the exact inverse of the candidate's two protected-file transform:
it re-added the 13 Python defaults, complete validation block, 13 Pine inputs, and complete
dispatch block, and removed only the visualization header. The exact diff is reproducible
from f25152ab with the command above; its observed hunk headers were:

~~~
config.py: @@ -222,6 +222,20 @@
config.py: @@ -551,6 +565,23 @@
MTC_V2.pine: @@ -1,5 +1,4 @@
MTC_V2.pine: @@ -174,6 +173,19 @@
MTC_V2.pine: @@ -1992,6 +2004,28 @@
~~~

Restored identity and expected RED:

~~~
git hash-object <pine>
96cb361eafc04cd7e57fe2e138696c2ffd4f46e1

git hash-object <config>
e472d0ac3e6df99c17e90195b620feae12acfd1f

rg -n -F --glob '*.pine' 'alert(' .
.\MTC_COMMAND_CENTER\01_MTC_PROJECT\01_PINE\MTC_V2.pine:2020:            alert('{"code":"' + l25_entry_code + '","order_type":"' + wt_order_type + '","amount":' + str.tostring(wt_amount) + ',"amount_type":"' + wt_amount_type + '","leverage":' + str.tostring(wt_leverage) + ',"reduce_only":' + (wt_reduce_only ? "true" : "false") + l25_tp_str + l25_sl_str + l25_cond_str + '}', alert.freq_once_per_bar_close)
.\MTC_COMMAND_CENTER\01_MTC_PROJECT\01_PINE\MTC_V2.pine:2028:            alert('{"code":"' + l25_exit_code + '","reduce_only":true}', alert.freq_once_per_bar_close)
RG_EXIT_CODE=0 HIT_LINE_COUNT=2

python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
PINE_ALERT_GUARD VIOLATION path=MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine matches=2
PINE_ALERT_GUARD BLOCK files=21 matches=2 allowlist=0
RESTORED_GUARD_EXIT_CODE=1

git status --short
 M MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py
 M MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine
~~~

Return to candidate:

~~~
git restore --source=f25152abe4747c888734fcfed988cdad1af3a944 --worktree -- <pine> <config>
CANDIDATE_PINE_BLOB=0075483d58a2a82cb1ec63b86392cfcf4318fc47
CANDIDATE_CONFIG_BLOB=0738f2ff2c44a83e896209b83063c9a0c0f2b6ec
PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0
CANDIDATE_GUARD_EXIT_CODE=0
DISPOSABLE_STATUS_COUNT=0
DISPOSABLE_WORKTREE_REMOVED=C:\tmp\R23_6b07fdb0
~~~

No tag was created, moved, retagged, or deleted.

## 11. Candidate commit and exact files

~~~
commit f25152abe4747c888734fcfed988cdad1af3a944

    feat(mtc): de-fang Pine controller

    Owner G2 authorization: WP-P0-23, 2026-08-25.

    Rollback freeze tag: legacy/pine-controller/2026-08-25 (77a10e65).
~~~

Candidate paths:

~~~
.github/workflows/pine-defang-guard.yml
MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py
MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine
MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py
MTC_COMMAND_CENTER/01_MTC_PROJECT/tools/optimization_parameter_mapper.py
MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py
MTC_COMMAND_CENTER/tools/repo_guard.ps1
~~~

## 12. Out-of-scope observation

repo_guard.ps1's pre-existing protected path list contains
MTC_COMMAND_CENTER/01_PINE and MTC_COMMAND_CENTER/MTC_V2, while the active protected Pine
edited here is under MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine. Consequently,
the two deliberate dirty-tree carrier runs printed “[protected] none.” The newly authorized
Pine-alert scanner still blocked in both required arms. Fixing the older protected-path list
was not in the eleven-row package and was not attempted.

## 13. Section 9 acceptance checklist — implementer evidence status

- [x] Owner authorization is explicitly recorded by the lane brief as WP-P0-23 T0/G2 against
  this package.
- [x] Freeze tag, peeled commit, protected blobs, and recoverable two-alert original verified.
- [x] Implementation commit touches only the seven implementation files/authorized anchors;
  this report is separately required by the lane brief.
- [x] Exactly one MTC_V2*.pine source exists; no MTC_V2_VIEW.pine or alert-capable copy exists
  in the active tree.
- [~] The 13 inputs and complete dispatch block are gone and no dangling wt_ survives.
  **Pine compile remains unverified without TradingView.**
- [x] Scanner and independent rg cover all 21 .pine files, find zero alert( literals, and
  report allowlist=0.
- [x] Exact pre-fix RED, arbitrary-tree RED, repaired GREEN, mutation restoration, commands,
  output, and exit codes recorded.
- [x] Thirteen Python defaults and complete L25 validation block are gone.
- [x] integrations_disabled is an empty compatibility no-op, emits no wt_ key, validates, and
  its new assertion has discriminating RED/GREEN evidence.
- [x] All seven tw_ declarations and all 24 tw_-containing declaration/check/validator/consumer
  lines are byte-identical.
- [ ] Render identity criteria 1–5 are **UNVERIFIED** without TradingView compile/export/
  Strategy Tester/screenshot data. Criterion 6 is source-level verified only.
- [x] Rollback was walked in a disposable worktree; both exact tag blob hashes and expected
  post-restore RED were recorded; candidate restoration returned GREEN and clean.
- [ ] Required T0 auditors and Lead independent acceptance are **PENDING** and cannot be issued
  by this implementer.
- [~] No deployment, TradingView publication, alert creation, host/venue, credential, testnet,
  live, master, merge, or tag action occurred. The feature-branch push is the sole later-brief
  override to the design package's older “no push” wording.

This report is an implementer handoff, not an acceptance verdict.

Final implementation commit SHA: f25152abe4747c888734fcfed988cdad1af3a944

## 14. AC-FIX follow-up — F3 case-variant enumeration and F4 Unicode root

**Date:** 2026-08-25

**Role:** Codex implementer, Gates 3–4 only; the live Claude lead retains Gate-5 acceptance.

**Repair audit tier:** T1 — bounded local-only non-economic guard code.
**Repair scope:** `MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py` only; this report is the
separately required evidence append. No Pine, config, mapper, test, `repo_guard.ps1`, workflow,
parity, MTC, trading, host, deployment, or credential surface changed.

### 14.1 F3 D026 — case-variant extension was fail-open

The untouched scanner was copied into the same relative path in scratch Git repo
`C:\tmp\wpp023_acfix_red_case`. With untracked `CASE_PROBE.PINE` containing `alert(`, the
pre-fix scanner silently omitted the file:

~~~
COMMAND: python MTC_COMMAND_CENTER\tools\check_no_pine_alerts.py
PINE_ALERT_GUARD PASS files=0 matches=0 allowlist=0
EXIT_CODE=0
~~~

The repair changes only the filename predicate from `name.endswith(".pine")` to
`name.lower().endswith(".pine")`. The exact same untracked probe then went RED and was named:

~~~
COMMAND: python MTC_COMMAND_CENTER\tools\check_no_pine_alerts.py
PINE_ALERT_GUARD VIOLATION path=CASE_PROBE.PINE matches=1
PINE_ALERT_GUARD BLOCK files=1 matches=1 allowlist=0
EXIT_CODE=1
~~~

After deleting the probe through `apply_patch`, the scratch repo returned GREEN:

~~~
PINE_ALERT_GUARD PASS files=0 matches=0 allowlist=0
EXIT_CODE=0
~~~

Enumeration was checked beyond the literal example. `_pine_files()` uses `os.walk()` over the
filesystem, prunes only `.git`, and does not derive candidates from Git, so untracked and ignored
Pine files are in scope. The untracked `.PINE` mutation above proves that behavior dynamically.
The current worktree inventory is:

~~~
FILESYSTEM_PINE_COUNT=21
LOWERCASE_DOT_PINE_COUNT=21
CASE_VARIANT_COUNT=0
GIT_TRACKED_PINE_COUNT=21
~~~

Thus the repo currently uses only lowercase `.pine`, while the repaired predicate covers every
ASCII case spelling. No directory-following rule or invariant needle was widened.

### 14.2 F4 — Windows locale decoding crash and error-code collision

The local runtime reports `locale.getpreferredencoding(False) == "cp1254"`. An untouched scanner
copy under real Git root `C:\tmp\wpp023_acfix_nonascii\Barış_Şemaay` reproduced the reported
failure before the repair:

~~~
Exception in thread Thread-1 (_readerthread):
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9e ... cp1254.py
...
File "...check_no_pine_alerts.py", line 40, in _resolve_repo_root
    if result.returncode != 0 or not result.stdout.strip():
AttributeError: 'NoneType' object has no attribute 'strip'
EXIT_CODE=1
~~~

The subprocess now explicitly uses `encoding="utf-8", errors="replace"`; captured stdout and
stderr are also normalized to strings before evaluation. The exact real Unicode Git root now
decodes, resolves, scans, and exits normally:

~~~
PINE_ALERT_GUARD PASS files=0 matches=0 allowlist=0
EXIT_CODE=0
~~~

To falsify the failure classification in that same Unicode-path repo, a scratch `git.exe` emitted
the UTF-8 root plus a nonexistent `missing` component. The repaired top-level CLI produced its
contracted named BLOCK and the distinct inability-to-evaluate code:

~~~
PINE_ALERT_GUARD BLOCK reason=git_root_invalid detail=[WinError 2] Sistem belirtilen dosyayı bulamıyor: 'C:\\tmp\\wpp023_acfix_nonascii\\Barış_Şemaay\\missing'
EXIT_CODE=2
~~~

A valid Unicode repository correctly PASSes; an invalid decoded root correctly BLOCKs. Neither
case can now fall through to the violation code 1 via the former `None.strip()` crash.

### 14.3 Existing fail-closed arms and no-regression proof

All requested arms were re-executed against the repaired scanner/current unchanged carrier:

| Arm | Observed terminal evidence | Exit |
|---|---|---:|
| Scanner violation (`CASE_PROBE.PINE`) through `repo_guard.ps1` | scanner `BLOCK files=1 matches=1`; carrier `RESULT: BLOCKED` | scanner 1; carrier 1 |
| Scanner missing through `repo_guard.ps1` | `[pine-alert] scanner could not execute: ... [Errno 2] No such file or directory`; `RESULT: BLOCKED` | carrier 1 |
| Interpreter absent through `repo_guard.ps1` | `[pine-alert] scanner could not execute: F4 forced interpreter absent`; `RESULT: BLOCKED` | carrier 1 |
| Unreadable `READ_FAIL.pine` held with `FileShare.None` | `UNEVALUATED path=READ_FAIL.pine`; `BLOCK files=1 ... errors=1` | scanner 2 |
| Non-Git directory | `BLOCK reason=git_root_unavailable detail=fatal: not a git repository ...` | scanner 2 |

The required fixed-worktree carrier run after the one-file implementation commit was:

~~~
[dirty]     clean
[pine-alert] PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0
[unpushed]  1 commit(s) ahead of upstream

RESULT: PASS
EXIT_CODE=0
~~~

Additional checks:

~~~
python -m py_compile MTC_COMMAND_CENTER\tools\check_no_pine_alerts.py
EXIT_CODE=0

git diff --check
EXIT_CODE=0

git show --stat --oneline bc413924
bc413924 fix(guard): scan Pine paths case-insensitively
 MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py | 12 ++++++++----
 1 file changed, 8 insertions(+), 4 deletions(-)
~~~

F2 remained explicitly out of scope. An enumerated uppercase
`ONLY_ALERTCONDITION.PINE` containing only `alertcondition(` produced
`PINE_ALERT_GUARD PASS files=1 matches=0 allowlist=0`; `ALERT_NEEDLE` remains the literal
`b"alert("`.

This is implementer evidence, not self-acceptance. Gate 5 remains with the live Claude lead.

Final AC-FIX implementation commit SHA: bc413924d4e076fcabd98cf645e369ec06d43e97

## 15. AC-F2 - widened Pine alert invariant for alert-condition declarations

Owner authorization: Baris authorized the design amendment on 2026-08-25. WP-P0-19 section 6.1.3
previously named only the literal `alert(` as the invariant needle; this lane amends that section
to also cover `alertcondition(`. Nothing else in the design changes, and the allowlist remains
literally empty.

The scanner now counts two independent byte needles:

~~~
b"alert("
b"alertcondition("
~~~

The widened scanner was first run before touching Q-Trend and caught exactly the owner-authorized
file:

~~~
PINE_ALERT_GUARD VIOLATION path=MTC_COMMAND_CENTER/03_QUANTLENS/00_INBOX_REPORTS/1 Haziran/Stg Q Trend/Q Trend.pine matches=5
PINE_ALERT_GUARD BLOCK files=21 matches=5 allowlist=0
~~~

Treated file:

~~~
MTC_COMMAND_CENTER/03_QUANTLENS/00_INBOX_REPORTS/1 Haziran/Stg Q Trend/Q Trend.pine
~~~

The file is a third-party downloaded Q-Trend Pine v5 indicator in an inbox/archive directory. Its
five alert-condition declarations carried only human-readable Q-Trend messages, no JSON/webhook
payload and no venue routing. The active copy was de-fanged in place: the five declarations were
commented out, the indicator logic/rendering lines were otherwise left unchanged, and the header
records that the original pre-de-fang file is recoverable from git history at commit
`480598eaad02788b12d8b505cb93bcc346c1e5bd`.

Honest scope statement: the invariant now covers alert emission and alert-condition declaration. It
does not claim that all alert-related or WunderTrading material has been removed from the repository.
Payload builders in a Pine library and the original dispatch block quoted inside two tracked `.md`
files still exist and are guard-invisible by design.

AC-F2 proof, all from `C:\WPP023_20260825`:

New needle RED, with a scratch lowercase `.pine` containing only `alertcondition(`:

~~~
PINE_ALERT_GUARD VIOLATION path=ACF2_ALERTCONDITION_PROBE.pine matches=1
PINE_ALERT_GUARD BLOCK files=22 matches=1 allowlist=0
~~~

New needle GREEN after deleting that scratch file:

~~~
PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0
~~~

Old needle RED, with a scratch lowercase `.pine` containing only `alert(`:

~~~
PINE_ALERT_GUARD VIOLATION path=ACF2_ALERT_PROBE.pine matches=1
PINE_ALERT_GUARD BLOCK files=22 matches=1 allowlist=0
~~~

Old needle GREEN after deleting that scratch file:

~~~
PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0
~~~

Case-insensitive enumeration still holds, with an uppercase `.PINE` file containing only
`alertcondition(`:

~~~
PINE_ALERT_GUARD VIOLATION path=ACF2_CASE_PROBE.PINE matches=1
PINE_ALERT_GUARD BLOCK files=22 matches=1 allowlist=0
~~~

Final whole-tree sweep after all scratch files were removed:

~~~
PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0
~~~

This is implementer evidence, not self-acceptance. Gate 5 remains with the live Claude lead.
