REQUEST_CHANGES

# RP6-P0 Codex T0 audit — round 10

**TIER: T0. APPLIED AUDITOR CONTRACT: Codex `gpt-5.6-sol`, effort xhigh,
fresh independent report-only audit.** The audited package is commit
`c14c7992a1f6a5377f8cf1499154e54737af028d`. No source, Git state, host, or
network was mutated. Audit fixtures existed only under the local temporary
directory and were removed. This report is the one authorized repository write.

## Subject identity

The four kickoff files are byte-identical to their blobs at `c14c7992`.

```text
RP6-P0.sh
  bytes  = 107252
  sha256 = a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617
  CR     = 0
  bash -n rc = 0

SELF_QA_RP6.md
  bytes  = 391019
  sha256 = 87494fbd0b2f4ca7f1b97774fb9c59ee03983757b5ab61f5f0f2b0793852441b

STATUS_RP6_P0.md
  bytes  = 54399
  sha256 = c0a13d150853b5c9ac4f03441e25fadcf431d2289a51434d7be98146a91497cf

RP6_R10_REPORT_2026-08-11.md
  bytes  = 26091
  sha256 = a1f927847ae9d33d981b1808d177058d65daae22a6f6ff2c8c224f0c6be53ebc
```

The worktree contains unrelated user/session changes. None overlaps the four
frozen files above, and none was touched.

## Published R10 commands executed

PowerShell does not expose `sed` on its PATH, so an initial PowerShell attempt
did not start a harness and is not evidence. I then launched fresh Git Bash
processes from `WPI_BLOCKS_DRAFT` and ran each published pipeline unchanged
inside that shell.

```text
sed -n '/^# R10_GRAMMAR_HARNESS_BEGIN$/,/^# R10_GRAMMAR_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
  rc=0
  R10_GRAMMAR_SUMMARY cases=10 pass=10 fail=0 result=PASS

sed -n '/^# R10_F3_HARNESS_BEGIN$/,/^# R10_F3_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
  rc=0
  R10_F3_QA_SUMMARY cases=14 pass=14 fail=0 result=PASS

sed -n '/^# R10_F4_HARNESS_BEGIN$/,/^# R10_F4_HARNESS_END$/p' SELF_QA_RP6.md | bash --noprofile --norc
  rc=0
  R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS
```

The summary lines appeared in the real output. This closes the narrow
round-9 F1 failure mode for these three commands: each pipeline actually ran
the named harness. The accepting summaries do not settle the defects below.

## Findings

### 1. HIGH — the grammar fence is fail-open and its 89/161 equality is lossy

`SELF_QA_RP6.md:5687-5696,5720-5743,5782-5787` models only literal
double-quoted `p0_stop "..."` / `p0_fail "..."` calls and one exact single-quoted
direct-`printf` spelling. Its supposedly independent site count uses the same
lexical restriction. An executable emitter written with another valid shell
spelling disappears from both counts, which is catalogue Pattern 12.

Executed falsification: I inserted one reachable, valid single-quoted emitter
into a temporary copy immediately after `p0_probe_kind() {`:

```text
[ -z "${P0_R10_ALT_SYNTAX_MUTANT:-}" ] || p0_stop 'r10_alt_syntax detail=single_quoted'
```

The mutation was present exactly once. Running the published R10 grammar
harness against that mutant and the live declaration still returned:

```text
R10_GRAMMAR_DECLARED forms=89 sites=161
R10_GRAMMAR_DERIVED  forms=89 sites=161
ASSERT_MET grammar_closed declared==derived forms=89 sites=161
ASSERT_MET site_total_independent expected=161 derived=161 wrapper_sites=160 direct_sites=1
R10_GRAMMAR_SUMMARY cases=10 pass=10 fail=0 result=PASS
AUDIT_MUTANT_HARNESS_RC=0
```

The normalization is independently lossy even within its modeled syntax.
It groups sites by prefix, reason, and field-name order, then stores an
independent set of values for each field. That destroys correlations between
fields. For example, the three `identity_unexpected` emitters become one line
whose `observed_numeric`, `expected_numeric`, and `account` value sets admit a
Cartesian product. Changing `RP6-P0.sh:1266` from `account=gatea` to
`account=mtc-bridge` is a semantic relabelling, but the other two sites preserve
both account values in the union. The published harness again returned all ten
assertions PASS and rc 0. An independent grouping found 12 forms with this
correlation loss, admitting 65 synthetic field-value combinations beyond the
actual site tuples.

I also independently re-derived the current bytes without using the published
awk implementation. The narrow arithmetic itself is correct:

```text
sites=161 (P0_STOP=153, P0_FAIL=8)
forms=89
declared_sites=161
declared_forms=89
current mismatches=0
current executable p0_stop/p0_fail spellings outside the modeled form=0
```

That confirms the requested 89/161 claim only for today's modeled spellings;
it does not establish the report's stronger “complete/exhaustive grammar”
claim or protect a future edit.

**Required repair.** Make grammar coverage fail closed. Census every executable
wrapper call and direct result emitter with a broader independent mechanism and
emit a coverage error for every syntax the normalizer cannot parse. Preserve
each site's correlated normalized tuple rather than independent per-field
unions (or declare each exact tuple separately). Add and execute D026 mutants
for at least an alternate valid quoting form and the correlation-preserving
relabel above; both must make the fence return nonzero.

### 2. HIGH — F3 still turns an unrecognized producer token into host-state FAIL

`RP6-P0.sh:1600-1612` correctly STOPs on empty, multiline, and non-printable
followed-target output. But `RP6-P0.sh:1618-1622` maps every remaining printable
single line through `*) P0_FKIND="other"`. That includes arbitrary producer text,
not only a recognized complete GNU `stat -c %F` kind. The caller then emits
`P0_FAIL reason=interpreter_target_kind_unexpected ...` at rc 1.

