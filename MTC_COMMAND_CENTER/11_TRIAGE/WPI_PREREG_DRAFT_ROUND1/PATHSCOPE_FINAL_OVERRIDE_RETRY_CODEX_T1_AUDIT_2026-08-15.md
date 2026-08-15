REQUEST_CHANGES

Date: 2026-08-15  
Auditor: fresh independent `gpt-5.6-sol`, effort `high`, T1  
Frozen subject: `40091b2b795be3339dc0df7014df6bfc091e4eca`  
Authority: the owner-authorized transport retry only; no repair round is authorized.

The published harness and every named C-3/C-4 repair fixture reproduce. Acceptance still
fails because the mandatory complete-grammar audit found three adjacent REQUIRED defects:
executable command text and a URI/list member can still reach `PASS rc=0` with zero
terminal accounting; member provenance is laundered across a mixed value; and duplicate
and repeated-empty members collapse before terminal accounting. Per the dispatch, this
returns the lane directly to the owner boundary. No repair was attempted.

## Session header evidence

This header was printed and confirmed before any audit work:

```text
SESSION HEADER
model: gpt-5.6-sol
effort: high
sandbox: danger-full-access
session id: 01a0062e-fdf6-7121-b2f5-9474d5086ed9
transport confirmation: danger-full-access confirmed; audit may proceed
```

The header did not read `read-only`. No Git, Python, or hash command was refused by
policy. GNU `sha256sum` was not installed; Git-object bytes were therefore redirected
byte-for-byte to scratch and hashed with `Get-FileHash`. This was a missing executable,
not a transport refusal.

## Identity re-derivation

Preflight command and real output:

```powershell
git -C C:\PSRETRY rev-parse HEAD
git -C C:\PSRETRY status --porcelain
```

```text
HEAD=40091b2b795be3339dc0df7014df6bfc091e4eca
STATUS_PORCELAIN=<empty>
```

For each artifact I ran `Get-Item`, `Get-FileHash -Algorithm SHA256`,
`git cat-file -s`, byte-exact `git cat-file blob` redirection followed by
`Get-FileHash`, and `git rev-parse 40091b2b:<path>`.

| artifact | worktree bytes | worktree SHA-256 | Git-object bytes | Git-object SHA-256 | blob OID | result |
|---|---:|---|---:|---|---|---|
| `pathscope_prover.py` | 137520 | `28848d60f74a7c668db3019bbac58550f4a55c1c02038c013153316c711edf9c` | 137520 | `28848d60f74a7c668db3019bbac58550f4a55c1c02038c013153316c711edf9c` | `695ca9c951e31f53da9580d41326583d71086bb3` | MATCH |
| `SELF_QA_PATHSCOPE.md` | 315514 | `75e5581ea33580d21f3e30d614c2122be3f5ab59156fa0a9746f52801efb4761` | 311577 | `f99d972f46c12ab1eea3fb426b9f9f39d98b6a3724cfcd229140d1433da0703d` | `96af8b035e243a6f39486e4e674dfde7448ae917` | MATCH |
| `STATUS_PATHSCOPE.md` | 12359 | `6c2c409a338a9084c40a660150b803c916c3383940e5be6cb531e66c0d58a804` | 12197 | `4fb9ab89e369fee8389e33b032f0eff6d6e06d8768ee8b0ca1bd610f4ae6bb57` | `06e963d6915e9627a3e0538631f4b81eaf023ca5` | MATCH |
| `PATHSCOPE_FINAL_OVERRIDE_REPAIR_REPORT_2026-08-14.md` | 21897 | `595ff2a4a76362550242780f60caf8ba2ad75243296944a8c9a14eedc5c504cf` | 21579 | `3dae5d6d245963254db368bc11f8295cd0b98ef78c16c44a14d690dfa8df5bb0` | `a45fc81a0b9e57f7cc6bfe0ece3c28b8b4079da6` | MATCH |

The same table was re-derived after every subject execution with identical values and
`CAT_RC=0`. Immediately before this verdict file was created, `HEAD` was still the frozen
commit and `git status --porcelain` was empty.

## 1. Published PowerShell harness

I extracted the body of `### The harness, verbatim` from the frozen Git-object bytes of
`SELF_QA_PATHSCOPE.md`. No fixture, path, or command text was retyped or substituted.

```text
HARNESS_BYTES=27699
HARNESS_LINES=472
HARNESS_SHA256=0C6E0B28A6F2057DCE2EC9CB802B77D2864148A7C1382ED424EDBDEDA723C93D
HARNESS_FIRST=$ErrorActionPreference = 'Stop'
HARNESS_LAST=Pop-Location
```

