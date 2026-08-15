# RP7 and Bridge suite optional-nits backlog

**Planning/backlog only. None of the ten items below is a required repair. This record authorizes no change to any accepted byte, no operational action, and no gate or acceptance decision.** RP7's Lead record classifies all six Claude findings as optional backlog and says that changing the accepted bytes would reopen T0 (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:65-71`). The Bridge-suite Lead record likewise classifies all four findings as backlog rather than repairs and says that changing the audited bytes would reopen T1 (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:46-49`).

**Estimate status for every item: `NO SOURCED ESTIMATE`.** The permitted evidence supplies no disjoint hour range for these nits; the work catalogue defines `NO SOURCED ESTIMATE` as the required label when work is defined but no disjoint row price is sourced (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:31-36`). What would settle an estimate: an owner-authorized scope identifying whether the target is a successor record or accepted historical bytes, followed by a timed edit-and-review plan for that exact scope.

## RP7 accepted-candidate nits

The subject is candidate `80cbed461d0b0371e6eabbfff0e732e5001affaf`, whose four accepted artifacts and exact identities are frozen in the acceptance record (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:9-20`).

### RP7-NIT-1 — unqualified terminal counts

**Exact finding in Claude's words:**

> **NIT-1 - unqualified terminal counts.** `D026_SUMMARY ... red_green_pairs=43
> controls=12` still carries no "single-subject" qualifier, although the fence
> body (`SELF_QA_RP7.md:926`) and the report both state plainly that a
> single-subject RED "is only a fixture the already-fixed code rejects". A reader
> of the terminal line alone would over-read it. This is the prior round's NIT-2,
> unchanged; the multi-subject counters beside it are the ones carrying real
> falsification weight.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md:488-494`.

- **Applies to:** `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:1342-1347` (the fence's count checks and terminal `D026_SUMMARY`) and its frozen transcript at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:1602`.
- **Tier reopened by a byte fix:** **T0** (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:65-71`).
- **Still applicable:** **YES.** The accepted terminal format still prints `red_green_pairs` and `controls` without a `single_subject` label, while the preceding assertion names `scope=single_subject` (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:1345-1347`).
- **Suggested disposition:** **Fold into the next authorized touch of the RP7 fence/evidence surface.** Do not open a standalone T0 cycle for wording-only clarification.

### RP7-NIT-2 — oracle identity absent from canonical output

**Exact finding in Claude's words:**

