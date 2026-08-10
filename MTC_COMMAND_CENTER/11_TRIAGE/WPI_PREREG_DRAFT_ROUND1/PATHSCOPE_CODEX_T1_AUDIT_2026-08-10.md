REQUEST_CHANGES: 9 required findings

# Codex T1 audit - section 10.2 path-scope prover

Date: 2026-08-10  
Tier: T1 - local-only, non-economic static-analysis tooling  
Applied auditor contract: fresh `gpt-5.6-sol`, effort high, one flagship reviewer; T1 maximum two rounds  
Scope: report only; no source, block, preregistration, status, memory, or Git mutation;
no staging/production host contact and no network; local fixture files only under `%TEMP%`

The prover is not sound enough to serve as the section 10.2 Stage-1 gate. Multiple complete
Bash fragments reach filesystem or network primitives while the prover emits no path, no
`UNRESOLVED` marker, and `PATHSCOPE verdict=PASS rc=0`. This is the fatal under-reporting
class named in the review contract.

## Audited identity

Exact command:

```powershell
$p='MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py'
$i=Get-Item -LiteralPath $p
$h=Get-FileHash -Algorithm SHA256 -LiteralPath $p
[pscustomobject]@{Length=$i.Length; SHA256=$h.Hash} | Format-List
```

Observed output, rc 0:

```text
Length : 49820
SHA256 : 3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6
```

Current real-input identities:

```text
RP6-P0.sh     bytes=93421 sha256=75db028e76438bc88caba19b9c3b6411e5f573f7b6c2bd13c3883d24e4389570
RP7-WPI-RO.sh bytes=70941 sha256=23e55667bec2453e21605b3551d5802b9cc28a82040789f3ead988b69aa01aad
```

Python compatibility check:

```powershell
python --version
python -B -c "import ast, pathlib; p=pathlib.Path(r'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py'); ast.parse(p.read_text(encoding='utf-8'), filename=str(p), feature_version=(3,12)); print('AST_FEATURE_3_12=PASS')"
"COMMAND_RC=$LASTEXITCODE"
```

```text
Python 3.14.2
AST_FEATURE_3_12=PASS
COMMAND_RC=0
```

## Shared adversarial fixture setup

This is the exact common setup used by findings 1-8. It writes only under the Windows
temporary directory; it does not execute any shell fixture.

```powershell
$QA = Join-Path ([System.IO.Path]::GetTempPath()) 'pathscope-codex-t1-audit-20260810'
New-Item -ItemType Directory -Path $QA | Out-Null
[System.IO.File]::WriteAllLines((Join-Path $QA 'constants.env'), [string[]]@(
  'ROOT=/safe',
  'PWD=/safe',
  'URL=http://127.0.0.1:8790/api/status',
  'HOST=198.51.100.10'
))
[System.IO.File]::WriteAllLines((Join-Path $QA 'allowlist.txt'), [string[]]@(
  '/safe/**',
  '127.0.0.1:8790'
))
$TOOL = 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py'
```

## Findings

### 1. CRITICAL - the `NO_PATH_COMMANDS`/control shortcut silently discards real sinks

`pathscope_prover.py:563-574,769-770` returns immediately for `pushd` and `trap`.
`pushd` consumes a filesystem path. A trap body is shell source that can execute a
filesystem primitive. Neither route produces a path or an unresolved marker.

Exact commands:

```powershell
[System.IO.File]::WriteAllLines((Join-Path $QA 'pushd.sh'), [string[]]@('#!/bin/bash','pushd "$ROOT"'))
[System.IO.File]::WriteAllLines((Join-Path $QA 'trap.sh'), [string[]]@('#!/bin/bash',"trap 'cat /etc/passwd' EXIT"))
foreach($name in @('pushd','trap')) {
  python -B $TOOL "$QA\$name.sh" "$QA\constants.env" "$QA\allowlist.txt"
  "COMMAND_RC=$LASTEXITCODE"
}
```

Observed output:

```text
PATHSCOPE shell=...\pushd.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
PATHSCOPE shell=...\trap.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
```

Required repair: do not place commands in a no-path shortcut when any accepted form can
carry a path or executable shell string. Parse `pushd` operands and recursively analyze
trap actions, or return a specific rc-3 unresolved reason.

### 2. CRITICAL - ordinary SSH and NSS host grammar silently disappears

