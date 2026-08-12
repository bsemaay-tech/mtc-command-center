# WP-I stale-hit remediation plan — 2026-08-12

Author: Claude `claude-opus-5` (Gate-3 counterpart IMPLEMENTER). The Codex Lead independently
owns acceptance. **This document does not claim acceptance and does not apply any correction.**

## 1. Scope, anchor, tier, and write constraint

**Task.** One remediation plan covering every REMAINING stale hit listed by the two source audits:

1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_INCOMPLETE_CORRECTION_SWEEP_2026-08-12.md`
2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_PACKAGE_CLAIM_AUDIT_2026-08-12.md`

**Audit tier.** T2 documentation/evidence. No trading, Pine, parity, MTC behavior, backtest or
optimization surface is in scope. No file in this plan is executable product code.

**HEAD anchor.** The contract names `6078ddb49389692845e914d396c4e04e83507579`.

> **Anchor drift — disclosed, not silently accepted, and explicitly bounded.** Repository HEAD
> moved twice while this plan was being written, both times by a concurrent session:
> `6078ddb4` (named anchor) → `0a3692dc` (SEC102 evidence-document claim audit) →
> `4e012466` (claim-audit synthesis across five evidence documents), the HEAD at completion.
>
> **Everything in this disclosure is a statement about the fixed diff
> `6078ddb4..4e012466` only. It is not a statement about HEAD, which continues to move.**
> That range touches **four** files (`git diff --name-only 6078ddb4..4e012466`):
>
> 1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_SEC102_2026-08-12.md` — new (+112)
> 2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_CLAIM_AUDIT_SYNTHESIS_2026-08-12.md` — new (+125)
> 3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/STATUS_SEC102.md` — modified (+29/−1)
> 4. `MTC_COMMAND_CENTER/11_TRIAGE/FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md` — modified (+24)
>
> *(An earlier draft of this paragraph said "exactly three files" and omitted `STATUS_SEC102.md`;
> corrected 2026-08-12 against the diff itself. `STATUS_SEC102.md` is not a class-A or class-B
> target of this plan.)* **Within that range, no class-A or class-B target file below was
> modified.** The one affected reference is C-16, in the handoff file.
>
> **Beyond `4e012466` this plan makes no claim.** The one affected reference, C-16, is cited below
> exactly as the source sweep cited it — `FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md:198-209`,
> **at the named anchor `6078ddb4`**. Commits inside the bounded range, and later commits beyond it,
> can shift that leave-alone history block; **no current-tree line number is claimed for it.** C-16
> is a Part-C leave-alone entry, so nothing is applied to it and no current line is needed —
> a reader who does need to locate it must re-read the block at the anchor and re-verify.
>
> **Every class-A and class-B `file:line` reference in this plan is anchored at `6078ddb4`.**
> Where a source audit's own line citation had already drifted by the anchor, the drift is called
> out in the entry. Any reader applying this plan at a later HEAD must re-verify line numbers
> rather than trust these citations — the guarantee here is bounded by a named commit, not by
> "current".

**Sole writable path.** `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STALE_REMEDIATION_PLAN_2026-08-12.md`
— this file. **No existing file is to be edited by this task.** Every file named below is
read-only for the purposes of *this* task; the entries are proposals for a later, separately
authorized application pass. No Git mutation, no host contact, no network, no tests or backtests
were performed. Handoffs and memory were not updated.

**Classification vocabulary used throughout.**

| Class | Meaning | Action |
|---|---|---|
| **A — genuine current-state staleness** | Text presented as current state that the current bytes contradict. | Correct the text. |
| **B — once-valid derivative, now unlabelled** | The finding was true when produced and its provenance is worth keeping, but nothing in the document marks it closed, so it now reads as a live defect. | Do **not** delete. Add an explicit superseded/history marker in place. |
| **C — already history** | Already struck through, time-bounded, labelled superseded/corrected, or an unchosen alternative. | **LEAVE ALONE.** Editing these destroys deliberately retained provenance. |

## 2. Indeterminate values — flagged, not invented

Two values in this plan are **not determined by the repository** and are therefore left as
placeholders. No number is guessed for either.

| ID | Value | Why indeterminate |
|---|---|---|
| **IND-1** | `r17_literal_zero_measurements` (true measured value) | The R17 harness hardcodes the field rather than measuring it (§3.1). Nothing in the repo computes it. Requires execution — see the proposed computation and regeneration procedure in §3.1.3. |
| **IND-2** | `literal_zero_fields` / `literal_zero_lines` for the R16 side (`6` / `3` as measured rather than asserted) | Same root cause. `SELF_QA_RP6.md:13417-13418` assigns both as constants. The values happen to match a manual count, but no byte-level derivation exists in the repo. |

Every entry below that depends on IND-1 or IND-2 marks its proposed replacement text
`INDETERMINATE pending execution` and is written so that the surrounding prose is **true without
the number**. Nothing in this plan may be applied in a way that publishes a number for IND-1 or
IND-2 before the computation in §3.1.3 has actually run.

---

# PART A — Class A: genuine current-state staleness

Ordered by severity.

**Count.** **14 CONTRACTED entries covering 16 cited sites** (A1.4 carries two sub-hits and A2.2
covers two ledger lines, which is why sites exceed entries), **plus the optional A1.5 addendum —
1 entry / 2 extra sites, explicitly NOT contracted**. **Part A total: 15 entries / 18 sites.**
Class B remains **15 entries**.

## 3.1 SEV-1 — R17 publishes a hardcoded literal-zero field, and four documents claim the class was eliminated

Source: prereg-package audit **F1** (its "most consequential finding"). Contract item 5 + 6.

### 3.1.1 The root defect (evidence, not a claim)

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:13417-13419`, exact current text:

```text
literal_zero_fields=6
literal_zero_lines=3
rok "r17_pass_format_audit r16_literal_zero_fields=$literal_zero_fields r16_lines=3 r17_literal_zero_measurements=0"
```

Three separate problems visible in three lines:

1. `literal_zero_fields` and `literal_zero_lines` are **assigned as constants**. Nothing counts them.
2. `r17_literal_zero_measurements=0` is a **literal string in the emitter**. No count, comparison,
   or scan produces it before `rok` marks the assertion met.
3. `literal_zero_lines` is assigned at `:13418` and then **never read** — the emitter hardcodes
   `r16_lines=3` instead of expanding `$literal_zero_lines`. The one variable that could have
   carried a measurement is dead.

Consequence at `SELF_QA_RP6.md:13458`, the published transcript line:

```text
R17_ASSERT_MET r17_pass_format_audit r16_literal_zero_fields=6 r16_lines=3 r17_literal_zero_measurements=0
```

This is self-refuting on its face: the assertion that R17 publishes no literal-zero measurement
is itself a published literal-zero field.

### 3.1.2 What IS supported — preserve this, do not over-correct

The narrower fact is genuinely evidenced and **must survive the correction**:

- `SELF_QA_RP6.md:13290-13302` — `r17_target_report()` computes `dynamic_targets` for real:
  `n_vt` from `grep -c '^VARTARGET '`, `n_dyn_var` and `n_opaque` from `grep -c` over `UNMODELED`
  records, `n_effect` from a line count, and `n_dyn=$((n_dyn_var + n_opaque + n_effect))`.
  This is a measurement.
- `SELF_QA_RP6.md:13460-13461` — the RED/GREEN pair for the dynamic-target class exists:
  `D026_RED_WEAKENED_R16 mutant=eval rc=0 summary=PASS` against
  `D026_GREEN_R17 mutant=eval refused rc=1 report=[… dynamic_targets=1 … opaque_mutators=1 …]`.

**So: `dynamic_targets` was converted from a hardcoded literal into a computed field, and its
falsification pair exists. What is NOT supported is the broader claim that the literal-zero
measurement class was eliminated.** Every correction below keeps the first and drops the second.

### 3.1.3 Proposed real computation + transcript regeneration (prerequisite to any number)

