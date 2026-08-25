# WP-P0-10 Kernel Economic Golden Suite — Implementer Lane Report

**Date:** 2026-08-25

**Branch:** `feature/wp-p0-10-golden-suite-20260825`

**Redispatch starting HEAD:** `c8a873ea680dc3c643c10ab074e62a39a8cf2bac`

**Audit tier:** T0, as assigned by the package contract

**Implementer status:** 23 families built; families 18 and 19 remain formally blocked; independent Lead acceptance is pending

**Acceptance language:** none; this is implementation and self-QA evidence, not an audit verdict

## 1. Scope and fixture contract

The binding package contract is
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md:382-389`.
The fixed family catalogue is
`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1763-1804`.
The semantic authority is
`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/CAPABILITY_CANONICALIZATION_TABLE.md`.

The new data-only corpus is under `fixtures/`. It does not edit kernel, optimizer, Pine,
Bridge, schema, contract, or existing parity-corpus files. The existing 858-event Bridge /
QuantLens corpus is referenced by family 1 as a companion, labelled **ENTRY SIGNAL GOLDEN**, and
pinned by Git blob OID `31bdafae4d4d94787508043e9681874f9dc43bda`; it was not copied,
recaptured, or modified.

Each built fixture records:

1. literal configuration, frozen metadata, and normalized bars (or an empty bar list for static validation);
2. expected output as `{path, value, citations}` assertions;
3. at least one exact WP-P0-09 row citation adjacent to **every** expected assertion;
4. canonical output and final-state SHA-256 values under the normalization declared in `fixtures/README.md`; and
5. one exact single-field candidate-output mutation, its WP-P0-09 discriminator citation, and its restoration value.

`fixtures/verify_fixtures.py` contains no economic implementation. It checks the data contract,
requires every expected assertion and mutation to cite the WP-P0-09 table, verifies the stored
hashes, applies exactly one declared candidate-output mutation per family, requires exactly one
mismatch, restores the field, and requires byte identity. This is the fixture comparison seam
future kernel subjects must drive; no expected value was captured from A, B, Pine, or current
runtime behaviour.

## 2. All 25 families, build status, and oracle authority

The precise citation behind every expected value is stored beside that value in the named JSON
fixture. The table below gives the complete deciding-row set for each family; the verifier rejected
any assertion whose `citations` list was empty or did not resolve into the WP-P0-09 authority file.

| # | Fixed family name | Status / fixture | Decided WP-P0-09 oracle rows |
|---:|---|---|---|
| 1 | Entry signal | **BUILT** — `fixtures/family_01.json` | C01/GF-01 `:131-141`; C42/GF-42 `:1222-1270` |
| 2 | Direction / flip / regime lock | **BUILT** — `fixtures/family_02.json` | C05/GF-05 `:227-237`; C21/GF-21 `:606-616`; C32/GF-32 `:830-863`; C33/GF-33 `:871-886` |
| 3 | Position sizing | **BUILT** — `fixtures/family_03.json` | C07/GF-07 `:291-316`; C31/GF-31 `:812-822` |
| 4 | Contract multiplier | **BUILT** — `fixtures/family_04.json` | C08/GF-08 `:324-334` |
| 5 | Minimum notional | **BUILT** — `fixtures/family_05.json` | C09/GF-09 `:342-352` |
| 6 | Rounding / qty step / min qty | **BUILT** — `fixtures/family_06.json` | C09/GF-09 `:342-352`; C31/GF-31 `:812-822` |
| 7 | SL calculation (ATR / percent / swing) | **BUILT** — `fixtures/family_07.json` | C11/GF-11 `:411-421`; C24/GF-24 `:660-670` |
| 8 | TP calculation (ATR / percent / R) | **BUILT** — `fixtures/family_08.json` | C12/GF-12 `:429-439`; C24/GF-24 `:660-670` |
| 9 | Multi-TP lifecycle incl. partial TP1 fill | **BUILT** — `fixtures/family_09.json` | C13/GF-13 `:447-457` |
| 10 | Break-even trigger and buffer | **BUILT** — `fixtures/family_10.json` | C14/GF-14 `:465-475`; C36/GF-36 `:938-964` |
| 11 | Trailing activation and monotonicity | **BUILT** — `fixtures/family_11.json` | C15/GF-15 `:483-493`; C37/GF-37 `:972-987` |
| 12 | Opposite-signal exit | **BUILT** — `fixtures/family_12.json` | C05/GF-05 `:227-237`; C16/GF-16 `:501-511`; C21/GF-21 `:606-616` |
| 13 | Time exit (bars / EOD / EOW) | **BUILT** — `fixtures/family_13.json` | C17/GF-17 `:519-529`; C25/GF-25 `:678-688` |
| 14 | Bar gaps through the stop | **BUILT** — `fixtures/family_14.json` | C11/GF-11 `:411-421`; C20/GF-20 `:575-598` |
| 15 | Same-bar SL/TP collision | **BUILT** — `fixtures/family_15.json` | C19/GF-19 `:557-567` |
| 16 | Pyramiding / add / partial reduction | **BUILT** — `fixtures/family_16.json` | C06/GF-06 `:245-281`; C13/GF-13 `:447-457` |
| 17 | Fees, slippage, funding | **BUILT** — `fixtures/family_17.json` | C08/GF-08 `:324-334`; C22/GF-22 `:624-634` |
| 18 | Snapshot drift / bucket-capital divergence | **BLOCKED — UNBUILT** | WP-P0-09 explicit non-decision `:1282-1287`; no `SNAPSHOT_MISMATCH` row exists |
| 19 | Allocator ↔ Guardian boundary | **BLOCKED — UNBUILT** | C07 partially decides quantity ownership at `:291-316`, but WP-P0-09 explicitly leaves the internal split undecided at `:1282-1287`; no `REFERENCE_DIVERGENCE` row exists |
| 20 | Short-side symmetry | **BUILT** — `fixtures/family_20.json` | C24/GF-24 `:660-670`; cross-cutting reflection rule `:1274-1276` |
| 21 | NaN / zero / boundary precision | **BUILT** — `fixtures/family_21.json` | C07/GF-07 `:291-316`; C09/GF-09 `:342-352`; C24/GF-24 `:660-670` |
| 22 | Duplicate and reordered bars | **BUILT** — `fixtures/family_22.json` | C26/GF-26 `:696-706` |
| 23 | Cancellation and revision ordering | **BUILT** — `fixtures/family_23.json` | C26/GF-26 `:696-706` |
| 24 | `OrderIntent` idempotence | **BUILT** — `fixtures/family_24.json` | C26/GF-26 `:696-706` |
| 25 | Venue and session edge cases | **BUILT** — `fixtures/family_25.json` | C09/GF-09 `:342-352`; C17/GF-17 `:519-529`; C22/GF-22 `:624-634`; C25/GF-25 `:678-688`; C27/GF-27 `:716-738` |

## 3. Per-family targeted RED, restoration, and GREEN evidence

Each mutation below changed one candidate-output path only. The executed verifier required
`mismatch_count=1` and required the only mismatching path to be the declared target. “RESTORED”
means that exact path was put back to its fixture value before the byte comparison.

| # | Exact single-field mutation and real RED output | Real restoration and GREEN output |
|---:|---|---|
| 1 | `producer.bar4.raw`: `NONE → LONG`; `RED mismatch_count=1 path=producer.bar4.raw expected="NONE" actual="LONG"` | `RESTORED ... value="NONE"`; `GREEN byte_match=true sha256=91eef43f7169d2e28d39238181a8248506adbb182d2bc5c9885d5043805ad285` |
| 2 | `events.bar2`: `NONE → ENTER_SHORT`; `RED mismatch_count=1 path=events.bar2 expected="NONE" actual="ENTER_SHORT"` | `RESTORED ... value="NONE"`; `GREEN byte_match=true sha256=ced1f206dff54019b905e954d80ffd2181b104c9c7231ec3ad3c48ccd04864b3` |
| 3 | `request.has_snapshot_id`: `false → true`; `RED mismatch_count=1 path=request.has_snapshot_id expected=false actual=true` | `RESTORED ... value=false`; `GREEN byte_match=true sha256=e5d8b74eef8667f02d99e5df137f9a648aae0eed19c26961151f41c0fe8d6fe6` |
| 4 | `resolution.proposed_qty`: `2 → 20`; `RED mismatch_count=1 path=resolution.proposed_qty expected="2" actual="20"` | `RESTORED ... value="2"`; `GREEN byte_match=true sha256=11a4b28d02f2fa141f110cbc1e74004ec71328979326b87625582c6b1ea8b4d5` |
| 5 | `decision.outcome`: `REJECT → ACCEPT`; `RED mismatch_count=1 path=decision.outcome expected="REJECT" actual="ACCEPT"` | `RESTORED ... value="REJECT"`; `GREEN byte_match=true sha256=d62f3739b539187d67e6c258348b39718648e9fd38b09e3c0fae018928524602` |
| 6 | `round.quantity`: `1.23 → 1.239`; `RED mismatch_count=1 path=round.quantity expected="1.23" actual="1.239"` | `RESTORED ... value="1.23"`; `GREEN byte_match=true sha256=0c6d749e01512e96e614f0fbc76db61691ba43a9e74a127fe92cb4733a2dcc3f` |
| 7 | `swing.long.stop`: `97.00 → 90.00`; `RED mismatch_count=1 path=swing.long.stop expected="97.00" actual="90.00"` | `RESTORED ... value="97.00"`; `GREEN byte_match=true sha256=f8ec773fa7df3a892c61ab7a355e2f57429d29d1eb1539be3ba7e129a1fe548a` |
| 8 | `missing_stop.outcome`: `BLOCK → TARGET_AT_102.00`; `RED mismatch_count=1 path=missing_stop.outcome expected="BLOCK" actual="TARGET_AT_102.00"` | `RESTORED ... value="BLOCK"`; `GREEN byte_match=true sha256=181a1d0a10782909b0487aa1fe9eb90f8572546f0306e462661b048b420633b8` |
| 9 | `fills.tp1.qty`: `4 → 10`; `RED mismatch_count=1 path=fills.tp1.qty expected="4" actual="10"` | `RESTORED ... value="4"`; `GREEN byte_match=true sha256=e5ed0bdba1c023410c3aee3924dd9405b44688577582fe263fb34e2f640af0ce` |
| 10 | `canonical.exit_bar`: `3 → 2`; `RED mismatch_count=1 path=canonical.exit_bar expected=3 actual=2` | `RESTORED ... value=3`; `GREEN byte_match=true sha256=4ad1ef2864af7bc72fc6cacb8f78c504f34da91e50d274f5d4ae0ca4aa1668b5` |
| 11 | `canonical.stop_effective_bar`: `2 → 1`; `RED mismatch_count=1 path=canonical.stop_effective_bar expected=2 actual=1` | `RESTORED ... value=2`; `GREEN byte_match=true sha256=7ab8da96a1b534f2b636365a09de19fa8d90e8cbb26720400bf4a94dfbf408be` |
| 12 | `priority.filter_without_stop_or_opposite`: `ma_filter → htf_trend_filter`; `RED mismatch_count=1 path=priority.filter_without_stop_or_opposite expected="ma_filter" actual="htf_trend_filter"` | `RESTORED ... value="ma_filter"`; `GREEN byte_match=true sha256=8d5b57c24500d04c2bec12740983e02f813aad0346e9caef01c61805b15752ee` |
| 13 | `eod_exit.timestamp`: `2026-01-02T21:45:00Z → 2026-01-05T00:00:00Z`; `RED mismatch_count=1 path=eod_exit.timestamp expected="2026-01-02T21:45:00Z" actual="2026-01-05T00:00:00Z"` | `RESTORED ... value="2026-01-02T21:45:00Z"`; `GREEN byte_match=true sha256=0194a890d4f65022f0779048c3b3e5758eb74814fcb75046fbba265b3a74f464` |
| 14 | `fills.long_stop_gap`: `90.00 → 91.00`; `RED mismatch_count=1 path=fills.long_stop_gap expected="90.00" actual="91.00"` | `RESTORED ... value="90.00"`; `GREEN byte_match=true sha256=d1e13a43ecff20559df15b9bf50609851055c84e4122a9f0588c67f62ca52989` |
| 15 | `stop_first.fill`: `95.00 → 105.00`; `RED mismatch_count=1 path=stop_first.fill expected="95.00" actual="105.00"` | `RESTORED ... value="95.00"`; `GREEN byte_match=true sha256=1445452e6f3d6840044e5a5f33e2b6f7af403765ca111d698d1caff407659c91` |
| 16 | `events.bar5`: `BLOCK:POST_EXIT_COOLDOWN → ENTER_LONG:1@100.00`; `RED mismatch_count=1 path=events.bar5 expected="BLOCK:POST_EXIT_COOLDOWN" actual="ENTER_LONG:1@100.00"` | `RESTORED ... value="BLOCK:POST_EXIT_COOLDOWN"`; `GREEN byte_match=true sha256=9a9e6ee85ad88ef167e0c2562a4519403fcf55f78673a96bf670abbd312ce62d` |
| 17 | `pnl.net`: `17.5599 → 18.00`; `RED mismatch_count=1 path=pnl.net expected="17.5599" actual="18.00"` | `RESTORED ... value="17.5599"`; `GREEN byte_match=true sha256=2c51205f4b48a0406dad3fe4b4d7273b15d94d351330fe7b661f188a0646c661` |
| 20 | `mirror.family_07.stop`: `105.00 → 95.00`; `RED mismatch_count=1 path=mirror.family_07.stop expected="105.00" actual="95.00"` | `RESTORED ... value="105.00"`; `GREEN byte_match=true sha256=db46cf79bba84207562a1b122335ee574efb761632ee2247bedba3a37795c8a7` |
| 21 | `adx.exact_25`: `BLOCK:adx_filter → PASS`; `RED mismatch_count=1 path=adx.exact_25 expected="BLOCK:adx_filter" actual="PASS"` | `RESTORED ... value="BLOCK:adx_filter"`; `GREEN byte_match=true sha256=d6a234fb0a83858e07a491c863bb4bbb747d36dac8252f93bf1942f4b5e5e46d` |
| 22 | `duplicate.intent_count`: `1 → 2`; `RED mismatch_count=1 path=duplicate.intent_count expected=1 actual=2` | `RESTORED ... value=1`; `GREEN byte_match=true sha256=056ffd37b7450e84d14b48b106ac14f116f399482c04c66c60973f1cf4133d40` |
| 23 | `revision.accepted`: `2 → 1`; `RED mismatch_count=1 path=revision.accepted expected=2 actual=1` | `RESTORED ... value=2`; `GREEN byte_match=true sha256=54094df873625f83bd1cb1c3370a5480b0044bd029d36612cc36e301e7f77221` |
| 24 | `economic_effects.count`: `1 → 2`; `RED mismatch_count=1 path=economic_effects.count expected=1 actual=2` | `RESTORED ... value=1`; `GREEN byte_match=true sha256=0900f02fe9222f87459ba33e544d0fe173ea0c77b80f9d69fbbb49f2670d81e9` |
| 25 | `freshness.age_45_001`: `MISSED_DECISION_STALE:NO_ORDER → AGING:ORDER`; `RED mismatch_count=1 path=freshness.age_45_001 expected="MISSED_DECISION_STALE:NO_ORDER" actual="AGING:ORDER"` | `RESTORED ... value="MISSED_DECISION_STALE:NO_ORDER"`; `GREEN byte_match=true sha256=941e3340642546e168ccdb78f39a30ff89958999810a931edda565776d14b3b5` |

Executed command for each independent run (different empty output directories):

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_committed_run1_20260825
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures\verify_fixtures.py MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_10_GOLDEN_SUITE_2026-08-25\fixtures C:\tmp\wp_p010_committed_run2_20260825
```

