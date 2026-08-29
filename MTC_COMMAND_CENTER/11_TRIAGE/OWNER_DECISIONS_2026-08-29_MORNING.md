# Owner decisions — 2026-08-29 morning (verbatim + mapping)

Owner's message (verbatim): "my ansvers are below / 1 freeze, 2 document, 3 correct,
4 writer-populates, 5 safe-reconcile, 6 preserve, 7 no blanket Max, 8 required guard,
9 correct docs, 10 fail closed, 11 controlled flatten policy but no arming yet,
12 deliberate migration only." Plus: "make as much paralel lanes as possible and keep updating
package status so codex can update dasboard."

Ask numbering = the repaired `MORNING_REPORT_2026-08-29_NIGHT2.md:594-660` (asks 1..12 in file
order, N31 renumbering, P10-confirmed).

| # | Ask | Owner answer | Lead action |
|---|---|---|---|
| 1 | Registry rebuild freeze + one-line guard | **freeze** | Freeze stands: NO registry rebuild, NO rewrite of the 44 mis-labelled files. Guard BUILD dispatched (lane W1) per `SPEC_READY_REGISTRY_GUARD.md` with the DEFER stored-data choice: stored 41-file set untouched; guard refuses to promote on labels the checks never granted. |
| 2 | Range Filter | **document** | Option A+B lane dispatched (W2) per `LANE_READY_RANGEFILTER_OPTION_AB.md`: test + limitation entry, zero behaviour change, `range_filter.py` untouched. |
| 3 | Gate scorecards (stamps + hardcoded flag) | **correct** | Lane W34: fix hardcoded `regime_breakdown_present = True` (mega_walk_forward.py:1204) to a computed value with falsification test, and neutralise the existence-stamps per Option B of `OWNER_DECISION_SEVENTH_PATTERN.md`. No stored scorecard rewritten (freeze). |
| 4 | Forward-paper queue inert | **writer-populates** | Lane W34 (same lane): scorecard writer populates the two numbers the queue reads. Queue code unchanged. Existing "forward paper candidate" folder labels remain non-evidence (guard from ask 1 enforces). |
| 5 | Stale working copy (270 behind, 1 ahead) | **safe-reconcile** | Lead executes in-session: rescue the local commit + dirty state onto a pushed rescue branch, then bring the checkout to current master. Nothing discarded. |
| 6 | Frozen Pine tag carries two live alert calls | **preserve** | No action. Tag stays as history. Recorded. |
| 7 | Claude Max permission | **no blanket Max** | Max remains orchestrator-only. No Max audits/build lanes without a per-instance owner grant. Recorded in memory. |
| 8 | Pine alert guard required check | **required guard** | DONE 2026-08-29: ruleset 21444962 now requires both `Bridge suite (Python 3.12)` and `pine-alert-guard` on master. Detector-hardening (Workstream B) remains NOT authorized — owner approved only the settings change. |
| 9 | Safety sentence in older survey (mainnet lock never reached; protection = hardcoded testnet) | **correct docs** | Doc-correction lane queued (W9, next wave): make explicit that protection is the hardcoded `network="testnet"` (`bridge/app.py:203`), not the mainnet triple-lock. |
| 10 | Bridge settings not read by running code | **fail closed** | Authorized: bridge refuses to start on a setting it does not implement. Code lane queued (W10, next wave — design-first per DESIGN_DEFECT_PATTERNS). Build + tests + PR only; NO deploy to any host (host actions stay owner-gated). |
| 11 | Kill-flatten | **controlled flatten policy but no arming yet** | Lane W1112: produce the controlled-flatten policy + deliberate-migration runbook package on top of `DESIGN_P5_SCHEMA_MIGRATION.md` (audited 0 HIGH). NO arming, NO migration execution, NO host action. |
| 12 | 11+1 inert controls / schema migration | **deliberate migration only** | Same package as 11: migration happens once, deliberately, with backup, on a future owner go — this session prepares only the runbook. |

Standing constraint refreshers honoured: no `mtc_v2/**` behaviour change (W2 touches only its
test + feature-contract doc, per its authorized paste-ready spec); no broker/host/TESTNET action;
no push of the P0-11 branch; master changes only via PR with CI.
