# VERDICT: REQUEST_CHANGES

TIER: **T0**. APPLIED AUDITOR CONTRACT: fresh independent Claude auditor, exact
model `claude-opus-5`, effort **xhigh**, default Claude Pro account. This was a
read-only audit except for this single verdict file. No model, sub-agent, or
external CLI was delegated. No Git mutation, network, remote-host, deployment,
credential, broker, exchange, ARM, order, backtest, or trading action occurred.

Round 18 settles two of the four round-17 required repairs cleanly, settles a
third only partially, and does not deliver the first one into the audited bytes.
Two executed findings block acceptance:

1. a **named-assignment class the repaired round-18 policy does not model at
   all** — assignment through *word expansion*, including a target named at run
   time — which returns the full `16/16 PASS` with every mutation counter at
   zero; and
2. the `waittarget` grammar that closes `wait -p` **is not present in the
   delivered evidence bytes**. The shipped `SELF_QA_RP6.md` policy still accepts
   the round-18 wait mutant at `16/16 PASS`.

This verdict fills **no** acceptance slot. Dual flagship acceptance is **not**
reached: a fresh independent Codex `gpt-5.6-sol` xhigh audit of these same
round-18 bytes is still required, and the r18 Codex session was the implementer,
not an auditor.

## Exact identities audited

Both re-derived from current bytes before execution:

```text
RP6-P0.sh        bytes=110817   sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
SELF_QA_RP6.md   bytes=1065504  sha256=0bbf41dd2985a587c97a992589c7576b31e92217d11ecb888b4c8b2c84b84481
```

Both match the kickoff exactly. Execution proceeded.

## Execution methodology and the real published result

I ran the published command verbatim from `WPI_BLOCKS_DRAFT`, redirecting
stdout and stderr to scratch files outside the repository.

**Disclosed deviation from the operator's foreground-only instruction.** The
published command took **5738 seconds** on this host. The available foreground
execution call is hard-capped at 600 seconds; my first verbatim foreground
attempt was killed by that cap at 600 s with SIGTERM (rc 143) after four
asserts. A 5738-second command therefore cannot complete inside one foreground
call. All runs below were executed as session-tracked local background
processes and **blocked on to completion inside the same session** — no run was
left in flight, no result was inferred, and every rc, stderr byte count, and
summary line reported here was read from the completed process's own captured
output. This is a change of call mechanics only, not of the command.

Real result of the published command:

```text
outer rc = 0
stderr bytes = 0
elapsed = 5738 s
```

```text
R18_BLOCK_IDENTITY before bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
R18_ASSERT_MET block_identity_before unchanged bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
R18_ASSERT_MET delivered_r17_selfqa_bound commit=671d9b40 bytes=1038848 sha256=07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac
R18_ASSERT_MET wait_mutant_applied bytes=110938 sha256=0e893287ad64e6f6117a13c9c864fa56288b7e0e208ab79847402fe3f9382b9b bash_n=0
R18_ASSERT_MET delivered_r17_rebind_only fields=2 normalized_bytes_unchanged=yes
R18_ASSERT_MET D026_RED_DELIVERED_R17 mutant=wait_p rc=0 summary=[R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=15 fail=0 result=PASS] target=[R17_ASSERT_MET r17_dynamic_targets_measured variable_targets=113 inventory_targets=0 dynamic_targets=0 dynamic_variable_targets=0 opaque_mutators=0 effect_unmodeled=0 nonfunction_bare=11]
R18_ASSERT_MET wait_p_bash_semantics target=P0_R18_WAIT_TARGET changed=yes numeric=yes rc=0
R18_ASSERT_MET wait_target_grammar_injected functions=1 dispatches=1
R18_ASSERT_MET r18_policy_instrumentation target_record_channel=present
R18_ASSERT_MET GREEN_CLEAN_R18_POLICY rc=0 summary=[R17_DYNAMIC_TARGETS_SUMMARY cases=16 pass=16 fail=0 result=PASS] pass_format=measured_and_falsified
R18_ASSERT_MET D026_GREEN_R18 mutant=wait_p rc=1 record=[UNMODELED kind=dynamic_variable_target:wait_p line=1567 raw=["$P0_R18_WAIT_NAME"]] summary=[R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=11 fail=4 result=FAIL]
R18_ASSERT_MET assigning_option_matrix_executed rc=1 printf_v=dynamic_target_refused read_a=option_refused wait_p_literal=target_recorded wait_unknown=option_refused wait_p_missing=target_refused
R18_ASSERT_MET effect_partition_conserved admitted=37 target_grammar=13 prefix_recursive=3 action_grammar=1 no_named_target=20
R18_ASSERT_MET assigning_option_matrix entries=3 printf_v=target_grammar wait_p=target_grammar read_a=fail_closed_unmodeled_option
R18_BLOCK_IDENTITY after bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
R18_ASSERT_MET block_identity_after unchanged bytes=110817 sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
R18_ASSIGNING_EFFECT_SUMMARY cases=14 pass=14 fail=0 result=PASS
```

