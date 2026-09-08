# W305B Harness Continuation Report

## Verdict

**IMPLEMENTATION COMPLETE; CANONICAL GATE CORRECTLY REFUSED.** Items 5-8 were repaired as four separate red-green commits, the corrected-vNext self-test directory is green, and the one authorized canonical gate invocation persisted its receipt. The gate makes no acceptance claim: its claim label is `BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_REFUSED`, while `acceptance_reachable` remains `true` (`W305B_GATE_RECEIPT.json:183`, `W305B_GATE_RECEIPT.json:634-644`).

The canonical receipt contains 28 refusal records. Seven are the predicted semantic-review, RULE2-08/M1, and PROBE-P012-02-A/08-A M4 records; the remaining 21 records form **four finding groups** described below (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:29-33`, `W305B_GATE_RECEIPT.json:1152-1336`).

## Authority, preflight, and scope

- The continuation authorized work only in `verify_bceg.py`, its self-tests, and gate validators; it expressly prohibited kernel, golden, catalog, input, probe, baseline, seal, and design-byte changes (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:3-9`).
- Preflight found `W305_DONE.txt`, branch `feature/wp-p0-12-corrected-vnext-20260831`, starting HEAD `b22a912cf6e35fbb72f326ffa0379c922aacf0a3`, and a clean worktree. The required starting commit is identified by the continuation (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:11-14`).
- Write lane: branch `feature/wp-p0-12-corrected-vnext-20260831`; worktree `C:\WP012BUILD`; exact substantive paths were `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py` and `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py`; evidence outputs were `W305B_GATE_RECEIPT.json` and this report. The lane prompt names the worktree as sole-lane and supplies the same scope (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:4-9`).
- Live-dependency status: **NOT VERIFIED**. No host, broker, credential, deploy, scheduled task, or live-trading action was taken. Execution was limited to the local tests and canonical gate explicitly excepted by the task (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:3-9`).
- No push, merge, PR, or master-branch write was performed; the continuation expressly forbids pushing and working on master (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:7`, `C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:29-34`).

## Saved patch disposition

**DISCARDED after a successful `git apply --check`.** The continuation permitted either applying or discarding the verbatim partial patch, but required the choice and reason to be reported (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:15-19`). The patch explicitly said its selectors remained harness-authored because the catalog had no machine-readable projection declaration, then continued to branch on scenario IDs (`C:\tmp\LANE_PROMPTS_20260828\W305_item5_partial_uncommitted.patch:382-392`, `C:\tmp\LANE_PROMPTS_20260828\W305_item5_partial_uncommitted.patch:408-419`, `C:\tmp\LANE_PROMPTS_20260828\W305_item5_partial_uncommitted.patch:600-633`). That was not a compliant starting implementation for item 5, whose required disposition was to use sealed declarations or refuse `EXPECTATION_UNSEALED` (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:24`). I therefore implemented a smaller fail-closed change from the clean starting HEAD.

## Items 5-8 and red-green evidence

The source finding described the four defects precisely: reader-authored projection selectors (`C:\tmp\LANE_PROMPTS_20260828\_packets_V305C\W279B_HARNESS_EXTRACT.md:3-35`), reader-supplied economic inputs (`C:\tmp\LANE_PROMPTS_20260828\_packets_V305C\W279B_HARNESS_EXTRACT.md:39-81`), scenario-identity closed sets (`C:\tmp\LANE_PROMPTS_20260828\_packets_V305C\W279B_HARNESS_EXTRACT.md:85-111`), and a provenance refusal reporting only one of nineteen paths (`C:\tmp\LANE_PROMPTS_20260828\_packets_V305C\W279B_HARNESS_EXTRACT.md:115-129`).

### Item 5 — sealed RULE-2 projections

