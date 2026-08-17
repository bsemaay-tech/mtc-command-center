# VERDICT: REQUEST_CHANGES

TIER: **T0**. APPLIED AUDITOR CONTRACT: fresh Codex `gpt-5.6-sol`, xhigh,
Codex flagship slot. Session header model: **`gpt-5.6-sol`**. Session effort:
**xhigh**. This was a read-only audit except for this verdict file. No model or
CLI was sub-delegated. No Git mutation, network, remote-host, deployment,
backtest, broker, exchange, ARM, order, or trading action occurred.

The current r17 evidence is non-accepting. The new round-17 effect model admits
an executed dynamic variable-target surface: Bash `wait -p VAR` assigns to the
caller-selected variable, but r17 puts `wait` in the safe effect-model list and
never sends its `-p` target through `VARTARGET` / `dynamic_variable_target`.
With only the fixture identity rebound to the temporary mutant, the complete
published r17 fence returned `15/15 PASS`, `dynamic_targets=0`, while Bash
independently demonstrated that the dynamic target was mutated. This is a
required Pattern 12/13 repair and defeats the claimed closed effect model.

There are also required evidence/provenance repairs: the r17 pass-format audit
contains three uncomputed count fields (one unsupported literal-zero field),
the evidence lane still contains eleven empty transcript slots under contrary
"resolved / real captured output" claims, and the kickoff's `r10a -> r17`
byte-identity premise is false. The block is unchanged from **round 11**, not
round 10a.

## Exact identities audited

- `RP6-P0.sh`: **110817 bytes**, SHA-256
  `5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330`.
- `SELF_QA_RP6.md` (current round 17): **1038848 bytes**, SHA-256
  `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`.

Both were re-derived from current bytes before execution and match the r17
kickoff identities.

The requested historical identity claim does **not** reproduce:

```text
round 10 / commit 71a62cc8: bytes=107252 sha256=a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617
round 11 / commit 2d033fa6: bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
round 17 / commit 671d9b40: bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
current HEAD:                 bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
```

`git diff --numstat 71a62cc8 2d033fa6 -- RP6-P0.sh` reported `55 10`.
`STATUS_RP6_P0.md:1301,1356,1394` and `SELF_QA_RP6.md:6462,6541,6658,6681,7949`
also preserve the 107252-byte / `a090ae73...` round-10 identity. Therefore the
block is byte-identical **r11 -> r17**, not `r10a -> r17`. Later r11-r17 audits
do account for the current bytes, so this is a provenance/contract error rather
than evidence that the present block escaped all later review.

## Published command: verbatim result

I ran the command published at `RP6_R17_REPORT_2026-08-12.md:71` verbatim from
`WPI_BLOCKS_DRAFT`, redirecting stdout/stderr to scratch files outside the repo.
It returned outer rc 0 with zero stderr bytes. Summary lines:

```text
R17_BLOCK_IDENTITY before bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
R17_ASSERT_MET carried_r16_grammar cases=50 pass=50 fail=0 rc=0
R17_ASSERT_MET r17_dynamic_targets_measured variable_targets=113 inventory_targets=0 dynamic_targets=0 dynamic_variable_targets=0 opaque_mutators=0 effect_unmodeled=0 nonfunction_bare=10
R17_ASSERT_MET r17_bare_effect_model_closed nonfunction_bare=10 unmodeled=0
R17_ASSERT_MET r17_pass_format_audit r16_literal_zero_fields=6 r16_lines=3 r17_literal_zero_measurements=0
R17_ASSERT_MET D026_RED_WEAKENED_R16 mutant=eval rc=0 summary=PASS
R17_ASSERT_MET D026_GREEN_R17 mutant=eval refused rc=1 report=[variable_targets=113 inventory_targets=0 dynamic_targets=1 dynamic_variable_targets=0 opaque_mutators=1 effect_unmodeled=0 nonfunction_bare=10]
R17_ASSERT_MET D026_RED_WEAKENED_R16 mutant=dot_source rc=0 summary=PASS
R17_ASSERT_MET D026_GREEN_R17 mutant=dot_source refused rc=1 report=[variable_targets=113 inventory_targets=0 dynamic_targets=1 dynamic_variable_targets=0 opaque_mutators=1 effect_unmodeled=0 nonfunction_bare=10]
R17_BLOCK_IDENTITY after bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=15 fail=0 result=PASS
```