Every value the implementer published reproduces. The harness does what it says
it does. The findings below are about what it does **not** measure.

Bash version on this host: `5.2.37(1)-release`.

## Required finding R1 — HIGH — assignment through word expansion is unmodeled

**Patterns 12 and 13. This is a new class, not a new spelling.**

Bash assigns named variables through *word expansion*, in **any** word position,
under command words the round-18 partition classifies as having no named target.
Executed on this host, in one `--noprofile --norc` shell:

```text
1 colon_defassign      WX_A=[alpha]     # : "${WX_A:=alpha}"
2 test_defassign       WX_B=[beta]      # test -n "${WX_B:=beta}"
3 bracket_defassign    WX_C=[gamma]     # [ -n "${WX_C:=gamma}" ]
4 type_defassign       WX_D=[echo]      # type -t "${WX_D:=echo}"
5 arith_assign         WX_E=[42]        # : "$((WX_E=42))"
6 indirect_defassign   WX_F=[delta]     # nm=WX_F; : "${!nm:=delta}"
7 indirect_arith       WX_G=[7]         # nm2=WX_G; : "$((${nm2}=7))"
8 echo_defassign       WX_H=[eps]       # echo "${WX_H:=eps}"
```

Case 6 is the decisive one: **`${!nm:=v}` assigns the variable named at run time
by `$nm`** — a dynamically-resolved assignment target, the exact property round
18 claims to have closed, reached with no builtin, no option, and no command
word outside the "no named target" class.

### Fence-level RED — executed against the *repaired* round-18 policy

I rebuilt the repaired round-18 policy using the published harness's own
plumbing verbatim (`r18_insert_after_probe`, `r18_patch_wait_policy`,
`r18_instrument_r17`, `r18_rebind_r17`), substituting only the mutant payload. I
inserted one guarded symbolic class immediately after the existing
`p0_probe_kind()` anchor (`RP6-P0.sh:1566`) carrying five word-expansion
assignments, including the indirect runtime-named form. Only the two fixture
identity constants were rebound; no policy, parser, assertion, or expected
result was changed.

```text
mutant            bytes=111018 sha256=917a15688a3aaaf7096cb2f301b466d7b333929e333e9f9cfea6fa3d1407b427 bash_n=0
bash semantics    A=alpha B=beta C=gamma D=42 E=delta runtime_named_target=P0_WEXP_E
policy rc         0
policy stderr     0 bytes
summary           R17_DYNAMIC_TARGETS_SUMMARY cases=16 pass=16 fail=0 result=PASS
target report     variable_targets=113 inventory_targets=0 dynamic_targets=0 dynamic_variable_targets=0 opaque_mutators=0 effect_unmodeled=0 nonfunction_bare=11
records naming the mutant   0
elapsed           2007 s
```

**The repaired round-18 policy certifies, at a full `16/16 PASS` with every
mutation counter at zero, a subject that performs five executed named-variable
assignments — one of them to a target named at run time.** Not one record
anywhere in the token stream mentions the mutant. This is precisely the failure
round 17 was blocked for, one class deeper.

### Why all four round-18 mechanisms miss it — source trace

