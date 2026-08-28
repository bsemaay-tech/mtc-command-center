# WP-P0-11 direct-build row arm report

Date: 2026-08-28

Branch: `feature/wp-p0-11-kernel-legacy-compatible-20260825`

Tier: T0

Actors: Codex implementer `/root`; independent read-only Lead `/root/p011_g2_lead`.

## Outcome

**Gate outcome: STOP.** The arm has 33 applicable rows GREEN after real clean-producer execution and producer-mutation RED, 7 applicable rows STOP, and 2 policy-only rows (C25/C27). The independently reproduced totals are 134/134 compared expected leaves, 33 clean GREEN executions, 33 producer mutation REDs, and 69 RED mismatches.

- Previously closed: C01-C24 (24 GREEN).
- Closed here: C26, C31, C33, C36-C41 (9 GREEN).
- Producer execution unavailable: C28-C30 (3 STOP).
- Frozen expectation contradicts the named authority: C32, C34, C35, C42 (4 STOP).

This is a truthful partial. The Stage-1 authority re-pin is owner-escalated and is not part of this lane.

## Part-3 rows

Every P0-09 citation records the frozen pinned-table location and the current-master location. Source ranges below were opened before use.

| Row | Result | Status | Authority rule location |
|---|---|---|---|
| C26 | A accepts both identical bar identities and emits 2 outputs. Only the A duplicate-bar half is evidenced; the controller L25 half is explicitly unevidenced. | GREEN | A `runner.py:334-350`; P009 pinned `690-707`, current `696-713` |
| C28 | Frozen source seams exist, but the manifest scenario asserts route values only; no authorized executable Pine producer is available to prove payload/alert dispatch. | STOP | controller `config.py:226-238`, Pine `2010-2028`; P009 pinned `740-759`, current `746-765` |
| C29 | Frozen source seams exist, but key/value inspection is not observable L25 payload execution. | STOP | controller `config.py:231-238`, Pine `2017-2020`; P009 pinned `760-783`, current `766-789` |
| C30 | Frozen validation/payload seams exist, but source inspection is not executable protective-payload dispatch. | STOP | controller `config.py:569-584`, Pine `2017-2020`; P009 pinned `784-803`, current `790-809` |
| C31 | `off` ignores pending re-entry; `research` reaches the pending branch. | GREEN | A `runner.py:1393-1409`; P009 pinned `804-823`, current `810-829` |
| C32 | Only `local` and `carry_to_next_bar_after_protective_exit` validate; the frozen short `next_bar_*` aliases raise `ValueError`. | STOP | A `config.py:458-469`; P009 pinned `824-864`, current `830-870` |
| C33 | Bars 10/11/12 yield allowed `[false,false,true]`; first allowed bar is 12. | GREEN | A `runner.py:1293-1308`; P009 pinned `865-887`, current `871-893` |
| C34 | With assumed capital 1000: unrealized -600, equity 400, required margin 400, deficit 0, exit percentage 0. | STOP | A `runner.py:1445-1461`; P009 pinned `888-911`, current `894-917` |
| C35 | Clean `debug_mode=true` raises `NameError` on undefined `EXECUTION_PROFILE_RAW_CLOSE_ONLY`. | STOP | A `runner.py:1049-1060`, `config.py:10`; P009 pinned `912-931`, current `918-937` |
| C36 | Actual A TradingView-research BE branch activates BE at the close trigger. | GREEN | A `exits.py:286-350`; P009 pinned `932-965`, current `938-971` |
| C37 | Actual A TradingView-research trailing branch activates trailing at the close trigger. | GREEN | A `exits.py:286-330`; P009 pinned `966-988`, current `972-994` |
| C38 | Actual frozen-B pivot FSM produces age OK, break 101, long pulse, and reset waits. | GREEN | B `confirmation_layer.py:350-394` at `b5ed1afa`; P009 pinned `989-1070`, current `995-1076` |
| C39 | Actual frozen-B runner produces Edge `[true,false]`, Signal `[true,true]`, and blocks a first evaluation level without a fresh edge. | GREEN | B `mtc_runner.py:1220-1225,1660-1674`; P009 pinned `1071-1090`, current `1077-1096` |
| C40 | 10:30 LTF sees prior-closed HTF 100 at 10:00, never future 200. | GREEN | A `htf.py:106-163`; P009 pinned `1091-1140`, current `1097-1146` |
| C41 | Actual A gate producer has raw long true and gated long false. | GREEN | A `gates.py:27-40,364-411`, `runner.py:1227-1239`; P009 pinned `1141-1200`, current `1147-1206` |
| C42 | Clean RF emits one `rf_flip_short` at 99, while the frozen expected count is 0; Supertrend matches. | STOP | A `range_filter.py:16-92`, `supertrend.py:18-55`; P009 pinned `1201-1285`, current `1207-1291` |

No mutation is credited for a STOP row. Exact source inspections, clean probes, arithmetic, commands, outputs, and mismatches are in `evidence/row_arm/unresolved_rows.json`.

## Carried findings

**F-1: OPEN / STOP.** C28-C30 are pinned to controller tag `legacy/pine-controller/2026-08-25` (`77a10e65`), never current A. The earlier source parser simulated payload and dispatch and was rejected by independent review. It has been removed. Because this lane has no authorized executable Pine producer, it records source inspection only and makes no preservation claim.

**F-2: truthful limitation.** C26 executes and mutates the A duplicate-bar producer. It does not claim controller L25 coverage.

**F-3: CLOSED by C41.** The verifier-owned scenario produces `raw_signal.long=true` and `gated_signal.long=false` through actual A gate functions. Removing the HTF-close substitution makes the mutation RED. Extract: `evidence/f3_raw_gated_divergence.json`.

**F-4: narrowed, option (b).** The frozen `p011_gate.py`, receipt, and matrix were not edited. The only supported wording for `evidence/discrimination_matrix/` is exactly **"comparator field-sensitivity self-test, one record"**. The rejected additive producer-matrix implementation and artifacts were removed; no full-stream producer-mutation claim remains.

The frozen receipt still publishes the numeric fields `matrix_rows: 76`, `red: 76`, and `restored_green: 76`. Because the receipt is owner-pinned and read-only, those fields remain unchanged and must be interpreted only under the one-record comparator-self-test limitation above; they are not producer-boundary evidence.

All 17 structural restoration commands execute. Fourteen attacks RED as expected and all 17 restorations produce the pre-committed expected result. The three attacks that do not reach their intended comparator failure (`deleted_applicable_c_row`, `changed_resolved_config_and_local_hash`, `changed_data_byte`) stop earlier at the frozen checkout guard. The two inaccurate IDs were corrected.

## Anti-regression and evidence

- Every expected leaf in a GREEN row is recursively compared: 134 expected, 134 compared.
- Scenario identity is verifier-owned and contract-bound before producer execution.
- Missing scenario identity, input, expected leaf, or required member fails closed: `evidence/row_arm_contract_mutations.json` records 3 FAIL and 1 STOP.
- Row evidence: `evidence/row_arm/`; independent verifier: `evidence/row_arm_remeasure.py`.
- Structural evidence: `evidence/structural_mutations.json`.
- Frozen full-sequence SHA-256: `727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e`.
- Frozen gate SHA-256: `7797908a5570c14fa5133dc544f00eba03082cea35bfe41f3dd022acc1655529`.

## Scope boundary

Stage-1 authority pin/freezer, receipt, manifest, profiles, schema, external anchor, A, B, Pine, backtest, adapters, and kernel remain unchanged. Owner resolution is required for C32/C34/C35/C42, an executable authorized Pine route is required for C28-C30, and the gate remains STOP.
