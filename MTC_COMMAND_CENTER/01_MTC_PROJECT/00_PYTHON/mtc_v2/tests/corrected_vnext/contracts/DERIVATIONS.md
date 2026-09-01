# CONTRACT_TABLES — independent expected-value worksheet (lane W127b)

- **Author identity:** `claude-family lane W127b on Claude MAX Opus, non-implementer, owner ruling
  Q3a 2026-08-31; continuation of capped W127`.
- **Producer role:** `CONTRACT_TABLES` per `P012_FRESH_DESIGN_V1.md:444` (§15.1) — the `2.0.0`
  expected event/result artifacts, hand-derived from §§7-14 plus frozen records.
- **Design under derivation:** `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`, version
  **v1.4** (title line 1; v1.4 micro-fold change log lines 640-646). **Line span used: 1-646**
  (whole file). Primary correction semantics §§7-14 lines 183-433; gate/enumeration §15 lines
  435-549; OPEN ledger §19 lines 600-615.
- **Design revision applied (lane W156, 2026-08-31):** the bundle now derives from design **v1.5**
  (same file, 967 lines; sole normative addition is §22 lines 676-930 plus the §15.6 note lines
  551-577) together with owner addendum 20 (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:337-348`,
  verbatim `1a 2a 3a 4a 5a`). Sections 0-11 below are the v1.4 derivation and are left intact as the
  historical record; the `## v1.5 revision` section at the end of this file re-derives every cell
  those two sources make computable, keeps every other sealed value byte-identical, and states what
  stays blocked. Where the two disagree, the `## v1.5 revision` section governs.
- **Design revision applied (lane W167, 2026-09-01):** the bundle now derives from design **v1.8**
  (same file, 1273 lines; sole normative change is §23 lines 969-1273, which supersedes the v1.7
  §23 text). Sections 1-22 are unchanged from v1.5 and their line numbers were re-verified by
  heading position this session, so every v1.5 citation in this worksheet and in all 17 artifacts
  remains exact. Owner addendum 22 authorised the single micro-fold closing G79-F01/DS35-F01 and
  DS35-F02..F04 (design `:1231-1237`); addenda 19, 20 and 21 apply unchanged. The
  `## v1.8 revision` section at the end of this file re-derives exactly the seven golden-node
  classes enumerated by the design's own tables-revision scope list (`:1175-1202`) and states what
  §23 forces versus what it labels an `AMENDMENT-CHOICE`. Where it disagrees with any earlier
  section of this file, the `## v1.8 revision` section governs.
- **Owner Reading Y applied (lane W172, 2026-09-01):** owner addendum 26 answered **W167-D04**. The
  owner chose **Reading Y**: a `decision_events` row is required for every closed §23.1 reason whose
  named decision is **actually evaluated** on that scenario, even where the prior tables artifact
  never carried that reason, so §23.1 `:1033-1034` applies to the tables family on its own terms. The
  anti-padding half of the same sentence still binds: a reason is emitted because its named decision
  was evaluated, never to equalize row counts. The `## W172 Reading Y revision` section at the end of
  this file records the ten added rows on eight scenarios, their derived payloads, the two rows
  deliberately withheld, and the disposition of findings G83-F01..F06. Where it disagrees with any
  earlier section of this file, including `## v1.8 revision`, the `## W172 Reading Y revision`
  section governs.
- **Repository evidence identity:** `C:\WFMERGE54` HEAD `108ea066a710ff7ef5c09246903fe3d523da1d56`;
  `mtc_v2/core` tree OID `c7f4aa1b46792c67c171237cea62c06497aa35ea`. Both re-verified this session
  with `git rev-parse HEAD` and `git rev-parse HEAD:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core`;
  both match the design's stated premise at `P012_FRESH_DESIGN_V1.md:5`.
- **Independence fence (design §15.1:444; lane W127 authority block):** every expected value below is
  `INDEPENDENT_DERIVATION` — obtained by the explicit arithmetic shown here from the design's stated
  contract semantics. No kernel was run. No `observed/` path was read. No corrected-kernel
  implementation exists: `git ls-files | grep -i "corrected_vnext\|economics.py\|semantics.py\|economic_records"`
  returns exactly one path, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/test_trailing_exit_semantics.py`
  (an unrelated legacy backtest test that matched the `semantics.py` substring), which was not opened.
- **§16 fence:** the design's mandatory `SEMANTIC_COVERAGE_REVIEW` (`P012_FRESH_DESIGN_V1.md:551-562`)
  is **owner-held and PENDING**. This lane neither claims nor performs it, and the claude family is
  excluded from that reviewer role because it authored these tables.

---

## 0. Audit of the W127 partial (task step 1)

The capped W127 attempt left two files in this directory: `DERIVATIONS.md` (37 761 bytes) and
`golden/corrected_vnext/RULE2-01-RED.json` (3 145 bytes). Both were read in full and every value in
them was **re-derived from scratch** against design v1.4 before this file was written.

### 0.1 Design version the partial reflects

**The partial already reflects v1.4, not an earlier version.** Its §6 derives
`RULE2-06-EQUAL-PRICE-RED` including the `TARGET-FAR` / `TARGET-NEAR` byte-order tie-break, and its
§9 cites the v1.4 micro-fold row `DS18-F01` at design line 645 and the v1.4 catalog sentence at
design line 454. The lane brief's caution that the partial "may predate v1.4's new scenario" is
therefore **not borne out**; recorded as discrepancy **D-17** (prompt-versus-evidence, clause C-2).

### 0.2 Verified and kept

| # | Item audited | Outcome |
|---|---|---|
| V-01 | RULE2-01-RED arithmetic: risk amount 100, stop distance 10, risk qty 5, cap qty 50, qty 5, notional 1000; legacy qty 10, legacy notional 2000 | re-derived, identical, **kept** |
| V-02 | RULE2-01-GREEN: fallback notional 100, raw qty 1, cap qty 100, qty 1 on both versions | re-derived, identical, **kept** |
| V-03 | RULE2-02-RED/GREEN: risk amount 10, qty 1, notional 100; corrected refuses at 101, admits at 100 | re-derived, identical, **kept** |
| V-04 | RULE2-03-RED/GREEN: `REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION` on `price_tick` 0.25 vs 0.5; no refusal at 0.5/0.5 | re-derived, identical, **kept** |
| V-05 | RULE2-04-RED/GREEN: gap reference 90, final fill 90, `fill_trigger=GAP_OPEN`, legacy close 92; GREEN no touch on either predicate | re-derived, identical, **kept** |
| V-06 | RULE2-05-RED/GREEN: impact 1, fill 101; zero-impact fill 100 | re-derived, identical, **kept** |
| V-07 | RULE2-06-RED: ordered `[TARGET-NEAR, TARGET-FAR]`, 1 @ 105 then 1 @ 110, no stop remainder, gross 15; legacy 2 @ 90, gross −20 | re-derived, identical, **kept** |
| V-08 | RULE2-06-GREEN: only stop touches, 2 @ 90 on both versions, gross −20 | re-derived, identical, **kept** |
| V-09 | RULE2-06-EQUAL-PRICE-RED: `TARGET-FAR` (0x46) before `TARGET-NEAR` (0x4e), 1 @ 105 twice, gross 10 | re-derived, identical, **kept** |
| V-10 | RULE2-07-RED: fee notional 100, fee 0.1 each, deltas −0.1 each, gross 0, net −0.2, equity 999.8; guard count 1, `guard_blocked_raw` true | re-derived, identical, **kept** |
| V-11 | RULE2-08-RED: notional 100, long cashflow rate −0.001, delta −0.1, equity 999.9 | re-derived, identical, **kept** |
| V-12 | Catalog conservation recount: RED 9, GREEN 8, PROBE 10, rows 27 | re-counted from the design independently, identical, **kept** |
| V-13 | Repository citations `position_sizer.py:43-50,66-68`; `config.py:48,49,69`; `runner.py:733-738,780-783`; `DECISIONS.md:31`; `exits.py:365-374,400-406,424-447` | every line opened and read this session, all support the claim, **kept** |

### 0.3 Corrected

| # | What the partial said | Correction and authority |
|---|---|---|
| C-01 | design line span "1-647", change log "lines 640-647" | The design file has **646 lines** and ends with a final LF (`wc -l` = 646; `tail -c 1` = `\n`). Corrected to 1-646 / 640-646. |
| C-02 | RULE2-07-GREEN cross-version projection listed legacy `fee_events` and `funding_events` as `A:0` | Design `:476` — `LEGACY_P011_EXACT_V1` keeps absent legacy containers absent and forbids `GATE_READER` from synthesizing empty `fee_events`/`funding_events`. The legacy selector resolves **ABSENT**, and design `:510` counts present-versus-absent as *divergence*. Those rows were therefore invalid GREEN members. **Removed** from the GREEN projection and re-classified as version-specific added containers under design `:181`. |
| C-03 | RULE2-08-GREEN projection listed `funding_events` `A:0` = `A:0` and `RESULT_SURFACE/cumulative_funding` as `ABSENT / I:0` = `I:0`, "Equal? yes" | Same authority as C-02, plus design `:394` (legacy `PortfolioState` carries no funding ledger). Left state is unambiguously ABSENT; the pair is unequal. **Removed** from the GREEN projection; the declared GREEN member is the economic cash/equity value 1000 stated at design `:429`. |
| C-04 | RULE2-06-RED divergent row `RESULT_SURFACE/collision` = `B:1, chosen="TARGETS"` | `chosen="TARGETS"` is not a design value. Design `:335` gives `chosen=STOP` only for the `STOP_FIRST` row; the `TARGET_FIRST` row's receipt column (design `:336`) is **"Ordered chosen event ids"**. Replaced by `ordered_chosen_exit_ids` plus the pessimistic-field divergence the design names at `:345`, evidenced by the legacy collision return `is_pessimistic=True` at `exits.py:370`. |
| C-05 | Fee/cash cells marked `BLOCKED-ON-OPEN-03`; synthetic record ids marked `BLOCKED-ON-OPEN-01`; metrics and schema marked `BLOCKED-ON-OPEN-09` | Mislabelled. OPEN-01/03 govern the **production** record and fee schedule, and design `:124` forbids a production admission value from populating a synthetic RULE-2 vector — so no OPEN-01/03 answer can ever supply these cells. OPEN-09 has been answered `APPLICABLE / schema APPROVED`. Re-labelled `BLOCKED-MISSING-SCENARIO-INPUT` (vector gap), `BLOCKED-MISSING-RECORD-BYTES` (synthetic record bytes never listed) and `BLOCKED-DESIGN-UNENUMERATED` (design fixes no node set) as appropriate. See §0.5. |
| C-06 | `golden/corrected_vnext/RULE2-01-RED.json` wrote `"cash_events": []`, `"fee_events": []` and `"equity_curve": {"last": 1000}` while simultaneously listing those cells as blocked | Writing `[]` asserts a derived zero-length container, and design `:508` makes missing, null and empty **different** nodes. Design `:100` mandates a fee cash event for the entry fill, so `[]` is affirmatively wrong, and `1000` asserts a zero fee. Every genuinely underivable cell now carries the marker string as its **value**, so no unsupported number or container length is sealed. |
| C-07 | RULE2-07-RED divergent-projection table included `trade/0/gross_realized_pnl` `I:0` versus `I:0` with the note "equal value, but split reported" | A `rule2_divergent_projection` member must actually differ; design `:510` says identical present values are not divergence, and design §15.4 refuses "correction without divergence". **Removed** from the divergent set. DEF-P012-07's divergence is carried by `fee_events`, `net_trade_pnl`, the guard nodes and equity, all of which do differ. |
| C-08 | `provenance.author` = "claude-family lane W127, non-implementer, owner ruling Q3a 2026-08-31" | Updated to the W127b identity required by this lane (see header). |
| C-09 | Line cites `§15.3:511` (event-order rule) and `§15.3:471` (RESULT_SURFACE contents) | Off by one and by three: the event-order rule is at design line **512**; the RESULT_SURFACE member list is at design line **474**. Corrected throughout. |
| C-10 | `D-07 / D-08` recorded as unresolved DISCREPANCY-CANDIDATES ("may differ from IEEE-754 binary64 accumulation by up to one ULP") | **Resolved** by explicit binary64 hand arithmetic in §0.6 below: both accumulations land exactly on the binary64 nearest the design's written decimal. Downgraded from open candidates to recorded, closed derivations. |

### 0.4 Added by W127b (not present in the partial)

- All 16 remaining expected-surface artifacts (the partial sealed only `RULE2-01-RED`).
- `scenario_catalog.json` with all 27 declared rows, including the 10 `PROBE` rows the partial never
  enumerated as catalog rows.
- `CONTRACT_TABLES_MANIFEST.json`.
- Binding of the owner's now-answered OPEN rows (§0.5) and the OPEN-02 conflict (**D-12**).
- Probe first-changed-node derivations and their enumeration-order ambiguities (**D-14**, **D-16**).

### 0.5 The ten OPEN rows are answered — so what is actually still blocked

`C:\tmp\LANE_PROMPTS_20260828\open_item_applicability_DRAFT.json` (`draft_revision` 3) carries an
owner-approved terminal disposition for **all ten** rows OPEN-01..OPEN-10; every one is `APPLICABLE`.
Consequently **this bundle contains zero `BLOCKED-ON-OPEN-nn` cells.** That is the honest count, and
it is a change from the partial, which predates the answers.

Where an answer genuinely changes a derivation it is cited in the artifact's `open_item_bindings`
array:

| OPEN | Where used | Effect |
|---|---|---|
| OPEN-02 (`STOP_FIRST` mandatory) | `RULE2-06-RED`, `RULE2-06-EQUAL-PRICE-RED`, `RULE2-06-GREEN` | **No value effect; conflict recorded (D-12).** Design `:343` declares `TARGET_FIRST` as an explicit *input* of the two RED scenarios and design `:331` forbids closing OPEN-06 from silently rewriting the pair, so the design's synthetic input governs the sealed values. For the GREEN row design `:339` makes all three policies select the sole touched class, so the answer is value-neutral there. |
| OPEN-05 (funding rules approved; same-timestamp = INCLUDE) | `RULE2-08-RED`, `RULE2-08-GREEN` | No value effect: design `:429` places the position open *before and after* the RED timestamp and closed *before* the GREEN timestamp, so eligibility is the same under INCLUDE or EXCLUDE. The INCLUDE answer creates a separate build fixture obligation (a fill at the exact funding timestamp) that no declared scenario exercises. |
| OPEN-06 (P19 RETIRE, P20 RETAIN) | `RULE2-04-RED`, `RULE2-04-GREEN` | **Closes the contingency.** Design `:273` and `:287` make the corrected gap/open projection OPEN-06-contingent. The owner's answer retires P19 (close-only close-triggered/close-filled stop) and retains P20 (gap-aware open/stop reference), per `P012_OPEN06_RETAINED_RETIRED_PROPOSAL_V1.md:61-62`, which is exactly the corrected behaviour design `:287` states. The sealed value 90 still comes from the design, not from the owner answer. |
| OPEN-09 (additive schema APPROVED) | every scenario | Removes the partial's `BLOCKED-ON-OPEN-09` schema-approval marker. It does **not** enumerate a metric node set, so `metrics` is `BLOCKED-DESIGN-UNENUMERATED`, not OPEN-blocked. |
| OPEN-10 (guards keep gross-minus-fees; funding excluded) | `RULE2-07-RED`, `RULE2-07-GREEN`, `RULE2-08-RED` | Confirms the basis design `:384` already fixes from D017, and settles design `:431` ("guard outcomes follow the sourced OPEN-10 decision") for RULE2-08: the captured funding delta does **not** enter the guard basis. |

The residual blocks are design gaps, not owner gaps. Four marker classes are used:

- `BLOCKED-MISSING-SCENARIO-INPUT` — the declared synthetic vector omits an input the cell needs.
- `BLOCKED-MISSING-RECORD-BYTES` — the cell is a digest/id/field of a *synthetic frozen test record*
  whose exact bytes the design never lists. Design `:124` forbids substituting the answered
  production record, so this can never be closed by an OPEN answer.
- `BLOCKED-DESIGN-UNENUMERATED` — the design names the member but fixes no node set for it
  (`metrics`; the complete `decision_events` reason vocabulary).
- `BLOCKED-BUILD-ARTIFACT` — a path/digest that only exists after the Gate-2 build (serialized
  scenario-input files, probe kernel-variant trees, patch files, observed outputs).

### 0.6 Node kinds and the two decimal equities (resolves the partial's D-07 / D-08)

Design `:480` fixes node kind by **token shape**, not by value: a number token with no fraction and
no exponent is an integer node (`I:`); a token with a fraction or exponent is a binary64 float node
(`F:`). This bundle therefore writes prices, quantities, multipliers, notionals and counts the design
states as bare integers (`100`, `5`, `2`, `1`, `1000`) as integer tokens, and rates, ticks, fractions,
fee/funding deltas and fee-adjusted equities the design states with a fraction (`0.001`, `0.5`,
`0.01`, `-0.1`, `999.8`) as float tokens.

The partial left the two fee/funding equities as an unresolved one-ULP caveat. They are resolved here
by explicit binary64 arithmetic (round-to-nearest, ties-to-even; hex-float digits obtained by long
division, shown so a stranger can re-check them):

```
0.1  = 0x1.999999999999(9...)p-4 ; the tail after 13 hex fraction digits is 0.9999..(16) = 9/15 = 0.6 ulp
       0.6 >= 0.5 -> round up -> fl(0.1) = 0x1.999999999999ap-4 = 0.1 + 0.4 * 2^-56
0.2  = same digit string one binade up ; fl(0.2) = 0x1.999999999999ap-3 = exactly 2 * fl(0.1)
999.8 = 999.8 / 2^9 = 1.952734375 -> hex fraction digits f, 3, e, then repeating 6
        13 digits f3e6666666666 ; tail 0.6666..(16) = 6/15 = 0.4 ulp ; 0.4 < 0.5 -> truncate
        fl(999.8) = 0x1.f3e6666666666p+9 = 999.8 - 0.4 * 2^-43
999.9 = 999.9 / 2^9 = 1.9529296875 -> hex fraction digits f, 3, f, then repeating 3
        13 digits f3f3333333333 ; tail 0.3333..(16) = 3/15 = 0.2 ulp ; 0.2 < 0.5 -> truncate
        fl(999.9) = 0x1.f3f3333333333p+9 = 999.9 - 0.2 * 2^-43
ulp at both = 2^(9-52) = 2^-43
```

RULE2-08 equity, one addition (design `:429`):

```
1000 + fl(-0.1) exactly = 999.9 - 0.4 * 2^-56 = 999.9 - 0.0000488 * 2^-43
candidates: fl(999.9) = 999.9 - 0.2 * 2^-43   (distance 0.1999512 * 2^-43)
            next up   = 999.9 + 0.8 * 2^-43   (distance 0.8000488 * 2^-43)
-> rounds to fl(999.9). The token 999.9 is exact for this accumulation.
```

RULE2-07 equity, two subtractions (design `:384`):

```
step 1: 1000 - fl(0.1) -> fl(999.9)                       (identical to the RULE2-08 case above)
step 2: fl(999.9) - fl(0.1)
        exact = 999.8 - 0.2 * 2^-43 - 0.4 * 2^-56 = 999.8 - 0.2000488 * 2^-43
        candidates: fl(999.8) = 999.8 - 0.4 * 2^-43   (distance 0.1999512 * 2^-43)
                    next up   = 999.8 + 0.6 * 2^-43   (distance 0.8000488 * 2^-43)
        -> rounds to fl(999.8). The token 999.8 is exact for this accumulation.
        The equivalent single-step form 1000 + fl(-0.2) gives the same result:
        fl(0.2) = 0.2 + 1.11e-17, and 1.11e-17 is far below the 5.68e-14 half-ulp.
```

Fee and funding amounts, checked the same way:

```
fl(0.001)          = 0x1.0624dd2f1a9fcp-10 = 0.001 + 2.08e-20
100 * fl(0.001)    exactly = 0.1 + 2.08e-18 ; half-ulp at 0.1 is 6.94e-18 ; nearest is fl(0.1)
-> fee_amount 0.1 and fee_cash_delta -0.1 are exact for the token written.
-> funding_cash_delta = 100 * fl(-0.001) * (+1) -> fl(-0.1), exact for the token written.
net_trade_pnl      = 0 + fl(-0.1) + fl(-0.1) = -2 * fl(0.1) = fl(-0.2) exactly -> token -0.2 exact.
```

**Conclusion: D-07 and D-08 are closed.** No sealed decimal in this bundle depends on an unverified
rounding assumption. (The remaining §16 exposure is design limit L3 — a defect shared by the
enumerator and both serializations — which no arithmetic here can retire.)

### 0.7 Surface schema and container policy

All 17 RED/GREEN rows are `2.0.0`, so `surface_schema_id = CORRECTED_V2` (design `:476`), which
requires all six ordered containers `decision_events`, `fill_events`, `cash_events`, `fee_events`,
`funding_events`, `exit_events`; any may be explicitly empty. `SEQUENCE_FIELD_V1` (design `:512`)
gives every member an integer `sequence` starting at zero and equal to its array index; every
container written in this bundle satisfies that.

A container is written **empty** only where emptiness is *derived*, and is written as a **marker
string** where it is not. The asymmetry is deliberate and is grounded in design §3:

- A fill unconditionally requires a fee cash event (`:100`, step 11), so a scenario that *has* a fill
  but *no* `CostSchedule` cannot have `cash_events`/`fee_events` = `[]`; those cells are blocked.
- Funding is applied only per schedule event (`:398`), and `:425` refuses only *missing required
  interval data*. A vector that spans no funding interval therefore has a derived
  `funding_events` = `[]`.
- A scenario with no fill (RULE2-02-RED refusal, RULE2-03 pre-evaluation refusal, RULE2-04-GREEN
  no-touch, RULE2-07-GREEN empty fill input, RULE2-08-GREEN ineligible tick) has derived empty
  `fill_events`, `cash_events`, `fee_events` and `exit_events`.

---

## 1. DEF-P012-01 — contract multiplier in sizing (design `:183-220`)

### RULE2-01-RED — `close_only_deterministic_v2`

Inputs, exactly as design `:216` states them: `sizing_equity=1000`, `risk_pct=10`,
`final_entry_fill=100`, finite `stop=90`, `cm=2`, `qty_step=1`, `min_qty=0`, `min_notional=0`,
`BPS_OF_REFERENCE_V1` with `slippage_bps=0`, `price_tick=1`, test-only `max_leverage_cap=10`
(explicitly *not* the shipped default `1.0` at `config.py:69`, which this session read and confirmed
is `"max_leverage_cap": 1.0`).

```
risk_amount        = 1000 * (10/100)            = 100                       [:194]
stop supplied and finite, distance > 0 -> risk branch                       [:199-203]
stop_distance      = |100 - 90|                 = 10                        [:201]
risk_raw_qty       = 100 / (10 * 2)             = 5                         [:202]
selected_raw_qty   = 5                                                      [:203]
leverage_cap_qty   = (1000 * 10) / (100 * 2)    = 50                        [:206]
raw_qty            = min(5, 50)                 = 5                         [:207]
qty                = floor_to_qty_step(5, 1)    = 5                         [:208]
order_notional     = 5 * 100 * 2                = 1000                      [:209]
admit: 1000 >= min_notional 0                   -> admitted                 [:234]
slippage impact    = |100| * 0 / 10_000         = 0                         [:304]
buy -> unrounded   = 100 + 0                    = 100                       [:305]
final_entry_fill   = ceil_to_price_tick(100, 1) = 100                       [:307]
slippage_application_count = 1                                              [:311]
position.quantity after entry = 5
```

Legacy arithmetic for the divergence proof (design `:187`; independently confirmed against
`position_sizer.py:44-47`, which computes `per_unit_risk = abs(entry - sl)` then
`raw_qty = risk_amount / per_unit_risk` with **no** multiplier factor, and `:66`, which applies the
multiplier only to `order_notional`):

```
legacy risk_raw_qty     = 100 / 10      = 10
legacy leverage_cap_qty = (1000*10)/(100*2) = 50   (position_sizer.py:52-54 already includes cm)
legacy raw_qty          = min(10, 50)   = 10
legacy order_notional   = 10 * 100 * 2  = 2000
legacy position.quantity = 10
```

Declared `rule2_divergent_projection` (design `:217`: quantity, order notional, later position
quantity, and any quantity-derived cash event), resolved as design `:510` tagged states:

| Node | `1.0.0` BASELINE | `2.0.0` CONTRACT_TABLES | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/quantity` | `PRESENT(I:10)` | `PRESENT(I:5)` | yes |
| `/RESULT_SURFACE/order_notional` | `PRESENT(I:2000)` | `PRESENT(I:1000)` | yes |
| `/RESULT_SURFACE/final_position/quantity` | `PRESENT(I:10)` | `PRESENT(I:5)` | yes |
| quantity-derived cash event | — | `BLOCKED-MISSING-SCENARIO-INPUT` | not a sealed member |

`decision_events` gains the sizing multiplier identity row required by design `:218`
("sizing decision adds multiplier identity"): `{sequence:1, decision:"SIZING_MULTIPLIER_IDENTITY",
contract_multiplier:2}`.

Blocked cells: `cash_events`, `fee_events`, `fill_events/0/liquidity_role`, `equity_curve/last`
(all `BLOCKED-MISSING-SCENARIO-INPUT`, discrepancy **D-01**); `metrics` and the complete
`decision_events` vocabulary (`BLOCKED-DESIGN-UNENUMERATED`); run-manifest record ids/digests
(`BLOCKED-MISSING-RECORD-BYTES`).

### RULE2-01-GREEN — `close_only_deterministic_v2`

Inputs (design `:216`): `sizing_equity=1000`, `fallback_size_pct=10`, `final_entry_fill=100`,
`stop` = a supplied quiet binary64 NaN with exact bits `0x7ff8000000000000` decoded by the scenario
input adapter, `cm=1`, `qty_step=1`, `min_qty=0`, `min_notional=0`, `slippage_bps=0`, `price_tick=1`,
`max_leverage_cap=10`.

```
stop supplied but not finite -> fallback branch                             [:197-198]
fallback_notional  = 1000 * (10/100)            = 100                       [:195]
fallback_raw_qty   = 100 / (100 * 1)            = 1                         [:196]
selected_raw_qty   = 1
leverage_cap_qty   = (1000 * 10) / (100 * 1)    = 100                       [:206]
raw_qty            = min(1, 100)                = 1                         [:207]
qty                = floor_to_qty_step(1, 1)    = 1                         [:208]
order_notional     = 1 * 100 * 1                = 100                       [:209]
final_entry_fill   = ceil_to_price_tick(100 + 0, 1) = 100
```

Legacy takes the same branch: `position_sizer.py:43` tests `sl is not None and math.isfinite(sl)`,
which a NaN fails, so `:48-50` computes `fallback_notional = equity * (fallback_size_pct/100)` then
`raw_qty = fallback_notional / entry` = `100 / 100` = `1`. Design `:212` states exactly this
("Those selector branches exactly preserve the current kernel guard and initializer").

Declared `rule2_green_projection` (design `:216` "both final quantities are `1`"; `:218` "no
behavioral projection changes on GREEN"):

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |
| `/RESULT_SURFACE/final_position/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |
| `/RESULT_SURFACE/order_notional` | `PRESENT(I:100)` | `PRESENT(I:100)` | yes |

The NaN stop is never serialized (design `:216` final sentence; design `:480` also refuses a
non-finite value in a comparison artifact), so no `stop_price` node exists on either surface — the
selector resolves **ABSENT** on both sides. This is recorded in the artifact's `no_serialized_nodes`
block rather than as a value.

---

## 2. DEF-P012-02 — real minimum-notional admission (design `:222-245`)

### RULE2-02-RED — `close_only_deterministic_v2`

Inputs (design `:241`): `sizing_equity=1000`, `risk_pct=1`, `final_fill=100`, `stop=90`, `cm=1`,
`slippage_bps=0`, `price_tick=1`, `max_leverage_cap=10`, `qty_step=1`, `min_qty=0`; legacy runtime
`min_notional=0` (design cites `config.py:48`, read this session: `"instrument_min_notional": 0.0`);
corrected frozen test record `min_notional=101`.

```
risk_amount      = 1000 * (1/100)     = 10
stop_distance    = |100 - 90|         = 10
risk_raw_qty     = 10 / (10 * 1)      = 1            (pre-floor quantity 1, design :241)
leverage_cap_qty = (1000 * 10)/(100*1) = 100
raw_qty          = min(1, 100)        = 1
floored_qty      = 1
order_notional   = 1 * 100 * 1        = 100                                 [:233]
corrected: admit iff 100 >= 101 -> FALSE -> REFUSED_MIN_NOTIONAL            [:234, :241]
           observed notional 100, required 101, opens no position           [:241]
legacy   : reject iff 100 < 0   -> FALSE -> opens                           (position_sizer.py:67)
```

Declared `rule2_divergent_projection` (design `:243`: "RED gains the typed refusal, removes
entry/position/fill-dependent events, and records the instrument digest"):

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/RESULT_SURFACE/refusals/0/code` | `ABSENT` | `PRESENT(S:"REFUSED_MIN_NOTIONAL")` | yes (absent vs present) |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:1)` | `PRESENT(A:0)` | yes |
| `/RESULT_SURFACE/final_position` | `PRESENT(O:…)` LONG qty 1 | `PRESENT(N)` null | yes |
| `/EVENT_SURFACE/decision_events/3/decision` | `ABSENT` | `PRESENT(S:"REFUSED_MIN_NOTIONAL")` | yes |

Derived empties: no position opens, so there is no fill, hence no fee cash event (design `:100`
attaches a fee to a fill) and no exit — `fill_events`, `cash_events`, `fee_events`, `exit_events` and
`funding_events` are all derivably `[]`. Equity is untouched, so `equity_curve` = `{first:1000,
last:1000}` is derived, not assumed.

### RULE2-02-GREEN — `close_only_deterministic_v2`

Same named inputs with `min_notional=100` on **both** adapters (design `:241`).

```
order_notional = 1 * 100 * 1 = 100
corrected: 100 >= 100  -> TRUE  -> admits   (equality passes because the legacy comparison
                                             is strict '<', design :236)
legacy   : 100 <  100  -> FALSE -> admits   (position_sizer.py:67)
```

Declared `rule2_green_projection` (design `:241` "equality passes and both open"; the probe at
`:245` binds "the admission/refusal projection"):

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/RESULT_SURFACE/admitted` | `PRESENT(B:1)` | `PRESENT(B:1)` | yes |
| `/EVENT_SURFACE/fill_events/0/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |
| `/RESULT_SURFACE/final_position/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |

Here the entry fill *does* occur, so `cash_events`/`fee_events` are blocked (**D-01**), unlike the
RED row.

---

## 3. DEF-P012-03 — frozen instrument metadata (design `:247-263`)

### RULE2-03-RED — `close_only_deterministic_v2`

Inputs (design `:259`): synthetic `BPS_OF_REFERENCE_V1` schedule with `slippage_bps=0`; synthetic
frozen record `price_tick=0.5`; runtime override `price_tick=0.25`; every other runtime economic
field equal to its frozen-record field.

```
corrected: runtime price_tick 0.25 != record price_tick 0.5
           -> REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION, before the first bar     [:143, :255, :259]
           -> "RED becomes a typed pre-evaluation refusal"                        [:261]
legacy   : InstrumentMetadata.from_config accepts and uses runtime 0.25           [:251, :259]
```

Declared `rule2_divergent_projection` (design `:261`):

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/RESULT_SURFACE/refusals/0/code` | `ABSENT` | `PRESENT(S:"REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION")` | yes |
| `/EVENT_SURFACE/decision_events/1/decision` | `ABSENT` | `PRESENT(S:"REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION")` | yes |
| `/EVENT_SURFACE/fill_events` | legacy evaluated run | `PRESENT(A:0)` | yes |
| consumed `price_tick` | `PRESENT(F:0.25)` | refusal — no value consumed | yes |

`0.5` and `0.25` are float nodes (fraction present, design `:480`). Their canonical enumerator forms
are `F:0x1.0000000000000p-1` and `F:0x1.0000000000000p-2` respectively — both exact powers of two,
hand-checked. This is informational; the artifact writes the tokens `0.5` and `0.25`.

Derived empties: the refusal precedes evaluation, so no scenario output exists — all five economic
containers are derivably `[]`.

### RULE2-03-GREEN — `close_only_deterministic_v2`

Inputs (design `:259`): same zero-impact schedule; `price_tick=0.5` on both sides; every runtime
field exactly equal to the frozen record.

```
corrected: no override mismatch -> identity validated -> no refusal    [:259, :261]
legacy   : identical economic values
```

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/RESULT_SURFACE/refusals` | `PRESENT(A:0)` | `PRESENT(A:0)` | yes |
| consumed `price_tick` | `PRESENT(F:0.5)` | `PRESENT(F:0.5)` | yes |
| `/RESULT_SURFACE/final_position` | `PRESENT(N)` | `PRESENT(N)` | yes |

The vector specifies no equity, entry or exit action, so the agreeing projection is only "identity
validated; no override refusal; `price_tick=0.5` consumed identically" — discrepancy **D-02**
(thin GREEN).

---

## 4. DEF-P012-04 — gap-aware protective stops (design `:265-291`)

### RULE2-04-RED — `close_only_deterministic_v2`

Inputs (design `:287`): existing long `quantity=1`, no active target, `stop=100`, `price_tick=1`,
`BPS_OF_REFERENCE_V1` with `slippage_bps=0`, next bar `open=90, high=95, low=85, close=92`.
**Not supplied:** entry basis, `contract_multiplier`, initial equity — discrepancy **D-03**.

```
Long, open(90) <= stop(100) -> trigger, reference (pre-slippage) = open = 90   [:277 table row 1]
slippage impact = |90| * 0 / 10_000 = 0                                        [:304]
sell (exit long) -> unrounded_fill = 90 - 0 = 90                               [:308]
final_fill = floor_to_price_tick(90, 1) = 90                                   [:308]
fill_trigger = GAP_OPEN                                                        [:289]
slippage_application_count = 1                                                 [:311]
a gap is never improved back to the stop                                       [:283]
```

Legacy: the `close_only_deterministic_v2` profile triggers from close and fills at close (design
`:269`). Independently confirmed at `exits.py:424-447`: `_evaluate_close_only_stop_hit` returns no
hit when `bar.close > stop_price` (for a long) and otherwise returns `fill_price=bar.close`. Here
`close 92 > stop 100` is false, so the legacy fill price is **92**.

Declared `rule2_divergent_projection` (design `:289`; the probe at `:291` fixes the fill-price node):

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/reference_price` | `PRESENT(I:92)` | `PRESENT(I:90)` | yes |
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:92)` | `PRESENT(I:90)` | yes |
| `/EVENT_SURFACE/fill_events/0/fill_trigger` | `ABSENT` | `PRESENT(S:"GAP_OPEN")` | yes |
| gross PnL / cash / equity / trade / metrics | — | `BLOCKED-MISSING-SCENARIO-INPUT` | not sealed |

Conditional note, **not sealed**: were the entry basis `100` and `cm=1` as in the sibling vectors,
corrected gross would be `(90-100)*1*1 = -10` and legacy `(92-100)*1*1 = -8` — still divergent. The
vector does not state them, so those cells stay blocked rather than being guessed (**D-03**).

OPEN-06 binding: see §0.5. The corrected value 90 is taken from design `:287`, and the owner's
P19-RETIRE / P20-RETAIN disposition makes it the disposition-consistent behaviour.

### RULE2-04-GREEN — `close_only_deterministic_v2`

Inputs (design `:287`): same quantity, absent target, tick and zero-impact record; `stop=100`,
bar `open=105, high=106, low=101, close=104`.

```
corrected gap-aware: open(105) <= stop(100)? no.  low(101) <= stop(100)? no.
                     -> neither predicate -> no stop fill                    [:281 table row 5]
legacy close-only  : close(104) > stop(100) -> no hit                        (exits.py:435-436)
```

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/EVENT_SURFACE/exit_events` | `PRESENT(A:0)` | `PRESENT(A:0)` | yes |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:0)` | `PRESENT(A:0)` | yes |
| `/RESULT_SURFACE/final_position/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |

`exit_events` and `fill_events` exist in the legacy shape (design `:593` lists one `ExitEvent` in
current `core/types.py`), so both sides resolve `A:0` and the pair is a valid GREEN member — unlike
`fee_events`/`funding_events`, which do not exist at `1.0.0` at all (see C-02).

Derived empties: no fill, therefore no fee (design `:100`); the vector spans no funding interval.

---

## 5. DEF-P012-05 — in-path slippage, applied exactly once (design `:293-319`)

### RULE2-05-RED — `close_only_deterministic_v2`

Inputs (design `:315`): buy intent, `reference=100`, `slippage_bps=100`, `price_tick=0.01`,
`requested_quantity=1`. `contract_multiplier` is not restated — `cm=1` is taken from the shipped
kernel default `"instrument_contract_multiplier": 1.0` at `config.py:49` (design `:145` states the
same), tagged `(cm-default)` and recorded as discrepancy **D-06**.

```
impact          = |100| * 100 / 10_000        = 1                           [:304]
buy -> unrounded_fill = 100 + 1               = 101                         [:305]
final_fill      = ceil_to_price_tick(101, 0.01) = 101                       [:307]  (already aligned)
slippage_application_count = 1                                              [:311]
order_notional  = 1 * 101 * 1                 = 101                         (cm-default)
```

Legacy passes the reference price through with no cost adjustment (design `:297`), so the legacy fill
is **100**.

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/reference_price` | `ABSENT` | `PRESENT(I:100)` | yes (absent vs present) |
| `/EVENT_SURFACE/fill_events/0/slippage_impact` | `ABSENT` | `PRESENT(I:1)` | yes |
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:100)` | `PRESENT(I:101)` | yes |
| `/EVENT_SURFACE/fill_events/0/slippage_application_count` | `ABSENT` | `PRESENT(I:1)` | yes |

Design `:317` also lists entry-relative stops/targets, notional, fee basis, PnL and equity as RED
changes "as applicable"; this vector has no stop, target, schedule or equity, so those selectors
resolve ABSENT on both sides or are blocked, and are **not** sealed divergent members.

`price_tick 0.01` is a float node; its canonical form is `F:0x1.47ae147ae147bp-7` (hand-derived:
`0.01 / 2^-7 = 1.28`; hex fraction `47ae147ae147a|e14…`, next digit `e` = 14 ≥ 8, round up to
`…47b`). Informational only.

### RULE2-05-GREEN — `close_only_deterministic_v2`

Inputs (design `:315`): same reference `100`, tick `0.01`, quantity `1`, `slippage_bps=0`.

```
impact = |100| * 0 / 10_000 = 0
buy -> unrounded_fill = 100 + 0 = 100 ; ceil_to_price_tick(100, 0.01) = 100
corrected final_fill = 100 ; legacy final_fill = 100
```

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:100)` | `PRESENT(I:100)` | yes |

