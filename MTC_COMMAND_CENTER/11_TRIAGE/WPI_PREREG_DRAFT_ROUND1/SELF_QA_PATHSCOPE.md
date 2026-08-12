# Self-QA — Stage-1 path-scope prover, repair round 2

> **⚠ ROUND-3 AMENDMENT (2026-08-13) — C-1 repair; all transcripts/counts/digests
> below are ROUND-2 and STALE.** The flagship execution audit
> (`PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`, verdict REQUEST_CHANGES) found
> CRITICAL **C-1**: assignment prefixes and declaration-builtin assignments
> (`LD_PRELOAD=/etc/evil.so cat …`, `export LD_PRELOAD=…`, `env LD_PRELOAD=… …`)
> were silently dropped — the out-of-allowlist path was invisible and the verdict
> was `PASS rc=0`. The round-3 source fix adds `record_assignment_value` and
> calls it at the three holes; seven P9 fixtures + CASES + a determinism pair
> were added to the harness below. **EXECUTED 2026-08-13 ~00:30 by the Lead:** the
> complete harness (including the seven P9 fixtures and the `assign_prefix`
> determinism pair) ran from the repository root, rc 0, stderr 0 bytes. All seven
> P9 predictions were confirmed by measurement — five silent sinks show
> RED `PASS rc=0` → GREEN `rc=1` with the out-of-allowlist path visible, both
> controls stay rc 0 with no false positive. The round-3 stdout below replaces the
> round-2 stdout (the harness changed, so the round-2 line counts 511/644 no
> longer reproduce; current counts are 552/1189). The prediction table in
> §"Round 3 — C-1 repair" is retained with its executed confirmation.

Date: 2026-08-11
Audit tier: T1 (local-only static analysis)
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`
Implementer: `claude-opus-5` (effort xhigh, Max account) — not the auditor of record.

Every run below used CPython 3.14.2 with `-B`; the repaired source also parses with
`ast.parse(..., feature_version=(3, 12))`. A Python 3.12 executable is not installed on
this workstation. No shell fixture was executed, no host was contacted, and no network
call was made. Fixture files are written only under the Windows temporary directory.

## Identities

| artefact | bytes | SHA-256 | git blob |
|---|---|---|---|
| `pathscope_prover.py` round 1 (the audited bytes) | 49820 | `3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6` | `3f0820a9a6412f769b59b23a41df3bc6808bf6dc` |
| `pathscope_prover.py` round 2 | 122446 | `890016F0B9A8CDE4EED33F8733F69055471B07C6096F6BC07450457E6C52AF1D` | historical (r2 audit anchor) |
| `pathscope_prover.py` round 3 (this repair) | 124251 | `0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7` | uncommitted |
| `WPI_BLOCKS_DRAFT/RP6-P0.sh` | 107252 | `A090AE736CBECD9973E8AE948B052504B21CBE8B61602F4B5AC592394FAD0617` | `3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c` |
| `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` | 99903 | `11621044D0ADC21AF93E1CFC7B88EF88DE8ACA4683A69AB16CBC542A124141A4` | `5c9a2f597cceaef80d1cbd0fc100732f4b216cf5` |

The round-1 artefact is reconstructed **from its pinned blob**, not from the working tree,
so the RED column stays reproducible after the repair is committed. The two blocks are
likewise read from their pinned blobs: a concurrent session owns the RP6 working-tree file,
and a Stage-1 proof must in any case be taken over frozen bytes rather than a live file.

## How to reproduce every RED and every GREEN in one command

Save the fenced block below as `%TEMP%\pathscope_r2_harness.ps1`, then from
`C:\LAB\Tradingview_LAB_CLEAN`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r2_harness.ps1"
```

It writes every fixture, reconstructs the round-1 prover from its pinned blob, extracts
both real blocks from their pinned blobs, runs the complete case list against **both**
provers, writes `RED_R1.txt` and `GREEN_R2.txt` next to the fixtures, and finishes with the
determinism check. Nothing in it depends on shell state established elsewhere, and it
contains no placeholder that must be edited before it runs. Its own stdout was:

```text
R1_BASELINE bytes=49820 sha256=3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6
R2_REPAIRED bytes=124251 sha256=0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7
BLOCK RP6-P0.sh bytes=107252 sha256=A090AE736CBECD9973E8AE948B052504B21CBE8B61602F4B5AC592394FAD0617 git_blob=3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c
BLOCK RP7-WPI-RO.sh bytes=99903 sha256=11621044D0ADC21AF93E1CFC7B88EF88DE8ACA4683A69AB16CBC542A124141A4 git_blob=5c9a2f597cceaef80d1cbd0fc100732f4b216cf5
WROTE C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2\RED_R1.txt lines=552
WROTE C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2\GREEN_R2.txt lines=1189
DETERMINISM find_exec rc1=1 rc2=1 equal=True sha1=11c5cb8e39a2e9061e8c1d159817794b75b3ec2479649b146176f699d28067dd sha2=11c5cb8e39a2e9061e8c1d159817794b75b3ec2479649b146176f699d28067dd
DETERMINISM assign_prefix rc1=1 rc2=1 equal=True sha1=32da284224350fdb4a236c4d2238aad2f718b8b48cd89f04cf3fd1b57c30317a sha2=32da284224350fdb4a236c4d2238aad2f718b8b48cd89f04cf3fd1b57c30317a
DETERMINISM RP6-P0 rc1=3 rc2=3 equal=True sha1=2e9d6f4465fcd4a6ee0cee9edfe6fc883725ef3b6dd8f6fa9eb97dec1fa605db sha2=2e9d6f4465fcd4a6ee0cee9edfe6fc883725ef3b6dd8f6fa9eb97dec1fa605db
DETERMINISM RP7-WPI-RO rc1=3 rc2=3 equal=True sha1=1f59ab2eb1759e958a046e2e7e1115261df2aee4028a08dcf64b11d3182cb395 sha2=1f59ab2eb1759e958a046e2e7e1115261df2aee4028a08dcf64b11d3182cb395
```

This stdout is the **Lead's executed round-3 run (2026-08-13, from the repository root,
outer rc 0, stderr 0 bytes)**. `R2_REPAIRED` is the size and digest of the round-3 repaired
file at the moment the transcripts were produced; it matches the identity table. The
round-2 stdout (`R2_REPAIRED bytes=122446 … RED lines=511 / GREEN lines=644`, RP6-P0 output
sha `66959360…dc0e`, RP7 output sha `1ebedc0d…7f4b`) is history recorded in
`PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`, which reproduced it byte-for-byte. The two
real-block runs still return rc=3 deterministically after the repair; their output digests
changed because allowlisted assignment values now emit `ALLOW-LEXICAL` rows (`External
evidence:` the Lead's run transcript archived at the session scratchpad
`pathscope_r3_run.out`).

The `<QA>` token inside both transcripts is the literal fixture directory
`C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2`, normalised by the
harness so the transcripts do not carry a user-specific path.

### The harness, verbatim

```powershell
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Run from the repository root C:\LAB\Tradingview_LAB_CLEAN.
$TOOL = 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py'
$QA   = Join-Path ([System.IO.Path]::GetTempPath()) 'pathscope-repair-r2'
$R1   = Join-Path $QA 'pathscope_prover_R1.py'
New-Item -ItemType Directory -Path $QA -Force | Out-Null

function New-Fixture([string]$Name, [string[]]$Lines) {
  [System.IO.File]::WriteAllText((Join-Path $QA $Name), (($Lines -join "`n") + "`n"))
}

# --- the round-1 artefact under audit, reconstructed from its pinned blob ---
cmd /c "git cat-file blob 3f0820a9a6412f769b59b23a41df3bc6808bf6dc > `"$R1`""
$h1 = (Get-FileHash -Algorithm SHA256 -LiteralPath $R1).Hash
$l1 = (Get-Item -LiteralPath $R1).Length
"R1_BASELINE bytes=$l1 sha256=$h1"
$h2 = (Get-FileHash -Algorithm SHA256 -LiteralPath $TOOL).Hash
$l2 = (Get-Item -LiteralPath $TOOL).Length
"R2_REPAIRED bytes=$l2 sha256=$h2"

# --- the round-1 audit's own constants and allowlist, unchanged ---
New-Fixture 'constants.env' @(
  'ROOT=/safe',
  'PWD=/safe',
  'URL=http://127.0.0.1:8790/api/status',
  'HOST=198.51.100.10')
New-Fixture 'allowlist.txt' @('/safe/**', '127.0.0.1:8790')
New-Fixture 'constants_home.env' @('ROOT=/safe', 'PWD=/safe', 'HOME=/home/gatea')
New-Fixture 'allowlist_terminal.txt' @('terminal:/safe/conf')

# --- kickoff deliverable 2 of round 1: the original GREEN/RED set ---
New-Fixture 'green.sh'          @('#!/bin/bash', 'leaf="$ROOT/input"', 'cat "$leaf"')
New-Fixture 'literal.sh'        @('#!/bin/bash', 'cat /etc/passwd')
New-Fixture 'assembled.sh'      @('#!/bin/bash', 'p="/etc"', 'q="mtc-bridge"', 'cat "$p/$q/x"')
New-Fixture 'dynamic.sh'        @('#!/bin/bash', 'p="$(printf /safe)"', 'cat "$p/x"')
New-Fixture 'nested.sh'         @('#!/bin/bash', 'unused="$(cat /etc/shadow)"')