| # | Mechanism | Why it cannot fire |
|---|---|---|
| 1 | `vartarget()` target grammar (`SELF_QA_RP6.md:17325`, `:17344-17346`) | Called only from `cmdword()` when the *command word* is `printf -v` or one of the eleven generic mutating builtins. A `${A:=v}` sitting in an operand of `:` / `test` / `[` never reaches it. |
| 2 | `waittarget()` (`:13236-13270`, injected) | Same dispatch, gated on `w == "wait"`. |
| 3 | 37-member effect partition (`:13690-13728`) | `r17_effect_model_probe` subtracts the 37-word model from the observed bare command words. `:`, `test`, `[`, `type`, `cd`, `echo` are all **admitted members**, so the assignment-carrying word is subtracted and `effect_unmodeled` stays 0. |
| 4 | Inventory name-misuse rule (`:13677-13684`) | `r17_inventory_target_count` scans **only** `^VARTARGET ` lines for `name=`. Word expansion emits no `VARTARGET` record, so `inventory_targets` is structurally unreachable at 0. |

The counters that were supposed to make an unmodeled effect visible —
`dynamic_targets`, `dynamic_variable_targets`, `opaque_mutators`,
`effect_unmodeled` — are each fed **only** by records that the command-word
dispatch produces. A construct that carries its effect in an operand rather than
in the command word produces no record, and therefore cannot raise any of them.
The analyzer registered one additional non-function bare word
(`nonfunction_bare` 10 → 11) and classified it as a safe member of the model.
That is the disappearance Pattern 12 names.

### A tracked-inventory variant, reported honestly

I ran the same construction against the tracked inventory variable
`P0_RO_TOOLS`, both directly and through the indirect runtime-named form. Bash
assigns it in both forms:

```text
mutant          bytes=110946 sha256=7b79040fff08c89979d02b7e78ac6fb92d561b102b6220b7d77dbcf62479832f bash_n=0
bash semantics  direct_form   P0_RO_TOOLS=[p0_inv_bad]
bash semantics  indirect_form runtime_named_target=P0_RO_TOOLS P0_RO_TOOLS=[p0_inv_bad]
policy rc       1
summary         R17_DYNAMIC_TARGETS_SUMMARY cases=15 pass=11 fail=4 result=FAIL
elapsed         1830 s
```

**This variant does not escape, and I do not claim it does.** It is refused —
but the refusal comes from a *carried lexical* assertion, not from the
assigning-effect model:

```text
R17_ASSERT_UNMET carried_r16_grammar rc=1 summary=[R16_GRAMMAR_SUMMARY cases=50 pass=49 fail=1 result=FAIL]
R17_ASSERT_UNMET r17_clean_verdict_failed rc=1 report=[variable_targets=113 inventory_targets=0 dynamic_targets=0 dynamic_variable_targets=0 opaque_mutators=0 effect_unmodeled=0 nonfunction_bare=10]
```

The effect layer reported **all zeros** and produced **zero** records naming the
mutant; one of the fifty carried R16 cases tripped on the added inventory
*text*. I did not isolate which of the fifty. The consequence is the point: the
guard that fires here is a text-count conservation check keyed to three specific
variable names, so it is defeated by any other target name — which the R1 mutant
above, using `P0_WEXP_*` names, demonstrates with a full `16/16 PASS`.

### Bounded, and not currently live in the block

Two facts that matter for the owner's decision:

- The surviving class is **finite and closable**, not an unbounded enumeration.
  Bash's assignment-capable expansions are exactly `${name=word}`,
  `${name:=word}`, their indirect `${!name…}` forms, and the arithmetic
  assignment operators (`=`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `&=`,
  `^=`, `|=`, `++`, `--`) inside `$(( ))`, `(( ))`, array subscripts, and `let`.
  The tokenizer already carries the information needed: `vartarget` reads
  per-token expansion and escape flags (`TE[p]`, `TX[p]`). The repair is a
  token-level rule — "any token whose raw text matches an assignment-capable
  expansion form gets a terminal disposition, whatever the command word" —
  applied at the token layer instead of the command-word layer.
