# W303C Refresh Anchor Report

## Verdict

**FINDING.** The mechanical anchor refresh is complete at implementation commit
`f19572bc28d7abf9905f6f59388dae268fc78782`. The refreshed anchor and source bundle copy have the
same measured SHA-256, and the one-line sidecar records that digest. The canonical gate passed the
anchor/seal identity boundary and persisted seal `83bbe48c51d0acf78b47c7f5891d78a8b6e1a5dabb98c92673dda224a4597fb2`,
but it refused with 42 records. Only one of ten probes was `DETECTED`; nine were
`COULD_NOT_EVALUATE` with inner refusal `PROBE_KERNEL_DIFF_INVALID`
(`W303C_GATE_RECEIPT.json:739,818-916,918-1167,2157-2164`).

One shared new finding, **W303C-F01**, covers those nine kernel probes. The other 33 refusal records
are the review record, the RULE2-01-GREEN provenance record, and the KERNEL/producer plus
RULE2-06/RULE2-08 harness outcomes already classified in the W284R residual table
(`W284R_VALIDATOR_REPAIR_REPORT.md:334-369,395-419`).

## Scope and preflight

- Worktree: `C:\WP012BUILD`; branch: `feature/wp-p0-12-corrected-vnext-20260831`. The lane requires
  that exact worktree/branch, a clean start, and the W303B completion marker
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:3-7`); the marker reads
  `exit=0` (`C:\tmp\LANE_PROMPTS_20260828\W303B_DONE.txt:1`).
- Audit tier: **T2**, because the changed repository artifacts are contract/evidence bytes, not
  economic behavior or an executable kernel. The repository defines T2 as docs/evidence
  (`AGENTS.md:38-40`; `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md:24-33`).
- Authorized implementation paths are the tracked in-repository anchor and sidecar; the mandated
  evidence paths are `W303C_GATE_RECEIPT.json` and this report
  (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:15-23,35-40`).
- No kernel, harness, golden, catalog, manifest, input, probe, or design byte is authorized by this
  lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:21-23`).
- Live dependency: **NOT VERIFIED independently**. The checked write-lane mirror records no tracked
  live/scheduled dependency for this branch/worktree at its prior released claim
  (`MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:37`). No broker, venue, host, network, Pine,
  backtest, optimization, or launcher action was performed; the common clause allows local tests
  and verifiers (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:33-36`).
- Preflight repository guard: `RESULT: PASS`; it measured a clean worktree, no staged paths, branch
  merge-base one commit behind local `origin/master`, and no risky untracked file. This was a local,
  no-fetch check, as the guard defines (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md:24-32,47-50`).

## SHA table

The SHA values and byte counts below were measured with `Get-FileHash -Algorithm SHA256` and
`Get-Item.Length`; both anchor JSON files were also parsed successfully. The source and destination
contain the same schema and seal at line 2 and line 4 respectively
(`C:\tmp\P012_CONTRACT_TABLES_W127\IMPLEMENTATION_ANCHOR_DRAFT.json:2-4`;
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json:2-4`).

| Artifact | Bytes | Measured SHA-256 / recorded value |
|---|---:|---|
| Source `C:\tmp\P012_CONTRACT_TABLES_W127\IMPLEMENTATION_ANCHOR_DRAFT.json` | 7,592 | `dd7ce17ef32bdc03cafffbc8df97ab20d74f60cc6277c7094cb60732c300b9dd` |
| Destination `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json` | 7,592 | `dd7ce17ef32bdc03cafffbc8df97ab20d74f60cc6277c7094cb60732c300b9dd` |
| Sidecar (64 lowercase hex bytes plus LF; 65 bytes total) | 65 | `dd7ce17ef32bdc03cafffbc8df97ab20d74f60cc6277c7094cb60732c300b9dd` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/implementation_anchor.json.sha256:1`) |

Measured equality: `source_sha256 == destination_sha256` and `source_bytes == destination_bytes`.
The verifier hashes exact file bytes and compares the sidecar to that digest
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:186-187,2000-2006`).

## Implementation diff and commit

`git diff --stat` before staging reported exactly the two implementation files required by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:25-28`):

```text
 .../corrected_vnext/contracts/implementation_anchor.json | 16 ++++++++++++++--
 .../contracts/implementation_anchor.json.sha256          |  2 +-
 2 files changed, 15 insertions(+), 3 deletions(-)
