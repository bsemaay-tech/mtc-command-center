# LEAD_ADJUDICATION — P1CAP_DELTA_GEMINI (gemini-3.8-flash-high delta review of the Lead-authored P1FIX `af921d75`) — 2026-09-15 06:52Z

**Verdict as returned: PASS-WITH-NITS — F-1..F-11 and L-1..L-6 all RESOLVED; `lead_authorship: NOTED`; one NIT G-D-01.** Delta-review slot for the capture tool: SATISFIED (Gemini). The tool remains NONACCEPTED: exact Opus after the 2026-09-16 20:00Z reset, exact Sol after the Codex reset (Sep 19); the Lead does not accept its own code.

## Envelope and provenance
Single attempt 06:46:05-06:50:26Z: conversation `ae72a8a5-0a7b-4631-8c19-7e0486be8a36`, SUCCESS, 192.4 s, usage input 187 885 / output 34 844 / thinking 23 483 / cache 2 349 565; `REVIEW.log` sha256 `1ce4d5fa…`; response 17 752 chars sha256 `ea6f7bb0…` (`REPORT_RESPONSE_UTF8.md`); sentinel present. Native reads (`NATIVE_READ_VERIFICATION.json`): 35 steps, 35/35 displayed content EQUAL to the packet bytes, 0 failures: the full diff (907 lines, six views), the full tool at `af921d75` (717 lines), the full tests (544 lines), the html, the pre-fix tool at the ranges needed for the RED judgements, all sources. Outside read idx 2 = the CLI's AGENTS.md context load only.

## Finding and Lead disposition
| # | Finding | Disposition |
|---|---|---|
| G-D-01 (NIT) | two of the twelve pre-fix RED arms (`test_requery_identity_mismatch_refuses`, `test_write_once_refuses_an_existing_output`) fail on the pre-fix tool because of tightened detail assertions, not missing rejection logic | Agreed and already stated in the disposition ("the 9 passing tests fence behaviour that already existed"; those two refusals existed pre-fix — the detail text and the exclusive-create form are what changed). No code change; the other ten RED arms fail pre-fix for the defect itself (window, run-id, signature order, error bytes, provenance, coin identity, content re-query, `CapturingInfo` error capture). |

## Consequence for today
The owner's real read-only capture may proceed under `OD-20260915-P012-P1FIX-LEAD-1` once he hands the Lead his `personal_sign` signature over the printed message (run_id `p012-path1-20260914T1500Z-1900Z-r1`); the capture output is NONACCEPTING evidence, intaken only after the exact roster completes.

Recorded by Claude Opus 5 Lead (743291).
