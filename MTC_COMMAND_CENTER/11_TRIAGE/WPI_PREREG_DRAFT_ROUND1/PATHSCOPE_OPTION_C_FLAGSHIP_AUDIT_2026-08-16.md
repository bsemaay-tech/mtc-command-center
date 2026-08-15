REQUEST_CHANGES

# Pathscope Option C — fresh flagship execution audit, 2026-08-16

Auditor: `claude-opus-5`, fresh session. I did not design, review or implement Option C.
Subject: worktree `C:\PSCAUD`, commit `ec98cbd4d629d7e035f99da70d5e73fb7f610da1`.

Two REQUIRED findings. Under owner decision D1 this returns the lane to the owner
boundary; it does not authorize a second implementation round.

The short version: **the accounting layer is real and it works.** Every published digest
reproduces byte-exactly under a runner I wrote myself, conservation and provenance are
genuine checks with independent inputs, and I could not construct a normalization or
identity escape. But the **class is not closed.** The admission-boundary guard closes one
branch of `scan_args` and leaves at least three others open, and I reproduced the original
F1 attack — `${LD_PRELOAD:=/etc/evil.so}` — reaching `PASS rc=0` with zero issues by moving
the identical token into a data-role option-value position. Separately, the
reading-cardinality check that the design calls "independent" is computed from the same
list the splitter emits from, and cannot fail for the reason it exists.

---

## 1. Session header and transport

The kickoff asks me to print a session header and confirm
`--dangerously-bypass-approvals-and-sandbox`. That flag is a Codex CLI flag; this audit ran
in Claude Code, which has no equivalent header line. I therefore report the property the
precondition actually protects — **can this session do the work and write the verdict** —
by measurement rather than by quoting a banner.

| capability | result |
|---|---|
| read-only Git (`rev-parse`, `status`, `log`, `cat-file blob`, `ls-files`, `diff`) | works |
| CPython execution of prover, composite and QA runner as subprocesses | works |
| SHA-256 / SHA-1 / Git blob-OID computation | works |
| write to scratch (`C:\tmp\psaudit`) and to the one verdict file | works |

One policy restriction applied and is disclosed here because it changed my method: this
session's tool policy refuses to **spawn a nested PowerShell process**, so I could not
execute `pathscope_option_c_harness.ps1` verbatim. This is not a `TRANSPORT-BLOCK` — no
Git, Python or hash command was refused, and no analysis was blocked. I worked around it in
the way an independent auditor should prefer anyway: I extracted the harness, proved its
byte identity, and then **re-implemented its measurements in Python and ran those**. Every
published digest reproduced. See §3.

State before and after the work:

```
$ git rev-parse HEAD
ec98cbd4d629d7e035f99da70d5e73fb7f610da1
$ git status --porcelain
(empty)
$ git rev-parse --abbrev-ref HEAD
HEAD
$ git branch -a --contains HEAD
* (no branch)
+ codex/pathscope-accounting-redesign-20260815
  remotes/origin/codex/pathscope-accounting-redesign-20260815
```

Re-run after all analysis and before writing this file: identical, `git status --porcelain`
empty. The only write I made inside `C:\PSCAUD` is this file.

```
$ git diff --stat 5aa06511 ec98cbd4
 ...PE_OPTION_C_IMPLEMENTATION_REPORT_2026-08-15.md |  319 ++++
 .../WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md   |  304 +++-
 .../WPI_PREREG_DRAFT_ROUND1/STATUS_PATHSCOPE.md    |   30 +-
 .../WPI_PREREG_DRAFT_ROUND1/composite_pathproof.py |  701 ++++++--
 .../pathscope_option_c_qa.py                       |  653 ++++++++
 .../WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py    | 1667 +++++++++++++++++---
 6 files changed, 3332 insertions(+), 342 deletions(-)
```

---

## 2. Identity derivation

`* text=auto` at the repository root has already caused three defects here, so both forms
are measured independently, and the blob OID is recomputed from the blob bytes rather than
trusted from `git rev-parse`.

Directory `.gitattributes` pins `pathscope_prover.py text eol=lf` and
`composite_pathproof.py text eol=lf`. It does **not** pin `pathscope_option_c_qa.py` — see
NIT-3.