`build_projection_results` no longer reads actual kernel results to invent selectors or expected values. It accepts the sealed catalog row and the two permitted expected documents, and refuses `EXPECTATION_UNSEALED` because the current row has neither sealed projection field (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3424-3449`). The pipeline records that typed refusal and stops the projection claim (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3680-3691`). Tests cover a GREEN row and every RED/GREEN catalog row (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2097-2143`).

Quoted RED:

```text
FAILED ...::test_w305_item5_refuses_reader_authored_projection_when_catalog_has_none
Failed: DID NOT RAISE <class '...verify_bceg.GateRefusal'>
1 failed
```

Quoted GREEN:

```text
3 passed
150 passed
```

Commit: `b0933b1a21541bf5294bdc9fe31c6c5f53313ee2` — `fix(mtc-v2): refuse unsealed RULE-2 projections`.

### Item 6 — sealed economic inputs only

`corrected_contract_config` now transports optional collision/slippage values only when present in sealed `economic_inputs`; it supplies no reader default or literal model (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1184-1204`). `_target_book_overrides` was removed. `_declared_target_book` transports a sealed declaration without arithmetic and gives the equal-price case the required `INPUT_DECLARATION_MISSING` refusal because no such input exists (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1207-1226`). The full-gate path retains and reports that typed refusal (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3608-3627`). Tests bind both missing target input and the absence of reader defaults (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2146-2170`).

Quoted RED:

```text
Failed: DID NOT RAISE <class '...verify_bceg.GateRefusal'>
AssertionError: assert 'same_bar_collision_policy_id' not in config
```

Quoted GREEN:

```text
targeted item-6 tests passed
146 passed
```

Commit: `4c57e4e49a816235cab4b78cce7b762268de58a7` — `fix(mtc-v2): stop reader-authored economic inputs`.

### Item 7 — declaration-driven closed sets

`validate_corrected_closed_sets` now receives the sealed catalog row and derives conditional members from `owning_def_ids`, `role`, and the emitted closed ordering-rule token, rather than parsing or enumerating the scenario ID (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:649-655`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:721-740`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:880-930`). The regression test renames `RULE2-02-GREEN` while preserving the declaration and validates the same observed surface (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:1610-1625`).

Quoted RED:

```text
GateRefusal: CLOSED_SET_VIOLATION: unknown members ['admitted']
1 failed
```

Quoted GREEN:

```text
3 passed
147 passed
```

Commit: `d9a32f5fcc8cac61587ee4e6c4017ea425d4eb08` — `fix(mtc-v2): derive closed sets from declarations`.

### Item 8 — complete provenance refusal

`GateRefusal` now supports a backward-compatible first `pointer` plus an explicit complete `pointers` list and `count` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:136-165`). Provenance partitions lifted and refused paths, then emits one refusal record containing every remaining refused path (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:2166-2189`). The regression test derives the manifest path set, accounts for the decision-134 exception, and compares the complete refusal set (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:717-735`).

Quoted RED:

```text
AttributeError: 'GateRefusal' object has no attribute 'pointers'
1 failed
```

Quoted GREEN:

```text
1 passed
148 passed
```

Commit: `66d1c4257ae4d703f99562e7070636d670d38b0f` — `fix(mtc-v2): report all changed provenance paths`.

## Verification

Final corrected-vNext self-test command:

```text
cd C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON
python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
308 passed in 5.56s
```