Real terminal summary from each process:

```text
SUMMARY built=23 blocked=2 red=23 restored=23 green=23
```

The full terminal output produced the 69 per-family lines transcribed in the table above: one RED,
one RESTORED, and one GREEN for every built family.

## 4. Two-process determinism evidence

The two commands above were separate Python processes and rendered one normalized output file per
built family. A byte-array comparison over files with the same names returned:

```text
DETERMINISM_RUNS=2
OUTPUT_FILES_RUN1=23
OUTPUT_FILES_RUN2=23
BYTE_IDENTICAL=23/23
MISMATCHES=0
FAMILY_01_SHA256=91eef43f7169d2e28d39238181a8248506adbb182d2bc5c9885d5043805ad285
```

The normalization contract is fixed in `fixtures/README.md` and repeated in each fixture:
UTF-8 JSON object of assertion path to value, sorted keys, compact separators, and one LF terminator.
This evidence establishes deterministic fixture-oracle rendering; it does not claim that a future
kernel implementation has already executed the scenarios.

## 5. Formal blockers: families 18 and 19

### 5.1 Family 18 — snapshot drift / bucket-capital divergence

Family 18 remains **BLOCKED and unbuilt**. The WP-P0-09 table explicitly says it does not decide
snapshot-drift handling (`CAPABILITY_CANONICALIZATION_TABLE.md:1282-1287`), and the literal
`SNAPSHOT_MISMATCH` occurs zero times in all three merged WP-P0-09 documents. C07 carries snapshot
identity, but it does not decide the mismatch trigger, typed rejection event, no-order result, final
state, or guard-removal discriminator.

