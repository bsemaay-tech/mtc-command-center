# Hours ledger — 2026-08-31 evening -> 2026-09-01 (build night)

Method: wall-clock envelopes from N_TIMES stamps + artifact mtimes. Lanes overlap
heavily; spans are NOT summable effort and NOT owner-billable hours. USD not measured by
the Lead (CodeBurn banner is the source for spend).

| Arc | Envelope (local) | Landings |
|---|---|---|
| Session open + re-verify + W152 inputs attempt | 18:04 - 18:35 | W152 honest BLOCK 0/17 |
| Owner 1a + N104 inventory + fan-out wave 1 | 18:35 - 19:30 | N104 168 packages; 8 census/audit lanes |
| W155 v1.5 addendum + fleet fold/verify cycle | 19:30 - 20:45 | v1.5 COMPLETE-WITH-OPEN-EMBED; W157/158/159 folds; G68-71 verifies |
| Owner 5 words + detection + tables/inputs parallel | 20:45 - 23:00 | G63+GM27 dual-zero; W156 revision; W152B 17/17; G73 zero |
| Lead re-seal + dry-run + THE RUN | 23:00 - 22:40* | seal 02b47a8e; dry-run 17/17; W153 PASS (dispatcher 22:23) |
| Kernel phases A+B (cap-relay) | 22:40 - 02:10 | 10 commits; 278 tests; legacy exact |
| Phase C + adjudication + fixes | 02:10 - 03:10 | W164 honest STOP; G76 12 classes; W165 fixes 293/293 |
| Diff census + close-out | 03:10 - 03:40 | G77 clean grant/fences; ledgers; handoff |

*N_TIMES prefixes are sequence-only; mtimes govern (recorded timebase rule).

Lane count: ~45 dispatched this session (13 codex incl. relays, 18 grok, 1 gemini,
1 MAX Opus, 8 opencode, 4 Lead-act scripts). Codex caps: 5 (all recovered by
probe/dispatcher/partial-audit recipes). Night harvest: ~100 findings folded+verified
across fleet + build tooling + Lead records + kernel adjudication.