- The current block contains **none** of these forms. Measured on
  `RP6-P0.sh`: zero `${name=…}` / `${name:=…}`, zero `${!name…}`, zero
  arithmetic-assignment expansions, zero `(( ))` command forms. So this is a gap
  in the analyzer's *guarantee*, not a live unsafe construct in the audited
  block.

## Required finding R2 — HIGH — the `wait -p` repair is not in the delivered bytes

The round-18 `waittarget` grammar exists **only** as awk `print` statements
inside the R18 harness (`SELF_QA_RP6.md:13236-13270`) that patch a *temporary
copy* of the tokenizer, in a `mktemp -d` directory destroyed by the harness's own
`trap … EXIT`. The shipped R16 grammar fence (`:16574-18766`) contains **zero**
occurrences of `waittarget`:

```text
sed -n '/^# R16_GRAMMAR_HARNESS_BEGIN$/,/^# R16_GRAMMAR_HARNESS_END$/p' SELF_QA_RP6.md | grep -c 'waittarget'
0
```

The document's own published top-level R17 command (`:13969`) defaults `QA` to
`SELF_QA_RP6.md`, so it runs the **unpatched** grammar. I executed that shipped
policy against the published wait mutant, rebinding only the two fixture
identity constants (rebind proved normalized-byte-identical):

```text
mutant                     bytes=110938 sha256=0e893287ad64e6f6117a13c9c864fa56288b7e0e208ab79847402fe3f9382b9b
matches published mutant   yes
rebind-only                yes
policy rc                  0
policy stderr              0 bytes
summary                    R17_DYNAMIC_TARGETS_SUMMARY cases=16 pass=16 fail=0 result=PASS
target report              variable_targets=113 inventory_targets=0 dynamic_targets=0 dynamic_variable_targets=0 opaque_mutators=0 effect_unmodeled=0 nonfunction_bare=11
records naming the wait target   0
elapsed                    2062 s
```

(This run omitted only `r18_instrument_r17`, whose inserted line is a
`grep … || true` that prints records; it is output-only and cannot change any
rc or assertion.)

So the answer to the kickoff's own question is: **the `waittarget` injection is
a demonstration, not a delivered acceptance layer.** It proves the repair
*would* work; it does not put the repair anywhere an independent runner will
execute it. `SELF_QA_RP6.md:13153` honestly discloses that the harness "patches
only the temporary extracted R16 tokenizer", but two higher-level claims outrun
that disclosure:

- `STATUS_RP6_P0.md:19-33` — "**F1 - closed by structural inversion**… The
  repaired policy makes the same bytes non-accepting";
- `SELF_QA_RP6.md:16527-16531` — "The round-18 harness above **supersedes** this
  claim with the 37-member conserved effect partition and the fail-closed
  `waittarget` grammar."

Neither states that the repaired grammar is absent from the shipped fence and
survives only for the lifetime of a scratch directory. Round 17's required
repair 1 was to *make* `wait -p` enter a fail-closed target grammar. On the
delivered bytes, it still does not.

## Required finding R3 — MEDIUM — the measured pass-format scan has a narrow grammar

The round-17 self-certifying constants are genuinely **gone**: `grep` for
`r16_literal_zero_fields`, `r17_literal_zero_measurements`, and
`r17_pass_format_audit` across `SELF_QA_RP6.md` returns zero hits. The
replacement derives real values — I reproduced them by running the published
matcher functions standalone against the current fence:

```text
REAL scanned_producers=28
REAL uncomputed_numeric_fields=0
```

Those are measurements, not selections, and the falsification mutant does move
the assertion 0 → 1 (`GREEN_CLEAN_R18_POLICY … pass_format=measured_and_falsified`
in the published run). Repair 2 is real work.

But the matcher's grammar is narrow, so `uncomputed_numeric_fields=0` means
"zero of the shapes this matcher can see", not "zero unsupported numeric result
fields". I built eight candidate unsupported-numeric-result shapes and ran the
**published** `r17_uncomputed_result_fields` and `r17_result_producer_count`
over them verbatim:

```text
producers_seen  = 6   (of 8 producer lines)
detected_fields = 2   (of 8 unsupported shapes)
reported: unsupported_count=0
          unsupported_count=$S2_VAR
```

| Shape | Detected |
|---|---|
| `count=0` direct numeric literal | **yes** |
| `count=$V`, `V` assigned one bare numeric literal | **yes** |
| `count=$B` where `B=$A` and `A=0` (one level deeper) | no |
| `count=$((0))` | no |
| `count=${UNSET:-0}` | no |
| `count=$V` where `V=0` is assigned twice | no |
| `printf "R17_… %s" "$V"` — double quotes, not `printf 'R17_` | no (not even counted as a producer) |
| `[ 1 -eq 1 ] && rok "…"` — any same-line prefix before the producer | no (not even counted as a producer) |

Two causes: producer recognition requires the stripped line to *begin* with
`rok "`, `rbad "`, or `printf 'R17_`; and field recognition covers only a direct
`[A-Za-z_]\w*=[0-9]+` or a `$VAR` whose backing variable was assigned exactly
once with a bare numeric literal. The two-level indirection case is the same
class the matcher was built to catch, one hop further out.

The round-17 required repair asked that the assertion "fail when a new
uncomputed result field appears". It fails for the one shape that was removed
and for one neighbour; it does not for six others. Narrow the published claim to
the grammar actually implemented, or widen the grammar.

## Nits (no repair required)

- **N1.** `SELF_QA_RP6.md:13385` emits `wait_mutant_applied … bash_n=$?` from
  inside the success branch of `if ! cmp -s … && bash -n …; then`. By then `$?`
  is the *condition's* status, so this field is structurally always `0`. It is
  harmless — the branch already requires `bash -n` to have succeeded — but it is
  a value that cannot fail, printed as if it were a measurement.
- **N2.** `RP6_R18_REPORT_2026-08-12.md:161-177` presents a `text` block under
  "Published exact command and real output" that omits two of the fourteen
  emitted asserts (`block_identity_before unchanged`,
  `block_identity_after unchanged`). The `cases=14` total is correct; the quoted
  transcript is a filtered subset presented without saying so.
- **N3.** The eleven `LOCAL_TRANSCRIPT_ABSENT` markers cite audit files by
  *line number*. Those citations are correct today (verified below) but will
  silently rot if either audit file is ever edited.

## First-class audit questions

### 1. Structural assigning-effect closure

**Not closed.** The 37-member universe is real and conserves — I re-derived it
independently from the `P0_R17_EFFECT_MODEL_EOF` heredoc: 37 raw lines, 37
unique, no duplicates, and the published partition
`13 + 3 + 1 + 20 = 37` reconciles exactly. All thirteen target-class members
(`printf`, `wait`, and the eleven generic mutating builtins) are present in the
universe. The `vartarget` option set is a genuine whitelist and is fail-closed:
an unmodeled option, an option after an operand, a missing target, and an
expanded / escaped / non-identifier target each produce an explicit `UNMODELED`
record. Prefix recursion routes correctly — `prefix_classify`
(`SELF_QA_RP6.md:17262-17286`) strips `command` / `builtin` / `exec`, fails
closed on unmodeled prefix options, and dispatch sits in `cmdword()` downstream
of the strip. The published option matrix (`printf -v`, `wait -p`, `read -a`,
bundling, missing operand, unknown option, literal vs expanded target) executes
and refuses as claimed.

The **second assignment-capable form I derived independently** is R1: word
expansion. It is admitted, executed, and reaches no terminal class. The
partition is conserved over *command words*; the property it is asked to
support is about *assignment effects*, and those are not a function of the
command word alone. Zero facts plus PASS is exactly what R1 produces.

**On the `waittarget` injection:** it is a demonstration, not an executable
acceptance layer — see R2. Tracing the actual published top-level command
(`:13969`) shows it runs the shipped, unpatched grammar.

### 2. D026 RED/GREEN honesty

**Honest and correctly constructed, for the class it covers.** Verified
explicitly, each as required by D026:

- Commit `671d9b40` yields the delivered r17 `SELF_QA_RP6.md` at exactly
  **1038848 bytes / `07cf843d5f00bef7f980017cbe01e0dc63ddb95dce5c7253d9e9a351b0d449ac`** —
  re-derived by me directly from Git, matching the kickoff.
- The RED rebind changes **only** `EXPECTED_SHA` and `EXPECTED_BYTES`: the
  harness's normalized-hash comparison proves byte-equality elsewhere, and I
  independently reproduced the same rebind-only property in my own runs
  (`SHIPPED_REBIND_ONLY=yes`).
- **RED verified:** the delivered r17 fence *accepts* the wait mutant —
  `rc=0`, `cases=15 pass=15 fail=0 result=PASS`, `dynamic_targets=0`.
- **Bash really assigns the symbolic target:** `wait_p_bash_semantics
  target=P0_R18_WAIT_TARGET changed=yes numeric=yes rc=0`.
- **GREEN verified:** the repaired policy refuses the same mutant —
  `rc=1`, `UNMODELED kind=dynamic_variable_target:wait_p line=1567
  raw=["$P0_R18_WAIT_NAME"]`, `cases=15 pass=11 fail=4 result=FAIL`.
- I rebuilt the wait mutant myself and got **byte-identical** identity to the
  published one (110938 / `0e893287…`), which cross-validates my rig against
  the implementer's.

The RED/GREEN pair is sound. Its limitation is scope, not honesty: the GREEN is
produced by a grammar that exists only in a temporary file (R2), and the pair
says nothing about R1's class.

### 3. Measured pass-format scan

Former constants confirmed gone; the scan derives rather than chooses; the
falsification does change state 0 → 1. Matcher-shaped blind spot confirmed and
quantified: **2 of 8** shapes detected, **6 of 8** producer lines recognized.
See R3.

### 4. Eleven transcript contradictions

**Honest and sufficient.** Exactly eleven markers, in exactly the required
distribution:

```text
SELF_QA_RP6.md            8   (:15865 :16177 :16293 :16338 :18780 :19065 :19190 :19236)
STATUS_RP6_P0.md          1   (:369)
RP6_R15_REPORT_2026-08-11.md  1   (:180)
RP6_R16_REPORT_2026-08-11.md  1   (:277)
```

I checked both cited external records directly. They carry real executed
summaries at the cited lines:

```text
RP6_CODEX_T0_AUDIT_R15_2026-08-12.md:146-148
  R15_GRAMMAR_SUMMARY cases=44 pass=44 fail=0 result=PASS
  R15_F1_RED_SUMMARY  cases=58 pass=58 fail=0 result=PASS
  R11_GUARDS_SUMMARY  fences=23 pass=23 fail=0 result=PASS

RP6_CODEX_T0_AUDIT_R16_2026-08-12.md:23-25
  R16_GRAMMAR_SUMMARY cases=50 pass=50 fail=0 result=PASS
  R16_F1_RED_SUMMARY  cases=52 pass=52 fail=0 result=PASS
  R11_GUARDS_SUMMARY  fences=25 pass=25 fail=0 result=PASS
```

The marker text states the local transcript is absent, names the external
record, and says no output is reconstructed. Nothing was invented. My
independent sweep of all four files found **zero** remaining empty fences and no
`@@` placeholder under a resolved claim; the surviving `PENDING` strings are in
historical round-5 sections that correctly describe themselves as pending.

On the two historical reports keeping their original prose: **this is honest and
sufficient.** The marker explicitly labels the contrary historical claim as not
local evidence (`contrary_following_claim=historical_not_local_evidence`,
`contrary_resolved_claim=historical_not_local_evidence`). Preserving a
historical document's text while flagging the specific sentence it contradicts
is the correct disposition under the no-unfilled-slot rule — the alternative,
editing history, is worse. Round-17 repair 3 is **settled**.

### 5. Claim and provenance scope

