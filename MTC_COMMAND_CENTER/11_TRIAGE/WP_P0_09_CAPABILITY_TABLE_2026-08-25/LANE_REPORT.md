# Lane Q Report — WP-P0-09 Capability Canonicalization

**Status:** REPAIR ROUND 5 COMPLETE. **Round 5 answers one binding finding the Lead reproduced independently: GF-32's corrected-vNext arm asserted a false oracle.** It claimed no entry on bars 1 through 5 and a flat end state, on a reading of C21 and C05 that neither rule supports — C21 blocks the bar of the protective exit only, and C05 forbids a *carried* decision, not a fresh one on a later bar's own signal. With `cooldown_bars: 0`, no post-exit cooldown key and fresh raw `(1,0)` on bar 2, the decided rule **must** re-enter there: `0.995000 @ 100.00`, sized off the `995.00` the standing-touch stop leaves, ending long from bar 2 rather than flat. Field 8's aggregate RED claim fell with it and is replaced by per-run axes — `local` shares the corrected run's bar **and** price and differs on quantity alone. GF-33 was swept for contradiction and deliberately left unchanged. Applied and recorded in §2.9. Round 2 answered the Lead's first two diff-inspection findings; round 3 answered five more. **Round 4 answers a single binding finding that supersedes round 3's own defence of its remaining gap:** a fixture may not defer its expected output to a later execution of the code it exists to pin. Five legacy arms did exactly that — GF-32's five enum runs, GF-34's L2, GF-36's L3, GF-37's L3 — and the sibling GF-33 arm did it too. All are now literal, and deriving them found four substantive errors those deferrals had been hiding: two arms whose configuration A cannot express, two whose bars could not reach the branch they claimed to observe, one asserted value that was simply wrong, and one prose instruction to invent a fixture row. Everything is applied and recorded in §2.8. Rounds 1–3 are preserved unchanged in §2.1–§2.7, and rounds 1–4 are preserved unchanged by round 5 except for the four GF-32 fields §2.9 lists. Awaiting the Lead's T0 acceptance audit.

**Date:** 2026-08-25

**Branch:** `feature/wp-p0-09-capability-table-20260825`

**Lane input base SHA:** `fead492b0b87f207aa6e7a259372b9767d4301f9`

**Repair-round evidence base:** `ac873ae7ba835a3b719e3a0485a9d45eb2fe3a90` (the commit carrying the round-0 documents; every citation in the repaired documents was re-read at this commit, in both repair rounds)

**Output commit:** the commit containing this report. A Git commit cannot contain its own final SHA. **No commit, stage, push, merge, rebase or any other Git write was performed by this lane; the Lead owns Git.**

**Citation convention in all three documents:** every citation names a repo-root-relative path in full; the single declared abbreviation is a **same-line continuation** (`` `:N-M` `` binds to the most recent full path on the same line), declared in `CAPABILITY_CANONICALIZATION_TABLE.md` §1.1.

## 1. Delivered outcome

Three analysis-only Markdown files under one directory:

1. `CAPABILITY_CANONICALIZATION_TABLE.md` — **41** indexed decisions (C01–C41), each with A behaviour, B behaviour, Pine reference, the exact disagreement, reasoned canonical semantics, a chosen implementation, and an eight-field literal golden-fixture specification.
2. `COVERAGE_SWEEP.md` — reproducible source and configuration coverage across all 192 A keys under contiguous ranges, B's 17 classes and 205 fields, all 153 Pine inputs, the five modules the audit required be swept, per-case WP-P0-06 mapping, explicit non-economic dispositions, and a negative/absence sweep with the commands that reproduce it.
3. `LANE_REPORT.md` — this scope, repair record, QA and handoff.

Ticket #45 was incorporated as prior authority and **not reopened**: missed decisions always replay for state and are actionable only inside the freshness bound, otherwise skipped with an explained divergence; venue candle timestamps are authoritative, internal state is UTC, host-local time and DST are excluded, and the NTP/drift mechanism remains WP-P0-26 scope. The other half of that same specification line — **"Exact bound values are decided in this table's row"** (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:377`) — is discharged by C27, which decides the two boundaries at `15 s` and `45 s` with both endpoints inclusive to `AGING`. Round 1 deferred them; that was a package-contract violation and is corrected in §2.6.

## 2. Repair round 1 — what the audit found and what changed

### 2.1 Finding 1 (CRITICAL) — C07 violated the accepted sizing contract

**What was wrong.** The round-0 C07 listed `PCT_EQUITY_NOTIONAL` as a normalized method, omitted `VOLATILITY_TARGET`, and specified GF-07 as "requested qty 20 … each output includes snapshot ID and source" — a message carrying both a calculated quantity and a snapshot binding.

**What the contract actually says**, re-read at the evidence base: `SizingMethod` has exactly `RISK_AT_STOP`, `FIXED_QTY`, `FIXED_NOTIONAL`, `VOLATILITY_TARGET` (`MTC_COMMAND_CENTER/contracts/mtc_contracts/sizing.py:17-21`); `SizingRequest` is snapshot-independent, carries exactly one request constant, and carries no executable quantity (`:39-97`; `MTC_COMMAND_CENTER/contracts/README.md:10-13`); the split is `SizingRequest` → `BoundSizingIntent` (`MTC_COMMAND_CENTER/contracts/mtc_contracts/sizing.py:100-121`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1053`, `:1082-1089`); quantities are orchestrator-bound, allocator-computed and Guardian-authorised (`:1143-1150`, `:1186-1194`); and a non-normalizable source rule is `NOT_EXPRESSIBLE` with a named catalogue substitute (`:1283`).

**What changed.** C07 was re-decided end to end. `PCT_EQUITY_NOTIONAL` is deleted from the document. `VOLATILITY_TARGET` is present. GF-07 became six sub-fixtures that assert the *request*, not a quantity, including an explicit rejection case for every forbidden field name and for the literal string `PCT_EQUITY_NOTIONAL`. A's percent-of-equity fallback is dispositioned through §5.4/§5.5 as `NOT_EXPRESSIBLE` plus a named catalogue substitute, because it cannot be written without account state. GF-07's RED (iii) cites the WP-P0-04 lane's own already-proven fifth-member break (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_04_CONTRACTS_2026-08-25/LANE_REPORT.md:119`).

Three further C07 content errors were found while re-reading the source and corrected: `fixed_qty` is not dormant, it is **rejected** unless it equals `1.0` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:457-462`); `equity_source` is not a runtime choice, it is **overwritten to `"Realized"`** before validation (`:614-618`); and the same is true of `use_notional_assert`.

### 2.2 Finding 2 (HIGH) — missing economically active capabilities

Four rows were added, each for a behaviour named in the finding or found directly in its required omitted-module sweep. **No speculative rows were added** for snapshot drift, the allocator/Guardian split, venue edges or debug configuration, per the Lead's correction.

| New row | Why it is a capability, not a note |
|---|---|
| **C38** — swing-break/pivot confirmation state machine | B implements a real 420-line FSM (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/confirmation_layer.py:175-411`) that A and Pine do not have; A ships a same-named module whose every step function returns the raw signal unchanged (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/confirmation.py:93-114`, `:117-131`, `:134-152`) behind fifteen validated configuration keys. This is the third behaviour the round-0 table hid |
| **C39** — entry-event mode and first-eval-bar edge requirement | `entry_mode ∈ {Edge, Signal}` and `first_bar_requires_edge` change the trade population and the existence of the first trade of a window (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:1220-1225`, `:1660-1674`); A cannot express either |
| **C40** — higher-timeframe series construction and alignment | From the required sweep of `htf.py` and `gates.py`: the alignment offset is inferred from data rather than declared (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:144-149`), a named chart timezone silently degrades to UTC (`:75-96`), and B's two HTF paths use two further offsets. This is what corpus cases 147, 155 and 162 turn on |
| **C41** — indicator readiness substitution and MA/MACD equation authority | From the required sweep of `gates.py`: an unready HTF MA is **replaced by the raw HTF close** (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/gates.py:395-402`) and a missing previous histogram by `0.0` (`:217`); separately the two engines seed EMA differently and sample the HTF MA at different rates (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/ma.py:376-406`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/indicators.py:22-29`). **Repair round 3 corrected this row's Pine description and re-derived both decisions:** the tracked Pine has a custom SMA-seeded LTF MA (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:261-273`) *and* built-in HTF/MACD paths that advance on every LTF bar by documented intent (`:903-905`, `:920-921`), so A's per-LTF-bar sampling and A's `0.0` substitution are **Pine-faithful**, and C41 now rejects them on economic grounds it states, not as parity defects — see §2.7 finding 4 |

Eight settings found in the widened sweep are **non-economic** and carry explicit dispositions with reasoning in `COVERAGE_SWEEP.md` §7 rather than capability rows: `debug_mode`, `export_debug_csv`, `debug_dir`, `tick_size_source`, A's `use_notional_assert`, A's `equity_source`, `instrument_symbol` and `instrument_point_value`. Two whole modules — `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fee_model.py` and `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fills.py` — are dispositioned as **legacy non-authority** because neither has any importer in the production tree (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/__init__.py:3-17`; the only reference to `fills` anywhere is one test at `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/test_fill_contract_baseline.py:3-6`). Giving either a capability row would have asserted a live capability that does not exist.

### 2.3 Finding 3 (HIGH) — the WP-P0-06 mapping was not truthful or discriminating

The aggregate row "A 23 soft-pass quantity mismatches → C07-C09" is replaced by `COVERAGE_SWEEP.md` §10, which maps **all 23 soft-pass cases and all 8 unresolved A failures individually**, each with its own `parity_summary.md` block citation, its own capability cited to the implementing line, and its own discriminating fixture.

Reading the per-case blocks surfaced three structural facts the round-0 mapping did not state, and they change the attribution:

- For **all 23** soft-pass cases TradingView, PineTS and Python report the **same trade count** and `PineTS/Python = PASS`; only the TradingView comparisons fail, on a strict **quantity** tolerance. The two Python-side engines agree.
- The eight failures split in two: cases 110 and 111 fail **all three** pairwise comparisons at identical counts (a timing and price divergence); cases 134, 147, 153, 154, 155 and 162 record `TW/PineTS = PASS` with `PineTS/Python = FAIL`, so the A implementation is the diverging one.
- Each case therefore has **two axes**, and §10 names both per case: the varied capability that selects the trade population and, through the stop distance, the sizing input; and the recorded divergence carrier.

Cases 147, 155 and 162 are mapped to **C40 and C41** with **GF-40** and **GF-41** as their discriminating fixtures, and the documents state explicitly that GF-02's Boolean plumbing cannot discriminate an alignment offset or an equation difference.

**B 402/416 attribution corrected.** Round 0 recorded both as "dynamic confirmation" mapped to C03/C04 — which are A's N-bar transform and level-retest transform, neither of which B implements. The case files name the mapped paths: case 402 varies `confirmation.p_right = 14` under the parent "Use Confirmation: Swing Break + Momentum = On" (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/cases/parity_bnd_211_swing_right_bars_v03.json:115-145`) and case 416 varies `confirmation.dyn_update_mode = "ANY"` (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/cases/parity_bnd_217_dynamic_update_mode_v02.json:115-135`). Both are re-attributed to **C38**, with **C23** secondary because both pass only after overlap clipping under an explicitly unresolved raw-count-versus-overlap policy (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:167-173`, `:187-200`).

Five evidence-quality caveats are recorded rather than smoothed over in §10.5, including that cases 105 and 115 did not apply the value they name and that cases 127 and 133 produced no trade-set effect at all.

### 2.4 Finding 4 (HIGH) — fixtures were not implementable

**All 41 fixtures were rewritten**, not only the six named. The audit named GF-10, GF-20, GF-32, GF-34, GF-36 and GF-37 "and every sibling with the same specification gap"; every round-0 fixture had that gap, so every one now uses the eight-field form declared in `CAPABILITY_CANONICALIZATION_TABLE.md` §1.4: type, exact configuration, frozen metadata, a literal bar sequence, ordered typed events, exact fills and quantities, exact end state and reasons, and a named RED discriminator with the `file:line` of the rival behaviour.