This does not meet the round-9 required repair, which explicitly required a
recognized complete kind before `P0_FKIND` is assigned. It also violates
Patterns 1, 5, and 6: a successful producer status plus an unrecognized result
grammar is inability to evaluate, not an observation of deviant host state.

Executed against the real round-10 functions by adding one local shim mode to
the published F3 harness:

```text
followed-target stdout = made up stat kind
followed-target rc     = 0

AUDIT_UNRECOGNISED rc=1 last=[P0_FAIL reason=interpreter_target_kind_unexpected kind=other path=/fixture/python expected=regular]
R10_F3_QA_SUMMARY cases=14 pass=14 fail=0 result=PASS
```

The existing fence therefore stays green while the residual defect is live.

**Required repair.** Define the complete accepted `%F` token grammar for the
pinned producer. Assign `P0_FKIND=other` only for explicitly recognized,
complete non-regular kinds; STOP with a declared reason on any unknown printable
token. Add D026 RED against the current catch-all (rc 1) and GREEN against the
repair (exact STOP line, rc 3), while retaining the directory rc-1 and regular
rc-0 regressions.

### 3. HIGH — the published RED recipe still masks its own failing status

`SELF_QA_RP6.md:6386-6395` says the R9 RED twin is published in full so a third
party can run it verbatim. The recipe runs the failing harness, prints
`R9_RED_RC=$?`, and then executes `rm -f "$mutant"`. Running those exact published
lines produced:

```text
R9_GRAMMAR_SUMMARY cases=5 pass=2 fail=3 result=FAIL
R9_RED_RC=1
```

but the published recipe process returned **rc 0**, because cleanup is its last
command. This contradicts `RP6_R10_REPORT_2026-08-11.md:103-118` and
`SELF_QA_RP6.md:5591-5599`, which record the published/verbatim RED twin as rc 1
and say every command's status agrees with its verdict. It repeats the exact
round-9 F1 / Pattern-10 defect at the recipe level.

The ten newly added fence guards themselves are behaviorally sound. I
independently extracted each fence, inserted exactly one `COUNTER=7` immediately
before its real guard, checked the adjacency, and ran the mutant. All ten
returned rc 1: R5_F1/F2/F3, R6_F1/F2/F3, R7_F2/F3/C3, and R9_GRAMMAR. However,
`SELF_QA_RP6.md:6546-6578` publishes only a prose algorithm and transcript, not
the exact executable falsification command it says is “in the harness above.”
There is no such harness in the file. Under D026, the implementer's transcript
is supplemental until the exact command plus status is published, even though
this audit independently confirmed the behavior.

**Required repair.** Preserve the RED harness status across cleanup and exit
with it (or use an EXIT trap for cleanup), then record the whole recipe's real
rc 1. Publish an executable, self-checking guard-falsification fence—not only a
transcript—and record its real output/status.

### 4. MEDIUM — F4's repair is sound, but its evidence prose still outruns it

The byte repair at `RP6-P0.sh:675-676` is truthful: the reason now names the
internal binding predicate. The published F4 harness also reaches that exact
line at rc 3 after a mutation and confirms the three named ordinary cases plus
the valid case.

The surrounding claims are broader than the executed predicate:

- `RP6-P0.sh:671-674` says the fence “deletes the three upstream gates.” The
  mutation at `SELF_QA_RP6.md:6293-6296` neutralizes two sites: the omission loop
  and the count check. It does not delete the freeze-unfilled or disagreement
  gates.
- `SELF_QA_RP6.md:6145-6153`, `RP6_R10_REPORT_2026-08-11.md:362-369`, and the
  status layer describe the three tested cases as “every input class that leaves
  the binding unset.” The real parser also has malformed-entry, unknown-tool,
  duplicate, non-absolute, whitespace, glob, non-python frozen-path, and other
  early-stop classes. Those were not executed by R10_F4.

This does not reopen the reason-token repair; it is a Pattern-9 evidence
overclaim. The specific `17 -> 19` correction is accurate—the mandated block
contains 19 commands—and the `57 -> 172` correction now correctly treats both
counts as machine-dependent observations rather than a stable measurement.

**Required repair.** Narrow the F4 prose everywhere to the three input classes
actually executed and to the two gates actually neutralized, or extend the
harness to substantiate the broader claims. Correct the stale source comment.

## Finding disposition and minimum repair set

Round-9 findings 1, 2, and 3 remain open in the evidence/behavior above. The
round-9 finding-4 relabel itself is repaired, but its evidence prose needs the
narrow correction in finding 4 of this report.

Minimum repair set:

1. Make the grammar fence fail closed over unmodeled emitter syntax and preserve
   per-site value correlations; add the two discriminating mutants.
2. STOP on an unrecognized printable followed-target `%F` result and add real
   RED/GREEN evidence.
3. Make the published RED recipe itself return 1 and publish the executable
   ten-guard falsification harness with real output.
4. Narrow the F4 prose/comment to what its execution establishes.

## Final verdict

**VERDICT: REQUEST_CHANGES.** The three required R10 pipelines genuinely execute
and pass, and the current modeled declaration does reconcile at 89 forms / 161
sites. Acceptance is nevertheless impossible: the grammar closure test passes
two load-bearing mutants it claims to kill, the F3 producer grammar still has an
rc-1 false verdict, and the published RED evidence still returns rc 0 when run
as published. No host, deployment, credential, ARM, broker, exchange, trading,
or freeze authority is implied or granted.