Design `:317` requires corrected artifacts to retain explicit zero-impact lineage. The nodes
`slippage_model_id`, `slippage_bps`, `slippage_impact` and `slippage_application_count` carry it.
They are **version-specific added nodes** and, per design `:181`, are excluded from the cross-version
GREEN equality and compared against their own expected artifact instead. The artifact records this in
its `version_specific_lineage_nodes` block.

---

## 6. DEF-P012-06 — named same-bar collision policy (design `:321-347`)

### RULE2-06-RED — `raw_close_only_v1`

Inputs (design `:343`): synthetic long, `entry_fill=100`, `reference_quantity=2`, `qty_step=1`,
`stop=90`, `TARGET-NEAR` at `105` with fraction `0.5`, `TARGET-FAR` at `110` with fraction `0.5`,
`price_tick=1`, `BPS_OF_REFERENCE_V1` with `slippage_bps=0`, bar `open=100, high=115, low=85,
close=105`, corrected policy `TARGET_FIRST`. `contract_multiplier` not restated — `cm=1`
(cm-default, **D-06**). Initial equity not given — absolute equity blocked (**D-04**).

Touch check (design `:343` "The two targets and stop all touch"): `high 115 >= 110` and
`high 115 >= 105`; `low 85 <= 90`. Confirmed against the profile's own evaluators —
`raw_close_only_v1` takes the OHLC branch at `exits.py:362-363`, which evaluates stop and target
independently.

```
TARGET_FIRST: touched targets nearest to entry first; long ascending target price   [:336]
              apply each target's declared fraction to the reference quantity        [:336]
TARGET-NEAR exit qty = 0.5 * 2 = 1  @ reference 105
TARGET-FAR  exit qty = 0.5 * 2 = 1  @ reference 110
remaining   = 2 - 1 - 1 = 0  -> no stop remainder                                    [:336]
slippage_bps 0, sell: floor_to_price_tick(105, 1) = 105 ; floor_to_price_tick(110, 1) = 110
ordered chosen exit ids = [TARGET-NEAR, TARGET-FAR]                                  [:336 receipt]
gross realized PnL (cm-default cm = 1):
  TARGET-NEAR: (105 - 100) * 1 * 1 =  5
  TARGET-FAR : (110 - 100) * 1 * 1 = 10
  lifecycle gross total            = 15
```

