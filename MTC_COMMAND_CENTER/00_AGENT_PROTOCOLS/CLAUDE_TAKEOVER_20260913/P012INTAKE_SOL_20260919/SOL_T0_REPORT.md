# Independent T0 review — WP-P0-12 funding intake NIT slice

Reviewer: gpt-5.6-sol, xhigh. I did not read an Opus report or a Lead verification/adjudication before reaching this verdict.

## Verified identities

- Computed worktree HEAD: `8cbf4f1a7b04afb5b011eb9fb609fbd03089b7f3` (exact brief pin).
- Computed parent: `a871e42965322d4fc66e317ef7067d6fca28972c`.
- Commit stat: exactly four files, `+342/-36`:
  - `IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py`
  - `IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py`
  - `IBKR_PAPER_BRIDGE/tests/test_mtc_funding_export_real_capture.py`
  - `IBKR_PAPER_BRIDGE/tests/test_funding_intake_adapter.py`
- HEAD blob OIDs:
  - exporter: `1ba132ef0c471aba302d66390b78f18f354c4c25`
  - adapter: `214d8c4302167ec975a394df8d3ada3af21b6b0f`
  - real-capture tests: `fd57dd744148bdd0477c6d2a99a76f2262122ecf`
  - adapter tests: `20e0b3779f25f5d22a6256c0e43207ee617e55e3`
- Authority read directly at `C:/CT13/DECISIONS.md`: `OD-20260916-P012-INTAKE-D1-D6-R-1` and `OD-20260918-P012-D6START-B-1`. The latter says the capture-window start is exclusive: a payment at or just after the start belongs to the previous window.

## D-1 through D-6

| Rule | Owner rule and implementation | Independent failing input and observed outcome | Status |
|---|---|---|---|
| D-1 | SHA-256 over the exact captured funding-row bytes, tagged `HL_USERFUNDING_ROW_V1`; re-derived from `coverage.source_witnesses[event_id]` and the located span in the two funding-pass byte strings. | Replaced the digest with SHA-256 of a canonical JSON reserialization. Refused `CANDIDATE_BINDING_INVALID`: digest does not hash the exact captured row bytes. | VERIFIED |
| D-2 | `hl-funding:<account-short>:<coin>:<time_ms>`; re-derived from the captured row and witnessed account scope. | Used the floored-hour milliseconds instead of the captured `time_ms`, updating retained/inventory identities consistently. Refused `CANDIDATE_COVERAGE_INVALID`, naming the captured D-2 identity and the invented identity. | VERIFIED |
| D-3 | Venue timestamp verbatim plus its floored `interval_hour_utc`. | Rounded `17:00:00.041Z` to `17:00:00Z`. Refused `CANDIDATE_BINDING_INVALID`, explicitly naming D-3 and the verbatim expected stamp. | VERIFIED |
| D-4 | A payment-derived price is never admitted; the binding must name an oracle locator. | Set `oracle_price_source = "DERIVED_FROM_PAYMENT"`. Refused `CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE`. The tool checks locator shape/name only and does not open or authenticate the oracle capture. | DECLARED-NOT-CHECKED for the named capture; rejection fence VERIFIED |
| D-5 | The witness identity must name the ownership-signature record for the same scope. | Named an ownership record for another scope. Refused `CANDIDATE_COVERAGE_INVALID`, naming D-5 and both scopes. The tool validates the identity text but does not reopen the named manifest/signature record. | VERIFIED as a naming rule; record contents DECLARED-NOT-CHECKED |
| D-6 | Whole-hour window; two byte-identical funding passes; shifted one-second boundary band; all captured rows inventoried; fills/payment position drives the expected hour grid. | Supplied only one funding pass. Refused `CANDIDATE_COVERAGE_INVALID`: at least two passes required. Separate start/end boundary and pass/fills tests also passed as described below. | VERIFIED |

`ACCEPTED_EVIDENCE_KINDS` remains exactly `('SYNTHETIC_FIXTURE',)`. The real profile remains explicit through `evidence_kind=` / `--evidence-kind`; the packet cannot select it.

