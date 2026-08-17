# Audit 2 D026 map count recheck - 2026-08-12

Analyst: Codex
Scope: independent read-only re-derivation of
`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md`.

Constraints followed: no map edit, no host/SSH/network execution, no git mutation. I wrote only
this recheck file.

## Method

I counted table rows directly from the map, one row per ID:

| Group | Row IDs | Count | Map lines |
|---|---:|---:|---|
| RP6-P0 | `RP6-01`..`RP6-11` | 11 | `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:21-31` |
| RP7-WPI-RO | `RP7-01`..`RP7-05` | 5 | `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:47-51` |
| Transport | `TR-01`..`TR-09` | 9 | `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:75-83` |
| SEC102 | `SEC-01`..`SEC-05` | 5 | `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:95-99` |
| Pathscope | `PS-01`..`PS-09` | 9 | `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:117-125` |

Total rows re-derived: 39.

## Count comparison

| Category | Map count | My count | Result |
|---|---:|---:|---|
| Total closure/evidence rows mapped | 39 (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:131`) | 39 | MATCH |
| Fully closed with located RED + GREEN on stated final bytes | 28 (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:132`) | 29 | DISAGREE |
| Unlocated/supplemental evidence flags | 11 (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:134`) | 10 | DISAGREE |
| Disclosed residuals/limitations with no closure test by design | 15 (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:135`) | 15 | MATCH |
| Open current-audit findings | 0 (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:133`) | 0 | MATCH, but stale contradicting text remains at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:137` |

Total row classifications I disagree with: 1 (`RP6-11`).

## Classification disagreement

| Row | Map row classification | Corrected classification | Corrected count impact |
|---|---|---|---|
| `RP6-11` | The table row still says `UNLOCATED - supplemental`, no located RED/GREEN pair, no qualifying GREEN binding, and `OPEN` (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:31`). | Fully closed for the current post-r17 map count. Round 17 supplies an explicit falsification/RED and GREEN pair for the dynamic-target class and ties GREEN to unchanged final block bytes. | Fully closed `28 -> 29`; unlocated/supplemental `11 -> 10`; open remains `0`. |

Evidence for the correction:

- The map's own r17 note says round 17 closes `RP6-11` by inversion, uses a temporary r16 fence with only the indirect-execution refusal removed, exercises two structurally different class members, and records the Lead verbatim run with `R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=15 fail=0 result=PASS` and unchanged block identity (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:160-171`).
- `SELF_QA_RP6.md` defines the r17 target count and states the deliberate RED construction: current r16 already refuses `eval`/`source`/`.`; the r17 harness removes only that refusal from an extracted r16 fence, then proves the weakened fence certifies both dynamic-target mutants clean while r17 refuses the same bytes (`SELF_QA_RP6.md:13137-13150`).
- The transcript contains the located REDs and GREENs: `D026_RED_WEAKENED_R16 mutant=eval rc=0 summary=PASS`, `D026_GREEN_R17 mutant=eval refused rc=1`, `D026_RED_WEAKENED_R16 mutant=dot_source rc=0 summary=PASS`, `D026_GREEN_R17 mutant=dot_source refused rc=1`, followed by the 15/15 PASS summary (`SELF_QA_RP6.md:13450-13471`; also summarized in `STATUS_RP6_P0.md:58-70`).
- Final byte identity is tied to the same subject: `RP6-P0.sh` remains 110817 bytes, SHA-256 `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330` (`SELF_QA_RP6.md:13120-13124`, `SELF_QA_RP6.md:13450-13470`, `STATUS_RP6_P0.md:16-18`). I re-derived the current file identity locally and it matches.

The r17 bytes still lack independent audit (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:173-175`), but that affects acceptance provenance, not this map category as defined at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:7` (located RED, located GREEN, explicit identity, GREEN tied to final bytes).

## Fully closed row triad check

The 28 rows already labeled fully closed in the main tables all cite the required triad:

| Rows | Check |
|---|---|
| `RP6-01`..`RP6-10` | Each row has RED command/output, explicit mutation/pre-fix identity, GREEN command/output, and `RP6 final subject above`; the final subject is named at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:13` and the rows are at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:21-30`. |
| `RP7-01`..`RP7-05` | Each row has RED output/identity, GREEN output, and `RP7 final subject above`; final bytes are named at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:43` and rows are at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:47-51`. I re-derived the current `RP7-WPI-RO.sh` and `SELF_QA_RP7.md` identities and they match the map. |
| `SEC-01`..`SEC-05` | Each row names the RED source/output, mutation/pre-fix identity, GREEN source/output, and final SEC module plus r11 evidence bytes; identities are named at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:89-91` and rows are at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:95-99`. I re-derived the current module and r11 evidence identities and they match the map. |
| `PS-01`..`PS-08` | Each row names the RED output signature, pinned round-1 identity, GREEN output signature, and final pathscope prover bytes; identities are named at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:111-113` and rows are at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:117-124`. I re-derived the current prover and self-QA identities and they match the map. |

With `RP6-11` corrected by r17, the fully closed set is:
`RP6-01`..`RP6-11`, `RP7-01`..`RP7-05`, `SEC-01`..`SEC-05`, and `PS-01`..`PS-08` = 29 rows.

## Overlap check

The map's pre-r17 table has exactly one double-count candidate: `RP6-11`, because the row is both
unlocated/supplemental and open (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:31`), and the summary
explicitly calls that the deliberate overlap (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:134`).
I found no other table row that is both open and unlocated/supplemental.

After applying the map's own r17 disposition and the current status evidence, there is no current
overlap: `RP6-11` moves to fully closed, the current open count is 0, and the remaining
unlocated/supplemental rows are only `TR-01`..`TR-09` plus `PS-09` = 10 rows.

Stale text to fix later: `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:137` still says one open
current-audit finding remains. Corrected number: 0.

## Residual count check

I confirm the map's residual total of 15 under the map's grouping:

| Source | Map residual count | My count | Evidence |
|---|---:|---:|---|
| RP6-P0 | 1 | 1 | The current status frames the surviving limitation as the static source/census proof boundary rather than runtime/bash equivalence (`STATUS_RP6_P0.md:237-240`, `STATUS_RP6_P0.md:299-302`) with named subcases such as caller-provided same-name function and quoted-literal command-word residuals (`STATUS_RP6_P0.md:361-372`). Counted as one RP6 residual family for this D026 map. |
| RP7-WPI-RO | 2 | 2 | The status discloses the `/dev/fd`/MSYS2 limitation (`STATUS_RP7.md:102-110`), and the self-QA states the remaining wrapper-kill attribution limit: another SIGKILL concurrent with the wrapper kill can still be reported as kill-after (`SELF_QA_RP7.md:4485-4487`). |
| Transport | 1 | 1 | F1 remains honestly open as the outer SSH account-shell boundary, owner-accepted with disclosure and not a freeze blocker (`STATUS_TRANSPORT.md:6-16`, `STATUS_TRANSPORT.md:273-292`). |
| SEC102 | 4 | 4 | The status lists exactly four accepted trusted-base assumptions (`STATUS_SEC102.md:29-49`). The GLM second opinion is PASS-WITH-NITS and supplemental on execution; its one nit is not a required repair and is already inside the disclosed item (`STATUS_SEC102.md:50-61`). The map's SEC102 count of 4 is still right. |
| Pathscope | 7 | 7 | The status points to the repair report for every finding disposition (`STATUS_PATHSCOPE.md:5-8`) and states the lexical/host proof boundary (`STATUS_PATHSCOPE.md:26-34`). The repair report lists residuals R1-R7 explicitly (`PATHSCOPE_REPAIR_R2_REPORT.md:312-349`). |

Residual total: 1 + 2 + 1 + 4 + 7 = 15.

## Post-r17 state

The current RP6 byte state is consistent with r17 resolution:

- `RP6-P0.sh`: 110817 bytes, SHA-256 `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`; matches map/status (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:13`, `STATUS_RP6_P0.md:16-18`).
- `SELF_QA_RP6.md`: 1038848 bytes, SHA-256 `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`; matches map (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:15`).
- The current status states that round 17 supplies the missing executed pair for the dynamic-target class and replaces the misleading literal target-count claim with a measured record (`STATUS_RP6_P0.md:20-25`).

Therefore the `open current-audit findings = 0` claim is supported by the current r17 evidence, but the map's row-level and supplemental-count text still need Lead edits to avoid carrying the obsolete pre-r17 `RP6-11` classification.
