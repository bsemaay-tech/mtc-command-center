# W303D re-seal #13 in-repo bundle-copy refresh report

Date: 2026-09-03
Actor: Codex implementer lane
Status: **COPY AND COMMITS COMPLETE; CANONICAL GATE REFUSED**
Finding count: **2 root-cause findings covering 7 unexpected refusal records**.

The five contract-copy bytes were refreshed and committed exactly as authorized. The one canonical
gate reached the full comparison pipeline, but measured 8/10 probes `DETECTED` and returned nine
refusal records: the two predicted residual records plus seven unexpected records
(`W303D_GATE_RECEIPT.json:617-839`). This report does not claim package acceptance.

## Scope, routing, and preflight

The lane authorizes only the four named bundle copies, the regenerated anchor sidecar, this report,
and the gate receipt; it forbids every kernel, harness, golden, input, probe, and design edit
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303D_REFRESH_ALL_COPIES_SEAL13.md:10-22,33-38`). The active
write lane was branch `feature/wp-p0-12-corrected-vnext-20260831`, worktree `C:\WP012BUILD`, with
the seven exact output paths listed in this report and no tracked-file live or scheduled dependency.
The branch, both required external markers, and an empty `git status --porcelain=v1` were measured
before the first write, as the lane requires
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303D_REFRESH_ALL_COPIES_SEAL13.md:3-8`;
`C:\tmp\LANE_PROMPTS_20260828\W299B_DONE.txt:1`;
`C:\tmp\LANE_PROMPTS_20260828\RESEAL13_DONE.txt:1`).

Gate-1 classification is **T1**: these are non-economic verifier contract copies under the
owner-gated MTC path, with no economic, live, host, security, broker, deploy, or schema write. T1 is
the repository category for non-economic product code/scripts (`AGENTS.md:20-31,38-40`). C-1
requires this lane to work without any other assistant or model, so no independent acceptance audit
was invoked (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).

W300B finished before the gate with `exit=0` and reported 0 findings
(`C:\tmp\LANE_PROMPTS_20260828\W300B_DONE.txt:1`;
`C:\tmp\LANE_PROMPTS_20260828\W300B_BASELINE_REGEN_REPORT.md:3-9`). Its baseline manifest consumes
re-seal #13 `e4ffde6a420202d2c9f3872f99c5527c1af7e7b83341764ec874d774f8aaa531`, pins catalog
`bdfb42e7058df08cd57ea9c57434784e452676be16ea61be7324f2f866148742`, and records 17 completed / 0
blocked (`C:\tmp\P012_BASELINE_RUN\BASELINE_BYTES_MANIFEST.json:9-26`).

## Byte-for-byte copy evidence

`Get-FileHash -Algorithm SHA256` was run on each source and destination after the copy. The four
copied pairs are equal. The sidecar contains the new anchor digest as 64 lowercase hexadecimal
characters plus one LF (65 bytes), as required by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303D_REFRESH_ALL_COPIES_SEAL13.md:14-20`).

| In-repo file | Bundle source / generated SHA-256 | In-repo SHA-256 or value | Equal | Evidence |
|---|---|---|---|---|
| `CONTRACT_TABLES_MANIFEST.json` | `fdaaedf5693f7fd6487a1d2c3179e08b5d9d493034e2014a5b22c7023b08c632` | `fdaaedf5693f7fd6487a1d2c3179e08b5d9d493034e2014a5b22c7023b08c632` | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\CONTRACT_TABLES_MANIFEST.json:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json:1` |
| `scenario_catalog.json` | `bdfb42e7058df08cd57ea9c57434784e452676be16ea61be7324f2f866148742` | `bdfb42e7058df08cd57ea9c57434784e452676be16ea61be7324f2f866148742` | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\scenario_catalog.json:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json:1` |
| `DERIVATIONS.md` | `92e9a8fd3870b7ce9457ff8c67aac85bb39cbe2b33381f6a42f0e9f363795bf5` | `92e9a8fd3870b7ce9457ff8c67aac85bb39cbe2b33381f6a42f0e9f363795bf5` | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\DERIVATIONS.md:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md:1` |
| `implementation_anchor.json` | `0433a420ce446e7b0f629ce71de576a6460235497db141ec512d536fbf961852` | `0433a420ce446e7b0f629ce71de576a6460235497db141ec512d536fbf961852` | yes | `C:\tmp\P012_CONTRACT_TABLES_W127\IMPLEMENTATION_ANCHOR_DRAFT.json:1`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:1` |
| `implementation_anchor.json.sha256` | new anchor digest `0433a420ce446e7b0f629ce71de576a6460235497db141ec512d536fbf961852` | sidecar value `0433a420ce446e7b0f629ce71de576a6460235497db141ec512d536fbf961852` | yes | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:1-4`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1` |

The four staged Git blob OIDs also equalled `git hash-object --no-filters` over their corresponding
bundle sources; the staged sidecar blob equalled the working-file blob. This verifies that Git did
not alter the copied bytes.

Measured `git diff --stat` before the first commit:

```text
 .../contracts/CONTRACT_TABLES_MANIFEST.json        | 44 ++++++++++++++----
 .../tests/corrected_vnext/contracts/DERIVATIONS.md | 17 +++++++
 .../contracts/implementation_anchor.json           |  8 +++-
 .../contracts/implementation_anchor.json.sha256    |  2 +-
 .../contracts/scenario_catalog.json                | 54 +++++++++++-----------
 5 files changed, 88 insertions(+), 37 deletions(-)