**Settled.** The opening (`SELF_QA_RP6.md:3-11`) now distinguishes the original
2026-08-10 fences from later round-specific fences that "use local temporary
directories and remove them through their published traps", and labels
whole-session no-host/network/Git negatives as **author attestations** unless an
adjacent transcript proves the narrower claim. Round-15/16/17/18 attestations are
labelled at their own sites.

Block history re-derived independently from Git:

```text
71a62cc8 (round 10)   bytes=107252  sha256=a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617
2d033fa6 (round 11)   bytes=110817  sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
671d9b40 (round 17)   bytes=110817  sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
f184139b (HEAD)       bytes=110817  sha256=5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
```

`2d033fa6` is the **last commit touching the block** in the full follow-history.
Therefore **r11 → r18** is correct and `r10a → r18` is false. Round-17 repair 4
is **settled**.

### 6. Adversarial closure and verdict

An assignment-capable class survives without a terminal disposition (R1), and a
delivered repair is missing from the audited bytes (R2). Verdict:
**REQUEST_CHANGES**.

## Thirteen-pattern adjudication

| Pattern | Adjudication |
|---|---|
| 1 — STOP is not a result | No new host-state rc mapping. But R1 repeats the r17 shape: the analyzer reports clean coverage for an effect it never modelled. |
| 2 — Whose kernel answered? | No host or namespace admission executed. Not implicated. |
| 3 — The leaf is not the path | No path-admission byte changed. Not implicated. |
| 4 — Privileged child environment | All runs local and unprivileged. Scratch use is now accurately disclosed in the opening. Not implicated. |
| 5 — grep is not a parser | **FAIL (R3).** The pass-format scan is a regex over producer lines presented as a scan of "result fields"; 6 of 8 shapes and 2 of 8 producer forms escape it. |
| 6 — Read status before stdout | rc and stderr captured before adjudication in the published run and in all four of mine. No defect. |
| 7 — Nonzero read is not EOF | No reader-completion finding. Not implicated. |
| 8 — The name is not the identity | Current byte identities exact and re-derived; r10a provenance now corrected to r11. **Settled.** |
| 9 — The sentence outruns the probe | **FAIL.** "F1 — closed by structural inversion" and "supersedes this claim … fail-closed `waittarget` grammar" (R2) outrun a grammar that is not in the delivered bytes; `uncomputed_numeric_fields=0` (R3) outruns its matcher. |
| 10 — Evidence that cannot fail | **FAIL (R1).** The repaired policy returns `16/16 PASS` with all counters zero on a subject performing five executed assignments — nothing in that measurement can register the class. N1 is a minor instance. |
| 11 — Declared instrument is not executed instrument | **FAIL (R2).** The instrument that produces GREEN is a temporary patched copy; the instrument the document publishes for execution is the unpatched shipped fence, and it accepts the mutant. |
| 12 — Unmodeled must not disappear | **FAIL (R1).** Word-expansion assignment disappears into the no-named-target class and yields `effect_unmodeled=0`, `dynamic_targets=0`, `inventory_targets=0`. |
| 13 — Every admitted member needs a terminal disposition | **FAIL (R1).** No `VARTARGET`, `dynamic_variable_target`, opaque-mutator, or effect-unmodeled disposition is reachable for an operand-carried assignment; zero records were emitted naming the mutant. |

## Rule 8 — has the accept-with-disclosure boundary been reached?

**Not yet — but this must be the last iteration on the current method.**

Rule 8 as written triggers when the property "cannot close structurally
(another class survives that the grammar cannot refuse without unbounded
enumeration)". That condition is **not** met here. The surviving class is
finite and closable: Bash's assignment-capable expansions are a small, fully
enumerable syntactic set, and the tokenizer already carries the per-token
expansion and escape flags a token-level rule would need. R2 is a delivery
defect, not a closure defect at all.

What *has* been demonstrated three rounds running is that the **method** is
wrong. r16 → r17 → r18 each closed one class by extending a command-word
enumeration, and each reopened at the next class. The repair that closes R1 is
not another enumeration entry — it is moving the effect model from the
command-word layer to the token layer, so that any token whose raw text carries
an assignment-capable expansion gets a terminal disposition regardless of which
command word it sits under. If a token-level model is built and an
assignment-capable class *still* survives, Rule 8 is reached and the honest
answer then is accept-with-disclosure.