| file | form | bytes | SHA-256 | Git blob OID |
|---|---|---:|---|---|
| `pathscope_prover.py` | working tree | 185272 | `3DA28F8EC3F4762836350293D8B51A797E2B2A3EAA1D06EEE36C768F706C969F` | n/a |
| `pathscope_prover.py` | Git blob | 185272 | `3DA28F8EC3F4762836350293D8B51A797E2B2A3EAA1D06EEE36C768F706C969F` | `db220dc6edf117cd1e1627bbed36fda3cb0b6057` |
| `composite_pathproof.py` | working tree | 152451 | `A7C93D82F03C01DDEBA2DE742E6E3DD88C8EDA7DBA968D0C36AFD85EE9EBA7E6` | n/a |
| `composite_pathproof.py` | Git blob | 152451 | `A7C93D82F03C01DDEBA2DE742E6E3DD88C8EDA7DBA968D0C36AFD85EE9EBA7E6` | `1b1c55f0cf4c0c619fae9bc01f042134a61a38b9` |
| `pathscope_option_c_qa.py` | working tree | 25576 | `A86636BA9B57528E38C70BD66C029625B4BC574D06C7237AA29AC5A9B18F2353` | n/a |
| `pathscope_option_c_qa.py` | Git blob | 24923 | `7468E05F9058B58FCF66F6EF02BC051B91F36496F66D009DAA332410BA6C76D1` | `627aa40593c011f0f59a14bdd9fea587115e9ba1` |

Line-ending measurement: prover working tree `CRLF=0 LF=4349`, blob `CRLF=0 LF=4349`;
composite working tree `CRLF=0 LF=3319`, blob `CRLF=0 LF=3319`; QA runner working tree
`CRLF=653 LF=653`, blob `CRLF=0 LF=653`.

Blob-OID recomputation (`sha1("blob <n>\0" + bytes)`) matched `git rev-parse` for all three.
The prover's two forms are byte-identical and were measured separately, confirming the
report's §8 table. The QA runner's two forms are **not** byte-identical.