```

`git diff --check`, `git diff --cached --check`, and the repository guard all returned success. The
five staged paths were exactly the five paths in the table. The prescribed implementation commit is
`a854ab4d4d444245aff533ad99f0f7d697ac3a11`, with subject
`chore(mtc-v2): refresh in-repo bundle copies to re-seal #13`, matching the lane instruction
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303D_REFRESH_ALL_COPIES_SEAL13.md:24-27`).

## Canonical gate — exactly one invocation

The only canonical-gate invocation was made from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON`:

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:\tmp\P012_BASELINE_RUN --output C:\WP012BUILD\W303D_GATE_RECEIPT.json
```

It returned exit `2`, wrote the requested receipt normally (no stdout fallback was needed), and the
receipt SHA-256 is
`338a330cee5ff2ec9ad47e77a21df7b6be76bbb0d03cf7e2db63cc9b709b9738`. The receipt declares
`full-gate`, reaches the comparison pipeline, and carries the refused claim label
(`W303D_GATE_RECEIPT.json:611-618,790-839`).

Seal, all 19 member digests/sizes, anchor seal, anchor sidecar, baseline seal/catalog, baseline
members, and baseline summary passed because the verifier reaches `validate_catalog` only after
all those checks return; any failure raises an early singular refusal
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1996-2063`).
The receipt records the resulting seal, catalog, and anchor identities exactly
(`W303D_GATE_RECEIPT.json:2033-2041`). All ten probe pins also passed: every probe has
`digest_status: PROBE_DIGEST_MATCH` (`W303D_GATE_RECEIPT.json:618-788`).

### Full refusal list

The following is the complete nine-record `refusals` array, preserving receipt order and values
(`W303D_GATE_RECEIPT.json:790-839`):

```json
1. {"check_id":"SEMANTIC_COVERAGE_REVIEW_MISSING","detail":"C:\\WP012BUILD\\MTC_COMMAND_CENTER\\01_MTC_PROJECT\\00_PYTHON\\mtc_v2\\tests\\corrected_vnext\\contracts\\semantic_coverage_review.json"}
2. {"check_id":"EXPECTED_PATH_CHANGED_AFTER_BASE","detail":"MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json","pointer":"MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json"}
3. {"check_id":"PROBE_NOT_DETECTED","comparator_first_differing_node":"/RESULT_SURFACE/admitted","measured_failed_check":"CLOSED_SET_VIOLATION","scenario_id":"PROBE-P012-02-A"}
4. {"check_id":"PROBE_NOT_DETECTED","comparator_first_differing_node":"/RESULT_SURFACE/cumulative_funding","measured_failed_check":"CLOSED_SET_VIOLATION","scenario_id":"PROBE-P012-08-A"}
5. {"check_id":"CLOSED_SET_VIOLATION","detail":"missing member cumulative_funding","pointer":"/RESULT_SURFACE/cumulative_funding","scenario_id":"RULE2-08-RED"}
6. {"check_id":"CLOSED_SET_VIOLATION","detail":"missing member cumulative_funding","pointer":"/RESULT_SURFACE/cumulative_funding","scenario_id":"RULE2-08-GREEN"}
7. {"check_id":"CORRECTED_EXPECTATION_MISMATCH","pointer":"/EVENT_SURFACE/cash_events","scenario_id":"RULE2-08-RED"}
8. {"check_id":"RULE2_PROJECTION_COULD_NOT_EVALUATE","detail":"KeyError: 'cumulative_funding'","scenario_id":"RULE2-08-RED"}
9. {"check_id":"CORRECTED_EXPECTATION_MISMATCH","pointer":"/EVENT_SURFACE/decision_events","scenario_id":"RULE2-08-GREEN"}
```