The constant block at `SELF_QA_RP6.md:13417-13419` must be replaced with a derivation over bytes.
What that derivation is remains to be designed, reviewed, and executed under a separate
authorization — **not applied by this task**.

#### NON-AUTHORITATIVE PROCEDURE SKETCH

An earlier revision of this section carried a concrete `grep`/`sed` scanner as if it were the
replacement. **That sketch has been removed and is not an implementation.** It was never executed
against the repo, its pattern was never validated, and a naive `<name>=0` scan cannot distinguish a
hardcoded literal from a genuine measured-zero output: fields such as `fail=0`, `rc=0`,
`inventory_targets=0` or `dynamic_targets=0` are real measurements that happen to evaluate to zero,
and counting them would inflate the audit exactly the way the defect this section documents
deflates it. Publishing a number from an untested scanner would repeat the original error in the
opposite direction. What follows is a requirements list for whoever implements the real thing, not
runnable code:

1. **Decide and document the counting rules first** — source-literal vs transcript-textual (fork
   (a) below), and whether the audit counts its own output line (fork (b) below). Both must be
   written down in the corrected prose before any scan runs.
2. **Enumerate the bounded set of R16/R17 emitter fields by hand**, recording line number and field
   name as evidence for each. The emitter regions are bounded and small enough to enumerate; do not
   substitute a regex sweep for the enumeration.
3. **Derive the published counts from that enumeration**, never from constants. No field in the
   emitted line may be a hardcoded number.
4. **Falsify the detector before trusting it.** Inject a known literal-zero field into a scanned
   region and show the count rises by exactly 1; then remove or mutate that field and show it falls
   by exactly 1. A detector that does not move under both operations is not evidence.
5. **Run the published R17 fence verbatim and regenerate the transcript** (see the regeneration
   paragraph below for the run command and the transcript block to replace).
6. **Re-pin the `SELF_QA_RP6.md` identity and every downstream identity claim** in the same pass
   (see the same paragraph, and §7).
7. **IND-1 and IND-2 remain `INDETERMINATE` until that execution has happened.** No value may be
   published before it — including `0`.

Regeneration detail for requirements 5 and 6: rerun the published R17 fence verbatim via its own run command
at `SELF_QA_RP6.md:13444`, and replace the transcript block containing `:13458` with the real
captured output. The `SELF_QA_RP6.md` byte identity (`1038848 B` / `07cf843d…`) **will change**;
every document pinning that identity must be re-pinned in the same pass, and the r17 bytes have no
independent audit either way (`AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:25`).

**Two definitional forks the implementer must resolve before running, because they change the
answer and the repo does not settle them:**

- **(a) Source-literal vs transcript-textual.** Under a source-literal rule — the `0` written into
  the emitter itself, not expanded from a variable or command substitution —
  `inventory_targets=0` / `dynamic_targets=0` in the `r17_dynamic_targets_measured` line do **not**
  count — they are `%s` expansions of computed variables that happened to evaluate to 0. Under a
  purely textual scan of the emitted transcript, they **would** count. The R16 audit that produced
  `6` used the source-literal rule; consistency argues for keeping it, but this must be stated
  explicitly in the corrected prose rather than assumed.
- **(b) Self-counting.** The audit emitter itself publishes `r17_literal_zero_measurements` as an
  expansion of its own computed count. If that expands to `0` it is a
  literal-zero-*looking* field produced by a measurement. Whether the
  audit counts its own output line is undecided in the repo.

**Because of (a) and (b), the final numeric output is `INDETERMINATE pending execution` (IND-1,
IND-2). Do not publish a value — including `0` — until the scan has actually run under a stated
rule.** The lower bound that IS certain today: under a textual reading the current R17 output
contains at least one literal-zero field, so the present `=0` is false under that reading.

### 3.1.4 Downstream prose corrections (apply only after §3.1.3, or apply the hedged form now)

Each entry gives exact current file:line, exact stale text, and exact proposed replacement.

---

**A1.1 — `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md:48-56`** *(class A)*

Exact stale text (lines 48-56):

```text
`dynamic_targets` is the measured total of unresolved target surfaces:
`dynamic_variable_target` records, `indirect_execution_builtin:*` records, and
R17 effect-model misses. No literal zero is published as a measurement in the R17
pass format.

The pass-format audit found **six literal-zero fields across three R16 success
lines** that could be read as measurements (`expand_aliases_enabled=0`, the
three shadow counts, `inventory_targets=0`, and `dynamic_targets=0`). R17 does
not republish those as literals; it emits measured counts or omits the detail.
```

Proposed replacement:

```text
`dynamic_targets` is the measured total of unresolved target surfaces:
`dynamic_variable_target` records, `indirect_execution_builtin:*` records, and
R17 effect-model misses. It is computed at `SELF_QA_RP6.md:13290-13302` from
tokenizer records — this specific field is a real measurement, and its RED/GREEN
falsification pair is published at `SELF_QA_RP6.md:13460-13461`.

**Scope correction 2026-08-12 — the broader pass-format claim is NOT supported.**
This section previously read "No literal zero is published as a measurement in the
R17 pass format" and reported the pass-format audit as finding **six literal-zero
fields across three R16 success lines**. Those figures are **asserted, not
measured**: `SELF_QA_RP6.md:13417-13418` assigns `literal_zero_fields=6` and
`literal_zero_lines=3` as constants, and `:13419` emits
`r17_literal_zero_measurements=0` as a source literal — that published field is
itself a literal zero presented as a measurement. The true count is
**INDETERMINATE pending execution** of the measured scan and transcript
regeneration described in `WPI_STALE_REMEDIATION_PLAN_2026-08-12.md` §3.1.3.
No value for it, including zero, may be published until that scan has run.
```

Justification: the file states as current fact the exact proposition the R17 harness contradicts
in its own bytes, while the narrower `dynamic_targets` fact it also states is true and is preserved.

---

**A1.2 — `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_ACCEPTANCE_MATRIX_2026-08-12.md:25`** *(class A)*

Exact stale fragment inside the "Latest current-state result" cell:

```text
and `dynamic_targets` converted from a hardcoded literal into a real measurement (six such literal-zero fields found across three r16 lines; `r17_literal_zero_measurements=0`).
```

Proposed replacement fragment (rest of the cell unchanged):

```text
and `dynamic_targets` converted from a hardcoded literal into a real measurement (computed at `SELF_QA_RP6.md:13290-13302`). **[corrected 2026-08-12 — the accompanying pass-format figures are withdrawn]** The former parenthetical "six such literal-zero fields found across three r16 lines; `r17_literal_zero_measurements=0`" is **not evidence**: all three values are hardcoded at `SELF_QA_RP6.md:13417-13419`. The literal-zero measurement class is **NOT** established as eliminated; the true count is INDETERMINATE pending the measured rerun. The `dynamic_targets` conversion and its RED/GREEN pair are unaffected and stand.
```

Justification: this is the acceptance matrix — the document an Audit-2 auditor treats as the
authority on what was accepted. It must not carry an unmeasured number as a closure basis.

---

**A1.3 — `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:31`** *(class A)*

Exact stale fragment inside the RP6-11 **GREEN** cell:

```text
with `dynamic_targets` converted from a hardcoded literal into a measured field (`r17_literal_zero_measurements=0`)
```

Proposed replacement fragment:

```text
with `dynamic_targets` converted from a hardcoded literal into a measured field (computed at `SELF_QA_RP6.md:13290-13302`) — **note (added 2026-08-12): the former citation `r17_literal_zero_measurements=0` is withdrawn as unsupported (hardcoded at `SELF_QA_RP6.md:13417-13419`); it never bore on this row's closure, which rests on the RED/GREEN pair at `SELF_QA_RP6.md:13460-13461`**
```

Justification: removes the unsupported field while explicitly preserving the RP6-11 **FULLY
CLOSED** disposition, which does not depend on it. The row's closure basis is the RED/GREEN pair,
not the pass-format audit — this correction must not be read as reopening RP6-11.