> **NIT-2 - the published transcript no longer names the oracle.**
> `%SYSTEMD_ANALYZE%` and `%SYSTEMD_VERSION%` are canonicalised, so the published
> bytes record only `major_minimum=259 major_ok=yes`. That is the deliberate cost
> of host-independent determinism and is within the R3 contract, the real values
> are retained in run-owned raw evidence, and the prose names
> `systemd 259 (259.5-0ubuntu3)` - but the transcript alone cannot answer "which
> manager answered". Adding a canonical major-version token (e.g.
> `oracle_major=259`) would restore that without reintroducing per-host variance.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md:495-502`.

- **Applies to:** the canonical-map and publication logic in `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:247-262`, especially the `%SYSTEMD_ANALYZE%` and `%SYSTEMD_VERSION%` substitutions.
- **Tier reopened by a byte fix:** **T0** (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:65-71`).
- **Still applicable:** **YES.** The accepted canonicalizer still replaces the tool and version values with presentation tokens and emits only substitution counts (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:247-262`).
- **Suggested disposition:** **Fold into the next authorized touch of the RP7 canonical-output contract.** Any addition must preserve the accepted determinism contract and receive the tier required for the changed bytes.

### RP7-NIT-3 — asymmetric line adjudication

**Exact finding in Claude's words:**

> **NIT-3 - asymmetric line adjudication.** `subject_case` compares the terminal
> line by exact string equality; `run_case` uses `grep -F -m1` over the whole
> stdout, so a matching line anywhere satisfies it. Exact rc equality is still
> required, so the risk is small, but the two halves of the fence hold different
> standards for the same kind of assertion.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md:503-507`.

- **Applies to:** `run_case` at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:541-553` and `subject_case` at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:1157-1162`.
- **Tier reopened by a byte fix:** **T0** (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:65-71`).
- **Still applicable:** **YES.** `run_case` still accepts the first fixed-string match anywhere in stdout, while `subject_case` still compares the last line exactly (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:549-553`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:1157-1162`).
- **Suggested disposition:** **Fold into the next authorized touch of the RP7 fence.** Align the two assertion forms only when that surface is already legitimately reopened.

### RP7-NIT-4 — implementer-run attribution ambiguity

**Exact finding in Claude's words:**

> **NIT-4 - whose two runs.** `STATUS_RP7.md`'s documentary bullet reports scratch
> roots `...MxAGFJ3F` / `...CXTNsYx4` and mount digests `0ba118d4...` /
> `90021811...` for "the fence was run twice back to back on this workstation"
> without saying these are the **implementer's** runs; the Lead's two retained
> runs used different roots again, and mine a third pair. The chronology table
> keeps the two roles distinct, so this is ambiguity rather than contradiction,
> but one word would remove it.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md:508-514`.

- **Applies to:** `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md:212-226`, especially the unqualified “this workstation” wording and the named roots/digests at lines 213 and 220-222.
- **Tier reopened by a byte fix:** **T0** (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:65-71`).
- **Still applicable:** **YES.** The accepted status bullet still attributes the runs only to “this workstation” and does not name the implementer (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_RP7.md:212-222`).
- **Suggested disposition:** **Fold into the next authorized touch of `STATUS_RP7.md`.** Do not reopen T0 solely to add the missing role word.

### RP7-NIT-5 — retained evidence omits the binding-record TSV

**Exact finding in Claude's words:**

> **NIT-5 - the binding record is not exported.** `RP7_RAW_EVIDENCE_DIR` retains
> `mount_projection_1/2/decoy.txt` (the summary lines) but not the
> `ro.*.mount_projection.tsv` the digest is taken over, so a reader of the
> retained evidence cannot re-check the `kind=point` binding without re-running. I
> verified the gate by falsification (§5 arm 3) and rebuilt a projection myself to
> confirm the record's shape and digest, so nothing is unproven - it is only
> unproven *from the exported evidence alone*.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md:515-521`.

- **Applies to:** the raw-evidence export in `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:264-272` and mount-projection summary/binding gate in `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:458-493`.
- **Tier reopened by a byte fix:** **T0** (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:65-71`).
- **Still applicable:** **YES.** The accepted fence writes summary files under `$ROOT/raw`, while the binding check reads the projection path returned by the evidence machinery; the export copies only `$ROOT/raw` (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:269-270`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:458-489`).
- **Suggested disposition:** **Fold into the next authorized touch of the RP7 retained-evidence contract.** Treat the exported member set and its validation as part of that future authorized scope.

### RP7-NIT-6 — conservative NUL STOP

**Exact finding in Claude's words:**

> **NIT-6 - one conservative STOP.** A fragment containing a NUL byte is parsed
> normally by systemd 259, which sees a real `[Install]`; the block STOPs
> `nul_byte` at rc 3. The direction is safe (non-accepting), the fixture is
> declared in band, and row 7's digest pin would refuse such a fragment anyway -
> but it is an inability-to-evaluate on an input the manager reads without
> difficulty.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md:522-527`.

- **Applies to:** the row-6 fragment parser's NUL branch in `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:661-667` and the corresponding fence arm in `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/SELF_QA_RP7.md:831`.
- **Tier reopened by a byte fix:** **T0** (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:65-71`).
- **Still applicable:** **YES.** The accepted parser still emits `PARSE nul_byte` and exits 3 when a NUL is present (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh:661-667`).
- **Suggested disposition:** **Close as won't-fix-with-reason:** the recorded direction is safe/non-accepting and the accepted evidence says the row-7 digest pin would refuse the fragment (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md:522-527`). Reconsider only under an explicit future scope that needs exact systemd parity for NUL-bearing fragments.

## Bridge suite-repair nits

The accepted T1 subject is repair commit `6c746b65`; its changed set is `.gitattributes`, `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`, and the repair report, with no product-code or `WPI_*` change (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:7-17`). The independent audit returned PASS-WITH-NITS with four nits and zero required findings (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:31-40`).

### SUITE-NIT-1 — stale-checkout remediation

**Exact finding in Claude's words:**

> ### NIT-1 — stale checkouts are not covered, and remediation is not documented
>
> `.gitattributes` only takes effect when a file is written to the working tree.
> The blob for `ledger_schema.json` is identical in `678d4be2` and `6c746b65`, so
> a pre-existing clone that merely fetches this commit will **not** have that file
> rewritten and will keep its CRLF working copy — and A1 will recur there. This
> affects any already-checked-out Windows copy (for example `C:\P10BASE`, or a
> developer machine), though not the Linux deploy target, which clones fresh and
> was never affected.
>
> The report does state the principle — "attributes do not retroactively rewrite
> an existing checkout" — and records that it refreshed the file here, which is
> why I am not raising this as REQUIRED. What is missing is the instruction for
> everyone else.
>
> Suggested addition: *"Existing checkouts must run
> `git checkout -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json`
> (or `git add --renormalize .`) once after taking this commit; a plain fetch will
> not fix a stale CRLF working copy."*

Source: `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:292-310` (audit artifact at commit `7d4e9a96`, identified by the Lead record at `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:9-13`).

- **Applies to:** operational intake of repair commit `6c746b65` into any pre-existing Windows checkout, and the missing instruction after the accepted repair report's attribute-refresh disclosure at `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:90-99`.
- **Tier reopened by a byte fix:** **T1** if the accepted report is edited; **no audit tier is reopened by the one-time checkout refresh itself**, because the Lead classifies that as an operational action rather than a code change (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:48-64`).
- **Still applicable:** **YES operationally until each stale checkout is refreshed.** The Lead says the issue “bites right now,” identifies `C:\P10BASE` in that state, and records the one-time command outside the accepted report (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:51-64`).
- **Suggested disposition:** **Close as won't-fix-with-reason for accepted bytes:** the Lead already recorded the operational instruction in the adjudication and morning handoff rather than patching the audited report (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:58-64`). Keep the operational reminder active wherever commit `6c746b65` is consumed; this backlog itself authorizes no checkout action.

