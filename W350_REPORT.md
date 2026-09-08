# W350 re-anchor follow-up report

## Verdict

W350 completed the authorized re-anchor copy and provenance re-measurement. The one canonical gate run refused with the two remaining records shown verbatim below; `EXPECTED_PATH_CHANGED_AFTER_BASE` is absent, and expected-source provenance reports `MATCH` with zero changed paths (`W350_GATE_RECEIPT.json:124-134`, `W350_GATE_RECEIPT.json:657-668`). Findings outside the lane prediction: **0** (`C:\tmp\LANE_PROMPTS_20260828\LANE_W350_REANCHOR_FOLLOWUP.md:19-21`).

## Scope and lane record

- Branch: `feature/wp-p0-12-corrected-vnext-20260831`; worktree: `C:\WP012BUILD`.
- Pre-edit HEAD: `7333263a2351be1aa9464a61406ffcd3be46a2f2`; the worktree was clean and was not on `master`. These are the mandatory stop conditions (`C:\tmp\LANE_PROMPTS_20260828\LANE_W350_REANCHOR_FOLLOWUP.md:3-7`).
- The Lead record existed and named `63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5` as the new base (`C:\tmp\LANE_PROMPTS_20260828\REPIN16_DONE.txt:1`).
- Allowed in-repo paths: the manifest, anchor, anchor sidecar, provenance record, receipt, and this report (`C:\tmp\LANE_PROMPTS_20260828\LANE_W350_REANCHOR_FOLLOWUP.md:6-7`).
- Audit tier: T1, because these machine-read verifier contracts affect gate behavior but do not change economic/runtime code. No external model or CLI was dispatched because C-1 requires this lane to be performed in this session (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).
- Live/scheduled dependency status: **NOT VERIFIED**. No broker, venue, host, network, backtest, optimization, server, or launcher action was part of the authorized lane (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:33-36`).

Precondition transcript:

```text
REPIN16_DONE=exists
HEAD_FULL:
7333263a2351be1aa9464a61406ffcd3be46a2f2
HEAD_SHORT:
7333263a
BRANCH:
feature/wp-p0-12-corrected-vnext-20260831
STATUS_PORCELAIN:
<empty>
```

## Bundle copies and SHA-256 pairs

The in-repo manifest now carries the re-anchored SHA in both `seal_state` and `seal`, plus the Lead re-anchor history entry (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:565-578`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:959-965`). The in-repo anchor carries the same base, the measured core-tree OID, and the Lead history entry (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:4-6`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:137-144`).

```text
source=cac3e4e89eeac4aab2eabb50ccb2d6337ea013f9d3a0ce79e3b8f352e137be43 C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json
target=cac3e4e89eeac4aab2eabb50ccb2d6337ea013f9d3a0ce79e3b8f352e137be43 C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\tests\corrected_vnext\contracts\CONTRACT_TABLES_MANIFEST.json
equal=True
source=22b2f91397e34d84d79670c3ca60a3f6a02d8fde5770814a94fab54f6954ae19 C:\tmp\P012_CONTRACT_TABLES_W127\IMPLEMENTATION_ANCHOR_DRAFT.json
target=22b2f91397e34d84d79670c3ca60a3f6a02d8fde5770814a94fab54f6954ae19 C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\tests\corrected_vnext\contracts\implementation_anchor.json
equal=True
sidecar=22b2f91397e34d84d79670c3ca60a3f6a02d8fde5770814a94fab54f6954ae19
sidecar_equal=True
```

The sidecar pins the measured anchor hash (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`).

## Decision-134 provenance record re-measurement

Member path:
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:16`).

| Field | Before | After |
|---|---|---|
| `implementation_base_sha` | `5e8e579410ee55008bfd2d2d85054fd1d782f32c` | `63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5` |
| `base_state` | `PRESENT_AT_BASE` | `PRESENT_AT_BASE` |
| `base_blob_oid` | `b811ce9d9d4efe574828c6d3fc2703bea71b71a8` | `0ad42dafc7c6634319afddc9ff12a43d095438ae` |
| `current_blob_oid` | `f7b72d452e1d2abed58a97e541ee156d3e5821c2` | `0ad42dafc7c6634319afddc9ff12a43d095438ae` |
| `lane_ids` | `W156`, `W167`, `W172`, `W316D` | previous values plus `W350` |
| `reason` | W316D sentence ended the record | one W350 re-measurement sentence appended |

The before values were read with `git show HEAD:<path>` at lines 5-19 of the committed JSON. The after values, lane ID, and appended sentence are at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:5-20`.

Required Git measurements and literal output:

```text
git rev-parse --verify --quiet 63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json
0ad42dafc7c6634319afddc9ff12a43d095438ae
BASE_RC=0

git rev-parse HEAD:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json
0ad42dafc7c6634319afddc9ff12a43d095438ae
CURRENT_RC=0
```

The loader enforces exact top-level/member key sets and validates the base SHA, state, blob OIDs, non-empty lane IDs, integer owner decision, and non-empty reason (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1932-1949`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1978-2047`). Direct invocation returned:

```text
closed_schema_records=1
closed_schema_path=MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json
```

## Canonical gate

The lane authorized exactly one canonical full-gate invocation and fixed its output path (`C:\tmp\LANE_PROMPTS_20260828\LANE_W350_REANCHOR_FOLLOWUP.md:19-21`). It was invoked once:

```text
cd C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W350_GATE_RECEIPT.json
exit=1
```