---

**A1.4 — `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:158-173`** *(class A, two sub-hits)*

*Contract item 6 names `:158-173`; the source audit F1 named `:160-173`. Current bytes: the stale
statements sit at `:159-160` and `:173`, inside the `:158-173` disposition block. Both are listed.*

**Sub-hit :159-160** — exact stale text. The stale claim is one sentence that wraps across two
lines; it begins with the word `Round` at the end of `:159` and ends at `:160`, so the whole
sentence is quoted rather than the `:160` fragment alone — a fragment-only edit would leave a
dangling `Round` on `:159`:

```text
Round
17's pass-format audit found **six** such literal-zero fields across three r16 success lines.
```

Proposed replacement (same two-line span):

```text
Round
17's pass-format audit reported six such literal-zero fields across three r16 success lines —
**but see the correction note below: that figure is asserted, not measured.**
```

**Sub-hit :173** — exact stale text:

```text
`r17_literal_zero_measurements=0`, block identity unchanged.
```

Proposed replacement:

```text
block identity unchanged. *(Corrected 2026-08-12 — `r17_literal_zero_measurements=0` was removed
from this evidence list. It is hardcoded at `SELF_QA_RP6.md:13417-13419`, not measured, so it is
not evidence of record. The measured `R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=15 fail=0` and the
unchanged block identity are unaffected. The true literal-zero count is INDETERMINATE pending the
measured rerun in `WPI_STALE_REMEDIATION_PLAN_2026-08-12.md` §3.1.3. This is a fourth instance of
the same class the map already records: a number that looks measured and is not.)*
```

Justification: `:173` is labelled "Lead verbatim run (evidence of record)". A hardcoded constant
must not sit in an evidence-of-record list. `:164-165`, which states the `dynamic_targets`
composition, is **correct and must be left as-is**.

---

**A1.5 (addendum — found during inspection, not enumerated in either source audit)**

Two further sites publish the same unsupported field. The contract requires **every** remaining
stale hit; these are surfaced rather than silently dropped, and flagged as additions so the Lead
can accept or reject them separately from the contracted set.