```

`git diff --check` and `git diff --cached --check` both returned 0. The cached name list contained
only those two paths. The pre-commit repository guard returned `RESULT: PASS`; the normal commit
hooks were not bypassed, consistent with repository rules
(`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/TESTS.md:21-22`;
`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md:10-19`).

Implementation commit:

```text
f19572bc28d7abf9905f6f59388dae268fc78782
chore(mtc-v2): refresh in-repo implementation anchor to re-seal #12
APPROVED-PATCH-PLAN: W303C
```

The trailer follows the protected-path modification gate
(`MTC_COMMAND_CENTER/09_DOCS/PROTECTED_PATHS_POLICY.md:15-24`).

## Canonical gate

Exactly one canonical invocation was run from
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON` as required by the lane
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:29-36`):

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate \
  --baseline-root C:\tmp\P012_BASELINE_RUN \
  --output C:\WP012BUILD\W303C_GATE_RECEIPT.json
```

Measured process exit: `2`. The verifier defines exit 2 for a refusing full-gate receipt and writes
the receipt to `--output` before returning (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3545-3561`).

Receipt measurements:

| Field | Measured value | Evidence |
|---|---:|---|
| SHA-256 | `f0326c30b005fa890ef94a6a7400b6a56cab30f2e8b3e03ed50021831736da58` | exact persisted bytes |
| Bytes | 79,581 | exact persisted bytes |
| Lines | 2,166 | exact persisted text |
| Claim label | `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED` | `W303C_GATE_RECEIPT.json:739` |
| Acceptance reachable | `true` | `W303C_GATE_RECEIPT.json:248` |
| Refusal records | 42 | exact array at `W303C_GATE_RECEIPT.json:918-1167` |
| Acceptance blockers | 41 | exact array at `W303C_GATE_RECEIPT.json:2-246` |
| Probes | 10 | exact array at `W303C_GATE_RECEIPT.json:818-916` |

The anchor refusal cleared: neither `IMPLEMENTATION_ANCHOR_SEAL_MISMATCH` nor
`IMPLEMENTATION_ANCHOR_DIGEST_MISMATCH` appears in the emitted refusal list, while the persisted
identity block records the expected seal and refreshed anchor digest
(`W303C_GATE_RECEIPT.json:918-1167,2157-2164`). Because sealed-producer validation raises before
baseline/scenario/probe evaluation, reaching the ten-probe and 17-scenario arrays is also evidence
that the seal/member boundary did not refuse; this is an inference from verifier order
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1988-2008`;
`W303C_GATE_RECEIPT.json:818-916,1168-2155`).

## Full refusal list

This is the complete emitted order from `W303C_GATE_RECEIPT.json:918-1167`.