Legacy: the OHLC dispatcher at `exits.py:365-374` returns, when stop and target both hit,
`fill_price=stop_hit.fill_price`, `exit_pct=1.0`, `is_pessimistic=True`, `exit_id=stop_hit.exit_id`.
The stop reference itself comes from `exits.py:400-406`: `open 100 <= stop 90` is false, `low 85 <=
90` is true, so `fill_price = stop_price = 90`. Legacy therefore exits the full quantity `2` at `90`
with `gross = (90-100)*2*1 = -20` — exactly what design `:343` states.

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/exit_id` | `PRESENT(S:"STOP")` | `PRESENT(S:"TARGET-NEAR")` | yes |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:1)` | `PRESENT(A:2)` | yes |
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:90)` | `PRESENT(I:105)` | yes |
| `/EVENT_SURFACE/fill_events/1/final_fill_price` | `ABSENT` | `PRESENT(I:110)` | yes |
| `/RESULT_SURFACE/collision/ordered_chosen_exit_ids` | `ABSENT` (policy is implicit at 1.0.0, design `:325`) | `PRESENT(A:2)` `["TARGET-NEAR","TARGET-FAR"]` | yes |
| `/RESULT_SURFACE/collision/is_pessimistic` | `PRESENT(B:1)` (`exits.py:370`) | `PRESENT(B:0)` | yes |
| lifecycle gross realized PnL | `PRESENT(I:-20)` (cm-default) | `PRESENT(I:15)` (cm-default) | yes |
| absolute equity | — | `BLOCKED-MISSING-SCENARIO-INPUT` (**D-04**) | not sealed |

Design `:345` names "chosen exit id/reason, price, pessimistic/ambiguity fields, PnL, equity, and
metrics" plus "policy id and collision decision events" — the rows above cover every one that this
vector supplies inputs for.

### RULE2-06-EQUAL-PRICE-RED — `raw_close_only_v1` (v1.4 micro-fold, design `:343`, `:454`, `:645`)

Inputs: the exact `RULE2-06-RED` inputs **except that `TARGET-FAR` is also at `105`** (design `:343`).
Both equal-price targets and the stop touch (`high 115 >= 105`; `low 85 <= 90`).

Tie-break derivation (design `:336` "equal prices by `exit_id` UTF-8 byte order"):

```
TARGET-NEAR = 54 41 52 47 45 54 2D 4E 45 41 52
TARGET-FAR  = 54 41 52 47 45 54 2D 46 41 52
common prefix "TARGET-" = 54 41 52 47 45 54 2D  (7 bytes, identical)
byte 8: TARGET-FAR = 0x46 ('F') ; TARGET-NEAR = 0x4e ('N') ; 0x46 < 0x4e
-> TARGET-FAR orders first
```

```
TARGET-FAR  exit qty = 0.5 * 2 = 1 @ 105   (fill sequence 0)
TARGET-NEAR exit qty = 0.5 * 2 = 1 @ 105   (fill sequence 1)
remaining = 0 -> no stop remainder
ordered chosen exit ids = [TARGET-FAR, TARGET-NEAR]
gross realized PnL (cm-default): each (105 - 100) * 1 * 1 = 5 ; lifecycle total = 10
```

Legacy is unchanged from RULE2-06-RED (the stop still wins the implicit collision): full quantity `2`
at `90`, gross `-20`, `is_pessimistic=True`.

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/exit_id` | `PRESENT(S:"STOP")` | `PRESENT(S:"TARGET-FAR")` | yes |
| `/EVENT_SURFACE/fill_events/1/exit_id` | `ABSENT` | `PRESENT(S:"TARGET-NEAR")` | yes |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:1)` | `PRESENT(A:2)` | yes |
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:90)` | `PRESENT(I:105)` | yes |
| `/RESULT_SURFACE/collision/ordered_chosen_exit_ids` | `ABSENT` | `PRESENT(A:2)` `["TARGET-FAR","TARGET-NEAR"]` | yes |
| lifecycle gross realized PnL | `PRESENT(I:-20)` | `PRESENT(I:10)` | yes |

Design `:343` states the declared divergent projection for this scenario is "the ordered chosen exit
ids and fill-event sequence", which the first five rows carry.

### RULE2-06-GREEN — `raw_close_only_v1`

Inputs (design `:343`): same position, quantity step, stop, two targets, fractions, tick,
zero-impact record and policy; bar `open=100, high=104, low=85, close=95`.

```
targets: high 104 >= 105 ? no ; >= 110 ? no  -> neither target touches
stop   : low  85  <= 90  ? yes               -> stop touches
only one class touches -> all three policies select it                        [:339]
stop reference: open 100 <= 90 ? no ; low 85 <= 90 ? yes -> reference = stop = 90  [:279 row 2]
slippage_bps 0, sell: floor_to_price_tick(90, 1) = 90
both versions fill the full quantity 2 at 90                                  [:343]
gross realized PnL (cm-default) = (90 - 100) * 2 * 1 = -20  on BOTH versions
```

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| chosen exit class / `fill_events/0/exit_id` | `PRESENT(S:"STOP")` | `PRESENT(S:"STOP")` | yes |
| `/EVENT_SURFACE/fill_events/0/quantity` | `PRESENT(I:2)` | `PRESENT(I:2)` | yes |
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:90)` | `PRESENT(I:90)` | yes |
| lifecycle gross realized PnL | `PRESENT(I:-20)` | `PRESENT(I:-20)` | yes |

The cm-default affects both versions identically here, so the GREEN equality does not depend on it.
`collision.is_pessimistic` is `B:0` on both sides: the legacy raw dispatcher only sets
`is_pessimistic=True` in the both-hit branch at `exits.py:366-374`, and this bar takes the
stop-only branch at `exits.py:375-376`.

**OPEN-02 conflict (D-12).** The owner has answered OPEN-02 with `STOP_FIRST` as the *mandatory*
same-bar policy for acceptance-bearing `2.0.0` runs. The two RED scenarios above declare
`TARGET_FIRST` as an explicit scenario input, and `RULE2-06-EQUAL-PRICE-RED` exists specifically to
exercise the `TARGET_FIRST` equal-price tie-break. The OPEN-06 proposal's own P23 row makes that
tie-break applicable only "IF `TARGET_FIRST` IS CHOSEN"
(`P012_OPEN06_RETAINED_RETIRED_PROPOSAL_V1.md:65`), and the applicability draft records P23 as
"not-applicable-under-STOP_FIRST". Design `:331` nevertheless states that closing OPEN-06 "may not
silently rewrite this pair", and the lane brief directs that the design's synthetic numbers govern
scenario values. **This bundle therefore seals `TARGET_FIRST` for the RULE2-06 RED pair and raises
the conflict for owner/§16 resolution.** Under `STOP_FIRST` both RED scenarios would collapse onto
the legacy result and DEF-P012-06 would have no divergent projection at all, which design §15.4
refuses as "correction without divergence".

---

## 7. DEF-P012-07 — provenanced real fee schedule (design `:349-388`)

### RULE2-07-RED — `close_only_deterministic_v2`

Inputs (design `:384`): `initial_equity=1000`, long round trip `quantity=1`, entry and exit final
fills `100`, `cm=1`, `BPS_OF_REFERENCE_V1` with `slippage_bps=0`, `price_tick=1`, two **taker**
fills, `taker_rate=0.001`, `fixed_component=0`, `minimum_fee=0`, no funding event, rounding rule
`EXACT_IDENTITY_V1` defined for this fixture as `round_and_apply_minimum(x) = x`. Guard settings:
only the consecutive-loss guard enabled, test-only `max_consecutive_losses=1`, all other L16 guards
and guard recovery disabled.

```
per fill (design :360-364):
  fee_notional   = |100 * 1 * 1|            = 100                            [:360]
  raw_fee        = 100 * 0.001 + 0          = 0.1                            [:361]
  fee_amount     = EXACT_IDENTITY_V1(0.1)   = 0.1                            [:362, :384]
  fee_cash_delta = -0.1                                                       [:363]
two fills (entry F0, exit F1) -> two fee cash events, each -0.1              [:384]

gross_realized_pnl = (100 - 100) * 1 * 1 = 0                                 [:378, :384]
net_trade_pnl      = 0 + (-0.1) + (-0.1) = -0.2                              [:378, :384]
corrected equity   = 1000 - 0.1 - 0.1     = 999.8                            [:384; exact, see 0.6]
legacy             : gross 0, no v2 net field, equity stays 1000             [:353, :384]
```

Cash-ledger ordering (design `:100-101`, §3 steps 10-12) and the typed-projection join
(design `:75`, `:376`):

```
entry fill F0 -> cash_events[0] = FEE(F0)                -0.1   cash_event_id CE-FEE-0
exit  fill F1 -> cash_events[1] = FEE(F1)                -0.1   cash_event_id CE-FEE-1
              -> cash_events[2] = GROSS_REALIZATION(F1)     0   cash_event_id CE-GROSS-1
fee_events[0] joins CE-FEE-0 ; fee_events[1] joins CE-FEE-1
each fee_cash_delta equals the joined cash row's signed_delta                [:75, :376]
gross realization appears ONLY in cash_events                                [:75]
only cash_events are applied to equity: 1000 + (-0.1) + (-0.1) + 0 = 999.8   [:75]
```

Guard derivation (design `:380`, `:384`; `DECISIONS.md:31` D017 "Interim daily/consecutive-loss PnL
is gross minus fees"; `runner.py:734-738` read this session — the counter increments when
`self.state.last_realized_pnl < 0.0` on a full close and resets otherwise; `runner.py:780-783` — the
predicate is `self._l16_consec_loss_count < int(self.config["max_consecutive_losses"])`, and
`runner.py:793-794` folds it into `guard_blocked_raw`):

```
legacy   : the full close stores gross last_realized_pnl = 0
           (0 < 0.0) is false -> count = 0 -> consec_loss_ok = true -> guard_blocked_raw = false
corrected: guard_pnl_basis = GROSS_MINUS_FEES ; last_closed_guard_pnl = -0.2
           (-0.2 < 0.0) is true -> count = 1
           predicate (1 < 1) is false -> consec_loss_ok = false -> guard_blocked_raw = true
this no-funding fixture does not decide OPEN-10                              [:384]
```

Declared `rule2_divergent_projection` (design `:386`):

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fee_events` | `ABSENT` (no such container in `LEGACY_P011_EXACT_V1`, design `:476`, `:353`) | `PRESENT(A:2)`, each `fee_cash_delta` `F:-0.1` | yes |
| `/RESULT_SURFACE/trades/0/net_trade_pnl` | `ABSENT` (single `pnl` field, design `:353`) | `PRESENT(F:-0.2)` | yes |
| `/RESULT_SURFACE/guards/guard_pnl_basis` | `ABSENT` | `PRESENT(S:"GROSS_MINUS_FEES")` | yes |
| `/RESULT_SURFACE/guards/last_closed_guard_pnl` | `ABSENT` | `PRESENT(F:-0.2)` | yes |
| `/RESULT_SURFACE/guards/consecutive_loss_count` | `PRESENT(I:0)` | `PRESENT(I:1)` | yes |
| `/RESULT_SURFACE/guards/guard_blocked_raw` | `PRESENT(B:0)` | `PRESENT(B:1)` | yes |
| `/RESULT_SURFACE/equity_curve/last` | `PRESENT(I:1000)` | `PRESENT(F:999.8)` | yes (value and kind) |

`gross_realized_pnl` is `0` on both versions and is therefore **not** a divergent member (correction
C-07). `0.001`, `0.1`, `-0.1`, `-0.2` and `999.8` are float nodes; `100`, `0`, `1` and `1000` are
integer nodes.

Blocked cells: the exit intent is unnamed, so `fill_events/1/event_class`,
`fee_events/1/event_class`, `exit_events/0/exit_id` and `exit_events/0/reason` are
`BLOCKED-MISSING-SCENARIO-INPUT` (**D-05**); `event_timestamp`, `lifecycle_id` and
`settlement_currency` are not stated by the vector; `schedule_id`/`schedule_digest` are
`BLOCKED-MISSING-RECORD-BYTES`. The economically load-bearing fields — `rate 0.001`,
`fixed_component 0`, `fee_notional 100`, `fee_amount 0.1`, `fee_cash_delta -0.1`,
`liquidity_role TAKER` — are all sealed from the vector.

### RULE2-07-GREEN — `close_only_deterministic_v2`

Inputs (design `:384`): `initial_equity=1000`, an **empty fill-event input**, the same zero-impact
model/parameter record, the same guard settings.

```
no fills -> no fee events, no gross realization, no position, no exit
both versions: equity 1000 ; consecutive_loss_count 0 ; position/trade/guard projections unchanged
```

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/RESULT_SURFACE/equity_curve/last` | `PRESENT(I:1000)` | `PRESENT(I:1000)` | yes |
| `/RESULT_SURFACE/guards/consecutive_loss_count` | `PRESENT(I:0)` | `PRESENT(I:0)` | yes |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:0)` | `PRESENT(A:0)` | yes |
| `/RESULT_SURFACE/final_position` | `PRESENT(N)` | `PRESENT(N)` | yes |

`fee_events` and `funding_events` are **excluded** from this GREEN projection (correction C-02):
they do not exist in the legacy shape, so the legacy selector resolves ABSENT and design `:510` would
score `ABSENT` versus `A:0` as divergence. They are version-specific added containers under design
`:181`.

`/RESULT_SURFACE/guards/last_closed_guard_pnl` is deliberately **ABSENT** rather than `0`: no
lifecycle closes in this fixture, and design `:508` makes missing and zero different nodes.

### 7.1 Note on the guard-basis authority

Design `:380` cites `DECISIONS.md:31` for the interim gross-minus-fees basis. That line was read this
session and reads: "D017 | 2026-07-18 | Interim daily/consecutive-loss PnL is gross minus fees;
funding capture is deferred and live remains blocked." The owner's OPEN-10 answer extends exactly
this rule to `2.0.0` for all three controls with no per-control divergence.

---

## 8. DEF-P012-08 — per-interval funding and `funding_events` (design `:390-433`)

### RULE2-08-RED — `close_only_deterministic_v2`

Inputs (design `:429`): funding-only event, `lifecycle_id=1`, `initial_equity=1000`, `open_qty=1`,
`mark=100`, `cm=1`, `event_id="TEST-FUND-1"`, `event_timestamp="2000-01-01T00:00:00Z"`,
`raw_rate=0.001`, venue convention **LONG pays positive**; the position is open immediately before
and after the event timestamp under the synthetic snapshot rule, so it is eligible.

```
notional           = |100 * 1 * 1|                    = 100                  [:403]
convention "positive rate paid by LONG"
                   -> long_cashflow_rate = -raw_rate  = -0.001               [:404]
side_factor (long) = +1                                                       [:406]
funding_cash_delta = 100 * (-0.001) * (+1)            = -0.1                 [:407, :429]
negative delta debits equity                                                  [:410]
corrected equity   = 1000 + (-0.1)                    = 999.9                [:429; exact, see 0.6]
cumulative_funding = -0.1
```

Legacy has no funding ledger and no funding cashflow at all (design `:394`; `core/types.py` has no
funding fields per design `:593`), so legacy equity stays `1000`.