## Ten claimed closures

1. **D6-START B — behavior VERIFIED.** `_build()` computes `start_limit = (start.seconds + profile.end_tolerance_seconds, start.fraction)` and `end_limit` identically, then admits `start_limit <= stamp < end_limit`. The synthetic profile has tolerance zero. Reverting only `start_limit` to `start.sort_key` made exactly the two exclusion tests fail: `2 failed, 75 passed, 2 deselected`; restoring HEAD returned `77 passed, 2 deselected`. The exact `start+1.000s` test stayed accepting. Artifact descriptions are not fully closed; see NIT-1.

2. **NIT-1 — VERIFIED.** My packet used `coverage.evidence_kind = "SOL_UNKNOWN_PACKET_KIND"` while the caller explicitly admitted real capture. It refused `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE` and said only `'REAL_CAPTURE_READ_ONLY'` was accepted under that run; the message did not name the synthetic default.

3. **NIT-3 — report kind and schedule key VERIFIED; carried `production_mode` label remains stale.** A real candidate reports `REAL_CAPTURE_FUNDING_CANDIDATE_REPORT_V1` and `inputs.candidate_schedule_id`; it has no `synthetic_schedule_id`. The synthetic candidate and report were byte-identical to the parent: candidate SHA-256 `6ca9299ec0312259a4e6d7812d251ea82bc0b90a193f264f6fdceddea1923e28`, canonical report SHA-256 `504ea4dadb852906f7c7aecf8a0d433bc0192b3e164975edc10f4d92d161b0de`. See NIT-2 for the remaining real-report label.

4. **NIT-4 — VERIFIED.** The adapter D-1 decision text no longer conflates the source digest and Bridge payload digest. `D5_RESOLVED_NOTE` appears in both per-binding provenance and the gap report entry.

5. **NIT-7 — VERIFIED.** Every accepted real bound event reports settlement rate/time source `HL_USERFUNDING_ROW_V1_CAPTURED`; the synthetic output remains `SYNTHETIC_BINDING_ONLY` and is byte-identical to the parent.

6. **NIT-8 — VERIFIED.** Actual `--help` output contains both evidence profiles and no unconditional `SYNTHETIC_ONLY` claim.

7. **NIT-9 — VERIFIED.** In the event-building loop, the retained payload is integrity-checked against its own Bridge digest and carried as evidence, but no rate/size/payment value is compared with the captured venue row. The only cross-clock note is ledger `effective_ts` versus binding `event_timestamp`. The new limitation is truthful.

8. **NIT-A — implementation VERIFIED.** `_export_tool_outcome_today()` passes the draft coverage to `build_funding_candidate()` without `evidence_kind=`, so the default profile is synthetic. `_validate_coverage()` calls `_require_evidence_kind()` before the closed-shape and D-1..D-6 checks. The actual r1 draft deterministically reports `CANDIDATE_EVIDENCE_KIND_MISMATCH`, not a `KeyError`. The regression test does not prove the result is computed; see NIT-3.

9. **NIT-2/NIT-5 — partially VERIFIED.** The module/real-completion documentation accurately explains `[start+tolerance, end+tolerance)` and the D-4 substring check as a naming-convention guard, not cryptographic verification. Other public/output descriptions still state the old interval semantics; see NIT-1.

10. **Scope/collateral/honesty — VERIFIED.** Exactly four files changed. No `bridge/` runtime module changed. The only production import added is the adapter importing the existing exporter; no new dependency, environment read, network client, subprocess, credential path, database write, migration, or live-copy path was introduced. SQLite remains `mode=ro&immutable=1`. The adjustment to `test_d6_without_a_fill_for_the_symbol_the_position_source_is_the_payments` builds local `shifted_row1`, `shifted_id1`, bindings, passes, and rows; shared `ROW1`, `ID1`, and `FUNDING_PASS` remain unchanged.

## Boundary reproduction

