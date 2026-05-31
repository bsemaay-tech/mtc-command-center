# Scorecard and MTC_V2 Readiness

Date: 2026-05-31

This note documents the dashboard scoring and MTC_V2 readiness layer. It is read-only and does not change
`MTC_V2.pine`, producer specs, parity artifacts, or live-trading settings.

## Strategy scorecard

The 100-point score is a triage score, not a profit forecast.

| Component | Max | Meaning |
|---|---:|---|
| Source coverage | 20 | URL and transcript/source material are present. |
| Rule quality | 25 | Entry/exit rules are deterministic and explicit enough to test. |
| Backtest evidence | 35 | Pipeline maturity, metrics, trades, and parity proof where available. |
| Execution readiness | 10 | Promotion/parity/paper-trade artifacts are attached. |
| Risk / cleanliness | 10 | Penalizes blocked rows, weak source quality, missing source material, and thin rules. |

Bands:

- `85+`: high-confidence triage candidate.
- `65-84`: usable but still needs a gate such as parity, promotion pack, or forward evidence.
- `<65`: review before spending more execution time.

## MTC_V2 readiness buckets

| Bucket | Meaning |
|---|---|
| `READY_FOR_MTC_V2_REVIEW` | Evidence is strong enough to enter a read-only MTC_V2 review queue. |
| `NEEDS_FORWARD_EVIDENCE` | Parity is close/done, but forward paper-trade evidence is still needed. |
| `NEEDS_PINETS_PARITY` | A promoted strategy must pass PineTS/Python parity first. |
| `NEEDS_PROMOTION_PACK` | Backtest evidence exists, but the promotion proof packet is missing. |
| `NEEDS_BACKTEST` | The candidate is eligible but still needs walk-forward/OOS evidence. |
| `BLOCKED_SOURCE_AUDIT` | Source/formula/rule evidence is not safe enough for integration planning. |
| `PARKED_OR_SPLIT` | The row is rejected, wiki-only, or must be split into separate formulas. |
| `LOW_SCORE_REVIEW` | The score is below the useful threshold for MTC_V2 planning. |

## 2026-05-31 calibration result

- `READY_FOR_MTC_V2_REVIEW`: 0 rows.
- Leading candidate: `QL_ALPHA_LINK_8EMA_1H`, score `88/100`.
- LINK is not marked ready because forward paper-trade evidence is incomplete: `0/30` target trades.
- This is intentional. MTC_V2 readiness is stricter than Pipeline progress; it requires evidence after parity, not just a high score.

Generated exports:

- `11_TRIAGE/mtc_v2_readiness_export_2026-05-31.md`
- `11_TRIAGE/mtc_v2_readiness_export_2026-05-31.csv`

## UI changes

- Pipeline has search, score-band, and next-action filters.
- Audit has a score-band filter in addition to the existing column filters.
- MTC_V2 has its own readiness tab with status and score filters.
- Strategy detail pages now include a decision panel: audit status, score, MTC_V2 readiness, and blocker/next action.
- Other dashboard tabs now include short explanations of what decision each tab supports.

## Snapshot cache

The local HTTP server caches `/api/snapshot` briefly in memory to make normal reloads faster. The dashboard
Refresh button calls `/api/snapshot?refresh=1`, which forces a fresh rebuild.
