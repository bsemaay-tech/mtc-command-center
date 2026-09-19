# T0 Corroboration Review Report: WP-P0-20 Preselection Procedure (V1.6 Frozen Artifact)

**Reviewer Role:** Supplemental Read-Only Corroboration Reviewer (`SUPPLEMENTAL_UNEXECUTED`)  
**Subject Packet:** `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16`  
**Execution Environment:** Windows, Python 3.12 (Pinned Interpreter `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`)  
**Corroborated Frozen Digest (V1.6):** `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126`  

---

## 1. Verified Packet Identity & Computed Digests (QUOTED)

All Lead-computed digests from [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/PACKET_SHA256SUMS.txt) and [`package/SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/SHA256SUMS.txt) were verified across the packet files:

| File Path | SHA-256 Digest (QUOTED) | Status |
|---|---|---|
| `authority/BENCHMARK_PLAN.json` | `c6f07afd14301e640841e7f4ec95dfcef860df3a02e3ef3768c1513c517104c7` | MATCH |
| `authority/BENCHMARK_RUNBOOK.md` | `5cec0af80885c9ebf3731d35f2cec7b2a6294031c244c868a4783de63eff7d1d` | MATCH |
| `authority/DECISIONS_rows_D9.md` | `b5e17fd678bfef22010fe6bd2e7040163cc0b754311874fc5dd6bca19302cbbf` | MATCH |
| `authority/LEAD_REPRODUCTION_V16.md` | `1688097f43784ee0a2e12555a20aa0926ce2c0ed73e8f9248b91d77b61510241` | MATCH |
| `authority/LEAD_TERMINAL_ELIG14.md` | `a20cf46252fee9730bfb79133a61059eeaae2248e03043db8c5dd3733b153ce4` | MATCH |
| `authority/LEAD_TERMINAL_ELIG15.md` | `ce5290fa28ac0997139aee6d77723ad2a480caf514eb85a701d112e6319b7593` | MATCH |
| `authority/P020_HANDOFF_lines53-70.md` | `3a277e23b957cacbf139893bd72ce5cce18a1c265554e3aae05d24c19a9b26a2` | MATCH |
| `authority/PRESELECTION_FROZEN_V15.json` | `b75489841a096f6f7271b12880c10cc318cfc25c8f19f7dedc8711baaefdc17b` | MATCH |
| `authority/run_bounded_benchmark.py` | `3d4453cd23ad0f56ae0b34f94b21b7b1f3715f180091821b383369aa62fab324` | MATCH |
| `authority/SYNTH-P020-BOUNDED-INSTRUMENT-V1.json` | `b55287f26d5ff0a4bd6afb7a9112844bc64cb68014b5e12f40b7e536f436e91e` | MATCH |
| `authority/SYNTH-P020-BOUNDED-INSTRUMENT-V2.json` | `1a1289641992d004977c274ef63c60e72f84319015d2a838f4574facf6db5a15` | MATCH |
| `authority/SYNTH-P020-BOUNDED-INSTRUMENT-V3.json` | `69b6f246ad721ccfde23f87c0b21b6470b8fb75b88552bfad004ef8c69d557f9` | MATCH |
| `package/preselect_profile.py` | `c82693d492268944a7b3ed42aebe57a03ce033c3e9e23b4ccc24a60d6931c8d5` | MATCH |
| `package/PRESELECT_RUNBOOK.md` | `53faa45e583617be11f80cbc1550a3ee806175daa684e8f1620d288e03aab344` | MATCH |
| `package/PRESELECTION_FROZEN.json` | `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126` | MATCH |
| `package/PRESELECTION_PREREG_V1.md` | `39f52ed0fc01bcc1017b36b9f2071ee59a66ecb46a07e89a60b0890c4a605d4c` | MATCH |
| `package/REPORT.md` | `47efb87f7e01435a2fcbf9ede484b59f6b41a3673758ea3bdb1f14686766050e` | MATCH |
| `package/REPORT_R2.md` | `3969621dd0b882b8b88dafe10be02ef71365a73336f46396e9d7c562f15b6541` | MATCH |
| `package/REPORT_R3.md` | `fe9f765d2a8deeb2861868bc36fc38b731c8bee0cf5b9ab4618614be3ae5ffd5` | MATCH |
| `package/REPORT_R4.md` | `ee88be55a6a430162a8737112e1739090b9cb77efc25fbab43efbf7b7790ade4` | MATCH |
| `package/REPORT_R5.md` | `385c4c33dc3793e71f6716d38268a52325e8aa93f67ba3c92a2992bb04c77226` | MATCH |
| `package/REPORT_R6.md` | `7b515c3dea93ab358caa9074c38716e4b0fb4a9472e4cb81fbdb57925f24fede` | MATCH |
| `package/REPORT_R7.md` | `d92c4bf1fa4355841c4c460bbef24de22e34b314cc20194a14eb267168a8403a` | MATCH |
| `package/SHA256SUMS.txt` | `9f8f567615cb03255cea14f350da10f8aa8d6b2167b13f17dc4776cfb19d0dcd` | MATCH |
| `package/tests/test_preselect.py` | `25d53fe47b0340825070de2938e4855aa4bb457de9ff63d0b5f41bbc641a057b` | MATCH |
| `package/tests/test_sizing_floor.py` | `00efdc0fb76deff9f4f7debe1743f0cde3649d018cb60c8980fe621b9c1e629d` | MATCH |
| `REVIEW_BRIEF.md` | `fcb869458726c39cad7b4c9ee806277315178b46a075ec535d9181ca28f01af9` | MATCH |

---

## 2. Conformance Table (Owner-Approved Shape vs. Implementation)

| Owner-Approved Mandate / Bullet | Implementing Text / Code Reference | Status |
|---|---|---|
| **1. Five BTCUSDT frozen datasets/timeframes:** `15m, 1h, 2h, 4h, 1D` preserved in fixed order. | [`PRESELECTION_PREREG_V1.md:200-217`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L200-L217); [`preselect_profile.py:125-128`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L125-L128); [`PRESELECTION_FROZEN.json:72-118, 449-455`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json#L72-L118) | **EQUAL** |
| **2. Three measured sizes per family:** `512, 1024, 2048` rows; exactly 15 trials; one process. | [`PRESELECTION_PREREG_V1.md:220-234, 484-489`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L220-L234); [`preselect_profile.py:51-53, 1238-1254`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L51-L53); [`PRESELECTION_FROZEN.json:149, 285-421`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json#L149) | **EQUAL** |
| **3. Candidate universe:** Nine OHLC-only `GEN_*` families and 359 already-registered parameter records; no new parameters or risk values. | [`PRESELECTION_PREREG_V1.md:145-176`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L145-L176); [`preselect_profile.py:129-132, 458-466`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L129-L132); [`PRESELECTION_FROZEN.json:153-263, 432`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json#L153-L263) | **EQUAL** |
| **4. Frozen deterministic ordering:** Families sorted by `(grid_size, strategy_id)` ascending; parameters by canonical JSON ASCII bytes. | [`PRESELECTION_PREREG_V1.md:177-199`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L177-L199); [`preselect_profile.py:157-164, 259-268`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L157-L164); [`PRESELECTION_FROZEN.json:71, 153-264, 786-788`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json#L71) | **EQUAL** |
| **5. Binary eligibility predicate:** Committed P020 2.1.0 trade event and successful ledger projection; zero economic metric reads. | [`PRESELECTION_PREREG_V1.md:358-434`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L358-L434); [`preselect_profile.py:1031-1100`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L1031-L1100); [`PRESELECTION_FROZEN.json:119-142`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json#L119-L142) | **EQUAL** |
| **6. Disjoint calibration windows & 1D limitation:** Rows 2049–4096 (15m, 1h, 2h, 4h) and 2049–2409 (1D, 361 rows, `SHORT_CALIBRATION_WINDOW_1D`); D1 Option A ratified. | [`PRESELECTION_PREREG_V1.md:235-357`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L235-L357); [`preselect_profile.py:55-121, 308-406, 995-1005`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L55-L121); [`PRESELECTION_FROZEN.json:4-70, 272-284, 422-428`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json#L4-L70) | **EQUAL** |
| **7. Lexicographically first complete matching:** 5 distinct families across 5 timeframes over frozen matrix; backtrack on failure. | [`PRESELECTION_PREREG_V1.md:470-481`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L470-L481); [`preselect_profile.py:412-444, 1102-1153, 1224-1234`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L412-L444); [`PRESELECTION_FROZEN.json:436`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json#L436) | **EQUAL** |
| **8. One-shot 15-trial locked check:** Fail-closed `BENCHMARK_PROFILE_BLOCKED` on any non-trade-bearing trial; no adaptive second selection. | [`PRESELECTION_PREREG_V1.md:482-543`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L482-L543); [`preselect_profile.py:1238-1266`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L1238-L1266); [`PRESELECTION_FROZEN.json:143-150`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json#L143-L150) | **EQUAL** |
| **9. Single `--oneshot` execution mode & T0 token gate:** Gated on digest token matching `PRESELECTION_FROZEN.json`; no `--calibrate`/`--eligibility` modes; `--freeze` rejects tokens. | [`preselect_profile.py:908-932, 1283-1311`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L908-L932); [`PRESELECTION_PREREG_V1.md:544-591`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L544-L591); [`PRESELECT_RUNBOOK.md:90-139`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECT_RUNBOOK.md#L90-L139) | **EQUAL** |
| **10. Owner decision D-P20-2 (Acceptance reporter untouched):** `check_p020_acceptance.py` untouched and excluded from artifact. | [`REPORT_R2.md:21-23`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/REPORT_R2.md#L21-L23); [`REPORT_R7.md:5`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/REPORT_R7.md#L5) | **EQUAL** |
| **11. Owner decision D9-A (Record V3 & Sizing Floor):** Instrument V3 `quantity_step = 0.00001` (venue-realistic Hyperliquid BTC step); risk fraction `0.0001` unchanged; provenance cites `OD-20260914-P020-RECORD-V3-1`. | [`SYNTH-P020-BOUNDED-INSTRUMENT-V3.json:25-39`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/SYNTH-P020-BOUNDED-INSTRUMENT-V3.json#L25-L39); [`DECISIONS_rows_D9.md:2`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/DECISIONS_rows_D9.md#L2); [`BENCHMARK_PLAN.json:290-294, 315`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/BENCHMARK_PLAN.json#L290-L294); [`run_bounded_benchmark.py:25`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/run_bounded_benchmark.py#L25) | **EQUAL** |

---

## 3. Detailed Technical Corroboration

### 3.1 Key-by-Key Diff: `authority/PRESELECTION_FROZEN_V15.json` vs. `package/PRESELECTION_FROZEN.json`

Every top-level key in `PRESELECTION_FROZEN.json` was compared against `PRESELECTION_FROZEN_V15.json`:

1. `artifact_version`: **DIFFERENT** (`"p020-preselection-frozen-v1.5"` → `"p020-preselection-frozen-v1.6"`)
2. `supersedes`: **DIFFERENT** (`"p020-preselection-frozen-v1.4"` → `"p020-preselection-frozen-v1.5"`)
3. `instrument_record_interval`: **DIFFERENT** (`record_id` `"SYNTH-P020-BOUNDED-INSTRUMENT-V2"` → `"SYNTH-P020-BOUNDED-INSTRUMENT-V3"`; `sha256` `1a1289...` → `69b6f2...`; `start_inclusive`/`end_exclusive` remain `2019-09-08T00:00:00Z` / `2026-05-01T00:00:00Z`)
4. `prereg_sha256`: **DIFFERENT** (`3f2ae5...` → `39f52e...`)
5. `procedure_code_sha256`: **DIFFERENT** (`54f35c...` → `c82693...`)
6. `runbook_sha256`: **DIFFERENT** (`63874f...` → `53faa4...`)
7. `source_pins.BENCHMARK_PLAN.json`: **DIFFERENT** (`8cf52e...` → `c6f07a...`)
8. `source_pins.run_bounded_benchmark.py`: **DIFFERENT** (`b8a8f2...` → `3d4453...`)
9. `authority`: **EQUAL**
10. `calibration_window_rule`: **EQUAL**
11. `calibration_windows`: **EQUAL** (all rows and SHA-256 hashes identical across all 5 timeframes)
12. `canonicalization`: **EQUAL**
13. `datasets`: **EQUAL** (all datasets, normalized paths, rows, and hashes identical)
14. `eligibility_predicate`: **EQUAL** (guards, forbidden_reads, trade_bearing, ledger_projection identical)
15. `eligibility_run`: **EQUAL** (one_shot, 15 trials, second_selection FORBIDDEN, selection_binding identical)
16. `execution_identity_recheck`: **EQUAL**
17. `execution_status`: **EQUAL** (`"FROZEN_NOT_EXECUTED"`)
18. `family_order`: **EQUAL** (ranks 1–9, strategy IDs, grid sizes, fixed records, canonical bytes, and hashes identical)
19. `family_ordering_rule`: **EQUAL**
20. `impl_head`: **EQUAL** (`"b9b72f858dc830a9389517f79da5ea3c1fa6122c"`)
21. `limitations`: **EQUAL** (`SHORT_CALIBRATION_WINDOW_1D` identical)
22. `measurement_inputs`: **EQUAL** (all 15 prefix definitions, timestamps, rows, and hashes identical)
23. `owner_decision`: **EQUAL**
24. `procedure`: **EQUAL** (`"PRESELECTION_PREREG_V1.md"`)
25. `registered_record_total`: **EQUAL** (`359`)
26. `required_review`: **EQUAL**
27. `selected_manifest_sha256`: **EQUAL** (`"712ddc2745c7fec8b3ab52e0e07d42a26d8d2a216ba0ea638192e795aa0b0e9a"`)
28. `selection_rule`: **EQUAL**
29. `source_pins.STRATEGY_INPUT_COMPATIBILITY.json`: **EQUAL**
30. `source_pins.mega_walk_forward.py`: **EQUAL**
31. `source_pins.p020_benchmark_runner.py`: **EQUAL**
32. `source_pins.p020_economics.py`: **EQUAL**
33. `source_pins.p020_owner_policy.py`: **EQUAL**
34. `source_pins.p020_simulator.py`: **EQUAL**
35. `source_pins.package.py`: **EQUAL**
36. `timeframe_order`: **EQUAL**

**Conclusion:** No selection rule, family ordering, parameter record, calibration window, or measurement input was altered between V1.5 and V1.6.

---

### 3.2 Owner Decision D9-A in Bytes

Comparison of [`authority/SYNTH-P020-BOUNDED-INSTRUMENT-V3.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/SYNTH-P020-BOUNDED-INSTRUMENT-V3.json) against [`authority/SYNTH-P020-BOUNDED-INSTRUMENT-V2.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/SYNTH-P020-BOUNDED-INSTRUMENT-V2.json) confirms that V3 differs from V2 strictly in three items:
1. `record_id`: `"SYNTH-P020-BOUNDED-INSTRUMENT-V3"` (was `"SYNTH-P020-BOUNDED-INSTRUMENT-V2"`).
2. `quantity_step`: `0.00001` (was `1`).
3. Added provenance block (`provenance.quantity_step_correction`):
```json
    "quantity_step_correction": {
      "from": 1,
      "to": 0.00001,
      "reason": "the V1/V2 step of one whole contract floored every risk-sized order on 1h/2h/4h/1D to zero under the owner risk fraction 0.0001 (D8-A diagnostic, LEAD_TERMINAL_ELIG15.md); venue-realistic Hyperliquid BTC step per 03_PRODUCTION_CLOSURE_MATRIX.md:32 row I-3; owner ratification OD-20260914-P020-RECORD-V3-1 (chat: D9 A)",
      "ratified_by": "Baris Semaay",
      "ratified_at_utc": "2026-09-14T12:59:00Z"
    }
```
`minimum_quantity: 0`, `minimum_notional: 0`, `effective_interval` (`2019-09-08T00:00:00Z` to `2026-05-01T00:00:00Z`), and owner policy value `requested_risk_fraction: "0.0001"` remain strictly unchanged across the entire benchmark and preselection stack.

---

### 3.3 Sizing Floor Test (`package/tests/test_sizing_floor.py`)

Inspection of [`test_sizing_floor.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/tests/test_sizing_floor.py) confirms:
- Parametrized over all five timeframes (`15m, 1h, 2h, 4h, 1D`) with a synthetic BTC-scale price frame (~$100,000–$105,000).
- **GREEN Arm (`test_v3_quantity_step_is_trade_bearing_for_synthetic_btc_scale_frame`):** Evaluates `ps.trade_bearing_gate` with `v3_plan` (referencing V3 bytes); succeeds without exception (trade-bearing).
- **RED Arm (`test_v2_quantity_step_blocks_the_same_synthetic_btc_scale_frame`):** Monkeypatches `driver.RECORD_PATHS["instrument"]` to `V2_PATH` and invokes `v2_plan_from(v3_plan)`; asserts `driver.BenchmarkProfileBlocked` with the exact clause `no actual trade-bearing 2.1.0 successor result`.
- The test directly depends on the instrument record bytes (V3 allows fractional contract orders with `0.00001`, whereas V2 quantizes fractional risk orders below 1.0 down to 0).

