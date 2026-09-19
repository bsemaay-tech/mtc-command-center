# LEAD_ADJUDICATION — exact Sol (`gpt-5.6-sol` xhigh, second flagship) T0 read of the P0-12 capture-tool NIT slice `1029d6e9`

**Lane:** `C:/tmp/SOL_QUEUE_20260919/P1CAP/sol` (Codex Pro account `free`), generated against worktree
pin `C:/tmp/P1CAP_20260914 @ 1029d6e9`, second lane in the Lead's chain (after P031). Launch
08:40:23Z-09:07:00Z (27 min), `launch.exit` exit=0. Report `SOL_T0_REPORT.md`, 301 lines. Sol
states it read no Opus report or adjudication before fixing its verdict — an independent second
flagship, different family, as the roster requires.

**Verdict as returned:** `VERDICT: REQUEST_CHANGES` — **two REQUIRED findings** (R-1, R-2), plus
two NITs (N-1: the same "NIT-4 has no mutant" record error the exact-Opus re-read already caught
as NIT-B; N-2: the same `ruff format` regression exact-Opus caught as NIT-A). Sol reached both
NITs independently — a second confirmation of both, not new information, so no new record fix
needed there beyond what `LEAD_VERIFICATION_P1CAP_NIT.md` already carries.

## Worktree integrity
`git status --porcelain` in `C:/tmp/P1CAP_20260914` after the lane: only the four pre-existing
untracked scratch files (`REPORT.md`, `SHA256SUMS.txt`, `TASK_P1CAP.md`, `TASK_P1FIX.md` — present
since before this session touched anything). `HEAD` unchanged at `1029d6e9`. The lane's
`--add-dir` grant of write access to the worktree was not exercised.

## Adjudication — both REQUIRED findings CONFIRMED, independently reproduced

### R-1 — later-page lower-bound checked against the wrong value
**Citation check:** `capture_own_account_evidence.py:362` (`if t < start_ms:`) and `:388-389`
(`if len(parsed) < limit: return ...`) — **EXACT**, read directly from `git show 1029d6e9:...`.
`cursor = start_ms` is at `:317` (report's `:323` is close; the substance is exact — the row-time
floor never advances past the constant `start_ms`, even though `cursor` itself advances page to
page at `:392`).

**Independent reproduction** (`LEAD_REPRO_R1.py`, written from scratch, not Sol's own test file —
a different fake `Info` double, different fixture data): `HL_FILLS_PAGE_LIMIT=2`; page 1 full
(`tid=1@T0`, `tid=2@T1`, 2 rows == limit, continues, cursor becomes `T1`); page 2 short (`tid=3@T0`,
1 row, `T0 < T1` but `T0 >= start_ms`) on **both** passes (pass 1 and the requery pass return the
identical malformed sequence, so `requery_check` agrees). Result: **`run_capture` returns a
manifest with no refusal** — the stale/duplicate-window row is silently accepted as new data.
Matches Sol's described shape exactly. **CONFIRMED.**

### R-2 — a 2xx non-JSON response is accepted as valid account state
**Citation check:** `capture_own_account_evidence.py:91-102` (`CapturingInfo.post`'s
`except ValueError: return {"error": ...}` fallback) and `:450-463` (`account_state_query`'s
`if not isinstance(parsed, dict)` check) — **EXACT**. Confirmed against the SDK
(`hyperliquid/api.py:30-33`) that `_handle_exception` does not raise for `status_code < 400`, so a
2xx response with a non-JSON body reaches the fallback untouched — matches R-2's premise.

**Independent reproduction** (`LEAD_REPRO_R2.py`, a real `CapturingInfo` with a fake `.session`
returning `FakeResponse(b"<html>502 Bad Gateway</html>", status_code=200)`): `account_state_query`
records the bytes, then **accepts the `{"error": "Could not parse JSON: ..."}` dict as a valid
account state and returns normally** — no refusal, `account_state.json` on disk contains the HTML
error page. **CONFIRMED.**

## Standing
Both REQUIRED findings are real, independently confirmed by the PACKAGE session with fresh
reproduction scripts (not a re-run of Sol's own arms). `1029d6e9` is **NOT merge-ready**: the
roster's exact-Opus PASS-WITH-NITS (0 REQUIRED) and Gemini PASS did not catch either gap — this is
exactly the value of the two-flagship-plus-Gemini-plus-Lead-reproduction rule, and it worked as
designed. Per the Lead's routing: PACKAGE session repairs as the disclosed builder (T0 repair
round 1 of cap 3), then the full review roster (Gemini delta, exact-Opus, Sol) re-reads the repaired
bytes before any merge-readiness claim.

Recorded by the P0-12 PACKAGE session (Claude Sonnet 5), 2026-09-19.