This clean run reproduces the published numbers. It does not establish that the
enumerated effect model covers every variable-target surface.

## Required finding F1 - HIGH - the effect model admits `wait -p` dynamic assignment

`SELF_QA_RP6.md:13247-13285` is an explicit enumeration of allowed non-function
bare words; `wait` is admitted at `:13272`. The variable-mutating dispatch at
`:16807-16809` covers `declare`, `typeset`, `local`, `readonly`, `export`,
`read`, `mapfile`, `readarray`, `getopts`, `unset`, and `let`, but omits `wait`.
The target parser at `:16844-16878` is consequently never called for `wait -p`.

I made one temporary subject outside the repository by inserting the following
symbolic class immediately after the existing `p0_probe_kind()` definition
anchor (`RP6-P0.sh:1566`): a guarded background child followed by
`wait -n -p "$DYNAMIC_NAME"`. I did not place a large fixture body in the repo
or this verdict. The only harness adaptation was rebinding its two declared
fixture identity constants to that temporary subject's measured identity; no
policy, parser, assertion, or expected result was changed.

The complete rebound published fence returned:

```text
MUTANT_BYTES=110906 MUTANT_SHA256=c3881ee5ab5796bdb157d26cb118cbf6ca65b39a2a07c7e65ff431443dbd8ef0
REBOUND_OUTER_RC=0 STDERR_BYTES=0
R17_ASSERT_MET block_identity_before unchanged bytes=110906 sha256=c3881ee5ab5796bdb157d26cb118cbf6ca65b39a2a07c7e65ff431443dbd8ef0
R17_ASSERT_MET carried_r16_grammar cases=50 pass=50 fail=0 rc=0
R17_ASSERT_MET r17_dynamic_targets_measured variable_targets=113 inventory_targets=0 dynamic_targets=0 dynamic_variable_targets=0 opaque_mutators=0 effect_unmodeled=0 nonfunction_bare=11
R17_ASSERT_MET r17_bare_effect_model_closed nonfunction_bare=11 unmodeled=0
R17_ASSERT_MET block_identity_after unchanged bytes=110906 sha256=c3881ee5ab5796bdb157d26cb118cbf6ca65b39a2a07c7e65ff431443dbd8ef0
R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=15 fail=0 result=PASS
WAIT_P_MUTATION target=RP6_WAIT_TARGET changed=yes numeric=yes
```

This is not a hypothetical spelling gap. Bash executed the same option class
and changed the variable named by the expanded `-p` argument, while both the
carried r16 grammar and r17's added effect layer certified the subject clean.
The r17 model is therefore another incomplete enumeration, not a closed effect
model. The minimum required repair is to disposition `wait -p` as a named-variable
target with a fail-closed option/operand grammar and add an executed RED/GREEN
pair. Because the stated property is structural, the repair must also audit the
remaining "safe" builtin list for assigning options rather than merely add the
single spelling found here.

## First-class questions

### 1. Is the correction itself correct?

**Partly.** The correction that the shipped r16 tokenizer already refuses bare
`eval`, `source`, and `.` is correct. The branch is explicit at
`SELF_QA_RP6.md:16763-16765`, and the clean verbatim run plus both published
mutants reproduce that refusal. The broader statement that no other admissible
construct can mutate through an unresolved target is false: F1 is an admitted,
executed counterexample.

### 2. Is the r17 effect model closed?

**No.** It is a hand-maintained allow-list. F1 survives both layers and returns
the full `15/15 PASS` after ordinary fixture-identity rebinding. An admissible
bare word therefore slips between the safe-word enumeration and the mutating-
builtin target grammar.

### 3. Is the weakened-r16 RED honest?