Published command, run from `C:\PSRETRY` under the ordinary Windows user profile:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r5_harness.ps1"
```

Real result (bulky transcripts remained in scratch):

```text
OUTER_RC=0
STDOUT_BYTES=2424
STDERR_BYTES=0
R1_BASELINE bytes=49820 sha256=3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6
R3_PREREPAIR bytes=124251 sha256=0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7
R4_PREREPAIR bytes=131599 sha256=553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB
R5_REPAIRED bytes=137520 sha256=28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C
WROTE RED_R1.txt lines=768 sha256=667BF364D0008B3A5869C3ECC2CA16FDAC0C1D60086B3F8FB50CC3E93E70E89D
WROTE GREEN_R5.txt lines=1557 sha256=A534BDCFBBD7B21D874602EB5E90336CBF0796881BE650C3EEC973AF4DBE328C
WROTE RED_R3.txt lines=150 sha256=599B4482C91FCC22F5CA9BCE09261F193F25A4321BF53F650EAA31EEE8C4CBCC
WROTE RED_R4.txt lines=324 sha256=BC142778035AE9B759A47869CCEA86D8C23D9406735BBDB189009188C36CC01B
```

All seven published determinism pairs reported `equal=True`, identical rc values, and
identical digest pairs:

```text
find_exec rc1=1 rc2=1 sha=f0f0bf2d...f11bd
assign_prefix rc1=1 rc2=1 sha=dc1ab295...49ae1
c2_list_prefix rc1=1 rc2=1 sha=eed53413...e53bd
c3_ws_relative rc1=3 rc2=3 sha=7c905b08...38d6c
c4_export_quoted rc1=1 rc2=1 sha=fa1ff7ce...30581
RP6-P0 rc1=3 rc2=3 sha=01bffdd3...dfdc0
RP7-WPI-RO rc1=3 rc2=3 sha=2d87cffc...7c10a
```

The prior Turkish-profile normalization defect is closed for this literal run: the four
recorded transcript hashes and all determinism hashes reproduce, stderr is empty, and the
harness did not raise `TRANSCRIPT_LEAK`.

## 2. Independent C-3 execution

Command template (one independently written static fixture per row; no fixture was
executed as shell):

```powershell
python -B C:\PSRETRY\MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py <case>.sh <constants> <allowlist>
```

Real results:

| shape | rc | terminal result |
|---|---:|---|
| whitespace list, later relative member | 3 | `/elsewhere/relative/escape.so` FORBID; whole value and `/safe/lib` present; coverage STOP |
| URI plus later absolute member | 1 | allowed `127.0.0.1:8790` endpoint plus `/etc/escape` FORBID |
| colon-bearing whole pathname | 1 | `/safe/relative:dir/file` FORBID plus `/safe/dir/file` member |
| empty-only list with `PWD=/elsewhere` | 1 | `/elsewhere` FORBID with `sources=PWD` |
| executable command text `ssh -v` without `/` | 3 | coverage STOP; no false PASS |

The five named C-3 shapes close. Literal RED/GREEN against the exact committed round-4
blob and repaired bytes was also executed independently:

```text
R4 bytes=131599 sha256=553A97E9...E2EB
R5 bytes=137520 sha256=28848D60...DF9C
c3_ws_relative      R4 rc=0 PASS -> R5 rc=3 coverage/FORBID
c3_uri_absolute     R4 rc=0 PASS -> R5 rc=1 /etc/escape FORBID
c3_colon_whole      R4 rc=0 PASS -> R5 rc=1 whole pathname FORBID
c3_empty_only       R4 rc=0 PASS -> R5 rc=1 PWD FORBID
c3_cmdtext_noslash  R4 rc=0 PASS -> R5 rc=3 coverage STOP
```

## 3. Independent C-4 execution and call-site reachability

Both quoted shapes were executed at assignment-prefix, `env`, and `export` sites:

| shape/site | R4 rc | R5 rc | observed R5 caller attribution |
|---|---:|---:|---|
| absolute, prefix | 1 | 1 | `/etc/escape.so` FORBID, `assignment prefix` |
| absolute, `env` | 1 | 1 | `/etc/escape.so` FORBID, `env assignment` |
| absolute, quoted `export` | 0 | 1 | `/etc/escape.so` FORBID, `export assignment` |
| quoted-space, prefix | 1 | 3 | one `/safe dir/escape` FORBID row retained; coverage STOP |
| quoted-space, `env` | 1 | 3 | one `/safe dir/escape` FORBID row retained; coverage STOP |
| quoted-space, quoted `export` | 0 | 3 | one `/safe dir/escape` FORBID row retained; coverage STOP |

Thus quote recovery is reachable at each caller. The two declaration closures have literal
R4 RED (`PASS rc=0`) and R5 GREEN (rc 1/3), while prefix and `env` are measured controls.

## 4. C-2 closures and quoted/escaped-space guards

Independent real outputs:

```text
c2_list_prefix       rc=1  /etc/escape FORBID
c2_list_env          rc=1  /etc/escape FORBID
c2_list_export       rc=1  /etc/escape FORBID
c2_allow_list        rc=0  whole value and /safe/lib + /safe/lib64 accounted
c2_empty_plus_path   rc=3  /etc/escape FORBID + resolved /safe empty member
c2_cmdtext_path      rc=3  /etc/key FORBID + coverage STOP
c2_relative          rc=1  /elsewhere/relative/path.so FORBID
c2_quoted_guard      rc=3  one `/safe dir/escape` FORBID row retained
c2_escaped_guard     rc=3  /etc/escape FORBID; no loss of the whole reading
```

The quoted guard was falsified with MUT-A. Current and mutant both return rc 3, so the rc
is not used as evidence: current contains the single forbidden `/safe dir/escape`; MUT-A
removes that row and leaves only the fabricated allowed `/safe` and `/safe/dir/escape`
rows. This is a discriminating row-level proof.

## 5. Complete assignment-member grammar inspection

I inspected `record_assignment_value`, `assignment_member_kind`, `split_list_members`,
`record_assignment_members`, and `output_report`, then executed adjacent fixtures.

Command template was the same direct `python -B <frozen-prover> <fixture> <constants>
<allowlist>` invocation used above. The decisive real outputs were:

```text
adv_cmdtext_bare_operand RC=0
  fixture: GIT_SSH_COMMAND="ssh evil.example" cat "$ROOT/f"
  resolved_fs_path_count=1; coverage_issue_count=0
  only assignment-independent row: /safe/f
  PATHSCOPE verdict=PASS rc=0