# --- CRITICAL findings 1-4: silent sink loss ---
New-Fixture 'pushd.sh'          @('#!/bin/bash', 'pushd "$ROOT"')
New-Fixture 'pushd_forbidden.sh' @('#!/bin/bash', 'pushd /etc')
New-Fixture 'popd_stack.sh'     @('#!/bin/bash', 'popd +1')
New-Fixture 'trap.sh'           @('#!/bin/bash', 'trap ''cat /etc/passwd'' EXIT')
New-Fixture 'ssh.sh'            @('#!/bin/bash', 'ssh "$HOST"')
New-Fixture 'ssh_command.sh'    @('#!/bin/bash', 'ssh -p 2222 "$HOST" ''cat /etc/passwd''')
New-Fixture 'getent.sh'         @('#!/bin/bash', 'getent hosts "$HOST"')
New-Fixture 'find_exec.sh'      @('#!/bin/bash', 'find "$ROOT" -exec cat /etc/passwd \;')
New-Fixture 'find_unknown.sh'   @('#!/bin/bash', 'find "$ROOT" -pathscope-unmodeled')
New-Fixture 'curl_upload.sh'    @('#!/bin/bash', 'curl --upload-file=/etc/passwd "$URL"')
New-Fixture 'curl_net.sh'       @('#!/bin/bash', 'curl "$URL"')
New-Fixture 'tar_option.sh'     @('#!/bin/bash', 'tar --create --file=/etc/pathscope-evil.tar "$ROOT"')
New-Fixture 'cp_option.sh'      @('#!/bin/bash', 'cp --target-directory=/etc "$ROOT/input"')
New-Fixture 'cp_unknown.sh'     @('#!/bin/bash', 'cp --pathscope-unmodeled=1 "$ROOT/a" "$ROOT/b"')

# --- same class as 1-4, found during repair ---
New-Fixture 'python_c.sh'       @('#!/bin/bash', 'python3 -c ''open("/etc/passwd")''')
New-Fixture 'alias.sh'          @('#!/bin/bash', 'alias ll=''cat /etc/passwd''')
New-Fixture 'hash_p.sh'         @('#!/bin/bash', 'hash -p /etc/passwd ff')
New-Fixture 'mapfile_cb.sh'     @('#!/bin/bash', 'mapfile -C ''cat /etc/passwd'' -c 1 arr')
New-Fixture 'systemctl_link.sh' @('#!/bin/bash', 'systemctl link /etc/systemd/system/evil.service')
New-Fixture 'jobs_x.sh'         @('#!/bin/bash', 'jobs -x cat /etc/passwd')

# --- HIGH findings 5-7 ---
New-Fixture 'tilde.sh'          @('#!/bin/bash', 'cat ~/secret')
New-Fixture 'tilde_user.sh'     @('#!/bin/bash', 'cat ~gatea/secret')
New-Fixture 'tilde_home.sh'     @('#!/bin/bash', 'cat ~/secret')
New-Fixture 'symlink_lexical.sh' @('#!/bin/bash', 'cat "$ROOT/link/passwd"')
New-Fixture 'redir_rw.sh'       @('#!/bin/bash', 'read x <> /etc/x')

# --- remaining redirection grammar ---
New-Fixture 'redir_clobber.sh'  @('#!/bin/bash', 'echo x >| /etc/y')
New-Fixture 'redir_amp.sh'      @('#!/bin/bash', 'ls &> /etc/z')
New-Fixture 'fddup.sh'          @('#!/bin/bash', 'exec 3>&2', 'echo hi >&2', 'exec 3>&-')
New-Fixture 'exec_redir.sh'     @('#!/bin/bash', 'exec 3> "$ROOT/out"')
New-Fixture 'devtcp.sh'         @('#!/bin/bash', 'cat < /dev/tcp/198.51.100.10/8790')
New-Fixture 'devtcp_allow.sh'   @('#!/bin/bash', 'cat < /dev/tcp/127.0.0.1/8790')

