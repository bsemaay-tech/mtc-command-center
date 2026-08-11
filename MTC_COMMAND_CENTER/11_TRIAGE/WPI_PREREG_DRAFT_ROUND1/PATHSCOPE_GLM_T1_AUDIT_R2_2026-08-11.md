# GLM-5.2 T1 audit — path-scope prover, repair round 2

Date: 2026-08-11
Auditor: GLM-5.2 via the Z.AI Coding Plan route (canonical auditor 4).
Role: T1 second-opinion / supplemental for this round.
Tier: T1 — local-only Stage-1 static analysis. No host, network, trading, Pine,
parity, MTC, deployment, transport, or runtime action.

## Why GLM carries this round (Codex unavailability)

Codex `gpt-5.6-sol` — the normal flagship auditor of record — could not audit this
artefact: its provider content filter terminates the run while merely reading
`pathscope_prover.py`, because the prover's sink-detection source carries attack
grammar (forbidden-path tables, exfil URL patterns, ssh/nss host grammar) **as
data**. That is a concrete tooling blocker, not a finding. Per the audit-tier
policy the T1 conditional second-opinion slot is authorised when the diff exceeds
~300 lines; this repair (49 820 B → 122 446 B) does. The Lead records Codex's
unavailability. GLM did not write these bytes (`claude-opus-5` did), so the
no-self-audit rule is satisfied.

## Audited identity (verified independently)

```
HEAD                          = 7fb228ce1f124788b87601a77fd361d52b69a037
pathscope_prover.py bytes     = 122446
pathscope_prover.py sha256    = 890016F0B9A8CDE4EED33F8733F69055471B07C6096F6BC07450457E6C52AF1D
```

Matches the kickoff and `STATUS_PATHSCOPE.md` exactly. `pathscope_prover.py` is a
tracked, unmodified file; it is not under concurrent edit. The untracked files in
the same directory at session start are unrelated run logs, not audit bytes.

## ⚠ Read-only / non-execution disclosure (governs the whole verdict)

**GLM could not execute the suite in this session.** The harness is a PowerShell
script (`SELF_QA_PATHSCOPE.md` §"The harness, verbatim"). In this session the
sandbox gates (a) `powershell`, (b) writes outside the repo, and (c) every
`python` invocation other than `--version`. GLM therefore could not run the
published harness, the reconstructed round-1 prover, the round-2 prover, or any
adversarial fragment. No shell fixture was executed, no host contacted, no
network call made — this is the intended Stage-1 posture, but it is also the
reason the execution steps below are marked `PENDING-LEAD-EXECUTION`.