Unblock condition: WP-P0-09 must add a decided eight-field row specifying the exact
`SNAPSHOT_MISMATCH` input, ordered event/rejection, quantities and no-order result, final state, and
the guard-absent RED / guard-present GREEN discriminator. This is a **genuine D026 coverage hole**:
the required snapshot-drift regression case does not exist and is not waived as a cosmetic gap.

### 5.2 Family 19 — Allocator ↔ Guardian boundary

Family 19 remains **BLOCKED and unbuilt**. C07 decides that RA owns `proposed_qty` and that the
Guardian authorizes it unchanged or rejects, but WP-P0-09 expressly leaves the internal split
undecided (`CAPABILITY_CANONICALIZATION_TABLE.md:1282-1287`). The literal
`REFERENCE_DIVERGENCE` occurs zero times in all three merged WP-P0-09 documents, so there is no
row-derived discriminator, tolerance, typed rejection event, no-resize/no-order result, or final
state.

Unblock condition: WP-P0-09 must add a decided eight-field `REFERENCE_DIVERGENCE` row specifying
the deterministic recomputation comparison, any tolerance, authorize-unchanged-or-reject result,
ordered events, no-order/final-state oracle, and exact RED/GREEN discriminator.

No fixture file named `family_18.json` or `family_19.json` exists. Their statuses and unblock
conditions are first-class entries in `fixtures/manifest.json`, preventing absence from being read
as completion.