- `[15:00, 18:00)` with the real-shaped `18:00:00.060Z` row: accepted as `REAL_CAPTURE_CANDIDATE_BUILT`.
- The same row shifted to `18:00:01.060Z`: refused `CANDIDATE_BINDING_OUT_OF_INTERVAL`.
- Start-side mutant (`start_limit = start.sort_key`): only `test_d6_start_tolerance_excludes_a_stamp_within_one_second_of_the_window_start` and `test_d6_start_tolerance_excludes_a_stamp_just_inside_the_boundary` turned RED.
- The implemented grid/band matches the two owner decisions: the end hour is part of the completeness grid, while event admission is the shifted half-open band.

## Real r1 dry run

Command subject: `C:/tmp/CLAUDE_P0_RUN_20260913/P012_PATH1_REAL_CAPTURE_20260915/r1`, output under `C:/tmp/SOL_P012INTAKE_SCRATCH/r1_nit_8cbf4f1a`.

- Adapter exit: `0`.
- Dynamic draft outcome: `CANDIDATE_EVIDENCE_KIND_MISMATCH`.
- Capture change count across recursive file SHA-256 values: `0`.
- Output digests:
  - `binding_packet_draft.json`: `d72ea7f72509f8c48e6a634d2f2769440704bc6d3925c71c68f3717f2d979544` (intentionally differs from the old record because D-5 text changed).
  - `retained_rows_expected.json`: `e8b0176520ce05c12dc4ef65429c1d555da50e9a6ab618ac31e9fc37f285f931` (matches old record).
  - `intake_gap_report.json`: `7d0ccef76000db99c4fba80611f2e549cc399e55491ceafa321aa7dadcb9fd98` (intentionally differs because the outcome is now computed and D-5 is resolved).
  - `binding_packet_real_capture.json`: `f3bde0b7a1b008739df927c119fd5a654836b40af9149b58ed6e241fcd0c979b` (matches old record).
- Exporter pure function on the emitted packet plus fixture retained rows:
  - real profile as emitted: refused `CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE`;
  - default profile: refused `CANDIDATE_EVIDENCE_KIND_MISMATCH`;
  - real profile with an independently named fixture oracle locator: accepted `REAL_CAPTURE_CANDIDATE_BUILT`, candidate SHA-256 `419ef74ad649f6ff32fb6fd0f48658e72cfa74bdc4f567bd633082b1eee8f1f4`.
- Accepted fixture-oracle root remains structurally non-consumable: no root `events`, `schedule_id`, or `settlement_currency`; `artifact_kind = REAL_CAPTURE_FUNDING_CANDIDATE_V1`, `synthetic_only = false`, and admission status `REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD`.
- Full address `0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49` appeared zero times in outputs. The only `0x` + 40-hex match was the zero-hash prefix.

## RED, mutants, and GREEN evidence

- Parent tools (`a871e429`) against the new/modified tests, excluding only the two CLI tests that require an external writable non-Git path: `8 failed, 69 passed, 2 deselected`. The eight failures were the intended unknown-kind message, real report labels, two start exclusions, real settlement source, help text, payload limitation, and adapter D-5/outcome test.
- Restored HEAD: `77 passed, 2 deselected`.
- Independent start-limit mutant: `2 failed, 75 passed, 2 deselected`; restored HEAD: `77 passed, 2 deselected`.
- A hardcoded-correct NIT-A mutant returned `CANDIDATE_EVIDENCE_KIND_MISMATCH` without calling the exporter; the adapter test still passed (`1 passed`). This is the evidence for NIT-3.
- Test-to-defect mapping:
  - unknown-kind test catches the stale synthetic-only refusal text;
  - real report test catches synthetic report/schedule labels;
  - three start-boundary tests catch no start shift, off-by-one inclusion, and off-by-one exclusion;
  - settlement-source test catches reuse of the synthetic source label;
  - help test catches the unconditional synthetic-only description;
  - limitation test catches omission of the retained-payload non-cross-check disclosure;
  - modified no-fill test preserves the earlier position-source branch after the new start band;
  - adapter test catches the visible D-5 labels and final outcome code, but can pass when the outcome is hardcoded instead of computed.