Ledger and join (design `:414-423`): one funding-kind `cash_events` row
`{cash_event_id:"CE-FUND-0", kind:"FUNDING", lifecycle_id:1, signed_delta:-0.1}` and one
`funding_events` row that is its typed projection, joined by `cash_event_id`, with
`funding_cash_delta == -0.1 ==` the joined cash row's signed delta. Only the cash row is applied to
equity. `fill_events` is `A:0` because design `:429` states neither RULE2-08 vector contains a fill
intent, so §3's fill-only slippage sequence is not entered and no `CostSchedule` is consumed.

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/funding_events` | `ABSENT` | `PRESENT(A:1)`, `funding_cash_delta` `F:-0.1` | yes |
| `/EVENT_SURFACE/cash_events` | `ABSENT` | `PRESENT(A:1)` funding-kind `F:-0.1` | yes |
| `/RESULT_SURFACE/cumulative_funding` | `ABSENT` | `PRESENT(F:-0.1)` | yes |
| `/RESULT_SURFACE/equity_curve/last` | `PRESENT(I:1000)` | `PRESENT(F:999.9)` | yes (value and kind) |

Sealed `funding_events[0]` fields, all from the vector and the §14 field list at `:417-420`:
`sequence 0`, `funding_event_id "TEST-FUND-1"`, `event_timestamp "2000-01-01T00:00:00Z"`,
`lifecycle_id 1`, `position_side "LONG"`, `open_qty 1`, `contract_multiplier 1`, `mark_price 100`,
`raw_rate 0.001`, `positive_rate_payer "LONG"`, `long_cashflow_rate -0.001`, `notional 100`,
`funding_cash_delta -0.1`, `cumulative_funding -0.1`, `cash_event_id "CE-FUND-0"`. Float nodes:
`raw_rate`, `long_cashflow_rate`, `funding_cash_delta`, `cumulative_funding`, equity. Integer nodes:
`sequence`, `lifecycle_id`, `open_qty`, `contract_multiplier`, `mark_price`, `notional`.
`schedule_id`, `schedule_digest` and `source_event_digest` are `BLOCKED-MISSING-RECORD-BYTES`.

Guard outcome (design `:431` "Guard outcomes follow the sourced OPEN-10 decision and are explicit
comparison nodes"): under the owner's OPEN-10 answer the guard basis stays gross-minus-fees and the
captured funding delta does **not** enter it, so `guard_pnl_basis = "GROSS_MINUS_FEES"`,
`funding_included_in_guard_basis = false`, `consecutive_loss_count = 0` (no lifecycle closes).

### RULE2-08-GREEN — `close_only_deterministic_v2`

Inputs (design `:429`): `lifecycle_id=1`, the same complete schedule containing `TEST-FUND-1`, the
same snapshot rule and initial equity `1000`, but the position is **closed immediately before** the
event timestamp.

```
required event coverage present -> not REFUSED_MISSING_FUNDING_EVENT          [:425, :429]
no position eligible at the event timestamp -> no funding row emitted         [:429]
no fill intent in either vector -> no fill, no fee, no gross realization      [:429]
both versions: economic cash/equity projection = 1000                         [:429]
```

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/RESULT_SURFACE/equity_curve/last` | `PRESENT(I:1000)` | `PRESENT(I:1000)` | yes |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:0)` | `PRESENT(A:0)` | yes |
| `/RESULT_SURFACE/final_position` | `PRESENT(N)` | `PRESENT(N)` | yes |

`funding_events` and `RESULT_SURFACE/cumulative_funding` are **excluded** from this GREEN projection
(corrections C-02 / C-03) and recorded as version-specific added nodes. The declared GREEN member is
the economic cash/equity value `1000` that design `:429` names.

`trades` is written `[]` on the reading that the pre-window close named by the vector supplies no
fill facts and mutates no equity (the vector fixes the projection at 1000). That reading is a
judgement call and is recorded in the artifact and as discrepancy **D-05**.

---

## 9. Catalog conservation recount (design's own declaration arithmetic)

Re-counted from the v1.4 design itself, **not** from the lane spec:

| Owning DEF | RED rows | GREEN rows | PROBE ids | Design lines |
|---|---|---|---|---|
| DEF-P012-01 | RULE2-01-RED | RULE2-01-GREEN | PROBE-P012-01-A, PROBE-P012-01-B | `:216`, `:220` |
| DEF-P012-02 | RULE2-02-RED | RULE2-02-GREEN | PROBE-P012-02-A | `:241`, `:245` |
| DEF-P012-03 | RULE2-03-RED | RULE2-03-GREEN | PROBE-P012-03-A | `:259`, `:263` |
| DEF-P012-04 | RULE2-04-RED | RULE2-04-GREEN | PROBE-P012-04-A | `:287`, `:291` |
| DEF-P012-05 | RULE2-05-RED | RULE2-05-GREEN | PROBE-P012-05-A, PROBE-P012-05-B | `:315`, `:319` |
| DEF-P012-06 | RULE2-06-RED, **RULE2-06-EQUAL-PRICE-RED** | RULE2-06-GREEN | PROBE-P012-06-A | `:343`, `:347`, `:454` |
| DEF-P012-07 | RULE2-07-RED | RULE2-07-GREEN | PROBE-P012-07-A | `:384`, `:388` |
| DEF-P012-08 | RULE2-08-RED | RULE2-08-GREEN | PROBE-P012-08-A | `:429`, `:433` |

**Totals: RED = 9, GREEN = 8, PROBE = 10, catalog rows = 27.**

Cross-checks against the design's own conservation statements:

- `:541` "all nine RED scenarios exhibited their declared old/new differences" ⇒ 9 RED ✓
  (8 numbered plus `RULE2-06-EQUAL-PRICE-RED`; the v1.4 micro-fold row `DS18-F01` at `:645` records
  that it "sweeps the RED receipt count from eight to nine").
- `:542` "all eight GREEN projections agreed" ⇒ 8 GREEN ✓ (the equal-price RED has no GREEN sibling;
  design `:343` declares it as "one additional declared synthetic `RED` scenario").
- `:454` "For each DEF, the catalog contains its declared RED row, GREEN row, and every declared
  `probe_id` exactly once; it also contains the additional DEF-P012-06 `RULE2-06-EQUAL-PRICE-RED` row
  exactly once" ✓ — verified mechanically: the emitted catalog has 27 rows and 27 unique
  `scenario_id` values.
- `:174-179` fail-probe contract: each declared `probe_id` binds exactly once to a `PROBE` catalog
  row; the per-DEF probe counts match each correction section's "Fail probe(s)" paragraph; total 10 ✓.

Expected-surface artifacts authored: one file per RED/GREEN scenario → **17 files** under
`golden/corrected_vnext/`, each carrying both `EVENT_SURFACE` and `RESULT_SURFACE`. PROBE rows carry
no expected artifact of their own; each compares its variant output to the independently sealed
producer named by its `base_scenario_id` (design `:465`).

---

## 10. Probe rows — bindings and first-changed-node derivations

Each row's `expected_first_changed_node` is the node the design names, evaluated against this
bundle's node layout. Where a *different* node would be enumerated earlier under design `:508`'s
UTF-8-byte-order object walk, that is recorded rather than silently substituted (**D-14**).

| Probe | Base | Kind | Expected failed check | Design-named node | Enumeration note |
|---|---|---|---|---|---|
| PROBE-P012-01-A | RULE2-01-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/quantity` | if the variant also rewrites `decision_events/1/contract_multiplier`, `decision_events` sorts before `fill_events` and would fail first |
| PROBE-P012-01-B | RULE2-01-GREEN | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/quantity` | expected 1, variant 0 |
| PROBE-P012-02-A | RULE2-02-GREEN | KERNEL | RULE-2 GREEN cross-version | `/RESULT_SURFACE/admitted` | the cross-version check compares only the declared shared projection (design `:476`), so earlier full-surface changes belong to the separate corrected-expectation check |
| PROBE-P012-03-A | RULE2-03-RED | INPUT | record-identity preflight | `BLOCKED-MISSING-RECORD-BYTES` | the refusal precedes any scenario output, so no comparison-surface node exists; the changed artifact is the record file, whose bytes the design never lists (**D-15**) |
| PROBE-P012-04-A | RULE2-04-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `decision_events/1/reference_price`, `decision_events/1/reference_source` and `fill_events/0/fill_trigger` all change and sort earlier (`fill_trigger` < `final_fill_price` because byte 3 is `l` 0x6c vs `n` 0x6e) |
| PROBE-P012-05-A | RULE2-05-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/final_fill_price` | actual 100 vs expected 101; `final_fill_price` sorts before `slippage_*` and `unrounded_fill_price`, so it is genuinely first |
| PROBE-P012-05-B | RULE2-05-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/final_fill_price` | actual 102 vs expected 101; design `:311` also refuses the second application via `slippage_application_count` |
| PROBE-P012-06-A | RULE2-06-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/exit_id` | design `:347` fixes expected first fill `TARGET-NEAR` vs variant `TARGET-FAR`; in this layout `decision_events/2/ordered_chosen_exit_ids/0` carries the same reversal and sorts earlier |
| PROBE-P012-07-A | RULE2-07-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fee_events/1/liquidity_role` | the vector states no maker rate, so whether `fee_amount`/`fee_cash_delta`/`cash_events/1/signed_delta` also change is underivable; if they do, `cash_events` sorts before `fee_events` (**D-16**) |
| PROBE-P012-08-A | RULE2-08-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | expected −0.1 vs variant +0.1; `cash_events/0/signed_delta` carries the same flip and sorts earlier, so the catalog records it as the first changed node |

Modified-copy trees, modification manifests, their digests, and every serialized scenario-input digest
are `BLOCKED-BUILD-ARTIFACT` (**D-10**): design `:459-465` requires a complete kernel variant tree
plus a `KERNEL_FILE_PATCH` with before/after file digests, and no corrected kernel source exists
pre-implementation. `IMPLEMENTATION_BASE_SHA` is likewise not yet fixed.

---

## 11. Discrepancies

Design ambiguities and prompt/evidence conflicts that forced a judgement call. These are reported,
not silently resolved (clause C-2; lane W127 line 54).

- **D-01** Design `:100` mandates a fee cash event for every executed fill, but RULE2-01, RULE2-02-GREEN,
  RULE2-05 and the RULE2-06 family supply no `CostSchedule`, and design `:149` refuses a missing
  schedule rather than defaulting it. Those `cash_events`/`fee_events`/`liquidity_role` cells are
  `BLOCKED-MISSING-SCENARIO-INPUT`, not guessed as zero. Strictly read, `:149` would make the corrected
  adapter refuse these scenarios outright, which contradicts the concrete corrected quantities the
  design states for them.
- **D-02** RULE2-03-GREEN specifies no equity, entry or exit action, so its cross-version projection
  has no positive economic value — only "identity validated; no override refusal".
- **D-03** RULE2-04-RED omits entry basis, `contract_multiplier` and initial equity, yet design `:289`
  requires gross PnL, cash/equity, trade and metrics to change on RED. Those cells are
  `BLOCKED-MISSING-SCENARIO-INPUT`; only the fill-price/`fill_trigger` divergence — the node the
  design's own probe at `:291` fixes — is sealed.
- **D-04** RULE2-06-RED, RULE2-06-GREEN and RULE2-06-EQUAL-PRICE-RED omit initial equity; absolute
  equity and metric cells are blocked. Gross realized PnL is sealed under the cm-default.
- **D-05** RULE2-07-RED says "long round trip" and RULE2-07-GREEN says "empty fill-event input"
  without naming the exit intent; `exit_events/0/exit_id`, `exit_events/0/reason` and the exit
  `event_class` are blocked. Relatedly, RULE2-08-GREEN names a pre-window close with no fill facts;
  `trades` is written `[]` as a recorded judgement call.
- **D-06** `contract_multiplier` is not restated in RULE2-04, RULE2-05 or the RULE2-06 family. It is
  taken as `cm = 1` from the shipped kernel default at `config.py:49` (design `:145` states the same)
  and tagged `(cm-default)` — a cited default, not an invented number. Every affected divergence uses
  the same `cm` on both versions, so no old-versus-new difference depends on it.
- **D-07 / D-08** *(resolved by this lane, was open in the partial)* The design's decimals `999.8`
  (`:384`) and `999.9` (`:429`) were shown in §0.6 to be exactly the binary64 results of the stated
  accumulations. No residual ULP ambiguity.
- **D-09** Bundle format: expected surfaces are authored one file per scenario with two nested
  surface keys, plus non-schema `provenance`, `open_item_bindings` and `blocked_cells` members. The
  design fixes `EXPECTED_ROOT` but not a per-surface file split; a file-per-surface split, and
  stripping the authoring metadata, are mechanical if the Gate-2 build requires them.
- **D-10** PROBE modified-copy digests, patch digests, serialized scenario-input digests and all
  `observed/` digests are `BLOCKED-BUILD-ARTIFACT`. This bundle seals only the `2.0.0` expected values
  and the catalog structure.
- **D-11** *(reclassified from the partial)* The additive `CORRECTED_V2` result/event schema was
  OPEN-09 in the partial. The owner has now answered OPEN-09 `APPLICABLE / schema APPROVED`, so this
  is no longer an OPEN block. What remains is that the approval does not enumerate a metric node set
  or a complete `decision_events` vocabulary — recorded as `BLOCKED-DESIGN-UNENUMERATED`.
- **D-12** **OPEN-02 versus the declared RULE2-06 RED pair.** The owner answered OPEN-02 with
  `STOP_FIRST` as the mandatory policy for acceptance-bearing `2.0.0` runs, while design `:343`
  declares `TARGET_FIRST` as an explicit input of `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED`, and
  the OPEN-06 proposal records P23 (the equal-price tie-break) as not-applicable under `STOP_FIRST`
  (`P012_OPEN06_RETAINED_RETIRED_PROPOSAL_V1.md:65`). Design `:331` forbids closing OPEN-06 from
  silently rewriting the pair, so this bundle seals `TARGET_FIRST`. Under `STOP_FIRST` both RED
  scenarios would collapse onto the legacy result and DEF-P012-06 would have no divergent projection,
  which design §15.4 refuses. **Owner resolution required.**
- **D-13** The design fixes the six `EVENT_SURFACE` container names and the exact `fee_events` /
  `funding_events` row field lists, but it does **not** fix `RESULT_SURFACE` member names beyond the
  categories at `:474`, nor the `decision_events` reason vocabulary, nor the `fill_events` /
  `cash_events` / `exit_events` field names. Those names are authored by this lane. Node pointers —
  and therefore every "first changed node" — depend on them.
- **D-14** Consequence of D-13: for four probes the design's named refusal node is not necessarily the
  first node the enumerator reaches. Recorded per probe in §10 and in each catalog row's `note`.
- **D-15** `PROBE-P012-03-A` refuses before any scenario output exists, so it has no
  comparison-surface node to name. Its `expected_first_changed_node` is recorded as
  `BLOCKED-MISSING-RECORD-BYTES` — the changed artifact is the frozen record file, whose bytes and
  detached `.sha256` the design never lists.
- **D-16** `PROBE-P012-07-A` reclassifies a taker exit as maker, but the RULE2-07 vector states no
  maker rate, so whether the fee amount and the joined cash delta also change is underivable. Only
  the role node is certain to differ.
- **D-17** The lane brief anticipated that the W127 partial "may predate v1.4's new scenario
  `RULE2-06-EQUAL-PRICE-RED`". It does not: the partial derives that scenario and cites the v1.4
  micro-fold. Recorded per clause C-2 (prompt disagreed with the evidence).
- **D-18** Design `:444` requires `CONTRACT_TABLES` to be "sealed at `EXPECTED_SEAL_SHA` no later than
  `IMPLEMENTATION_BASE_SHA`", and design `:448` requires a Lead-accepted `IMPLEMENTATION_ANCHOR`.
  Neither exists yet, and this lane is forbidden to use Git. `CONTRACT_TABLES_MANIFEST.json` records
  the bundle's own file digests as the sealable content and leaves `EXPECTED_SEAL_SHA` /
  `IMPLEMENTATION_BASE_SHA` to the Lead.

---

## v1.5 revision

**Lane:** W156 (`C:\tmp\LANE_PROMPTS_20260828\LANE_W156_TABLES_REVISION_V15.md`). Same author
family and same independence fence as the rest of this worksheet: no `mtc_v2.core` import, no
`observed/` path, no implementer-authored scenario-input file, every value below obtained by
explicit written arithmetic from the design and the owner decision file alone.

**Design under revision:** `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`, version
**v1.5** (title line 1; v1.5 change log lines 932-966). File length **967 lines**, final LF present.
Sections 1-21 are unchanged from v1.4; the sole normative addition is **§22** (lines 676-930) plus
the §15.6 computability note (lines 551-577). Line spans used by this revision:

| §22 subsection | Lines |
|---|---|
| 15.6 computability/revision-scope note | 551-577 |
| 22.1 classification and canonical input envelope | 684-723 |
| 22.2 shared mechanical bindings `M-01`..`M-09` | 725-745 |
| 22.3 shared synthetic record bindings | 747-839 |
| 22.4 per-scenario embeddings RULE2-01..03 | 840-855 |
| 22.5 per-scenario embeddings RULE2-04..06 | 857-880 |
| 22.6 per-scenario embeddings RULE2-07..08 | 882-894 |
| 22.7 RULE2-01-GREEN NaN wire contract | 896-916 |
| 22.8 honest `[OPEN-EMBED]` refusals | 918-930 |

**Line-number mapping for the pre-existing sections 0-11 of this worksheet.** Those sections cite
design **v1.4** line numbers. v1.5 changed the file in exactly two places: it inserted §15.6
(27 content lines plus a blank, 28 lines total) immediately before the old §16, and it appended §22
and the v1.5 change log after the old end of file. Therefore:

- every v1.4 citation to a line **≤ 549** is still exact in v1.5 (verified: §15.5 is still 537-549);
- every v1.4 citation to a line **≥ 551** shifts by **+28** (verified against the v1.5 headings:
  v1.4 §16 551 → v1.5 579; v1.4 §18 577 → 605; v1.4 §19 600 → 628; v1.4 change log 640 → 668; v1.4
  EOF 646 → 674).

Sections 0-11 above use almost exclusively citations ≤ 549 and are therefore still exact as written;
the few above 549 (for example the `core/types.py` shape-census citation written `:593`, and the §16
citation in the header) map to `:621` and `:579-590` under that rule. The `## v1.5 revision` section
below states v1.5 line numbers directly. `CONTRACT_TABLES_MANIFEST.json` has had its three stale
spans corrected against the v1.5 headings.

**Owner authority for the five formerly refused embeddings:**
`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:337-348`,
addendum 20 item 49, owner verbatim `1a 2a 3a 4a 5a`, read this session:

| `OPEN-EMBED` | Owner answer | Cells it makes derivable here |
|---|---|---|
| 01 | initial equity `1000` where the vector omits it (RULE2-03/04/05/06 families) | every `equity_curve` node in those rows, and the real sizing premises that depend on the seed |
| 02 | RULE2-04 entry basis/fill `100` via the §22.5 candidate entry/BE path | `RULE2-04-RED` gross PnL, trade row, cash rows, equity; `RULE2-04-GREEN` `final_position/entry_fill_price` |
| 03 | RULE2-06-EQUAL-PRICE equal-target book is corrected-machinery-only; the legacy arm honestly does not construct it | that row's account/equity/fee/net cells; and the honest not-runnable-on-legacy catalog note |
| 04 | RULE2-08-RED pre-event entry basis/fill `100` | `final_position/entry_fill_price` |
| 05 | RULE2-08-GREEN closed lifecycle from ordinary pre-window bars | converts the already-sealed empty containers and equity `1000` from premise-blocked to premise-supported |

**Verification of the addendum's golden-impact list (lane step 1).** The §15.6 table at design
`:558-573` and the W155 report's golden-impact table were re-checked row by row against this
worksheet's own `blocked_cells` records rather than trusted. Two corrections to that list are
recorded as **V15-D06** in the discrepancy block below: it under-states RULE2-02-RED (which also
gains its cost/funding schedule identities) and it does not mention that `PROBE-P012-07-A`'s
`D-16` maker-rate ambiguity is closed by §22.3's maker binding. Everything else it names matched.

---

### R-0 Shared arithmetic

#### R-0.1 The bound synthetic `CostSchedule` (design `:796-812`)

Every section-22 `CostSchedule` — including the rows that emit no fill — carries
`venue_scope="SYNTHETIC"`, `product_type_scope="LINEAR_TEST_CONTRACT"`,
`symbol_scope="SYNTH-<scenario_id>"`, settlement `TEST-USD`, effective interval
`[1999-12-31T00:00:00Z, 2000-01-02T00:00:00Z)`, `maker_rate=0.00015`, `fixed_component=0`,
`minimum_fee=0`, `fee_rounding_rule="EXACT_IDENTITY_V1"`, `slippage_model_id="BPS_OF_REFERENCE_V1"`,
`slippage_parameters={slippage_bps: <the section 7-13 scenario value>}`, and
`liquidity_roles = {ENTRY, MARKET_EXIT, PROTECTIVE_STOP_EXIT, TARGET_EXIT}` all mapped to `TAKER`.
`taker_rate=0.00045` everywhere **except RULE2-07**, which keeps its section-13 stated `0.001`
(design `:802`). This closes **D-01** for every scenario except in the two respects recorded as
V15-D01 and V15-D03 below.

The fee formula is unchanged (design `:357-364`):

```
fee_notional   = abs(final_fill_price * fill_qty * contract_multiplier)
raw_fee        = fee_notional * selected_liquidity_rate + fixed_component
fee_amount     = round_and_apply_minimum(raw_fee)   ; EXACT_IDENTITY_V1 -> identity
fee_cash_delta = -fee_amount
```

`fixed_component = 0` and `minimum_fee = 0`, so `fee_amount = fee_notional * rate` exactly as a
real number, and the only question is which binary64 that product rounds to.

#### R-0.2 `fl(0.00045)` by hand

```
45 * 2^64 = 45 * 18446744073709551616 = 830103483316929822720
830103483316929822720 / 100000 = 8301034833169298.2272
fractional part 0.2272 < 0.5  -> round to nearest gives the integer 8301034833169298
=> fl(0.00045) = 8301034833169298 * 2^-64            (53-bit significand: 2^52 <= m < 2^53)
              = 0.00045 - 0.2272 * 2^-64             (fl is BELOW the decimal)
   hex-float   0x1.d7dbf487fcb92p-12 ; raw bits 0x3f3d7dbf487fcb92
```

#### R-0.3 Each fee product, rounded to binary64 by hand

Because `fl(0.00045) = M * 2^-64` with `M = 8301034833169298`, the exact real product for an integer
notional `n` is `P * 2^-64` with `P = n * M` — an exact integer numerator. Rounding to binary64 keeps
the top 53 bits of `P`: with `L = bitlength(P)` and `s = L - 53`, the truncated significand is
`q = floor(P / 2^s)` and the discarded remainder is `rem = P - q * 2^s`; round up iff
`rem > 2^(s-1)`, or `rem = 2^(s-1)` and `q` is odd. `T` below is the significand of the binary64
nearest the "clean" decimal, for comparison.

| `n` | `P = n * M` | `L` | `s` | `q` | `rem` | `2^(s-1)` | round | significand | `T` = significand of `fl(clean)` | sealed token |
|---|---|---|---|---|---|---|---|---|---|---|
| 1000 | 8301034833169298000 | 63 | 10 | 8106479329266892 | 592 | 512 | up | 8106479329266893 | `fl(0.45)` = 8106479329266893 | `0.45` |
| 100 | 830103483316929800 | 60 | 7 | 6485183463413514 | 8 | 64 | down | 6485183463413514 | `fl(0.045)` = 6485183463413514 | `0.045` |
| 101 | 838404518150099098 | 60 | 7 | 6550035298047649 | 26 | 64 | down | 6550035298047649 | `fl(0.04545)` = 6550035298047649 | `0.04545` |
| 200 | 1660206966633859600 | 61 | 8 | 6485183463413514 | 16 | 128 | down | 6485183463413514 | `fl(0.09)` = 6485183463413514 | `0.09` |
| 90 | 747093134985236820 | 60 | 7 | 5836665117072162 | 84 | 64 | up | 5836665117072163 | `fl(0.0405)` = 5836665117072163 | `0.0405` |
| 105 | 871608657482776290 | 60 | 7 | 6809442636584189 | 98 | 64 | up | 6809442636584190 | `fl(0.04725)` = 6809442636584190 | `0.04725` |
| **110** | 913113831648622780 | 60 | 7 | 7133701809754865 | **60** | 64 | **down** | **7133701809754865** | `fl(0.0495)` = 7133701809**754866** | **`0.049499999999999995`** |
| 180 | 1494186269970473640 | 61 | 8 | 5836665117072162 | 168 | 128 | up | 5836665117072163 | `fl(0.081)` = 5836665117072163 | `0.081` |

**The `n = 110` row is the one case where the product is not the binary64 nearest the clean
decimal.** `rem = 60` is four units below the tie point `64`, so the product rounds **down** and
lands exactly one ULP below `fl(0.0495)`: raw bits `0x3fa95810624dd2f1` against
`fl(0.0495) = 0x3fa95810624dd2f2`. Writing the token `0.0495` in `RULE2-06-RED` would therefore seal
a value the stated arithmetic does not produce. The sealed token is the shortest decimal that
round-trips to the actual bits: **`0.049499999999999995`**. Every other fee token in this revision
is the clean decimal, and every token in the table round-trips to the bits stated.

Raw bits for the sealed fee tokens (all verified to round-trip):

```
0.45                  0x3fdccccccccccccd      0.045   0x3fa70a3d70a3d70a
0.04545               0x3fa74538ef34d6a1      0.09    0x3fb70a3d70a3d70a
0.0405                0x3fa4bc6a7ef9db23      0.04725 0x3fa83126e978d4fe
0.049499999999999995  0x3fa95810624dd2f1      0.081   0x3fb4bc6a7ef9db23
```

The maker rate is needed only by `PROBE-P012-07-A` (R-19): `100 * fl(0.00015)` rounds to
`fl(0.015) = 0x3f8eb851eb851eb8`, token `0.015`.

#### R-0.4 Equity accumulation and the observation-window scope

Design `:75` and `:100` step 11 fix the ledger: each chosen fill appends its fee cash event, and an
exit additionally appends its gross realized PnL in the same fill sequence; **only `cash_events` are
applied to equity**, in sequence order. This bundle therefore writes

```
equity_curve.last = equity_curve.first + sum(cash_events[i].signed_delta) in sequence order
```

`equity_curve.first` is the equity at the **start of the observation window**. Design v1.5 gives
four rows an evaluation-only window that expressly excludes their setup fills
(`RULE2-04-RED/GREEN` at `:868-869`, the three `RULE2-06` rows at `:872-874`, `RULE2-08-RED` at
`:888`); the remaining rows take the `M-06` default of first-through-last bar (`:734`), where the
window start is the account seed. The window-scoped reading is the only one that keeps the `:75`
invariant true, and it reproduces every `equity_curve.first = 1000` this bundle had already sealed.
The design fixes no explicit scoping rule, so this is recorded as **V15-D02**, not absorbed.

Accumulations, each shown with the raw bits of the result and the sealed token (every token is the
shortest decimal that round-trips to those bits):

```
RULE2-01-RED    1000 - fl(0.45)     = 999.55                0x408f3c6666666666
RULE2-01-GREEN  1000 - fl(0.045)    = 999.955               0x408f3fa3d70a3d71
RULE2-02-GREEN  1000 - fl(0.045)    = 999.955               0x408f3fa3d70a3d71
RULE2-05-RED    1000 - fl(0.04545)  = 999.95455             0x408f3fa2eb1c432d
RULE2-05-GREEN  1000 - fl(0.045)    = 999.955               0x408f3fa3d70a3d71
RULE2-04-*      1000 - fl(0.045)    = 999.955               (window start; pre-window entry fee)
RULE2-06-*      1000 - fl(0.09)     = 999.91                0x408f3f47ae147ae1  (window start)

RULE2-04-RED    999.955 - fl(0.0405)              = 999.91450000000009   0x408f3f50e560418a
                999.91450000000009 + (-10)        = 989.91450000000009   0x408eef50e560418a
RULE2-06-RED    999.91  - fl(0.04725)             = 999.86275            0x408f3ee6e978d4fe
                999.86275 + 5                     = 1004.86275           0x408f66e6e978d4fe
                1004.86275 - fl(0.049499999999999995) = 1004.81325       0x408f668189374bc7
                1004.81325 + 10                   = 1014.81325           0x408fb68189374bc7
RULE2-06-GREEN  999.91  - fl(0.081)               = 999.829              0x408f3ea1cac08312
                999.829 + (-20)                   = 979.829              0x408e9ea1cac08312
RULE2-06-EQUAL  999.91  - fl(0.04725)             = 999.86275            0x408f3ee6e978d4fe
                999.86275 + 5                     = 1004.86275           0x408f66e6e978d4fe
                1004.86275 - fl(0.04725)          = 1004.8155            0x408f668624dd2f1b
                1004.8155 + 5                     = 1009.8155            0x408f8e8624dd2f1b
```

`RULE2-04-RED` is the second place where the clean decimal is wrong: the stated accumulation lands
on `999.91450000000009`, **not** on `fl(999.9145)`, so the sealed equity tokens are
`999.91450000000009` (window start plus fee) and `989.91450000000009` (after the `-10` gross row).