`pathscope_prover.py:562,838-845` records a network operand only when it already has URL
or `host:port` grammar. Ordinary `ssh host` is a network primitive using the implicit port
22, but the host operand is ignored. `getent hosts host` is even earlier classified as a
no-path command. Both return a clean pass against an allowlist that contains neither
`198.51.100.10:22` nor that host.

Exact commands:

```powershell
[System.IO.File]::WriteAllLines((Join-Path $QA 'ssh.sh'), [string[]]@('#!/bin/bash','ssh "$HOST"'))
[System.IO.File]::WriteAllLines((Join-Path $QA 'getent.sh'), [string[]]@('#!/bin/bash','getent hosts "$HOST"'))
foreach($name in @('ssh','getent')) {
  python -B $TOOL "$QA\$name.sh" "$QA\constants.env" "$QA\allowlist.txt"
  "COMMAND_RC=$LASTEXITCODE"
}
```

Observed output for each fixture:

```text
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
```

Required repair: implement separate, complete argv grammars for every registered network
primitive, including implicit ports and path-bearing options. Any unparsed operand or
option that might affect an endpoint must be rc 3. Adjudicate `getent` databases explicitly;
do not silently assert that all forms are path/network-free.

### 3. CRITICAL - `find -exec` hides a nested forbidden primitive

`pathscope_prover.py:789-797` stops scanning at the first operand that is not path-shaped.
It neither parses nor rejects the remainder of the expression. The fixture reaches
`/etc/passwd` through `find -exec`, but only the allowed search root is reported.

Exact command:

```powershell
[System.IO.File]::WriteAllLines((Join-Path $QA 'find_exec.sh'), [string[]]@(
  '#!/bin/bash','find "$ROOT" -exec cat /etc/passwd \;'
))
python -B $TOOL "$QA\find_exec.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
```

Observed output:

```text
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:find
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
```

Required repair: parse the complete `find` expression, recursively analyze `-exec`,
`-execdir`, `-ok`, and `-okdir` command vectors, and adjudicate other path-bearing actions;
return rc 3 for any action grammar not fully modeled.

### 4. CRITICAL - `--option=PATH` is silently discarded by registered sink adapters

`nonoption_operands()` at `pathscope_prover.py:630-650` discards option tokens containing
`=`. The command-specific handlers at `798-837` do not recover generic path-valued options.
This omits a curl upload source, a tar archive destination, and a cp target directory while
reporting only allowed/provenance-backed operands.

Exact commands:

```powershell
[System.IO.File]::WriteAllLines((Join-Path $QA 'curl_upload.sh'), [string[]]@('#!/bin/bash','curl --upload-file=/etc/passwd "$URL"'))
[System.IO.File]::WriteAllLines((Join-Path $QA 'tar_option.sh'), [string[]]@('#!/bin/bash','tar --create --file=/etc/pathscope-evil.tar "$ROOT"'))
[System.IO.File]::WriteAllLines((Join-Path $QA 'cp_option.sh'), [string[]]@('#!/bin/bash','cp --target-directory=/etc "$ROOT/input"'))
foreach($name in @('curl_upload','tar_option','cp_option')) {
  python -B $TOOL "$QA\$name.sh" "$QA\constants.env" "$QA\allowlist.txt"
  "COMMAND_RC=$LASTEXITCODE"
}
```

Observed output:

```text
curl_upload:
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0

tar_option:
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:tar
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0

cp_option:
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/input verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cp
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
```

Required repair: use per-command option grammars that capture both `--name value` and
`--name=value`, including source and destination paths. Unknown options for a registered
sink must be rejected as rc 3 unless proved path-independent.

### 5. HIGH - tilde is falsely reported as a resolved-and-allowed path

`canonical_path()` at `pathscope_prover.py:474-488` treats every nonempty non-absolute word
as relative to pinned `PWD`. Bash expands a leading tilde from `HOME`; it does not resolve
it under `PWD`. The tool prints the false path `/safe/~/secret` with `verdict=ALLOW`. The
overall rc happens to be 3 only because the false path has no constant provenance. This
still violates the kickoff's central rule: a path must not be reported resolved-and-allowed
unless it was genuinely established.

Exact commands:

```powershell
[System.IO.File]::WriteAllLines((Join-Path $QA 'tilde.sh'), [string[]]@('#!/bin/bash','cat ~/secret'))
python -B $TOOL "$QA\tilde.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
& 'C:\Program Files\Git\bin\bash.exe' --noprofile --norc -c "printf '%s\n' ~/secret"
"COMMAND_RC=$LASTEXITCODE"
```

Observed output:

```text
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/~/secret verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=~/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
/c/Users/BarışSemaay/secret
COMMAND_RC=0
```

Required repair: implement Bash tilde rules from pinned inputs or emit only an unresolved
rc-3 record. Never emit an `ALLOW` row for the invented `PWD/~/...` path.

### 6. HIGH - lexical tree membership is presented as unconditional host-path `ALLOW`

The only path canonicalization is `posixpath.normpath()` (`pathscope_prover.py:481-486`).
It cannot establish whether an intermediate host component is a symlink or mount crossing
to an object outside the lexical tree, yet `output_report()` prints unconditional
`verdict=ALLOW` and `closed_and_allowlisted`. The status mentions lexical normalization,
but neither the status nor output states that the `ALLOW` conclusion itself is lexical-only
and symlink/mount-unaware.

Exact command:

```powershell
[System.IO.File]::WriteAllLines((Join-Path $QA 'symlink_lexical.sh'), [string[]]@(
  '#!/bin/bash','cat "$ROOT/link/passwd"'
))
python -B $TOOL "$QA\symlink_lexical.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
```

Observed output:

```text
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/link/passwd verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
```

Required repair: define the proof as lexical argv scope and say so in every relevant
verdict, then bind it to a separate symlink/mount-chain proof; or reject tree membership
that the Stage-1 evidence cannot establish. Do not label lexical normalization alone as a
closed host-path proof.

### 7. HIGH - the required `<>` redirection is not tokenized and the real target disappears

`<>` is absent from `ShellLexer.OPERATORS` at `pathscope_prover.py:94-98` and from
`Analyzer.REDIRS` at `575`. The lexer splits it into `<` and `>`, invents `>` as a path,
and omits `/etc/x` because `read` is in `NO_PATH_COMMANDS`. The outcome is rc 3, but the
unresolved reason is accidental provenance on a false path, not an explicit unsupported
construction, and the required path set is wrong.

Exact command:

```powershell
[System.IO.File]::WriteAllLines((Join-Path $QA 'redir_rw.sh'), [string[]]@('#!/bin/bash','read x <> /etc/x'))
python -B $TOOL "$QA\redir_rw.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
```

Observed output:

```text
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/> verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:redirection <
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=>
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
```

Required repair: tokenize `<>` before `<` and `>`, record its real target as one read/write
filesystem sink, and add a regression fixture proving `/etc/x` is reported forbidden.

### 8. MEDIUM - `unresolved_count` is an issue count, not an unresolved-path count

`output_report()` at `pathscope_prover.py:1099-1113` prints `len(all_issues)` as
`unresolved_count`. `all_issues` contains parser, control, opaque-command, provenance, and
path issues. It is not a set of unresolved paths. The published QA then calls 37 and 65
"unresolved paths." The heredoc fixture has three issues even though the heredoc body is
data, while the array fixture counts both the assignment construction and its later use.

Exact command:

```powershell
[System.IO.File]::WriteAllLines((Join-Path $QA 'heredoc.sh'), [string[]]@(
  '#!/bin/bash','cat <<EOF','/etc/passwd','EOF'
))
[System.IO.File]::WriteAllLines((Join-Path $QA 'array.sh'), [string[]]@(
  '#!/bin/bash','A=(/etc/passwd)','cat "${A[0]}"'
))
foreach($name in @('heredoc','array')) {
  python -B $TOOL "$QA\$name.sh" "$QA\constants.env" "$QA\allowlist.txt"
  "COMMAND_RC=$LASTEXITCODE"
}
```

Observed output excerpts:

```text
heredoc: PATHSCOPE resolved_count=0 unresolved_count=3 ... COMMAND_RC=3
array:   PATHSCOPE resolved_count=0 unresolved_count=2 ... COMMAND_RC=3
```

Required repair: distinguish resolved unique paths, unresolved path-bearing arguments,
and non-path parser/coverage issues. Do not describe an `Issue` cardinality as a path set.

### 9. MEDIUM - the real-input diagnostic evidence is not literally re-runnable