Specific repairs:

- **GF-20** previously said "four rows pin …" without defining any row. It now defines **R1–R9 in an explicit table** with side, stop, target, literal test bar and expected fill, so it references only rows that exist.
- **GF-10** and **GF-34** now supply a literal venue margin schedule, literal bars, and the exact liquidation bar, mark price and quantity that schedule produces — plus a `MARGIN_MODEL_UNAVAILABLE` arm with no schedule. **Round 1 and round 2 did not actually deliver that for GF-10:** the three fields disagreed about the capital and the liquidation bar, and the "exact liquidated quantity" was promised and never given. Round 3 closed it — see §2.7 finding 2.
- **GF-32, GF-33, GF-34, GF-36, GF-37** now all set `tw_audit_semantics_mode: "research"`, because every `tw_*` branch is gated on it (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1293-1295`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:294`) — without it the round-0 fixtures would have observed no branch at all. Each also gains a control run at `"off"` that proves the gate.
- **No exact A snapshot is claimed that is not derivable.** ~~Fixtures whose legacy output depends on executing pinned code are given a third, record-it-later type and state the exact tuple to record; fixtures whose output follows from the cited arithmetic over the literal bars assert it. GF-31 is asserted (`1.234567 → 1.23` versus `1.234567`); GF-32's five legacy arms are recorded.~~ **This round-1 disposition is superseded in round 4.** The third type is withdrawn from the table entirely, and every legacy arm is now asserted from its own literal inputs. GF-31's assertion stands unchanged. See §2.8.
- **GF-36 and GF-37** use bar sequences chosen so the modes land on distinct exit bars and distinct `(bar, price)` pairs, which is what makes them discriminating. ~~(GF-36: bars 1, 2, 4; GF-37: bar 1 at `104.00`, bar 2 at `103.00`, bar 3 at `103.00`.)~~ **Both parenthesised lists are superseded in round 4, and the GF-37 one was wrong:** its bar-1 value was the revised stop price, not the fill, and the bar opened below that stop, so the adverse-gap arm fills at `101.00`. The round-4 outcomes are GF-36 bars 1, 2, 3 and 4 at `100.00 / 100.00 / 100.00 / 99.00`, and GF-37 `(1, 101.00)`, `(2, 103.00)`, `(2, 104.00)`, `(3, 103.00)`. See §2.8.
- **GF-19** uses `O=100, H=106, L=94` deliberately: `|100−106| = |100−94|`, so B's `d_high <= d_low` tie resolves high-first and fills the **target** where A hard-codes the **stop** (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:612-619`).
- **GF-40 and GF-41** are new and exist specifically so the 31 corpus mappings have fixtures that can discriminate HTF alignment and MA/MACD equations. **Rounds 1 and 2 left four of their arms as prose** — GF-40 R2 and R3, GF-41 F1 and F3 — which are precisely the arms cases 147, 155 and 162 are mapped to, and GF-40 R4 named a timeframe string A does not accept. Round 3 rewrote every arm literally and corrected R4; GF-41 also gained F2b and now separates four behaviours rather than two. See §2.7 finding 3.

### 2.5 Finding 5 (HIGH) — citation fidelity

**Non-resolving references.** C27, C28, C31 and C35 cited `_AI_MEMORY/MASTER_ARCHITECTURE_DECISIONS_AND_TARGET_STATE_2026-08-19.md`. Two searches confirm it exists nowhere:

```
$ find MTC_COMMAND_CENTER -iname "*MASTER_ARCHITECTURE*" -o -iname "*TARGET_STATE*"
MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md

$ git log --all --diff-filter=A --name-only -- "*MASTER_ARCHITECTURE_DECISIONS*"
(no output)
```

Each reference was replaced with the resolving primary source **and the claim re-derived from it**, not carried over:

| Row | Round-0 reference | Replacement, and what changed in the claim |
|---|---|---|
| C27 | lines 2297 to 2325 of the non-existent `_AI_MEMORY/MASTER_ARCHITECTURE_DECISIONS_AND_TARGET_STATE_2026-08-19.md`, for the fresh/aging bound | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2317-2325`. **The claim changed:** round 0 asserted `venue open + timeframe + 45 s` as a settled inclusive deadline, which is imprecise in both directions — the deadline runs from bar close, and `+ 45 s` is the inclusive end of `AGING`. GF-27 gained an R5 arm asserting `FRESHNESS_BOUND_UNSET_FAIL_CLOSED` (`MTC_COMMAND_CENTER/contracts/README.md:36-38`). **Round 1 additionally marked the two numbers `[OPEN]` and declined to decide them; round 2 withdraws that deferral — see §2.6 finding 2** |
| C28 | lines 559 to 571 of the same non-existent file, for "five route codes, no consumers" | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:226-230` plus a recorded negative search. **A new precise fact was found:** the five route codes are the only `wt_*` keys `validate_config` never type-checks — validation begins at `wt_order_type` (`:569-580`) |
| C31 | line 581 and lines 598 to 610 of the same non-existent file, for the audit-mode branches | The five real branch sites: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:61-62`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:294-298`, `:302`, `:334`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:563-564`, `:1293-1295`. **The claim strengthened:** this key is the master gate for every other `tw_*` key, which forced the GF-32/34/36/37 repairs |
| C35 | line 587, lines 591 to 593 and lines 598 to 610 of the same non-existent file, for "stamped, no consumer" | The two lines that read it: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:133` and `:1050-1057`, where the second is a `debug_mode`-gated provenance dictionary |

**Undeclared shorthand.** Round 0 declared a `core/…` / `defaults.py` / `src/…` shorthand and then also used unprefixed `11_TRIAGE/` document names. All shorthand is withdrawn. Every citation now names a full repo-root-relative path; the one remaining abbreviation, the same-line continuation, is declared in `CAPABILITY_CANONICALIZATION_TABLE.md` §1.1 and is mechanically resolvable.

**False content claims found and corrected.** These were found by re-reading each cited range, not by re-reading the round-0 text:

| Row | Round-0 claim | Source | Correction |
|---|---|---|---|
| C19 | "A touch mode **exposes an explicit collision policy** and defaults to pessimistic stop-first" | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:362-379` | **False.** A hard-codes stop-first and sets `is_pessimistic=True`; there is no policy field, key or branch. C19's chosen implementation changed from **A** to **A-corrected**, since the policy field is an addition. The likely origin of the error is B's dead `fills` module, which *does* declare a four-value policy (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/fills.py:36-47`) but has no production importer |
| C19 | "Pine … resolves **explicit** collision stop-first" | `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:1305-1310` | Pine also **hard-codes** it; "explicit" is withdrawn |
| C30 | all four protective `wt_*` keys are "**without consumers**" | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:581-584` | **Imprecise.** `wt_use_tp` and `wt_use_sl` have a real cross-validation consumer that can reject a configuration |
| C06 | "B … **effectively disables pyramiding**" | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:136-154`, `:1390-1402` | **Incomplete.** B refuses `pyramiding`, `max_pyramid_positions` and `same_bar_reentry_max_per_bar` other than 1, but `signal_mode_max_entries` (1–3) and `signal_mode_cooldown_bars` keep a live same-side add path in `Signal` mode |
| C07 | "`fixed_qty` … declared but not the controlling arithmetic"; "`equity_source` is declared … A's runtime uses a realized/frozen sizing basis" | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:457-462`, `:614-618` | **Understated.** `fixed_qty` is rejected unless default; `equity_source` and `use_notional_assert` are overwritten to constants before validation |
| C12 | B "can fabricate … a **2%** target" | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/tp_calculator.py:163-165`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py:94` | The fallback uses the configured `percent`, whose **default** is 2.0. Restated precisely |
| C12/C11 | ATR `.01` fallback cited to `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/tp_calculator.py:73-80` | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/tp_calculator.py:132-133` | The cited range was the mode dispatch, not the fallback. Range in bounds but **not content-faithful**; re-anchored |
| C14/C15 | A "updates trailing first and applies BE only when trailing does not own the stop" | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:551-558`, `:565-567` | True but it omitted the actual defect: A runs the stop-owner update **before** the same bar's price-exit test, so a revision is effective on its own trigger bar |
| Coverage §2 | A ranges "`146-150`" and "`29-35`" | `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:36`, `:151` | **Two keys fell outside every declared range** — `debug_mode` and `level_proximity_lookback`, the latter economically active and a corpus case. Ranges are now contiguous 29–245 |

### 2.6 Repair round 2 — the Lead's independent inspection of the round-1 diff

The Lead inspected the real three-file round-1 diff with an executable citation parser and against the original package contract, and returned two required corrections. Both are applied. No other round-1 content was altered.

#### Finding 1 (CRITICAL) — the citation-shape claim was false

`CAPABILITY_CANONICALIZATION_TABLE.md` §1.1 declares that a line-range continuation never crosses a line boundary, and round-1 §4.3 asserted that every *sampled* continuation satisfied it. The Lead's parser reported `FULL=497`, `CONT=471`, `ERRORS=143` in `COVERAGE_SWEEP.md`, 2 orphan continuations in `CAPABILITY_CANONICALIZATION_TABLE.md`, and 4 citation-shaped tokens that were neither a full repo-root-relative path nor a declared continuation. **The round-1 claim was an unverified assertion presented as a check, and it was wrong.** Round 1 sampled where it should have enumerated.

**What was actually broken — two distinct failures, not one.**

1. **Cross-row inference.** Most orphans were table rows and list items whose first citation token was a continuation binding to the *previous row's* path. `COVERAGE_SWEEP.md` §2's thirteen A configuration-range rows and §3's sixteen B class rows are the clearest cases: each row opened with a bare line-range while its anchoring path sat one row above. That is exactly the inference §1.1 forbids.
2. **Continuation before anchor.** The rest were lines that *did* carry a full path, but only after the continuation. Every per-case row in §10.2 and most of §10.4 opened its corpus-evidence cell with a bare line-range and named the implementing path one cell later.

**What changed.** Every orphan was expanded to its complete repo-root-relative path on its own line. **The convention was not weakened to permit cross-row inference; §1.1 stands unchanged.** Measured against the round-1 files:

| File | Lines edited for orphan repair | Of those, lines carrying no full path at all | Of those, lines carrying one only after the continuation |
|---|---:|---:|---:|
| `COVERAGE_SWEEP.md` | 111 | 86 | 25 |
| `CAPABILITY_CANONICALIZATION_TABLE.md` | 2 | 1 (GF-07.C) | 1 (C27's `[OPEN]` sentence) |
| `LANE_REPORT.md` | 0 | 0 | 0 |

The affected `COVERAGE_SWEEP.md` sections are §2 (13 range rows plus 3 prose findings), §3 (16 class rows plus 5 B-behaviour rows), §4.1–§4.5 (25 omitted-module rows), §6 (9 Pine range rows plus 1 absence finding), §7 (4 disposition rows), §8 (2 negative-sweep rows), §10.2 (7 case rows), §10.4 (22 case rows) and §10.5 (4 caveats).

**The four suspicious tokens.** Each is named below in a form that is deliberately *not* citation-shaped, so this table cannot itself reintroduce the defect.

| Where | Round-1 token | Round-2 form |
|---|---|---|
| `COVERAGE_SWEEP.md` §8 | bare `core/config.py` with line 62 appended | full path `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:62` |
| `COVERAGE_SWEEP.md` §8 | bare `core/runner.py` with line 133 appended | full path `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:133` |
| `LANE_REPORT.md` §2.5, C27 row | the elided `…2026-08-19.md` form with lines 2297 to 2325 appended | **non-citation prose with no line-number token.** The file is proven not to exist, so no path form would be legitimate. Its three sibling rows (C28, C31, C35) referenced the same non-existent file with the same shorthand and are rendered the same way |
| `LANE_REPORT.md` §2.5, C12/C11 row | bare `tp_calculator.py` with lines 73 to 80 appended | full path `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/tp_calculator.py:73-80` — that file **does** exist, and the range was re-read to confirm it is the mode dispatch this row describes |

#### Finding 2 (CRITICAL) — C27 violated the original package contract

The binding lane specification states both halves of this row: the ticket-#45 freshness-conditional missed-decision policy is already decided, **and** "Exact bound values are decided in this table's row" (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:377`). Round-1 C27 discharged the first half and refused the second: it marked the two numbers `[OPEN]`, said it recorded rather than ratified them, listed them as lane limitation 3, and carried them into §7 as an open issue awaiting owner ratification. The one quantity WP-P0-09 was instructed to decide here was the one thing the row declined to decide.