adv_uri_bare_member RC=0
  fixture: LD_LIBRARY_PATH=$URL:evil.so cat "$ROOT/f"
  allowed endpoint 127.0.0.1:8790 and /safe/f only; evil.so has no row
  PATHSCOPE verdict=PASS rc=0

adv_provenance_mixed RC=0
  fixture: LD_LIBRARY_PATH=$ROOT/lib:/safe/literal cat "$ROOT/f"
  /safe/literal verdict=ALLOW-LEXICAL sources=ROOT
  provenance_issue_count=0; PATHSCOPE verdict=PASS rc=0

adv_provenance_control RC=3
  fixture: LD_LIBRARY_PATH=/safe/literal cat "$ROOT/f"
  /safe/literal sources=NONE
  provenance_issue_count=1; PATHSCOPE verdict=REJECT rc=3

adv_duplicate RC=1
  fixture: LD_LIBRARY_PATH=/etc/escape:/etc/escape cat "$ROOT/f"
  only one `/etc/escape` member use is printed

adv_empty_multiplicity RC=0
  fixture: LD_LIBRARY_PATH=:: cat "$ROOT/f"
  three empty members collapse to one `/safe` row
  PATHSCOPE verdict=PASS rc=0
```

Source confirmation:

- lines 1343-1370 compute one union `sources` set for the complete expanded RHS and pass
  that same set to every derived member;
- lines 1459-1462 activate word-list coverage only when an option or `/` occurs, leaving
  multiword executable text such as `ssh evil.example` in the silent `bare` residual;
- lines 1476-1490 deduplicate every candidate/member into `pool` and reduce any number of
  empty members to one Boolean;
- lines 1491-1497 emit no record for `bare` members; and
- lines 2943-2997 aggregate paths by value and evidence by a set, so multiplicity cannot
  be recovered in the report.

These executions produce REQUIRED findings F1-F3 below.

## 6. D026 and changed-fence discriminating power

The published harness itself reconstructed and executed the exact committed pre-repair
blobs. I independently repeated the C-3/C-4 R4/R5 comparisons above. I then created seven
single-line mutation copies in scratch; every anchor matched exactly once before mutation.

```text
MUT-A anchor_count=1: quoted guard loses the whole forbidden row
MUT-B anchor_count=1: c2_list_prefix, c3_uri_absolute, c3_empty_only -> PASS rc=0
MUT-C anchor_count=1: c3_ws_relative, c3_cmdtext_noslash -> PASS rc=0
MUT-D anchor_count=1: c3_uri_absolute -> PASS rc=0
MUT-E anchor_count=1: c3_empty_only -> PASS rc=0
MUT-F anchor_count=1: c3_colon_whole -> PASS rc=0
MUT-G anchor_count=1: both quoted export declarations -> PASS rc=0
```

I also executed every behavior-changing carried fixture against its stated deviant:

| carried fence | deviant | discriminating observation |
|---|---|---|
| `assign_benign`, `c2_benign_scalars` | MUT-E | current has the `/safe` empty-member row; mutant does not; both stay rc 0 |
| `c2_list_bare_first` | MUT-F | current adds the colon-bearing whole row/provenance STOP; mutant does not |
| `c2_list_space` | MUT-A | current has the whole-value row/provenance STOP; mutant does not |
| `c2_empty_member` | MUT-E | current has the resolved `/safe` row; mutant does not |
| `c2_quoted_space` | MUT-A | current has `/safe dir/escape` FORBID; mutant does not |
| `c2_escaped_space` | MUT-C | current has word-list rows and coverage STOP; mutant does not |

The `c2_command_text` and `c2_words_with_path` carried changes are reason-text extensions,
not newly claimed closure behavior: both remain rc 3 and retain their FORBID rows under R4
and R5; I reproduced both old and new reason strings. The harness's real-block cases were
not substantively audited because RP6/RP7 are explicitly excluded from this dispatch.

The claimed named closures therefore have literal D026 evidence. That evidence does not
close the independent adjacent failures in section 5.

## 7. Compatibility, self-QA, and delta

Commands and real output:

```text
COMMAND=python --version
Python 3.14.2
PYTHON_VERSION_RC=0

