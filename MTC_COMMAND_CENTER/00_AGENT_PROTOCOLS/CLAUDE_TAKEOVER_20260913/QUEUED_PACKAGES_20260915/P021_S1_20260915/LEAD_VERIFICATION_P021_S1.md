# LEAD_VERIFICATION — WP-P0-21 S1 catalogue-only slice `701c5ddd` (branch `feature/p021-s1-policy-v1-numbers-20260915`, worktree `C:/tmp/P021_S1_20260915` from `origin/master` `fcac0ac6`) — 2026-09-15 19:42Z

Lead-built (Claude Opus 5, session 5, disclosed) under `OD-20260915-P021-S2-RECOMMENDED-1`; the Lead does not accept it. Unmerged until a T1 verdict (the catalogue is a research-gate contract).

| Item | Result | Evidence |
|---|---|---|
| Scope | three files: `03_QUANTLENS/tools/p021_readiness_rules.py` (+62/−12 incl. two pin constants), `tests/test_p021_eligibility.py` (+18/−1), `tests/test_strategy_type_policy_set.py` (+3/−1); the hashed policy-set artifact and `strategy_type_policy_set.py` untouched (ask H) | `DIFF_STAT_fcac0ac6_701c5ddd.txt` |
| What closed | `gap_ratio_max = 0.0001` (CLOSED, `P021_DECISION_3 = T`); DATA_QUALITY limits `gap_ratio_metric = m2_missing_bar_ratio`, `gap_ratio_formula_id` (B-17 pin), `dataset_hash_contract = ds-v1` (B-13 pin); divergence `divergence_metric = M-C` + definition (B-05); `POLICY_SET.owner_decisions` + dated S2 source | the diff |
| Still refusing | every check keeps `accepted_corrected_engine.B01`; `validate_catalog` still raises for a ready-looking rule; `readiness_record()["ready"] is False` | self-check + RED 3 |
| Tests (pinned 3.12.12, `PYTHONPATH=contracts;tools`) | `59 passed, 108 subtests passed` (eligibility + policy-set + data_gap_ratio) | `LEAD_PYTEST.txt` |
| Self-check | `SELF-CHECK PASS: 7 checks all refuse readiness`; 13 closed / 3 open; modified-copy arm re-pointed to `divergence_tolerance` | `LEAD_SELF_CHECK.txt` |
| RED 1 | new tests + OLD catalogue (scratch dir shadowing): **47 failed / 5 passed** (the fence asserts 3 open numbers and the new limits) | `LEAD_RED_ARM_1_new_tests_old_catalogue.txt` |
| RED 2 | OLD tests + new catalogue: **47 failed / 5 passed** (old fence pins 4 open numbers) | `LEAD_RED_ARM_2_old_tests_new_catalogue.txt` |
| RED 3 | mutant with `missing_rules=()` on DATA_QUALITY → `ValueError: P021.DATA_QUALITY could be presented as ready`, python exit 1 | `LEAD_RED_ARM_3_mutant_b01_dropped.txt` |
| Ruff `--select E9,F821,F811,F401,F841` | one finding: `test_strategy_type_policy_set.py:4` `json` unused — **pre-existing on master** (same finding on `fcac0ac6` bytes), left untouched (surface not in the CI Ruff path list) | `LEAD_RUFF.txt` |
| Guard | PASS | `LEAD_GUARD.txt` |
| Not verified | no real bundle evaluated (no evaluator exists — B-01); the catalogue's `check_set_identity` stays `None`; T0/T1 roster not yet read |

Next: Gemini detection root `P021_S1_GEMINI` (queued); T1 roster (exact Sol Fri / Wednesday Opus if allowance) before any PR.
