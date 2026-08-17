# PATHSCOPE — Claude Pro T1 EXECUTION audit, round 2 (flagship EXECUTION slot)

Date: 2026-08-12
Auditor: `claude-opus-5`, effort **high** (T1), default Claude Pro account — fresh session,
non-implementer (Max implemented r2; this session did not).
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`
Mode: read-only on the repository. The only repository byte written by this lane is this file.
No git mutation, no host contact, no network. Shell fixtures were never executed — they are
input **data** to a static reader only.

## VERDICT: REQUEST_CHANGES

One **CRITICAL** surviving silent sink was constructed and confirmed under audit contract item 2,
which states: *"Any surviving silent sink is CRITICAL."* The finding is C-1 below: **variable
assignment prefixes are discarded without a path record and without a coverage record**, so a
fragment that makes the dynamic loader open an out-of-allowlist path still returns `PASS rc=0`.

This is not a regression and it does not retract the round-2 repair, which I independently
re-executed and found substantial and honest: 13 of the 16 round-1 zero-record rows are closed,
every filesystem ALLOW is now disclosed as lexical, determinism is exact, and the fail-closed
coverage machinery works everywhere it is reached. C-1 is a **new** instance of the same defect
class the repair was built to eliminate, in a construct the repair's `Spec` registry never sees.

Because a CRITICAL is open, pathscope does **not** yet hold a flagship EXECUTION acceptance.
I am not stating the acceptance sentence from contract item 5.

---

## 1. Identity — re-derived before anything else

| artefact | expected (kickoff) | re-derived here | match |
|---|---|---|---|
| `pathscope_prover.py` bytes | 122446 | 122446 | ✅ |
| `pathscope_prover.py` SHA-256 | `890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d` | `890016f0b9a8cde4eed33f8733f69055471b07c6096f6bc07450457e6c52af1d` | ✅ |

I audited exactly the nominated bytes.

## 2. Execution — the published harness, run verbatim

The harness was **not retyped**. I extracted lines 64–319 of
`SELF_QA_PATHSCOPE.md` (the fenced block between the ```` ```powershell ```` at `:63` and the
closing fence at `:320`) programmatically, wrote them to `%TEMP%\pathscope_r2_harness.ps1`
(14364 B, SHA-256 `CEE2D39FC0C5ABDBB33E633C177690BCEF865EBA3472610BDFC27A6D68887C17`,
256 lines, zero non-ASCII), and invoked the published command at `:32-34`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r2_harness.ps1"
```

Exit code 0. Stdout reproduced the documented transcript at `SELF_QA_PATHSCOPE.md:43-51`
**byte for byte, including all three determinism digests**:

```text
R1_BASELINE bytes=49820 sha256=3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6
R2_REPAIRED bytes=122446 sha256=890016F0B9A8CDE4EED33F8733F69055471B07C6096F6BC07450457E6C52AF1D
BLOCK RP6-P0.sh bytes=107252 sha256=A090AE736CBECD9973E8AE948B052504B21CBE8B61602F4B5AC592394FAD0617 git_blob=3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c
BLOCK RP7-WPI-RO.sh bytes=99903 sha256=11621044D0ADC21AF93E1CFC7B88EF88DE8ACA4683A69AB16CBC542A124141A4 git_blob=5c9a2f597cceaef80d1cbd0fc100732f4b216cf5
WROTE ...\pathscope-repair-r2\RED_R1.txt lines=511
WROTE ...\pathscope-repair-r2\GREEN_R2.txt lines=644
DETERMINISM find_exec rc1=1 rc2=1 equal=True sha1=11c5cb8e...67dd sha2=11c5cb8e...67dd
DETERMINISM RP6-P0 rc1=3 rc2=3 equal=True sha1=66959360...dc0e sha2=66959360...dc0e
DETERMINISM RP7-WPI-RO rc1=3 rc2=3 equal=True sha1=1ebedc0d...7f4b sha2=1ebedc0d...7f4b
```

### Real counts (measured, not copied)

| quantity | claimed | measured | match |
|---|---|---|---|
| RED_R1.txt lines | 511 | 511 | ✅ |
| GREEN_R2.txt lines | 644 | 644 | ✅ |
| runs per suite | 62 fixtures + 4 real-block | **66** blocks parsed in each transcript | ✅ |
| determinism `equal=` | True ×3 | True ×3 | ✅ |

**D026 RED-before-GREEN discipline holds structurally**: the harness reconstructs the round-1
artefact from pinned blob `3f0820a9…` and calls `Invoke-Suite $R1` (line 303) *before*
`Invoke-Suite $TOOL` (line 304). RED is produced from bytes that cannot contain the repair.

### Published D026 table vs. executed reality

I mechanically parsed all 62 fixture rows of the D026 table (`SELF_QA_PATHSCOPE.md:329-392`),
extracted the `rc N` from both the R1 RED and R2 GREEN cells, and compared against the rc values
in the transcripts I produced.

```
CHECKED=62 RC_MISMATCHES=0
```

**Every published rc in both columns matches execution.** The table is not fabricated.

### Determinism — stronger than the published claim

The harness's own check re-runs three single cases. I went further and re-ran the **entire
harness** a second time as an independent process, then compared whole-transcript digests:

| artefact | run 1 | run 2 | equal |
|---|---|---|---|
| `RED_R1.txt` | `2E61BFE2…7CDED5` | `2E61BFE2…7CDED5` | ✅ |
| `GREEN_R2.txt` | `02ECC4C0…8DB8638` | `02ECC4C0…8DB8638` | ✅ |

All 66 runs × 2 suites are byte-identical across independent invocations. Determinism is
**confirmed at a higher standard than the document claims**.

## 3. MATERIAL DISCLOSURE — the four real-block runs are historical, not current coverage

I re-derived both columns rather than trusting the kickoff.

| block | pinned identity actually run by the harness | current repository identity | same? |
|---|---|---|---|
| `RP6-P0.sh` | 107252 B, `A090AE73…0617`, blob `3c7b7d26…` | **110817 B, `5132bacd…3330`, blob `4729b8fa…`** | ❌ |
| `RP7-WPI-RO.sh` | 99903 B, `11621044…41A4`, blob `5c9a2f59…` | **108301 B, `0e93f90d…9e62`, blob `d886148392…`** | ❌ |

At the moment of measurement both current files were committed at HEAD (`git rev-parse HEAD:<path>`
equalled `git hash-object <path>` for both) — and their HEAD blobs are **not** the pinned blobs the
harness reconstructs. Deltas were +3565 B (RP6) and +8398 B (RP7).

> **The "current" column moved while this audit was running.** At the closing delta capture,
> a concurrent lane had modified `RP7-WPI-RO.sh` again: it is now **108376 B, SHA-256
> `7d8283ef…aeb8`, worktree blob `8fc40798…`, uncommitted** (HEAD still `d886148392…`). RP6-P0.sh
> was unchanged at `5132bacd…`. The audited prover bytes were re-verified unchanged at
> `890016f0…af1d`, so this audit's target held throughout; only the comparison column moved.
> This makes the point of this section sharper rather than weaker: "current RP6/RP7 bytes" is a
> moving target owned by other lanes, which is precisely why a Stage-1 proof is taken over frozen
> blobs — and equally why a run over those frozen blobs can never be cited as current coverage.

**Consequently, and stated explicitly as the kickoff requires: the four real-block runs are
HISTORICAL PINNED REGRESSIONS. They establish determinism and RED-vs-GREEN discrimination for
the prover. They establish NOTHING about the prover's behaviour on today's RP6/RP7 bytes, and no
result from them may be cited as current-block coverage.**

I record — without endorsing it as coverage — that on the pinned bytes both real blocks fail
closed rather than passing:

| run | rc | resolved fs paths | unresolved paths | coverage issues |
|---|---|---|---|---|
| RP6-P0 + `placeholder.constants` | 3 `input_parse_error` (placeholder guard fires at line 7) | — | — | — |
| RP7-WPI-RO + `placeholder.constants` | 3 `input_parse_error` (placeholder guard fires at line 7) | — | — | — |
| RP6-P0 + `real.constants` | 3 `static_resolution_incomplete` | 1 | 3 | 35 |
| RP7-WPI-RO + `real.constants` | 3 `static_resolution_incomplete` | 3 | 34 | 38 |

Neither pinned block is provable by this prover; both are rejected. The placeholder guard
correctly refuses `<ALLOCATE-AT-DISPATCH>` before analysis.

## 4. Answers to the two questions the kickoff put to me

### Q1 — sixteen versus four: wording defect, or an overstated coverage claim?

**Answer: it is a wording/category defect. The round-1 CRITICAL count of four is correct and is
NOT understated, and the sentence does NOT overstate what the repair closed.**

Evidence:

- The round-1 audit of record (`PATHSCOPE_CODEX_T1_AUDIT_2026-08-10.md`) declares exactly four
  CRITICALs, at `:78`, `:112`, `:144`, `:173`. Four **findings** is right.
- My transcript confirms the claim-audit's `F-3`: the `rc 0` / zero-record pattern appears in
  **16** RED rows, exactly the sixteen named — `pushd`, `pushd_forbidden`, `popd_stack`, `trap`,
  `ssh`, `ssh_command`, `getent`, `python_c`, `alias`, `hash_p`, `mapfile_cb`, `systemctl_link`,
  `jobs_x`, `fddup`, `herestring`, `nc_client`.
- The sentence at `:325-327` is wrong in **both directions at once**, which is why it is a
  category error rather than a miscount:
  - **Over-inclusion.** Of the 16 rows, only 8 belong to round-1 CRITICALs F1/F2. Six
    (`python_c`, `alias`, `hash_p`, `mapfile_cb`, `systemctl_link`, `jobs_x`) are the F1-EXT
    class found *during the repair*, not round-1 findings. Two (`fddup`, `herestring`) are
    labelled "coverage:" in the table's own finding column and are not findings at all — they
    are `rc 0 — (no row)` in **both** columns because they are benign.
  - **Under-inclusion.** Two of the four CRITICALs — F3 (`find -exec`) and F4 (`--option=PATH`)
    — produce **no** zero-record row whatsoever. In RED they emit a visible decoy path
    (`find_exec` → `rc 0 — /safe ALLOW`, `curl_upload` → `rc 0 — 127.0.0.1:8790 ALLOW`,
    `tar_option`, `cp_option`, `cp_unknown`, `find_unknown`). Their defect is *incomplete*
    modelling with a reassuring path shown, which is a different and arguably nastier shape than
    silence.
- The repair claim itself survives: of the 16 zero-record RED rows, **13 are closed** in GREEN.
  The 3 that remain zero-record are `popd_stack`, `fddup`, `herestring` — and I adjudicate all
  three benign (see NIT-2): none reaches a filesystem or network primitive.

So: fix the sentence, do not re-open the CRITICAL count. Suggested correction — *"The rows that
read `rc 0 — (no row)` in the RED column are sixteen fragments exhibiting the silent-sink
pattern of CRITICAL findings 1 and 2 and the F1-EXT class found during repair; CRITICAL findings
3 and 4 instead emit a misleading partial path. Thirteen of the sixteen are closed in GREEN;
`popd_stack`, `fddup` and `herestring` remain zero-record because no path or endpoint is
reached."*

### Q2 — U-3, converted from unsupported assertion to measured fact

All three assertions at `SELF_QA_PATHSCOPE.md:8-10` are **TRUE**. I measured them:

| assertion | measurement | result |
|---|---|---|
| every run used CPython 3.14.2 | `python -V` → `Python 3.14.2`; interpreter `C:\Python314\python.exe`; the harness invokes bare `python -B` at lines 285/294/311/313, which resolves to that interpreter | ✅ TRUE |
| repaired source parses with `ast.parse(..., feature_version=(3,12))` | `ast.parse` over the 122446-byte source at digest `890016f0…af1d` → `AST_PARSE_312_OK nodes= 19504`, no exception | ✅ TRUE |
| Python 3.12 is not installed | `py -0p` lists only `-V:3.14` (`C:\Python314\python.exe`) and `-V:3.13` (WindowsApps 3.13.3824.0); `py -3.12 -V` → `No suitable Python runtime found` | ✅ TRUE |

**U-3 therefore downgrades from "unsupported claim" to "true but unevidenced".** The claim-audit
was right that the transcript at `:43-51` proves none of the three — it prints artefact
identities, line counts and determinism only. The remedy is documentary: either cite this audit,
or add the three probes to the harness so it prints them. **No factual correction is needed.**
This is the cheapest of the open documentary items.

## 5. CRITICAL C-1 — variable assignment prefixes are a surviving silent sink

**Severity: CRITICAL** (contract item 2: "Any surviving silent sink is CRITICAL").

### Minimal reproducer

```bash
#!/bin/bash
LD_PRELOAD=/etc/evil.so cat "$ROOT/f"
```

run with the harness's own `constants.env` and `allowlist.txt` (`ROOT=/safe`, allowlist
`/safe/**`). Actual output of the audited bytes:

```text
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
```

`/etc/evil.so` appears **nowhere**. No `PATH` row, no `UNRESOLVED` row,
`coverage_issue_count=0`, and the verdict is `PASS rc=0`. This is precisely the contract's
definition of a silent sink. `LD_PRELOAD` is not a decorative variable: the dynamic loader
`open()`s and maps that file at `execve` time, before `cat` runs. It is the canonical Unix
code-injection vector, and the path is outside the allowlist.

### Root cause, at source level

`pathscope_prover.py:2293-2297`:

```python
index = 0
while index < len(tokens) and self.assignment(tokens[index]):
    index += 1
if index >= len(tokens):
    return
```

Assignment-prefix tokens are skipped by advancing `index`; their **values are never inspected
for path content and never produce a coverage record**. `args = tokens[index + 1:]` (`:2314`)
then excludes them permanently. The bare-assignment early `return` at `:2296-2297` is why
`X=/etc/passwd` alone also yields `rc 0` with zero records.

The same hole exists on the declaration builtins at `:2299-2307`: for
`export`/`readonly`/`declare`/`local`/`typeset`, the loop registers only bare *names*
(`if not self.assignment(token) and NAME_RE.fullmatch(...)`), so a token of the form
`LD_PRELOAD=/etc/evil.so` is skipped with no path check at all.

This is a **third category** that the round-2 fail-closed design does not cover. The repair's
stated invariant is "unlisted option or unregistered command → rc-3 coverage record". An
assignment prefix is neither an option nor a command, so it falls through and **fails open** —
the one direction the design promises never to fail in.

### Extent — 14 targeted probes

Every case below carries an out-of-allowlist path in an assignment. Column `/etc/ shown?` asks
whether the assignment's path appears anywhere in the prover's output.

| # | fragment | rc | `/etc/` shown? | silent sink? |
|---|---|---|---|---|
| b01 | `LD_PRELOAD=/etc/evil.so cat "$ROOT/f"` | **0** | no | **YES — CRITICAL** |
| b02 | `LD_LIBRARY_PATH=/etc/evil cat "$ROOT/f"` | **0** | no | **YES — CRITICAL** |
| b03 | `FOO=/etc/passwd cat "$ROOT/f"` | **0** | no | yes (benign var, same mechanism) |
| b07 | `env LD_PRELOAD=/etc/evil.so cat "$ROOT/f"` | **0** | no | **YES — CRITICAL** |
| b09 | `export LD_PRELOAD=/etc/evil.so` ; `cat "$ROOT/f"` | **0** | no | **YES — CRITICAL** |
| b11 | `LD_PRELOAD=/etc/a.so BASH_ENV=/etc/b.sh cat "$ROOT/f"` | **0** | no | **YES — CRITICAL** (both dropped) |
| b12 | `LD_PRELOAD="$ROOT/ok.so" cat "$ROOT/f"` | 0 | n/a | allowlisted path also invisible |
| b13 | `IFS=: cat "$ROOT/f"` | 0 | n/a | no path — correct |
| b08 | `X=/etc/passwd` (never used) | **0** | no | yes (no primitive reached) |
| b04 | `PYTHONSTARTUP=/etc/evil.py python3 "$ROOT/s.py"` | 3 | **no** | masked — see note |
| b05 | `PYTHONPATH=/etc/evilmods python3 "$ROOT/s.py"` | 3 | **no** | masked |
| b06 | `PERL5LIB=/etc/evillib perl "$ROOT/s.pl"` | 3 | **no** | masked |
| b10 | `GIT_SSH_COMMAND=/etc/evil.sh git fetch` | 3 | **no** | masked |
| b14 | `LD_PRELOAD=/etc/evil.so cat /etc/passwd` | 1 | yes (`/etc/passwd` only) | masked |

**Note on the rc-3 rows — this is the dangerous part.** b04/b05/b06/b10 return rc 3, but *not*
because of the assignment. They trip an unrelated rule about the command (e.g. b04's record is
`python3 runs the program at this path; its content is not part of the analyzed input`). The
assignment path is invisible in those runs too. **In all 14 probes, without exception, the
assignment's path is never reported.** Where the fragment is caught, it is caught by luck of a
neighbouring rule; where no neighbouring rule fires, it passes clean.

### Why this matters for WP-I specifically

The blocks this prover exists to gate are deployment scripts that set environment for
interpreters and services. An assignment prefix pointing outside the release root is exactly the
shape of escape the prover is meant to make impossible to state without detection — and it is
currently the shape it cannot see.

### Required repair (direction only — I am the auditor, not the implementer)

Treat assignment prefixes and declaration-builtin assignments as first-class. Minimally: extract
each assignment's value, and if it resolves to a path-shaped string, emit a `PATH` row bound to
the assignment site; if it does not statically resolve, emit a `kind=coverage` record. A
name-based allowlist of loader/interpreter variables (`LD_*`, `BASH_ENV`, `ENV`, `PYTHON*`,
`PERL5LIB`, `GIT_SSH_COMMAND`, …) is a reasonable prioritisation but is **not** sufficient on its
own — it fails open on the next variable nobody enumerated, which is the same mistake
`NO_PATH_COMMANDS` made in round 1. Fail-closed on the construct, not on a name list.

## 6. Thirteen-pattern adjudication table

54 new adversarial fragments, in 13 families. All local, harmless, symbolic bodies; none was
executed as shell. Verdicts are from the audited bytes.

| # | pattern family | probes | representative fragment | prover behaviour | adjudication |
|---|---|---|---|---|---|
| P1 | cwd-mutating builtins | a01, a16, a35, a36 | `cd /etc` | rc 1, `/etc FORBID` (`cd -` → rc 3 coverage) | ✅ PASS |
| P2 | test / conditional primitives | a02, a03, a04 | `[[ -f /etc/passwd ]]` | rc 1, `/etc/passwd FORBID` | ✅ PASS |
| P3 | process substitution | a05, a06 | `cat <(cat /etc/passwd)` | rc 3, path FORBID + coverage record | ✅ PASS (fail-closed) |
| P4 | coproc | a07 | `coproc cat /etc/passwd` | rc 3, 2 coverage records incl. "may forward a path" | ✅ PASS (fail-closed) |
| P5 | compound-command redirection | a08–a11, a25–a28 | `while read -r l; do :; done < /etc/passwd` | rc 1, target FORBID — all 8 | ✅ PASS |
| P6 | `$(< file)` read-substitution | a12 | `x=$(< /etc/passwd)` | rc 1, `/etc/passwd FORBID` | ✅ PASS |
| P7 | `eval` | a13 | `eval 'cat /etc/passwd'` | rc 3, `eval is forbidden` | ✅ PASS |
| P8 | wrapper prefixes | a14, a15, a17, a18 | `command cat /etc/passwd` | rc 1, FORBID — all 4 unwrapped | ✅ PASS |
| **P9** | **assignment prefixes / export** | **a19, a20, b01–b14** | **`LD_PRELOAD=/etc/evil.so cat "$ROOT/f"`** | **rc 0, zero records, path invisible** | ❌ **CRITICAL C-1** |
| P10 | interpreter `-c` / `bash -c` | a21, b04–b06 | `bash -c 'cat /etc/passwd'` | rc 3, coverage record | ✅ PASS (fail-closed) |
| P11 | registered multi-path sinks | a22–a24, a29 | `dd if=/etc/passwd of=/tmp/x` | rc 1 or rc 3; `ln -s` emits both paths | ✅ PASS |
| P12 | variable dataflow into sinks | a30–a33 | `readonly P=/etc/passwd; cat "$P"` | rc 1 FORBID; `printf -v` → rc 3 | ✅ PASS |
| P13 | fd reads & no-path builtins | a34, a38–a40 | `exec 4< /etc/passwd; read -u 4` | rc 1 FORBID; `umask`/`ulimit` rc 0 (no path — correct) | ✅ PASS |

12 of 13 families are handled correctly, most of them fail-closed with a specific coverage
record. P9 is the sole failure, and it fails **open**.

## 7. Contract item 3 — finding-6 / R1 honesty

**PASS.** No output presents lexical membership as an unconditional host ALLOW.

| check | R1 baseline | R2 audited bytes |
|---|---|---|
| `PATH` rows reading bare `verdict=ALLOW` | **24** | **0** |
| `PATH` rows reading `verdict=ALLOW-LEXICAL` | 0 | all allows |
| disclosure header `semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none` | 0 runs | **64 of 66 runs** |
| verdict reason string | `closed_and_allowlisted` | `closed_and_allowlisted_lexical_argv_scope` |

The two runs without the header are `RP6-P0` and `RP7-WPI-RO` with `placeholder.constants`,
which abort at `rc 3 input_parse_error` **before any analysis**. They make no ALLOW claim, so no
disclosure is owed. Not a defect.

The residual R1 (symlink/mount binding) is disclosed as `not_established` on every run that
reaches analysis, and the ALLOW token itself carries `-LEXICAL`. A reader cannot mistake this
output for a resolved host guarantee. **Finding 6 is honestly discharged as a disclosure.**

## 8. Contract item 4 — fail-closed on unmodeled syntax, and determinism

**PASS on both.**

Fail-closed behaviour is real and specific, not a blanket rc 3:

```text
UNRESOLVED line=2 kind=coverage reason=cp has no modeled grammar for option --pathscope-unmodeled expression=--pathscope-unmodeled=1
UNRESOLVED line=2 kind=coverage reason=find has no modeled grammar for the predicate -pathscope-unmodeled expression=-pathscope-unmodeled
UNRESOLVED line=2 kind=coverage reason=opaque command coproc has no registered argv grammar expression=coproc
```

Unlisted options on registered commands, unregistered commands, and unmodeled shell constructs
each produce a distinct rc-3 coverage record naming the construct. My P3/P4/P7/P10 probes reached
this path with syntax the implementer never saw and it held every time.

The single exception is C-1: assignment prefixes reach **none** of this machinery.

Determinism: confirmed 3× by the harness and additionally by whole-transcript equality across two
independent full harness runs (§2).

## 9. Nits

- **NIT-1 — `ENDPOINT` rows use bare `verdict=ALLOW` while `PATH` rows use `ALLOW-LEXICAL`.**
  Three occurrences in GREEN, e.g.
  `ENDPOINT value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=URL uses=line=2:curl`.
  No DNS resolution is performed (the header does disclose `host_probe=none`), so an endpoint
  allow is just as lexical as a path allow. The asymmetric token invites exactly the
  over-reading finding 6 was repaired to prevent. Suggest `ALLOW-LEXICAL` for symmetry.
- **NIT-2 — three zero-record rows survive in GREEN**: `popd_stack` (`popd +1`), `fddup`
  (`exec 3>&2 …`), `herestring` (`cat <<< "$ROOT"`). I adjudicate all three **benign**: none
  names a path or endpoint, and no filesystem/network primitive is reached with an argument.
  Worth one sentence in the document so the pattern is not mistaken for an unclosed sink.
  (`popd`/`cd` do mutate cwd, which would affect later *relative* paths; no fixture exercises
  that, and it is out of scope for `lexical_argv_scope`. Flagging for the record only.)
- **NIT-3 — `SELF_QA_PATHSCOPE.md:6` states the implementer ran effort `xhigh`.** Unverifiable
  from artefacts; no action, noted only because this kickoff corrected its own tier field.

## 10. Documentary defects — status after this audit

| id | claim | status after execution |
|---|---|---|
| F-3 | `:325-327` calls the `rc 0 — (no row)` rows "the four CRITICAL findings" | **CONFIRMED FALSE.** 16 such rows. Wording/category defect, not a miscount and not an overstatement of closure — see §4 Q1. Correction text supplied. |
| U-3 | `:8-10` Python 3.14.2 `-B`, `ast.parse` 3.12, no 3.12 installed | **ALL THREE MEASURED TRUE** (§4 Q2). Reclassify from "unsupported" to "true but unevidenced"; remedy is a citation or three added probes, not a factual correction. |

F-1, F-2, U-1, U-2 are Transport-lane findings and outside this lane; I did not examine them.

## 11. What this audit does and does not establish

**Establishes.** The round-2 repair is real and largely excellent: 13 of 16 zero-record rows
closed; every published D026 rc reproduces exactly; determinism exact across independent runs;
fail-closed coverage records specific and reliable across 12 of 13 adversarial families; the
finding-6 disclosure honest and pervasive. The prover is dramatically stronger than round 1
(24 bare ALLOW rows → 0).

**Does not establish.** (a) Any statement about current RP6/RP7 bytes — the four real-block runs
are historical pinned regressions against superseded blobs (§3). (b) Absence of silent sinks —
I found one, C-1, and its root cause is structural rather than a missing table entry, so nearby
variants may exist. (c) Anything about symlink or mount behaviour, which the tool correctly
declines to claim.

## 12. Recommendation

**REQUEST_CHANGES.** Repair C-1 fail-closed at the construct level, then re-audit. C-1 is the
only blocking item; NIT-1/2/3 and the two documentary defects can ride along in the same round.
Because a CRITICAL is open, pathscope does **not** hold a flagship EXECUTION acceptance at these
bytes. Codex unavailability (provider content filter on the sink-detection source) and the
favorable GLM-5.2 supplemental read-audit remain on record and are unaffected by this verdict.

---

## Delta gate

Per the kickoff's corrected gate (a global clean-status gate cannot pass in this worktree, which
carries ~100 pre-existing untracked run logs).

1. **Before execution**, `git status --porcelain` → `before`: **128 entries**.
2. Lane executed. All fixtures and transcripts were written to `%TEMP%\pathscope-repair-r2` and
   to the session scratchpad — never into the repository.
3. **Path-scoped confirmation** (the kickoff's item 4, and per the Lead's delta-gate note the
   governing gate for this lane):

```
$ git status --porcelain -- MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md
?? MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md
```

The single entry at the audited path is this verdict file, untracked, and nothing else at that
path. **Path-scoped gate: PASS.**

4. **Whole-status delta — advisory**, per the Lead's note that concurrent lanes commit in this
   worktree. `before` = 128 entries, `after` = 124 entries. The delta is **not** confined to this
   file, and every extra entry is attributable to a concurrent lane, not to this one:

   **Entries appearing in `after` but not `before`:**

   | entry | attribution |
   |---|---|
   | `?? …/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md` | **this lane** — the verdict file |
   | ` M …/WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` | **concurrent lane** — RP7 row-build work; see §3 note. This lane never opened this file for writing; it only hashed it. |
   | `?? …/11_TRIAGE/RP7_ROWS_1_9_BUILD_CODEXFREE_RUN_2026-08-13.log` | **concurrent lane** — Codex-free RP7 rows 1–9 build run log, dated 2026-08-13 |

   **Entries present in `before` but gone from `after`** (another lane committed them mid-run;
   HEAD advanced from `a0fa8271` to `ddce3c10` via `ee31544c`): the five ` M`
   `WPI_BLOCKS_DRAFT/` files (`KICKOFF_CLAUDEPRO_RP6_2NDFLAGSHIP_AUDIT.md`,
   `RP6_R15_REPORT_2026-08-11.md`, `RP6_R16_REPORT_2026-08-11.md`, `SELF_QA_RP6.md`,
   `STATUS_RP6_P0.md`) and two `??` files (`RP6_R18_REPORT_2026-08-12.md`,
   `RP7_CLAUDE_T0_2NDFLAG_AUDIT_2026-08-12.md`). **None of these was touched by this lane.**

   A strict `after` − `before` = {this file} test therefore **fails on the whole-status form**,
   solely because of concurrent-lane commits and edits. Per the Lead's delta-gate note the
   path-scoped confirmation in item 3 is the governing gate, and it passes. This lane wrote
   exactly one repository byte: this file.
