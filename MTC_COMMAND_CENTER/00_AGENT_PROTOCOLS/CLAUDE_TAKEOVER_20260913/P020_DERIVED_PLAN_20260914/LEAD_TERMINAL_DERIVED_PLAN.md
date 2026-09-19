# LEAD_TERMINAL — WP-P0-20 derived measurement plan (from the V1.6 one-shot outputs) — derived 2026-09-14 21:11Z, validated 2026-09-15 05:03Z

## 1. P20DERIVFIX lane (Codex Plus gpt-5.5 high, 20:52Z-20:56Z, exit 0) — Lead adjudication: ACCEPTED
- Closes Opus round-6 **N6-8** (the derivation tool never re-ran the matching) and **N6-6** (dead `base_plan` parameter). `derive_benchmark_plan.py` sha256 `0bfd18915a0952cbf8bd1058b5d560a5cd30558a3f2f6d2ae6706947152289d7`; `SHA256SUMS.txt` verified (`sha256sum -c` OK); `REPORT_FIX2.md` in the tool dir.
- `lexicographic_first_matching` transcribed from `preselect_profile.py:412-443`: Lead byte-compared the two function bodies — identical except the docstring and the refusal class/code (`PreselectRefused("BENCHMARK_PROFILE_BLOCKED", …)` → `DerivationRefused("DERIVE_REFUSED_SELECTION_MISMATCH: …")`). `verified_selection` re-derives from `eligibility_matrix_binary_only` (booleans in the real record — checked; `is True` test is correct) and refuses when the recorded selection is not the lexicographically first matching.
- RED test `test_refuses_consistently_rewritten_matrix_and_selection` (tests:216): swaps GEN_A/GEN_B on 15m/1h and marks both eligible so every OLD check passes; refused with the new code. GREEN: `test_happy_path` unchanged, asserts `selection_rederived: true`.
- Lead re-run on the pinned 3.12 venv: `16 passed in 0.25s` (15 → 16). `EXPECTED_FROZEN_SHA256` unchanged = V1.6 `cb756020…`. No `--oneshot`, no git, no write into the package (confirmed).

## 2. Derivation run (Lead; single read; inputs hashed BEFORE the run — `RUN_LOG.txt`)
| Input | sha256 |
|---|---|
| `PRESELECTION_CALIBRATION.json` | `808cbcb4ce529450e7e832baeffae00d00e64a57c456331936a75232c3299427` |
| `PRESELECTION_ELIGIBILITY.json` | `fc5f8895a38147cbc76d93560b61f33cdea3b8215088acfbe6f6e8014c7bc6c2` |
| `PRESELECTION_FROZEN.json` (V1.6) | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` |
| base `benchmark/BENCHMARK_PLAN.json` | `c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7` |
| `derive_benchmark_plan.py` | `0bfd1891…` (above) |
Output **`BENCHMARK_PLAN_DERIVED.json` sha256 `d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580`**; a second run to a separate file is BYTE-IDENTICAL. `derivation` block carries all four input digests, `tool_sha256`, the frozen `family_order` (9 ids), `selection_rederived: true`, `rule_text`. Trials: 15 = 5 pairs × sizes 512/1024/2048 in frozen family order — `GEN_TRIPLE_EMA_STACK/15m`, `GEN_STOCH_OVERSOLD_CROSS/1h`, `GEN_KELTNER_BREAKOUT/2h`, `GEN_MACD_BULL_CROSS/4h`, `GEN_DONCHIAN_BREAKOUT/1D` (ids `p020-01…p020-15`). All non-trial base-plan keys value-equal to the base (checked key by key).

## 3. Driver validation without touching the package (`VALIDATE_PLAN_HARNESS.txt`)
`run_bounded_benchmark.py` (sha256 `3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324`) imported from the real benchmark dir with `PLAN_PATH` pointed at the derived file → `_validate_plan(_load_plan())` returned normally: **PLAN_VALID** (manifest digest, compatibility digest, V3/cost/funding record digests + sidecars, dataset digests, five families × 512/1024/2048 from `derivation.family_order`, five timeframes). A plain copy of the benchmark dir cannot be used (record paths are pinned absolute → `PLAN_INVALID: external instrument record path mismatch` in a scratch dir — expected, recorded).

## 4. What the reviewers should look at (derived-plan review roster: Lead ✔ + Gemini 3.7 + exact Sol; **no Opus this week** — roster limitation recorded; the derivation TOOL carries Opus round-5/6 acceptance and this delta closes two of its NITs)
- The driver reads `derivation.family_order` only; it does NOT verify `derivation.*_sha256` against the recorded outputs — the Lead's `RUN_LOG.txt` is that chain today. Reviewer question: should the driver pin `derivation.eligibility_sha256`/`calibration_sha256` before `--run`?
- Plan swap: `--run` reads `ROOT/BENCHMARK_PLAN.json`; the derived plan must be copied over the base plan in `C:/tmp/P020_LEAD_20260912/benchmark/` right before the run (base plan kept as `BENCHMARK_PLAN_BASE_c6f07afd.json`; `SHA256SUMS_V16.txt` refreshed; the frozen `source_pins` pinned the BASE plan and stay valid because `derivation.base_plan_sha256` = that pin).
- Owner authority for the measurement: `OD-20260914-P020-MEASURE-1` (B YES) — after this review, once, with its own terminal record; ~minutes of CPU, no token cost.

Recorded by Claude Opus 5 Lead (b9df29).
