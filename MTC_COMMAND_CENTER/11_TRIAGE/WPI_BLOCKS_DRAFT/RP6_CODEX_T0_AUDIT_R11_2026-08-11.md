REQUEST_CHANGES

# RP6-P0 Codex T0 audit — round 11

**TIER: T0. APPLIED AUDITOR CONTRACT: Codex `gpt-5.6-sol`, effort xhigh,
fresh independent report-only audit.** The audited package is commit
`2d033fa67b1df3e451d2d05ec29033ed2c8d1e95`. No source, Git state,
staging/remote host, or network was mutated. Temporary local audit fixtures were
removed. This report is the one authorized repository write.

## Subject identity and scope

The four kickoff files and the preregistration declaration they consume are
byte-identical to their blobs at `2d033fa6`. `RP6-P0.sh` matches the kickoff
identity exactly:

```text
RP6-P0.sh
  bytes  = 110817
  sha256 = 5132bacde24cbff8c9267a82f6ac6e3b0cebe3d3c82b092518efac1245103330
  CR     = 0
  bash -n rc = 0

SELF_QA_RP6.md
  bytes  = 467356
  sha256 = 96e9920ee99399b9a258be97ce8df71abea6ef7bb67e63d31df9d5a8fb7b293f

STATUS_RP6_P0.md
  bytes  = 60499
  sha256 = aad774947702851716c1fd5f224fdc5590c888e5731fe808806043bab3bfef56

RP6_R11_REPORT_2026-08-11.md
  bytes  = 25274
  sha256 = 21ffd9a26b9ad1d25538149d8196cca7642da7dfa377c79d70d48610111ed323
```

All five audited/dependent files have zero CR bytes. `git diff --check` on the
round-11 commit is clean. Commit `2d033fa6` changes only the four files named by
the kickoff; the required preregistration §8.1.1 declaration was already present
in its parent, as the repair report discloses. I found no Pine, parity, MTC,
trading-logic, credential, broker, exchange, or other protected-surface edit in
this repair.

The worktree contains unrelated untracked logs and evidence from other sessions.
None overlaps the frozen subject files, and none was touched.

## Published commands executed verbatim

I extracted all 23 lines directly from the mandated-command block at
`SELF_QA_RP6.md:7822-7844` and executed each unchanged from
`WPI_BLOCKS_DRAFT` in a fresh local Git Bash `--noprofile --norc` process. The
observed status vector and terminal summaries were:

```text
bash -n RP6-P0.sh                  rc=0
C13_R3_BACKSTOP                    rc=0  C13_R3_BACKSTOP_QA_SUMMARY inputs=2 mutations=2 cases=4 result=PASS
RP6_FULLBLOCK_D026                 rc=0  RP6_FULLBLOCK_D026_SUMMARY findings=7 round3_residuals=3 real_lstat_arms=2 execution_domain_cases=9 readlink_stop_arms=3 result=PASS
F2_FREEZE_GATE                     rc=0  F2_FREEZE_GATE_QA_SUMMARY placeholder_rc=3 filled_fixture_rc=0 result=PASS
RP6_R4_D026                        rc=0  RP6_R4_D026_SUMMARY findings=4 pth_forge=real_venv manager_bound=real_timeout inventory_basis=23e55667@d6a976aa result=PASS
C13_R4B                            rc=0  C13_R4B_ARM_QA_SUMMARY cases=27 result=PASS
R5_F1                              rc=0  R5_F1_QA_SUMMARY cases=6 pass=6 fail=0 result=PASS
R5_F2                              rc=0  R5_F2_QA_SUMMARY cases=4 pass=4 fail=0 result=PASS
R5_F3                              rc=0  R5_F3_QA_SUMMARY cases=5 pass=5 fail=0 result=PASS
R6_F1                              rc=0  R6_F1_QA_SUMMARY cases=3 pass=3 fail=0 result=PASS
R6_F2                              rc=0  R6_F2_QA_SUMMARY cases=10 pass=10 fail=0 result=PASS
R6_F3                              rc=0  R6_F3_QA_SUMMARY cases=7 pass=7 fail=0 result=PASS
R7_F2                              rc=0  R7_F2_QA_SUMMARY cases=4 pass=4 fail=0 result=PASS
R7_F3                              rc=0  R7_F3_QA_SUMMARY cases=4 pass=4 fail=0 result=PASS
R7_C3                              rc=0  R7_C3_QA_SUMMARY cases=8 pass=8 fail=0 result=PASS
R9_GRAMMAR                         rc=0  R9_GRAMMAR_SUMMARY cases=5 pass=5 fail=0 result=PASS
R10_F3                             rc=0  R10_F3_QA_SUMMARY cases=14 pass=14 fail=0 result=PASS
R10_F4                             rc=0  R10_F4_QA_SUMMARY cases=16 pass=16 fail=0 result=PASS
R11_GRAMMAR                        rc=0  R11_GRAMMAR_SUMMARY cases=15 pass=15 fail=0 result=PASS
R11_F1_RED                         rc=0  R11_F1_RED_SUMMARY cases=17 pass=17 fail=0 result=PASS
R11_F3                             rc=0  R11_F3_QA_SUMMARY cases=85 pass=85 fail=0 result=PASS
R11_GUARDS                         rc=0  R11_GUARDS_SUMMARY fences=15 pass=15 fail=0 result=PASS
R11_R9RED                          rc=1  R9_RED_VERDICT status_preserved_across_cleanup exit=1
```

