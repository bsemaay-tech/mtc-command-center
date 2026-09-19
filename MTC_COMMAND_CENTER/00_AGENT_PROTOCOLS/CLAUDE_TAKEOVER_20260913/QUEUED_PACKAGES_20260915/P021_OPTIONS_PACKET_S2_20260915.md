# WP-P0-21 — options packet S2: the measure-first numbers the owner can close now (`gap_ratio_max`, the gap-ratio formula and dataset-digest pins, the divergence metric) — 2026-09-15 night

Prepared by the Claude Opus 5 Lead (session 5, `03c6c8`) as slice S2 of `P021_GAP_TABLE_20260915.md`. **Nothing here changes code; every closed number would be recorded as policy v1, provisional and reversible, exactly like the twelve numbers closed on 2026-09-07 (`p021_readiness_rules.py` `CLOSED_NUMBERS`).** Decision 6 A of 2026-09-12 ("keep unset, measure-first; return an evidence-backed options packet after the relevant measurement") is what this packet answers for the items whose measurement exists.

## 1. `gap_ratio_max` (blocker B-02) — the 2026-09-08 packet stands; one more measurement is added
The options packet `C:/tmp/P021_GAP_RATIO_MAX_POLICY_20260908.md` (Lead, 2026-09-08; Gemini 3.8 + Grok 4.6 reviewed the T1 measurement packet) was never answered — no `P021_DECISION_3` row exists in CT13 `DECISIONS.md`, the takeover records or RUN_STATE. Its content is unchanged and re-presented verbatim in substance:

| Measurement | Value | Source |
|---|---|---|
| 17 Binance Futures 5m series, 2024-01-01 → 2026-05-03, 300 s step | **4,105,966 bars; 0 series with an internal gap event**; `m1`/`m2`/`m3` min = median = max = 0.0; one series (POLUSDT) with 73,875 *leading* absent slots (coverage, not a gap) | `P021_COHORT_MEASUREMENT_20260907/MEASUREMENTS.json` (two independently written drivers agreed) |
| 93 derived files, 17 assets, 15m/1h/2h/4h/1D (the P0-20 derived datasets) | **4,477,626 rows; zero timestamp gaps** (timestamp-only scan; proves neither volume validity nor candle closure) | `01_MTC_PROJECT/docs/optimization/DATASET_AND_REGIME_USAGE_RULES.md:6` on `master` ("Bundle reports confirm 93 datasets, 17 assets, 4,477,626 rows …"); restated in `P021_P030_OWNER_DECISION_PACKET_20260912.md` §2 (decision 2) |

| Option | `gap_ratio_max` on `m2_missing_bar_ratio` | What it forbids | Characteristic failure |
|---|---|---|---|
| Z zero tolerance | `0.0` | any internal gap refuses the series | false FAIL on the first venue outage ever seen |
| **T one-bar tolerance — RECOMMENDED** | `0.0001` (≈ 24 missing bars in a 245,873-bar 5m series; ≈ 2 h of 5m data) | more than a handful of missing bars | a small cluster of holes passes |
| L loose | `0.001` (≈ 246 bars; a missing 5m day = 288) | only visibly broken series | a nearly-whole missing day nearly clears |
Both scans measured exactly `0.0`, so **no option is data-calibrated**; T and Z admit the same 110 series today; the choice is an appetite for unseen gapping. Companions (measured, not invented): `gap_ratio_metric = "m2_missing_bar_ratio"` pinned explicitly; **coverage is a separate rule** (`requested_period_coverage`) — leading/trailing absence must refuse on its own, never through `gap_ratio_max`.

**Ask (one line):** `P021_DECISION_3 = Z | T | L` (recommended **T**), optionally `P021_GAP_METRIC = m2` (default).