# --- expansions and quoting ---
New-Fixture 'heredoc.sh'        @('#!/bin/bash', 'cat <<EOF', '/etc/passwd', 'EOF')
New-Fixture 'heredoc_subst.sh'  @('#!/bin/bash', 'cat <<EOF', '$(cat /etc/shadow)', 'EOF')
New-Fixture 'heredoc_quoted.sh' @('#!/bin/bash', 'cat <<''EOF''', '$(cat /etc/shadow)', 'EOF')
New-Fixture 'herestring.sh'     @('#!/bin/bash', 'cat <<< "$ROOT"')
New-Fixture 'array.sh'          @('#!/bin/bash', 'A=(/etc/passwd)', 'cat "${A[0]}"')
New-Fixture 'brace.sh'          @('#!/bin/bash', 'cat /safe/{a,b}')
New-Fixture 'arith.sh'          @('#!/bin/bash', 'cat "/safe/$((1+1))"')
New-Fixture 'param_default.sh'  @('#!/bin/bash', 'cat "${MISSING:-/etc/passwd}"')
New-Fixture 'param_subst.sh'    @('#!/bin/bash', 'cat "${ROOT/x/y}"')
New-Fixture 'ansic.sh'          @('#!/bin/bash', 'cat $''/etc/passwd''')
New-Fixture 'continuation.sh'   @('#!/bin/bash', 'cat \', '"$ROOT/input"')
New-Fixture 'backtick.sh'       @('#!/bin/bash', 'unused="`cat /etc/shadow`"')
New-Fixture 'glob.sh'           @('#!/bin/bash', 'cat "$ROOT"/*')

# --- argv shapes ---
New-Fixture 'source.sh'         @('#!/bin/bash', 'source "$ROOT/lib.sh"')
New-Fixture 'dot_source.sh'     @('#!/bin/bash', '. "$ROOT/lib.sh"')
New-Fixture 'xargs.sh'          @('#!/bin/bash', 'xargs -a "$ROOT/list" cat')
New-Fixture 'multipath.sh'      @('#!/bin/bash', 'install -m 0644 "$ROOT/a" /etc/b')
New-Fixture 'scp_remote.sh'     @('#!/bin/bash', 'scp "$ROOT/a" gatea@198.51.100.10:/tmp/b')
New-Fixture 'nc_client.sh'      @('#!/bin/bash', 'nc "$HOST" 8790')
New-Fixture 'grep_files.sh'     @('#!/bin/bash', 'grep -q needle "$ROOT/f"')
New-Fixture 'sed_prog.sh'       @('#!/bin/bash', 'sed -n ''s/a/b/p'' "$ROOT/f"')
New-Fixture 'func_positional.sh' @('#!/bin/bash', 'f() { cat "$1"; }', 'f /etc/passwd')
New-Fixture 'func_body.sh'      @('#!/bin/bash', 'g() { cat "$ROOT/ok"; }', 'g')
New-Fixture 'case_loop.sh'      @('#!/bin/bash', 'for n in a b; do', '  case "$n" in', '    a) cat "$ROOT/a" ;;', '    *) cat /etc/other ;;', '  esac', 'done')
New-Fixture 'terminal_stat.sh'  @('#!/bin/bash', 'stat /safe/conf')
New-Fixture 'terminal_cat.sh'   @('#!/bin/bash', 'cat /safe/conf')

# --- C-1 repair (round 3): assignment-prefix silent sink, adversarial family P9 ---
# These exercise the three holes that shared one defect class: the assignment
# prefix loop, the declaration builtins, and the env wrapper. Every fixture is a
# local symbolic body; none is executed as shell.
New-Fixture 'assign_prefix.sh'       @('#!/bin/bash', 'LD_PRELOAD=/etc/evil.so cat "$ROOT/f"')
New-Fixture 'assign_prefix_allow.sh' @('#!/bin/bash', 'LD_PRELOAD="$ROOT/ok.so" cat "$ROOT/f"')
New-Fixture 'assign_bare.sh'         @('#!/bin/bash', 'X=/etc/passwd')
New-Fixture 'assign_benign.sh'       @('#!/bin/bash', 'IFS=: cat "$ROOT/f"')
New-Fixture 'assign_export.sh'       @('#!/bin/bash', 'export LD_PRELOAD=/etc/evil.so', 'cat "$ROOT/f"')
New-Fixture 'assign_env.sh'          @('#!/bin/bash', 'env LD_PRELOAD=/etc/evil.so cat "$ROOT/f"')
New-Fixture 'assign_multi.sh'        @('#!/bin/bash', 'LD_PRELOAD=/etc/a.so BASH_ENV=/etc/b.sh cat "$ROOT/f"')

# --- the real blocks, extracted from their pinned committed blobs ---
cmd /c "git cat-file blob 3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c > `"$QA\RP6-P0.sh`""
cmd /c "git cat-file blob 5c9a2f597cceaef80d1cbd0fc100732f4b216cf5 > `"$QA\RP7-WPI-RO.sh`""
foreach ($b in @('RP6-P0.sh', 'RP7-WPI-RO.sh')) {
  $p = Join-Path $QA $b
  $bh = (Get-FileHash -Algorithm SHA256 -LiteralPath $p).Hash
  $bl = (Get-Item -LiteralPath $p).Length
  $bg = (git hash-object $p)
  "BLOCK $b bytes=$bl sha256=$bh git_blob=$bg"
}
New-Fixture 'real.constants' @(
  'WPI_CANDIDATE_SHA=2ce41e34bceb599d80af24c5c33d835820ec321b',
  'WPI_RELEASE_ROOT=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b',
  'WPI_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b',
  'WPI_UNIT_FRAGMENT=/usr/local/lib/systemd/system/mtc-bridge-first-start.service',
  'WPI_STATE_DIR=/var/lib/mtc-bridge',
  'WPI_LOG_DIR=/var/log/mtc-bridge',
  'WPI_CONF_DIR=/etc/mtc-bridge',
  'WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status',
  'P0_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b',
  'REMOTE_BASE=/home/gatea/wpi_staging_STAGE1_STATIC_BINDING')
New-Fixture 'real.allowlist' @(
  '<WPI_RELEASE_ROOT>/**',
  '<WPI_VENV_ROOT>/**',
  '<WPI_UNIT_FRAGMENT>',
  'terminal:<WPI_CONF_DIR>',
  'terminal:<WPI_STATE_DIR>',
  'terminal:<WPI_LOG_DIR>',
  '<REMOTE_BASE>/**',
  '127.0.0.1:8790')
New-Fixture 'placeholder.constants' @(
  'WPI_CANDIDATE_SHA=2ce41e34bceb599d80af24c5c33d835820ec321b',
  'WPI_RELEASE_ROOT=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b',
  'WPI_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b',
  'WPI_UNIT_FRAGMENT=/usr/local/lib/systemd/system/mtc-bridge-first-start.service',
  'WPI_STATE_DIR=/var/lib/mtc-bridge',
  'WPI_LOG_DIR=/var/log/mtc-bridge',
  'WPI_CONF_DIR=/etc/mtc-bridge',
  'WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status',
  'P0_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b',
  'REMOTE_BASE=/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>')

# --- the case list: fixture, constants, allowlist ---
$CASES = @(
  @('green','constants.env','allowlist.txt'),
  @('literal','constants.env','allowlist.txt'),
  @('assembled','constants.env','allowlist.txt'),
  @('dynamic','constants.env','allowlist.txt'),
  @('nested','constants.env','allowlist.txt'),
  @('pushd','constants.env','allowlist.txt'),
  @('pushd_forbidden','constants.env','allowlist.txt'),
  @('popd_stack','constants.env','allowlist.txt'),
  @('trap','constants.env','allowlist.txt'),
  @('ssh','constants.env','allowlist.txt'),
  @('ssh_command','constants.env','allowlist.txt'),
  @('getent','constants.env','allowlist.txt'),
  @('find_exec','constants.env','allowlist.txt'),
  @('find_unknown','constants.env','allowlist.txt'),
  @('curl_upload','constants.env','allowlist.txt'),
  @('curl_net','constants.env','allowlist.txt'),
  @('tar_option','constants.env','allowlist.txt'),
  @('cp_option','constants.env','allowlist.txt'),
  @('cp_unknown','constants.env','allowlist.txt'),
  @('python_c','constants.env','allowlist.txt'),
  @('alias','constants.env','allowlist.txt'),
  @('hash_p','constants.env','allowlist.txt'),
  @('mapfile_cb','constants.env','allowlist.txt'),
  @('systemctl_link','constants.env','allowlist.txt'),
  @('jobs_x','constants.env','allowlist.txt'),
  @('tilde','constants.env','allowlist.txt'),
  @('tilde_user','constants.env','allowlist.txt'),
  @('tilde_home','constants_home.env','allowlist.txt'),
  @('symlink_lexical','constants.env','allowlist.txt'),
  @('redir_rw','constants.env','allowlist.txt'),
  @('redir_clobber','constants.env','allowlist.txt'),
  @('redir_amp','constants.env','allowlist.txt'),
  @('fddup','constants.env','allowlist.txt'),
  @('exec_redir','constants.env','allowlist.txt'),
  @('devtcp','constants.env','allowlist.txt'),
  @('devtcp_allow','constants.env','allowlist.txt'),
  @('heredoc','constants.env','allowlist.txt'),
  @('heredoc_subst','constants.env','allowlist.txt'),
  @('heredoc_quoted','constants.env','allowlist.txt'),
  @('herestring','constants.env','allowlist.txt'),
  @('array','constants.env','allowlist.txt'),
  @('brace','constants.env','allowlist.txt'),
  @('arith','constants.env','allowlist.txt'),
  @('param_default','constants.env','allowlist.txt'),
  @('param_subst','constants.env','allowlist.txt'),
  @('ansic','constants.env','allowlist.txt'),
  @('continuation','constants.env','allowlist.txt'),
  @('backtick','constants.env','allowlist.txt'),
  @('glob','constants.env','allowlist.txt'),
  @('source','constants.env','allowlist.txt'),
  @('dot_source','constants.env','allowlist.txt'),
  @('xargs','constants.env','allowlist.txt'),
  @('multipath','constants.env','allowlist.txt'),
  @('scp_remote','constants.env','allowlist.txt'),
  @('nc_client','constants.env','allowlist.txt'),
  @('grep_files','constants.env','allowlist.txt'),
  @('sed_prog','constants.env','allowlist.txt'),
  @('func_positional','constants.env','allowlist.txt'),
  @('func_body','constants.env','allowlist.txt'),
  @('case_loop','constants.env','allowlist.txt'),
  @('terminal_stat','constants.env','allowlist_terminal.txt'),
  @('terminal_cat','constants.env','allowlist_terminal.txt'),
  @('assign_prefix','constants.env','allowlist.txt'),
  @('assign_prefix_allow','constants.env','allowlist.txt'),
  @('assign_bare','constants.env','allowlist.txt'),
  @('assign_benign','constants.env','allowlist.txt'),
  @('assign_export','constants.env','allowlist.txt'),
  @('assign_env','constants.env','allowlist.txt'),
  @('assign_multi','constants.env','allowlist.txt')
)

function Invoke-Suite([string]$Prover, [string]$OutFile) {
  $lines = New-Object System.Collections.Generic.List[string]
  foreach ($case in $CASES) {
    $name, $constants, $allowlist = $case
    $lines.Add("=== $name ===")
    $out = & python -B $Prover (Join-Path $QA "$name.sh") (Join-Path $QA $constants) (Join-Path $QA $allowlist) 2>&1
    $rc = $LASTEXITCODE
    foreach ($line in $out) { $lines.Add(([string]$line).Replace($QA, '<QA>')) }
    $lines.Add("COMMAND_RC=$rc")
  }
  foreach ($pair in @(@('RP6-P0','placeholder.constants'), @('RP7-WPI-RO','placeholder.constants'),
                      @('RP6-P0','real.constants'), @('RP7-WPI-RO','real.constants'))) {
    $block, $constants = $pair
    $lines.Add("=== $block with $constants ===")
    $out = & python -B $Prover (Join-Path $QA "$block.sh") (Join-Path $QA $constants) (Join-Path $QA 'real.allowlist') 2>&1
    $rc = $LASTEXITCODE
    foreach ($line in $out) { $lines.Add(([string]$line).Replace($QA, '<QA>')) }
    $lines.Add("COMMAND_RC=$rc")
  }
  [System.IO.File]::WriteAllText($OutFile, (($lines -join "`n") + "`n"))
  "WROTE $OutFile lines=$($lines.Count)"
}

Invoke-Suite $R1   (Join-Path $QA 'RED_R1.txt')
Invoke-Suite $TOOL (Join-Path $QA 'GREEN_R2.txt')

# --- determinism: same input, same bytes, same order ---
foreach ($pair in @(@('find_exec','constants.env','allowlist.txt'),
                    @('assign_prefix','constants.env','allowlist.txt'),
                    @('RP6-P0','real.constants','real.allowlist'),
                    @('RP7-WPI-RO','real.constants','real.allowlist'))) {
  $name, $constants, $allowlist = $pair
  $a = (& python -B $TOOL (Join-Path $QA "$name.sh") (Join-Path $QA $constants) (Join-Path $QA $allowlist) 2>&1) -join "`n"
  $ra = $LASTEXITCODE
  $b = (& python -B $TOOL (Join-Path $QA "$name.sh") (Join-Path $QA $constants) (Join-Path $QA $allowlist) 2>&1) -join "`n"
  $rb = $LASTEXITCODE
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $ha = ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($a)))).Replace('-','').ToLowerInvariant()
  $hb = ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($b)))).Replace('-','').ToLowerInvariant()
  "DETERMINISM $name rc1=$ra rc2=$rb equal=$($a -ceq $b) sha1=$ha sha2=$hb"
}
```

## Round 3 — C-1 repair (assignment-prefix silent sink, family P9)

**Status: EXECUTED 2026-08-13 by the Lead — all seven predictions CONFIRMED by
measurement.** The table below was written as an implementer prediction; the Lead's run of
the complete harness confirmed every row. Measured results (exact lines from the run's
`RED_R1.txt` / `GREEN_R2.txt`):

```text
assign_prefix       R1: PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted   (silent sink)
assign_prefix       R2: PATH value=/etc/evil.so verdict=FORBID uses=line=2:assignment prefix → REJECT rc=1
assign_export       R1: PASS rc=0 (sink)  R2: PATH value=/etc/evil.so verdict=FORBID uses=line=2:export assignment → REJECT rc=1
assign_env          R1: PASS rc=0 (sink)  R2: PATH value=/etc/evil.so verdict=FORBID uses=line=2:env assignment → REJECT rc=1
assign_multi        R1: PASS rc=0 (sink)  R2: /etc/a.so FORBID + /etc/b.sh FORBID → REJECT rc=1
assign_bare         R1: PASS rc=0 (sink)  R2: PATH value=/etc/passwd verdict=FORBID → REJECT rc=1
assign_prefix_allow R1: rc=0              R2: /safe/ok.so ALLOW-LEXICAL + /safe/f ALLOW-LEXICAL → PASS rc=0 (control holds)
assign_benign       R1: rc=0              R2: /safe/f ALLOW-LEXICAL → PASS rc=0 (control holds)
```

| fixture | shell fragment | hole | R1 RED (predicted) | R2 GREEN (predicted) |
|---|---|---|---|---|
| `assign_prefix` | `LD_PRELOAD=/etc/evil.so cat "$ROOT/f"` | prefix loop | rc 0 — /safe/f ALLOW (sink: `/etc/evil.so` invisible) | rc 1 — `/etc/evil.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `assign_prefix_allow` | `LD_PRELOAD="$ROOT/ok.so" cat "$ROOT/f"` | prefix loop | rc 0 — /safe/f ALLOW (allowlisted path also invisible) | rc 0 — `/safe/ok.so` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL |
| `assign_bare` | `X=/etc/passwd` | prefix loop (bare) | rc 0 — (no row) | rc 1 — `/etc/passwd` FORBID |
| `assign_benign` | `IFS=: cat "$ROOT/f"` | prefix loop (control) | rc 0 — /safe/f ALLOW | rc 0 — /safe/f ALLOW-LEXICAL (no false positive) |
| `assign_export` | `export LD_PRELOAD=/etc/evil.so` ; `cat "$ROOT/f"` | declaration builtin | rc 0 — /safe/f ALLOW (sink) | rc 1 — `/etc/evil.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `assign_env` | `env LD_PRELOAD=/etc/evil.so cat "$ROOT/f"` | env wrapper | rc 0 — /safe/f ALLOW (sink) | rc 1 — `/etc/evil.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `assign_multi` | `LD_PRELOAD=/etc/a.so BASH_ENV=/etc/b.sh cat "$ROOT/f"` | prefix loop (×2) | rc 0 — /safe/f ALLOW (both dropped) | rc 1 — `/etc/a.so` FORBID; `/etc/b.sh` FORBID; `/safe/f` ALLOW-LEXICAL |

The R1 RED predictions assume round 1 already dropped assignment values (the defect class
predates round 2); `assign_env`/`assign_export` R1 behaviour in particular must be
**measured**, not trusted. The `cat "$ROOT/f"` operand resolves to `/safe/f` in every row
because `ROOT=/safe`.