The R9 RED-twin recipe therefore now returns the real failing status rather than
the cleanup status. Its real output included
`R9_GRAMMAR_SUMMARY cases=5 pass=2 fail=3 result=FAIL`, `R9_RED_RC=1`, and the
published terminal verdict above. `R11_GUARDS` is an executable fence, not prose:
all 15 extracted fences had exactly one guard, the forced counter assignment was
verified immediately adjacent to it, and every mutant returned rc 1.

## Independent adversarial checks

### Correlation-preserving relabel

I independently changed only the first `identity_unexpected` tuple's
`account=gatea` to `account=mtc-bridge` in a temporary copy. The mutation changed
one source line, remained valid shell, and produced:

```text
R11_GRAMMAR_CENSUS emitter_lines=163 unmodeled=0
ASSERT_UNMET grammar_closed declared!=derived diff_lines=2
R11_GRAMMAR_SUMMARY cases=15 pass=13 fail=2 result=FAIL
AUDIT_RELABEL_GRAMMAR_RC=1
```

The second failed case is the harness's own already-applied relabel mutant; the
load-bearing result is that the base tuple comparison itself failed. Correlation
preservation is therefore real.

### F3 producer grammar and STOP/FAIL classification

The published 85-case fence reproduced both unknown-token STOPs at rc 3, both
round-10 catch-all RED results at rc 1, every listed recognized non-regular kind
at rc 1, and regular kinds at rc 0. I additionally drove the real
`p0_assert_venv_root` caller through an independent local `stat` shim:

```text
LEAF_UNKNOWN rc=3 last=[P0_STOP reason=path_probe_kind_unrecognized path=/fixture/venv rc=0 detail=novel stat token expected=complete_gnu_stat_percent_F_token]
FOLLOW_UNKNOWN rc=3 last=[P0_STOP reason=link_target_kind_unrecognized path=/fixture/venv rc=0 detail=novel followed token expected=complete_gnu_stat_percent_F_token]
```

Thus no successful-producer plus unrecognized-token path I found reaches a
host-state FAIL. The accepted set also covers the embedded file-type strings in
the two locally installed GNU `stat` builds inspected read-only (coreutils 8.32
and Ubuntu GNU coreutils 9.7). I found no missing GNU `%F` token.

### Novel valid emitter syntax

The required fail-closed property does not hold. Finding 1 below records the
executed counterexample.

## Findings

### 1. HIGH — the line-oriented census still misses valid executable emitter syntax

`SELF_QA_RP6.md:6847-6856`: the “broader independent” census still searches for
the contiguous textual word `p0_stop`/`p0_fail` or the contiguous result literal.
Shell command words can be assembled from adjacent quoted and unquoted segments,
so a real wrapper invocation need not contain that text contiguously.

Executed falsification: immediately after `p0_probe_kind() {` in a temporary copy
I inserted this valid, reachable emitter:

```bash
[ -z "${P0_R11_CMDQUOTE_MUTANT:-}" ] || p0_s""top "r11_cmdquote detail=quoted_command_word"
```