Lifecycle-net values (design `:378`: gross plus every linked fee and funding cash delta, applied in
fill order; the pre-window entry fee is lifecycle-linked even where it is outside the window):

```
RULE2-04-RED     fee_total = -fl(0.045) - fl(0.0405)                = -0.085499999999999993  0xbfb5e353f7ced916
                 net = -10 - fl(0.045) - fl(0.0405)                 = -10.0855               0xc0242bc6a7ef9db2
RULE2-06-RED     fee_total = -fl(0.09) - fl(0.04725) - fl(0.0495-)  = -0.18674999999999997   0xbfc7e76c8b439580
                 net = 15 - fl(0.09) - fl(0.04725) - fl(0.0495-)    = 14.81325               0x402da0624dd2f1aa
RULE2-06-GREEN   fee_total = -fl(0.09) - fl(0.081)                  = -0.17099999999999999   0xbfc5e353f7ced916
                 net = -20 - fl(0.09) - fl(0.081)                   = -20.171                0xc0342bc6a7ef9db2
RULE2-06-EQUAL   fee_total = -fl(0.09) - fl(0.04725) - fl(0.04725)  = -0.1845                0xbfc79db22d0e5604
                 net = 10 - fl(0.09) - fl(0.04725) - fl(0.04725)    = 9.8155                 0x4023a189374bc6a8
```

(`fl(0.0495-)` denotes the one-ULP-low `0.049499999999999995` derived in R-0.3.) Three `fee_total`
tokens are not their clean decimals and are written as the exact round-tripping shortest decimals
above; all four `net_trade_pnl` tokens happen to be clean.

#### R-0.5 Record identities (design `:751-753`, `:764-794`, `:826-828`)

Record ids are the `MECHANICAL` string `SYNTH-{INSTRUMENT|COST|FUNDING}-<scenario_id>-V1`, except
that `RULE2-08-RED` and `RULE2-08-GREEN` share the exact funding record id
`SYNTH-FUNDING-RULE2-08-V1`. Every `InstrumentRecord` carries effective interval
`[1999-12-31T00:00:00Z, 2000-01-02T00:00:00Z)`, written here with the closed member set
`{start_inclusive, end_exclusive}` fixed at `:772-773`. Those cells were
`BLOCKED-MISSING-RECORD-BYTES` / `BLOCKED-MISSING-SCENARIO-INPUT` and are now filled in all 17
artifacts.

**Digests are NOT filled.** Design `:697-700` keeps record and input digests `MECHANICAL` build
artifacts computed from later-authored bytes, `:759-761` expressly refuses to fabricate the
provenance `captured_at_utc` and `human_reviewer` members, and the canonical-JSON rule at `:697-699`
fixes sorted keys, no BOM, LF, a final LF, duplicate-key refusal and finite tokens but **not** the
separator or indentation width. The exact byte string that a SHA-256 would hash is therefore still
undetermined, for the record files and for the RULE2-08 source event alike. Every
`*_record_digest`, `*_schedule_digest`, `instrument_source_document_digest` and
`source_event_digest` cell stays `BLOCKED-MISSING-RECORD-BYTES`. Recorded as **V15-D05**.

---

### R-1 RULE2-01-RED

Bars `[INIT98, ENTRY100]` (`:732`, `:850`); entry fill 100, quantity 5, `contract_multiplier = 2`,
all unchanged from §7 and re-verified against the v1.5 config deltas at `:850`
(`initial_capital=1000`, `risk_per_long_pct=10`, `max_leverage_cap=10`, tick/step/minima
`1/1/0/0`, `instrument_contract_multiplier=2`, percent stop 10, `tp_mode="None"`).

```
fee_notional = abs(100 * 5 * 2)      = 1000                       [:360, :850]
raw_fee      = 1000 * fl(0.00045) + 0                             [:361, :796-802]
fee_amount   = EXACT_IDENTITY_V1(raw_fee) = 0.45                  [R-0.3 n=1000]
fee_cash_delta = -0.45                                            [:363]
liquidity_role(ENTRY) = TAKER                                     [:802-812]
cash_events  = [ FEE(F0) -0.45 ]                                  [:100 step 11]
equity_curve = { first 1000, last 1000 + (-0.45) = 999.55 }       [:75, R-0.4]
fee event timestamp = 2000-01-01T00:11:00Z                        [:732 M-04, :734 M-06]
```

Filled: `fill_events/0/liquidity_role`, `cash_events`, `fee_events`, `equity_curve/last`,
`run_manifest.instrument_record_id`, `instrument_effective_interval`, `cost_schedule_id`,
`funding_schedule_id`. Unchanged: quantity 5, order notional 1000, both `SIZING_*` decision rows,
`funding_events []`, `exit_events []`.

### R-2 RULE2-01-GREEN

Same bars; fallback branch selected by the §22.7 NaN wire; quantity 1, `cm = 1` (`:851`).

```
fee_notional = abs(100 * 1 * 1) = 100 ; fee_amount 0.045 ; fee_cash_delta -0.045
equity_curve = { first 1000, last 999.955 }
```

§22.7 (`:896-916`) binds only the strict-JSON transport of the exact bits
`0x7ff8000000000000` at `/corrected_only/economic_inputs/stop_price_f64`, and `:916` restates that
no NaN is serialized. The `no_serialized_nodes` block is therefore kept and only its citation is
extended; no `stop_price` node is created on either surface.

### R-3 RULE2-02-RED

No fill (corrected refuses `REFUSED_MIN_NOTIONAL`), so no fee and no equity change. v1.5 `:852`
makes both thresholds explicit inputs (runtime `instrument_min_notional=0`, record
`minimum_notional=101`) and binds a complete C and F for the row even though it emits no fill.
Filled: the three record identities plus the effective interval. Everything else byte-identical.

### R-4 RULE2-02-GREEN

Entry admitted at equality (`100 >= 100`), quantity 1, `cm = 1` (`:853`).

```
fee_notional = abs(100 * 1 * 1) = 100 ; fee_amount 0.045 ; fee_cash_delta -0.045
equity_curve = { first 1000, last 999.955 }
```

### R-5 RULE2-03-RED

`[NO_ACTION100]` (`:733` M-05, `:854`); runtime `instrument_price_tick=0.25` against record
`price_tick=0.5`; the corrected adapter refuses `REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION` before
the first bar. Owner addendum 20 (1a) binds `initial_capital = 1000`, and the refusal precedes any
cash event, so

```
equity_curve = { first 1000, last 1000 }          [addendum 20 (1a); :255, :261]
```

Filled: `equity_curve` (was wholly blocked) plus the three record identities and the interval. The
tick values, the refusal row and all five empty containers are byte-identical.

### R-6 RULE2-03-GREEN

`[NO_ACTION100]`; runtime and record `price_tick=0.5` (`:855`); identity validates. A first Range
Filter call only initializes its line and cannot emit an entry for any finite constant OHLC
(`:733`, `:743-745`), so there is no fill, no fee and no equity movement:
`equity_curve = { first 1000, last 1000 }`. Same four record cells filled.

### R-7 RULE2-04-RED

Owner addendum 20 (1a) and (2a) close both refusals, so the §22.5 candidate prefix at `:857-864`
and `:868` is the bound premise. Re-derived from the bound inputs (`initial_capital=1000`,
`risk_per_long_pct=1`, `max_leverage_cap=10`, tick/step/minima `1/1/0/0`,
`instrument_contract_multiplier=1`, percent stop 10 with `use_break_even=true`, `be_trigger_r=1`,
`be_buffer_r=0`, `tp_mode="None"`):

```
prefix bar 1 ENTRY100 close 100 -> entry
  risk_amount   = 1000 * 1%          = 10
  percent stop  = 100 * (1 - 0.10)   = 90     -> stop_distance 10 = 1R
  risk_raw_qty  = 10 / (10 * 1)      = 1
  cap_qty       = (1000 * 10)/(100*1)= 100 ; raw = min(1,100) = 1 ; qty = 1
prefix bar 2 BE100 = (00:12:00Z, 2, 101, 110, 101, 110, 0)
  be_trigger_r 1 -> trigger price = 100 + 1 * 10 = 110 ; bar high 110 >= 110 -> BE fires
  new active stop = entry + be_buffer_r * R = 100 + 0 = 100        [:857-864; exits.py:278-350]
=> the premise design 10:287 states (LONG qty 1, active stop 100, no target) is REACHED, and the
   entry basis is the owner-bound 100.
evaluation bar (00:13:00Z, 3, 90, 95, 85, 92, 0), window = that bar only          [:868]
  open 90 <= stop 100 -> GAP_OPEN, reference 90, slippage 0, floor tick 1 -> fill 90  (unchanged)
  gross_realized_pnl = (90 - 100) * 1 * 1 = -10                    [addendum 20 (2a); :868 cm=1]
  fee_notional = abs(90 * 1 * 1) = 90 ; fee_amount 0.0405 ; delta -0.0405   [R-0.3 n=90]
  liquidity_role(PROTECTIVE_STOP_EXIT) = TAKER                     [:802-812, :868]
  in-window cash_events = [ FEE(F0) -0.0405 , GROSS(F0) -10 ]      [:100 step 11]
pre-window entry fee = abs(100 * 1 * 1) * fl(0.00045) = 0.045
  equity at window start = 1000 - 0.045 = 999.955
  equity_curve.last = 999.955 - 0.0405 - 10 = 989.91450000000009   [R-0.4]
trade row: entry 100, exit 90, qty 1, gross -10,
  fee_total = -0.085499999999999993 , funding_total 0 , net_trade_pnl = -10.0855   [:378, R-0.4]
```

Filled: `exit_events/0/gross_realized_pnl`, `fill_events/0/liquidity_role`, `cash_events`,
`fee_events`, `trades`, `equity_curve`, and the four record-identity cells. Unchanged: the
`PROTECTIVE_STOP_TRIGGER_EVAL` row, reference 90, final fill 90, `fill_trigger GAP_OPEN`,
`slippage_application_count 1`. **D-03 is closed by owner authority, not by this lane's choice.**

### R-8 RULE2-04-GREEN

Same bound prefix and config, evaluation bar `(00:13:00Z, 3, 105, 106, 101, 104, 0)` (`:869`).
Neither the corrected gap-aware predicate (`open 105 <= 100`? no; `low 101 <= 100`? no) nor the
legacy close-only predicate fires, so the position survives.

```
final_position.entry_fill_price = 100                       [addendum 20 (2a)]
window = the evaluation bar only ; no in-window fill -> no in-window cash row
equity_curve = { first 999.955, last 999.955 }              [pre-window entry fee 0.045; R-0.4]
```

All five containers stay derivably empty inside the window.

### R-9 RULE2-05-RED

`[INIT98, ENTRY100]`, `slippage_bps=100`, `price_tick=0.01`, `cm = 1` **explicit** at `:870`.
The fill price 101 and impact 1 are unchanged. Design `:360` bases the fee on the **final** fill:

```
fee_notional = abs(101 * 1 * 1) = 101 ; fee_amount 0.04545 ; delta -0.04545   [R-0.3 n=101]
equity_curve = { first 1000, last 999.95455 }
```

`D-06` is closed for this row: `order_notional 101` was sealed under the shipped cm-default and is
now an explicit design input (`:786-794`, `:870`); the value is byte-identical.

### R-10 RULE2-05-GREEN

Same path with `slippage_bps=0`; fill 100.

```
fee_notional = abs(100 * 1 * 1) = 100 ; fee_amount 0.045 ; delta -0.045
equity_curve = { first 1000, last 999.955 }
```

### R-11 RULE2-06-RED

Bars `[INIT98, ENTRY100, (00:12:00Z, 2, 100, 115, 85, 105, 0)]`, profile `raw_close_only_v1`,
`initial_capital=1000` (addendum 20 (1a)), `risk_per_long_pct=2`, tick/step/minima `1/1/0/0`,
`cm=1` explicit, percent stop 10, `tp_mode="Multi-TP"`, `tp1_r_multiple=0.5`, `tp1_close_pct=50`,
`tp2_r_multiple=1` (`:872`). Re-derivation of the reached book:

```
risk_amount 1000 * 2% = 20 ; stop 90 ; distance 10 = 1R ; risk_raw_qty 20/10 = 2 ; qty 2
TP1 = 100 + 0.5 * 10 = 105 ; TP2 = 100 + 1 * 10 = 110           [exits.py:175-210,213-273]
```

which is exactly the section-12 stated book (entry 100, quantity 2, stop 90, targets 105/110). The
collision, ordering, fills, quantities and gross values are unchanged. New:

```
window = the collision bar only, 2000-01-01T00:12:00Z                       [:872]
F0 TARGET-NEAR: fee_notional abs(105*1*1) = 105 ; fee 0.04725 ; delta -0.04725
F1 TARGET-FAR : fee_notional abs(110*1*1) = 110 ; fee 0.049499999999999995 (R-0.3 n=110)
in-window cash_events (design :100 step 11, fee then gross per exit fill):
  0 FEE(F0)   -0.04725
  1 GROSS(F0) +5
  2 FEE(F1)   -0.049499999999999995
  3 GROSS(F1) +10
pre-window entry fee = abs(100 * 2 * 1) * fl(0.00045) = 0.09
equity_curve = { first 999.91, last 1014.81325 }                            [R-0.4]
trade row: gross 15, fee_total -0.18674999999999997, funding_total 0, net 14.81325
```

`D-06` closed for this row as at R-9; the sealed `5`, `10` and `15` are byte-identical.

### R-12 RULE2-06-GREEN

Same prelude/config, evaluation bar `(00:12:00Z, 2, 100, 104, 85, 95, 0)` (`:873`). Only the stop
touches; both versions fill quantity 2 at 90 with gross `-20` (unchanged).

```
fee_notional = abs(90 * 2 * 1) = 180 ; fee 0.081 ; delta -0.081             [R-0.3 n=180]
in-window cash_events = [ FEE(F0) -0.081 , GROSS(F0) -20 ]
pre-window entry fee 0.09 -> equity_curve = { first 999.91, last 979.829 }
trade row: gross -20, fee_total -0.17099999999999999, net -20.171
```

### R-13 RULE2-06-EQUAL-PRICE-RED

Owner addendum 20 (3a) closes `OPEN-EMBED-03` by ruling that the equal-price target book is
constructed by the **corrected 2.0.0 target-book test machinery directly**, the legacy engine
untouched, and that the row is recorded honestly as **not runnable on legacy for that book**. The
row still "inherits the RULE2-06-RED config" (`:874`), so the position itself (quantity 2, entry
100, stop 90) comes from the same real prelude on both arms; only the two equal targets at 105 are
corrected-only. The tie-break, ordered ids, fills and the sealed `5`/`5`/`10` are unchanged.

```
window = 2000-01-01T00:12:00Z only                                          [:874]
F0 TARGET-FAR and F1 TARGET-NEAR: fee_notional abs(105*1*1) = 105 each ; fee 0.04725 each
in-window cash_events = [ FEE(F0) -0.04725, GROSS(F0) +5, FEE(F1) -0.04725, GROSS(F1) +5 ]
pre-window entry fee 0.09 -> equity_curve = { first 999.91, last 1009.8155 }
trade row: gross 10, fee_total -0.1845, funding_total 0, net 9.8155
```

The not-runnable-on-legacy fact is recorded in the artifact (`legacy_arm_construction`) and in the
catalog row, and as **V15-D04**; the `1.0.0` expected artifact stays `OUT-OF-LANE` as before.

### R-14 RULE2-07-RED

v1.5 `:886` binds the bar series `[INIT98, ENTRY100, (00:12:00Z, 2, 100, 100, 100, 100, 0)]`,
`initial_capital=1000`, fallback `10%`, tick/step/minima `1/1/0/0`, `cm=1`, no SL/TP,
`use_time_stop=true`, `time_stop_bars=1`, `time_stop_condition="Always"`, the exact `GUARD07` switch
set (`:737`), and the corrected exit naming.

```
entry: fallback_notional 1000 * 10% = 100 ; raw_qty 100/100 = 1 ; qty 1    (matches the sealed 1)
time_stop_bars 1 -> the position closes on the next bar at close 100       (matches the sealed 100)
corrected event class / exit id / reason = MARKET_EXIT / TIME_STOP / time_stop      [:886]
lifecycle id starts at 1                                                            [:886]
fee event timestamps = 2000-01-01T00:11:00Z (F0) and 2000-01-01T00:12:00Z (F1)   [:886, :734]
settlement_currency = TEST-USD                                                      [:798-799]
schedule_id = SYNTH-COST-RULE2-07-RED-V1                                            [:751-753]
taker rate stays the section-13 stated 0.001                                        [:802]
```

Filled: `fill_events/1/event_class`, a new `fill_events/1/exit_id`, `fee_events/1/event_class`,
both `fee_events/*/event_timestamp`, both `fee_events/*/lifecycle_id`, both
`fee_events/*/schedule_id`, both `fee_events/*/settlement_currency`, `exit_events/0/exit_id`,
`exit_events/0/reason`, and the four record-identity cells. **D-05 is closed for RULE2-07-RED.**
Every economic value — rate `0.001`, `fee_notional 100`, `fee_amount 0.1`, `fee_cash_delta -0.1`,
gross `0`, `net_trade_pnl -0.2`, equity `1000 -> 999.8`, and all six guard nodes — is byte-identical.

### R-15 RULE2-07-GREEN

`:887` supplies the non-empty but no-signal LEGACY input (`[NO_ACTION100]`, `initial_capital=1000`,
`use_time_stop=false`, exact `GUARD07`) that realizes design `:384`'s "empty fill-event input"
without a state-injection field. No fill exists, so no fee and no equity movement: every already
sealed value stands. Filled: the four record-identity cells only.

### R-16 RULE2-08-RED

Owner addendum 20 (4a) binds the pre-event entry basis/fill to `100` via the `:888` candidate
prefix `[(1999-12-31T23:58:00Z,0,98,98,98,98,0),(1999-12-31T23:59:00Z,1,100,100,100,100,0)]` with
`initial_capital=1000`, fallback `10%`, tick/step/minima `.01/1/0/0`, `cm=1`, no SL/TP.

```
fallback_notional 1000 * 10% = 100 ; raw_qty 100/100 = 1 ; qty 1   -> the stated open_qty 1
final_position.entry_fill_price = 100                              [addendum 20 (4a)]
window = [2000-01-01T00:00:00Z, 2000-01-01T00:01:00Z]              [:888]  -> the prefix fill is
  OUTSIDE the compared surface, so fill_events stays A:0 and equity_curve.first stays 1000
C is absent / NOT_CONSUMED                                         [:888; :429]
position_snapshot_rule = END_OF_INTERVAL_INCLUDE_SAME_TIMESTAMP_V1 [:826-828]
schedule_id = SYNTH-FUNDING-RULE2-08-V1 (shared with GREEN)        [:751-754]
```

The funding arithmetic is unchanged and re-verified: `notional = abs(100 * 1 * 1) = 100`,
`long_cashflow_rate = -0.001`, `funding_cash_delta = 100 * (-0.001) * (+1) = -0.1`,
`equity 1000 + (-0.1) = 999.9` (§0.6 already proved both tokens exact).

`mark_price_source = "SPOT_ORACLE"` is a member of the schedule's event object (`:829-838`), not of
the design `:417-420` `funding_events[]` row field list, so it is **not** added as a surface node.

Filled: `decision_events/1/position_snapshot_rule`, `funding_events/0/schedule_id`,
`final_position/entry_fill_price`, `run_manifest.instrument_record_id`,
`instrument_effective_interval`, `funding_schedule_id`.

### R-17 RULE2-08-GREEN

Owner addendum 20 (5a) closes `OPEN-EMBED-05`: the closed lifecycle is built with ordinary price
bars before the observation window, by the real mechanism, with nothing injected. Those fills are
pre-window, so they contribute no in-window fill, cash, fee, gross-realization or exit fact — which
is exactly the empty-container reading this artifact had already sealed as a judgement call under
**D-05**. The sealed values do not change; their status changes from premise-blocked to
premise-supported. No `CostSchedule` is consumed (`:889`), so no fee arises even from the
pre-window round trip, and equity stays `1000` on both versions.

The owner answer names no specific pre-window bars and `:889` declares no closing evaluation bar, so
the window's `end_timestamp` remains `BLOCKED-MISSING-SCENARIO-INPUT` and no bar-level cell is
authored. Filled: `instrument_record_id`, `instrument_effective_interval`, and
`funding_schedule_id = SYNTH-FUNDING-RULE2-08-V1` (shared with RED per `:751-754`).

---

### R-18 What is still blocked, and why

| Marker | Where | Why v1.5 does not close it |
|---|---|---|
| `BLOCKED-MISSING-RECORD-BYTES` | every `instrument_record_digest`, `instrument_source_document_digest`, `cost_schedule_digest`, `funding_schedule_digest`, `fee_events/*/schedule_digest`, `funding_events/0/schedule_digest`, `funding_events/0/source_event_digest`, and `PROBE-P012-03-A`'s first changed node | `:697-700` keeps digests build artifacts; `:759-761` refuses to fabricate `captured_at_utc` / `human_reviewer`; the canonical-JSON rule does not fix separators or indentation, so the hashed byte string is still undetermined (**V15-D05**) |
| `BLOCKED-DESIGN-UNENUMERATED` | every `/RESULT_SURFACE/metrics`; the complete `decision_events` vocabulary in all 17 artifacts | §22 binds inputs only; it enumerates no metric node set and no reason vocabulary |
| `BLOCKED-BUILD-ARTIFACT` | all 27 catalog `input.digest` values; probe modified-copy and modification-manifest digests | unchanged; the Lead pins these later. **No input path or input digest field was touched by this lane.** |
| `BLOCKED-MISSING-SCENARIO-INPUT` | `RULE2-08-GREEN` `observation_window.end_timestamp` only | `:889` declares no closing evaluation bar and addendum 20 (5a) names none |

