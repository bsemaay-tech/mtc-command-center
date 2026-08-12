# WP-I summary-vs-detail consistency sweep - 2026-08-12

Analyst: Codex  
Scope type: T2 docs/evidence consistency sweep  
Write policy followed: this is the only file written. No swept file was edited. No git add/commit/checkout/reset/stash was run.

## Enumeration

I enumerated the sweep set from tracked Git history only, per the kickoff:

```text
git rev-list -1 --before='2026-08-12 00:00:00' HEAD
=> d12088260dae0a033796e45807f525e966adce41

git log --since='2026-08-12 00:00:00' --name-only --pretty=format: -- MTC_COMMAND_CENTER/11_TRIAGE
git diff --name-only d12088260dae0a033796e45807f525e966adce41 -- MTC_COMMAND_CENTER/11_TRIAGE
```

Tracked files swept: 132. Untracked run logs/scratch directories under `11_TRIAGE` were visible in `git status`, but were not part of the kickoff enumeration contract and were not swept as records.

## Result summary

- Files with findings: 11.
- Files swept and found consistent for this sweep's criteria: 121.
- Internal contradictions found: 3 primary contradictions, with several stale/detail remnants under those same files.
- Cross-file disagreements found: 7 current-state disagreements plus 2 low citation-drift findings.
- Single most consequential inconsistency: `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` simultaneously says D026 current-audit open findings are zero and that one open finding remains (`RP6-11`). An auditor reading only the stale line could believe the already-closed RP6-11 finding is still a freeze-relevant open item.

## Findings

### INT-01 / XFILE-01 - D026 map still says one open finding remains

Type: stale; incomplete supersession/strikethrough.

Stale reading:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:139` says: "one open current-audit finding remains (`RP6-11`)."

Correct readings in the same file:
- `.../AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:31` classifies `RP6-11` as "CLOSED by round 17" and "FULLY CLOSED."
- `.../AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:134` corrects fully closed from 28 to 29.
- `.../AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:135` strikes the old one-open statement and says round 17 resolved it to 0 open.
- `.../AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:136` corrects unlocated/supplemental from 11 to 10.

Correct reading: 39 rows / 29 closed / 10 supplemental / 15 residuals / 0 open. The same file's corrected row and corrected count block are newer and supported by the round-17 evidence. Line 139 is the stale surviving old value.

Why it matters: this is the most consequential inconsistency because it changes the freeze-relevant D026 status from "0 open" to "1 open" depending on which line an auditor reads.

### XFILE-02 - D026 count recheck report is stale after its target map was repaired

Type: stale derivative report.

Stale readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md:29` says the map count is 28 closed vs the recheck's 29.
- `.../AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md:30` says the map count is 11 supplemental vs the recheck's 10.
- `.../AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md:40` says the `RP6-11` row still reads unlocated/open.
- `.../AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md:76-77` says stale one-open text remains at the map.
- `.../AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md:101` says the map row-level and supplemental-count text still need edits.

Correct readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:31` now marks `RP6-11` fully closed.
- `.../AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:134-136` now shows 29 closed, 0 open, 10 supplemental.
- `.../AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md:62-74` correctly derives the intended current count as 29 closed and 10 supplemental after applying r17.
- `.../AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md:98-99` confirms the post-r17 `SELF_QA_RP6.md` identity and r17 closure evidence.

Correct reading: the recheck was accurate when it found the defect, but its "map still needs edits" conclusion is stale after the later map repair. The only surviving map defect is line 139, not the row or 29/10 counts.

### INT-02 - Audit 2 handoff package says D026/freeze-input packets both exist and do not exist

Type: stale; internal contradiction.

Current packet-exists readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:23` says missing material 7, the D026 map for current WP-I work, is "CLOSED AS A PACKET" and cites the completed 39-row map.
- `.../AUDIT2_HANDOFF_PACKAGE.md:24` says missing material 8, the freeze-input ledger, is "PARTIAL - analysis delivered, final ledger NOT-YET-AVAILABLE."
- `.../AUDIT2_HANDOFF_PACKAGE.md:32-39` summarizes the current result as 16 closed, 1 partial, 3 open.