**What changed.** C27 decides the values, and states them as a rule a fixture can fail against:

| State | Decided comparison, age measured from bar close | Missed decision discovered in this state |
|---|---|---|
| `FRESH` | `age < 15 s` | acted on |
| `AGING` | `15 s ≤ age ≤ 45 s` | acted on; warning only, never a resize |
| `STALE` | `age > 45 s` | never acted on late — skipped and logged as an explained divergence |

Four things are pinned that round 1 left implicit:

1. **The two numbers are decided at `15 s` and `45 s`** — the values §12.3 documents (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2317-2325`).
2. **Both endpoints belong to `AGING`**, so the three states partition the whole age axis with no gap and no overlap. Round 0's phrasing and round 1's silence both left the endpoints undecided.
3. **The age datum is the venue-authoritative bar close** — `age = observation_utc − (venue_open_timestamp_utc + timeframe_seconds)`. Round 1 wrote that definition and then quoted the brief's bar-open thresholds beside it, which double-counts the timeframe. Both forms are now given side by side and stated to be the same inequality.
4. **Both boundaries are frozen-package constants.** A package omitting either does not build, and a consumer handed an unset bound still fails closed (`MTC_COMMAND_CENTER/contracts/README.md:36-38`).

**Why this is not a re-opening of ticket #45.** The policy shape — always replay, act only inside the bound, otherwise skip and log an explained divergence, first action at the next actionable bar close — is ticket #45's and is unchanged. Only the two numbers moved, from documented-and-`[OPEN]` to decided, which is the movement the delivery plan assigns to this row. The brief's `[OPEN]` marker sits in a carrier-assignment paragraph that names owners rather than values (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2332`), and WP-P0-09 is the owner it names for the values.

**GF-27 changed with it.** Field 2 labels the constants as the decided package values rather than a fixture-local choice, and field 8 gains a third RED that mutates the decision itself: `aging_upper_s` from `45` to `30` must flip R3 to `MISSED_DECISION_STALE`; `fresh_below_s` from `15` to `20` must flip R2 to `FRESH`; `aging_endpoints_inclusive: false` must move both R2 and R3. Without that RED the numbers would be a comment, not a decision. The five run arms and their observation timestamps are unchanged, and were already consistent with the inclusive-endpoint reading now decided.

**Documents corrected for consistency:** the C27 index row in §2 of the table, §5's explicit-non-decisions list, and in this report §1's ticket-#45 paragraph, §2.5's C27 row, §4.9's boundary row, limitation 3 in §5 and the open issue in §7.

#### Round-2 verification, and what it is not

`python` and `py -3` are still refused by this session's tool-permission layer whenever a script argument is supplied, so `<scratchpad>/validate_citations.py` still could not be executed here. The check run instead is mechanical rather than sampled, and is described exactly so the Lead can judge it:

1. Enumerate every line carrying a continuation token — ripgrep for a backtick immediately followed by a colon and a digit.
2. Enumerate every line carrying a repo-root-relative `path` plus line-number token.
3. Take the set difference. Any line in (1) and not in (2) is an orphan by definition.
4. For lines in both, emit both token classes through **one alternating pattern** so ripgrep prints them in document order, then read the first token on each line; a line whose first token is a continuation is an ordering orphan.

Run against the round-1 files, step 4 identified **exactly the 2 table orphans the Lead's parser reported** — GF-07.C and C27's `[OPEN]` sentence — which is the evidence that this procedure reproduces the Lead's rule rather than approximating it. Run against the round-2 files, steps 3 and 4 return no orphan in any of the three documents, and the suspicious-token pattern returns no match in any of the three.

**This is still not a machine assertion from the Lead's own parser.** It is a reproduction of its rule with the tools this session is permitted to run. **Round 2's own claim that it "returns no orphan" was, on the SHAPE axis, correct — but it did not check the RANGE axis of each continuation's *binding*, and round 3 found one binding error it had missed. See §2.7 finding 1.**

### 2.7 Repair round 3 — the Lead's second set of findings

The Lead ran its own inline validator against the round-2 diff and re-read the C41 sources. Five findings were returned; all five are applied. No other round-2 content was altered.

#### Finding 1 (CRITICAL) — one citation binding error survived round 2

This report's §2.1 contract sentence named the contracts README with lines 10 to 13 appended, and then, later on the **same line**, carried a bare continuation with lines 100 to 121 appended. Under the same-line rule declared in `CAPABILITY_CANONICALIZATION_TABLE.md` §1.1 that continuation binds to `MTC_COMMAND_CENTER/contracts/README.md`, which is **83 lines long**, so lines 100 to 121 do not exist in it. The intended target was the `BoundSizingIntent` definition in `MTC_COMMAND_CENTER/contracts/mtc_contracts/sizing.py`, and that path is now written out in full on that line. **The offending pair is described here in prose rather than reproduced, so this paragraph cannot itself reintroduce the defect** — the same device §2.6 used for its four suspicious tokens.

This was a **binding** failure, not an orphan: the continuation *had* a full path earlier on its line, so round 2's orphan procedure — which only asked whether an anchor existed — could not see it. Round 3's check resolves each continuation to its anchor and then range-checks it against that anchor's actual line count, which is the axis that catches this class. The corrected line 33 now carries three anchors — `sizing.py`, `README.md` and the architecture brief — and every continuation on it resolves inside its own anchor's bounds.

#### Finding 2 (HIGH) — GF-10 was contradictory and incomplete

Round-2 GF-10 said in field 5 that liquidation fires at **bar 2**, then in field 6 changed `bucket_capital` to `250` mid-sentence and had liquidation fire at **bar 1**, while field 3's common metadata still said `1000`. Field 6 also promised "the exact liquidated quantity" and never gave one. Three statements, three different fixtures.

GF-10.B is now self-contained and arithmetically closed. `bucket_capital` moved out of the shared metadata into a per-sub-fixture value (`GF-10.A 1000`, **`GF-10.B 250`**, `GF-10.C 1000`); the entry is fixed at `20 @ 100.00` by an explicit `entry_qty_override`, because at `250` the sizer would propose `5` and the fixture needs a position the bucket cannot carry; and `PARTIAL_TO_MAINTENANCE` is now **defined**, as the least `qty_step`-rounded `x` satisfying `250 + 20 × (96 − 100) − x × 96 × 0.005 >= (20 − x) × 96 × 0.10`. That gives raw `x = 22 / 9.12 = 2.412280701754…`, adverse-ceiled to the `0.01` step as **`2.42`**, fee **`1.1616`**, post-event equity **`168.8384`**, remaining quantity **`17.58`** and maintenance requirement **`168.768`**. The fixture also asserts that `2.41` is rejected (`168.8432 < 168.864`), and it carries the same formula forward to bars 2 and 3 — `6.13 @ 92.00` at bar 2, **no** liquidation at bar 3 — so config, metadata, events, fills and end state all describe one run.

#### Finding 3 (HIGH) — GF-40 and GF-41 still contained non-literal arms that three corpus cases depend on

Round-2 GF-40 R2 promised a "timezone anchor" with no bars and no timestamps, and R3 said "removes the first HTF window entirely" without enumerating what bars remained. GF-41 F1 gave closes but no timestamps or OHLCV, and F3 was the single sentence "a series whose MACD histogram is `None` on the first qualifying bar". Cases 147, 155 and 162 are mapped to exactly those arms, so three of the eight unresolved failures had no implementable discriminator.

Every arm those mappings reference is rewritten with an exact configuration, exact timestamps, full OHLCV, the expected visible series or indicator value per bar, typed events, and the rival engines' exact outputs. R4 was additionally **wrong**, not merely vague: it set `htf_trend_timeframe: "5"`, which is not one of A's six accepted strings, so it would have raised on the timeframe lookup instead of exercising the shorter-than-LTF path; it now uses `"30"` against a 60-minute LTF, which is the real path (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/htf.py:175-179`). GF-41 F1's round-2 RED also asserted the wrong number for B — it claimed `ewm(span=3, adjust=False)` yields `27.5` on bar 3; the correct value is `22.5`, and B's full column is now given as `10.0, 15.0, 22.5, 31.25, 40.625`.

#### Finding 4 (HIGH) — C41 was not content-faithful about Pine, and its decision rested on that

Round-2 C41 said "`ta.ema` is SMA-seeded, which is the convention A's tracker follows", and chose the SMA seed **because it matches Pine**. Re-reading the tracked Pine shows that is not one claim but a conflation of two different paths, and that the second one inverts the conclusion:

- The **custom LTF** MA, `calc_ma_line`, is explicitly SMA-seeded and explicitly `na` before `bar_index >= length − 1` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:261-273`, with `calc_sma` at `:255-256`), and it is what the LTF `ma_filter` and `ma_slope` gates use (`:785-786`, `:789-791`). A's `MovingAverageTracker` reproduces it exactly.
- The **HTF** path does not use `calc_ma_line` at all. It calls the built-ins on `request.security(..., close[1], barmerge.lookahead_off)` and advances them on **every LTF bar over the repeated prior-closed value, deliberately** — the file says so in its own comments (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:903-905`, `:920-921`, with the code at `:906-918` and `:922-934`). **A's `HtfMovingAverageTracker` is a faithful reproduction of that**, not a divergence from it. The round-2 row treated A's per-LTF-bar sampling as an A-only defect; it is a Pine-faithful behaviour.
- The seed of the TradingView built-ins is not present in this repository, so no `ta.ema`-equivalence claim can be supported in either direction, and C41 now makes none.

Both decisions are re-argued from consequence rather than resemblance. The **SMA seed** is chosen because a first-value seed makes the estimator a function of where the data window starts — so two runs beginning one bar apart disagree forever, a live restart does not reproduce the series it replaced, and the estimator returns a value before it has `length` observations, which makes C23's warm-up undeclarable; B's own internal inconsistency (`ema` first-value-seeded, `rma` SMA-seeded, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/indicators.py:22-29`, `:32-59`) is evidence the first-value seed was not a decision. Agreement with `calc_ma_line` is recorded as corroboration, not as the argument. The **one-sample-per-closed-HTF-bar** basis is chosen in **knowing divergence from Pine**, because per-LTF-bar feeding makes the declared length mean LTF bars rather than HTF bars, makes the estimator's value depend on the execution granularity used to observe it, makes it depend on LTF data completeness, and makes warm-up undeclarable. The cost is stated in the row: cases 147, 155 and 162 will not reproduce the TradingView workbook after the change, and what survives is a declared-property claim rather than a numeric-identity claim.

Two further Pine facts were found while re-reading and are now recorded rather than left implied: A's `0.0` substitution for a missing previous MACD histogram **reproduces Pine** (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:999-1002`), and A's loose multiplicative HTF buffer **reproduces Pine** (`:1040-1042`). Both are still rejected, and the row now says plainly that it is rejecting a Pine behaviour and why.

GF-41 was rebuilt to discriminate all four: **A**, **B**, the **custom Pine LTF** path and the **built-in Pine HTF** path. F1 separates B from `{A, custom-Pine-LTF}` on the seed and asserts the A-equals-Pine agreement as a GREEN. F2 uses `SMA` deliberately so no built-in seed assumption is needed, and asserts that A **and** the built-in Pine HTF path both read `108.00` on the `09:00`–`11:00` bars where the decided rule reads `104.00`. F2b isolates the buffer sign on a bar where all three compute `104.00`, producing four distinct verdicts. F3 produces three distinct verdicts on its bar 4. F4 isolates the raw-close substitution in the opposite direction to F2.

#### Finding 5 (MEDIUM) — the account of the citation validator was not truthful