Published harness identity, extracted independently (locate the second ` ```powershell `
fence in the committed markdown, take its 624 lines verbatim):

```
MD bytes=331119 sha256=A3FA7FD436CD3A85856323EF116387B2FA000F4E7F29C39BE1A2C8C457B82B3D
powershell fence starts (0-based): [126, 267]
harness fence lines=624 (md lines 269..892)
HARNESS[LF]   bytes=36758 sha256=A6C1E45DC276E7956DAB08C13CEAC7C6BB430C6ABA4607A6AC11D27A2962174B
HARNESS[CRLF] bytes=37382 sha256=61FB09D27F53BF3F97902849215FF4AC9BEE9B3DC19846BBA3AE2F4B8AA27FC7
```

The CRLF form reproduces the report's `HARNESS_BYTES=37382` /
`HARNESS_SHA=61FB09D2...FC7` exactly. Both forms are recorded here because the report gives
only one, and the file is markdown-embedded text.

Reconstructed pinned blobs (all four provers plus both real blocks) matched their published
bytes, SHA-256 and recomputed OIDs:

```
R1_BASELINE  bytes=49820  sha256=3D6AF544...D43E6 git_blob=3f0820a9a6412f769b59b23a41df3bc6808bf6dc
R3_PREREPAIR bytes=124251 sha256=07249679...25F7  git_blob=e600a107f2e2a790653cc544a94cd7436b7b070a
R4_PREREPAIR bytes=131599 sha256=553A97E9...E2EB  git_blob=55ea3a852f7781d03d57483f554c1b8ac62007c6
R5_FROZEN    bytes=137520 sha256=28848D60...DF9C  git_blob=695ca9c951e31f53da9580d41326583d71086bb3
BLOCK RP6-P0.sh      bytes=107252 sha256=A090AE73...0617 git_blob=3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c
BLOCK RP7-WPI-RO.sh  bytes=99903  sha256=11621044...41A4 git_blob=5c9a2f597cceaef80d1cbd0fc100732f4b216cf5
```

---

## 3. Reproduction of the published evidence

I rebuilt the fixture set, case lists and transcript format from the committed markdown in
my own Python runner (`C:\tmp\psaudit\aud_harness.py`), under a scratch `TEMP`, and ran the
prover myself. Not one number below is copied from the implementer's report.

**Every published fence reproduced byte-exactly.**

```
FENCE RED_R1.txt                 published=667BF364...E89D measured=667BF364...E89D match=True
FENCE RED_R3.txt                 published=599B4482...CBCC measured=599B4482...CBCC match=True
FENCE RED_R4.txt                 published=BC142778...C01B measured=BC142778...C01B match=True
FENCE R5_BASELINE.txt            published=A534BDCF...E328C measured=A534BDCF...E328C match=True
FENCE GREEN_OPTION_C.txt         published=B70F54B1...EE64 measured=B70F54B1...EE64 match=True
FENCE GREEN_OPTION_C_REPEAT.txt  published=B70F54B1...EE64 measured=B70F54B1...EE64 match=True
FENCE RED_R5_OPTION_C.txt        published=78DD1C3B...F74A measured=78DD1C3B...F74A match=True
FENCE GREEN_OPTION_C_ATTACKS.txt published=49051247...9E6D measured=49051247...9E6D match=True
FULL_SUITE_DETERMINISM equal=True sha256=B70F54B11703220DA272B526C5C2564A3D08CA67C8B073F2B81857B804D4EE64
REGRESSION_RC cases=109 candidate_cases=109 deltas=c2_benign_words:0->3,c3_colon_whole:1->3
REGRESSION_BYTES declared_blocks=60 mismatches=NONE
BYTE_IDENTICAL_ACTUAL_TOTAL=60
BYTE_IDENTICAL_UNDECLARED=[]
BLOCKS_CHANGED=49
```

Line counts also matched (768 / 150 / 324 / 1557 / 3442 / 3442 / 155 / 222).

`BYTE_IDENTICAL_ACTUAL_TOTAL=60` with `BYTE_IDENTICAL_UNDECLARED=[]` is the check the
harness does not make: the declared 60-block list is not merely satisfied, it is **exactly**
the set of byte-identical blocks. Nothing was quietly identical outside the declaration and
nothing declared was missing.

### 3.1 The committed mutation runner, executed by me

```
$ python -B pathscope_option_c_qa.py <candidate> <frozen R5> <composite> <fixture dir>
```

All 44 lines reproduced identically to `SELF_QA_PATHSCOPE.md:159-202`: `M01`…`M15` each
`rc=3 summary=FAIL faults>0 pass_present=false terminal=accounting_invariant_failed`
(including the two required conservation arms `M01_delete_disposition faults=4` and
`M03_unknown_member faults=7`), all 18 `ATTACK` lines with the published `r5_rc`/`candidate_rc`
pairs, all 8 `COMPOSITE_MUTATION` STOPs with their published reasons, both `COMPAT_MUTATION`
lines, and `OPTION_C_MUTATIONS PASS arms=23 checks=25`.

### 3.2 The eighteen attack cases, RED against frozen R5 and GREEN against the candidate

Measured, not predicted. Guard family `guard_colon/true/echo/printf/equal` all
`r5_rc=0 → candidate_rc=3`; controls `control_single_quote` and `control_fallback` stay
`0 → 0` and are **byte-identical** to R5's output; `f1_command_words` and `f1_uri_bare`
`0 → 3`; `f2_provenance` `0 → 3`; `f3_duplicate` `1 → 1` with two distinct member IDs;
`f3_empty` `0 → 0` with three separate empty PWD members.

### 3.3 The seven retired determinism digests, re-measured twice each

All seven reproduced `SELF_QA_PATHSCOPE.md:204-210` exactly, e.g.

```
DETERMINISM find_exec       rc1=1 rc2=1 equal=True sha1=f0f0bf2d...f11bd sha2=f0f0bf2d...f11bd
DETERMINISM assign_prefix   rc1=1 rc2=1 equal=True sha1=8428decd...5469d sha2=8428decd...5469d
DETERMINISM c2_list_prefix  rc1=1 rc2=1 equal=True sha1=bb6c9e7e...1eaad sha2=bb6c9e7e...1eaad
DETERMINISM c3_ws_relative  rc1=3 rc2=3 equal=True sha1=5734d342...6dba9 sha2=5734d342...6dba9
DETERMINISM c4_export_quoted rc1=1 rc2=1 equal=True sha1=3df2ae08...9be94 sha2=3df2ae08...9be94
DETERMINISM RP6-P0          rc1=3 rc2=3 equal=True sha1=19cb227c...c7e67 sha2=19cb227c...c7e67
DETERMINISM RP7-WPI-RO      rc1=3 rc2=3 equal=True sha1=cad3d354...e1077 sha2=cad3d354...e1077
```

Plus the two full-suite runs (3442 lines each) are byte-identical.

### 3.4 Regression honesty — full projection census

The report claims 11 row deltas. I censused every `PATH`/`ENDPOINT` row in all 109 blocks
after stripping the new `member_id` suffix:

```
BLOCKS_TOTAL=109  BLOCKS_WITH_PROJECTION_DELTA=10
TOTAL_ROW_DELTAS=11 SOURCES_ONLY=10 OTHER=1
```

The ten are exactly the declared exact-provenance corrections (`sources=ROOT`→`NONE` in
`c2_list_prefix`, `c2_list_env`, `c2_list_export`, `c2_quoted_space`, `c2_escaped_space` ×2,
`c3_ws_relative`, `c4_typeset_quoted`; `sources=URL`→`NONE` in `c3_uri_list`, `c3_uri_pair`).
The eleventh is the declared RP7 case:

```
R5  : PATH value=/ verdict=FORBID rule=- sources=NONE uses=line=542:...,line=679:...,line=681:assignment prefix
CAND: PATH value=/ verdict=FORBID rule=- sources=NONE uses=line=542:...,line=679:...
```

RP7-WPI-RO.sh:681 is `seen_roots="$seen_roots$r "`. The candidate's member row for it is
`text=b64u:IC8g` — which decodes to `" / "` — with
`reason=member_normalization_failed`, exactly as declared. R5 trimmed it to the false
candidate `/`. **No unpredicted delta exists.** This is honestly reported.

---

## 4. My own attacks

Four batteries, ~90 fixtures, none of them in the implementer's 18-case set.

### 4.1 REQUIRED-1 — the admission boundary is not closed

`file: MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py:2532-2546,2547-2577,2611-2646,2648-2687,1330`

The guard sits at the **top of the `scan_args` loop** (2555-2577). It is only consulted for
a token the loop examines directly. Three routes never reach it.

**(a) Data-role option operands.** `_apply_option` (2645) and `_apply_cluster` (2685) consume
the *next* token via `consume_token_value`, whose first statement is
`if role == "data": return` (2533-2534). The token is never expanded and never classified.

The cleanest possible demonstration — identical token, two positions:

```
ab_printf_operand  printf '%s' ${LD_PRELOAD:=/etc/evil.so}     rc=3 issues=1  REJECT rc=3 reason=static_resolution_incomplete
ab_printf_optval   printf -v ${LD_PRELOAD:=/etc/evil.so} hello rc=0 issues=0  PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
ab_read_operand    read ${LD_PRELOAD:=/etc/evil.so}            rc=3 issues=1  REJECT rc=3 reason=static_resolution_incomplete
ab_read_optval     read -p ${LD_PRELOAD:=/etc/evil.so} x       rc=0 issues=0  PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
ab_kill_operand    kill ${LD_PRELOAD:=/etc/evil.so}            rc=3 issues=1  REJECT rc=3 reason=static_resolution_incomplete
ab_kill_optval     kill -s ${LD_PRELOAD:=/etc/evil.so} 1       rc=0 issues=0  PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
```

Full output of one of them, showing that the report is not merely silent but affirmatively
clean:

```
$ cat aud_optval_read_p.sh
#!/bin/bash
read -p ${LD_PRELOAD:=/etc/evil.so} x
$ python -B pathscope_prover.py aud_optval_read_p.sh constants.env allowlist.txt
PATHSCOPE shell=aud_optval_read_p.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
rc=0
```

Worse, with a real command attached the tool issues a *positive* clean bill of health:

```
$ cat aud_optval_nice_n.sh
#!/bin/bash
nice -n ${LD_PRELOAD:=/etc/evil.so} cat "$ROOT/f"
...
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
rc=0
```

The composite does not save it — I fed the real prover output to
`SubprocessPathProver._interpret_output`:

```
aud_optval_read_p      prover_rc=0  composite=PASS  reason=prover_closed_and_allowlisted_lexical_scope
aud_subscript          prover_rc=0  composite=PASS  reason=prover_closed_and_allowlisted_lexical_scope
aud_for_list           prover_rc=0  composite=PASS  reason=prover_closed_and_allowlisted_lexical_scope
```

Surface size, measured by importing the module: **33 of 92 registered command specs carry at
least one data-role option, 161 such options in total** — `head, tail, touch, mkdir, cp, mv,
ln, chown, basename, du, df, stat, truncate, ls, install, mktemp, sort, uniq, cut, wait,
kill, set, printf, seq, date, read, mapfile, readarray, history, bind, complete, compgen,
ss` — plus the wrapper specs at `pathscope_prover.py:2733-2744` (`timeout`, `exec`, `nice`,
`ionice`, `stdbuf`), which I confirmed by execution (`aud_optval_stdbuf`, `aud_optval_nice_n`).

**(b) A subscripted assignment target defeats the guard's classifier.**
`parameter_assignment_effect` decides on `re.match(r"^[A-Za-z_][A-Za-z0-9_]*(?::?=)", expr)`
(`pathscope_prover.py:1330`), so anything between the name and the operator misses. Probed
directly against the real function:

```
${X:=v}      -> ASSIGNMENT_EFFECT      ${X[0]:=v}   -> NO_ASSIGNMENT_EFFECT
${X=v}       -> ASSIGNMENT_EFFECT      ${X[0]=v}    -> NO_ASSIGNMENT_EFFECT
"${X:=v}"    -> ASSIGNMENT_EFFECT      ${X[@]:=v}   -> NO_ASSIGNMENT_EFFECT
${X:=${Y}}   -> ASSIGNMENT_EFFECT      ${!X:=v}     -> NO_ASSIGNMENT_EFFECT
${X}${Y:=v}  -> ASSIGNMENT_EFFECT
'${X:=v}'    -> NO_ASSIGNMENT_EFFECT (correct: inert control)
${X:-v}      -> NO_ASSIGNMENT_EFFECT (correct: supported fallback)
```

This is on the **exact `:` carrier from design §10.1**, one bracket pair apart:

```
$ cat guard_colon.sh                      $ cat aud_subscript.sh
#!/bin/bash                               #!/bin/bash
: ${LD_PRELOAD:=/etc/evil.so}             : ${LD_PRELOAD[0]:=/etc/evil.so}
...                                       ...
UNRESOLVED line=2 kind=coverage            (no rows at all)
  reason=assignment_parameter_expansion_not_modeled
PATHSCOPE verdict=REJECT rc=3             PATHSCOPE verdict=PASS rc=0
  reason=static_resolution_incomplete       reason=closed_and_allowlisted_lexical_argv_scope
```

I did not execute a shell fixture (out of scope), so the bash semantics here are asserted
from documentation, not measured: for a name without the array attribute, bash's
`name[0]` designates the same storage as `name`, so `${LD_PRELOAD[0]:=v}` performs the same
assignment side effect as `${LD_PRELOAD:=v}`. Flagged in §7 as a claim I did not measure.
Finding (a) does not depend on it.

**(c) Contexts the traversal reaches but the guard does not.** All `PASS rc=0`, zero issues:

| fixture | script line |
|---|---|
| `aud_for_list` | `for i in ${LD_PRELOAD:=/etc/evil.so}; do :; done` |
| `aud_case_subject` | `case ${LD_PRELOAD:=/etc/evil.so} in *) : ;; esac` |
| `aud_heredoc_body` | `cat <<EOF` / `${LD_PRELOAD:=/etc/evil.so}` / `EOF` |
| `aud_herestring` | `cat <<< ${LD_PRELOAD:=/etc/evil.so}` |
| `aud_test_bracket` | `[ -n "${LD_PRELOAD:=/etc/evil.so}" ]` |
| `aud_dblbracket` | `[[ -n ${LD_PRELOAD:=/etc/evil.so} ]]` |

For contrast, these **are** correctly stopped (`rc=3`), which shows the traversal is
otherwise reaching the construct: subshell, command substitution, function body, pipeline
RHS, `&&`-list, redirection target, `--`-terminated operand, unknown command, assignment
RHS, `export`/`env` RHS, `trap` body, double-quoted path-free operand, and a
two-expansion token.

**Why this is REQUIRED and not a disclosed residual.** Residual §11.1 discloses only that
the guard "does not claim complete Bash coverage of every context in which an
assignment-bearing expansion could occur", and scopes the closure to "the registered
`scan_args` path". Routes (a) and (b) are *inside* `scan_args`, on registered commands, in
argv position. The design's own closing claim in §11 — "unmodeled assignment-effect argv
cannot silently cross the admission boundary" — is false as measured. Route (c) is gestured
at by §11.1, but §11.1's phrase "remains unproved parser/grammar coverage" reads as *stops
as a coverage issue*, whereas the measured behaviour is silent `PASS rc=0`.

This is the same shape as the four previous Pathscope cycles: the named finding was closed,
and the same class was found one step further out.

### 4.2 REQUIRED-2 — the reading-cardinality check is self-confirming

`file: MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py:2084-2089, 2349-2355`

Design §3.3: *"Independent cardinality checks require colon count `separator_count + 1` and
words count equal to the `\S+` match count before disposition accounting."* Design §4:
*"`S(v,r)` is the **independently counted** separator/match set."* Acceptance §12.3 lists
"independent reading cardinality" among the things that must run before PASS. Report §3
claims it was implemented.

What is implemented:

```python
expected_counts = (
    ("whole", 1),
    ("colon", len(colon_spans) if colon_separators else 0),
    ("words", len(word_matches) if words_active else 0),
    ("word-colon", len(word_colon_spans)),
)
```

and the check (2349-2355) compares `Counter(member.reading for member in members)` against
those. But `colon_spans`, `word_matches` and `word_colon_spans` are the **exact lists the
emission loops at 2045, 2057 and 2076 iterate**. The expected value and the artifact are
produced by the same statement. Apply the project's own test — *what would have to be true
for this check to fail?* — and the answer is "a typo inside a `for x in <list>: append`
loop". It cannot fail because the splitter under-split, which is the failure mode
conservation was bought to defend against.

I demonstrated this with three **source-level** mutations of the production splitter. The
implementer's M01–M15 all mutate the ledger *after* `Analyzer.run()`; none mutates the code
that builds it, so none can detect this.

Baseline (unmutated candidate): `f3_duplicate rc=1 members=3 faults=0`,
`f2_provenance rc=3 members=3 faults=0`, `f1_command_words rc=3 members=3 faults=0`,
`aud_prov_split_const rc=0 members=3 faults=0`.

```
S1_drop_last_colon_span   (splitter drops one colon span and its separator)
   f3_duplicate         rc=1 members=1 faults=0 | REJECT rc=1 path_outside_allowlist
   f2_provenance        rc=0 members=1 faults=0 | PASS rc=0   <-- false PASS
   f1_command_words     rc=3 members=3 faults=0 | REJECT rc=3
   aud_prov_split_const rc=0 members=1 faults=0 | PASS rc=0