The five small published QA fixtures are literally re-runnable and every published
assertion held. The real placeholder commands also reproduce rc 3. However,
`SELF_QA_PATHSCOPE.md:211-227` says a second run replaced the placeholder, used
`git archive HEAD`, checked `git hash-object`, and produced the 1/37 and 4/65 summaries,
but it gives none of those exact setup, extraction, identity-check, or invocation commands.
The summary therefore cannot be pasted and rerun as published, contrary to the review
contract and defect pattern 10.

Exact rerun command for the five commands that are present in the document:

```powershell
$SELFQA = Join-Path ([System.IO.Path]::GetTempPath()) 'pathscope-prover-self-qa'
foreach($name in @('green','literal','assembled','dynamic','nested')) {
  python -B $TOOL "$SELFQA\$name.sh" "$SELFQA\constants.env" "$SELFQA\allowlist.txt"
  "COMMAND_RC=$LASTEXITCODE"
}
```

Observed rc vector and assertions:

```text
green=0 literal=1 assembled=1 dynamic=3 nested=1
All five published resolved/unresolved counts, path rows, reason tokens, and verdicts reproduced.
```

Required repair: publish the literal static-constant replacement, immutable extraction,
blob/SHA identity checks, exact prover invocations, rc values, and complete real outputs.

## Required lexer/resolver coverage exercised

All entries below used the same direct CLI form shown above. No shell fixture was executed.

| Construction / sink | Observed result |
|---|---|
| single quote, ANSI-C quote | forbidden `/etc/passwd`, rc 1 |
| double quote + backslash-newline | `/safe/input` ALLOW, rc 0 |
| heredoc | rc 3, but body tokens are misread as commands |
| here-string | no path argument, rc 0 |
| `$(...)`, backticks | explicit command-substitution unresolved, rc 3 |
| arrays | explicit array/parameter unresolved, rc 3 |
| `${var:-default}` | forbidden fallback expanded, rc 1 |
| `${var/x/y}` | explicit unsupported expansion, rc 3 |
| arithmetic | rc 3, mislabeled `command substitution` |
| brace expansion | rc 3 for the exercised forbidden construction; no silent pass found |
| tilde | false resolved `ALLOW` row plus rc 3; finding 5 |
| `>`, `>>`, `<`, `&>` | actual target reported, rc 1 |
| `<>` | false target reported; finding 7 |
| fd duplication `>&2` | no filesystem path, rc 0 |
| `exec 3>/...` | actual target forbidden, rc 1 |
| `source`, `.` | path reported and explicit rc 3 |
| `cd` | path reported, rc 1 |
| `pushd` | silent pass; finding 1 |
| `find -exec` | nested path silently omitted; finding 3 |
| `xargs -a` | opaque-command/path unresolved, rc 3 |
| `tar`/`cp`/`install` positional multi-path argv | positional paths reported |
| `tar`/`cp`/`curl` path options | silently omitted; finding 4 |
| `/dev/tcp` | treated as forbidden filesystem path, rc 1; no network verdict |
| `ssh`, `getent hosts` | endpoint silently omitted; finding 2 |
| exact/tree/terminal rules | terminal `stat` ALLOW rc 0; same path via `cat` FORBID rc 1 |
| `.`, `..`, repeated/trailing slash | lexical normalization reproduced; tree escape forbidden |

## Determinism

Exact command ran each input twice in memory and compared complete stdout plus rc. No output
file was created:

```powershell
$cases=[ordered]@{
  find_exec=@("$QA\find_exec.sh","$QA\constants.env","$QA\allowlist.txt")
  RP7=@(
    'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh',
    "$QA\static.constants",
    "$QA\static.allowlist"
  )
}
foreach($item in $cases.GetEnumerator()) {
  $a=& python -B $TOOL @($item.Value) 2>&1; $rca=$LASTEXITCODE
  $b=& python -B $TOOL @($item.Value) 2>&1; $rcb=$LASTEXITCODE
  $ta=[string]::Join([Environment]::NewLine,[string[]]$a)
  $tb=[string]::Join([Environment]::NewLine,[string[]]$b)
  $sha=[System.Security.Cryptography.SHA256]::Create()
  $ha=([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($ta)))).Replace('-','').ToLowerInvariant()
  $hb=([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($tb)))).Replace('-','').ToLowerInvariant()
  "$($item.Key) rc1=$rca rc2=$rcb equal=$($ta -ceq $tb) sha1=$ha sha2=$hb"
}
```