## Format-only proof

- `4c802e9b` exporter: Ruff format check says it would reformat.
- `b667dbcc` exporter: Ruff format check says already formatted.
- Parsed AST SHA-256 is identical for both blobs: `e9ee1777fe8b73fa9a781c40093195aed761df294f8861992a378cea7f701f60`. The diff is formatter reflow only.

## Tests and static checks

- Mandatory focused set: the sandbox cannot create or clean `C:/bt_opus_intake_nit` (`PermissionError`). Under the authorized scratch Git root, `205 passed, 1 skipped`; the remaining 35 were all `CANDIDATE_STAGING_UNSAFE` because every writable sandbox root has a `.git` ancestor. No product assertion outside that path policy failed.
- Full Bridge suite: `1672 passed, 1 skipped, 35 failed` in 165.85 s. All 35 failures are the same externally staged CLI tests blocked by the sandbox Git ancestry. The totals account for the brief's expected 1707 tests exactly; there was no unrelated failure.
- Ruff 0.16.8 could not be installed because network access is denied and the managed uv cache/tool directories are ACL-blocked. Installed Ruff 0.16.4 reported exactly the five known exporter findings: UP035, 3× ISC004, SIM101, with no new finding in the adapter. The two expected test-file I001 findings are version-specific and were not reproduced by 0.16.4.

## Findings

### REQUIRED

None.

### NIT-1 — shifted-start semantics are not consistently represented in public/output metadata

Behavior is correct, but `tools/export_mtc_funding.py:1491-1493` still documents the pure function as admitting `[start_inclusive, end_exclusive)`. The accepted real candidate at `tools/export_mtc_funding.py:1744-1749` emits `effective_interval.start_inclusive` and only `end_tolerance_seconds`, although the effective real admission band is `[start+1s, end+1s)`. The adapter gap report at `tools/funding_intake_adapter.py:563-566` likewise says only “1-second end tolerance.” My accepted r1 fixture emitted exactly `{'start_inclusive': '2026-09-14T15:00:00Z', 'end_exclusive': '2026-09-14T19:00:00Z', 'end_tolerance_seconds': 1}`. Add a real-profile admission-band description (or both boundary tolerances) and update the adapter sentence; synthetic keys/bytes can remain unchanged.

### NIT-2 — the real report still says its source-event digest domain is pending

`tools/export_mtc_funding.py:1844` emits the synthetic-era `PRODUCTION_MODE_UNAVAILABLE` value for both profiles. On an accepted real candidate it is `UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN`, even though D-1's real domain is now implemented and verified. Non-production status is truthful elsewhere, so this does not weaken admission; it is the remaining stale `production_mode` portion of the carried synthetic-label nit.

### NIT-3 — NIT-A's test does not prove the adapter computes the exporter outcome

The implementation at `tools/funding_intake_adapter.py:396-411` correctly calls the exporter, but `tests/test_funding_intake_adapter.py:137-139` asserts only the resulting code. A mutant that hardcoded the now-correct `CANDIDATE_EVIDENCE_KIND_MISMATCH` and never called `build_funding_candidate()` passed the test. Monkeypatch the exporter entry point to return a sentinel refusal and assert the sentinel reaches the gap report (or assert the call arguments).

## NOT VERIFIED

- Exact green `240 passed, 1 skipped` and full `1707 passed, 1 skipped` under the brief's external `C:/bt_opus_intake_nit` paths: the managed sandbox denies those writes. All tests were accounted for, but 35 external-staging cases could not reach their intended bodies.
- Exact Ruff 0.16.8 seven-finding transcript: the pinned version was unavailable offline. Ruff 0.16.4 reproduced the five production-file baseline findings.
- The named oracle and ownership-signature records themselves: the tool intentionally validates their locators/identity strings without reopening those artifacts.

VERDICT: PASS-WITH-NITS
