# W351 second-pass inside-fence fold report

**Verdict:** CLOSED (originally FINDING; corrected by W353). Both facts hold at HEAD `4642998d`: (a) the fold's four scoped source/test items are implemented and the final contract self-test suite is green (`318 passed in 6.36s`, measured command evidence below); and (b) the receipt discrepancy this lane itself declared as D-1 was closed by W351B at commit `4642998d`, which regenerated the one permitted canonical gate receipt at the final anchor bytes so that it now records `implementation_anchor_sha256 = "6991a6a4cf7f81d4a30f3e0badb6ca257e9d31b7a7f9bd71a4d51a0779ea837d"` (`W351_GATE_RECEIPT.json:1932`), equal to the committed sidecar (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`). The D-1 text below is retained unchanged as the honest record of the intermediate-anchor receipt; see `## W351B` and `## W353`.

**Start identity:** worktree `C:\WP012BUILD`, branch `feature/wp-p0-12-corrected-vnext-20260831`, clean starting HEAD `3ed6ea87`. The lane requires that exact clean non-`master` start (`C:\tmp\LANE_PROMPTS_20260828\LANE_W351_SECOND_PASS_FOLD.md:4-6`).

**Tier and impact:** T1, because the change adds executable contract self-tests. No Pine, strategy, parity, kernel, golden, input, catalog, manifest, probe, baseline, schema, network, host, broker, or trading behavior changed. The stage defines Pine/strategy/parity as protected (`MTC_COMMAND_CENTER/01_MTC_PROJECT/AGENTS.md:3-5`); the final diff contains only the lane-whitelisted files plus this report and receipt.

## Measured command evidence

### New-test RED then GREEN

The four intended assertions were temporarily inverted together, without changing `verify_bceg.py`. The selected run returned:

```text
FFFF                                                                     [100%]
FAILED ...::test_contract_selftest_suite_reports_only_failing_test_ids
E AssertionError: Left contains one more item: 'mtc_v2/tests/corrected_vnext/contracts/selftests/test_synthetic_contract.py::test_failing_contract'
FAILED ...::test_contract_selftest_suite_reports_empty_failure_ids_when_all_pass
E {'returncode': 0} != {'returncode': 1}
FAILED ...::test_contract_selftest_suite_records_timeout
E {'returncode': 124} != {'returncode': 125}
FAILED ...::test_contract_selftest_suite_records_oserror
E {'returncode': 126} != {'returncode': 127}
4 failed in 1.53s
```

After restoring the intended assertions, the identical four-test selection returned:

```text
....                                                                     [100%]
4 passed in 1.34s
```

The final implementations are at `4642998d:contracts/selftests/test_verify_bceg.py:399-466`; the production contract they exercise is `4642998d:verify_bceg.py:4068-4106`.

### Final contract self-test suite

Working directory:
`C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2`