Measured over the two expected surfaces of all 17 golden artifacts (walked structurally, counting
leaf string values equal to a marker, so `v15_filled_cells.old_marker` bookkeeping is excluded):
**`BLOCKED-MISSING-SCENARIO-INPUT` = 0**, `BLOCKED-MISSING-RECORD-BYTES` = 81 (every one a digest),
`BLOCKED-DESIGN-UNENUMERATED` = 17 (one `/RESULT_SURFACE/metrics` per artifact; the
`decision_events`-vocabulary block is a `blocked_cells` note, not a surface value). The single
remaining `BLOCKED-MISSING-SCENARIO-INPUT` in the bundle is
`RULE2-08-GREEN` `/observation_window/end_timestamp`, an authoring member outside both surfaces.

### R-19 `PROBE-P012-07-A` — `D-16` closed by §22.3

The probe classifies one declared taker exit as maker. `D-16` recorded that the outcome was
underivable because the RULE2-07 vector stated no maker rate. Design `:799` now binds
`maker_rate = 0.00015` on every section-22 `CostSchedule`, RULE2-07 included, so:

```
variant  fee_notional 100 * fl(0.00015) = 0.015   (0x3f8eb851eb851eb8)
expected fee_notional 100 * fl(0.001)   = 0.1
=> fee_amount, fee_cash_delta and the joined cash row all change.
Under the :508 UTF-8 byte-order walk, cash_events sorts before fee_events, so the first changed
node is /EVENT_SURFACE/cash_events/1/signed_delta (expected -0.1, variant -0.015).
```

The catalog row's `expected_first_changed_node` is updated to that node and its note records the
design-named event-role node alongside it — the same treatment already used for `PROBE-P012-08-A`.
No other probe row changes; `PROBE-P012-01-A`'s `D-14` ordering ambiguity and
`PROBE-P012-03-A`'s `D-15` blocked node both survive v1.5 unchanged in substance
(`PROBE-P012-03-A`'s note is extended to say why).

### R-20 Discrepancies raised by this revision

Recorded per clause C-2; none is absorbed.

- **V15-D01** — `RULE2-08` fill-versus-schedule conflict. Owner addendum 20 (4a) and (5a) bind real
  pre-window fills for both RULE2-08 rows, while design `:888-889` binds `C` as absent /
  `NOT_CONSUMED` and `:429` still asserts that "neither vector contains a fill intent". Design
  `:149` refuses a fill whose `CostSchedule` is missing. The conflict does not reach the compared
  surface (both windows start after those fills, so no in-window fill exists and no fee is
  charged), and no sealed value depends on it — but the input materializer must resolve it before
  a run, because a strict reading of `:149` would refuse the pre-window entry outright.
- **V15-D02** — no `equity_curve` scoping rule. §22 gives four rows an evaluation-only observation
  window that excludes their setup fills, but the design fixes nothing about whether
  `equity_curve.first`/`last` are run-scoped or window-scoped. This revision uses the window-scoped
  reading because it is the only one that satisfies the `:75` invariant
  (`last = first + sum(in-window cash deltas)`) and because it reproduces every already-sealed
  `first = 1000`. `net_trade_pnl` and `fee_total` remain lifecycle-scoped per `:378` and therefore
  include a pre-window entry fee that the in-window `cash_events` container does not carry. Owner
  or §16 confirmation is requested.
- **V15-D03** — universal `CostSchedule` versus GREEN equality. §22.3 binds a non-zero taker rate
  for *every* scenario, including GREEN rows, while `1.0.0` has no fee model at all (`:353`).
  Corrected equity therefore differs from legacy equity on every fill-bearing GREEN row
  (`RULE2-01-GREEN`, `RULE2-02-GREEN`, `RULE2-04-GREEN`, `RULE2-05-GREEN`, `RULE2-06-GREEN`). None
  of those rows' *declared* GREEN projections contains equity, so §15.4 is not violated — but
  `equity_curve` and `net_trade_pnl` must never be added to a GREEN projection member list. Each
  affected artifact carries a `cross_version_note` saying so.
- **V15-D04** — `RULE2-06-EQUAL-PRICE-RED` has no legacy counterpart for its target book. Owner
  addendum 20 (3a) rules the equal-price book corrected-machinery-only and records the row as not
  runnable on legacy for that book, while the catalog row still declares
  `required_semantics_versions ["1.0.0","2.0.0"]`. This lane recorded the fact in the row rather
  than editing the gate-bearing `required_semantics_versions` array, which is the Lead's to change.
- **V15-D05** — "canonical" bytes are not byte-determined. `:697-699` fixes sorted keys, no BOM, LF,
  a final LF, duplicate-key refusal and finite tokens, but not the separator or indentation width,
  and `:759-761` refuses to fabricate two provenance members. Consequently no record digest and not
  even the fully enumerated RULE2-08 source-event digest (`:833-838`) is computable, and this lane
  refused to guess one.
- **V15-D06** — two omissions in the addendum's own golden-impact list. It does not name
  `RULE2-02-RED`'s cost/funding schedule identities (which §22.4 `:852` does bind and which this
  revision fills), and it does not name `PROBE-P012-07-A`'s `D-16` closure (R-19). Both were found
  by checking the list against this worksheet rather than trusting it, as the lane requires.

- **V15-D07** — `IMPLEMENTATION_ANCHOR_DRAFT.json` violates the bundle's own serialization rule.
  Byte-inspected this session: 2827 bytes, **34 CR bytes (CRLF line endings) and no final LF**,
  against design `:480`'s UTF-8 / LF / required-final-LF rule. The lane spec forbids this lane from
  touching that file, so it was left exactly as found and is **not** listed in the manifest's
  `files` array, which means the manifest's `byte_discipline` sentence remains true as written.
  Raised for the Lead, who owns that file.
  **RE-MEASURED AND CORRECTED BY LANE W172 under G83-F05.** The 2827-byte / 34-CR / no-final-LF
  measurement above describes the file as it stood at lane W156; it is **false against the file on
  disk now**. Measured this session by byte inspection of
  `C:\tmp\P012_CONTRACT_TABLES_W127\IMPLEMENTATION_ANCHOR_DRAFT.json`: SHA-256
  `97a3c196323c08e2cf796f31569b396a5b8f886d0b347e3855984b8b9baab0f4`, **3268 bytes, 0 CR bytes, no
  BOM, final LF present**. The file therefore now CONFORMS to design `:480`, and V15-D07 as a
  current-disk claim is **CLOSED by re-measurement**, not by any act of this lane - the file was not
  touched by W172 and remains outside `files[]`. The size grew and the CRLF endings disappeared
  between W156 and now; the Lead's reseal_history block is inside the file at `:35-41`. Which act
  rewrote those bytes is **NOT VERIFIED** - no pre-W167 copy of the file was found. W167's report
  (`W167_TABLES_V18_REPORT.md:74-75,232`) repeats the stale claim that V15-D07 "still stands"; that
  report is outside this lane's write scope and the correction is recorded here and in
  `W172_READING_Y_REPORT.md` instead.

### R-21 Honest limits of this revision

This revision makes the `2.0.0` expected values complete **for design v1.5 plus owner addendum 20**.
It verifies no implementation: no kernel, driver, backtest, verifier, generator or baseline was
executed, no `observed/` path was read, and no corrected-kernel source exists. Local SHA-256 and
IEEE-754 arithmetic over this bundle's own files is the only computation performed, and every
binary64 result above is reproducible by hand from the integer method in R-0.3. The §16
`SEMANTIC_COVERAGE_REVIEW` remains owner-held and PENDING, and the claude family remains excluded
from that reviewer role because it authored these tables. Seal state and the two commit identities
remain the Lead's act; this lane did not touch them.

---

## v1.8 revision

**Lane:** W167 (`C:\tmp\LANE_PROMPTS_20260828\LANE_W167_TABLES_V18.md`). Same author family and the
same independence fence as the rest of this worksheet: no `mtc_v2.core` import, no `observed/` path,
no implementer-authored input file, no kernel executed. Every value below is obtained by written
arithmetic or by literal member-set reconciliation from the design text and the owner decision file
alone. Where the two disagree with an earlier section of this worksheet, this section governs.

**Design under revision:** `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`, version **v1.8**
(title line 1; v1.8 change log `:1229-1251`). File length **1273 lines**, final LF present.

### W-0 Line-number verification and the revision fence

The v1.8 file appends **§23** and changes nothing before it. Verified by re-reading the heading line
numbers rather than trusting the change log: `## 22.` is still at `:676`, `### 22.8` at `:918`, the
v1.5 change log at `:932`, and `## 23.` begins at `:969` and runs to EOF at `:1273`. Every v1.5
citation used by the `## v1.5 revision` section above and by all 17 sealed artifacts is therefore
**still exact**; no citation in this bundle needed re-mapping. The §23 subsection spans are:

| §23 subsection | Lines |
|---|---|
| 23 preamble (supersedes the v1.7 §23 text; sole v1.8 normative change) | 969-985 |
| 23.1 `decision_events` closed shape and reason vocabulary | 987-1053 |
| 23.2 equity-curve observation-window rule | 1055-1072 |
| 23.3 closed `fill_events` / `exit_events` member sets | 1074-1109 |
| 23.4 closed `RESULT_SURFACE`, guards and refusal objects | 1111-1168 |
| 23.5 TABLES REVISION SCOPE and expected KERNEL DELTA | 1170-1227 |
| 23.6 v1.8 change log | 1229-1251 |
| 23.7 v1.8 closed enumeration summary | 1253-1273 |

**Scope fence.** Design `:1171-1172` limits the tables family to seven numbered golden-node classes
and then re-seal by the Lead. This lane changed only those classes. It did **not** touch
`scenario_catalog.json`, any catalog `input.digest`, `IMPLEMENTATION_ANCHOR_DRAFT.json`, or the
manifest's `seal` / `seal_state` blocks. `CONTRACT_TABLES_MANIFEST.json` was edited in exactly two
respects, both stated in `revision_history`: the `files[]` `sha256`/`bytes` entries of the files this
lane actually revised, and the `design` version/line-span block. Design `:1204-1227` is the KERNEL delta
list and is **not** authority for this lane to edit code; nothing outside this bundle was written.

**Owner authority.** Addendum 22 authorised exactly one micro-fold closing four findings
(`:1231-1237`): `FUNDING_ELIGIBILITY` labelled `AMENDMENT-CHOICE` at all three enumeration sites,
`COLLISION_RESOLVED.collision` closed as a JSON boolean with domain `{false,true}` present on the
sole-class receipt, tables-revision item 1 re-pointed at the nine-closed-reason mapping, and
`cumulative_funding` made unconditional on every DEF-P012-08 RESULT. Addenda 19, 20 and 21 apply
unchanged; nothing in this revision re-opens or re-reads them.

### W-1 What §23 forces and what it labels a choice

The lane requires this split to be stated rather than presented as forced. Read off the design's own
labels:

| Class revised here | Disposition in v1.8 | Cite |
|---|---|---|
| `kernel_semantics_version` on every member of all six containers | **FORCED** by §4's every-event identity rule | `:998-1002`, `:1257` |
| No `lifecycle_id` on a `decision_events` member | **FORCED** — lifecycle joins live on the typed economic/position projections | `:1007-1009` |
| `MIN_NOTIONAL_ADMITTED` / `REFUSED_MIN_NOTIONAL` payload `{order_notional, required_min_notional}` | **FORCED** by §8's `admit iff order_notional >= min_notional` | `:1018-1019` |
| `INSTRUMENT_RECORD_VALIDATED` / `REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION` payload `{field, record_value, runtime_value}` | **FORCED** by §§5.2 and 9 | `:1020-1021` |
| Fill common 14-member set; exit common 8-member set; conditional `exit_id` / `fill_trigger` / `target_fraction` / `reference_quantity`; `unrounded_fill_price` FORBIDDEN | **FORCED** (CLOSED) by §§2.1, 3, 4, 10-13 | `:1076-1109`, `:1262-1264` |
| `max_consecutive_losses` forbidden on RESULT | **FORCED** — it is an M-09 configuration input | `:1145-1147` |
| Guard basis `GROSS-MINUS-FEES` on all three named controls | **FORCED** by owner addendum 15 item 35 | `:1147-1150` |
| Refusal `order_notional` replacing `observed_notional` | **FORCED** — §8 names `order_notional` | `:1165-1166` |
| Flat decision rows, no `details` wrapper | `AMENDMENT-CHOICE` | `:1258` |
| `SIZING_COMPUTED` spelling and its one-row fold | `AMENDMENT-CHOICE` (third form; §§3 and 7 force the facts, not the spelling) | `:1017`, `:1044`, `:1243` |
| `MIN_NOTIONAL_ADMITTED` completed-state spelling | `AMENDMENT-CHOICE` | `:1018` |
| `PROTECTIVE_STOP_EVALUATED` spelling and the omission of bar OHLC | `AMENDMENT-CHOICE` | `:1022` |
| One `COLLISION_RESOLVED` spelling; `collision` present on the sole-class receipt rather than varying the closed member set | `AMENDMENT-CHOICE` (the boolean **domain** and content rule are forced by §12) | `:1023`, `:1234` |
| **`FUNDING_ELIGIBILITY` as the reason spelling, one reason for eligible and skipped alike** | `AMENDMENT-CHOICE` — §14 forces event-time eligibility and its boolean terminal disposition, **not** this name | `:1024`, `:1052`, `:1233`, `:1260` |
| Omitting `SLIPPAGE_RESOLVED`, `FEE_SCHEDULE_RESOLVED`, `GUARD_BASIS_RESOLVED`, `MARKET_EXIT_SELECTED` | `AMENDMENT-CHOICE` | `:1026-1031` |
| Window-scoped `equity_curve.first`/`last`; run-scoped endpoints ABSENT | `AMENDMENT-CHOICE` — §§2.1, 15.3 and M-06 force neither reading | `:1066-1072`, `:1261` |
| `price_tick_alignment` spelling | `AMENDMENT-CHOICE` | `:1092-1093` |
| RESULT base spellings `trades` / `warnings` / `refusals` etc. | `AMENDMENT-CHOICE` where §15.3 states only the category | `:1119-1120`, `:1265` |
| Positive `admitted` boolean retained | `AMENDMENT-CHOICE` | `:1129` |
| **`cumulative_funding` unconditional on both DEF-P012-08 RESULT rows** | `AMENDMENT-CHOICE` — §14 names cumulative funding but is silent on member presence when nothing is eligible | `:1131`, `:1236`, `:1266` |
| Top-level `collision` object forbidden; the decision row is the single receipt | `AMENDMENT-CHOICE` | `:1135-1137`, `:1251` |
| `funding_included_in_guard_basis` forbidden | `AMENDMENT-CHOICE` (disposes G76-05c as *not a comparison node*) | `:1152-1155` |

No value in this bundle is presented as design-forced where the design labels it a choice.

### W-2 Item 1 — `decision_events` on all 17 scenarios

**The mapping actually executed.** Design `:1175-1181` (the DS35-F03 repair) tells the tables family
to reconcile *its own* prior reasons through the §23.1 independence table `:1042-1053`, removing only
the names mapped to no separate reason and folding or renaming the others exactly as that table
states, and says the kernel-only four-name removal set does **not** apply here. Executed literally:

| Prior tables reason | v1.8 disposition | Rows affected |
|---|---|---|
| `SIZING_MULTIPLIER_IDENTITY` + `SIZING_SELECTOR` | FOLD to one `SIZING_COMPUTED` | 01-RED, 01-GREEN, 02-RED, 02-GREEN |
| `ADMIT_MIN_NOTIONAL` | RENAME `MIN_NOTIONAL_ADMITTED` | 02-GREEN |
| `REFUSED_MIN_NOTIONAL` | keep, flat, add required timestamp | 02-RED |
| `REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION` | keep, flat, timestamp FORBIDDEN | 03-RED |
| `INSTRUMENT_RECORD_VALIDATED` | keep, timestamp FORBIDDEN | 03-GREEN |
| `PROTECTIVE_STOP_TRIGGER_EVAL` | RENAME `PROTECTIVE_STOP_EVALUATED`, drop the four `bar_*` members | 04-RED, 04-GREEN |
| `SLIPPAGE_MODEL_IDENTITY` | REMOVE (mapped to no separate reason) | 05-RED, 05-GREEN |
| `COLLISION_POLICY_IDENTITY` + `SAME_BAR_COLLISION` | FOLD to one `COLLISION_RESOLVED` | 06-RED, 06-GREEN, 06-EQUAL-PRICE-RED |
| `FEE_SCHEDULE_IDENTITY` | REMOVE (mapped to no separate reason) | 07-RED |
| `GUARD_BASIS_IDENTITY` | REMOVE (mapped to no separate reason) | 07-RED, 07-GREEN |
| `FUNDING_ELIGIBILITY` | keep, reduce to the closed triple, drop `lifecycle_id` | 08-RED |
| `FUNDING_TICK_SKIPPED` | RENAME `FUNDING_ELIGIBILITY`, `eligible=false` carries the skip | 08-GREEN |
| `SEMANTICS_VALIDATED` | keep at sequence 0 on all 17 | all |

`SEMANTICS_VALIDATED` stays on 03-RED: `:1034-1036` excepts only a *preflight*-refused scenario, and
`:1035-1036` states that a pre-evaluation refusal still produces its typed refusal reason. 03-RED produces
a scenario output carrying that refusal, so it is not preflight-refused; the design's own preflight
case is `PROBE-P012-03-A`, which refuses before any scenario output exists (design `:263`).

**Per-reason timestamps.** `:1004-1006`: `REQUIRED` means the timestamp of the `MarketEvent` or
funding event being evaluated under M-06; `FORBIDDEN` means absent, not null. The evaluated event per
row is fixed by §22:

```
01-*, 02-*, 05-*, 07-RED entry decisions -> ENTRY100  = 2000-01-01T00:11:00Z   [:732 M-04]
04-RED / 04-GREEN stop evaluation        -> eval bar  = 2000-01-01T00:13:00Z   [:868-869]
06-RED / 06-GREEN / 06-EQUAL collision   -> eval bar  = 2000-01-01T00:12:00Z   [:872-874]
08-RED / 08-GREEN funding eligibility    -> TEST-FUND-1 = 2000-01-01T00:00:00Z [:888-889, :833-838]
03-RED / 03-GREEN record decisions       -> FORBIDDEN (performed before event evaluation) [:1020-1021]
```

**Payload arithmetic that was re-derived rather than copied.** The only new numbers the closed sets
require are the `SIZING_COMPUTED` `order_notional` values, and each is the section-7 product
`qty * final_entry_fill * contract_multiplier` already sealed on `/RESULT_SURFACE/order_notional`:

```
01-RED    5 * 100 * 2 = 1000      (selector RISK;     risk_amount 100 / (stop distance 10 * cm 2) = 5)
01-GREEN  1 * 100 * 1 = 100       (selector FALLBACK; fallback_notional 100 / (100 * 1) = 1)
02-RED    1 * 100 * 1 = 100       (selector RISK;     risk_amount 10 / (10 * 1) = 1)
02-GREEN  1 * 100 * 1 = 100       (selector RISK;     identical inputs to 02-RED)
```

All four equal the already-sealed `order_notional` node byte for byte; no equity, fee, funding, PnL
or fill value changed anywhere in this item.

**Members dropped because they are outside a closed set** (not because they were wrong): the sizing
rows' `stop_price` / `stop_distance` / `risk_amount` / `reason` / `fallback_notional`; the stop rows'
`bar_open` / `bar_high` / `bar_low` / `bar_close`; 04-GREEN's `"reference_source": null`; the
collision rows' folded `same_bar_collision_policy_id` duplicate; 07-RED's fee/guard identity
payloads; 08-RED's decision `lifecycle_id`; 08-GREEN's `reason` and `event_coverage_present`. The
`event_coverage_present` fact survives in that artifact's `derivable_empty_containers_note`, which
design `:429` still requires to be true.

**04-GREEN's null.** `:1022` closes GM28-F05: `reference_source` and `reference_price` are both
present **iff** a fill reference was selected, and both absent if neither predicate triggers. The
sealed `"reference_source": null` was therefore a wrong tagged state under `:508` (null and absent
are different nodes) and is removed, not re-valued. This is the only sealed *node kind* this item
corrected.

**Row-set reading.** See discrepancy **W167-D04**: §23.1 `:1033-1034` also carries a general
occurrence rule, which read on its own would add further rows. This lane executed item 1's
reconciliation mapping, which is the tables-family instruction, and recorded the alternative.

### W-3 Item 2 — section-4 identity on every event member

`:998-1002` and `:1182-1185`: every member of `decision_events`, `fill_events`, `cash_events`,
`fee_events`, `funding_events` and `exit_events` requires `kernel_semantics_version`, with no
container exception, explicitly including the §13 fee rows and §14 funding rows. Added mechanically
with the constant `"2.0.0"` — the value is the artifact's own
`expected_semantics_version` and `run_manifest.kernel_semantics_version`, so no new fact is asserted.
Members added per artifact:

```
01-RED 5   01-GREEN 5   02-RED 3   02-GREEN 6   03-RED 2   03-GREEN 2
04-RED 7   04-GREEN 2   05-RED 4   05-GREEN 4
06-RED 12  06-GREEN 7   06-EQUAL 12
07-RED 9   07-GREEN 1   08-RED 4   08-GREEN 2      total 87
```

(the count is every member of all six containers in that artifact, including the re-authored
`decision_events` rows; each carries the field exactly once). Verified mechanically afterwards: every
member of all six containers in all 17 artifacts carries the field, and every `sequence` still equals
its array index under `SEQUENCE_FIELD_V1` (`:512`).

### W-4 Item 3 — `equity_curve` under the §23.2 window rule

`:1057-1064` now fixes the rule the `## v1.5 revision` section had to record as missing (**V15-D02**):
`first` is realized equity at `observation_window.start_timestamp` after every **earlier** cash event
but **before** any cash event at the inclusive start timestamp; `last` is `first` plus, in
section-3/array order, every `cash_events.signed_delta` whose event timestamp lies in the closed
window; with no in-window cash event `last == first`; pre-window fees, funding and gross realizations
affect `first`; unrealized position value never does. `:1066-1072` labels the window scope an
`AMENDMENT-CHOICE` and states that run-scoped endpoints are **not** `CORRECTED_V2` comparison nodes.

Re-derived for the five rows item 3 names. Every window here starts and ends on the evaluation bar,
so every in-window cash row carries exactly the start timestamp and is therefore excluded from
`first` and included in `last`:

```
04-RED    window [00:13:00Z, 00:13:00Z]
          earlier cash: pre-window ENTRY fee only, fee_notional 100*1*1 -> -fl(0.045)
          first = 1000 - fl(0.045)                       = 999.955            0x408f3fa3d70a3d71
          in-window: FEE -fl(0.0405) then GROSS -10
          last  = 999.955 - fl(0.0405) - 10              = 989.91450000000009 0x408eef50e560418a
04-GREEN  same window; no in-window cash row
          first = last = 999.955
06-RED    window [00:12:00Z, 00:12:00Z]
          earlier cash: pre-window ENTRY fee, fee_notional 100*2*1 -> -fl(0.09)
          first = 1000 - fl(0.09)                        = 999.91             0x408f3f47ae147ae1
          in-window: -fl(0.04725), +5, -fl(0.0495-), +10
          last                                           = 1014.81325         0x408fb68189374bc7
06-GREEN  first = 999.91 ; in-window -fl(0.081), -20
          last                                           = 979.829            0x408e9ea1cac08312
06-EQUAL  first = 999.91 ; in-window -fl(0.04725), +5, -fl(0.04725), +5
          last                                           = 1009.8155          0x408f8e8624dd2f1b
```

`fl(0.0495-)` is the one-ULP-low `0.049499999999999995` derived in R-0.3; the intermediate binary64
steps and raw bits are unchanged from R-0.4 and were re-checked against it rather than re-asserted.
**All ten tokens are byte-identical to the v1.5 seal.** Design `:1188` warns that prior authorship is
not proof; these five rows survive because the §23.2 rule reproduces them, not because they were
already written.

The rule was also applied to the twelve rows item 3 does not name, as a consistency check: each takes
the M-06 default first-through-last-bar window (`:734`), has no cash event before or at its start
timestamp, and therefore keeps `first` = the account seed `1000`, with `last` the same accumulation
already sealed. No token moved. `08-GREEN` is the one row where the new "pre-window gross
realizations affect `first`" clause bites — recorded as **W167-D03**.

### W-5 Item 4 — guards

`:1142-1147`: a present `guards` object admits exactly `guard_pnl_basis`,
`consecutive_loss_count`, `consec_loss_ok`, `guard_blocked_raw`, plus `last_closed_guard_pnl`
required exactly when a lifecycle closed and produced that fact; `max_consecutive_losses` and
`funding_included_in_guard_basis` are forbidden.

```
07-RED    remove max_consecutive_losses (M-09 input, not a RESULT member)
          remaining: guard_pnl_basis GROSS_MINUS_FEES  [owner addendum 15 item 35, :1147-1150]
                     last_closed_guard_pnl -0.2        [required: lifecycle 1 closed, gross 0 + two
                                                        fee deltas of -fl(0.1) = fl(-0.2)]
                     consecutive_loss_count 1          [design 13:384: the closed lifecycle is a loss
                                                        on the gross-minus-fees basis]
                     consec_loss_ok false, guard_blocked_raw true
                                                       [design 13:384: count < max is 1 < 1 = false]
          every remaining value byte-identical.
07-GREEN  remove max_consecutive_losses
          remaining: GROSS_MINUS_FEES, count 0, consec_loss_ok true, guard_blocked_raw false
          last_closed_guard_pnl stays ABSENT - no lifecycle closes (design 13:384, 22.6:887) and
          :1145 requires absent, not zero or null. Values byte-identical.
08-RED    remove funding_included_in_guard_basis   [:1152-1155 disposes G76-05c as NOT a
                                                    comparison node]
          guard_pnl_basis GROSS_MINUS_FEES         [addendum 15 item 35; funding stays out of the
                                                    basis, which is exactly why the extra boolean
                                                    carries no independent fact]
          consecutive_loss_count 0                 [derived: the candidate prefix only opens, the
                                                    position is LONG at and after the funding event
                                                    and final_position is LONG, so no lifecycle has
                                                    closed at any point]
          last_closed_guard_pnl ABSENT             [same reason]
          consec_loss_ok / guard_blocked_raw       BLOCKED-MISSING-SCENARIO-INPUT - see W167-D01
```

### W-6 Item 5 — conditional fill and exit members

`:1090-1099` and `:1106-1107`. Applied to RULE2-04 and the RULE2-06 family and re-verified on all 17:

```
unrounded_fill_price REMOVED   05-RED (101) and 05-GREEN (100). :1097-1099 makes unrounded_fill a
                               section-11 formula intermediate, not a member; the final tick-aligned
                               price and the three slippage facts already carry the section-11 facts.
exit_id                        present on every exit-class fill, absent on every entry fill: verified
                               on every fill row in the bundle.
                               [CENSUS CORRECTED BY LANE W172 under G83-F02: this line originally
                               read "on all 22 fill rows in the bundle". The measured container
                               lengths are 13 fill_events members and 7 exit_events members across
                               the 17 goldens (01-RED 1, 01-GREEN 1, 02-GREEN 1, 04-RED 1, 05-RED 1,
                               05-GREEN 1, 06-RED 2, 06-GREEN 1, 06-EQUAL 2, 07-RED 2 = 13 fills;
                               04-RED 1, 06-RED 2, 06-GREEN 1, 06-EQUAL 2, 07-RED 1 = 7 exits).
                               W167's report additionally said "all 6 exit rows" at
                               W167_TABLES_V18_REPORT.md:33; W-6's own prose below already
                               enumerates seven exits. The conditional rules themselves were
                               re-verified on the 13 and 7 rows that exist and still hold, so NO
                               GOLDEN VALUE CHANGES from this correction - only the count sentence
                               was wrong.]
fill_trigger                   required only on PROTECTIVE_STOP_EXIT. Present and correct on 04-RED
                               (GAP_OPEN, design-named at :289). ADDED to 06-GREEN's stop fill and to
                               its exit row, where it was missing. Absent on every entry, target and
                               market-exit fill (07-RED's MARKET_EXIT row checked explicitly).
target_fraction /              required only on TARGET_EXIT: present on the four target fills of
reference_quantity             06-RED and 06-EQUAL, absent on every stop, entry and market-exit fill.
exit_events.fill_trigger       re-derived: required on 04-RED (GAP_OPEN) and on 06-GREEN's
                               PROTECTIVE_STOP exit; absent on the four TARGET exits and on 07-RED's
                               time-stop market exit.
```

06-GREEN's added value is derived from the section-10 table (`:277-281`): long, `open 100 <= stop 90`
is false, `low 85 <= stop 90` is true, so the trigger is the stop-level touch and the reference is
the stop level `90` — which is exactly the reference the artifact already sealed. The design names
only the `GAP_OPEN` token, so the non-gap spelling `STOP_TOUCH` is tables-authored; recorded as
**W167-D02**.

### W-7 Item 6 — the top-level RESULT member set

`:1116` fixes the seven base members and `:1128-1131` the four conditionals; `:1133-1137` forbids
everything else and the top-level `collision` object. Re-derived on all 17:

| Row | Base 7 | `order_notional` | `admitted` | `guards` | `cumulative_funding` | change |
|---|---|---|---|---|---|---|
| 01-RED / 01-GREEN | yes | 1000 / 100 | - | - | - | none |
| 02-RED | yes | 100 | - (refused, not admitted) | - | - | none |
| 02-GREEN | yes | 100 | `true` | - | - | none |
| 03-RED / 03-GREEN | yes | - | - | - | - | none |
| 04-RED / 04-GREEN | yes | - | - | - | - | none |
| 05-RED / 05-GREEN | yes | 101 / 100 | - | - | - | none |
| 06-RED / 06-GREEN / 06-EQUAL | yes | - | - | - | - | **top-level `collision` REMOVED** |
| 07-RED / 07-GREEN | yes | - | - | yes | - | see W-5 |
| 08-RED | yes | - | - | yes | `-0.1` | see W-5 |
| 08-GREEN | yes | - | - | - | `0` | none |

`order_notional` is retained on exactly DEF-P012-01, DEF-P012-02 and DEF-P012-05 and is absent from
RULE2-04/06/07/08, as `:1128` requires — note that 07-RED's entry *does* have a notional of
`1 * 100 * 1 = 100`, and `:1133-1135` expressly refuses to make a generic kernel-computed
`order_notional` a node of a scenario whose design projection does not name it.

`cumulative_funding` is now **unconditional** on both DEF-P012-08 rows (`:1131`, `:1196-1200`). Both
were already present — `-0.1` on 08-RED and `0` on 08-GREEN — so the micro-fold confirms them rather
than changing them, and the tables list and the kernel list now agree. The design labels the
unconditional presence an `AMENDMENT-CHOICE`, not a forced identity (`:1131`, `:1236`).

The three removed `collision` objects carried `is_pessimistic` and `ambiguity_record` members that
§12 never enumerated; `:1135-1137` makes the closed `COLLISION_RESOLVED` decision the single receipt.
Nothing those objects carried is lost: `collision`, `same_bar_collision_policy_id` and
`ordered_chosen_exit_ids` are all members of the decision row, and the policy id is additionally on
`run_manifest`, whose internal members §23 does not close.

### W-8 Item 7 — refusal objects

`:1162-1166`. `RULE2-02-RED`'s refusal member `observed_notional` is **renamed** `order_notional`,
giving the closed triple `{code, order_notional, required_min_notional}` = `{REFUSED_MIN_NOTIONAL,
100, 101}`; the design says the prior spelling is replaced rather than canonized because §8 names
`order_notional`. `RULE2-03-RED`'s refusal was re-checked against the five-member tagged object
`{code, field, record_value, runtime_value, stage="PRE_EVALUATION"}` and already conformed exactly,
with no free-form `detail`; **no byte of it changed**. No other artifact has a `refusals[]` member.

### W-9 What is still blocked after v1.8

| Marker | Count over the two surfaces | Where | Why v1.8 does not close it |
|---|---|---|---|
| `BLOCKED-MISSING-RECORD-BYTES` | 81 | every `*_record_digest`, `*_schedule_digest`, `instrument_source_document_digest`, `source_event_digest` | unchanged: `:697-700` keeps digests `MECHANICAL` build artifacts, `:759-761` refuses to fabricate `captured_at_utc` / `human_reviewer`, and the canonical-JSON rule still fixes no separator or indentation width (**V15-D05**) |
| `BLOCKED-DESIGN-UNENUMERATED` | 17 | one `/RESULT_SURFACE/metrics` per artifact | `:1271` states in terms that this amendment "does not un-block design-unenumerated metrics" |
| `BLOCKED-MISSING-SCENARIO-INPUT` | 2 | `RULE2-08-RED` `/RESULT_SURFACE/guards/consec_loss_ok` and `/guard_blocked_raw` | **new**: §23.4 newly requires four guard members while §22.6 binds no guard configuration for RULE2-08 (**W167-D01**) |
| `BLOCKED-BUILD-ARTIFACT` | 0 on these surfaces | catalog `input.digest`, probe copies | untouched by this lane |

**The `decision_events` vocabulary block is CLOSED.** All 17 artifacts previously carried a
`blocked_cells` entry reading "the design fixes no complete `decision_events` reason vocabulary";
§23.1 now enumerates nine closed reasons with exact per-reason member sets, so that entry is removed
from all 17. That is the only entry removed. Design `:1271-1273` confirms the amendment closes the
named schema classes and nothing else, and no other blocked cell was shrunk. Measured
mechanically over the two surfaces of all 17 artifacts after the revision, with a structural walk
that counts leaf string values equal to a marker: `BLOCKED-MISSING-RECORD-BYTES` 81,
`BLOCKED-DESIGN-UNENUMERATED` 17, `BLOCKED-MISSING-SCENARIO-INPUT` 2, `BLOCKED-BUILD-ARTIFACT` 0,
`BLOCKED-ON-OPEN-nn` 0. The bundle's one non-surface `BLOCKED-MISSING-SCENARIO-INPUT`
(`RULE2-08-GREEN` `/observation_window/end_timestamp`) is unchanged.

**V15-D02 is CLOSED** by §23.2, as a labelled choice rather than a forced identity. Every artifact
sentence that recorded it as an open scoping question has been rewritten to cite `:1057-1072` and to
say so.

### W-10 Discrepancies raised by this revision

Recorded per clause C-2; none is absorbed into a derived value.

- **W167-D01** — §23.4 requires four guard members; §22.6 binds no guard configuration for RULE2-08.
  `:1139-1143` makes `consec_loss_ok` and `guard_blocked_raw` required members of a present `guards`
  object, and `:1189-1192` names `RULE2-08-RED` for guard re-derivation. The guard predicate is
  `count < max_consecutive_losses` (design `:384`). `consecutive_loss_count = 0` is derivable, but
  §22.6 `:888` binds no guard switch and no maximum for either RULE2-08 row, and only RULE2-07 binds
  `GUARD07` / `max_consecutive_losses = 1` (M-09 `:737`). Design `:923` states that another
  scenario's value is not authority, so this lane refused to borrow RULE2-07's maximum and marked
  both cells `BLOCKED-MISSING-SCENARIO-INPUT`. Under any `max_consecutive_losses >= 1` the values
  would be `true` and `false`; the design binds no such value here. **Owner or §16 resolution
  requested**, or an input-embedding binding for RULE2-08's guard switches.
- **W167-D02** — closed member presence, open value domain. §23.3 makes `fill_trigger` REQUIRED on
  every `PROTECTIVE_STOP_EXIT` fill and its exit row, but the design names only the `GAP_OPEN` token
  (`:289`); it enumerates no token for section 10's other long branch (`low <= stop`, reference =
  `stop`). The same holds for `PROTECTIVE_STOP_EVALUATED`'s `predicate` and `reference_source` values
  and for the `selector`, `target_ordering_rule` and `price_tick_alignment` values. This lane
  authored `STOP_TOUCH` for the non-gap trigger and kept the pre-existing `OPEN_BEYOND_STOP`,
  `NO_TOUCH`, `BAR_OPEN`, `RISK`, `FALLBACK`, `LONG_ASCENDING_TARGET_PRICE`,
  `LONG_ASCENDING_TARGET_PRICE_THEN_EXIT_ID_UTF8_BYTE_ORDER`, `CEIL` and `FLOOR` spellings. These are
  tables-authored strings in the sense of **D-13**, and every "first changed node" whose value they
  are depends on them. v1.8 closed the member sets but not these domains.
- **W167-D03** — §23.2 versus `RULE2-08-GREEN`'s unnamed pre-window bars. `:1063` makes pre-window
  gross realizations affect `equity_curve.first`. Owner addendum 20 (5a) places lifecycle 1 opening
  and closing on ordinary bars before the window but names none of them, and §22.6 `:889` declares
  no closing evaluation bar. `first = 1000` is derivable only under the premise that the pre-window
  round trip realizes zero gross PnL and consumes no cost schedule — which is the only reading
  consistent with design `:429` fixing that row's compared cash/equity projection at `1000` and with
  `:888-889` binding `C` as absent / `NOT_CONSUMED`. The premise is stated in the artifact and the
  token is unchanged; the design does not state it directly.