S2_drop_span_keep_separator   (honest separator list retained; only the span dropped)
   f3_duplicate         rc=1 members=2 faults=0 | REJECT rc=1
   f2_provenance        rc=0 members=2 faults=0 | PASS rc=0   <-- false PASS
   f1_command_words     rc=3 members=3 faults=0 | REJECT rc=3
   aud_prov_split_const rc=0 members=2 faults=0 | PASS rc=0

S3_disable_words   (words_active forced False)
   f3_duplicate         rc=1 members=3 faults=0 | REJECT rc=1
   f2_provenance        rc=3 members=3 faults=0 | REJECT rc=3
   f1_command_words     rc=0 members=1 faults=0 | PASS rc=0   <-- false PASS
   aud_prov_split_const rc=0 members=3 faults=0 | PASS rc=0
```

Three points:

1. **Zero accounting faults in every arm.** The layer whose entire purpose is to notice a
   member that went missing notices nothing.
2. **S3 turns the F1 finding itself back on.** `f1_command_words` —
   `GIT_SSH_COMMAND="ssh evil.example"` — regresses from `rc=3` to `PASS rc=0` with one
   `whole` member classified `ALLOWED_WITH_REASON reason=whole_scalar_no_lexical_sink`.
   That is precisely the audit brief's third suggested direction: *a disposition that
   satisfies the counters while carrying no information.* It satisfies them perfectly.
3. **S2 shows the design's own formula was not implemented.** `separator_count + 1` would
   have caught S2; `len(colon_spans)` does not. The implementation is weaker than the
   accepted text, and the report does not disclose the deviation.

To be exact about severity: I could **not** construct an input that exploits this against
the current splitter — see §4.3, where every URI-swallowing attempt failed closed. This is
an unmet contract and a defence-in-depth failure, not a demonstrated input-level exploit.
It is REQUIRED because §12.3 is an explicit acceptance item, because report §3's claim that
"independent reading cardinality" runs is false as written, and because the whole authorized
value of an accounting layer is to stop depending on the splitter being right.

### 4.3 Attacks that failed — the layer held

These are recorded because a clean result after a real attempt is evidence too.

**Provenance cannot be inherited from a neighbour.** Identical rendered text, opposite
orders, and the ROOT-sourced member is correctly the first or the second accordingly:

```
LD_LIBRARY_PATH=$ROOT:/safe   colon.M0000 src=ROOT ALLOWED | colon.M0001 src=-    UNRESOLVED
LD_LIBRARY_PATH=/safe:$ROOT   colon.M0000 src=-    UNRESOLVED | colon.M0001 src=ROOT ALLOWED
```

A literal neighbour never picks up the constant's name, and an allowlisted literal with no
provenance terminates `UNRESOLVED_FAIL_CLOSED reason=member_exact_provenance_missing` rather
than being allowed. The validator recomputes provenance from the trace and re-derives the
candidate and rule match from `member.text` (2196-2276), so the expected value has an
independent origin — a real check.

**Raw slices are bound to the producing substring.** `f2_provenance`'s literal member
carries exactly `[{"origin":"literal","raw_end":39,"raw_start":26,"raw_text":"/safe/literal"}]`,
verified against `value.expression[26:39]`.

**No occurrence-ID collision constructible.** Measured directly, no duplicates:

```
aud_id_many_subs        rc=3 members=8 unique=8 values=8 dup=[]
aud_id_nested_subs      rc=3 members=4 unique=4 values=4 dup=[]
     A0000.V0000.whole.M0000  A0001.V0000.whole.M0000
     A0001.V0001.whole.M0000  A0002.V0000.whole.M0000