Round 2 wrote that "a reproducible validator was written to `<scratchpad>/validate_citations.py`", gave its invocation, and said it was "left in the scratchpad for the Lead to run" and that "running the validator remains the first action the acceptance audit should take". That presented an artifact the Lead has no access to as though it were part of the deliverable, and it implied the Lead's audit was waiting on this lane's tooling when in fact the Lead had already run its own. §4.3 and §5 are rewritten to say what actually happened; see the corrected §4.3 preamble.

### 2.8 Repair round 4 — the deferred-oracle finding

The Lead returned one binding finding: **GF-20, GF-32, GF-34, GF-36, GF-37 and any sibling with the same gap must be literal, implementable specifications with exact configuration, OHLCV, metadata and ordered events, fills, prices and states; an arm whose oracle is "whatever the pinned legacy code produces" is not one and is forbidden.** Round 3 had defended those arms as principled restraint (§5, limitation 2). That defence was wrong, and round 4 withdraws it. Rounds 1–3 are otherwise preserved: no decision, no canonical rule, no citation and no other fixture changed.

#### Why the defence was wrong

A deferred oracle is not a cautious specification, it is an **unfalsifiable** one. Its expected value is defined as the output of the very code the fixture exists to pin, so it agrees with that code by construction and can never fail. It therefore cannot detect the one class of error it is most exposed to: that the arm's own inputs never reach the branch it claims to observe. Round 4 derived all six deferred arms by hand, and **four of them were broken in exactly that way**:

| Arm | What deriving it found |
|---|---|
| **GF-32**, all five enum runs | The declared bar 1 was `99,99,94,96` under `execution_profile_id: "close_only_deterministic_v2"`. A close-only long stop fires only when `bar.close <= stop_price` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:434-443`), and `96 > 95.00`. **No protective exit occurred**, the protective-exit bar index was never recorded (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1289-1291`), and every one of the five branches returned early on its own `is None` guard. Five arms observing nothing. Separately, `tw_reversal_reentry_delay_bars: 1` collapsed three of the five enum outcomes onto one bar, so even a correct recording would not have discriminated them |
| **GF-34** L2 | Two independent defects. Its `sizing_method: FIXED_QTY, requested_fixed_qty: 20` names a method **A does not have** — `calc_qty` offers risk-at-stop and a percent-of-equity fallback and nothing else (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:43-55`). And even granting `20 @ 100.00`, at `initial_capital 1000` and a leverage-derived margin fraction of `0.20` the legacy deficit is `1000 − 16m`, positive only below a mark of `62.50`, while the lowest price in the declared bars was `84`. **The branch could not fire**, so L2 would have recorded "no margin call" and the row's whole claim — that the legacy branch fabricates a loss — would have gone untested |
| **GF-36** L3 | Field 2 read `execution_profile_id: "raw_close_only_v1"` **disabled** in favour of "the touch profile", naming a profile A does not declare. A has exactly two (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py:10-15`) and its close-only predicate matches only `close_only_deterministic_v2` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:560-561`), so `raw_close_only_v1` **is** the touch path. Same `FIXED_QTY` defect as GF-34 |
| **GF-37** L3 | Same two configuration defects, and deriving L3 exposed that **the round-3 asserted value for L1 was wrong**: `104.00` is the revised trail stop, not the fill. A writes the revision before the same bar's price test, bar 1 opens at `101` — already below `104.00` — so the adverse-gap arm fills at the **open**, `101.00` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:400-402`). An arm asserted at the stop price would have passed against an implementation that ignores the gap rule entirely |

The two arms that were merely deferred rather than broken — GF-33's `delay = 2` arm and GF-29's legacy payload — are now derived too. **GF-29 never needed an execution at all:** Pine's entry payload is a literal string concatenation of constants and inputs with no strategy state in it (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:2020`), so its exact bytes follow from that line and the input defaults (`:181-188`).

#### What changed, fixture by fixture

| Fixture | Round-4 repair |
|---|---|
| **GF-32** | Bar 1 close `96 → 94` so the stop is reachable; `tw_reversal_reentry_delay_bars` `1 → 2`; sequence extended to six bars with bar 3 carrying **no** raw signal and an open (`99`) that differs from its close (`100`). All five enum outcomes now derived and asserted, each with the predicate that produces it: `local` bar 2 @ `100.00`; `carry` bar 3 @ `100.00` on a signal-less bar; `next_bar_open` bar 3 @ the **open** `99.00`; `next_bar_close` bar 4 @ `100.00`; `delay` bar 5 @ `100.00`. Quantities asserted: `1.000000` at entry, then `0.994000` at a close of `100.00` and `1.004040` at the open of `99.00`, on `instrument_qty_step 0.000001` chosen so A's research-mode six-decimal floor and its step floor agree and cannot confound the timing. **Round 5 supersedes this row on the corrected arm only:** round 4 repaired the five legacy arms and left the corrected-vNext arm asserting no entry and a flat end state, which §2.9 replaces with a bar-2 re-entry of `0.995000 @ 100.00` and a long end state. The five legacy outcomes, predicates and quantities above are unchanged |
| **GF-33** | The `delay = 2` arm is derived rather than deferred: earliest re-entry **bar 5 @ `100.00`, quantity `0.994000`**, against the corrected rule's **bar 5 @ `100.00`, quantity `0.995000`** — same bar, same price, different size, because the legacy close-only stop fills at `94.00` and the corrected standing stop at `95.00`. A third arm holds the delay at `2` and varies only the mode, isolating the **`<` versus `<=`** window asymmetry (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1306-1308`): the same integer key yields deferral windows `{1}` and `{1, 2}` and first admissible bars 3 and 4 |
| **GF-34** | `FIXED_QTY` replaced by A's real fallback path — `fallback_size_pct: 400.0` at `initial_capital 1000` gives exactly `40` under a non-binding leverage cap of `50`. Bars re-chosen against the branch's own threshold (`m < 93.75` at quantity `40`) to `98,98,94,95 / 94,94,88,89 / 88,88,84,85`. L2 now asserts **every** checkpoint, not only the firing one: deficits `−136.00`, `−8.00`, `−8.00`, then `+184.00` at bar 2's low of `88`, where `liquidation_qty = 736 / 17.6 = 41.818…` clamps to the position's `40`, giving `exit_pct = 1.0` — a **full close of `40 @ 88.00`**, realised `−480.00`, equity `520.00`. V2 asserts the decided venue rule over the same bars: `800/380`, `560/356`, `400/340`, **no breach on any bar**, which is what makes "the legacy loss is invented" a falsifiable claim rather than an assertion |
| **GF-36** | Profile corrected to `raw_close_only_v1`, `FIXED_QTY` replaced by risk-at-stop keys yielding `1`. Bars re-chosen to `101,106,99,104 / 103,104,99,103 / 103,106,100,105 / 99,101,98,100`, with no low reaching the initial stop, so every exit is caused by the break-even revision alone. Four asserted outcomes on four bars: L1 bar 1 @ `100.00`, L3 bar 2 @ `100.00`, L2 bar 3 @ `100.00`, V1 bar 4 @ `99.00` — the last an **adverse-gap open**, because only the decided next-bar rule leaves the revision inactive long enough for the gap bar to arrive |
| **GF-37** | Same two configuration corrections. Bars unchanged. L1 corrected from `104.00` to **`101.00`** with the reason stated in the fixture rather than silently swapped; L3 derived as **bar 2 @ `104.00`**, which shares a bar with L2 and differs in price because it anchors on the previous bar's high `107` rather than the current close `106`. Four distinct `(bar, price)` pairs: `(1, 101.00)`, `(2, 103.00)`, `(2, 104.00)`, `(3, 103.00)` |
| **GF-20** | R4 and R8 test bars changed to `109,110,108,110` and `91,92,90,90`, with canonical fills `109.00` and `91.00` against close-only `110.00` and `90.00`. **The prose instruction to re-run a row with a different bar is deleted.** Field 8 now states all four rival close-only fills as numbers, so every gap row discriminates as written and none is contingent on a later re-selection |
| **GF-29** | Retyped `static-validation` and its payload asserted byte for byte from the Pine concatenation, including the three optional segments that are empty under the flag defaults. The one runtime-dependent element, the rendering of `str.tostring(wt_amount)`, is asserted twice — at `100.0` and at `250.5` — so a formatting change fails the fixture instead of sitting unstated |
| **Table §1.4 and §4 rule 7** | The third type is **removed as a type.** §1.4 declares two types and states why there is no third; §4 rule 7 requires every fixture to state its own oracle and says why the prohibition is not stylistic. The withdrawn name appears nowhere in the table as a live type label |

#### What round 4 did not do

No canonical semantics, chosen implementation, decision-index row, corpus mapping or citation from rounds 1–3 was altered. GF-10, GF-40 and GF-41 — the round-3 repairs — are untouched. C27's decided bound values are untouched. No source, Pine, contract, schema or corpus file was read for anything other than verification, and none was written.

### 2.9 Repair round 5 — GF-32's corrected arm asserted a false oracle

The Lead independently reproduced GF-32's corrected-vNext arm and returned one binding finding, which is applied here. **Round 4 fixed the five legacy arms and left the corrected arm wrong.** No other round-4 content is altered, and no decision, canonical rule or citation from rounds 1–4 is changed.

#### What was wrong

Round-4 GF-32 field 5 asserted "**and no entry on bars 1, 2, 3, 4 or 5**" for the corrected-vNext run, and field 7 asserted that it "ends **flat** at bar 5 with realised `−5.00`". The stated justification was that bars 2 and 5 "carry a live raw signal and are refused because C21 blocks every new entry on a protective-exit bar and C05 forbids a carried decision". **That justification misapplies both predicates, and neither reaches bar 2.**

- **C21 blocks the bar of the exit, not the bars after it.** Its canonical sentence is that a stop, target, margin, filter, time or Guardian exit blocks all new entries **for that bar**, and A's admission permits a same-bar re-entry only after an opposite-signal exit (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py:119-121`, `:137-142`). The exit is at bar 1; bar 2 is outside the rule entirely.
- **C05 forbids a *carried* decision, not a fresh one.** Its rule is that with no same-close reversal "**no stale decision is carried**: a later entry requires a fresh valid decision on its own bar" — which is a *requirement on* a later entry, not a prohibition of one. GF-32's own bar table declares bar 2 as "earliest bar with its own signal", injected raw `(1,0)`.
- **Nothing else in the run refuses bar 2.** The common configuration sets `cooldown_bars: 0`, declares no `post_exit_cooldown_bars` key at all, and disables every gate. Under the decided policy the corrected rule therefore **must** enter on bar 2, and the arm that asserted it does not was asserting the opposite of the rule the row decides.

#### What the corrected arm actually is, derived