## D026 RED/GREEN pairs (round 2 — see ROUND-3 AMENDMENT above; STALE)

`R1 RED` is the round-1 artefact at SHA-256 `3D6AF544…D43E6`. `R2 GREEN` is the repair.
The rows that read `rc 0 — (no row)` in the RED column are sixteen fragments exhibiting
the silent-sink pattern of CRITICAL findings 1 and 2 and the F1-EXT class found during
repair; CRITICAL findings 3 and 4 instead emit a misleading partial path. Thirteen of the
sixteen are closed in GREEN; `popd_stack`, `fddup` and `herestring` remain zero-record
because no path or endpoint is reached.

| fixture | shell fragment | finding | R1 RED | R2 GREEN |
|---|---|---|---|---|
| `green` | `leaf="$ROOT/input" ; cat "$leaf"` | round-1 GREEN, must stay GREEN | rc 0 — /safe/input ALLOW | rc 0 — /safe/input ALLOW-LEXICAL |
| `literal` | `cat /etc/passwd` | round-1 RED A, must stay RED | rc 1 — /etc/passwd FORBID | rc 1 — /etc/passwd FORBID |
| `assembled` | `p="/etc" ; q="mtc-bridge" ; cat "$p/$q/x"` | round-1 RED B, must stay RED | rc 1 — /etc/mtc-bridge/x FORBID | rc 1 — /etc/mtc-bridge/x FORBID |
| `dynamic` | `p="$(printf /safe)" ; cat "$p/x"` | round-1 RED C, must stay RED | rc 3 — (no row) | rc 3 — (no row) |
| `nested` | `unused="$(cat /etc/shadow)"` | round-1 completeness check | rc 1 — /etc/shadow FORBID | rc 1 — /etc/shadow FORBID |
| `pushd` | `pushd "$ROOT"` | F1 | rc 0 — (no row) | rc 0 — /safe ALLOW-LEXICAL |
| `pushd_forbidden` | `pushd /etc` | F1 | rc 0 — (no row) | rc 1 — /etc FORBID |
| `popd_stack` | `popd +1` | F1 | rc 0 — (no row) | rc 0 — (no row) |
| `trap` | `trap 'cat /etc/passwd' EXIT` | F1 | rc 0 — (no row) | rc 1 — /etc/passwd FORBID |
| `ssh` | `ssh "$HOST"` | F2 | rc 0 — (no row) | rc 1 — 198.51.100.10:22 FORBID |
| `ssh_command` | `ssh -p 2222 "$HOST" 'cat /etc/passwd'` | F2 | rc 0 — (no row) | rc 3 — 198.51.100.10:2222 FORBID |
| `getent` | `getent hosts "$HOST"` | F2 | rc 0 — (no row) | rc 3 — (no row) |
| `find_exec` | `find "$ROOT" -exec cat /etc/passwd \;` | F3 | rc 0 — /safe ALLOW | rc 1 — /etc/passwd FORBID; /safe ALLOW-LEXICAL |
| `find_unknown` | `find "$ROOT" -pathscope-unmodeled` | F3 | rc 0 — /safe ALLOW | rc 3 — /safe ALLOW-LEXICAL |
| `curl_upload` | `curl --upload-file=/etc/passwd "$URL"` | F4 | rc 0 — 127.0.0.1:8790 ALLOW | rc 1 — /etc/passwd FORBID; 127.0.0.1:8790 ALLOW |
| `curl_net` | `curl "$URL"` | F4 | rc 0 — 127.0.0.1:8790 ALLOW | rc 0 — 127.0.0.1:8790 ALLOW |
| `tar_option` | `tar --create --file=/etc/pathscope-evil.tar "$ROOT"` | F4 | rc 0 — /safe ALLOW | rc 1 — /etc/pathscope-evil.tar FORBID; /safe ALLOW-LEXICAL |
| `cp_option` | `cp --target-directory=/etc "$ROOT/input"` | F4 | rc 0 — /safe/input ALLOW | rc 1 — /etc FORBID; /safe/input ALLOW-LEXICAL |
| `cp_unknown` | `cp --pathscope-unmodeled=1 "$ROOT/a" "$ROOT/b"` | F4 | rc 0 — /safe/a ALLOW; /safe/b ALLOW | rc 3 — /safe/a ALLOW-LEXICAL; /safe/b ALLOW-LEXICAL |
| `python_c` | `python3 -c 'open("/etc/passwd")'` | F1-EXT | rc 0 — (no row) | rc 3 — (no row) |
| `alias` | `alias ll='cat /etc/passwd'` | F1-EXT | rc 0 — (no row) | rc 1 — /etc/passwd FORBID |
| `hash_p` | `hash -p /etc/passwd ff` | F1-EXT | rc 0 — (no row) | rc 1 — /etc/passwd FORBID |
| `mapfile_cb` | `mapfile -C 'cat /etc/passwd' -c 1 arr` | F1-EXT | rc 0 — (no row) | rc 1 — /etc/passwd FORBID |
| `systemctl_link` | `systemctl link /etc/systemd/system/evil.service` | F1-EXT | rc 0 — (no row) | rc 3 — (no row) |
| `jobs_x` | `jobs -x cat /etc/passwd` | F1-EXT | rc 0 — (no row) | rc 3 — (no row) |
| `tilde` | `cat ~/secret` | F5 | rc 3 — /safe/~/secret ALLOW | rc 3 — (no row) |
| `tilde_user` | `cat ~gatea/secret` | F5 | rc 3 — /safe/~gatea/secret ALLOW | rc 3 — (no row) |
| `tilde_home` | `cat ~/secret` | F5 | rc 3 — /safe/~/secret ALLOW | rc 1 — /home/gatea/secret FORBID |
| `symlink_lexical` | `cat "$ROOT/link/passwd"` | F6 | rc 0 — /safe/link/passwd ALLOW | rc 0 — /safe/link/passwd ALLOW-LEXICAL |
| `redir_rw` | `read x <> /etc/x` | F7 | rc 3 — /safe/> ALLOW | rc 1 — /etc/x FORBID |
| `redir_clobber` | `echo x >\| /etc/y` | coverage: redirection grammar | rc 3 — (no row) | rc 1 — /etc/y FORBID |
| `redir_amp` | `ls &> /etc/z` | coverage: redirection grammar | rc 3 — /etc/z FORBID | rc 1 — /etc/z FORBID |
| `fddup` | `exec 3>&2 ; echo hi >&2 ; exec 3>&-` | coverage: redirection grammar | rc 0 — (no row) | rc 0 — (no row) |
| `exec_redir` | `exec 3> "$ROOT/out"` | coverage: exec + redirection | rc 0 — /safe/out ALLOW | rc 0 — /safe/out ALLOW-LEXICAL |
| `devtcp` | `cat < /dev/tcp/198.51.100.10/8790` | coverage: /dev/tcp | rc 1 — /dev/tcp/198.51.100.10/8790 FORBID | rc 1 — 198.51.100.10:8790 FORBID |
| `devtcp_allow` | `cat < /dev/tcp/127.0.0.1/8790` | coverage: /dev/tcp | rc 1 — /dev/tcp/127.0.0.1/8790 FORBID | rc 3 — 127.0.0.1:8790 ALLOW |
| `heredoc` | `cat <<EOF ; /etc/passwd ; EOF` | F8 | rc 3 — (no row) | rc 0 — (no row) |
| `heredoc_subst` | `cat <<EOF ; $(cat /etc/shadow) ; EOF` | F8 | rc 3 — /etc/shadow FORBID | rc 1 — /etc/shadow FORBID |
| `heredoc_quoted` | `cat <<'EOF' ; $(cat /etc/shadow) ; EOF` | F8 | rc 3 — /etc/shadow FORBID | rc 0 — (no row) |
| `herestring` | `cat <<< "$ROOT"` | coverage: here-string | rc 0 — (no row) | rc 0 — (no row) |
| `array` | `A=(/etc/passwd) ; cat "${A[0]}"` | F8 | rc 3 — (no row) | rc 3 — (no row) |
| `brace` | `cat /safe/{a,b}` | coverage: brace expansion | rc 3 — /safe ALLOW | rc 3 — (no row) |
| `arith` | `cat "/safe/$((1+1))"` | coverage: arithmetic | rc 3 — (no row) | rc 3 — (no row) |
| `param_default` | `cat "${MISSING:-/etc/passwd}"` | coverage: ${var:-default} | rc 1 — /etc/passwd FORBID | rc 1 — /etc/passwd FORBID |
| `param_subst` | `cat "${ROOT/x/y}"` | coverage: ${var/x/y} | rc 3 — (no row) | rc 3 — (no row) |
| `ansic` | `cat $'/etc/passwd'` | coverage: $'...' | rc 1 — /etc/passwd FORBID | rc 1 — /etc/passwd FORBID |
| `continuation` | `cat \ ; "$ROOT/input"` | coverage: backslash-newline | rc 0 — /safe/input ALLOW | rc 0 — /safe/input ALLOW-LEXICAL |
| `backtick` | `unused="`cat /etc/shadow`"` | coverage: backtick substitution | rc 1 — /etc/shadow FORBID | rc 1 — /etc/shadow FORBID |
| `glob` | `cat "$ROOT"/*` | coverage: glob | rc 3 — (no row) | rc 3 — (no row) |
| `source` | `source "$ROOT/lib.sh"` | coverage: source | rc 3 — /safe/lib.sh ALLOW | rc 3 — /safe/lib.sh ALLOW-LEXICAL |
| `dot_source` | `. "$ROOT/lib.sh"` | coverage: . | rc 3 — /safe/lib.sh ALLOW | rc 3 — /safe/lib.sh ALLOW-LEXICAL |
| `xargs` | `xargs -a "$ROOT/list" cat` | coverage: xargs | rc 3 — (no row) | rc 3 — /safe/list ALLOW-LEXICAL |
| `multipath` | `install -m 0644 "$ROOT/a" /etc/b` | coverage: multi-path argv | rc 1 — /etc/b FORBID; /safe/a ALLOW | rc 1 — /etc/b FORBID; /safe/a ALLOW-LEXICAL |
| `scp_remote` | `scp "$ROOT/a" gatea@198.51.100.10:/tmp/b` | F2 | rc 3 — (no row) | rc 3 — /safe/a ALLOW-LEXICAL; 198.51.100.10:22 FORBID |
| `nc_client` | `nc "$HOST" 8790` | F2 | rc 0 — (no row) | rc 1 — 198.51.100.10:8790 FORBID |
| `grep_files` | `grep -q needle "$ROOT/f"` | coverage: registered text tool | rc 3 — (no row) | rc 0 — /safe/f ALLOW-LEXICAL |
| `sed_prog` | `sed -n 's/a/b/p' "$ROOT/f"` | coverage: opaque program text | rc 3 — (no row) | rc 3 — /safe/f ALLOW-LEXICAL |
| `func_positional` | `f() { cat "$1"; } ; f /etc/passwd` | coverage: positional dataflow | rc 3 — (no row) | rc 3 — (no row) |
| `func_body` | `g() { cat "$ROOT/ok"; } ; g` | coverage: function body | rc 0 — /safe/ok ALLOW | rc 0 — /safe/ok ALLOW-LEXICAL |
| `case_loop` | `for n in a b; do ;   case "$n" in ;     a) cat "$ROOT/a" ;; ;     *) cat /etc/other ;; ;   esac ; done` | coverage: case/for | rc 1 — /etc/other FORBID; /safe/a ALLOW | rc 1 — /etc/other FORBID; /safe/a ALLOW-LEXICAL |
| `terminal_stat` | `stat /safe/conf` | coverage: terminal rule | rc 3 — /safe/conf ALLOW | rc 3 — /safe/conf ALLOW-LEXICAL |
| `terminal_cat` | `cat /safe/conf` | coverage: terminal rule | rc 1 — /safe/conf FORBID | rc 1 — /safe/conf FORBID |