adjacent_cross_analyzer rc=3 members=4 unique=4 values=4 dup=[]
aud_id_same_line_many   rc=3 members=3 unique=3 values=3 dup=[]
f3_empty                rc=0 members=4 unique=4 values=1 dup=[]
```

Both nested-analyzer construction sites (`1508`, `3938`) pass `self.context`; only `main`
(`4343`) mints a fresh one. `merge` (1484-1501) rebases display lines only and never
rewrites an ID.

**No normalization or allowlist escape.** Twenty attempts to smuggle a path outside `/safe`
into an ALLOW — `//etc/escape`, `/safe//../etc/escape`, `/safe/./../etc/escape`,
`/safe/x/../../etc/escape`, backslash-escaped, `$'…'` ANSI-C, trailing slash, space-padded,
`/safexx/escape`, embedded newline, `~/evil.so` — every one returned `rc=1` FORBIDDEN or
`rc=3` UNRESOLVED. Endpoint side (`userinfo` confusion, scheme case, default port, trailing
dot in host) likewise: no false ALLOW.

**URI-authority colon swallowing.** `URI_PREFIX_RE = [A-Za-z][A-Za-z0-9+.-]*://[^/]*` is
greedy across colons, so a colon can be absorbed and a member never split — the one
structural way to exploit REQUIRED-2 from input alone. Eight constructions
(`http://127.0.0.1:8790:/etc/escape`, `$ROOT/a:http://h:/etc/escape`,
`$ROOT/l:x://y:z:/etc/escape`, `file://x:/etc/escape`, `$URL:/etc/escape`, …) all failed
closed at `rc=1` or `rc=3`, mostly via `member_normalization_failed`. I could not reach
`rc=0`.