1. `SEMANTIC_COVERAGE_REVIEW_MISSING` — `C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\tests\corrected_vnext\contracts\semantic_coverage_review.json`.
2. `EXPECTED_PATH_CHANGED_AFTER_BASE` — pointer and detail `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-GREEN.json`.
3. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-01-A; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
4. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-01-B; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
5. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-02-A; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
6. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-04-A; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
7. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-05-A; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
8. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-05-B; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
9. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-06-A; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
10. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-07-A; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
11. `PROBE_COULD_NOT_EVALUATE / PROBE_KERNEL_DIFF_INVALID` — PROBE-P012-08-A; changed `['config.py', 'confirmation.py', 'economics.py', 'exits.py', 'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py', 'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']`.
12. `CLOSED_SET_VIOLATION` — RULE2-01-RED `/RESULT_SURFACE/order_notional`; `missing member order_notional`.
13. `CLOSED_SET_VIOLATION` — RULE2-01-GREEN `/RESULT_SURFACE/order_notional`; `missing member order_notional`.
14. `CLOSED_SET_VIOLATION` — RULE2-02-RED `/RESULT_SURFACE/order_notional`; `missing member order_notional`.
15. `CLOSED_SET_VIOLATION` — RULE2-02-GREEN `/RESULT_SURFACE/admitted`; `missing member admitted`.
16. `CLOSED_SET_VIOLATION` — RULE2-04-RED `/EVENT_SURFACE/exit_events/0/reason`; `unknown reason 'STOP'`.
17. `CLOSED_SET_VIOLATION` — RULE2-05-RED `/RESULT_SURFACE/order_notional`; `missing member order_notional`.
18. `CLOSED_SET_VIOLATION` — RULE2-05-GREEN `/RESULT_SURFACE/order_notional`; `missing member order_notional`.
19. `CLOSED_SET_VIOLATION` — RULE2-06-GREEN `/EVENT_SURFACE/exit_events/0/reason`; `unknown reason 'STOP'`.
20. `CLOSED_SET_VIOLATION` — RULE2-07-RED `/EVENT_SURFACE/exit_events/0/reason`; `unknown reason 'MARKET_EXIT'`.
21. `CLOSED_SET_VIOLATION` — RULE2-07-GREEN `/RESULT_SURFACE/guards`; `missing member guards`.
22. `CLOSED_SET_VIOLATION` — RULE2-08-RED `/RESULT_SURFACE/cumulative_funding`; `missing member cumulative_funding`.
23. `CLOSED_SET_VIOLATION` — RULE2-08-GREEN `/RESULT_SURFACE/cumulative_funding`; `missing member cumulative_funding`.
24. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-01-RED `/RESULT_SURFACE/order_notional`.
25. `RULE2_PROJECTION_COULD_NOT_EVALUATE` — RULE2-01-RED; `KeyError: 'order_notional'`.
26. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-01-GREEN `/RESULT_SURFACE/order_notional`.
27. `RULE2_PROJECTION_COULD_NOT_EVALUATE` — RULE2-01-GREEN; `KeyError: 'order_notional'`.
28. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-02-RED `/RESULT_SURFACE/order_notional`.
29. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-02-GREEN `/RESULT_SURFACE/admitted`.
30. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-04-RED `/EVENT_SURFACE/exit_events/0/reason`.
31. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-05-RED `/RESULT_SURFACE/order_notional`.
32. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-05-GREEN `/RESULT_SURFACE/order_notional`.
33. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-06-RED `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id`.
34. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-06-EQUAL-PRICE-RED `/RESULT_SURFACE/run_manifest/same_bar_collision_policy_id`.
35. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-06-GREEN `/EVENT_SURFACE/exit_events/0/reason`.
36. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-07-RED `/EVENT_SURFACE/exit_events/0/reason`.
37. `RULE2_PROJECTION_COULD_NOT_EVALUATE` — RULE2-07-RED; `KeyError: 'guards'`.
38. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-07-GREEN `/RESULT_SURFACE/guards`.
39. `RULE2_PROJECTION_COULD_NOT_EVALUATE` — RULE2-07-GREEN; `KeyError: 'guards'`.
40. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-08-RED `/EVENT_SURFACE/cash_events`.
41. `RULE2_PROJECTION_COULD_NOT_EVALUATE` — RULE2-08-RED; `KeyError: 'cumulative_funding'`.
42. `CORRECTED_EXPECTATION_MISMATCH` — RULE2-08-GREEN `/EVENT_SURFACE/decision_events`.

Records 1-11 are at `W303C_GATE_RECEIPT.json:918-999`; records 12-23 are at
`W303C_GATE_RECEIPT.json:1001-1071`; records 24-42 are at `W303C_GATE_RECEIPT.json:1073-1167`.

## Probe table

| Probe | Status | Digest status | Measured failed check / inner refusal | Evidence |
|---|---|---|---|---|
| PROBE-P012-01-A | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:819-827` |
| PROBE-P012-01-B | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:828-836` |
| PROBE-P012-02-A | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:837-845` |
| PROBE-P012-03-A | `DETECTED` | `PROBE_DIGEST_MATCH` | `RECORD_IDENTITY_PREFLIGHT` | `W303C_GATE_RECEIPT.json:846-862` |
| PROBE-P012-04-A | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:863-871` |
| PROBE-P012-05-A | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:872-880` |
| PROBE-P012-05-B | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:881-889` |
| PROBE-P012-06-A | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:890-898` |
| PROBE-P012-07-A | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:899-907` |
| PROBE-P012-08-A | `COULD_NOT_EVALUATE` | `PROBE_ARTIFACT_INVALID` | `PROBE_KERNEL_DIFF_INVALID` | `W303C_GATE_RECEIPT.json:908-916` |

Measured outcome: **1/10 DETECTED; 9/10 COULD_NOT_EVALUATE**
(`W303C_GATE_RECEIPT.json:818-916`).

## Findings

### W303C-F01 — Nine kernel modified copies differ from their sealed base in 15 files, not one