Per `AGENTS.md` four-auditor rule 1 ("a canonical auditor that cannot execute the
mandated test suite must return BLOCK; non-execution is never acceptance") and
rule 4 (the known GLM failure mode: PASS-WITH-NITS printed while unable to run the
suite), **this opinion is SUPPLEMENTAL, not acceptance, and no PASS is printed on
a read.** The kickoff's tail explicitly provides the sanctioned escape for this
GLM slot: mark the run steps `PENDING-LEAD-EXECUTION` and the Lead (who holds
powershell/python authority) runs them.

Everything below the line is therefore a **static code review** of
`pathscope_prover.py` plus the published transcripts — valuable, but not a
substitute for execution.

---

## Contract point 1 — re-run the published harness

**Status: `PENDING-LEAD-EXECUTION`.** GLM could not run it. The Lead should run,
verbatim, the single command in `SELF_QA_PATHSCOPE.md` §"How to reproduce":

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r2_harness.ps1"
```

(The fenced block under §"The harness, verbatim" is that `.ps1`, in full.)

What acceptance-by-execution must show, and what GLM checked by reading:

1. **62 fixture cases + 4 real-block arms, both provers.** The harness `CASES`
   list and the real-block loop are self-contained; the RED transcript
   (`SELF_QA_PATHSCOPE.md` §"Complete RED transcript", 511 lines) runs the
   reconstructed round-1 blob `3f0820a9…`, the GREEN transcript (644 lines) runs
   the working-tree repair. GLM confirmed by reading that the published
   transcripts carry one `=== name ===` / `COMMAND_RC=N` block per case in the
   same order as `CASES`, and that the four real-block arms are present in both.
   *Reproduction is the Lead's to perform.*

2. **RED-before-GREEN (D026).** The four CRITICAL rows are visible in the
   published transcripts: e.g. `trap` is `rc 0 — (no row)` on RED and
   `rc 1 — /etc/passwd FORBID` on GREEN; `find_exec` is `rc 0 — /safe ALLOW` on
   RED and `rc 1 — /etc/passwd FORBID; /safe ALLOW-LEXICAL` on GREEN. The RED
   column is taken from the **pinned blob**, so it stays reproducible after the
   repair commits — this satisfies D026's "RED against the pre-fix behaviour"
   without a risky in-place reversion. *GLM read-confirms; execution is the
   Lead's.*

3. **Determinism.** The published tail reports `equal=True` with identical
   sha256 pairs for `find_exec`, `RP6-P0`, `RP7-WPI-RO`. GLM independently
   confirms the code is deterministic by construction: `output_report` emits
   issues via `sorted(...)` (line 2696), path/endpoint rows via `sorted(table)`
   (line 2719), and sorted evidence/source sets (lines 2728–2731) — there is no
   insertion-order or set-iteration dependence in the output path. *Execution
   confirmation is the Lead's.*

GLM could not add a reproduction transcript of its own. That is the single
biggest gap in this audit and the reason it is supplemental.

## Contract point 2 — adversarial silent-sink hunt (static)

The round-1 CRITICALs were all one class: a Bash fragment reaches a
filesystem/network primitive while the prover emits no path, no coverage record,
and `verdict=PASS rc=0`. GLM's static hunt targeted the places a *new* such class
could hide after the repair, and traced each through the code.

**Structural reason no silent sink survives.** The verdict logic in
`output_report` (lines 2741–2748) is:

- any `Issue` (parse/provenance/coverage/path/endpoint) ⇒ `REJECT rc=3`;
- else any forbidden path/endpoint ⇒ `REJECT rc=1`;
- else — and only else — `PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope`.

So a `PASS rc=0` is reachable **only if every construct in the input was modelled
and every resolved path/endpoint is allowlisted with zero issues**. The only
operands that can be dropped without an issue are those of a `path_free` command
(`scan_args` lines 1295–1301), and `path_free` (lines 804–817) is `True` only when
the command declares no path/net/shell/fd/form/unmodeled option and every
positional role is `data`. GLM checked **every** `path_free` entry (the block at
lines 1006–1059): each is a shell builtin/utility whose argv operands are not file
paths (`echo`, `printf`, `:`, `true`, `set`, `shopt`, `kill`, `wait`, `seq`,
`date`, `popd`, `dirs`, …). File-reading commands (`cat`, `head`, `tail`, …)
default to `rest="path"`, so their positionals are recorded. There is therefore
no argv route from a `PASS rc=0` to a real primitive.

**Vectors GLM traced (each resolves to REJECT, not silent PASS):**

| # | Fragment | Code path | Predicted verdict |
|---|----------|-----------|-------------------|
| A | `command cat /etc/passwd` | `analyze_wrapped` recurses via `analyze_command(args[start:])` (1562); `scan_prefix` stops at first non-option (1584) | `FORBID /etc/passwd` rc 1 |
| B | `builtin cat /etc/passwd` | same recursion (1562); `builtin` has no flags so any `-X` STOPs in `_apply_cluster` | `FORBID /etc/passwd` rc 1 |
| C | `exec cat /etc/passwd` | `scan_prefix` → `start<len` → recurse (1562); pure-redirect `exec >file` returns early (1557–8) | `FORBID /etc/passwd` rc 1 |
| D | `timeout 5 cat /etc/passwd` | `scan_prefix`, `start+=1` skips duration (1549), recurse | `FORBID /etc/passwd` rc 1 |
| E | `env cat /etc/passwd` | `analyze_wrapped("env",…)` consumes env-options/assignments then recurses (1527) | `FORBID /etc/passwd` rc 1 |
| F | `sudo cat /etc/passwd` | emits privilege-transition STOP (1530–2) **and** analyzes operands (1538) | rc 3 + `FORBID` |
| G | `dd if=/etc/passwd of=/safe/x` | `dd` not registered → opaque STOP (2411) + arg scan (2413–23) | rc 3 (STOP; path not extracted but not silent) |
| H | `rsync /etc/passwd /safe/x` | not registered → opaque STOP (2411) | rc 3 |
| I | `cp --copy-contents /etc/passwd /safe/x` | unlisted option → `role` None → coverage STOP (1320–4) | rc 3 |
| J | `sort -no /safe/out /etc/passwd` | short cluster: `-n` flag, `-o` value-takes remainder → remainder empty → consumes next token; matches getopt (1402–9) | `ALLOW-LEXICAL /safe/out` + `FORBID /etc/passwd` rc 1 |
| K | `cat <(cat /etc/shadow)` | `(`,`)` are operators (165); `normalize_control_tokens`/command-split either treat `(...)` as a subshell group (inner analysed → FORBID) or `<` consumes `(` as a redir target and `/etc/shadow` falls through as a positional to the outer `cat` → FORBID. Worst case adds bogus `ALLOW-LEXICAL` rows `(`/`cat`/`)` but never hides `/etc/shadow` | `FORBID /etc/shadow` rc 1 |
| L | `eval 'cat /etc/passwd'` | `eval` → coverage STOP (2322–4); argument not re-analysed (conservative) | rc 3 |
| M | `python3 /etc/passwd` | `analyze_interpreter` records the script operand as a path **and** STOPs | rc 3 + path row |
| N | `cat <<-EOF` + tab body + `$(cat /etc/shadow)` | `_consume_heredocs` strips leading tabs for `<<-` (289), harvests substitutions only for unquoted delimiter (300–3) | `FORBID /etc/shadow` rc 1 |

GLM's prediction for every row is **REJECT, never `PASS rc=0`**. The four that
most warrant the Lead's execution confirmation are A–F (wrapper recursion),
J (short cluster), and K (process substitution) — those are where a recursion or
tokenisation gap could hide. GLM traced them to non-silent outcomes, but execution
is the proof.

**New fixtures GLM recommends the Lead add to `SELF_QA_PATHSCOPE.md`** (one-line
each, no expectation of edit during this read-only audit — for the next revision):

```
wrapper_command    #!/bin/bash ; command cat /etc/passwd
wrapper_builtin    #!/bin/bash ; builtin cat /etc/passwd
wrapper_exec       #!/bin/bash ; exec cat /etc/passwd
wrapper_env        #!/bin/bash ; env cat /etc/passwd
procesub           #!/bin/bash ; cat <(cat /etc/shadow)
dd_opaque          #!/bin/bash ; dd if=/etc/passwd of=/safe/x
unlisted_opt       #!/bin/bash ; cp --copy-contents /etc/passwd /safe/x
cluster_value      #!/bin/bash ; sort -no /safe/out /etc/passwd
heredoc_dash_tab   #!/bin/bash ; cat <<-EOF ; $(cat /etc/shadow) ; EOF   (unquoted)
```

None of these is a *known* silent sink; they close the coverage map for the
constructs a re-audit is most likely to probe next.

## Contract point 3 — judgment of finding 6 (ALLOW-LEXICAL honesty)

**Finding 6 is honestly and machine-readably repaired as a DISCLOSURE; the
residual (symlink/mount binding) is correctly recorded and acceptable for a T1
tool.** Anchors:

- `SEMANTICS_LINE` (2671–2674) is printed **unconditionally** on every run
  (2704): `semantics=lexical_argv_scope symlink_resolution=not_established
  mount_boundary=not_established host_probe=none`.
- The filesystem allow token is `ALLOW-LEXICAL`, not `ALLOW` (2717); network
  stays `ALLOW` because an endpoint literal is the address itself, not a lexical
  tree member.
- A clean run reports `reason=closed_and_allowlisted_lexical_argv_scope` (2747);
  the unconditional `closed_and_allowlisted` string from round 1 no longer exists
  on the PASS path.
- The published GREEN transcript shows `symlink_lexical` (`cat "$ROOT/link/passwd"`)
  emitting exactly `verdict=ALLOW-LEXICAL … PASS rc=0
  reason=closed_and_allowlisted_lexical_argv_scope` under the semantics line.

The second half of the round-1 required repair — *binding* the lexical result to
a symlink/mount-chain proof — is **not** in this tool and is recorded as residual
R1 in `PATHSCOPE_REPAIR_R2_REPORT.md`. GLM agrees a static reader of frozen bytes
genuinely cannot perform that binding, and that inventing a host probe here would
be exactly the §10.2 defect the contract forbids. Per contract point 3, "an
honestly-scoped weaker claim is acceptable for a T1 tool whose composite proof is
SEC102." No run presents lexical membership as an unconditional host ALLOW any
more. **Finding 6: closed (as disclosure + residual R1).**

## Contract point 4 — determinism + fail-closed

- **Fail-closed on unmodeled syntax.** `ShellLexer` raises `LexError` on
  unterminated quotes/expansions/heredocs (e.g. 278, 438, 240, 257, 296);
  `Analyzer.run` catches it and records a `KIND_PARSE` issue (2605–2607), which
  forces `REJECT rc=3` (2741–2743). Unregistered commands, unlisted options,
  unmodeled expansions, arrays, globs, arithmetic and `$()`-into-path all raise
  specific coverage/path issues → rc 3. The direction of error is uniformly
  conservative (over-report or STOP).
- **Determinism.** Output ordering is `sorted(...)` throughout `output_report`
  (2696, 2719, 2728–2731); there is no nondeterministic iteration on the output
  path. The published `equal=True` determinism lines are consistent with this.
  Determinism is reproducibility, not soundness.

## Residuals (GLM concurs with all seven)

GLM reviewed `PATHSCOPE_REPAIR_R2_REPORT.md` residuals R1–R7. All seven are
either disclosed limits (R1 lexical-vs-host; R7 renamed count fields) or
conservative over-reporting (R2 function positional dataflow — sound only because
every positional fails closed; R3 alias expansion — unexpanded alias STOPs; R4
`dirname`/`basename` over-report; R5 inline-value provenance; R6 finite registry
→ resolved set is a lower bound). **None is a silent false-ALLOW.** R2 deserves a
standing note: it is sound *only* while every positional expansion stays
fail-closed; if a future change lets a positional reach a sink without a STOP, R2
becomes a live finding.

## Coverage observations (nits, not findings)

- `date` (lines 1054–1056) is grouped under the comment "builtins whose complete
  accepted grammar carries no path" but declares `path="-f --file -r --reference"`.
  The computed `path_free` is correct (`False`); only the grouping comment is
  imprecise. No behavioural impact.
- Process substitution `<(...)` (contract point 2, row K) has no explicit handler
  and no fixture. GLM traced it to a non-silent outcome; a fixture would make
  that explicit.
- `dd`/`rsync`/`cpio`/`openssl`/`base64`/`mount`/`su` are not registered → opaque
  STOP. That is safe, but for a tool that will be pointed at real release scripts,
  adding even minimal `Spec`s for `dd` (path `if=`/`of=`) and `rsync` would turn a
  blind STOP into a reported path set. Optional, not required.

## Verdict

**SUPPLEMENTAL — non-accepting; execution `PENDING-LEAD-EXECUTION`.**

- GLM found **no silent-sink defect** in static review. The repair closes the
  round-1 CRITICAL class by construction: `PASS rc=0` requires all issue counts
  zero, the only silently-dropped operands belong to genuinely path-free
  builtins, unregistered commands and unlisted options STOP, wrappers recurse,
  and redirections/expansions/heredocs/tilde are modelled.
- Finding 6 is honestly disclosed; residuals R1–R7 are conservative-direction.
- **GLM could not execute the suite**, so per four-auditor rule 1 / contract
  point 5 this opinion is **not acceptance** and no PASS is printed on a read.

**Lead action to close the round.** Run the published harness verbatim
(point 1). If (a) the RED/GREEN transcripts reproduce, (b) determinism holds, and
(c) the contract-point-2 fragments above all resolve to `REJECT` (never
`PASS rc=0`), the appropriate label for this round is **PASS-WITH-NITS**, the
single nit being: add a process-substitution (and the recommended wrapper)
fixtures so the coverage map is explicit. If any of those fragments instead
returns `PASS rc=0`, that is a CRITICAL silent sink and the round is
`REQUEST_CHANGES`.

## Clean-tree proof

Read-only audit; the only repo change is this one sanctioned deliverable.

Prover bytes unchanged (re-hashed at end of audit):
```
890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d  pathscope_prover.py   (= kickoff / STATUS, unchanged)
```
Scratch removed — `_glm_scratch/` and `.glm_audit_probe.tmp` no longer exist;
`git status --porcelain | grep glm_scratch` → `NONE`.

Pathscope-scope `git status --porcelain` at end of audit (the 8 `*_RUN_*.log`
rows were already untracked at session start; the only new row is this file):
```
?? .../PATHSCOPE_GLM_T1_AUDIT_R2_2026-08-11.md     <-- the one sanctioned deliverable
?? .../PATHSCOPE_R2_CODEX_AUDIT_RUN_2026-08-11.log      (pre-existing)
?? .../PATHSCOPE_R2_CODEX_AUDIT_V2_RUN_2026-08-11.log   (pre-existing)
?? .../PATHSCOPE_R2_MAX_RUN_2026-08-11.log              (pre-existing)
?? .../PREREG_A_CODEX_RUN_2026-08-11.log                 (pre-existing)
?? .../PREREG_B_CODEX_RUN_2026-08-11.log                 (pre-existing)
?? .../PREREG_MERGE_R3_CODEX_RUN_2026-08-11.log          (pre-existing)
?? .../SEC102_R1_CODEX_RUN_2026-08-11.log                (pre-existing)
?? .../SEC102_R2_CODEX_RUN_2026-08-11.log                (pre-existing)
```
`pathscope_prover.py`, `SELF_QA_PATHSCOPE.md`, `STATUS_PATHSCOPE.md`, and
`PATHSCOPE_REPAIR_R2_REPORT.md` are tracked and unmodified. No git mutation was
performed. The pre-existing dirty entries elsewhere in the tree
(`WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh`, `SELF_QA_RP7.md`, and untracked run logs) are
from other concurrent sessions and are not part of this audit scope.