---

### 3.4 Closure of Historical Findings (R1–R6, S1–S5, NIT-1, NIT-4, T1–T4, V1.5)

- **R1 / R5 (Predicate parity & No economic leak):** [`preselect_profile.py:1031-1100`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L1031-L1100) implements `trade_bearing_gate`, clause-for-clause identical to `_execute_trial:459-493` with count parity and ledger checks; no R-multiples or PnL are converted or returned.
- **R2 / S1 (Single transaction & Selection re-derivation):** `_run_oneshot` runs calibration in memory, matches via `lexicographic_first_matching`, and verifies via `verified_selection` ([`preselect_profile.py:1102-1153`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L1102-L1153)) before running 15 trials; no mutable file read exists between steps.
- **R3 / S2 (Atomic exclusive reservation):** `reserve_outputs` ([`preselect_profile.py:700-715`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L700-L715)) uses `open(path, "xb")` before running simulations; failure seeks and truncates reserved files to record `ABORTED` records without deleting.
- **R4 / S3 (Single read per dataset):** `verify_frozen_identity` ([`preselect_profile.py:549-630`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L549-L630)) hashes dataset raw bytes once; `dataset_lines` slices in-memory bytes without reopening files.
- **S4 (No trade series materialization):** `trade_bearing_gate` ([`preselect_profile.py:1085-1089`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L1085-L1089)) checks `hasattr(trades, "__len__")` and takes `len(trades)` without iterating or indexing `trades`.
- **NIT-1 (Disjointness at consumption):** `calibration_frame` ([`preselect_profile.py:995-1005`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L995-L1005)) calls `assert_disjoint` where the window is parsed.
- **NIT-4 (Self-binding procedure digest):** `build_freeze` records `procedure_code_sha256` and `verify_frozen_identity` validates it before execution ([`preselect_profile.py:578-582, 875`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L578-L582)).
- **T1 (Carried token digest):** `require_t0_authorization` ([`preselect_profile.py:908-932`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L908-L932)) parses the exact hashed bytes and passes the accepted digest into both output records.
- **T2 (Single plan parse):** `verify_frozen_identity` parses `verified_plan` and passes it to `_run_oneshot` without post-preflight file reloads.
- **T3 (Two-output commit / abort atomicity):** `ReservedOutputs.commit` ([`preselect_profile.py:660-676`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py#L660-L676)) writes, truncates, flushes both handles before closing; failures write `ABORTED` to both files.
- **T4 / S5 (Refusal phase separation):** Documented in [`PRESELECT_RUNBOOK.md:167-183`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECT_RUNBOOK.md#L167-L183) and [`PRESELECTION_PREREG_V1.md:531-537`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md#L531-L537).

---

## 4. Exact Read Coverage with Ranges & Continuations

Every native read tool call adhered to the ≤150 lines per view rule. Complete read coverage for all required files within `_gemini_packets_20260913/P020_PRESELECT_V16`:

1. [`AGENTS.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md): Lines 1–64 (Complete).
2. [`REVIEW_BRIEF.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/REVIEW_BRIEF.md): Lines 1–59 (Complete).
3. [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/PACKET_SHA256SUMS.txt): Lines 1–28 (Complete).
4. [`package/PRESELECTION_PREREG_V1.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_PREREG_V1.md):
   - View 1: Lines 1–150
   - Continuation 1: Lines 151–300
   - Continuation 2: Lines 301–450
   - Continuation 3: Lines 451–600
   - Continuation 4: Lines 601–612 (Complete).
5. [`package/PRESELECTION_FROZEN.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECTION_FROZEN.json):
   - View 1: Lines 1–150
   - Continuation 1: Lines 151–300
   - Continuation 2: Lines 301–457 (Complete).
6. [`package/preselect_profile.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/preselect_profile.py):
   - View 1: Lines 1–150
   - Continuation 1: Lines 151–300
   - Continuation 2: Lines 301–450
   - Continuation 3: Lines 451–600
   - Continuation 4: Lines 601–750
   - Continuation 5: Lines 751–900
   - Continuation 6: Lines 901–1050
   - Continuation 7: Lines 1051–1200
   - Continuation 8: Lines 1201–1315 (Complete).
7. [`package/tests/test_preselect.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/tests/test_preselect.py):
   - View 1: Lines 1–150
   - Continuation 1: Lines 151–300
   - Continuation 2: Lines 301–450
   - Continuation 3: Lines 451–600
   - Continuation 4: Lines 601–750
   - Continuation 5: Lines 751–900
   - Continuation 6: Lines 901–1050
   - Continuation 7: Lines 1051–1200
   - Continuation 8: Lines 1201–1350
   - Continuation 9: Lines 1351–1500
   - Continuation 10: Lines 1501–1650
   - Continuation 11: Lines 1651–1800
   - Continuation 12: Lines 1801–1865 (Complete).
8. [`package/REPORT_R2.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/REPORT_R2.md):
   - View 1: Lines 1–150
   - Continuation 1: Lines 151–303 (Complete).
9. [`package/REPORT_R3.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/REPORT_R3.md):
   - View 1: Lines 1–150
   - Continuation 1: Lines 151–300
   - Continuation 2: Lines 301–390 (Complete).
10. [`package/REPORT_R4.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/REPORT_R4.md):
    - View 1: Lines 1–150
    - Continuation 1: Lines 151–300
    - Continuation 2: Lines 301–461 (Complete).
11. [`package/REPORT_R5.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/REPORT_R5.md): Lines 1–125 (Complete).
12. [`package/REPORT_R6.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/REPORT_R6.md):
    - View 1: Lines 1–150
    - Continuation 1: Lines 151–228 (Complete).
13. [`package/REPORT_R7.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/REPORT_R7.md):
    - View 1: Lines 1–150
    - Continuation 1: Line 151 (Complete).
14. [`package/tests/test_sizing_floor.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/tests/test_sizing_floor.py): Lines 1–110 (Complete).
15. [`authority/SYNTH-P020-BOUNDED-INSTRUMENT-V3.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/SYNTH-P020-BOUNDED-INSTRUMENT-V3.json): Lines 1–45 (Complete).
16. [`authority/SYNTH-P020-BOUNDED-INSTRUMENT-V2.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/SYNTH-P020-BOUNDED-INSTRUMENT-V2.json): Lines 1–38 (Complete).
17. [`authority/LEAD_TERMINAL_ELIG15.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/LEAD_TERMINAL_ELIG15.md): Lines 1–45 (Complete).
18. [`authority/LEAD_REPRODUCTION_V16.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/LEAD_REPRODUCTION_V16.md): Lines 1–22 (Complete).
19. [`authority/PRESELECTION_FROZEN_V15.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/PRESELECTION_FROZEN_V15.json):
    - View 1: Lines 1–150
    - Continuation 1: Lines 151–300
    - Continuation 2: Lines 301–457 (Complete).
20. [`authority/DECISIONS_rows_D9.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/DECISIONS_rows_D9.md): Lines 1–4 (Complete).
21. [`package/PRESELECT_RUNBOOK.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/PRESELECT_RUNBOOK.md):
    - View 1: Lines 1–150
    - Continuation 1: Lines 151–206 (Complete).
22. [`package/SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/package/SHA256SUMS.txt): Lines 1–14 (Complete).
23. [`authority/P020_HANDOFF_lines53-70.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/P020_HANDOFF_lines53-70.md): Lines 1–19 (Complete).
24. [`authority/BENCHMARK_PLAN.json`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/BENCHMARK_PLAN.json):
    - View 1: Lines 1–150
    - Continuation 1: Lines 151–300
    - Continuation 2: Lines 301–383 (Complete).
25. [`authority/run_bounded_benchmark.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P020_PRESELECT_V16/authority/run_bounded_benchmark.py):
    - Lines 440–520 (Required eligibility predicate range).
    - Lines 1–40 (RECORD_PATHS & sidecars).

---

## 5. NOT VERIFIED

- **Live Command & Test Execution:** As a read-only corroboration reviewer under `SUPPLEMENTAL_UNEXECUTED`, no shell commands, pytest suites, or python scripts were executed. All observations are based exclusively on static byte comparisons.
- **Real Market Dataset Simulations & Full Eligibility Execution:** The real 45-cell calibration and 15 locked eligibility trials on the actual BTCUSDT CSVs were not executed. Whether a complete 5-family matching exists under V3 and whether all 15 measurement trials pass remains unexecuted.
- **Worktree Cleanliness & Live Git State:** The live repository worktree status and branch heads outside the read-only packet were not inspected with Git commands.
- **Canonical Acceptance:** Corroboration is independent and supplemental; canonical acceptance remains reserved for the Lead and authorized flagship reviewers.

---

## 6. Findings Summary

- **REQUIRED Findings:** None (0).
- **NIT Findings:** None (0).

---

```json
{
  "part": "P020_PRESEL_G37_V16",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