The only canonical invocation was run after all four item commits, as required by the continuation (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:29-34`):

```text
python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W305B_GATE_RECEIPT.json
exit code: 1
receipt bytes: 78006
receipt SHA-256: 4AE7DECA66DDF78F212E948C5123F9343A2606094FC8C6494D00C115B0362AD0
```

The receipt covers 9 RED, 8 GREEN, and 10 PROBE rows (`W305B_GATE_RECEIPT.json:634-637`). Its ten probes are seven `DETECTED` and three `NOT_DETECTED`; the complete per-probe records are in `W305B_GATE_RECEIPT.json:980-1150`. Receipt commit: `34175404ec9ce4e6e28b39eaf909fadf754d121d` — `test(mtc-v2): record W305B canonical gate receipt`.

## Full canonical refusal list

The following is the complete 28-record `refusals` array, in receipt order (`W305B_GATE_RECEIPT.json:1152-1336`). Fields are quoted without reinterpreting them.

1. `SEMANTIC_COVERAGE_REVIEW_MISSING` — detail `C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\tests\corrected_vnext\contracts\semantic_coverage_review.json` (`W305B_GATE_RECEIPT.json:1153-1156`).
2. `EXPECTED_PATH_CHANGED_AFTER_BASE` — count `18`; detail `18 expected paths changed after the implementation base`; first pointer `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-RED.json` (`W305B_GATE_RECEIPT.json:1157-1162`). Full `pointers` list (`W305B_GATE_RECEIPT.json:1162-1181`):
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-01-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-GREEN.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-02-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-03-GREEN.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-03-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-04-GREEN.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-04-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-05-GREEN.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-05-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-GREEN.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-06-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-GREEN.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-07-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-GREEN.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/golden/corrected_vnext/RULE2-08-RED.json`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/DERIVATIONS.md`
   - `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/scenario_catalog.json`
3. `PROBE_NOT_DETECTED` — `PROBE-P012-02-A`; comparator `/RESULT_SURFACE/admitted`; measured `CLOSED_SET_VIOLATION` (`W305B_GATE_RECEIPT.json:1183-1188`).
4. `PROBE_NOT_DETECTED` — `PROBE-P012-06-A`; comparator `/EVENT_SURFACE/cash_events`; measured `CORRECTED_EXPECTATION` (`W305B_GATE_RECEIPT.json:1189-1194`).
5. `PROBE_NOT_DETECTED` — `PROBE-P012-08-A`; comparator `/RESULT_SURFACE/cumulative_funding`; measured `CLOSED_SET_VIOLATION` (`W305B_GATE_RECEIPT.json:1195-1200`).
6. `CLOSED_SET_VIOLATION` — `RULE2-08-RED`; `/RESULT_SURFACE/cumulative_funding`; detail `missing member cumulative_funding` (`W305B_GATE_RECEIPT.json:1201-1206`).
7. `CLOSED_SET_VIOLATION` — `RULE2-08-GREEN`; `/RESULT_SURFACE/cumulative_funding`; detail `missing member cumulative_funding` (`W305B_GATE_RECEIPT.json:1207-1212`).
8. `OBSERVED_ARTIFACT_STALE` — `RULE2-06-RED`; `tests/corrected_vnext/observed/2.0.0/RULE2-06-RED.json`; detail `committed=c05cdf34e3138934024adb6dafa5e33f3e6b3cbf82bec69e9be37e2319ad27e8 live_run=303c457576d73f57b6501b6d5eb95c7a598d8e1cfdcf774b1390c03b1ba29756` (`W305B_GATE_RECEIPT.json:1213-1218`).
9. `EXPECTATION_UNSEALED` — `RULE2-01-RED`; `/rule2_divergent_projection` (`W305B_GATE_RECEIPT.json:1219-1224`).
10. `EXPECTATION_UNSEALED` — `RULE2-01-GREEN`; `/rule2_green_projection` (`W305B_GATE_RECEIPT.json:1225-1230`).
11. `EXPECTATION_UNSEALED` — `RULE2-02-RED`; `/rule2_divergent_projection` (`W305B_GATE_RECEIPT.json:1231-1236`).
12. `EXPECTATION_UNSEALED` — `RULE2-02-GREEN`; `/rule2_green_projection` (`W305B_GATE_RECEIPT.json:1237-1242`).
13. `EXPECTATION_UNSEALED` — `RULE2-03-RED`; `/rule2_divergent_projection` (`W305B_GATE_RECEIPT.json:1243-1248`).
14. `EXPECTATION_UNSEALED` — `RULE2-03-GREEN`; `/rule2_green_projection` (`W305B_GATE_RECEIPT.json:1249-1254`).
15. `EXPECTATION_UNSEALED` — `RULE2-04-RED`; `/rule2_divergent_projection` (`W305B_GATE_RECEIPT.json:1255-1260`).
16. `EXPECTATION_UNSEALED` — `RULE2-04-GREEN`; `/rule2_green_projection` (`W305B_GATE_RECEIPT.json:1261-1266`).
17. `EXPECTATION_UNSEALED` — `RULE2-05-RED`; `/rule2_divergent_projection` (`W305B_GATE_RECEIPT.json:1267-1272`).
18. `EXPECTATION_UNSEALED` — `RULE2-05-GREEN`; `/rule2_green_projection` (`W305B_GATE_RECEIPT.json:1273-1278`).
19. `CORRECTED_EXPECTATION_MISMATCH` — `RULE2-06-RED`; `/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids/0` (`W305B_GATE_RECEIPT.json:1279-1283`).
20. `EXPECTATION_UNSEALED` — `RULE2-06-RED`; `/rule2_divergent_projection` (`W305B_GATE_RECEIPT.json:1284-1289`).
21. `INPUT_DECLARATION_MISSING` — `RULE2-06-EQUAL-PRICE-RED`; `/corrected_only/economic_inputs/target_book`; detail `equal-price corrected-only target book is absent from the sealed input` (`W305B_GATE_RECEIPT.json:1290-1295`).
22. `EXPECTATION_UNSEALED` — `RULE2-06-GREEN`; `/rule2_green_projection` (`W305B_GATE_RECEIPT.json:1296-1301`).
23. `EXPECTATION_UNSEALED` — `RULE2-07-RED`; `/rule2_divergent_projection` (`W305B_GATE_RECEIPT.json:1302-1307`).
24. `EXPECTATION_UNSEALED` — `RULE2-07-GREEN`; `/rule2_green_projection` (`W305B_GATE_RECEIPT.json:1308-1313`).
25. `CORRECTED_EXPECTATION_MISMATCH` — `RULE2-08-RED`; `/EVENT_SURFACE/cash_events` (`W305B_GATE_RECEIPT.json:1314-1318`).
26. `EXPECTATION_UNSEALED` — `RULE2-08-RED`; `/rule2_divergent_projection` (`W305B_GATE_RECEIPT.json:1319-1324`).
27. `CORRECTED_EXPECTATION_MISMATCH` — `RULE2-08-GREEN`; `/EVENT_SURFACE/decision_events` (`W305B_GATE_RECEIPT.json:1325-1329`).
28. `EXPECTATION_UNSEALED` — `RULE2-08-GREEN`; `/rule2_green_projection` (`W305B_GATE_RECEIPT.json:1330-1335`).

## Finding classification

### FINDING-1 — sealed projection declarations are absent

Sixteen gate records refuse `EXPECTATION_UNSEALED` across the rows that reach projection evaluation (`W305B_GATE_RECEIPT.json:1219-1278`, `W305B_GATE_RECEIPT.json:1284-1289`, `W305B_GATE_RECEIPT.json:1296-1313`, `W305B_GATE_RECEIPT.json:1319-1335`). The equal-price row stops earlier on missing economic input, but the catalog-wide self-test confirms that all 17 RED/GREEN rows lack an authorized projection declaration (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py:2117-2143`). This is a table/design authoring item; changing catalog/design bytes was expressly outside W305B scope (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:7-9`).

### FINDING-2 — equal-price target construction is not sealed

The equal-price scenario has no sealed `/corrected_only/economic_inputs/target_book`, so the harness cannot reproduce the premise without becoming an economic-input producer. The gate correctly records `INPUT_DECLARATION_MISSING` (`W305B_GATE_RECEIPT.json:1290-1295`), matching item 6's specified fail-closed disposition (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:25`). Resolution requires an owner-authorized input/catalog/design change outside this lane.