Observed output:

```text
find_exec rc1=0 rc2=0 equal=True sha1=d7c13a55cdb0bf820dd831f3fd7a7e28ef0c45c6519d4e2ab0581bbebc40f10b sha2=d7c13a55cdb0bf820dd831f3fd7a7e28ef0c45c6519d4e2ab0581bbebc40f10b
RP7 rc1=3 rc2=3 equal=True sha1=c80d9c7d6ed4e0cc1e765dc4790dffbb9bae674ee4ac7357ffdebecd46039755 sha2=c80d9c7d6ed4e0cc1e765dc4790dffbb9bae674ee4ac7357ffdebecd46039755
```

Ordering and byte output were deterministic in the exercised cases. Determinism does not
repair the coverage defects.

## All ten design-defect patterns checked

| Pattern | Audit result |
|---|---|
| 1 - STOP is not a result | Violated in the more severe direction: inability/omission becomes PASS (findings 1-4). |
| 2 - Whose kernel answered? | Static tool executes no host probe; its unconditional host-path wording still exceeds its lexical domain (finding 6). |
| 3 - The leaf is not the path | Intermediate symlink/mount traversal is not established (finding 6). |
| 4 - Privileged child environment | No child shell/interpreter is launched by the prover; no instance found. |
| 5 - grep is not a parser | Equivalent grammar defect: command argv is partially pattern-matched and then silently accepted (findings 2-4, 7). |
| 6 - Read status before stdout | Python input-read exceptions return rc 3; no direct instance found. |
| 7 - Nonzero read is not EOF | `Path.read_text()` is whole-input and exception-checked; no direct instance found. |
| 8 - Name is not identity | Constant provenance names are not presented as host identity; no direct instance found. |
| 9 - Sentence outruns probe | `ALLOW`/`closed_and_allowlisted` outruns lexical and incomplete sink coverage (findings 1-6). |
| 10 - Evidence that cannot fail | Static real-input diagnostic lacks literal commands (finding 9). |

## Current RP6/RP7 results and trust decision

With the draft's unresolved `<REMOTE_BASE>` value, both real runs honestly stop before
analysis:

```text
RP6 rc=3: PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
RP7 rc=3: PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
```

With only `REMOTE_BASE=/home/gatea/wpi_staging_STAGE1_STATIC_BINDING` substituted for
diagnostic depth, the current working-tree blocks reproduce the published shape:

```text
RP6 rc=3
PATHSCOPE resolved_count=1 unresolved_count=37
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=359:redirection >,line=361:redirection >
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete

RP7 rc=3
PATHSCOPE resolved_count=4 unresolved_count=65
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=183:redirection >,line=624:redirection >,line=625:redirection >
PATH value=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python verdict=ALLOW rule=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=WPI_VENV_ROOT uses=line=763:test
PATH value=/proc/self/mountinfo verdict=FORBID rule=- sources=NONE uses=line=413:redirection <
PATH value=/proc/uptime verdict=FORBID rule=- sources=NONE uses=line=173:redirection <
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
```

These counts are reproducible outputs of these exact bytes, but they are **not trustworthy
counts from a sound tool**. The resolved set is incomplete because multiple sink routes are
silently omitted, and `unresolved_count` counts heterogeneous `Issue` records rather than
unresolved paths. They must not be used to freeze either block, to assert complete scope,
or to reconcile section 10.1. At most, the printed paths and issues are a deterministic
lower-bound diagnostic from a currently unsound analyzer.

## Minimum acceptance repair set

1. Remove every silent-pass sink class demonstrated in findings 1-4; unmodeled command or
   option grammar must produce a specific rc-3 unresolved marker.
2. Correct Bash expansion/operator modeling for tilde and `<>`; add falsifications for
   brace, arithmetic, arrays, substitutions, heredoc, and every redirection grammar.
3. Define and disclose lexical-versus-host path semantics, including symlink/mount limits.
4. Separate unresolved path cardinality from general parser/coverage issues.
5. Add D026-style RED/GREEN tests for every silent-pass fixture above, proving RED against
   the current implementation and GREEN after repair.
6. Publish literally rerunnable real-block diagnostic commands and complete output.

Until those repairs and a fresh T1 re-audit accept, section 10.2 is not satisfied and the
Stage-1 archive must not be frozen.
