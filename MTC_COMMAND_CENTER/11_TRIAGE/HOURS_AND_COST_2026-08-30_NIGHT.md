# Hours ledger — night session 2026-08-30 21:45 -> (open)

Method: wall-clock spans of lane dispatch/landing stamps in
`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt`. Lanes overlap heavily: spans are NOT summable
effort and NOT owner-billable hours. USD is not measured by the Lead; the only USD figures the
owner sees come from his CodeBurn banner (session start banner read $576.95 day /
$5,883.41 month).

| Package / activity | Span (wall-clock) | Lanes | Notes |
|---|---|---|---|
| Session bring-up (probes, specs, feed, Wayfinder rev-1) | 21:45-22:30 | Lead only | all 5 routes probed alive; Claude Pro capped until 23:00 |
| WP-P0-12 fresh-family design | 21:55 -> open | W93 (codex/secondary, xhigh) | addendum 13 |
| Fold wave (P0-14, P0-30, V2A-03) | 21:55 -> open | W95/W96/W99 (codex free/third/fourth) | |
| Fold wave (P0-13, V2A-01, V2A-02) | queued 23:02 | W94b/W97b/W98b (claude pro) | Pro cap death at 21:56 launch |
| Verify censuses (P0-31M1 v1.1, P0-22 v1.2) | 22:05 -> open | G27/G28 (grok), GM11b (gemini, relaunched 22:35 after quote-trap death) | wave-15 fold verify debt |
| Supplemental reviews (P0-21 v1.1, P0-13 v1.2) | 22:15 -> open | DS11 (glm-5.3-flash), DS12 (deepseek-v4-flash), sequential chain | |
| Promotion diagnostic run (display only) | 22:05-22:15 | Lead local | 984 candidates, zero full-PASS |

| P0-12 fresh chain | 21:55-22:38 design (W93 died 21:58 + W93b) -> 22:40-23:16 4-family audit (G29/GM13b/DS13/P44) -> 23:17 repair r1 (W105, open) | codex secondary + grok + gemini + opencode + claude | flagship REQUEST_CHANGES, no blocker |
| P0-30 two cycles | 21:55-23:00 (W96 -> N83+G30 -> W102 -> N87 clean) | codex x2, grok x2 | CONVERGED |
| P0-31M1 five cycles | 22:05-23:22 (G27+GM11 -> W100 -> N85+G31 -> W104 -> N88 -> W106 subtractive -> N90 TERMINAL PARK) | codex x4, grok x2, gemini | PARKED v1.4, stopping rule |
| P0-22 two cycles | 22:05-23:28 (G28+GM12 -> W101 -> N86 -> W109) | codex x3, grok, gemini | CONVERGED v1.4 |
| P0-13 / P0-14 / V2A-01 | fold + verify cycles, 21:55-23:33 | claude x3 + codex + grok x2 + gemini | ALL CONVERGED |
| V2A-02 / V2A-03 | folds + verify pairs, 21:55 -> open (W110 running; G34 running) | claude x2, codex x3, grok x2, gemini | in flight |
| P0-21 | DS11 review -> W108 fold -> N92+GM15 verify pair (open) | opencode + codex x2 + gemini | GM15 clean; N92 pending |

Update cadence: on each waiter landing cycle. Final roll-up at session close feeds the
status-feed `session_time_report`, this file, and the Wayfinder hours CSV.