### FINDING-3 — RULE2-06 artifacts and probe depend on removed reader shaping

Without `_target_book_overrides`, `RULE2-06-RED` differs from its golden at `/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids/0`, its committed observation is stale, and `PROBE-P012-06-A` is not detected (`W305B_GATE_RECEIPT.json:1189-1194`, `W305B_GATE_RECEIPT.json:1213-1218`, `W305B_GATE_RECEIPT.json:1279-1283`). Those three records are one coherent Rule-6 re-authoring problem, not three independent fixes. Golden, observed, probe, input, catalog, and design changes were all outside W305B scope (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:7-9`).

### FINDING-4 — 18 expected paths still changed after the provenance base

Owner decision 134 lifts one formerly refused path, but 18 manifest members remain changed after the implementation base. The repaired record now reports the exact count and every path (`W305B_GATE_RECEIPT.json:1157-1181`). This closes the under-reporting defect but does not clear the underlying provenance blocker.

### Predicted/non-finding refusal buckets

- The missing semantic review is the predicted review record (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:30-32`, `W305B_GATE_RECEIPT.json:1153-1156`).
- The two RULE2-08 closed-set records and two RULE2-08 corrected mismatches are the known M1 cluster (`W305B_GATE_RECEIPT.json:1201-1212`, `W305B_GATE_RECEIPT.json:1314-1329`).
- `PROBE-P012-02-A` and `PROBE-P012-08-A` are the two predicted M4 non-detections (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:30-32`, `W305B_GATE_RECEIPT.json:1183-1188`, `W305B_GATE_RECEIPT.json:1195-1200`).

## Discrepancies

1. **Probe-count prediction:** the continuation predicted two `PROBE_NOT_DETECTED` records, but the canonical run produced three: P012-02-A, P012-06-A, and P012-08-A (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:30-32`, `W305B_GATE_RECEIPT.json:1183-1200`). P012-06-A is classified in FINDING-3.
2. **Provenance path count:** item 8 inherited the earlier “one path of nineteen” finding, but item 3 had already installed the decision-134 exception. The final measured refusal therefore contains 18 unlifted paths, not 19 (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:11-14`, `C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:27`, `W305B_GATE_RECEIPT.json:1157-1181`). Repository state wins; the implementation reports all 18.
3. **Write-lane mirror versus narrow scope:** repository protocol says the checked `SESSION_LOCK.md` mirror is populated before the first write (`MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md:1-23`), while the continuation declared this the sole worktree lane and restricted writes to the named harness/evidence outputs (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:4-9`, `C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:33-37`). No out-of-scope `SESSION_LOCK.md` byte was changed; the required branch, worktree, exact paths, and live-dependency status are recorded in this report.
4. **Guard timing:** repository protocol requires read-only auditing before editing (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md:11`). Marker, branch, HEAD, cleanliness, scope, and patch applicability were checked before editing, but the repository guard script itself was first run after the item-5 working-tree edit and before its commit. It passed before every commit, but its first-run timing did not meet the protocol literally.

## Commit inventory

The lane used one substantive commit per numbered item, followed by the required receipt commit; this matches the continuation's item/commit rule (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:29-34`).

