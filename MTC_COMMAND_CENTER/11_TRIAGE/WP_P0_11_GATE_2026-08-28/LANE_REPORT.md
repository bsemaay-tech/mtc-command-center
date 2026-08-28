# WP-P0-11 direct-build row arm report

Date: 2026-08-28

Branch: `feature/wp-p0-11-kernel-legacy-compatible-20260825`

Tier: T0 evidence work; no production, trading, Pine, kernel, backtest, adapter, schema, or Stage-1 authority artifact changed.

## Outcome

**Gate outcome: STOP.** Of 42 manifest rows, 36 applicable rows are GREEN after real producer RED, 4 applicable rows are `UNRESOLVED_AUTHORITY_CONTRADICTION`, and C25/C27 are policy-only. This is a truthful partial, not a request to re-pin Stage 1.

- Previously closed: C01-C24 (24 GREEN).
- Closed here: C26, C28-C31, C33, C36-C41 (12 GREEN).
- Unresolved: C32, C34, C35, C42 (4 STOP).
- Policy-only: C25, C27.

The executable arm independently remeasures 163/163 expected leaves, 36 clean GREEN executions, 36 real producer mutation REDs, and 73 RED mismatches. Evidence: `evidence/row_arm/` and `evidence/row_arm_remeasure.py`.

## Row results and dual authority citations

Every P0-09 citation gives both the frozen pinned-blob location and the current-master location. Source line ranges below were opened before use.

| Row | Frozen producer result | Status | Authority rule location |
|---|---|---|---|
| C26 | A accepts both identical bar identities and emits 2 outputs; controller L25 contains both entry and exit dispatch | GREEN | A `runner.py:334-350`; controller `MTC_V2.pine:2010-2028`; P009 pinned `690-707`, current `696-713` |
| C28 | EL/ES select exact entry routes, XL/XS exact exit routes, XA fallback; empty route set emits no alert; exact entry payload compared | GREEN | controller `config.py:226-238`, Pine `2010-2028`; P009 pinned `740-759`, current `746-765` |
| C29 | exact L25 payload compares order type, amount, amount type, leverage, and reduce-only; WT amount does not alter legacy kernel quantity | GREEN | controller `config.py:231-238`, Pine `2017-2020`; P009 pinned `760-783`, current `766-789` |
| C30 | exact payload includes TP 105.13, SL 95.34, reduce-only and conditional-order flag; TP/SL cross-rule compared | GREEN | controller `config.py:569-584`, Pine `2017-2020`; P009 pinned `784-803`, current `790-809` |
| C31 | `off` ignores pending re-entry; `research` reaches the pending branch | GREEN | A `runner.py:1393-1409`; P009 pinned `804-823`, current `810-829` |
| C32 | only `local` and `carry_to_next_bar_after_protective_exit` validate; the frozen short `next_bar_*` names raise `ValueError` | UNRESOLVED | A `config.py:458-469`; P009 pinned `824-864`, current `830-870` |
| C33 | candidate bars 10/11/12 yield allowed `[false,false,true]`, first allowed 12 | GREEN | A `runner.py:1293-1308`; P009 pinned `865-887`, current `871-893` |
| C34 | with the most favorable omitted capital assumption 1000, unrealized -600, equity 400, required margin 400, deficit 0, exit percentage 0 | UNRESOLVED | A `runner.py:1445-1461`; P009 pinned `888-911`, current `894-917` |
| C35 | clean `debug_mode=true` raises `NameError` on undefined `EXECUTION_PROFILE_RAW_CLOSE_ONLY` before metadata assignment | UNRESOLVED | A `runner.py:1049-1060`, `config.py:10`; P009 pinned `912-931`, current `918-937` |
| C36 | TradingView research BE branch activates BE at the close trigger | GREEN | A `exits.py:286-350`; P009 pinned `932-965`, current `938-971` |
| C37 | TradingView research trailing branch activates trailing at the close trigger | GREEN | A `exits.py:286-330`; P009 pinned `966-988`, current `972-994` |
| C38 | B pivot FSM: age OK, break level 101, close 102 emits long pulse and resets waits | GREEN | B `confirmation_layer.py:350-394` at `b5ed1afa`; P009 pinned `989-1070`, current `995-1076` |
| C39 | B entry mode: Edge `[true,false]`, Signal `[true,true]`; first evaluation without a fresh edge is blocked | GREEN | B `mtc_runner.py:1220-1225,1660-1674`; P009 pinned `1071-1090`, current `1077-1096` |
| C40 | 10:30 LTF sees prior-closed HTF 100 at completed timestamp 10:00, never future 200 | GREEN | A `htf.py:106-163`; P009 pinned `1091-1140`, current `1097-1146` |
| C41 | raw long is true while HTF substitution 101 blocks gated long, directly evidencing raw/gated independence | GREEN | A `gates.py:27-40,364-411`, `runner.py:1227-1239`; P009 pinned `1141-1200`, current `1147-1206` |
| C42 | clean RF sequence emits one `rf_flip_short` at 99 because 99 is below line 100; frozen expected count is 0; Supertrend half matches | UNRESOLVED | A `range_filter.py:16-92`, `supertrend.py:18-55`; P009 pinned `1201-1285`, current `1207-1291` |

