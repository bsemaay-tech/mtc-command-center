# Wednesday exact-Opus queue — Claude Pro weekly reset 2026-09-16 20:00Z (prepared 2026-09-15 by the session-4 Lead)

Owner standing: exact `claude-opus-5` xhigh T0 reviews run on the Claude PRO profile (`~/.claude`), one at a time, never while `agy.exe` (Gemini) runs; `REVIEW_POLICY` requires the exact Opus slot on every acceptance. No owner word is needed to start these three — they are the acceptance-path reviews already authorized by the package rows (P031 `OD-20260914-P031-BATCH-GO-1` + `OD-20260914-P020-OPUS6-1` "P031 takes its exact Opus after the reset"; P030 `OD-20260914-P030-EXPORTER-GO-1`; P1CAP `OD-20260915-P012-P1FIX-LEAD-1`). The P020 measurement acceptance is NOT in this queue (measurement held for the Grok pre-screen, Sep 18+).

| # | Package | Subject | Brief | Launcher | Prior roster | Est. |
|---|---|---|---|---|---|---|
| 1 | P0-31 | `C:/tmp/P031_M1_20260913` @ `48bd70de` (batch + P31FIX + Lead RED test) | `P031/REVIEW_BRIEF.md` | `P031/opus/run.ps1` | Gemini detection RC → delta PASS-WITH-NITS; Lead ✔; Sol pending (Sep 19) | ~25-40 min |
| 2 | P0-12 Path 1 | `C:/tmp/P1CAP_20260914` @ `af921d75` (Lead-authored P1FIX) + real capture r1 as evidence | `P1CAP/REVIEW_BRIEF.md` | `P1CAP/opus/run.ps1` | Gemini detection RC → delta PASS-WITH-NITS; Lead ✔ (author; does not accept); Sol pending | ~25-40 min |
| 3 | P0-30 | `C:/tmp/P030_INTEGRATION_20260913` @ `daf6a43b` (nits K-01..K-05 OPEN; O9FIX waits for Codex) | `P030/REVIEW_BRIEF.md` | `P030/opus/run.ps1` | Gemini PASS-WITH-NITS; Lead ✔; Sol pending | ~20-30 min |
| 4 (if allowance remains) | P0-26 | `C:/tmp/P026_REPAIR_20260915` @ `6ac9cfb7` (Lead-built completion-marker repair; blocker: P030 adapter isolated root — owner A/B pending; if "A" the candidate gains one more commit before Wednesday) | `P026/REVIEW_BRIEF.md` (written 09:58Z; pinned to `6ac9cfb7`; under option A the Lead re-pins brief + launcher to the new HEAD first) | `P026/opus/run.ps1` (started BY HAND after lanes 1-3, not by `run_queue.ps1`; refuses on HEAD drift) | Gemini corroboration pending; Lead ✔ (author) | ~20 min |
Addendum to lane 2 (P1CAP): the P0-28 eligibility wrapper `capture_own_account_eligibility.py` (Lead-written, reuses the reviewed tool) and its real read `p028-eligibility-20260915-r1` are recorded under `QUEUED_PACKAGES_20260915/P028_ELIGIBILITY_CAPTURE_20260915/`; the P1CAP brief may take it as read-only context ("a second consumer of the same custody primitives") — not a separate lane.

Order rationale: P031 first (largest, longest chain), P1CAP second (owner-facing evidence path), P030 third (nits known; a REQUEST_CHANGES there costs least). If the weekly Pro allowance is exhausted after two, the third waits for the following reset — record it, do not squeeze.

## Before starting each lane
1. `ListAgents` + `tasklist` for `agy.exe`: none. No Gemini call during a Pro lane (the Opus lane runs `git rev-parse`/`show` only, but keep the rule).
2. Verify the worktree HEAD (the launcher refuses on drift) and that no uncommitted change exists in it (`git -C <wt> -c safe.directory=* status --short` must show only the lane TASK files).
3. Start detached: `powershell -NoProfile -ExecutionPolicy Bypass -File C:\tmp\OPUS_QUEUE_20260916\<pkg>\opus\run.ps1`; wait on `launch.exit`; the report is `<pkg>/opus/OPUS_T0_REPORT.md`; the stream is `stream.jsonl`.
4. Adjudicate (grep every citation; reproduce at least one RED arm; write `LEAD_ADJUDICATION_OPUS.md` beside the report); record under CT13 `<package>_OPUS_20260916/`; append the ledger row.
5. A REQUEST_CHANGES → correction brief for Codex (Sep 19) or, with an owner word, the Lead (as on 2026-09-15).

## Serial launcher
`run_queue.ps1` runs 1 → 2 → 3 serially, skips a lane whose `launch.exit` exists, refuses while `agy.exe` runs, and stops on a non-zero exit. It is PREPARED; start it only after 20:00Z on 2026-09-16 and only from the Lead session.
