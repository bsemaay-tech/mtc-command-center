### Independent Read-Only Detection Review: WP-P0-12 Funding Intake Slice-4 T0 Repair Round 1 (`a871e429`)

This review evaluates commit `a871e429` on branch `feature/p012-funding-intake-adapter-20260915`, addressing Opus reviewer finding **REQUIRED-1** from [`sources/OPUS_REPORT_attempt1_9ef072a8.md`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/sources/OPUS_REPORT_attempt1_9ef072a8.md#L264-L298).

---

### (a) Execution Traces

#### 1. No-Fills Accepting Test Trace
[`test_d6_without_a_fill_for_the_symbol_the_position_source_is_the_payments`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/subject/test_real_capture_HEAD_lines_890-975_new_tests.py#L40-L69) tests window `[2026-09-14T17:00:00Z, 2026-09-14T18:00:00Z)` with `r1_bindings()` (events at `17:00:00.041Z` and `18:00:00.060Z`, both reporting `szi = "0.00058"`) parametrized over `fills = b"[]"` and an ETH-only fill.

- **`_real_fills` output**:
  - For `b"[]"`, `_json_array_spans` yields 0 rows; `fills` is empty $\rightarrow$ returns `(None, [])`.
  - For the ETH fixture, the row's `coin` is `"ETH"`, whereas `symbol` is `"BTC"`. Line 40 (`value.get("coin") != symbol`) takes the branch; line 41 confirms `coin` is a string, and `continue` executes. The loop finishes with `fills` empty $\rightarrow$ returns `(None, [])`.
- **`payments_position` resolution**:
  - In [`_real_completion`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/subject/export_mtc_funding_HEAD_lines_1140-1290_real_fills_completion.py#L78-L145), `opening is None` triggers lines 95–104 before the grid walk.
  - `constant = {row.szi for row in pass_rows}` evaluates to `{Decimal('0.00058')}`.
  - `len(constant) == 1`, so `payments_position = Decimal('0.00058')`.
- **Grid walk & expected vs. observed**:
  - `grid = list(range(start.seconds, end.seconds + 1, _HOUR_SECONDS))` covers `[1789405200, 1789408800]` (hours `17:00:00Z` and `18:00:00Z`).
  - `position_at(time_ms)` checks `if payments_position is not None:` and immediately returns `Decimal('0.00058')` ($\neq 0$).
  - `expected = ["2026-09-14T17:00:00Z", "2026-09-14T18:00:00Z"]`.
  - Both captured payments round down to hours `17:00:00Z` and `18:00:00Z`, so `observed = ["2026-09-14T17:00:00Z", "2026-09-14T18:00:00Z"]`.
  - `expected == observed` holds.
- **Per-row `szi` check**:
  - For both rows, `position_at(row.time_ms)` returns `Decimal('0.00058')`, matching each row's `szi`.
- **Emitted `completion_check`**:
  - `"expected_funding_hours"`: `["2026-09-14T17:00:00Z", "2026-09-14T18:00:00Z"]`
  - `"observed_funding_hours"`: `["2026-09-14T17:00:00Z", "2026-09-14T18:00:00Z"]`
  - `"opening_position"`: `None` (since `opening is None`)
  - `"position_source"`: [`REAL_POSITION_SOURCE_PAYMENTS`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/subject/export_mtc_funding_HEAD_lines_150-200_constants_limitations.py#L9-L13) (since `payments_position is not None`)
- **Mutant failure mechanism**:
  - **M1** (no-fills branch returns `Decimal(0)`): `position_at` returns 0; `expected` collapses to `[]`; `expected != observed` triggers refusal `CANDIDATE_COVERAGE_INVALID`. Assertion line 54 `assert result.accepted is True` fails with:
    `D-6: the fills-derived position expects payments at [] but the captured funding passes carry payments at ['2026-09-14T17:00:00Z', '2026-09-14T18:00:00Z']`. Kills M1 on both test parameters.
  - **M2** (`position_source` relabelled): Assertion line 57 `assert check["position_source"] == exporter.REAL_POSITION_SOURCE_PAYMENTS` fails on both test parameters.
  - **M3** (`opening_position` always `None`): Survives this test because `opening_position` is expected to be `None` here; killed by the normal-path test below.

#### 2. Normal-Path Test Trace
[`test_d6_the_completion_check_names_the_fills_witness_as_the_position_source`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/subject/test_real_capture_HEAD_lines_890-975_new_tests.py#L9-L25) executes `build(evidence_kind=REAL)` using default fixtures.

- **`_real_fills` output**: Parses `FILLS_R1`, validates chain continuity from initial `startPosition="0.0"`, and returns `(Decimal("0.0"), fills_tuples)`.
- **`_real_completion` resolution**:
  - `opening is None` is `False`; `payments_position` remains `None`.
  - `position_at` calculates position from `opening + sum(...)`.
  - `opening_position` emits `str(opening)` $\rightarrow$ `"0.0"`.
  - `position_source` evaluates `payments_position is not None` as `False` $\rightarrow$ emits [`REAL_POSITION_SOURCE_FILLS`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/subject/export_mtc_funding_HEAD_lines_150-200_constants_limitations.py#L8) (`"coverage.fills_witness"`).
- **Mutant kills**:
  - **M3**: Assertion line 22 `assert check["opening_position"] == "0.0"` fails (`assert None == '0.0'`).
  - **M2**: Assertion line 20 `assert check["position_source"] == exporter.REAL_POSITION_SOURCE_FILLS` fails.

---

### (b) Adversarial Verification & Behaviour Preservation

1. **Path Isolation & Accidental Acceptance**:
   - The other-coin fixture cannot slip into the fills path: `_real_fills` filters strictly on `value.get("coin") == symbol`, ensuring `opening` is `None` and `fills` is `[]`.
   - The test asserts `check["position_source"] == REAL_POSITION_SOURCE_PAYMENTS`, `check["position_source"] != REAL_POSITION_SOURCE_FILLS`, `"fills witness carries no fill" in check["position_source"]`, and `check["opening_position"] is None`. Accidental routing through the fills path would fail all four assertions.

2. **Premature Refusal Analysis**:
   - Window: `start = 17:00:00Z`, `end = 18:00:00Z` are whole-hour ISO timestamps.
   - Payments at `17:00:00.041Z` and `18:00:00.060Z` sit within the window (end tolerance allows stamps up to `18:00:01Z`).
   - All preceding gates (profile kind `REAL_CAPTURE_READ_ONLY`, closed-shape coverage dict, D-1/D-2/D-3 digest and signature checks, non-empty inventory) pass cleanly.
   - Mutating `payments_position` in M1 causes failure strictly inside `_real_completion`, confirming execution reaches and exercises the D-6 completion check.

3. **Behaviour Preservation & Scope**:
   - Refusal codes and strings remain identical: the `CANDIDATE_COVERAGE_INVALID` refusal message in `export_mtc_funding.py:116-120` was moved before `position_at` verbatim.
   - The synthetic candidate path and fixtures are untouched.
   - Scope is restricted to exactly the 2 targeted files ([`subject/DIFF_STAT_9ef072a8_a871e429.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/subject/DIFF_STAT_9ef072a8_a871e429.txt#L1-L3)): 94 insertions, 14 deletions across [`export_mtc_funding.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/subject/export_mtc_funding_HEAD_lines_1140-1290_real_fills_completion.py) and [`test_mtc_funding_export_real_capture.py`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917/subject/test_real_capture_HEAD_lines_890-975_new_tests.py).

4. **Record Honesty**:
   - `LEAD_RED_lane8_R1_M1_no_fills_branch_returns_zero.txt`: 2 failed, 230 passed, 1 skipped.
   - `LEAD_RED_lane8_R1_M2_position_source_relabelled.txt`: 3 failed, 229 passed, 1 skipped.
   - `LEAD_RED_lane8_R1_M3_opening_position_always_none.txt`: 1 failed, 231 passed, 1 skipped.
   - `LEAD_PYTEST_GREEN_R1.txt`: 232 passed, 1 skipped.
   - `LEAD_FULL_BRIDGE_SUITE_R1.txt`: 1669 passed, 1 skipped, 1 warning (exit=0).
   - `LEAD_GUARD_R1.txt`: `RESULT: PASS`, working tree clean, dirty/staged entry count = 2.

5. **Review of Prior NITs 1–8**:
   - NITs 1–8 from the initial review are documentation/label polish items outside this commit's scope; none constitute a defect warranting elevation to REQUIRED.

---

### (c) Findings

No findings with severity REQUIRED or NIT exist within the repair commit.

---

### (d) Exact Read Coverage

All reads performed using built-in read capability within the packet directory (at most 150 lines per view; all continuations tracked):

1. `PACKET_SHA256SUMS.txt`: lines 1–16 (complete)
2. `subject/DIFF_9ef072a8_a871e429.patch`: lines 1–150; continuation lines 151–154 (complete)
3. `subject/DIFF_STAT_9ef072a8_a871e429.txt`: lines 1–4 (complete)
4. `subject/COMMIT_a871e429.txt`: lines 1–36 (complete)
5. `subject/export_mtc_funding_HEAD_lines_150-200_constants_limitations.py`: lines 1–52 (complete)
6. `subject/export_mtc_funding_HEAD_lines_1140-1290_real_fills_completion.py`: lines 1–150; continuation lines 151–152 (complete)
7. `subject/test_real_capture_HEAD_lines_1-120_fixtures.py`: lines 1–120; continuation line 121 (complete)
8. `subject/test_real_capture_HEAD_lines_195-275_helpers.py`: lines 1–82 (complete)
9. `subject/test_real_capture_HEAD_lines_890-975_new_tests.py`: lines 1–87 (complete)
10. `sources/OPUS_REPORT_attempt1_9ef072a8.md`: lines 255–336 (encompassing required lines 262–300 and 329–335)
11. `sources/LEAD_FULL_BRIDGE_SUITE_R1.txt`: lines 1–33 (complete)
12. `sources/LEAD_GUARD_R1.txt`: lines 1–17 (complete)
13. `sources/LEAD_PYTEST_GREEN_R1.txt`: lines 1–5 (complete)
14. `sources/LEAD_RED_lane8_R1_M1_no_fills_branch_returns_zero.txt`: lines 1–90 (complete)
15. `sources/LEAD_RED_lane8_R1_M2_position_source_relabelled.txt`: lines 1–119 (complete)
16. `sources/LEAD_RED_lane8_R1_M3_opening_position_always_none.txt`: lines 1–32 (complete)

---

### (e) NOT VERIFIED

1. **Live Execution & Environment**: As a supplemental read-only reviewer (`SUPPLEMENTAL_UNEXECUTED`), no commands were executed; all test counts, durations, and exit statuses in the Lead logs were verified from recorded text and code inspection.
2. **Repository & External Workspace**: Files outside `_gemini_packets_20260913/P012_INTAKE_R1_20260917` were not opened.
3. **Hyperliquid Venue & Oracle Validation**: Venue API response dynamics, timestamp behaviors under clock skew, and live oracle captures were not queried.
4. **Downstream Store Integration**: Schema v10 store compatibility and production admission remain unverified (production admission stands refused under `OD-20260914-P012-ADMISSION-Q3`).

---

```json
{
  "part": "P012_INTAKE_R1_GEMINI",
  "verdict": "PASS",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "required_1": "CLOSED",
  "no_fills_branch_reached": true,
  "mutants_killed": {
    "M1": true,
    "M2": true,
    "M3": true
  },
  "findings": [],
  "required_scope_unread": []
}
```

GEMINI_READ_ONLY_OK