Command (with the user Scripts directory added to this process's `PATH`, `PYTHONPATH=..`, and `PYTHONDONTWRITEBYTECODE=1`):

```text
pytest tests/corrected_vnext/contracts/selftests -q
........................................................................ [ 22%]
........................................................................ [ 45%]
........................................................................ [ 67%]
........................................................................ [ 90%]
..............................                                           [100%]
318 passed in 6.36s
```

This is the measured prior 314 tests plus four additions, as required by the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W351_SECOND_PASS_FOLD.md:36-37`).

### Canonical gate - executed once

Working directory:
`C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON`

```text
PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W351_GATE_RECEIPT.json
EXIT=2
```

Verbatim measured receipt facts:

```text
refusals = ["SEMANTIC_COVERAGE_REVIEW_MISSING"]
probes = 10/10 DETECTED
implementation_anchor_sha256 = "302b1c6d6d25224aef42c99f92f8bafb2f7bde86dd8e0ddc252d189317679864"
```

The sole refusal is recorded at `W351_GATE_RECEIPT.json:650-654`; the ten `DETECTED` probe rows span `W351_GATE_RECEIPT.json:478-648`; the receipt's seal and anchor identities are at `W351_GATE_RECEIPT.json:1931-1932`.

## Per-item result

| Item | Before | After | Authority | RED / GREEN evidence |
|---|---|---|---|---|
| W279D-F05 anchor re-seal #16 | `reseal_history[-1].reason` named design v1.16; anchor SHA-256/sidecar was `22b2f91397e34d84d79670c3ca60a3f6a02d8fde5770814a94fab54f6954ae19` (`3ed6ea87:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:124`; `3ed6ea87:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`). | Only `v1.16` changed to `v1.17` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:124`). Final file SHA-256 and sidecar are `6991a6a4cf7f81d4a30f3e0badb6ca257e9d31b7a7f9bd71a4d51a0779ea837d` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`). `EXPECTED_SEAL_SHA` stayed `40aaf7da2a67753b74922576111cf1aede911c9de1815f6d34a04d22f8666fab` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:4`). No semantic review receipt exists; the gate records its absence (`W351_GATE_RECEIPT.json:650-654`). | Decisions 149/151 and 147; T350 authorizes the one-string correction and sidecar move (`C:\tmp\LANE_PROMPTS_20260828\_packets_T350\T350_TRIAGE_REPORT.md:276-302,487`). | Byte-level diff shows only `v1.16` -> `v1.17` in the anchor. The final suite is GREEN (measured command evidence above). Gate identity mismatch is finding D-1 below. |
| W279D-F06 real runner tests | The W346 gate test replaced `run_contract_selftest_suite` and used `raising=False`; no test called the real function (`3ed6ea87:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:125-131`; `C:\tmp\LANE_PROMPTS_20260828\W279D_REPORT.md:243-262`). | The existing monkeypatch now uses `raising=True` (`4642998d:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:125-132`). Four tests call the real function: mixed fail/pass parsing, all-pass, timeout, and OSError (`4642998d:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:399-466`). | Decision 150; T350 bounds the work to this file and names the real invocation, parsing, timeout, and OSError arms (`C:\tmp\LANE_PROMPTS_20260828\_packets_T350\T350_TRIAGE_REPORT.md:304-320,488`). | Each temporary assertion inversion failed on its covered value: exact failing ID, return code 0, timeout 124, and OSError 126; restored selection GREEN `4 passed in 1.34s`, and final suite GREEN `318 passed in 6.36s` (measured command evidence above). |
| GM83D-F02 retargeted test name | The name claimed an unconsumed schedule without a digest while the body asserted consumed schedule `SYNTH-COST-RULE2-07-RED-V1` with digest (`3ed6ea87:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py:149-160`; `C:\tmp\LANE_PROMPTS_20260828\GM83D_REPORT.md:20-27`). | Renamed to `test_corrected_manifest_carries_the_consumed_cost_schedule_and_digest`; body unchanged (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_results_corrected.py:149-161`). No `NOT_CONSUMED` test was added. | Decisions 144/147 and W342; T350 authorizes only the name half and leaves `NOT_CONSUMED` to W347B-D01 (`C:\tmp\LANE_PROMPTS_20260828\_packets_T350\T350_TRIAGE_REPORT.md:118-135,489`). | Final suite GREEN `318 passed in 6.36s` (measured command evidence above). |
| W279D-F04 honest provenance coverage naming | The prior record could be read as seven live provenance tests, although six replace the git changed-path measurement with a synthesized list (`C:\tmp\LANE_PROMPTS_20260828\W279D_REPORT.md:193-216`). | Exact statement for the Lead: **ONE live git-measured refusal test (`test_expected_source_provenance_refuses_expected_path_changed_after_base`) plus SIX exception-logic tests over a synthesized changed-path list.** No repository source change was made for this item. | Decision 147 / W342C; T350 defines this as a record-only correction (`C:\tmp\LANE_PROMPTS_20260828\_packets_T350\T350_TRIAGE_REPORT.md:255-274,490`). | No code change required; final suite GREEN `318 passed in 6.36s` (measured command evidence above). |

## Scope and final integrity checks

- `verify_bceg.py`, kernel, goldens, inputs, catalog, manifest, probes, baseline, design, and `C:\tmp\P012_CONTRACT_TABLES_W127` were not changed; those paths are forbidden by the lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W351_SECOND_PASS_FOLD.md:6-9`).
- `git diff --check` returned no error after the final edit.
- Final anchor file SHA-256 equals final sidecar: `6991a6a4cf7f81d4a30f3e0badb6ca257e9d31b7a7f9bd71a4d51a0779ea837d` (`contracts/implementation_anchor.json.sha256:1`).
- The absent section-16 receipt is consistent with the sole gate refusal (`W351_GATE_RECEIPT.json:650-654`).