- **W167-D04** — two readings of which rows carry which reason. §23.1 `:1033-1034` states a general
  occurrence rule ("emitted ... when their named decision is actually evaluated"), while §23.5 item 1
  `:1175-1181` instructs the tables family to reconcile *its prior reasons* through the independence
  table, and the occurrence sentence recurs only in the **KERNEL** delta list (`:1211`, "emit a
  non-empty reason trail where a listed decision occurs"). Read on its own, the occurrence rule would
  additionally place `MIN_NOTIONAL_ADMITTED` on 01-RED, 01-GREEN, 05-RED, 05-GREEN and 07-RED (every
  admitted in-window entry evaluates section 3 step 8 against `minimum_notional = 0`),
  `SIZING_COMPUTED` on 07-RED, and `PROTECTIVE_STOP_EVALUATED` on the three RULE2-06 rows (their stop
  candidate is evaluated through the section-10 table). This lane executed item 1's mapping, because
  it is the instruction addressed to this family and because the alternative would require authoring
  a further predicate token (W167-D02). **Owner or §16 resolution requested** — the two readings give
  materially different `decision_events` arrays on eight of the seventeen rows.
- **W167-D05** — §7's sizing formula versus §11 / §22.5's declared quantity on `RULE2-05`. Section 3
  steps 7-8 and §7 size from the **final** entry fill: for 05-RED that is
  `fallback_notional 100 / (final fill 101 * cm 1) = 0.990099`, and `qty_step = 1` (`:870`) floors it
  to `0`. §11 `:315` and §22.5 `:870` instead declare requested quantity `1`, which is what the
  bundle seals, together with `order_notional 101`. The two cannot both hold. This is why no
  `SIZING_COMPUTED` row was authored for either RULE2-05 row even under the W167-D04 alternative
  reading: the row's `selector` and `order_notional` members cannot be filled without choosing
  between §7 and §11. Recorded, not resolved; no sealed value was changed.
  **NARROWED BY LANE W172 under G83-F03: W167-D05 is real on `RULE2-05-RED` ONLY.** The sentence
  above over-extended it to `RULE2-05-GREEN`. On GREEN the reference and final entry fill are both
  `100` (`slippage_bps = 0`, design `:315`, `:871`), so §7's fallback path gives
  `100 / (100 * 1) = 1`, `qty_step = 1` floors it to `1`, and `order_notional = 1 * 100 * 1 = 100` -
  which agrees with §11 `:315`'s declared requested quantity `1` and with the sealed
  `/RESULT_SURFACE/order_notional 100`. There is no §7-versus-§11 conflict on GREEN, so
  `SIZING_COMPUTED` **is** derivable there and lane W172 authored it under Reading Y. D05 continues
  to block `SIZING_COMPUTED` on `RULE2-05-RED` alone, where the final fill is `101` and the two
  sections give `0` and `1`.
- **W167-D06** — the manifest `seal` / `seal_state` blocks are now stale by construction. This lane
  revised 18 files and updated their `files[]` digests as the lane spec directs, but `EXPECTED_SEAL_SHA`
  is the Lead's act and was deliberately left untouched, so it no longer covers the current bytes.
  Design `:1171-1172` puts the re-seal with the Lead. Flagged so no reader mistakes the recorded seal
  for a seal of these bytes.

### W-11 Honest limits of this revision

This revision makes the seven §23.5 golden-node classes conform to design v1.8 plus owner addendum 22
(with addenda 19-21 unchanged). It verifies no implementation: no kernel, driver, backtest, verifier,
generator or baseline was executed, no `observed/` path was read, no implementer input file was
opened, and no corrected-kernel source exists. Local SHA-256, structural JSON walks and IEEE-754
checks over this bundle's own files are the only computation performed, and every binary64 result
cited here is the one already derived by hand in R-0.2 to R-0.4. No economic vector value, fee,
funding delta, PnL, equity token, fill price, quantity or record identity changed: the item-3
re-derivation reproduced all ten named equity tokens exactly, and the remaining six items are
member-set, spelling and node-kind repairs plus two newly required guard members that could not be
derived. The §16 `SEMANTIC_COVERAGE_REVIEW` remains owner-held and PENDING, and the claude family
remains excluded from that reviewer role because it authored these tables. Design `:1271-1273` still
governs the claim: this amendment makes the named schema classes design-computable; it does not claim
the present goldens or kernel conform, does not un-block design-unenumerated metrics, does not change
any economic vector, and grants no build, execution, re-seal, deployment or trading authority.

---

## W172 Reading Y revision

**Lane:** W172 (`C:\tmp\LANE_PROMPTS_20260828\LANE_W172_TABLES_READING_Y.md`). Standing clauses
`N_COMMON_CLAUSES.md` C-1..C-7 read in full first. Same author family and the same independence
fence as the rest of this worksheet: no `mtc_v2.core` import, no `observed/` path, no
implementer-authored scenario-input file, no kernel, driver, verifier, generator or baseline
executed. Every value below is obtained by written arithmetic from the design text alone. Where this
section disagrees with any earlier section of this worksheet, including `## v1.8 revision`, this
section governs.

**Authority.** Owner addendum 26, 2026-09-01, answering **W167-D04**: **READING Y**. A
`decision_events` row is required for every closed reason whose named decision is *actually
evaluated* on that scenario, even where the prior tables artifact never carried it, so design
`:1033-1034` applies to the tables family on its own terms. The anti-padding half of that sentence
still binds. The independent family (G83, `DETECT_G83_TABLES_V18.md`) had ruled W167-D04
`GENUINELY AMBIGUOUS - OWNER MUST DECIDE` and put the question to the owner; its per-row table was
read as evidence and **re-verified against the design row by row here**, not copied.

**Design under derivation:** unchanged - `P012_FRESH_DESIGN_V1.md` v1.8, 1273 lines. No design line
was re-numbered and no §23 span moved.

### Y-0 Occurrence test actually applied

For each of the 17 scenarios and each of the nine closed reasons in the `:1016-1024` table, the
question asked was: *is that reason's named decision evaluated inside this artifact's compared
observation window?* Two fences did most of the work and are stated here because they are what keeps
Reading Y from becoming padding:

1. **Window fence.** The `EVENT_SURFACE` of every artifact is scoped to its declared
   `observation_window` - that is already why `RULE2-04-RED`'s setup fills, the `RULE2-06` family's
   prelude entry and `RULE2-08-RED`'s pre-event entry are absent from their fill, cash and fee
   containers (design `:868`, `:872-874`, `:888`). A sizing or admission predicate evaluated on an
   excluded prefix bar is therefore **not** an in-window evaluation and gets no row. This is why
   `SIZING_COMPUTED` and `MIN_NOTIONAL_ADMITTED` are added to `RULE2-07-RED` (full-span window
   `00:10:00Z..00:12:00Z`, entry inside) but **not** to `RULE2-04`, the `RULE2-06` family or
   `RULE2-08`.
2. **Terminal-reason fence.** Where a predicate terminates in a refusal, the refusal reason is the
   row (`:1035`); the admitted spelling is not also emitted. `RULE2-02-RED` therefore keeps
   `REFUSED_MIN_NOTIONAL` and gains nothing.

Result: **eight of seventeen** scenarios grow, by **ten rows** in total. The other nine do not. That
matches G83's measured table; it was reached independently here and each addition is derived below.

### Y-1 `MIN_NOTIONAL_ADMITTED` additions

Design `:97` (section 3 step 8) applies the `min_notional` check to every fill-producing entry;
design `:230-235` (section 8) makes it `admit iff order_notional >= min_notional`, with `:237`
stating that equality passes because the legacy comparison is strict `<`. Members are fixed at
`:1018`: `event_timestamp` REQUIRED, plus `order_notional` and `required_min_notional`. Placement is
after `SIZING_COMPUTED` where that row exists, because section 3 orders sizing at step 7 and
admission at step 8 and the independence row `:1045` states that section 8 makes admission a
separate predicate after sizing.

```
row            order_notional   required_min_notional   ts                     sequence
RULE2-01-RED   1000  = 5*100*2  0   (:216, :850)        2000-01-01T00:11:00Z   2
RULE2-01-GREEN  100  = 1*100*1  0   (:216, :851)        2000-01-01T00:11:00Z   2
RULE2-05-RED    101  = 1*101*1  0   (:870, minima .01/1/0/0)                   1
RULE2-05-GREEN  100  = 1*100*1  0   (:870-871)          2000-01-01T00:11:00Z   2
RULE2-07-RED    100  = 1*100*1  0   (:886, minima 1/1/0/0)                     2
```

Every `order_notional` above equals that artifact's already-sealed value byte for byte: `1000`
(`RULE2-01-RED.json` `/RESULT_SURFACE/order_notional`), `100`, `101`, `100`, and - for
`RULE2-07-RED`, which has no RESULT `order_notional` - the product of its own sealed quantity `1`,
sealed final entry fill `100` and design-bound `contract_multiplier 1`. Every
`required_min_notional` is `0`, read off the row's own `tick/step/minima` shorthand under M-08
`:736`, which design `:844-846` states replaces the same member of the InstrumentRecord. Every
comparison admits. **No economic value moved.**

`RULE2-01-RED` sizing check (already in W-2, repeated because Y-1 depends on it): risk_amount
`1000 * 10% = 100`; stop distance `|100 - 90| = 10`; `risk_raw_qty = 100 / (10 * 2) = 5`;
`leverage_cap_qty = (1000 * 10) / (100 * 2) = 50`; `min(5, 50) = 5`; `qty_step 1` floors to `5`;
`order_notional = 5 * 100 * 2 = 1000`.

`/RESULT_SURFACE/admitted` was **not** added anywhere. Design `:1129` scopes that RESULT member to
the DEF-P012-02 minimum-notional predicate, so it stays on `RULE2-02-GREEN` alone. The decision row
and the RESULT boolean are different nodes with different conditions.

### Y-2 `SIZING_COMPUTED` additions

Members at `:1017`: `event_timestamp` REQUIRED, `selector`, `contract_multiplier`,
`order_notional`. Section 7 `:194-209` supplies the arithmetic; section 3 steps 7-8 `:96-97` supply
the placement.

**`RULE2-05-GREEN`** - design `:871` inherits the RED config with `slippage_bps = 0`, so the final
entry fill is the reference `100` (`:315`). `initial_capital = 1000` (OPEN-EMBED-01, owner addendum
20 item 49 `1a`); `fallback_size_pct = 10`:

```
fallback_notional  = 1000 * 10% = 100                      (:195)
fallback_raw_qty   = 100 / (100 * 1) = 1                   (:196)
leverage_cap_qty   = (1000 * 10) / (100 * 1) = 100         (:206)
raw_qty            = min(1, 100) = 1                       (:207)
qty                = floor_to_qty_step(1) = 1              (:208, qty_step 1 at :870-871)
order_notional     = 1 * 100 * 1 = 100                     (:209)
selector           = FALLBACK                              (:197-198; no SL/TP at :870-871 sets
                                                            use_sl false under M-08 :736)
contract_multiplier= 1                                     (:871, :788-789)
event_timestamp    = 2000-01-01T00:11:00Z                  (M-04 :732, M-06 :734)
```

`qty 1` and `order_notional 100` are the sealed values. The §7 result agrees with §11 `:315`, so
**W167-D05 does not arise on GREEN** (G83-F03, folded at the W167-D05 entry above).

**`RULE2-07-RED`** - design `:886` binds `initial_capital = 1000`, fallback `10%`,
`max_leverage_cap = 10`, `tick/step/minima 1/1/0/0`, `multiplier 1`, no SL/TP; design `:384` states
entry final fill `100` with `slippage_bps = 0`:

```
fallback_notional  = 1000 * 10% = 100                      (:195)
fallback_raw_qty   = 100 / (100 * 1) = 1                   (:196)
leverage_cap_qty   = (1000 * 10) / (100 * 1) = 100         (:206)
raw_qty            = min(1, 100) = 1                       (:207)
qty                = floor_to_qty_step(1) = 1              (:208) - the sealed quantity
order_notional     = 1 * 100 * 1 = 100                     (:209)
selector           = FALLBACK                              (:197-198; "no SL/TP" at :886 / M-08 :736)
contract_multiplier= 1                                     (:384, :886)
event_timestamp    = 2000-01-01T00:11:00Z                  (M-04 :732, M-06 :734; the entry bar is
                                                            inside this row's full-span window)
```

The `FALLBACK` token is **design-named** at `:911` ("Expected/observed JSON records only the
`FALLBACK` decision"). Only `RISK` is a tables-authored spelling; see Y-5. G83-F06's table lists
`RISK / FALLBACK` together as authored - verified this session, that half of its row is wrong.

**`RULE2-05-RED` - `SIZING_COMPUTED` DELIBERATELY WITHHELD.** W167-D05 is real on this row: §7
sizes from the **final** fill `101`, giving `100 / (101 * 1) = 0.990099...` which `qty_step 1`
floors to `0`, against §11 `:315` and `:870` declaring requested quantity `1` and the sealed
`order_notional 101`. The row's `selector` and `order_notional` members cannot both be filled
without choosing between the two sections, so no row was authored and the omission is recorded on
the artifact in `w172_revised_nodes`. This is the lane spec's binding exception and G83's finding
alike. The `MIN_NOTIONAL_ADMITTED` row that WAS added there restates the artifact's own
already-sealed `order_notional 101` - the whole artifact is already derived on the §11 branch
(final_position quantity `1`, fill quantity `1`) - and does **not** resolve D05.

### Y-3 `PROTECTIVE_STOP_EVALUATED` additions on the three RULE2-06 rows

Members at `:1022`: `event_timestamp` REQUIRED, `position_side`, `stop_price`, `predicate`; plus
`reference_source` and `reference_price` **iff a fill reference was selected**.

*Why the decision is evaluated.* Section 3 step 2 `:91` says that for exits the adapter records
which stop and targets touched, before choosing any winner or reference. Design `:343` states in
terms that on `RULE2-06-RED` "the two targets and stop all touch", on `RULE2-06-GREEN` "only the
stop touches", and on `RULE2-06-EQUAL-PRICE-RED` "both equal-price targets and the stop touch". The
independence row `:1046` states that sections 3, 10 and 12 **separate stop evaluation from same-bar
policy resolution**, and maps the prior kernel name `SOLE_EXIT_CLASS` onto
`PROTECTIVE_STOP_EVALUATED` - which is exactly the sole-touched-class shape of `RULE2-06-GREEN`.
The stop evaluation and the policy resolution are therefore two distinct closed reasons on a
DEF-P012-06 row. `:1023`'s restriction is on `COLLISION_RESOLVED` (DEF-P012-06 only, never RULE2-04
close-only selection); it says nothing that would suppress the stop reason here.

*Order.* Step 2 precedes step 3, so the stop evaluation is sequence 1 and `COLLISION_RESOLVED` moves
from sequence 1 to sequence 2 on all three rows. `sequence` remains the contiguous array identity
(`:997`).

*Predicate.* Section 10's table `:277-281`, long rows:

```
row            evaluation OHLC (o/h/l/c)   open <= stop 90   otherwise low <= stop 90   branch
06-RED         100/115/85/105              100 <= 90 FALSE   85 <= 90 TRUE              row 2
06-GREEN       100/104/85/95               100 <= 90 FALSE   85 <= 90 TRUE              row 2
06-EQUAL       100/115/85/105              100 <= 90 FALSE   85 <= 90 TRUE              row 2
```

Bars from design `:343` and `:872-874`. `stop_price 90` is the stated scenario input (`:343`;
`:872` reaches it through `sl_percent 10` on entry `100`). `position_side` is `LONG` (`:343`).
`event_timestamp` is the evaluation bar `2000-01-01T00:12:00Z` (`:872-874`, M-06 `:734`).

*Reference members.*

- `06-GREEN`: **present**. The stop is the sole touched class, `:343` states both versions fill the
  full quantity at stop `90`, and section 10 row 2 makes the stop level the reference, so a fill
  reference was selected. `reference_source = STOP_LEVEL`, `reference_price = 90` - the value the
  artifact already seals on its stop fill.
- `06-RED` and `06-EQUAL`: **absent**. Under `TARGET_FIRST` (`:336`, `:872`, `:874`) the touched
  targets consume the reference quantity `2`, `stop_remainder_quantity` is `0` (already sealed on
  the collision row), so no stop fill intent was chosen at step 3 and no stop reference was selected
  at step 4 (`:92-93`). `:1022`'s `iff` therefore keeps both members off.

**No economic value moved:** `stop_price 90` and `reference_price 90` restate stated scenario
inputs and already-sealed nodes; no fill, cash, fee, PnL, equity or metrics node was touched on any
of the three rows.

### Y-4 The nine rows that do NOT grow, and why

```
02-RED    predicate terminates in refusal -> REFUSED_MIN_NOTIONAL is the row (:1019, :1035)
02-GREEN  already carries all three reasons its evaluation produces
03-RED    pre-evaluation refusal; nothing after it is evaluated (:1035-1036)
03-GREEN  no intent, no fill, no funding event in window (:855)
04-RED    entry sizing/admission are on the excluded prefix; window is the evaluation bar (:868)
04-GREEN  same window fence (:869)
07-GREEN  NO_ACTION100, no intent or fill (:887); guards evaluated but no guard reason exists
          (:1026-1028 removes GUARD_BASIS_RESOLVED)
08-RED    entry on the [OPEN-EMBED-04] prefix, window [00:00:00Z, 00:01:00Z] (:888); guards as above
08-GREEN  no fill, no eligible position; FUNDING_ELIGIBILITY eligible=false already carries the
          skipped tick (:1024, :1052)
```

**Candidate considered and declined: `INSTRUMENT_RECORD_VALIDATED` on rows other than 03-GREEN.**
Section 3 step 1 `:90` validates immutable-record identities on every run, and `:846` states that
every other LEGACY runtime instrument field is explicit and exactly equal to the record. Read at its
widest, Reading Y might place this reason on all 17. It was **not** added, for a payload reason
rather than an occurrence reason: `:1020` fixes the members as the single triple
`{field, record_value, runtime_value}`, and the design names a compared field for exactly one
correction - DEF-P012-03's `price_tick` (`:259`, `:854-855`). For any other row the design neither
names which of the twelve instrument fields the row would carry nor states that one row is emitted
per field, so **no member value is derivable and no row count is derivable**. Authoring either would
be an invented payload. Recorded as **W172-D03**; not absorbed.

### Y-5 G83-F06 - labeling every tables-authored value token

Method: the exact string of every leaf value on the two comparison surfaces of all 17 artifacts was
inventoried this session and grepped against the whole design file. A token whose exact string does
not occur in the design is tables-authored (the **D-13** / **W167-D02** class). Each such token is
now named in a new per-artifact `authored_value_tokens` array carrying the pointer, the value, the
design text that forces the **fact**, and the statement that the **spelling** is tables-authored -
the same treatment W167 gave `STOP_TOUCH` and no less.

```
token                                                     grep hits in design   disposition
FALLBACK                                                  1  (:911)             DESIGN-NAMED
GAP_OPEN                                                  1  (:289)             DESIGN-NAMED
GROSS-MINUS-FEES                                          3  (:1148 etc)        DESIGN-NAMED
RISK, OPEN_BEYOND_STOP, NO_TOUCH, BAR_OPEN, CEIL, FLOOR,   0 each               TABLES-AUTHORED
BUY, SELL, LONG, FEE(kind), GROSS_REALIZATION,
FUNDING(kind), GROSS_MINUS_FEES(underscore form),
LONG_ASCENDING_TARGET_PRICE,
LONG_ASCENDING_TARGET_PRICE_THEN_EXIT_ID_UTF8_BYTE_ORDER,
STOP_TOUCH
LOW_TOUCH, STOP_LEVEL                                     0 each               TABLES-AUTHORED,
                                                                               NEW IN W172
```

Fourteen artifacts gained the ledger; `RULE2-03-RED`, `RULE2-03-GREEN` and `RULE2-08-GREEN` carry no
authored token on either surface and were not touched. **Two corrections to G83's own table**, made
because it is evidence and not authority: (a) `FALLBACK` is design-named at `:911`, so only `RISK`
of that pair is authored; (b) G83's table stops at seven token families, while the inventory also
finds `BUY` / `SELL`, `LONG`, the three `cash_events.kind` tokens and the underscore form of
`GROSS_MINUS_FEES` - all now labeled, so the fix does not leave a residue of the same class.

**Deliberately NOT labeled, and why, so the omission is recorded rather than absorbed:** the
identity strings `F0` / `F1`, `CE-FEE-0` / `CE-FEE-1` / `CE-GROSS-0` / `CE-GROSS-1` / `CE-FUND-0`,
and the `SYNTH-...-V1` record ids. Those are `MECHANICAL` identity strings under §22.1 `:695-708`
and §22.3 `:751-753`, not value-domain spellings of an economic fact; §22.3 `:751-753` fixes the
`SYNTH-` form outright. They are a different class from D-13 and are named here so that a later
reader does not read their absence from `authored_value_tokens` as a claim that they are
design-forced.

### Y-6 G83 findings - disposition

```
G83-F01  MEDIUM  FOLDED. RULE2-08-RED's blocked_cells gained /guards/consec_loss_ok and
                 /guards/guard_blocked_raw. Post-fix cross-check this session: for all 17 artifacts
                 the set of ledger pointers is exactly the set of marked leaf values - 101 cells
                 (100 on the two surfaces, plus RULE2-08-GREEN's off-surface
                 /observation_window/end_timestamp), zero ledger-only and zero value-only entries.
G83-F02  LOW     FOLDED. W-6 census corrected in place: 13 fills / 7 exits measured. No golden value
                 changes; the conditional rules hold on the rows that exist.
G83-F03  LOW     FOLDED. W167-D05 narrowed to RULE2-05-RED at its own entry above, and
                 SIZING_COMPUTED authored on RULE2-05-GREEN in Y-2.
G83-F04  LOW     FOLDED. RULE2-08-RED's OPEN-10 binding no longer asserts
                 funding_included_in_guard_basis as a live false fact; design :1152-1155 and
                 :1189-1192 removed that member from the artifact.
G83-F05  LOW     FOLDED. V15-D07 re-measured and corrected at its own entry above: 3268 bytes, 0 CR,
                 final LF present, so the current-disk claim is closed by measurement. Which act
                 rewrote the bytes is NOT VERIFIED.
G83-F06  LOW     FOLDED, with two corrections to G83's table. See Y-5.
```

No G83 finding is disputed.

### Y-7 Discrepancies raised by this revision

Recorded per clause C-2; none absorbed into a derived value.

- **W172-D01 - a computed notional is now a decision node on a scenario whose RESULT deliberately
  omits it.** Reading Y places `SIZING_COMPUTED` on `RULE2-07-RED` with `order_notional 100`, while
  design `:1128` keeps the RESULT member `order_notional` on DEF-P012-01/02/05 only and `:1133-1135`
  expressly refuses to make "a generic kernel-computed `order_notional` a node of a scenario whose
  design projection does not name it". The two are different member sets in different subsections
  and do not contradict each other, but the design does show §23.4 declining to serialize a
  computed-but-undeclared fact in the very case Reading Y now serializes in §23.1. Flagged so the
  Lead and §16 see the consequence rather than discovering it at the gate. No value moved either
  way.
- **W172-D02 - Reading Y required two more tables-authored value tokens.** `LOW_TOUCH` (the
  `predicate` for section 10's second long branch) and `STOP_LEVEL` (the `reference_source` for that
  branch's stop-level reference) are authored spellings. The design enumerates both the branch
  (`:277-281`) and the reference-source domain (`:93` - "entry reference, gap/open stop reference,
  stop level, target level, or market-exit close"), so the **facts** are design-forced and closed;
  only the strings are this family's. This is the same gap W167 recorded as W167-D02 when it
  authored `STOP_TOUCH` for the identical branch, and it is the reason W167 gave for not executing
  Reading Y. The tokens are labeled on their artifacts under Y-5. An owner or §16 ruling that
  authored value spellings must be design-enumerated before seal would reopen every "first changed
  node" whose value they are, `GAP_OPEN` excepted.
- **W172-D03 - `INSTRUMENT_RECORD_VALIDATED` occurrence is undecidable under Reading Y.** See Y-4.
  Section 3 step 1 validates record identities on every run, but `:1020`'s closed triple names one
  compared field and the design names a compared field only for DEF-P012-03. Neither the field nor
  the row count is derivable for the other sixteen rows, so no row was authored. Owner or §16
  resolution requested if Reading Y is meant to reach this reason.
- **W172-D04 - the manifest carries no `revision_history` entry for this lane.** The lane spec
  authorises manifest edits to `files[]` rows for files actually revised, and nothing else. The
  `files[]` digests and byte counts were therefore updated for the 16 revised files and no
  `revision_history` entry, `design` block change or `blocked_cell_markers` change was written. The
  bundle's own convention is that each revision records itself in `revision_history`; that entry is
  outstanding and is the Lead's to add. `seal`, `seal_state` and `reseal_history` were not touched
  and **W167-D06 still stands**: `EXPECTED_SEAL_SHA` `02b47a8e...` does not cover these bytes.
- **W172-D05 - `W167_TABLES_V18_REPORT.md` still carries two claims this lane has disproved.**
  `:33` says the fill/exit conditionals were re-verified "on all 22 fill rows and all 6 exit rows"
  (measured: 13 and 7), and `:74-75` / `:232` say V15-D07 about the anchor's CRLF bytes "still
  stands" (measured: 0 CR, final LF present). That report is outside this lane's write scope, so
  both corrections are recorded here and in `W172_READING_Y_REPORT.md` and the report file was left
  byte-identical.

### Y-8 Honest limits of this revision

This revision applies one owner ruling and folds one detection report. It verifies no
implementation: no kernel, adapter, driver, gate, backtest, verifier, generator or baseline exists
or was executed, no `observed/` path was read, no implementer-authored input file was opened. Local
SHA-256, structural JSON walks and written arithmetic over this bundle's own files are the only
computation performed. **No economic value moved:** a structural comparison of the pre-revision and
post-revision bytes this session shows zero differences in `RESULT_SURFACE` and in the
`fill_events`, `cash_events`, `fee_events`, `funding_events` and `exit_events` containers of all 17
artifacts, and every pre-existing `decision_events` member survives unchanged except for the
sequence renumbering on the three RULE2-06 rows. Reading Y is an owner ruling on a schema question;
it does not make the goldens conform to a kernel that does not exist, does not un-block
design-unenumerated metrics, does not close W167-D01/D02/D03/D05/D06, and grants no build,
execution, re-seal, deployment or trading authority. The §16 `SEMANTIC_COVERAGE_REVIEW` remains
owner-held and PENDING, and the claude family remains excluded from that reviewer role because it
authored these tables.
