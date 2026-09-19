# SUPPLEMENTAL READ-ONLY CORROBORATION REVIEW: WP-P0-20 DERIVED MEASUREMENT PLAN AND DERIVATION TOOL

**Reviewer Model:** Gemini 3.7 Flash (High)  
**Role:** Supplemental Read-Only Corroboration Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Scope Authority:** Owner Decision `OD-20260914-P020-MEASURE-1` (B YES)  
**Evaluation Standard:** Strict byte-level corroboration against frozen artifacts, base plan, derivation rule, and owner handoff invariants. No commands executed; read-only byte inspection only.

---

## 1. Verified Packet Identity & Digest Cross-Check

All digests below are quoted and corroborated directly against `PACKET_SHA256SUMS.txt`, `derived/RUN_LOG.txt`, and the respective artifact contents:

| Component | File Path | Lead Quoted SHA-256 Digest | Match Status |
|---|---|---|---|
| **Base Plan** | `authority/BENCHMARK_PLAN.json` | `c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7` | EQUAL |
| **Driver** | `authority/run_bounded_benchmark.py` | `3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324` | EQUAL |
| **Frozen Preselection V1.6** | `inputs/PRESELECTION_FROZEN.json` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | EQUAL |
| **Eligibility Output** | `inputs/PRESELECTION_ELIGIBILITY.json` | `fc5f8895a38147cbc76d93560b61f33cdea3b8215088acfbe6f6e8014c7bc6c2` | EQUAL |
| **Calibration Output** | `inputs/PRESELECTION_CALIBRATION.json` | `808cbcb4ce529450e7e832baeffae00d00e64a57c456331936a75232c3299427` | EQUAL |
| **Derivation Tool** | `tool/derive_benchmark_plan.py` | `0bfd18915a0952cbf8bd1058b5d560a5cd30558a3f2f6d2ae6706947152289d7` | EQUAL |
| **Tool Test Suite** | `tool/tests/test_derive_benchmark_plan.py` | `185af7b237d11d6e9365716c4ff127eedc967d4a91f82b9107e016d95ad4c22a` | EQUAL |
| **Derived Benchmark Plan** | `derived/BENCHMARK_PLAN_DERIVED.json` | `d84b043a2b262d1c9a3c98f29f538eec169c05a0ecad0a97d801a01d9a7e2580` | EQUAL |

---

## (a) Trial Conformance Table (15 Trials)

Each of the 15 trials in `derived/BENCHMARK_PLAN_DERIVED.json` was compared against:
1. `inputs/PRESELECTION_FROZEN.json` `datasets[timeframe]` and `measurement_inputs[timeframe].prefixes[input_rows]`;
2. `inputs/PRESELECTION_FROZEN.json` `family_order` entry for the family (`fixed_parameter_record`);
3. The selected family/timeframe mapping recorded in `inputs/PRESELECTION_ELIGIBILITY.json` and `inputs/PRESELECTION_CALIBRATION.json`:
   - `15m` $\rightarrow$ `GEN_TRIPLE_EMA_STACK`
   - `1h` $\rightarrow$ `GEN_STOCH_OVERSOLD_CROSS`
   - `2h` $\rightarrow$ `GEN_KELTNER_BREAKOUT`
   - `4h` $\rightarrow$ `GEN_MACD_BULL_CROSS`
   - `1D` $\rightarrow$ `GEN_DONCHIAN_BREAKOUT`
4. The trial ordering, which strictly follows frozen `family_order` ranks 1, 2, 3, 4, 7.

