# WP-P0-21 — S1 catalogue slice brief (engineering follow-on of `OD-20260915-P021-S2-RECOMMENDED-1`) — written 2026-09-15 18:5xZ, NOT built tonight

**Why not built tonight:** the S2 packet §5 called this "one small T1 change with a RED/GREEN". Reading the bytes on `master` (`fcac0ac6`) shows it is entangled with two test fences and the hashed policy-set artifact, so it deserves a daytime slot with the T1 roster, not a night edit. Owner's values are recorded; nothing is lost by waiting.

## What the owner's word changes (recorded, not yet in code)
| Item | Value | Where it must land |
|---|---|---|
| B-02 `gap_ratio_max` | `0.0001` on `m2_missing_bar_ratio` (`P021_DECISION_3 = T`) | `03_QUANTLENS/tools/p021_readiness_rules.py`: `OPEN_NUMBERS` (line 166) → `CLOSED_NUMBERS` (+1 `ClosedNumber`, source = the decision row); `RULES[0]` (`P021.DETERMINISTIC_REPLAY`, lines 195-204): `missing_numbers=()` and a `("gap_ratio_max", …)` limit; `POLICY_SET["owner_decisions"]["P021_DECISION_3"] = "T"` + a dated S2 source pointer |
| B-17 formula pin | `m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)` | same rule: limit `("gap_ratio_formula_id", …)`; `missing_rules` −= `gap_ratio_formula.B17` |
| B-13 digest pin | `dataset_hash_required` satisfied by the `ds-v1` digest of the scanned bundle | same rule: limit `("dataset_hash_contract", "ds-v1")`; `missing_rules` −= `dataset_hash_contract.B13` |
| B-05 divergence metric | `M-C` | `RULES[6]` (`P021.BACKTEST_FORWARD_DIVERGENCE`, lines 228-234): limit `("divergence_metric", "M-C")` (+ the M-C definition text from `P021_OPTIONS_PACKET_S2_20260915.md` §4); `missing_rules` −= `divergence_metric.B05`; `POLICY_SET["owner_decisions"]["P021_DIVERGENCE_METRIC"] = "M-C"` |

## What else moves with it (the entanglement)
1. `validate_catalog` (lines 253-295) pins `EXPECTED_OPEN_NUMBER_NAMES` / `EXPECTED_CLOSED_NUMBER_NAMES` and the refusal wiring — they follow the constants automatically, but `self_check()` (lines 340-377) uses `RULES[3]` + `gap_ratio_max` as its "modified copy" arm → re-point that arm to `divergence_tolerance` (still OPEN) and update the printed lines.
2. `tests/test_p021_eligibility.py:33-38` `_EXPECTED_OPEN_NUMBERS` (four names; `assert_readiness_fence` asserts `len == 4` in setUp/tearDown of EVERY test) → three names, `len == 3`.
3. `tests/test_strategy_type_policy_set.py:113-121` `test_current_readiness_catalogue_stays_refused` pins the same four names → three.
4. **The hashed policy-set artifact**: `strategy_type_policy_set.py` `_SHARED_KEYS` carries `gap_ratio_max` (nullable; the accepted fixture has `"gap_ratio_max": None` and `"gap_method_version": "data_gap_ratio_m2_v1"`, version `p021pol-v1:4a807136…`). `POLICY_SET["reversible"]` says a change is "a new hashed strategy_type_policy_set version plus fresh evidence, per decisions 129/130". Setting `shared.gap_ratio_max = 0.0001` therefore mints a NEW policy-set version hash — that is B-22 territory (policy-set ratification, still OPEN in the gap table). **Decide first (owner, one line): does the S2 word also ratify the new policy-set version that carries `gap_ratio_max = 0.0001` (B-22 for that field), or does the catalogue close the number while the artifact stays `None` until B-22 is ratified as a whole?** Recommended: the latter (catalogue now, artifact with B-22) — it keeps one ratification event for the whole set.
5. Every check must STILL refuse readiness after the slice (`accepted_corrected_engine.B01` stays in every `missing_rules`; `validate_catalog` raises if any rule "could be presented as ready") — the RED/GREEN: GREEN = self-check passes with 3 open numbers and the new limits present; RED = the old tests (four names) fail on the new bytes, and a mutant that also drops `accepted_corrected_engine.B01` from `RULES[0]` must be refused by `validate_catalog`.

## Slice mechanics (daytime)
Fresh worktree from `origin/master` (`git worktree add --detach` then branch `feature/p021-s1-policy-v1-numbers-<date>`); pinned 3.12.12; `python -m unittest` for the two test files + `python p021_readiness_rules.py` self-check; Ruff (`--select E9,F821,F811,F401,F841`); guard PASS; Gemini detection; T1 roster before merge (the catalogue is a research-gate contract). Lead-built = disclosed, never Lead-accepted.

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