## Complete RED transcript (round-1 bytes, `3D6AF544…D43E6`)

```text
=== green ===
PATHSCOPE shell=<QA>\green.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/input verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== literal ===
PATHSCOPE shell=<QA>\literal.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assembled ===
PATHSCOPE shell=<QA>\assembled.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/mtc-bridge/x verdict=FORBID rule=- sources=NONE uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== dynamic ===
PATHSCOPE shell=<QA>\dynamic.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=3 reason=command substitution expression="$p/x"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nested ===
PATHSCOPE shell=<QA>\nested.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== pushd ===
PATHSCOPE shell=<QA>\pushd.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== pushd_forbidden ===
PATHSCOPE shell=<QA>\pushd_forbidden.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== popd_stack ===
PATHSCOPE shell=<QA>\popd_stack.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== trap ===
PATHSCOPE shell=<QA>\trap.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== ssh ===
PATHSCOPE shell=<QA>\ssh.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== ssh_command ===
PATHSCOPE shell=<QA>\ssh_command.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== getent ===
PATHSCOPE shell=<QA>\getent.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== find_exec ===
PATHSCOPE shell=<QA>\find_exec.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:find
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== find_unknown ===
PATHSCOPE shell=<QA>\find_unknown.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:find
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== curl_upload ===
PATHSCOPE shell=<QA>\curl_upload.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== curl_net ===
PATHSCOPE shell=<QA>\curl_net.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== tar_option ===
PATHSCOPE shell=<QA>\tar_option.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:tar
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== cp_option ===
PATHSCOPE shell=<QA>\cp_option.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/input verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cp
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== cp_unknown ===
PATHSCOPE shell=<QA>\cp_unknown.sh
PATHSCOPE resolved_count=2 unresolved_count=0
PATH value=/safe/a verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cp
PATH value=/safe/b verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cp
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== python_c ===
PATHSCOPE shell=<QA>\python_c.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== alias ===
PATHSCOPE shell=<QA>\alias.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== hash_p ===
PATHSCOPE shell=<QA>\hash_p.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== mapfile_cb ===
PATHSCOPE shell=<QA>\mapfile_cb.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== systemctl_link ===
PATHSCOPE shell=<QA>\systemctl_link.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== jobs_x ===
PATHSCOPE shell=<QA>\jobs_x.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== tilde ===
PATHSCOPE shell=<QA>\tilde.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/~/secret verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=~/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde_user ===
PATHSCOPE shell=<QA>\tilde_user.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/~gatea/secret verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=~gatea/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde_home ===
PATHSCOPE shell=<QA>\tilde_home.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/~/secret verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=~/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== symlink_lexical ===
PATHSCOPE shell=<QA>\symlink_lexical.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/link/passwd verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== redir_rw ===
PATHSCOPE shell=<QA>\redir_rw.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/> verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:redirection <
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=>
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== redir_clobber ===
PATHSCOPE shell=<QA>\redir_clobber.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=opaque command y has no registered path-argument contract expression=y
UNRESOLVED line=2 reason=redirection has no target expression=>
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== redir_amp ===
PATHSCOPE shell=<QA>\redir_amp.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/etc/z verdict=FORBID rule=- sources=NONE uses=line=2:redirection &>
UNRESOLVED line=2 reason=opaque command ls has no registered path-argument contract expression=ls
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== fddup ===
PATHSCOPE shell=<QA>\fddup.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== exec_redir ===
PATHSCOPE shell=<QA>\exec_redir.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/out verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:redirection >
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== devtcp ===
PATHSCOPE shell=<QA>\devtcp.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/dev/tcp/198.51.100.10/8790 verdict=FORBID rule=- sources=NONE uses=line=2:redirection <
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== devtcp_allow ===
PATHSCOPE shell=<QA>\devtcp_allow.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/dev/tcp/127.0.0.1/8790 verdict=FORBID rule=- sources=NONE uses=line=2:redirection <
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== heredoc ===
PATHSCOPE shell=<QA>\heredoc.sh
PATHSCOPE resolved_count=0 unresolved_count=3
UNRESOLVED line=2 reason=here input is outside the accepted static path subset expression=EOF
UNRESOLVED line=3 reason=opaque command passwd has no registered path-argument contract expression=passwd
UNRESOLVED line=4 reason=opaque command EOF has no registered path-argument contract expression=EOF
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== heredoc_subst ===
PATHSCOPE shell=<QA>\heredoc_subst.sh
PATHSCOPE resolved_count=1 unresolved_count=3
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=3:cat
UNRESOLVED line=2 reason=here input is outside the accepted static path subset expression=EOF
UNRESOLVED line=3 reason=dynamic command name: command substitution expression=$(cat /etc/shadow)
UNRESOLVED line=4 reason=opaque command EOF has no registered path-argument contract expression=EOF
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== heredoc_quoted ===
PATHSCOPE shell=<QA>\heredoc_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=3
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=3:cat
UNRESOLVED line=2 reason=here input is outside the accepted static path subset expression='EOF'
UNRESOLVED line=3 reason=dynamic command name: command substitution expression=$(cat /etc/shadow)
UNRESOLVED line=4 reason=opaque command EOF has no registered path-argument contract expression=EOF
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== herestring ===
PATHSCOPE shell=<QA>\herestring.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== array ===
PATHSCOPE shell=<QA>\array.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=array assignment is outside the accepted scalar subset expression=A=(...)
UNRESOLVED line=3 reason=unsupported parameter expansion ${A[0]} expression="${A[0]}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== brace ===
PATHSCOPE shell=<QA>\brace.sh
PATHSCOPE resolved_count=1 unresolved_count=2
PATH value=/safe verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=/safe/
UNRESOLVED line=2 reason=opaque command a,b has no registered path-argument contract expression=a,b
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== arith ===
PATHSCOPE shell=<QA>\arith.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=2 reason=command substitution expression="/safe/$((1+1))"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== param_default ===
PATHSCOPE shell=<QA>\param_default.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== param_subst ===
PATHSCOPE shell=<QA>\param_subst.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=2 reason=unsupported parameter expansion ${ROOT/x/y} expression="${ROOT/x/y}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== ansic ===
PATHSCOPE shell=<QA>\ansic.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== continuation ===
PATHSCOPE shell=<QA>\continuation.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/input verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== backtick ===
PATHSCOPE shell=<QA>\backtick.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== glob ===
PATHSCOPE shell=<QA>\glob.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=2 reason=glob expansion makes the path set dynamic expression="$ROOT"/*
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== source ===
PATHSCOPE shell=<QA>\source.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/lib.sh verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:source
UNRESOLVED line=2 reason=sourced values are outside the closed scalar input set expression=source
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== dot_source ===
PATHSCOPE shell=<QA>\dot_source.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/lib.sh verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:.
UNRESOLVED line=2 reason=sourced values are outside the closed scalar input set expression=.
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== xargs ===
PATHSCOPE shell=<QA>\xargs.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=opaque command xargs has no registered path-argument contract expression=xargs
UNRESOLVED line=2 reason=opaque command xargs may forward a path or endpoint expression="$ROOT/list"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== multipath ===
PATHSCOPE shell=<QA>\multipath.sh
PATHSCOPE resolved_count=2 unresolved_count=0
PATH value=/etc/b verdict=FORBID rule=- sources=NONE uses=line=2:install
PATH value=/safe/a verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:install
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== scp_remote ===
PATHSCOPE shell=<QA>\scp_remote.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=remote-path grammar needs an explicit transport parser expression="$ROOT/a"
UNRESOLVED line=2 reason=remote-path grammar needs an explicit transport parser expression=gatea@198.51.100.10:/tmp/b
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nc_client ===
PATHSCOPE shell=<QA>\nc_client.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== grep_files ===
PATHSCOPE shell=<QA>\grep_files.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=opaque command grep has no registered path-argument contract expression=grep
UNRESOLVED line=2 reason=opaque command grep may forward a path or endpoint expression="$ROOT/f"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== sed_prog ===
PATHSCOPE shell=<QA>\sed_prog.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=opaque command sed has no registered path-argument contract expression=sed
UNRESOLVED line=2 reason=opaque command sed may forward a path or endpoint expression="$ROOT/f"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== func_positional ===
PATHSCOPE shell=<QA>\func_positional.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=2 reason=dynamic shell parameter $1 expression="$1"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== func_body ===
PATHSCOPE shell=<QA>\func_body.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/ok verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== case_loop ===
PATHSCOPE shell=<QA>\case_loop.sh
PATHSCOPE resolved_count=2 unresolved_count=0
PATH value=/etc/other verdict=FORBID rule=- sources=NONE uses=line=5:cat
PATH value=/safe/a verdict=ALLOW rule=/safe/** sources=ROOT uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== terminal_stat ===
PATHSCOPE shell=<QA>\terminal_stat.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/conf verdict=ALLOW rule=/safe/conf [terminal] sources=NONE uses=line=2:stat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=/safe/conf
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== terminal_cat ===
PATHSCOPE shell=<QA>\terminal_cat.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/conf verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== RP6-P0 with placeholder.constants ===
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
=== RP7-WPI-RO with placeholder.constants ===
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
=== RP6-P0 with real.constants ===
PATHSCOPE shell=<QA>\RP6-P0.sh
PATHSCOPE resolved_count=1 unresolved_count=39
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=398:redirection >,line=400:redirection >
UNRESOLVED line=398 reason=opaque command builtin has no registered path-argument contract expression=builtin
UNRESOLVED line=400 reason=opaque command builtin has no registered path-argument contract expression=builtin
UNRESOLVED line=410 reason=opaque command argument: unpinned variable RUNID expression="$RUNID"
UNRESOLVED line=410 reason=opaque command rp0_require_safe_component has no registered path-argument contract expression=rp0_require_safe_component
UNRESOLVED line=412 reason=opaque command argument: unpinned variable EV_STAGE_ID expression="$EV_STAGE_ID"
UNRESOLVED line=412 reason=opaque command rp0_require_safe_component has no registered path-argument contract expression=rp0_require_safe_component
UNRESOLVED line=814 reason=dynamic command name: unpinned variable rl expression="$rl"
UNRESOLVED line=845 reason=unpinned variable P0_LOOKUP expression="$resolved"
UNRESOLVED line=857 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=857 reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=938 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=938 reason=opaque command  may forward a path or endpoint expression="$P0_FD_SELF"
UNRESOLVED line=945 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=945 reason=opaque command  may forward a path or endpoint expression="$P0_FD_SELF"
UNRESOLVED line=952 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=952 reason=opaque command argument: unpinned variable EV_LOG expression="$EV_LOG"
UNRESOLVED line=992 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=992 reason=opaque command argument: unpinned variable flag expression="$flag"
UNRESOLVED line=1156 reason=array assignment is outside the accepted scalar subset expression=p0_pw_parts=(...)
UNRESOLVED line=1166 reason=relative path depends on unpinned PWD expression=<
UNRESOLVED line=1168 reason=dynamic command name: unpinned variable P0_GETENT expression="$P0_GETENT"
UNRESOLVED line=1320 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1320 reason=opaque command argument: unpinned variable path expression="$path"
UNRESOLVED line=1348 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1348 reason=opaque command argument: unpinned variable path expression="$path"
UNRESOLVED line=1386 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1386 reason=opaque command  may forward a path or endpoint expression=/
UNRESOLVED line=1394 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1394 reason=opaque command  may forward a path or endpoint expression=/
UNRESOLVED line=1473 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1561 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1561 reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=1586 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1586 reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=1673 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1673 reason=opaque command argument: unpinned variable d expression="$d"
UNRESOLVED line=1731 reason=dynamic shell parameter $1 expression="$py"
UNRESOLVED line=1766 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=1766 reason=opaque command argument: unpinned variable py expression="$py"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== RP7-WPI-RO with real.constants ===
PATHSCOPE shell=<QA>\RP7-WPI-RO.sh
PATHSCOPE resolved_count=3 unresolved_count=69
PATH value=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python verdict=ALLOW rule=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=WPI_VENV_ROOT uses=line=999:test
PATH value=/proc/self/mountinfo verdict=FORBID rule=- sources=NONE uses=line=633:redirection <
PATH value=/proc/uptime verdict=FORBID rule=- sources=NONE uses=line=232:redirection <
UNRESOLVED line=190 reason=unpinned variable WPI_LEAF_FD expression="$fd"
UNRESOLVED line=246 reason=dynamic shell parameter $1 expression="$leaf"
UNRESOLVED line=268 reason=dynamic shell parameter $1 expression="$leaf"
UNRESOLVED line=314 reason=unpinned variable EV_DIR expression="$EV_DIR"
UNRESOLVED line=315 reason=dynamic command name: unpinned variable WPI_ENV expression="$WPI_ENV"
UNRESOLVED line=317 reason=unpinned variable WPI_LEAF_FD expression="$efd"
UNRESOLVED line=317 reason=unpinned variable WPI_LEAF_FD expression="$ofd"
UNRESOLVED line=334 reason=unpinned variable WPI_LEAF_FD expression=/dev/fd/"$ofd"
UNRESOLVED line=335 reason=unpinned variable WPI_LEAF_FD expression=/dev/fd/"$efd"
UNRESOLVED line=350 reason=dynamic shell parameter $3 expression="$file"
UNRESOLVED line=351 reason=opaque command -s has no registered path-argument contract expression=-s
UNRESOLVED line=351 reason=opaque command argument: dynamic shell parameter $3 expression="$file"
UNRESOLVED line=396 reason=dynamic shell parameter $6 expression="$dfd"
UNRESOLVED line=419 reason=dynamic shell parameter $3 expression="$file"
UNRESOLVED line=461 reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=593 reason=array assignment is outside the accepted scalar subset expression=WPI_MI_DEVICE=(...)
UNRESOLVED line=593 reason=array assignment is outside the accepted scalar subset expression=WPI_MI_FSTYPE=(...)
UNRESOLVED line=593 reason=array assignment is outside the accepted scalar subset expression=WPI_MI_POINT=(...)
UNRESOLVED line=593 reason=array assignment is outside the accepted scalar subset expression=WPI_MI_ROOT=(...)
UNRESOLVED line=593 reason=array assignment is outside the accepted scalar subset expression=WPI_MI_SOURCE=(...)
UNRESOLVED line=595 reason=dynamic shell parameter $1 expression="$file"
UNRESOLVED line=597 reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=619 reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_DEVICE+=
UNRESOLVED line=619 reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_POINT+=
UNRESOLVED line=619 reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_ROOT+=
UNRESOLVED line=619 reason=dynamic command name: dynamic shell parameter $3 expression="$device"
UNRESOLVED line=619 reason=dynamic command name: dynamic shell parameter $4 expression="$root"
UNRESOLVED line=619 reason=dynamic command name: dynamic shell parameter $5 expression="$mount_point"
UNRESOLVED line=620 reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_FSTYPE+=
UNRESOLVED line=620 reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_SOURCE+=
UNRESOLVED line=620 reason=dynamic command name: dynamic shell parameter $1 expression="$fstype"
UNRESOLVED line=620 reason=dynamic command name: dynamic shell parameter $2 expression="$source"
UNRESOLVED line=635 reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=642 reason=unpinned variable WPI_LEAF_FD expression="$outfd"
UNRESOLVED line=662 reason=array assignment is outside the accepted scalar subset expression=points=(...)
UNRESOLVED line=671 reason=array assignment is outside the accepted scalar subset expression=root_candidates=(...)
UNRESOLVED line=677 reason=array assignment is outside the accepted scalar subset expression=roots=(...)
UNRESOLVED line=682 reason=compound assignment is outside the accepted scalar subset expression=roots+=
UNRESOLVED line=682 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=708 reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=720 reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=723 reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=750 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=751 reason=opaque command argument: unpinned variable WPI_MOUNT_PROJECTION_DIGEST expression="mount_topology_mismatch observed=$WPI_MOUNT_PROJECTION_DIGEST attested=$WPI_ATTESTED_MOUNTINFO_SHA256 format=normalised_path_projection_v2"
UNRESOLVED line=762 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=763 reason=opaque command argument: unpinned variable WPI_MOUNT_BEFORE expression="mount_topology_changed before=$before after=$WPI_MOUNT_PROJECTION_DIGEST format=normalised_path_projection_v2"
UNRESOLVED line=769 reason=dynamic shell parameter $2 expression="$path"
UNRESOLVED line=849 reason=opaque command builtin has no registered path-argument contract expression=builtin
UNRESOLVED line=850 reason=opaque command builtin has no registered path-argument contract expression=builtin
UNRESOLVED line=853 reason=opaque command argument: unpinned variable RUNID expression="$RUNID"
UNRESOLVED line=853 reason=opaque command rp0_require_safe_component has no registered path-argument contract expression=rp0_require_safe_component
UNRESOLVED line=854 reason=opaque command argument: unpinned variable EV_STAGE_ID expression="$EV_STAGE_ID"
UNRESOLVED line=854 reason=opaque command rp0_require_safe_component has no registered path-argument contract expression=rp0_require_safe_component
UNRESOLVED line=860 reason=opaque command  has no registered path-argument contract expression=
UNRESOLVED line=924 reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=925 reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=927 reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=929 reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=1010 reason=unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1011 reason=unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1012 reason=opaque command -s has no registered path-argument contract expression=-s
UNRESOLVED line=1012 reason=opaque command argument: unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1012 reason=unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1013 reason=opaque command -s has no registered path-argument contract expression=-s
UNRESOLVED line=1013 reason=opaque command argument: unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1013 reason=unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1043 reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=1045 reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=1426 reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
```