| Purpose | Commit |
|---|---|
| Item 5 — sealed projection refusal | `b0933b1a21541bf5294bdc9fe31c6c5f53313ee2` |
| Item 6 — sealed economic-input transport | `4c57e4e49a816235cab4b78cce7b762268de58a7` |
| Item 7 — declaration-driven closed sets | `d9a32f5fcc8cac61587ee4e6c4017ea425d4eb08` |
| Item 8 — complete provenance pointers | `66d1c4257ae4d703f99562e7070636d670d38b0f` |
| Canonical receipt | `34175404ec9ce4e6e28b39eaf909fadf754d121d` |

The report itself is committed separately because its exact output path and committed state are required (`C:\tmp\LANE_PROMPTS_20260828\LANE_W305B_HARNESS_CONTINUATION.md:36-37`). Nothing was pushed.

## Repository guard handoff

The repository protocol requires this compact handoff shape (`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md:31-49`):

```text
branch:            feature/wp-p0-12-corrected-vnext-20260831
files changed:     MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py
                   MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py
                   W305B_GATE_RECEIPT.json
                   W305B_HARNESS_CONTINUATION_REPORT.md
checks run:        targeted RED/GREEN tests quoted above
                   python -m pytest mtc_v2/tests/corrected_vnext/contracts/selftests -q
                   python -m mtc_v2.tests.corrected_vnext.verify_bceg --mode full-gate --baseline-root C:/tmp/P012_BASELINE_RUN --output C:/WP012BUILD/W305B_GATE_RECEIPT.json
                   git diff --check
                   MTC_COMMAND_CENTER/tools/repo_guard.ps1 before every commit
guard:             PASS (branch merge-base 1 commit behind local origin/master; limit 30)
commit:            item and receipt hashes listed above; report is the final lane commit
pushed:            no
remaining dirty:   none after report commit
next action:       Lead triages four findings; do not treat this refused receipt as acceptance
```
