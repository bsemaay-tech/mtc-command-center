# CONTRACT_TABLES — independent expected-value worksheet (lane W127b)

- **Author identity:** `claude-family lane W127b on Claude MAX Opus, non-implementer, owner ruling
  Q3a 2026-08-31; continuation of capped W127`.
- **Producer role:** `CONTRACT_TABLES` per `Design section 15.1, "hand-derived from sections 7-14 plus"` (§15.1) — the `2.0.0`
  expected event/result artifacts, hand-derived from §§7-14 plus frozen records.
- **Design under derivation:** `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`, version
  **v1.4** (title Design v1.4 change log, "v1.4 change log — micro-fold (owner"; v1.4 micro-fold change log Design v1.4 change log, "v1.4 change log — micro-fold (owner"). **Line span used: 1-646**
  (whole file). Primary correction semantics §§7-14 Design section 7, "event values change on RED"; gate/enumeration §15 lines
  435-549; OPEN ledger §19 Design section 19, "ledger exists, but this lane".
- **Design revision applied (lane W156, 2026-08-31):** the bundle now derives from design **v1.5**
  (same file, 967 lines; sole normative addition is §22 Design section 22.1, "AMENDMENT-CHOICE (W320, owner decision 144, 2026-09-03) — §22.1" plus the §15.6 note lines
  551-577) together with owner addendum 20 (`C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:337-348`,
  verbatim `1a 2a 3a 4a 5a`). Sections 0-11 below are the v1.4 derivation and are left intact as the
  historical record; the `## v1.5 revision` section at the end of this file re-derives every cell
  those two sources make computable, keeps every other sealed value byte-identical, and states what
  stays blocked. Where the two disagree, the `## v1.5 revision` section governs.
- **Design revision applied (lane W167, 2026-09-01):** the bundle now derives from design **v1.8**
  (same file, 1273 lines; sole normative change is §23 Design section 23, "of section 23 and is", which supersedes the v1.7
  §23 text). Sections 1-22 are unchanged from v1.5 and their line numbers were re-verified by
  heading position this session, so every v1.5 citation in this worksheet and in all 17 artifacts
  remains exact. Owner addendum 22 authorised the single micro-fold closing G79-F01/DS35-F01 and
  DS35-F02..F04 (design `Design section 23.6, "the `FUNDING_ELIGIBILITY` reason spelling; all"`); addenda 19, 20 and 21 apply unchanged. The
  `## v1.8 revision` section at the end of this file re-derives exactly the seven golden-node
  classes enumerated by the design's own tables-revision scope list (`Design section 23.5, "W261):** the tables family must"`) and states what
  §23 forces versus what it labels an `AMENDMENT-CHOICE`. Where it disagrees with any earlier
  section of this file, the `## v1.8 revision` section governs.
- **Owner Reading Y applied (lane W172, 2026-09-01):** owner addendum 26 answered **W167-D04**. The
  owner chose **Reading Y**: a `decision_events` row is required for every closed §23.1 reason whose
  named decision is **actually evaluated** on that scenario, even where the prior tables artifact
  never carried that reason, so §23.1 `Design section 23.1, "when their named decision is actually evaluated"` applies to the tables family on its own terms. The
  anti-padding half of the same sentence still binds: a reason is emitted because its named decision
  was evaluated, never to equalize row counts. The `## W172 Reading Y revision` section at the end of
  this file records the ten added rows on eight scenarios, their derived payloads, the two rows
  deliberately withheld, and the disposition of findings G83-F01..F06. Where it disagrees with any
  earlier section of this file, including `## v1.8 revision`, the `## W172 Reading Y revision`
  section governs.
- **Repository evidence identity:** `C:\WFMERGE54` HEAD `108ea066a710ff7ef5c09246903fe3d523da1d56`;
  `mtc_v2/core` tree OID `c7f4aa1b46792c67c171237cea62c06497aa35ea`. Both re-verified this session
  with `git rev-parse HEAD` and `git rev-parse HEAD:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core`;
  both match the design's stated premise at `Design section 1, "The current `mtc_v2/core` behavior is the `LEGACY_COMPATIBLE` baseline"`.
- **Independence fence (design §Design section 15.1, "other than the kernel implementer"; lane W127 authority block):** every expected value below is
  `INDEPENDENT_DERIVATION` — obtained by the explicit arithmetic shown here from the design's stated
  contract semantics. No kernel was run. No `observed/` path was read. No corrected-kernel
  implementation exists: `git ls-files | grep -i "corrected_vnext\|economics.py\|semantics.py\|economic_records"`
  returns exactly one path, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/test_trailing_exit_semantics.py`
  (an unrelated legacy backtest test that matched the `semantics.py` substring), which was not opened.

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** The two assertions immediately
above - "No corrected-kernel implementation exists" and the `git ls-files` search said to return
"exactly one path" - were true when this fence was written against `C:\WFMERGE54` HEAD
`108ea066a710ff7ef5c09246903fe3d523da1d56`, and are **false at the current build**. Both are
withdrawn here. Nothing else in this bullet moves, and no derived value anywhere in this worksheet
moves.

**Measured this session, not inherited.** Repository `C:\WP012BUILD`, branch
`feature/wp-p0-12-corrected-vnext-20260831`, HEAD `d32e903a4007593b85aad9aa882a1f049196980d`,
`mtc_v2/core` tree OID `efac978355c89fc38f7592d68556b7c5d7bc9eef`. Running the sentence's own search,
`git ls-files | grep -i "corrected_vnext\|economics.py\|semantics.py\|economic_records"`, returns
**1316 paths**, not one. Of those, **170** end in `.py`, and they include
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economics.py` and
`.../mtc_v2/core/semantics.py` - the corrected-kernel implementation itself. Per pattern the counts
are `corrected_vnext` 1211, `economic_records` 1021, `semantics.py` 12, `economics.py` 11. The same
search run against the first-seal commit `108ea066` returns **exactly one path**, the
`test_trailing_exit_semantics.py` named above: the original wording recorded a true measurement at a
commit this bundle has since moved past, and became false as the build advanced.

**What replaces the withdrawn assertions.** The independence properties this fence may assert are the
ones the design actually names for the `CONTRACT_TABLES` producer
(design `Design section 15.1, "hand-derived from sections 7-14 plus frozen records"`): an author
other than the kernel implementer, no `mtc_v2.core` import, and no `observed/` path read. All three
still hold for every value in this worksheet, and **no `observed/` path was read**. The design
permits the frozen records as a derivation source, and that is what was used: the derivation source
for the record-bound members of this worksheet is the **committed economic record bytes together
with their detached `.sha256` sidecars**
(design `Design section 5.1, "contains the lower-case SHA-256 of those exact file bytes"`) - not a
kernel reading, not an `observed/` artifact, and not an implementer-authored input file. The
separate property that these tables were sealed **before** the corrected kernel existed is therefore
not carried by any repository search run now. It is carried by the design's honest limit L14
(design `Design section 17, "The pre-implementation seal property is carried by the measured history"`)
about the decision-147 `IMPLEMENTATION_BASE_SHA` re-anchor, which states that the
owner-directed re-seal chain is **asserted and human-reviewed under section 16, not machine-checked**.
That is the honest carrier, and it is weaker than a search result - which is exactly why the search
sentence is withdrawn rather than re-measured.

**Corroborating history, measured here.** The same search returns **41 paths** at commit `5e8e5794`,
the first commit carrying this bundle, with `mtc_v2/core/economics.py`, `mtc_v2/core/semantics.py`
and `mtc_v2/core/economic_records/` all **absent**; it returns **44** at its child `cf36e0c4`
("feat(mtc-v2): add exact semantics and transition records"), where the corrected kernel first
appears. This lane measured that history; it does not machine-prove the seal ordering, and does not
claim to.
- **§16 fence:** the design's mandatory `SEMANTIC_COVERAGE_REVIEW` (`Design section 16, "authored `semantic_coverage_review.json`. The reviewer"`)
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
§9 cites the v1.4 micro-fold row `DS18-F01` at Design section 15.3, "every `RED`/`GREEN` catalog scenario and" and the v1.4 catalog sentence at
Design section 15.2, "INPUT`, `EXPECTED`, `OBSERVED`, `KERNEL`, or". The lane brief's caution that the partial "may predate v1.4's new scenario" is
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
| C-01 | design line span "1-647", change log "Design v1.4 change log, "its catalog row; §15.5 sweeps"" | The design file has **646 lines** and ends with a final LF (`wc -l` = 646; `tail -c 1` = `\n`). Corrected to 1-646 / 640-646. |
| C-02 | RULE2-07-GREEN cross-version projection listed legacy `fee_events` and `funding_events` as `A:0` | Design `Design section 14, "funding cashflow and remains at"` — `LEGACY_P011_EXACT_V1` keeps absent legacy containers absent and forbids `GATE_READER` from synthesizing empty `fee_events`/`funding_events`. The legacy selector resolves **ABSENT**, and design `Design section 15.5, "blocker is present the receipt"` counts present-versus-absent as *divergence*. Those rows were therefore invalid GREEN members. **Removed** from the GREEN projection and re-classified as version-specific added containers under design `Design section 6, "to the named behavioral projection."`. |
| C-03 | RULE2-08-GREEN projection listed `funding_events` `A:0` = `A:0` and `RESULT_SURFACE/cumulative_funding` as `ABSENT / I:0` = `I:0`, "Equal? yes" | Same authority as C-02, plus design `Design section 14, ". Legacy has no funding"` (legacy `PortfolioState` carries no funding ledger). Left state is unambiguously ABSENT; the pair is unequal. **Removed** from the GREEN projection; the declared GREEN member is the economic cash/equity value 1000 stated at design `Design section 14, ". Legacy has no funding"`. |
| C-04 | RULE2-06-RED divergent row `RESULT_SURFACE/collision` = `B:1, chosen="TARGETS"` | `chosen="TARGETS"` is not a design value. Design `Design section 12, "quantity at stop `90` on"` gives `chosen=STOP` only for the `STOP_FIRST` row; the `TARGET_FIRST` row's receipt column (design `Design section 12, "quantity at stop `90` on"`) is **"Ordered chosen event ids"**. Replaced by `ordered_chosen_exit_ids` plus the pessimistic-field divergence the design names at `Design section 12, "quantity at stop `90` on"`, evidenced by the legacy collision return `is_pessimistic=True` at `exits.py:370`. |
| C-05 | Fee/cash cells marked `BLOCKED-ON-OPEN-03`; synthetic record ids marked `BLOCKED-ON-OPEN-01`; metrics and schema marked `BLOCKED-ON-OPEN-09` | Mislabelled. OPEN-01/03 govern the **production** record and fee schedule, and design `Design section 5, "a future implementer's choice."` forbids a production admission value from populating a synthetic RULE-2 vector — so no OPEN-01/03 answer can ever supply these cells. OPEN-09 has been answered `APPLICABLE / schema APPROVED`. Re-labelled `BLOCKED-MISSING-SCENARIO-INPUT` (vector gap), `BLOCKED-MISSING-RECORD-BYTES` (synthetic record bytes never listed) and `BLOCKED-DESIGN-UNENUMERATED` (design fixes no node set) as appropriate. See §0.5. |
| C-06 | `golden/corrected_vnext/RULE2-01-RED.json` wrote `"cash_events": []`, `"fee_events": []` and `"equity_curve": {"last": 1000}` while simultaneously listing those cells as blocked | Writing `[]` asserts a derived zero-length container, and design `Design section 15.2, "PROBE_ROOT`, target kind (`INPUT`, `EXPECTED"` makes missing, null and empty **different** nodes. Design `Design section 3, "the applicable entry/market/stop intent or"` mandates a fee cash event for the entry fill, so `[]` is affirmatively wrong, and `1000` asserts a zero fee. Every genuinely underivable cell now carries the marker string as its **value**, so no unsupported number or container length is sealed. |
| C-07 | RULE2-07-RED divergent-projection table included `trade/0/gross_realized_pnl` `I:0` versus `I:0` with the note "equal value, but split reported" | A `rule2_divergent_projection` member must actually differ; design `Design section 15.2, "PROBE_ROOT`, target kind (`INPUT`, `EXPECTED"` says identical present values are not divergence, and design §15.4 refuses "correction without divergence". **Removed** from the divergent set. DEF-P012-07's divergence is carried by `fee_events`, `net_trade_pnl`, the guard nodes and equity, all of which do differ. |
| C-08 | `provenance.author` = "claude-family lane W127, non-implementer, owner ruling Q3a 2026-08-31" | Updated to the W127b identity required by this lane (see header). |
| C-09 | Line cites `§Design section 15.3, "an unlisted event array refuses"` (event-order rule) and `§Design section 15.3, "an unlisted event array refuses"` (RESULT_SURFACE contents) | Off by one and by three: the event-order rule is at design line **512**; the RESULT_SURFACE member list is at design line **474**. Corrected throughout. |
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
| OPEN-02 (`STOP_FIRST` mandatory) | `RULE2-06-RED`, `RULE2-06-EQUAL-PRICE-RED`, `RULE2-06-GREEN` | **No value effect; conflict recorded (D-12).** Design `Design section 12, "both versions choose and fill"` declares `TARGET_FIRST` as an explicit *input* of the two RED scenarios and design `Design section 12, "both versions choose and fill"` forbids closing OPEN-06 from silently rewriting the pair, so the design's synthetic input governs the sealed values. For the GREEN row design `Design section 12, "both versions choose and fill"` makes all three policies select the sole touched class, so the answer is value-neutral there. |
| OPEN-05 (funding rules approved; same-timestamp = INCLUDE) | `RULE2-08-RED`, `RULE2-08-GREEN` | No value effect: design `Design section 14, ". Legacy has no funding"` places the position open *before and after* the RED timestamp and closed *before* the GREEN timestamp, so eligibility is the same under INCLUDE or EXCLUDE. The INCLUDE answer creates a separate build fixture obligation (a fill at the exact funding timestamp) that no declared scenario exercises. |
| OPEN-06 (P19 RETIRE, P20 RETAIN) | `RULE2-04-RED`, `RULE2-04-GREEN` | **Closes the contingency.** Design `Design section 8, "Those inputs derive risk amount `10`, stop"` and `Design section 10, "Legacy fills at close `92"` make the corrected gap/open projection OPEN-06-contingent. The owner's answer retires P19 (close-only close-triggered/close-filled stop) and retains P20 (gap-aware open/stop reference), per `P012_OPEN06_RETAINED_RETIRED_PROPOSAL_V1.md:61-62`, which is exactly the corrected behaviour design `Design section 10, "Legacy fills at close `92"` states. The sealed value 90 still comes from the design, not from the owner answer. |
| OPEN-09 (additive schema APPROVED) | every scenario | Removes the partial's `BLOCKED-ON-OPEN-09` schema-approval marker. It does **not** enumerate a metric node set, so `metrics` is `BLOCKED-DESIGN-UNENUMERATED`, not OPEN-blocked. |
| OPEN-10 (guards keep gross-minus-fees; funding excluded) | `RULE2-07-RED`, `RULE2-07-GREEN`, `RULE2-08-RED` | Confirms the basis design `Design section 12, "quantity at stop `90` on"` already fixes from D017, and settles design `Design section 14, "no fill at all /"` ("guard outcomes follow the sourced OPEN-10 decision") for RULE2-08: the captured funding delta does **not** enter the guard basis. |

The residual blocks are design gaps, not owner gaps. Four marker classes are used:

- `BLOCKED-MISSING-SCENARIO-INPUT` — the declared synthetic vector omits an input the cell needs.
- `BLOCKED-MISSING-RECORD-BYTES` — the cell is a digest/id/field of a *synthetic frozen test record*
  whose exact bytes the design never lists. Design `Design section 5, "future implementer's choice. Synthetic"` forbids substituting the answered
  production record, so this can never be closed by an OPEN answer.
- `BLOCKED-DESIGN-UNENUMERATED` — the design names the member but fixes no node set for it
  (`metrics`; the complete `decision_events` reason vocabulary).
- `BLOCKED-BUILD-ARTIFACT` — a path/digest that only exists after the Gate-2 build (serialized
  scenario-input files, probe kernel-variant trees, patch files, observed outputs).

### 0.6 Node kinds and the two decimal equities (resolves the partial's D-07 / D-08)

Design `Design section 15.3, "converted to IEEE-754 binary64 using"` fixes node kind by **token shape**, not by value: a number token with no fraction and
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

RULE2-08 equity, one addition (design `Design section 14, "rate `-0.001`, `funding_cash_delta=-0.1`, and corrected"`):

```
1000 + fl(-0.1) exactly = 999.9 - 0.4 * 2^-56 = 999.9 - 0.0000488 * 2^-43
candidates: fl(999.9) = 999.9 - 0.2 * 2^-43   (distance 0.1999512 * 2^-43)
            next up   = 999.9 + 0.8 * 2^-43   (distance 0.8000488 * 2^-43)
-> rounds to fl(999.9). The token 999.9 is exact for this accumulation.
```

RULE2-07 equity, two subtractions (design `Design section 13, "all other L16 guards and"`):

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

All 17 RED/GREEN rows are `2.0.0`, so `surface_schema_id = CORRECTED_V2` (design `Design section 14, "changes: add `funding_events`, cumulative funding"`), which
requires all six ordered containers `decision_events`, `fill_events`, `cash_events`, `fee_events`,
`funding_events`, `exit_events`; any may be explicitly empty. `SEQUENCE_FIELD_V1` (design `Design section 15.3, "containers: `decision_events`, `fill_events`, `cash_events`, `fee_events`, `funding_events`, and"`)
gives every member an integer `sequence` starting at zero and equal to its array index; every
container written in this bundle satisfies that.

A container is written **empty** only where emptiness is *derived*, and is written as a **marker
string** where it is not. The asymmetry is deliberate and is grounded in design §3:

- A fill unconditionally requires a fee cash event (`Design section 3, "14's event-time eligibility rule"`, step 11), so a scenario that *has* a fill
  but *no* `CostSchedule` cannot have `cash_events`/`fee_events` = `[]`; those cells are blocked.
- Funding is applied only per schedule event (`Design section 14, "1`, the same complete schedule"`), and `Design section 14, "1`, the same complete schedule"` refuses only *missing required
  interval data*. A vector that spans no funding interval therefore has a derived
  `funding_events` = `[]`.
- A scenario with no fill (RULE2-02-RED refusal, RULE2-03 pre-evaluation refusal, RULE2-04-GREEN
  no-touch, RULE2-07-GREEN empty fill input, RULE2-08-GREEN ineligible tick) has derived empty
  `fill_events`, `cash_events`, `fee_events` and `exit_events`.

---

## 1. DEF-P012-01 — contract multiplier in sizing (design `Design section 7, "and leverage-cap quantity `50`; the"`)

### RULE2-01-RED — `close_only_deterministic_v2`

Inputs, exactly as design `Design section 7, "required quantities are legacy `10"` states them: `sizing_equity=1000`, `risk_pct=10`,
`final_entry_fill=100`, finite `stop=90`, `cm=2`, `qty_step=1`, `min_qty=0`, `min_notional=0`,
`BPS_OF_REFERENCE_V1` with `slippage_bps=0`, `price_tick=1`, test-only `max_leverage_cap=10`
(explicitly *not* the shipped default `1.0` at `config.py:69`, which this session read and confirmed
is `"max_leverage_cap": 1.0`).

```
risk_amount        = 1000 * (10/100)            = 100                       Design section 7, "and the required quantities are"
stop supplied and finite, distance > 0 -> risk branch                       Design section 7, "and the required quantities are"
stop_distance      = |100 - 90|                 = 10                        Design section 7, "and the required quantities are"
risk_raw_qty       = 100 / (10 * 2)             = 5                         Design section 7, "and the required quantities are"
selected_raw_qty   = 5                                                      Design section 7, "raw_qty          = min(selected_raw_qty, leverage_cap_qty"
leverage_cap_qty   = (1000 * 10) / (100 * 2)    = 50                        Design section 7, "raw_qty          = min(selected_raw_qty, leverage_cap_qty"
raw_qty            = min(5, 50)                 = 5                         Design section 7, "raw_qty          = min(selected_raw_qty, leverage_cap_qty"
qty                = floor_to_qty_step(5, 1)    = 5                         Design section 7, "raw_qty          = min(selected_raw_qty, leverage_cap_qty"
order_notional     = 5 * 100 * 2                = 1000                      Design section 7, "changed projection: quantity, order notional"
admit: 1000 >= min_notional 0                   -> admitted                 Design section 7, "changed projection: quantity, order notional"
slippage impact    = |100| * 0 / 10_000         = 0                         Design section 7, "changed projection: quantity, order notional"
buy -> unrounded   = 100 + 0                    = 100                       Design section 7, "changed projection: quantity, order notional"
final_entry_fill   = ceil_to_price_tick(100, 1) = 100                       Design section 7, "position quantity, and any quantity-derived"
slippage_application_count = 1                                              Design section 7, "quantity, and any quantity-derived cash"
position.quantity after entry = 5
```

Legacy arithmetic for the divergence proof (design `Design section 6, "fields and intentionally added ledger/container"`; independently confirmed against
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

Declared `rule2_divergent_projection` (design `Design section 7, "RULE2-01-GREEN` uses `execution_profile_id=close_only_deterministic_v2`, sizing equity"`: quantity, order notional, later position
quantity, and any quantity-derived cash event), resolved as design `Design section 15.3, "node_kind, canonical_value)`, `ABSENT`, or `REFUSAL"` tagged states:

| Node | `1.0.0` BASELINE | `2.0.0` CONTRACT_TABLES | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/quantity` | `PRESENT(I:10)` | `PRESENT(I:5)` | yes |
| `/RESULT_SURFACE/order_notional` | `PRESENT(I:2000)` | `PRESENT(I:1000)` | yes |
| `/RESULT_SURFACE/final_position/quantity` | `PRESENT(I:10)` | `PRESENT(I:5)` | yes |
| quantity-derived cash event | — | `BLOCKED-MISSING-SCENARIO-INPUT` | not a sealed member |

`decision_events` gains the sizing multiplier identity row required by design `Design section 7, "adds multiplier identity; corrected quantity"`
("sizing decision adds multiplier identity"): `{sequence:1, decision:"SIZING_MULTIPLIER_IDENTITY",
contract_multiplier:2}`.

Blocked cells: `cash_events`, `fee_events`, `fill_events/0/liquidity_role`, `equity_curve/last`
(all `BLOCKED-MISSING-SCENARIO-INPUT`, discrepancy **D-01**); `metrics` and the complete
`decision_events` vocabulary (`BLOCKED-DESIGN-UNENUMERATED`); run-manifest record ids/digests
(`BLOCKED-MISSING-RECORD-BYTES`).

### RULE2-01-GREEN — `close_only_deterministic_v2`

Inputs (design `Design section 7, "RULE2-01-GREEN` uses `execution_profile_id=close_only_deterministic_v2`, sizing equity"`): `sizing_equity=1000`, `fallback_size_pct=10`, `final_entry_fill=100`,
`stop` = a supplied quiet binary64 NaN with exact bits `0x7ff8000000000000` decoded by the scenario
input adapter, `cm=1`, `qty_step=1`, `min_qty=0`, `min_notional=0`, `slippage_bps=0`, `price_tick=1`,
`max_leverage_cap=10`.

```
stop supplied but not finite -> fallback branch                             Design section 7, "quantity, and any quantity-derived cash"
fallback_notional  = 1000 * (10/100)            = 100                       Design section 7, "quantity, and any quantity-derived cash"
fallback_raw_qty   = 100 / (100 * 1)            = 1                         Design section 7, "quantity, and any quantity-derived cash"
selected_raw_qty   = 1
leverage_cap_qty   = (1000 * 10) / (100 * 1)    = 100                       Design section 7, "raw_qty          = min(selected_raw_qty, leverage_cap_qty"
raw_qty            = min(1, 100)                = 1                         Design section 7, "raw_qty          = min(selected_raw_qty, leverage_cap_qty"
qty                = floor_to_qty_step(1, 1)    = 1                         Design section 7, "order_notional   = qty * final_entry_fill * cm"
order_notional     = 1 * 100 * 1                = 100                       Design section 7, "order_notional   = qty * final_entry_fill * cm"
final_entry_fill   = ceil_to_price_tick(100 + 0, 1) = 100
```

Legacy takes the same branch: `position_sizer.py:43` tests `sl is not None and math.isfinite(sl)`,
which a NaN fails, so `:48-50` computes `fallback_notional = equity * (fallback_size_pct/100)` then
`raw_qty = fallback_notional / entry` = `100 / 100` = `1`. Design `Design section 7, "Those selector branches exactly preserve"` states exactly this
("Those selector branches exactly preserve the current kernel guard and initializer").

Declared `rule2_green_projection` (design `Design section 7, "preserve the current kernel guard"` "both final quantities are `1`"; `Design section 7, "preserve the current kernel guard"` "no
behavioral projection changes on GREEN"):

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |
| `/RESULT_SURFACE/final_position/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |
| `/RESULT_SURFACE/order_notional` | `PRESENT(I:100)` | `PRESENT(I:100)` | yes |

The NaN stop is never serialized (design `Design section 7, "binary64 NaN stop with exact"` final sentence; design `Design section 15.3, "exponent is converted to IEEE-754"` also refuses a
non-finite value in a comparison artifact), so no `stop_price` node exists on either surface — the
selector resolves **ABSENT** on both sides. This is recorded in the artifact's `no_serialized_nodes`
block rather than as a value.

---

## 2. DEF-P012-02 — real minimum-notional admission (design `Design section 8, "with observed notional `100` and"`)

### RULE2-02-RED — `close_only_deterministic_v2`

Inputs (design `Design section 8, "leverage-cap quantity `100`, and floored"`): `sizing_equity=1000`, `risk_pct=1`, `final_fill=100`, `stop=90`, `cm=1`,
`slippage_bps=0`, `price_tick=1`, `max_leverage_cap=10`, `qty_step=1`, `min_qty=0`; legacy runtime
`min_notional=0` (design cites `config.py:48`, read this session: `"instrument_min_notional": 0.0`);
corrected frozen test record `min_notional=101`.

```
risk_amount      = 1000 * (1/100)     = 10
stop_distance    = |100 - 90|         = 10
risk_raw_qty     = 10 / (10 * 1)      = 1            (pre-floor quantity 1, Design section 8, "distance `10`, pre-floor quantity `1")
leverage_cap_qty = (1000 * 10)/(100*1) = 100
raw_qty          = min(1, 100)        = 1
floored_qty      = 1
order_notional   = 1 * 100 * 1        = 100                                 Design section 8, "test record uses `min_notional=101`."
corrected: admit iff 100 >= 101 -> FALSE -> REFUSED_MIN_NOTIONAL            [Design section 8, "frozen test record uses `min_notional=101", Design section 8, "frozen test record uses `min_notional=101"]
           observed notional 100, required 101, opens no position           Design section 8, "frozen test record uses `min_notional=101"
legacy   : reject iff 100 < 0   -> FALSE -> opens                           (position_sizer.py:67)
```

Declared `rule2_divergent_projection` (design `Design section 8, "typed refusal, removes entry/position/fill-dependent events"`: "RED gains the typed refusal, removes
entry/position/fill-dependent events, and records the instrument digest"):

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/RESULT_SURFACE/refusals/0/code` | `ABSENT` | `PRESENT(S:"REFUSED_MIN_NOTIONAL")` | yes (absent vs present) |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:1)` | `PRESENT(A:0)` | yes |
| `/RESULT_SURFACE/final_position` | `PRESENT(O:…)` LONG qty 1 | `PRESENT(N)` null | yes |
| `/EVENT_SURFACE/decision_events/3/decision` | `ABSENT` | `PRESENT(S:"REFUSED_MIN_NOTIONAL")` | yes |

Derived empties: no position opens, so there is no fill, hence no fee cash event (design `Design section 3, "for that fill; on an"`
attaches a fee to a fill) and no exit — `fill_events`, `cash_events`, `fee_events`, `exit_events` and
`funding_events` are all derivably `[]`. Equity is untouched, so `equity_curve` = `{first:1000,
last:1000}` is derived, not assumed.

### RULE2-02-GREEN — `close_only_deterministic_v2`

Same named inputs with `min_notional=100` on **both** adapters (design `Design section 8, "Legacy opens; corrected emits `REFUSED_MIN_NOTIONAL"`).

```
order_notional = 1 * 100 * 1 = 100
corrected: 100 >= 100  -> TRUE  -> admits   (equality passes because the legacy comparison
                                             is strict '<', Design section 8, "passes because the legacy comparison")
legacy   : 100 <  100  -> FALSE -> admits   (position_sizer.py:67)
```

Declared `rule2_green_projection` (design `Design section 8, "so equality refuses. The RULE-2-GREEN"` "equality passes and both open"; the probe at
`Design section 8, "so equality refuses. The RULE-2-GREEN"` binds "the admission/refusal projection"):

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/RESULT_SURFACE/admitted` | `PRESENT(B:1)` | `PRESENT(B:1)` | yes |
| `/EVENT_SURFACE/fill_events/0/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |
| `/RESULT_SURFACE/final_position/quantity` | `PRESENT(I:1)` | `PRESENT(I:1)` | yes |

Here the entry fill *does* occur, so `cash_events`/`fee_events` are blocked (**D-01**), unlike the
RED row.

---

## 3. DEF-P012-03 — frozen instrument metadata (design `Design section 9, "before evaluation with `REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION`."`)

### RULE2-03-RED — `close_only_deterministic_v2`

Inputs (design `Design section 8, "floored quantity `1`. The"`): synthetic `BPS_OF_REFERENCE_V1` schedule with `slippage_bps=0`; synthetic
frozen record `price_tick=0.5`; runtime override `price_tick=0.25`; every other runtime economic
field equal to its frozen-record field.

```
corrected: runtime price_tick 0.25 != record price_tick 0.5
           -> REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION, before the first bar     [Design section 5.1, "Each record also carries source", Design section 8, "corrected frozen test record uses", Design section 8, "corrected frozen test record uses"]
           -> "RED becomes a typed pre-evaluation refusal"                        Design section 9, "corrected refuses before evaluation with"
legacy   : InstrumentMetadata.from_config accepts and uses runtime 0.25           [Design section 8, "corrected frozen test record uses", Design section 8, "corrected frozen test record uses"]
```

Declared `rule2_divergent_projection` (design `Design section 8, "corrected output differs from the"`):

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/RESULT_SURFACE/refusals/0/code` | `ABSENT` | `PRESENT(S:"REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION")` | yes |
| `/EVENT_SURFACE/decision_events/1/decision` | `ABSENT` | `PRESENT(S:"REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION")` | yes |
| `/EVENT_SURFACE/fill_events` | legacy evaluated run | `PRESENT(A:0)` | yes |
| consumed `price_tick` | `PRESENT(F:0.25)` | refusal — no value consumed | yes |

`0.5` and `0.25` are float nodes (fraction present, design `Design section 15.3, "is integer, while `100.0` and"`). Their canonical enumerator forms
are `F:0x1.0000000000000p-1` and `F:0x1.0000000000000p-2` respectively — both exact powers of two,
hand-checked. This is informational; the artifact writes the tokens `0.5` and `0.25`.

Derived empties: the refusal precedes evaluation, so no scenario output exists — all five economic
containers are derivably `[]`.

### RULE2-03-GREEN — `close_only_deterministic_v2`

Inputs (design `Design section 8, "with observed notional `100` and"`): same zero-impact schedule; `price_tick=0.5` on both sides; every runtime
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

## 4. DEF-P012-04 — gap-aware protective stops (design `Design section 10, "92`; the OPEN-06-contingent corrected projection"`)

### RULE2-04-RED — `close_only_deterministic_v2`

Inputs (design `Design section 10, "low=85, close=92`. Legacy fills"`): existing long `quantity=1`, no active target, `stop=100`, `price_tick=1`,
`BPS_OF_REFERENCE_V1` with `slippage_bps=0`, next bar `open=90, high=95, low=85, close=92`.
**Not supplied:** entry basis, `contract_multiplier`, initial equity — discrepancy **D-03**.

```
Long, open(90) <= stop(100) -> trigger, reference (pre-slippage) = open = 90   [Design section 10, "Legacy fills at close `92" table row 1]
slippage impact = |90| * 0 / 10_000 = 0                                        Design section 10, "Legacy fills at close `92"
sell (exit long) -> unrounded_fill = 90 - 0 = 90                               Design section 10, "Legacy fills at close `92"
final_fill = floor_to_price_tick(90, 1) = 90                                   Design section 10, "reference/final price, gross PnL, cash/equity"
fill_trigger = GAP_OPEN                                                        Design section 10, "reference/final price, gross PnL, cash/equity"
slippage_application_count = 1                                                 Design section 10, "gap is never improved back"
a gap is never improved back to the stop                                       Design section 10, "gap is never improved back"
```

Legacy: the `close_only_deterministic_v2` profile triggers from close and fills at close (design
`Design section 8, "distance `10`, pre-floor quantity `1"`). Independently confirmed at `exits.py:424-447`: `_evaluate_close_only_stop_hit` returns no
hit when `bar.close > stop_price` (for a long) and otherwise returns `fill_price=bar.close`. Here
`close 92 > stop 100` is false, so the legacy fill price is **92**.

Declared `rule2_divergent_projection` (design `Design section 10, "probe `PROBE-P012-04-A`: return stop `100"`; the probe at `Design section 10, "probe `PROBE-P012-04-A`: return stop `100"` fixes the fill-price node):

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/reference_price` | `PRESENT(I:92)` | `PRESENT(I:90)` | yes |
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:92)` | `PRESENT(I:90)` | yes |
| `/EVENT_SURFACE/fill_events/0/fill_trigger` | `ABSENT` | `PRESENT(S:"GAP_OPEN")` | yes |
| gross PnL / cash / equity / trade / metrics | — | `BLOCKED-MISSING-SCENARIO-INPUT` | not sealed |

Conditional note, **not sealed**: were the entry basis `100` and `cm=1` as in the sibling vectors,
corrected gross would be `(90-100)*1*1 = -10` and legacy `(92-100)*1*1 = -8` — still divergent. The
vector does not state them, so those cells stay blocked rather than being guessed (**D-03**).

OPEN-06 binding: see §0.5. The corrected value 90 is taken from design `Design section 10, "100` rather than open `90"`, and the owner's
P19-RETIRE / P20-RETAIN disposition makes it the disposition-consistent behaviour.

### RULE2-04-GREEN — `close_only_deterministic_v2`

Inputs (design `Design section 10, "gap/open reference `90` and final"`): same quantity, absent target, tick and zero-impact record; `stop=100`,
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

`exit_events` and `fill_events` exist in the legacy shape (design `Design section 15.3, "containers: `decision_events`, `fill_events`, `cash_events`, `fee_events`, `funding_events`, and `exit_events`; any"` lists one `ExitEvent` in
current `core/types.py`), so both sides resolve `A:0` and the pair is a valid GREEN member — unlike
`fee_events`/`funding_events`, which do not exist at `1.0.0` at all (see C-02).

Derived empties: no fill, therefore no fee (design `Design section 3, "fill sequence. They use section"`); the vector spans no funding interval.

---

## 5. DEF-P012-05 — in-path slippage, applied exactly once (design `Design section 10, "price_tick=1`, synthetic `BPS_OF_REFERENCE_V1` slippage with `slippage_bps=0`, and"`)

### RULE2-05-RED — `close_only_deterministic_v2`

Inputs (design `Design section 11, "inputs derive impact `1` and"`): buy intent, `reference=100`, `slippage_bps=100`, `price_tick=0.01`,
`requested_quantity=1`. `contract_multiplier` is not restated — `cm=1` is taken from the shipped
kernel default `"instrument_contract_multiplier": 1.0` at `config.py:49` (design `Design section 7, "versus corrected `5`. Required"` states the
same), tagged `(cm-default)` and recorded as discrepancy **D-06**.

```
impact          = |100| * 100 / 10_000        = 1                           Design section 11, "= ceil_to_price_tick(unrounded_fill) for a"
buy -> unrounded_fill = 100 + 1               = 101                         Design section 11, "= ceil_to_price_tick(unrounded_fill) for a"
final_fill      = ceil_to_price_tick(101, 0.01) = 101                       Design section 11, "= ceil_to_price_tick(unrounded_fill) for a"  (already aligned)
slippage_application_count = 1                                              Design section 11, "= ceil_to_price_tick(unrounded_fill) for a"
order_notional  = 1 * 101 * 1                 = 101                         (cm-default)
[VALUE SUPERSEDED BY LANE W186 under owner addendum 28 decision 68; marker added by lane W224
 under GM62-F04: the order_notional line above reads 1 * 101 * 1 = 101. Owner addendum 28
 decision 68 ruled that design section 7 governs this row and its quantity is ZERO, so
 order_notional = 0 * 101 * 1 = 0. The current sealed byte is "order_notional": 0
 (RULE2-05-RED.json:43) and the golden's own before/after record is RULE2-05-RED.json:91.
 The four lines above it - impact 1, unrounded_fill 101, final_fill 101 and
 slippage_application_count 1 - are UNCHANGED and still current, and so is the
 divergent-projection table below, whose four rows name reference price, impact, final fill
 price and application count only; W186 Z-5 says in terms that "its fill price 101 and impact 1
 stand". NO VALUE MOVED HERE - the superseded product above is left exactly as written. The
 re-derivation is W186 Z-5, in the section "W186 owner addendum 28 decision 68 re-derivation -
 RULE2-05-RED" below. GM62-F04 named R-0.4, R-9 and the Y-1 table; this line is the same residue
 in the same class and is marked here rather than left.]
```

Legacy passes the reference price through with no cost adjustment (design `Design section 10, "corrected projection selects gap/open reference"`), so the legacy fill
is **100**.

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/reference_price` | `ABSENT` | `PRESENT(I:100)` | yes (absent vs present) |
| `/EVENT_SURFACE/fill_events/0/slippage_impact` | `ABSENT` | `PRESENT(I:1)` | yes |
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:100)` | `PRESENT(I:101)` | yes |
| `/EVENT_SURFACE/fill_events/0/slippage_application_count` | `ABSENT` | `PRESENT(I:1)` | yes |

Design `Design section 11, "entry price, entry-relative stops/targets, notional"` also lists entry-relative stops/targets, notional, fee basis, PnL and equity as RED
changes "as applicable"; this vector has no stop, target, schedule or equity, so those selectors
resolve ABSENT on both sides or are blocked, and are **not** sealed divergent members.

`price_tick 0.01` is a float node; its canonical form is `F:0x1.47ae147ae147bp-7` (hand-derived:
`0.01 / 2^-7 = 1.28`; hex fraction `47ae147ae147a|e14…`, next digit `e` = 14 ≥ 8, round up to
`…47b`). Informational only.

### RULE2-05-GREEN — `close_only_deterministic_v2`

Inputs (design `Design section 11, "101`; legacy fill is `100"`): same reference `100`, tick `0.01`, quantity `1`, `slippage_bps=0`.

```
impact = |100| * 0 / 10_000 = 0
buy -> unrounded_fill = 100 + 0 = 100 ; ceil_to_price_tick(100, 0.01) = 100
corrected final_fill = 100 ; legacy final_fill = 100
```

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:100)` | `PRESENT(I:100)` | yes |

Design `Design section 11, "corrected artifacts retain explicit zero-impact"` requires corrected artifacts to retain explicit zero-impact lineage. The nodes
`slippage_model_id`, `slippage_bps`, `slippage_impact` and `slippage_application_count` carry it.
They are **version-specific added nodes** and, per design `Design section 6, "version-specific and are compared against"`, are excluded from the cross-version
GREEN equality and compared against their own expected artifact instead. The artifact records this in
its `version_specific_lineage_nodes` block.

---

## 6. DEF-P012-06 — named same-bar collision policy (design `Design section 12, "tick, test-only zero-impact model/parameter record"`)

### RULE2-06-RED — `raw_close_only_v1`

Inputs (design `Design section 12, "no stop remainder. `RULE2-06-GREEN` uses"`): synthetic long, `entry_fill=100`, `reference_quantity=2`, `qty_step=1`,
`stop=90`, `TARGET-NEAR` at `105` with fraction `0.5`, `TARGET-FAR` at `110` with fraction `0.5`,
`price_tick=1`, `BPS_OF_REFERENCE_V1` with `slippage_bps=0`, bar `open=100, high=115, low=85,
close=105`, corrected policy `TARGET_FIRST`. `contract_multiplier` not restated — `cm=1`
(cm-default, **D-06**). Initial equity not given — absolute equity blocked (**D-04**).

Touch check (design `Design section 12, "tick, test-only zero-impact model/parameter record"` "The two targets and stop all touch"): `high 115 >= 110` and
`high 115 >= 105`; `low 85 <= 90`. Confirmed against the profile's own evaluators —
`raw_close_only_v1` takes the OHLC branch at `exits.py:362-363`, which evaluates stop and target
independently.

```
TARGET_FIRST: touched targets nearest to entry first; long ascending target price   Design section 12, "targets, target fractions, tick, test-only"
              apply each target's declared fraction to the reference quantity        Design section 12, "step, stop, two targets, target"
TARGET-NEAR exit qty = 0.5 * 2 = 1  @ reference 105
TARGET-FAR  exit qty = 0.5 * 2 = 1  @ reference 110
remaining   = 2 - 1 - 1 = 0  -> no stop remainder                                    Design section 12, "stop touches, so both versions"
slippage_bps 0, sell: floor_to_price_tick(105, 1) = 105 ; floor_to_price_tick(110, 1) = 110
ordered chosen exit ids = [TARGET-NEAR, TARGET-FAR]                                  [Design section 12, "full quantity at stop `90" receipt]
gross realized PnL (cm-default cm = 1):
  TARGET-NEAR: (105 - 100) * 1 * 1 =  5
  TARGET-FAR : (110 - 100) * 1 * 1 = 10
  lifecycle gross total            = 15
```

Legacy: the OHLC dispatcher at `exits.py:365-374` returns, when stop and target both hit,
`fill_price=stop_hit.fill_price`, `exit_pct=1.0`, `is_pessimistic=True`, `exit_id=stop_hit.exit_id`.
The stop reference itself comes from `exits.py:400-406`: `open 100 <= stop 90` is false, `low 85 <=
90` is true, so `fill_price = stop_price = 90`. Legacy therefore exits the full quantity `2` at `90`
with `gross = (90-100)*2*1 = -20` — exactly what design `Design section 12, "low=85, close=95`; only the stop"` states.

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fill_events/0/exit_id` | `PRESENT(S:"STOP")` | `PRESENT(S:"TARGET-NEAR")` | yes |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:1)` | `PRESENT(A:2)` | yes |
| `/EVENT_SURFACE/fill_events/0/final_fill_price` | `PRESENT(I:90)` | `PRESENT(I:105)` | yes |
| `/EVENT_SURFACE/fill_events/1/final_fill_price` | `ABSENT` | `PRESENT(I:110)` | yes |
| `/RESULT_SURFACE/collision/ordered_chosen_exit_ids` | `ABSENT` (policy is implicit at 1.0.0, design `Design section 12, "stop remainder. `RULE2-06-GREEN` uses `execution_profile_id=raw_close_only_v1"`) | `PRESENT(A:2)` `["TARGET-NEAR","TARGET-FAR"]` | yes |
| `/RESULT_SURFACE/collision/is_pessimistic` | `PRESENT(B:1)` (`exits.py:370`) | `PRESENT(B:0)` | yes |
| lifecycle gross realized PnL | `PRESENT(I:-20)` (cm-default) | `PRESENT(I:15)` (cm-default) | yes |
| absolute equity | — | `BLOCKED-MISSING-SCENARIO-INPUT` (**D-04**) | not sealed |

Design `Design section 12, "equity, and metrics; every corrected"` names "chosen exit id/reason, price, pessimistic/ambiguity fields, PnL, equity, and
metrics" plus "policy id and collision decision events" — the rows above cover every one that this
vector supplies inputs for.

**ROWS SUPERSEDED BY LANE W167 under design v1.9 `Design v1.9 section 23.4, "Every `CORRECTED_V2` `RESULT_SURFACE` has exactly"`; marker added by lane W224 under
GM62-F05.** The table above lists two `/RESULT_SURFACE/collision/*` members -
`ordered_chosen_exit_ids` and `is_pessimistic` - as live divergent `2.0.0` nodes, and the paragraph
above states that the rows cover every selector design `Design section 12, "receipt, list the protective stop first if it touched, followed by every touched target in the"` names. **That object no longer exists
on any row.** Design **v1.9** `Design section 23.4, "object; the closed `COLLISION_RESOLVED` decision"` states in terms that "A top-level `collision` object is
forbidden", and `Design section 23.4, "object; the closed `COLLISION_RESOLVED` decision"` makes the closed `COLLISION_RESOLVED` decision the single receipt; lane
W167 removed the object from all three RULE2-06 artifacts under item 6 - see W167 W-7, the section
"W-7 Item 6 - the top-level RESULT member set" below. `RULE2-06-RED`'s `RESULT_SURFACE` now carries
exactly the seven base members - `final_position`, `trades`, `equity_curve`, `metrics`, `warnings`,
`refusals`, `run_manifest` (`RULE2-06-RED.json:49-71`) - and **no `collision` node of any kind**;
`is_pessimistic` occurs nowhere in that artifact, measured this session. Where the current state
lives: the ordered ids are `["TARGET-NEAR","TARGET-FAR"]` on the `COLLISION_RESOLVED` decision row
(`RULE2-06-RED.json:27`), and the removal record is on the artifact itself
(`RULE2-06-RED.json:101`). **The divergence the two rows assert is unchanged** - the legacy OHLC
dispatcher still returns `is_pessimistic=True` at `exits.py:370` and the corrected run still chooses
both targets - it is now carried by the decision row rather than by a second RESULT object, so the
rows describe the pre-W167 serialization and were correct when written. **NO VALUE MOVED** - neither
row names a money figure, rate, quantity or price, and the lifecycle gross `-20` / `15` row and the
absolute-equity row below them are untouched.

### RULE2-06-EQUAL-PRICE-RED — `raw_close_only_v1` (v1.4 micro-fold, design `Design section 12, "with full bar `open=100, high=104"`, `Design section 15.2, "subject_producer_id`, modified-copy path/digest below `PROBE_ROOT"`, `Design section 15.3, "tag PRESENT except under the"`)

Inputs: the exact `RULE2-06-RED` inputs **except that `TARGET-FAR` is also at `105`** (design `Design section 12, "touches, so both versions choose"`).
Both equal-price targets and the stop touch (`high 115 >= 105`; `low 85 <= 90`).

Tie-break derivation (design `Design section 12, "scope for DEF-P012-06 because it"` "equal prices by `exit_id` UTF-8 byte order"):

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

Design `Design section 12, "has UTF-8 byte `0x46` and"` states the declared divergent projection for this scenario is "the ordered chosen exit
ids and fill-event sequence", which the first five rows carry.

**ROW SUPERSEDED BY LANE W167 under design v1.9 `Design v1.9 section 23.4, "Every `CORRECTED_V2` `RESULT_SURFACE` has exactly"`; marker added by lane W224 under
GM62-F05.** The table above lists `/RESULT_SURFACE/collision/ordered_chosen_exit_ids` as a live
divergent `2.0.0` node on `RULE2-06-EQUAL-PRICE-RED`, and the paragraph above counts it among "the
first five rows". **The top-level `collision` object no longer exists on this row either**, for the
reason set out in full at the identical marker on `RULE2-06-RED` above. This artifact's
`RESULT_SURFACE` carries the seven base members and no `collision` node
(`RULE2-06-EQUAL-PRICE-RED.json:50-72`); the ordered ids `["TARGET-FAR","TARGET-NEAR"]`, the
equal-price `target_ordering_rule` and `tie_break_applied: true` are on the `COLLISION_RESOLVED`
decision row (`RULE2-06-EQUAL-PRICE-RED.json:28`), and the removal record is at
`RULE2-06-EQUAL-PRICE-RED.json:105`. The `0x46 < 0x4e` byte-order derivation above is **unchanged
and still current** - it now fixes the order of that decision row's member. **NO VALUE MOVED.**

### RULE2-06-GREEN — `raw_close_only_v1`

Inputs (design `Design section 12, "bar `open=100, high=104, low=85, close=95"`): same position, quantity step, stop, two targets, fractions, tick,
zero-impact record and policy; bar `open=100, high=104, low=85, close=95`.

```
targets: high 104 >= 105 ? no ; >= 110 ? no  -> neither target touches
stop   : low  85  <= 90  ? yes               -> stop touches
only one class touches -> all three policies select it                        Design section 12, "stop, two targets, target fractions"
stop reference: open 100 <= 90 ? no ; low 85 <= 90 ? yes -> reference = stop = 90  [Design section 10, "the OPEN-06-contingent corrected projection selects" row 2]
slippage_bps 0, sell: floor_to_price_tick(90, 1) = 90
both versions fill the full quantity 2 at 90                                  Design section 12, "only the stop touches, so"
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
"not-applicable-under-STOP_FIRST". Design `Design section 12, "quantity at stop `90` on"` nevertheless states that closing OPEN-06 "may not
silently rewrite this pair", and the lane brief directs that the design's synthetic numbers govern
scenario values. **This bundle therefore seals `TARGET_FIRST` for the RULE2-06 RED pair and raises
the conflict for owner/§16 resolution.** Under `STOP_FIRST` both RED scenarios would collapse onto
the legacy result and DEF-P012-06 would have no divergent projection at all, which design §15.4
refuses as "correction without divergence".

---

## 7. DEF-P012-07 — provenanced real fee schedule (design `Design section 13, "fixture as `round_and_apply_minimum(x)=x"`)

### RULE2-07-RED — `close_only_deterministic_v2`

Inputs (design `Design section 11, "corrected fill is `101`."`): `initial_equity=1000`, long round trip `quantity=1`, entry and exit final
fills `100`, `cm=1`, `BPS_OF_REFERENCE_V1` with `slippage_bps=0`, `price_tick=1`, two **taker**
fills, `taker_rate=0.001`, `fixed_component=0`, `minimum_fee=0`, no funding event, rounding rule
`EXACT_IDENTITY_V1` defined for this fixture as `round_and_apply_minimum(x) = x`. Guard settings:
only the consecutive-loss guard enabled, test-only `max_consecutive_losses=1`, all other L16 guards
and guard recovery disabled.

```
per fill (Design section 13, "0`, minimum fee `0`, no"):
  fee_notional   = |100 * 1 * 1|            = 100                            Design section 13, "and test rounding rule `EXACT_IDENTITY_V1"
  raw_fee        = 100 * 0.001 + 0          = 0.1                            Design section 13, "and test rounding rule `EXACT_IDENTITY_V1"
  fee_amount     = EXACT_IDENTITY_V1(0.1)   = 0.1                            [Design section 13, "funding event, and test rounding", Design section 13, "funding event, and test rounding"]
  fee_cash_delta = -0.1                                                       Design section 13, "no funding event, and test"
two fills (entry F0, exit F1) -> two fee cash events, each -0.1              Design section 13, "funding event, and test rounding"

gross_realized_pnl = (100 - 100) * 1 * 1 = 0                                 [Design section 13, "lifecycle net is `-0.2`, and", Design section 13, "lifecycle net is `-0.2`, and"]
net_trade_pnl      = 0 + (-0.1) + (-0.1) = -0.2                              [Design section 13, "and equity remains `1000`.", Design section 13, "and equity remains `1000`."]
corrected equity   = 1000 - 0.1 - 0.1     = 999.8                            [Design section 13, "and equity remains `1000`."; exact, see 0.6]
legacy             : gross 0, no v2 net field, equity stays 1000             [Design section 13, "gross PnL and cash delta are `0`", Design section 13, "equity remains `1000`"]
```

Cash-ledger ordering (design `Design section 3, "3. Exact ordering for `2.0.0"`, §3 steps 10-12) and the typed-projection join
(design `Design section 2.1, "equal the joined cash row's signed"`, `Design section 13, "cash_event_id`; the gate equality-checks `fee_cash_delta"`):

```
entry fill F0 -> cash_events[0] = FEE(F0)                -0.1   cash_event_id CE-FEE-0
exit  fill F1 -> cash_events[1] = FEE(F1)                -0.1   cash_event_id CE-FEE-1
              -> cash_events[2] = GROSS_REALIZATION(F1)     0   cash_event_id CE-GROSS-1
fee_events[0] joins CE-FEE-0 ; fee_events[1] joins CE-FEE-1
each fee_cash_delta equals the joined cash row's signed_delta                [Design section 2.1, "must equal the joined cash", Design section 13, "and equity remains `1000`."]
gross realization appears ONLY in cash_events                                Design section 13, "field, and equity remains `1000"
only cash_events are applied to equity: 1000 + (-0.1) + (-0.1) + 0 = 999.8   Design section 13, "fixture enables only the consecutive-loss"
```

Guard derivation (design `Design section 13, "guards and guard recovery are"`, `Design section 13, "guards and guard recovery are"`; `DECISIONS.md:31` D017 "Interim daily/consecutive-loss PnL
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
this no-funding fixture does not decide OPEN-10                              Design section 13, "last_realized_pnl=0`, so its consecutive-loss count"
[TOKEN SUPERSEDED BY LANE W200 under design v1.9 item 9; marker added by lane W205 under
 G103-F02: the "corrected:" line above spells the basis GROSS_MINUS_FEES. Design v1.9 section 23.4, "and time-stop guards as `GROSS-MINUS-FEES"
 fixes the 2.0.0 basis for daily-loss, consecutive-loss and time-stop guards as the hyphenated
 GROSS-MINUS-FEES, and design v1.9 section 23.5 item 9 (Design v1.9 section 23.4, "and time-stop guards as `GROSS-MINUS-FEES") directed the change; lane
 W200 made it. The current byte is "guard_pnl_basis": "GROSS-MINUS-FEES" (RULE2-07-RED.json:54).
 SPELLING ONLY - last_closed_guard_pnl -0.2, count 1, the false predicate and guard_blocked_raw
 true on the lines above and below are unchanged and still current. NO VALUE MOVED; the node-by-
 node restatement is W200 W-2 (DERIVATIONS.md:2911-2925).]
```

Declared `rule2_divergent_projection` (design `Design section 13, "classify one declared taker exit"`):

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/fee_events` | `ABSENT` (no such container in `LEGACY_P011_EXACT_V1`, design `Design section 15.3, "funding_events`, `sequence`, or any other"`, `Design section 13, "0`, legacy has no v2"`) | `PRESENT(A:2)`, each `fee_cash_delta` `F:-0.1` | yes |
| `/RESULT_SURFACE/trades/0/net_trade_pnl` | `ABSENT` (single `pnl` field, design `Design section 13, "0`, legacy has no v2"`) | `PRESENT(F:-0.2)` | yes |
| `/RESULT_SURFACE/guards/guard_pnl_basis` | `ABSENT` | `PRESENT(S:"GROSS_MINUS_FEES")` | yes |
| `/RESULT_SURFACE/guards/last_closed_guard_pnl` | `ABSENT` | `PRESENT(F:-0.2)` | yes |
| `/RESULT_SURFACE/guards/consecutive_loss_count` | `PRESENT(I:0)` | `PRESENT(I:1)` | yes |
| `/RESULT_SURFACE/guards/guard_blocked_raw` | `PRESENT(B:0)` | `PRESENT(B:1)` | yes |
| `/RESULT_SURFACE/equity_curve/last` | `PRESENT(I:1000)` | `PRESENT(F:999.8)` | yes (value and kind) |

`gross_realized_pnl` is `0` on both versions and is therefore **not** a divergent member (correction
C-07). `0.001`, `0.1`, `-0.1`, `-0.2` and `999.8` are float nodes; `100`, `0`, `1` and `1000` are
integer nodes.

**TOKEN SUPERSEDED BY LANE W200 under design v1.9 item 9; marker added by lane W205 under
G103-F02.** The `2.0.0` cell of the `/RESULT_SURFACE/guards/guard_pnl_basis` row above
(`DERIVATIONS.md:756`) reads `PRESENT(S:"GROSS_MINUS_FEES")`, and the guard-derivation fence
(`DERIVATIONS.md:736`) spells the same token with underscores. Design **v1.9** `Design section 23.4, "and time-stop guards as `GROSS-MINUS-FEES"` fixes the
`2.0.0` basis for daily-loss, consecutive-loss and time-stop guards as the hyphenated
`GROSS-MINUS-FEES`, and design v1.9 section 23.5 item 9 (`Design v1.9 section 23.4, "and time-stop guards as `GROSS-MINUS-FEES"`) directed the family to change
the inconsistent values; lane W200 did so - see W200 W-2 (`DERIVATIONS.md:2888-2931`). The
current byte is `"guard_pnl_basis": "GROSS-MINUS-FEES"` (`RULE2-07-RED.json:54`;
`RULE2-07-GREEN.json:38`). Both sites above describe the pre-W200 serialization and were correct
when written. **Spelling only:** the row's `1.0.0` `ABSENT`, its presence on `2.0.0` and its
`Differs? yes` all still hold, every other row of this table is unchanged, and the `guards` object
itself still exists on both RULE2-07 rows. **NO VALUE MOVED** - the basis names the same economic
rule under either spelling, and the node-by-node restatement is W200 W-2
(`DERIVATIONS.md:2911-2925`). (G103-F02 named the table row only; the fence line is the same
residue in the same derivation and is marked here rather than left. Recorded in
`W205_DERIVATIONS_RESIDUE_REPORT.md`.)

Blocked cells: the exit intent is unnamed, so `fill_events/1/event_class`,
`fee_events/1/event_class`, `exit_events/0/exit_id` and `exit_events/0/reason` are
`BLOCKED-MISSING-SCENARIO-INPUT` (**D-05**); `event_timestamp`, `lifecycle_id` and
`settlement_currency` are not stated by the vector; `schedule_id`/`schedule_digest` are
`BLOCKED-MISSING-RECORD-BYTES`. The economically load-bearing fields — `rate 0.001`,
`fixed_component 0`, `fee_notional 100`, `fee_amount 0.1`, `fee_cash_delta -0.1`,
`liquidity_role TAKER` — are all sealed from the vector.

### RULE2-07-GREEN — `close_only_deterministic_v2`

Inputs (design `Design section 13, "gross-minus-fees interim basis, corrected `last_closed_guard_pnl=-0.2"`): `initial_equity=1000`, an **empty fill-event input**, the same zero-impact
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
they do not exist in the legacy shape, so the legacy selector resolves ABSENT and design `Design section 15.3, "six ordered containers: `decision_events`, `fill_events"` would
score `ABSENT` versus `A:0` as divergence. They are version-specific added containers under design
`Design section 6, "and intentionally added ledger/container nodes"`.

`/RESULT_SURFACE/guards/last_closed_guard_pnl` is deliberately **ABSENT** rather than `0`: no
lifecycle closes in this fixture, and design `Design section 15.3, "- `RESULT_SURFACE`: final position/state, lifecycle"` makes missing and zero different nodes.

### 7.1 Note on the guard-basis authority

Design `Design section 13, ". The current time-stop profit/loss"` cites `DECISIONS.md:31` for the interim gross-minus-fees basis. That line was read this
session and reads: "D017 | 2026-07-18 | Interim daily/consecutive-loss PnL is gross minus fees;
funding capture is deferred and live remains blocked." The owner's OPEN-10 answer extends exactly
this rule to `2.0.0` for all three controls with no per-control divergence.

---

## 8. DEF-P012-08 — per-interval funding and `funding_events` (design `Design section 13, "0`, no funding event, and"`)

### RULE2-08-RED — `close_only_deterministic_v2`

Inputs (design `Design section 14, "The named inputs derive notional"`): funding-only event, `lifecycle_id=1`, `initial_equity=1000`, `open_qty=1`,
`mark=100`, `cm=1`, `event_id="TEST-FUND-1"`, `event_timestamp="2000-01-01T00:00:00Z"`,
`raw_rate=0.001`, venue convention **LONG pays positive**; the position is open immediately before
and after the event timestamp under the synthetic snapshot rule, so it is eligible.

```
notional           = |100 * 1 * 1|                    = 100                  Design section 14, "-raw_rate  if venue convention says positive rate is paid by LONG"
convention "positive rate paid by LONG"
                   -> long_cashflow_rate = -raw_rate  = -0.001               Design section 14, "is open immediately before and"
side_factor (long) = +1                                                       Design section 14, "the event timestamp under the"
funding_cash_delta = 100 * (-0.001) * (+1)            = -0.1                 [Design section 14, "snapshot rule. The named inputs", Design section 14, "snapshot rule. The named inputs"]
negative delta debits equity                                                  Design section 14, "inputs derive notional `100`, long"
corrected equity   = 1000 + (-0.1)                    = 999.9                [Design section 14, "inputs derive notional `100`, long"; exact, see 0.6]
cumulative_funding = -0.1
```

Legacy has no funding ledger and no funding cashflow at all (design `Design section 14, "has no funding cashflow and"`; `core/types.py` has no
funding fields per design `Design section 15.3, "be explicitly empty. Legacy reproduction"`), so legacy equity stays `1000`.

Ledger and join (design `Design section 14, "funding-kind `cash_events[]` row selected by"`): one funding-kind `cash_events` row
`{cash_event_id:"CE-FUND-0", kind:"FUNDING", lifecycle_id:1, signed_delta:-0.1}` and one
`funding_events` row that is its typed projection, joined by `cash_event_id`, with
`funding_cash_delta == -0.1 ==` the joined cash row's signed delta. Only the cash row is applied to
equity. `fill_events` is `A:0` because design `Design section 14, "eligible, no funding row is"` states neither RULE2-08 vector contains a fill
intent, so §3's fill-only slippage sequence is not entered and no `CostSchedule` is consumed.

| Node | `1.0.0` | `2.0.0` | Differs? |
|---|---|---|---|
| `/EVENT_SURFACE/funding_events` | `ABSENT` | `PRESENT(A:1)`, `funding_cash_delta` `F:-0.1` | yes |
| `/EVENT_SURFACE/cash_events` | `ABSENT` | `PRESENT(A:1)` funding-kind `F:-0.1` | yes |
| `/RESULT_SURFACE/cumulative_funding` | `ABSENT` | `PRESENT(F:-0.1)` | yes |
| `/RESULT_SURFACE/equity_curve/last` | `PRESENT(I:1000)` | `PRESENT(F:999.9)` | yes (value and kind) |

Sealed `funding_events[0]` fields, all from the vector and the §14 field list at `Design section 14, "sequence, funding_event_id, event_timestamp, lifecycle_id, position_side,"`:
`sequence 0`, `funding_event_id "TEST-FUND-1"`, `event_timestamp "2000-01-01T00:00:00Z"`,
`lifecycle_id 1`, `position_side "LONG"`, `open_qty 1`, `contract_multiplier 1`, `mark_price 100`,
`raw_rate 0.001`, `positive_rate_payer "LONG"`, `long_cashflow_rate -0.001`, `notional 100`,
`funding_cash_delta -0.1`, `cumulative_funding -0.1`, `cash_event_id "CE-FUND-0"`. Float nodes:
`raw_rate`, `long_cashflow_rate`, `funding_cash_delta`, `cumulative_funding`, equity. Integer nodes:
`sequence`, `lifecycle_id`, `open_qty`, `contract_multiplier`, `mark_price`, `notional`.
`schedule_id`, `schedule_digest` and `source_event_digest` are `BLOCKED-MISSING-RECORD-BYTES`.

Guard outcome (design `Design section 14, "outcomes follow the sourced OPEN-10"` "Guard outcomes follow the sourced OPEN-10 decision and are explicit
comparison nodes"): under the owner's OPEN-10 answer the guard basis stays gross-minus-fees and the
captured funding delta does **not** enter it, so `guard_pnl_basis = "GROSS_MINUS_FEES"`,
`funding_included_in_guard_basis = false`, `consecutive_loss_count = 0` (no lifecycle closes).

**SUPERSEDED BY LANE W200 under design v1.9 item 9; marker added by lane W205 under G103-F01.**
The paragraph above derives a `guards` object for `RULE2-08-RED` and names three of its members as
expected `2.0.0` comparison nodes. **That object no longer exists on this row.**
`funding_included_in_guard_basis` went first, removed by lane W167 item 4 under design `Design section 22.6, "if the owner binds entry"`
(W167 W-5, `DERIVATIONS.md:1922-1930`). Design **v1.9** section 23.5 item 9 (`Design section 23.4, "AMENDMENT-CHOICE`: `funding_included_in_guard_basis` is forbidden because"`) then
directed removal of the **whole** `guards` object on `RULE2-08-RED` unless a separate owner-approved
scenario-input amendment binds its threshold and requires re-derivation; no such amendment exists,
and lane W200 removed the object - see W200 W-3 (`DERIVATIONS.md:2933-2968`). `RULE2-08-RED`'s
`RESULT_SURFACE` now carries exactly eight keys - `final_position`, `trades`, `equity_curve`,
`cumulative_funding`, `metrics`, `warnings`, `refusals`, `run_manifest`
(`RULE2-08-RED.json:40-59`) - and **no guard node of any kind**. Where the current state lives: the
removal record on the artifact itself (`RULE2-08-RED.json:93`, `w200_revised_nodes`) and W200 W-3.
Design v1.9 `Design v1.9 section 22.6, "F contains exactly `TEST-FUND-1`, raw"` admits a `guards` member exactly when a declared guard projection is evaluated,
and none is declared for this vector. The OPEN-10 disposition the paragraph above reads is
**unchanged and still binds the family**; it simply has no node on this row
(`RULE2-08-RED.json:21`). **NO VALUE MOVED** - none of the removed members is a money figure, rate,
quantity or price, and `notional 100`, `long_cashflow_rate -0.001`, `funding_cash_delta -0.1`,
`cumulative_funding -0.1` and `equity_curve` `1000` / `999.9` are byte-identical (W200 W-3,
`DERIVATIONS.md:2963-2968`).

### RULE2-08-GREEN — `close_only_deterministic_v2`

Inputs (design `Design section 14, "999.9`. Legacy has no"`): `lifecycle_id=1`, the same complete schedule containing `TEST-FUND-1`, the
same snapshot rule and initial equity `1000`, but the position is **closed immediately before** the
event timestamp.

```
required event coverage present -> not REFUSED_MISSING_FUNDING_EVENT          [Design section 14, "id `1`, the same complete", Design section 14, "id `1`, the same complete"]
no position eligible at the event timestamp -> no funding row emitted         Design section 14, "1`, the same complete schedule"
no fill intent in either vector -> no fill, no fee, no gross realization      Design section 14, "1`, the same complete schedule"
both versions: economic cash/equity projection = 1000                         Design section 14, "lifecycle id `1`, the same"
```

| Node | `1.0.0` | `2.0.0` | Equal? |
|---|---|---|---|
| `/RESULT_SURFACE/equity_curve/last` | `PRESENT(I:1000)` | `PRESENT(I:1000)` | yes |
| `/EVENT_SURFACE/fill_events` | `PRESENT(A:0)` | `PRESENT(A:0)` | yes |
| `/RESULT_SURFACE/final_position` | `PRESENT(N)` | `PRESENT(N)` | yes |

`funding_events` and `RESULT_SURFACE/cumulative_funding` are **excluded** from this GREEN projection
(corrections C-02 / C-03) and recorded as version-specific added nodes. The declared GREEN member is
the economic cash/equity value `1000` that design `Design section 14, "id `1`, the same complete"` names.

`trades` is written `[]` on the reading that the pre-window close named by the vector supplies no
fill facts and mutates no equity (the vector fixes the projection at 1000). That reading is a
judgement call and is recorded in the artifact and as discrepancy **D-05**.

---

## 9. Catalog conservation recount (design's own declaration arithmetic)

Re-counted from the v1.4 design itself, **not** from the lane spec:

| Owning DEF | RED rows | GREEN rows | PROBE ids | Design lines |
|---|---|---|---|---|
| DEF-P012-01 | RULE2-01-RED | RULE2-01-GREEN | PROBE-P012-01-A, PROBE-P012-01-B | `Design section 7, "quantity node. `PROBE-P012-01-B` changes the"`, `Design section 7, "quantity node. `PROBE-P012-01-B` changes the"` |
| DEF-P012-02 | RULE2-02-RED | RULE2-02-GREEN | PROBE-P012-02-A | `Design section 8, "1`, leverage-cap quantity `100`, and"`, `Design section 8, "1`, leverage-cap quantity `100`, and"` |
| DEF-P012-03 | RULE2-03-RED | RULE2-03-GREEN | PROBE-P012-03-A | `Design section 8, "1`, leverage-cap quantity `100`, and"`, `Design section 8, "1`, leverage-cap quantity `100`, and"` |
| DEF-P012-04 | RULE2-04-RED | RULE2-04-GREEN | PROBE-P012-04-A | `Design section 10, "close `92`; the OPEN-06-contingent corrected"`, `Design section 10, "close `92`; the OPEN-06-contingent corrected"` |
| DEF-P012-05 | RULE2-05-RED | RULE2-05-GREEN | PROBE-P012-05-A, PROBE-P012-05-B | `Design section 11, "legacy fill is `100`, corrected"`, `Design section 11, "legacy fill is `100`, corrected"` |
| DEF-P012-06 | RULE2-06-RED, **RULE2-06-EQUAL-PRICE-RED** | RULE2-06-GREEN | PROBE-P012-06-A | `Design section 12, "target fractions, tick, test-only zero-impact"`, `Design section 12, "target fractions, tick, test-only zero-impact"`, `Design section 12, "Fail probe `PROBE-P012-06-A` binds exactly once"` |
| DEF-P012-07 | RULE2-07-RED | RULE2-07-GREEN | PROBE-P012-07-A | `Design section 13, "gross PnL and cash delta are `0`"`, `Design section 13, "Fail probe `PROBE-P012-07-A`: classify one declared taker exit as maker."` |
| DEF-P012-08 | RULE2-08-RED | RULE2-08-GREEN | PROBE-P012-08-A | `Design section 14, "`RULE2-08-RED` is a synthetic funding-only event"`, `Design section 14, "Fail probe `PROBE-P012-08-A`: flip the sign for the long positive-rate event."` |

**Totals: RED = 9, GREEN = 8, PROBE = 10, catalog rows = 27.**

Cross-checks against the design's own conservation statements:

- `Design section 15.2, "failed check, and expected first"` "all nine RED scenarios exhibited their declared old/new differences" ⇒ 9 RED ✓
  (8 numbered plus `RULE2-06-EQUAL-PRICE-RED`; the v1.4 micro-fold row `DS18-F01` at `Design v1.4 change log, "row; §15.5 sweeps the RED"` records
  that it "sweeps the RED receipt count from eight to nine").
- `Design section 15.2, "first changed node/path. `execution_profile_id` is"` "all eight GREEN projections agreed" ⇒ 8 GREEN ✓ (the equal-price RED has no GREEN sibling;
  design `Design section 12, "projection. The shipped close-only default"` declares it as "one additional declared synthetic `RED` scenario").
- `Design section 15.2, "execution_profile_id` is part of the"` "For each DEF, the catalog contains its declared RED row, GREEN row, and every declared
  `probe_id` exactly once; it also contains the additional DEF-P012-06 `RULE2-06-EQUAL-PRICE-RED` row
  exactly once" ✓ — verified mechanically: the emitted catalog has 27 rows and 27 unique
  `scenario_id` values.
- `:174-179` fail-probe contract: each declared `probe_id` binds exactly once to a `PROBE` catalog
  row; the per-DEF probe counts match each correction section's "Fail probe(s)" paragraph; total 10 ✓.

Expected-surface artifacts authored: one file per RED/GREEN scenario → **17 files** under
`golden/corrected_vnext/`, each carrying both `EVENT_SURFACE` and `RESULT_SURFACE`. PROBE rows carry
no expected artifact of their own; each compares its variant output to the independently sealed
producer named by its `base_scenario_id` (design `Design section 15.2, "top-level gate compares the variant"`).

---

## 10. Probe rows — bindings and first-changed-node derivations

Each row's `expected_first_changed_node` is the node the design names, evaluated against this
bundle's node layout. Where a *different* node would be enumerated earlier under design `Design section 15.2, "the current node first, then"`'s
UTF-8-byte-order object walk, that is recorded rather than silently substituted (**D-14**).

| Probe | Base | Kind | Expected failed check | Design-named node | Enumeration note |
|---|---|---|---|---|---|
| PROBE-P012-01-A | RULE2-01-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/quantity` | if the variant also rewrites `decision_events/1/contract_multiplier`, `decision_events` sorts before `fill_events` and would fail first |
| PROBE-P012-01-B | RULE2-01-GREEN | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/quantity` | expected 1, variant 0 |
| PROBE-P012-02-A | RULE2-02-GREEN | KERNEL | RULE-2 GREEN cross-version | `/RESULT_SURFACE/admitted` | the cross-version check compares only the declared shared projection (design `Design section 15.2, "OBSERVED`, `KERNEL`, or `GATE`), expected"`), so earlier full-surface changes belong to the separate corrected-expectation check |
| PROBE-P012-03-A | RULE2-03-RED | INPUT | record-identity preflight | `BLOCKED-MISSING-RECORD-BYTES` | the refusal precedes any scenario output, so no comparison-surface node exists; the changed artifact is the record file, whose bytes the design never lists (**D-15**) |
| PROBE-P012-04-A | RULE2-04-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `decision_events/1/reference_price`, `decision_events/1/reference_source` and `fill_events/0/fill_trigger` all change and sort earlier (`fill_trigger` < `final_fill_price` because byte 3 is `l` 0x6c vs `n` 0x6e) |
| PROBE-P012-05-A | RULE2-05-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/final_fill_price` | actual 100 vs expected 101; `final_fill_price` sorts before `slippage_*` and `unrounded_fill_price`, so it is genuinely first |
| PROBE-P012-05-B | RULE2-05-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/final_fill_price` | actual 102 vs expected 101; design `Design section 11, ". Each must make the"` also refuses the second application via `slippage_application_count` |
| PROBE-P012-06-A | RULE2-06-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fill_events/0/exit_id` | design `Design section 12, "CONTRACT_TABLES` expected artifact unchanged. The"` fixes expected first fill `TARGET-NEAR` vs variant `TARGET-FAR`; in this layout `decision_events/2/ordered_chosen_exit_ids/0` carries the same reversal and sorts earlier |
| PROBE-P012-07-A | RULE2-07-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/fee_events/1/liquidity_role` | the vector states no maker rate, so whether `fee_amount`/`fee_cash_delta`/`cash_events/1/signed_delta` also change is underivable; if they do, `cash_events` sorts before `fee_events` (**D-16**) |
| PROBE-P012-08-A | RULE2-08-RED | KERNEL | corrected expectation | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | expected −0.1 vs variant +0.1; `cash_events/0/signed_delta` carries the same flip and sorts earlier, so the catalog records it as the first changed node |

**PREAMBLE AND TABLE SUPERSEDED BY LANE W262 under design v1.11 `Design v1.11 section 15.2, "before/after file SHA-256 values, and"` (amendment-choice W261);
marker added by lane W262 under W262-R01.** The preamble above says a *different* earlier-enumerated
node "is recorded rather than silently substituted (**D-14**)", and for `PROBE-P012-06-A`,
`PROBE-P012-07-A` and `PROBE-P012-08-A` the catalog carried that earlier node instead of the
Design-named node this table lists. Design v1.11 `Design v1.11 section 15.2, ". `GATE_READER` makes a fresh"` supersedes the strict first-node equality:
the catalog's `expected_first_changed_node` is now the design-named target node, which need only be a
member of the complete changed-node set, and the comparator's traversal-order first node is recorded
separately as `comparator_first_differing_node`. `PROBE-P012-03-A`'s `BLOCKED-MISSING-RECORD-BYTES`
cell is superseded by design v1.11 `Design v1.11 section 8, "is not named here: lines"`, which names the mutated record path. The per-row
before/after values, the rule quoted in full and the measured comparator nodes are in the W262 section
appended at the end of this worksheet. **NO ECONOMIC VALUE MOVED BY THIS MARKER** - the preamble and
table above are left exactly as their lanes wrote them.

Modified-copy trees, modification manifests, their digests, and every serialized scenario-input digest
are `BLOCKED-BUILD-ARTIFACT` (**D-10**): design `Design section 15.2, "bytes remain outside the variant"` requires a complete kernel variant tree
plus a `KERNEL_FILE_PATCH` with before/after file digests, and no corrected kernel source exists
pre-implementation. `IMPLEMENTATION_BASE_SHA` is likewise not yet fixed.

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** In the paragraph above, two
assertions are false at the current build and are withdrawn: "no corrected kernel source exists
pre-implementation", and "`IMPLEMENTATION_BASE_SHA` is likewise not yet fixed". The corrected kernel
source exists at `C:\WP012BUILD` HEAD `d32e903a`, and `IMPLEMENTATION_BASE_SHA` is fixed at
`63cfe2dd2dcb3373f2fa18c385f67a1c2d113bb5` under owner decision 147
(`IMPLEMENTATION_ANCHOR_DRAFT.json:5` and `:137-144`). The `BLOCKED-BUILD-ARTIFACT` classification in
D-10 itself is untouched by this marker and is not re-adjudicated here. The measurement, and the true replacement wording, are
recorded once at this worksheet's section-0 independence fence, in the W359 marker there.

---

## 11. Discrepancies

Design ambiguities and prompt/evidence conflicts that forced a judgement call. These are reported,
not silently resolved (clause C-2; lane W127 line 54).

- **D-01** Design `Design section 3, "for that fill; on an"` mandates a fee cash event for every executed fill, but RULE2-01, RULE2-02-GREEN,
  RULE2-05 and the RULE2-06 family supply no `CostSchedule`, and design `Design section 5.1, "no BOM, LF line endings, and a required final LF. Its"` refuses a missing
  schedule rather than defaulting it. Those `cash_events`/`fee_events`/`liquidity_role` cells are
  `BLOCKED-MISSING-SCENARIO-INPUT`, not guessed as zero. Strictly read, `Design section 5.1, "file with no BOM, LF line endings, and a required final LF. Its"` would make the corrected
  adapter refuse these scenarios outright, which contradicts the concrete corrected quantities the
  design states for them.
- **D-02** RULE2-03-GREEN specifies no equity, entry or exit action, so its cross-version projection
  has no positive economic value — only "identity validated; no override refusal".
- **D-03** RULE2-04-RED omits entry basis, `contract_multiplier` and initial equity, yet design `Design section 10, "price, gross PnL, cash/equity, exit"`
  requires gross PnL, cash/equity, trade and metrics to change on RED. Those cells are
  `BLOCKED-MISSING-SCENARIO-INPUT`; only the fill-price/`fill_trigger` divergence — the node the
  design's own probe at `Design section 10, "price, gross PnL, cash/equity, exit"` fixes — is sealed.
- **D-04** RULE2-06-RED, RULE2-06-GREEN and RULE2-06-EQUAL-PRICE-RED omit initial equity; absolute
  equity and metric cells are blocked. Gross realized PnL is sealed under the cm-default.
- **D-05** RULE2-07-RED says "long round trip" and RULE2-07-GREEN says "empty fill-event input"
  without naming the exit intent; `exit_events/0/exit_id`, `exit_events/0/reason` and the exit
  `event_class` are blocked. Relatedly, RULE2-08-GREEN names a pre-window close with no fill facts;
  `trades` is written `[]` as a recorded judgement call.
- **D-06** `contract_multiplier` is not restated in RULE2-04, RULE2-05 or the RULE2-06 family. It is
  taken as `cm = 1` from the shipped kernel default at `config.py:49` (design `Design section 7, "sizing equity `1000`, `fallback_size_pct=10%`, final"` states the same)
  and tagged `(cm-default)` — a cited default, not an invented number. Every affected divergence uses
  the same `cm` on both versions, so no old-versus-new difference depends on it.
- **D-07 / D-08** *(resolved by this lane, was open in the partial)* The design's decimals `999.8`
  (`Design section 13, "false, and `guard_blocked_raw` is true"`) and `999.9` (`Design section 13, "false, and `guard_blocked_raw` is true"`) were shown in §0.6 to be exactly the binary64 results of the stated
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
  `STOP_FIRST` as the mandatory policy for acceptance-bearing `2.0.0` runs, while design `Design section 12, "close-only default is out of"`
  declares `TARGET_FIRST` as an explicit input of `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED`, and
  the OPEN-06 proposal records P23 (the equal-price tie-break) as not-applicable under `STOP_FIRST`
  (`P012_OPEN06_RETAINED_RETIRED_PROPOSAL_V1.md:65`). Design `Design section 12, "RED` scenario owned by DEF-P012-06"` forbids closing OPEN-06 from
  silently rewriting the pair, so this bundle seals `TARGET_FIRST`. Under `STOP_FIRST` both RED
  scenarios would collapse onto the legacy result and DEF-P012-06 would have no divergent projection,
  which design §15.4 refuses. **Owner resolution required.**
- **D-13** The design fixes the six `EVENT_SURFACE` container names and the exact `fee_events` /
  `funding_events` row field lists, but it does **not** fix `RESULT_SURFACE` member names beyond the
  categories at `Design section 14, "RED golden's equity/net/metrics nodes"`, nor the `decision_events` reason vocabulary, nor the `fill_events` /
  `cash_events` / `exit_events` field names. Those names are authored by this lane. Node pointers —
  and therefore every "first changed node" — depend on them.
- **D-14** Consequence of D-13: for four probes the design's named refusal node is not necessarily the
  first node the enumerator reaches. Recorded per probe in §10 and in each catalog row's `note`.

  **DISCREPANCY CLOSED BY LANE W262 under design v1.11 `Design v1.11 section 15.2, "fresh byte-for-byte scratch copy of"` (amendment-choice W261); marker
  added by lane W262 under W262-R01.** The design no longer requires the named node to be the first
  node the enumerator reaches: it must only be a member of the complete changed-node set, and the
  comparator's traversal-order first node is recorded beside it in each catalog row as
  `comparator_first_differing_node`. **D-14** is therefore closed as a derivation ambiguity. The
  bullet above is left exactly as lane W127b wrote it.
- **D-15** `PROBE-P012-03-A` refuses before any scenario output exists, so it has no
  comparison-surface node to name. Its `expected_first_changed_node` is recorded as
  `BLOCKED-MISSING-RECORD-BYTES` — the changed artifact is the frozen record file, whose bytes and
  detached `.sha256` the design never lists.

  **DISCREPANCY CLOSED BY LANE W262 under design v1.11 `Design v1.11 section 8, "decision 143, 2026-09-03, default (a"` (amendment-choice W261); marker
  added by lane W262 under W262-R01.** The record bytes now exist, and design v1.11 `Design v1.11 section 8, "frozen test record uses `min_notional=101"` names
  this probe's node as the mutated record path
  `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json`, "not a placeholder";
  design v1.11 `Design v1.11 section 15.2, "first changed node/path. `execution_profile_id` is"` makes that mutated record path the path member of the difference set for a
  record-identity refusal before scenario output. The catalog field no longer reads
  `BLOCKED-MISSING-RECORD-BYTES`. **D-15** is closed for that field; the bullet above is left exactly
  as lane W127b wrote it.
- **D-16** `PROBE-P012-07-A` reclassifies a taker exit as maker, but the RULE2-07 vector states no
  maker rate, so whether the fee amount and the joined cash delta also change is underivable. Only
  the role node is certain to differ.
- **D-17** The lane brief anticipated that the W127 partial "may predate v1.4's new scenario
  `RULE2-06-EQUAL-PRICE-RED`". It does not: the partial derives that scenario and cites the v1.4
  micro-fold. Recorded per clause C-2 (prompt disagreed with the evidence).
- **D-18** Design `Design section 15.1, "The later run manifest and"` requires `CONTRACT_TABLES` to be "sealed at `EXPECTED_SEAL_SHA` no later than
  `IMPLEMENTATION_BASE_SHA`", and design `Design section 15.1, "The later run manifest and"` requires a Lead-accepted `IMPLEMENTATION_ANCHOR`.
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
**v1.5** (title Design v1.5 change log, "v1.5 change log — input-embedding addendum"; v1.5 change log Design v1.5 change log, "v1.5 change log — input-embedding addendum"). File length **967 lines**, final LF present.
Sections 1-21 are unchanged from v1.4; the sole normative addition is **§22** (Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is") plus
the §15.6 computability note (Design section 15.6, "15.6 v1.5 input-embedding computability note"). Line spans used by this revision:

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
`Design section 15.3, "OWNER-RULED (owner addendum 29, decision 71):** Section"` and the W155 report's golden-impact table were re-checked row by row against this
worksheet's own `blocked_cells` records rather than trusted. Two corrections to that list are
recorded as **V15-D06** in the discrepancy block below: it under-states RULE2-02-RED (which also
gains its cost/funding schedule identities) and it does not mention that `PROBE-P012-07-A`'s
`D-16` maker-rate ambiguity is closed by §22.3's maker binding. Everything else it names matched.

---

### R-0 Shared arithmetic

#### R-0.1 The bound synthetic `CostSchedule` (design `Design section 22.3, "or not its row emits"`)

Every section-22 `CostSchedule` — including the rows that emit no fill — carries
`venue_scope="SYNTHETIC"`, `product_type_scope="LINEAR_TEST_CONTRACT"`,
`symbol_scope="SYNTH-<scenario_id>"`, settlement `TEST-USD`, effective interval
`[1999-12-31T00:00:00Z, 2000-01-02T00:00:00Z)`, `maker_rate=0.00015`, `fixed_component=0`,
`minimum_fee=0`, `fee_rounding_rule="EXACT_IDENTITY_V1"`, `slippage_model_id="BPS_OF_REFERENCE_V1"`,
`slippage_parameters={slippage_bps: <the section 7-13 scenario value>}`, and
`liquidity_roles = {ENTRY, MARKET_EXIT, PROTECTIVE_STOP_EXIT, TARGET_EXIT}` all mapped to `TAKER`.
`taker_rate=0.00045` everywhere **except RULE2-07**, which keeps its section-13 stated `0.001`
(design `Design section 22.3, "ENTRY`, `PROTECTIVE_STOP_EXIT`, `TARGET_EXIT`, and `MARKET_EXIT"`). This closes **D-01** for every scenario except in the two respects recorded as
V15-D01 and V15-D03 below.

The fee formula is unchanged (design `Design section 13, "fixture as `round_and_apply_minimum(x)=x"`):

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

**TOKEN SUPERSEDED BY LANE W186 under owner addendum 28 decision 68; marker added by lane W224
under GM62-F04.** The `n = 101` row of the table above and the `0.04545  0x3fa74538ef34d6a1` entry
of the raw-bits fence above both label `0.04545` a **sealed** token. `101` was `RULE2-05-RED`'s
`fee_notional` and no other row in this bundle uses it; under owner addendum 28 decision 68 that
row's quantity is ZERO, so `fee_notional = abs(101 * 0 * 1) = 0`, `fee_amount = 0` and
`fee_cash_delta = 0` (`RULE2-05-RED.json:36`, before/after at `RULE2-05-RED.json:94-96`). **No
artifact in this bundle seals `0.04545` on any node any more** - measured this session over all 17
goldens under `golden/corrected_vnext/`, the only remaining occurrences of that token are inside
`RULE2-05-RED.json`'s own dated records, `v15_filled_cells` (`:65-66`) and the `before:` values of
`w186_revised_nodes` (`:94-96`). **The arithmetic itself is unchanged and still correct**:
`fl(0.04545)` really is significand `6550035298047649` at bits `0x3fa74538ef34d6a1`, the row was
correct when written, and every other row of the table and every other line of the fence names a
token this bundle still seals. Only the word "sealed" stopped applying to this one row. **NO VALUE
MOVED.** The re-derivation is W186 Z-5. GM62-F04 named R-0.4, R-9 and the Y-1 table; this row is the
same residue in the same class and is marked here rather than left.

The maker rate is needed only by `PROBE-P012-07-A` (R-19): `100 * fl(0.00015)` rounds to
`fl(0.015) = 0x3f8eb851eb851eb8`, token `0.015`.

#### R-0.4 Equity accumulation and the observation-window scope

Design `Design section 2.1, "must equal the joined cash"` and `Design section 3, "fill; on an exit, append"` step 11 fix the ledger: each chosen fill appends its fee cash event, and an
exit additionally appends its gross realized PnL in the same fill sequence; **only `cash_events` are
applied to equity**, in sequence order. This bundle therefore writes

```
equity_curve.last = equity_curve.first + sum(cash_events[i].signed_delta) in sequence order
```

`equity_curve.first` is the equity at the **start of the observation window**. Design v1.5 gives
four rows an evaluation-only window that expressly excludes their setup fills
(`RULE2-04-RED/GREEN` at `Design section 22.5, "qty `1`, active stop `100"`, the three `RULE2-06` rows at `Design section 22.5, "qty `1`, active stop `100"`, `RULE2-08-RED` at
`Design section 22.6, "addendum 20 (5a) GREEN has"`); the remaining rows take the `M-06` default of first-through-last bar (`Design section 22.2, "and corrected intent/event timestamps are"`), where the
window start is the account seed. The window-scoped reading is the only one that keeps the `Design section 2.1, "Normative cash-ledger rule:** every fee"`
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
[VALUE SUPERSEDED BY LANE W186 under owner addendum 28 decision 68; marker added by lane W224
 under GM62-F04: the RULE2-05-RED line above reads 1000 - fl(0.04545) = 999.95455 at bits
 0x408f3fa2eb1c432d. Owner addendum 28 decision 68 ruled that design section 7 governs that row
 and its quantity is ZERO, so the fee is 0, the joined cash delta is 0, and the accumulation is
 1000 - 0 = 1000. The current sealed bytes are "equity_curve": {"first": 1000, "last": 1000}
 (RULE2-05-RED.json:45), with the golden's own before/after record at RULE2-05-RED.json:97.
 equity_curve.first 1000 is UNCHANGED; only last moved. Every other line of this fence, and the
 whole window-scoping derivation above it, is unchanged and still current. NO VALUE MOVED HERE -
 the superseded accumulation above is left exactly as written. W186 Z-5 already named this line,
 by its pre-W205 number :1182; that pointer is itself stale and is corrected under GM62-F07 in
 the W224 section below.]

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

Lifecycle-net values (design `Design section 13, "every linked fee and funding"`: gross plus every linked fee and funding cash delta, applied in
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

#### R-0.5 Record identities (design `Design section 22.3, "INSTRUMENT|COST|FUNDING}-<scenario_id>-V1`, except"`, `Design section 22.3, "INSTRUMENT|COST|FUNDING}-<scenario_id>-V1`, except"`, `Design section 22.3, "INSTRUMENT|COST|FUNDING}-<scenario_id>-V1`, except"`)

Record ids are the `MECHANICAL` string `SYNTH-{INSTRUMENT|COST|FUNDING}-<scenario_id>-V1`, except
that `RULE2-08-RED` and `RULE2-08-GREEN` share the exact funding record id
`SYNTH-FUNDING-RULE2-08-V1`. Every `InstrumentRecord` carries effective interval
`[1999-12-31T00:00:00Z, 2000-01-02T00:00:00Z)`, written here with the closed member set
`{start_inclusive, end_exclusive}` fixed at `:772-773`. Those cells were
`BLOCKED-MISSING-RECORD-BYTES` / `BLOCKED-MISSING-SCENARIO-INPUT` and are now filled in all 17
artifacts.

**Digests are NOT filled.** Design `Design section 22.1, "record and input digests are"` keeps record and input digests `MECHANICAL` build
artifacts computed from later-authored bytes, `Design section 22.3, "results computed after canonical bytes"` expressly refuses to fabricate the
provenance `captured_at_utc` and `human_reviewer` members, and the canonical-JSON rule at `Design section 22.1, "tokens; record and input digests"`
fixes sorted keys, no BOM, LF, a final LF, duplicate-key refusal and finite tokens but **not** the
separator or indentation width. The exact byte string that a SHA-256 would hash is therefore still
undetermined, for the record files and for the RULE2-08 source event alike. Every
`*_record_digest`, `*_schedule_digest`, `instrument_source_document_digest` and
`source_event_digest` cell stays `BLOCKED-MISSING-RECORD-BYTES`. Recorded as **V15-D05**.

---

### R-1 RULE2-01-RED

Bars `[INIT98, ENTRY100]` (`Design section 22.2, "INIT98=(2000-01-01T00:10:00Z,0,98,98,98,98,0)"`, `Design section 22.4, "requested quantity is sizing-derived"`); entry fill 100, quantity 5, `contract_multiplier = 2`,
all unchanged from §7 and re-verified against the v1.5 config deltas at `Design section 22.4, "requested quantity is sizing-derived"`
(`initial_capital=1000`, `risk_per_long_pct=10`, `max_leverage_cap=10`, tick/step/minima
`1/1/0/0`, `instrument_contract_multiplier=2`, percent stop 10, `tp_mode="None"`).

```
fee_notional = abs(100 * 5 * 2)      = 1000                       [Design section 13, "equity is `999.8`; legacy gross", Design section 22.4, "as RED except runtime `instrument_min_notional=100"]
raw_fee      = 1000 * fl(0.00045) + 0                             [Design section 13, "no v2 net field, and", Design section 22.3, "production fee claims. Except RULE2-07"]
fee_amount   = EXACT_IDENTITY_V1(raw_fee) = 0.45                  [R-0.3 n=1000]
fee_cash_delta = -0.45                                            Design section 7, "versus corrected `5`. Required"
liquidity_role(ENTRY) = TAKER                                     Design section 7, "versus corrected `5`. Required"
cash_events  = [ FEE(F0) -0.45 ]                                  [Design section 3, "exits, record which stop/targets touched" step 11]
equity_curve = { first 1000, last 1000 + (-0.45) = 999.55 }       [Design section 2.1, "is forbidden on fee and", R-0.4]
fee event timestamp = 2000-01-01T00:11:00Z                        [Design section 22.2, "order is `(timestamp,bar_index,open" M-04, Design section 22.2, "order is `(timestamp,bar_index,open" M-06]
```

Filled: `fill_events/0/liquidity_role`, `cash_events`, `fee_events`, `equity_curve/last`,
`run_manifest.instrument_record_id`, `instrument_effective_interval`, `cost_schedule_id`,
`funding_schedule_id`. Unchanged: quantity 5, order notional 1000, both `SIZING_*` decision rows,
`funding_events []`, `exit_events []`.

### R-2 RULE2-01-GREEN

Same bars; fallback branch selected by the §22.7 NaN wire; quantity 1, `cm = 1` (`Design section 22.4, "exact NaN wire from section 22.7 selects fallback"`).

```
fee_notional = abs(100 * 1 * 1) = 100 ; fee_amount 0.045 ; fee_cash_delta -0.045
equity_curve = { first 1000, last 999.955 }
```

§22.7 (`Design section 22.7, "The sole accepted pointer is"`) binds only the strict-JSON transport of the exact bits
`0x7ff8000000000000` at `/corrected_only/economic_inputs/stop_price_f64`, and `Design section 22.7, "Serializes no NaN."` restates that
no NaN is serialized. The `no_serialized_nodes` block is therefore kept and only its citation is
extended; no `stop_price` node is created on either surface.

### R-3 RULE2-02-RED

No fill (corrected refuses `REFUSED_MIN_NOTIONAL`), so no fee and no equity change. v1.5 `Design section 22.4, ", restating section 8"`
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

Owner addendum 20 (1a) and (2a) close both refusals, so the §22.5 candidate prefix at `Design section 22.5, "BE100=(2000-01-01T00:12:00Z,2,101,110,101,110,0)"`
and `Design section 22.5, "(2000-01-01T00:13:00Z,3,90,95,85,92,0)"` is the bound premise. Re-derived from the bound inputs (`initial_capital=1000`,
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
  new active stop = entry + be_buffer_r * R = 100 + 0 = 100        [Design section 22.5, "values, the real path reaches"; exits.py:278-350]
=> the premise Design section 10, "fills at close `92`; the" states (LONG qty 1, active stop 100, no target) is REACHED, and the
   entry basis is the owner-bound 100.
evaluation bar (00:13:00Z, 3, 90, 95, 85, 92, 0), window = that bar only          Design section 10, "close `92`; the OPEN-06-contingent corrected"
  open 90 <= stop 100 -> GAP_OPEN, reference 90, slippage 0, floor tick 1 -> fill 90  (unchanged)
  gross_realized_pnl = (90 - 100) * 1 * 1 = -10                    [addendum 20 (2a); Design section 22.5, "the real path reaches LONG" cm=1]
  fee_notional = abs(90 * 1 * 1) = 90 ; fee_amount 0.0405 ; delta -0.0405   [R-0.3 n=90]
  liquidity_role(PROTECTIVE_STOP_EXIT) = TAKER                     [Design section 22.3, "0.045%`/`0.015%` becomes decimal", Design section 22.5, "active stop `100`, and no target before"]
  in-window cash_events = [ FEE(F0) -0.0405 , GROSS(F0) -10 ]      [Design section 3, "Append the fee cash event for that fill" step 11]
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

`[INIT98, ENTRY100]`, `slippage_bps=100`, `price_tick=0.01`, `cm = 1` **explicit** at `Design section 22.5, "1`; C has `slippage_bps=100`, entry"`.
The fill price 101 and impact 1 are unchanged. Design `Design section 11, "fill is `100`, corrected fill"` bases the fee on the **final** fill:

```
fee_notional = abs(101 * 1 * 1) = 101 ; fee_amount 0.04545 ; delta -0.04545   [R-0.3 n=101]
equity_curve = { first 1000, last 999.95455 }
```

`D-06` is closed for this row: `order_notional 101` was sealed under the shipped cm-default and is
now an explicit design input (`Design section 22.3, "The tables lane records the"`, `Design section 22.5, "and owner fee decision; equity"`); the value is byte-identical.

**VALUES SUPERSEDED BY LANE W186 under owner addendum 28 decision 68; marker added by lane W224
under GM62-F04.** Section R-9 above derives `fee_notional = abs(101 * 1 * 1) = 101`,
`fee_amount 0.04545`, `delta -0.04545` and `equity_curve = { first 1000, last 999.95455 }`, and the
`D-06` paragraph immediately above records `order_notional 101` as sealed and byte-identical.
**Four of those figures moved.** Owner addendum 28 decision 68 - recorded at the **W167-D05**
resolution below, citing `N_TIMES.txt:571` - ruled that design section 7 governs this row and the
quantity is ZERO. The current sealed bytes are `quantity 0` (`RULE2-05-RED.json:30`),
`fee_notional 0`, `fee_amount 0`, `fee_cash_delta 0` (`RULE2-05-RED.json:36`), `order_notional 0`
(`RULE2-05-RED.json:43`) and `equity_curve {"first": 1000, "last": 1000}`
(`RULE2-05-RED.json:45`); the golden's own before/after ledger is `RULE2-05-RED.json:90-97`. **What
still stands on this row:** `equity_curve.first 1000`, the fill price `101`, the impact `1`, the
explicit `cm = 1` input and the `:360` final-fill fee basis - W186 Z-5 says in terms "its fill price
101 and impact 1 stand". **D-06 itself remains closed** for this row; only the value the paragraph
calls byte-identical moved. **NO VALUE MOVED BY THIS MARKER** - the superseded arithmetic above is
left exactly as written. The re-derivation is W186 Z-5, which already named this section by its
pre-W205 number `:1369-1380`; that pointer is itself stale and is corrected under GM62-F07 in the
W224 section below.

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
window = the collision bar only, 2000-01-01T00:12:00Z                       Design section 12, "remainder. `RULE2-06-GREEN` uses `execution_profile_id=raw_close_only_v1` and"
F0 TARGET-NEAR: fee_notional abs(105*1*1) = 105 ; fee 0.04725 ; delta -0.04725
F1 TARGET-FAR : fee_notional abs(110*1*1) = 110 ; fee 0.049499999999999995 (R-0.3 n=110)
in-window cash_events (Design section 3, "on an exit, append gross" step 11, fee then gross per exit fill):
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
window = 2000-01-01T00:12:00Z only                                          Design section 12, "execution_profile_id=raw_close_only_v1` and the same position"
F0 TARGET-FAR and F1 TARGET-NEAR: fee_notional abs(105*1*1) = 105 each ; fee 0.04725 each
in-window cash_events = [ FEE(F0) -0.04725, GROSS(F0) +5, FEE(F1) -0.04725, GROSS(F1) +5 ]
pre-window entry fee 0.09 -> equity_curve = { first 999.91, last 1009.8155 }
trade row: gross 10, fee_total -0.1845, funding_total 0, net 9.8155
```

The not-runnable-on-legacy fact is recorded in the artifact (`legacy_arm_construction`) and in the
catalog row, and as **V15-D04**; the `1.0.0` expected artifact stays `OUT-OF-LANE` as before.

### R-14 RULE2-07-RED

v1.5 `Design section 22.6, "MARKET_EXIT/TIME_STOP/time_stop"` binds the bar series `[INIT98, ENTRY100, (00:12:00Z, 2, 100, 100, 100, 100, 0)]`,
`initial_capital=1000`, fallback `10%`, tick/step/minima `1/1/0/0`, `cm=1`, no SL/TP,
`use_time_stop=true`, `time_stop_bars=1`, `time_stop_condition="Always"`, the exact `GUARD07` switch
set (`Design section 22.2, "use_consecutive_loss_halt=true"`), and the corrected exit naming.

```
entry: fallback_notional 1000 * 10% = 100 ; raw_qty 100/100 = 1 ; qty 1    (matches the sealed 1)
time_stop_bars 1 -> the position closes on the next bar at close 100       (matches the sealed 100)
corrected event class / exit id / reason = MARKET_EXIT / TIME_STOP / time_stop      Design section 13, "is `-0.2`, and corrected equity"
lifecycle id starts at 1                                                            Design section 13, "100`, each derived fee cash"
fee event timestamps = 2000-01-01T00:11:00Z (F0) and 2000-01-01T00:12:00Z (F1)   [Design section 22.6, "plus exact `GUARD07`. | The", Design section 22.2, "0)`. | One first bar"]
settlement_currency = TEST-USD                                                      Design section 13, "event, and test rounding rule"
schedule_id = SYNTH-COST-RULE2-07-RED-V1                                            Design section 13, "0`, no funding event, and"
taker rate stays the section-13 stated 0.001                                        Design section 13, "rate `0.001`, fixed component `0"
```

Filled: `fill_events/1/event_class`, a new `fill_events/1/exit_id`, `fee_events/1/event_class`,
both `fee_events/*/event_timestamp`, both `fee_events/*/lifecycle_id`, both
`fee_events/*/schedule_id`, both `fee_events/*/settlement_currency`, `exit_events/0/exit_id`,
`exit_events/0/reason`, and the four record-identity cells. **D-05 is closed for RULE2-07-RED.**
Every economic value — rate `0.001`, `fee_notional 100`, `fee_amount 0.1`, `fee_cash_delta -0.1`,
gross `0`, `net_trade_pnl -0.2`, equity `1000 -> 999.8`, and all six guard nodes — is byte-identical.

### R-15 RULE2-07-GREEN

`Design section 22.6, "section-13 test values, with C"` supplies the non-empty but no-signal LEGACY input (`[NO_ACTION100]`, `initial_capital=1000`,
`use_time_stop=false`, exact `GUARD07`) that realizes design `Design section 12, "zero-impact model/parameter record, and policy"`'s "empty fill-event input"
without a state-injection field. No fill exists, so no fee and no equity movement: every already
sealed value stands. Filled: the four record-identity cells only.

### R-16 RULE2-08-RED

Owner addendum 20 (4a) binds the pre-event entry basis/fill to `100` via the `:888` candidate
prefix `[(1999-12-31T23:58:00Z,0,98,98,98,98,0),(1999-12-31T23:59:00Z,1,100,100,100,100,0)]` with
`initial_capital=1000`, fallback `10%`, tick/step/minima `.01/1/0/0`, `cm=1`, no SL/TP.

```
fallback_notional 1000 * 10% = 100 ; raw_qty 100/100 = 1 ; qty 1   -> the stated open_qty 1
final_position.entry_fill_price = 100                              [addendum 20 (4a)]
window = [2000-01-01T00:00:00Z, 2000-01-01T00:01:00Z]              Design section 14, "does not state the GREEN"  -> the prefix fill is
  OUTSIDE the compared surface, so fill_events stays A:0 and equity_curve.first stays 1000
C is absent / NOT_CONSUMED                                         [Design section 22.6, "fallback `10%`, `max_leverage_cap=10`, tick/step/minima `.01/1/0/0"; Design section 14, "no funding cashflow and remains"]
position_snapshot_rule = END_OF_INTERVAL_INCLUDE_SAME_TIMESTAMP_V1 Design section 14, "uses `execution_profile_id=close_only_deterministic_v2`, lifecycle id `1"
schedule_id = SYNTH-FUNDING-RULE2-08-V1 (shared with GREEN)        Design section 14, "snapshot rule and initial equity"
```

The funding arithmetic is unchanged and re-verified: `notional = abs(100 * 1 * 1) = 100`,
`long_cashflow_rate = -0.001`, `funding_cash_delta = 100 * (-0.001) * (+1) = -0.1`,
`equity 1000 + (-0.1) = 999.9` (§0.6 already proved both tokens exact).

`mark_price_source = "SPOT_ORACLE"` is a member of the schedule's event object (`Design section 22.3, "and LONG-pays-positive convention, and contains"`), not of
the design `Design section 14, "are read from the frozen"` `funding_events[]` row field list, so it is **not** added as a surface node.

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
| `BLOCKED-MISSING-RECORD-BYTES` | every `instrument_record_digest`, `instrument_source_document_digest`, `cost_schedule_digest`, `funding_schedule_digest`, `fee_events/*/schedule_digest`, `funding_events/0/schedule_digest`, `funding_events/0/source_event_digest`, and `PROBE-P012-03-A`'s first changed node | `Design section 22.1, "input digests are lower-case SHA-256"` keeps digests build artifacts; `Design section 22.3, "exactly `captured_at_utc`, `extraction_method`, `human_reviewer`, `owner_decision_ref"` refuses to fabricate `captured_at_utc` / `human_reviewer`; the canonical-JSON rule does not fix separators or indentation, so the hashed byte string is still undetermined (**V15-D05**) |
| `BLOCKED-DESIGN-UNENUMERATED` | every `/RESULT_SURFACE/metrics`; the complete `decision_events` vocabulary in all 17 artifacts | §22 binds inputs only; it enumerates no metric node set and no reason vocabulary |
| `BLOCKED-BUILD-ARTIFACT` | all 27 catalog `input.digest` values; probe modified-copy and modification-manifest digests | unchanged; the Lead pins these later. **No input path or input digest field was touched by this lane.** |
| `BLOCKED-MISSING-SCENARIO-INPUT` | `RULE2-08-GREEN` `observation_window.end_timestamp` only | `Design section 22.6, "but its closing evaluation bar"` declares no closing evaluation bar and addendum 20 (5a) names none |

Measured over the two expected surfaces of all 17 golden artifacts (walked structurally, counting
leaf string values equal to a marker, so `v15_filled_cells.old_marker` bookkeeping is excluded):
**`BLOCKED-MISSING-SCENARIO-INPUT` = 0**, `BLOCKED-MISSING-RECORD-BYTES` = 81 (every one a digest),
`BLOCKED-DESIGN-UNENUMERATED` = 17 (one `/RESULT_SURFACE/metrics` per artifact; the
`decision_events`-vocabulary block is a `blocked_cells` note, not a surface value). The single
remaining `BLOCKED-MISSING-SCENARIO-INPUT` in the bundle is
`RULE2-08-GREEN` `/observation_window/end_timestamp`, an authoring member outside both surfaces.

### R-19 `PROBE-P012-07-A` — `D-16` closed by §22.3

The probe classifies one declared taker exit as maker. `D-16` recorded that the outcome was
underivable because the RULE2-07 vector stated no maker rate. Design `Design section 22.3, "`maker_rate=0.00015`,"` now binds
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
  pre-window fills for both RULE2-08 rows, while design `Design section 22.6, "equity AMENDMENT-CHOICE. RULE2-08-GREEN row: C"` binds `C` as absent /
  `NOT_CONSUMED` and `Design section 14, "is false. The design does"` still asserts that "neither vector contains a fill intent". Design
  `Design section 5.1, "endings, and a required final LF. Its"` refuses a fill whose `CostSchedule` is missing. The conflict does not reach the compared
  surface (both windows start after those fills, so no in-window fill exists and no fee is
  charged), and no sealed value depends on it — but the input materializer must resolve it before
  a run, because a strict reading of `Design section 5.1, "The run manifest pins both"` would refuse the pre-window entry outright.
- **V15-D02** — no `equity_curve` scoping rule. §22 gives four rows an evaluation-only observation
  window that excludes their setup fills, but the design fixes nothing about whether
  `equity_curve.first`/`last` are run-scoped or window-scoped. This revision uses the window-scoped
  reading because it is the only one that satisfies the `Design section 2.1, "equal the joined cash row's signed"` invariant
  (`last = first + sum(in-window cash deltas)`) and because it reproduces every already-sealed
  `first = 1000`. `net_trade_pnl` and `fee_total` remain lifecycle-scoped per `Design section 13, "gross realized PnL plus every"` and therefore
  include a pre-window entry fee that the in-window `cash_events` container does not carry. Owner
  or §16 confirmation is requested.
- **V15-D03** — universal `CostSchedule` versus GREEN equality. §22.3 binds a non-zero taker rate
  for *every* scenario, including GREEN rows, while `1.0.0` has no fee model at all (`Design section 13, "has no fee ledger"`).
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
  `RULE2-02-RED`'s cost/funding schedule identities (which §22.4 `Design section 22.4, ", restating section 8"` does bind and which this
  revision fills), and it does not name `PROBE-P012-07-A`'s `D-16` closure (R-19). Both were found
  by checking the list against this worksheet rather than trusting it, as the lane requires.

- **V15-D07** — `IMPLEMENTATION_ANCHOR_DRAFT.json` violates the bundle's own serialization rule.
  Byte-inspected this session: 2827 bytes, **34 CR bytes (CRLF line endings) and no final LF**,
  against design `Design section 15.3, "a present non-integer/misaligned sequence, or"`'s UTF-8 / LF / required-final-LF rule. The lane spec forbids this lane from
  touching that file, so it was left exactly as found and is **not** listed in the manifest's
  `files` array, which means the manifest's `byte_discipline` sentence remains true as written.
  Raised for the Lead, who owns that file.
  **RE-MEASURED AND CORRECTED BY LANE W172 under G83-F05.** The 2827-byte / 34-CR / no-final-LF
  measurement above describes the file as it stood at lane W156; it is **false against the file on
  disk now**. Measured this session by byte inspection of
  `C:\tmp\P012_CONTRACT_TABLES_W127\IMPLEMENTATION_ANCHOR_DRAFT.json`: SHA-256
  `97a3c196323c08e2cf796f31569b396a5b8f886d0b347e3855984b8b9baab0f4`, **3268 bytes, 0 CR bytes, no
  BOM, final LF present**. The file therefore now CONFORMS to design `Design section 15.3, "LF line endings, and a required final LF. Parsing"`, and V15-D07 as a
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

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** In the paragraph above, "no
corrected-kernel source exists" is false at the current build and is withdrawn; every other claim in
R-21 stands, including that this revision verifies no implementation and that no `observed/` path was
read. The measurement, and the true replacement wording, are
recorded once at this worksheet's section-0 independence fence, in the W359 marker there.

---

## v1.8 revision

**Lane:** W167 (`C:\tmp\LANE_PROMPTS_20260828\LANE_W167_TABLES_V18.md`). Same author family and the
same independence fence as the rest of this worksheet: no `mtc_v2.core` import, no `observed/` path,
no implementer-authored input file, no kernel executed. Every value below is obtained by written
arithmetic or by literal member-set reconciliation from the design text and the owner decision file
alone. Where the two disagree with an earlier section of this worksheet, this section governs.

**Design under revision:** `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`, version **v1.8**
(title Design section 23.6, "23.6 v1.8 change log — terminal"; v1.8 change log `Design section 23.6, "23.6 v1.8 change log — terminal"`). File length **1273 lines**, final LF present.

### W-0 Line-number verification and the revision fence

The v1.8 file appends **§23** and changes nothing before it. Verified by re-reading the heading line
numbers rather than trusting the change log: `## 22.` is still at `Design section 22, "v1.5 input-embedding addendum"`, `### 22.8` at `Design section 22.8, "[OPEN-EMBED]"`, the
v1.5 change log at `Design v1.5 change log, "v1.5 change log — input-embedding addendum"`, and `## 23.` begins at `Design section 23, "v1.8 terminal micro-fold"` and runs to the end of the file. Every v1.5
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

**Scope fence.** Design `Design section 23.5, "must re-derive only these golden"` limits the tables family to seven numbered golden-node classes
and then re-seal by the Lead. This lane changed only those classes. It did **not** touch
`scenario_catalog.json`, any catalog `input.digest`, `IMPLEMENTATION_ANCHOR_DRAFT.json`, or the
manifest's `seal` / `seal_state` blocks. `CONTRACT_TABLES_MANIFEST.json` was edited in exactly two
respects, both stated in `revision_history`: the `files[]` `sha256`/`bytes` entries of the files this
lane actually revised, and the `design` version/line-span block. Design `Design section 23.5, "authority for this lane to"` is the KERNEL delta
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
| `kernel_semantics_version` on every member of all six containers | **FORCED** by §4's every-event identity rule | `Design section 4, "Version appears in every event"`, `Design section 23.1, "requires `kernel_semantics_version`"` |
| No `lifecycle_id` on a `decision_events` member | **FORCED** — lifecycle joins live on the typed economic/position projections | `Design section 23.1, "`lifecycle_id` is not a `decision_events` member"` |
| `MIN_NOTIONAL_ADMITTED` / `REFUSED_MIN_NOTIONAL` payload `{order_notional, required_min_notional}` | **FORCED** by §8's `admit iff order_notional >= min_notional` | `Design section 23.1, "Section 8's `admit iff order_notional >= min_notional`"` |
| `INSTRUMENT_RECORD_VALIDATED` / `REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION` payload `{field, record_value, runtime_value}` | **FORCED** by §§5.2 and 9 | `Design section 23.1, "Sections 5.2 and 9 typed pre-evaluation refusal"` |
| Fill common 14-member set; exit common 8-member set; conditional `exit_id` / `fill_trigger` / `target_fraction` / `reference_quantity`; `unrounded_fill_price` FORBIDDEN | **FORCED** (CLOSED) by §§2.1, 3, 4, 10-13 | `Design section 23.3, "Every `fill_events[]` member has exactly these common members"`, `Design section 23.3, "Every `exit_events[]` member has exactly"` |
| `max_consecutive_losses` forbidden on RESULT | **FORCED** — it is an M-09 configuration input | `Design section 23.4, "`max_consecutive_losses` is an M-09 configuration"` |
| Guard basis `GROSS-MINUS-FEES` on all three named controls | **FORCED** by owner addendum 15 item 35 | `Design section 23.4, "time-stop guards as `GROSS-MINUS-FEES`"` |
| Refusal `order_notional` replacing `observed_notional` | **FORCED** — §8 names `order_notional` | `Design section 23.4, "Section 8 names `order_notional`, so the prior `observed_notional` spelling is replaced"` |
| Flat decision rows, no `details` wrapper | `AMENDMENT-CHOICE` | `Design section 23.1, "A `details` wrapper is forbidden"` |
| `SIZING_COMPUTED` spelling and its one-row fold | `AMENDMENT-CHOICE` (third form; §§3 and 7 force the facts, not the spelling) | `Design section 23.1, "one third-form terminal reason carries the computed sizing facts"`, `Design section 23.1, "one third-form terminal reason carries the section-7 computed facts"`, `Design section 23.1, "`SIZING_COMPUTED`, flat"` |
| `MIN_NOTIONAL_ADMITTED` completed-state spelling | `AMENDMENT-CHOICE` | `Design section 23.1, "use a completed-state reason rather than the prior imperative spelling"` |
| `PROTECTIVE_STOP_EVALUATED` spelling and the omission of bar OHLC | `AMENDMENT-CHOICE` | `Design section 23.1, "completed-evaluation spelling carries the minimal outcome and omits bar OHLC"` |
| One `COLLISION_RESOLVED` spelling; `collision` present on the sole-class receipt rather than varying the closed member set | `AMENDMENT-CHOICE` (the boolean **domain** and content rule are forced by §12) | `Design section 23.1, "one terminal resolution spelling carries that receipt"`, `Design section 23.1, "the boolean remains present on the sole-class receipt"` |
| **`FUNDING_ELIGIBILITY` as the reason spelling, one reason for eligible and skipped alike** | `AMENDMENT-CHOICE` — §14 forces event-time eligibility and its boolean terminal disposition, **not** this name | `Design section 23.1, "Section 14 forces event-time eligibility and its boolean terminal disposition"`, `Design section 23.1, "use one `FUNDING_ELIGIBILITY` reason for both eligible and skipped dispositions"`, `Design section 23.1, "`eligible=false` represents a skipped tick"`, `Design section 23.1, "does not name a decision-reason spelling"` |
| Omitting `SLIPPAGE_RESOLVED`, `FEE_SCHEDULE_RESOLVED`, `GUARD_BASIS_RESOLVED`, `MARKET_EXIT_SELECTED` | `AMENDMENT-CHOICE` | `Design section 23.1, "use one compared node for each fact"` |
| Window-scoped `equity_curve.first`/`last`; run-scoped endpoints ABSENT | `AMENDMENT-CHOICE` — §§2.1, 15.3 and M-06 force neither reading | `Design section 23.2, "none chooses run-scoped versus window-scoped endpoints"`, `Design section 23.2, "none chooses run-scoped versus window-scoped endpoints"` |
| `price_tick_alignment` spelling | `AMENDMENT-CHOICE` | `Design section 23.3, "price_tick_alignment` is an `AMENDMENT-CHOICE` spelling"` |
| RESULT base spellings `trades` / `warnings` / `refusals` etc. | `AMENDMENT-CHOICE` where §15.3 states only the category | `Design section 22.6, "EXACT_IDENTITY_V1` rounding, zero fixed/minimum, and"`, `Design section 23.1, "target prices require the `exit_id"` |
| Positive `admitted` boolean retained | `AMENDMENT-CHOICE` | `Design section 23.4, "but is silent about RESULT-member"` |
| **`cumulative_funding` unconditional on both DEF-P012-08 RESULT rows** | `AMENDMENT-CHOICE` — §14 names cumulative funding but is silent on member presence when nothing is eligible | `Design section 23.4, "but is silent about RESULT-member"`, `Design section 23.5, "collision` object from every DEF-P012-06"`, `Design section 23.6, "the closed decision row is"` |
| Top-level `collision` object forbidden; the decision row is the single receipt | `AMENDMENT-CHOICE` | `Design section 23.4, "funding but is silent about"`, `Design section 23.6, "the closed decision row is"` |
| `funding_included_in_guard_basis` forbidden | `AMENDMENT-CHOICE` (disposes G76-05c as *not a comparison node*) | `Design section 23.4, "funding but is silent about"` |

No value in this bundle is presented as design-forced where the design labels it a choice.

### W-2 Item 1 — `decision_events` on all 17 scenarios

**The mapping actually executed.** Design `Design section 23.5, "23.1's independence table, removing"` (the DS35-F03 repair) tells the tables family
to reconcile *its own* prior reasons through the §23.1 independence table `Design section 23.1, "branch. `AMENDMENT-CHOICE`: one third-form terminal reason carries the computed"`, removing only
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

`SEMANTICS_VALIDATED` stays on 03-RED: `Design section 23.1, "refusal still produces its typed"` excepts only a *preflight*-refused scenario, and
`Design section 23.1, "refusal still produces its typed"` states that a pre-evaluation refusal still produces its typed refusal reason. 03-RED produces
a scenario output carrying that refusal, so it is not preflight-refused; the design's own preflight
case is `PROBE-P012-03-A`, which refuses before any scenario output exists (design `Design section 8, "Fail probe `PROBE-P012-02-A`: change the"`).

**Per-reason timestamps.** `Design section 22.2, "of the bar that supplies"`: `REQUIRED` means the timestamp of the `MarketEvent` or
funding event being evaluated under M-06; `FORBIDDEN` means absent, not null. The evaluated event per
row is fixed by §22:

```
01-*, 02-*, 05-*, 07-RED entry decisions -> ENTRY100  = 2000-01-01T00:11:00Z   [Design section 22.2, "already-stated reference/final entry `100`; no" M-04]
04-RED / 04-GREEN stop evaluation        -> eval bar  = 2000-01-01T00:13:00Z   Design section 22.5, "from `M-08` except `use_break_even=true`, `be_trigger_r=1"
06-RED / 06-GREEN / 06-EQUAL collision   -> eval bar  = 2000-01-01T00:12:00Z   Design section 22.5, "from `M-08` except `use_break_even=true`, `be_trigger_r=1"
08-RED / 08-GREEN funding eligibility    -> TEST-FUND-1 = 2000-01-01T00:00:00Z [Design section 22.6, "with `initial_capital=1000`, fallback `10%`, `max_leverage_cap=10", Design section 22.6, "with `initial_capital=1000`, fallback `10%`, `max_leverage_cap=10"]
03-RED / 03-GREEN record decisions       -> FORBIDDEN (performed before event evaluation) Design section 23.1, "and the section-9 GREEN case"
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
design `Design section 13, "execution_profile_id=close_only_deterministic_v2` and initial equity `1000"` still requires to be true.

**04-GREEN's null.** `Design section 23.1, "held by the digest-bound `MarketEvent"` closes GM28-F05: `reference_source` and `reference_price` are both
present **iff** a fill reference was selected, and both absent if neither predicate triggers. The
sealed `"reference_source": null` was therefore a wrong tagged state under `Design section 15.3, "ordered containers: `decision_events`, `fill_events`, `cash_events"` (null and absent
are different nodes) and is removed, not re-valued. This is the only sealed *node kind* this item
corrected.

**Row-set reading.** See discrepancy **W167-D04**: §23.1 `Design section 23.1, "when their named decision is actually evaluated"` also carries a general
occurrence rule, which read on its own would add further rows. This lane executed item 1's
reconciliation mapping, which is the tables-family instruction, and recorded the alternative.

### W-3 Item 2 — section-4 identity on every event member

`Design section 23.1, "there is no event-container"` and `Design section 23.5, "including the section-13 fee and section-14"`: every member of `decision_events`, `fill_events`, `cash_events`,
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

`Design section 23.2, "not run-scoped equity and not mark-to-market equity"` now fixes the rule the `## v1.5 revision` section had to record as missing (**V15-D02**):
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
**All ten tokens are byte-identical to the v1.5 seal.** Design `Design section 23.5, "after re-derivation; prior authorship is"` warns that prior authorship is
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
                     consecutive_loss_count 1          [Design section 13, "enables only the consecutive-loss guard": the closed lifecycle is a loss
                                                        on the gross-minus-fees basis]
                     consec_loss_ok false, guard_blocked_raw true
                                                       [Design section 13, "D017's gross-minus-fees interim basis": count < max is 1 < 1 = false]
          every remaining value byte-identical.
07-GREEN  remove max_consecutive_losses
          remaining: GROSS_MINUS_FEES, count 0, consec_loss_ok true, guard_blocked_raw false
          last_closed_guard_pnl stays ABSENT - no lifecycle closes (Design section 13, "so its count becomes `1", Design section 22.6, "per the §14 RED equity") and
          Design section 23.4, "guard_pnl_basis, consecutive_loss_count, consec_loss_ok, guard_blocked_raw" requires absent, not zero or null. Values byte-identical.
08-RED    remove funding_included_in_guard_basis   [Design section 23.4, "as **not a comparison node" disposes G76-05c as NOT a
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
          [GUARD CENSUS SUPERSEDED BY LANE W200 under design v1.9 item 9; marker added by lane
           W205 under G103-F01 and G103-F02. Two things in the block above stopped being current.
           (a) TOKEN, on the two RULE2-07 lines: "guard_pnl_basis GROSS_MINUS_FEES" (07-RED) and
               "remaining: GROSS_MINUS_FEES" (07-GREEN) spell the basis with underscores. Design
               v1.9 Design section 23.4, "time-stop guards as `GROSS-MINUS-FEES`, with" fixes the hyphenated GROSS-MINUS-FEES and design v1.9 section 23.5
               item 9 (Design section 23.4, "time-stop guards as `GROSS-MINUS-FEES`, with") directed the change; lane W200 made it. Both goldens now read
               "GROSS-MINUS-FEES" (RULE2-07-RED.json:54, RULE2-07-GREEN.json:38). SPELLING ONLY -
               every RULE2-07 guard fact listed above (last_closed_guard_pnl -0.2, count 1,
               consec_loss_ok false, guard_blocked_raw true on RED; count 0, true, false and
               last_closed_guard_pnl ABSENT on GREEN) is unchanged and still current.
           (b) OBJECT, the whole 08-RED sub-block: design v1.9 section 23.5 item 9 (Design v1.9 section 23.4, "guard_pnl_basis, consecutive_loss_count, consec_loss_ok, guard_blocked_raw")
               directed removal of the RULE2-08-RED guards object unless a separate owner-approved
               scenario-input amendment binds its threshold and requires re-derivation. No such
               amendment exists and lane W200 removed the object. RULE2-08-RED now carries no
               guards member of any kind - its RESULT_SURFACE keys are final_position, trades,
               equity_curve, cumulative_funding, metrics, warnings, refusals, run_manifest
               (RULE2-08-RED.json:40-59). The 08-RED lines above naming guard_pnl_basis,
               consecutive_loss_count, last_closed_guard_pnl and the two
               BLOCKED-MISSING-SCENARIO-INPUT cells describe the pre-W200 artifact and were
               correct when written. Current state: RULE2-08-RED.json:93 (the removal record) and
               W200 W-3 (DERIVATIONS.md:2933-2968). W167-D01, named on the last line above,
               is NOT closed by the removal; it is relocated into the absence of the object.
           NO VALUE MOVED by either change - W200 W-2 (DERIVATIONS.md:2911-2925) and W-3
           (DERIVATIONS.md:2963-2968).
           G103-F02 named the 08-RED lines only; the two RULE2-07 token lines above are the same
           residue in the same block and are marked here rather than left.]
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
                               (GAP_OPEN, design-named at Design section 10, "price, gross PnL, cash/equity, exit"). ADDED to 06-GREEN's stop fill and to
                               its exit row, where it was missing. Absent on every entry, target and
                               market-exit fill (07-RED's MARKET_EXIT row checked explicitly).
target_fraction /              required only on TARGET_EXIT: present on the four target fills of
reference_quantity             06-RED and 06-EQUAL, absent on every stop, entry and market-exit fill.
exit_events.fill_trigger       re-derived: required on 04-RED (GAP_OPEN) and on 06-GREEN's
                               PROTECTIVE_STOP exit; absent on the four TARGET exits and on 07-RED's
                               time-stop market exit.
```

06-GREEN's added value is derived from the section-10 table (`Design section 10, "at close `92`; the OPEN-06-contingent"`): long, `open 100 <= stop 90`
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

**ROW SUPERSEDED BY LANE W200 under design v1.9 item 9; marker added by lane W224 under
GM62-F06.** The `08-RED` row of the table above still reads `guards` **`yes`**. Design **v1.9**
section 23.5 item 9 (`Design section 23.4, "supplies that input member only"`) directs removal of the `RULE2-08-RED` `guards` object "unless a
separate owner-approved scenario-input amendment binds its threshold and requires re-derivation";
no such amendment exists and lane W200 removed the object - see W200 W-3, the section
"W-3 `RULE2-08-RED` - the directed removal of the `guards` object" below. That row's
`RESULT_SURFACE` now carries exactly eight keys - `final_position`, `trades`, `equity_curve`,
`cumulative_funding`, `metrics`, `warnings`, `refusals`, `run_manifest` (`RULE2-08-RED.json:40-59`)
- and **no guard node of any kind**; the removal record is at `RULE2-08-RED.json:93`. The
`07-RED / 07-GREEN` row's `guards` **`yes`** immediately above it is **unchanged and still
current**, as is `08-RED`'s `cumulative_funding` **`-0.1`** in the same row. Lane W205 marked the
three other sites G103-F01 named; this table is the site it missed, and GM62-F06 named it. **NO
VALUE MOVED.**

**ROW SUPERSEDED BY LANE W186 under owner addendum 28 decision 68; marker added by lane W224 under
GM62-F04.** The `05-RED / 05-GREEN` row of the same table reads `order_notional` **`101 / 100`**.
`RULE2-05-RED`'s `order_notional` is now `0` (`RULE2-05-RED.json:43`, before/after at
`RULE2-05-RED.json:91`) under owner addendum 28 decision 68; `RULE2-05-GREEN`'s `100` is unchanged.
The finding the row carries - that `order_notional` is **retained** as a top-level member on
DEF-P012-05 - is unchanged and still current, and so is the paragraph below the table; only the
`101` half of that one value cell is superseded. GM62-F04 named R-0.4, R-9 and the Y-1 table; this
cell is the same residue in the same class and is marked here rather than left. **NO VALUE MOVED.**

`order_notional` is retained on exactly DEF-P012-01, DEF-P012-02 and DEF-P012-05 and is absent from
RULE2-04/06/07/08, as `Design section 23.4, "entry-sizing/notional projection | Sections 7-8 and"` requires — note that 07-RED's entry *does* have a notional of
`1 * 100 * 1 = 100`, and `Design section 23.4, "entry-sizing/notional projection | Sections 7-8 and"` expressly refuses to make a generic kernel-computed
`order_notional` a node of a scenario whose design projection does not name it.

`cumulative_funding` is now **unconditional** on both DEF-P012-08 rows (`Design section 23.4, "DEF-P012-02, or DEF-P012-05 declares the"`, `Design section 23.6, "DEF-P012-08 RESULT rows as the"`). Both
were already present — `-0.1` on 08-RED and `0` on 08-GREEN — so the micro-fold confirms them rather
than changing them, and the tables list and the kernel list now agree. The design labels the
unconditional presence an `AMENDMENT-CHOICE`, not a forced identity (`Design section 23.4, "the kernel already share, while"`, `Design section 23.6, "rows as the minimal fixed shape; tables"`).

The three removed `collision` objects carried `is_pessimistic` and `ambiguity_record` members that
§12 never enumerated; `Design section 23.4, "is the single receipt and avoids duplicating an unenumerated object."` makes the closed `COLLISION_RESOLVED` decision the single receipt.
Nothing those objects carried is lost: `collision`, `same_bar_collision_policy_id` and
`ordered_chosen_exit_ids` are all members of the decision row, and the policy id is additionally on
`run_manifest`, whose internal members §23 does not close.

### W-8 Item 7 — refusal objects

`Design section 23.4, "the prior `observed_notional` spelling is"`. `RULE2-02-RED`'s refusal member `observed_notional` is **renamed** `order_notional`,
giving the closed triple `{code, order_notional, required_min_notional}` = `{REFUSED_MIN_NOTIONAL,
100, 101}`; the design says the prior spelling is replaced rather than canonized because §8 names
`order_notional`. `RULE2-03-RED`'s refusal was re-checked against the five-member tagged object
`{code, field, record_value, runtime_value, stage="PRE_EVALUATION"}` and already conformed exactly,
with no free-form `detail`; **no byte of it changed**. No other artifact has a `refusals[]` member.

### W-9 What is still blocked after v1.8

| Marker | Count over the two surfaces | Where | Why v1.8 does not close it |
|---|---|---|---|
| `BLOCKED-MISSING-RECORD-BYTES` | 81 | every `*_record_digest`, `*_schedule_digest`, `instrument_source_document_digest`, `source_event_digest` | unchanged: `Design section 22.1, ". These are the existing"` keeps digests `MECHANICAL` build artifacts, `Design section 22.3, "values stated in §14 and"` refuses to fabricate `captured_at_utc` / `human_reviewer`, and the canonical-JSON rule still fixes no separator or indentation width (**V15-D05**) |
| `BLOCKED-DESIGN-UNENUMERATED` | 17 | one `/RESULT_SURFACE/metrics` per artifact | `Design section 23.1, "rule and receipt table force"` states in terms that this amendment "does not un-block design-unenumerated metrics" |
| `BLOCKED-MISSING-SCENARIO-INPUT` | 2 | `RULE2-08-RED` `/RESULT_SURFACE/guards/consec_loss_ok` and `/guard_blocked_raw` | **new**: §23.4 newly requires four guard members while §22.6 binds no guard configuration for RULE2-08 (**W167-D01**) |
| `BLOCKED-BUILD-ARTIFACT` | 0 on these surfaces | catalog `input.digest`, probe copies | untouched by this lane |

**ROW SUPERSEDED BY LANE W200 under design v1.9 item 9; marker added by lane W205 under G103-F01.**
The `BLOCKED-MISSING-SCENARIO-INPUT` row of the table above (`DERIVATIONS.md:2049`) locates its
two cells at `RULE2-08-RED` `/RESULT_SURFACE/guards/consec_loss_ok` and `/guard_blocked_raw`.
**Those two pointers no longer exist.** Design **v1.9** section 23.5 item 9 (`Design section 23.4, "guard_pnl_basis, consecutive_loss_count, consec_loss_ok, guard_blocked_raw"`) directed
removal of the whole `RULE2-08-RED` `guards` object and lane W200 removed it (W-3,
`DERIVATIONS.md:2933-2968`); the artifact's own `blocked_cells` ledger lost the two matching
rows in the same act, eight entries down to six (`RULE2-08-RED.json:94`; the six that remain are at
`RULE2-08-RED.json:104-109`). The count `2` in the row above, and the same v1.8 counts restated at
`DERIVATIONS.md:2074-2076`, are the census **as measured for v1.8** and are left exactly as
measured. This lane measured no replacement count and states none: a surface-restricted structural
walk over all 17 artifacts is a re-measurement act, not a residue marker, and no number in this
worksheet was moved to place this marker. **W167-D01**, the design gap that forced the two markers
in the first place, is **not closed** by the removal - it is relocated into the absence of the
object (`RULE2-08-RED.json:93`). The other three rows of the table, and the `RULE2-08-GREEN`
`/observation_window/end_timestamp` sentence below, are untouched by W200. **NO VALUE MOVED.**

**The `decision_events` vocabulary block is CLOSED.** All 17 artifacts previously carried a
`blocked_cells` entry reading "the design fixes no complete `decision_events` reason vocabulary";
§23.1 now enumerates nine closed reasons with exact per-reason member sets, so that entry is removed
from all 17. That is the only entry removed. Design `Design section 23.1, "decision_events` closed shape and reason"` confirms the amendment closes the
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
  `Design section 22.6, "00Z`. F contains exactly"` makes `consec_loss_ok` and `guard_blocked_raw` required members of a present `guards`
  object, and `Design section 23.4, "guard_pnl_basis, consecutive_loss_count, consec_loss_ok, guard_blocked_raw"` names `RULE2-08-RED` for guard re-derivation. The guard predicate is
  `count < max_consecutive_losses` (design `Design section 13, "so its count becomes `1"`). `consecutive_loss_count = 0` is derivable, but
  §22.6 `Design section 22.6, "to the existing sealed RULE2-07-RED"` binds no guard switch and no maximum for either RULE2-08 row, and only RULE2-07 binds
  `GUARD07` / `max_consecutive_losses = 1` (M-09 `Design section 22.2, "states only the consecutive-loss guard"`). Design `Design section 22.1, "both cost members are JSON"` states that another
  scenario's value is not authority, so this lane refused to borrow RULE2-07's maximum and marked
  both cells `BLOCKED-MISSING-SCENARIO-INPUT`. Under any `max_consecutive_losses >= 1` the values
  would be `true` and `false`; the design binds no such value here. **Owner or §16 resolution
  requested**, or an input-embedding binding for RULE2-08's guard switches.
- **W167-D02** — closed member presence, open value domain. §23.3 makes `fill_trigger` REQUIRED on
  every `PROTECTIVE_STOP_EXIT` fill and its exit row, but the design names only the `GAP_OPEN` token
  (`Design section 10, "reference/final price, gross PnL, cash/equity"`); it enumerates no token for section 10's other long branch (`low <= stop`, reference =
  `stop`). The same holds for `PROTECTIVE_STOP_EVALUATED`'s `predicate` and `reference_source` values
  and for the `selector`, `target_ordering_rule` and `price_tick_alignment` values. This lane
  authored `STOP_TOUCH` for the non-gap trigger and kept the pre-existing `OPEN_BEYOND_STOP`,
  `NO_TOUCH`, `BAR_OPEN`, `RISK`, `FALLBACK`, `LONG_ASCENDING_TARGET_PRICE`,
  `LONG_ASCENDING_TARGET_PRICE_THEN_EXIT_ID_UTF8_BYTE_ORDER`, `CEIL` and `FLOOR` spellings. These are
  tables-authored strings in the sense of **D-13**, and every "first changed node" whose value they
  are depends on them. v1.8 closed the member sets but not these domains.
- **W167-D03** — §23.2 versus `RULE2-08-GREEN`'s unnamed pre-window bars. `:1063` makes pre-window
  gross realizations affect `equity_curve.first`. Owner addendum 20 (5a) places lifecycle 1 opening
  and closing on ordinary bars before the window but names none of them, and §22.6 `Design section 22.6, "its closing evaluation bar and premise are not declared reachable"` declares
  no closing evaluation bar. `first = 1000` is derivable only under the premise that the pre-window
  round trip realizes zero gross PnL and consumes no cost schedule — which is the only reading
  consistent with design `Design section 13, "legacy has no v2 net"` fixing that row's compared cash/equity projection at `1000` and with
  `Design section 22.6, "is 1000 → 999.9 (fee) → 999.8"` binding `C` as absent / `NOT_CONSUMED`. The premise is stated in the artifact and the
  token is unchanged; the design does not state it directly.
- **W167-D04** — two readings of which rows carry which reason. §23.1 `Design section 23.1, "total order when their named"` states a general
  occurrence rule ("emitted ... when their named decision is actually evaluated"), while §23.5 item 1
  `Design section 23.5, "reasons through section 23.1's"` instructs the tables family to reconcile *its prior reasons* through the independence
  table, and the occurrence sentence recurs only in the **KERNEL** delta list (`Design section 23.5, "reasons through section 23.1's"`, "emit a
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
  `fallback_notional 100 / (final fill 101 * cm 1) = 0.990099`, and `qty_step = 1` (`Design section 22.5, "requested qty is explicitly `1"`) floors it
  to `0`. §11 `Design section 11, "is `100`, corrected fill is"` and §22.5 `Design section 22.5, "corrected requested qty is explicitly"` instead declare requested quantity `1`, which is what the
  bundle seals, together with `order_notional 101`. The two cannot both hold. This is why no
  `SIZING_COMPUTED` row was authored for either RULE2-05 row even under the W167-D04 alternative
  reading: the row's `selector` and `order_notional` members cannot be filled without choosing
  between §7 and §11. Recorded, not resolved; no sealed value was changed.
  **NARROWED BY LANE W172 under G83-F03: W167-D05 is real on `RULE2-05-RED` ONLY.** The sentence
  above over-extended it to `RULE2-05-GREEN`. On GREEN the reference and final entry fill are both
  `100` (`slippage_bps = 0`, design `Design section 11, "fill is `100`, corrected fill"`, `Design section 22.5, "qty `1` at reference `100"`), so §7's fallback path gives
  `100 / (100 * 1) = 1`, `qty_step = 1` floors it to `1`, and `order_notional = 1 * 100 * 1 = 100` -
  which agrees with §11 `Design section 11, "fill `101`; legacy fill is"`'s declared requested quantity `1` and with the sealed
  `/RESULT_SURFACE/order_notional 100`. There is no §7-versus-§11 conflict on GREEN, so
  `SIZING_COMPUTED` **is** derivable there and lane W172 authored it under Reading Y. D05 continues
  to block `SIZING_COMPUTED` on `RULE2-05-RED` alone, where the final fill is `101` and the two
  sections give `0` and `1`.
  **RESOLVED by owner addendum 28 decision 68, 2026-09-01 (`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:571`):
  SECTION 7 GOVERNS, quantity ZERO.** Lane W186 re-derived `RULE2-05-RED` under that word, authored
  the withheld `SIZING_COMPUTED` row, and moved four economic values. See section
  "W186 owner addendum 28 decision 68 re-derivation — `RULE2-05-RED`" below. W167-D05 is closed.
- **W167-D06** — the manifest `seal` / `seal_state` blocks are now stale by construction. This lane
  revised 18 files and updated their `files[]` digests as the lane spec directs, but `EXPECTED_SEAL_SHA`
  is the Lead's act and was deliberately left untouched, so it no longer covers the current bytes.
  Design `Design section 23.5, "these golden nodes, then the"` puts the re-seal with the Lead. Flagged so no reader mistakes the recorded seal
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
remains excluded from that reviewer role because it authored these tables. Design `Design section 23.1, "fills, or PnL. `AMENDMENT-CHOICE`: one"` still
governs the claim: this amendment makes the named schema classes design-computable; it does not claim
the present goldens or kernel conform, does not un-block design-unenumerated metrics, does not change
any economic vector, and grants no build, execution, re-seal, deployment or trading authority.

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** In the paragraph above, "no
corrected-kernel source exists" is false at the current build and is withdrawn; every other claim in
W-11 stands, including that no economic vector value moved. The measurement, and the true replacement wording, are
recorded once at this worksheet's section-0 independence fence, in the W359 marker there.

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
`Design section 23.1, "require the `exit_id` UTF-8 byte-order"` applies to the tables family on its own terms. The anti-padding half of that sentence
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
   containers (design `Design section 22.5, ". | If both opens approve"`, `Design section 22.5, ". | If both opens approve"`, `Design section 22.6, "with `initial_capital=1000`, fallback `10%`, `max_leverage_cap=10`, tick/step/minima `.01/1/0/0"`). A sizing or admission predicate evaluated on an
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

Design `Design section 3, "min_notional` checks using final fill"` (section 3 step 8) applies the `min_notional` check to every fill-producing entry;
design `Design section 8, "passes because the legacy comparison"` (section 8) makes it `admit iff order_notional >= min_notional`, with `Design section 8, "passes because the legacy comparison"`
stating that equality passes because the legacy comparison is strict `<`. Members are fixed at
`Design section 22.2, "fixes event placement without changing"`: `event_timestamp` REQUIRED, plus `order_notional` and `required_min_notional`. Placement is
after `SIZING_COMPUTED` where that row exists, because section 3 orders sizing at step 7 and
admission at step 8 and the independence row `Design section 23.1, "but no reason spelling. `selector"` states that section 8 makes admission a
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
`Design section 22.2, "bar_index,open,high,low,close,volume)`."`, which design `Design section 22.4, "is `MECHANICAL`; economic values and"` states replaces the same member of the InstrumentRecord. Every
comparison admits. **No economic value moved.**

**VALUES SUPERSEDED BY LANE W186 under owner addendum 28 decision 68; marker added by lane W224
under GM62-F04.** The `RULE2-05-RED` line of the Y-1 fence above reads `101  = 1*101*1` with
sequence `1`, and the paragraph above restates that `101` as the artifact's "already-sealed value
byte for byte" - the third of the four figures it lists. **That value moved, and so did the
sequence.** Owner addendum 28 decision 68 ruled that design section 7 governs `RULE2-05-RED` and
its quantity is ZERO, so `order_notional = 0 * 101 * 1 = 0`; lane W186 additionally authored the
`SIZING_COMPUTED` row lane W172 had withheld, which pushed `MIN_NOTIONAL_ADMITTED` from sequence
`1` to sequence `2`. The current bytes are `{"sequence": 2, "decision": "MIN_NOTIONAL_ADMITTED",
... "order_notional": 0, "required_min_notional": 0}` (`RULE2-05-RED.json:27`), with the golden's
own before/after record at `RULE2-05-RED.json:99`. **What still stands:** `required_min_notional 0`,
the admitting comparison - which now reads `0 >= 0` and still admits - and every other line of the
fence: `RULE2-01-RED 1000`, `RULE2-01-GREEN 100`, `RULE2-05-GREEN 100` and `RULE2-07-RED 100` are
unchanged and still current, as are the `1000`, `100` and `100` the paragraph lists beside the
`101`. W186 already recorded this at Y-2 below - "The Y-1 table line `RULE2-05-RED 101 = 1*101*1`
and this paragraph both describe the pre-ruling artifact" - but placed no marker at the site;
GM62-F04 named the site and this marker closes it. **NO VALUE MOVED.**

`RULE2-01-RED` sizing check (already in W-2, repeated because Y-1 depends on it): risk_amount
`1000 * 10% = 100`; stop distance `|100 - 90| = 10`; `risk_raw_qty = 100 / (10 * 2) = 5`;
`leverage_cap_qty = (1000 * 10) / (100 * 2) = 50`; `min(5, 50) = 5`; `qty_step 1` floors to `5`;
`order_notional = 5 * 100 * 2 = 1000`.

`/RESULT_SURFACE/admitted` was **not** added anywhere. Design `Design section 23.4, "in admission | Section 8 GREEN"` scopes that RESULT member to
the DEF-P012-02 minimum-notional predicate, so it stays on `RULE2-02-GREEN` alone. The decision row
and the RESULT boolean are different nodes with different conditions.

### Y-2 `SIZING_COMPUTED` additions

Members at `Design section 22.2, "their reference price. | This fixes"`: `event_timestamp` REQUIRED, `selector`, `contract_multiplier`,
`order_notional`. Section 7 `Design section 6, "nodes remain version-specific and are"` supplies the arithmetic; section 3 steps 7-8 `Design section 3, "fill-producing intent, `CorrectedEconomicsAdapter` performs this"` supply
the placement.

**`RULE2-05-GREEN`** - design `Design section 22.5, "qty is explicitly `1`; C"` inherits the RED config with `slippage_bps = 0`, so the final
entry fill is the reference `100` (`Design section 11, "fill is `100`, corrected fill"`). `initial_capital = 1000` (OPEN-EMBED-01, owner addendum
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

`qty 1` and `order_notional 100` are the sealed values. The §7 result agrees with §11 `Design section 11, ", and requested quantity "`, so
**W167-D05 does not arise on GREEN** (G83-F03, folded at the W167-D05 entry above).

**`RULE2-07-RED`** - design `Design section 22.6, "0,98,98,98,98,0),(1999-12-31T23"` binds `initial_capital = 1000`, fallback `10%`,
`max_leverage_cap = 10`, `tick/step/minima 1/1/0/0`, `multiplier 1`, no SL/TP; design `Design section 11, "corrected fill is `101`."` states
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

The `FALLBACK` token is **design-named** at `Design section 22.7, "records only the `FALLBACK` decision"` ("Expected/observed JSON records only the
`FALLBACK` decision"). Only `RISK` is a tables-authored spelling; see Y-5. G83-F06's table lists
`RISK / FALLBACK` together as authored - verified this session, that half of its row is wrong.

**`RULE2-05-RED` - `SIZING_COMPUTED` DELIBERATELY WITHHELD.** W167-D05 is real on this row: §7
sizes from the **final** fill `101`, giving `100 / (101 * 1) = 0.990099...` which `qty_step 1`
floors to `0`, against §11 `Design section 11, ", and requested quantity "` and `Design section 22.5, "corrected requested qty is explicitly"` declaring requested quantity `1` and the sealed
`order_notional 101`. The row's `selector` and `order_notional` members cannot both be filled
without choosing between the two sections, so no row was authored and the omission is recorded on
the artifact in `w172_revised_nodes`. This is the lane spec's binding exception and G83's finding
alike. The `MIN_NOTIONAL_ADMITTED` row that WAS added there restates the artifact's own
already-sealed `order_notional 101` - the whole artifact is already derived on the §11 branch
(final_position quantity `1`, fill quantity `1`) - and does **not** resolve D05.

**SUPERSEDED by lane W186 under owner addendum 28 decision 68:** section 7 governs and the quantity
is zero, so `SIZING_COMPUTED` is derivable on `RULE2-05-RED` after all and was authored with
`selector FALLBACK`, `contract_multiplier 1`, `order_notional 0`. `MIN_NOTIONAL_ADMITTED` moved to
sequence `2` and its `order_notional` to `0`. The Y-1 table line
`RULE2-05-RED 101 = 1*101*1` and this paragraph both describe the pre-ruling artifact.

### Y-3 `PROTECTIVE_STOP_EVALUATED` additions on the three RULE2-06 rows

Members at `:1022`: `event_timestamp` REQUIRED, `position_side`, `stop_price`, `predicate`; plus
`reference_source` and `reference_price` **iff a fill reference was selected**.

*Why the decision is evaluated.* Section 3 step 2 `Design section 3, "but do not choose a"` says that for exits the adapter records
which stop and targets touched, before choosing any winner or reference. Design `Design section 12, "close=95`; only the stop touches"` states in
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
(`Design section 23.1, "equal target prices require the"`).

*Predicate.* Section 10's table `Design section 10, "Either | neither predicate | no stop"`, long rows:

```
row            evaluation OHLC (o/h/l/c)   open <= stop 90   otherwise low <= stop 90   branch
06-RED         100/115/85/105              100 <= 90 FALSE   85 <= 90 TRUE              row 2
06-GREEN       100/104/85/95               100 <= 90 FALSE   85 <= 90 TRUE              row 2
06-EQUAL       100/115/85/105              100 <= 90 FALSE   85 <= 90 TRUE              row 2
```

Bars from design `Design section 12, "all touch. Legacy's implicit"` and `Design section 22.5, "M-08` except `use_break_even=true`, `be_trigger_r=1`, `be_buffer_r=0"`. `stop_price 90` is the stated scenario input (`Design section 12, "all touch. Legacy's implicit"`;
`Design section 22.5, "use_break_even=true`, `be_trigger_r=1`, `be_buffer_r=0`, plus `tp_mode="` reaches it through `sl_percent 10` on entry `100`). `position_side` is `LONG` (`Design section 12, "leaving no stop remainder. `RULE2-06-GREEN"`).
`event_timestamp` is the evaluation bar `2000-01-01T00:12:00Z` (`Design section 22.5, "use_break_even=true`, `be_trigger_r=1`, `be_buffer_r=0`, plus `tp_mode="`, M-06 `Design section 22.2, "high,low,close,volume)`."`).

*Reference members.*

- `06-GREEN`: **present**. The stop is the sole touched class, `Design section 12, "touches, so both versions choose"` states both versions fill the
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
Section 3 step 1 `Design section 3, "Validate exact semantic-version and immutable-record"` validates immutable-record identities on every run, and `Design section 22.4, "instrument field is explicit and"` states that
every other LEGACY runtime instrument field is explicit and exactly equal to the record. Read at its
widest, Reading Y might place this reason on all 17. It was **not** added, for a payload reason
rather than an occurrence reason: `Design section 23.1, "INSTRUMENT_RECORD_VALIDATED` | `FORBIDDEN` | `field`, `record_value`, `runtime_value` | Section 5.2"` fixes the members as the single triple
`{field, record_value, runtime_value}`, and the design names a compared field for exactly one
correction - DEF-P012-03's `price_tick` (`Design section 8, "admission projection and requires as"`, `Design section 22.4, "other runtime instrument fields equal"`). For any other row the design neither
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
FALLBACK                                                  1  (Design section 22.7, "it selects fallback sizing. The")             DESIGN-NAMED
GAP_OPEN                                                  1  (Design section 10, "reference/final price, gross PnL, cash/equity")             DESIGN-NAMED
GROSS-MINUS-FEES                                          3  (Design section 23.4, "time-stop guards as `GROSS-MINUS-FEES`, with" etc)        DESIGN-NAMED
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
because it is evidence and not authority: (a) `FALLBACK` is design-named at `Design section 22.7, "22.7 RULE2-01-GREEN NaN wire contract"`, so only `RISK`
of that pair is authored; (b) G83's table stops at seven token families, while the inventory also
finds `BUY` / `SELL`, `LONG`, the three `cash_events.kind` tokens and the underscore form of
`GROSS_MINUS_FEES` - all now labeled, so the fix does not leave a residue of the same class.

**Deliberately NOT labeled, and why, so the omission is recorded rather than absorbed:** the
identity strings `F0` / `F1`, `CE-FEE-0` / `CE-FEE-1` / `CE-GROSS-0` / `CE-GROSS-1` / `CE-FUND-0`,
and the `SYNTH-...-V1` record ids. Those are `MECHANICAL` identity strings under §22.1 `Design section 22.1, "no independent economic content. It fixes the strict input envelope"`
and §22.3 `Design section 22.3, "SYNTH-{INSTRUMENT|COST|FUNDING}-<scenario_id>-V1"`, not value-domain spellings of an economic fact; §22.3 `Design section 22.3, "SYNTH-{INSTRUMENT|COST|FUNDING}-<scenario_id>-V1"` fixes the
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
                 funding_included_in_guard_basis as a live false fact; Design section 22.6, "999.9 (fee) → 999.8 (funding) per" and
                 Design section 23.4, "The section-22.1 closed envelope supplies" removed that member from the artifact.
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
  design `Design section 23.4, "DEF-P012-02, or DEF-P012-05 declares the"` keeps the RESULT member `order_notional` on DEF-P012-01/02/05 only and `Design section 23.4, "DEF-P012-02, or DEF-P012-05 declares the"`
  expressly refuses to make "a generic kernel-computed `order_notional` a node of a scenario whose
  design projection does not name it". The two are different member sets in different subsections
  and do not contradict each other, but the design does show §23.4 declining to serialize a
  computed-but-undeclared fact in the very case Reading Y now serializes in §23.1. Flagged so the
  Lead and §16 see the consequence rather than discovering it at the gate. No value moved either
  way.
- **W172-D02 - Reading Y required two more tables-authored value tokens.** `LOW_TOUCH` (the
  `predicate` for section 10's second long branch) and `STOP_LEVEL` (the `reference_source` for that
  branch's stop-level reference) are authored spellings. The design enumerates both the branch
  (`Design section 10, "Legacy fills at close `92"`) and the reference-source domain (`Design section 3, "reference, gap/open stop reference, stop"` - "entry reference, gap/open stop reference,
  stop level, target level, or market-exit close"), so the **facts** are design-forced and closed;
  only the strings are this family's. This is the same gap W167 recorded as W167-D02 when it
  authored `STOP_TOUCH` for the identical branch, and it is the reason W167 gave for not executing
  Reading Y. The tokens are labeled on their artifacts under Y-5. An owner or §16 ruling that
  authored value spellings must be design-enumerated before seal would reopen every "first changed
  node" whose value they are, `GAP_OPEN` excepted.
- **W172-D03 - `INSTRUMENT_RECORD_VALIDATED` occurrence is undecidable under Reading Y.** See Y-4.
  Section 3 step 1 validates record identities on every run, but `Design section 23.1, "INSTRUMENT_RECORD_VALIDATED` | `FORBIDDEN` | `field`, `record_value`, `runtime_value"`'s closed triple names one
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

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** Two assertions in the paragraph
above are false at the current build and are withdrawn: the *exists* arm of "no kernel, adapter,
driver, gate, backtest, verifier, generator or baseline exists or was executed", and "a kernel that
does not exist" in the sentence beginning "Reading Y is an owner ruling on a schema question". Only the *exists* arm is withdrawn; the *was executed* arm stands - this lane
executed no kernel, adapter, driver, gate, backtest, verifier, generator or baseline.
The surviving true statement is the intended one: this revision **does not claim that the goldens
conform to the kernel**, and nothing here compares them to it. The measurement, and the true replacement wording, are
recorded once at this worksheet's section-0 independence fence, in the W359 marker there.

## W186 owner addendum 28 decision 68 re-derivation — `RULE2-05-RED`

### Z-0 The ruling and its exact scope

Owner addendum 28, decision 68, 2026-09-01, verbatim in the repository at
`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:571`:

> "(68) RULE2-05-RED: SECTION 7 GOVERNS, quantity ZERO - the sealed golden currently carries the
> section-11 outcome and must be re-derived by the tables family under this word, the only authority
> that may change a sealed golden."

That resolves discrepancy **W167-D05** (`DERIVATIONS.md:2040-2056`), which recorded that design
section 7 `Design section 7, "position quantity, and any quantity-derived"` sizes `RULE2-05-RED` from the **final** entry fill `101` and floors to `0`,
while design section 11 `Design section 11, "legacy fill is `100`, corrected"` and section 22.5 `Design section 22.5, "entry TAKER `0.00045`; F empty."` declare requested quantity `1`. Lane W172
withheld `SIZING_COMPUTED` on this row rather than choose (`DERIVATIONS.md:2208-2216`). The owner has
now chosen. The ruling names one row and one branch; sections 11 and 22.5 keep every other value they
supply to this scenario (reference `100`, `slippage_bps 100`, impact `1`, final fill `101`, tick
`0.01`, `contract_multiplier 1`, fee rate `0.00045`), and this lane changed nothing outside
`RULE2-05-RED`.

**POINTERS SUPERSEDED BY LANE W205's line insertions; markers added by lane W224 under GM62-F07.**
Both citations in the paragraph above are pre-W205 numbering and are **left intact**. Measured this
session against the current bytes: `DERIVATIONS.md:2040-2056` (the **W167-D05** record) is now
`DERIVATIONS.md:2240-2256`, and `DERIVATIONS.md:2208-2216` (lane W172's withheld-`SIZING_COMPUTED`
record) is now `DERIVATIONS.md:2429-2437`. The second is **not** the `:2295-2303` that W205's V-3
table computed for it: that column applied V-3's uniform `+87` shift to W186's own number, and
W186's number was already four lines low, so the mechanical result lands on the `FALLBACK`
paragraph rather than on the withheld-row record. Both records still exist, unmoved and unedited;
only the numbers naming them changed. Neither citation was rewritten - this worksheet is
append-only and one lane does not edit another lane's record to match a later state. **NO VALUE
MOVED.** Full index in section U-2 below.

### Z-1 The governing arithmetic, written out

Inputs, each with the design line that supplies it:

```
sizing_equity        = 1000        OPEN-EMBED-01 closed 1a by owner addendum 20 item 49; the
                                   binding is recorded on this artifact's open_item_bindings
                                   and Design section 22.5, "1`; C has `slippage_bps=100`, entry" leaves initial_capital as [OPEN-EMBED-01]
fallback_size_pct    = 10          Design section 22.5, "reference `100`; corrected requested qty"  ("fallback_size_pct=10")
max_leverage_cap     = 10          Design section 22.5, "reference `100`; corrected requested qty"
qty_step             = 1           Design section 22.5, "at reference `100`; corrected requested" tick/step/minima .01/1/0/0 under M-08 Design section 22.2, "use_break_even=false`, `use_trailing=false`. `percent stop"
min_qty              = 0           Design section 22.5, "at reference `100`; corrected requested" under M-08 Design section 22.2, "use_break_even=false`, `use_trailing=false`. `percent stop"
min_notional         = 0           Design section 22.5, "qty `2`, stop `90`, targets" under M-08 Design section 22.2, "no SL/TP` means `use_sl=false`, `tp_mode="
cm                   = 1           Design section 22.5, "tp1_r_multiple=.5`, `tp1_close_pct=50`, `tp2_r_multiple=1`. | Real" ("instrument_contract_multiplier=1"); also Design section 22.3, "records by reference (`SYNTH-COST-RULE2-07-RED-V1` and"
stop_price           = absent      Design section 22.5, "instrument_contract_multiplier=1`, no SL/TP." ("no SL/TP") means use_sl=false under M-08 Design section 22.2, "no SL/TP` means `use_sl=false`"
reference_price      = 100         Design section 11, "with reference `100`, `slippage_bps=100`", supplied by the ENTRY100 bar close at M-04 Design section 22.2, "whose close supplies the already-stated reference/final entry `100`"
slippage_bps         = 100         Design section 11, "with reference `100`, `slippage_bps=100`", Design section 22.5, "C has `slippage_bps=100`"
price_tick           = 0.01        Design section 11, "reference `100`, `slippage_bps=100`, `price_tick=0.01`", Design section 22.5, "tick/step/minima `.01/1/0/0`, `instrument_contract_multiplier=1`, no SL/TP"
```

Section 11 `Design section 11, "fields; changes entry price, entry-relative"` first fixes the final entry fill; that value is unchanged by the ruling and is
restated here because section 7 `Design section 7, "required quantities are legacy `10"` divides by it:

```
impact         = abs(100) * 100 / 10_000 = 1                         (:304)
unrounded_fill = 100 + 1 = 101              (buy)                    (:305)
final_fill     = ceil_to_price_tick(101) = 101   (tick 0.01)         (:307)
```

Section 3 `Design section 3, "the final fill, then size"` places sizing after the final fill is known: "For an entry, construct any
entry-relative stop from the final fill, then size from final fill and final stop" / "Floor quantity
to `qty_step`". Section 7 `Design section 6, "nodes remain version-specific and are"` then gives, term by term:

```
fallback_notional = sizing_equity * (fallback_size_pct / 100)
                  = 1000 * (10 / 100) = 100                          (:195)

selector          = FALLBACK
                    stop_price is absent, and Design section 7, "stop leaves quantity at zero." select fallback_raw_qty on that branch;
                    Design section 7, "stop leaves quantity at zero." restates it ("An absent or supplied non-finite stop selects fallback
                    sizing"). The token FALLBACK is design-named at Design section 22.7, "absent stop node, preserving section".

fallback_raw_qty  = fallback_notional / (final_entry_fill * cm)
                  = 100 / (101 * 1)
                  = 100 / 101
                  = 0.990099009900990099...                          (:196)

selected_raw_qty  = fallback_raw_qty = 0.990099...                   (:198)

leverage_cap_qty  = (sizing_equity * max_leverage_cap) / (final_entry_fill * cm)
                  = (1000 * 10) / (101 * 1)
                  = 10000 / 101
                  = 99.009900990099...                               (:206)

raw_qty           = min(0.990099..., 99.009900...) = 0.990099...     (:207)

qty               = floor_to_qty_step(0.990099..., step 1) = 0       (:208)

order_notional    = qty * final_entry_fill * cm = 0 * 101 * 1 = 0    (:209)
```

The floor is exact and needs no binary64 case analysis: `100 / 101` is strictly greater than `0` and
strictly less than `1`, so flooring to a step of `1` gives `0` under any rounding of the quotient.
`10000 / 101` is greater than `1`, so the leverage cap is not binding and does not change the result.

This is the same arithmetic the withheld-row record already carried at `DERIVATIONS.md:2208-2211`;
the ruling changes which of the two sections the artifact seals, not the computation.

**POINTER SUPERSEDED BY LANE W205's line insertions; marker added by lane W224 under GM62-F07.**
The citation above is pre-W205 numbering and is **left intact**. `DERIVATIONS.md:2208-2211` - the
arithmetic the withheld-row record carried - is now `DERIVATIONS.md:2429-2432`, measured this
session. W205's V-3 table computed `:2295-2298` for it by applying a uniform `+87` shift to W186's
own number, which was already four lines low; see the marker in Z-0 above. **NO VALUE MOVED.**

### Z-2 Section 8 admission still holds

Design `Design section 3, "min_notional` checks using final fill"` applies the `min_notional` check to the fill-producing entry, and `Design section 8, "order_notional = floored_qty * final_entry_fill * contract_multiplier"` gives
`order_notional = floored_qty * final_entry_fill * contract_multiplier` and
`admit iff order_notional >= min_notional`:

```
order_notional        = 0 * 101 * 1 = 0                              (:233)
required_min_notional = 0                                            (:870 under M-08 :736)
admit iff 0 >= 0  ->  TRUE                                           (:234)
```

`:237` states that equality passes "because the legacy comparison is strict `<`". So
`MIN_NOTIONAL_ADMITTED` survives on this row; only its `order_notional` member moves, from `101` to
`0`, and its `sequence` moves from `1` to `2` because a `SIZING_COMPUTED` row now precedes it
(`Design section 23.1, "Section 8 makes admission a"` section-3 order; `Design section 23.1, "Section 8 makes admission a"` "section 8 makes admission a separate predicate after sizing").

### Z-3 The withheld row CAN now be filled

**Yes.** `SIZING_COMPUTED` is added at sequence `1`. Its member set is closed at `:1017`:
`event_timestamp` REQUIRED, plus `selector`, `contract_multiplier`, `order_notional`, on top of the
common `sequence`, `decision`, `kernel_semantics_version` at `:994`.

```
sequence                 = 1                       (Design section 3, "performs this total order" section-3 order: step 1 validation,
                                                    then steps 7-8 sizing, then step 8 admission)
decision                 = SIZING_COMPUTED         (Design section 22.2, "timestamp,bar_index,open,high,low")
kernel_semantics_version = "2.0.0"                 (Design section 23.1, "no reason spelling. `selector` has", Design section 23.1, "no reason spelling. `selector` has")
event_timestamp          = 2000-01-01T00:11:00Z    (M-04 Design section 22.2, "98` initializes the line and" gives ENTRY100's timestamp;
                                                    M-06 Design section 22.2, "98` initializes the line and" puts the corrected event at the bar
                                                    that supplies its reference price)
selector                 = FALLBACK                (Design section 7, "its cataloged input bytes/digest, multiplier", Design section 7, "its cataloged input bytes/digest, multiplier"; token design-named at Design section 22.7, "3. Supplies the resulting quiet")
contract_multiplier      = 1                       (Design section 22.5, "the section-12 stated `TARGET-FAR=105`, `TARGET-NEAR=105", Design section 22.3, "An InstrumentRecord contains exactly `contract_multiplier")
order_notional           = 0                       (Design section 7, "is `fallback_notional / entry`; neither", Z-1 above)
```

Every member of the payload is now derivable, and each is derived above from a quoted design line.
Exactly what blocked the row — the choice between `selector`/`order_notional` under section 7 and
under section 11 — is what the owner ruled. Nothing else about the row was blocked, so nothing else
holds it back.

One naming limit, carried forward unchanged from lane W172 rather than newly incurred here: the
`FALLBACK` token is design-named at `Design section 22.7, "22.7 RULE2-01-GREEN NaN wire contract"`, but that sentence sits inside section 22.7, whose subject
is the `RULE2-01-GREEN` NaN wire. It is the design's only spelling of the section-7 fallback branch,
and lane W172 used it on `RULE2-05-GREEN` and `RULE2-07-RED` on that basis (`DERIVATIONS.md:2204-2206`).
This lane uses it identically. Recorded as **W186-D03**.

**POINTER SUPERSEDED BY LANE W205's line insertions; marker added by lane W224 under GM62-F07.**
The citation above is pre-W205 numbering and is **left intact**. `DERIVATIONS.md:2204-2206` - lane
W172's paragraph recording that the `FALLBACK` token is design-named at `Design section 22.7, "22.7 RULE2-01-GREEN NaN wire contract"` and used on
`RULE2-05-GREEN` and `RULE2-07-RED` on that basis - is now `DERIVATIONS.md:2425-2427`, measured
this session. W205's V-3 table computed `:2291-2293` for it, four lines low for the reason given in
the Z-0 marker above; that span is the tail of the preceding fence, not the paragraph W186 meant.
**W186-D03 is unaffected and remains open. NO VALUE MOVED.**

### Z-4 Values downstream of the quantity

Each node below is changed only where a quoted design line determines it from `qty = 0`.

**Fee, design section 13.** The row's `CostSchedule` members come from `Design section 22.3, "not production fee claims. Except"` (`fixed_component=0`,
`minimum_fee=0`, `fee_rounding_rule="EXACT_IDENTITY_V1"`) and `Design section 22.3, "not production fee claims. Except"` (`taker_rate=0.00045`, ENTRY maps
to TAKER); `Design section 13, "no funding event, and test"` defines the test rule as `round_and_apply_minimum(x)=x`.

```
fee_notional   = abs(final_fill_price * fill_qty * contract_multiplier)
               = abs(101 * 0 * 1) = 0                                (:360)
raw_fee        = fee_notional * selected_liquidity_rate + fixed_component
               = 0 * 0.00045 + 0 = 0                                 (:361)
fee_amount     = round_and_apply_minimum(0) = 0                      (:362, :800, :384)
fee_cash_delta = -fee_amount = 0                                     (:363)
```

`rate 0.00045`, `fixed_component 0`, `liquidity_role TAKER`, `settlement_currency TEST-USD`,
`schedule_id`, `lifecycle_id 1`, `fill_id F0`, `event_class ENTRY` and `event_timestamp` are
unchanged: none of them is a function of quantity.

**Cash ledger, design section 2.1.** `Design section 2.1, "signed delta must equal the"` requires the typed fee projection and its joined cash row
to carry equal signed deltas, and `Design section 13, "equality-checks `fee_cash_delta` and the joined"` repeats the equality check, so
`cash_events/0/signed_delta = 0`.

**Equity curve, design section 23.2.** `Design section 23.2, "first` plus, in section-3/array order"`: `last` is `first` plus every in-window
`cash_events` `signed_delta` in section-3/array order. The M-06 `Design section 22.2, "One first bar initializes Range"` window for this row is the full
bar span `2000-01-01T00:10:00Z .. 2000-01-01T00:11:00Z`, so the single fee cash row is in window:

```
equity_curve.first = 1000                                (window start is the account seed, R-0.4)
equity_curve.last  = 1000 + 0 = 1000                     (:1060-1061)
```

This endpoint is robust to the one open question in Z-6: if the design instead emitted no fill and
therefore no fee or cash row, `Design section 23.2, "last == first`. Pre-window"` says "With no in-window cash event, `last == first`", which is
`1000` as well. `last = 1000` holds on both readings.

**Position quantity, design section 7.** `Design section 7, "cash event. `RULE2-01-GREEN` uses `execution_profile_id=close_only_deterministic_v2"` names the projection set for a changed section-7
quantity: "Required changed projection: quantity, order notional, later position quantity, and any
quantity-derived cash event." `final_position.quantity` therefore follows the floored `0`.
`final_position.side LONG` and `final_position.entry_fill_price 101` are not quantity-derived —
`:275-280` / `:406` fix the long side and `:315` / `:307` fix the fill price — and are unchanged.

**RESULT `order_notional`.** `:209` and `:233` both give `0 * 101 * 1 = 0`. The member stays present:
`:1128` requires it exactly when DEF-P012-01/02/05 declares the entry-sizing/notional projection, and
this row owns DEF-P012-05.

### Z-5 Before/after, one line per changed node

```
pointer                                        before      after   forcing design line
/EVENT_SURFACE/decision_events/1               (absent)    row     Design section 23.1, "SIZING_COMPUTED` | `REQUIRED` | `selector`, `contract_multiplier`, `order_notional" SIZING_COMPUTED payload
/EVENT_SURFACE/decision_events/2.sequence      1           2       Design section 23.1, "SIZING_COMPUTED` | `REQUIRED` | `selector`, `contract_multiplier`, `order_notional", Design section 23.1, "SIZING_COMPUTED` | `REQUIRED` | `selector`, `contract_multiplier`, `order_notional"
/EVENT_SURFACE/decision_events/2.order_notional 101        0       Design section 8, "order_notional = floored_qty * final_entry_fill * contract_multiplier"
/EVENT_SURFACE/fill_events/0/quantity          1           0       Design section 7, "and fallback quantity is `fallback_notional"
/EVENT_SURFACE/cash_events/0/signed_delta      -0.04545    0       Design section 2.1, "tick-aligned price, quantity, liquidity role", Design section 13, "fee_notional = abs(final_fill_price * fill_qty"
/EVENT_SURFACE/fee_events/0/fee_notional       101         0       Design section 13, "fee_cash_delta = -fee_amount"
/EVENT_SURFACE/fee_events/0/fee_amount         0.04545     0       Design section 13, "fee_notional = abs(final_fill_price * fill_qty"
/EVENT_SURFACE/fee_events/0/fee_cash_delta     -0.04545    0       Design section 13, "fee_cash_delta = -fee_amount"
/RESULT_SURFACE/final_position/quantity        1           0       Design section 7, "Required changed projection: quantity"
/RESULT_SURFACE/order_notional                 101         0       Design section 7, "order_notional   = qty * final_entry_fill * cm", Design section 8, "order_notional = floored_qty * final_entry_fill * contract_multiplier"
/RESULT_SURFACE/equity_curve/last              999.95455   1000    Design section 23.2, "`last` is `first` plus"
```

`equity_curve.first`, every `run_manifest` member, every `blocked_cells` marker, `metrics`,
`trades`, `warnings`, `refusals`, the `EVENT_SURFACE` container set and every fill member other than
`quantity` are unchanged. `funding_events` and `exit_events` stay empty.

**FOUR ECONOMIC VALUES MOVED**, in contrast to the W167 and W172 revisions, which moved none:
`order_notional 101 -> 0`, `fee_amount 0.04545 -> 0` with its two joined deltas
`-0.04545 -> 0`, `equity_curve.last 999.95455 -> 1000`, and the quantity nodes
`1 -> 0`. Superseded binary64 token: R-0.4 `:1182` records `RULE2-05-RED 1000 - fl(0.04545) =
999.95455` at bits `0x408f3fa2eb1c432d`; under this ruling the accumulation is `1000 - 0 = 1000` and
that line no longer describes this row. R-9 `:1369-1380` is likewise superseded for its
`fee_notional`, `fee_amount`, delta and `equity_curve` values; its fill price `101` and impact `1`
stand.

**POINTERS SUPERSEDED BY LANE W205's line insertions; markers added by lane W224 under GM62-F07.**
The two internal pointers in the paragraph above are pre-W205 numbering and are **left intact**.
Measured this session: R-0.4's superseded accumulation line, cited as `:1182`, is now
`DERIVATIONS.md:1288`; section R-9, cited as `:1369-1380`, is now `DERIVATIONS.md:1486-1497`. Both
were accurate when W186 wrote them and both now carry an in-place W224 marker at the site. **W205's
V-3 census of "six pre-existing citations inside this file" did not count these two** - the true
count is eight, and V-3's own "Now at" column is superseded by measurement; see section U-2 below.
**NO VALUE MOVED.**

### Z-6 What the ruling does NOT determine — recorded, not filled

**W186-D01 — whether a zero-quantity entry still emits a fill, a fee row and a position.**
The ruling fixes the quantity. It does not say whether the corrected adapter emits
`fill_events/0`, `cash_events/0`, `fee_events/0` and a `final_position` at all once the floored
quantity is `0`. The design does not settle this either:

- `Design section 3, "quantity to `qty_step`; apply `min_qty"` (step 8) names a `min_qty` check but states **no predicate** for it. This row's `min_qty` is
  `0` (`Design section 22.5, "qty `1`, active stop `100"` under M-08 `Design section 22.2, "tuple order is `(timestamp,bar_index"`), so a `qty >= min_qty` reading admits and a `qty > min_qty` reading
  refuses. The design gives neither.
- `Design section 3, "for that fill; on an"` (steps 10-11) append the fill decision, its fill event and its fee cash event
  unconditionally once the step-8 checks pass.
- `Design section 13, "event, and test rounding rule"` charges a fee "For every executed entry or exit fill" without defining whether a
  zero-quantity fill is executed.
- `Design section 7, ". Required changed projection: quantity"` states the conditions that "return zero quantity" without stating what the transition then
  emits.
- The closed reason table `Design section 23.1, "The allowed `decision` values and their exact members"` contains no minimum-quantity or zero-quantity reason, and
  `Design section 23.1, "A reason not in this table requires a later"` says a reason not in that table requires a later schema amendment. The closed refusal-code
  table `Design section 23.4, "For the refusal codes exercised by the finite CORRECTED_V2 corpus"` likewise enumerates only `REFUSED_MIN_NOTIONAL` and
  `REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION`. Under the current closed schema nothing can refuse
  this row.

This lane therefore kept the container shape the artifact already sealed — one fill, one cash row,
one fee row, one `final_position` — and re-derived their values, because that is the reading the
closed schema can express and because deleting three containers would be a change made by inference,
which this lane is fenced from. The alternative reading (no fill, empty
`fill_events`/`cash_events`/`fee_events`, and some other `final_position`) is recorded here, not
chosen. `equity_curve.last = 1000` is identical under both readings; `final_position` is the one node
where they differ. **Owner or §16 resolution requested.**

**W186-D02 — signed zero on `fee_cash_delta`.**
`Design section 13, "fee_cash_delta = -fee_amount"` gives `fee_cash_delta = -fee_amount`. With `fee_amount = 0` the mathematical result is `0` and
the IEEE-754 binary64 result of negating `+0.0` is `-0.0`, a distinct bit pattern
(`0x8000000000000000` versus `0x0000000000000000`). The design fixes no signed-zero serialization
rule, and `Design section 23.4, "economic rule but does not"`-class node comparison under `Design section 15.3, "node; a token with a"` compares tokens. This lane writes `0`, matching
`cash_events/0/signed_delta` so the `Design section 2.1, "joined one-to-one by `cash_event_id`; the"` equality join holds token for token. The `-0` alternative
is recorded, not adopted.

**W186-D04 — the catalog's recorded expected-artifact digest is now stale.**
`scenario_catalog.json` pins `expected_artifacts["2.0.0"].digest` for `RULE2-05-RED` at
`a5962ccfed7b893d41ea2b2d43c1b2532328a9fb1eaea07b11f605a82c6cd7f9`, the pre-revision bytes. The lane
spec keeps the catalog untouched and puts re-sealing with the Lead, so this lane did **not** edit it.
Flagged so no reader mistakes the catalog row for a digest of the current bytes; the Lead must
refresh it with the new digest recorded in the W186 report. This is the same class as W167-D06 and
does not affect any expected value.

**W186-D05 — the prompt's premise, checked against the repository.**
The lane spec says the golden "withheld the affected value rather than guess". Verified and true for
`SIZING_COMPUTED` (`RULE2-05-RED.json` `w172_revised_nodes`, entry 2), but the artifact did **not**
withhold the quantity itself: it sealed the section-11 outcome (`quantity 1`, `order_notional 101`,
`fee 0.04545`, `equity 999.95455`) throughout, which is exactly what the owner's own wording at
`N_TIMES.txt:571` says ("the sealed golden currently carries the section-11 outcome"). The
repository and the owner agree; the lane spec's one-clause summary understated the reach. Recorded
under C-2 because it changed the size of the edit: this is a value re-derivation, not only the
filling of one withheld row.

### Z-7 The ruling does not spread — every other row re-checked

Item 4 of the lane spec requires that a change implied elsewhere be reported, not made. Nothing is
implied elsewhere. `RULE2-05-RED` is the **only** row in the corpus whose corrected final entry fill
differs from its reference price, because it is the only row with a non-zero `slippage_bps`
(`:315`, `:870`). Every other row that sizes an entry binds `slippage_bps=0` explicitly:
`RULE2-01-RED/GREEN` at `:216` and `:850-851`, `RULE2-02-RED/GREEN` at `:241` and `:852-853`,
`RULE2-03` at `:259` and `:854`, `RULE2-04-RED/GREEN` at `:287` and `:868-869`, `RULE2-05-GREEN` at
`:315` and `:871`, the `RULE2-06` family at `:872-874`, `RULE2-07-RED` at `:384` and `:886`; and
`RULE2-08-RED`'s `CostSchedule` is absent/`NOT_CONSUMED` at `:888`, with its entry basis and fill
bound to `100` by owner addendum 20 item 49 (4a). Sizing over a final fill above the reference is
precisely what pushes `fallback_notional / final_fill` below one step. Every other fill-producing
row, re-checked by hand this session against its own `:850-888` bindings:

```
row                    path      arithmetic                                    qty  sealed  moves?
RULE2-01-RED           risk      100 / (|100-90| * 2) = 5;  cap 50             5    5       no  (:216)
RULE2-01-GREEN         fallback  100 / (100 * 1) = 1;       cap 100            1    1       no  (:216)
RULE2-02-RED           risk      10 / (10 * 1) = 1;         cap 100            1    1       no  (:241)
RULE2-02-GREEN         risk      10 / (10 * 1) = 1;         cap 100            1    1       no  (:241)
RULE2-04-RED/GREEN     risk      10 / (|100-90| * 1) = 1;   cap 100            1    1       no  (:868)
RULE2-05-GREEN         fallback  100 / (100 * 1) = 1;       cap 100            1    1       no  (:871, Y-2)
RULE2-06-*             risk      20 / (|100-90| * 1) = 2;   cap 100            2    2       no  (:872-874)
RULE2-07-RED           fallback  100 / (100 * 1) = 1;       cap 100            1    1       no  (:886, Y-2)
RULE2-08-RED           fallback  100 / (100 * 1) = 1;       cap 100            1    1       no  (:888)
RULE2-03-RED/GREEN     none      NO_ACTION100; no intent, no fill              -    -       no  (:854-855)
RULE2-07-GREEN         none      no intent, no fill                            -    -       no  (:887)
RULE2-08-GREEN         none      premise blocked on OPEN-EMBED-05              -    -       no  (:889)
```

Every quotient above is an exact integer or larger than its step, so no floor moves. W172 had already
narrowed W167-D05 to `RULE2-05-RED` alone on the same ground (`DERIVATIONS.md:2048-2056`); this
session re-derived all twelve rows independently rather than inheriting that conclusion. **No other
scenario file was opened for writing and none was changed.**

**POINTER SUPERSEDED BY LANE W205's line insertions; marker added by lane W224 under GM62-F07.**
The citation above is pre-W205 numbering and is **left intact**. `DERIVATIONS.md:2048-2056` - lane
W172's **NARROWED BY LANE W172 under G83-F03** paragraph inside the W167-D05 record - is now
`DERIVATIONS.md:2248-2256`, measured this session. W205's V-3 table computed `:2135-2143` for it
and that mapping was correct in the pre-W224 bytes; the further shift is this lane's own
insertions, accounted for in section U-2 below. **NO VALUE MOVED.**

### Z-8 Honest limits of this re-derivation

One owner ruling applied to one row. No kernel, adapter, driver, gate, backtest, verifier, generator
or baseline exists or was executed; no `observed/` path was read; no implementer-authored input file
was consumed as an authority — every input value above is quoted from the design text, and the
`tests/.../inputs/RULE2-05-RED.json` bytes were not used to derive any value. Local SHA-256, a
structural JSON parse for byte discipline and duplicate-key equality, and written arithmetic over
this bundle's own files are the only computation performed. The ruling closes W167-D05 and opens
W186-D01 through W186-D05; it does not close W167-D01/D02/D03/D06, does not un-block
design-unenumerated metrics or the `BLOCKED-MISSING-RECORD-BYTES` digests, and grants no build,
execution, re-seal, deployment or trading authority. Re-sealing, and refreshing the stale catalog
digest under W186-D04, remain the Lead's acts under design `Design section 23.4, "record-lineage predicate remains outside what"`. The §16
`SEMANTIC_COVERAGE_REVIEW` remains owner-held and PENDING, and the claude family remains excluded
from that reviewer role because it authored these tables.

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** In the paragraph above, the
*exists* arm of "No kernel, adapter, driver, gate, backtest, verifier, generator or baseline exists or
was executed" is false at the current build and is withdrawn. Only the *exists* arm is withdrawn; the *was executed* arm stands - this lane
executed no kernel, adapter, driver, gate, backtest, verifier, generator or baseline. The measurement, and the true replacement wording, are
recorded once at this worksheet's section-0 independence fence, in the W359 marker there.

## W200 v1.9 `GOLDEN-OVER` repair — `RULE2-07-RED`, `RULE2-07-GREEN`, `RULE2-08-RED`

### W-0 What this lane is, and what it is not

Design **v1.9** is the authority for this section. The design file read for it is
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`, whose title line reads
`# WP-P0-12 CORRECTED_VNEXT Fresh-Family Design v1.9` (`Design v1.9 section 23.8, "11 per-token items, T1-T11, kept"`) and which is **1317 lines** long. Owner
addendum 28 decision 67 approved that text as drafted — verbatim at
`C:\tmp\LANE_PROMPTS_20260828\N_TIMES.txt:571`: *"(67) v1.9 TOKEN AMENDMENT APPROVED as drafted"*.

Section 23.5's tables-revision **item 9** at `Design section 23.5, "23.5 TABLES REVISION SCOPE and"` is therefore a direction already written
into an approved design. This lane **implements two clauses of that item and decides nothing**. It
adds no design name, chooses no value, and resolves no OPEN row.

Independence, stated as a fact rather than a promise: no `mtc_v2.core` import; no `observed/` path
read; no implementer-authored input file consumed as a derivation authority — the
`tests/corrected_vnext/contracts/inputs/**` bytes were not opened for any value here; no kernel,
driver, verifier, gate, generator, backtest or baseline exists or was executed. Local SHA-256, a
structural JSON parse with duplicate-key checking, a byte check for BOM/CR/final-LF, and literal
reconciliation against the design text are the whole of the computation performed.

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** In the paragraph above, the
*exists* arm of "no kernel, driver, verifier, gate, generator, backtest or baseline exists or was
executed" is false at the current build and is withdrawn. Only the *exists* arm is withdrawn; the *was executed* arm stands - this lane
executed no kernel, adapter, driver, gate, backtest, verifier, generator or baseline. The measurement, and the true replacement wording, are
recorded once at this worksheet's section-0 independence fence, in the W359 marker there.

### W-1 The two design passages, quoted from the file this lane read

**`Design section 23.4, "23.4 Closed `RESULT_SURFACE`, guards, and"`** (section 23.4, the guard-basis token):

```
`last_closed_guard_pnl` is additionally required exactly when a lifecycle closed and produced that
fact; it is absent, not zero or null, otherwise. `max_consecutive_losses` is an M-09 configuration
input, not a RESULT member, and is forbidden. Owner addendum 15 item 35 fixes the `2.0.0` basis for
daily-loss, consecutive-loss, and time-stop guards as `GROSS-MINUS-FEES`, with no per-control
divergence
```

The token the design fixes is **hyphenated**: `GROSS-MINUS-FEES`. The lane spec's summary of
`Design section 23.5, "23.5 TABLES REVISION SCOPE and"` is accurate; the sentence begins on `Design section 23.5, "23.5 TABLES REVISION SCOPE and"` and the citation closes on `Design section 23.5, "23.5 TABLES REVISION SCOPE and"`.

**`Design section 23.5, "23.5 TABLES REVISION SCOPE and"`** (section 23.5, tables-revision item 9):

```
9. **v1.9 design housekeeping for the four rejected table defects:** change the three inconsistent
   guard-basis values to section 23.4's `GROSS-MINUS-FEES`; use `null` for unavailable metrics in all
   17 goldens unless the owner separately chooses the `[]` alternative permitted by section 23.4;
   replace missing-record/source-byte digest placeholders with the actual lower-case SHA-256 values
   after canonical bytes exist; and remove the RULE2-08-RED `guards` object unless a separate
   owner-approved scenario-input amendment binds its threshold and requires re-derivation. Re-seal
   only in the later tables lane. These are housekeeping dispositions, not additional design names
```

Both directions the lane spec claims are present, in the exact words it claims. Item 9's other two
clauses — the `metrics` `null` change and the digest placeholders — are **out of this lane's scope**
and were not performed; they touch all 17 goldens and are named here only so their omission is a
recorded choice rather than an oversight.

`V19_TOKEN_AMENDMENT_PROPOSAL.md:373` and `:376`, the source item 9 cites at `:1235`, carry the same
two dispositions and name the exact byte positions:
`RULE2-07-GREEN.json:37`, `RULE2-07-RED.json:53`, `RULE2-08-RED.json:45` for the token, and
`RULE2-08-RED.json:47-48` for the removal.

### W-2 `RULE2-07-RED` and `RULE2-07-GREEN` — the guard-basis token

Reconciliation, not arithmetic: the design fixes a **token**, and the golden carried a different
serialization of the same token.

```
design text at Design section 23.5, "s `GROSS-MINUS-FEES`; use `null` for"        GROSS-MINUS-FEES      (hyphen, hyphen)
golden bytes before         GROSS_MINUS_FEES      (underscore, underscore)
golden bytes after          GROSS-MINUS-FEES      identical to the design token
```

The underscore form was never design-forced. Lane W172 had already labeled it as such under G83-F06:
each artifact's `authored_value_tokens` carried the statement *"the underscore spelling
GROSS_MINUS_FEES is this family's serialization of the design's hyphenated GROSS-MINUS-FEES"*, and
the W172 census at `DERIVATIONS.md:2316-2321` counted `GROSS-MINUS-FEES` as **DESIGN-NAMED** with 3
grep hits while listing `GROSS_MINUS_FEES (underscore form)` among the **TABLES-AUTHORED** tokens
with 0 hits. v1.9 item 9 now directs the family to stop serializing it differently. That labeled
entry has therefore been **removed** from `authored_value_tokens` on both rows: the value is now the
design's own token, so keeping it on a census of tables-authored spellings would assert the opposite
of the truth. `RULE2-07-GREEN`'s ledger held only that entry and is now the empty array `[]`; the key
is retained because design 15.3 `Design section 15.3, "nodes are emitted as `O"` counts missing, null and empty as three different states, and
an empty census is the true statement that the artifact carries no tables-authored token.

**POINTER SUPERSEDED BY LANE W205's line insertions; marker added by lane W224 under GM62-F07.**
The citation above is pre-W205 numbering and is **left intact**. `DERIVATIONS.md:2316-2321` - the
Y-5 token census rows that count `GROSS-MINUS-FEES` as DESIGN-NAMED and list
`GROSS_MINUS_FEES (underscore form)` as TABLES-AUTHORED - is now `DERIVATIONS.md:2533-2538`,
measured this session. W205's V-3 table computed `:2403-2408` for it and that mapping was correct
in the pre-W224 bytes; the further shift is this lane's own insertions, accounted for in section
U-2 below. The same span is cited from outside this file at `W200_GOLDEN_OVER_REPORT.md:69`, which
is a dated lane report and outside this lane's write scope. **NO VALUE MOVED.**

**No economic value moved on either row.** The basis names the same economic rule under either
spelling; owner addendum 15 item 35 fixes the rule, not the punctuation. Restated node by node:

```
RULE2-07-RED    last_closed_guard_pnl  -0.2      unchanged
                consecutive_loss_count  1        unchanged
                consec_loss_ok          false    unchanged
                guard_blocked_raw       true     unchanged
                fee_amount per fill     0.1      unchanged   fee_total -0.2, net -0.2
                gross_realized_pnl      0        unchanged   equity 1000 / 999.8
RULE2-07-GREEN  consecutive_loss_count  0        unchanged
                consec_loss_ok          true     unchanged
                guard_blocked_raw       false    unchanged
                last_closed_guard_pnl   ABSENT   unchanged   equity 1000 / 1000
```

The guard predicate itself is untouched: design `Design section 13, "last_realized_pnl=0`, so its consecutive-loss count"` states that `RULE2-07-RED` enables only the
consecutive-loss guard with test-only `max_consecutive_losses=1`, that corrected
`last_closed_guard_pnl=-0.2` under the gross-minus-fees basis, that the count becomes `1`, that
`count < max_consecutive_losses` is false, and that `guard_blocked_raw` is true. Every one of those
five facts is what the artifact still carries.

### W-3 `RULE2-08-RED` — the directed removal of the `guards` object

Item 9 makes the removal conditional: *"unless a separate owner-approved scenario-input amendment
binds its threshold and requires re-derivation"*. The condition is checked, not assumed:

1. `Design section 22.6, "0,98,98,98,98,0),(1999-12-31T23"` is the **only** scenario-input row for `RULE2-08-RED` (section 22.6, `Design section 22.6, "0,98,98,98,98,0),(1999-12-31T23"`). It binds
   the state-building prefix, the after-event bar, `initial_capital=1000`, fallback `10%`,
   `max_leverage_cap=10`, tick/step/minima `.01/1/0/0`, multiplier `1`, and no SL/TP. It binds **no
   guard switch and no `max_consecutive_losses`**.
2. `M-09` at `Design section 22.2, "states only the consecutive-loss guard"` defines `GUARD07` — including `use_consecutive_loss_halt=true` and
   `max_consecutive_losses=1` — and section 22.6 attaches `GUARD07` to `RULE2-07-RED` (`Design section 22.6, "040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe`) by reference; under addendum"`) and
   `RULE2-07-GREEN` (`Design section 22.6, "040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe`) by reference; under addendum"`) **only**. Neither `RULE2-08` row carries it.
3. A search of every `.md` and `.txt` file under `C:\tmp\LANE_PROMPTS_20260828\` for the phrases
   *"scenario-input amendment"*, *"scenario_input amendment"* and *"threshold amendment"* returns
   four hits and **not one of them is an amendment**: this lane's own spec
   (`LANE_W200_GOLDEN_OVER_REPAIR.md:23`), the design sentence itself (`Design section 23.5, "amendment binds its threshold and"`), the proposal that
   asks for the removal (`V19_TOKEN_AMENDMENT_PROPOSAL.md:376`), and the Lead's own log line
   recording that no such amendment exists (`N_TIMES.txt:653`). **No such amendment exists.**

The condition is therefore unmet and removal is what the design directs. Section 23.4 `Design section 23.4, "a declared guard projection is"` agrees
independently: the conditional member `guards` is *"Required exactly when a declared guard projection
is evaluated"*, and no guard projection is declared for this vector, so the object was not admissible
in the first place. After the removal, `RULE2-08-RED`'s `RESULT_SURFACE` carries exactly the seven
base members of `:1133` plus the one conditional member `cumulative_funding` that `:1148` requires on
every `DEF-P012-08` result — eight keys, no more:

```
final_position, trades, equity_curve, cumulative_funding, metrics, warnings, refusals, run_manifest
```

**No economic value moved.** The removed object contained one token and one derived integer
(`consecutive_loss_count 0`) plus two cells that were already `BLOCKED-MISSING-SCENARIO-INPUT`; no
money figure, rate, quantity, price or equity token was inside it, and nothing outside it was derived
from it. Byte-identical after the removal: `notional 100`, `raw_rate 0.001`,
`long_cashflow_rate -0.001`, `funding_cash_delta -0.1`, `cumulative_funding -0.1`, `mark_price 100`,
`final_position` `LONG` / `1` / `100`, and `equity_curve` `1000` / `999.9`.

### W-4 The cascade, stated in full rather than absorbed

The lane spec requires that a directed removal must not cascade silently. It did not cascade into any
value. It did have four bookkeeping consequences **inside the same artifact**, each of which is a
record *about* the removed object rather than a value on either comparison surface, and each of which
would have been a live false statement if left standing:

| Consequence | Why leaving it was not an option |
|---|---|
| `blocked_cells` lost its two `/guards/...` rows (8 → 6) | The ledger is the census of this artifact's marked cells. Rows naming pointers that no longer exist are the same census-versus-artifact mismatch lane W172 repaired under G83-F01, in the opposite direction. |
| `authored_value_tokens` lost its `/guards/guard_pnl_basis` row (4 → 3) | The pointer no longer exists. |
| `open_item_bindings[0].effect_on_this_scenario` rewritten | It asserted *"so `guard_pnl_basis` stays `GROSS_MINUS_FEES`"* — a live fact about a node this lane deleted. It now records the removal instead, exactly as lane W172 rewrote the same sentence under G83-F04 when item 4 removed `funding_included_in_guard_basis`. |
| `unchanged_sealed_values` clause struck | It claimed *"and every guard node are byte-identical to the pre-v1.5 seal"*. There is no guard node. Every other value it names is still byte-identical and still claimed. |

Nothing else in the bundle changed as a consequence. In particular the `RULE2-08-GREEN` artifact
already carried **no** `guards` object (its `RESULT_SURFACE` keys are `final_position`, `trades`,
`equity_curve`, `cumulative_funding`, `metrics`, `warnings`, `refusals`, `run_manifest`), so the two
`DEF-P012-08` rows are now consistent with each other for the first time.

### W-5 The three `DESIGN-GAP` rows were not opened for writing

`RULE2-04-RED`, `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED` are going to the owner because the
design does not settle them. They were not edited, and their SHA-256 digests are unchanged from the
values `CONTRACT_TABLES_MANIFEST.json` recorded under seal `1beaca483f0c...`:

```
RULE2-04-RED.json              9f7a541c08bb477b...   unchanged
RULE2-06-RED.json              25c747ac53111c51...   unchanged
RULE2-06-EQUAL-PRICE-RED.json  102aa04e93dfa9c5...   unchanged
```

So are the other eleven artifacts this lane did not name. Fourteen of seventeen goldens are
byte-identical to the sealed bytes; three changed.

### W-6 Discrepancies — recorded, not resolved

**W200-D01 — section 14 says `DEF-P012-08` guard outcomes ARE comparison nodes.** Design `Design section 13, "attribution, and fee-adjusted equity/metrics/guard outcomes."`
reads *"Guard outcomes follow the sourced OPEN-10 decision and are explicit comparison nodes"*, and
`Design section 23.4, "evaluated | Section 13 and section"` cites *"section 14's OPEN-10-controlled explicit comparison nodes"* as forcing text for the
conditional `guards` member. Item 9 at `Design section 23.4, "is evaluated | Section 13 and"` nevertheless directs removal of this row's guards
object. This lane resolved the tension in favour of removal on three grounds — item 9 is the newer,
row-specific, owner-approved direction; `Design section 23.4, "entry-sizing/notional projection | Sections 7-8 and"` conditions the member on a **declared guard
projection being evaluated**, and `Design section 22.6, "is superseded. RULE2-08-RED row: C"` declares none; and `Design section 14, "1, basis 100, multiplier 1"`'s sentence is an
expected-golden-changes statement for the section as a whole, whose antecedent (a captured funding
decision feeding a guard basis) has no evaluable guard on this vector. **The design's direction here
is less clear than the lane spec's summary claims, and this is the one place a reader could reach the
opposite reading.** Not silently absorbed.

**W200-D02 — item 9 says "the three inconsistent guard-basis values"; only two were re-spelled.**
`V19_TOKEN_AMENDMENT_PROPOSAL.md:373` names all three byte positions including `RULE2-08-RED.json:45`.
But item 9's own later clause, and `V19:376`, direct removal of the object that contains that third
value. Removal subsumes re-spelling: the third value no longer exists to be re-spelled. A reader
counting three changed tokens will find two. Recorded rather than reconciled by inventing a third.

**W200-D03 — line drift between v1.8 and v1.9 citations.** The guard-basis sentence is at `:1147-1150`
in v1.8 and `:1164-1167` in v1.9; the `RULE2-08-RED` scenario-input row is at `:888` in v1.8 and
`:894` in v1.9; the closed guards member set is at `:1139-1143` in v1.8 and `:1156-1160` in v1.9. The
pre-existing citations inside all 17 goldens, and `provenance.design_version`, still read **v1.8**.
This lane did not renumber outside the nodes it revised; doing so on three rows would have left a
bundle whose 17 artifacts disagree about which design they cite. The renumber is a bundle-wide act.

**W200-D04 — W167-D01 is relocated, not closed.** The missing scenario input that forced
`consec_loss_ok` and `guard_blocked_raw` to be marked is unchanged: `:894` still binds no guard
threshold for either `RULE2-08` row. The removal changes how that gap is expressed — an absent object
instead of two marked cells — and nothing about the gap itself. If the owner later binds a `RULE2-08`
guard threshold, the object must be reinstated and genuinely re-derived, which is exactly what item 9's
`unless` clause anticipates.

**W200-D05 — the manifest still describes v1.8.** `CONTRACT_TABLES_MANIFEST.json` records
`design.version` as v1.8, `design.total_lines` as 1273 and 38 v1.8 `line_spans_by_section` entries,
while the design this lane read is v1.9 with 1317 lines. This lane confined its manifest edits to
`files[]` for the files it actually revised, the one census field its own removal falsified, and its
`revision_history` entry. Re-describing the design is a bundle-wide act for the Lead.

### W-7 Honest limits of this repair

Two clauses of one design item, applied to three rows. This lane closes no OPEN row, un-blocks no
`BLOCKED-MISSING-RECORD-BYTES` digest, does not touch the design-unenumerated `metrics` marker on any
of the 17 artifacts, and grants no build, execution, re-seal, deployment or trading authority. It did
not touch the three `DESIGN-GAP` rows, the catalog, `IMPLEMENTATION_ANCHOR_DRAFT.json`, any catalog
row/input path/input digest, `seal_state`, `seal`, `reseal_history`, or anything under
`tests/corrected_vnext/`. The recorded `EXPECTED_SEAL_SHA` `1beaca483f0c...` **no longer covers these
bytes**, and three `scenario_catalog.json` `expected_artifacts['2.0.0'].digest` pins are now stale;
re-sealing and re-pinning are the Lead's acts under design `Design section 23.5, "must re-derive only these golden"`. The §16
`SEMANTIC_COVERAGE_REVIEW` remains owner-held and PENDING, and the claude family remains excluded from
that reviewer role because it authored these tables.

## W205 residue-marker pass — the two G103 findings, marked and not rewritten

### V-0 What this pass is, and what it is not

Lane `C:\tmp\LANE_PROMPTS_20260828\LANE_W205_DERIVATIONS_RESIDUE.md`, standing clauses
`N_COMMON_CLAUSES.md` C-1..C-7 read in full first. Family: the tables family, which authored these
bytes. This pass **adds markers and changes nothing else**. It authors no value, moves no value,
resolves no OPEN row, closes no discrepancy, and touches no golden, catalog, manifest, anchor, seal
field or `files[]` entry — the only bundle file written is this one, alongside the lane report
`W205_DERIVATIONS_RESIDUE_REPORT.md`. Re-seal #6 is the Lead's act.

Independence, stated as a fact rather than a promise: no `mtc_v2.core` import; no `observed/` path
read; no `tests/corrected_vnext/contracts/inputs/**` byte opened; no kernel, driver, verifier, gate,
generator, backtest or baseline exists or was executed. Local SHA-256, byte counts, and reading the
design file, the three affected goldens and this worksheet are the whole of the computation done.

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** In the paragraph above, the
*exists* arm of "no kernel, driver, verifier, gate, generator, backtest or baseline exists or was
executed" is false at the current build and is withdrawn. Only the *exists* arm is withdrawn; the *was executed* arm stands - this lane
executed no kernel, adapter, driver, gate, backtest, verifier, generator or baseline. The measurement, and the true replacement wording, are
recorded once at this worksheet's section-0 independence fence, in the W359 marker there.

The two findings are `DETECT_G103_W200_GOLDEN.md` **G103-F01** (MEDIUM) and **G103-F02** (LOW), both
deliberately sealed over at Lead re-seal #5 and named in `CONTRACT_TABLES_MANIFEST.json:374,380` and
`:499-500`.

### V-1 The five markers placed

Each marker follows this worksheet's own convention and **leaves the original text intact and
readable**: a bold `<VERB> BY LANE <lane> under <finding>` lead-in immediately after the superseded
prose — the form used at `:2309` (W186), `:2135` and `:1659` (W172) — or a bracketed in-fence note in
the form used at `:1971` for W172's census correction.

| # | Site (this file, current numbering) | What was stale there | Finding | Marker |
|---|---|---|---|---|
| 1 | `:736` (guard-derivation fence, `RULE2-07-RED`) | basis spelled `GROSS_MINUS_FEES` | G103-F02 class, site not named by G103 | in-fence bracket `:740-747` |
| 2 | `:756` (`rule2_divergent_projection` table row) | `2.0.0` cell reads `PRESENT(S:"GROSS_MINUS_FEES")` | **G103-F02, the named site** | paragraph `:766-781` |
| 3 | `:871-874` (`RULE2-08-RED` guard-outcome paragraph) | derives a `guards` object and names three of its members as expected `2.0.0` nodes | **G103-F01, named site** | paragraph `:876-894` |
| 4 | `:1910`, `:1919`, `:1922-1930` (W167 W-5 fence) | the `07-RED` and `07-GREEN` token lines; the whole `08-RED` sub-block | **G103-F01 named the `08-RED` lines**; the two token lines are the same residue | in-fence bracket `:1933-1958` |
| 5 | `:2049` (W-9 blocked-cell census row) | locates two cells at `/guards/consec_loss_ok` and `/guard_blocked_raw` | **G103-F01, named site** | paragraph `:2052-2066` |

All four sites G103 named are marked. Three further sites of the identical residue class — `:736`,
`:1910`, `:1919` — sit inside the same two blocks and are covered by the same markers rather than
left, because a reader landing on them takes the same superseded spelling as current. That G103-F02
named only the table row is recorded as a discrepancy in the lane report.

**NO VALUE MOVED.** Not one digit, token, marker or table cell of the original text was altered: the
diff against the pre-pass bytes is **87 inserted lines, zero changed lines, zero deleted lines**. The
pre-pass file measured `b0fa1e4136eda00b82bfacfe0c2dee67f928f3dcbcdb3a5e383c958129f41218` / 199980
bytes, which is what `CONTRACT_TABLES_MANIFEST.json:76-77` still pins.

### V-2 Sites examined and deliberately left, so the omission is recorded rather than absorbed

- **Y-5's token census at `:2399-2412`, restated at `:2419`.** It lists
  `GROSS_MINUS_FEES (underscore form)` among the TABLES-AUTHORED tokens. It is a dated census of the
  ledgers **as lane W172 wrote them**, not a statement of a required expected `2.0.0` node, and W200
  W-2 at `:2902` already names its exact lines and states the current disposition — that the labeled
  entry was removed from `authored_value_tokens` on both `RULE2-07` rows. A marker there would add
  nothing a reader does not already reach.
- **W200's own section, `:2830-3055`.** Its `GROSS_MINUS_FEES` occurrences are `before:` values in a
  changelog of the very act that superseded them, and its `guards` references describe the object it
  removed. Correct as written.
- **`W167_TABLES_V18_REPORT.md:66,183` and `W172_READING_Y_REPORT.md:192`**, which G103 noted carry
  the same pre-removal census. They are dated prior-lane reports, not live ledgers, and are outside
  this lane's write scope. Editing a dated report to match a later state destroys the record of what
  was believed when.
- **`RULE2-04-RED`, `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED`** — nothing concerning those three
  rows was read for a value or touched. They carry the two open owner questions.
- **The design citation `Design section 12, "declared synthetic `RED` scenario owned"` at `Design section 22.5, "the section-12 stated `TARGET-FAR=105`, `TARGET-NEAR=105"`.** The OPEN-10 sentence it quotes sits at `Design section 12, "declared synthetic `RED` scenario owned"` in design
  v1.9. That is the citation drift **W200-D03** already records as a bundle-wide act, not a residue
  of the removed object; renumbering one citation in isolation would leave this worksheet
  disagreeing with itself about which design revision it cites.

### V-3 What placing the markers cost — line numbers, stated rather than absorbed

Inserting 87 lines moves every later line of this file. The shift, applied to the pre-pass numbering:

```
original lines    1 - 739    unchanged
                740 - 756    +8
                757 - 849    +25
                850 - 1887   +45
               1888 - 1979   +71
               1980 - 2968   +87
```

Six pre-existing citations **inside this file** now name the wrong line and were **not** rewritten:
they are other lanes' records in an append-only worksheet, and this pass does not edit history to
match a later state. Their corrected targets, measured this session:

| Citation at | Reads | Now at |
|---|---|---|
| `:2522` (W186 Z-0) | `DERIVATIONS.md:2040-2056` | `:2127-2143` |
| `:2525` (W186 Z-0) | `DERIVATIONS.md:2208-2216` | `:2295-2303` |
| `:2596` (W186 Z-1) | `DERIVATIONS.md:2208-2211` | `:2295-2298` |
| `:2643` (W186 Z-3) | `DERIVATIONS.md:2204-2206` | `:2291-2293` |
| `:2811` (W186 Z-7) | `DERIVATIONS.md:2048-2056` | `:2135-2143` |
| `:2902` (W200 W-2) | `DERIVATIONS.md:2316-2321` | `:2403-2408` |

**TABLE SUPERSEDED BY LANE W224 under GM62-F07; marker added by lane W224.** The `Now at` column of
the table above is superseded in two independent ways, and the table itself is **left intact**.
(a) **Three of its six rows never landed on the record they name.** V-3 computed the column by
applying its uniform `+87` shift to the citing lane's own numbers rather than by measuring the
target text. For `:2525`, `:2596` and `:2643` the citing numbers - all three written by lane W186
into the same block - were already four lines low, so `+87` reproduced the error: `:2295-2303`
lands on the `FALLBACK` paragraph and the first five lines of the withheld-row record rather than
on that record, and `:2291-2293` lands on the tail of the preceding fence. The other three rows,
`:2522`, `:2811` and `:2902`, were correct in the pre-W224 bytes. (b) **Every row's `Citation at`
and `Now at` value has since shifted again**, because lane W224 inserted its own markers into this
file. (c) **The census of "six" is incomplete:** W186 Z-5 carries two further internal pointers,
`:1182` and `:1369-1380`, which V-3 did not count; the true count is **eight**. Section U-2 below
gives all eight, measured against the current bytes rather than computed, together with this lane's
own shift table. The paragraph above is otherwise correct and its reasoning is adopted unchanged:
these are other lanes' records in an append-only worksheet and none of them was rewritten. **NO
VALUE MOVED.**

Eleven citation occurrences reach this file from outside it and are equally shifted. All are outside
this lane's write scope and none was touched: `CONTRACT_TABLES_MANIFEST.json:374,380,500`
(`DERIVATIONS.md:748` → `:756`) and `:499` (`:846-849` → `:871-874`, `:1877-1885` → `:1922-1930`,
`:1978` → `:2049`); `W200_GOLDEN_OVER_REPORT.md:69` (`:2316-2321` → `:2403-2408`); and
`W186_RULE205RED_REPORT.md:33,36,42,116,193,238` (`:2040-2056` → `:2127-2143`, `:2208-2216` →
`:2295-2303`, `:2419` → `:2506`, `:2204-2206` → `:2291-2293`, `:2048-2056` → `:2135-2143`, `:2054` →
`:2141`). The two dated lane reports are left untouched by fence; the manifest is the Lead's at
re-seal #6. **Whether to renumber any of them is a bundle-wide act of the same class as W200-D03 and
W200-D05. Recorded as W205-D01.**

### V-4 Honest limits of this pass

- **W205-D01** — the line-number consequence in V-3. Six internal and eleven external citation
  occurrences now name the wrong line. None of them names a value; every one of them names a
  location. Recorded, not repaired, because repairing them is a bundle-wide renumber.
- This pass did **not** re-measure the `BLOCKED-*` census of W-9 (`:2045-2050`, restated at
  `:2074-2076`). It is the v1.8 census, it is now marked as such, and **no replacement count is
  stated anywhere in this pass**. A surface-restricted structural walk over all 17 artifacts is a
  re-measurement act, not a residue marker.
- **W167-D01**, **W200-D01** and the owner questions on `RULE2-04-RED`, `RULE2-06-RED` and
  `RULE2-06-EQUAL-PRICE-RED` are untouched and remain open. The W200 removal relocated W167-D01 into
  the absence of the object; it did not close it, and this pass closes nothing.
- The recorded `EXPECTED_SEAL_SHA` `d642252ed2e16b6a8a2f336e21cb9acb63890008864062c8706fce4672eab438`
  (`CONTRACT_TABLES_MANIFEST.json:378,389`, Lead re-seal #5) **no longer covers these bytes**, and
  `files[]` at `:75-77` still pins the pre-pass digest and byte count. Re-sealing and re-pinning are
  the Lead's acts under design `Design section 23.5, "these golden nodes, then the"`; this pass deliberately performed neither, and updated no
  `files[]` entry and no seal field.

## W224 supersession-marker pass — the GM62 live-but-superseded sites, marked and not rewritten

### U-0 What this pass is, and what it is not

Lane `C:\tmp\LANE_PROMPTS_20260828\LANE_W224_DERIVATIONS_SUPERSEDE.md`, standing clauses
`N_COMMON_CLAUSES.md` C-1..C-7 read in full first, census
`C:\tmp\LANE_PROMPTS_20260828\DETECT_GM62_DERIVATIONS.md` read in full first. Family: the tables
family, which authored these bytes. This pass **adds markers and changes nothing else**. It authors
no value, moves no value, derives nothing new, resolves no OPEN row, closes no discrepancy, and
touches no golden, catalog, manifest, anchor, seal field or `files[]` entry — the only bundle file
written is this one, alongside the lane report `W224_DERIVATIONS_SUPERSEDE_REPORT.md`. Re-seal #7 is
the Lead's act.

Independence, stated as a fact rather than a promise: no `mtc_v2.core` import; no `observed/` path
read; no `tests/corrected_vnext/contracts/inputs/**` byte opened; no implementer-authored input file
consumed; no kernel, driver, verifier, gate, generator, backtest or baseline exists or was executed.
Local SHA-256, byte and line counts, and reading the design file, the seventeen goldens under
`golden/corrected_vnext/`, the prior lane reports and this worksheet are the whole of the
computation done.

**FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359 under the owner's extension of
decision 153 (Q-F = a), 2026-09-04; finding W354 D-3.** In the paragraph above, the
*exists* arm of "no kernel, driver, verifier, gate, generator, backtest or baseline exists or was
executed" is false at the current build and is withdrawn. Only the *exists* arm is withdrawn; the *was executed* arm stands - this lane
executed no kernel, adapter, driver, gate, backtest, verifier, generator or baseline. The measurement, and the true replacement wording, are
recorded once at this worksheet's section-0 independence fence, in the W359 marker there.

The census findings acted on are `DETECT_GM62_DERIVATIONS.md` **GM62-F04** (MEDIUM), **GM62-F05**
(MEDIUM), **GM62-F06** (MEDIUM) and **GM62-F07** (LOW). **GM62-F01**, **GM62-F02** and **GM62-F03**
are not this family's to close and were not touched — see U-4. **GM62-F08** is recorded as an open
item and was deliberately **not** derived — see U-5.

### U-1 The nine supersession markers placed

Each marker follows this worksheet's own convention and **leaves the original text intact and
readable**: a bold `<VERB> SUPERSEDED BY LANE <lane> under <basis>; marker added by lane <lane>
under <finding>` lead-in immediately after the superseded block — the form standing at `:921` and
`:2165` before this pass — or a bracketed in-fence note in the form standing at `:785`. Both were
read at those sites before the first marker below was written.

| # | Site (this file, current numbering) | What was stale there | Finding | Marker |
|---|---|---|---|---|
| 1 | `:516` (§5 `RULE2-05-RED` sizing fence) | `order_notional = 1 * 101 * 1 = 101` | GM62-F04 class, site **not named** by GM62 | in-fence bracket `:517-529` |
| 2 | `:613-614` (§6 `RULE2-06-RED` divergent table) | two `/RESULT_SURFACE/collision/*` rows read live | **GM62-F05, named site** | paragraph `:622-640` |
| 3 | `:674` (§6 `RULE2-06-EQUAL-PRICE-RED` divergent table) | `/RESULT_SURFACE/collision/ordered_chosen_exit_ids` reads live | **GM62-F05, named site** | paragraph `:680-690` |
| 4 | `:1220`, `:1239` (R-0.3 fee table and raw-bits fence) | `0.04545` labelled a **sealed** token; no artifact seals it now | GM62-F04 class, site **not named** by GM62 | paragraph `:1244-1258` |
| 5 | `:1288` (R-0.4 accumulation fence) | `RULE2-05-RED 1000 - fl(0.04545) = 999.95455` | **GM62-F04, named site** | in-fence bracket `:1292-1302` |
| 6 | `:1486-1497` (R-9) | `fee_notional 101`, `fee_amount 0.04545`, its delta, `equity_curve.last 999.95455`, and D-06's `order_notional 101` | **GM62-F04, named site** | paragraph `:1499-1515` |
| 7 | `:2105` (W167 W-7 member-set table) | the `08-RED` row reads `guards` `yes` | **GM62-F06, named site** | paragraph `:2108-2120` |
| 8 | `:2102` (same table) | the `05-RED / 05-GREEN` row reads `order_notional` `101 / 100` | GM62-F04 class, site **not named** by GM62 | paragraph `:2122-2129` |
| 9 | `:2343`, `:2348-2350` (W172 Y-1 fence and its prose) | `RULE2-05-RED 101 = 1*101*1` at sequence `1`, restated as "already-sealed value byte for byte" | **GM62-F04, named site** | paragraph `:2356-2371` |

All six sites the census named are marked. Three further sites of the identical residue class —
`:516`, `:1220`/`:1239` and `:2102` — were found by reading and are marked rather than left, on the
same ground lane W205 gave at V-1: a reader landing on them takes a superseded value as current.
That the census did not name them is recorded as **W224-D02** below.

**Every current value asserted in those nine markers was measured this session** against the
seventeen goldens under `golden/corrected_vnext/`, not taken from a prior report. The markers that
carry the `RULE2-05-RED` re-derivation rest on `RULE2-05-RED.json:27,30,36,43,45` (the current
bytes) and `RULE2-05-RED.json:90-99` (the artifact's own before/after ledger). Those that carry the
collision removal rest on `RULE2-06-RED.json:27,49-71,101` and
`RULE2-06-EQUAL-PRICE-RED.json:28,50-72,105`. The one that carries the guards removal rests on
`RULE2-08-RED.json:40-59,93`.

**NO VALUE MOVED.** Not one digit, token, marker or table cell of the original text was altered: the
diff against the pre-pass bytes is **422 inserted lines, zero changed lines, zero deleted
lines** — 198 of them inserted into the body, the rest this appended section, which shifts nothing.
The pre-pass file measured `669567296f868186eb0ff227af3f251b6cc59fc4a9f8d6d0c054001b5b32aefc` /
216084 bytes, which is what `CONTRACT_TABLES_MANIFEST.json:74-78` still pins. Unlike the W205 pass,
the "zero deleted" half of that claim **is** verifiable here, because the pre-pass bytes were
preserved before this pass began, in the bundle snapshot
`C:\tmp\P012_LEAD_RESEAL\bundle_snapshots\20260902_0129\DERIVATIONS.md`, and the diff above was
taken against them line by line.

### U-2 The stale internal pointers — measured, not computed

GM62-F07 names six broken internal citations, taking them from lane W205's V-3 table. **The true
count is eight, and three of V-3's six rows do not land on the record they name.** V-3 built its
`Now at` column by applying a uniform `+87` line shift to each citing lane's own number instead of
measuring the target text; where the citing number was already wrong, the shift reproduced the
error. Every row below was found by **reading the target text in the current bytes**.

| Citation at (now) | Reads | V-3 said | Measured now | Target |
|---|---|---|---|---|
| `:2652` (W186 Z-0) | `DERIVATIONS.md:2040-2056` | `:2127-2143` | `:2240-2256` | the **W167-D05** record |
| `:2655` (W186 Z-0) | `DERIVATIONS.md:2208-2216` | `:2295-2303` **wrong** | `:2429-2437` | W172's withheld-`SIZING_COMPUTED` record |
| `:2738` (W186 Z-1) | `DERIVATIONS.md:2208-2211` | `:2295-2298` **wrong** | `:2429-2432` | the arithmetic inside that record |
| `:2791` (W186 Z-3) | `DERIVATIONS.md:2204-2206` | `:2291-2293` **wrong** | `:2425-2427` | W172's `FALLBACK`-token paragraph |
| `:2874` (W186 Z-5) | `R-0.4 :1182` | **not counted** | `:1288` | the superseded accumulation line |
| `:2876` (W186 Z-5) | `R-9 :1369-1380` | **not counted** | `:1486-1497` | section R-9 |
| `:2976` (W186 Z-7) | `DERIVATIONS.md:2048-2056` | `:2135-2143` | `:2248-2256` | W172's **NARROWED** paragraph |
| `:3074` (W200 W-2) | `DERIVATIONS.md:2316-2321` | `:2403-2408` | `:2533-2538` | the Y-5 token-census rows |

The three wrong rows share one cause: lane W186 wrote `:2204-2206`, `:2208-2211` and `:2208-2216`
into the same block, each **four lines low** in the numbering of its own day, and V-3 carried the
error forward mechanically. The other five rows were correct at their time and are restated above
only because this pass shifted them again.

**Not one citation was rewritten.** Each of the eight now carries an in-place bracket or paragraph
naming the measured target and leaving the original number readable, and V-3's own table carries a
marker at `:3331-3346`. Rewriting another lane's record to match a later state is what an
append-only worksheet forbids; that reasoning is W205's at V-3 and is adopted here unchanged.

**This pass's own line shift.** Inserting 198 lines into the body moves every later line of this
file. Applied to the pre-pass (post-W205) numbering:

```
pre-pass lines    1 - 516     unchanged
                517 - 607     +13
                608 - 645     +33
                646 - 1197    +45
               1198 - 1230    +61
               1231 - 1425    +72
               1426 - 2016    +90
               2017 - 2241   +113
               2242 - 2529   +130
               2530 - 2597   +142
               2598 - 2644   +148
               2645 - 2722   +156
               2723 - 2813   +165
               2814 - 2909   +172
               2910 - 3148   +181
               3149 - 3176   +198
```

Citation occurrences that reach this file **from outside it** are equally shifted and none was
touched: they are the Lead's at re-seal, or dated lane reports that a later state may not edit.
Their targets, re-measured here from the pre-pass numbers lane W205 recorded at V-3:

| External citation | Named target | Now at |
|---|---|---|
| `CONTRACT_TABLES_MANIFEST.json:374,380,500` | `DERIVATIONS.md:756` | `:801` |
| `CONTRACT_TABLES_MANIFEST.json:499` | `:871-874`, `:1922-1930`, `:2049` | `:916-919`, `:2012-2020`, `:2162` |
| `W200_GOLDEN_OVER_REPORT.md:69` | `:2403-2408` | `:2533-2538` |
| `W186_RULE205RED_REPORT.md:33` | `:2040-2056` | `:2240-2256` |
| `W186_RULE205RED_REPORT.md:36` | `:2208-2216` (four lines low) | `:2429-2437` |
| `W186_RULE205RED_REPORT.md:42` | the W186 section header | `:2641` |
| `W186_RULE205RED_REPORT.md:116` | `:2204-2206` (four lines low) | `:2425-2427` |
| `W186_RULE205RED_REPORT.md:193` | `:2048-2056` | `:2248-2256` |
| `W186_RULE205RED_REPORT.md:238` | the W167-D05 closure annotation | `:2257-2260` |

Two of those rows correct V-3 as well: V-3 mapped the W186 section header to `:2506`, where it in
fact stood at `:2511` before this pass, and mapped the closure annotation to `:2141`, where the
annotation itself is the **RESOLVED** block and `:2141` sat inside the **NARROWED** paragraph.
**Whether to renumber any external citation remains a bundle-wide act of the same class as
W200-D03, W200-D05 and W205-D01. Recorded as W224-D01, not repaired here.**

### U-3 Sites examined and deliberately left, so the omission is recorded rather than absorbed

- **§0.3 correction row C-04 at `:93`.** It records that the W127 partial's
  `RESULT_SURFACE/collision` = `{B:1, chosen="TARGETS"}` was replaced at v1.4 by
  `ordered_chosen_exit_ids` plus the pessimistic-field divergence. That replacement is itself
  superseded by the W167 removal marked at `:622-640`. It is left because §0.3 is a dated ledger of
  what the partial said and how it was corrected **then**, in the same class as the `before:` values
  of a changelog, which V-2 already ruled correct as written. A reader reaches the current state
  through the §6 markers.
- **W172 Y-4's `08-RED` line at `:2504`**, which reads "guards as above". Its subject is why that row
  gains no `decision_events` row — a conclusion the guards-object removal does not disturb — not the
  presence of a RESULT `guards` member. Left.
- **The W167-D01 record at `:2200-2209` and the G83-F01 disposition at `:2562`.** Both are
  discrepancy and finding ledgers, and the marker lane W205 placed at `:2165-2179` already states
  that W167-D01 is relocated into the absence of the object rather than closed. Left.
- **W186's own section `:2641-3001` and W200's own section `:3002-3236`.** Their `101`, `0.04545`,
  `999.95455` and `guards` occurrences are `before:` values in the changelogs of the very acts that
  superseded them. Correct as written; V-2 ruled the same way for W200.
- **Y-5's token census at `:2530-2541`, restated at `:2549`.** Left for the reason V-2 gave, which
  this pass re-read and did not disturb.
- **`W167_TABLES_V18_REPORT.md`, `W172_READING_Y_REPORT.md`, `W186_RULE205RED_REPORT.md` and
  `W200_GOLDEN_OVER_REPORT.md`.** Dated prior-lane reports, outside this lane's write scope. Editing
  a dated report to match a later state destroys the record of what was believed when.
- **`RULE2-04-RED`, `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED` as *values*.** Their goldens were
  read for the collision-object markers and for nothing else; no value on any of the three was
  touched, and the two open owner questions on them are untouched.

### U-4 GM62-F01, F02 and F03 — left to the Lead, deliberately

The three say that sealed values rest on requirements the design never closes:
`COLLISION_RESOLVED.touched_exit_ids` ordering (**GM62-F01**), the `RESULT_SURFACE.trades[]` member
schema (**GM62-F02**) and the `cash_events[]` container schema (**GM62-F03**). **Closing any of them
is a design act, and two of the three are already owner questions.** This lane read them, wrote
nothing at their sites, and changed no value they name. They are not marked either, because a
supersession marker asserts that a later ruling exists and no later ruling exists for any of the
three. The Lead is routing them.

**FINDING SUPERSEDED BY OWNER ADDENDUM 29 DECISIONS 71 AND 72; marker added by lane W244 under
addendum 29 decision 73.** The paragraph above says that no later ruling exists for any of the
three and that they are therefore left unmarked. **That is no longer true for two of the three.**
The owner closed **GM62-F01** and **GM62-F02** on 2026-09-02: decision 71 closes the
`RESULT_SURFACE.trades[]` member set
(`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-29_EVENING.md:596-610`) and decision 72
fixes the `COLLISION_RESOLVED.touched_exit_ids` receipt order (same file, `:612-623`). Decision 73
(same file, `:631-635`) authorises this family to re-derive the four goldens they name.
**GM62-F03** - the `cash_events[]` container schema - is untouched by addendum 29 and stands open
exactly as written. **NO VALUE MOVED BY THIS MARKER** - the paragraph above is left exactly as
lane W224 wrote it, and the re-derivation it now points at is recorded in the W244 section below.

### U-5 GM62-F08 — recorded as an open item, not derived

**GM62-F08** says the `RULE2-05-RED` zero-quantity container shape — one `fill_events` row, one
`cash_events` row, one `fee_events` row and a `final_position`, all with zero values — is asserted
because the closed schema can express it rather than derived from a design line that governs a
zero-quantity order transition.

**That is already recorded in this worksheet, in the words of the lane that made the choice.**
**W186-D01** at `:2891-2917` states the gap, quotes the five design lines that fail to settle it
(`Design section 3, "For each chosen fill intent"`, `Design section 3, "For each chosen fill intent"`, `Design section 7, "= sizing_equity * (risk_pct / 100"`, `Design section 13, "realized PnL plus every linked"`, and `Design section 23.1, "touched target in the scenario's declared exit-candidate order; this is"` with `Design section 23.1, "touched target in the scenario's declared exit-candidate order; this is"` and `Design section 23.4, "the kernel already share, while"`), records the
alternative reading as considered and not chosen, and ends **"Owner or §16 resolution requested."**
The finding and the discrepancy are the same fact.

This pass **did not derive the missing reasoning and states none**. Inventing a derivation after the
value was sealed would be authoring a design fact by inference, which this family is fenced from,
and it would turn an honestly recorded open question into a false closure. GM62-F08 therefore stands
**open, pointing at W186-D01 (`:2891-2917`)**, and belongs in the owner queue rather than in this
pass's work.

### U-6 Honest limits of this pass

- **W224-D01** — the line-number consequence in U-2. Nine external citation occurrences and every
  internal citation named above now sit at different numbers. None of them names a value; every one
  of them names a location. Recorded, not repaired, because repairing them is a bundle-wide
  renumber.
- **W224-D02** — the GM62 census named six of the nine live-but-superseded sites this pass found.
  `:516`, `:1220`/`:1239` and `:2102` are the same residue class and are marked rather than left.
  Recorded so the census's coverage claim is not taken as exhaustive.
- **W224-D03** — three of the six rows of W205's V-3 `Now at` column never landed on the record they
  name, and V-3's count of "six pre-existing citations" omitted the two W186 Z-5 pointers. Both are
  corrected by measurement in U-2 and marked at `:3331-3346`; V-3's own text is left intact.
- This pass **re-measured no census and states no replacement count**. The `BLOCKED-*` counts of W-9,
  and every scenario, catalog and container count in this worksheet, are exactly as their lanes
  measured them.
- **GM62-F01, F02, F03** are open design questions, **GM62-F08** is an open item pointing at
  **W186-D01**, and **W167-D01**, **W200-D01**, **W205-D01**, **W186-D02**, **W186-D03** and the
  owner questions on `RULE2-04-RED`, `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED` are untouched and
  remain open. This pass closes nothing.

  **CLAUSE SUPERSEDED BY OWNER ADDENDUM 29 DECISIONS 71 AND 72; marker added by lane W244 under
  addendum 29 decision 73.** **GM62-F01** and **GM62-F02** are no longer open design questions.
  The owner closed them at
  `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-29_EVENING.md:596-610` and `:612-623`, and
  the open owner questions on `RULE2-04-RED`, `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED` named
  in the bullet above are answered for exactly those two subjects - trade-row member set and
  receipt order - and for nothing else. **GM62-F03**, **GM62-F08**, **W167-D01**, **W200-D01**,
  **W205-D01**, **W186-D01**, **W186-D02** and **W186-D03** are untouched by lane W244 and remain
  open. **NO VALUE MOVED BY THIS MARKER** - the bullet above is left exactly as lane W224 wrote it.
- The recorded `EXPECTED_SEAL_SHA` `df561e7993df37e473c39b1fe174289d244d0b9b16cea9ab6aed72c11b91a964`
  (`CONTRACT_TABLES_MANIFEST.json:388,399`, Lead re-seal #6) **no longer covers these bytes**, and
  `files[]` at `:74-78` still pins the pre-pass digest
  `669567296f868186eb0ff227af3f251b6cc59fc4a9f8d6d0c054001b5b32aefc` and 216084 bytes. Re-sealing and
  re-pinning are the Lead's acts under design `Design section 23.5, "then the Lead must re-seal"`; this pass deliberately performed neither,
  and updated no `files[]` entry and no seal field. The stale `scenario_catalog.json` digest pins
  recorded at W186-D04 and by W200 are equally untouched.

---

## W244 re-derivation under owner addendum 29 decisions 71 and 72 - four goldens, shape and order only

This section is written by the tables family under **owner addendum 29 decision 73**, the only
authority under which a sealed golden may change. The three ruling texts are quoted at their
ledger lines below, then every node this lane moved is listed with its before and after value.
**No economic value moved anywhere in this pass**: not one price, quantity, fee, funding amount,
PnL, equity figure or metric differs from the pre-pass bytes in any of the four files.

### W244-1 The authority, quoted

**Decision 71** (`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-29_EVENING.md:596-610`),
quoted at `:602-606`:

> The owner rules that every completed trade row has exactly: `entry_fill_price` (quantity-weighted
> over entry fills), `quantity`, `exit_ids` (in exit-event sequence order), `gross_realized_pnl`,
> `fee_total`, `funding_total`, `net_trade_pnl`. No `exit_fill_price` member; per-piece exit prices
> live only in the closed `exit_events[]` schema. A trade that exits in several pieces is ONE row
> whose `exit_ids` lists every piece in sequence order.

**Decision 72** (same file, `:612-623`), quoted at `:616-619`:

> The owner rules the receipt order is the scenario's declared exit-candidate order, stop first,
> then targets in declaration order. This never changes which exits execute, their prices, or PnL.

and at `:620-621`:

> `touched_exit_ids` becomes `["STOP","TARGET-NEAR","TARGET-FAR"]` in both

**Decision 73** (same file, `:631-635`), quoted at `:631-634`:

> Authorises, in the build worktree only: design v1.9 -> v1.10 amendment closing the trade-row
> member set and the receipt order; the tables family re-deriving the four goldens named in 71 and
> 72 under protected scope `MTC_V2`; Lead re-seal #8; and one gate rerun after that seal.

### W244-2 Decision 71 - `RULE2-04-RED` and `RULE2-07-RED` trade rows

The ruling closes the member set at exactly seven members and orders `exit_ids` by `exit_events[]`
sequence order. The member spelling and key order taken here are the ones the three RULE2-06
sheets already carry (`golden/corrected_vnext/RULE2-06-GREEN.json:47`,
`golden/corrected_vnext/RULE2-06-RED.json:52`,
`golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json:53`): `entry_fill_price`, `quantity`,
`exit_ids`, `gross_realized_pnl`, `fee_total`, `funding_total`, `net_trade_pnl`.

`exit_ids` is derived from each file's own `exit_events[]` container and from nothing else.

| Golden | `exit_events[]` read | Derived `exit_ids` |
|---|---|---|
| `RULE2-04-RED` | one member, `sequence` 0, `exit_id` `STOP` (`golden/corrected_vnext/RULE2-04-RED.json:41`) | `["STOP"]` |
| `RULE2-07-RED` | one member, `sequence` 0, `exit_id` `TIME_STOP` (`golden/corrected_vnext/RULE2-07-RED.json:44`) | `["TIME_STOP"]` |

Per-node before/after, one node removed and one node added per file:

| Pointer | Before | After |
|---|---|---|
| `RULE2-04-RED` `/RESULT_SURFACE/trades/0/exit_fill_price` | `90` | member removed (decision 71) |
| `RULE2-04-RED` `/RESULT_SURFACE/trades/0/exit_ids` | absent | `["STOP"]` |
| `RULE2-07-RED` `/RESULT_SURFACE/trades/0/exit_fill_price` | `100` | member removed (decision 71) |
| `RULE2-07-RED` `/RESULT_SURFACE/trades/0/exit_ids` | absent | `["TIME_STOP"]` |

The two removed per-piece exit prices are not lost: decision 71 says they "live only in the closed
`exit_events[]` schema", and both are still on disk unchanged at
`golden/corrected_vnext/RULE2-04-RED.json:41` (`final_fill_price` `90`) and
`golden/corrected_vnext/RULE2-07-RED.json:44` (`final_fill_price` `100`).

Every other member of both trade rows, and every other node of both files, is byte-identical to the
pre-pass bytes: `entry_fill_price` `100` / `quantity` `1` / `gross_realized_pnl` `-10` /
`fee_total` `-0.085499999999999993` / `funding_total` `0` / `net_trade_pnl` `-10.0855` on
`RULE2-04-RED`, and `entry_fill_price` `100` / `quantity` `1` / `gross_realized_pnl` `0` /
`fee_total` `-0.2` / `funding_total` `0` / `net_trade_pnl` `-0.2` on `RULE2-07-RED`.

### W244-3 Decision 72 - `RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED` receipt order

The declared exit-candidate order comes from the RULE 2 scenario binding in the DEF-P012-06 text,
`Design section 12, "order; this receipt-only listing rule"` (inside the `Design section 12, "order; this receipt-only listing rule"` block the ruling cites), which declares the
candidates in this order:

> `RULE2-06-RED` is a synthetic long under `execution_profile_id=raw_close_only_v1` with entry fill
> `100`, reference quantity `2`, `qty_step=1`, stop `90`, target `TARGET-NEAR` at `105` with target
> fraction `0.5`, target `TARGET-FAR` at `110` with target fraction `0.5`

Declaration order is therefore stop `90`, then `TARGET-NEAR`, then `TARGET-FAR`. The same line
binds `RULE2-06-EQUAL-PRICE-RED` as using "the exact `RULE2-06-RED` inputs except that `TARGET-FAR`
is also at `105`", so its declared candidate order is identical. Under decision 72 the receipt is
stop first, then targets in that declaration order: `["STOP", "TARGET-NEAR", "TARGET-FAR"]` in
both, which is exactly the value the ruling names at `:620-621`.

| Pointer | Before | After |
|---|---|---|
| `RULE2-06-RED` `/EVENT_SURFACE/decision_events/2/touched_exit_ids` | `["TARGET-NEAR", "TARGET-FAR", "STOP"]` | `["STOP", "TARGET-NEAR", "TARGET-FAR"]` |
| `RULE2-06-EQUAL-PRICE-RED` `/EVENT_SURFACE/decision_events/2/touched_exit_ids` | `["TARGET-NEAR", "TARGET-FAR", "STOP"]` | `["STOP", "TARGET-NEAR", "TARGET-FAR"]` |

`ordered_chosen_exit_ids` is untouched on both, as the ruling requires: it stays
`["TARGET-NEAR", "TARGET-FAR"]` on `RULE2-06-RED` (long ascending target price) and
`["TARGET-FAR", "TARGET-NEAR"]` on `RULE2-06-EQUAL-PRICE-RED` (equal prices, `exit_id` UTF-8
byte-order tie-break). `collision`, `same_bar_collision_policy_id`, `reference_quantity`,
`stop_remainder_quantity`, `target_ordering_rule` and `tie_break_applied` are untouched, as are
every `fill_events`, `cash_events`, `fee_events`, `funding_events` and `exit_events` member and the
whole `RESULT_SURFACE` of both files. `RULE2-06-GREEN` already carries `touched_exit_ids` `["STOP"]`
(`golden/corrected_vnext/RULE2-06-GREEN.json:27`), which is already stop-first and needs no move;
it was read and not written.

### W244-4 The economic-value proof

Each of the four files was compared node by node against the pre-pass snapshot at
`C:/tmp/SNAPSHOTS/20260902_1009/P012_CONTRACT_TABLES_W127/golden/corrected_vnext/`. Every JSON leaf
was addressed by pointer on both sides and the two leaf maps compared:

| File | Leaves before | Leaves after | Numeric leaves changed in place | Changed pointers | Removed | Added |
|---|---|---|---|---|---|---|
| `RULE2-04-RED` | 244 | 244 | 0 | 0 | 1 (`/RESULT_SURFACE/trades/0/exit_fill_price`) | 1 (`/RESULT_SURFACE/trades/0/exit_ids/0`) |
| `RULE2-07-RED` | 305 | 305 | 0 | 0 | 1 (`/RESULT_SURFACE/trades/0/exit_fill_price`) | 1 (`/RESULT_SURFACE/trades/0/exit_ids/0`) |
| `RULE2-06-RED` | 316 | 316 | 0 | 3 (the three `touched_exit_ids` slots) | 0 | 0 |
| `RULE2-06-EQUAL-PRICE-RED` | 326 | 326 | 0 | 3 (the three `touched_exit_ids` slots) | 0 | 0 |

Not one numeric leaf differs in value on either side of the pass in any of the four files. The only
numeric leaves that exist on one side and not the other are the two `exit_fill_price` members that
decision 71 removes by name, and both survive unchanged as `final_fill_price` in `exit_events[]`.
The six changed pointers are all string slots inside `touched_exit_ids`, and the multiset of the
three strings is identical before and after in both files - a permutation, which is exactly what
decision 72 orders.

### W244-5 Class sweep

`exit_fill_price` and `touched_exit_ids` were swept across the whole bundle - every golden, this
worksheet, every report file, `scenario_catalog.json`, `CONTRACT_TABLES_MANIFEST.json`,
`IMPLEMENTATION_ANCHOR_DRAFT.json` and `tests/corrected_vnext/contracts/inputs/`. Seven sites exist.
Four are the goldens re-derived above; `RULE2-06-GREEN.json:27` already satisfies decision 72 and
was not written; this worksheet's U-4 paragraph and its U-6 bullet carry the markers placed by this
lane; and `W224_DERIVATIONS_SUPERSEDE_REPORT.md:192` is a dated prior-lane report, left untouched on
this worksheet's own standing ground at `:3537-3539` - "Editing a dated report to match a later
state destroys the record of what was believed when." No fifth golden needs to move.

### W244-6 What this lane did not do

- No `CONTRACT_TABLES_MANIFEST.json`, `scenario_catalog.json` or `IMPLEMENTATION_ANCHOR_DRAFT.json`
  edit. The four goldens and this worksheet now differ from every digest pinned for them; re-seal #8
  and every re-measurement are the Lead's acts under design `Design section 23.5, "the Lead must re-seal them"`, and decision 73 names that
  re-seal as a separate authorised step.
- No design edit. Decision 73 authorises the v1.9 -> v1.10 amendment, but a parallel lane owns it;
  this lane derived from the ledger text, which decision 73 makes the standing authority.
- No kernel read or run, no `observed/` read, no verifier or baseline executed. Decisions 71 and 72
  both say "Kernel unchanged by this decision".
- **W244-D01** - the line-number consequence, measured from the diff against the pre-pass snapshot.
  This pass is insertion-only: **0 lines were deleted or rewritten**. It inserted a 12-line marker
  block after pre-pass line `:3553` (diff hunk `3553a3554,3565`), a 10-line marker block after
  pre-pass line `:3591` (hunk `3591a3604,3613`), and appended this whole section after the pre-pass
  last line `:3598`. Every citation into this worksheet at a pre-pass line at or above `:3553` still
  lands where it did; a citation in `:3554-:3591` now sits 12 lines lower, and one at `:3592` or
  below sits 22 lines lower. This is the same class W224 recorded as W224-D01 and is recorded, not
  repaired.

## W262 re-derivation of the ten PROBE rows under design v1.11 (amendment-choice W261)

This section is written by the tables family under design **v1.11** section 23.5 item 12
(Design section 23.1, "with domain exactly `{false,true"), which assigns exactly these ten
rows to this family, and under the amendment-choice recorded by lane W261
(`C:\tmp\LANE_PROMPTS_20260828\W261_PROBE_NODE_RULE_REPORT.md:1-16`). The lane is
`C:\tmp\LANE_PROMPTS_20260828\LANE_W262_PROBE_ROWS_REDERIVE.md`, standing clauses C-1..C-7
(`C:\tmp\LANE_PROMPTS_20260828\N_COMMON_CLAUSES.md`).

**No economic value moved anywhere in this pass**: no price, quantity, fee, funding amount, PnL,
equity figure, digest or metric differs from the pre-pass bytes. Two files changed:
`scenario_catalog.json` (the ten `role: PROBE` rows only) and this worksheet (insertion-only).

### W262-1 The rule, quoted

Design v1.11 `Design v1.11 section 15.3, "2026-09-03) - the sealed member"`, inserted by lane W261 into section 15.2 step 6, quoted in full:

> **AMENDMENT-CHOICE (W261):** In step 6, the prior equality phrase is superseded by this exact rule.
> A probe is `DETECTED` only when the real top-level gate refuses before an accepting receipt, the
> observed failed check id equals the row's `expected_failed_check`, and the row's
> `expected_first_changed_node` is in the complete set of nodes/paths at which the corrected output
> differs from the sealed expected artifact. For a record-identity refusal before scenario output, the
> mutated record path is the path member of that difference set. The receipt records the catalog
> target as `expected_first_changed_node` and, beside it, the comparator's own first differing node as
> `comparator_first_differing_node`. The latter is the first unequal node emitted by the section-15.3
> recursive walk: emit the current node first, then visit object children by UTF-8 byte-sorted key and
> array children by ascending index, applying the same order recursively. These two nodes may differ.
> The design names the node a modification targets; the comparator's traversal order is an
> implementation fact the design did not state. Requiring the targeted node to be a changed node
> preserves the design's intent and the exact-match discipline without binding it to key order.

Three consequences are taken from that text and nothing else is read into it.

1. `expected_first_changed_node` is **the catalog target — the node the design names a modification
   targets** — and it must be a member of the complete changed-node/path set. It is no longer
   required to be the enumerator's first node.
2. The comparator's traversal-order first node is a **separate** recorded identity whose exact member
   name the design gives as `comparator_first_differing_node` (`Design section 15.2, "failed check, and expected first"`).
3. For `PROBE-P012-03-A`, a record-identity refusal before scenario output, **the mutated record path
   is the path member of the difference set** (`Design section 15.2, "failed check, and expected first"`).

Design v1.11 `Design v1.11 section 8, "row's `expected_first_changed_node` is `/RESULT_SURFACE/admitted"` names that path for `PROBE-P012-03-A`:

> Now that the record bytes exist, this probe's `expected_first_changed_node` is the record path whose
> bytes were mutated, `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json`, not
> a placeholder.

Design v1.11 `Design v1.11 section 15.2, "is a convenience locator only."` authorises the `design_lines` refresh performed in W262-4:

> `design_lines` in a catalog row is a convenience locator only. The authority is the probe id's
> normative sentence found by text in this design, so the tables family may refresh stale line numbers
> without a design change.

The comparator values below are **not** derived by this family; they are read as evidence of what the
comparator does from lane W256's measured ten-probe table
(`C:\WP012BUILD\W256_PROBES_REPORT.md:171-182`). No kernel, driver, verifier or baseline was executed
by this lane, no `observed/` path was read, and `mtc_v2.core` was not imported (design `Design section 15.2, "changing the base scenario, or"`).

### W262-2 `expected_first_changed_node` — per-row before and after

The "design-named node" column of §10 (`Design section 23.1, "add an object node without"`) and each probe's normative design sentence are
the authority for the *after* value; the W256 column is the authority for the comparator value.

| Probe | Before | After | Why | Design cite (v1.11) |
|---|---|---|---|---|
| `PROBE-P012-01-A` | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/fill_events/0/quantity` — unchanged | already the design-named target; `Design section 15.2, "or `GATE`), expected failed check"` only removes the first-node requirement | `Design section 7, "stop returns zero; `RULE2-01-GREEN` still"` ("must refuse at the quantity node") |
| `PROBE-P012-01-B` | `/EVENT_SURFACE/fill_events/0/quantity` | `/EVENT_SURFACE/fill_events/0/quantity` — unchanged | already the design-named target | `Design section 7, "so a supplied binary64 NaN"` |
| `PROBE-P012-02-A` | `/RESULT_SURFACE/admitted` | `/RESULT_SURFACE/admitted` — unchanged | already the design-named target, and the measured comparator node is the same | `Design section 8, "refuses. The RULE-2-GREEN cross-version check"` ("the admission/refusal projection") |
| `PROBE-P012-03-A` | `BLOCKED-MISSING-RECORD-BYTES` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | the record bytes exist; the mutated record path is the path member of the difference set | `Design section 8, "The RULE-2-GREEN cross-version check must"` + `Design section 8, "The RULE-2-GREEN cross-version check must"` + `Design section 15.2, "modification-manifest path/digest below `PROBE_ROOT`, target"` |
| `PROBE-P012-04-A` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/fill_events/0/final_fill_price` — unchanged | already the design-named target; the three earlier-sorting nodes no longer compete for the field | `Design section 10, "gap/open reference `90` and final"` ("must refuse at the fill-price node") |
| `PROBE-P012-05-A` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/fill_events/0/final_fill_price` — unchanged | already the design-named target | `Design section 12, "step, stop, two targets, target"` |
| `PROBE-P012-05-B` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `/EVENT_SURFACE/fill_events/0/final_fill_price` — unchanged | already the design-named target, and the measured comparator node is the same | `Design section 12, "unchanged. The corrected-expectation check must refuse at the first"` |
| `PROBE-P012-06-A` | `/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids/0` | `/EVENT_SURFACE/fill_events/0/exit_id` | the row carried the earlier-sorting node under D-14; the design names the first *fill* (`TARGET-NEAR` vs `TARGET-FAR`), and §10 `Design section 23.1, "containers—`decision_events`, `fill_events`, `cash_events`, `fee_events"` records `/EVENT_SURFACE/fill_events/0/exit_id` as the design-named node. It is a changed node: the reversal changes it | `Design section 12, "the same position, quantity step"` + `Design section 15.2, "OBSERVED`, `KERNEL`, or `GATE`), expected"` |
| `PROBE-P012-07-A` | `/EVENT_SURFACE/cash_events/1/signed_delta` | `/EVENT_SURFACE/fee_events/1/liquidity_role` | same class as 06-A: §10 `Design section 23.1, "containers—`decision_events`, `fill_events`, `cash_events`, `fee_events"` records the event-role node as the design-named node, and the catalog row's own note says so. It is a changed node: taker becomes maker | `Design section 14, "has no funding cashflow and"` ("the event-role/rate/fee nodes") + `Design section 15.2, "and expected first changed node/path."` |
| `PROBE-P012-08-A` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | same class: §10 `Design section 23.1, "containers—`decision_events`, `fill_events`, `cash_events`, `fee_events"` and the catalog row's own note record the typed funding projection as the node the design names. It is a changed node: the sign flip changes it | `Design section 15.2, "OBSERVED`, `KERNEL`, or `GATE`), expected"` ("the cash-delta node") + `Design section 15.2, "OBSERVED`, `KERNEL`, or `GATE`), expected"` |

Seven of the ten `expected_first_changed_node` values are unchanged. Three moved from an
enumeration-order node back to the design-named target node the same rows already identified in
prose, because v1.11 gives the enumeration-order node its own field. One placeholder was replaced.

### W262-3 `comparator_first_differing_node` — the member added, with its measured value

Each value below is the "Measured node" cell of the W256 ten-probe run at the cited line. This family
measured nothing; it copied the measurement and cites it.

| Probe | `comparator_first_differing_node` (new member) | W256 cite | W256 status |
|---|---|---|---|
| `PROBE-P012-01-A` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `C:\WP012BUILD\W256_PROBES_REPORT.md:173` | NOT_DETECTED under the superseded v1.10 rule |
| `PROBE-P012-01-B` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `C:\WP012BUILD\W256_PROBES_REPORT.md:174` | NOT_DETECTED under the superseded v1.10 rule |
| `PROBE-P012-02-A` | `/RESULT_SURFACE/admitted` | `C:\WP012BUILD\W256_PROBES_REPORT.md:175` | DETECTED |
| `PROBE-P012-03-A` | `core/economic_records/instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json` | `C:\WP012BUILD\W256_PROBES_REPORT.md:176` | NOT_DETECTED under the superseded v1.10 rule |
| `PROBE-P012-04-A` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `C:\WP012BUILD\W256_PROBES_REPORT.md:177` | NOT_DETECTED under the superseded v1.10 rule |
| `PROBE-P012-05-A` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `C:\WP012BUILD\W256_PROBES_REPORT.md:178` | NOT_DETECTED under the superseded v1.10 rule |
| `PROBE-P012-05-B` | `/EVENT_SURFACE/fill_events/0/final_fill_price` | `C:\WP012BUILD\W256_PROBES_REPORT.md:179` | DETECTED |
| `PROBE-P012-06-A` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `C:\WP012BUILD\W256_PROBES_REPORT.md:180` | NOT_DETECTED under the superseded v1.10 rule |
| `PROBE-P012-07-A` | `/EVENT_SURFACE/cash_events/1/signed_delta` | `C:\WP012BUILD\W256_PROBES_REPORT.md:181` | DETECTED |
| `PROBE-P012-08-A` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `C:\WP012BUILD\W256_PROBES_REPORT.md:182` | DETECTED |

W256 also records why five of these are `cash_events/0/signed_delta`: the comparison walks object keys
in UTF-8 order, so `cash_events` precedes `decision_events`, `fee_events`, `fill_events` and
`funding_events` (`C:\WP012BUILD\W256_PROBES_REPORT.md:184`). That is exactly the traversal order
design `Design section 15.2, "design_lines` in a catalog row"` now states.

### W262-4 `design_lines` — per-row before and after, re-measured against v1.11

Each probe's normative sentence was found **by text** in v1.11 and its current line written, as
`Design section 15.2, "normative sentence found by text"` permits. The sentences are the eight `Fail probe`/`Fail probes` sentences of sections 7-14
(`Design section 7, "Fail probes: `PROBE-P012-01-A` replaces the",Design section 8, "fail:** the second sentence of",Design section 9, "Fail probe `PROBE-P012-03-A`: mutate one",Design section 10, "Fail probe `PROBE-P012-04-A`: return stop",Design section 11, "Fail probes: `PROBE-P012-05-A` omits the",Design section 12, "Fail probe `PROBE-P012-06-A` binds exactly",Design section 13, "Fail probe `PROBE-P012-07-A`: classify one",Design section 14, "Fail probe `PROBE-P012-08-A`: flip the").

| Probe | Before | After | Sentence found by text at |
|---|---|---|---|
| `PROBE-P012-01-A` | Design v1.10 section 7, "corrected expected producer remains at" | Design v1.11 section 7, "corrected expected producer remains at" | "`PROBE-P012-01-A` replaces the corrected multiplier with `1` …" |
| `PROBE-P012-01-B` | Design v1.10 section 7, "corrected expected producer remains at" | Design v1.11 section 7, "corrected expected producer remains at" | "`PROBE-P012-01-B` changes the corrected selector …" (same sentence line) |
| `PROBE-P012-02-A` | Design v1.10 section 8, "leverage-cap quantity `100`, and floored" | Design v1.11 section 8, "leverage-cap quantity `100`, and floored" | "Fail probe `PROBE-P012-02-A`: change the corrected comparison to `>` …" |
| `PROBE-P012-03-A` | Design v1.10 section 9, "probe `PROBE-P012-03-A`: mutate one record" | Design v1.11 section 9, "probe `PROBE-P012-03-A`: mutate one record" | "Fail probe `PROBE-P012-03-A`: mutate one record byte …" |
| `PROBE-P012-04-A` | Design v1.10 section 10, "PROBE-P012-04-A`: return stop `100` rather" | Design v1.11 section 10, "PROBE-P012-04-A`: return stop `100` rather" | "Fail probe `PROBE-P012-04-A`: return stop `100` rather than open `90` …" |
| `PROBE-P012-05-A` | Design v1.10 section 11, "omits the application (actual `100" | Design v1.11 section 11, "omits the application (actual `100" | "Fail probes: `PROBE-P012-05-A` omits the application …" |
| `PROBE-P012-05-B` | Design v1.10 section 11, "omits the application (actual `100" | Design v1.11 section 11, "omits the application (actual `100" | "… and `PROBE-P012-05-B` applies it twice …" (same sentence line) |
| `PROBE-P012-06-A` | Design v1.10 section 12, "kind `KERNEL`. Its sole" | Design v1.11 section 12, "kind `KERNEL`. Its sole" | "Fail probe `PROBE-P012-06-A` binds exactly once …" |
| `PROBE-P012-07-A` | Design v1.10 section 13, "PROBE-P012-07-A`: classify one declared taker" | Design v1.11 section 13, "PROBE-P012-07-A`: classify one declared taker" | "Fail probe `PROBE-P012-07-A`: classify one declared taker exit as maker." |
| `PROBE-P012-08-A` | Design v1.10 section 14, "probe `PROBE-P012-08-A`: flip the sign" | Design v1.11 section 14, "probe `PROBE-P012-08-A`: flip the sign" | "Fail probe `PROBE-P012-08-A`: flip the sign for the long positive-rate event." |

The v1.10 sentence lines W256 recorded
(`C:\WP012BUILD\W256_PROBES_REPORT.md:251`) were Design section 7, "Those selector branches exactly preserve"; Design section 8, "fail:** the second sentence of"; Design section 9, "mutate one record byte without updating the detached digest"; Design section 10, "Trigger | Reference fill before slippage"; Design section 11, "1`; any second application is"; Design section 12, "subject_producer_id=KERNEL_2`, and target kind `KERNEL"; Design section 13, "projection of exactly one fee-kind"; Design section 14, "final sentence.** The retained sentence"; W261's
insertion at design `Design section 8, "the second sentence of the"` moved every sentence after section 9 down by six lines, which is
exactly the difference between those and the values written here.

### W262-5 Notes — what was appended and what was retained

Every original `note` string is retained verbatim; text was only appended to the end of it.

- `PROBE-P012-01-A`, `PROBE-P012-04-A`, `PROBE-P012-06-A` — the three notes that recorded the **D-14**
  ordering ambiguity. Each gains one sentence saying v1.11 closed it and how: `:481-493` requires only
  membership in the changed-node set and records the comparator node separately.
- `PROBE-P012-03-A` — one sentence recording that the record bytes now exist, that `:272-276` names
  the real record path, and that **D-15** is closed for that field.
- `PROBE-P012-07-A`, `PROBE-P012-08-A` — one sentence each recording the re-derivation of the field to
  the design-named node and the comparator node beside it.
- `PROBE-P012-05-A` — one sentence. Its note claimed `final_fill_price` "is the first changed node";
  that is true only within the fill row, and W256 measured `cash_events/0/signed_delta` first. The
  claim is superseded, not deleted.
- `PROBE-P012-01-B`, `PROBE-P012-02-A`, `PROBE-P012-05-B` — notes untouched. They record no ordering
  claim that v1.11 changes.

### W262-6 What this lane did not do

- No `modified_copy_digest` or `modification_manifest_digest` was touched. All twenty remain
  `BLOCKED-BUILD-ARTIFACT`, the honest marker. W256 measured the real digest pairs
  (`C:\WP012BUILD\W256_PROBES_REPORT.md:110-120`); pinning them is the Lead's two-party act at
  re-seal #10.
- No `RED`/`GREEN` catalog row, no golden artifact, no `CONTRACT_TABLES_MANIFEST.json`, no
  `IMPLEMENTATION_ANCHOR_DRAFT.json` and no numeric content anywhere in this worksheet was edited.
- **STALE PINS, two of them.** `CONTRACT_TABLES_MANIFEST.json:150-152` pins `scenario_catalog.json` at
  `f8e788d808f26c42…` / 40893 bytes and `:145-147` pins `DERIVATIONS.md` at `a8440a1250fed65e…` /
  260783 bytes. Both files now differ. Re-pinning and re-seal #10 are the Lead's acts under design
  `Design section 23.5, "nodes, then the Lead must"`, as at re-seals #2, #3, #4, #8 and #9.
- No kernel read or run, no `observed/` read, no verifier, driver or baseline executed, no
  `mtc_v2.core` import, no repository write outside this bundle. The measured probe nodes were read
  from lane W256's committed report only.
- No design edit. v1.11 is W261's act; this lane derived from its text.
- **W262-D01** — the line-number consequence, measured by diff against
  `C:\tmp\SNAPSHOTS\20260902_1400_preW262\DERIVATIONS.md`. This pass is insertion-only: **0 lines
  deleted or rewritten**. It inserted a 13-line marker block after pre-pass line `:1026`
  (hunk `1026a1027,1039`), a 7-line marker block after `:1089` (hunk `1089a1103,1109`), a 9-line
  marker block after `:1093` (hunk `1093a1114,1122`), and appended this section after the pre-pass
  last line `:3773`. A citation into this worksheet at or above `:1026` still lands where it did; one
  in `:1027-1089` sits 13 lines lower; one in `:1090-1093` sits 20 lines lower; one at `:1094` or
  below sits 29 lines lower. This is the class W224 recorded as W224-D01 and W244 as W244-D01, and is
  recorded, not repaired.


## Re-seal #12 - nine KERNEL probe digests re-pinned (2026-09-02 23:3x, Lead act under owner decision 132)

The authorized kernel repairs (W283..W285, W284 item 0) changed `mtc_v2/core`; the nine KERNEL probes pinned the pre-fix tree `2c749345ed9be5186659369f091ce77a2e42d61a`. W299 re-derived each variant over the repaired tree `e8e250589d6b5a887e6f1a77874405836772d4bd` by applying the unchanged `modification.patch` (patch bytes, expected check and expected first-changed node unchanged; one base-relative change `economics.py` per variant). The Lead recomputed both digests per probe from the committed bytes (two-party pin) and wrote them into the PROBE rows; no RED/GREEN row, golden, input or derivation value moved.

| probe | modification_manifest_digest | modified_copy_digest |
|---|---|---|
| PROBE-P012-01-A | `a2329ab11a87751862453cad8942332b3b54108c9f294656635a7eb9f849c87e` | `7b93a0dd06421ae979d0dc6736402d778cada45d2fc7aba4767ebb029093d12a` |
| PROBE-P012-01-B | `cab810b62324678258bea30250788bb8f4c6097d75d50bdf3ad075664beff762` | `d8eae81dbcc4648a1a8dafa65c890e713eed965129002118c14330abb6c9aad6` |
| PROBE-P012-02-A | `eebbcde982c72aec02584714cfbba0bf10468249576411649a2bbb0617d1240f` | `ff4592347f00b7187513665a07c02d4d7108909de9796cb6fd7527da2d4d941f` |
| PROBE-P012-04-A | `9f44a7cd0ed4b6984232455bfe118904d05eefa7976f96127caf67a4cdc64102` | `dc313ee4328eecaad6ef34408cd4ab4838254589e213e4448c3540f71cf5ba92` |
| PROBE-P012-05-A | `684637b72cf10ceaf740452b46878427bce8dd33855c64ec23670e9e5b9cc81c` | `216152ca35050558068fc24e1d64df7473296a6b7048c1b3515720dbf8f8d294` |
| PROBE-P012-05-B | `ecb0bc2559c65ed920128adb085ff1c97726f7595ca002748e5c70563c7824da` | `009890b989aeba839d40585a6b1a489a1e26ae0928d543fbba56a7b449ac1b79` |
| PROBE-P012-06-A | `f54132eda453169414d4e7c16e70edfe257f55ccb3f1ec1c7bfc2f1e59610902` | `fa51d604ef31863ae91f932ef32e95b2a9d72a0a924acdb0406fcadc4f371841` |
| PROBE-P012-07-A | `c9f81cec21a789f4131f333a501b8260ef8ca3ede884df6b197eef3ab9a6a1e5` | `ea91b62f48edbb9ff15072a763f7255daf88c067bcab9645e7d3b4fc5b63e4da` |
| PROBE-P012-08-A | `d976769490645ea5fefefbe7e44b0921807bdc561b3f9e77293601f8068823c9` | `48e63ab55bbd160d0d5f2b50747aac65674af91893dc35ce796d6bd1cfc8b95a` |


## Re-seal #13 - nine KERNEL probe variants rebuilt on the final core and re-pinned (2026-09-03, Lead act under owner decision 132)

W299's variants (re-seal #12) had been patched onto the old variant trees, so fourteen repaired core files stayed stale inside them and the gate refused PROBE_KERNEL_DIFF_INVALID. W299B deleted each variant and recreated it as a byte-for-byte copy of the final core tree `457a06d6e5e67b255c2830be8989f4e0610fba63` plus the unchanged `modification.patch` (one changed file per variant). The Lead recomputed both digests per probe from the committed bytes (two-party pin); no RED/GREEN row, golden, input or derivation value moved.

| probe | modification_manifest_digest | modified_copy_digest |
|---|---|---|
| PROBE-P012-01-A | `dcad00109d4f0ceb49e01f644fbfb167b69fac5ef23f85ac4dd0c76a6b729643` | `bf3d60086b94fc6ac1987ac3be48d4043295c046b3bf965d8f0db1bc082c1d5f` |
| PROBE-P012-01-B | `3721ff47900bb4d134827206009012b48d94e845c162ce18f3f852f15b289ba2` | `a68dd872f75977c85931c762d24f6525a53e978ee633aff023c14644e5ed9d8a` |
| PROBE-P012-02-A | `f37e6d9f3443292d9458ec5de609c1b4854fa2b4f67a3289b64ff9fdf91036c8` | `0e51bd03658fa54a255560459038abfadd030aac8e65b703dcfaedf9aa15f316` |
| PROBE-P012-04-A | `24f70876403398f1663a659bdc1a63b44af355f5d4118c02ed4e95c94b7c0d72` | `c35479033870e5c1811626ce623ca67a4a779bf3dea66f03375d2f8fa4022f9c` |
| PROBE-P012-05-A | `44251938704af7f92d1e880b4dd3b4239c21ac927daae4db3840fc23c19643d5` | `59eff888dbb654e8cda576132fe4244aa7f2a3f7d55f7501e620a716586838ac` |
| PROBE-P012-05-B | `709a543786be9a07e77d1b81f6676d6c95c5bd027248e0aa85ea4dad78198661` | `41844cf3db3790a028cd6bf71f7859ec90db94bb83083fb07785b76497090365` |
| PROBE-P012-06-A | `39c8af08f17c7bf3f8d7c689b8ce0db7d3d1ee8504aa5fedf5d401c0149e5380` | `2fe755a71836585361592e9bd3b913f843ccb3a9c0ba523a44e1d65561048869` |
| PROBE-P012-07-A | `57fee87191150d2afb983017339e1cec1a63faed80694155af803313afd40f37` | `b65811b6d77e376d34ffad34b7210cf6a0f983ee3bdf9c5efd0c2e88c4ca2e9c` |
| PROBE-P012-08-A | `96aaa32930b1bfff487fadb7cdea34e14408e62fe939787c0c5e162ddb35c47d` | `98e73b51a0ee3ac05a285a8a0710f73ea0a9e621171317b4806cf0eb335c04c1` |

## W311 - sealed-input changes M1 (owner decision 137) and M7 (owner decision 139) (2026-09-03, tables family, insertion-only)

Authority: `C:\WLDOCS\MTC_COMMAND_CENTER\11_TRIAGE\OWNER_DECISIONS_2026-08-29_EVENING.md:1150` (addendum 45),
items `137` (M1) and `139` (M7). Owner's fence, verbatim: "Keep every change strictly limited to those items."
No golden, probe, design, manifest-seal or anchor byte was touched; the Lead re-seals.

### M7 (decision 139) - `RULE2-06-EQUAL-PRICE-RED` receives its sealed corrected-only `target_book`

Changed input: `tests/corrected_vnext/contracts/inputs/RULE2-06-EQUAL-PRICE-RED.json`.

| | sha256 | bytes |
|---|---|---|
| before | `5972c66c0fbb5e357f548daaf5fdd2ed0dd42fd948229235260bdbe6c2dee978` | 1833 |
| after | `0c65c82b911f3a510d074df00bc81335bb3397697e96f422f5c05267e4ea085c` | 1908 |

Exact JSON delta - one added member at `/corrected_only/economic_inputs/target_book`; no other member of the
document was added, removed or changed:

```json
{"TP1":["TARGET-NEAR",105,0.5],"TP2":["TARGET-FAR",105,0.5]}
```

Design lines the values are quoted from (no number is invented):

- Design section 12, "quantity step, stop, two targets" (section 12): "`RULE2-06-RED` is a synthetic long
  ... stop `90`, target `TARGET-NEAR` at `105` with target fraction `0.5`, target `TARGET-FAR` at `110` with
  target fraction `0.5` ... `RULE2-06-EQUAL-PRICE-RED` ... uses the exact `RULE2-06-RED` inputs except that
  `TARGET-FAR` is also at `105`."
- Design section 22.1, "whose sole member is `same_bar_collision_policy_id=" (section 22.5, the equal-price scenario row):
  "Corrected book remains the section-12 stated `TARGET-FAR=105`, `TARGET-NEAR=105`, fractions `.5/.5`, policy
  `TARGET_FIRST`".
- Design section 22.1, "whose sole member is `same_bar_collision_policy_id=" (section 22.5, the `RULE2-06-RED` row) supplies the
  alias direction: "corrected aliases TP1/TP2 mechanically to the stated `TARGET-NEAR`/`TARGET-FAR` ids and uses
  stated fractions `.5/.5`". `TP1` therefore carries `TARGET-NEAR` and `TP2` carries `TARGET-FAR`.

Arithmetic (design-stated; restated only to show that the equal-price override is the sole difference from
`RULE2-06-RED`): the sealed config carries entry-bar close `100`, `sl_percent=10`, `tp1_r_multiple=0.5` and
`tp2_r_multiple=1` (`tests/corrected_vnext/contracts/inputs/RULE2-06-EQUAL-PRICE-RED.json:1`). Risk per unit is
`100 * 10 / 100 = 10`, so legacy Multi-TP builds `TP1 = 100 + 10 * 0.5 = 105` and `TP2 = 100 + 10 * 1 = 110`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:264-286` at branch HEAD `ac2d2ca9`). The
equal-price scenario differs only in that design `Design section 12, "target fractions, tick, test-only zero-impact"` places `TARGET-FAR` at `105` as well, so the sealed book
carries `105` for both ids. Fractions `0.5`/`0.5` applied to reference quantity `2` give quantity `1` per target,
as design `Design section 12, "with full bar `open=100, high=104"` states.

Transport shape (`MECHANICAL`, not an economic value): the gate reads the member as an object keyed by the legacy
working-exit id, whose value supplies `(exit_id, target_price, qty_fraction)`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1207-1226,1329-1340` at
branch HEAD `ac2d2ca9`). Bytes are canonical per design `Design section 22.2, "is explicit in input bytes"`: sorted keys, `(',',':')` separators, UTF-8, LF
line endings, one final LF - byte-identical round-trip verified against the pre-change file.

### M1 (decision 137) - NOT PERFORMED: `DESIGN-GAP`, no cost record is named and none exists

The lane instruction is to bind the cost record "the design's scenario row names" and, "if the design names none,
STOP and report DESIGN-GAP (do not invent a record)". The design names none, and refuses one:

- Design section 22.3, "values stated in §14 and" (section 22.1): "both cost members are JSON `null`
  only for RULE2-08, where section 14 says no cost schedule is consumed".
- Design section 15.2, "GREEN row, and every declared" (section 14): "Neither vector contains a fill intent,
  so section 3's fill-only slippage sequence is not entered and no slippage value or `CostSchedule` is consumed."
- Design section 22.1, "members are JSON `null` only for RULE2-08, where section 14 says no cost" and Design section 22.1, "members are JSON `null` only for RULE2-08, where section 14 says no cost" (section 22.6, both RULE2-08 rows): "C is
  absent/`NOT_CONSUMED`."

No candidate exists either: branch `feature/wp-p0-12-corrected-vnext-20260831` at HEAD `ac2d2ca9` carries sixteen
sealed cost records under
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economic_records/costs/`
(`HYPERLIQUID-BTC-PERP-BASE-TIER0-V1`, `SYNTH-COST-RULE2-01-RED/GREEN-V1` through `SYNTH-COST-RULE2-07-RED/GREEN-V1`,
and `SYNTH-COST-RULE2-06-EQUAL-PRICE-RED-V1`); there is no `SYNTH-COST-RULE2-08-*` record. The listing was taken
read-only with `git -C C:\WP012BUILD ls-tree -r --name-only HEAD`; nothing under `C:\WP012BUILD` was written.

`RULE2-08-RED.json` and `RULE2-08-GREEN.json` are therefore unchanged
(`5136b0ce11f9e7b949e8b5105ce128df65ffcaf3ba0399f27141978ef341b0c1` and
`3cb3cf0db3ab22134449f07c1c90e738a643736e16f97860889d80a08ebb900d`, identical before and after this lane), their
catalog rows are untouched, and the pre-existing conflict recorded above at `DERIVATIONS.md:1735-1741` (V15-D01)
stands unresolved. Closing M1 requires an owner-gated design amendment that either names a RULE2-08 cost record or
withdraws the pre-window fill premise.

### Catalog rows changed by this section

One row only: `scenario_catalog.json` index `11`, `scenario_id="RULE2-06-EQUAL-PRICE-RED"`, member `/input/digest`
re-pinned from `5972c66c...` to `0c65c82b...`. That row has no `input.bytes` member. No other catalog member
changed. `scenario_catalog.json` sha256 before `bdfb42e7058df08cd57ea9c57434784e452676be16ea61be7324f2f866148742`,
after `a9ba2a89a1de83b4ba9687b3f9708ee8ca8fc1b15f36c737bd115586cdf051f6` (49676 bytes both).

## W312 - M6 sealed RULE-2 projections and M4 probe/collision re-derivation (owner decisions 138 and 140) (2026-09-03, tables family, insertion-only)

Authority: ledger addendum 45, owner decisions `138` (M6) and `140` (M4). Lane spec
`C:\tmp\LANE_PROMPTS_20260828\LANE_W312_TABLES_M6_M4.md`. Design file read as it stands:
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`, whose own title line `Design section 23.12, "decisions 138 and 143, 2026-09-03"` says **v1.13**
(the lane spec says v1.12 - recorded as a discrepancy in the lane report). Every design citation
below is a measured line number of that v1.13 file, not a carried-forward v1.8 number.

No kernel was executed, no observed artifact was read, and no design, input, manifest-seal, anchor
or probe-manifest byte was written. The only bundle file changed by this lane is
`scenario_catalog.json` (fifteen rows gain one declared-projection member each) plus this
insertion-only worksheet entry.

### W312-A. What the harness names and what the design defines

`build_projection_results` at branch `feature/wp-p0-12-corrected-vnext-20260831` HEAD `8b9e2964`
(`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3424-3449`,
read read-only through `git show`) refuses `EXPECTATION_UNSEALED` with pointer
`/rule2_divergent_projection` for a `RED` row and `/rule2_green_projection` for a `GREEN` row
(`:3441-3443`, `:3445-3449`). Those two member names on the catalog row are therefore the members
the harness reads. The pipeline records the typed refusal and stops the projection claim at
`:3682-3691`; the probe path reaches the same refusal through `_green_projection_differences`
(`:2992-3009`) from the `RULE2_GREEN_CROSS_VERSION_EXPECTATION` branch at `:3083-3096`.

The design defines the member's content, not the harness: design `Design section 6, "175 and `rule2_green_projection[]` at line"` `rule2_divergent_projection[]`
is "exact nodes that must differ", `Design section 6, "175 and `rule2_green_projection[]` at line"` `rule2_green_projection[]` is "exact behavioral nodes that
must agree", and `Design section 15.3, "Differs” means the two tagged"` says each declared member "is a pair of version-local node selectors" whose
sides resolve to `PRESENT(node_kind, canonical_value)`, `ABSENT` or `REFUSAL(refusal_code)`, with
present-versus-absent, present-versus-refusal, absent-versus-refusal, distinct refusal codes and
unequal present values or kinds all counting as divergence. `:555` requires every RED scenario to
differ at every declared node and `:556` requires the named GREEN projection to be equal.

Sealed member shape, one object per declared node:

```text
selector            the node the design names (an RFC 6901 pointer, or the design's own
                    non-pointer projection name where the design names a consumed value)
legacy              the 1.0.0 tagged state: tag PRESENT/ABSENT/REFUSAL, node_kind, value,
                    source DESIGN_DERIVED, design_lines, and where one exists an advisory
                    baseline_selector_advisory path
corrected           the 2.0.0 side: a version-local selector into the sealed CONTRACT_TABLES
                    artifact plus its node_kind, or a declared REFUSAL where the design says
                    the corrected run consumes nothing
expected_relation   DIFFERS for a divergent member, EQUAL for a GREEN member
derivation          the W312-M6 entry id in this worksheet
```

`node_kind` uses the design `Design section 15.3, "canonical string, so that GATE_READER"` enumerator letters (`I`, `F`, `S`, `B`, `N`, `A`, `O`) and the
`value` member carries the raw value, not a hand-encoded canonical string, so the gate applies its
own `canonical_node` (`verify_bceg.py:514-530`) to it. The corrected side is a selector rather than a
pinned value because design `Design section 15.3, "carries `sequence`, including an empty"` name `CONTRACT_TABLES` itself as the right-hand producer: the
sealed golden is the expectation, and duplicating its bytes here would create a second seal that can
drift. Every corrected selector below was resolved against its golden this session and its resolved
canonical node is quoted.

### W312-B. Per-value derivations, fifteen rows, fifty-five sealed members

Rows sealed: nine RED (`RULE2-01-RED`, `-02-RED`, `-03-RED`, `-04-RED`, `-05-RED`, `-06-RED`,
`RULE2-06-EQUAL-PRICE-RED`, `-07-RED`) - eight of the nine; and six GREEN (`RULE2-01-GREEN` through
`RULE2-07-GREEN`) - six of the eight. `RULE2-08-RED` and `RULE2-08-GREEN` are **STOPPED, nothing
derived, no byte written**, per the lane's M1-pending instruction: "waits for owner M1b".

#### RULE2-01-RED - `rule2_divergent_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fill_events/0/quantity` | PRESENT(I:10) | PRESENT(`I:5`) | DIFFERS |
| 2 | `/RESULT_SURFACE/final_position/quantity` | PRESENT(I:10) | PRESENT(`I:5`) | DIFFERS |
| 3 | `/RESULT_SURFACE/order_notional` | PRESENT(I:2000) | PRESENT(`I:1000`) | DIFFERS |

- **W312-M6-01R-1** - legacy risk_raw_qty = 100 / (|100-90|) = 10 ; corrected = 100 / (10 * cm 2) = 5 (Design section 7, "notional, later position quantity, and" states legacy 10 versus corrected 5)
- **W312-M6-01R-2** - the entry fill quantity is the position quantity after entry: legacy 10, corrected 5 (Design section 7, "notional, later position quantity, and")
- **W312-M6-01R-3** - legacy order_notional = 10 * 100 * 2 = 2000 ; corrected = 5 * 100 * 2 = 1000 (Design section 7, "notional, later position quantity, and" order-notional projection)

#### RULE2-01-GREEN - `rule2_green_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fill_events/0/quantity` | PRESENT(I:1) | PRESENT(`I:1`) | EQUAL |
| 2 | `/RESULT_SURFACE/final_position/quantity` | PRESENT(I:1) | PRESENT(`I:1`) | EQUAL |
| 3 | `/RESULT_SURFACE/order_notional` | PRESENT(I:100) | PRESENT(`I:100`) | EQUAL |

- **W312-M6-01G-1** - non-finite stop -> fallback on both versions: fallback_notional = 1000 * 10/100 = 100 ; raw_qty = 100 / (100 * 1) = 1 on both (Design section 7, "uses `execution_profile_id=close_only_deterministic_v2`, sizing equity `1000" 'both final quantities are 1')
- **W312-M6-01G-2** - same fallback quantity 1 carried to the position (Design section 7, "uses `execution_profile_id=close_only_deterministic_v2`, sizing equity `1000")
- **W312-M6-01G-3** - order_notional = 1 * 100 * 1 = 100 on both versions (Design section 7, "uses `execution_profile_id=close_only_deterministic_v2`, sizing equity `1000")

#### RULE2-02-RED - `rule2_divergent_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/RESULT_SURFACE/refusals/0/code` | ABSENT | PRESENT(`S:20:UkVGVVNFRF9NSU5fTk9USU9OQUw=`) | DIFFERS |
| 2 | `/EVENT_SURFACE/fill_events` | PRESENT(A:1) | PRESENT(`A:0`) | DIFFERS |
| 3 | `/EVENT_SURFACE/decision_events/2/decision` | ABSENT | PRESENT(`S:20:UkVGVVNFRF9NSU5fTk9USU9OQUw=`) | DIFFERS |

- **W312-M6-02R-1** - 1.0.0 has no typed refusal object at all; 2.0.0 refuses because 100 >= 101 is false (Design section 8, "48`); the corrected frozen test", Design section 8, "48`); the corrected frozen test")
- **W312-M6-02R-2** - legacy rejects only when 100 < 0, which is false, so legacy opens and fills once (A:1); corrected opens no position, so fill_events is A:0 (Design section 8, "48`); the corrected frozen test", Design section 8, "48`); the corrected frozen test")
- **W312-M6-02R-3** - the typed refusal decision row exists only at 2.0.0; index 2 is the third and last decision row of this artifact after Reading Y removed the padded fourth row (Design section 8, "48`); the corrected frozen test")

#### RULE2-02-GREEN - `rule2_green_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/RESULT_SURFACE/admitted` | PRESENT(B:1) | PRESENT(`B:1`) | EQUAL |
| 2 | `/EVENT_SURFACE/fill_events/0/quantity` | PRESENT(I:1) | PRESENT(`I:1`) | EQUAL |
| 3 | `/RESULT_SURFACE/final_position/quantity` | PRESENT(I:1) | PRESENT(`I:1`) | EQUAL |

- **W312-M6-02G-1** - order_notional = 1 * 100 * 1 = 100 ; corrected admits iff 100 >= 100 (true) and legacy rejects iff 100 < 100 (false), so both admit (Design section 8, "uses its sourced default `min_notional=0", Design section 8, "uses its sourced default `min_notional=0"; the positive boolean is Design section 23.4, "Every `CORRECTED_V2` `RESULT_SURFACE` has exactly")
- **W312-M6-02G-2** - both versions size and fill quantity 1 (Design section 8, "uses its sourced default `min_notional=0")
- **W312-M6-02G-3** - both versions carry position quantity 1 (Design section 8, "uses its sourced default `min_notional=0")

#### RULE2-03-RED - `rule2_divergent_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/RESULT_SURFACE/refusals/0/code` | ABSENT | PRESENT(`S:41:UkVGVVNFRF9JTlNUUlVNRU5UX09WRVJSSURFX09OX0VWQUxVQVRJT04=`) | DIFFERS |
| 2 | `/EVENT_SURFACE/decision_events/1/decision` | ABSENT | PRESENT(`S:41:UkVGVVNFRF9JTlNUUlVNRU5UX09WRVJSSURFX09OX0VWQUxVQVRJT04=`) | DIFFERS |
| 3 | `consumed price_tick` | PRESENT(F:0x1.0000000000000p-2) | REFUSAL(REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION) | DIFFERS |

- **W312-M6-03R-1** - legacy accepts the runtime override and raises no refusal; corrected refuses before the first bar (Design section 8, "48`); the corrected frozen test", Design section 8, "48`); the corrected frozen test")
- **W312-M6-03R-2** - the pre-evaluation refusal decision row exists only at 2.0.0 (Design section 8, "48`); the corrected frozen test", Design section 8, "48`); the corrected frozen test")
- **W312-M6-03R-3** - legacy consumes runtime price_tick 0.25; corrected consumes no tick because it refuses before evaluation, which Design section 15.3, "KERNEL_1` to the exact unpadded" tags REFUSAL (Design section 8, "48`); the corrected frozen test")

#### RULE2-03-GREEN - `rule2_green_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/decision_events/1/runtime_value` | PRESENT(F:0x1.0000000000000p-1) | PRESENT(`F:0x1.0000000000000p-1`) | EQUAL |
| 2 | `/RESULT_SURFACE/refusals` | PRESENT(A:0) | PRESENT(`A:0`) | EQUAL |
| 3 | `/RESULT_SURFACE/final_position` | PRESENT(N) | PRESENT(`N`) | EQUAL |

- **W312-M6-03G-1** - price_tick 0.5 is supplied on both sides and every runtime field equals the frozen record, so the consumed tick is 0.5 on both (Design section 8, "frozen test record uses `min_notional=101")
- **W312-M6-03G-2** - no override mismatch, so neither version raises a refusal (Design section 8, "frozen test record uses `min_notional=101", Design section 8, "frozen test record uses `min_notional=101")
- **W312-M6-03G-3** - the vector states no entry or exit action, so no position exists on either version (Design section 8, "frozen test record uses `min_notional=101")

#### RULE2-04-RED - `rule2_divergent_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fill_events/0/reference_price` | PRESENT(I:92) | PRESENT(`I:90`) | DIFFERS |
| 2 | `/EVENT_SURFACE/fill_events/0/final_fill_price` | PRESENT(I:92) | PRESENT(`I:90`) | DIFFERS |
| 3 | `/EVENT_SURFACE/fill_events/0/fill_trigger` | ABSENT | PRESENT(`S:8:R0FQX09QRU4=`) | DIFFERS |

- **W312-M6-04R-1** - legacy close-only triggers and fills from close 92; corrected gap-aware takes open 90 as the reference because open 90 <= stop 100 (Design section 10, "corrected projection selects gap/open reference")
- **W312-M6-04R-2** - slippage_bps 0 so impact = |90| * 0 / 10000 = 0 ; sell -> 90 - 0 = 90 ; floor_to_price_tick(90, 1) = 90 versus legacy 92 (Design section 10, "the OPEN-06-contingent corrected projection selects", Design section 10, "the OPEN-06-contingent corrected projection selects", Design section 10, "the OPEN-06-contingent corrected projection selects")
- **W312-M6-04R-3** - fill_trigger is a 2.0.0-only node recording GAP_OPEN (Design section 10, "the OPEN-06-contingent corrected projection selects")

#### RULE2-04-GREEN - `rule2_green_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/exit_events` | PRESENT(A:0) | PRESENT(`A:0`) | EQUAL |
| 2 | `/EVENT_SURFACE/fill_events` | PRESENT(A:0) | PRESENT(`A:0`) | EQUAL |
| 3 | `/RESULT_SURFACE/final_position/quantity` | PRESENT(I:1) | PRESENT(`I:1`) | EQUAL |

- **W312-M6-04G-1** - corrected: open 105 <= stop 100 false and low 101 <= stop 100 false -> no stop; legacy: close 104 > stop 100 -> no hit; no exit on either version (Design section 10, "fills at close `92`; the")
- **W312-M6-04G-2** - no exit means no fill on either version (Design section 10, "fills at close `92`; the", Design section 10, "fills at close `92`; the")
- **W312-M6-04G-3** - the existing long of quantity 1 survives the bar on both versions (Design section 10, "fills at close `92`; the")

#### RULE2-05-RED - `rule2_divergent_projection` (4 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fill_events/0/reference_price` | ABSENT | PRESENT(`I:100`) | DIFFERS |
| 2 | `/EVENT_SURFACE/fill_events/0/slippage_impact` | ABSENT | PRESENT(`I:1`) | DIFFERS |
| 3 | `/EVENT_SURFACE/fill_events/0/final_fill_price` | PRESENT(I:100) | PRESENT(`I:101`) | DIFFERS |
| 4 | `/EVENT_SURFACE/fill_events/0/slippage_application_count` | ABSENT | PRESENT(`I:1`) | DIFFERS |

- **W312-M6-05R-1** - 1.0.0 records no pre-slippage reference; 2.0.0 records reference 100 (Design section 12, "/`110`, leaving no stop", Design section 12, "/`110`, leaving no stop")
- **W312-M6-05R-2** - impact = |100| * 100 / 10000 = 1, a 2.0.0-only node (Design section 12, "/`110`, leaving no stop", Design section 12, "/`110`, leaving no stop")
- **W312-M6-05R-3** - legacy passes the reference through unadjusted at 100; corrected buy -> 100 + 1 = 101 ; ceil_to_price_tick(101, 0.01) = 101 (Design section 12, "/`110`, leaving no stop", Design section 12, "/`110`, leaving no stop")
- **W312-M6-05R-4** - slippage is applied exactly once, a 2.0.0-only count node (Design section 12, "/`110`, leaving no stop", Design section 12, "/`110`, leaving no stop")

#### RULE2-05-GREEN - `rule2_green_projection` (1 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fill_events/0/final_fill_price` | PRESENT(I:100) | PRESENT(`I:100`) | EQUAL |

- **W312-M6-05G-1** - impact = |100| * 0 / 10000 = 0 ; buy -> 100 + 0 = 100 ; ceil_to_price_tick(100, 0.01) = 100, equal to the legacy pass-through 100 (Design section 12, "low=85, close=95`; only the stop")

#### RULE2-06-RED - `rule2_divergent_projection` (6 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fill_events/0/exit_id` | PRESENT(S, value not pinned) | PRESENT(`S:11:VEFSR0VULU5FQVI=`) | DIFFERS |
| 2 | `/EVENT_SURFACE/fill_events` | PRESENT(A:1) | PRESENT(`A:2`) | DIFFERS |
| 3 | `/EVENT_SURFACE/fill_events/0/final_fill_price` | PRESENT(I:90) | PRESENT(`I:105`) | DIFFERS |
| 4 | `/EVENT_SURFACE/fill_events/1/final_fill_price` | ABSENT | PRESENT(`I:110`) | DIFFERS |
| 5 | `/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids` | ABSENT | PRESENT(`A:2`) | DIFFERS |
| 6 | `/RESULT_SURFACE/trades/0/gross_realized_pnl` | PRESENT(I:-20) | PRESENT(`I:15`) | DIFFERS |

- **W312-M6-06R-1** - legacy's implicit stop-first path exits at the stop; corrected TARGET_FIRST orders long targets by ascending price, 105 < 110, so the first corrected fill is TARGET-NEAR (Design section 12, "tick, test-only zero-impact model/parameter record", Design section 12, "tick, test-only zero-impact model/parameter record", Design section 12, "tick, test-only zero-impact model/parameter record")
- **W312-M6-06R-2** - legacy exits the full quantity 2 in one fill (A:1); corrected exits 0.5 * 2 = 1 at TARGET-NEAR then 0.5 * 2 = 1 at TARGET-FAR, leaving remainder 2 - 1 - 1 = 0, so A:2 (Design section 12, "tick, test-only zero-impact model/parameter record", Design section 12, "tick, test-only zero-impact model/parameter record")
- **W312-M6-06R-3** - legacy stop reference 90 (low 85 <= 90); corrected first target reference 105, floor_to_price_tick(105, 1) = 105 (Design section 12, "with full bar `open=100, high=104")
- **W312-M6-06R-4** - legacy has no second fill; corrected second target fills at floor_to_price_tick(110, 1) = 110 (Design section 12, "full bar `open=100, high=104, low=85")
- **W312-M6-06R-5** - 1.0.0 has no policy id and no collision receipt; 2.0.0 emits the ordered chosen ids as a 2-member array (Design section 12, "with full bar `open=100, high=104", Design section 12, "with full bar `open=100, high=104", Design section 12, "with full bar `open=100, high=104", Design section 23.4, "AMENDMENT-CHOICE`: section 12 requires a")
- **W312-M6-06R-6** - legacy gross = (90 - 100) * 2 * 1 = -20 ; corrected gross = (105-100)*1*1 + (110-100)*1*1 = 5 + 10 = 15 (Design section 12, "with full bar `open=100, high=104", Design section 12, "with full bar `open=100, high=104")

#### RULE2-06-EQUAL-PRICE-RED - `rule2_divergent_projection` (6 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fill_events/0/exit_id` | PRESENT(S, value not pinned) | PRESENT(`S:10:VEFSR0VULUZBUg==`) | DIFFERS |
| 2 | `/EVENT_SURFACE/fill_events/1/exit_id` | ABSENT | PRESENT(`S:11:VEFSR0VULU5FQVI=`) | DIFFERS |
| 3 | `/EVENT_SURFACE/fill_events` | PRESENT(A:1) | PRESENT(`A:2`) | DIFFERS |
| 4 | `/EVENT_SURFACE/fill_events/0/final_fill_price` | PRESENT(I:90) | PRESENT(`I:105`) | DIFFERS |
| 5 | `/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids` | ABSENT | PRESENT(`A:2`) | DIFFERS |
| 6 | `/RESULT_SURFACE/trades/0/gross_realized_pnl` | PRESENT(I:-20) | PRESENT(`I:10`) | DIFFERS |

- **W312-M6-06ER-1** - equal prices 105/105 force the exit_id UTF-8 tie-break: after the common prefix TARGET-, 0x46 (F) < 0x4e (N), so TARGET-FAR fills first; legacy still exits at the stop (Design section 12, "close=95`; only the stop touches", Design section 12, "close=95`; only the stop touches")
- **W312-M6-06ER-2** - legacy has no second fill; corrected second equal-price target is TARGET-NEAR (Design section 12, "open=100, high=104, low=85, close=95`; only", Design section 12, "open=100, high=104, low=85, close=95`; only")
- **W312-M6-06ER-3** - legacy one fill of quantity 2; corrected 0.5 * 2 = 1 twice, remainder 0, so two fills (Design section 12, "high=104, low=85, close=95`; only the")
- **W312-M6-06ER-4** - legacy stop reference 90; corrected first equal-price target reference 105 (Design section 12, "record, and policy with full")
- **W312-M6-06ER-5** - 1.0.0 has no collision receipt; 2.0.0 emits [TARGET-FAR, TARGET-NEAR] (Design section 12, "record, and policy with full", Design section 12, "record, and policy with full", Design section 23.4, "as those fill events state")
- **W312-M6-06ER-6** - legacy gross = (90 - 100) * 2 * 1 = -20 ; corrected gross = (105-100)*1*1 twice = 10 (Design section 12, "zero-impact model/parameter record, and policy", Design section 12, "zero-impact model/parameter record, and policy")

#### RULE2-06-GREEN - `rule2_green_projection` (3 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fill_events/0/final_fill_price` | PRESENT(I:90) | PRESENT(`I:90`) | EQUAL |
| 2 | `/EVENT_SURFACE/fill_events/0/quantity` | PRESENT(I:2) | PRESENT(`I:2`) | EQUAL |
| 3 | `/RESULT_SURFACE/trades/0/gross_realized_pnl` | PRESENT(I:-20) | PRESENT(`I:-20`) | EQUAL |

- **W312-M6-06G-1** - targets do not touch (high 104 < 105 and < 110); the stop touches (low 85 <= 90), so all three policies select the sole class; stop reference = 90 and floor_to_price_tick(90, 1) = 90 on both versions (Design section 12, "close=95`; only the stop touches", Design section 12, "close=95`; only the stop touches")
- **W312-M6-06G-2** - only the stop touches, so both versions fill the full reference quantity 2 (Design section 12, "close=95`; only the stop touches")
- **W312-M6-06G-3** - gross = (90 - 100) * 2 * 1 = -20 on both versions (Design section 12, "the stop touches, so both", Design section 12, "the stop touches, so both")

#### RULE2-07-RED - `rule2_divergent_projection` (7 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/EVENT_SURFACE/fee_events` | ABSENT | PRESENT(`A:2`) | DIFFERS |
| 2 | `/RESULT_SURFACE/trades/0/net_trade_pnl` | ABSENT | PRESENT(`F:-0x1.999999999999ap-3`) | DIFFERS |
| 3 | `/RESULT_SURFACE/guards/guard_pnl_basis` | ABSENT | PRESENT(`S:16:R1JPU1MtTUlOVVMtRkVFUw==`) | DIFFERS |
| 4 | `/RESULT_SURFACE/guards/last_closed_guard_pnl` | ABSENT | PRESENT(`F:-0x1.999999999999ap-3`) | DIFFERS |
| 5 | `/RESULT_SURFACE/guards/consecutive_loss_count` | PRESENT(I:0) | PRESENT(`I:1`) | DIFFERS |
| 6 | `/RESULT_SURFACE/guards/guard_blocked_raw` | PRESENT(B:0) | PRESENT(`B:1`) | DIFFERS |
| 7 | `/RESULT_SURFACE/equity_curve/last` | PRESENT(I:1000) | PRESENT(`F:0x1.f3e6666666666p+9`) | DIFFERS |

- **W312-M6-07R-1** - 1.0.0 has no fee model and no fee_events container (Design section 13, "and equity remains `1000`.", Design section 13, "and equity remains `1000`.", Design section 15.3, "funding_events`, and `exit_events`; any may"); 2.0.0 emits one fee row per taker fill, so A:2
- **W312-M6-07R-2** - 1.0.0 has no net field; corrected net = 0 + (-0.1) + (-0.1) = -0.2 (Design section 13, "cash delta are `0`, legacy", Design section 13, "cash delta are `0`, legacy")
- **W312-M6-07R-3** - the guard basis node exists only at 2.0.0 (Design section 13, "enables only the consecutive-loss guard", Design section 13, "enables only the consecutive-loss guard", Design section 23.1, "tie_break_applied` iff an equal-price tie")
- **W312-M6-07R-4** - the closed-guard PnL node exists only at 2.0.0; its value is the lifecycle net -0.2 (Design section 13, "are disabled. The legacy full", Design section 13, "are disabled. The legacy full")
- **W312-M6-07R-5** - legacy stores gross last_realized_pnl 0, so (0 < 0) is false and the count resets to 0; corrected stores -0.2, so (-0.2 < 0) is true and the count is 1 (Design section 13, "other L16 guards and guard")
- **W312-M6-07R-6** - legacy predicate (0 < 1) is true so nothing is blocked; corrected predicate (1 < 1) is false so guard_blocked_raw is true (Design section 13, "all other L16 guards and")
- **W312-M6-07R-7** - legacy equity stays 1000 with no fee model; corrected equity = 1000 - 0.1 - 0.1 = 999.8, which is also a float node against a legacy integer node (Design section 13, "guards and guard recovery are", Design section 13, "guards and guard recovery are")

#### RULE2-07-GREEN - `rule2_green_projection` (4 members)

| # | selector | `1.0.0` derived state | `2.0.0` resolved node | relation |
|---|---|---|---|---|
| 1 | `/RESULT_SURFACE/equity_curve/last` | PRESENT(I:1000) | PRESENT(`I:1000`) | EQUAL |
| 2 | `/RESULT_SURFACE/guards/consecutive_loss_count` | PRESENT(I:0) | PRESENT(`I:0`) | EQUAL |
| 3 | `/EVENT_SURFACE/fill_events` | PRESENT(A:0) | PRESENT(`A:0`) | EQUAL |
| 4 | `/RESULT_SURFACE/final_position` | PRESENT(N) | PRESENT(`N`) | EQUAL |

- **W312-M6-07G-1** - the empty fill-event input produces no fee and no realization, so equity stays 1000 on both versions (Design section 13, "and guard recovery are disabled.")
- **W312-M6-07G-2** - no lifecycle closes, so the counter stays 0 on both versions (Design section 13, "and guard recovery are disabled.")
- **W312-M6-07G-3** - the vector supplies an empty fill-event input, so fill_events is A:0 on both versions (Design section 13, "and guard recovery are disabled.")
- **W312-M6-07G-4** - no fill means no position on either version (Design section 13, "is true. Under D017's")

Mechanical check run this session over all fifty-five members: every corrected selector resolves in
its sealed golden, every resolved canonical node starts with the declared `node_kind`, and the
declared `expected_relation` equals the relation computed from the two tagged states. **0 failures.**

### W312-C. Two legacy sides deliberately left unpinned

`RULE2-06-RED` and `RULE2-06-EQUAL-PRICE-RED` member 1 (`/EVENT_SURFACE/fill_events/0/exit_id`) pin
the legacy side as `PRESENT` of kind `S` with **no value**. Design `Design section 12, "stop `90` on the named"` fixes only that legacy's
implicit stop-first path exits at the stop; it does not state legacy's own exit-id string. The removed
reader mapped `INITIAL_SL` to `STOP` in code, which is exactly the reader-authored shaping commit
`4c57e4e4` and `b0933b1a` deleted, so this lane does not restore it. The divergence claim does not
need it: the corrected ids are `TARGET-NEAR` and `TARGET-FAR`, which no legacy stop id equals.

### W312-D. Members the design excludes, restated so they are not re-added

- `fee_events` and `funding_events` are excluded from every GREEN projection (correction C-02 above):
  they do not exist in `LEGACY_P011_EXACT_V1` (design `Design section 15.3, "six ordered containers: `decision_events`, `fill_events"`), so the legacy side is `ABSENT` and
  design `Design section 15.3, "containers: `decision_events`, `fill_events`, `cash_events`, `fee_events"` scores `ABSENT` versus `A:0` as divergence.
- `equity_curve` and `net_trade_pnl` are excluded from the `RULE2-01/02/04/05/06` GREEN projections:
  1.0.0 has no fee model, so corrected equity carries a version-specific added effect (design `Design section 6, "to the named behavioral projection."`).
  They **are** members of `RULE2-07-GREEN`, whose vector has no fill and therefore no fee split.
- `RULE2-07-RED` `/RESULT_SURFACE/trades/0/gross_realized_pnl` stays excluded from the divergent set
  (correction C-07): it is `0` on both versions, and design `Design section 15.3, "funding_events`, and `exit_events`; any may"` says identical present values are
  not divergence.
- No `/RESULT_SURFACE/collision/*` member is sealed. That object was removed at design v1.9
  `Design section 23.1, "UTF-8 byte-order tie-break. **OWNER-RULED (owner"`; the sole receipt is the closed `COLLISION_RESOLVED` decision row (design `Design section 23.4, "object; the closed `COLLISION_RESOLVED` decision"`),
  which is what member 5 of both RULE2-06 RED rows selects.

### W312-E. M4 item 1 - `PROBE-P012-02-A` re-derivation

Design `Design section 8, ">` so equality refuses. The"` binds this probe: "change the corrected comparison to `>` so equality refuses. The
RULE-2-GREEN cross-version check must refuse on the admission/refusal projection for
`RULE2-02-GREEN`." Design `Design section 23.4, "admission/refusal projection. `AMENDMENT-CHOICE`: retain the"` names the admission node `admitted`.

Re-derived values, both **unchanged** from the sealed catalog row:

| member | sealed value | re-derived value | authority |
|---|---|---|---|
| `expected_failed_check` | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | `RULE2_GREEN_CROSS_VERSION_EXPECTATION` | design `Design section 8, "row's `expected_first_changed_node` is `/RESULT_SURFACE/admitted"` |
| `expected_first_changed_node` | `/RESULT_SURFACE/admitted` | `/RESULT_SURFACE/admitted` | design `Design section 8, "row's `expected_first_changed_node` is `/RESULT_SURFACE/admitted"`, `Design section 23.4, "admitted` | the DEF-P012-02 minimum-notional predicate"` |
| `comparator_first_differing_node` | `/RESULT_SURFACE/admitted` | `/RESULT_SURFACE/admitted` | same single-member projection |

What actually changed is the node's provenance, not its pointer. Before `4c57e4e4` the reader
synthesised `/RESULT_SURFACE/admitted` from `result["final_position"] is not None`. At HEAD the node
is a real closed-set member of the corrected `RESULT_SURFACE` for a DEF-P012-02 GREEN row
(`verify_bceg.py:891-892`) and is sealed in the golden as `"admitted": true`
(`golden/corrected_vnext/RULE2-02-GREEN.json`, resolved this session to `B:1`). Its arithmetic:
`order_notional = 1 * 100 * 1 = 100`; corrected admits iff `100 >= 100` (true); legacy rejects iff
`100 < 100` (false), so both admit and the sealed GREEN member `W312-M6-02G-1` is `EQUAL`.

**Reachability finding, reported and not absorbed.** After `b0933b1a`,
`_green_projection_differences` takes `(root, baseline_root, base_row)` and compares the sealed
`BASELINE_BYTES` legacy result against the sealed `CONTRACT_TABLES` golden
(`verify_bceg.py:2992-3009`); it no longer reads the probe variant's output at all. Design `Design section 15.2, "kernel module, changing the base"`
names exactly those two producers for this check. A `target_kind=KERNEL` variant therefore cannot
move either side, so the check the design names at `Design section 8, "perturbation as their own concrete"` is unreachable from this probe row as it
stands. Design `Design section 15.2, "remain outside the variant and"`'s own concrete fail input for this check is an expected-side perturbation
("Perturb corrected GREEN expected fill price by one ULP"), not a kernel patch. Closing this needs
one owner-gated design act - either amend `Design section 8, "their own concrete fail input"` to bind a check a `KERNEL_2` variant can fail, or
change the row's `target_kind`. **No value is invented here and no probe byte is written.**

### W312-F. M4 item 2 - `PROBE-P012-06-A` re-derivation

Design `Design section 12, "expected artifact unchanged. The corrected-expectation"` binds this probe to `base_scenario_id=RULE2-06-RED`, `subject_producer_id=KERNEL_2`,
`target_kind=KERNEL`, and states "The corrected-expectation check must refuse at the first changed
event sequence node: expected first fill `TARGET-NEAR`, modified-kernel first fill `TARGET-FAR`."

Re-derived values, all **unchanged** from the sealed catalog row:

| member | sealed value | re-derived value | authority |
|---|---|---|---|
| `expected_failed_check` | `CORRECTED_EXPECTATION` | `CORRECTED_EXPECTATION` | design `Design section 13, "100`, each derived fee cash"`, `Design section 15.2, "row's `expected_failed_check`, and the"` row 2 |
| `expected_first_changed_node` | `/EVENT_SURFACE/fill_events/0/exit_id` | `/EVENT_SURFACE/fill_events/0/exit_id` | design `Design section 13, "100`, each derived fee cash"`, `Design section 15.2, "row's `expected_failed_check`, and the"` |
| `comparator_first_differing_node` | `/EVENT_SURFACE/cash_events/0/signed_delta` | `/EVENT_SURFACE/cash_events/0/signed_delta` | derived below |

The comparator node was previously a W256 measurement. It is now derivable in writing, so it is
re-derived rather than carried. Design `Design section 15.3, "containers: `decision_events`, `fill_events`, `cash_events`, `fee_events"` walks object children in UTF-8 byte-sorted key
order. Top level: `EVENT_SURFACE` before `RESULT_SURFACE` (`E` = 0x45 < `R` = 0x52). Inside
`EVENT_SURFACE`: `cash_events` first (`c` = 0x63 < `d` = 0x64 of `decision_events`). The taker rate
for both TARGET roles is `0.00045` (design `Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is"`). Base order, sealed in the golden:

```text
base   fill 0 = TARGET-NEAR @ 105 -> fee = 105 * 1 * 0.00045 = 0.04725 -> cash_events[0] = -0.04725
base   fill 1 = TARGET-FAR  @ 110 -> fee = 110 * 1 * 0.00045 = 0.0495  -> cash_events[2] = -0.0495
variant reverses the TARGET_FIRST target-event order:
       fill 0 = TARGET-FAR  @ 110 -> fee = 110 * 1 * 0.00045 = 0.0495  -> cash_events[0] = -0.0495
-0.0495 != -0.04725, so /EVENT_SURFACE/cash_events/0/signed_delta is the first node the
comparator's traversal order reaches that differs.
```

`/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids/0` also changes under the variant
(`TARGET-NEAR` becomes `TARGET-FAR`) and remains a member of the complete changed-node set, which is
all design `Design section 15.3, "node_kind)`. Arrays use indices"` requires of it.

### W312-G. M4 item 3 - the `RULE2-06-RED` golden node, re-derived from the collision rule

Node: `/EVENT_SURFACE/decision_events/2/ordered_chosen_exit_ids/0`. Sealed byte before this lane:
`"TARGET-NEAR"`.

Design `Design section 12, "Long ascending target price; short"` (the `TARGET_FIRST` row of the section-12 tie-break table) fixes target ordering as
"Long ascending target price; short descending target price; equal prices by `exit_id` UTF-8 byte
order". Design `Design section 12, "touched target in the scenario's declared exit-candidate order; this receipt-only"` (**OWNER-RULED, owner addendum 29, decision 72**) says the receipt-only
`touched_exit_ids` listing rule "does not alter `ordered_chosen_exit_ids`, `TARGET_FIRST` execution
order, fills, or PnL", and design `Design section 23.4, "decision 71):** `exit_fill_price` is not"` repeats that in the closed `COLLISION_RESOLVED` shape.

Arithmetic from the sealed input `tests/corrected_vnext/contracts/inputs/RULE2-06-RED.json`
(`legacy_arm.config`: `sl_percent=10`, `tp1_r_multiple=0.5`, `tp2_r_multiple=1`, `tp_mode=Multi-TP`,
`tp1_close_pct=50`; `legacy_arm.bars[1].close=100`), with design `Design section 22.1, "legacy_arm.bars` and `legacy_arm.config` as the"`'s mechanical alias
"corrected aliases TP1/TP2 mechanically to the stated `TARGET-NEAR`/`TARGET-FAR` ids":

```text
risk per unit  = 100 * 10 / 100          = 10        -> percent stop = 100 - 10 = 90
TP1 = 100 + 10 * 0.5 = 105  -> alias TARGET-NEAR
TP2 = 100 + 10 * 1   = 110  -> alias TARGET-FAR
both targets touch (high 115 >= 110 and >= 105); the stop touches (low 85 <= 90)
TARGET_FIRST, long -> ascending target price: 105 < 110
-> ordered_chosen_exit_ids = [TARGET-NEAR, TARGET-FAR]
-> ordered_chosen_exit_ids/0 = "TARGET-NEAR"
prices are not equal, so the UTF-8 byte-order tie-break of Design section 12, "no stop remainder. `RULE2-06-GREEN` uses" is not entered
decision 72 (Design section 12, "touched, followed by every touched target in the scenario's declared exit-candidate order; this receipt-only") is receipt-only and does not touch this member
```

**The re-derivation reproduces the sealed byte exactly. No golden byte was written.** The sealed
value `"TARGET-NEAR"` is derived from design `Design section 12, "two targets, target fractions, tick"`, `Design section 12, "two targets, target fractions, tick"`, `Design section 12, "two targets, target fractions, tick"` and `Design section 22.1, "These are the existing sealed RULE2-07 cost records, bound"` and from the sealed
input, with no dependence on the removed reader shaping. What the removed shaping did affect is a
separate defect, recorded in the lane report: the `RULE2-06-RED` and `RULE2-06-GREEN` sealed inputs
carry no `/corrected_only/economic_inputs/target_book`, so at HEAD the corrected run keeps the
kernel's own `TP1`/`TP2` working-exit ids (`verify_bceg.py:1329-1340` applies the book only when the
member is present) and design `Design section 22.1, "members are JSON `null` only for RULE2-08, where section 14 says no cost schedule is consumed"`'s mechanical alias has no carrier for these two rows. That is an
owner-gated **input** change of exactly the shape W311 made for `RULE2-06-EQUAL-PRICE-RED` under
owner decision 139, and this lane may not write an input byte.

### W312-H. `RULE2-08-RED` and `RULE2-08-GREEN` - STOPPED

Nothing was derived and no byte was written for either row, or for `PROBE-P012-08-A`. The lane's
M1-pending instruction (Lead note 08:3x, ledger addendum 46) directs the stop, and W311 recorded M1
as a DESIGN-GAP: design `Design section 15.2, "scratch copy of the subject"` says no `CostSchedule` is consumed by RULE2-08, `Design section 22.3, "cost records by reference (`SYNTH-COST-RULE2-07-RED-V1"` makes both
cost members JSON `null` for those rows, and `Design section 22.1, "is superseded. For RULE2-08-RED, `cost_schedule_id"`/`Design section 22.1, "is superseded. For RULE2-08-RED, `cost_schedule_id"` say `C` is absent/`NOT_CONSUMED`, while
owner addendum 20 binds real pre-window fills. Reason of record: **waits for owner M1b.**

### W312-I. Byte record

| file | sha256 before | sha256 after | bytes |
|---|---|---|---|
| `scenario_catalog.json` | `a9ba2a89a1de83b4ba9687b3f9708ee8ca8fc1b15f36c737bd115586cdf051f6` | `c2a4ade275f0fcd50e6fe26974b8d5a0a69ce5029189535789c2b65d569590f6` | 49676 -> 78801 |

Measured leaf-level diff of the whole catalog against the pre-W312 snapshot
(`C:\tmp\SNAPSHOTS\20260903_0833_preW312\`): `removed: []`, `changed:` only the fifteen row
object-member counts (`O:n` -> `O:n+1`), `added:` 1072 leaves, every one of them inside a
`rule2_divergent_projection` or `rule2_green_projection` member. No probe row, no `RULE2-08` row, no
golden, no input, no manifest and no anchor byte moved.

For the Lead's re-seal: `CONTRACT_TABLES_MANIFEST.json` `files[1]` pins `scenario_catalog.json` and
must be re-pinned to the sha256 above. This lane may not move a manifest-seal byte.

## W319 - sealed corrected-only `target_book` for `RULE2-06-RED` and `RULE2-06-GREEN` (owner decision 142) (2026-09-03, tables family, insertion-only)

Authority: owner decision 142 = W312 D-7 default (a). Same defect class the owner closed for
`RULE2-06-EQUAL-PRICE-RED` with decision 139 (executed by W311, `W311_SEALED_INPUTS_REPORT.md`
section 2). No value below is computed; each is quoted from design v1.13
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`.

### W319-A. Design lines the values come from

`Design section 12, "the full quantity `2` at"` (section 12), verbatim:

> "`RULE2-06-RED` is a synthetic long under `execution_profile_id=raw_close_only_v1` with entry fill
> `100`, reference quantity `2`, `qty_step=1`, stop `90`, target `TARGET-NEAR` at `105` with target
> fraction `0.5`, target `TARGET-FAR` at `110` with target fraction `0.5`, `price_tick=1` ..."

> "`RULE2-06-GREEN` uses `execution_profile_id=raw_close_only_v1` and the same position, quantity
> step, stop, two targets, target fractions, tick, test-only zero-impact model/parameter record, and
> policy with full bar `open=100, high=104, low=85, close=95` ..."

`Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is"` (section 22.5, `RULE2-06-RED` row, "Corrected-only binding" column), verbatim:

> "corrected aliases TP1/TP2 mechanically to the stated `TARGET-NEAR`/`TARGET-FAR` ids and uses
> stated fractions `.5/.5`, policy `TARGET_FIRST`"

i.e. `TP1` -> `TARGET-NEAR`, `TP2` -> `TARGET-FAR`.

`Design v1.5 change log, "book/evaluation, records and explicit cm | prelude/alias `MECHANICAL`; vector/policy/records `ECONOMIC-BEARING`; account unbound | §22.5 row; §12 vector, owner"` (section 22.5, `RULE2-06-GREEN` row), verbatim:

> "Same config/prelude, explicitly including `instrument_contract_multiplier=1`; evaluation
> `(2000-01-01T00:12:00Z,2,100,104,85,95,0)`. | Same reached book; only stop touches ..."

So the GREEN book is the RED book; `:357` states the same two targets and target fractions for GREEN
independently.

### W319-B. Value ledger (per value: design line -> member written)

| member (JSON pointer) | value | design line quoted |
|---|---|---|
| `/corrected_only/economic_inputs/target_book/TP1/0` | `"TARGET-NEAR"` | `Design section 22.1, "corrected_only` has exactly `economic_inputs`, `observation_window"` alias direction; id stated at `Design section 12, "TARGET-NEAR`/`105`, then quantity"` |
| `/corrected_only/economic_inputs/target_book/TP1/1` | `105` | `Design section 12, "the same position, quantity step"` "target `TARGET-NEAR` at `105`" |
| `/corrected_only/economic_inputs/target_book/TP1/2` | `0.5` | `Design section 12, "uses `execution_profile_id=raw_close_only_v1` and the same"` "with target fraction `0.5`"; `Design section 22.1, "corrected_only` has exactly `economic_inputs`, `observation_window"` "fractions `.5/.5`" |
| `/corrected_only/economic_inputs/target_book/TP2/0` | `"TARGET-FAR"` | `Design section 22.1, "corrected_only` has exactly `economic_inputs`, `observation_window"` alias direction; id stated at `Design section 12, "the same position, quantity step"` |
| `/corrected_only/economic_inputs/target_book/TP2/1` | `110` | `Design section 12, "all touch. Legacy's implicit"` "target `TARGET-FAR` at `110`" |
| `/corrected_only/economic_inputs/target_book/TP2/2` | `0.5` | `Design section 12, "target `TARGET-FAR` at `110` with target fraction `0.5`"` "with target fraction `0.5`"; `Design section 22.5, "uses stated fractions `.5/.5`"` "fractions `.5/.5`" |

The same six values are written to `RULE2-06-GREEN.json`, on the authority of `Design section 22.5, "Same reached book; only stop touches"` "Same reached
book" and `Design section 12, "the same position, quantity step, stop, two targets, target fractions, tick"` "the same position, quantity step, stop, two targets, target fractions, tick ...".

The keys `"TP1"` and `"TP2"` are the kernel's own Multi-TP working-exit ids, not authored numbers:
`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:264-282` (branch HEAD `8112ff0b`,
read read-only via `git -C C:\WP012BUILD show HEAD:<path>`) constructs `WorkingExit("TP1","TP1",...)`
and `WorkingExit("TP2","TP2",...)` under `tp_mode == TP_MODE_MULTI`, which is the mode both rows'
`legacy_arm.config` sets (`tp_mode="Multi-TP"`, design `Design section 22.1, ". `legacy_arm` has exactly `bars"`).

### W319-C. Transport shape is `MECHANICAL` and read from the repository

`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:1207-1226`
reads the member at `/corrected_only/economic_inputs/target_book` and requires a JSON object;
`verify_bceg.py:1329-1340` fixes the value-tuple positions as
`[exit_id, target_price, qty_fraction]`, keyed by the legacy working-exit id. Shape written:

```json
{"TP1":["TARGET-NEAR",105,0.5],"TP2":["TARGET-FAR",110,0.5]}
```

identical in shape to the book W311 sealed for `RULE2-06-EQUAL-PRICE-RED`
(`{"TP1":["TARGET-NEAR",105,0.5],"TP2":["TARGET-FAR",105,0.5]}`), differing only in the `TARGET-FAR`
price, which design `Design section 12, "/`110`, leaving no stop"` states as `110` for `RULE2-06-RED`/`-GREEN` and `105` for the equal-price
row.

Byte discipline: canonical JSON per design `Design section 15.3, "a required final LF. Parsing"` and `Design section 22.3, "JSON object with exactly `event_timestamp="` - sorted object keys, no BOM, LF, one
required final LF, compact `(',' , ':')` separators. Verified by round-trip: re-serialising each
*pre-change* file with `json.dumps(sort_keys=True, separators=(',',':')) + "\n"` reproduced its exact
pre-change bytes (1773 and 1782), so the writer used the corpus's own encoder settings.

### W319-D. Measured leaf-level diff against the pre-W319 snapshot

For each of the two inputs (`C:\tmp\SNAPSHOTS\20260903_0900_preW319\`):

```
added  : /corrected_only/economic_inputs/target_book/TP1/0
         /corrected_only/economic_inputs/target_book/TP1/1
         /corrected_only/economic_inputs/target_book/TP1/2
         /corrected_only/economic_inputs/target_book/TP2/0
         /corrected_only/economic_inputs/target_book/TP2/1
         /corrected_only/economic_inputs/target_book/TP2/2
removed: []
changed: []
```

`scenario_catalog.json`: `added: []`, `removed: []`, `changed: ['/10/input/digest',
'/12/input/digest']` - rows `[10] RULE2-06-RED` and `[12] RULE2-06-GREEN`. Neither row has an
`input.bytes` member (the whole file contains no `"bytes"` key), so none was written; the
`digest_reason` strings were left untouched, and the W312-sealed projection members of both rows and
every `PROBE` row are byte-identical. Each old digest literal occurred exactly once in the file and
was replaced in place, so the file length is unchanged (78801 bytes before and after). Cross-check:
every catalog row whose `input.path` exists in the bundle now has `input.digest` equal to the
measured sha256 of that file - no mismatch.

### W319-E. Byte record

| file | sha256 before | sha256 after | bytes |
|---|---|---|---|
| `tests/corrected_vnext/contracts/inputs/RULE2-06-RED.json` | `c946e1a24f3b96ad0886132720a43df92ffb9c1fe2729e0a903940001650b349` | `8c62e57e0584207d99ab6d581a91535d341b65df46b362dc402a48da702f1f68` | 1773 -> 1848 |
| `tests/corrected_vnext/contracts/inputs/RULE2-06-GREEN.json` | `e4c4f861c48df32447f4dc1d32d65f61fec5c2dc9baf3f563983ed554de68cff` | `c334b07011bd538e7b9d02de451abbd5f389da8cf7392da64fed7dfc941dd4e2` | 1782 -> 1857 |
| `scenario_catalog.json` | `c2a4ade275f0fcd50e6fe26974b8d5a0a69ce5029189535789c2b65d569590f6` | `b43624dc94219576ce79225a1f4282d116b0b21307b77371abbd4a5b52d74234` | 78801 (unchanged) |

No golden, manifest-seal, anchor, probe or design byte was written; no kernel was executed and no
observed artifact was read.

For the Lead's re-seal: `CONTRACT_TABLES_MANIFEST.json` `files[1]` pins `scenario_catalog.json` and
`files[0]` pins `DERIVATIONS.md`; both must be re-pinned to the post-W319 sha256 values. This lane
may not move a manifest-seal byte.

## W321 - Tables acts for RULE2-08 branch after owner decision 144 (M1 binding; M6 rows; probe 08-A/02-A values; RED golden) (2026-09-03, tables family, insertion-only)

Authority: owner decisions 137/144 (M1), 138 (M6), 140 (M4), 143 (M4b). Design v1.15
`C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md` Design section 14, "bars before the observation window",Design section 22.1, "AMENDMENT-CHOICE (W320, owner decision 144, 2026-09-03) — §22.1",Design section 22.1, "AMENDMENT-CHOICE (W320, owner decision 144, 2026-09-03) — §22.1",Design section 22.6, "AMENDMENT-CHOICE (W320, owner decision 144, 2026-09-03) — §22.6",Design section 23.5, "owner-approved scenario-input amendment binds its" (W320 amendment);
Design section 14, "1) consumes the RED record",Design section 14, "1) consumes the RED record" (W320 repair); Design section 14, "1) consumes the RED record" (probe 08-A); Design section 8, "AMENDMENT-CHOICE (W317, owner decision 143" (probe 02-A W317 amendment).

### W321-A. M1 (decisions 137/144) — RULE2-08 input cost record binding

Design v1.15 section 14, "sha256 `040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe`), bound BY REFERENCE to the existing sealed RULE2-07 cost records under": "RULE2-08-RED consumes cost record `SYNTH-COST-RULE2-07-RED-V1` (sha256
`806e98512a3eb336538c8b68a52cef3ed80897cd2a87d9f270900c7ba094f29b`) and RULE2-08-GREEN consumes
`SYNTH-COST-RULE2-07-GREEN-V1` (sha256
`040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe`), bound BY REFERENCE to the
existing sealed RULE2-07 cost records."

Design v1.15 section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is": "For RULE2-08-RED, `cost_schedule_id` is `"SYNTH-COST-RULE2-07-RED-V1"` and
`cost_schedule_sha256` is `"806e98512a3eb336538c8b68a52cef3ed80897cd2a87d9f270900c7ba094f29b"`; for
RULE2-08-GREEN, `cost_schedule_id` is `"SYNTH-COST-RULE2-07-GREEN-V1"` and `cost_schedule_sha256` is
`"040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe"`."

The two cost record sha256 values were confirmed against the sealed records at
`core/economic_records/costs/` (read via COST_RECORDS_07.md in the W321 packet). Both match the
design exactly.

**Changes to RULE2-08-RED.json input:**
- `records.cost_schedule_id`: `null` → `"SYNTH-COST-RULE2-07-RED-V1"`
- `records.cost_schedule_sha256`: `null` → `"806e98512a3eb336538c8b68a52cef3ed80897cd2a87d9f270900c7ba094f29b"`
- No other member moved.

**Changes to RULE2-08-GREEN.json input:**
- `records.cost_schedule_id`: `null` → `"SYNTH-COST-RULE2-07-GREEN-V1"`
- `records.cost_schedule_sha256`: `null` → `"040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe"`
- No other member moved.

### W321-B. M6 (decision 138) — RULE2-08 sealed projections

#### W321-M6-08R-1 — `/EVENT_SURFACE/fee_events`

- Design v1.15 section 14, "0.1 (design fee identity lines": legacy has no funding cashflow and remains at equity 1000; legacy has no fee
  events.
- Design v1.15 section 14, "0 = 0.1 (design fee"; Design v1.15 section 14, "0 = 0.1 (design fee": the pre-window OPEN fill consumes the cost record at taker rate 0.001 on
  notional 100, producing fee cash delta -0.1. The corrected golden carries one fee event
  (CE-FEE-0, TAKER, notional 100, rate 0.001, signed_delta -0.1, EXACT_IDENTITY_V1).
- Legacy: ABSENT. Corrected: A:1. Relation: DIFFERS.

#### W321-M6-08R-2 — `/EVENT_SURFACE/funding_events`

- Design v1.15 section 14, "inputs derive notional `100`, long": legacy has no funding cashflow. Corrected has one funding event
  (TEST-FUND-1, notional 100, rate -0.001, funding_cash_delta -0.1).
- Legacy: ABSENT. Corrected: A:1. Relation: DIFFERS.

#### W321-M6-08R-3 — `/RESULT_SURFACE/equity_curve/last`

- Design v1.15 section 14, "+ 0 = 0.1 (design": legacy equity remains 1000.
- Design v1.15 section 14, "1 × 1) × 0.001 + 0"; Design v1.15 section 22.6, "row: C consumes `SYNTH-COST-RULE2-07-GREEN-V1` (sha256": corrected equity chain 1000 → 999.9 (pre-window OPEN fee at taker rate
  0.001 on notional 100: fee = abs(100 × 1 × 1) × 0.001 + 0 = 0.1, cash delta -0.1) → 999.8 (funding: notional 100 ×
  -0.001 = -0.1). equity_curve.last = 999.8.
- Legacy: PRESENT(I:1000). Corrected: F:999.8. Relation: DIFFERS.

#### W321-M6-08R-4 — `/RESULT_SURFACE/cumulative_funding`

- Design v1.15 section 14, "1000 → 999.9 (after fee −0.1": legacy has no funding cashflow, no cumulative_funding.
- Corrected: cumulative_funding = -0.1 (the single funding event's cash delta).
- Legacy: ABSENT. Corrected: F:-0.1. Relation: DIFFERS.

#### W321-M6-08G-1 — `/RESULT_SURFACE/equity_curve/last` — DESIGN-GAP (STOPPED)

- Design v1.15 section 14, "the GREEN pre-window bar prices/quantities": "The design does not state the GREEN pre-window bar prices/quantities
  (OPEN-EMBED-05 mechanism is bound by 5a, its numbers are not in the design): the fee arithmetic is
  therefore fee_i = abs(price_i × qty_i × multiplier) × 0.001 per pre-window fill, and equity at
  window start = 1000 − sum of fees. The numeric equity node for GREEN is a design-unenumerated value
  carrying the `BLOCKED-OPEN-EMBED-05` marker until the owner binds the GREEN prefix numbers; no price
  is invented."
- Design v1.15 section 17, "fee_i = abs(price_i × qty_i × multiplier) × 0.001 per pre-window fill) and" (L12): "the resulting equity node carries the `BLOCKED-OPEN-EMBED-05` marker
  until the owner binds the GREEN prefix numbers. No price is invented."
- Design v1.15 section 22.6, "OPEN and CLOSE before 2000-01-01T00" (§22.6 amendment): "the numeric equity node carries `BLOCKED-OPEN-EMBED-05`."
- **DESIGN-GAP:** The design does not enumerate the GREEN pre-window fill prices or quantities, so no
  numeric equity value is derivable. This projection member is STOPPED and removed from the catalog.
  The golden equity nodes carry `"BLOCKED-OPEN-EMBED-05"` (string marker, not a number).

#### W321-M6-08G-2 — `/EVENT_SURFACE/fill_events`

- Design v1.15 section 14, "no fill at all /": position is closed before the event; pre-window fills are outside the
  observation window and contribute no in-window fill events.
- Design v1.15 section 22.6, "00Z) each consuming the record at taker": "no fill in the observation window" is true.
- Legacy: PRESENT(A:0). Corrected: A:0. Relation: EQUAL.

#### W321-M6-08G-3 — `/RESULT_SURFACE/final_position`

- Design v1.15 section 14, "cashflow rate `-0.001`, `funding_cash_delta=-0.1`, and": position is closed immediately before the event timestamp.
- Design v1.15 section 22.6, "fills (OPEN and CLOSE before": under addendum 20 (5a) GREEN has pre-window fills (OPEN and CLOSE before
  2000-01-01T00:00:00Z); at window start no position is eligible.
- Legacy: PRESENT(N:null). Corrected: N:null. Relation: EQUAL.

#### W321-M6-08G-DESIGN-GAP — `/RESULT_SURFACE/equity_curve/last` — STOPPED

Design v1.15 section 14, "is bound by 5a, its": GREEN pre-window fill prices/quantities are unenumerated; fee arithmetic is
fee_i = abs(price_i × qty_i × multiplier) × 0.001 per pre-window fill; equity at window start =
1000 − sum of fees. Design v1.15 section 17, "is a formula (fee_i =" (L12): "the resulting equity node carries the
`BLOCKED-OPEN-EMBED-05` marker until the owner binds the GREEN prefix numbers. No price is
invented." Design v1.15 section 22.6, "00Z) each consuming the record" (§22.6 amendment): "the numeric equity node carries
`BLOCKED-OPEN-EMBED-05`." The design does not decide a numeric value for this node; the projection
member is STOPPED and removed from the catalog. The golden carries the string marker
`"BLOCKED-OPEN-EMBED-05"` in place of the former numeric `1000`.

### W321-C. M4 (decision 140) — PROBE-P012-08-A re-derivation

Design v1.15 section 14, "event. The corrected-expectation check must refuse at": "Fail probe `PROBE-P012-08-A`: flip the sign for the long positive-rate
event. The corrected-expectation check must refuse at the cash-delta node because independent
expected -0.1 differs from actual +0.1."

| member | value | derivation |
|---|---|---|
| `expected_failed_check` | `CORRECTED_EXPECTATION` | Design section 14, "event. The corrected-expectation check must refuse at"; variant changes kernel bytes (funding sign flip in economics.py), so the check is corrected-expectation (Design section 15.3, "empty. Legacy reproduction compares `KERNEL_1"). |
| `expected_first_changed_node` | `/EVENT_SURFACE/funding_events/0/funding_cash_delta` | Design section 14, "event. The corrected-expectation check must refuse at" names the cash-delta node; the design-named typed projection is the funding_cash_delta. |
| `comparator_first_differing_node` | `/EVENT_SURFACE/cash_events/1/signed_delta` | With the W320 amendment adding a fee cash event at index 0, the funding cash event moves to index 1. The variant flips only the funding sign, so cash_events[0] matches (-0.1 = -0.1) and cash_events[1] differs (-0.1 vs +0.1). Under UTF-8 key order, cash_events (0x63) precedes funding_events (0x75) in EVENT_SURFACE (0x45), which precedes RESULT_SURFACE (0x52). |

### W321-D. M4b (decision 143) — PROBE-P012-02-A re-derivation

Design v1.15 section 8, "of `RULE2-02-GREEN` - `order_notional =" (W317 amendment): re-targeted from `RULE2_GREEN_CROSS_VERSION_EXPECTATION`
to `CORRECTED_EXPECTATION`. The variant changes the corrected admission comparison from `>=` to `>`,
so the equal case of RULE2-02-GREEN (order_notional = 100 against min_notional = 100) no longer
admits.

| member | value | derivation |
|---|---|---|
| `expected_failed_check` | `CORRECTED_EXPECTATION` | Design section 10, "open `90` on RED; the": the one value comparison in section 15.4 whose left producer is a kernel is the corrected-expectation row at Design section 15.4, "Together with the legacy-reproduction and", KERNEL_2 against CONTRACT_TABLES. |
| `expected_first_changed_node` | `/RESULT_SURFACE/admitted` | Design section 10, "open `90` on RED; the": the node section 23.4 Design section 23.4, "admission | Section 8 GREEN admission/refusal" names as the DEF-P012-02 admission projection. It is a member of the changed-node set under Design section 15.2, "kind (`INPUT`, `EXPECTED`, `OBSERVED`, `KERNEL". |
| `comparator_first_differing_node` | `/EVENT_SURFACE/cash_events/0/signed_delta` | The variant refuses admission, so no position opens, fill_events empties, fee_events empties, and cash_events empties. The sealed expected artifact carries cash_events with one fee entry. Under UTF-8 key order, cash_events (0x63) is the first key in EVENT_SURFACE (0x45), which precedes RESULT_SURFACE (0x52). The first differing node is /EVENT_SURFACE/cash_events/0/signed_delta. |

### W321-E. Item 4c — RULE2-08-RED golden re-derivation

Design v1.15 section 14, "abs(100 × 1 × 1) × 0.001"; Design v1.15 section 22.6, "reference; under addendum 20 (5a": the corrected equity chain is 1000 → 999.9 (pre-window OPEN fee) →
999.8 (funding).

**Nodes changed in `golden/corrected_vnext/RULE2-08-RED.json`:**

| node | before | after | arithmetic |
|---|---|---|---|
| `EVENT_SURFACE.fee_events` | `[]` (A:0) | `[{sequence:0, fee_event_id:"CE-FEE-0", kind:"FEE", lifecycle_id:1, signed_delta:-0.1, liquidity_role:"TAKER", notional:100, rate_used:0.001, rounding_rule:"EXACT_IDENTITY_V1"}]` (A:1) | Design section 14, "0.001 + 0 = 0.1"; Design section 14, "0.001 + 0 = 0.1": pre-window OPEN fill at taker rate 0.001 on notional 100 → fee = abs(100 × 1 × 1) × 0.001 + 0 = 0.1, cash delta -0.1. |
| `EVENT_SURFACE.cash_events` | `[{sequence:0, kind:"FUNDING", signed_delta:-0.1}]` | `[{sequence:0, kind:"FEE", signed_delta:-0.1}, {sequence:1, kind:"FUNDING", signed_delta:-0.1}]` | Fee cash event added at index 0; funding cash event re-sequenced to index 1. |
| `RESULT_SURFACE.equity_curve.last` | `999.9` | `999.8` | 1000 - 0.1 (fee) - 0.1 (funding) = 999.8. |
| `RESULT_SURFACE.run_manifest.cost_schedule_id` | `"NOT_CONSUMED"` | `"SYNTH-COST-RULE2-07-RED-V1"` | Design section 14, "= 0.1 (design fee identity": cost record consumed by reference. |
| `cash_ledger_join` (prose) | no fee mentioned | fee + funding cash rows | Updated to reflect both cash rows. |
| `no_slippage_note` (prose) | "no CostSchedule is consumed" | "consumes cost record SYNTH-COST-RULE2-07-RED-V1 by reference" | Updated per W320 amendment. |
| `unchanged_sealed_values` (prose) | equity_curve.last 999.9 | equity_curve.last re-derived to 999.8 | Updated. |
| `provenance` | design_version v1.8 | design_version v1.15; W321 author entry added | Housekeeping. |

No other node in the golden was changed. The RULE2-08-GREEN golden equity nodes were changed from
numeric `1000` to string marker `"BLOCKED-OPEN-EMBED-05"` (Design v1.15 section 14, "state the GREEN pre-window bar"; Design v1.15 section 17, "a formula (fee_i = abs"; Design v1.15 section 22.6, "00Z) each consuming the record at taker 0.001"; V321C
F-05 repair). The GREEN `rule2_green_projection` member for `/RESULT_SURFACE/equity_curve/last` was
STOPPED (DESIGN-GAP) and removed from the catalog.

### W321-F. Catalog digest re-pins

| catalog row | member | before | after |
|---|---|---|---|
| `RULE2-08-RED` | `input.digest` | `5136b0ce11f9e7b949e8b5105ce128df65ffcaf3ba0399f27141978ef341b0c1` | `995da57180072a369425bd7e14211b7d88effa27dbaa878c3ab6bdf7c705ca37` |
| `RULE2-08-GREEN` | `input.digest` | `3cb3cf0db3ab22134449f07c1c90e738a643736e16f97860889d80a08ebb900d` | `979401efe76427ef27c78cc395e7087bf12b672f02cb5a207ce4f75bebe5e962` |
| `RULE2-08-RED` | `expected_artifacts.2.0.0.digest` | `6e76d54f82a5486d0500a9a8c2e0792e186db3a5d1f8ec8d18eff8eee27e4b17` | `759e341d0d3823fd019243bbb7cc5f4c1ce81a6a15262f4fb853e4a7d054e0f4` |

The manifest (`CONTRACT_TABLES_MANIFEST.json`) also carries digests for `scenario_catalog.json`,
`DERIVATIONS.md`, and `golden/corrected_vnext/RULE2-08-RED.json` which must be re-pinned by the Lead
(this lane may not move a manifest-seal byte).

### W321-G. Byte record

| file | sha256 before | sha256 after | bytes before → after |
|---|---|---|---|
| `tests/corrected_vnext/contracts/inputs/RULE2-08-RED.json` | `5136b0ce11f9e7b949e8b5105ce128df65ffcaf3ba0399f27141978ef341b0c1` | `995da57180072a369425bd7e14211b7d88effa27dbaa878c3ab6bdf7c705ca37` | 1556 → 1643 |
| `tests/corrected_vnext/contracts/inputs/RULE2-08-GREEN.json` | `3cb3cf0db3ab22134449f07c1c90e738a643736e16f97860889d80a08ebb900d` | `979401efe76427ef27c78cc395e7087bf12b672f02cb5a207ce4f75bebe5e962` | 1783 → 1872 |
| `scenario_catalog.json` | `b43624dc94219576ce79225a1f4282d116b0b21307b77371abbd4a5b52d74234` | `0c1266691bd98e6b57a68e3f4b07f2403ebfb6b3a199d5a0e0dfa612ad1a9511` | 78801 → 84402 |
| `golden/corrected_vnext/RULE2-08-RED.json` | `6e76d54f82a5486d0500a9a8c2e0792e186db3a5d1f8ec8d18eff8eee27e4b17` | `759e341d0d3823fd019243bbb7cc5f4c1ce81a6a15262f4fb853e4a7d054e0f4` | 20820 → 21879 |

No other file in the bundle was touched. No design, manifest-seal, anchor, or probe-manifest byte was
written. No kernel was executed and no observed artifact was read.

### W321-H. Round-2 residues correction (V321C round 2, 2026-09-03)

The V321C round-2 verifier accepted the M1 edits, digests, container, values and listed golden deltas
but found four F-06 residues (stale identities, stale locators, NOT_CONSUMED, projection 1000).
Dispositioned as follows:

1. **GREEN golden `run_manifest.cost_schedule_id`**: changed from `NOT_CONSUMED` to
   `SYNTH-COST-RULE2-07-GREEN-V1`, mirroring the RED golden's shape (Design v1.15 section 14, "core/economic_records/costs/`; no new record and" binds the
   GREEN record as consumed by the two pre-window fills).

2. **GREEN golden `version_specific_lineage_nodes` prose**: replaced the declared economic projection
   value `1000` with `BLOCKED-OPEN-EMBED-05` and added the design's reason (Design v1.15 section 14, "at all / record unconsumed":
   pre-window fill prices/quantities are unenumerated; no price is invented).

3. **DERIVATIONS.md byte record**: the W321-G table carries pre-normalization hashes written before
   the Lead's LF normalization. The current before-state identities are those in
   `LEAD_PRE_EDIT_SHA256.txt` (snapshot `C:\tmp\SNAPSHOTS\20260903_0950_preW321`):
   - `inputs/RULE2-08-RED.json`: `5136b0ce11f9e7b949e8b5105ce128df65ffcaf3ba0399f27141978ef341b0c1`
   - `inputs/RULE2-08-GREEN.json`: `3cb3cf0db3ab22134449f07c1c90e738a643736e16f97860889d80a08ebb900d`
   - `golden/RULE2-08-RED.json`: `6e76d54f82a5486d0500a9a8c2e0792e186db3a5d1f8ec8d18eff8eee27e4b17`
   - `golden/RULE2-08-GREEN.json`: `6ad9432df9bcc1ef8d7f5ec31fcb2a5c7b30a7c80c56095c74aaeb6a24e91b97`
   - `scenario_catalog.json`: `b43624dc94219576ce79225a1f4282d116b0b21307b77371abbd4a5b52d74234`
   - `DERIVATIONS.md`: `cfdc0ad910b020c84ed137bc236a801de7c4fcb5435b9918832571cb31734e76`
   Post-edit identities are measured by the Lead after LF normalization. Current v1.15 design citations:
   Design v1.15 section 14, "RULE2-08-RED consumes cost record `SYNTH-COST-RULE2-07-RED-V1`" (cost-record binding),
   Design v1.15 section 14, "The corrected equity chain is therefore" (RED arithmetic),
   Design v1.15 section 14, "numeric equity node for GREEN is a design-unenumerated value" (GREEN blocker), and
   Design v1.15 section 14, "Fail probe `PROBE-P012-08-A`: flip the sign" (probe rule).

4. **Catalog PROBE-P012-08-A row**: corrected `design_lines` from `447` to `498` and note locator
   from `Design section 14, "Fail probe `PROBE-P012-08-A`: flip the"` to `Design section 14, "1000`. `RULE2-08-GREEN` uses `execution_profile_id=close_only_deterministic_v2"` (the probe rule is at Design v1.15 section 14, "1000`. `RULE2-08-GREEN` uses `execution_profile_id=close_only_deterministic_v2").

Decisions cited: 137/144 (M1), 138 (M6), 140 (M4), 143 (M4b). Design v1.15 citations:
Design v1.15 section 14, "RULE2-08-RED consumes cost record `SYNTH-COST-RULE2-07-RED-V1`";
Design v1.15 section 14, "The corrected equity chain is therefore";
Design v1.15 section 14, "numeric equity node for GREEN is a design-unenumerated value";
Design v1.15 section 14, "Fail probe `PROBE-P012-08-A`: flip the sign";
Design v1.15 section 17, "fee arithmetic is a formula (fee_i = abs";
Design v1.15 section 22.1, "For RULE2-08-RED, `cost_schedule_id` is";
Design v1.15 section 22.3, "For cost records: RULE2-08-RED and RULE2-08-GREEN consume";
Design v1.15 section 22.6, "RULE2-08-RED row: C consumes"; and
Design v1.15 section 23.5, "owner-approved scenario-input amendment binds its threshold".

### W321-I. Round-3 residues correction (V321C round 3, 2026-09-03)

The V321C round-3 verifier accepted all prior work but found two active findings: F-07 (PROBE-P012-02-A
comparator pointer one level too deep) and F-06 residue (stale v1.15 locators in catalog input
digest_reason and RED golden provenance/cash_ledger_join/no_slippage_note). Dispositioned as follows:

1. **F-07 — PROBE-P012-02-A `comparator_first_differing_node`**: changed from
   `/EVENT_SURFACE/cash_events/0/signed_delta` to `/EVENT_SURFACE/cash_events`. The variant changes
   `>=` to `>` so equality refuses (Design v1.15 section 8, "output differs from the sealed"); the sealed expected artifact has one
   `cash_events` member, while the variant's `cash_events` is empty (no position opens, no fee).
   The comparator at `verify_bceg.py:1545-1549` returns the array pointer immediately on list-length
   mismatch (expected length 1 vs variant length 0), so the first differing node is
   `/EVENT_SURFACE/cash_events`, not a member within it. The design-named target node
   `/RESULT_SURFACE/admitted` (Design v1.15 section 8, "/RESULT_SURFACE/admitted`, the node section 23.4") is unchanged. Catalog member, DERIVATIONS
   entry, and W315 handoff table all updated.

2. **F-06 locators — catalog input `digest_reason`**: both RULE2-08-RED and RULE2-08-GREEN rows'
   `digest_reason` cited displaced design lines Design section 14, "same snapshot rule and initial"; Design section 22.1, "both cost members are JSON"; Design section 22.1, "both cost members are JSON"; Design section 22.6, "slippage; the corrected equity chain"; Design section 23.5, "/RESULT_SURFACE/equity_curve/{first,last}` on RULE2-04-RED/GREEN". Corrected to current v1.15
   lines Design section 14, "same snapshot rule and initial"; Design section 14, "same snapshot rule and initial"; Design section 22.1, "both cost members are JSON"; Design section 22.1, "both cost members are JSON"; Design section 22.6, "slippage; the corrected equity chain"; Design section 23.5, "/RESULT_SURFACE/equity_curve/{first,last}` on RULE2-04-RED/GREEN" (binding 490, RED arithmetic 492, GREEN blocker 494, amendments
   932, 968, 1107, 1183).

3. **F-06 locators — RED golden `provenance.design_lines`**: changed from
   Design section 14, "Expected golden changes: add `funding_events"; Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is"; Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is"; Design section 22.6, "1` at `100`; corrected event"; Design section 23.5, "row's `design_lines` convenience locator" to Design section 14, "Expected golden changes: add `funding_events"; Design section 14, "Expected golden changes: add `funding_events"; Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is"; Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is"; Design section 22.6, "1` at `100`; corrected event"; Design section 23.5, "row's `design_lines` convenience locator".

4. **F-06 locators — RED golden `cash_ledger_join`**: changed design citation from Design section 14, "the fee arithmetic is therefore"; Design section 22.6, "equity chain is 1000 → 999.9" to
   Design section 14, "the fee arithmetic is therefore"; Design section 22.6, "equity chain is 1000 → 999.9" (RED arithmetic Design section 14, "the fee arithmetic is therefore", §22.6 amendment Design section 22.6, "equity chain is 1000 → 999.9").

5. **F-06 locators — RED golden `no_slippage_note`**: changed design citation from Design section 14, "the fee arithmetic is therefore"; Design section 22.6, "equity chain is 1000 → 999.9" to
   Design section 14, "both versions' economic cash/equity projection"; Design section 22.6, "is false; the fee arithmetic".

Values, arithmetic, ids, and all other members unchanged. No economic number moved.

Decisions cited: 137/144 (M1), 138 (M6), 140 (M4), 143 (M4b). Design v1.15 citations:
Design v1.15 section 14, "RULE2-08-RED consumes cost record `SYNTH-COST-RULE2-07-RED-V1`";
Design v1.15 section 14, "The corrected equity chain is therefore";
Design v1.15 section 14, "numeric equity node for GREEN is a design-unenumerated value";
Design v1.15 section 14, "Fail probe `PROBE-P012-08-A`: flip the sign";
Design v1.15 section 17, "fee arithmetic is a formula (fee_i = abs";
Design v1.15 section 22.1, "For RULE2-08-RED, `cost_schedule_id` is";
Design v1.15 section 22.3, "For cost records: RULE2-08-RED and RULE2-08-GREEN consume";
Design v1.15 section 22.6, "RULE2-08-RED row: C consumes"; and
Design v1.15 section 23.5, "owner-approved scenario-input amendment binds its threshold".

### W321-J. V321C F-08 disposition — RED `authored_value_tokens` ledger synchronized (fifth pass, 2026-09-03)

The V321C round-4 verifier found that the RED golden's `authored_value_tokens` ledger still described
the pre-fee cash layout (F-08). Dispositioned as three ledger changes in
`golden/corrected_vnext/RULE2-08-RED.json`:

1. **Existing FUNDING entry pointer moved**: `/EVENT_SURFACE/cash_events/0/kind` → `/EVENT_SURFACE/cash_events/1/kind`,
   value `FUNDING` unchanged, design_fact and spelling text unchanged.
2. **New FEE entry added**: `/EVENT_SURFACE/cash_events/0/kind` = `FEE`, design_fact cites design v1.15
   Design section 2.1, "GROSS_REALIZATION, FUNDING}`. A fee" (section 2.1 cash-event kinds), spelling is TABLES-AUTHORED, labeled by lane W321 fifth pass
   under V321C F-08.
3. **New FEE entry added**: `/EVENT_SURFACE/fee_events/0/kind` = `FEE`, same design_fact and spelling
   as above.

The `no other golden node changed` sentence of W321-H is corrected by this entry: the
`authored_value_tokens` ledger is a dependent metadata inventory (DERIVATIONS.md Y-5, G83-F06), not an
economic node. FEE(kind) and FUNDING(kind) are explicitly in the tables-authored class
(DERIVATIONS.md:2564-2565). No economic value moved; no other golden node changed.

### W321-K - V321C F-09 locator correction

W321-J (above) states it corrects the `no other golden node changed` sentence of W321-H. The
verifier measured that sentence at current line 4769 inside W321-E: "No other node in the golden
was changed." W321-H (lines 4798-4828) contains the Round-2 residue corrections and no such
sentence. W321-J's disposition is otherwise unchanged.

## W341 - fresh-audit re-derivation of the RULE2-08 goldens under decision 144

Authority and method: owner decisions 137 and 144; design v1.15 at
C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md, SHA-256
137180aee4834fa6b87932e289d7ce8cf56d9471c08e7b53982445598347c62f, 1664 lines. This derivation
uses only that design, the sealed inputs already bound by it, and committed economic-record bytes.
No kernel was executed and no observed artifact was read. This entry supersedes the W321 claims at
lines 4657-4664 and 4751-4762 that the pre-window fee row belongs to the compared EVENT_SURFACE.

### W341-A. Window membership and RED equity

Design section 22.6, "OPEN and CLOSE before 2000-01-01T00" fixes the closed RED observation window as
[2000-01-01T00:00:00Z, 2000-01-01T00:01:00Z] and excludes the candidate setup fill. Design section 2.1, "row's signed delta must"
require every fee projection and fee cash row to remain a one-to-one joined projection of its fill.
Design section 14, "has no funding cashflow and" and Design section 22.6, "5a) GREEN has pre-window fills (OPEN and" place the OPEN fee before the window and derive the chain 1000 -> 999.9 -> 999.8.
Design section 23.1, "OWNER-RULED (owner addendum 29, decision 72):** `touched_exit_ids" define first as realized equity after all earlier cash but before cash at the inclusive
start, and last as first plus in-window cash deltas.

| RED container | Setup OPEN row | Funding-tick row | Derivation |
|---|---:|---:|---|
| fill_events | out | none | The setup fill is excluded by Design section 22.6, "NOT_CONSUMED`. `observation_window` is `[2000-01-01T00". |
| cash_events | fee out | funding in at sequence 0 | The fee stays joined to the excluded fill under Design section 2.1, "by `cash_event_id`; the typed row"; TEST-FUND-1 is at the inclusive start under Design section 14, "RULE2-08-GREEN` uses `execution_profile_id=close_only_deterministic_v2`, lifecycle id" and 1104. |
| fee_events | fee out | none | The typed fee row follows its joined fee cash/fill event under Design section 2.1, "by `cash_event_id`; the typed row" and 75. |
| funding_events | none | in at sequence 0 | Design section 14, "RULE2-08-GREEN` uses `execution_profile_id=close_only_deterministic_v2`, lifecycle id" and Design section 14, "RULE2-08-GREEN` uses `execution_profile_id=close_only_deterministic_v2`, lifecycle id" require the eligible funding row at 2000-01-01T00:00:00Z. |

Therefore RED cash_events changes from two rows to one funding row, re-sequenced 1 -> 0;
fee_events changes A:1 -> A:0; fill_events remains A:0; funding_events remains A:1.
equity_curve.first changes I:1000 -> F:999.9 because the pre-window fee is
abs(100 x 1 x 1) x 0.001 + 0 = 0.1 and signed -0.1 (Design section 14, "abs(100 × 1 × 1) × 0.001", Design section 14, "abs(100 × 1 × 1) × 0.001", Design section 22.6, "under addendum 20 (5a) GREEN").
equity_curve.last remains F:999.8 because 999.9 + (-0.1 funding) = 999.8 (Design section 14, "fee = abs(100 × 1",
488, 492, 1107, 1283-1289). GREEN keeps all six event containers empty and both equity cells at
BLOCKED-OPEN-EMBED-05 because Design section 14, "has no funding cashflow and", Design section 17, "but are not enumerated in", Design section 22.6, "by reference; under addendum 20" and Design section 22.6, "by reference; under addendum 20" enumerate no pre-window fill numbers.

### W341-B. Fee-row closed shape

No RULE2-08-RED fee_events[0] survives the window derivation. If a fee row were in scope, its closed
16-member shape would be: sequence, event_timestamp, lifecycle_id, fill_id, event_class,
liquidity_role, schedule_id, schedule_digest, rate, fixed_component, fee_notional, fee_amount,
fee_cash_delta, settlement_currency, cash_event_id (Design section 13, "sequence, event_timestamp, lifecycle_id, fill_id, event_class"), plus
kernel_semantics_version (Design section 23.4, "It is absent from RULE2-04/06/07/08"). The removed W321 row's fee_event_id, kind, signed_delta,
notional, rate_used and rounding_rule are not in that set. No member was renamed speculatively; the
whole row is absent because its generating fill is pre-window.

### W341-C. Record-backed digest derivation

Design section 5.1, "both record-file digest and source-byte" define detached record-file SHA-256 and require record/source digests in the run
manifest. Design section 22.1, "digests are lower-case SHA-256 of" make record-file and source-byte digests mechanical values after record bytes
exist. Each record and sidecar below is committed at the measured worktree (targeted git status was
clean). Every recomputed record hash matched its one-line sidecar.

| Record path below core/economic_records | Sidecar and recomputed SHA-256 | Golden use |
|---|---|---|
| instruments/SYNTH-INSTRUMENT-RULE2-08-RED-V1.json | 1316ce06307a6fbf01fa7c007146df2bf7525bed385fbbf0045d29129d9f7a71 | RED instrument_record_digest; marker replaced |
| instruments/SYNTH-INSTRUMENT-RULE2-08-GREEN-V1.json | 20adf2749d255efd3fe281ec3ead2e07df0a36a5ad59718a54d0a1a7c0712b17 | GREEN instrument_record_digest; marker replaced |
| funding/SYNTH-FUNDING-RULE2-08-V1.json | aa4eaa939a83af1faa768eed82a2cd0216c26fccfb335240d05c5b1f7069d26d | RED funding row schedule_digest and both manifest funding_schedule_digest nodes; markers replaced |
| costs/SYNTH-COST-RULE2-07-RED-V1.json | 806e98512a3eb336538c8b68a52cef3ed80897cd2a87d9f270900c7ba094f29b | Confirms RED decision-144 cost binding at Design section 14, "sha256 `040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe`), bound BY REFERENCE to the existing sealed RULE2-07 cost records under" and Design section 22.1, "members are JSON `null` only for RULE2-08, where section"; proposed run-manifest child stopped below |
| costs/SYNTH-COST-RULE2-07-GREEN-V1.json | 040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe | Confirms GREEN decision-144 cost binding at Design section 14, "sha256 `040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe`), bound BY REFERENCE to the existing sealed RULE2-07 cost records under" and Design section 22.1, "members are JSON `null` only for RULE2-08, where section"; proposed run-manifest child stopped below |

Both committed InstrumentRecords carry provenance.source_sha256 =
0ab0accb2711da0661a97b437ccf2d15cc64b123ec3c28d93e6944ec0640e6fc on their sole JSON line;
that record member supplies both instrument_source_document_digest nodes under Design section 5.1, "FundingSchedule` is a UTF-8 JSON".
The shared FundingSchedule asserts source_event_digest
d348f49ebea85fccfdbc41e90f4d8f2802cfd9fd22bae9e069fa6015a2086cf3. A measured 173-byte minified,
sorted-key, final-LF candidate hashes to that value, but Design section 22.7, "the strict JSON string and" and Design section 22.7, "the strict JSON string and" do not fix JSON
separator/indentation bytes and no source-event preimage file is committed. Therefore RED
funding_events/0/source_event_digest remains BLOCKED-MISSING-RECORD-BYTES rather than promoting an
asserted digest without its unique preimage.

### W341-D. run_manifest cost digest DESIGN-GAP

The proposed run_manifest.cost_schedule_digest remains ABSENT on both goldens. Design section 23.1, "BCEG-1 corpus, `predicate` has the"
names run_manifest only as one of seven RESULT members; section 23.4 does not enumerate a closed
run_manifest child set or the exact cost child spelling. Design section 14, "equity, but the position is", Design section 22.1, "digests are lower-case SHA-256 of" and Design section 23.13, "C consumes the RULE2-07 cost" bind the cost record
id and its SHA as corrected-input record members, while Design section 5.1, "both record-file digest and source-byte" requires a record-file digest in a
run manifest at the semantic level. Those facts do not close the JSON child name. The task's explicit
stop condition therefore applies: before ABSENT, after ABSENT, DESIGN-GAP. No BLOCKED marker was
inserted because the design names no marker-bearing child node. W276C_REPORT.md lines 58-60 and
T340_TRIAGE_REPORT.md lines 23 and 55 independently record this missing child schema as M6 outside
owner decisions 135-144.

### W341-E. Ledgers, provenance and catalog pins

RED blocked_cells changes from six entries to two: funding source_event_digest and metrics remain;
the record-backed funding schedule, instrument record, instrument source-document and manifest
funding schedule marker rows are removed. RED authored_value_tokens removes the two pre-window FEE
rows and moves FUNDING kind from cash_events/1 to cash_events/0. GREEN blocked_cells changes from
five entries to two: metrics and observation_window.end_timestamp remain. Both provenance blocks now
identify v1.15/W341 and their current design lines. The GREEN economic values and its two remaining
markers do not move.

Final golden SHA-256 values over the LF bytes written are:

- RULE2-08-RED.json: b4da2832a3218750935f464d4fd91a3a3dd1fdf6d6a46f661f6a3a884d6bba5f
- RULE2-08-GREEN.json: 1185758e987bca067eaed98b7dd2ecca322837893010b9a04dfcc04ceb0b796c

Only expected_artifacts.2.0.0.digest in the corresponding RULE2-08 catalog rows is re-pinned to
those values. No sealed projection pair carries a copied value that follows a changed node: RED
fee_events is selected dynamically from CONTRACT_TABLES and remains PRESENT as an A node even when
its cardinality changes from one to zero; the RED equity projection selects last, which stays 999.8;
GREEN fill_events/final_position stay A:0/N:null. Therefore no projection pair is changed.

## Discrepancies

- W341-D01: The lane prompt and T340 line 18 cite Design section 22.6, "hourly end snapshot, same-timestamp INCLUDE" for the RED phrase excluding the
  candidate setup fill; in the verified 1664-line v1.15 file that phrase is at Design section 22.6, "100`, hourly end snapshot, same-timestamp". Design section 22.6, "100`, hourly end snapshot, same-timestamp"
  is the GREEN row. The text, not the stale locator, was followed.
- W341-D02: The lane prompt and W279C-F04 assume section 23.4 contains a closed run_manifest child
  set naming cost_schedule_digest. It does not: Design section 23.4, "finite BCEG-1 `CORRECTED_V2` corpus, `RESULT_SURFACE.run_manifest" names only the run_manifest container.
  W276C-F07 and T340 M6 explicitly confirm the missing child schema. The node is stopped as required.
- W341-D03: The lane prompt and W279C-F02 call the fee_events member list a section-23.3 closed set.
  Section 23.3 at Design section 23.3, "23.3 Closed `fill_events` and `exit_events" closes fill_events and exit_events; the fee list is actually lines
  427-433 plus the common kernel_semantics_version rule at Design section 23.4, "The section-22.1 closed envelope supplies".
- W341-D04: Each committed RULE2-08 instrument record points source_locator at the mutable design
  path and carries source_sha256 0ab0accb...e6fc, while the current file at that locator hashes to
  137180ae...7c62f. The manifest nodes use the immutable record's provenance value, but the historical
  raw source preimage is not available at the current locator.
- W341-D05: scenario_catalog.json line 2398, in the out-of-scope PROBE-P012-08-A row, still names
  /EVENT_SURFACE/cash_events/1/signed_delta. After the design-directed removal of the pre-window fee
  row, the funding cash row is index 0. The catalog edit fence permits only the two RULE2-08 rows, so
  this PROBE row was not changed.
- W341-D06: DERIVATIONS.md is insertion-only, so the superseded W321 A:1 fee derivation remains at
  lines 4657-4664 and 4751-4762. This W341 entry records the current authoritative re-derivation.

## W341B - projection pair and 08-A pointer following the W341 window correction

Authority: `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md`, measured 1664 lines and
SHA-256 `137180aee4834fa6b87932e289d7ce8cf56d9471c08e7b53982445598347c62f`.

### W341B-A. RULE2-08-RED fee-events projection

Design section 22.6, "same-timestamp INCLUDE, and no other" says the RED `observation_window` is
`[2000-01-01T00:00:00Z,2000-01-01T00:01:00Z]`, "excluding the candidate setup fill."
Design section 22.6, "same-timestamp INCLUDE, and no other" says that OPEN fill is pre-window and pays the fee. Design section 2.1, "the typed row's signed" requires "every fee or funding
delta" to be present once in `cash_events[]` and once in its typed projection, joined one-to-one.
The current golden consequently has `fee_events: []` and only the funding row in `cash_events[0]`
(`golden/corrected_vnext/RULE2-08-RED.json:33-38`). Its fee-events node is therefore `A:0`.

Design section 15.3, "the exact unpadded legacy shape" say that a declared container value is "the container's cardinality as a
non-negative integer," expanded to a container of that length. That rule is inside the legacy-state
member list at Design section 15.3, "Container kind and length prevent". The corrected selector has a different exact shape at Design section 15.3, "Container kind and length prevent":
`selector`, `node_kind`, `source`, and `design_lines`; it admits no `value` member. The committed gate
reader enforces that exact four-member set and resolves its value from the corrected artifact
(`C:\WP012BUILD@HEAD:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/tests/corrected_vnext/verify_bceg.py:3590-3609`).
Accordingly the catalog's corrected selector already resolves dynamically to `PRESENT(A, A:0)` and
must remain byte-identical; inserting `"value": 0` would make the selector invalid.

Design section 15.3, "states are unequal. This explicitly" says: "Differs means the two tagged states are unequal" and explicitly counts
present-versus-absent. Legacy `ABSENT` versus corrected `PRESENT(A, A:0)` therefore remains
`DIFFERS`; the relation is unchanged.

### W341B-B. PROBE-P012-08-A comparator pointer

Design section 14, "event. The corrected-expectation check must refuse at the cash-delta" says: "flip the sign for the long positive-rate event"; independent expected
`-0.1` differs from actual `+0.1` at the cash-delta node. After the window correction, the only
`cash_events` row is the funding row at index 0
(`golden/corrected_vnext/RULE2-08-RED.json:33-34`). Design section 15.3, "a fraction or exponent is" define the comparator result
as the first unequal node from the recursive walk. Design section 15.3, "token with a fraction or" say to emit the current node first,
visit object keys in UTF-8 byte order, and visit array indices in ascending order. `cash_events`
sorts before `funding_events`; the equal row/container identities are visited first, then the first
unequal leaf is `signed_delta` in array index 0. The derived pointer is therefore
`/EVENT_SURFACE/cash_events/0/signed_delta`, replacing
`/EVENT_SURFACE/cash_events/1/signed_delta`. The row note is synchronized because it stated the old
index; no other probe-row member changes.

## Discrepancies

- W341B-D01: The lane prompt applies the cardinality `value` rule at Design section 15.3, "The 2.0.0 side, either a" to the
  corrected side (`LANE_W341B_CATALOG_FOLLOWUP.md:14-19`). In the current design those lines are
  inside the legacy declaration, while the corrected selector's exact member set at Design section 15.3, "The 2.0.0 side, either a"
  excludes `value`. The committed reader independently enforces that exact set at lines 3590-3609.
  Repository/design evidence wins under C-2, so the requested explicit corrected-side catalog value
  is stopped; the selector continues to resolve the current golden's `A:0` dynamically.
- W341B-D02: The prompt says the current catalog corrected side was sealed as explicit `A:1`
  (`LANE_W341B_CATALOG_FOLLOWUP.md:14-18`), but the pre-W341B snapshot contains only the selector,
  `node_kind: A`, source, and design lines, with no cardinality member
  (`C:\tmp\SNAPSHOTS\20260903_1739_preW341B\scenario_catalog.json:2027-2035`).
- W341B-D03: The prompt cites Design section 15.2, "INPUT`, `EXPECTED`, `OBSERVED`, `KERNEL`, or" for divergence
  (`LANE_W341B_CATALOG_FOLLOWUP.md:20-21`), but line 543 is blank in the measured v1.15 design. The
  governing present-versus-absent divergence rule is at Design section 15.3, "states are unequal. This explicitly".

## W345 - record digests on the fifteen goldens under owner decision Q-C

Owner decision Q-C (a) is recorded at
`C:\tmp\LANE_PROMPTS_20260828\OWNER_QC_A.txt:1`. The pre-edit snapshot is
`C:\tmp\SNAPSHOTS\20260903_195412_preW345`; its 17-source-file checksum manifest is
`C:\tmp\SNAPSHOTS\20260903_195412_preW345\SHA256SUMS.txt:1-17`.

The current design names the fee-row schedule digest at
Design section 13, "role all come from the" and closes the four manifest digest
members and their recipes at `Design section 23.4, "the exact raw source document/response bytes, copied"`. Exact record bytes and detached
sidecars are authoritative under `Design section 5.1, "detached `<file>.sha256` contains the lower-case"`; the source-document digest is
copied from InstrumentRecord provenance rather than from the record sidecar
(`Design section 23.4, "the exact raw source document/response bytes, copied"`). Each sealed input binds the same I/C/F ids and record hashes on its
single line under `tests/corrected_vnext/contracts/inputs/<golden>:1`.

In the table, I/C/F paths are below
`C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\core\economic_records\`.
Every named record and its adjacent `.sha256` is a one-line committed file (`:1`); targeted Git
status for this record root was empty. Sidecar and independently recomputed values agreed for all 45
records. `fee` is the number of fee-row `schedule_digest` nodes using C; `nodes` also includes the
four manifest nodes.

| Golden | nodes / fee | I record and SHA-256 | C record and SHA-256 | F record and SHA-256 |
|---|---:|---|---|---|
| RULE2-01-GREEN | 5 / 1 | instruments/SYNTH-INSTRUMENT-RULE2-01-GREEN-V1.json:1 / 2d8a75cb156c2d2709d5a505a6d1b267e6608cfef5a577f61f2a506382dbe3dd | costs/SYNTH-COST-RULE2-01-GREEN-V1.json:1 / a18832f5574b75c4ffd2284e929b0c465f7b390a1724159f8d369dbc41ec4633 | funding/SYNTH-FUNDING-RULE2-01-GREEN-V1.json:1 / baeddddba25249877943f20fa72cebb348b0d37130ea4c1468ef98f04121eb68 |
| RULE2-01-RED | 5 / 1 | instruments/SYNTH-INSTRUMENT-RULE2-01-RED-V1.json:1 / e3612111ca302bc86dfac316efb80d08aac12a8312287e7117b0115f289e1e5d | costs/SYNTH-COST-RULE2-01-RED-V1.json:1 / 39e569711f4059329430402adc50543c392c4d358bd6ec8e78489718b185a3ce | funding/SYNTH-FUNDING-RULE2-01-RED-V1.json:1 / 742910b2fc30c9d8c4f6ba447661230fad1ef7f71470c9f8aea846b0d06200c1 |
| RULE2-02-GREEN | 5 / 1 | instruments/SYNTH-INSTRUMENT-RULE2-02-GREEN-V1.json:1 / b3d480a84a2eb716bab12dca46483cb0372a64eb2cdbb85072521a103982c817 | costs/SYNTH-COST-RULE2-02-GREEN-V1.json:1 / 5d2fbe4f65f64e7b8b7ebf4cbb27c2b1daa43d7306655d883ae20822c3c44783 | funding/SYNTH-FUNDING-RULE2-02-GREEN-V1.json:1 / ba87c50c8fb4ee594526eb45c0ba47e77ebd9d65270e8d9ee27d250394771957 |
| RULE2-02-RED | 4 / 0 | instruments/SYNTH-INSTRUMENT-RULE2-02-RED-V1.json:1 / 527ae2deeb8360548c32d98cc7d3b0907288acb8549f6aace331852e18411946 | costs/SYNTH-COST-RULE2-02-RED-V1.json:1 / 2ebdfd2a4080cc779951d05e14dfd76517a2f08faf567fb9900b533f3ad74ce7 | funding/SYNTH-FUNDING-RULE2-02-RED-V1.json:1 / d73c96ed5cb8f8f3915f1ac4e69bbad85ceeaba7d56bd7c48644698d93d96968 |
| RULE2-03-GREEN | 4 / 0 | instruments/SYNTH-INSTRUMENT-RULE2-03-GREEN-V1.json:1 / dbc58337b036055593aaa88be054e405375204450e72a50612b0dd68179d9585 | costs/SYNTH-COST-RULE2-03-GREEN-V1.json:1 / 05ca006ccbba614eb0f8177181ac24d2e0b166d12db7826e00df79df279339c0 | funding/SYNTH-FUNDING-RULE2-03-GREEN-V1.json:1 / 3e2e121e537ad234802ed82e2ce6a39a75ea3f51bdf1fd072febbede6717cbf0 |
| RULE2-03-RED | 4 / 0 | instruments/SYNTH-INSTRUMENT-RULE2-03-RED-V1.json:1 / 498ae36ea28a7f40df519724b1fb80d98a68c7261cda8fc7c0c3d6893c909a9a | costs/SYNTH-COST-RULE2-03-RED-V1.json:1 / 9f391fcb1d19d9d7ad23f18c079631d976a895e09e8de135eed315d04642f4bb | funding/SYNTH-FUNDING-RULE2-03-RED-V1.json:1 / 38d3b55db92dc6f5c4864dd19a39492bd3306b01a10bc8767f08a1819c2eaf5f |
| RULE2-04-GREEN | 4 / 0 | instruments/SYNTH-INSTRUMENT-RULE2-04-GREEN-V1.json:1 / f71d1ab990f1da3d9c55e1960f79af91330908e0927c2b2e54f2020a9f596a11 | costs/SYNTH-COST-RULE2-04-GREEN-V1.json:1 / 95ea0075173c08bd7f8c1ae3ea49b41432823e325abdf29f4fced10affac6272 | funding/SYNTH-FUNDING-RULE2-04-GREEN-V1.json:1 / ba470d56e9468015f8b77a41bb0afa35dda930cb27e535bbb620e3a8abc10397 |
| RULE2-04-RED | 5 / 1 | instruments/SYNTH-INSTRUMENT-RULE2-04-RED-V1.json:1 / 6b707ef71df5e4b6565d2a5ee07a7c5cecc8805ed6b1a8ac9c8f0e4b613850ab | costs/SYNTH-COST-RULE2-04-RED-V1.json:1 / 3376e72230dc21797202a0dab1a16173c0909846ed767eea38047aa7d0775e16 | funding/SYNTH-FUNDING-RULE2-04-RED-V1.json:1 / 963c1e3407b711dc8ad460958b952cefed81d0b4da4b638cbdca865481b90a36 |
| RULE2-05-GREEN | 5 / 1 | instruments/SYNTH-INSTRUMENT-RULE2-05-GREEN-V1.json:1 / 5a101048abd939ecb89470a4125b209b322944764aee924b18a6dbea2540391a | costs/SYNTH-COST-RULE2-05-GREEN-V1.json:1 / 931974624690314deb43969bfe7721a81fd03380e2db36370791b403c5bf517d | funding/SYNTH-FUNDING-RULE2-05-GREEN-V1.json:1 / bd15cbfba5325a7496b0cbb91f16e6791e7455dc01a3e8d62eac025b79f00608 |
| RULE2-05-RED | 5 / 1 | instruments/SYNTH-INSTRUMENT-RULE2-05-RED-V1.json:1 / fcffb9aee0b759f30f8822d2360f6a3a7fdb747389c055e691ebdb0879dd7e51 | costs/SYNTH-COST-RULE2-05-RED-V1.json:1 / 5e133f8b0ceec2069fedc53d8995b3e5ae66873344cbbe9500b139de6dd7c681 | funding/SYNTH-FUNDING-RULE2-05-RED-V1.json:1 / 119ac0d21ed81d084bb4ca80d2b627dcf48e391f0a70173e402c9ff97382d0f6 |
| RULE2-06-EQUAL-PRICE-RED | 6 / 2 | instruments/SYNTH-INSTRUMENT-RULE2-06-EQUAL-PRICE-RED-V1.json:1 / 61b54a3761e99a2669506f1a4c785dc3d70e6abdbb9d993755935e0c93069a63 | costs/SYNTH-COST-RULE2-06-EQUAL-PRICE-RED-V1.json:1 / d0b3d31fac5e9cae42bcae54d63370f81b2a0a304f4e81a73fcbdf015c92223e | funding/SYNTH-FUNDING-RULE2-06-EQUAL-PRICE-RED-V1.json:1 / 93288e17b686ae9179aec7a38aca6d3f8dbbd37e23c85a09ba201dffcc0a8c6b |
| RULE2-06-GREEN | 5 / 1 | instruments/SYNTH-INSTRUMENT-RULE2-06-GREEN-V1.json:1 / 3039159a5b35c7bbae8f481abbe99b9a6bb6d376b86bd0e71129edddde249d64 | costs/SYNTH-COST-RULE2-06-GREEN-V1.json:1 / 7d8510ce6ee3101754fb6d7ffb55fa09109c3d3dda07b7b4d01c0d99a7913abf | funding/SYNTH-FUNDING-RULE2-06-GREEN-V1.json:1 / f3df84929ce109d51f6b4ea82924ee0850404d3f4c1abc6885642fa5eeb1b313 |
| RULE2-06-RED | 6 / 2 | instruments/SYNTH-INSTRUMENT-RULE2-06-RED-V1.json:1 / da5428f48b4b8141af15cf81bb25653ef8838f2694c00ec32083de1459f318d4 | costs/SYNTH-COST-RULE2-06-RED-V1.json:1 / eac27b27e42a843404e09a3778a5cd960afdde269469b854358c44bb048dc9ee | funding/SYNTH-FUNDING-RULE2-06-RED-V1.json:1 / 48a51d3129b433131c79d841c5065a54b169c1d7bc6f95e54125767ff070277a |
| RULE2-07-GREEN | 4 / 0 | instruments/SYNTH-INSTRUMENT-RULE2-07-GREEN-V1.json:1 / ae208b1e578362f005f11ebe48addc4b405950fc63c0f57cf9853c3eedc1e614 | costs/SYNTH-COST-RULE2-07-GREEN-V1.json:1 / 040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe | funding/SYNTH-FUNDING-RULE2-07-GREEN-V1.json:1 / 9e732a45d61e44c3d377200ef26a26a55d20eebb4213d300d03be109d10641ce |
| RULE2-07-RED | 6 / 2 | instruments/SYNTH-INSTRUMENT-RULE2-07-RED-V1.json:1 / f25b99e512c1efe24eebd10326cd39c7c370723d39c9c3ca5ec3c29851268df4 | costs/SYNTH-COST-RULE2-07-RED-V1.json:1 / 806e98512a3eb336538c8b68a52cef3ed80897cd2a87d9f270900c7ba094f29b | funding/SYNTH-FUNDING-RULE2-07-RED-V1.json:1 / c7c6001c331a518b31e05f5d9bcbabac2977dabf438aff4d58f10dce2bee4a19 |

All 15 InstrumentRecords carry
`provenance.source_sha256=0ab0accb2711da0661a97b437ccf2d15cc64b123ec3c28d93e6944ec0640e6fc`
on their cited line; that value supplies all 15 manifest source-document nodes under design
`Design section 23.4, "it is not the record-file sidecar digest"`. The result is 73 marker
replacements: 60 manifest nodes plus 13 fee-row schedule nodes. Every
corresponding `blocked_cells` row was removed, leaving only the existing metrics row in each golden;
every `authored_value_tokens` array is byte-equivalent as parsed to its snapshot counterpart. No
source-event digest occurs in these fifteen surfaces, so no unfixed source-event preimage stop was
encountered.

| Golden | Before SHA-256 | After SHA-256 / catalog expected-artifact pin |
|---|---|---|
| RULE2-01-GREEN.json | 38b79ef1cd114724c63e665f3f0e18a478e0693b79ee49356426561a6aaa597a | 27891e5eddc7e604e2087e9d39c9266d5825cefc16ea4a5c7672be57357d7458 |
| RULE2-01-RED.json | 74f6f80cd44f7f980c3f0b332681bcc34e0a4f5a21bf567c84a17b14aacc38fa | 3cf30e13db25a99093d9087c374c05dabbc6ca0a33ad6cebdfdd1d28df42b94d |
| RULE2-02-GREEN.json | aefa016537dd342e307a974c97b513fcbd1c9ef140ef7bfaee5a62b648b6a146 | 5cf90e11a1b5251d7615cd9001a35ec5673d7297ac716d4f6448a9292bd7a822 |
| RULE2-02-RED.json | b6b4e4bfb21c162cdee84e49762357f543afc6bf72320765748d70bdc030388d | 82c4651527a16c0daa21927ec7ae643ad0a5041eeebf3314f36b84a2435a10a0 |
| RULE2-03-GREEN.json | c10b5e71d7c84ccdc8668cb081ba5b394d3fbeba2119a0a53eeb96c9f4fea880 | 46b93e223eb7e5733ba5ef6d7e50345f5665437d9552c8852a8d2c04b9f631b9 |
| RULE2-03-RED.json | e04ddf0cdd14c68076ddd1b081467ee21fafb836d7a51751990bfb361b1bb724 | d475b8096699a1df6d0985f4b67eeda86c6b96dca36778da683fc859058e96b0 |
| RULE2-04-GREEN.json | 7309d4cbe1445cea9d8ccb4ca44bc91e81e45fd8c157fa3daed3b295561ba7f7 | 5384c298d0d103b67b8d9968267a4a4b736f5c75430cf623f61e80f0a9f025c5 |
| RULE2-04-RED.json | 50a990c2005ade1fa5db41cdd00f7bd194e0e89db1f3cd1b24d3d71e693aa85c | f31e3b879599e4fbc621fd4410944896a39aeac9411c59dff42164d8eb87b2b3 |
| RULE2-05-GREEN.json | 26bbb48caf2fb2c5f9f13f08f23664ede89f31c9bfa337d9b878ab68ffa19798 | b68bf0bb5975cc06c3f47fdf795221c8e255b88c9329f770558d97af2b7732f8 |
| RULE2-05-RED.json | 88197710a9a767a130d794dbbebe56a81fe9ef990081d3c15171b574e25dbc9a | 9a59aada281a548192e18e0333fad3fadfa8c19cbd17d603943a453a98193242 |
| RULE2-06-EQUAL-PRICE-RED.json | c05a51eb1e03b8864c495a3d48d3ccd722a2d598489038f055d755f32cb31de0 | 49c845eb7234e464dd29fea2dd79bae2aba1289afc2f8cff8c0d94729e89d590 |
| RULE2-06-GREEN.json | 45f10ddb072e19b2dae4473e09c6af74268bef11bb64247eea94dc8d0538cda2 | 1df73f308d3695f16ba1ee27fac598fea58cd0509c41da478af270293e20fb75 |
| RULE2-06-RED.json | 9d9d3a9748571d63c8790d9b7ef5df398ed945f75c59b7148975debfe167a581 | 6dcbefed552d175a25f7668e430d873715d7846782c34d33c8569bf2e4bde9ab |
| RULE2-07-GREEN.json | 1acd5a74f98d22165971486d6a2ede029f58bf984f85181617055ca473644a4a | f23d1d83007ce27f2094dcb6931021a4850c8a48d7e509da458e18d1efbe92ac |
| RULE2-07-RED.json | e4d966eee8587ca3d645e3abd9a98847daf8f41a3743250563624975f926435b | b26e0fafe9b61f319c25174792d735a0fe9a85cb9458cfa5addd7d992b1df1c4 |

Only the 15 corresponding `expected_artifacts.2.0.0.digest` catalog lines changed
(`scenario_catalog.json:30,150,270,378,502,607,717,839,952,1088,1161,1353,1546,1675,1870`).
The pins equal SHA-256 over the final LF golden bytes.

### W345 discrepancies

- W345-D01: The lane prompt's source-event line locators 916-919 and 1045-1054 are stale against the
  current v1.16 design: those ranges now contain the v1.4 change-log heading and CostSchedule text.
  The current source-event description is at `Design section 23.3, "buy-ceiling/sell-floor result; it adds no"`, and the digest
  recipes used here are at `Design section 23.4, "events state their quantities; the"`. No source-event node exists in the
  fifteen in-scope surfaces, so this locator drift changes no golden result.

## W348 - members admitted by design v1.16 (decision 151)

Authority is design v1.16's closed `run_manifest` schema and record-byte recipes
(Design section 23.4, "finite BCEG-1 `CORRECTED_V2` corpus, `RESULT_SURFACE.run_manifest") and its funding cash-row join
and closed member set (`Design section 2.1, "joined one-to-one by `cash_event_id`",Design section 2.1, "joined one-to-one by `cash_event_id`",Design section 23.1, "LONG_ASCENDING_TARGET_PRICE` when target prices decide"`). The pre-edit bundle snapshot
is `C:\tmp\SNAPSHOTS\20260903_202343_preW348`; its checksum manifest covers all 17 goldens plus
`scenario_catalog.json` and `DERIVATIONS.md` (`SHA256SUMS.txt:1-19`).

Every sealed input consumes an instrument, cost, and funding record through its one-line `records`
object (`tests/corrected_vnext/contracts/inputs/<scenario>.json:1`). Fifteen goldens already carried
all four record-digest members after W345 (`DERIVATIONS.md:5071-5140`). The two RULE2-08 goldens were
the remaining cost-record cases: Design v1.16 section 23.4, "cost schedule is consumed; absent" requires `cost_schedule_digest` when the cost
schedule is consumed, and Design section 14, "the existing sealed RULE2-07 cost records under"; Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is"; Design section 22.1, "superseded. For RULE2-08-RED, `cost_schedule_id` is"; Design section 22.6, "00Z) each consuming the record at taker 0.001", and 1221 bind their exact reused
RULE2-07 cost ids and hashes without introducing a new record or number.

This session verified all 51 I/C/F references across the 17 inputs, covering 48 unique record files.
All 48 records and all 48 adjacent sidecars are tracked in the record repository, and targeted status
for the record root is clean. Every recomputed record-file SHA-256 equals both its sidecar and its
sealed-input hash.

| Golden | W348 members added | Exact value | Derivation / authority |
|---|---|---|---|
| RULE2-01-GREEN | none | - | All admitted record-digest members already present from W345. |
| RULE2-01-RED | none | - | All admitted record-digest members already present from W345. |
| RULE2-02-GREEN | none | - | All admitted record-digest members already present from W345. |
| RULE2-02-RED | none | - | All admitted record-digest members already present from W345. |
| RULE2-03-GREEN | none | - | All admitted record-digest members already present from W345. |
| RULE2-03-RED | none | - | All admitted record-digest members already present from W345. |
| RULE2-04-GREEN | none | - | All admitted record-digest members already present from W345. |
| RULE2-04-RED | none | - | All admitted record-digest members already present from W345. |
| RULE2-05-GREEN | none | - | All admitted record-digest members already present from W345. |
| RULE2-05-RED | none | - | All admitted record-digest members already present from W345. |
| RULE2-06-EQUAL-PRICE-RED | none | - | All eleven admitted manifest members already present; no funding-kind cash row. |
| RULE2-06-GREEN | none | - | All eleven admitted manifest members already present; no funding-kind cash row. |
| RULE2-06-RED | none | - | All eleven admitted manifest members already present; no funding-kind cash row. |
| RULE2-07-GREEN | none | - | All admitted record-digest members already present from W345. |
| RULE2-07-RED | none | - | All admitted record-digest members already present from W345. |
| RULE2-08-GREEN | `/RESULT_SURFACE/run_manifest/cost_schedule_digest` | `040c8366a3f5fa23876dea6165f170efd3b1f5f02e2a4774d2175db5586a41fe` | SHA-256 over committed `costs/SYNTH-COST-RULE2-07-GREEN-V1.json:1`; equals its `.json.sha256:1`, the sealed input at `RULE2-08-GREEN.json:1`, and Design section 23.4, "decision 144's by-reference id-and-sha". |
| RULE2-08-RED | `/RESULT_SURFACE/run_manifest/cost_schedule_digest` | `806e98512a3eb336538c8b68a52cef3ed80897cd2a87d9f270900c7ba094f29b` | SHA-256 over committed `costs/SYNTH-COST-RULE2-07-RED-V1.json:1`; equals its `.json.sha256:1`, the sealed input at `RULE2-08-RED.json:1`, and Design section 23.4, "decision 144's by-reference id-and-sha". |
| RULE2-08-RED | `/EVENT_SURFACE/cash_events/0/funding_event_id` | `TEST-FUND-1` | The cash row and `funding_events/0` join by `cash_event_id=CE-FUND-0`; the value equals the joined funding row and sealed input id under Design section 2.1, "the one-to-one row join, while" and Design section 2.1, "the one-to-one row join, while", with the closed funding row shape Design section 23.1, "three kind values and the". |

The committed records are below
`C:\WP012BUILD\MTC_COMMAND_CENTER\01_MTC_PROJECT\00_PYTHON\mtc_v2\core\economic_records\`.
For the two changed goldens, the two InstrumentRecords, two reused CostSchedules, and one shared
FundingSchedule were read in full; every exact-byte SHA-256 matched both its adjacent `.sha256`
sidecar and the sealed input. Both InstrumentRecords also carry
`provenance.source_sha256=0ab0accb2711da0661a97b437ccf2d15cc64b123ec3c28d93e6944ec0640e6fc`
on their one-line record, which agrees with the existing manifest member under Design section 23.4, "source document/response bytes, copied from".

The funding cash-row member is a sealed identity, not a tables-authored token, and the two digest
members are record-derived; therefore neither changed golden's `authored_value_tokens` changes.
No marker was resolved or introduced, so both `blocked_cells` arrays remain unchanged. Provenance is
re-anchored to design v1.16 and each changed golden carries a `w348_admitted_members` ledger.

| Golden | Before SHA-256 | After SHA-256 / catalog expected-artifact pin |
|---|---|---|
| RULE2-08-GREEN.json | `1185758e987bca067eaed98b7dd2ecca322837893010b9a04dfcc04ceb0b796c` | `fec568d4d5912668816b91bd9ddce31757a9a38464b276e2a061380782ff0803` |
| RULE2-08-RED.json | `b4da2832a3218750935f464d4fd91a3a3dd1fdf6d6a46f661f6a3a884d6bba5f` | `5260d9eec444fe59e7af0acef79785d1981dd9f43de125353cbd9966e4f33aa1` |

Only the two matching `expected_artifacts.2.0.0.digest` catalog members changed. All four edited
JSON files parse, retain UTF-8/no-BOM/LF/final-LF byte discipline, and the two catalog pins equal
SHA-256 over the final golden bytes. No kernel was executed and no `observed/` file was read.

## W357 — owner decision 154 citation restyle (2026-09-04)

Owner decision 154, question Q-G, answer **"Cite by section + phrase"**, requires sealed-table
design citations to use a section number and a quoted phrase so later design insertions do not
make them stale by line-number drift.

Rule applied: every numeric design location was replaced by `Design section N, "<exact phrase>"`
(or `Design vX section N, "<exact phrase>"` where the source carried a version pin). Each phrase
is byte-exact in `P012_FRESH_DESIGN_V1.md` v1.18, occurs exactly once, and belongs to the stated
numbered section. No line or path locator remains in a bundle design citation.

| File | Numeric design locations restyled |
|---|---:|
| `CONTRACT_TABLES_MANIFEST.json` | 37 |
| `scenario_catalog.json` | 328 |
| `golden/corrected_vnext/RULE2-01-GREEN.json` | 47 |
| `golden/corrected_vnext/RULE2-01-RED.json` | 43 |
| `golden/corrected_vnext/RULE2-02-GREEN.json` | 38 |
| `golden/corrected_vnext/RULE2-02-RED.json` | 33 |
| `golden/corrected_vnext/RULE2-03-GREEN.json` | 27 |
| `golden/corrected_vnext/RULE2-03-RED.json` | 31 |
| `golden/corrected_vnext/RULE2-04-GREEN.json` | 43 |
| `golden/corrected_vnext/RULE2-04-RED.json` | 58 |
| `golden/corrected_vnext/RULE2-05-GREEN.json` | 48 |
| `golden/corrected_vnext/RULE2-05-RED.json` | 101 |
| `golden/corrected_vnext/RULE2-06-EQUAL-PRICE-RED.json` | 62 |
| `golden/corrected_vnext/RULE2-06-GREEN.json` | 76 |
| `golden/corrected_vnext/RULE2-06-RED.json` | 61 |
| `golden/corrected_vnext/RULE2-07-GREEN.json` | 45 |
| `golden/corrected_vnext/RULE2-07-RED.json` | 72 |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | 55 |
| `golden/corrected_vnext/RULE2-08-RED.json` | 86 |
| `DERIVATIONS.md` (pre-append body) | 477 |
| **Total** | **1768** |

The pre-append last line was:

> SHA-256 over the final golden bytes. No kernel was executed and no `observed/` file was read.

The pre-append prefix is preserved byte-for-byte; this section was appended after it. No expected
value, digest, data node, JSON key, key order, or encoding was changed. `EXPECTED_SEAL_SHA`, the
anchor, and the baseline were not touched; the Lead owns re-seal #17.

## W359 - owner extension of decision 153: the same false independence claim inside this worksheet (2026-09-04)

**Authority.** Owner decision 153 answered question Q-F with option (a). Asked directly on 2026-09-04
whether the same false independence wording carried by this worksheet should be corrected in the same
re-seal, the owner answered **"Correct it too"**. This section records that extension. The finding is
lane W354's discrepancy **D-3**: `DERIVATIONS.md` carried the first-seal independence wording in a
stronger form than `CONTRACT_TABLES_MANIFEST.json` did - it asserted that no corrected-kernel
implementation exists, and named a `git ls-files` search said to return exactly one path.

**Occurrences found: ten**, in nine paragraphs. Lane W354 named one; a search of this whole worksheet
for every sentence asserting that the corrected-kernel implementation does not exist, was not read, or
that a repository search returns nothing or one path found the other nine. Pre-edit line numbers:

| # | Pre-edit lines | Section | The false assertion |
|---|---|---|---|
| 1 | `:44-47` | section 0 independence fence | "No corrected-kernel implementation exists" plus the `git ls-files` search said to return "exactly one path" |
| 2 | `:1042-1043` | D-10 | "no corrected kernel source exists pre-implementation" and "`IMPLEMENTATION_BASE_SHA` is likewise not yet fixed" |
| 3 | `:1796` | R-21 honest limits (v1.5 revision) | "no corrected-kernel source exists" |
| 4 | `:2301` | W-11 honest limits (v1.8 revision) | "no corrected-kernel source exists" |
| 5 | `:2656-2657` | W172 Reading Y honest limits | *exists* arm of "no kernel, adapter, driver, gate, backtest, verifier, generator or baseline exists or was executed" |
| 6 | `:2664` | W172 Reading Y honest limits, same paragraph | "a kernel that does not exist" |
| 7 | `:3018-3019` | Z-8 honest limits (W186) | *exists* arm of "No kernel, adapter, driver, gate, backtest, verifier, generator or baseline exists or was executed" |
| 8 | `:3047-3048` | W200 W-0 independence statement | *exists* arm of "no kernel, driver, verifier, gate, generator, backtest or baseline exists or was executed" |
| 9 | `:3279-3280` | W205 independence statement | same *exists* arm |
| 10 | `:3419-3420` | W224 independence statement | same *exists* arm |

**Measured counts (this session; nothing inherited from W354).** Repository `C:\WP012BUILD`, branch
`feature/wp-p0-12-corrected-vnext-20260831`, HEAD `d32e903a4007593b85aad9aa882a1f049196980d`,
`mtc_v2/core` tree OID `efac978355c89fc38f7592d68556b7c5d7bc9eef`.

| Measurement | Commit | Result |
|---|---|---|
| `git ls-files \| grep -i "corrected_vnext\|economics.py\|semantics.py\|economic_records"` - the sentence's own search | HEAD `d32e903a` | **1316 paths** |
| the same search, `.py` members only | HEAD `d32e903a` | **170 paths**, including `mtc_v2/core/economics.py` and `mtc_v2/core/semantics.py` |
| pattern `corrected_vnext` | HEAD `d32e903a` | 1211 |
| pattern `economic_records` | HEAD `d32e903a` | 1021 |
| pattern `semantics.py` | HEAD `d32e903a` | 12 |
| pattern `economics.py` | HEAD `d32e903a` | 11 |
| the same search | first-seal `108ea066` | **1 path** - `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/test_trailing_exit_semantics.py`, exactly as the original sentence said |
| the same search | `5e8e5794`, first commit carrying this bundle | 41 paths; `mtc_v2/core/economics.py`, `mtc_v2/core/semantics.py`, `mtc_v2/core/economic_records/` all **absent** |
| the same search | `cf36e0c4`, its child | 44 paths; corrected kernel first appears |
| committed `mtc_v2/core/economic_records/**` | HEAD `d32e903a` | 51 `.json` records, 51 detached `.json.sha256` sidecars |

So the original wording recorded a **true** measurement at the first-seal commit and became false as
the build advanced. It is withdrawn, not re-measured, because the property it was standing in for -
that these tables were sealed before the kernel existed - can no longer be carried by a search.

**What replaced the false assertions.** At each of the ten sites the original bytes are left intact
and readable, following this worksheet's own supersession-marker convention (`:3289-3292`), and a bold
`FALSE ASSERTION WITHDRAWN AND CORRECTED BY LANE W359` marker was inserted immediately after the
containing paragraph. The marker at the section-0 fence carries the full measurement and the
replacement wording; the other eight markers name their own withdrawn clause and point back to it.
The replacement wording is:

- **no `observed/` path was read**, and `mtc_v2.core` was not imported - the two machine-relevant
  prohibitions the design actually places on the `CONTRACT_TABLES` producer, alongside authorship by a
  person other than the kernel implementer
  (design `Design section 15.1, "hand-derived from sections 7-14 plus frozen records"`);
- the **derivation source for the record-bound members is the committed economic record bytes with
  their detached `.sha256` sidecars**, which the design permits
  (design `Design section 5.1, "contains the lower-case SHA-256 of those exact file bytes"`);
- the property that the tables were **sealed before the kernel existed** is carried by the design's
  honest limit L14 about the decision-147 `IMPLEMENTATION_BASE_SHA` re-anchor
  (design `Design section 17, "The pre-implementation seal property is carried by the measured history"`),
  **asserted and human-reviewed under section 16, not machine-checked**.

For sites 5 and 7-10 only the *exists* arm is withdrawn; the *was executed* arm stands unchanged.

**One residual design citation restyled (Lead addition, owner decision 154, W357 class).** The single
numeric design locator still left in this file was a bare line-number pointer, **1479**, at pre-edit
`:5132-5133` in the W341 record-provenance section. Measured: design `P012_FRESH_DESIGN_V1.md` v1.18
is 1843 lines, and the line that pointer names is now the separator row `|---|---|` of the
refusal-object table in section 23.4 - the locator had gone stale exactly as decision 154
anticipated. The node the sentence is about,
`instrument_source_document_digest`, is defined in the run-manifest table at `Design section 23.4, "Lower-case SHA-256 over the exact raw source document/response bytes"`, inside
`### 23.4 Closed RESULT_SURFACE, guards, and refusal objects` (heading `Design section 23.4, ", guards, and refusal objects (G76-05c/07/08 / D-13)"`). It was
restyled to `Design section 23.4, "it is not the record-file sidecar digest"`. That phrase is
byte-exact in the design and occurs **exactly once** (`grep -o -F` count 1). No other citation was
touched.

**Change discipline.** The only bundle file this lane wrote is `DERIVATIONS.md`. The manifest, the
catalog, all seventeen goldens, the anchor draft and every lane report were not opened for writing.
No derived value, digest, table row, expected node or economic number moved. The pass is
insertion-only apart from the citation restyle: measured by `diff` against the pre-edit snapshot,
**106 lines inserted across nine marker hunks, one two-line citation replaced by three lines, zero
lines deleted**, plus this appended section.

| Measure | Before | After |
|---|---|---|
| `DERIVATIONS.md` sha256 | `3f23155e6de0718190c27a5fed68a9ee5062e60ee33a1fe410a13e9e5f26243f` | see the W359 report |
| line count (`wc -l`) | 5273 | see the W359 report |

The after-values are recorded in `C:\tmp\LANE_PROMPTS_20260828\W359_REPORT.md` rather than in this
file, because writing them here would change the bytes they describe.

**Line-number consequence** - the class this worksheet already records as W224-D01, W244-D01 and
W262-D01, recorded here and not repaired. Insertions land after pre-edit lines `:47`, `:1044`,
`:1802`, `:2312`, `:2669`, `:3030`, `:3051`, `:3282` and `:3424`. A citation into this worksheet at or
above pre-edit `:47` still lands where it did; one in `:48-1044` sits 45 lines lower; `:1045-1802` 55
lower; `:1803-2312` 62 lower; `:2313-2669` 68 lower; `:2670-3030` 78 lower; `:3031-3051` 85 lower;
`:3052-3282` 92 lower; `:3283-3424` 99 lower; `:3425-5132` 106 lower; `:5134` and below 107 lower.
Each offset was checked against a measured site: pre-edit `:1796` is now `:1851`, `:2301` is `:2363`,
`:2656` is `:2724`, `:3019` is `:3097`, `:3048` is `:3133`, `:3280` is `:3372`, `:3420` is `:3519`.

**Seal.** This file is a `files[]` member, so this edit moves `EXPECTED_SEAL_SHA`. That is expected and
authorised: the Lead recomputes it at re-seal #17. This lane recomputed no seal value, touched no seal
field, and touched nothing in `C:\WP012BUILD`.

The last pre-existing line of this worksheet, quoted to prove this section was appended after it, was:

> anchor, and the baseline were not touched; the Lead owns re-seal #17.

## W363 - two citation defects repaired under owner decision 154 (2026-09-04, tables family, citation-only)

**What this serves.** Owner decision 154 (question Q-G): *cite by section + phrase*, never by line
number. Lane W357 executed that decision across this bundle. Lane **V357A** verified it
independently, confirmed 982 of 982 distinct quoted phrases are byte-exact and singular in the
design, and found two residues. Lane **V359D** found a third. This lane repaired those three and
nothing else.

**Design measured first.** `P012_FRESH_DESIGN_V1.md`, sha256
`03fdf5952a2365b2de60b55292a1bd50fce8c6c51788c19b59cecc5d8f5b3c94`, 1843 lines, 215194 bytes -
identical to the `$.design` pin in `CONTRACT_TABLES_MANIFEST.json`, whose
`heading_line_map_measured_at_reseal17` also lists the two unnumbered change-log headings named
below as headings in their own right. Every phrase written by this lane was re-verified byte-exact
against those bytes with an occurrence count of exactly **1**.

**Defect 1 - section named, phrase in an unnumbered change-log block: 9 sites repaired.**
In the design's own heading structure `## v1.4 change log — micro-fold (owner 2026-08-31 "design a")`
and `## v1.5 change log — input-embedding addendum (owner 2026-08-31 `1a`)` are `##` headings: siblings
of `## 21.` and of `## 22.`, and higher-level than `### 22.8`. Text inside either block is therefore
not inside the numbered section that precedes it. Nine citation sites quoted such text while naming
`Design section 21` or `Design section 22.8`; five of the seven distinct phrases are the change log's
own heading text, so the citation did not resolve. Each locator was re-cited to
`Design v1.4 change log` or `Design v1.5 change log`; every quoted phrase is byte-identical to what it
was. Sites: `DERIVATIONS.md` lines 8 (twice), 135, 1035, 1200 (twice) and 4640;
`golden/corrected_vnext/RULE2-08-GREEN.json` `$.provenance.design_lines`;
`golden/corrected_vnext/RULE2-08-RED.json` `$.provenance.design_lines`.

**Defect 2 - bare numeric design locators in this file's running prose: 32 repaired.**
Thirty-two colon-plus-digits locators whose sentence named the design (`section N`, "design", `v1.x`)
and named no other file were stale by roughly 570 lines: they pointed into the v1.5-era and v1.8-era
design, which had 967 and 1273 lines against the present 1843. Each was found by its words, not by
its number, and restyled to `Design section N, "<byte-exact phrase>"`. One of the thirty-two named no
design text at all - it asserted that section 23 runs to the end of the file, and gave that end as a
number - and was restated as "runs to the end of the file"; no number replaced it.

**Defect 3 - two live numeric design locators introduced by W359: 2 repaired.** The two
`design`-prefixed numeric pointers written into the W359 record section were live citations, not
quoted historical specimens, and are restyled to `Design section 23.4, "<byte-exact phrase>"`. W359's
own self-check searched only for the spelling `design line <number>`, which cannot see the
backticked-colon spelling it had written; a check must match the form being eliminated, not the form
the checker happens to write.

**Deliberately excluded, and why (39 locators, none touched):**
- **20** in the W205/W224 residue tables headed "Site (this file, current numbering)", **2** more at
  the section 0.3 correction-row C-04 marker and the W186-D01 marker, and **1** at the W359 "pre-edit
  lines" pointer: these are locators into *this worksheet*, not into the design. Decision 154 governs
  design citations.
- **10** in the W359 census table headed "Pre-edit lines": quoted historical specimens inside a
  correction record, evidence of a past state.
- **6** in **W200-D03**, "line drift between v1.8 and v1.9 citations". These are design locators, but
  the numbers *are* the record: the paragraph's entire content is that one design text sits at two
  different positions in two versions. Replacing both with the same section+phrase citation would
  assert that no drift occurred. Reported in `W363_REPORT.md` rather than repaired; no number was
  invented and none was removed.

**Byte record.**

| file | sha256 before | sha256 after citation edits | bytes | lines |
|---|---|---|---:|---:|
| `DERIVATIONS.md` | `beb4ff4e6d45fa469db7c67244ed5e1da55b5311e313e8206f83ab1400d4a60e` | `051866adb35e8ba67db12e4d0097d004d8c6b3fe698700f9ae1e409f78bca907` | 449084 -> 450976 | 5492 -> 5492 |
| `golden/corrected_vnext/RULE2-08-GREEN.json` | `b1dbd1161bc4404a6804d880367cb4ed4df56028e5ae9fe1458a9d51d313a3ea` | `7e3b886e4899472c0a92c921f8e27e8c172e46d4bb7c8e29ff6c1314aab4ee69` | 15021 -> 15024 | 93 -> 93 |
| `golden/corrected_vnext/RULE2-08-RED.json` | `913a2e34468c7656d0bfed120a3ae17614c0f2b363d726c4dbc7f6791a0db1e1` | `7302ad0eda8a461ce70c19b25264a260fec85bd34aa02bbaf051faba11da8ae3` | 30019 -> 30022 | 125 -> 125 |

This section is itself appended to `DERIVATIONS.md` after those digests were taken, so this file's
final digest is not self-stateable here; it is recorded in
`C:\tmp\LANE_PROMPTS_20260828\W363_REPORT.md` for Lead re-seal #18. On both goldens the only leaf
that moved is `/provenance/design_lines`; key order, key count and every other leaf are
byte-identical. No other bundle member was opened for writing. `CONTRACT_TABLES_MANIFEST.json`,
`IMPLEMENTATION_ANCHOR_DRAFT.json`, `scenario_catalog.json`, `EXPECTED_SEAL_SHA` and every `sha256`
member are untouched; re-seal #18 is the Lead's act.