## 2. B-17 — the gap-ratio formula identity (a pin, not a number)
The design's blocker B-17 asks for `gap_ratio = f(...)` with numerator, denominator, calendar and bounds. The merged helper already computes the three candidates under fixed-step 24/7 semantics (`03_QUANTLENS/tools/data_gap_ratio.py`; `TIMEFRAME_SECONDS` is the single owner of the step; tests `tests/test_data_gap_ratio.py`): `m1 = gap_event_count / (observed_bar_count − 1)`, `m2 = missing bars in counted gaps / expected bars over the observed span`, `m3 = missing seconds / observed span seconds`. **Ask:** ratify `gap_ratio_formula_id = "m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, leading/trailing absence excluded)"` — recommended, because it is the formula the code already has and the one denominated in the units the engine consumes. Without this pin `P021.DATA_QUALITY` stays BLOCKED even after §1.

## 3. B-13 — which digest satisfies `dataset_hash_required` (a pin, not a number)
Three digests exist and the 2026-09-12 packet forbids silently equating them: the P0-21 `ds-v1` identity (`{contract: "ds-v1", digest: <bare hex>}`, emitted by the B1 producer and required by `require_ds_v1_digest`), P0-20's six-member `evaluation_run_hash` / `dataset_manifest_sha`, and P0-30's provenance-manifest hash. **Ask:** ratify that `P021.DATA_QUALITY.dataset_hash_required` is satisfied by the **`ds-v1` digest of the bundle the check actually scanned** (recommended: it is the identity of the bytes the scanner read; the P0-20/P0-30 hashes identify other objects and stay separate fields where a consumer needs them). Consequence: the DATA_QUALITY measured-value object carries `dataset_manifest_hash = <ds-v1 digest>` and names the contract.

## 4. B-05 — the backtest-vs-forward divergence metric (definition options; tolerance stays measure-first)
The plan leaves the metric `[OPEN]`; decisions 3 A/6 A keep divergence required only from `TESTNET_PAPER_ELIGIBLE` upward and its numbers unset until shadow evidence exists; the pair key is fixed (instrument, entry-bar timestamp, intent id). The **definition** can be chosen now so that the shadow windows record the right thing:
| Option | Metric | Unit | Pros | Cons |
|---|---|---|---|---|
| **M-A — RECOMMENDED** | per-pair signed difference of realized trade return (forward − backtest), aggregated as the mean over the aligned window, reported with the count and the standard deviation | return fraction per trade | directly the quantity the owner cares about (did forward behave like the backtest); pairs by intent id so slippage/fees enter honestly | needs ≥ N pairs (B-07 min pairs) before it is stable |
| M-B | intent-level agreement rate: share of backtest intents that the forward path produced at the same bar (entry/exit decisions match), independent of P&L | fraction | robust with few trades; catches signal drift before P&L does | says nothing about fills/costs |
| M-C | both — M-B as the gate on signal fidelity, M-A as the economic divergence, each with its own tolerance | — | separates "different decisions" from "same decisions, different economics" | two tolerances to ratify later (B-06 becomes two numbers) |
**Ask:** `P021_DIVERGENCE_METRIC = M-A | M-B | M-C` (recommended **M-C**: the two failure modes are different and the shadow window can record both at no extra cost). Tolerance (B-06), window length and minimum pairs (B-07) stay measure-first exactly as decision 6 A says — this packet asks for none of them.

## 5. What closing these does and does not do
- Closes: the two open numbers/pins of `P021.DATA_QUALITY` (B-02 value, B-17 formula, B-13 digest) → the check can reach `PASS` on a real bundle once the P0-12-gated producer exists (B-01 unchanged); the divergence metric's *definition* (B-05) → the shadow window schema can be fixed.
- Does not close: B-01 (P0-12 acceptance), B-06/B-07 (measure-first), B-04 risk-unit source, B-08/B-12/B-16 record hygiene (S1), B-09/B-11/B-15/B-22 (S3), and no readiness or acceptance of any candidate.
- Engineering after the answers: catalogue update (`OPEN_NUMBERS` → `CLOSED_NUMBERS` rows with the policy-v1 provenance text; `missing_rules` for B-13/B-17 removed) = one small T1 change with a RED/GREEN (the reporter must stop refusing on those names) — part of S1.

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`). Nothing here is a decision; the four asks are the owner's.