| Trial ID | Triple (Family, TF, Rows) | Dataset ID / SHA-256 / Path / Bar Sec / Sel Order / Symbol | Prefix SHA-256 | Parameter Record | Conformance Verdict |
|---|---|---|---|---|---|
| `p020-01-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n512` | `(GEN_TRIPLE_EMA_STACK, 15m, 512)` | `BINANCE_FUTURES_BTCUSDT_15m_20250901_20260427` / `472462faf3081027e9fbc791d1d62aeab424481a78860eb4bc5d786d8e50f372` / `normalized\binance_futures\BTCUSDT\15m\BINANCE_FUTURES_BTCUSDT_15m_20250901_20260427.csv` / 900 / 0 / `BTCUSDT` | `de7d720d0bfea6f21d886388085326a7921463e25d4f4926354aa769eb0410ab` | `{"stop_lookback": 10, "touch_atr": 0.15}` | EQUAL |
| `p020-02-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n1024` | `(GEN_TRIPLE_EMA_STACK, 15m, 1024)` | `BINANCE_FUTURES_BTCUSDT_15m_20250901_20260427` / `472462faf3081027e9fbc791d1d62aeab424481a78860eb4bc5d786d8e50f372` / `normalized\binance_futures\BTCUSDT\15m\BINANCE_FUTURES_BTCUSDT_15m_20250901_20260427.csv` / 900 / 0 / `BTCUSDT` | `38f94e7b1284d8f5c435ec6a658721d499f206a4f05027ca07139cf2e6c176c1` | `{"stop_lookback": 10, "touch_atr": 0.15}` | EQUAL |
| `p020-03-GEN_TRIPLE_EMA_STACK-BTCUSDT-15m-n2048` | `(GEN_TRIPLE_EMA_STACK, 15m, 2048)` | `BINANCE_FUTURES_BTCUSDT_15m_20250901_20260427` / `472462faf3081027e9fbc791d1d62aeab424481a78860eb4bc5d786d8e50f372` / `normalized\binance_futures\BTCUSDT\15m\BINANCE_FUTURES_BTCUSDT_15m_20250901_20260427.csv` / 900 / 0 / `BTCUSDT` | `06da7286af00f6d4d69ae40caa0bf96c2072da35db0f5f95c5669e9ca4b0a21d` | `{"stop_lookback": 10, "touch_atr": 0.15}` | EQUAL |
| `p020-04-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n512` | `(GEN_STOCH_OVERSOLD_CROSS, 1h, 512)` | `BINANCE_FUTURES_BTCUSDT_1h_20240408_20260413` / `888297ddba58206e2bcedece50198c917297b3f514a66e0137a700d78f18f384` / `normalized\binance_futures\BTCUSDT\1h\BINANCE_FUTURES_BTCUSDT_1h_20240408_20260413.csv` / 3600 / 1 / `BTCUSDT` | `bce37cff96da136d8b2d4375aecbc197ed19241cd66f4c3965c1c746bf7f3fd2` | `{"oversold": 20, "smooth_d": 3, "stoch_n": 14}` | EQUAL |
| `p020-05-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n1024` | `(GEN_STOCH_OVERSOLD_CROSS, 1h, 1024)` | `BINANCE_FUTURES_BTCUSDT_1h_20240408_20260413` / `888297ddba58206e2bcedece50198c917297b3f514a66e0137a700d78f18f384` / `normalized\binance_futures\BTCUSDT\1h\BINANCE_FUTURES_BTCUSDT_1h_20240408_20260413.csv` / 3600 / 1 / `BTCUSDT` | `8b0fd23dc69f0aa68c4faf882f459f6948b921a23153bae05714845a979b7466` | `{"oversold": 20, "smooth_d": 3, "stoch_n": 14}` | EQUAL |
| `p020-06-GEN_STOCH_OVERSOLD_CROSS-BTCUSDT-1h-n2048` | `(GEN_STOCH_OVERSOLD_CROSS, 1h, 2048)` | `BINANCE_FUTURES_BTCUSDT_1h_20240408_20260413` / `888297ddba58206e2bcedece50198c917297b3f514a66e0137a700d78f18f384` / `normalized\binance_futures\BTCUSDT\1h\BINANCE_FUTURES_BTCUSDT_1h_20240408_20260413.csv` / 3600 / 1 / `BTCUSDT` | `385143699bccdc9301279b54bd73a6b26c12ff96549c260b4358f5ee79143f39` | `{"oversold": 20, "smooth_d": 3, "stoch_n": 14}` | EQUAL |
| `p020-07-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n512` | `(GEN_KELTNER_BREAKOUT, 2h, 512)` | `BINANCE_FUTURES_BTCUSDT_2h_20240419_20260413` / `bf161b20c6f82beb0c3848170198d55e88dadd710ad079e437558f540b1c62bd` / `normalized\binance_futures\BTCUSDT\2h\BINANCE_FUTURES_BTCUSDT_2h_20240419_20260413.csv` / 7200 / 9 / `BTCUSDT` | `7041c16c8908b3640e3ef3c700e5f4ba1f4919bc5cdb2492689aa300b2600051` | `{"atr_len": 10, "ema_len": 20, "mult": 1.5}` | EQUAL |
| `p020-08-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n1024` | `(GEN_KELTNER_BREAKOUT, 2h, 1024)` | `BINANCE_FUTURES_BTCUSDT_2h_20240419_20260413` / `bf161b20c6f82beb0c3848170198d55e88dadd710ad079e437558f540b1c62bd` / `normalized\binance_futures\BTCUSDT\2h\BINANCE_FUTURES_BTCUSDT_2h_20240419_20260413.csv` / 7200 / 9 / `BTCUSDT` | `d4e68844e15cc0afa6e37cdd49d924edb2909dea4bf80940a3a209d43b48eb6d` | `{"atr_len": 10, "ema_len": 20, "mult": 1.5}` | EQUAL |
| `p020-09-GEN_KELTNER_BREAKOUT-BTCUSDT-2h-n2048` | `(GEN_KELTNER_BREAKOUT, 2h, 2048)` | `BINANCE_FUTURES_BTCUSDT_2h_20240419_20260413` / `bf161b20c6f82beb0c3848170198d55e88dadd710ad079e437558f540b1c62bd` / `normalized\binance_futures\BTCUSDT\2h\BINANCE_FUTURES_BTCUSDT_2h_20240419_20260413.csv` / 7200 / 9 / `BTCUSDT` | `d5d67c8cf43cd37f812f2705751e26aa5924fd623a14e3ecdf1a902c9ed7f669` | `{"atr_len": 10, "ema_len": 20, "mult": 1.5}` | EQUAL |
| `p020-10-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n512` | `(GEN_MACD_BULL_CROSS, 4h, 512)` | `BINANCE_FUTURES_BTCUSDT_4h_20190908_20260413` / `0181cc1231957e914889ebaabef40e48ae6aca55bd55ce3fe0202fc3fd1287a8` / `normalized\binance_futures\BTCUSDT\4h\BINANCE_FUTURES_BTCUSDT_4h_20190908_20260413.csv` / 14400 / 11 / `BTCUSDT` | `2d80d8af4b765f5afc62fa383ab57fd44fdf3b9fd96318ab989ceeb12eff8223` | `{"fast": 12, "signal": 13, "slow": 21}` | EQUAL |
| `p020-11-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n1024` | `(GEN_MACD_BULL_CROSS, 4h, 1024)` | `BINANCE_FUTURES_BTCUSDT_4h_20190908_20260413` / `0181cc1231957e914889ebaabef40e48ae6aca55bd55ce3fe0202fc3fd1287a8` / `normalized\binance_futures\BTCUSDT\4h\BINANCE_FUTURES_BTCUSDT_4h_20190908_20260413.csv` / 14400 / 11 / `BTCUSDT` | `2150669eba6952f873835b762dc9fd4a630fb047798a83a64615ae57dfb94e02` | `{"fast": 12, "signal": 13, "slow": 21}` | EQUAL |
| `p020-12-GEN_MACD_BULL_CROSS-BTCUSDT-4h-n2048` | `(GEN_MACD_BULL_CROSS, 4h, 2048)` | `BINANCE_FUTURES_BTCUSDT_4h_20190908_20260413` / `0181cc1231957e914889ebaabef40e48ae6aca55bd55ce3fe0202fc3fd1287a8` / `normalized\binance_futures\BTCUSDT\4h\BINANCE_FUTURES_BTCUSDT_4h_20190908_20260413.csv` / 14400 / 11 / `BTCUSDT` | `1c314ef7670d40bd87313dc290ff24ddd18f463e604983637522a110b5c154a0` | `{"fast": 12, "signal": 13, "slow": 21}` | EQUAL |
| `p020-13-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n512` | `(GEN_DONCHIAN_BREAKOUT, 1D, 512)` | `BINANCE_FUTURES_BTCUSDT_1D_20190908_20260413` / `9371bc43b8b6f19c3727ef8f4aedde9375e30e6443f01fd5855d56b356a765bc` / `normalized\binance_futures\BTCUSDT\1D\BINANCE_FUTURES_BTCUSDT_1D_20190908_20260413.csv` / 86400 / 12 / `BTCUSDT` | `6302f2d729f90adb20d42f956b6128e7b0edc10a42a45cb2b3e015372a475a1a` | `{"atr_buf": 0.0, "channel_len": 10, "stop_lookback": 10}` | EQUAL |
| `p020-14-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n1024` | `(GEN_DONCHIAN_BREAKOUT, 1D, 1024)` | `BINANCE_FUTURES_BTCUSDT_1D_20190908_20260413` / `9371bc43b8b6f19c3727ef8f4aedde9375e30e6443f01fd5855d56b356a765bc` / `normalized\binance_futures\BTCUSDT\1D\BINANCE_FUTURES_BTCUSDT_1D_20190908_20260413.csv` / 86400 / 12 / `BTCUSDT` | `86d5b2d0bf941321e3040c3fd5e038d8901e60f6374a6daa9c81e57a24078223` | `{"atr_buf": 0.0, "channel_len": 10, "stop_lookback": 10}` | EQUAL |
| `p020-15-GEN_DONCHIAN_BREAKOUT-BTCUSDT-1D-n2048` | `(GEN_DONCHIAN_BREAKOUT, 1D, 2048)` | `BINANCE_FUTURES_BTCUSDT_1D_20190908_20260413` / `9371bc43b8b6f19c3727ef8f4aedde9375e30e6443f01fd5855d56b356a765bc` / `normalized\binance_futures\BTCUSDT\1D\BINANCE_FUTURES_BTCUSDT_1D_20190908_20260413.csv` / 86400 / 12 / `BTCUSDT` | `9de0ef1c165c900936dd12c996e1641c644d63119204dee3a3ae711c12a93c12` | `{"atr_buf": 0.0, "channel_len": 10, "stop_lookback": 10}` | EQUAL |