Stale reading:
- `.../AUDIT2_HANDOFF_PACKAGE.md:189-193` says Audit 2 is not dispatchable partly because "the current-work D026/freeze-input/host evidence packets do not exist."

Correct reading: host execution evidence still does not exist, but the D026 packet exists and the freeze-input analysis exists as a partial packet. Line 192 overgeneralizes an older "not available" state.

### XFILE-03 - SEC102 status is stale in three readiness records

Type: stale; cross-file disagreement.

Stale readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:14` says "SEC102 round 9 and its Codex audit are pending."
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_RED_LOCATIONS.md:46` says SEC102 r9 repair, GREEN, Codex r9 acceptance, and GLM second opinion are pending.
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:189-191` says "SEC102 and pathscope still have pending review work."

Correct readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:11` says SEC102 is accepted-with-disclosure and freeze blocker #4 cleared.
- `.../AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:31` records owner acceptance, Codex/GLM evidence, and "Nothing - freeze blocker #4 is CLEARED."
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md:4` labels SEC102 accepted-with-disclosure.
- `.../STATUS_SEC102.md:63-65` says WP-I freeze blocker #4 is cleared.

Correct reading: SEC102 is ACCEPTED-WITH-DISCLOSURE by owner decision and blocker #4 is cleared. Pathscope remains pending, but SEC102 does not.

### XFILE-04 - `AUDIT2_D026_RED_LOCATIONS` still says the current-work D026 packet is not available

Type: stale; cross-file disagreement.

Stale reading:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_RED_LOCATIONS.md:35-39` says the complete current-work D026 packet is "NOT-YET-AVAILABLE."

Correct readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:133-141` contains the completed/current 39-row map summary and says packet 7 can be marked closed.
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:23` marks the D026 map packet closed.

Correct reading: the old RED-location index may remain useful as partial source context, but it is no longer true that the current-work D026 packet is unavailable.

### INT-03 / XFILE-05 - Freeze blocker map carries old D026 counts and old blocker-7 wording

Type: stale; internal contradiction and cross-file disagreement.

Old D026-count reading:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:61-67` labels the section "one open D026 gap" and says the D026 map had 28 closed, 11 supplemental/unlocated, 15 residuals, and one current-audit RED with no repaired GREEN.

Correct readings:
- `.../WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:154-157` later says the summary/detail defect was corrected and counts moved to 39 rows / 29 closed / 10 supplemental / 15 residuals / 0 open.
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:134-136` carries the same corrected counts.

Old blocker-7 wording:
- `.../WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:19` says `run_p0.sh` wires none of the five `P0_ATTESTED_*` inputs and is unchanged.

Correct readings:
- `.../WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:101-104` says `run_p0.sh` defines, exports, and logs all five values as `<PIN-AT-FREEZE>` literals, so the problem is unfilled placeholders, not missing wiring.
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:84-88` explicitly corrects the shape: current bytes define/export/log the five values as markers and RP6 refuses them, so no end-to-end P0 PASS is possible while they remain unfilled.

Correct reading: item 7 is still open, but the precise defect is "wired as placeholder markers requiring freeze fill," not "wires none." The D026 numbers should be the corrected 39/29/10/15/0 set.

Status-label note:
- `.../WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:1-5` still presents the file as a 13:45 snapshot even though the body contains later R17 and 18:20 corrections (`:84-96`, `:152-164`). The title is stale as a current-state label, though the later body text is useful.

### XFILE-06 - `.gitattributes` durability analysis still carries the transient `SELF_QA_RP6.md` mismatch as current

Type: stale; cross-file disagreement.

Stale readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md:12` says `SELF_QA_RP6.md` no longer matches the current-cycle accepted row.
- `.../WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md:49` measures current `SELF_QA_RP6.md` as 1038848 B / `07cf843d...` but marks the quoted identity match as `NO` against 1024538 B / `897a5a...`.
- `.../WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md:68` says the current measured bytes no longer match the old identity "still printed" in the D026 map.

