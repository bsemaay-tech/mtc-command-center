# W352 report — owner decision 158 ratification-chain derivation

## Status

IMPLEMENTED WITH AN INHERITED INPUT BLOCKER. The W352 behavior and its four tests are green. The full suite and canonical gate cannot reach the prompt's predicted outcome because the forbidden external design bytes no longer match the repository manifest pin.

## Scope and authority

- Gate-1 tier: T1, because the only product change is a non-economic verifier/harness check. The worktree is `C:\WP012BUILD`, the branch is `feature/wp-p0-12-corrected-vnext-20260831`, and the measured starting HEAD is `d119d814afa69ca4131d047a120963a1416b023d`. There is no live, scheduled, broker, venue, host, deployment, credential, Pine, parity, or trading dependency.
- Allowed writes are the verifier, its contract self-tests, this report, the one canonical-gate receipt, and the external done marker. The kernel, goldens, inputs, catalog, manifest, anchor, probes, baseline, design, schemas, and every other repository path remain read-only, as required by `C:\tmp\LANE_PROMPTS_20260828\LANE_W352_RATIFICATION_CHAIN.md:5-9`.

## HEAD measurements

- The hard-coded tuple is `("#5", "#6", "#7", "#8", "#9")` at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:85`.
- Its only read is the equality check at `verify_bceg.py:448`; the refusal remains `SEMANTIC_COVERAGE_REVIEW_INVALID` through `_semantic_review_invalid` at `verify_bceg.py:209-211`, with the member/detail string constructed at `verify_bceg.py:449-450`. No other code site reads the tuple (`rg -n 'SEMANTIC_COVERAGE_REVIEW_CHAIN'`).
- `CONTRACT_TABLES_MANIFEST.json.reseal_history` starts at line 581 and contains 18 entries through line 966. The linked, chronological re-seal acts are `#2`, `#3`, `#4`, `#5`, `#6`, `#7`, `#8`, `#9`, `#10`, `#11`, `#12`, `#12b`, `#13`, `#14`, `#14b`, `#15`, and `#16`; the eighteenth entry is a base re-anchor, not a re-seal. The first two actors lack explicit numeric labels, but their old/new seal linkage precedes the explicit `#4` entry and the second entry says the input pins from re-seal `#2` stand unchanged (`CONTRACT_TABLES_MANIFEST.json:582-629`). Explicit identifiers and entry boundaries are at `:629`, `:653`, `:696`, `:727`, `:758`, `:804`, `:815`, `:839`, `:848`, `:869`, `:877`, `:898`, `:911`, `:920`, and `:933`.
- The corrective acts `#12b` and `#14b` are explicitly called re-seals by their `actor` fields, even though their seal values did not change (`CONTRACT_TABLES_MANIFEST.json:867-873`, `:909-916`). The final row is explicitly called a `base re-anchor`, has an unchanged seal value, and says only `IMPLEMENTATION_BASE_SHA` and the anchor moved (`CONTRACT_TABLES_MANIFEST.json:959-965`). The parallel anchor document records that operation in `base_repin_history` (`implementation_anchor.json:128-143`).
- Therefore the exact expected chain measured from HEAD is `["#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#12b", "#13", "#14", "#14b", "#15", "#16"]`.

## Rule recorded before coding

Read only `CONTRACT_TABLES_MANIFEST.json.reseal_history`; never use a number or bound supplied by the receipt. Preserve history order. Include every entry whose actor explicitly identifies a `re-seal #N` or `re-seal #Nb`. Because the two oldest rows predate actor labels, backfill only that leading prefix from the first explicit numeric re-seal label (`#4`) and its position, yielding `#2`, `#3`; do not silently infer an unlabeled entry later in the history. Include the `b` corrective acts because the manifest itself classifies them as re-seals and retains them as distinct history entries. Exclude the base re-anchor because the manifest calls it a base re-anchor rather than a re-seal and says the seal did not move; the anchor classifies that act under `base_repin_history`. A future explicitly labeled re-seal automatically appends to the derived chain. A future unlabeled non-base history entry makes derivation fail closed rather than narrowing the ratification set.

## Baseline test measurement

- Bare `pytest tests/corrected_vnext/contracts/selftests -q` was unavailable on PATH.
- From `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`, `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q` collected 318 tests: 316 passed and 2 failed. Both failures stop at `verify_bceg.py:2231` because the external design currently measures SHA-256 `03fdf5952a2365b2de60b55292a1bd50fce8c6c51788c19b59cecc5d8f5b3c94` and 1,843 lines while the manifest pins SHA-256 `5c657ec93c714b59d56a9ca99e7f42005061ceaad6f8d2889e2d691af3381c09` and 1,800 lines (`CONTRACT_TABLES_MANIFEST.json:13-16`).

## Implementation

Before, the verifier declared the literal tuple at old `verify_bceg.py:85` and compared the receipt directly with it at old `:448-450`. After, the verifier:

1. recognizes manifest actor identifiers of the form `re-seal #N` or `re-seal #Nb` without declaring a chain list (`verify_bceg.py:85-87`);
2. derives and validates the ordered chain from `reseal_history`, backfills only the leading legacy rows, retains corrective rows, excludes explicitly named base re-anchors, and refuses missing or duplicate identifiers (`verify_bceg.py:234-301`); and
3. loads the bundle manifest at the ratification check, compares the receipt to the complete derived list by exact equality, and retains the same `owner_ratification.chain: <detail>` shape (`verify_bceg.py:517-528`). The refusal producer is still `SEMANTIC_COVERAGE_REVIEW_INVALID` (`verify_bceg.py:211-213`).

No other refusal was changed. `rg -n 'SEMANTIC_COVERAGE_REVIEW_CHAIN|#5 through #9' tests/corrected_vnext/verify_bceg.py` returns no match.

## Per-test RED/GREEN evidence

The synthetic-manifest writer and synthetic full-gate setup are at `test_verify_bceg.py:49-56` and `:106-123`. The four guarded behaviors are at `:386-483`.

| Test | RED proving discrimination | Restored GREEN | What removal breaks |
|---|---|---|---|
| `test_w352_old_chain_is_refused_when_manifest_is_past_nine` | On the untouched pre-fix verifier, the focused command failed: expected return `2`, got accepting return `0`; stdout carried `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED`. | `1 passed in 0.14s`; also green in the final four-test run. | Restoring the old constant accepts the stale `#5..#9` receipt after manifest `#10` exists (`test_verify_bceg.py:386-407`). |
| `test_w352_manifest_derived_chain_clears_ratification_check` | With an evidence-only old-constant mutant, the focused test failed: expected return `0`, got refusal return `2`, with detail `expected seal ids #5, #6, #7, #8, #9`. | Green in `4 passed, 155 deselected in 0.16s`. | Removing manifest derivation rejects the exact manifest-derived chain (`test_verify_bceg.py:410-431`). |
| `test_w352_reseal_absent_from_manifest_is_refused` | With an evidence-only prefix-comparison mutant, the focused test failed: expected refusal return `2`, got accepting return `0`. | Green in `4 passed, 155 deselected in 0.16s`. | Weakening exact equality lets a receipt append `#999` and widen the ratified set (`test_verify_bceg.py:434-457`). |
| `test_w352_derivation_handles_legacy_corrective_and_base_history_rows` | With the evidence-only old-constant mutant, the focused test failed: actual `[#5..#9]` differed from expected `[#20, #21, #22, #22b, #23]`. | Green in `4 passed, 155 deselected in 0.16s`. | Removing the derivation loses legacy-prefix backfill, the corrective act, future reseals, and base re-anchor exclusion (`test_verify_bceg.py:460-483`). |

The old-constant mutant run produced `2 failed in 0.25s`; the widening mutant produced `1 failed in 0.25s`. Both mutants were removed. Final focused command `python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py -q -k w352` produced `4 passed, 155 deselected in 0.16s`. The neighboring receipt tests produced `13 passed, 146 deselected in 1.20s`. `python -m py_compile` passed for the verifier and test file. `git diff --check` passed. Black was not installed, so `python -m black --check ...` could not run.

## Full suite after the change

From the `mtc_v2` directory, `$env:PYTHONPATH='..'; python -m pytest tests/corrected_vnext/contracts/selftests -q` collected 322 tests: **320 passed, 2 failed** in 5.93 seconds. This is exactly four additions over the measured 318-test HEAD suite. The same two pre-existing tests fail at the design-pin check, now at `verify_bceg.py:2304`; no W352 test fails.

## Canonical gate — one invocation only

The single invocation used `python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --root C:/WP012BUILD/MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2 --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W352_GATE_RECEIPT.json`. It stopped at `DESIGN_PIN_MISMATCH` before the missing-review branch at `verify_bceg.py:4243-4246`, before the ratification-chain check, and before probe results were produced.

The measured refusal list, quoted verbatim, is **`["DESIGN_PIN_MISMATCH"]`**. There are no probe results, so no `10/10 DETECTED` claim is made. The exact stdout is preserved in `W352_GATE_RECEIPT.json:1-9`; its refusal and differing design measurements are at `:4-7`.

The early `GateRefusal` handler writes only stdout and returns before the normal `--output` writer (`verify_bceg.py:4290-4296`, `:4303-4310`), so the invocation itself did not create the file. The required receipt path contains an exact manual preservation of that stdout; the gate was not rerun.

## Discrepancies

- The lane prompt describes the 318-test HEAD suite as green. The measured HEAD suite is 316 passed / 2 failed because the forbidden external design file has drifted from the repository manifest pin. This lane will not change or mask that design mismatch.
- The lane prompt requires the canonical refusal list `["SEMANTIC_COVERAGE_REVIEW_MISSING"]` and probes 10/10 DETECTED (`LANE_W352_RATIFICATION_CHAIN.md:35-39`). The one actual gate run stopped earlier with `["DESIGN_PIN_MISMATCH"]` and no probe section because the external design mismatch is evaluated first.
- The lane prompt requires `--output` to leave the receipt at `C:/WP012BUILD/W352_GATE_RECEIPT.json` (`LANE_W352_RATIFICATION_CHAIN.md:36-42`). On a top-level `GateRefusal`, the verifier bypasses its output-file writer (`verify_bceg.py:4290-4296`, `:4303-4310`). This report discloses that the committed receipt is the exact captured stdout, not a file emitted by the invocation.