The bar-1 exit fills at the standing-touch stop `95.00`, not the close `94.00`, realising `−5.00` and leaving a sizing snapshot of `995.00` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1504-1505`). Bar 2 closes at `100.00`; `sl_percent: 5.0` gives a stop of `95.00` and a per-unit risk of `5.00`; `risk_per_long_pct: 0.5` gives `995 × 0.005 / 5.00 = 0.995000` exactly, with the leverage cap non-binding on either basis (`10.0` on `1000`, `9.95` on `995.00`). Bar 5's raw `(1,0)` is fresh and otherwise admissible and still produces no fill, because `max_entries: 1` and the bar-2 position is open — asserted as a typed `MAX_ENTRIES` block rather than as an absence. The bar-2 stop is a standing order active from the next tradable instant after entry (C11), so bar 2's own low of `94` is not eligible to fill it, and bars 3, 4 and 5 all bottom at `99`. **Corrected-vNext ends long `0.995000` open from bar 2, with realised `−5.00`.**

#### Why round 4 did not catch it, stated exactly

Round 4's finding was that an arm may not defer its oracle. GF-32's corrected arm did **not** defer — it asserted. An asserted oracle is falsifiable, which is the whole point of §2.8, but being falsifiable is not being true: this one was derived from a mis-stated predicate rather than from an unreachable configuration, so the reachability checks round 4 ran against the five legacy arms could not see it. **The evidence was already in this report.** §4.4's round-4 arithmetic bullet derives `995 × 0.005 / 5.00 = 0.995000` and calls it "the corrected re-entry" — the number was correct and was attached only to GF-33, while GF-32's corrected arm, sharing that fixture's bars and equity, was recorded as taking no re-entry at all. The flat oracle is what kept those two facts from being compared.

#### The discriminator claim was false in both halves

Round-4 field 8 read "five REDs at four different bars, two different prices and two different quantities, **against a corrected run that takes no re-entry at all**". Once the corrected run re-enters at bar 2, that aggregate is wrong twice over: the corrected run does re-enter, and `local` re-enters on the **same bar at the same price**, so there are not five distinct RED event timings. Field 8 now states the axis per run: `local` differs on **quantity alone** (`0.994000` against `0.995000`, the residue of a close-only `94.00` fill against a standing-touch `95.00`); `carry` on **bar and quantity** (bar 3, `0.994000`); `next_bar_open` on **bar, price and quantity** (bar 3, `99.00`, `1.004040`); `next_bar_close` on **bar and quantity** (bar 4, `0.994000`); `delay` on **bar and quantity** (bar 5, `0.994000`). Counted across the five, the bar axis yields three distinct later bars, the price axis one departure, and the quantity axis all five. **`local` is now the sharpest RED in the fixture and the one no event-level comparison can see** — it is the same fill-semantics residue GF-33 RED (iii) isolates, arriving one bar earlier.

#### GF-33 swept, and deliberately unchanged

GF-33's cross-references were re-read against this repair. Its corrected arm enters at **bar 5** under an explicit `post_exit_cooldown_bars: 2`, which blocks its bars 2 and 3; GF-32's corrected run declares no such key. The two arms therefore share bars, realised PnL and size and differ only in entry bar, for a declared configuration reason. **No cited predicate contradicts GF-33's bar-5 entry, so nothing in GF-33 was changed** — the fixture stands as a separate arm. GF-32 field 7 now states the difference explicitly so the two corrected end states cannot be read as a contradiction. GF-33 field 6's "D2 and the corrected run land on the same bar and the same price and differ only in quantity" remains true as written.

#### What round 5 changed

| Location | Change |
|---|---|
| `CAPABILITY_CANONICALIZATION_TABLE.md` GF-32 field 5 | The "no entry on bars 1, 2, 3, 4 or 5" oracle is replaced by bar 2 `ENTER_LONG` at close `100.00` and bar 5 `BLOCK(reason=MAX_ENTRIES)`, each with the predicate that produces it, and the withdrawn reading of C21/C05 is named rather than silently swapped |
| `CAPABILITY_CANONICALIZATION_TABLE.md` GF-32 field 6 | Two fills become **three**; the bar-2 re-entry `0.995000 @ 100.00` is asserted with its derivation and its non-binding leverage cap |
| `CAPABILITY_CANONICALIZATION_TABLE.md` GF-32 field 7 | End state changes from **flat** to **long `0.995000` from bar 2**, with the GF-33 contrast stated so the two corrected arms are not read as inconsistent |
| `CAPABILITY_CANONICALIZATION_TABLE.md` GF-32 field 8 | The aggregate "five REDs at four different bars … against a corrected run that takes no re-entry at all" is withdrawn and replaced by the per-run axes above |
| `LANE_REPORT.md` | This §2.9; the status header; the §2.8 GF-32 row marked superseded on the corrected arm; §4.4's GF-32/GF-33 sizing bullet attributed to both corrected arms; §4.3's round-4 continuation count restated; two §4.10 rows added |

Nothing else was touched. The five legacy arms, their bars, their predicates and their quantities are exactly as round 4 derived them; GF-33, GF-20, GF-34, GF-36, GF-37, GF-10, GF-40 and GF-41 are unchanged; `COVERAGE_SWEEP.md` was not written in this round. No source, Pine, contract, schema or corpus file was written, and no Git write of any kind was performed.

## 3. Decisions preserved unchanged

Repair round 1 changed only what the five findings required. These round-0 decisions were re-checked against their sources and **kept**: C01, C02 (semantics unchanged; its evidence base widened and its scope narrowed so C40/C41 own the HTF and equation axes), C03's canonical rule, C04's canonical rule, C05, C06's two-concept vocabulary, C08, C09, C11, C12, C13, C14, C15, C16, C17, C18's ownership split, C20, C21, C22, C23, C24, C25 (ticket #45, incorporated not re-decided), C26, C28-C30's retirements, C31-C37's retirements. No capability was invented that is not present in a cited source, and no decision was made on migration convenience.

## 4. Gate 4 self-QA — exact commands and outputs

### 4.1 Diff confinement

Round-4 capture, taken after every edit in this round:

```
$ git status --porcelain
 M MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md
 M MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/COVERAGE_SWEEP.md
 M MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/LANE_REPORT.md