---

## (b) Base-Plan Key Preservation Table

Comparison of every top-level key between `authority/BENCHMARK_PLAN.json` (`c6f07afd...`) and `derived/BENCHMARK_PLAN_DERIVED.json` (`d84b043a...`):

| Top-Level Key | Status | Value Comparison / Details |
|---|---|---|
| `plan_version` | EQUAL | `"p020-bounded-performance-v1"` |
| `task` | EQUAL | `"LOCAL RESEARCH ENGINEERING + BOUNDED PERFORMANCE"` |
| `execution_status` | EQUAL | `"UNEXECUTED"` |
| `owner_authorization` | EQUAL | `"AUTHORIZED_BOUNDED_SUCCESSOR_PATH_MEASUREMENT"` |
| `research_only` | EQUAL | `true` |
| `no_profitability_or_strategy_selection_results` | EQUAL | `true` |
| `not_representative_performance_feasibility_profitability_strategy_selection_or_acceptance` | EQUAL | `true` |
| `trade_bearing_requirement` | EQUAL | `{"all_trials_required": true, "failure_status": "BENCHMARK_PROFILE_BLOCKED", "fallback_assumption": "FORBIDDEN"}` |
| `manifest` | EQUAL | Path `C:/tmp/P020_DERIVED_20260912/selected_manifest.json`, sha256 `712ddc2745c7fec8b3ab52e0e07d42a26d8d2a216ba0ea638192e795aa0b0e9a` |
| `compatibility` | EQUAL | Path `C:/tmp/P020_LEAD_20260912/dataset/STRATEGY_INPUT_COMPATIBILITY.json`, sha256 `3820d859b25a7b8cb1a0b746fc9f0d106d56d13e191d1324390f3bdd2e783c5d` |
| `implementation_sources` | EQUAL | 7 source entries and their sha256 digests (`run_bounded_benchmark.py`, `p020_benchmark_runner.py`, `p020_simulator.py`, `p020_economics.py`, `package.py`, `p020_owner_policy.py`, `mega_walk_forward.py`) |
| `trial_policy` | EQUAL | Identical dictionary (15 trials, 5 families, sizes [512, 1024, 2048], max rows 5000, fixed_2R, long, forbidden paths) |
| `trials` | DIFFERENT | Replaced 15 trials from base placeholder set with the 15 derived trials from V1.6 preselection outputs (mandated behavior) |
| `p020_profile` | EQUAL | Records V3 (`SYNTH-P020-BOUNDED-INSTRUMENT-V3.json` sha256 `69b6f246...`), Cost V1 (`27ee3b0e...`), Funding V1 (`fdeab636...`), interval, assumptions, forbidden inferences, calibration sub-block |
| `resource_measurement` | EQUAL | Wall clock, CPU, RAM, working set, `timing_excluded_from_semantic_comparison: true` |
| `repetition` | EQUAL | Interrupted/resumed, reference, comparison, extrapolation specifications |
| `output_contract` | EQUAL | Root non-existence requirement, 5 artifact names, 10 `does_not_publish` entries |
| `derivation` | ADDED | Added provenance block recording the 4 input digests, `family_order` (9 IDs), `selection_rederived: true`, `tool_sha256`, `rule_text` |

