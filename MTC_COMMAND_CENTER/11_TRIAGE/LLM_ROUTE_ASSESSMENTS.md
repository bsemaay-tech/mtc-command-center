# LLM route assessments — per-session ledger

Standing owner rule (2026-08-30, addendum 6 item 16): every session appends its measured
route/model assessment here, newest first. Grades are evidence-based (lane outcomes in that
session's time log), never vibes. This file accumulates route knowledge across sessions.

---

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