Records 1-2 are the predicted review and RULE2-01-GREEN provenance records. Records 3-9 are the
seven unexpected records and are accounted for in the two findings below.

## Probe table

All ten probe artifacts and pins were valid. Eight reached the declared failed check and are
`DETECTED`; two reached an earlier/different check and are `NOT_DETECTED`
(`W303D_GATE_RECEIPT.json:618-788`).

| Probe | Status | Digest status | Expected failed check | Measured failed check | First measured node |
|---|---|---|---|---|---|
| `PROBE-P012-01-A` | `DETECTED` | `PROBE_DIGEST_MATCH` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-01-B` | `DETECTED` | `PROBE_DIGEST_MATCH` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-02-A` | `NOT_DETECTED` | `PROBE_DIGEST_MATCH` | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | `CLOSED_SET_VIOLATION` | `/RESULT_SURFACE/admitted` |
| `PROBE-P012-03-A` | `DETECTED` | `PROBE_DIGEST_MATCH` | `RECORD_IDENTITY_PREFLIGHT` | `RECORD_IDENTITY_PREFLIGHT` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` |
| `PROBE-P012-04-A` | `DETECTED` | `PROBE_DIGEST_MATCH` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-05-A` | `DETECTED` | `PROBE_DIGEST_MATCH` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-05-B` | `DETECTED` | `PROBE_DIGEST_MATCH` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/fill_events/0/final_fill_price` |
| `PROBE-P012-06-A` | `DETECTED` | `PROBE_DIGEST_MATCH` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/0/signed_delta` |
| `PROBE-P012-07-A` | `DETECTED` | `PROBE_DIGEST_MATCH` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | `/EVENT_SURFACE/cash_events/1/signed_delta` |
| `PROBE-P012-08-A` | `NOT_DETECTED` | `PROBE_DIGEST_MATCH` | `CORRECTED_EXPECTATION` | `CLOSED_SET_VIOLATION` | `/RESULT_SURFACE/cumulative_funding` |

## Findings

### F-01 — PROBE-P012-02-A reaches an earlier closed-set check

The probe expected `RULE2_GREEN_CROSS_VERSION_EXPECTATION` at
`/RESULT_SURFACE/admitted`, but measured `CLOSED_SET_VIOLATION` at that same pointer
(`W303D_GATE_RECEIPT.json:653-668`). Both node values are: sealed expected = **PRESENT `true`**;
modified-copy observed = **ABSENT**. The sealed expected value is explicit in the golden
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-GREEN.json:38-46`).