## 6. Counts, scope, and implementer self-QA

**Final counts: 23 BUILT, 2 BLOCKED, 25 TOTAL.** Built family numbers are
`1..17,20..25`; blocked numbers are exactly `18,19`.

Checks executed during implementation:

- fixture verifier, twice in separate processes: `built=23 blocked=2 red=23 restored=23 green=23` each time;
- two-run byte comparison: `BYTE_IDENTICAL=23/23`, `MISMATCHES=0`;
- JSON/citation integrity: all expected assertion paths unique, every citation non-empty and rooted in the WP-P0-09 canonicalization table, every stored output hash and state hash reproduced;
- blocked-manifest integrity: exactly families 18 and 19, each with missing semantics and an unblock condition;
- no family-18 or family-19 fixture file exists;
- family-1 companion corpus identity: Git blob `31bdafae4d4d94787508043e9681874f9dc43bda`, declared `48077` bars and `858` signals;
- no protected implementation or existing parity-corpus path changed.

The required T0 dual-flagship audit belongs to the live Claude Lead and follows this implementer
handoff. No audit or acceptance claim is issued here.

## 7. Git record

Fixture corpus commit: `5ff870ee` (`test(wp-p0-10): add 23 cited golden fixtures`).

The final pushed branch SHA is printed as the last line of the implementer's final output. A tracked
report cannot contain the SHA of the same commit that contains it: inserting that SHA changes the
tree and therefore changes the commit. This report records the stable content commit above and the
final output supplies the exact pushed tip without asserting a false self-reference.

**Final pushed commit SHA:** supplied in implementer output after commit and push.