**Honestly labelled but insufficient for the closure claimed.** The weakening
at `SELF_QA_RP6.md:13201-13215` removes exactly the existing three-name indirect-
execution refusal. The RED correctly proves that this explicit branch is needed
to reject the `eval` and dot-source fixtures; it does not falsely claim the
shipped r16 bytes admit them. That is a legitimate equivalent falsification for
that narrow explicit-refusal class.

It proves less than the r17 closure needs. The GREEN is produced by the carried
r16 special case at `:16763-16765`, not by demonstrating that r17's new generic
effect model catches an unenumerated assigning builtin. It therefore cannot be
closure evidence for the universal effect-model claim or for every dynamically
resolved target surface. F1 supplies the missing falsification and is RED
against the delivered r17 fence.

### 4. How many literal-zero measurement fields are there?

For the r17 pass-format audit producer itself, a dependency scan gives:

```text
r16_literal_zero_fields       source=constant assignment 6   measured=no
r16_lines                     source=direct literal 3       measured=no
r17_literal_zero_measurements source=direct literal 0       measured=no
uncomputed count fields=3
uncomputed literal-zero measurement fields=1
```

Thus `r17_literal_zero_measurements=0` is false: the truthful count of
unsupported literal-zero measurement fields in the r17 pass-format audit output
is **1**, namely that field itself. The line has two direct literals (`3` and
`0`), while the displayed `6` is indirectly sourced from another constant.

The wider r17 harness has five other literal `=0` success tokens in producer
text (`bash_n`, D026 RED `rc`, carried `fail`/`rc`, and effect-model
`unmodeled`). Each is emitted only after a real command result or measured count
is checked; they are branch-conditioned restatements, not unsupported count
measurements. The seven values in `r17_dynamic_targets_measured` are computed at
`SELF_QA_RP6.md:13290-13301`; the narrow clean-block `dynamic_targets=0` is a
real measurement. No other uncomputed r17 count field was found outside the
three-field pass-format assertion above.

The self-certifying pass-format line at `:13417-13419` is a substantive evidence
defect: it certifies its class clean while instantiating it. It invalidates the
broad pass-format audit, but not by itself the independently computed clean-block
target report. F1 independently invalidates the claimed completeness of that
target report.

## Known-defect adjudication

### Eleven unfilled transcript positions

The disclosed count reproduces exactly:

- eight in `SELF_QA_RP6.md`: `:15341`, `:15651`, `:15763`, `:15807`,
  `:18241`, `:18524`, `:18645`, `:18690`;
- one in `STATUS_RP6_P0.md:299`;
- one in `RP6_R15_REPORT_2026-08-11.md:180`; and
- one in `RP6_R16_REPORT_2026-08-11.md:277`.

These are not needed to believe that the commands have ever run: the prior
Codex r16 verdict records an independent execution of the five relevant
harnesses, and this audit reproduced current r17 plus its carried r16 grammar.
Consequently the technical r16 gate is not erased merely because the local
slots are empty.

They are nevertheless a required documentary repair on the current evidence
bytes. `SELF_QA_RP6.md:15338,15648,18238,18521` labels the empty slots "Real
captured output"; `STATUS_RP6_P0.md:294-299` makes the same claim; and the
round-15/16 prose says the placeholders were resolved. The binding evidence-
authoring rule forbids an unfilled slot under a resolved claim. Either paste the
exact independently verified output with provenance, or narrow each claim to
the external evidence record and mark the local transcript absent. Do not invent
or reconstruct output.

The prior r16 PASS-WITH-NITS was technically supportable under its explicit
external-execution contract, so its code/census conclusion is not retracted.
Its classification of the slots as optional is no longer adequate for the
current r17 evidence document under the now-explicit no-unfilled-slot rule.

### S-1 - every-fence / no-temp contradiction

**Scope-wrong, documentary; no false host-state result shown.**
`SELF_QA_RP6.md:5-7` says every later fence created no temp file, while the r17
harness itself calls `mktemp -d` and writes a temporary extracted fence and
mutants at `:13170-13227,13328-13336`. Earlier examples cited by the kickoff
also reproduce. The scratch state is real and is part of harness operation, but
it is locally created and removed; no accepted predicate depends on pretending
it does not exist. Narrow the opening sentence to its original fences or state
the later scratch contract accurately.

