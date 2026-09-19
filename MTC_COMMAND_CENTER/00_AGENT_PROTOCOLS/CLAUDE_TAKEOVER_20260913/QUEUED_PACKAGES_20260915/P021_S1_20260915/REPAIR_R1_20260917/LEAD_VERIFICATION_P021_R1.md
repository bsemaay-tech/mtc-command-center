# LEAD_VERIFICATION — WP-P0-21 S1 catalogue-only slice, T0 repair round 1 (`eada65ed`) after the lane-6 exact-Opus read of `7fecf204` returned REQUEST_CHANGES — 2026-09-17 18:4x-19:1x UTC+3

**Trigger:** lane 6 (optional lane, run by hand 18:22-18:42 UTC+3 on the reopened Pro window; launcher exit 0, 153 turns, 250-line report `OPUS_QUEUE_20260916/P021S1/ATTEMPT1_REQUEST_CHANGES_7fecf204/OPUS_T0_REPORT.md`) → **REQUEST_CHANGES**, two REQUIRED findings, five NITs. Mechanics VERIFIED by the reviewer (identities, scope, B-17 pin byte-identical across code/DECISIONS row/packet/test, both RED arms reproduced with a control arm, the ready-fence under its own mutants, 10 of 13 value mutations caught).
**REQUIRED-1:** `DIVERGENCE_METRIC_DEFINITION` pinned a Lead-authored statistic — "mean absolute difference of realised R-multiples" (signed → absolute; return fraction → R-multiple, whose risk-unit source B-04 is OPEN and not wired; count and standard deviation dropped) and "different side/size class" (an undefined classification) — instead of the ratified option M-C (packet §4: M-B as the gate on signal fidelity + M-A as the economic divergence, each with its own tolerance). The reviewer also noted that the counted Gemini review of `7fecf204` graded the definition EQUAL against evidence that did not support it ("two reviewers agreeing is not corroboration" — the Lead's own memory lesson, instantiated on the Lead's own slice).
**REQUIRED-2:** one `divergence_tolerance` declared where the ratified M-C row says "B-06 becomes two numbers"; the slice's own definition said "their own tolerances" (plural) — self-contradiction.
**NITs:** N-1 `self_check()` prints a hard-coded S2 line it never verifies; N-2 S2 provenance unpinned (three mutations survive); N-3 the B-13 carrier field `dataset_manifest_hash` named nowhere; N-4 ready-fence precision (no change); N-5 the closed number appended by tuple rebinding.
**Role:** Lead = builder of the slice (`OD-20260915-P021-S1-CATALOGUE-ONLY-1`) and of this repair (disclosed); T0 cap 3 rounds — round 1.

## Lead reading before the repair
The reviewer's fidelity walk is right on every point: the packet's M-C is defined by reference to rows M-A and M-B, and the first spelling re-authored both halves. Reproduction here is by reading (a definition string vs the packet rows in CT13 `QUEUED_PACKAGES_20260915/P021_OPTIONS_PACKET_S2_20260915.md:32-34`), not by execution; the two REQUIRED shapes are then turned into mutants below.

## Repair (`eada65ed`, +69/−15, three files)
- `p021_readiness_rules.py`: `DIVERGENCE_METRIC_M_A` and `DIVERGENCE_METRIC_M_B` restated VERBATIM from the packet rows (ASCII hyphen for the en dash; unit clauses appended); `DIVERGENCE_METRIC_DEFINITION` = the M-C row + the sentence naming the two B-06 numbers + M-B + M-A; no R-multiple and no "size class" anywhere → no B-04 dependency. `OPEN_NUMBERS`: `divergence_tolerance` → `divergence_tolerance_intent` (M-B gate, B-06) + `divergence_tolerance_return` (M-A economic divergence, B-06); the divergence rule's `missing_numbers` (four names) and the self-check wiring probe follow. NIT-1: the self-check's S2 line interpolates `CLOSED_NUMBER_VALUES` and the DATA_QUALITY / divergence limits instead of a literal.
- `tests/test_p021_eligibility.py` (`assert_readiness_fence`, run in every test's setUp/tearDown): `_EXPECTED_OPEN_NUMBERS` = the four names; the definition asserted by equality with the module constant, by the verbatim M-A and M-B sentences and the unit clause, by the absence of "absolute" / "R-multiple" / "size class", and by "each with its own tolerance"; the two B-06 names first in the rule's `missing_numbers` and as the whole B-06 set of `open_numbers`; four open numbers; NIT-2 provenance pins (`s2_decided_at == "2026-09-15"`, the decision row in `s2_source_document` and in the `gap_ratio_max` source).
- `tests/test_strategy_type_policy_set.py`: the catalogue open-number set at lines 118-122 follows (+2/−1); the accepted policy-set artifact fixture (`:21-57`) and its version hash (`:56`) are UNTOUCHED.
Ruff: 12 findings at HEAD → 12 at `eada65ed` (0 new); the three files were not ruff-formatted before either and are left as they were.

## Evidence
| Arm | Result | File |
|---|---|---|
| RED R1 — the old definition restored (mutant of the patched module) | **46 failed / 13 passed** (the fence runs in every test) | `LEAD_RED_P021_R1_R1_old_definition_restored.txt` |
| RED R2 — B-06 collapsed to one `divergence_tolerance` | **47 failed / 12 passed** (incl. the policy-set catalogue test) | `LEAD_RED_P021_R1_R2_single_tolerance.txt` |
| RED N2 — `s2_decided_at` rewritten to 2020-01-01 | **46 failed / 13 passed** | `LEAD_RED_P021_R1_N2_s2_decided_at_rewritten.txt` |
| RED N1 — `gap_ratio_max` 0.0001 → 0.001 | **46 failed / 13 passed**; `--self-check` now prints `gap_ratio_max=0.001` (the mutated value, no stale literal) | `LEAD_RED_P021_R1_N1_gap_ratio_max_0_001.txt` |
| GREEN — the three mandated modules, pinned Bridge 3.12 interpreter, `PYTHONPATH=MTC_COMMAND_CENTER/contracts;MTC_COMMAND_CENTER/03_QUANTLENS/tools`, ASCII basetemp | **59 passed, 108 subtests**; `--self-check` exit 0, `READY=False`, `OPEN NUMBERS: 4` | `LEAD_PYTEST_GREEN_R1.txt` |
| Guard | `RESULT: PASS`; staged exactly the three files | `LEAD_GUARD_R1.txt` |
| Gemini delta (`P021_R1_GEMINI`, packet `P021_R1_20260917`, 16 files incl. the packet's §4 rows) | COUNTED **PASS**, REQUIRED-1/2 CLOSED, zero substantive differences word by word, fence cannot pass for the wrong reason, artifact fixture untouched, 0 findings; 40 reads / 0 outside / 0 mismatches; 176 s | `GEMINI/` (+ `LEAD_ADJUDICATION.md` there) |

## Carried (not part of this commit)
N-3 (`dataset_manifest_hash` carrier field — record it as a DATA_QUALITY limit or name the deferral), N-5 (fold `gap_ratio_max` into the `CLOSED_NUMBERS` literal), N-4 (record the exact ready-fence guarantee, no code). The reviewer's NOT VERIFIED item 3 (the accepted policy-set artifact's hash is recorded only inside the test that asserts it) → record the hash in the P021 records outside the test.

## Roster
Lane 6 re-pinned to `eada65ed` (launcher, brief addendum 2026-09-17, agent brief, queue row, log); attempt 1 archived. The second exact-Opus read runs after lane 7 if the Pro window allows, else on the next reset; Sol (Sat 2026-09-19) generates from the pin that stands. The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