### SUITE-NIT-2 — published A2 proof does not run the audited test

**Exact finding in Claude's words:**

> ### NIT-2 — the published A2 proof does not execute the test under audit
>
> The proof in the report builds a bundle, mutates a manifest, and then asserts
> with a hand-written copy of the comparison. It never invokes
> `test_invariants_preserve_risk_and_history`. It therefore demonstrates that the
> comparison logic is sound, not that the repaired test is discriminating — those
> are different claims, and the section heading claims the latter.
>
> The conclusion is correct: I proved discriminating power on the real test above.
> But this is precisely the "prose outran its evidence" pattern this project has
> been bitten by repeatedly, and the proof should be replaced with one that runs
> the real test. Recommend adopting the wrap-`wal.main` method used in this audit.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:312-323` (audit artifact at commit `7d4e9a96`, identified at `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:9-13`).

- **Applies to:** `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:200-206` and the hand-written comparison at lines 255-278; the accepted proof labels itself “A2 discriminating-power proof” but executes an inline assertion (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:200-206`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:255-278`).
- **Tier reopened by a byte fix:** **T1** (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:46-49`).
- **Still applicable:** **YES to the accepted report.** Its published proof still uses the inline `assert mutated_schema_version == source_schema_version`; the independent audit separately ran the real test and obtained the intended RED/GREEN (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:255-278`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:170-201`).
- **Suggested disposition:** **Fold into the next authorized touch of the suite-repair evidence surface.** Use the independent audit's real-test falsification method in a successor evidence record; do not rewrite the accepted historical report solely for this nit.

### SUITE-NIT-3 — option-3 rationale omits absolute-baseline dependency

**Exact finding in Claude's words:**

> ### NIT-3 — the A2 rationale overstates option 3 and omits its dependency
>
> The report says option 3 "tests the real contract" while rejecting option 2 as
> tautological. Option 3 still reads the expected value from the same database the
> product reads, so it cannot detect a wrong baseline. It is the right choice, but
> the honest justification is that absolute baseline coverage lives elsewhere in
> the suite (`test_order_identity.py:1567`). Recommend one sentence naming that
> test, so a future editor does not delete it without realising this test depends
> on it.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:325-333` (audit artifact at commit `7d4e9a96`, identified at `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:9-13`).

- **Applies to:** the option comparison and rationale in `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:153-163`, plus the test dependency identified by the auditor at `IBKR_PAPER_BRIDGE/tests/test_order_identity.py:1567` (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:203-218`).
- **Tier reopened by a byte fix:** **T1** (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:46-49`).
- **Still applicable:** **YES to the accepted rationale.** It still says option 3 “tests the real contract” without naming the separate absolute-baseline test (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:153-163`).
- **Suggested disposition:** **Fold into the next authorized touch of the suite-repair rationale or the dependent test documentation.** Preserve the dependency explicitly in a successor record rather than altering accepted historical bytes standalone.

### SUITE-NIT-4 — unverifiable validation claim and loose ancestry wording

**Exact finding in Claude's words:**

> ### NIT-4 — "independently validated" is unverifiable, and the ancestry phrasing is loose
>
> The claim that the rule "was previously used and independently validated in
> commit `ebb750da`" is half-verifiable: the identical rule is genuinely in that
> commit, which I confirmed. "Independently validated" cites no audit artifact and
> I could not verify it. Separately, "before it was absent from the present base"
> understates the situation — `ebb750da` is not an ancestor of HEAD at all, so the
> rule was never in this lineage. Recommend stating that plainly.

Source: `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:335-342` (audit artifact at commit `7d4e9a96`, identified at `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:9-13`).

- **Applies to:** `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:88-95`, especially “independently validated” and “absent from the present base.”
- **Tier reopened by a byte fix:** **T1** (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:46-49`).
- **Still applicable:** **YES to the accepted report.** The report still makes both challenged statements (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_REPAIR_REPORT_2026-08-15.md:88-95`), while the auditor records that `ebb750da` is not an ancestor and that no supporting audit artifact was found (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:220-226`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md:335-342`).
- **Suggested disposition:** **Fold into the next authorized touch of the suite-repair provenance/evidence surface.** State the divergent-lineage fact and cite any validation artifact that actually exists; if none exists, use `UNKNOWN` rather than repeating the claim.

## Backlog boundary

This record makes no acceptance decision. RP7 remains accepted at T0 on candidate `80cbed46` with zero required repairs (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:65-75`), and the suite repairs remain accepted at T1, not merged and not a release (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:1-3`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-72`). Any future disposition requires separate Lead/owner scope and the applicable audit workflow; this backlog supplies neither.