**Record forging.** All variable-content fields are `b64u:`-encoded, whitespace-free tokens;
a value whose text is literally `A0000.V0000.colon.M0000` produced a normal conserved single
member and could not inject a row.

**Composite adjudication on real prover output** behaved as designed on twelve cases,
including the new fourth semantic arm
(`f1_command_words → STOP / prover_member_resolution_incomplete`),
`literal → FAIL / prover_forbidden_operand`, `green` and `f3_empty → PASS`.

---

## 5. Findings

### REQUIRED-1 — the assignment-effect admission guard is bypassable inside its own route
`pathscope_prover.py:2533-2534` (data-role early return), `2645`/`2685` (option-value
consumption), `1330` (name-only regex).
`${LD_PRELOAD:=/etc/evil.so}` reaches `PASS rc=0` with zero coverage issues via any
data-role option operand on 33 of 92 registered specs plus the wrapper specs (161 options),
via a subscripted target `${LD_PRELOAD[0]:=…}` on the exact `:` carrier of design §10.1, and
via `for`-lists, `case` subjects, heredoc bodies, here-strings and `[`/`[[` tests. The
composite passes these through. Evidence §4.1. Residual §11.1 does not disclose the first
two, and the §11 closing claim that "unmodeled assignment-effect argv cannot silently cross
the admission boundary" is falsified.