The receipt reports the re-anchored base, zero changed expected paths, and provenance `MATCH` (`W350_GATE_RECEIPT.json:124-134`). Its SHA-256 is `39c466309205fd05facbae7aa2bfd2cea55f9907f25e70722eeda92a0870b9d5` (measured with `Get-FileHash -Algorithm SHA256`).

### Refusal list, verbatim

```json
"refusals": [
  {
    "check_id": "SEMANTIC_COVERAGE_REVIEW_MISSING",
    "detail": "C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"
  },
  {
    "check_id": "PROBE_NOT_DETECTED",
    "comparator_first_differing_node": "/RESULT_SURFACE/admitted",
    "measured_failed_check": "CLOSED_SET_VIOLATION",
    "scenario_id": "PROBE-P012-02-A"
  }
]
```

This is the receipt's complete two-item list (`W350_GATE_RECEIPT.json:657-668`).

## Probe table

| Probe | Status | Expected failed check | Measured failed check | Expected first changed node | Comparator first differing node |
|---|---|---|---|---|---|
| PROBE-P012-01-A | DETECTED | CORRECTED_EXPECTATION | CORRECTED_EXPECTATION | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| PROBE-P012-01-B | DETECTED | CORRECTED_EXPECTATION | CORRECTED_EXPECTATION | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| PROBE-P012-02-A | NOT DETECTED | CORRECTED_EXPECTATION | CLOSED_SET_VIOLATION | `/RESULT_SURFACE/admitted` | `/RESULT_SURFACE/admitted` |
| PROBE-P012-03-A | DETECTED | RECORD_IDENTITY_PREFLIGHT | RECORD_IDENTITY_PREFLIGHT | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | same |
| PROBE-P012-04-A | DETECTED | CORRECTED_EXPECTATION | CORRECTED_EXPECTATION | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| PROBE-P012-05-A | DETECTED | CORRECTED_EXPECTATION | CORRECTED_EXPECTATION | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| PROBE-P012-05-B | DETECTED | CORRECTED_EXPECTATION | CORRECTED_EXPECTATION | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/fill_events/0/final_fill_price` |
| PROBE-P012-06-A | DETECTED | CORRECTED_EXPECTATION | CORRECTED_EXPECTATION | `/EVENT_SURFACE/fill_events/0/exit_id` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| PROBE-P012-07-A | DETECTED | CORRECTED_EXPECTATION | CORRECTED_EXPECTATION | `/EVENT_SURFACE/fee_events/1/liquidity_role` | `/EVENT_SURFACE/cash_events/1/signed_delta` |
| PROBE-P012-08-A | DETECTED | CORRECTED_EXPECTATION | CORRECTED_EXPECTATION | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | `/EVENT_SURFACE/cash_events/0/signed_delta` |

The receipt supplies all ten rows: two 01 probes (`W350_GATE_RECEIPT.json:485-519`), 02 and 03 (`W350_GATE_RECEIPT.json:520-553`), 04 and both 05 probes (`W350_GATE_RECEIPT.json:554-604`), and 06 through 08 (`W350_GATE_RECEIPT.json:605-655`). Measured totals: **9 DETECTED**, **1 NOT DETECTED**.

## Regression risk

The manifest and anchor are exact Lead-bundle copies, but the provenance exception is now unused because the expected path is identical at the base and current build (`W350_GATE_RECEIPT.json:124-133`). A later edit to that golden remains subject to the verifier's exact blob-identity checks (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/expected_provenance_exceptions.json:20-23`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2034-2047`).

## QA and repository guard

- Bundle byte equality: manifest `True`; anchor `True` (SHA-256 transcript above).
- Anchor sidecar equality: `True` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`).
- Closed-schema loader: one accepted record (loader contract at `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1932-2047`).
- `git diff --check`: no output.
- `MTC_COMMAND_CENTER/tools/repo_guard.ps1`: `RESULT: PASS`; it measured six intended dirty entries, no protected match, no risky untracked file, and `PINE_ALERT_GUARD PASS files=21 matches=0 allowlist=0`.
- Parity/Pine/MTC strategy impact: no behavior file changed; the lane whitelist is limited to verifier contracts and evidence (`C:\tmp\LANE_PROMPTS_20260828\LANE_W350_REANCHOR_FOLLOWUP.md:6-7`).

Guard-format close-out:

```text
branch:            feature/wp-p0-12-corrected-vnext-20260831
files changed:     contracts/CONTRACT_TABLES_MANIFEST.json; contracts/implementation_anchor.json; contracts/implementation_anchor.json.sha256; contracts/expected_provenance_exceptions.json; W350_GATE_RECEIPT.json; W350_REPORT.md
checks run:        SHA-256 pair comparison; load_expected_provenance_exceptions; canonical full-gate once; git diff --check; repo_guard.ps1
guard:             PASS
commit:            this report is included in the lane's single commit; final SHA is measured after commit
pushed:            no
remaining dirty:   measured after commit
next action:       Lead inspects the committed W350 receipt and report; no merge, push, or live action is authorized
```

## Discrepancies

None. The actual refusal list contains the review-missing record and the predicted 02-A refusal, with no additional refusal (`C:\tmp\LANE_PROMPTS_20260828\LANE_W350_REANCHOR_FOLLOWUP.md:19-21`, `W350_GATE_RECEIPT.json:657-668`).

## Findings

**0.** No refusal outside the lane prediction was measured (`C:\tmp\LANE_PROMPTS_20260828\LANE_W350_REANCHOR_FOLLOWUP.md:19-21`, `W350_GATE_RECEIPT.json:657-668`).