`bash -n` returned 0. Extracting the real function and setting the variable proved
that the shell resolves the constructed command word to `p0_stop`:

```text
AUDIT_CMDQUOTE_INSERTED=1
AUDIT_CMDQUOTE_BASH_N_RC=0
AUDIT_CMDQUOTE_EXEC_RC=3 LAST=[P0_STOP reason=r11_cmdquote detail=quoted_command_word]
```

The published R11 fence nevertheless certified the mutated bytes:

```text
R11_GRAMMAR_DECLARED tuples=149 sites=163
R11_GRAMMAR_DERIVED  tuples=149 sites=163
R11_GRAMMAR_CENSUS   emitter_lines=163 unmodeled=0
ASSERT_MET census_no_unmodeled_syntax
ASSERT_MET census_covers_every_emitter census_lines=163 derived_sites=163
R11_GRAMMAR_SUMMARY cases=15 pass=15 fail=0 result=PASS
AUDIT_CMDQUOTE_GRAMMAR_RC=0
```

This is catalogue Pattern 12 and reproduces the substance of round-10 finding 1
under a different valid quoting form. `STATUS_RP6_P0.md:20-21` and
`RP6_R11_REPORT_2026-08-11.md:86-90` therefore overstate the current property as
fail-closed.

**Required repair.** Replace or strengthen the census so quoted, continued, or
otherwise constructed wrapper command words and result literals cannot disappear.
An AST-backed check or an explicit fail-closed source-style policy is acceptable,
but the policy must reject every syntax it does not model rather than assume a
contiguous grep token. Add this command-word-fragmentation mutant to D026 and show
RED on the current fence and nonzero on the repaired fence.

### 2. MEDIUM — F4's current published harness comment still carries the overclaim

`SELF_QA_RP6.md:6194-6199`: inside the live, still-mandated `R10_F4` harness, the
comment says “Every input class that leaves the binding unset is shown” and then
names only omitted, unfilled, and disagreeing pins. The new prose above the fence
correctly limits the evidence to three classes, but it did not narrow this second
claim inside the published harness. That contradicts the round-11 report's
“every claim narrowed” disposition and is catalogue Pattern 9.

The old overclaim in `RP6_R10_REPORT_2026-08-11.md:362-364` is adequately corrected
by the R11 report/SELF_QA/status scope-fenced correction and need not be edited in
place. This finding is only the stale claim in the writable current `SELF_QA_RP6.md`.

**Required repair.** Change the harness comment to “the three input classes this
fence executes” (or equivalent) and retain the explicit list. No executable
harness widening is required.

## Thirteen-pattern disposition

1. STOP versus FAIL: finding 2 from round 10 is closed at both classifiers.
2. Observation domain: no new round-11 defect found.
3. Parent/path binding: no new round-11 defect found.
4. Privileged child environment: no new round-11 defect found.
5. Grammar versus substring matching: the `%F` token classifier is explicit; no
   F3 residual found.
6. Producer status/shape before semantics: the real functions STOP before caller
   semantics on unknown output.
7. Reader completion: no new round-11 reader change.
8. Numeric/kernel identity: no new round-11 identity change.
9. Claim outruns predicate: required finding 2 above.
10. Falsifiable evidence: R9 status and the 15 guard fences are now executable;
    finding 1 identifies the missing discriminating mutant for the census claim.
11. Declared versus executed instrument: the F3 fence drives the real functions
    through a disclosed shim; no new gap found.
12. Unmodeled analyzer input disappears: required finding 1 above.
13. Terminal disposition/conservation: correlated tuple relabel is caught; no new
    round-11 conservation defect found.

## Final verdict

**VERDICT: REQUEST_CHANGES.** Round-10 findings 2 and 3 are closed, and the
round-10 report's scope-fenced F4 correction is adequate. Acceptance is still
impossible because the replacement grammar fence certifies a valid reachable
emitter syntax it does not census, and the current F4 harness retains one binding
overclaim. Minimum repair set: close the command-word-fragmentation census hole
with executed D026 RED/GREEN evidence, and narrow the stale F4 harness comment.
No host, deployment, credential, ARM, broker, exchange, trading, or freeze
authority is implied or granted.