### REQUIRED-2 — the reading-cardinality invariant cannot fail for the reason it exists
`pathscope_prover.py:2084-2089` with `2349-2355`.
`expected_counts` is `len()` of the very lists the member-emission loops iterate, so the
"independent cardinality check" of design §3.3/§4 and acceptance §12.3 is not implemented;
the design's stated `separator_count + 1` formula is not used either. Three source-level
splitter mutations each produce a false `PASS rc=0` with **zero** accounting faults, one of
them reinstating the F1 finding. Evidence §4.2. Report §3's claim that independent reading
cardinality runs is incorrect as written.

### NIT-1 — mutation arm M23 is tautological
`pathscope_option_c_qa.py:641-644`. It takes the candidate's own output, substitutes
`sources=ROOT` → `sources=ROOT,ROOT`, then asserts the result differs from the original.
That is true by construction and proves nothing about the prover. **No repair required**:
the property M23 is supposed to defend — argv-only projection byte identity — *is* genuinely
checked twenty lines earlier at `637-640`, where the frozen-R5 and candidate outputs are
compared for real, and I reproduced that comparison independently.

### NIT-2 — M16 does not demonstrate the arm it removes
`pathscope_option_c_qa.py:511-526`. With the member-unresolved arm replaced by `elif False:`
the composite STOPs for `prover_pass_terminal_mismatch`, i.e. a *different* check catches it.
The arm's own discriminating power is untested. Safety is preserved either way; no repair
required.

### NIT-3 — the third changed source has no eol pin and no published identity
`WPI_PREREG_DRAFT_ROUND1/.gitattributes` pins `pathscope_prover.py` and
`composite_pathproof.py` to `text eol=lf` but not `pathscope_option_c_qa.py`, which is
therefore governed by the root `* text=auto`. Working tree 25576 B CRLF
`A86636BA…F2353`; Git blob 24923 B LF `7468E05F…C76D1`. No published digest depends on it —
I reproduced the entire mutation transcript from the CRLF working-tree copy — but this is
the exact recorded-hash-form ambiguity that has already caused three defects here, and the
runner's identity appears in neither identity table.

### NIT-4 — accounting faults are deduped across nested analyzers
`pathscope_prover.py:1499-1501`. `merge` appends a nested fault only `if fault not in
self.accounting_faults`, so two structurally identical faults carrying `value_id=None,
member_id=None` collapse and `accounting_fault_count` under-reports multiplicity. It cannot
produce a PASS — the summary is `FAIL` and rc 3 regardless.

### NIT-5 — residual §11.10 confirmed live and correctly scoped
Measured: `c2_uri_allow` gives prover `PASS rc=0` with
`ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL`,
and the composite returns `STOP / prover_endpoint_disposition_missing`. So the composite
currently cannot accept **any** report containing an allowed ENDPOINT projection row. This
over-STOPs and cannot produce a false PASS, exactly as §11.10 says; it does not block the
mandated suite because RP6-P0 and RP7-WPI-RO are rc 3 on other grounds. Honestly disclosed.

---

## 6. Is the class closed?

**No.**

The redesign closes a great deal, and I want to be precise about what it does close, because
the answer is not "this was a wasted round":