For a KERNEL probe, the verifier computes every member digest against the sealed base tree and
requires the measured changed-file list to equal the one declared `modifications[0].file`; otherwise
it refuses `PROBE_KERNEL_DIFF_INVALID`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2339-2359,2373-2382`).

All nine affected manifests declare this value at JSON pointer `/modifications/0/file`:

```text
declared/expected changed-file list = ['economics.py']
```

The gate measured this value for every affected modified copy:

```text
actual changed-file list = ['config.py', 'confirmation.py', 'economics.py', 'exits.py',
  'gates.py', 'htf.py', 'indicators.py', 'instrument.py', 'ma.py', 'position_manager.py',
  'position_sizer.py', 'results.py', 'rounding.py', 'runner.py', 'types.py']
```

The declared value is present in each affected manifest at line 1:

| Probe | Declared pointer and evidence | Actual evidence |
|---|---|---|
| PROBE-P012-01-A | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-A/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:819-827` |
| PROBE-P012-01-B | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-01-B/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:828-836` |
| PROBE-P012-02-A | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-02-A/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:837-845` |
| PROBE-P012-04-A | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-04-A/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:863-871` |
| PROBE-P012-05-A | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-A/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:872-880` |
| PROBE-P012-05-B | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-05-B/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:881-889` |
| PROBE-P012-06-A | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-06-A/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:890-898` |
| PROBE-P012-07-A | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-07-A/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:899-907` |
| PROBE-P012-08-A | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/probes/PROBE-P012-08-A/modification_manifest.json:1` | `W303C_GATE_RECEIPT.json:908-916` |

This is one shared package-shape finding across nine probes, not nine independent root causes. The
scope forbids changing probe or kernel bytes, so it is reported without repair
(`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:15-23`).

## Discrepancies

1. **The prompt's short target path does not exist from the named worktree root.** The lane names
   `mtc_v2/tests/corrected_vnext/contracts/...`
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:15-22`), while `git ls-files`
   identifies the tracked files under
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/...`. The source
   anchor itself lists that full repository prefix for the contract evidence surface
   (`C:\tmp\P012_CONTRACT_TABLES_W127\IMPLEMENTATION_ANCHOR_DRAFT.json:23-28`). The repository path
   was used, as C-2 requires (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:9-13`).
2. **The 10/10 probe prediction is false.** The prompt predicts ten `DETECTED` outcomes
   (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:29-34`); the receipt records one
   `DETECTED` and nine `COULD_NOT_EVALUATE` outcomes (`W303C_GATE_RECEIPT.json:818-916`). The pointer
   and both compared values for the newly exposed mismatch are recorded in W303C-F01.
3. **The total refusal composition therefore has nine records beyond the predicted residual set.**
   W284R classifies 24 KERNEL/producer records, seven RULE2-06/RULE2-08 harness records, one review
   record, and one RULE2-01-GREEN provenance record (`W284R_VALIDATOR_REPAIR_REPORT.md:334-369,
   395-419`). Those 33 remain, but the current receipt additionally carries nine
   `PROBE_KERNEL_DIFF_INVALID` records (`W303C_GATE_RECEIPT.json:918-999`).
4. **Repository write-back and model-audit defaults cannot be completed inside this lane.** The
   governance stage normally requires current state in `HANDOFF.md` and a T2 model audit
   (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md:15-20,24-37`), but the lane/common clauses permit
   only named paths and explicitly forbid invoking any other assistant
   (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7,25-31`;
   `C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:15-23,35-40`). No `HANDOFF.md`
   update or independent acceptance claim is made.

## Verification and handoff

Commands executed for this lane:

```text
MTC_COMMAND_CENTER\tools\repo_guard.ps1                         # preflight: PASS
Get-FileHash -Algorithm SHA256 <source>,<destination>           # equal
git diff --stat                                                 # exactly two implementation files
git diff --check                                                # exit 0
git diff --cached --name-only                                   # exact two implementation paths
git diff --cached --check                                       # exit 0
MTC_COMMAND_CENTER\tools\repo_guard.ps1                         # pre-commit: PASS
git commit ...                                                  # f19572bc...
python -m mtc_v2.tests.corrected_vnext.verify_bceg ...          # exactly once; exit 2
```

The gate receipt and this report are the only post-implementation evidence files required by the
lane (`C:\tmp\LANE_PROMPTS_20260828\LANE_W303C_REFRESH_ANCHOR_SEAL12.md:35-40`). No push, merge, PR,
or destructive Git action is authorized (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:25-31`).

Independent Gate-5 acceptance: **NOT VERIFIED / unavailable inside this lane** because C-1 forbids
all other model/assistant invocation (`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md:3-7`).