## Complete GREEN transcript (repaired bytes)

```text
=== green ===
PATHSCOPE shell=<QA>\green.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/input verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== literal ===
PATHSCOPE shell=<QA>\literal.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assembled ===
PATHSCOPE shell=<QA>\assembled.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/mtc-bridge/x verdict=FORBID rule=- sources=NONE uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== dynamic ===
PATHSCOPE shell=<QA>\dynamic.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=3 kind=unresolved_path reason=cat argument is not statically known: command substitution expression="$p/x"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nested ===
PATHSCOPE shell=<QA>\nested.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== pushd ===
PATHSCOPE shell=<QA>\pushd.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:pushd
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== pushd_forbidden ===
PATHSCOPE shell=<QA>\pushd_forbidden.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc verdict=FORBID rule=- sources=NONE uses=line=2:pushd
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== popd_stack ===
PATHSCOPE shell=<QA>\popd_stack.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== trap ===
PATHSCOPE shell=<QA>\trap.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== ssh ===
PATHSCOPE shell=<QA>\ssh.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=198.51.100.10:22 verdict=FORBID rule=- sources=HOST uses=line=2:ssh
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== ssh_command ===
PATHSCOPE shell=<QA>\ssh_command.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=198.51.100.10:2222 verdict=FORBID rule=- sources=HOST uses=line=2:ssh
UNRESOLVED line=2 kind=coverage reason=ssh remote command text executes on the remote host and is outside the local static path domain expression='cat /etc/passwd'
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== getent ===
PATHSCOPE shell=<QA>\getent.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=1 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_endpoint reason=getent resolves the hosts database through NSS, whose backing service set (files, DNS, LDAP, NIS, systemd-resolved) is host configuration and is not statically determined expression=getent
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== find_exec ===
PATHSCOPE shell=<QA>\find_exec.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:find
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== find_unknown ===
PATHSCOPE shell=<QA>\find_unknown.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:find
UNRESOLVED line=2 kind=coverage reason=find has no modeled grammar for the predicate -pathscope-unmodeled expression=-pathscope-unmodeled
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== curl_upload ===
PATHSCOPE shell=<QA>\curl_upload.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:curl
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== curl_net ===
PATHSCOPE shell=<QA>\curl_net.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== tar_option ===
PATHSCOPE shell=<QA>\tar_option.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/pathscope-evil.tar verdict=FORBID rule=- sources=NONE uses=line=2:tar
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:tar
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== cp_option ===
PATHSCOPE shell=<QA>\cp_option.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc verdict=FORBID rule=- sources=NONE uses=line=2:cp
PATH value=/safe/input verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cp
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== cp_unknown ===
PATHSCOPE shell=<QA>\cp_unknown.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cp
PATH value=/safe/b verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cp
UNRESOLVED line=2 kind=coverage reason=cp has no modeled grammar for option --pathscope-unmodeled expression=--pathscope-unmodeled=1
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== python_c ===
PATHSCOPE shell=<QA>\python_c.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=python3 -c program text is opaque to static path analysis and can open any path or endpoint expression=-c
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== alias ===
PATHSCOPE shell=<QA>\alias.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== hash_p ===
PATHSCOPE shell=<QA>\hash_p.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:hash
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== mapfile_cb ===
PATHSCOPE shell=<QA>\mapfile_cb.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== systemctl_link ===
PATHSCOPE shell=<QA>\systemctl_link.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=systemctl verb link is not in the modeled read-only set and can install, link or remove unit files expression=link
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== jobs_x ===
PATHSCOPE shell=<QA>\jobs_x.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=jobs option -x changes the operand grammar in a way this tool does not model expression=-x
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde ===
PATHSCOPE shell=<QA>\tilde.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: tilde expansion depends on HOME, which is not a pinned absolute constant expression=~/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde_user ===
PATHSCOPE shell=<QA>\tilde_user.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: tilde expansion ~gatea names a home directory that is not statically known expression=~gatea/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde_home ===
PATHSCOPE shell=<QA>\tilde_home.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/home/gatea/secret verdict=FORBID rule=- sources=HOME uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== symlink_lexical ===
PATHSCOPE shell=<QA>\symlink_lexical.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/link/passwd verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== redir_rw ===
PATHSCOPE shell=<QA>\redir_rw.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/x verdict=FORBID rule=- sources=NONE uses=line=2:redirection <>
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== redir_clobber ===
PATHSCOPE shell=<QA>\redir_clobber.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/y verdict=FORBID rule=- sources=NONE uses=line=2:redirection >|
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== redir_amp ===
PATHSCOPE shell=<QA>\redir_amp.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/z verdict=FORBID rule=- sources=NONE uses=line=2:redirection &>
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== fddup ===
PATHSCOPE shell=<QA>\fddup.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== exec_redir ===
PATHSCOPE shell=<QA>\exec_redir.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/out verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:redirection >
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== devtcp ===
PATHSCOPE shell=<QA>\devtcp.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=198.51.100.10:8790 verdict=FORBID rule=- sources=NONE uses=line=2:redirection < /dev/tcp
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== devtcp_allow ===
PATHSCOPE shell=<QA>\devtcp_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=1 parse_issue_count=0
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=NONE uses=line=2:redirection < /dev/tcp
UNRESOLVED line=2 kind=provenance reason=allowlisted endpoint has no preregistered-constant provenance expression=/dev/tcp/127.0.0.1/8790
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== heredoc ===
PATHSCOPE shell=<QA>\heredoc.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== heredoc_subst ===
PATHSCOPE shell=<QA>\heredoc_subst.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=3:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== heredoc_quoted ===
PATHSCOPE shell=<QA>\heredoc_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== herestring ===
PATHSCOPE shell=<QA>\herestring.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== array ===
PATHSCOPE shell=<QA>\array.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=array assignment is outside the accepted scalar subset expression=A=(...)
UNRESOLVED line=3 kind=unresolved_path reason=cat argument is not statically known: unsupported parameter expansion ${A[0]} expression="${A[0]}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== brace ===
PATHSCOPE shell=<QA>\brace.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: brace expansion makes the word set dynamic expression=/safe/{a,b}
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== arith ===
PATHSCOPE shell=<QA>\arith.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: arithmetic expansion expression="/safe/$((1+1))"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== param_default ===
PATHSCOPE shell=<QA>\param_default.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== param_subst ===
PATHSCOPE shell=<QA>\param_subst.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: unsupported parameter expansion ${ROOT/x/y} expression="${ROOT/x/y}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== ansic ===
PATHSCOPE shell=<QA>\ansic.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== continuation ===
PATHSCOPE shell=<QA>\continuation.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/input verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== backtick ===
PATHSCOPE shell=<QA>\backtick.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== glob ===
PATHSCOPE shell=<QA>\glob.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=glob expansion makes the path set dynamic expression="$ROOT"/*
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== source ===
PATHSCOPE shell=<QA>\source.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/lib.sh verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:source
UNRESOLVED line=2 kind=coverage reason=sourced file content is outside the analyzed input expression=source
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== dot_source ===
PATHSCOPE shell=<QA>\dot_source.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/lib.sh verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:.
UNRESOLVED line=2 kind=coverage reason=sourced file content is outside the analyzed input expression=.
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== xargs ===
PATHSCOPE shell=<QA>\xargs.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/list verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:xargs
UNRESOLVED line=2 kind=coverage reason=xargs appends operands read from standard input to the command it runs; that operand set is not statically determined expression=xargs
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== multipath ===
PATHSCOPE shell=<QA>\multipath.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/b verdict=FORBID rule=- sources=NONE uses=line=2:install
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:install
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== scp_remote ===
PATHSCOPE shell=<QA>\scp_remote.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:scp
ENDPOINT value=198.51.100.10:22 verdict=FORBID rule=- sources=NONE uses=line=2:scp
UNRESOLVED line=2 kind=unresolved_path reason=scp remote path operand is a path on the peer host, which this allowlist does not describe expression=gatea@198.51.100.10:/tmp/b
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nc_client ===
PATHSCOPE shell=<QA>\nc_client.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=198.51.100.10:8790 verdict=FORBID rule=- sources=HOST uses=line=2:nc
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== grep_files ===
PATHSCOPE shell=<QA>\grep_files.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:grep
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== sed_prog ===
PATHSCOPE shell=<QA>\sed_prog.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:sed
UNRESOLVED line=2 kind=coverage reason=sed program text can open files of its own and is not statically analyzed expression='s/a/b/p'
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== func_positional ===
PATHSCOPE shell=<QA>\func_positional.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: dynamic shell parameter $1 expression="$1"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== func_body ===
PATHSCOPE shell=<QA>\func_body.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/ok verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== case_loop ===
PATHSCOPE shell=<QA>\case_loop.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/other verdict=FORBID rule=- sources=NONE uses=line=5:cat
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== terminal_stat ===
PATHSCOPE shell=<QA>\terminal_stat.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=1 parse_issue_count=0
PATH value=/safe/conf verdict=ALLOW-LEXICAL rule=/safe/conf [terminal] sources=NONE uses=line=2:stat
UNRESOLVED line=2 kind=provenance reason=allowlisted path has no preregistered-constant provenance expression=/safe/conf
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== terminal_cat ===
PATHSCOPE shell=<QA>\terminal_cat.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/conf verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== RP6-P0 with placeholder.constants ===
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
=== RP7-WPI-RO with placeholder.constants ===
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
=== RP6-P0 with real.constants ===
PATHSCOPE shell=<QA>\RP6-P0.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=3 unresolved_endpoint_count=0 coverage_issue_count=35 provenance_issue_count=0 parse_issue_count=0
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=398:redirection >,line=400:redirection >
UNRESOLVED line=163 kind=coverage reason=opaque command p0_on_err has no registered argv grammar expression=p0_on_err
UNRESOLVED line=410 kind=coverage reason=opaque command argument: unpinned variable RUNID expression="$RUNID"
UNRESOLVED line=410 kind=coverage reason=opaque command rp0_require_safe_component has no registered argv grammar expression=rp0_require_safe_component
UNRESOLVED line=412 kind=coverage reason=opaque command argument: unpinned variable EV_STAGE_ID expression="$EV_STAGE_ID"
UNRESOLVED line=412 kind=coverage reason=opaque command rp0_require_safe_component has no registered argv grammar expression=rp0_require_safe_component
UNRESOLVED line=814 kind=coverage reason=dynamic command name: unpinned variable rl expression="$rl"
UNRESOLVED line=845 kind=unresolved_path reason=unpinned variable P0_LOOKUP expression="$resolved"
UNRESOLVED line=857 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=857 kind=coverage reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=938 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=938 kind=coverage reason=opaque command  may forward a path or endpoint expression="$P0_FD_SELF"
UNRESOLVED line=945 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=945 kind=coverage reason=opaque command  may forward a path or endpoint expression="$P0_FD_SELF"
UNRESOLVED line=952 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=952 kind=coverage reason=opaque command argument: unpinned variable EV_LOG expression="$EV_LOG"
UNRESOLVED line=992 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=992 kind=coverage reason=opaque command argument: unpinned variable flag expression="$flag"
UNRESOLVED line=1156 kind=coverage reason=array assignment is outside the accepted scalar subset expression=p0_pw_parts=(...)
UNRESOLVED line=1166 kind=unresolved_path reason=relative path depends on unpinned PWD expression=<
UNRESOLVED line=1168 kind=coverage reason=dynamic command name: unpinned variable P0_GETENT expression="$P0_GETENT"
UNRESOLVED line=1320 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1320 kind=coverage reason=opaque command argument: unpinned variable path expression="$path"
UNRESOLVED line=1348 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1348 kind=coverage reason=opaque command argument: unpinned variable path expression="$path"
UNRESOLVED line=1386 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1386 kind=coverage reason=opaque command  may forward a path or endpoint expression=/
UNRESOLVED line=1394 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1394 kind=coverage reason=opaque command  may forward a path or endpoint expression=/
UNRESOLVED line=1473 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1561 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1561 kind=coverage reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=1586 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1586 kind=coverage reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=1673 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1673 kind=coverage reason=opaque command argument: unpinned variable d expression="$d"
UNRESOLVED line=1731 kind=unresolved_path reason=dynamic shell parameter $1 expression="$py"
UNRESOLVED line=1766 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1766 kind=coverage reason=opaque command argument: unpinned variable py expression="$py"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== RP7-WPI-RO with real.constants ===
PATHSCOPE shell=<QA>\RP7-WPI-RO.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=34 unresolved_endpoint_count=0 coverage_issue_count=38 provenance_issue_count=0 parse_issue_count=0
PATH value=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python verdict=ALLOW-LEXICAL rule=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=WPI_VENV_ROOT uses=line=999:test
PATH value=/proc/self/mountinfo verdict=FORBID rule=- sources=NONE uses=line=633:redirection <
PATH value=/proc/uptime verdict=FORBID rule=- sources=NONE uses=line=232:redirection <
UNRESOLVED line=132 kind=coverage reason=opaque command wpi_on_err has no registered argv grammar expression=wpi_on_err
UNRESOLVED line=190 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$fd"
UNRESOLVED line=246 kind=unresolved_path reason=dynamic shell parameter $1 expression="$leaf"
UNRESOLVED line=268 kind=unresolved_path reason=dynamic shell parameter $1 expression="$leaf"
UNRESOLVED line=314 kind=unresolved_path reason=cd argument is not statically known: unpinned variable EV_DIR expression="$EV_DIR"
UNRESOLVED line=315 kind=coverage reason=exec argument is not statically known: unpinned variable WPI_ENV expression="$WPI_ENV"
UNRESOLVED line=317 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$efd"
UNRESOLVED line=317 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$ofd"
UNRESOLVED line=334 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression=/dev/fd/"$ofd"
UNRESOLVED line=335 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression=/dev/fd/"$efd"
UNRESOLVED line=350 kind=unresolved_path reason=dynamic shell parameter $3 expression="$file"
UNRESOLVED line=351 kind=unresolved_path reason=dynamic shell parameter $3 expression="$file"
UNRESOLVED line=396 kind=coverage reason=read option value is not statically known: dynamic shell parameter $4 expression="$fd"
UNRESOLVED line=396 kind=unresolved_path reason=dynamic shell parameter $6 expression="$dfd"
UNRESOLVED line=419 kind=unresolved_path reason=dynamic shell parameter $3 expression="$file"
UNRESOLVED line=461 kind=coverage reason=read option value is not statically known: unpinned variable WPI_CAP_FD expression="$fd"
UNRESOLVED line=461 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_DEVICE=(...)
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_FSTYPE=(...)
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_POINT=(...)
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_ROOT=(...)
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_SOURCE=(...)
UNRESOLVED line=595 kind=unresolved_path reason=dynamic shell parameter $1 expression="$file"
UNRESOLVED line=597 kind=coverage reason=read option value is not statically known: declared variable fd has no static value expression="$fd"
UNRESOLVED line=597 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=619 kind=coverage reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_DEVICE+=
UNRESOLVED line=619 kind=coverage reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_POINT+=
UNRESOLVED line=619 kind=coverage reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_ROOT+=
UNRESOLVED line=619 kind=coverage reason=dynamic command name: dynamic shell parameter $3 expression="$device"
UNRESOLVED line=619 kind=coverage reason=dynamic command name: dynamic shell parameter $4 expression="$root"
UNRESOLVED line=619 kind=coverage reason=dynamic command name: dynamic shell parameter $5 expression="$mount_point"
UNRESOLVED line=620 kind=coverage reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_FSTYPE+=
UNRESOLVED line=620 kind=coverage reason=compound assignment is outside the accepted scalar subset expression=WPI_MI_SOURCE+=
UNRESOLVED line=620 kind=coverage reason=dynamic command name: dynamic shell parameter $1 expression="$fstype"
UNRESOLVED line=620 kind=coverage reason=dynamic command name: dynamic shell parameter $2 expression="$source"
UNRESOLVED line=635 kind=coverage reason=read option value is not statically known: declared variable infd has no static value expression="$infd"
UNRESOLVED line=635 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=642 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$outfd"
UNRESOLVED line=662 kind=coverage reason=array assignment is outside the accepted scalar subset expression=points=(...)
UNRESOLVED line=671 kind=coverage reason=array assignment is outside the accepted scalar subset expression=root_candidates=(...)
UNRESOLVED line=677 kind=coverage reason=array assignment is outside the accepted scalar subset expression=roots=(...)
UNRESOLVED line=682 kind=coverage reason=compound assignment is outside the accepted scalar subset expression=roots+=
UNRESOLVED line=682 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=708 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=720 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=723 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=750 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=751 kind=coverage reason=opaque command argument: unpinned variable WPI_MOUNT_PROJECTION_DIGEST expression="mount_topology_mismatch observed=$WPI_MOUNT_PROJECTION_DIGEST attested=$WPI_ATTESTED_MOUNTINFO_SHA256 format=normalised_path_projection_v2"
UNRESOLVED line=762 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=763 kind=coverage reason=opaque command argument: unpinned variable WPI_MOUNT_BEFORE expression="mount_topology_changed before=$before after=$WPI_MOUNT_PROJECTION_DIGEST format=normalised_path_projection_v2"
UNRESOLVED line=769 kind=unresolved_path reason=dynamic shell parameter $2 expression="$path"
UNRESOLVED line=853 kind=coverage reason=opaque command argument: unpinned variable RUNID expression="$RUNID"
UNRESOLVED line=853 kind=coverage reason=opaque command rp0_require_safe_component has no registered argv grammar expression=rp0_require_safe_component
UNRESOLVED line=854 kind=coverage reason=opaque command argument: unpinned variable EV_STAGE_ID expression="$EV_STAGE_ID"
UNRESOLVED line=854 kind=coverage reason=opaque command rp0_require_safe_component has no registered argv grammar expression=rp0_require_safe_component
UNRESOLVED line=860 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=924 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=925 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=927 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=929 kind=coverage reason=read option value is not statically known: declared variable fd has no static value expression="$fd"
UNRESOLVED line=929 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=1010 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1011 kind=unresolved_path reason=unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1012 kind=unresolved_path reason=unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1012 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1013 kind=unresolved_path reason=unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1013 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1043 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=1045 kind=coverage reason=read option value is not statically known: declared variable fd has no static value expression="$fd"
UNRESOLVED line=1045 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=1426 kind=coverage reason=read option value is not statically known: unpinned variable WPI_CAP_OUT_FD expression="$fd"
UNRESOLVED line=1426 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
```

