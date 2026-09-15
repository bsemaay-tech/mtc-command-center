# LEAD_VERIFICATION — WP-P0-12 funding intake adapter (non-accepting half), candidate `004a0711414bcf212d142b62a7d6121c70eff971` — 2026-09-15 15:24Z

**Authority:** `OD-20260915-BUILD-ABC-1` item (b) (owner "all"). **Scope decision, recorded before code:** `P012_FUNDING_INTAKE_DESIGN_20260915.md` — the export tool has no production mode to feed; the adapter builds the intake half only and invents nothing. **Result: built by the Lead (disclosed), green, committed on `feature/p012-funding-intake-adapter-20260915` from `origin/master` `fcac0ac6`, pushed; NOT reviewed, NOT accepted; not an input to any admission path.**

| Item | Fact |
|---|---|
| Files (2 added, 0 modified) | `IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py` (366 lines), `IBKR_PAPER_BRIDGE/tests/test_funding_intake_adapter.py` (212 lines). `export_mtc_funding.py`, the capture tool and every Bridge module untouched. |
| Inputs consumed | `CAPTURE_MANIFEST.json` (kind `P012_PATH1_OWN_ACCOUNT_CAPTURE_MANIFEST_V1`) + `DERIVED_EXTRACTION.json` (label `DERIVED_VIEW_NOT_ORIGINAL_BYTES`) of one capture run; strict JSON (duplicate keys and non-finite constants refused) |
| Outputs (write-once dir; sha256 sidecars; sorted keys; no clock) | `binding_packet_draft.json`, `retained_rows_expected.json`, `intake_gap_report.json` — all labelled `NONACCEPTING_INTAKE_DRAFT` |
| Fill rules | COPIED: venue stamp (`time` → `…Z` with ms), `fundingRate` → `raw_rate`, `usdc`/`szi` as `observed`, `capture_sha256` → `provenance.source_sha256`, `json_pointer` + capture file → `source_locator`; TOOL-RULE: `positive_rate_payer = "LONG"` (= `export_mtc_funding.APPROVED_PAYER`); DERIVED-LABELLED: `funding_event_id` under the proposed D-2 rule (`hl-funding:<short>:<coin>:<time_ms>`), the coverage witness under the proposed D-6 rule (hour-aligned window AND two byte-identical funding passes); UNRESOLVED: `source_event_digest`, `payload_digest` (D-1), `oracle_price` / `oracle_price_source` (D-4), evidence-kind admission (D-5) |
| Address handling | manifest address (public) → short form `0x1E26…AC49` only; the full address appears in no output (asserted by test and re-checked on the r1 run: 0 hits) |
| Tests (pinned Bridge 3.12; `--basetemp C:/bt_*`) | `7 passed` — `LEAD_PYTEST_focused.txt`: fills-only-what-bytes-supply; never-fabricated (the arithmetic oracle price `78758.x` must not appear); completeness rule arms; refusals (foreign coin, non-integer time, wrong kind, wrong manifest kind, duplicate JSON keys); determinism + write-once + clock-free; `main` end-to-end + exit 3 on an existing output dir |
| RED arm | mutant fills `oracle_price` by `usdc / (szi × rate)` → `2 failed, 5 passed` (`LEAD_RED_ARM_fabrication_fence.txt`) |
| Ruff / format / guard | `All checks passed!`; `ruff format` applied; repo guard `RESULT: PASS` (`LEAD_GUARD.txt`) |
| Real dry run (read-only on capture r1, 15:20Z) | `NONACCEPTING_INTAKE_DRAFT events=2 fills=5 complete=True export_tool_would_refuse=CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`; outputs + sha256 in `intake_r1/` (`LEAD_INTAKE_r1_stdout.txt`) |

## What it does not do
No production packet; no evidence kind the export tool accepts; no oracle price; no digest domain; no schema-v10 database (the tool never writes one, and manufacturing one from a capture would be the fabrication the tool forbids); no change to `export_mtc_funding.py`; no network; no key.

## Next
Gemini DETECTION review (`P012_INTAKE_GEMINI`, queued in the 15:26Z chain); exact Opus / Sol only if the owner wants this half reviewed as a candidate (it is documentary-adjacent engineering under P0-12; the P0-12 Lead lane decides D-1..D-6 first). The Lead never accepts its own code.

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).

## Slice 2 — 2026-09-15 16:52Z (`65c4bc40`, test-only)
Gemini detection attempt 1 on `004a0711` (voided by the CLI 503 after a complete PASS-WITH-NITS report; `P012_INTAKE_GEMINI/LEAD_ADJUDICATION.md`): NIT-01 = the determinism test's clock assertion exempted `binding_packet_draft.json` through a vacuous disjunction → tightened to "every `YYYY-MM-DDT` prefix in every output is the capture day `2026-09-14T`"; RED arm `LEAD_RED_ARM_nit01_wall_clock.txt` (wall-clock mutant: 1 failed / 6 passed; the old assertion would have passed it); GREEN 7 passed (`C:/bt_intake_nit1`); Ruff `LEAD_RUFF_nit01.txt` clean; guard `LEAD_GUARD_nit01.txt` PASS; pushed. NIT-02 (D-6 completeness rule: end-boundary latency, expected count) folded into the design note's D-6 row as owner options — no adapter change. Adapter bytes unchanged since `004a0711`.
