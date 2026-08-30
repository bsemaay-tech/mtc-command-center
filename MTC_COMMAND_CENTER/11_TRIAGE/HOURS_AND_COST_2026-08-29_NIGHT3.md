# Hours and cost — 2026-08-29 evening → 2026-08-30 dawn (night 3)

Measured from the lane log (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt`, evening block onward).
Times are wall-clock stamps the Lead wrote at dispatch/landing; they are the measurement, and
its pattern is: stamped by the Lead when acting, not by the lanes. USD is NOT MEASURED by the
Lead; the only reading taken was the CodeBurn banner at evening session start
($316.84 day / $5,186.30 month at ~21:00). No closing figure was captured.

## What the night produced (chains, not lanes)

| Chain | Result | Rounds/lanes |
|---|---|---|
| P0-11 repair chain | CLOSED at repair 8b (`bfa074df`) | N49B, P22, N50, N52 |
| P0-11 STAGE 3 | BUILT + audited + repaired + CLOSED (`2eedfb87`); gate STOP by design | N51, G20, P25(b), N58(b), N62(b), N64, N65 |
| Bridge fail-closed | design CLOSED (P20+N48); candidate V1 NOT-CONFIRMED -> V2 CONFIRMED (P21, W50b, P21b); owner V2 approval pending | 5 lanes |
| P0-20 papers | 3 repair rounds + cap fired -> PARKED with one owner question (falsifier #5 oracle defect, Lead-verified) | W54, W59, W60, P23, P26, P27, N54(b), N59, N63, G16, GM2 |
| P0-12 design | 2 repair rounds -> PARKED at round cap (N57b BLOCK) | N45, G17, W55, N53, W56, N57(b) |
| Design drafts | P0-13, P0-21, P0-22, P0-31M1, P0-14 drafted; each has a detection audit (P0-14's landed at dawn, G21); three folds ran at dawn (W64/65/66) | W51/52/53/57/58, G18/G19/G21, P24, N61 |
| Governance | OD-1+OD-2 merged to master (PR #142); promotion rule approved+recorded; 3 Lead self-audits (DS3, N60, + evening feed repairs) all findings accepted | — |
| v3 (stage 4) | design re-pinned (W61 v2c) -> re-pin audited NOT-CONFIRMED (N66b) -> repaired v2d (W68, 8/8); P29 second-actor rebuild ran: measurable identities all match, remaining steps STOP by design | W61, N66(b), W68, P29 |

## Route reality measured tonight

- Codex ×4: all four hit caps at least once (secondary 401-expired then re-authed by owner;
  fourth 01:59; secondary 01:59; third 02:59; free survived longest). Reset-scheduler pattern
  (timed dispatchers + conditional launch) recovered every window.
- Claude Pro: session cap hit ~00:00, reset 02:50; ~5-concurrent held before that.
- Grok: 1 slow-start misdeclared dead by the Lead (G17 delivered), then 3 clean read-only
  deliveries (G18, G19, G20 — G20 found the double_build reintroduction first). Zone confirmed:
  read-only census work.
- Gemini: 2 of 8 runs delivered (GM2, GM3). 6 died on the launcher integrity check tripping on
  `.impeccable\hook.cache.json` churn — TOOL-BLOCKED while this session is active. Owner item.
- OpenCode Go: 0 of 4 tool-using lanes delivered (non-interactive permission gate); 1 no-tool
  probe fine. Benched pending an auto-approve mechanism.

## Lead errors recorded tonight

1. G17 declared dead while it was delivering (corrected in feed after DS3 caught it).
2. "Paper 1 v1.2 delivered" recorded while the W59 report held placeholders (N60-F01; corrected).
3. Evening feed carried 7 stale/overclaimed rows at one point (DS3 5H+4M; all fixed, pushed).
4. Two waiters false-resolved on stale/exit-written files (S16, S6 W60 row); waiter logic moved
   to fresh-report keying mid-night.
5. Time-math slip at 01:41 read as 02:20 (no action taken on it — caught before acting).

## Day-half addendum (11:30 -> ~21:30, same continuous session)

Measured from N_TIMES.txt. Session total ~24.5h continuous orchestration.

- THREE merges today: PR #143 (WP-P0-11, one unit, owner-signed v3), PR #144 (bridge
  fail-closed, KVM2 untouched), PR #145 (promotion report-only diagnostic). Master ended at
  108ea066.
- WP-P0-12: rounds 4-10 (unlock -> loop cap 8 -> owner narrowing round) -> FINAL PARKED at
  design v1.8; detection never clean; nothing built. ~6h of lane spans in the day-half.
- Draft fleet: P0-13 v1.2 (verified), P0-21 v1.1, P0-22 v1.2, P0-31M1 v1.1, P0-14 v1 + G21,
  P0-30 v1 + N79 + DS10, V2A-01/02/03 v1 + G22/G25/G26 censuses. All parked warm.
- Route caps in day-half: Codex 2 quota deaths (recovered), Claude Pro 1 window (17:33-18:02,
  bridged). Apostrophe-trap session tally: 6 lanes.
- CodeBurn banner at wind-down: $544.46 day / $5,850.92 month (banner reading, not a Lead
  measurement; owner budget flag remains open as fact, answered as question 08-29 ruling 6).