## Determinism

The last three lines of the harness stdout above run each of `find_exec`, `RP6-P0` and
`RP7-WPI-RO` twice in memory and compare the complete stdout byte for byte plus the rc.
All three report `equal=True` with identical digests, so ordering and output are stable.
Determinism is not soundness; it is only the property that the recorded transcripts can be
re-derived.

## Real-block diagnostic — literally re-runnable

Finding 9 was that the round-1 real-input evidence could not be pasted and re-run. The
four real-block cases are the last four sections of both transcripts above, produced by the
same single harness command, and they carry their own identity check:

* `=== RP6-P0 with placeholder.constants ===` and `=== RP7-WPI-RO with placeholder.constants ===`
  use the draft §1 value `REMOTE_BASE=/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>`
  exactly as the preregistration carries it. Both STOP at rc 3 before analysis. This is the
  honest Stage-1 result and the repair did not relax it.
* `=== RP6-P0 with real.constants ===` and `=== RP7-WPI-RO with real.constants ===` replace
  **only** that one placeholder with the disclosed non-authoritative static value
  `/home/gatea/wpi_staging_STAGE1_STATIC_BINDING`, for diagnostic depth. This is not
  acceptance evidence.

Both constants files and the machine-form §10.1 allowlist are written literally by the
harness (`real.constants`, `placeholder.constants`, `real.allowlist`); no value has to be
substituted by hand. The block bytes come from `git cat-file blob`, and the harness prints
`git hash-object` of what it extracted so the reader can confirm the extraction is the
committed blob.

Round-1 versus round-2 on the same bytes:

```text
RP6-P0.sh  round 1: resolved_count=1 unresolved_count=39                       rc 3
RP6-P0.sh  round 2: resolved_fs_path_count=1 resolved_net_endpoint_count=0
                    unresolved_path_count=3 unresolved_endpoint_count=0
                    coverage_issue_count=35 provenance_issue_count=0 parse_issue_count=0   rc 3

RP7-WPI-RO round 1: resolved_count=3 unresolved_count=69                       rc 3
RP7-WPI-RO round 2: resolved_fs_path_count=3 resolved_net_endpoint_count=0
                    unresolved_path_count=34 unresolved_endpoint_count=0
                    coverage_issue_count=38 provenance_issue_count=0 parse_issue_count=0   rc 3
```

The single round-1 number `unresolved_count` is gone. It was an `Issue` cardinality and was
being read as a path-set cardinality. Nothing about these counts converts either block into
a PASS, and they remain a lower-bound diagnostic until a fresh T1 audit accepts the tool.