**The owner has a genuine choice here, and it should be made explicitly.**
Accept-with-disclosure is defensible right now, because the audited block
contains none of the surviving forms — the residual is a guarantee gap in the
analyzer, not an unsafe construct in `RP6-P0.sh`. The decision belongs to the
owner, not to this audit.

## Minimum required repairs

1. **R1** — give assignment-capable word expansions a terminal disposition at
   the token layer, independent of the command word: `${name=…}`,
   `${name:=…}`, the indirect `${!name…}` forms, and arithmetic assignment
   operators inside `$(( ))`, `(( ))`, array subscripts, and `let`. Add an
   executed D026 RED against these delivered round-18 bytes and a GREEN after
   repair. The RED must include the indirect runtime-named form.
2. **R2** — put the `waittarget` grammar into the shipped R16 fence in
   `SELF_QA_RP6.md` so the document's own published R17 command refuses the
   wait mutant, and re-run. Until then, correct `STATUS_RP6_P0.md:19-33` and
   `SELF_QA_RP6.md:16527-16531`, which claim a closure the delivered bytes do
   not have.
3. **R3** — either widen the pass-format matcher (producer recognition beyond a
   line-initial `rok "` / `rbad "` / `printf 'R17_`; field recognition beyond a
   single-assignment bare numeric literal) or narrow the published claim to the
   grammar actually implemented.

## What round 18 did settle

Stated plainly so the next round does not redo it: **repair 3 (eleven transcript
contradictions) and repair 4 (claim scope, attestation labelling, r11→r18
provenance) are settled and verified.** Repair 2 is real measured work with a
real falsification, limited by R3. Repair 1 is correctly designed and correctly
demonstrated, but not delivered into the audited bytes.

## Scope, delegation, and acceptance status

Read-only except this file. No sub-delegation. No Git mutation. The block
`RP6-P0.sh` was read and hashed, never written; its identity is unchanged before
and after every run above.

**This verdict fills the fresh Claude T0 auditor slot on the round-18 bytes with
a non-accepting result. It is not dual flagship acceptance.** A fresh
independent Codex `gpt-5.6-sol` xhigh audit of the same round-18 identity
remains required, and the round-18 Codex session was the implementer — its
self-QA is not an independent Codex audit.

## Delta gate

Path-scoped delta gate governs; the whole-status delta is advisory with
attribution, per the operator's instruction.

Baseline captured before execution: **175** porcelain entries
(`git status --porcelain=v1 --untracked-files=all`).

Final capture after the audit and after writing this file: **176** entries. A
set comparison of the complete before/after captures produced exactly **one
addition and no removal**:

```text
=> ?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md
```

Required path-scoped status for that exact file:

```text
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP6_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md
```

Supporting confirmations:

```text
git status --porcelain=v1 -- …/RP6-P0.sh            (empty — block unwritten)
git diff --name-only -- …/WPI_BLOCKS_DRAFT          (empty — no tracked file changed)
RP6-P0.sh       5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
SELF_QA_RP6.md  0bbf41dd2985a587c97a992589c7576b31e92217d11ecb888b4c8b2c84b84481
```

Both audited identities are unchanged from the pre-execution re-derivation. All
harness scratch, mutants, and captured output were written outside the
repository; every mutant lived in a `mktemp -d` directory removed by its own
trap.

**Whole-status delta (advisory, with attribution):** no other repository path
changed during this audit session — the addition set is exactly this one file
and the removal set is empty. The concurrent-lane movement noted by the
interrupted predecessor session (RP7 rows-1-9 and PATHSCOPE paths) was already
present in this session's 175-entry baseline and is attributable to those lanes,
not to this audit. The path-scoped gate therefore passes, and the whole-status
delta happens to pass as well.

**Author attestation:** no host, SSH, network, deployment, credential, broker,
exchange, ARM, order, backtest, trading, or Git mutation occurred in this
session. This is a whole-session negative and is an author attestation; the
repository write scope is proved separately by the delta gate above.