The cause is deterministic. The modified copy changes the equality boundary from `<` to `<=`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-02-A/modification_manifest.json:1`).
At the sealed `100 == 100` boundary, the modified copy takes the refusal path rather than emitting
`MIN_NOTIONAL_ADMITTED`; the result producer emits `admitted: true` only when that decision exists
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/results.py:978-981`). The closed-set
validator requires `admitted` on RULE2-02-GREEN before the cross-version check runs
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:857-876,2664-2715`).

### F-02 — unresolved RULE2-08 lifecycle construction causes six unexpected records

The gate reconfirms W304's row-7 stop. Both sealed RULE2-08 inputs bind no cost schedule, while the
ordinary pre-window lifecycle construction needs one; the runner refuses that construction before
the funding event can be evaluated (`W304_PRODUCER_CONTRACT_REPORT.md:153-175`). A permitted
read-only diagnostic call to `execute_corrected_scenario` measured the same current surface for both
RULE2-08 rows: one `SEMANTICS_VALIDATED` decision, empty cash/funding arrays, absent
`cumulative_funding`, null final position, and an empty refusal array. No file was written by that
diagnostic. The gate's five scenario records and one dependent probe record are
`W303D_GATE_RECEIPT.json:806-837`.

The required pointer and both compared values for each unexpected record are:

| Receipt record | Pointer | Sealed/declared value | Measured current value |
|---|---|---|---|
| `PROBE-P012-08-A / PROBE_NOT_DETECTED` | expected first node `/EVENT_SURFACE/funding_events/0/funding_cash_delta`; measured first node `/RESULT_SURFACE/cumulative_funding` | failed check `CORRECTED_EXPECTATION`; funding delta `-0.1`; cumulative funding `-0.1` | failed check `CLOSED_SET_VIOLATION`; funding delta ABSENT; cumulative funding ABSENT |
| `RULE2-08-RED / CLOSED_SET_VIOLATION` | `/RESULT_SURFACE/cumulative_funding` | PRESENT `-0.1` | ABSENT |
| `RULE2-08-GREEN / CLOSED_SET_VIOLATION` | `/RESULT_SURFACE/cumulative_funding` | PRESENT `0` | ABSENT |
| `RULE2-08-RED / CORRECTED_EXPECTATION_MISMATCH` | `/EVENT_SURFACE/cash_events` | one FUNDING row with `signed_delta: -0.1` | `[]` |
| `RULE2-08-RED / RULE2_PROJECTION_COULD_NOT_EVALUATE` | `/RESULT_SURFACE/cumulative_funding` | PRESENT `-0.1` | ABSENT, producing `KeyError: 'cumulative_funding'` |
| `RULE2-08-GREEN / CORRECTED_EXPECTATION_MISMATCH` | `/EVENT_SURFACE/decision_events` | `[SEMANTICS_VALIDATED, FUNDING_ELIGIBILITY(eligible=false)]` | `[SEMANTICS_VALIDATED]` |

The sealed RED values are at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-RED.json:25-44`;
the sealed GREEN values are at
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-GREEN.json:23-38`.
The probe's declared check/node and the gate's measured check/node are both retained in the receipt
(`W303D_GATE_RECEIPT.json:772-787`).

## Discrepancies

1. **The prompt's shortened repository path does not exist at the worktree root.** The prompt names
   `mtc_v2/tests/corrected_vnext/contracts/`, while tracked repository discovery places the copies
   under `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/`.
   Repository paths were used under C-2
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303D_REFRESH_ALL_COPIES_SEAL13.md:10-20`;
   `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`;
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:7-12`).
2. **The 10/10 probe prediction is false.** The measured result is 8/10 `DETECTED` and 2/10
   `NOT_DETECTED`; all ten pins passed
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303D_REFRESH_ALL_COPIES_SEAL13.md:28-32`;
   `W303D_GATE_RECEIPT.json:618-788`). F-01 and F-02 give the pointer and both values for the two
   unexpected probe records.
3. **The predicted two-record residual list is conditional on W304 closing the producer contract,
   but W304 did not close row 7.** Its own report records the RULE2-08 stop and the lifecycle/cost
   conflict (`W304_PRODUCER_CONTRACT_REPORT.md:153-175`). The current receipt therefore has the two
   predicted records plus seven unexpected records (`W303D_GATE_RECEIPT.json:790-839`).
4. **Normal repository write-back/audit defaults conflict with this lane's tighter scope.** The
   governance stage normally requires a T1 independent audit and a `HANDOFF.md` update
   (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md:15-20,24-37`;
   `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/OUTPUTS.md:3-9`), while this lane permits only the named
   bytes and C-1 forbids other assistants
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303D_REFRESH_ALL_COPIES_SEAL13.md:10-22,33-38`;
   `C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7,25-31`). No `HANDOFF.md` byte was changed
   and no independent acceptance verdict is claimed.

## Verification and handoff

- The required implementation commit is `a854ab4d4d444245aff533ad99f0f7d697ac3a11`; it contains only
  the five contract-copy paths and the exact required subject.
- The canonical gate was invoked exactly once; its durable full receipt is
  `W303D_GATE_RECEIPT.json:1-2042`.
- The supplemental diagnostic executed only two current corrected scenarios to expose the exact
  compared values already identified by the gate. It did not write any artifact, rerun the gate,
  or change the finding set; local verifiers are permitted by C-6
  (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:33-36`).
- No kernel, harness, golden, input, probe, design, baseline, Pine, broker, host, network, or live
  byte was changed by W303D. No push, PR, merge, hook bypass, or destructive Git action was
  performed (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-36`).

Practical next action: owner/Lead resolution is still required for the sealed RULE2-08
lifecycle-versus-absent-cost-schedule conflict. Separately, the probe contract must decide whether
PROBE-P012-02-A should count the earlier `CLOSED_SET_VIOLATION` as detection or should be shaped to
reach its declared cross-version check. Those are outside this refresh lane
(`W304_PRODUCER_CONTRACT_REPORT.md:153-175`; `W303D_GATE_RECEIPT.json:653-668,772-787`).
