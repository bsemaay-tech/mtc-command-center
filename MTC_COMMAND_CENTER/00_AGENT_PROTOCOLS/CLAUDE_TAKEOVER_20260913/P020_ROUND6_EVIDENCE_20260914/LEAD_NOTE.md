# WP-P0-20 preselection — round 6 (V1.6, owner D9-A) evidence — 2026-09-14 (Claude Opus 5 Lead, session b9df29)

| Step | Route | Time (Z) | Result | Record |
|---|---|---|---|---|
| V1.6 build (lane P20R7) | Codex Plus gpt-5.5 high | 15:08-15:22 | record V3 (`quantity_step` 1 → 0.00001; sha `69b6f246…`), plan/driver re-pin, `tests/test_sizing_floor.py` (5 timeframes V3 GREEN / V2 RED), runbook/prereg pins, re-freeze **V1.6 `cb75602080850873e28dc3aa268ad1072a0f1d50148d91ad75c9896cf37fb126`** twice byte-identical, derivation tool re-pinned; 106 tests | `REPORT_R7.md`, `SHA256SUMS.txt`, `TASK_P20R7.md` |
| Lead reproduction | Lead | 16:13-16:16 | REPRODUCED — SHA 13/13, 106 tests, deterministic freeze = builder = package, V3 vs V2 diff exactly record_id/quantity_step/provenance, frozen key diff V1.5→V1.6 only version/digest/pin keys (family_order, selection_rule, calibration_windows, measurement_inputs EQUAL), PLAN_VALID, derive 15 tests + pin = V1.6; **per-timeframe real-cell smoke** (family_order[0]): 15m/1h/2h/4h TRADE-BEARING, 1D BLOCKED (no signal) | `LEAD_REPRODUCTION_V16.md`, raw output, scripts |
| V1.5 shot outputs | Lead | 16:17 | both ABORTED files moved (digest-verified) to `P020_ELIGIBILITY_RUN_V15/ABORTED_ARCHIVE/` under D9-A (new shot); never deleted | `V15_ABORTED_ARCHIVE_NOTE.txt` |
| Gemini 3.7 corroboration | Gemini (chain v2; attempt 1 GUARD race archived) | 16:30-16:36 | **PASS**, 0 findings, 63/63 native reads verified, whole packet read; V1.5→V1.6 diff and D9-A corroborated from bytes | `gemini/` |
| Exact Opus R6 | Claude Pro `claude-opus-5` xhigh (the week's last slot, `OD-20260914-P020-OPUS6-1`) | 16:37- | running at recording time | round-6 dir `opus/` (recorded when terminal) |
| Exact Sol R6 | Codex Plus `gpt-5.6-sol` xhigh | queued for the 20:10Z pool reset (`codex_reset_queue_r6.ps1`) | pending | — |
| Grok pre-screen | — | — | NOT AVAILABLE (SuperGrok weekly cap until 2026-09-18); supplemental slot vacant, recorded in the one-shot launcher gate | — |

One-shot V1.6 launcher prepared: `C:/tmp/CLAUDE_P0_RUN_20260913/p020_eligibility_run_v16.ps1` (+ wrapper) — gates: Opus R6 + Sol R6 accepting, Gemini SATISFIED for V1.6, Lead REPRODUCED, HEAD `b9b72f85…`, frozen = token `cb756020…`, procedure/test digests, no prior outputs, no agy. Runs only when the Lead starts it after the roster accepts. Selection rules unchanged since V1.1; nothing executed on real data beyond the disclosed smoke.

NOT VERIFIED: the 45-cell matrix and the 15 trials (the shot); whether 1D has any trade-bearing family under V3 (if none, `BENCHMARK_PROFILE_BLOCKED` returns and the owner's D7 options B/C/D come back); Opus and Sol verdicts (pending at recording time).
