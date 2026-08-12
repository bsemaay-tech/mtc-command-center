I now have the full, independently-verified picture. **This task is already complete — done twice, in two independent lanes, both committed.** Dispatching Codex now would overwrite a committed audit artefact, so I'm surfacing before touching anything.

## What happened (reconstructed from commits + files)

| Commit | What |
|---|---|
| `bdb35431` | Map written (Codex, packet 7) with original counts **39 / 28 / 11 / 15 / open=1** |
| `d3a8b7b4` | Map refreshed for round 17 — RP6-11 resolved, summary → 0 open — **but the RP6-11 table row and line 139 were left stale** |
| `2285ae85` | **1st independent re-derivation (Codex)** caught it: RP6-11 row still read UNLOCATED/OPEN after the summary already said 0. Map corrected **28→29 closed, 11→10 supplemental**. Wrote `AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md` (the file the kickoff asks me to "create") |
| `0ab0588b` | **2nd independent recount (Claude-Lead)** confirmed all five counts AND caught that line 139 was still stale; fixed it |

So the kickoff's premise — *"nobody has re-derived them"* — was true when written, but both re-derivations have since run and committed. The GLM second-recheck attempt itself died (202 bytes of warnings); the Claude-Lead lane took it up and that's the committed `0ab0588b`.

## My own independent recount of the *current* map (Lead inspection, not relay)

Counted every table row by ID:

| Category | Map (current) | My count | |
|---|---:|---:|---|
| Total rows | 39 | **39** (RP6 11 + RP7 5 + TR 9 + SEC 5 + PS 9) | ✅ |
| Fully closed (RED+GREEN+final bytes) | 29 | **29** (RP6-01…11, RP7-01…05, SEC-01…05, PS-01…08) | ✅ |
| Unlocated/supplemental | 10 | **10** (TR-01…09, PS-09) | ✅ |
| Disclosed residuals | 15 | **15** (1+2+1+4+7) | ✅ |
| Open findings | 0 | **0** | ✅ |

Row-classification disagreements with the current map: **0**. RP6-11 is correctly FULLY CLOSED (RED = weakened-r16-fence `eval`/`dot_source` rc 0; GREEN = r17 `refused rc=1`; block `5132bacd…` unchanged). No double-count remains. The map is internally consistent — line 139 included.

## The problem with re-dispatching now

`AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md` is a **committed** file that records Codex's *historical DISAGREE* (28→29) against the old map. A fresh Codex run against the *current* (already-corrected) map would find **all-MATCH** and, per the kickoff's "write exactly one new file" instruction, would **overwrite** that lane record. The prior Lead file explicitly stopped and refused to do this ("Overwriting it would erase Codex's lane record"). It would also burn premium Codex tokens re-confirming an already-twice-confirmed count.

## Recommendation

**Accept as-is.** The kickoff's goal — independent re-derivation of the five counts — is met, by two lanes, committed. The current map is correct.

If you specifically want a **third** fresh lane (e.g. you don't trust that the committed lanes weren't contaminated), say so and I'll dispatch Codex via the mandated launcher to a **new** path (`..._THIRD_RECHECK_CODEX_2026-08-12.md`) rather than overwriting. I won't overwrite the committed recheck file or edit the map without your explicit nod.

Which would you like: **(a)** accept the existing coverage, **(b)** third Codex lane at a new path, or **(c)** something else?