- The R5 defects are genuinely dead. `pool` text dedupe, the single-empty Boolean, the
  RHS-wide source union and the missing dispositions are all gone, and the checks that would
  catch their return use independent inputs — provenance is recomputed from the trace, the
  candidate and rule match are re-derived from `member.text`, and `Counter(M)==Counter(D)`
  plus global ID uniqueness are real constraints on real data. Post-hoc corruption of the
  ledger faults in all fifteen arms; I reproduced every one.
- F1, F2 and F3 as filed are closed and stay closed under my own re-measurement.
- The regression contract is honest to the row: 109 cases, exactly two authorized rc
  changes, 60 declared byte-identical blocks that are exactly the 60 actually identical
  blocks, and 11 projection deltas that are exactly the 11 declared.

What is not closed is the thing the brief asked about. Conservation quantifies over
*admitted* values, and the admission boundary still has open doors: the same
`${NAME:=value}` construct the guard was built for walks straight through a data-role option
operand, a subscripted target, a `for`-list or a heredoc and comes out the other side as
`PASS rc=0` — in one case with a reassuring `ALLOW-LEXICAL` row attached. And the property
that would have detected an incomplete split — the one place the design explicitly demanded
an *independent* count — was implemented as a comparison of a list against its own length.

That is the fifth appearance of one pattern: the named findings were closed, and the same
class was found one step further out.

**What I am least sure about.** Two things.

First, whether REQUIRED-2 is reachable from input alone. I attacked it hard and failed — the
URI-swallowing route, which is the only structural under-split I could find, fails closed on
normalization every time. So a reader could reasonably call REQUIRED-2 a documentation
defect plus a defence-in-depth gap rather than a live hole. I kept it REQUIRED because §12.3
is an explicit acceptance item, because report §3 states the check runs when it does not, and
because the accounting layer's entire purchase was independence from splitter correctness.
If Barış disagrees with that weighting, the honest minimum is to correct the two claims.

Second, the bash semantics of `${NAME[0]:=value}` on a scalar. I did not execute a shell —
that is outside this audit's scope — so I assert it from documentation rather than
measurement. If it turns out not to assign, finding (b) weakens. Findings (a) and (c) are
measured end to end and do not depend on it.

I did not manufacture a finding to look thorough. REQUIRED-1 is six lines of A/B output away
from anyone who looks, and I would have written PASS if the option-value probe had come back
rc 3.

---

## 7. What I could not verify

1. **The published PowerShell harness, run verbatim.** This session's tool policy refuses to
   spawn a nested PowerShell process. I extracted the harness, proved its byte identity
   (37382 B / `61FB09D2…FC7`, matching the report), and re-implemented its measurements in
   Python; all eight transcript digests, the determinism pair, the 109-case rc map, the
   60-block byte-identity set, the seven retired determinism digests and all 44 mutation
   lines reproduced. What I did **not** exercise is the PowerShell script's own control flow
   — its `throw` paths, `Assert-Sha256`, the transcript-leak assertion and its outer rc/stderr
   behaviour. The report's `OUTER_RC=0 STDOUT_BYTES=7661 STDERR_BYTES=0` is unconfirmed.
2. **An actual Python 3.12 interpreter.** Reproduced the report's claim exactly:
   `py -3.12 -V` → `rc=103`, "No suitable Python runtime found". All three sources do parse
   under `ast.parse(..., feature_version=(3,12))` — I ran that myself — and everything else
   ran on CPython 3.14.2.
3. **Shell execution semantics.** No fixture was executed as shell, per scope. The
   `${NAME[0]:=value}` claim in REQUIRED-1(b) is documentary.
4. **`SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md`** is not present in this worktree at
   `ec98cbd4`. I recovered it from commit `a4833939` in the same repository's history and
   applied its three questions; that is the origin of REQUIRED-2.
5. **`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` §D1** — I read the authorization as quoted in
   the design and report; I did not independently locate the owner file.
6. **Out of scope, not examined:** RP6, RP7, transport, SEC102, and the composite's
   behaviour above `_interpret_output` (`prove`, member aggregation).
7. **Exhaustiveness.** My attack batteries are ~90 fixtures. Absence of a further escape is
   not proof of absence — particularly for REQUIRED-1 route (c), where I enumerated shell
   contexts by hand rather than from a grammar.

---

## 8. Scope compliance

Read-only except this one file. No `add`, `commit`, `checkout`, `reset`, `stash`, `merge`,
`push`, `amend` or `worktree`. `git status --porcelain` empty before and after; HEAD
unchanged at `ec98cbd4d629d7e035f99da70d5e73fb7f610da1`. Scratch work confined to
`C:\tmp\psaudit`. Source mutants for §4.2 were written to a system temp directory and never
to the repository. No host, network, deployment, service, credential, broker/exchange, ARM,
order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push or economic action.
`C:\LAB\Tradingview_LAB_CLEAN`, `C:\R7FINAL`, `C:\RO` and `C:\PSC` were not touched.