Correct readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:15` now records `SELF_QA_RP6.md` as 1038848 B / `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`.
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:25` records the same post-r17 identity and keeps the r16 identity only as history.

Correct reading: the gitattributes analysis correctly captured a transient concurrent mismatch at its snapshot time, but that mismatch is no longer current after the D026 map and acceptance matrix were updated.

### XFILE-07 - Freeze-literal shared fact is not carried identically everywhere

Type: ambiguous/incomplete wording; not a numeric falsehood.

Incomplete readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:24` says "17 freeze literals remain" without carrying the now-required 27 raw occurrence qualifier.
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:101-104` says "17 remaining freeze literals" without qualifying distinct definitions at the local point of use.
- `MTC_COMMAND_CENTER/11_TRIAGE/FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md:196-199` says the RP6 cross-check must resolve the Lead-found 17-vs-27 discrepancy. This is explicitly time-scoped as "IN FLIGHT at handoff time" at `:188`, so it was not wrong when written; it is stale if the file is consumed as a completed 2026-08-13 morning handoff.

Correct readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:88` says 17 means distinct `P0_FIXED_*` definitions, while 27 is raw occurrences including 10 guard/fence occurrences.
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md:114-127` gives the same 17 definitions / 27 raw occurrences reconciliation and lists the 10 guard occurrences.
- `MTC_COMMAND_CENTER/11_TRIAGE/LEDGER_RP6_CLAIMS_GLM_CROSSCHECK_2026-08-12.md:8` confirms the 17 distinct definitions.
- `.../LEDGER_RP6_CLAIMS_GLM_CROSSCHECK_2026-08-12.md:12` states the 17-vs-27 discrepancy is resolved and both counts are correct with different referents.
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:166-168` later says the 17-vs-27 figures were reconciled.

Correct reading: 17 distinct freeze-input definitions; 27 raw string occurrences. Short "17 freeze literals" statements are understandable only if "literals" is read as definitions, but the kickoff requires both numbers to be carried identically.

### XFILE-08 - GLM RP6 ledger cross-check still reports a stale ledger citation after the ledger was corrected

Type: stale derivative report; low severity.

Stale readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md:19-21` says the one genuine defect is the stale `STATUS_RP6_P0.md:311-312` citation.
- `.../RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md:139-148` says the ledger line 88 still cites `STATUS_RP6_P0.md:311-312`.
- `.../RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md:207` repeats that stale-citation defect.
- `MTC_COMMAND_CENTER/11_TRIAGE/LEDGER_RP6_CLAIMS_GLM_CROSSCHECK_2026-08-12.md:18` repeats the same stale-citation defect in the wrapper verdict.

Correct reading:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:88` now cites `STATUS_RP6_P0.md:396-397`, notes the count field at `:274`, and explicitly says the citation was corrected from `:311-312`.

Correct reading: the GLM cross-check was correct when it found the stale citation, but its defect statement is now stale after the ledger was amended.

### XFILE-09 - Freeze-input ledger identity anchors have stale acceptance-matrix line numbers

Type: stale citation only; content hashes are correct.

Stale readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:11` says the RP6 hash matches `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:14`.
- `.../WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:13` says the `run_p0.sh` hash matches `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:31`.

Correct readings:
- `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:24` is the current RP6 identity row.
- `.../AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:49` is the current `run_p0.sh` transport identity row.

Correct reading: the hashes in the ledger are substantively right, but some acceptance-matrix line anchors shifted after same-day edits. This is not an artifact identity mismatch.

## Shared facts checked clean

RP6 block identity is consistent wherever currently stated as a current fact: 110817 B, SHA-256 `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`, unchanged r10a through r17. Clean anchors include `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:24`, `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:13`, `STATUS_RP6_P0.md:16-18`, `RP6_R17_REPORT_2026-08-12.md:16-23`, and `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:93-96`.