### U-4 - whole-session negatives

**Author attestations, not transcript-proved facts.** The cited output proves
the displayed commands' results, not a complete historical command log, network
log, or write set. These negatives do not establish the census property and are
not shown false, but they must be labelled attestations unless linked to an
independent provenance record. This audit's own delta gate below applies only to
this audit session and cannot retroactively prove earlier sessions.

## Thirteen-pattern adjudication

| Pattern | Adjudication |
|---|---|
| 1 - STOP is not a result | No new host-state rc mapping is introduced, but F1 is worse than a STOP/FAIL mix-up: the analyzer reports clean coverage for an effect it did not model. |
| 2 - Whose kernel answered? | No host or namespace admission was executed. Not implicated. |
| 3 - The leaf is not the path | No path-admission byte changed. Not implicated. |
| 4 - Privileged child environment | The published run is local and unprivileged. Scratch files exist, contrary to the opening prose, but no privileged child was introduced. |
| 5 - grep is not a parser | Grep is present, but F1 is primarily a missing shell-effect grammar case, owned by Pattern 12. |
| 6 - Read status before stdout | The verbatim and falsification runs captured rc and stderr before adjudication. No new read-order defect found. |
| 7 - Nonzero read is not EOF | No reader-completion finding in r17. |
| 8 - The name is not the identity | Current byte identities are exact. The r10a provenance claim is false, but that is a claim-scope error rather than resolver-name substitution. |
| 9 - The sentence outruns the probe | **FAIL.** "Closed effect model," `r17_literal_zero_measurements=0`, resolved-transcript claims, the every-fence/no-temp sentence, and `r10a -> r17` identity all outrun their evidence. |
| 10 - Evidence that cannot fail | **FAIL.** The pass-format assertion has no computation; the eval/dot RED does not falsify the generic safe-builtin enumeration; eleven transcript slots are empty under captured-output claims. |
| 11 - Declared instrument is not executed instrument | The published r17 command was executed verbatim. No separate instrument-binding finding. |
| 12 - Unmodeled must not disappear | **FAIL (required F1).** `wait -p` is an unmodeled assigning form that disappears into the safe allow-list and produces `effect_unmodeled=0`. |
| 13 - Every admitted member needs a terminal disposition | **FAIL (required F1).** The `-p` target reaches no `VARTARGET`, `dynamic_variable_target`, opaque-mutator, or effect-unmodeled disposition. |

## Minimum required repairs

1. Make `wait -p` and every other assigning option reachable from the admitted
   builtin set enter a fail-closed target grammar; add a D026 RED against these
   delivered r17 bytes (or an equivalent deliberate mutation) and GREEN after
   repair, with real commands and summary output.
2. Replace `SELF_QA_RP6.md:13417-13419` with a real measured pass-format scan.
   Publish the derived count, not a chosen expected literal, and make the
   assertion fail when a new uncomputed result field appears.
3. Resolve the eleven transcript contradictions by pasting exact provenance-
   backed output or truthfully marking the local evidence absent and citing the
   external execution record.
4. Narrow `SELF_QA_RP6.md:5-7`, label historical whole-session negatives as
   attestations, and correct the block stability boundary from r10a to r11.

No current-r17 Codex acceptance slot is filled by this verdict. Dual flagship
acceptance is not reached.

## Delta gate

The final before/after comparison and path-scoped status confirmation are
recorded below after this sole authorized file was created. The baseline had
115 pre-existing porcelain entries; the final capture had 116. A set comparison
of the complete captures produced exactly one addition and no removal:

```text
=> ?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R17_2026-08-12.md
```

The required path-scoped confirmation was:

```text
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CODEX_T0_AUDIT_R17_2026-08-12.md
```

`git diff --name-only` was empty. Thus the before/after delta contains only this
exact verdict path; no tracked file changed and the delta gate passes.
