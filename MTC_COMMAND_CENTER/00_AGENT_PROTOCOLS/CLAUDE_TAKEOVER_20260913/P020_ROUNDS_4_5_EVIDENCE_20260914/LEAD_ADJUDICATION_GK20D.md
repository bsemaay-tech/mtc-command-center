# LEAD_ADJUDICATION — GK20D (Grok pre-screen of V1.5) — 2026-09-14 08:08Z

`GROK_V15_VERDICT: NITS` (07:31-07:58Z; 96 + 5 + 15 tests reproduced; real-stack detect-0 arm run; RED probes 1-6b). Closure table: T1-T4, S1-S5, NIT-1/4, R1-R6, N4-1..N4-4, Sol-4, the new interval check, D5 and the derivation tool all CLOSED / present with file:line; selection rules, family order, canonical bytes, windows, prefixes unchanged V1.4→V1.5. No REQUIRED.

| # | Grok NIT | Lead check | Disposition |
|---|---|---|---|
| 1 | `open(path,"xb")` is an exclusive create, not a lock; commit truncate now removes residue but a concurrent writer can still occupy the reserved file before commit | unchanged class (GK20B/C, Opus N4-2, Sol-2); mitigated by truncate | residual, not a re-freeze trigger |
| 2 | cost/funding records and the plan's `records.effective_interval` text + runbook sentence still carry the V1 end date `2025-09-22T08:00Z`; only the instrument record was extended | Lead END-TO-END smoke (LEAD_REPRODUCTION_V15.md addendum): real driver + real engine + real records on a synthetic in-range frame → GATE PASSED; only `instrument.py` enforces an interval (grep) | documentation residual inside pinned artifacts (plan text, runbook, cost/funding metadata) — fold into the next reviewed change; not enforced, not a blocker |
| 3 | the packaged smoke test checks window starts + prefix row 1 only, hardcoded runtime_config, not last_ts/all prefixes | CONFIRMED weaker than the freeze check; the freeze-time check itself covers first+last of all 10 windows/prefixes (Lead arm 40/40) | test-strength NIT — next batch |
| 4 | prereg §(d) still cites `preselect_profile.py:456-522` (now `:549-629`) and the gate/frozen text cites `:459-493` (driver now `:460-504` after D5) | CONFIRMED (Grok opened the lines); N4-1 partially addressed | documentation NIT — next batch |
| 5 | driver family-set tests depend on ROOT matching the plan's absolute instrument path (pass only from the benchmark dir) | CONFIRMED by Grok's copy run | test-portability NIT — next batch |

Disposition: pre-screen clean of REQUIRED; five NITs recorded as residuals for the next reviewed change. Roster for V1.5 so far: Lead REPRODUCED (+ end-to-end smoke), Grok NITS, Gemini PASS; Opus R5 running (Pro); Sol R5 queued (10:06Z). Adjudicated by Claude Opus 5 Lead (session 2c48d1).
