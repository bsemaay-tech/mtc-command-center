# LLM route assessments — per-session ledger

Standing owner rule (2026-08-30, addendum 6 item 16): every session appends its measured
route/model assessment here, newest first. Grades are evidence-based (lane outcomes in that
session's time log), never vibes. This file accumulates route knowledge across sessions.

---

## Session 2026-08-29 21:00 → 2026-08-30 ~21:30 — DAY-HALF ADDENDUM (same session, appended at wind-down)

Evidence base: N_TIMES.txt 11:30→21:30 block (~30 further lanes). Grade deltas vs the morning
entry below; unchanged routes not repeated.

| Route | Delta | Measured evidence |
|---|---|---|
| Gemini 3.7 Flash | C+ → B | After the owner-authorized launcher fix: 5 further clean deliveries (GM6 papers-closure corroboration, GM8 v3 corroboration, G25 census 10 findings, G26 census 6 findings incl. a clean special-check, one relaunch after an apostrophe-trap death). Zero tool-losses post-fix. Still corroborator/census only — no runtime detection. |
| OpenCode Go | B− → B | In-cwd packet pattern held: DS6 (v3 detection, zero findings, legitimate), DS10 (P0-30 supplemental: 6 NEW findings — 2M/4L — with ZERO overlap against Codex N79's 8; different family genuinely widens coverage). New trap measured: plan-agent completes analysis then STOPS at a write-confirmation prompt and exits rc=0 without writing the deliverable — Lead transcribed verbatim with a provenance note. For file-writing deliverables use build-agent or accept log-transcription. |
| Codex ×4 | A (confirmed) | Carried P0-12 rounds 4-10 detection (N72..N82: detection out-found the flagship in EVERY round — 10+ consecutive detection wins now), promo detection N76, final v3 round N68 zero-findings grade held honest. 2 further quota deaths, both recovered by reset-dispatchers. |
| Claude Pro | A (confirmed) | Flagship audits P32..P43 + all design/fold/narrow writer lanes; one cap window (17:33-18:02) bridged by the reset-dispatcher. Authorship limit measured: 10 rounds could not write P0-12's design to detection-clean — family exhaustion is real, not a lane failure. |

Dispatch-trap tally for the whole session: apostrophe-in-inline-prompt killed 6 lanes
(N66c, N68-dispatcher, GM6, P42, G26, DS10-wave15-never-launched). HARD RULE proven again:
spec-file for EVERY dispatch, zero exceptions — the last three deaths were Lead violations of
its own ban under time pressure.

## Session 2026-08-29 21:00 → 2026-08-30 ~11:30 (overnight + morning; Lead: Claude Fable 5 MAX)

Evidence base: `C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt` (this session's block) and the lane
reports it cites. ~45 lanes dispatched across 7 routes.

| Route | Grade | Measured evidence |
|---|---|---|
| Codex ×4 accounts (gpt-5.6-sol) | A — essential workhorse | Built stage 3, the bridge, every code repair; best detector in the fleet (N-lanes out-found the flagship 8 times, always by probing). 8 quota deaths mid-lane; survivable ONLY because 4 accounts = 4 separate reset clocks + reset-scheduler pattern. |
| Claude Pro (claude -p lanes) | A — essential co-lead | Authored every design/paper/repair text; flagship audits graded honestly. ~5 concurrent held. Weakness: a capped lane dies silently mid-report (W59 placeholder report caused the session's worst record error). |
| Claude MAX (Fable, orchestrator) | n/a by role | ~40 waiter cycles, ~35 dispatches, 3 self-audit rounds accepting 24 findings against the Lead's own records. From addendum 6: auditor-fallback allowed under the shared-pool guard. |
| Grok (SuperGrok) | B — narrow but real | 4 clean read-only census audits; G20 found the stage-3 double_build reintroduction FIRST by pure reading. 2 deaths; slow starts mimic death (a wrong Lead death-call recorded). Zone: read-only census/detection with a watcher; never execution lanes. |
| Gemini 3.7 Flash (read-only launcher) | C+ — insurance, not discovery | 4 successes / 7 tool-losses (launcher integrity check vs .impeccable churn — fixed this session with an owner-authorized one-line ignore). Wins are independent CONFIRMATION (GM2 fully reproduced the papers BLOCK). GM7 said PASS where runtime detection found a HIGH — reading-only cannot catch runtime defects. Keep as OD-1 corroborator; never acceptance. |
| OpenCode Go (deepseek-v4-flash / glm-5.3-flash / kimi-k3) | B− — newly proven | 4 lanes lost to harness misuse (root cause found: reads OUTSIDE the lane cwd hit the non-interactive permission gate; fix = in-cwd packets). First real audit (DS5, deepseek-v4-flash) produced 3 legitimate findings, 2 entered a repair union. Build-agent writes unproven. |
| OpenRouter | not exercised | Zero calls; no volume-mechanical task arose. No verdict. |

Operational lessons that transfer: (1) 4-family parallel audit packets (Codex+Claude+Grok+
Gemini) cost zero wall-clock and found real defects the primary pair missed twice; now the
default. (2) Every route caps under max-parallel — timed reset-dispatchers with conditional
launch recovered every window. (3) PS5.1 dispatch traps (unquoted Start-Process args; nested
-Command quoting; apostrophes in inline prompts; stderr-wrap under *> with EAP=Stop) killed
5 lanes; dedicated launch-script files are the only safe pattern.