No mutation was run for C32/C34/C35/C42 because the frozen authority establishes no clean GREEN route for the frozen expected value. Their real commands, output, arithmetic, and mismatches are in `evidence/row_arm/unresolved_rows.json`.

## Carried findings

### F-1 - closed for the authority that exists

C28-C30 now evaluate the controller tag `legacy/pine-controller/2026-08-25` at commit `77a10e6573d93f8aaf777010ea507bbec0a7668b`. They compare actual L25 route selection, exact constructed payload text, alert dispatch/fallback behavior, and protective flag effects. Current master A is never used for this deleted surface. This is source-level frozen-producer evidence only; no TradingView execution credit is claimed.

### F-3 - closed by C41

The verifier-owned C41 scenario produces `raw_signal.long=true` and `gated_signal.long=false` through the actual A `_apply_entry_gates` producer. Removing the legacy HTF-close substitution makes the mutation RED. Durable extract: `evidence/f3_raw_gated_divergence.json`.

### F-4 - old claim narrowed; additive result remains partial

The frozen `p011_gate.py` and its pinned matrix were not edited. Every claim about `evidence/discrimination_matrix/` is narrowed to exactly **"comparator field-sensitivity self-test, one record"**.

The additive `evidence/producer_discrimination_matrix/` scans all 96,154 pinned observations and computes applied-value and changed-record counts at the observation-producer boundary. It proves RED-then-GREEN for 68/76 catalog paths. Seven `position.working_exits[*]` leaves and `position.completed_exit_ids[*]` have zero occurrences and fail closed; they are not claimed as exercised. The required clean rebuild command was executed but the frozen builder stopped on later ratified checkout changes outside the gate package, so the additive matrix remains STOP.

All 17 structural commands now execute. The two inaccurate IDs are corrected to `missing_first_observation` and `changed_first_observation_position_state`. Twelve comparator attacks still RED and self-restore GREEN; the two provenance restores execute to the gate's expected STOP, while the three build attacks and restores stop earlier at the same frozen checkout guard. Nothing is represented as a GREEN restoration comment.

## Anti-regression properties

- Every declared expected leaf is recursively compared; the independent remeasurement proves 163 expected leaves equal 163 compared leaves.
- Scenario identity and expanded L25/F3 setup are verifier-owned and bound before producer execution.
- Missing required scenario members, inputs, or expected leaves fail closed; `evidence/row_arm_contract_mutations.json` records three FAIL and one STOP cases.

## Frozen identities and evidence

- `p011_gate.py`: `7797908a5570c14fa5133dc544f00eba03082cea35bfe41f3dd022acc1655529`
- manifest: `13075e23bc2db8517320098f38608851cee123fe57026e9e8607db2a5f08eb2b`
- receipt: `34823d99e606812bed09325c15381ea03face9b52a6684ec0f7e1152f1aad007`
- schema: `c18fb1622ab38b374d65a1304994f0e9f5d8993f948e75d99694bdfceb5fdb2e`
- pinned full sequence: `727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e`
- row-arm batch: `evidence/row_arm/batch_manifest.json`
- unresolved rows: `evidence/row_arm/unresolved_rows.json`
- producer-boundary matrix: `evidence/producer_discrimination_matrix/discrimination_matrix.json`
- structural transcript: `evidence/structural_mutations.json`

## Scope and next gate

Stage-1 re-pin, authority receipt, manifest dispositions, profiles, schema, external anchor, A, B, Pine, backtest, adapters, and kernel remain unchanged. The next gate is owner resolution of the four frozen-oracle contradictions plus the carved-out Stage-1 re-pin; independent dual-flagship acceptance remains required before any broader acceptance claim.
