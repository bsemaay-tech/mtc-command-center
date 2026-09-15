# LEAD_ADJUDICATION — P1CAP_GEMINI (gemini-3.8-flash-high detection review of the P012 Path 1 capture tool candidate `e77af1c8`) — 2026-09-15 06:05Z

**Verdict as returned: REQUEST_CHANGES — 2 REQUIRED, 9 NITs (`evidence_class` SUPPLEMENTAL_UNEXECUTED).** Lead findings L-1..L-6: L-1/L-3/L-5/L-6 CONFIRMED, L-2/L-4 EXTENDED. Non-accepting, as expected for a first detection pass; both REQUIRED findings verified by the Lead against the bytes (below) and go to the correction lane P1FIX.

## Envelope and provenance
- Single attempt 05:58:11-06:02:11Z: conversation `ac81cedd-94c6-47a7-b26f-a1c9d83d3915`, SUCCESS, 192.9 s, 1 turn, usage input 124 656 / output 49 202 / thinking 32 655 / cache 937 739; `REVIEW.log` sha256 `0953f25b…`; response 37 778 chars sha256 `174334de…` (`REPORT_RESPONSE_UTF8.md`); sentinel present.
- Native reads (`NATIVE_READ_VERIFICATION.json`): 21 steps, 21/21 displayed content EQUAL to the packet bytes, 0 failures; every REQUIRED file read completely (tool 1-549 in four views, html 1-59, tests 1-225, both SDK excerpts, broker excerpt, verification, report, task, intake, owner packet 1-60, export excerpt, commit message, sums). One outside read: idx 2 `C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md` = the CLI's automatic context-file load (cwd = canonical checkout), before the first packet read; no other outside read.

## REQUIRED findings — Lead verification
| # | Finding | Lead check | Disposition |
|---|---|---|---|
| F-1 | `run_capture` `:426` `run_id = args.run_id or datetime.now(UTC).strftime(...)`: with `--ownership-signature` and no `--run-id` the message verified carries a fresh run_id → the owner's signature (made over the printed run_id) verifies MISMATCH by construction | CONFIRMED in the bytes (`:426`, `ownership_result(args.address, run_id, …)` at `:495`); the handoff plan already said "fix `--run-id` first" | REQUIRED → P1FIX: refuse `CAPTURE_REFUSED_RUN_ID_REQUIRED` when a signature is supplied without `--run-id`; verify the signature BEFORE any network call (L-4) |
| F-2 | `paged_query` `:283-297` admits every row the API returns; the SDK's `endTime` is inclusive (docstring) while the intake declares half-open intervals `[start_inclusive, end_exclusive)` (`REAL_OBSERVATION_INTAKE.md:31`) → an event at exactly `end` would be admitted; rows outside the requested window are trusted, never filtered | CONFIRMED: no timestamp filter in `paged_query`; intake wording verified; the Path 1 window 15:00Z→19:00Z is not affected in practice (events 16:03-18:08Z), but the semantics must be pinned before any capture is intake evidence | REQUIRED → P1FIX: filter rows to `[start_ms, end_ms)` for fills and funding (state the rule in the manifest `window.semantics`), refuse rows outside the requested range from the API (`CAPTURE_REFUSED_MALFORMED` "row outside window"), RED tests for both |

## NITs — disposition
F-3 (= L-4 verify order) and F-9 (= L-2 missing RED arms) fold into F-1's repair; F-4 (= L-3 funding identity + coin), F-5 (= L-5 `open("xb")`), F-6 (= L-5 error bytes), F-7 (= L-6 `raw_bytes_source`), F-10 (= L-1 lint/format) as in the Lead verification; **F-8 (new, EXTENDED L-2): `CapturingInfo.post` is never exercised by the tests (the `FakeInfo` double bypasses it) — add a unit test with a fake `session.post` returning a response object so the override's URL/JSON/timeout/exception order is fenced**; **F-11 (new): the re-query check compares identity SETS only, not row content — compare `{identity: row}` maps**. All NITs go to P1FIX as REQUIRED-for-the-lane items (cheap; the review roster should not re-open them).

## Roster
Gemini detection ✔ (this record; non-accepting by role) → P1FIX correction → Gemini delta + exact Sol → exact Opus after 2026-09-16 20:00Z. The real capture of the owner's account waits for P1FIX at minimum (F-1 makes any signed capture unverifiable today).

Recorded by Claude Opus 5 Lead (743291).