## Discrepancies

### D-1 - canonical receipt identifies an intermediate anchor byte layout

During post-gate diff inspection, the edited anchor line was found to have gained one leading space. The gate had already run once and recorded SHA-256 `302b1c6d6d25224aef42c99f92f8bafb2f7bde86dd8e0ddc252d189317679864` (`W351_GATE_RECEIPT.json:1932`). Restoring the original indentation made the final anchor a true one-string-only edit and changed its correct digest/sidecar to `6991a6a4cf7f81d4a30f3e0badb6ca257e9d31b7a7f9bd71a4d51a0779ea837d` (`contracts/implementation_anchor.json.sha256:1`). Therefore the receipt does **not** equal the final sidecar, contrary to the lane requirement (`C:\tmp\LANE_PROMPTS_20260828\LANE_W351_SECOND_PASS_FOLD.md:37-39`). The gate was not rerun because the same requirement permits the canonical gate ONCE. This is one required finding for Lead disposition.

### D-2 - bare `pytest` was initially absent from PATH

The first literal suite attempt returned PowerShell `CommandNotFoundException`. `python -m pytest` was available and produced `318 passed`; the literal command subsequently produced `318 passed` after adding `%APPDATA%\Python\Python314\Scripts` to the process-local `PATH`. This is an environment invocation discrepancy, not a repository test failure.

## W351B - receipt regenerated at the final bytes

The canonical gate was run once from `C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON` with the same full command recorded by W351 (`W351_REPORT.md:58-63`):

```text
PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W351_GATE_RECEIPT.json
```

The receipt's anchor digest moved from `implementation_anchor_sha256 = "302b1c6d6d25224aef42c99f92f8bafb2f7bde86dd8e0ddc252d189317679864"` (`b037ad93:W351_GATE_RECEIPT.json:1932`) to `implementation_anchor_sha256 = "6991a6a4cf7f81d4a30f3e0badb6ca257e9d31b7a7f9bd71a4d51a0779ea837d"` (`W351_GATE_RECEIPT.json:1932`), matching the committed sidecar (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`).

Verbatim measured receipt facts:

```text
refusals = ["SEMANTIC_COVERAGE_REVIEW_MISSING"]
probes = 10/10 DETECTED
implementation_anchor_sha256 = "6991a6a4cf7f81d4a30f3e0badb6ca257e9d31b7a7f9bd71a4d51a0779ea837d"
observed_build_sha = "b037ad93ab0e9cb820c4bf0a90a65d2d8f10ffb4"
```

The refusal is at `W351_GATE_RECEIPT.json:650-654`, the ten `DETECTED` probe rows span `W351_GATE_RECEIPT.json:478-648`, and the regenerated identities are at `W351_GATE_RECEIPT.json:121,1932`.

## W353 - record-only corrections (no code, no sealed byte)

Lane W353 changed two record lines in this file and one sentence in `W342C_REPORT.md`. No file under `mtc_v2/` was touched,
no gate and no test suite was run in W353, and no measurement is claimed here that W353 did not take.

- **Measured span correction.** The four real-runner tests were cited as `test_verify_bceg.py:399-469`. Measured at HEAD
  `4642998d`, the block opens at `def test_contract_selftest_suite_reports_only_failing_test_ids` on line 399 and its last
  non-blank line is the closing brace of `test_contract_selftest_suite_records_oserror` on line 466; line 469 is the next
  definition, `def sealed_producer_fixture(`. The citation now reads `399-466` at `W351_REPORT.md:35` and in the
  W279D-F06 row of the per-item table. This matches the span V351C measured.
- **No sealed byte can move.** Neither `W351_REPORT.md` nor `W342C_REPORT.md` appears in the sealed bundle. The bundle members
  are the 19 entries of `files[]` in
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json`
  (`DERIVATIONS.md`, `scenario_catalog.json`, and the 17 `golden/corrected_vnext/RULE2-*.json` goldens); both report paths are
  worktree-root files and appear in none of them. `EXPECTED_SEAL_SHA` is
  `40aaf7da2a67753b74922576111cf1aede911c9de1815f6d34a04d22f8666fab` before and after W353, unchanged
  (`CONTRACT_TABLES_MANIFEST.json` `seal.EXPECTED_SEAL_SHA`).