$ git diff --cached --name-only
(no output — nothing staged)
```

**Exactly three paths, all inside the authorized output directory, all Markdown.** No source, Pine, contract, schema, corpus, memory or protected file appears. Nothing was staged, committed or pushed in any round. Round 4 wrote two of the three files — `CAPABILITY_CANONICALIZATION_TABLE.md` and `LANE_REPORT.md`; `COVERAGE_SWEEP.md` carries its round-3 content unchanged and appears in the status only because the whole three-file diff is still uncommitted. Source files under `MTC_COMMAND_CENTER/01_MTC_PROJECT/` and `MTC_COMMAND_CENTER/02_MTC_BACKTEST/` were **read** in round 4 to derive the fixture arithmetic, and none was written; the status output above is the evidence. **Round 5 re-ran the same capture after its edits and got byte-identical output.** It wrote the same two files — `CAPABILITY_CANONICALIZATION_TABLE.md`, in GF-32 fields 5 through 8 only, and `LANE_REPORT.md`. `COVERAGE_SWEEP.md` was not opened for writing in round 5 and still carries its round-3 content. Round 5 executed only `git status --porcelain`, `git diff --check` and read-only ripgrep; **no source, Pine, contract, schema or corpus file was read or written in it**, because the finding it answers turns on predicates already cited in the table (C21, C05, C11) and on arithmetic already recorded in §4.4.

### 4.2 Whitespace

```
$ git diff --check
warning: in the working copy of '…/CAPABILITY_CANONICALIZATION_TABLE.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of '…/COVERAGE_SWEEP.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of '…/LANE_REPORT.md', LF will be replaced by CRLF the next time Git touches it
```

Clean, and re-run after every round-4 edit — and again after every round-5 edit — with the same three-line result. The three lines are the repository's CRLF-normalisation notices, not check findings: `git diff --check` reports trailing whitespace, space-before-tab and blank-line-at-EOF findings, and it emitted none. An earlier round reported `new blank line at EOF` in two files; both were fixed and the check re-run.

### 4.3 Citation validation — three axes

**What is true about tooling, stated plainly, because round 2's version of this paragraph was not.**

**No validator written by this lane has ever been executed.** This session's tool-permission layer refuses every form of script execution attempted: `python` and `py -3` with a script argument, `awk -f <file>`, and invoking a `.ps1` by path or with `&`. Inline PowerShell is additionally capped at roughly 1 KB per command, which is below what a three-axis validator needs. Round 2 nonetheless described a `validate_citations.py` in this session's scratchpad, gave its invocation, and told the Lead to run it. **That was wrong on two counts:** the scratchpad is session-local and the Lead cannot reach it, and the Lead did not need it — **the Lead had already written and run its own inline validator against the round-1 diff, and it was that validator, not this lane's, that found the 143 + 2 orphan continuations and the 4 suspicious tokens recorded in §2.6, and the line-33 binding error recorded in §2.7.** Every citation finding this lane has repaired was found by the Lead. The claim of an available lane validator is withdrawn; nothing in the scratchpad is part of this deliverable.

The Lead's validator implements the three axes this section reports against: **PATH** (the cited file exists), **RANGE** (every line and range is inside `[1, file_line_count]`, resolved through the continuation's binding), and **SHAPE** (the path is repo-root-relative, and every `` `:N-M` `` continuation has a full path earlier on its own line, per the declared convention). **The Lead will rerun it against this round-3 diff, and that rerun — not anything below — is the acceptance evidence.** What this lane could execute is `git`, `ripgrep` and `wc`, and the three axes were re-checked with those, as follows. Each result below is a human-checked reproduction of the Lead's rule, not a machine assertion.

**Axis 1 — PATH, exhaustive.** Every distinct cited path was enumerated and then resolved with `wc -l`:

```
$ grep -ohE '`(MTC_COMMAND_CENTER|IBKR_PAPER_BRIDGE|docs)/[A-Za-z0-9_./-]+\.(py|pine|md|json|csv)' \
    MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/*.md | tr -d '`' | sort -u
```

That yields **41 distinct source paths plus the three lane documents**. All 41 were passed to `wc -l` in two batches; **all 41 resolved**, with these bounds:

| File | Lines | | File | Lines |
|---|---:|---|---|---:|
| `…/mtc_v2/core/config.py` | 698 | | `…/src/engine/mtc_runner.py` | 2789 |
| `…/mtc_v2/core/confirmation.py` | 152 | | `…/src/engine/mtc_state.py` | 516 |
| `…/mtc_v2/core/exits.py` | 587 | | `…/src/modules/confirmation_layer.py` | 420 |
| `…/mtc_v2/core/gates.py` | 605 | | `…/src/modules/filters/htf_trend_filter.py` | 111 |
| `…/mtc_v2/core/htf.py` | 197 | | `…/src/modules/filters/macd_hub_filter.py` | 188 |
| `…/mtc_v2/core/instrument.py` | 40 | | `…/src/modules/risk/position_sizer.py` | 178 |
| `…/mtc_v2/core/ma.py` | 417 | | `…/src/modules/risk/sl_calculator.py` | 170 |
| `…/mtc_v2/core/position_manager.py` | 355 | | `…/src/modules/risk/tp_calculator.py` | 320 |
| `…/mtc_v2/core/position_sizer.py` | 70 | | `…/tests/test_fill_contract_baseline.py` | 40 |
| `…/mtc_v2/core/rounding.py` | 40 | | `…/MASTER_ARCHITECTURE…BRIEF_2026-08-21.md` | 3611 |
| `…/mtc_v2/core/runner.py` | 1698 | | `…/MASTER_WORK_PACKAGE…PLAN_2026-08-22.md` | 1106 |
| `…/mtc_v2/core/types.py` | 170 | | `…/WAYFINDER_DECISION_FOLD_2026-08-23.md` | 61 |
| `…/01_PINE/MTC_V2.pine` | 2079 | | `…/WP_P0_04_CONTRACTS…/LANE_REPORT.md` | 624 |
| `…/parity_suite_350/PARITY_STATUS_FINAL_20260304.md` | 215 | | `…/WP_P0_06_PARITY_CORPUS…/PARITY_CORPUS_INVENTORY.md` | 120 |
| `…/cases/parity_bnd_211_swing_right_bars_v03.json` | 145 | | `…/12_PARITY_PINETS/parity_summary.md` | 484 |
| `…/cases/parity_bnd_217_dynamic_update_mode_v02.json` | 152 | | `…/contracts/README.md` | 83 |
| `…/src/config/defaults.py` | 469 | | `…/contracts/mtc_contracts/execution.py` | 188 |
| `…/src/engine/__init__.py` | 17 | | `…/contracts/mtc_contracts/orders.py` | 128 |
| `…/src/engine/fee_model.py` | 347 | | `…/contracts/mtc_contracts/risk.py` | 112 |
| `…/src/engine/fills.py` | 556 | | `…/contracts/mtc_contracts/sizing.py` | 126 |
| `…/src/engine/indicators.py` | 457 | | | |

The one path in the documents that does **not** resolve is `_AI_MEMORY/MASTER_ARCHITECTURE_DECISIONS_AND_TARGET_STATE_2026-08-19.md`, which appears only inside sentences stating that it does not exist. It carries no line numbers and is not a citation.

**Axis 2 — RANGE.** Citation volume, as counted in round 1 with the coarse patterns below. **These two figures are superseded:** the Lead's parser counted `FULL=497` and `CONT=471` on the same round-1 files, and the round-2 orphan repair then inserted an explicit full path on 113 further lines. They are left here because the range reasoning that follows was performed against them.

```
$ grep -ohE '`(MTC_COMMAND_CENTER|…)/…:[0-9][0-9,-]*`' …/*.md | tr -d '`' | sort -u | wc -l
309                       # distinct full path:line citations
$ grep -ohE '`:[0-9][0-9,-]*`' …/*.md | sort | uniq -c | wc -l
333                       # distinct same-line continuations
```

Ranges were verified against the bounds table above by extracting every citation **in document order** — which preserves continuation binding — with:

```
$ sed -n '<line-list>p' <document> | grep -oE '[A-Za-z_0-9./-]*\.(py|md|json|pine):[0-9][0-9,-]*|:[0-9][0-9,-]*'
```

The lines that anchor a **small** file (where an out-of-bounds range is actually possible) were enumerated first with the Grep tool and then extracted with the command above; the anchoring lines are `CAPABILITY_CANONICALIZATION_TABLE.md` 135, 148, 226, 231-234, 246, 249, 252-253, 257, 271, 275, 293, 458, 525, 560, 564, 574, 578, 592, 596, 616, 622, 632, 660, 696, 708, 710, 826, 840, 866-868, 880, 888 and `COVERAGE_SWEEP.md` 74, 118, 127, 152, 164, 175, 192, 233, 309, 312, 328. Every continuation on those lines resolved to the immediately preceding full path and fell inside its bound. The maximum cited line per file, checked against the bounds table, is: `runner.py` 1575 of 1698; `mtc_runner.py` 2690 of 2789; `MTC_V2.pine` 2028 of 2079; `config.py` (A) 624 of 698; `gates.py` 598 of 605; `exits.py` 561 of 587; `defaults.py` 451 of 469; `ma.py` 406 of 417; `htf.py` 179 of 197; `confirmation.py` 152 of 152; `position_sizer.py` (A) 70 of 70; `rounding.py` 40 of 40; `sizing.py` 121 of 126; `contracts/README.md` 38 of 83; `htf_trend_filter.py` 96 of 111; `engine/__init__.py` 17 of 17; `test_fill_contract_baseline.py` 6 of 40; `WAYFINDER_DECISION_FOLD` 22 of 61; `PARITY_CORPUS_INVENTORY.md` 120 of 120; `parity_summary.md` 484 of 484; `MASTER_ARCHITECTURE…BRIEF` 2332 of 3611; `MASTER_WORK_PACKAGE…PLAN` 543 of 1106. **No citation exceeds its file's bound, and no range is inverted.**

**This axis is where round 2 failed, and the failure was specifically in the *binding* step, not the bounds step.** Round 2's procedure asked only whether each continuation had an anchor; it did not resolve each continuation to its anchor and range-check it against that anchor's own line count. The bare continuation with lines 100 to 121 appended, in this report's §2.1 contract sentence, had an anchor — `MTC_COMMAND_CENTER/contracts/README.md`, 83 lines — and was out of range against it, and round 2 reported the axis clean. §2.7 finding 1 records it.

**Round-3 re-check, run over all three documents.** Every citation token in the three files was emitted through **one alternating ripgrep pattern** with `--line-number --only-matching`, so full paths and continuations print interleaved in document order, grouped by source line. That yields **432 citation-carrying lines** across the three round-3 documents — 217 in `CAPABILITY_CANONICALIZATION_TABLE.md`, 168 in `COVERAGE_SWEEP.md` and 47 here. Each line was then walked left to right: each full path becomes the current anchor, each continuation is resolved to the current anchor, and each resolved range is checked against that anchor's `wc -l`. Result across the three round-3 documents: **every continuation has a full path earlier on its own line, and every resolved range falls inside its anchor's bounds.** The two known-hazard lines were re-checked by hand, both in this report, and both are described here in prose rather than reproduced. §2.1's contract sentence now carries three separate anchors — the sizing contract module (126 lines), the contracts README (83) and the architecture brief (3611) — with its only two continuations binding, in order, to the sizing module and then to the brief, each in range. §4.8's contract-conformance sentence carries the sizing module as its first anchor and binds both of its continuations to it, which is correct and was already so in round 2. **This is still a human-checked reproduction, and the Lead's rerun is the acceptance evidence.**

**Round-4 re-check, and the line counts that supersede the round-3 figures.** Round 4 rewrote seven fixture specifications and added a section to this report, so the round-3 count of 432 citation-carrying lines no longer describes these files and is superseded. The check was re-run over all three documents in the same way — enumerate every continuation token with `--line-number --only-matching`, then walk each carrying line left to right resolving each continuation to the nearest preceding full path on that line and range-checking it against that anchor's `wc -l`. Measured after the round-4 edits, `CAPABILITY_CANONICALIZATION_TABLE.md` carries continuations on **130** lines and `LANE_REPORT.md` on **23** (44 tokens); `COVERAGE_SWEEP.md` is unchanged from round 3. **The first pass found two real orphans, both introduced by this round**, in GF-33's field 5: the `D2` and `C2` bullets each opened with a bare line range whose anchor sat on the bullet above, which is the cross-row inference §1.1 forbids and the same class round 2 repaired at scale. Both were expanded to their full repo-root-relative path and the walk re-run; the second pass returns **no orphan and no out-of-range binding in any of the three documents**. Round 4 introduced **no new cited file** — every path it uses was already in the §4.3 bounds table — and it raised the maximum cited line in only one of them: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py`, from `561` to `571` of `587`. Its other new ranges sit well inside their anchors: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py` at most `62` of `70`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py` at most `1505` of `1698`, `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py` at most `624` of `698`, and `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine` at most `2020` of `2079`. **This remains a human-checked reproduction of the Lead's rule, not an execution of the Lead's parser; the Lead's rerun against this diff is the acceptance evidence.**

**Round-5 re-check, and the counts that supersede the round-4 figures.** Round 5 rewrote four fields of one fixture and added §2.9 to this report. Re-measured after those edits, `CAPABILITY_CANONICALIZATION_TABLE.md` still carries continuations on **130** lines — round 5 added no new continuation-carrying line to it, because its four edited fields are four existing lines — and `LANE_REPORT.md` now carries them on **24** lines (**45** tokens), up from 23 and 44: the one new line is §2.9's C21 bullet, whose single continuation resolves to `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py` (355 lines) and is in range. `COVERAGE_SWEEP.md` is unchanged from round 3 at **47** lines. The four edited table lines were walked left to right: GF-32 field 5's first token is a full path and its two continuations bind, in order, to `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py` (587) and `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_manager.py` (355); field 6 carries three full paths and no continuation; field 7 carries no citation; field 8's first token is a full path and all five of its continuations bind to `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py` (1698), the highest being `1393-1409`. **No orphan and no out-of-range binding was introduced, and round 5 cited no file that was not already in the §4.3 bounds table and raised no file's maximum cited line.** As in every prior round, this is a human-checked reproduction of the Lead's rule, not an execution of the Lead's parser.

**Axis 3 — SHAPE. This axis FAILED in round 1 and the round-1 text below is retained only so the failure is visible.** Round 1 claimed that "the enumeration above confirms every sampled continuation has a full path earlier on its line". The word doing the work was *sampled*: the enumeration covered the continuations that anchor small files, not all of them, and the claim was generalised beyond what was checked. The Lead's parser found 145 orphan continuations and 4 citation-shaped tokens outside the convention. **§2.6 records the finding, the repair and the re-check.** What remains true from round 1 and was re-confirmed after the repair: every full citation begins with `MTC_COMMAND_CENTER/`; the only abbreviation is the same-line continuation declared in `CAPABILITY_CANONICALIZATION_TABLE.md` §1.1 and repeated in `COVERAGE_SWEEP.md`; and bare module names appear only in `COVERAGE_SWEEP.md` §1.1's inventory table, where the directory is the adjacent column and a note says they are inventory entries carrying no line numbers, not citations.

### 4.4 Content fidelity — manually validated, claim by claim

Range validity is not content fidelity, so every repaired or high-risk claim was validated by reading the cited lines. The ones that changed a decision or a description are tabulated in §2.5; the ones that were validated and **confirmed correct** include: A's hard-coded stop-first collision (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/exits.py:362-379`); Pine's multiplier in the risk denominator (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:339-348`); A's omission of it (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:43-47`); B's tie-to-high-first heuristic (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:612-619`); A's `last_realized_pnl` time-exit input (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:677-685`); A's hard-coded Friday-21:00 EOW (`:692-695`); A's close-counting day counter (`:746-747`); B's entry-counting day counter (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py:373-376`); B's `5×`/200/2000 warm-up clamp (`:511-513`); B's `1.104`/`0.97` maintenance constants (`:36`, `:644-649`); B's swing window including the decision bar (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/risk/sl_calculator.py:135-142`) against A's append-at-end-of-bar history (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1043`); the `[OPEN]` status of the freshness numbers (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2332`); and the two `alert()` emissions the WP-P0-23 scope names (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:2020`, `:2028`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:543`).

Every arithmetic result asserted in a fixture was re-derived by hand from the cited source formula and the fixture's own literal inputs — for example GF-08's `100 / (5 × 10) = 2`, GF-09's `floor(99.87 / 0.25) × 0.25 = 99.75` and `ROUND_HALF_UP(101.125 / 0.25) × 0.25 = 101.25`, GF-06's `(1 × 100 + 2 × 110) / 3 = 106.6666667`, GF-22's `18.00 − 0.201 − 0.219 − 0.0201 = 17.5599`, GF-31's `floor(1.234567 × 10⁶) / 10⁶ = 1.234567`, and GF-15's `106 − 1.5 × 2.0 = 103.00`.

**Round-3 arithmetic, recomputed from scratch rather than carried over.**

- **GF-10.B.** Bar 1: `9.12·x >= 22` → `x = 22/9.12 = 2.412280701754…` → adverse-ceil `2.42`; fee `2.42 × 96 × 0.005 = 1.1616`; equity `170.00 − 1.1616 = 168.8384`; quantity `20 − 2.42 = 17.58`; maintenance `0.10 × 17.58 × 96 = 168.768`; `168.8384 >= 168.768` holds and the `2.41` alternative fails at `168.8432 < 168.864`. Bar 2: `8.74·x >= 53.5376` → `x = 6.125583…` → `6.13`; fee `2.8198`; equity `105.3786`; quantity `11.45`; maintenance `105.34`. Bar 3: equity `108.6186 >= 100.76`, no liquidation.
- **GF-41 F1.** Decided/A/custom-Pine EMA(3), SMA-seeded, over `10, 20, 30, 40, 50`: `None, None, 20.0, 30.0, 40.0`. B's `ewm(span=3, adjust=False)`, `alpha = 0.5`: `10.0, 15.0, 22.5, 31.25, 40.625`. **Round 2 asserted `27.5` for B's bar 3; the correct value is `22.5`, and it is corrected.**
- **GF-41 F2.** Decided `htf_ma = (100 + 108)/2 = 104.00` on bars `08:00`–`11:00`; long threshold `104.00 × 1.01 = 105.04`, short threshold `104.00 × 0.99 = 102.96`. A and the built-in Pine HTF path: `100.00` on `05:00`–`07:00`, `104.00` on `08:00`, `108.00` on `09:00`–`11:00`.
- **GF-41 F2b.** `104.50` against decided `(105.04, 102.96)` → both block; against A's and Pine's loose form `(102.96, 105.04)` → both pass; against B's `htf_ma = (108 + 104.50)/2 = 106.25`, buffer `1.0625` → `(false, true)`.
- **GF-41 F3.** Decided: `slow = None, 100.0, 108.0, 118.0, 124.0`; `macd_line = None, 0.0, 4.0, 5.0, 3.0`; `signal = None, None, None, 3.0, 3.0`; `hist = None, None, None, 2.0, 0.0`. B: `hist = 0.0, 0.0, 2.0, 1.5, −0.25`.
- **GF-40 R3.** A's inferred period is `08:00 − 00:00 = 8 h` against the declared `4 h`, so its shifted labels are `08:00, 16:00, 20:00` and bars `12:00`–`15:00` read `100` where the decided rule reads `108`.

**Round-4 arithmetic, derived from the cited source lines over each fixture's own literal inputs.** Every number below is new to this round, and each is the value an arm previously deferred.

- **GF-32 / GF-33 sizing.** Entry: `1000 × (0.5 / 100) = 5.00` of risk over `|100.00 − 95.00| = 5.00` gives `1.000000`, under a leverage cap of `(1000 × 1.0) / 100 = 10.0` that does not bind (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:43-55`). Legacy stop at the close `94.00` realises `−6.00`, leaving a snapshot of `994.00` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1504-1505`); re-entry at a close of `100.00` is `994 × 0.005 / 5.00 = 0.994000`, and at the open `99.00` against a stop of `94.05` it is `994 × 0.005 / 4.95 = 1.004040` after the six-decimal floor. The corrected standing-touch stop at `95.00` realises `−5.00`, leaving `995.00`, so the corrected re-entry is `995 × 0.005 / 5.00 = 0.995000`. The `0.994000` versus `0.995000` pair is the entire economic residue of the fill-semantics difference, carried into the next position's size. **Round-5 attribution, because round 4 got this half right and filed it in one place only.** Round 4 derived `0.995000` and attached it solely to GF-33's bar-5 corrected arm, while GF-32's corrected arm — same bars, same equity, same stop — was recorded as taking no re-entry at all. Both corrected arms size `0.995000` off the same `995.00` snapshot; they differ only in **when**, because GF-33 declares `post_exit_cooldown_bars: 2` and GF-32 declares no post-exit cooldown, so the residue surfaces at **bar 2** in GF-32 against `local` (same bar, same price, quantity only) and at **bar 5** in GF-33 against `D2`. §2.9 records the finding.
- **GF-32 enum windows.** With `tw_reversal_reentry_delay_bars: 2` and `n = bar_index − 1`: `carry` defers on `n < 2`, `delay` on `n <= 2`, and both queue predicates are `0 < n <= 2` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1306-1308`, `:1320`, `:1332`). The `next_bar_close` arm re-queues at bar 3 because `n = 2` still satisfies its predicate, which is why it lands one bar later than `carry` rather than beside it.
- **GF-34 threshold.** At quantity `40`, capital `1000` and `margin_frac 0.20`: required `= 8m`, equity `= 40m − 3000`, deficit `= 3000 − 32m`, positive exactly below `m = 93.75`. Checkpoints in probe order are `98`, `94`, `94`, `88`; the first three are above the threshold with deficits `−136.00`, `−8.00`, `−8.00`, and `88` gives `+184.00`. Liquidation quantity `= (184.00 × 4.0) / (88.00 × 0.20) = 736 / 17.6 = 41.818181…`, clamped to `40`, over a reference quantity of `40`, giving `exit_pct = 1.0`: a full close realising `−480.00` and leaving `520.00` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1449-1472`). Under the decided venue rule the same bars give equity against maintenance of `800.00 / 380.00`, `560.00 / 356.00`, `400.00 / 340.00` — solvent throughout. The old configuration's threshold, for the record, was `1000 − 16m > 0`, i.e. `m < 62.50`, against a sequence whose lowest price was `84`.
- **GF-34 entry quantity.** No stop, so the fallback path: `1000 × (400.0 / 100) / 100 = 40`, capped at `(1000 × 5.0) / 100 = 50`, giving `40`; admissible because `100 × 40 × 0.20 = 800 < 1000 × 5.0` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/position_sizer.py:48-55`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py:1490-1502`).
- **GF-36.** Entry `100.00`, initial stop `95.00`, `initial_R = 5.00`, BE trigger `105.00`, BE stop `100.00` at `be_buffer_r 0.0`. Probes over the four bars: highs `106, 104, 106, 101`; closes `104, 103, 105, 100`; previous-bar highs `100, 106, 104, 106`. First arming bar per mode is therefore 1 (`local`), 3 (`tradingview`), 2 (`next_bar_confirmed`) and, for the decided next-bar rule, an arm at bar 3 effective at bar 4. Fills: `100.00`, `100.00`, `100.00` at the stop price, and `99.00` at bar 4's open, which is already below the stop.
- **GF-37.** Entry `100.00`, `initial_R = 5.00`, activation at `105.00`, distance `1.5 × 2.0 = 3.00`. `local` anchors bar 1's high `107` → stop `104.00`, written before bar 1's own price test, and bar 1's open `101` is below it → fill `101.00`, **not** the `104.00` round 3 asserted. `tradingview` anchors bar 2's close `106` → stop `103.00`, touched by bar 2's low `103` → fill `103.00`. `next_bar_confirmed` anchors bar 1's high `107` on bar 2 → stop `104.00`, and bar 2 opens exactly at `104` → fill `104.00`. The decided rule anchors bar 2's close `106` effective on bar 3 → stop `103.00`, touched by bar 3's low `102` → fill `103.00`.
- **GF-20 R4 / R8.** LONG target `105.00` against a test bar `109,110,108,110`: the open `109` is already beyond the target, so the canonical favourable-gap fill is `109.00` and the close-only rival is `110.00`. SHORT target `95.00` against `91,92,90,90`: canonical `91.00`, close-only `90.00`. Neither row's stop is reached (`108 > 95.00`; `92 < 105.00`).
- **GF-29.** With the declared input defaults the three optional payload segments are empty and the fixed segments concatenate to `{"code":"ENTER_L_TEST","order_type":"market","amount":100,"amount_type":"quote","leverage":1,"reduce_only":true}` (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:2017-2020`). This is string construction, not simulation; no execution is involved in deriving it.

### 4.5 Mapping completeness

```
$ grep -nE '^\| `case_[0-9]{3}`' …/COVERAGE_SWEEP.md
```

returns 31 rows: `case_110, 111, 134, 147, 153, 154, 155, 162` (the 8 unresolved A failures, §10.2) and `case_103, 104, 105, 106, 109, 112, 113, 114, 115, 126, 127, 128, 129, 130, 132, 133, 137, 138, 139, 140, 141, 142, 143` (the 23 soft-pass cases, §10.4). **Each of the 31 appears exactly once**, which matches the corpus's own count of 31 TradingView-versus-Python strict failures (`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_06_PARITY_CORPUS_2026-08-24/PARITY_CORPUS_INVENTORY.md:46`). Every row carries a `parity_summary.md` block citation, a capability cited to its implementing line, and a named discriminating fixture. Corpus B's cases 402 and 416 are mapped separately in §10.3.

### 4.6 Omitted-module coverage

```
$ grep -nE '^### 4\.[1-5]' …/COVERAGE_SWEEP.md
```

returns the five required sweeps: A `confirmation.py`, A `gates.py`, A `htf.py`, B `engine/fee_model.py`, B `engine/fills.py`. Each is a table in which **every** finding carries an "Economically meaningful?" column and a disposition; the economically meaningful ones are dispositioned to C02, C04, C08, C16, C18, C22, C25, C38, C40 or C41, and the non-meaningful ones to §7's non-economic dispositions or to the legacy non-authority statement.

### 4.7 Fixture literalness and GF-20

```
$ grep -c '^- \*\*GF-[0-9]\{2\}\*\*'  …/CAPABILITY_CANONICALIZATION_TABLE.md   → 41
$ grep -c '^### C[0-9]\{2\} —'        …/CAPABILITY_CANONICALIZATION_TABLE.md   → 41
```

41 capability rows and 41 fixture specifications, one to one. Every specification has all eight fields. **GF-20 defines rows R1–R9 in its own table** with side, stop, target, a literal `O,H,L,C` test bar and the exact expected fill for each, so it references only rows that exist; after round 4 it also states each gap row's rival close-only fill as a number and carries **no instruction to re-run or re-select any row**. GF-28, GF-29 and GF-30 use the explicitly typed `static-validation` form for their retirement blocks and enumerate the exact key set and the exact expected result, with GF-29's Pine payload asserted byte for byte.

**Round-4 re-check of the fixture-type axis.** The table now declares exactly two fixture types (`CAPABILITY_CANONICALIZATION_TABLE.md` §1.4) and the third, record-it-later type appears nowhere in it as a live label. Round 3's claim in this section — that GF-32's five legacy arms and GF-34's L2, GF-36's L3 and GF-37's L3 "name the exact tuple to be recorded, so no undisclosed A snapshot is claimed" — is **withdrawn**: naming a tuple to be filled in later is not a specification, four of those six arms could not have reached the branch they claimed to observe, and one of the two arms round 3 did assert was numerically wrong. All six are now derived and asserted, and §2.8 records what deriving them found. Every one of the 41 fixtures now states its own oracle.

### 4.8 C07 versus the contract

```
$ grep -n 'PCT_EQUITY_NOTIONAL' …/*.md
```

returns matches only inside withdrawal or rejection sentences — the round-0 statement being withdrawn, the "must not appear in any artifact" rule, and GF-07.E's rejection assertion. The four-value enum in C07 is `RISK_AT_STOP`, `FIXED_QTY`, `FIXED_NOTIONAL`, `VOLATILITY_TARGET`, character-for-character the members of `SizingMethod` (`MTC_COMMAND_CENTER/contracts/mtc_contracts/sizing.py:17-21`). The two-message boundary is stated as `SizingRequest` → `BoundSizingIntent` with the orchestrator adding the snapshot binding and altering no request field, matching the class definitions (`:39-97`, `:100-121`) and §5.4/§5.5 (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1082-1089`, `:1143-1150`).

### 4.9 Boundary compliance

| Boundary | Result | Evidence |
|---|---|---|
| Analysis only; no source/Python/Pine/parity/MTC_V2/Bridge/schema/contract/corpus/memory change | PASS | §4.1 diff is three Markdown files |
| Exactly the three whitelisted paths written | PASS | §4.1 |
| No backtest executed | PASS | No project code was run, and no script of any kind was executed — the permission layer refuses `python`, `awk -f` and `.ps1` invocation alike. Only `git`, `ripgrep` and `wc` ran, all read-only |
| No network, no other worktree, no sub-delegation, no other AI CLI | PASS | None used; no Agent, no Task, no Codex invocation |
| No commit, stage, push, merge, rebase, checkout, reset, restore, stash or clean | PASS | Only `git status`, `git diff`, `git diff --check`, `git log --all --diff-filter=A` (read-only) were run |
| Every claim carries a resolving `file:line` citation and a reason | PASS | §4.3, §4.4 |
| No decision made on migration ease | PASS | No fixture or decision mentions migration convenience; C38 chooses **B** over A precisely because B holds the real implementation |
| Ticket #45 rows incorporated, not re-decided | PASS | C25 restates the decided policy unchanged. C27 restates the decided **policy** unchanged and, as the same specification line separately requires, decides the exact bound values. Deciding those numbers is this row's assigned work, not a re-opening of the policy |

### 4.10 Self-QA table

| Check | Result | Note |
|---|---|---|
| Correct worktree, branch and evidence base | PASS | `C:\WPP009_20260825`, `feature/wp-p0-09-capability-table-20260825`, `ac873ae7` |
| All five audit findings addressed completely | PASS | §2.1–§2.5 |
| Both Lead findings from the round-1 diff inspection addressed completely | PASS | §2.6 |
| All five Lead findings from the round-2 diff inspection addressed completely | PASS | §2.7 |
| The round-4 deferred-oracle finding addressed completely | PASS | §2.8 — all six deferred arms derived and asserted; the third fixture type removed from the table |
| The round-5 GF-32 corrected-oracle finding addressed completely | PASS | §2.9 — the corrected arm re-enters at bar 2 for `0.995000 @ 100.00` and ends long, and field 8's aggregate RED claim is replaced by per-run axes |
| Every fixture states its own oracle; no arm defers its expected output | **Rounds 1–3: FAIL** — six arms deferred, and the deferral concealed four unreachable configurations and one wrong asserted value. **Round 4: repaired**, with the arithmetic in §4.4 | §2.8; §4.7 |
| GF-32 legacy arms reach the branch they claim to observe | **Round 3: FAIL** — bar 1's close `96` could not trigger a close-only stop at `95.00`, so all five arms observed nothing. **Round 4: bar 1 close is `94`; five outcomes on four distinct bars** | §2.8 |
| GF-32's **corrected** arm asserts the oracle the decided rule actually produces | **Rounds 1–4: FAIL** — it asserted no entry on bars 1 through 5 and a flat end state, on a reading of C21 and C05 that neither rule supports, and round 4's deferred-oracle sweep covered only the legacy arms. **Round 5: repaired** — bar 2 `ENTER_LONG` `0.995000 @ 100.00`, bar 5 typed `MAX_ENTRIES`, ends long from bar 2 | §2.9; §4.4 |
| GF-32 field 8 states discriminator axes per run, not an aggregate timing claim | **Round 4: FAIL** — "five REDs at four different bars … against a corrected run that takes no re-entry at all"; `local` in fact shares the corrected run's bar **and** price. **Round 5: axis named per run; `local` differs on quantity alone, and it is the RED no event-level comparison can see** | §2.9 |
| GF-33 swept for contradiction, and changed only if a cited predicate proves it wrong | PASS | §2.9 — its corrected bar-5 entry follows from an explicit `post_exit_cooldown_bars: 2` that GF-32's corrected run does not declare; no predicate contradicts it, and no GF-33 field was edited |
| GF-34 L2 reaches the branch, and its config is one A can express | **Round 3: FAIL** — `FIXED_QTY` is not an A sizing method, and the declared bars could not produce a deficit above a mark of `62.50`. **Round 4: fallback-sized `40`, bars re-chosen against the `93.75` threshold, full close asserted** | §2.8; §4.4 |
| GF-36 / GF-37 name an execution profile A declares | **Round 3: FAIL** — both named a "touch profile" A does not have and disabled the one that **is** the touch path. **Round 4: `raw_close_only_v1`, cited to the predicate that makes it so** | §2.8 |
| GF-37 L1's asserted fill is the fill, not the stop price | **Round 3: FAIL** — asserted `104.00`, the revised stop, on a bar that opens at `101` below it. **Round 4: `101.00`, adverse-gap open, with the correction stated in the fixture** | §2.8; §4.4 |
| GF-20 references only rows that exist and contains no instruction to invent one | **Round 3: FAIL** — field 8 told the implementer to re-run R4 with a different bar. **Round 4: R4 and R8 bars replaced, all four rival fills stated as numbers, instruction deleted** | §2.8; §4.7 |
| GF-10.B self-contained: one `bucket_capital`, one liquidation bar, an exact liquidated quantity | **Round 2: FAIL** — three mutually contradictory statements and no quantity. **Round 3: repaired**, with the arithmetic recomputed in §4.4 | §2.7 finding 2 |
| Every GF-40 / GF-41 arm referenced by a corpus case mapping is literal | **Round 2: FAIL** — R2, R3, F1 and F3 were prose. **Round 3: every arm carries exact config, timestamps, OHLCV, expected per-bar values, typed events and exact rival outputs** | §2.7 finding 3 |
| C41 content-faithful about Pine; no unsupported `ta.ema` equivalence claim | **Round 2: FAIL** — conflated two Pine paths and rested the seed decision on the conflation. **Round 3: both paths stated separately from source; both decisions re-argued economically; the HTF departure from Pine is declared and costed** | §2.7 finding 4 |
| GF-41 discriminates A, B, custom-Pine-LTF and built-in-Pine-HTF | **Round 3: yes** — F1 (seed), F2 (sampling basis), F2b (buffer sign, four distinct verdicts), F3 (histogram readiness, three distinct verdicts), F4 (substitution, opposite direction) | §2.7 finding 4 |
| Truthful account of the citation validator | **Round 2: FAIL** — claimed an unreachable scratchpad script as a deliverable and told the Lead to run it. **Round 3: withdrawn**; the Lead's own validator is credited with every citation finding | §2.7 finding 5; §4.3 |
| The exact commit message required by the owner appears verbatim | PASS | §6 |
| Lead's corrections honoured (no speculative C38-C41) | PASS | §2.2; the four new rows are all named-or-swept behaviours |
| Work-package contract not broadened | PASS | §5 of the table lists the explicit non-decisions |
| Diff confinement and whitespace | PASS | §4.1, §4.2 |
| Citation PATH axis | PASS, mechanical | §4.3 |
| Citation RANGE axis, including each continuation's **binding** | **Round 2: FAIL** — one out-of-range bind in this report's §2.1 contract sentence, found by the Lead. **Round 3: repaired; all 432 citation-carrying lines re-walked with each continuation resolved to its anchor and range-checked** | §2.7 finding 1; §4.3 axis 2 |
| Citation SHAPE axis | **Round 1: FAIL** — 145 orphan continuations and 4 suspicious tokens, found by the Lead's validator, not by this lane. **Round 2: repaired and re-checked; round 3 re-confirmed** | §2.6 finding 1; §4.3 axis 3 |
| C27 decides the exact bound values the specification assigns to this row | **Round 1: FAIL** — deferred as `[OPEN]`. **Round 2: decided** | §2.6 finding 2 |
| Content fidelity of repaired and high-risk claims | PASS, manual | §4.4; nine false or imprecise claims found and corrected |
| 23 soft-pass + 8 failures, each exactly once, each with a discriminating fixture | PASS | §4.5 |
| Required omitted modules named and dispositioned | PASS | §4.6 |
| All named fixtures literal; GF-20 references only existing rows | PASS | §4.7 |
| C07 matches the contract enum and the two-message boundary | PASS | §4.8 |
| No exact A snapshot claimed without supplying it | PASS | Every legacy value in the table is now supplied and derived from the cited source arithmetic over the arm's own literal inputs; §4.4 shows the round-4 derivations |
| D026 readiness | PASS | Field 8 of every fixture names a RED with the rival behaviour's `file:line` |

## 5. Known limitations, stated rather than hidden

1. **No citation validator has been executed by this lane in any round, and none is available to the Lead from this lane.** Every form of script execution is refused by this session's tool-permission layer — `python` and `py -3` with a script argument, `awk -f <file>`, and running a `.ps1` by path or with `&` — and inline PowerShell is capped near 1 KB, below what a three-axis validator needs. This is not a cosmetic limitation; it is exactly where rounds 1 and 2 failed. Round 1 substituted a *sampled* manual check for the SHAPE axis and reported it as a pass; the Lead's own validator found 145 orphan continuations and 4 suspicious tokens behind that report. Round 2 replaced sampling with an enumerate-and-set-difference procedure that checked whether each continuation had an anchor but never resolved it to that anchor and range-checked it; the Lead's validator then found the §2.1 binding error behind *that* report. Round 3's procedure resolves and range-checks each binding (§4.3, axis 2), and it is still a human-checked reproduction of the Lead's rule. **Round 2 additionally claimed a `validate_citations.py` was left in the scratchpad for the Lead to run; that claim is withdrawn — the scratchpad is session-local and unreachable by the Lead, the Lead has its own validator, and it was the Lead's validator that found every citation defect repaired in rounds 2 and 3.** The Lead's rerun against this diff is the acceptance evidence for all three axes.
2. **~~Some fixtures do not assert their legacy outputs.~~ This limitation is withdrawn in round 4, and it was not a limitation — it was a defect.** Rounds 1–3 left GF-32's five arms, GF-34's L2, GF-36's L3, GF-37's L3 and GF-33's `delay = 2` arm with their oracles deferred to a future execution of the pinned code, and defended it as the honest alternative to inventing numbers. That was a false dichotomy: the third alternative, and the correct one, is to **derive** the numbers from the cited source arithmetic over inputs chosen so the branch is reachable — which requires no execution and is what round 4 did. The deferral also concealed real errors, because an arm whose expected value is defined as the code's own output cannot fail: four of the six could not reach the branch they claimed to observe, and one of the values round 3 *did* assert was wrong (§2.8). No fixture in the table defers its oracle now. **What remains true is narrower and is stated as its own limitation:** these derivations are hand-derivations from source, not executions, so WP-P0-10's first act on each repaired arm should be to run it and confirm the asserted values — and a mismatch is then a finding against this table, which is exactly the falsifiability the deferred form did not have. **Round 5 is the first time that limitation bit, and it bit on the corrected side rather than the legacy side.** GF-32's corrected arm was asserted, not deferred, and was still wrong — not in its arithmetic, which §4.4 had right, but in the predicate it applied: it read C21 and C05 as refusing a fresh raw signal two bars after a protective exit, and neither rule does (§2.9). **An asserted oracle is falsifiable; that is not the same as being true.** The consequence for WP-P0-10 is stated plainly here: re-derive each fixture's governing **predicate** from the decided row, not only its **numbers** from the cited arithmetic, because a misapplied predicate yields an internally consistent fixture that pins the wrong rule and whose RED claims then describe a discriminator the fixture does not have.
3. **The freshness bound values are decided in C27, not inherited and not deferred.** C27 closes them at `15 s` and `45 s` with both endpoints inclusive to `AGING`, because the delivery plan assigns the exact values to this row (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:377`). The architecture brief's `[OPEN]` marker sits in a carrier-assignment paragraph that names owners rather than values (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:2332`), and this row is the named owner. The residual exposure is stated plainly: if the owner wants different numbers, that is now a change to a **decided** row, and GF-27's third RED is what will catch it.
4. **C38 retires fifteen A configuration keys on the basis that they are inert.** The evidence is that every step function returns its input unchanged. GF-38 field 8 makes that a **proof obligation** for WP-P0-10 rather than an assumption: if the byte-identical comparison fails, the retirement is falsified and the investigation reopens. The same inverted-RED structure is used in GF-35.
5. **The WP-P0-06 corpus cannot validate any decision here.** Its generation-time Pine and Python identities are `UNKNOWN` and its Pine short-title differs from the tracked snapshot. It is used only as evidence that the implementations disagree.
6. **No parity percentage is asserted anywhere in these documents**, in line with the corpus inventory's own prohibition.

## 6. Staged-path contract

Only these exact paths are authorized for the lane commit, and only these three were written:

- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/COVERAGE_SWEEP.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/LANE_REPORT.md`

Commit message for the Lead, who owns Git — this exact string, verbatim:

```
fix(wp-p0-09): repair round 1 - contract-conformant sizing, missing capabilities, truthful mappings, literal fixtures
```

## 7. Open issues and downstream gates

There are no open WP-P0-09 semantic rows and no timebox remainder. The following are downstream by design, not omissions:

- WP-P0-10 implements GF-01 through GF-41 and supplies D026 RED/GREEN evidence for every fixture used to close a named defect, including the two inverted REDs (GF-35 and GF-38) whose failure reopens a retirement.
- The Lead runs the mandatory T0 two-flagship xhigh audit and independently verifies this diff, starting with the citation validator this session could not execute.
- Runtime, Pine, contract and configuration removal remain unauthorized here. WP-P0-23 already owns the `wt_*` and `alert()` removal scope; the `l18b_*` and `tw_*` retirements decided here need their own authorized package.
- Concrete venue margin and cost schedules, the named session/venue calendars C17, C18, C25 and C40 depend on, and the WP-P0-26 NTP/drift mechanism all require their own authoritative inputs. Every decision above defines fail-closed behaviour when they are absent.
- C27's bound values are decided and GF-27 asserts them, including a RED that mutates each boundary and each endpoint rule. What remains downstream is the WP-P0-26 NTP/drift mechanism that supplies the disciplined observation instant the age is measured against; the numbers themselves are no longer pending.
- **C41's HTF sampling basis is a declared, costed divergence from the Pine reference, and it needs an owner acknowledgement rather than silent implementation.** One sample per closed HTF bar is not what the tracked Pine does; the Pine advances its built-ins on every LTF bar over repeated values, deliberately (`MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:903-905`, `:920-921`), and A reproduces that. The consequence is stated in C41 and repeated here: after WP-P0-10 implements the decided rule, corpus cases 147, 155 and 162 will not reproduce the TradingView workbook, and no parity claim may be made on their numbers. The same applies, at smaller scale, to the three other Pine-faithful behaviours C41 rejects — the loose HTF buffer sign, the raw-close substitution when the MA tracker is unready, and the `0.0` previous-histogram substitution. GF-40 and GF-41 make each divergence a named, failing RED so none of them can be mistaken for a parity fix.

No push was performed. No Git write of any kind was performed.