**Preservation Verdict:** Zero missing base keys; zero altered non-trial keys; `trials` is the only modified field; `derivation` is the only added field.

---

## (c) N6-8 and N6-6 Closure Verification

| Issue ID | Finding Summary | Implementation Evidence | Test / Corroboration Evidence | Status |
|---|---|---|---|---|
| **N6-8** | Derivation tool did not re-derive matching from binary matrix; a consistently rewritten output pair would pass | [derive_benchmark_plan.py](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_DERIVED_PLAN_20260915/tool/derive_benchmark_plan.py#L80-L138) transcribed `lexicographic_first_matching` from `preselect_profile.py:412-443` (lines 80-104), implemented `verified_selection` (lines 107-138) requiring `matrix.get(s, {}).get(tf) is True` and `recorded == derived`, and bound output to `verify_inputs` (line 162). Added `derivation.selection_rederived: true` (line 230). | [test_derive_benchmark_plan.py:216-243](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_DERIVED_PLAN_20260915/tool/tests/test_derive_benchmark_plan.py#L216-L243) `test_refuses_consistently_rewritten_matrix_and_selection` swaps GEN_A/GEN_B and marks both eligible. On pre-fix tool this test would pass (code 0); with the fix it triggers `DerivationRefused("DERIVE_REFUSED_SELECTION_MISMATCH...")` and exits with code 2. | **CLOSED** |
| **N6-6** | Dead `base_plan` parameter in `derive_trials` | [derive_benchmark_plan.py:165](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_DERIVED_PLAN_20260915/tool/derive_benchmark_plan.py#L165) signature is `def derive_trials(frozen: dict, selection: dict) -> list[dict]:`. Call site at line 222 passes only `(frozen, selection)`. | Byte inspection confirms `base_plan` argument was completely removed. | **CLOSED** |

### Line-by-Line Comparison of `lexicographic_first_matching`:
- **Tool implementation** (`tool/derive_benchmark_plan.py:80-104`):
  - Function signature: `def lexicographic_first_matching(family_order: list, timeframes: tuple, eligible: set) -> dict:` (Line 80)
  - Docstring: `"""Transcribed from preselect_profile.py:412-443."""` (Line 81)
  - Assignment & search initialization: lines 82-84
  - Search loop, recursion, and backtracking: lines 85-97
  - Failure branch: lines 99-103 raising `DerivationRefused("DERIVE_REFUSED_SELECTION_MISMATCH: no complete matching of %d distinct families to %d timeframes" % (len(timeframes), len(timeframes)))`
  - Success return: line 104 `return dict(zip(timeframes, assignment))`
- **Procedure source** (`inputs/preselect_profile.py:412-443`):
  - Lines 412-436: Identical signature, initialization, search loop, recursion, and backtracking.
  - Lines 438-442: Raises `PreselectRefused("BENCHMARK_PROFILE_BLOCKED", ...)` instead of `DerivationRefused`.
  - Line 443: Identical `return dict(zip(timeframes, assignment))`.
- **Differences:** Only the docstring and exception class/code differ. All operational algorithmic lines are byte-for-byte identical.

---

## (d) Adjudication Questions (Q1, Q2, Q3)

### Question Q1: Driver Acceptance and Unpinned Derivation Digests
* **Analysis:** In `authority/run_bounded_benchmark.py:185-194`, `_validate_plan` checks `derivation.family_order` (verifying that exactly 5 distinct families are selected from `family_order`). It does not inspect `derivation.eligibility_sha256`, `calibration_sha256`, `frozen_sha256`, `base_plan_sha256`, or `tool_sha256`.
* **Label:** **NIT**
* **Reasoning:** For a once-only, Lead-executed measurement run under `OD-20260914-P020-MEASURE-1`, the documentary chain is fully sealed and tamper-evident:
  1. `PRESELECTION_FROZEN.json` V1.6 digest (`cb756020...`) was independently accepted by the full T0 roster;
  2. `PRESELECTION_ELIGIBILITY.json` (`fc5f8895...`) and `PRESELECTION_CALIBRATION.json` (`808cbcb4...`) were written via atomic exclusive-create during `--oneshot` and cross-pin each other;
  3. `derive_benchmark_plan.py` strictly verified all input digests before creating `BENCHMARK_PLAN_DERIVED.json` (`d84b043a...`);
  4. The Lead's pre-execution log `RUN_LOG.txt` and packet manifests bind all SHA-256 hashes;
  5. The measurement driver actively validates dataset file SHA-256 digests, prefix lengths, manifest records, and V3 record digests.
  Modifying the driver to enforce preselection digests would break research/execution boundary separation and invalidate the frozen driver hash (`3d4453cd...`) with zero operational security benefit.

### Question Q2: Plan-Swap Procedure
* **Analysis:** `run_bounded_benchmark.py` hardcodes `PLAN_PATH = ROOT / "BENCHMARK_PLAN.json"` (line 20). The Lead's procedure backs up the base plan as `BENCHMARK_PLAN_BASE_c6f07afd.json`, copies `BENCHMARK_PLAN_DERIVED.json` over `BENCHMARK_PLAN.json`, updates `SHA256SUMS_V16.txt`, validates with `--validate-plan`, and executes with `--run --output-root <new_dir>`.
* **Label:** **SOUND**
* **Reasoning:**
  1. On the `--run` path, `_validate_plan` verifies manifest, compatibility, V3 record files, implementation sources, and dataset file hashes against disk. It does not re-read `SHA256SUMS_V16.txt` or preselection `source_pins`.
  2. The preselection `source_pins` pinned the base plan (`c6f07afd...`) for the `--oneshot` eligibility preflight; that run is already terminal (`PROFILE_ELIGIBLE_NOT_ACCEPTED`).
  3. The derived plan embeds `derivation.base_plan_sha256 = "c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7"`, ensuring unbroken chain-of-custody back to the base plan.
  4. **What must be recorded:** The execution launcher must record pre-run and post-run SHA-256 digests of `BENCHMARK_PLAN.json`, `run_bounded_benchmark.py`, `selected_manifest.json`, the record files, sidecars, and every output artifact (`interrupted_resumed.jsonl`, `reference.jsonl`, `run_report.json`, checkpoints).

### Question Q3: Rule Transcription and Degrees of Freedom
* **Analysis:** Evaluated `RULE_TEXT` in `tool/derive_benchmark_plan.py:17-24` and `tool/DERIVATION_RULE.md` against owner handoff requirements in `authority/P020_HANDOFF_lines53-70.md`.
* **Label:** **SOUND**
* **Reasoning:** The derivation tool leaves zero degrees of freedom that could alter what is measured:
  - *Trial Ordering:* Fixed strictly to frozen `family_order` $\times$ sizes `[512, 1024, 2048]`.
  - *Symbol Resolution:* `symbol_from_dataset` extracts `"BTCUSDT"` from dataset metadata.
  - *Trial ID Formatting:* Deterministic string template (`p020-XX-...`) used solely for journal labeling.
  - *Parameters & Data:* Pinned directly to the frozen `fixed_parameter_record` and frozen `measurement_inputs.prefixes`.
  The derived plan is the exact mechanical consequence of the frozen selection.

---

## (e) Review Findings

1. **[NIT] Unpinned Derivation Digests on Driver Run Path**
   - *File:* `authority/run_bounded_benchmark.py:185-194`
   - *Severity:* `NIT`
   - *Description:* `_validate_plan` checks `derivation.family_order` but ignores `derivation.eligibility_sha256`, `calibration_sha256`, `frozen_sha256`, and `base_plan_sha256`. For the one-shot Lead measurement run, this is fully documented in `RUN_LOG.txt` and packet digests. Driver-level digest pinning may be considered in future framework iterations.
2. **[NIT] Documentation Line Citation Residuals (Opus N6-1 / N6-7 / Sol-6-3)**
   - *File:* `inputs/PRESELECTION_PREREG_V1.md`, `inputs/PRESELECTION_FROZEN.json:139`
   - *Severity:* `NIT`
   - *Description:* Line citation annotations referencing driver lines `:459-493` shifted after D5 edits. These are inert text residuals scheduled for cleanup on the next package re-freeze.

---

## (f) EXACT Read Coverage with Ranges and Continuations

Native reads performed within `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_DERIVED_PLAN_20260915/` (and repo router `AGENTS.md`):

1. `AGENTS.md`: lines 1–64 (complete)
2. `REVIEW_BRIEF.md`: lines 1–34 (complete)
3. `PACKET_SHA256SUMS.txt`: lines 1–32 (complete)
4. `tool/derive_benchmark_plan.py`: lines 1–150; continuation lines 151–262 (complete, 262 lines)
5. `tool/tests/test_derive_benchmark_plan.py`: lines 1–150; continuation lines 151–300; continuation lines 301–337 (complete, 337 lines)
6. `tool/DERIVATION_RULE.md`: lines 1–61 (complete, 61 lines)
7. `tool/REPORT_FIX2.md`: lines 1–72 (complete, 72 lines)
8. `tool/TASK_P20DERIVFIX.md`: lines 1–15 (complete, 15 lines)
9. `derived/BENCHMARK_PLAN_DERIVED.json`: lines 1–150; continuation lines 151–300; continuation lines 301–450; continuation lines 451–533 (complete, 533 lines)
10. `derived/RUN_LOG.txt`: lines 1–13 (complete, 13 lines)
11. `derived/VALIDATE_PLAN_HARNESS_S4.txt`: lines 1–5 (complete, 5 lines)
12. `derived/validate_derived_plan_harness.py`: lines 1–51 (complete, 51 lines)
13. `derived/VALIDATE_PLAN_SCRATCH.txt`: lines 1–2 (complete, 2 lines)
14. `derived/LEAD_TERMINAL_DERIVED_PLAN.md`: lines 1–28 (complete, 28 lines)
15. `inputs/PRESELECTION_ELIGIBILITY.json`: lines 1–79 (complete, 79 lines)
16. `inputs/PRESELECTION_CALIBRATION.json`: lines 1–77 (complete, 77 lines)
17. `inputs/PRESELECTION_FROZEN.json`: lines 1–150; continuation lines 151–300; continuation lines 301–457 (complete, 457 lines)
18. `inputs/preselect_profile.py`: lines 412–448 (`lexicographic_first_matching`); lines 1102–1154 (`verified_selection`) ONLY (90 lines total)
19. `authority/BENCHMARK_PLAN.json`: lines 1–150; continuation lines 151–300; continuation lines 301–383 (complete, 383 lines)
20. `authority/run_bounded_benchmark.py`: lines 1–50; lines 85–207; lines 586–692 (280 lines total)
21. `authority/P020_HANDOFF_lines53-70.md`: lines 1–19 (complete, 19 lines)
22. `authority/DECISIONS_rows_MEASURE.md`: lines 1–5 (complete, 5 lines)
23. `authority/LEAD_TERMINAL_ELIG16.md`: lines 1–33 (complete, 33 lines)
24. `authority/LEAD_ADJUDICATION_R6_OPUS.md`: lines 1–21 (complete, 21 lines)
25. `authority/tests/test_validate_plan_family_set.py`: lines 1–130 (complete, 130 lines)

Total view actions: 29 tool calls; all ranges $\le 150$ lines.

---

## (g) Non-Empty NOT VERIFIED

1. **No Test Execution:** As a supplemental read-only reviewer (`SUPPLEMENTAL_UNEXECUTED`), no commands or pytest test runs were executed by this reviewer; test outcomes are corroborated from byte logs and code inspection.
2. **Real External Filesystem:** Paths located in `C:/tmp/*` and `C:/P020_IMPL_20260912/*` are outside this packet and were not inspected or resolved on disk.
3. **Canonical Acceptance Authority:** This report provides read-only corroboration under `OD-20260914-P020-MEASURE-1`. It does not claim canonical repository acceptance or authorize live execution on its own.

---

## (h) Machine-Readable Review Summary

```json
{
  "part": "P020_DERIVED_G37",
  "verdict": "PASS-WITH-NITS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "q1": "NIT",
  "q2": "SOUND",
  "q3": "SOUND",
  "findings": [
    {
      "id": "FINDING-G37-01",
      "severity": "NIT",
      "path": "authority/run_bounded_benchmark.py",
      "lines": "185-194",
      "description": "_validate_plan verifies derivation.family_order but does not check the four input digests inside derivation block"
    },
    {
      "id": "FINDING-G37-02",
      "severity": "NIT",
      "path": "inputs/PRESELECTION_PREREG_V1.md",
      "lines": "prereg text",
      "description": "Documentation line citation residuals from D5 driver shift deferred to next package re-freeze"
    }
  ],
  "required_scope_unread": []
}
```

VERDICT: PASS-WITH-NITS

GEMINI_READ_ONLY_OK