| File:line | Exact stale text | Proposed replacement | Justification |
|---|---|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:96` | ``r17_literal_zero_measurements=0`, block identity unchanged (110817 B, `5132bacd…`).`` | ``block identity unchanged (110817 B, `5132bacd…`). *(`r17_literal_zero_measurements=0` removed 2026-08-12 — hardcoded at `SELF_QA_RP6.md:13417-13419`, not measured; INDETERMINATE pending the measured rerun.)*`` | Same defect, same evidence-list context, in the freeze blocker map. |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_R17_REPORT_2026-08-12.md:61-64` | ``Pass-format audit result: six literal-zero fields across three R16 success lines could be read as measurements (…). R17 publishes measured fields or omits those details; `r17_literal_zero_measurements=0`.`` | ``Pass-format audit result **[corrected 2026-08-12 — figures withdrawn]**: this report stated six literal-zero fields across three R16 success lines and `r17_literal_zero_measurements=0`. All three values are hardcoded at `SELF_QA_RP6.md:13417-13419`, not measured. R17 does publish measured fields for `dynamic_targets` (`SELF_QA_RP6.md:13290-13302`); the pass-format count itself is INDETERMINATE pending the measured rerun.`` | The r17 implementation report is the origin of the claim; leaving it uncorrected reseeds the defect on any re-read. |

---

## 3.2 SEV-2 — Blocker 8 is still presented as a live CONTRADICTED row and counted as such

Source: incomplete-correction sweep value 8. Contract item 8.

**Established current state.** The blocker-8 contract disagreement is **reconciled**. Plan rows
07/08 and `remote_close_tree_wpi.sh` agree on the three-argument contract; the stale two-arg record
was corrected in both respects (`WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:107-117`). Row 45's contract
question is therefore **FILLED**, and the identity-pin gap that remains
(`EXPECT_UID`/`EXPECT_GID` still `<PIN-AT-FREEZE>`) is **already carried in row 7 as
REQUIRES-HOST** — it must not be double-counted into row 45.

**Corrected tally (contract-supplied, arithmetic verified: 3 + 29 + 0 + 0 + 13 = 45):**

| Status | Current (stale) | Corrected |
|---|---:|---:|
| FILLED | 2 | **3** |
| LITERAL-MARKER | 29 | 29 |
| MISSING-CONSUMER | 0 | 0 |
| CONTRADICTED | 1 | **0** |
| REQUIRES-HOST | 13 | 13 |
| **Total rows** | 45 | **45** |

---

**A2.1 — `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:80`** *(class A — row 45)*

Exact stale text (status cell and the trailing clause):

```text
| 45 | Close-script argv, `WORK_ROOT`, scratch, and launch-domain contract | CONTRADICTED | … A stale current record still says the composition passes two args and exits before RUNID/EV_DIR at `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:167`. R3 keeps blocker 8 open until the prereg section 4.7, plan rows 07/08, derivation contract, launch-domain claim, scratch semantics, and bytes describe one byte-identical contract at `WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:410-414`; the blocker map keeps item 8 open at `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:20`.
```

Proposed replacement:

```text
| 45 | Close-script argv, `WORK_ROOT`, scratch, and launch-domain contract | FILLED | Current transport plan passes three args for close ops at `TRANSPORT_PLAN.tsv:8-9`; current close script requires exactly three args and assigns `EV_DIR`, `RUNID`, and `WORK_ROOT` at `remote_close_tree_wpi.sh:282-286`. **[reclassified 2026-08-12 ~19:40 — was CONTRADICTED]** The stale two-arg record at `RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:167` has since been corrected in both respects it was wrong about (the two-arg claim, and the "exits FAIL on argc" claim — an argv-count violation returns rc 3 STOP, not rc 1 FAIL). Plan, script and record now describe one contract, so no documentary contradiction survives. The residual `EXPECT_UID`/`EXPECT_GID` identity pins are **not** counted here — they are row 7's REQUIRES-HOST scope, and counting them twice would inflate the tally. See `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:107-117`.
```

Justification: this is the only row carrying `CONTRADICTED`, and the contradiction it cites was
repaired. The explicit non-double-count note is required so the reclassification does not silently
drop the real remaining gap.

---

**A2.2 — `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:134` and `:137`** *(class A — summary tally)*

*Contract item 8 names the tally at `:137`. Current bytes: the tally table spans `:132-139`;
`CONTRADICTED | 1` is at `:137` and `FILLED | 2` is at `:134`. Reclassifying row 45 to FILLED
moves both cells, so `:134` is included — correcting only `:137` would leave the table summing
to 44 and would be internally inconsistent.*

| Line | Exact stale text | Proposed replacement |
|---|---|---|
| `:134` | `\| FILLED \| 2 \|` | `\| FILLED \| 3 \|` |
| `:137` | `\| CONTRADICTED \| 1 \|` | `\| CONTRADICTED \| 0 \|` |

Add immediately below the table (after `:139`):

```text
*(Tally corrected 2026-08-12 — row 45 reclassified CONTRADICTED → FILLED after the stale two-arg
record was fixed; FILLED 2→3, CONTRADICTED 1→0. Total remains 45: 3 + 29 + 0 + 0 + 13. The
`EXPECT_UID`/`EXPECT_GID` gap remains counted once, in row 7's REQUIRES-HOST 13.)*
```

Justification: `:137` presents `CONTRADICTED 1` as current; `:134` must move with it or the table
no longer conserves 45. Contract item 8 fixes the target values; the arithmetic is verified above.

---

**A2.3 — `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:24`** *(class A — tally propagation; first of two hits on this line)*

Exact stale fragment:

```text
reconciles 45 duplicate-consumer rows (FILLED 2, LITERAL-MARKER 29, MISSING-CONSUMER 0, CONTRADICTED 1, REQUIRES-HOST 13)
```

Proposed replacement fragment:

```text
reconciles 45 duplicate-consumer rows (FILLED 3, LITERAL-MARKER 29, MISSING-CONSUMER 0, CONTRADICTED 0, REQUIRES-HOST 13) **[tally corrected 2026-08-12 — was FILLED 2 / CONTRADICTED 1; row 45's contract question is reconciled and the identity-pin gap is counted once, in row 7]**
```

Justification: contract item 8 requires the corrected tally to propagate here. This line is the
packet-level summary an Audit-2 auditor reads instead of the ledger.

---

**A2.4 — `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:99-100`** *(class A — tally propagation)*

Exact stale text:

```text
**Freeze-input ledger findings** (`WPI_FREEZE_INPUT_LEDGER_2026-08-12.md`, 45 rows: FILLED 2,
LITERAL-MARKER 29, MISSING-CONSUMER 0, CONTRADICTED 1, REQUIRES-HOST 13):
```

Proposed replacement:

```text
**Freeze-input ledger findings** (`WPI_FREEZE_INPUT_LEDGER_2026-08-12.md`, 45 rows: FILLED 3,
LITERAL-MARKER 29, MISSING-CONSUMER 0, CONTRADICTED 0, REQUIRES-HOST 13 — *tally corrected
2026-08-12; it read FILLED 2 / CONTRADICTED 1, which contradicted this same file's own item-8
reclassification twelve lines below at `:107-117`*):
```

Justification: the map states `CONTRADICTED 1` at `:99-100` and then reclassifies the only
contradicted row at `:107-117`. The file contradicts itself; the header tally is the stale side.

---

## 3.3 SEV-3 — The handoff package's per-packet detail contradicts its own 16/1/3 headline

Source: prereg-package audit **F2**. Contract item 7.

The headline at `AUDIT2_HANDOFF_PACKAGE.md:32-39` (16 closed / 1 partial / 3 open) and the summary
rows at `:23-24` are **current and correct**. The per-packet detail sections were not updated.

---

**A3.1 — `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:142-147`** *(class A)*

Exact stale text:

```text
### Packet 7 - current WP-I D026 map

[refreshed 2026-08-12] NOT-YET-AVAILABLE AS A COMPLETE PACKET. Partial exact sources
and their missing fields are indexed in `AUDIT2_D026_RED_LOCATIONS.md`. Final coverage must
map RP6, RP7, transport, SEC102, pathscope, and rows 1-9 to exact RED/GREEN commands and
outputs, pre-fix/mutation identity, and final accepted bytes.
```

Proposed replacement:

```text
### Packet 7 - current WP-I D026 map

**[updated 2026-08-12 ~16:35] CLOSED AS A PACKET; ROWS 1-9 STILL UNBUILT.**
`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` maps 39 closure rows across RP6, RP7, transport,
SEC102 and pathscope to exact RED/GREEN commands and outputs, mutation identity and final accepted
bytes: 29 fully closed, 0 open, 10 unlocated/supplemental (`TR-01`..`TR-09` plus `PS-09`), 15
disclosed residuals (`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:133-139`). Its one former OPEN
row, `RP6-11`, was resolved the same day by RP6 round 17. Rows 1-9 are absent because they are not
built yet — the packet's stated residual, not a gap in the map. `AUDIT2_D026_RED_LOCATIONS.md`
remains the partial-source index. *(This section previously read NOT-YET-AVAILABLE AS A COMPLETE
PACKET, contradicting the same file's `:23` and `:32-39`.)*
```

Justification: the same file says CLOSED at `:23` and `:33-34` and NOT-YET-AVAILABLE at `:144`.
A dispatcher reading only the detail section would treat a closed packet as missing.

---

**A3.2 — `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:149-155`** *(class A)*

Exact stale text:

```text
### Packet 8 - final freeze-input ledger

[refreshed 2026-08-12] NOT-YET-AVAILABLE. It must reconcile RP6 embedded pins, RP7
projection/trusted-Python/evidence-root pins, both tool maps, five row-8 attestation values
and wrapper copies, transport mount/OpenSSH/credential digests, close-script and archive
identities, block/wrapper hashes, allocations, accepting-input arms, and evidence-root
provenance. No final filled composite exists.
```

Proposed replacement:

```text
### Packet 8 - final freeze-input ledger

**[updated 2026-08-12 ~16:35] PARTIAL — analysis delivered, final ledger NOT-YET-AVAILABLE.**
`WPI_FREEZE_INPUT_LEDGER_2026-08-12.md` reconciles 45 duplicate-consumer rows (FILLED 3,
LITERAL-MARKER 29, MISSING-CONSUMER 0, CONTRADICTED 0, REQUIRES-HOST 13) and answers freeze
blockers 7, 8 and 9 with file:line evidence. The **final** ledger still cannot exist: it must
additionally carry RP6 embedded pins, RP7 projection/trusted-Python/evidence-root pins, both tool
maps, five row-8 attestation values and wrapper copies, transport mount/OpenSSH/credential digests,
close-script and archive identities, block/wrapper hashes, allocations, accepting-input arms, and
evidence-root provenance — all of which need the actual fills and allocations that only the Stage-1
run produces. No final filled composite exists. *(This section previously read a flat
NOT-YET-AVAILABLE, contradicting the same file's `:24` and `:32-39`.)*
```

Justification: PARTIAL and NOT-YET-AVAILABLE are different dispatch states. The correction keeps
every genuinely-missing item explicit, so nothing is upgraded by the edit. Tally matches A2.3.

---

**A3.3 — `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:193-195`** *(class A — partial correction only)*

Source: prereg-package audit **F3**, D026/freeze-input portion. Contract item 7.

Exact stale text (the remaining stale portion of the "Current dispatch status" sentence):

```text
the current-work
D026/freeze-input/host evidence packets do not exist, and the exact mandated suite baseline
and freeze-time ledger are unresolved.
```

Proposed replacement:

```text
the current-work **host-evidence** packet does not exist, and the exact mandated suite baseline
and freeze-time ledger are unresolved. *(Corrected 2026-08-12 — this clause also named the
current-work D026 and freeze-input packets as non-existent. Both exist:
`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` is Packet 7, CLOSED as a packet, and
`WPI_FREEZE_INPUT_LEDGER_2026-08-12.md` is Packet 8, PARTIAL — the final filled ledger is what is
missing, not the analysis. Packet 9 host evidence remains genuinely NOT-YET-AVAILABLE and is
unchanged.)*
```

Justification: three items were bundled into one clause; two are stale and one is true.
The correction splits them rather than striking the whole clause, so the genuine Packet-9 gap
is not accidentally cleared. **The SEC102 portion of this same paragraph at `:190-192` is already
corrected and must be LEFT ALONE** — see C-3.

---

## 3.4 SEV-4 — Open questions still says the current D026 map is absent

Source: prereg-package audit **F4**. Contract item 7.

**A4.1 — `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/OPEN_QUESTIONS_FOR_DISPATCHER.md:41-47`** *(class A)*

Exact stale text:

```text
## 3. Final D026 map for current WP-I work

[refreshed 2026-08-12] Open dispatch blocker: the corrected older WP-L/B3 mappings are
present, but the complete current RP6, RP7, transport, SEC102, pathscope, and future rows
1-9 map is not. Require exact RED command/output, pre-fix or mutation identity, GREEN
command/output, and final accepted identity per closure test. Current audit REDs without
accepted GREEN remain open; helper-only or non-literal evidence remains supplemental.
```

Proposed replacement:

```text
## 3. Final D026 map for current WP-I work

**[updated 2026-08-12] NARROWED — no longer a map-existence blocker.** The complete current
RP6/RP7/transport/SEC102/pathscope map now exists:
`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` supplies exact RED command/output, pre-fix or
mutation identity, GREEN command/output and final accepted identity per closure test — 39 rows,
29 fully closed, **0 open current-audit findings**, 10 unlocated/supplemental (`TR-01`..`TR-09`
plus `PS-09`), 15 disclosed residuals (`:133-139`). The corrected older WP-L/B3 mappings remain
present.

**What genuinely remains open:** rows 1-9 are not built, so they are absent from the map by design
rather than by omission; the 10 unlocated/supplemental rows are **not** upgraded by that map and
helper-only or non-literal evidence remains supplemental.

*(This section previously read "the complete current … map is not [present]" and "Current audit
REDs without accepted GREEN remain open." Both were true when written and both are now stale: the
map exists, and the last open RED — `RP6-11` — was closed by RP6 round 17.)*
```

Justification: this file is the dispatcher's blocker list. A resolved blocker left in it stops
dispatch on a condition that is already satisfied. The correction preserves the three conditions
that are still genuinely open.

---

## 3.5 SEV-5 — "17 freeze literals" published without the definitions/occurrences qualifier

Source: incomplete-correction sweep value 5. Contract item 8 (second hit on handoff `:24`).

Established: **17 distinct `P0_FIXED_*` definitions**; **27 raw `<PIN-AT-FREEZE>` occurrences**;
the extra 10 are fence/guard occurrences that enforce the refusal. Both numbers are correct with
different referents (`WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:88`,
`WPI_BLOCKS_DRAFT/RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md:202-205`).

| # | File:line | Exact stale text | Proposed replacement | Justification |
|---|---|---|---|---|
| **A5.1** | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:24` | `It establishes that RP6 cannot produce an end-to-end P0 PASS while 17 freeze literals remain` | `It establishes that RP6 cannot produce an end-to-end P0 PASS while the **17 distinct `P0_FIXED_*` freeze-literal definitions (27 raw `<PIN-AT-FREEZE>` occurrences — the extra 10 are the fence/guard occurrences that enforce the refusal; both counts are correct with different referents)** remain` | Bare "17" reads as a raw occurrence count and has already caused one spot-check disagreement. Ambiguity resolved at the point of use. |
| **A5.2** | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:103-104` | `With 17 remaining freeze` / `literals **RP6 cannot produce an end-to-end P0 PASS**` | `With the **17 distinct `P0_FIXED_*` freeze-literal definitions remaining (27 raw `<PIN-AT-FREEZE>` occurrences; the extra 10 are enforcing fence/guard occurrences — both counts correct, different referents; full reconciliation at `:166-168` of this file)**, **RP6 cannot produce an end-to-end P0 PASS**` | This is the file's current-state summary point; it omits a distinction the same file makes correctly 60 lines later. |

Both entries leave the load-bearing conclusion — source/audit acceptance ≠ host end-to-end PASS —
completely untouched.

---

# PART B — Class B: once-valid derivative findings now unlabelled

These were **correct when produced**. Their targets have since been repaired, so they now read as
live defects. **Do not delete them** — the provenance of who caught what, and when, is the record
of how the corrections were reached. Each gets an in-place history marker.

Contract item 9.

## 4.1 `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md`

Proposed **document-level banner**, inserted immediately after the title, covering all six hits:

```text
> **HISTORICAL / RESOLVED — 2026-08-12. Read this first.** This recheck was accurate when
> produced and its correction was adopted: the target map
> `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` was repaired at ~18:05 (row + summary) and again
> at ~19:25 (line 139). **Every "DISAGREE", "still says", and "still need Lead edits" statement
> below is therefore closed, not live.** The current map reads 39 rows / 29 fully closed / 0 open
> / 10 unlocated-supplemental / 15 residuals — exactly the figures this recheck derived. Retained
> in full as the record of the re-derivation that caught the misclassification. Note also that the
> map line numbers cited below (`:131`-`:137`) have themselves shifted with the repair; the
> current summary block is at `:133-139`.
```

Per-hit markers (each appended in place, so a reader landing mid-document is not misled):

| # | Line | Exact stale text | Proposed replacement | Justification |
|---|---|---|---|---|
| **B1.1** | `:29` | `\| Fully closed with located RED + GREEN on stated final bytes \| 28 (…:132) \| 29 \| DISAGREE \|` | `… \| 29 \| ~~DISAGREE~~ **RESOLVED — map now reads 29** \|` | The map was corrected to 29; the disagreement no longer exists. |
| **B1.2** | `:30` | `\| Unlocated/supplemental evidence flags \| 11 (…:134) \| 10 \| DISAGREE \|` | `… \| 10 \| ~~DISAGREE~~ **RESOLVED — map now reads 10** \|` | Same repair. |
| **B1.3** | `:32` | `MATCH, but stale contradicting text remains at `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:137`` | `MATCH. ~~…but stale contradicting text remains at `…:137`~~ **RESOLVED 2026-08-12 ~19:25 — that sentence (now `:139`) is struck through and corrected to ZERO open.**` | The cited stale text was corrected; the citation also drifted `:137`→`:139`. |
| **B1.4** | `:40` | `The table row still says `UNLOCATED - supplemental` … and `OPEN` (…:31).` | `~~The table row still says `UNLOCATED - supplemental` … and `OPEN`~~ **RESOLVED 2026-08-12 ~18:05 — `…:31` now reads "CLOSED by round 17 … FULLY CLOSED", with the correction annotated in the row itself.**` | The row was repaired; this is the single classification disagreement, now adopted. |
| **B1.5** | `:76-77` | `Stale text to fix later: `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:137` still says one open current-audit finding remains. Corrected number: 0.` | `~~Stale text to fix later: `…:137` still says one open current-audit finding remains.~~ **FIXED 2026-08-12 ~19:25** at what is now `…:139`; the corrected number 0 was adopted.` | The "to fix later" item was fixed. |
| **B1.6** | `:101` | `…but the map's row-level and supplemental-count text still need Lead edits to avoid carrying the obsolete pre-r17 `RP6-11` classification.` | `…and the map's row-level and supplemental-count text ~~still need Lead edits~~ **were edited 2026-08-12 ~18:05 and ~19:25; the obsolete pre-r17 `RP6-11` classification is gone.**` | The requested edits were made. |

## 4.2 `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_COUNT_SECOND_RECHECK_GLM_2026-08-12.md`

*Also prereg-package audit **F5** — see the dedup table §6.*

| # | Line | Exact stale text | Proposed replacement | Justification |
|---|---|---|---|---|
| **B2.1** | `:38` | `**Live defect — `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:139`:** still reads *"Freeze-relevant D026 result: **one open current-audit finding** remains (`RP6-11`)"* …` | `**~~Live defect~~ RESOLVED defect (fixed 2026-08-12 ~19:25) — `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:139`:** at the time of this recheck it still read *"…one open current-audit finding remains (`RP6-11`)"*. **It no longer does**: that sentence is now struck through and corrected to ZERO open, with the correction annotated in place. This entry is retained as the record of the catch. …` | The word "Live" is the defect: the finding was correct and is now closed, but nothing in the document says so. |
| **B2.2** | `:47` | `**(b)** Fix **map line 139** — replace the stale "one open … remains (RP6-11)" with the corrected 0-open statement (one-line Lead edit; T2 doc, no trading/parity/host surface).` | `**(b)** ~~Fix **map line 139**…~~ **DONE 2026-08-12 ~19:25** — map line 139 now carries the corrected 0-open statement with an in-place correction note. Retained as the record of the recommendation that was adopted.` | A proposed action that was carried out, still written in the imperative. |

*Not in scope for this plan: item 2 at `:39` (blocker-map `:64-65` "stale 28/11 sits prominently")
is explicitly labelled "Minor … Internally consistent as history" by its own author, and the
incomplete-correction sweep independently classifies blocker-map `:63-67` as **CURRENT (history)**.
It is listed in Part C as leave-alone.*

## 4.3 `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SUMMARY_VS_DETAIL_CONSISTENCY_SWEEP_2026-08-12.md`

| # | Line | Exact stale text | Proposed replacement | Justification |
|---|---|---|---|---|
| **B3.1** | `:27` | `Single most consequential inconsistency: `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` simultaneously says D026 current-audit open findings are zero and that one open finding remains (`RP6-11`). An auditor reading only the stale line could believe the already-closed RP6-11 finding is still a freeze-relevant open item.` | `Single most consequential inconsistency **(RESOLVED 2026-08-12 ~19:25 — see INT-01)**: `AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` *simultaneously said* D026 current-audit open findings are zero and that one open finding remains (`RP6-11`). **The map has since been corrected and no longer says both.** Retained as the record of the catch.` | The headline finding of the sweep, still in the present tense against a repaired target. |
| **B3.2** | `:31-46` (finding INT-01 / XFILE-01, whole block) | Heading `### INT-01 / XFILE-01 - D026 map still says one open finding remains`, plus `Type: stale; incomplete supersession/strikethrough.`, the "Stale reading" at `:36`, and `Line 139 is the stale surviving old value.` at `:44` | Retitle to `### INT-01 / XFILE-01 — [RESOLVED 2026-08-12 ~19:25] D026 map said one open finding remains`; change `Type:` to `Type: stale; incomplete supersession/strikethrough. **Status: CLOSED — the map line was corrected after this sweep.**`; change `:36` `says:` → `said, at the time of this sweep:`; change `:44` `Line 139 is the stale surviving old value.` → `Line 139 **was** the stale surviving old value; it is now struck through in place and corrected to ZERO open.` Leave the "Correct readings" list at `:38-42` unchanged — it was and remains accurate. | The whole finding block reads as live. Retitling plus tense correction preserves the finding and its provenance while removing the false current-state claim. |
| **B3.3** | `:65` | `Correct reading: the recheck was accurate when it found the defect, but its "map still needs edits" conclusion is stale after the later map repair. The only surviving map defect is line 139, not the row or 29/10 counts.` | `Correct reading: the recheck was accurate when it found the defect, but its "map still needs edits" conclusion is stale after the later map repair. ~~The only surviving map defect is line 139~~ — **line 139 was itself corrected 2026-08-12 ~19:25; no map defect from this class now survives**, and the row and 29/10 counts were never defective.` | The last surviving map defect this line names has since been repaired, so the sentence now overstates what remains. |

## 4.4 `MTC_COMMAND_CENTER/11_TRIAGE/LEDGER_RP6_CLAIMS_GLM_CROSSCHECK_2026-08-12.md`

**B4.1 — `:18`** *(class B)*

Exact stale text:

```text
**The one genuine defect — stale citation (NIT).** The ledger cites `STATUS_RP6_P0.md:311-312`, but that line no longer holds the claim — round 17 + the Lead's status correction shifted it. The claim is now at `:396-397` (recurs ~9×; count field at `:274`). Claim content true; line number stale — exactly the drift the kickoff flagged as likely. Optional fix: repoint to `:396-397`.
```

Proposed replacement:

```text
**The one genuine defect — stale citation (NIT). [RESOLVED 2026-08-12 ~17:55.]** At the time of this crosscheck the ledger cited `STATUS_RP6_P0.md:311-312`, which no longer held the claim — round 17 + the Lead's status correction shifted it. The claim is at `:396-397` (recurs ~9×; count field at `:274`). Claim content true; line number stale — exactly the drift the kickoff flagged as likely. ~~Optional fix: repoint to `:396-397`.~~ **The repoint was applied: `WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:88` now cites `:396-397` with `:274` as the count field, and annotates the former `:311-312` citation in place.** Retained as the record of the catch.
```

Justification: the recommended fix was applied; the finding is left standing as a live defect.

## 4.5 `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_LEDGER_GLM_CROSSCHECK_2026-08-12.md`

Same root cause as B4.1, three occurrences in one document. A document-level banner is proposed
plus three in-place markers, because this file states the finding in its abstract, its body, and
its verdict table — a single banner would leave two of the three reading as live.

Proposed **banner** after the title:

```text
> **One finding in this crosscheck is RESOLVED (2026-08-12 ~17:55).** Its "one genuine defect",
> the stale `STATUS_RP6_P0.md:311-312` citation, was repointed to `:396-397` in
> `WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:88`. Every other conclusion here — the 17-definitions /
> 27-occurrences reconciliation, the r16 source-vs-host acceptance characterization, and the
> consumer line citations — is CURRENT and unaffected.
```

| # | Line | Exact stale text | Proposed replacement | Justification |
|---|---|---|---|---|
| **B5.1** | `:19-21` | `The one genuine defect is a **stale line citation** (`STATUS_RP6_P0.md:311-312`), which the kickoff explicitly anticipated (…).` | `The one genuine defect **[since RESOLVED — repointed 2026-08-12 ~17:55]** was a **stale line citation** (`STATUS_RP6_P0.md:311-312`), which the kickoff explicitly anticipated (…).` | Abstract-level statement, present tense, target repaired. |
| **B5.2** | `:139-148` | `The ledger (line 88) cites `STATUS_RP6_P0.md:311-312` … **Claim content: true and present. Cited line number: stale.** … Recommended fix (optional, low): repoint the citation to `STATUS_RP6_P0.md:396-397` (or `:274` for the count).` | Prefix the section body with `**[RESOLVED 2026-08-12 ~17:55 — the recommended repoint was applied. Retained as the record of the catch.]** ` ; change `The ledger (line 88) cites` → `At the time of this crosscheck the ledger (line 88) cited` ; strike the final sentence: `~~Recommended fix (optional, low): repoint the citation to `STATUS_RP6_P0.md:396-397` (or `:274` for the count).~~ **Applied — `:88` now cites `:396-397`, count field `:274`.**` | Body section states the defect and requests a fix that was carried out. The verified recurrence list at `:142-144` is accurate and stays. |
| **B5.3** | `:207` | `\| `STATUS_RP6_P0.md:311-312` citation \| **STALE** (now at `:396-397` + recurs; `:274` for count) — the one defect, anticipated by the kickoff \|` | `\| `STATUS_RP6_P0.md:311-312` citation \| ~~**STALE**~~ **RESOLVED 2026-08-12 ~17:55** — repointed to `:396-397` (`:274` for count) in `WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:88`; was the one defect, anticipated by the kickoff \|` | Verdict-table rows are read standalone; `STALE` there reads as current status. |

## 4.6 `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md`

**B6.1 — `:12`** *(class B)*

Exact stale text (the "Most consequential finding" paragraph, stale portion):

```text
**Most consequential finding (stale):** `STATUS_TRANSPORT.md` does not reflect the round-6 Codex audit cycle. … The header still reads `REPAIRED-PENDING-REAUDIT` and the body never mentions it — the status was edited 2026-08-12 (owner ratification) without incorporating the audit.
```

Proposed replacement:

```text
**Most consequential finding (stale) — [RESOLVED 2026-08-12 ~18:20]:** at the time of this sweep, `STATUS_TRANSPORT.md` did not reflect the round-6 Codex audit cycle. … The header **then** read `REPAIRED-PENDING-REAUDIT` and the body never mentioned it — the status had been edited 2026-08-12 (owner ratification) without incorporating the audit. **This sweep's finding was adopted: `STATUS_TRANSPORT.md:3-10` now reads `CODEX-FLAGSHIP-ACCEPTED — PENDING SECOND FLAGSHIP` (round 6b) and credits this sweep for the catch, and `:12-23` records the full round-6 cycle.** Retained as the record of the catch.
```

The remainder of `:12` — the on-disk `TRANSPORT_CODEX_R6_AUDIT` / `R6B_CONFIRM` evidence, the
"already repaired in the bytes" note, and the "stale (understated), not wrong" characterization —
is accurate and stays.

Justification: this finding was acted on within two hours and the target file explicitly credits
it, yet the sweep still describes the pre-fix state in the present tense. Also note `:14` of this
same file carries the correct 17/27 reconciliation and is **CURRENT** — do not touch it.

---

# PART C — LEAVE ALONE

Contract items 4 and 10. Editing anything in this part destroys deliberately retained provenance
or re-opens a closed correction. **No entry here is to be modified by the application pass.**

## 5.1 Already-corrected in place (strikethrough + dated correction present)

| ID | File:line | Why leave alone |
|---|---|---|
| **C-1** | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:14` | The incomplete-correction sweep's "most consequential" hit. Already fixed: `~~SEC102 round 9 and its Codex audit are pending;~~` is struck and replaced with the ACCEPTED-WITH-DISCLOSURE / blocker-#4-CLEARED statement plus a dated correction note. |
| **C-2** | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_RED_LOCATIONS.md:46` | Already fixed: the r9/GREEN/Codex/GLM-pending sentence is struck through and marked **CORRECTED 2026-08-12 ~19:40 — all four are DONE**, with sources. |
| **C-3** | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:190-192` | The SEC102 clause is already struck and corrected in place. **Only the D026/freeze-input portion at `:193-195` is stale (A3.3).** The application pass must edit `:193-195` without disturbing `:190-192`. |
| **C-4** | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:90-109` | The blocker-8 analysis. `:92-101` is an explicit **SUPERSEDED 2026-08-12 ~19:40 — read this first** banner; `:103-109` is the analysis it expressly retains "as the record of how the reclassification was reached". *(Contract item 8 names `:92-116`; current bytes place the superseded block at `:90-109` — `:111-122` is Blocker 9, which is a separate, current, actionable item and is not covered by the banner. Range narrowed accordingly.)* |
| **C-5** | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:144` | The blocker-8 summary bullet, already struck through and marked `**[corrected 2026-08-12 ~19:40]** … RECLASSIFIED, not open as a contract contradiction`, with the original wording retained as history. *(Contract item 8 names `:143`; current bytes place this at `:144` — `:143` is the Blocker 7 bullet, which is current and correct. Pointer corrected.)* |
| **C-6** | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:88` | The `STATUS_RP6_P0.md:396-397` citation with its bolded in-place note that it read `:311-312` when written. This is the corrected target of B4.1/B5.x. |
| **C-7** | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md:31` (row-correction annotation), `:131`, `:134-136`, `:139` | The `~~28~~ → 29`, `~~11~~ → 10`, `~~1~~ → RESOLVED`, and the `:139` `~~one open~~ → ZERO` corrections, each with a dated in-place note. These are the repairs the Part-B derivatives were catching. *(A1.3/A1.4 touch only the `r17_literal_zero_measurements` fragments at `:31`, `:159-160` and `:173` — not these count corrections.)* |
| **C-8** | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/RUNID_MINTING_REVIEW_CODEX_2026-08-11.md:167` | Old two-arg / rc-1-FAIL text already struck through and corrected in both respects. This is what made blocker 8's contradiction disappear. |
| **C-9** | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md:3-25` | The corrected header plus the italic correction note and the newly-recorded round-6 cycle. Target of B6.1. |
| **C-10** | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_HANDOFF_PACKAGE.md:29-30` | The struck `~~15 of 20 … 5 remain open~~` headline, superseded in place by `:32-39`. |

## 5.2 CURRENT (history) — labelled history, time-bounded, or unchosen alternative

Named by the incomplete-correction sweep; grouped by file.

| ID | File:line | Kind |
|---|---|---|
| **C-11** | `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:63-67`, `:153-157` | 28/11 expressly "**as first written**" and "**superseded**", with 29/10/15/0 identified as current. Also the "minor" item at `AUDIT2_D026_COUNT_SECOND_RECHECK_GLM_2026-08-12.md:39` — its own author calls it internally consistent as history. |
| **C-12** | `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:85`, `:153-154`, `:159-160`, `:161-165`, `:166-168`, `:20`, `:107-117` | Corrected r17 attribution, ledger-citation drift recorded as record-quality history, transport defect history, the correct 17/27 reconciliation, and the item-8 reclassification. **Only `:96`, `:99-100` and `:103-104` of this file are stale (A1.5, A2.4, A5.2).** |
| **C-13** | `KICKOFF_CODEX_D026_MAP_COUNT_REDERIVE.md:13-16,31` | Records the pre-recheck input and explicitly says r17 made open=0. |
| **C-14** | `WPI_BLOCKS_DRAFT/KICKOFF_CODEX_RP6_CENSUS_R17.md:3` | Intended dispatch identity in a frozen kickoff, not a claim about the executed run header. |
| **C-15** | `WPI_BLOCKS_DRAFT/KICKOFF_GLM_ADVANCE_RP6_READ_AUDIT.md:26-27`, `WPI_BLOCKS_DRAFT/RP6_GLM_ADVANCE_READ_AUDIT_2026-08-12.md:5-13` | Pre-r17 audit input and result; not claims about the post-r17 state. |
| **C-16** | `FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md:198-209` **at `6078ddb4`** | Explicitly time-bounded to "IN FLIGHT at handoff time (2026-08-12 ~17:45)", before the 17/27 reconciliation landed. *(Cited as the source sweep cited it, at the named anchor. Commits inside `6078ddb4..4e012466` re-touched this file, and later commits can shift the block again; **no current-tree line number is claimed here.** This is a leave-alone entry, so nothing is applied to it — a reader who needs to locate the block must re-read it at the anchor and re-verify.)* |
| **C-17** | `KICKOFF_GLM_CROSSCHECK_LEDGER_RP6_CLAIMS.md:31,39` | The question sent for resolution, not a surviving conclusion. |
| **C-18** | `WPI_GITATTRIBUTES_DURABILITY_ANALYSIS_2026-08-12.md:5,12,49,68` | Explicitly a timestamped working-tree snapshot during the concurrent r17 change; accurately records a transient mismatch. |
| **C-19** | `WPI_PREREG_DRAFT_ROUND1/SEC102_ACCEPT_WITH_DISCLOSURE_RECOMMENDATION_2026-08-12.md:100-101` | **Unchosen alternative** — Option 3, not the current state. |
| **C-20** | `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md:5117-5119,6502-6505,6647,7978,9358`; `RP6_R15_REPORT_2026-08-11.md:283`; `RP6_R16_REPORT_2026-08-11.md:294` | Definition/input counts inside historical round sections; not raw-occurrence claims. |
| **C-21** | Every `KICKOFF_*` current-correct target value cited by the sweep: `KICKOFF_GLM_INCOMPLETE_CORRECTION_SWEEP.md:14,32-40`; `KICKOFF_CODEX_SUMMARY_VS_DETAIL_CONSISTENCY_SWEEP.md:38-40`; `KICKOFF_GLM_STATUS_VS_BYTES_SWEEP.md:28`; `KICKOFF_CODEX_PREREG_TRUSTED_BASE_CARRY_LIST.md:10` | Current-correct by construction. |

## 5.3 Correct records that must not be "corrected" toward the stale claim

| ID | File:line | Why |
|---|---|---|
| **C-22** | `WPI_SELFQA_CLAIM_AUDIT_RP6_2026-08-12.md:65-71` | Already states the F1 defect correctly and in full ("assign … as literals, then print the literal … No count or comparison computes any of the three values"). This is the *finding*, not a stale claim. |
| **C-23** | `WPI_BLOCKS_DRAFT/KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md:60,108-121` | Already poses the open question correctly (`r17_literal_zero_measurements=0` "is itself a" literal; "**`r16_lines=3` and `r17_literal_zero_measurements=0` are literals**"). The pending second-flagship audit depends on this framing surviving intact. |
| **C-24** | `SELF_QA_RP6.md:13290-13302`, `:13460-13461` | The genuine `dynamic_targets` computation and the RED/GREEN pair. The §3.1 corrections must preserve these, not weaken them. |
| **C-25** | `WPI_SUMMARY_VS_DETAIL_CONSISTENCY_SWEEP_2026-08-12.md:38-42`, `:159-165`, `:167-180`, `:204`; `WPI_STATUS_VS_BYTES_SWEEP_GLM_2026-08-12.md:8,10,14` | Correct current readings inside files that also carry Part-B hits. The B-markers must be surgical. |

---

# PART D — Deduplication map

Contract item 3. Overlaps are resolved to a single remediation entry; separately stale
occurrences of the same fact are **kept separate**, because each is independently readable.

| Fact | Sweep hit | Package-audit hit | Resolution |
|---|---|---|---|
| Map line 139 / RP6-11 open-count | value 1 & 2 STALE lists | **F5** (`AUDIT2_D026_COUNT_SECOND_RECHECK_GLM_2026-08-12.md:38`) | **One entry: B2.1.** F5 and the sweep name the identical line. |
| RP6-11 derivative staleness | value 2 STALE list explicitly cross-references its value-1 entries | — | **No new entries.** Value 2 adds no line not already in B1.4/B1.5/B1.6, B2.1/B2.2, B3.1/B3.2/B3.3. |
| R17 literal-zero class | — | **F1** (4 cited sites) | **A1.1–A1.4** — 4 contracted entries / 5 sites (A1.4 has two sub-hits) — plus the **non-contracted** addendum **A1.5** (1 entry / 2 further sites found in inspection). Each is a distinct document making the claim to a distinct audience → kept separate. |
| SEC102 stale status | value 9 STALE list (3 hits) | **F3** (2 hits) | All overlap. `AUDIT2_FREEZE_PREREQUISITES.md:14` → **C-1**; `AUDIT2_D026_RED_LOCATIONS.md:46` → **C-2**; `AUDIT2_HANDOFF_PACKAGE.md:190-192` → **C-3** (all already corrected). Only the non-SEC102 remainder of F3 survives as **A3.3**. |
| Packet 7/8 detail vs headline | — | **F2** | **A3.1, A3.2.** Two separate sections → two entries. |
| Current D026 map absent | — | **F4** | **A4.1.** |
| Blocker-8 CONTRADICTED | value 8 STALE list (8 hits) | — | **Four of the eight are already labelled history** — `WPI_FREEZE_INPUT_LEDGER_2026-08-12.md:90`, `:96`, `:98`, `:133`, mapped to **C-4** and **C-5**. **The other four are actionable:** ledger `:80` → **A2.1**; ledger `:126` (now `:137` in the authoring tree) → **A2.2** (with `:134` added for conservation); `AUDIT2_HANDOFF_PACKAGE.md:24` → **A2.3**; `WPI_FREEZE_BLOCKER_MAP_2026-08-12.md:99-100` → **A2.4**. 4 + 4 = 8; no hit is dropped and none is counted twice. |
| 17 vs 27 | value 5 STALE list (2 hits) | — | **A5.1, A5.2.** `AUDIT2_HANDOFF_PACKAGE.md:24` carries **both** A2.3 (tally) and A5.1 (17/27) — two distinct stale facts on one line, applied in one edit. |
| Ledger citation `:311-312` | value 4 STALE list (4 hits across 2 files) | — | **B4.1** (1 hit) + **B5.1/B5.2/B5.3** (3 hits). Kept separate: abstract, body and verdict table are each read standalone. |
| Transport status | value 7 STALE list (1 hit) | — | **B6.1.** |

**Sweep hits deliberately not carried forward as new work:** value 3 (r17 implementer attribution)
and value 6 (`SELF_QA_RP6.md` identity) are recorded **STALE: none** by the sweep itself. Nothing
is dropped silently.

---

# PART E — Application notes and self-QA

## 6.1 Ordering constraints for the (separately authorized) application pass

1. **A1.x must not be applied ahead of §3.1.3.** The hedged prose in A1.1–A1.5 is safe to apply
   immediately *because it publishes no number*. Any variant that states a value for IND-1/IND-2
   must wait for the measured rerun.
2. **A2.1 → A2.2 → {A2.3, A2.4} in that order.** The tally must not propagate before the row it
   summarizes is reclassified, or an intermediate state publishes a table that sums to 44.
3. **A3.3 and C-3 share a paragraph.** `:190-192` (corrected SEC102) must survive the `:193-195`
   edit byte-for-byte.
4. **A5.1 and A2.3 share line `:24`.** Apply as one edit to avoid a partial line.
5. **§3.1.3 changes `SELF_QA_RP6.md` bytes.** Every document pinning `1038848 B` / `07cf843d…`
   must be re-pinned in the same pass, and the r17 bytes still have no independent audit.
6. **Part B is additive only.** No Part-B entry deletes a finding; every one adds a marker.

## 6.2 Self-QA against the contract

| Check | Result |
|---|---|
| No path created other than the whitelist | **PASS** — `MTC_COMMAND_CENTER/11_TRIAGE/WPI_STALE_REMEDIATION_PLAN_2026-08-12.md` is the only file created. No other file read, opened or edited in write mode. |
| No Git mutation, no host, no network, no tests/backtests | **PASS** — read-only inspection (`git rev-parse`, `git log`, `git status`) only. |
| Both audits read completely | **PASS** — 167/167 and 507/507 lines. |
| Every remaining hit represented exactly once | **PASS** — **14 CONTRACTED class-A entries covering 16 cited sites** (A1.1–A1.4 = 4 entries / 5 sites, A1.4 carrying two sub-hits; A2.1–A2.4 = 4 entries / 5 sites, A2.2 carrying `:134` and `:137`; A3.1–A3.3 = 3/3; A4.1 = 1/1; A5.1–A5.2 = 2/2), **plus the optional A1.5 addendum = 1 entry / 2 extra sites**, giving **Part A a total of 15 entries across 18 sites**. A1.5 is explicitly **non-contracted** and is offered for separate accept/reject. **15 class-B entries**, 25 class-C leave-alone groups. Overlaps resolved in Part D; no hit appears in two remediation entries. |
| Line references verified against bytes at the `6078ddb4` anchor | **PASS** — every cited line read directly. Four drifts found and disclosed: contract `:158-173` vs audit `:160-173`, with the stale sentence spanning `:159-160` (A1.4); ledger `:92-116`→`:90-109` (C-4); ledger `:143`→`:144` (C-5); ledger tally `:137` requires `:134` (A2.2). Also noted: the count-recheck's own citations `:131-137` have drifted to `:133-139` (B-banner §4.1). **C-16 is cited only at the anchor (`FRESH_SESSION_HANDOFF_2026-08-13_MORNING.md:198-209` at `6078ddb4`); no current-tree line is claimed for it, since later commits can shift that leave-alone history block.** Verification is bounded by the disclosure in §1: class-A/B line numbers are anchored at `6078ddb4`, not at an arbitrary later HEAD. |
| History markers distinguished from staleness | **PASS** — Part C is the explicit leave-alone set; Part B is history-marking, not correction; Part A is correction. |
| Indeterminate values flagged, not invented | **PASS** — IND-1 and IND-2 in §2; no number published for either; both definitional forks stated. |
| Narrower supported fact preserved | **PASS** — the `dynamic_targets` computation (`SELF_QA_RP6.md:13290-13302`) and its RED/GREEN pair (`:13460-13461`) are affirmatively restated in A1.1–A1.4 and protected in C-24. |
| Repo-relative paths, directly applicable | **PASS** — all paths repo-relative; every class-A/B entry gives exact file:line anchored at `6078ddb4`, exact stale text, exact proposed replacement, and a one-line justification. |
| Acceptance not claimed | **PASS** — see the header. Acceptance is the Codex Lead's. |

## 6.3 Coverage honesty statement

This plan covers the two named audits and nothing else. It does **not** claim the repository is
free of staleness outside their scope: the sweep covered 148 Git-derived tracked paths changed
2026-08-12, and the claim audit covered 26 named documents. Untracked run logs and scratch paths
were not treated as records, consistent with the sweep's stated rule. Two sites (A1.5) were found
during inspection that neither audit enumerated — they are flagged as additions rather than folded
in silently, so the Lead can accept or reject them separately from the contracted set. Their
existence is weak evidence that the F1 propagation set was not exhaustively enumerated; a targeted
re-grep at application time is advisable.