COMMAND=python -B -c "ast.parse(..., feature_version=(3,12))"
AST_PARSE_FEATURE_VERSION_3_12=OK
AST_PARSE_RC=0

COMMAND=py -3.12 -V
No suitable Python runtime found
PY312_RUNTIME_RC=103
```

Python 3.12 feature-compatible parsing is confirmed by `ast.parse`; an actual Python 3.12
runtime is not installed, so runtime execution specifically under 3.12 was not verified.
The published self-QA result is confirmed by the clean literal harness run and exact
transcript/determinism hashes in section 1.

Read-only scope/delta checks:

```text
git show --stat 40091b2b
  4 files changed, 1981 insertions(+), 540 deletions(-)
git diff --name-status 2fb3eac0 40091b2b -- <four frozen artifacts>
  A repair report; M self-QA; M status; M prover
git diff --check 2fb3eac0 40091b2b -- <four frozen artifacts>
  rc=0, no output
git status --porcelain immediately before verdict write
  <empty>
```

No host, network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge, or economic action occurred. No shell
fixture body was executed as shell. No sub-agent or other model was invoked. No Git
mutation occurred. Scratch was confined to `%TEMP%`. The only repository write made by
this audit is this required verdict file.

## Findings

### REQUIRED F1 - adjacent command-text and URI/list members still disappear

`GIT_SSH_COMMAND="ssh evil.example"` is valid executable command text without `/`; it can
carry an endpoint operand, but the repaired predicate activates only when some word has an
option shape or `/`. The complete assignment produces no row or unresolved marker and the
run returns `PASS rc=0`. Likewise, `$URL:evil.so` splits into an allowed URI member and a
later bare loader member, but `evil.so` produces no terminal record and the run passes.
This is Pattern 12/13: admitted consumer syntax reaches zero accounting, and zero facts are
read as absence of risk. The disclosed `bare` residual does not satisfy the mandatory
terminal-conservation requirement.

### REQUIRED F2 - provenance is laundered across members

The source unions provenance for the complete RHS and attaches that union to every
derived member. Consequently the literal `/safe/literal` in
`$ROOT/lib:/safe/literal` inherits `sources=ROOT` and passes, while the identical literal
alone correctly produces a provenance STOP. Provenance must remain attached to the exact
substring/member that supplied it; another member's constant cannot authenticate a
literal neighbor.

### REQUIRED F3 - duplicate and repeated-empty members collapse

`pool` deduplication and the single `empty_member` Boolean erase input-member identity and
multiplicity before reporting. Two duplicate nonempty members produce one member use;
three empty members in `::` produce one PWD row and `PASS rc=0`. The output layer further
set-deduplicates evidence. This violates the required Pattern-13 conservation equation and
the dispatch's explicit duplicate/empty-collapse check: each admitted member needs one
stable terminal disposition, or an explicit duplicate/collision failure.

No NIT findings.

## Explicitly not verified

- Runtime execution under an actual Python 3.12 interpreter was not possible because that
  runtime is absent; 3.12 grammar compatibility was verified with `feature_version=(3,12)`.
- RP6, RP7, transport, and SEC102 correctness were not audited. The published harness ran
  its own fixed real-block cases as required, but no conclusion about those artifacts is
  drawn here.
- Host/runtime path binding, symlink resolution, mount boundaries, or any deployment/live
  property were not tested and remain outside this lexical static-prover audit.
- A raw `git status --porcelain` cannot be empty after the mandated verdict file is
  created: immediately before this write it was empty, and this file is the sole expected
  audit-attributable repository delta. No Git mutation was authorized to hide or stage it.

Final disposition: **REQUEST_CHANGES**. Per owner authority, stop at the owner boundary;
do not open another repair or audit cycle without new explicit authorization.
