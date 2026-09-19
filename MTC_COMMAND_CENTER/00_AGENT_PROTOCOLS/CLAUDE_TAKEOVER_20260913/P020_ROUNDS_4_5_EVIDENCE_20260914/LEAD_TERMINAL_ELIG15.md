# LEAD_TERMINAL — P020 V1.5 one-shot eligibility run (ELIG15) — 2026-09-14 10:45Z

**Outcome: the preregistered one-shot ran end-to-end and returned `BENCHMARK_PROFILE_BLOCKED: no complete matching of 5 distinct families to 5 timeframes`. Both reserved outputs hold ABORTED records (`error: BENCHMARK_PROFILE_BLOCKED`); the shot is spent. This is the fail-closed outcome the owner accepted in D1 Option A ("a false block is more likely; a false block ends as BENCHMARK_PROFILE_BLOCKED ... and comes back to you"). No selection exists. Nothing was silently substituted.**

## Run record
- 10:33:59Z gate passed: roster (Opus R5 PWN, Sol R5 PWN, Gemini SATISFIED, Lead REPRODUCED, Grok NITS), identities (HEAD b9b72f85…, frozen b7548984…, procedure 54f35c8c…, tests b8803172…), no prior outputs (V1.4 ABORTED files archived under the owner's reset ruling); 96 tests passed.
- 10:34:02Z `--oneshot --i-have-t0-review-authorization b7548984…` → exit 2 after 2 s: `BENCHMARK_PROFILE_BLOCKED: no complete matching of 5 distinct families to 5 timeframes` (captured in `oneshot_stdout.txt` — the launcher's capture fix worked).
- Outputs (package dir): `PRESELECTION_CALIBRATION.json` (91 B, sha256 2c016a7c…) and `PRESELECTION_ELIGIBILITY.json` (91 B, sha256 d7f4e4bb…), both `{"error": "BENCHMARK_PROFILE_BLOCKED", "kind": ..., "status": "ABORTED"}` — the phase table's "post-both-reservations transaction failure: no complete matching (`BENCHMARK_PROFILE_BLOCKED` raised before eligibility trials)" case. By design the binary matrix is NOT persisted on this path, so the record does not say which timeframe(s) had no trade-bearing family.
- Timing: 45 calibration cells in ~1.4 s is consistent with the engine's per-cell cost (a single real cell measured at 0.03 s in the diagnostic below); all 45 cells ran; the 15 locked trials were never reached.

## Lead diagnostic (disclosed; bounded)
Before concluding "environmental defect vs genuine block", the Lead ran ONE real calibration cell (family 1 `GEN_TRIPLE_EMA_STACK` × 15m, rows 2049-4096) through `trade_bearing_gate` in the scratch copy `C:/tmp/P020_PRESELECT_LEAD_REPRO_V15_20260913/` with the real preflight, real plan and real dataset bytes: **TRADE-BEARING (gate passed), 0.03 s**. So the real stack accepts the real frames (no schema/record/interval refusal — the V1.4 class of failure is gone) and the block is a genuine matrix outcome: at least one timeframe has no eligible family among the nine. Only this one cell was evaluated outside the tool; no other matrix cell, no matching, no trial was computed. Data-quality scan of all five windows (read-only): 0 NaN, 0 empty fields, monotonic timestamps, 0 duplicates.

## What must NOT happen without an owner ruling
- No second selection, no re-run, no rule change after this result (D1 text; prereg §(g)). The ABORTED files stay (never deleted).
- The Lead will not compute the rest of the matrix; the D1 text and the prereg forbid selecting on visible results, and the tool deliberately discards the matrix on BLOCKED.

## Owner decision D7 (see OWNER_DECISIONS_PENDING.md)

## D7 A — owner-authorized bounded diagnostic (chat "D7- A", ~10:55Z) — executed 10:58Z
Scratch copy, real preflight/plan/dataset bytes, no token, no matching, no selection, no economic value; family identities withheld/redacted.

| timeframe | calibration rows | trade-bearing families (of 9) | block reason class (all blocked cells) |
|---|---|---|---|
| 15m | 2048 | **4** | `no actual trade-bearing 2.1.0 successor result` |
| 1h | 2048 | **0** | same |
| 2h | 2048 | **0** | same |
| 4h | 2048 | **1** | same |
| 1D | 361 | **0** | same |

Reading: the block is not the 1D-only "false block" D1 anticipated — three timeframes (1h, 2h, 1D) have NO trade-bearing family and 4h has one; every blocked cell fails the same economic-path clause (`num_trades <= 0` / no committed event list), never a record/interval/schema refusal. Nine trend/breakout families producing zero trades on 2048 hourly and two-hourly BTC bars points at the sizing/profile path (synthetic instrument `quantity_step = 1`, `point_value = 1` at BTC prices, owner-policy sizing) or at the successor's event projection, rather than at the strategies themselves — a hypothesis for the next bounded diagnostic (D8), not a finding.

## D8 A — owner-authorized bounded diagnostic (chat "D8 A", ~11:05Z) — executed 11:08Z
Per timeframe (identities withheld; no P&L): signal counts per family and the fill outcome under the frozen profile.

| tf | rows | families with ≥1 entry signal | signal counts (sorted) | fills (trade-bearing) | classification |
|---|---|---|---|---|---|
| 15m | 2048 | 8 of 9 | 0,2,7,26,27,38,57,65,166 | 4 | 4 SIGNAL→FILL, 4 SIGNAL_NO_FILL, 1 NO_SIGNAL |
| 1h | 2048 | 8 of 9 | 0,3,5,18,27,31,50,53,140 | 0 | 8 SIGNAL_NO_FILL, 1 NO_SIGNAL |
| 2h | 2048 | 8 of 9 | 0,3,4,28,29,29,40,53,157 | 0 | 8 SIGNAL_NO_FILL, 1 NO_SIGNAL |
| 4h | 2048 | 8 of 9 | 0,1,1,27,32,36,42,63,190 | 1 | 7 SIGNAL_NO_FILL, 1 fill, 1 NO_SIGNAL |
| 1D | 361 | 3 of 9 | 0,0,0,0,0,0,1,1,30 | 0 | 6 NO_SIGNAL, 3 SIGNAL_NO_FILL |

Mechanism (read from the pinned kernel, no execution needed): the frozen profile sizes positions by `RISK_AT_STOP` with `requested_risk_fraction = 0.0001` (P020 owner policy `OD-20260912-P020-VALUES-1`) and floors the quantity to the instrument's `qty_step` (`mtc_v2/core/instrument.py:415-416` → `rounding.py:139-145`, ROUND_DOWN), where the synthetic instrument record carries `quantity_step = 1` (`InstrumentMetadata lot_size=Decimal('1.0')`, `PackageMetadata(qty_step=Decimal('1.0'))`). At BTC prices ($50k-$126k) with a 0.01 % risk fraction, the risk-derived quantity is far below one whole contract on hourly-and-slower stop distances, so it floors to 0 and no order is placed — "no actual trade-bearing 2.1.0 successor result". 15m's tighter stops let four families reach one contract. The strategies DO signal (8 of 9 on 1h/2h/4h). Conclusion: the preregistered eligibility test is currently dominated by a lot-quantization artefact of the synthetic instrument (venue-realistic BTC step is 0.00001 per the closure matrix row I-3), not by strategy behaviour. The same artefact would block the 15 locked measurement trials (rows 1..2048) — so it must be resolved for P020 to produce any measurement at all.