`SELF_QA_RP6.md` post-r17 identity is consistent in the current acceptance records: 1038848 B, SHA-256 `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`. The only stale exception is the transient `.gitattributes` analysis finding recorded above.

Second-flagship state is consistent in current acceptance/blocker records: RP6, RP7, transport, and pathscope are all still PENDING Claude Pro; GLM advance reviews are supplemental and do not close second-flagship slots. Clean anchors include `AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:14-18,26,28,30,33` and `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:11-15`.

The corrected round-17 implementer identity is consistent in the current RP6 status/report files: `gpt-5.5`, not `gpt-5.6-sol`. Clean anchors are `STATUS_RP6_P0.md:3-8` and `RP6_R17_REPORT_2026-08-12.md:3-8`.

## Files with findings

1. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_RED_LOCATIONS.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md`
5. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md`
6. `MTC_COMMAND_CENTER/11_TRIAGE/FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md`
7. `MTC_COMMAND_CENTER/11_TRIAGE/LEDGER_RP6_CLAIMS_GLM_CROSSCHECK_2026-08-12.md`
8. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md`
9. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_BLOCKER_MAP_2026-08-12.md`
10. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md`
11. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md`

## Files swept and found consistent

The following tracked files were swept and did not show a current summary-vs-detail contradiction, stale top status, incomplete strikethrough correction, or contradictory current statement of the kickoff's shared facts:

1. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/KICKOFF_AUDIT2_READINESS.md`
5. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md`
6. `MTC_COMMAND_CENTER/11_TRIAGE/FRESH_SESSION_HANDOFF_2026-08-12_MORNING.md`
7. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_AUDIT2_PACKETS_9_10_11_SCOPING.md`
8. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_AUDIT2_REFRESH_R1.md`
9. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_D026_CONSOLIDATION_MAP.md`
10. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_D026_MAP_COUNT_REDERIVE.md`
11. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_FREEZE_INPUT_LEDGER.md`
12. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_GITATTRIBUTES_DURABILITY_ANALYSIS.md`
13. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_PREREG_TRUSTED_BASE_CARRY_LIST.md`
14. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_CODEX_SUMMARY_VS_DETAIL_CONSISTENCY_SWEEP.md`
15. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_GLM_CROSSCHECK_LEDGER_RP6_CLAIMS.md`
16. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_GLM_STATUS_VS_BYTES_SWEEP.md`
17. `MTC_COMMAND_CENTER/11_TRIAGE/KICKOFF_GLM_WPL_B3_RECORD_SWEEP.md`
18. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/CONVERGENCE_NOTE_RP6_SEC102_2026-08-12.md`
19. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md`
20. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP7_2NDFLAGSHIP_AUDIT.md`
21. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_TRANSPORT_2NDFLAGSHIP_AUDIT.md`
22. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CODEX_RP6_CENSUS_R17.md`
23. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CODEX_RP6_R15_AUDIT.md`
24. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CODEX_RP6_R16_AUDIT.md`
25. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_CODEX_RP7_ROWS_1_9_BUILD.md`
26. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_GLM_ADVANCE_RP6_READ_AUDIT.md`
27. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_GLM_ADVANCE_RP7_READ_AUDIT.md`
28. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_GLM_ADVANCE_TRANSPORT_READ_AUDIT.md`
29. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/KICKOFF_RP6_REPAIR_R16.md`
30. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R15_2026-08-12.md`
31. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R16_2026-08-12.md`
32. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`
33. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R15_REPORT_2026-08-11.md`
34. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R16_REPORT_2026-08-11.md`
35. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R17_REPORT_2026-08-12.md`
36. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`
37. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`
38. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`
39. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md`
40. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/TRANSPORT_GLM_ADVANCE_READ_AUDIT_2026-08-12.md`
41. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/.gitattributes`
42. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py`
43. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CLAUDEPRO_PATHSCOPE_EXECUTION_AUDIT.md`
44. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CODEX_SEC102_R10_AUDIT.md`
45. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CODEX_SEC102_R11_AUDIT.md`
46. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CODEX_SEC102_R6_AUDIT.md`
47. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CODEX_SEC102_R7_AUDIT.md`
48. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CODEX_SEC102_R8_AUDIT.md`
49. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CODEX_SEC102_R9_AUDIT.md`
50. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_GLM_ADVANCE_PATHSCOPE_DISCLOSURE_AUDIT.md`
51. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_GLM_SEC102_2ND_OPINION.md`
52. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_SEC102_BUILD_R10.md`
53. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_SEC102_BUILD_R11.md`
54. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_SEC102_BUILD_R7.md`
55. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_SEC102_BUILD_R8.md`
56. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_SEC102_BUILD_R9.md`
57. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_GLM_ADVANCE_DISCLOSURE_AUDIT_2026-08-12.md`
58. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/RUNID_MINTING_REVIEW_CODEX_2026-08-11.md`
59. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_ACCEPT_WITH_DISCLOSURE_RECOMMENDATION_2026-08-12.md`
60. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_CODEX_T1_AUDIT_R10_2026-08-12.md`
61. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_CODEX_T1_AUDIT_R11_2026-08-12.md`
62. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_CODEX_T1_AUDIT_R6_2026-08-12.md`
63. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_CODEX_T1_AUDIT_R7_2026-08-12.md`
64. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_CODEX_T1_AUDIT_R8_2026-08-12.md`
65. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_CODEX_T1_AUDIT_R9_2026-08-12.md`
66. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_GLM_T1_2ND_OPINION_2026-08-12.md`
67. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_R10_REPORT_2026-08-12.md`
68. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_R11_REPORT_2026-08-12.md`
69. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_brace_command_word.sh`
70. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_brace_command_word.sh.in`
71. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_bracket_command_word.sh`
72. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_bracket_command_word.sh.in`
73. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_glob_command_word.sh`
74. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_glob_command_word.sh.in`
75. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_param_command_word.sh`
76. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_param_command_word.sh.in`
77. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_relative_interpreter.sh`
78. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_relative_interpreter.sh.in`
79. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_static_leaf.sh`
80. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_static_leaf.sh.in`
81. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_substitution_command_word.sh`
82. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_substitution_command_word.sh.in`
83. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_tilde_command_word.sh`
84. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/entry_tilde_command_word.sh.in`
85. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/green_render_static_leaf.json`
86. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_brace_command_word.json`
87. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_bracket_command_word.json`
88. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_glob_command_word.json`
89. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_param_command_word.json`
90. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_relative_interpreter.json`
91. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_substitution_command_word.json`
92. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r6_fixtures/red_render_tilde_command_word.json`
93. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_R6_REPORT_2026-08-11.md`
94. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_extglob_at_command_word.sh`
95. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_extglob_at_command_word.sh.in`
96. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_extglob_bang_command_word.sh`
97. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_extglob_bang_command_word.sh.in`
98. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_extglob_plus_command_word.sh`
99. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_extglob_plus_command_word.sh.in`
100. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_extglob_qmark_command_word.sh`
101. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_extglob_qmark_command_word.sh.in`
102. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_novel_operator_command_word.sh`
103. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_novel_operator_command_word.sh.in`
104. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_safe_set_leaf.sh`
105. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/entry_safe_set_leaf.sh.in`
106. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/green_render_safe_set_leaf.json`
107. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/red_render_extglob_at_command_word.json`
108. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/red_render_extglob_bang_command_word.json`
109. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/red_render_extglob_plus_command_word.json`
110. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/red_render_extglob_qmark_command_word.json`
111. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/sec102_r7_fixtures/red_render_novel_operator_command_word.json`
112. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_R7_REPORT_2026-08-11.md`
113. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_R8_REPORT_2026-08-11.md`
114. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_R9_REPORT_2026-08-12.md`
115. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R10.md`
116. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R11.md`
117. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R6.md`
118. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R7.md`
119. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R8.md`
120. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SELF_QA_SEC102_R9.md`
121. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md`
122. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md`
