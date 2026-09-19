# WP-P0-21 — design draft v1.6 fold note (what v1.5 must say after the 2026-09-07 / 09-12 decisions and the merged slice) — 2026-09-15 night

Prepared by the Claude Opus 5 Lead (session 5, `03c6c8`) as the preparation half of slice S1 in `P021_GAP_TABLE_20260915.md`. **This note edits nothing**: the design draft v1.5 lives outside the repository (`C:/tmp/OC_P021_V15_VERIFY/P021_DESIGN_DRAFT_V1.md`, 70 KB); v1.6 should be produced by applying the rows below to that file and placing the result under `11_TRIAGE/` so the catalogue can cite a repository path. Each row names the v1.5 text to change, the authority, and the exact replacement intent.

## A. Header and verdict
| v1.5 text | Change to | Authority |
|---|---|---|
| "**Version:** v1.5 (2026-08-31)…" | add "v1.6 (2026-09-1x) folds the 2026-09-07 policy decisions (`P021_DECISION_1 = A`, `P021_DECISION_2 = balanced`), the 2026-09-12 decisions 1/2/3/6 (`OD-20260914-P021-P030-RECORD-1`), and the merged slice PR #188 `ca2f8a68`" | the two decision records |
| "**Design verdict:** DRAFT COMPLETE; BUILD BLOCKED … No check code or fixture was executed." | "DESIGN + a merged rule catalogue and evidence contracts; BUILD of the evaluator still BLOCKED on B-01 (P0-12). Executed: the catalogue self-check, 103 tests post-merge (PR #188 record); no real candidate evaluated." | `P021_P030_HANDOFF.md` |
| "**Finding count:** 20 total: 17 named build blockers (B-01..B-17) and 3 discrepancies" | "22 blockers (B-01..B-17 + B-19..B-22 added by the 2026-09-12 packet; B-18 not used) and 3 discrepancies; state table in §Open questions" | catalogue `missing_rules` names |

## B. Check catalogue — per check
| Check | v1.5 says | v1.6 says |
|---|---|---|
| `P021.LOOKAHEAD_PREFIX` | "Which decision-time universe is authoritative … remain blocker B-12" | "B-12 DECIDED 2026-09-12 (decision 1): the fixed CLOSED-bar decision universe = union of full-series and prefix decisions; a one-sided mismatch fails; an empty union blocks — implemented by `p021_evidence_contracts.compare_lookahead`; the T0 roster of the contract slice is recorded as [exact Sol delta PASS; full T0 roster: NOT ESTABLISHED — S1 item 1]" |
| `P021.REPAINT_CLOSED_BAR` | "The exact proof artifact accepted for that runtime fact remains blocker B-16" | "B-16 DECIDED (decision 1): a runtime-emitted immutable closed-bar receipt bound to candidate/package/deployment/dataset/intent/runtime-code/instrument/timeframe/producer — `validate_closed_bar_runtime_receipt`; the five-branch outcome rule unchanged" |
| `P021.DATA_QUALITY` | `gap_ratio_max` B-02, formula B-17, hash B-13 open | keep OPEN but add: "measurements exist (17 × 5m: 4,105,966 bars, 0 internal gaps; 93 files: 4,477,626 rows, 0 gaps); options packet `P021_GAP_RATIO_MAX_POLICY_20260908.md` re-presented as S2 (`P021_OPTIONS_PACKET_S2_20260915.md`) — recommended T = 0.0001 on `m2`; B-17 = pin the `m2` identity already coded in `data_gap_ratio.py`; B-13 = the `ds-v1` digest of the scanned bundle" |
| `P021.BASIC_FAILURE_FLOOR` | B-03 / B-04 open | "B-03 CLOSED by policy v1 (day 30 / swing 30 / position 12 — position extrapolated); B-04 value CLOSED (single-trade loss multiple 1; stop-loss ceiling 0.5 % of equity = `P021_DECISION_1 = A`); B-04 **risk-unit source** still OPEN; B-22 policy-set ratification OPEN" |
| `P021.UNSIMULATED_CONTROLS` | B-08 allowance matrix open ⇒ always BLOCKED | "B-08 DECIDED (decision 1): a required-but-unsimulated control permits at most `SHADOW_ELIGIBLE`; informational controls only when openly listed in the independently computed manifest — `evaluate_control_evidence`; B-19 control-hash contract IMPLEMENTED (versioned preimage → bare sha256)" |
| `P021.BACKTEST_FORWARD_DIVERGENCE` | B-05/B-06/B-07 open, always BLOCKED | unchanged, plus: "pair key fixed (instrument, entry-bar timestamp, intent id); forward periods closed by policy v1 (21 / 119 / 364 days; forward trade-count minima 20 / 12 / 12); divergence required only from `TESTNET_PAPER_ELIGIBLE` upward (decision 3 A); metric definition options in S2 (M-A/M-B/M-C); B-20 provenance OPEN" |

## C. Threshold table
Add a "Policy v1 (2026-09-07, PROVISIONAL)" column carrying the twelve closed numbers verbatim from `p021_readiness_rules.py` `CLOSED_NUMBERS` (with the `extrapolated=True` marks on the position-class rows and the day-forward-period 3-vs-4-week discrepancy note), and mark the four `OPEN_NUMBERS` as the only open thresholds.

## D. Acceptance-gate mapping
Add B-14 DECIDED (decision 3 A): required check set by target state — every non-divergence P021 check for `SHADOW_ELIGIBLE`; all seven from `TESTNET_PAPER_ELIGIBLE` upward — and note that the catalogue does not yet encode `required_check_ids_by_target_state` (S1 code item).

## E. Open questions — the blocker table becomes a state table
Carry the ledger from `P021_GAP_TABLE_20260915.md` §2 verbatim (B-01 OPEN; B-02 OPEN measure-first with an unanswered options packet; B-03 CLOSED policy v1; B-04 value CLOSED / source OPEN; B-05..B-07 OPEN; B-08 DECIDED+IMPLEMENTED; B-09 OPEN; B-10 partly CLOSED; B-11 OPEN; B-12 DECIDED+IMPLEMENTED; B-13 PARTLY; B-14 DECIDED not encoded; B-15 OPEN; B-16 DECIDED+IMPLEMENTED; B-17 OPEN; B-19 IMPLEMENTED; B-20 OPEN; B-21 IMPLEMENTED; B-22 validator IMPLEMENTED / ratification OPEN). Keep every v1.5 citation; add the repository paths of the merged modules beside each IMPLEMENTED row.

## F. Discrepancies
D-01..D-03 unchanged. Add D-04: "the catalogue's `missing_rules` still lists `decision_domain.B12`, `forming_bar_runtime_proof.B16`, `state_allowance_matrix.B08`, `control_hash_contract.B19`, `intent_hash_contract.B21` although the contracts module implements the decided rules — either the catalogue is updated when the contract slice's T0 roster accepts it, or the design says the catalogue deliberately keeps refusing until then (recommended: the latter, stated explicitly, so a green catalogue never precedes the roster)."

## G. Not part of v1.6 (needs its own authority)
Any code change (catalogue update, encoding B-14), any threshold value, any RED/GREEN claim about the evaluator (none exists).

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
