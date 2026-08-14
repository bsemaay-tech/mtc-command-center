# Self-QA — Stage-1 path-scope prover, repair round 2

> **⚠ ROUND-4 AMENDMENT (2026-08-13) — C-2 repair; every transcript, count and
> digest in this file has been REGENERATED at round 4 and is current.** The Codex
> T1 execution re-audit of the round-3 bytes
> (`PATHSCOPE_CODEX_T1_EXEC_AUDIT_R3_2026-08-13.md`, verdict REQUEST_CHANGES)
> found CRITICAL **C-2**: `record_assignment_value` recorded a value only when
> the complete rendered value started with `/`, `./` or `../`, and then recorded
> it only as one whole blob — so a loader list with a later absolute member, a
> bare first member, a whitespace word list, an ordinary relative pathname, an
> empty list member, command text carrying an option path, and a URI-shaped
> value all returned `PASS rc=0` with the out-of-allowlist lexeme absent. The
> Lead additionally reproduced a false PASS in an incomplete first repair
> attempt, where a naive `str.split()` of the rendered value turned the single
> quoted pathname `/safe dir/escape` into two allowed paths. Round 4 replaces
> the first-character test with a member grammar (`record_assignment_members`)
> and adds the eighteen-fixture P10 family plus a third prover column — the
> round-3 committed blob — so the RED side of every C-2 closure is the actual
> pre-repair bytes, not a prediction. Round 4 also clears the three documentary
> nits from §5 of that audit. **The stale round-2 transcript warning below is
> retained for history; it no longer applies — the fences in this file are the
> round-4 run.**
>
> **⚠ ROUND-3 AMENDMENT (2026-08-13) — C-1 repair; all transcripts/counts/digests
> below were ROUND-2 and STALE at the time this was written.** The flagship execution audit
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
> longer reproduce; the counts *at round 3* were 552/1189). The prediction table in
> §"Round 3 — C-1 repair" is retained with its executed confirmation.
> *(Round-4 note: the harness changed again, so the current counts are 660/1363/150 —
> see the round-4 stdout fence, which is the authoritative one.)*

Date: 2026-08-11 (rounds 1–2) · 2026-08-13 (rounds 3–4)
Audit tier: T1 (local-only static analysis)
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`
Implementer: rounds 2 and 4 `claude-opus-5` (round 2 effort xhigh, round 4 effort high);
round 3 GLM-5.2. No implementer is the auditor of record, so the round-4 T1 execution
re-audit must be a fresh independent session of a flagship that is **not** `claude-opus-5`
and **not** GLM-5.2.

Every run below used CPython 3.14.2 with `-B`; the repaired source also parses with
`ast.parse(..., feature_version=(3, 12))`. A Python 3.12 executable is not installed on
this workstation — `py -3.12 -V` reports no such runtime. These three facts were
independently re-verified by the Codex round-3 execution re-audit
(`PATHSCOPE_CODEX_T1_EXEC_AUDIT_R3_2026-08-13.md` §5, item U-3, which recorded them as
"facts re-verified true; citation still absent"); this citation closes that nit. No shell
fixture was executed, no host was contacted, and no network call was made. Fixture files
are written only under the Windows temporary directory.

## Identities

| artefact | bytes | SHA-256 | git blob |
|---|---|---|---|
| `pathscope_prover.py` round 1 (the audited bytes) | 49820 | `3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6` | `3f0820a9a6412f769b59b23a41df3bc6808bf6dc` |
| `pathscope_prover.py` round 2 | 122446 | `890016F0B9A8CDE4EED33F8733F69055471B07C6096F6BC07450457E6C52AF1D` | historical (r2 audit anchor) |
| `pathscope_prover.py` round 3 (the C-2 pre-repair subject, RED column of family P10) | 124251 | `0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7` | `e600a107f2e2a790653cc544a94cd7436b7b070a` |
| `pathscope_prover.py` round 4 (this repair) | 131599 | `553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB` | uncommitted |
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

It writes every fixture, reconstructs the round-1 **and** round-3 provers from their pinned
blobs, extracts both real blocks from their pinned blobs, runs the complete case list
against the round-1 and the repaired prover, runs the C-2 family P10 additionally against
the round-3 pre-repair prover, writes `RED_R1.txt`, `GREEN_R2.txt` and `RED_R3.txt` next to
the fixtures, and finishes with the determinism check. Nothing in it depends on shell state
established elsewhere, and it contains no placeholder that must be edited before it runs.
Its own stdout was:

```text
﻿R1_BASELINE bytes=49820 sha256=3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6
R3_PREREPAIR bytes=124251 sha256=0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7
R2_REPAIRED bytes=131599 sha256=553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB
BLOCK RP6-P0.sh bytes=107252 sha256=A090AE736CBECD9973E8AE948B052504B21CBE8B61602F4B5AC592394FAD0617 git_blob=3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c
BLOCK RP7-WPI-RO.sh bytes=99903 sha256=11621044D0ADC21AF93E1CFC7B88EF88DE8ACA4683A69AB16CBC542A124141A4 git_blob=5c9a2f597cceaef80d1cbd0fc100732f4b216cf5
WROTE C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2\RED_R1.txt lines=660
WROTE C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2\GREEN_R2.txt lines=1363
WROTE C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-repair-r2\RED_R3.txt lines=150
DETERMINISM find_exec rc1=1 rc2=1 equal=True sha1=11c5cb8e39a2e9061e8c1d159817794b75b3ec2479649b146176f699d28067dd sha2=11c5cb8e39a2e9061e8c1d159817794b75b3ec2479649b146176f699d28067dd
DETERMINISM assign_prefix rc1=1 rc2=1 equal=True sha1=32da284224350fdb4a236c4d2238aad2f718b8b48cd89f04cf3fd1b57c30317a sha2=32da284224350fdb4a236c4d2238aad2f718b8b48cd89f04cf3fd1b57c30317a
DETERMINISM c2_list_prefix rc1=1 rc2=1 equal=True sha1=40e458dc11a9040bb4208e93097f19a3b5a9fd46c0d2043515ceb6ce3188bf62 sha2=40e458dc11a9040bb4208e93097f19a3b5a9fd46c0d2043515ceb6ce3188bf62
DETERMINISM RP6-P0 rc1=3 rc2=3 equal=True sha1=2e9d6f4465fcd4a6ee0cee9edfe6fc883725ef3b6dd8f6fa9eb97dec1fa605db sha2=2e9d6f4465fcd4a6ee0cee9edfe6fc883725ef3b6dd8f6fa9eb97dec1fa605db
DETERMINISM RP7-WPI-RO rc1=3 rc2=3 equal=True sha1=224cda7292d5e1b60f77b558e4b986d1ed39defdaa843f3a09e60a0625bb2ad2 sha2=224cda7292d5e1b60f77b558e4b986d1ed39defdaa843f3a09e60a0625bb2ad2
```

This stdout is the **round-4 implementer run (2026-08-13, from the repository root, outer
rc 0, stderr 0 bytes)**. `R2_REPAIRED` is the size and digest of the round-4 repaired file
at the moment the transcripts were produced; it matches the identity table. `R3_PREREPAIR`
is the committed round-3 blob, the exact bytes the Codex re-audit rejected, reconstructed by
the harness itself so the RED column of the C-2 family cannot be a prediction.

Round history for the same stdout lines, all reproduced by an independent auditor at the
time: the round-2 stdout (`R2_REPAIRED bytes=122446 … RED lines=511 / GREEN lines=644`,
RP6-P0 output sha `66959360…dc0e`, RP7 output sha `1ebedc0d…7f4b`) is recorded in
`PATHSCOPE_CLAUDE_T1_EXEC_AUDIT_2026-08-12.md`; the round-3 stdout (`R2_REPAIRED
bytes=124251 sha256=0724967E…25F7`, `RED lines=552 / GREEN lines=1189`, RP7 output sha
`1f59ab2e…b395`) is recorded and byte-reproduced in
`PATHSCOPE_CODEX_T1_EXEC_AUDIT_R3_2026-08-13.md` §2.

Two round-4 facts about the real blocks are worth stating explicitly:

* `RP6-P0` output is **byte-identical to round 3** — its determinism digest
  `2e9d6f44…05db` is unchanged. The C-2 member grammar adds nothing to that block, which is
  the measured form of the premise behind owner decision §1 of
  `WPI_OWNER_DECISIONS_2026-08-13.md` ("the audited block contains none of the surviving
  assignment forms").
* `RP7-WPI-RO` gains **exactly one** coverage record (line 681,
  `seen_roots="$seen_roots$r "`, a whitespace-separated word list carrying `/`) and loses
  none: `coverage_issue_count` 336 → 337, every other count unchanged, rc 3 unchanged. Its
  digest therefore moves from `1f59ab2e…b395` to `224cda72…2ad2`.

Neither block changes verdict direction. The tool was not tuned to admit either.

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
$R3   = Join-Path $QA 'pathscope_prover_R3.py'
New-Item -ItemType Directory -Path $QA -Force | Out-Null

function New-Fixture([string]$Name, [string[]]$Lines) {
  [System.IO.File]::WriteAllText((Join-Path $QA $Name), (($Lines -join "`n") + "`n"))
}

# --- the round-1 artefact under audit, reconstructed from its pinned blob ---
cmd /c "git cat-file blob 3f0820a9a6412f769b59b23a41df3bc6808bf6dc > `"$R1`""
$h1 = (Get-FileHash -Algorithm SHA256 -LiteralPath $R1).Hash
$l1 = (Get-Item -LiteralPath $R1).Length
"R1_BASELINE bytes=$l1 sha256=$h1"
# --- the round-3 artefact, the pre-repair subject of the C-2 finding ---
cmd /c "git cat-file blob e600a107f2e2a790653cc544a94cd7436b7b070a > `"$R3`""
$h3 = (Get-FileHash -Algorithm SHA256 -LiteralPath $R3).Hash
$l3 = (Get-Item -LiteralPath $R3).Length
"R3_PREREPAIR bytes=$l3 sha256=$h3"
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
# PWD pinned outside the allowlist, so an ordinary relative pathname in an
# assignment value resolves to a forbidden absolute path (C-2 relative case).
New-Fixture 'constants_pwd_outside.env' @(
  'ROOT=/safe',
  'PWD=/elsewhere',
  'URL=http://127.0.0.1:8790/api/status',
  'HOST=198.51.100.10')

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

# --- C-2 repair (round 4): assignment-value MEMBER grammar, family P10 ---
# Round 3 recorded an assignment value only when the complete rendered value
# started with '/', './' or '../', and recorded that value only as one blob.
# These fixtures cover the three sites (prefix, env, export) across every member
# shape the round-3 predicate lost or mis-read: a later absolute member of a
# colon list, a bare first member, a whitespace word list, an ordinary relative
# pathname, an empty list member, a quoted pathname containing a blank, an
# escaped blank followed by a later member, command text carrying an option
# path, a URI-shaped value, and the benign controls that must stay rc 0.
New-Fixture 'c2_list_prefix.sh'      @('#!/bin/bash', 'LD_LIBRARY_PATH=$ROOT/lib:/etc/escape cat "$ROOT/f"')
New-Fixture 'c2_list_env.sh'         @('#!/bin/bash', 'env LD_LIBRARY_PATH=$ROOT/lib:/etc/escape cat "$ROOT/f"')
New-Fixture 'c2_list_export.sh'      @('#!/bin/bash', 'export LD_LIBRARY_PATH=$ROOT/lib:/etc/escape', 'cat "$ROOT/f"')
New-Fixture 'c2_list_bare_first.sh'  @('#!/bin/bash', 'LD_PRELOAD=bare.so:/etc/escape.so cat "$ROOT/f"')
New-Fixture 'c2_list_space.sh'       @('#!/bin/bash', 'LD_PRELOAD="bare.so /etc/escape.so" cat "$ROOT/f"')
New-Fixture 'c2_relative.sh'         @('#!/bin/bash', 'LD_PRELOAD=relative/path.so cat "$ROOT/f"')
New-Fixture 'c2_empty_member.sh'     @('#!/bin/bash', 'LD_LIBRARY_PATH=:/etc/escape cat "$ROOT/f"')
New-Fixture 'c2_quoted_space.sh'     @('#!/bin/bash', 'X="$ROOT dir/escape" cat "$ROOT/f"')
New-Fixture 'c2_escaped_space.sh'    @('#!/bin/bash', 'X=$ROOT/a\ b:/etc/escape cat "$ROOT/f"')
New-Fixture 'c2_command_text.sh'     @('#!/bin/bash', 'GIT_SSH_COMMAND="ssh -i /etc/key" cat "$ROOT/f"')
New-Fixture 'c2_uri_forbid.sh'       @('#!/bin/bash', 'WEBHOOK=http://198.51.100.10:9999/x cat "$ROOT/f"')
New-Fixture 'c2_uri_allow.sh'        @('#!/bin/bash', 'WEBHOOK="$URL" cat "$ROOT/f"')
New-Fixture 'c2_env_quoted.sh'       @('#!/bin/bash', 'env "LD_PRELOAD=/etc/evil.so" cat "$ROOT/f"')
New-Fixture 'c2_bare_soname.sh'      @('#!/bin/bash', 'LD_PRELOAD=libc.so cat "$ROOT/f"')
New-Fixture 'c2_allow_list.sh'       @('#!/bin/bash', 'LD_LIBRARY_PATH=$ROOT/lib:$ROOT/lib64 cat "$ROOT/f"')
New-Fixture 'c2_benign_scalars.sh'   @('#!/bin/bash', 'IFS=: LC_ALL=C count=1 cat "$ROOT/f"')
New-Fixture 'c2_benign_words.sh'     @('#!/bin/bash', 'MSG="Permission denied" cat "$ROOT/f"')
New-Fixture 'c2_words_with_path.sh'  @('#!/bin/bash', 'MSG="denied /etc/secret" cat "$ROOT/f"')

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

# The C-2 family is run against three provers: round 1, the round-3 pre-repair
# subject of the finding, and the repaired bytes.
$C2CASES = @(
  @('c2_list_prefix','constants.env','allowlist.txt'),
  @('c2_list_env','constants.env','allowlist.txt'),
  @('c2_list_export','constants.env','allowlist.txt'),
  @('c2_list_bare_first','constants.env','allowlist.txt'),
  @('c2_list_space','constants.env','allowlist.txt'),
  @('c2_relative','constants_pwd_outside.env','allowlist.txt'),
  @('c2_empty_member','constants.env','allowlist.txt'),
  @('c2_quoted_space','constants.env','allowlist.txt'),
  @('c2_escaped_space','constants.env','allowlist.txt'),
  @('c2_command_text','constants.env','allowlist.txt'),
  @('c2_uri_forbid','constants.env','allowlist.txt'),
  @('c2_uri_allow','constants.env','allowlist.txt'),
  @('c2_env_quoted','constants.env','allowlist.txt'),
  @('c2_bare_soname','constants.env','allowlist.txt'),
  @('c2_allow_list','constants.env','allowlist.txt'),
  @('c2_benign_scalars','constants.env','allowlist.txt'),
  @('c2_benign_words','constants.env','allowlist.txt'),
  @('c2_words_with_path','constants.env','allowlist.txt')
)
$CASES = $CASES + $C2CASES

function Invoke-Suite([string]$Prover, [string]$OutFile, [object[]]$List, [bool]$WithBlocks) {
  if ($null -eq $List) { $List = $CASES }
  $lines = New-Object System.Collections.Generic.List[string]
  foreach ($case in $List) {
    $name, $constants, $allowlist = $case
    $lines.Add("=== $name ===")
    $out = & python -B $Prover (Join-Path $QA "$name.sh") (Join-Path $QA $constants) (Join-Path $QA $allowlist) 2>&1
    $rc = $LASTEXITCODE
    foreach ($line in $out) { $lines.Add(([string]$line).Replace($QA, '<QA>')) }
    $lines.Add("COMMAND_RC=$rc")
  }
  if ($WithBlocks) {
  foreach ($pair in @(@('RP6-P0','placeholder.constants'), @('RP7-WPI-RO','placeholder.constants'),
                      @('RP6-P0','real.constants'), @('RP7-WPI-RO','real.constants'))) {
    $block, $constants = $pair
    $lines.Add("=== $block with $constants ===")
    $out = & python -B $Prover (Join-Path $QA "$block.sh") (Join-Path $QA $constants) (Join-Path $QA 'real.allowlist') 2>&1
    $rc = $LASTEXITCODE
    foreach ($line in $out) { $lines.Add(([string]$line).Replace($QA, '<QA>')) }
    $lines.Add("COMMAND_RC=$rc")
  }
  }
  [System.IO.File]::WriteAllText($OutFile, (($lines -join "`n") + "`n"))
  "WROTE $OutFile lines=$($lines.Count)"
}

Invoke-Suite $R1   (Join-Path $QA 'RED_R1.txt')   $CASES   $true
Invoke-Suite $TOOL (Join-Path $QA 'GREEN_R2.txt') $CASES   $true
Invoke-Suite $R3   (Join-Path $QA 'RED_R3.txt')   $C2CASES $false

# --- determinism: same input, same bytes, same order ---
foreach ($pair in @(@('find_exec','constants.env','allowlist.txt'),
                    @('assign_prefix','constants.env','allowlist.txt'),
                    @('c2_list_prefix','constants.env','allowlist.txt'),
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

## Round 4 — C-2 repair (assignment-value MEMBER grammar, family P10)

**Status: EXECUTED 2026-08-13. Every cell below is measured, not predicted.** The RED
column of this family is the committed round-3 blob
`e600a107f2e2a790653cc544a94cd7436b7b070a` (124251 B, SHA-256 `0724967E…25F7`) — the exact
bytes the Codex re-audit rejected — reconstructed by the harness and run by the harness, in
`RED_R3.txt`. The `R1 rc` column is the round-1 blob, from `RED_R1.txt`. The `R4 rc` column
and the terminal accounting are from `GREEN_R2.txt`.

| fixture | shell fragment | R1 rc | **R3 rc (pre-repair)** | **R4 rc** | round-4 terminal accounting |
|---|---|---:|---:|---:|---|
| `c2_list_prefix` | `LD_LIBRARY_PATH=$ROOT/lib:/etc/escape cat "$ROOT/f"` | 0 | **0** | **1** | `/etc/escape` FORBID; `/safe/f`, `/safe/lib`, `/safe/lib:/etc/escape` ALLOW-LEXICAL |
| `c2_list_env` | `env LD_LIBRARY_PATH=$ROOT/lib:/etc/escape cat "$ROOT/f"` | 0 | **0** | **1** | `/etc/escape` FORBID; `/safe/f`, `/safe/lib`, `/safe/lib:/etc/escape` ALLOW-LEXICAL |
| `c2_list_export` | `export LD_LIBRARY_PATH=$ROOT/lib:/etc/escape` ; `cat "$ROOT/f"` | 0 | **0** | **1** | `/etc/escape` FORBID; `/safe/f`, `/safe/lib`, `/safe/lib:/etc/escape` ALLOW-LEXICAL |
| `c2_list_bare_first` | `LD_PRELOAD=bare.so:/etc/escape.so cat "$ROOT/f"` | 0 | **0** | **1** | `/etc/escape.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c2_list_space` | `LD_PRELOAD="bare.so /etc/escape.so" cat "$ROOT/f"` | 0 | **0** | **3** | `/etc/escape.so` FORBID; `/safe/f` ALLOW-LEXICAL; 1 coverage record (word-list reading) |
| `c2_relative` | `LD_PRELOAD=relative/path.so cat "$ROOT/f"` (PWD `/elsewhere`) | 0 | **0** | **1** | `/elsewhere/relative/path.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c2_empty_member` | `LD_LIBRARY_PATH=:/etc/escape cat "$ROOT/f"` | 0 | **0** | **3** | `/etc/escape` FORBID; `/safe/f` ALLOW-LEXICAL; 1 coverage record (empty member) |
| `c2_quoted_space` | `X="$ROOT dir/escape" cat "$ROOT/f"` | 0 | **1** | **1** | `/safe dir/escape` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c2_escaped_space` | `X=$ROOT/a\ b:/etc/escape cat "$ROOT/f"` | 0 | **0** | **1** | `/etc/escape` FORBID; `/safe/a b`, `/safe/a b:/etc/escape`, `/safe/f` ALLOW-LEXICAL |
| `c2_command_text` | `GIT_SSH_COMMAND="ssh -i /etc/key" cat "$ROOT/f"` | 0 | **0** | **3** | `/etc/key` FORBID; `/safe/f` ALLOW-LEXICAL; 1 coverage record (command text) |
| `c2_uri_forbid` | `WEBHOOK=http://198.51.100.10:9999/x cat "$ROOT/f"` | 0 | **0** | **1** | ENDPOINT `198.51.100.10:9999` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c2_uri_allow` | `WEBHOOK="$URL" cat "$ROOT/f"` | 0 | **0** | **0** | ENDPOINT `127.0.0.1:8790` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL (control) |
| `c2_env_quoted` | `env "LD_PRELOAD=/etc/evil.so" cat "$ROOT/f"` | 0 | **0** | **1** | `/etc/evil.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c2_bare_soname` | `LD_PRELOAD=libc.so cat "$ROOT/f"` | 0 | **0** | **0** | `/safe/f` ALLOW-LEXICAL — the **disclosed residual**, see below |
| `c2_allow_list` | `LD_LIBRARY_PATH=$ROOT/lib:$ROOT/lib64 cat "$ROOT/f"` | 0 | **0** | **0** | 4 ALLOW-LEXICAL rows, no false positive (control) |
| `c2_benign_scalars` | `IFS=: LC_ALL=C count=1 cat "$ROOT/f"` | 0 | **0** | **0** | `/safe/f` ALLOW-LEXICAL only (control) |
| `c2_benign_words` | `MSG="Permission denied" cat "$ROOT/f"` | 0 | **0** | **0** | `/safe/f` ALLOW-LEXICAL only (control) |
| `c2_words_with_path` | `MSG="denied /etc/secret" cat "$ROOT/f"` | 0 | **0** | **3** | `/etc/secret` FORBID; `/safe/f` ALLOW-LEXICAL; 1 coverage record — the positive twin of the row above |

**Twelve** fixtures move from a silent `PASS rc=0` on the pre-repair bytes to a non-zero
verdict with the out-of-allowlist lexeme printed. **Five** are controls whose rc must not
move and does not — two of them, `c2_uri_allow` and `c2_allow_list`, additionally print the
ALLOW-LEXICAL rows that round 3 dropped entirely, which is the same defect seen from the
allowed side. `c2_quoted_space` is not a closure — it is the **regression guard** for the defect
the Lead reproduced in the incomplete first attempt: round 3 already returned rc 1 there and
round 4 must keep returning rc 1 with the same single FORBID row for the whole quoted
pathname. Its falsification is MUT-A below.

### The rule, stated so it can be attacked

`record_assignment_members` (`pathscope_prover.py`) decides on the grammar of the value,
never on the variable name:

1. **URI.** A value (or member) matching `^[A-Za-z][A-Za-z0-9+.-]*://` belongs to the
   **endpoint** domain and is never colon-split into fragments.
2. **Whitespace.** The lexer already guarantees an assignment word contains no *unquoted*
   whitespace, and the shell does not word-split assignment values — so no blank here is a
   shell separator, and `X="$ROOT dir/escape"` stays one pathname. A *consumer* may still
   split it. The consumer reading is treated as live — one specific coverage record plus a
   row for every path-carrying word — when some word contains `/` **and** (some word is
   option-shaped, or a word after the first is absolute, or the first word is not
   path-shaped). A value where no word contains `/` carries no pathname under any reading
   and stays benign.
3. **Colon members.** Always applied, including when the value starts with `/`, because a
   consumer splits a path list regardless of shell quoting. The whole candidate is recorded
   as well, so neither the single-pathname reading nor any member can disappear.
4. **Empty member.** An empty member is fail-closed with a coverage record **only when the
   same value also has a path member** — so `IFS=:` is untouched by grammar, not by name.
5. **Terminal disposition for every member:** endpoint, path, empty, or `bare`.

### Disclosed residual, stated precisely this time

A member with **no `/`** — a bare soname `libc.so`, a scalar `1`, a tool name, an option
word — is resolved by the consumer's own search rules and is not an argv pathname, so it is
outside the lexical-argv-scope contract this tool proves and carries no row. That is the
whole residual. Unlike the round-3 disclosure, it no longer hides mixed lists
(`bare.so:/etc/escape.so` is caught), whitespace lists (`bare.so /etc/escape.so` is caught),
or relative pathnames (`relative/path.so` is caught).

Two consequences are disclosed rather than claimed away:

* The union of readings is **conservative, not exact**. `MSG="denied /etc/secret"` is
  rejected even though no consumer opens `/etc/secret` there. A fail-closed prover is
  allowed to over-reject; it is not allowed to under-report. `c2_words_with_path` records
  that behaviour deliberately.
* A whole-value row such as `/safe/lib:/etc/escape` ALLOW-LEXICAL is the single-pathname
  reading of a value whose list reading is also recorded. It never stands alone: the same
  run prints `/etc/escape` FORBID and the run rejects.

### D026 falsification — deliberate mutations of the round-4 source

D026 requires that a test offered as closure evidence be shown to fail without the fix. The
round-3 blob is the primary RED column above. Three additional mutations were applied to
copies of the round-4 source outside the repository (`C:\tmp\ps_c2\MUT_*.py`) and executed
against the same fixtures:

| mutation | one-line change | measured effect |
|---|---|---|
| **MUT-A** naive word split | `candidates = [rendered]` → `candidates = words if words else [rendered]` | `c2_quoted_space` **rc 1 → rc 0**, printing `/safe` and `/safe/dir/escape` as two ALLOW-LEXICAL rows and no FORBID. This is exactly the false PASS the Lead reproduced in the incomplete first attempt. |
| **MUT-B** no colon members | the member loop guard → `if False:` | `c2_list_prefix` **rc 1 → rc 0** (only `/safe/lib:/etc/escape` ALLOW remains), `c2_escaped_space` **rc 1 → rc 0**, `c2_empty_member` **rc 3 → rc 0** with no assignment row at all. |
| **MUT-C** no word-list reading | `if word_list_reading:` → `if False:` | `c2_command_text` and `c2_list_space` keep rc 3, but for the wrong reason: `/etc/key` and `/etc/escape.so` **vanish from the report** and are replaced by a bogus allowlisted relative path (`/safe/ssh -i /etc/key`, `/safe/bare.so /etc/escape.so`), leaving only a provenance issue. The sink-visibility property, not the rc, is what MUT-C falsifies. |

MUT-A's measured output, verbatim:

```text
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/dir/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
```

### Regression surface of round 4

Every one of the 87 fixture cases was run under the round-3 blob and the round-4 source and
compared byte for byte. Exactly **seventeen** differ:

* **fourteen** of the eighteen C-2 fixtures above. The other four — `c2_quoted_space`,
  `c2_bare_soname`, `c2_benign_scalars`, `c2_benign_words` — are byte-identical under both
  provers, which is the point of a regression guard and of three controls.
* **three** pre-existing endpoint cases — `curl_upload`, `curl_net`, `devtcp_allow` — whose
  only change is the NIT-1 label, `verdict=ALLOW` → `verdict=ALLOW-LEXICAL`. Their rc values
  are unchanged (1, 0, 3).

The remaining **sixty-six** pre-existing fixture cases are byte-identical under round 3 and
round 4. On the two real blocks, `RP6-P0` is byte-identical and `RP7-WPI-RO` gains one
coverage record and loses nothing.

All seven round-3 P9 assignment fixtures are **byte-identical** under round 3 and round 4:
the C-1 closure is preserved, not re-derived.

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
=== assign_prefix ===
PATHSCOPE shell=<QA>\assign_prefix.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_prefix_allow ===
PATHSCOPE shell=<QA>\assign_prefix_allow.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_bare ===
PATHSCOPE shell=<QA>\assign_bare.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_benign ===
PATHSCOPE shell=<QA>\assign_benign.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_export ===
PATHSCOPE shell=<QA>\assign_export.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_env ===
PATHSCOPE shell=<QA>\assign_env.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_multi ===
PATHSCOPE shell=<QA>\assign_multi.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_prefix ===
PATHSCOPE shell=<QA>\c2_list_prefix.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_env ===
PATHSCOPE shell=<QA>\c2_list_env.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_export ===
PATHSCOPE shell=<QA>\c2_list_export.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_bare_first ===
PATHSCOPE shell=<QA>\c2_list_bare_first.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_space ===
PATHSCOPE shell=<QA>\c2_list_space.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_relative ===
PATHSCOPE shell=<QA>\c2_relative.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_empty_member ===
PATHSCOPE shell=<QA>\c2_empty_member.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_quoted_space ===
PATHSCOPE shell=<QA>\c2_quoted_space.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_escaped_space ===
PATHSCOPE shell=<QA>\c2_escaped_space.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_command_text ===
PATHSCOPE shell=<QA>\c2_command_text.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_uri_forbid ===
PATHSCOPE shell=<QA>\c2_uri_forbid.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_uri_allow ===
PATHSCOPE shell=<QA>\c2_uri_allow.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_env_quoted ===
PATHSCOPE shell=<QA>\c2_env_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_bare_soname ===
PATHSCOPE shell=<QA>\c2_bare_soname.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_allow_list ===
PATHSCOPE shell=<QA>\c2_allow_list.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_benign_scalars ===
PATHSCOPE shell=<QA>\c2_benign_scalars.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_benign_words ===
PATHSCOPE shell=<QA>\c2_benign_words.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_words_with_path ===
PATHSCOPE shell=<QA>\c2_words_with_path.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
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
PATH value=/safe/input verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix,line=3:cat
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
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/etc/mtc-bridge/x verdict=FORBID rule=- sources=NONE uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== dynamic ===
PATHSCOPE shell=<QA>\dynamic.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=assignment value is not statically known: command substitution expression=p="$(printf /safe)"
UNRESOLVED line=3 kind=unresolved_path reason=cat argument is not statically known: command substitution expression="$p/x"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nested ===
PATHSCOPE shell=<QA>\nested.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is not statically known: command substitution expression=unused="$(cat /etc/shadow)"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
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
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== curl_net ===
PATHSCOPE shell=<QA>\curl_net.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:curl
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
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=NONE uses=line=2:redirection < /dev/tcp
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
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is not statically known: command substitution expression=unused="`cat /etc/shadow`"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
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
=== assign_prefix ===
PATHSCOPE shell=<QA>\assign_prefix.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_prefix_allow ===
PATHSCOPE shell=<QA>\assign_prefix_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/ok.so verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== assign_bare ===
PATHSCOPE shell=<QA>\assign_bare.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_benign ===
PATHSCOPE shell=<QA>\assign_benign.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== assign_export ===
PATHSCOPE shell=<QA>\assign_export.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:export assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_env ===
PATHSCOPE shell=<QA>\assign_env.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:env assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_multi ===
PATHSCOPE shell=<QA>\assign_multi.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/a.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/etc/b.sh verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_list_prefix ===
PATHSCOPE shell=<QA>\c2_list_prefix.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_list_env ===
PATHSCOPE shell=<QA>\c2_list_env.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=ROOT uses=line=2:env assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:env assignment
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:env assignment
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_list_export ===
PATHSCOPE shell=<QA>\c2_list_export.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=ROOT uses=line=2:export assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATH value=/safe/lib verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:export assignment
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:export assignment
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_list_bare_first ===
PATHSCOPE shell=<QA>\c2_list_bare_first.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_list_space ===
PATHSCOPE shell=<QA>\c2_list_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ and this tool does not model which consumer splits it expression=LD_PRELOAD="bare.so /etc/escape.so"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_relative ===
PATHSCOPE shell=<QA>\c2_relative.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/elsewhere/relative/path.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_empty_member ===
PATHSCOPE shell=<QA>\c2_empty_member.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment path list contains an empty member, which names the consumer's current directory rather than a static pathname expression=LD_LIBRARY_PATH=:/etc/escape
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_quoted_space ===
PATHSCOPE shell=<QA>\c2_quoted_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe dir/escape verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_escaped_space ===
PATHSCOPE shell=<QA>\c2_escaped_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/a b verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/a b:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_command_text ===
PATHSCOPE shell=<QA>\c2_command_text.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/key verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ and this tool does not model which consumer splits it expression=GIT_SSH_COMMAND="ssh -i /etc/key"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_uri_forbid ===
PATHSCOPE shell=<QA>\c2_uri_forbid.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=198.51.100.10:9999 verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_uri_allow ===
PATHSCOPE shell=<QA>\c2_uri_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_env_quoted ===
PATHSCOPE shell=<QA>\c2_env_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:env assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_bare_soname ===
PATHSCOPE shell=<QA>\c2_bare_soname.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_allow_list ===
PATHSCOPE shell=<QA>\c2_allow_list.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/lib64 verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/lib:/safe/lib64 verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_benign_scalars ===
PATHSCOPE shell=<QA>\c2_benign_scalars.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_benign_words ===
PATHSCOPE shell=<QA>\c2_benign_words.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_words_with_path ===
PATHSCOPE shell=<QA>\c2_words_with_path.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/secret verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ and this tool does not model which consumer splits it expression=MSG="denied /etc/secret"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== RP6-P0 with placeholder.constants ===
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
=== RP7-WPI-RO with placeholder.constants ===
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
=== RP6-P0 with real.constants ===
PATHSCOPE shell=<QA>\RP6-P0.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=7 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=3 unresolved_endpoint_count=0 coverage_issue_count=200 provenance_issue_count=0 parse_issue_count=0
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=398:redirection >,line=400:redirection >
PATH value=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python verdict=ALLOW-LEXICAL rule=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=P0_VENV_ROOT uses=line=751:assignment prefix
PATH value=/proc/self/fd/8 verdict=FORBID rule=- sources=NONE uses=line=263:assignment prefix
PATH value=/proc/self/ns/mnt verdict=FORBID rule=- sources=NONE uses=line=262:assignment prefix
PATH value=/proc/self/ns/net verdict=FORBID rule=- sources=NONE uses=line=260:assignment prefix
PATH value=/proc/self/ns/pid verdict=FORBID rule=- sources=NONE uses=line=261:assignment prefix
PATH value=/proc/self/ns/user verdict=FORBID rule=- sources=NONE uses=line=259:assignment prefix
UNRESOLVED line=158 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=163 kind=coverage reason=opaque command p0_on_err has no registered argv grammar expression=p0_on_err
UNRESOLVED line=173 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${1-} expression=s="${1-}"
UNRESOLVED line=174 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s//$'\r'/ } expression=s="${s//$'\r'/ }"
UNRESOLVED line=175 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s//$'\n'/ } expression=s="${s//$'\n'/ }"
UNRESOLVED line=179 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s:0:400} expression=P0_SAFE="${s:0:400}"
UNRESOLVED line=187 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${1-} expression=raw="${1-}"
UNRESOLVED line=214 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=rest="$1"
UNRESOLVED line=214 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=needle="$2"
UNRESOLVED line=216 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*"$needle"} expression=rest="${rest#*"$needle"}"
UNRESOLVED line=217 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=n=$(( n + 1 ))
UNRESOLVED line=219 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=P0_COUNT="$n"
UNRESOLVED line=235 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=map="$1"
UNRESOLVED line=235 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=want="$2"
UNRESOLVED line=248 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${e#*=} expression=P0_LOOKUP="${e#*=}"
UNRESOLVED line=363 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=P0_TOOL_COUNT_EXPECTED=$(( P0_TOOL_COUNT_EXPECTED + 1 ))
UNRESOLVED line=410 kind=coverage reason=opaque command argument: unpinned variable RUNID expression="$RUNID"
UNRESOLVED line=410 kind=coverage reason=opaque command rp0_require_safe_component has no registered argv grammar expression=rp0_require_safe_component
UNRESOLVED line=412 kind=coverage reason=opaque command argument: unpinned variable EV_STAGE_ID expression="$EV_STAGE_ID"
UNRESOLVED line=412 kind=coverage reason=opaque command rp0_require_safe_component has no registered argv grammar expression=rp0_require_safe_component
UNRESOLVED line=424 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=name="$1"
UNRESOLVED line=424 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=val="$2"
UNRESOLVED line=424 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=min="$3"
UNRESOLVED line=482 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=P0_FORBIDDEN_GID_COUNT=$(( P0_FORBIDDEN_GID_COUNT + 1 ))
UNRESOLVED line=542 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_STAT expression=P0_FROZEN_PIN="$P0_FIXED_STAT"
UNRESOLVED line=543 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_READLINK expression=P0_FROZEN_PIN="$P0_FIXED_READLINK"
UNRESOLVED line=544 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_ENV expression=P0_FROZEN_PIN="$P0_FIXED_ENV"
UNRESOLVED line=545 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_FIND expression=P0_FROZEN_PIN="$P0_FIXED_FIND"
UNRESOLVED line=546 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_SHA256SUM expression=P0_FROZEN_PIN="$P0_FIXED_SHA256SUM"
UNRESOLVED line=547 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_SYSTEMCTL expression=P0_FROZEN_PIN="$P0_FIXED_SYSTEMCTL"
UNRESOLVED line=548 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_SS expression=P0_FROZEN_PIN="$P0_FIXED_SS"
UNRESOLVED line=549 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_CURL expression=P0_FROZEN_PIN="$P0_FIXED_CURL"
UNRESOLVED line=550 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_TIMEOUT expression=P0_FROZEN_PIN="$P0_FIXED_TIMEOUT"
UNRESOLVED line=551 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_ID expression=P0_FROZEN_PIN="$P0_FIXED_ID"
UNRESOLVED line=552 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_GETENT expression=P0_FROZEN_PIN="$P0_FIXED_GETENT"
UNRESOLVED line=553 kind=coverage reason=assignment value is not statically known: unpinned variable P0_FIXED_TRUSTED_PYTHON expression=P0_FROZEN_PIN="$P0_FIXED_TRUSTED_PYTHON"
UNRESOLVED line=572 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${p0_pin%%=*} expression=p0_pin_name="${p0_pin%%=*}"
UNRESOLVED line=573 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${p0_pin#*=} expression=p0_pin_path="${p0_pin#*=}"
UNRESOLVED line=625 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${p0_pin%%=*} expression=P0_PIN_SEEN="$P0_PIN_SEEN$p0_pin_name "
UNRESOLVED line=626 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=P0_PIN_COUNT=$(( P0_PIN_COUNT + 1 ))
UNRESOLVED line=700 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=field="$1"
UNRESOLVED line=700 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=label="$2"
UNRESOLVED line=700 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=value="$3"
UNRESOLVED line=704 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${inner%\]} expression=inner="${inner%\]}"
UNRESOLVED line=704 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${value#*:\[} expression=inner="${value#*:\[}"
UNRESOLVED line=780 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=t="$1"
UNRESOLVED line=781 kind=coverage reason=assignment value is not statically known: command substitution expression=resolved="$(command -v "$t" 2>&1)"
UNRESOLVED line=781 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=797 kind=coverage reason=assignment value is not statically known: unpinned variable P0_LOOKUP expression=pin="$P0_LOOKUP"
UNRESOLVED line=813 kind=coverage reason=assignment value is not statically known: unpinned variable P0_LOOKUP expression=rl="$P0_LOOKUP"
UNRESOLVED line=814 kind=coverage reason=assignment value is not statically known: command substitution expression=canon="$(LC_ALL=C "$rl" -v -f -- "$resolved" 2>&1)"
UNRESOLVED line=814 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=crc=$?
UNRESOLVED line=814 kind=coverage reason=dynamic command name: unpinned variable rl expression="$rl"
UNRESOLVED line=827 kind=coverage reason=assignment value is not statically known: unpinned variable P0_LOOKUP expression=resolved="$pin"
UNRESOLVED line=845 kind=unresolved_path reason=unpinned variable P0_LOOKUP expression="$resolved"
UNRESOLVED line=847 kind=coverage reason=assignment value is not statically known: unpinned variable P0_TOOLS_RESOLVED expression=P0_TOOLS_RESOLVED="$P0_TOOLS_RESOLVED $t=$resolved"
UNRESOLVED line=848 kind=coverage reason=assignment value is not statically known: unpinned variable P0_TOOLS_RESOLUTION expression=P0_TOOLS_RESOLUTION="$P0_TOOLS_RESOLUTION $t=$P0_RESOLUTION"
UNRESOLVED line=855 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=label="$1"
UNRESOLVED line=855 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=p="$2"
UNRESOLVED line=857 kind=coverage reason=assignment value is not statically known: command substitution expression=raw="$(LC_ALL=C "$P0_STAT" -c '%F|%a|%u:%g' -- "$p" 2>&1)"
UNRESOLVED line=857 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=857 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=857 kind=coverage reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=872 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw%%|*} expression=P0_META_KIND="${raw%%|*}"
UNRESOLVED line=873 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw#*|} expression=rest="${raw#*|}"
UNRESOLVED line=874 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%|*} expression=P0_META_MODE="${rest%%|*}"
UNRESOLVED line=875 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*|} expression=P0_META_OWNER="${rest#*|}"
UNRESOLVED line=919 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=P0_TOOL_COUNT=$(( P0_TOOL_COUNT + 1 ))
UNRESOLVED line=938 kind=coverage reason=assignment value is not statically known: command substitution expression=rawpath="$(LC_ALL=C "$P0_READLINK" -v -- "$P0_FD_SELF" 2>&1)"
UNRESOLVED line=938 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=938 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=938 kind=coverage reason=opaque command  may forward a path or endpoint expression="$P0_FD_SELF"
UNRESOLVED line=945 kind=coverage reason=assignment value is not statically known: command substitution expression=fdid="$(LC_ALL=C "$P0_STAT" -L -c '%d:%i' -- "$P0_FD_SELF" 2>&1)"
UNRESOLVED line=945 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=945 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=945 kind=coverage reason=opaque command  may forward a path or endpoint expression="$P0_FD_SELF"
UNRESOLVED line=952 kind=coverage reason=assignment value is not statically known: command substitution expression=logid="$(LC_ALL=C "$P0_STAT" -c '%d:%i' -- "$EV_LOG" 2>&1)"
UNRESOLVED line=952 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=952 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=952 kind=coverage reason=opaque command argument: unpinned variable EV_LOG expression="$EV_LOG"
UNRESOLVED line=991 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=label="$1"
UNRESOLVED line=991 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=flag="$2"
UNRESOLVED line=992 kind=coverage reason=assignment value is not statically known: command substitution expression=raw="$(LC_ALL=C "$P0_ID" "$flag" 2>&1)"
UNRESOLVED line=992 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=992 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=992 kind=coverage reason=opaque command argument: unpinned variable flag expression="$flag"
UNRESOLVED line=1015 kind=coverage reason=assignment value is not statically known: command substitution expression=P0_CAPTURE="$raw"
UNRESOLVED line=1020 kind=coverage reason=assignment value is not statically known: unpinned variable P0_CAPTURE expression=uid="$P0_CAPTURE"
UNRESOLVED line=1024 kind=coverage reason=assignment value is not statically known: unpinned variable P0_CAPTURE expression=gid="$P0_CAPTURE"
UNRESOLVED line=1028 kind=coverage reason=assignment value is not statically known: unpinned variable P0_CAPTURE expression=gids="$P0_CAPTURE"
UNRESOLVED line=1053 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=count=$(( count + 1 ))
UNRESOLVED line=1155 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=acct="$1"
UNRESOLVED line=1156 kind=coverage reason=array assignment is outside the accepted scalar subset expression=p0_pw_parts=(...)
UNRESOLVED line=1166 kind=unresolved_path reason=relative path depends on unpinned PWD expression=<
UNRESOLVED line=1168 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=getent_rc=$?
UNRESOLVED line=1168 kind=coverage reason=dynamic command name: unpinned variable P0_GETENT expression="$P0_GETENT"
UNRESOLVED line=1176 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${p0_pw_parts[$(( ${#p0_pw_parts[@]} expression=rc_record="${p0_pw_parts[$(( ${#p0_pw_parts[@]} - 1 ))]}"
UNRESOLVED line=1179 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rc_record#P0_GETENT_RC=} expression=rc="${rc_record#P0_GETENT_RC=}"
UNRESOLVED line=1182 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rc_record#P0_GETENT_RC=} expression=P0_PW_RC="$rc"
UNRESOLVED line=1191 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${p0_pw_parts[0]} expression=raw="${p0_pw_parts[0]}"
UNRESOLVED line=1192 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${p0_pw_parts[1]} expression=rc_record="${p0_pw_parts[1]}"
UNRESOLVED line=1194 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rc_record#P0_GETENT_RC=} expression=rc="${rc_record#P0_GETENT_RC=}"
UNRESOLVED line=1200 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rc_record#P0_GETENT_RC=} expression=P0_PW_RC="$rc"
UNRESOLVED line=1207 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw%$'\n'} expression=raw="${raw%$'\n'}"
UNRESOLVED line=1213 kind=coverage reason=assignment value is not statically known: unpinned variable P0_SAFE expression=P0_PW_DIAG="$P0_SAFE"
UNRESOLVED line=1220 kind=coverage reason=assignment value is not statically known: unpinned variable P0_SAFE expression=P0_PW_DIAG="$P0_SAFE"
UNRESOLVED line=1225 kind=coverage reason=assignment value is not statically known: unpinned variable P0_SAFE expression=P0_PW_DIAG="$P0_SAFE"
UNRESOLVED line=1232 kind=coverage reason=assignment value is not statically known: unpinned variable P0_COUNT expression=n_colon="$P0_COUNT"
UNRESOLVED line=1234 kind=coverage reason=assignment value is not statically known: unpinned variable P0_SAFE expression=P0_PW_DIAG="$P0_SAFE"
UNRESOLVED line=1237 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw#*:} expression=rest="${raw#*:}"
UNRESOLVED line=1237 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw%%:*} expression=f1="${raw%%:*}"
UNRESOLVED line=1238 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*:} expression=rest="${rest#*:}"
UNRESOLVED line=1238 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%:*} expression=f2="${rest%%:*}"
UNRESOLVED line=1239 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*:} expression=rest="${rest#*:}"
UNRESOLVED line=1239 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%:*} expression=f3="${rest%%:*}"
UNRESOLVED line=1240 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*:} expression=rest="${rest#*:}"
UNRESOLVED line=1240 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%:*} expression=f4="${rest%%:*}"
UNRESOLVED line=1241 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*:} expression=rest="${rest#*:}"
UNRESOLVED line=1241 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%:*} expression=f5="${rest%%:*}"
UNRESOLVED line=1242 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*:} expression=rest="${rest#*:}"
UNRESOLVED line=1242 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%:*} expression=f6="${rest%%:*}"
UNRESOLVED line=1243 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*:} expression=f7="$rest"
UNRESOLVED line=1245 kind=coverage reason=assignment value is not statically known: unpinned variable P0_SAFE expression=P0_PW_DIAG="$P0_SAFE"
UNRESOLVED line=1247 kind=coverage reason=assignment value is not statically known: unpinned variable P0_SAFE expression=P0_PW_DIAG="$P0_SAFE"
UNRESOLVED line=1248 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw%%:*} expression=P0_PW_NAME="$f1"
UNRESOLVED line=1248 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%:*} expression=P0_PW_GID="$f4"
UNRESOLVED line=1248 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%:*} expression=P0_PW_UID="$f3"
UNRESOLVED line=1249 kind=coverage reason=assignment value is not statically known: unpinned variable P0_SAFE expression=P0_PW_DIAG="$P0_SAFE"
UNRESOLVED line=1255 kind=coverage reason=assignment value is not statically known: unpinned variable P0_CAPTURE expression=live_uid="$P0_CAPTURE"
UNRESOLVED line=1256 kind=coverage reason=assignment value is not statically known: unpinned variable P0_CAPTURE expression=live_gid="$P0_CAPTURE"
UNRESOLVED line=1319 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=field="$1"
UNRESOLVED line=1319 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=label="$2"
UNRESOLVED line=1319 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=path="$3"
UNRESOLVED line=1319 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $4 expression=attested="$4"
UNRESOLVED line=1320 kind=coverage reason=assignment value is not statically known: command substitution expression=raw="$(LC_ALL=C "$P0_READLINK" -v -- "$path" 2>&1)"
UNRESOLVED line=1320 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1320 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1320 kind=coverage reason=opaque command argument: unpinned variable path expression="$path"
UNRESOLVED line=1331 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${inner%\]} expression=inner="${inner%\]}"
UNRESOLVED line=1331 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw#*:\[} expression=inner="${raw#*:\[}"
UNRESOLVED line=1339 kind=coverage reason=assignment value is not statically known: command substitution expression=P0_NS_VALUE="$raw"
UNRESOLVED line=1346 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=field="$1"
UNRESOLVED line=1346 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=path="$2"
UNRESOLVED line=1348 kind=coverage reason=assignment value is not statically known: command substitution expression=raw="$(LC_ALL=C "$P0_STAT" -L -c '%d' -- "$path" 2>&1)"
UNRESOLVED line=1348 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1348 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1348 kind=coverage reason=opaque command argument: unpinned variable path expression="$path"
UNRESOLVED line=1357 kind=coverage reason=assignment value is not statically known: command substitution expression=P0_DEVICE="$raw"
UNRESOLVED line=1368 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=field="$1"
UNRESOLVED line=1368 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=path="$2"
UNRESOLVED line=1368 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=root_dev="$3"
UNRESOLVED line=1382 kind=coverage reason=assignment value is not statically known: unpinned variable P0_NS_VALUE expression=user="$P0_NS_VALUE"
UNRESOLVED line=1383 kind=coverage reason=assignment value is not statically known: unpinned variable P0_NS_VALUE expression=mnt="$P0_NS_VALUE"
UNRESOLVED line=1384 kind=coverage reason=assignment value is not statically known: unpinned variable P0_NS_VALUE expression=pid="$P0_NS_VALUE"
UNRESOLVED line=1385 kind=coverage reason=assignment value is not statically known: unpinned variable P0_NS_VALUE expression=net="$P0_NS_VALUE"
UNRESOLVED line=1386 kind=coverage reason=assignment value is not statically known: command substitution expression=root_canon="$(LC_ALL=C "$P0_READLINK" -v -f -- / 2>&1)"
UNRESOLVED line=1386 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1386 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1386 kind=coverage reason=opaque command  may forward a path or endpoint expression=/
UNRESOLVED line=1394 kind=coverage reason=assignment value is not statically known: command substitution expression=root_id="$(LC_ALL=C "$P0_STAT" -L -c '%d:%i' -- / 2>&1)"
UNRESOLVED line=1394 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1394 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1394 kind=coverage reason=opaque command  may forward a path or endpoint expression=/
UNRESOLVED line=1412 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${root_id%%:*} expression=root_dev="${root_id%%:*}"
UNRESOLVED line=1413 kind=coverage reason=assignment value is not statically known: unpinned variable P0_DEVICE expression=dev_user="$P0_DEVICE"
UNRESOLVED line=1414 kind=coverage reason=assignment value is not statically known: unpinned variable P0_DEVICE expression=dev_mnt="$P0_DEVICE"
UNRESOLVED line=1415 kind=coverage reason=assignment value is not statically known: unpinned variable P0_DEVICE expression=dev_pid="$P0_DEVICE"
UNRESOLVED line=1416 kind=coverage reason=assignment value is not statically known: unpinned variable P0_DEVICE expression=dev_net="$P0_DEVICE"
UNRESOLVED line=1472 kind=coverage reason=assignment value is not statically known: unpinned variable SECONDS expression=started="$SECONDS"
UNRESOLVED line=1473 kind=coverage reason=assignment value is not statically known: command substitution expression=raw="$(LC_ALL=C "$P0_ENV" -i LC_ALL=C "$P0_TIMEOUT" \
        --signal=TERM --kill-after="${P0_MANAGER_QUERY_KILL_AFTER_S}s" \
        "${P0_MANAGER_QUERY_BUDGET_S}s" \
        "$P0_SYSTEMCTL" --system --no-pager show --property=Version 2>&
UNRESOLVED line=1473 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1476 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1477 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=elapsed=$(( SECONDS - started ))
UNRESOLVED line=1505 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw#Version=} expression=value="${raw#Version=}"
UNRESOLVED line=1548 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=p="$1"
UNRESOLVED line=1548 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=raw="$2"
UNRESOLVED line=1559 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=p="$1"
UNRESOLVED line=1561 kind=coverage reason=assignment value is not statically known: command substitution expression=raw="$(LC_ALL=C "$P0_STAT" -c '%F' -- "$p" 2>&1)"
UNRESOLVED line=1561 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1561 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1561 kind=coverage reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=1586 kind=coverage reason=assignment value is not statically known: command substitution expression=sub="$(LC_ALL=C "$P0_STAT" -L -c '%F' -- "$p" 2>&1)"
UNRESOLVED line=1586 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=subrc=$?
UNRESOLVED line=1586 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1586 kind=coverage reason=opaque command argument: unpinned variable p expression="$p"
UNRESOLVED line=1644 kind=coverage reason=assignment value is not statically known: unpinned variable P0_COUNT expression=n_eacces="$P0_COUNT"
UNRESOLVED line=1645 kind=coverage reason=assignment value is not statically known: unpinned variable P0_COUNT expression=n_enoent="$P0_COUNT"
UNRESOLVED line=1646 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=classes=$(( n_eacces + n_enoent ))
UNRESOLVED line=1664 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=d="$1"
UNRESOLVED line=1673 kind=coverage reason=assignment value is not statically known: command substitution expression=canon="$(LC_ALL=C "$P0_READLINK" -v -f -- "$d" 2>&1)"
UNRESOLVED line=1673 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1673 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1673 kind=coverage reason=opaque command argument: unpinned variable d expression="$d"
UNRESOLVED line=1710 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=py="$1"
UNRESOLVED line=1731 kind=unresolved_path reason=dynamic shell parameter $1 expression="$py"
UNRESOLVED line=1766 kind=coverage reason=assignment value is not statically known: command substitution expression=raw="$(LC_ALL=C "$P0_ENV" -i LC_ALL=C "$py" -I -S -c 'import sys
if not (sys.flags.isolated and sys.flags.no_site):
    sys.stdout.write("P0PY_STARTUP_UNPROVEN isolated=%d no_site=%d" % (sys.flags.isolated, sys.flags.no_site))
    raise Sys
UNRESOLVED line=1766 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=1766 kind=coverage reason=opaque command argument: unpinned variable py expression="$py"
UNRESOLVED line=1770 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1794 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw#P0PY } expression=version="${raw#P0PY }"
UNRESOLVED line=1799 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${version#*.} expression=minor="$rest"
UNRESOLVED line=1799 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${version#*.} expression=rest="${version#*.}"
UNRESOLVED line=1799 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${version%%.*} expression=major="${version%%.*}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== RP7-WPI-RO with real.constants ===
PATHSCOPE shell=<QA>\RP7-WPI-RO.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=7 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=34 unresolved_endpoint_count=0 coverage_issue_count=337 provenance_issue_count=0 parse_issue_count=0
PATH value=/ verdict=FORBID rule=- sources=NONE uses=line=542:assignment prefix,line=679:assignment prefix,line=681:assignment prefix
PATH value=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py verdict=ALLOW-LEXICAL rule=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=WPI_RELEASE_ROOT uses=line=1150:local assignment
PATH value=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE/requirements.lock verdict=ALLOW-LEXICAL rule=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=WPI_RELEASE_ROOT uses=line=1151:local assignment
PATH value=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python verdict=ALLOW-LEXICAL rule=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=WPI_VENV_ROOT uses=line=980:local assignment,line=999:test
PATH value=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/lib/python3.12/site-packages verdict=ALLOW-LEXICAL rule=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=WPI_VENV_ROOT uses=line=1034:local assignment,line=1152:local assignment
PATH value=/proc/self/mountinfo verdict=FORBID rule=- sources=NONE uses=line=633:redirection <
PATH value=/proc/uptime verdict=FORBID rule=- sources=NONE uses=line=232:redirection <
UNRESOLVED line=118 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=127 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=132 kind=coverage reason=opaque command wpi_on_err has no registered argv grammar expression=wpi_on_err
UNRESOLVED line=135 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${1-} expression=s="${1-}"
UNRESOLVED line=136 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s//$'\r'/ } expression=s="${s//$'\r'/ }"
UNRESOLVED line=137 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s//$'\n'/ } expression=s="${s//$'\n'/ }"
UNRESOLVED line=139 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s:0:300} expression=WPI_SAFE="${s:0:300}"
UNRESOLVED line=143 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=name="$1"
UNRESOLVED line=143 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${2-} expression=value="${2-}"
UNRESOLVED line=148 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=name="$1"
UNRESOLVED line=148 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=minimum="$3"
UNRESOLVED line=148 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${2-} expression=value="${2-}"
UNRESOLVED line=155 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=name="$1"
UNRESOLVED line=155 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${2-} expression=value="${2-}"
UNRESOLVED line=162 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=name="$1"
UNRESOLVED line=162 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${2-} expression=value="${2-}"
UNRESOLVED line=171 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=name="$1"
UNRESOLVED line=171 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=observed="$2"
UNRESOLVED line=171 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=expected="$3"
UNRESOLVED line=176 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=176 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=path="$2"
UNRESOLVED line=176 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=source="$3"
UNRESOLVED line=186 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=value="$1"
UNRESOLVED line=187 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
UNRESOLVED line=188 kind=coverage reason=assignment value is not statically known: unpinned variable EV_DIR expression=leaf="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").suppressed_value.bin"
UNRESOLVED line=189 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LEAF_FD expression=fd="$WPI_LEAF_FD"
UNRESOLVED line=190 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$fd"
UNRESOLVED line=196 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=path="$1"
UNRESOLVED line=200 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=WPI_PATH_FIELD="path=[unrenderable] path_sha256=$WPI_LINE"
UNRESOLVED line=204 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=WPI_PATH_FIELD="path=$path"
UNRESOLVED line=211 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=211 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=path="$2"
UNRESOLVED line=211 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=source="$3"
UNRESOLVED line=219 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=map="$1"
UNRESOLVED line=219 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=wanted="$2"
UNRESOLVED line=223 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${entry#*=} expression=found="${entry#*=}"
UNRESOLVED line=227 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${entry#*=} expression=WPI_LINE="$found"
UNRESOLVED line=234 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${BASH_REMATCH[1]} expression=whole="${BASH_REMATCH[1]}"
UNRESOLVED line=234 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${BASH_REMATCH[2]} expression=frac="${BASH_REMATCH[2]}"
UNRESOLVED line=235 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${BASH_REMATCH[2]} expression=frac="${frac}000"
UNRESOLVED line=235 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${frac:0:3} expression=frac="${frac:0:3}"
UNRESOLVED line=236 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=WPI_LINE=$(( 10#$whole * 1000 + 10#$frac ))
UNRESOLVED line=240 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=leaf="$1"
UNRESOLVED line=246 kind=unresolved_path reason=dynamic shell parameter $1 expression="$leaf"
UNRESOLVED line=263 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=leaf="$1"
UNRESOLVED line=268 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=268 kind=unresolved_path reason=dynamic shell parameter $1 expression="$leaf"
UNRESOLVED line=274 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=label="$1"
UNRESOLVED line=275 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
UNRESOLVED line=276 kind=coverage reason=assignment value is not statically known: unpinned variable EV_DIR expression=WPI_READ_DIAG="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.read.stderr"
UNRESOLVED line=277 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LEAF_FD expression=WPI_READ_DIAG_FD="$WPI_LEAF_FD"
UNRESOLVED line=297 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=WPI_CAP_BIND_PREFIX="$1"
UNRESOLVED line=297 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=WPI_CAP_BIND_REASON="$2"
UNRESOLVED line=301 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=label="$1"
UNRESOLVED line=303 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_BIND_PREFIX expression=bind_prefix="$WPI_CAP_BIND_PREFIX"
UNRESOLVED line=303 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_BIND_REASON expression=bind_reason="$WPI_CAP_BIND_REASON"
UNRESOLVED line=307 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
UNRESOLVED line=308 kind=coverage reason=assignment value is not statically known: unpinned variable EV_DIR expression=WPI_CAP_OUT="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stdout"
UNRESOLVED line=309 kind=coverage reason=assignment value is not statically known: unpinned variable EV_DIR expression=WPI_CAP_ERR="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").$label.stderr"
UNRESOLVED line=310 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LEAF_FD expression=ofd="$WPI_LEAF_FD"
UNRESOLVED line=311 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LEAF_FD expression=efd="$WPI_LEAF_FD"
UNRESOLVED line=312 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=start="$WPI_LINE"
UNRESOLVED line=314 kind=unresolved_path reason=cd argument is not statically known: unpinned variable EV_DIR expression="$EV_DIR"
UNRESOLVED line=315 kind=coverage reason=exec argument is not statically known: unpinned variable WPI_ENV expression="$WPI_ENV"
UNRESOLVED line=317 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=317 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$efd"
UNRESOLVED line=317 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$ofd"
UNRESOLVED line=334 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=brc=$?
UNRESOLVED line=334 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression=/dev/fd/"$ofd"
UNRESOLVED line=335 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=erc=$?
UNRESOLVED line=335 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression=/dev/fd/"$efd"
UNRESOLVED line=342 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=end="$WPI_LINE"
UNRESOLVED line=343 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=WPI_CAP_RC="$rc"
UNRESOLVED line=344 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=WPI_CAP_ELAPSED_MS=$(( end - start ))
UNRESOLVED line=349 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=349 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=reason="$2"
UNRESOLVED line=349 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=file="$3"
UNRESOLVED line=350 kind=unresolved_path reason=dynamic shell parameter $3 expression="$file"
UNRESOLVED line=351 kind=unresolved_path reason=dynamic shell parameter $3 expression="$file"
UNRESOLVED line=394 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=394 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=reason="$2"
UNRESOLVED line=394 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=source="$3"
UNRESOLVED line=394 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $4 expression=fd="$4"
UNRESOLVED line=394 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $5 expression=diag="$5"
UNRESOLVED line=394 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $6 expression=dfd="$6"
UNRESOLVED line=396 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=396 kind=coverage reason=read option value is not statically known: dynamic shell parameter $4 expression="$fd"
UNRESOLVED line=396 kind=unresolved_path reason=dynamic shell parameter $6 expression="$dfd"
UNRESOLVED line=402 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${whole#*$'\n'} expression=extra="${whole#*$'\n'}"
UNRESOLVED line=402 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${whole%%$'\n'*} expression=first="${whole%%$'\n'*}"
UNRESOLVED line=413 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${whole%%$'\n'*} expression=WPI_LINE="$first"
UNRESOLVED line=417 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=417 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=reason="$2"
UNRESOLVED line=417 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=file="$3"
UNRESOLVED line=419 kind=unresolved_path reason=dynamic shell parameter $3 expression="$file"
UNRESOLVED line=429 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=429 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=reason="$2"
UNRESOLVED line=429 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=stream="$3"
UNRESOLVED line=431 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_OUT expression=WPI_CAP_FD_SOURCE="$WPI_CAP_OUT"
UNRESOLVED line=431 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_OUT_FD expression=WPI_CAP_FD="$WPI_CAP_OUT_FD"
UNRESOLVED line=432 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_ERR expression=WPI_CAP_FD_SOURCE="$WPI_CAP_ERR"
UNRESOLVED line=432 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_ERR_FD expression=WPI_CAP_FD="$WPI_CAP_ERR_FD"
UNRESOLVED line=446 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=446 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=reason="$2"
UNRESOLVED line=446 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=stream="$3"
UNRESOLVED line=447 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_FD expression=fd="$WPI_CAP_FD"
UNRESOLVED line=447 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_FD_SOURCE expression=source="$WPI_CAP_FD_SOURCE"
UNRESOLVED line=458 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=458 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=reason="$2"
UNRESOLVED line=458 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=stream="$3"
UNRESOLVED line=459 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_FD expression=fd="$WPI_CAP_FD"
UNRESOLVED line=459 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_FD_SOURCE expression=source="$WPI_CAP_FD_SOURCE"
UNRESOLVED line=460 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG expression=diag="$WPI_READ_DIAG"
UNRESOLVED line=460 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG_FD expression=dfd="$WPI_READ_DIAG_FD"
UNRESOLVED line=461 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=461 kind=coverage reason=read option value is not statically known: unpinned variable WPI_CAP_FD expression="$fd"
UNRESOLVED line=461 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=474 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=474 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=path="$2"
UNRESOLVED line=474 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${3:-path_not_evaluable} expression=unreadable="${3:-path_not_evaluable}"
UNRESOLVED line=475 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_PATH_FIELD expression=path_field="$WPI_PATH_FIELD"
UNRESOLVED line=492 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=raw="$WPI_LINE"
UNRESOLVED line=494 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw#*|} expression=rest="${raw#*|}"
UNRESOLVED line=494 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${raw%%|*} expression=WPI_META_KIND="${raw%%|*}"
UNRESOLVED line=495 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*|} expression=rest="${rest#*|}"
UNRESOLVED line=495 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%|*} expression=WPI_META_MODE="${rest%%|*}"
UNRESOLVED line=496 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*|} expression=rest="${rest#*|}"
UNRESOLVED line=496 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%|*} expression=WPI_META_OWNER="${rest%%|*}"
UNRESOLVED line=497 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*|} expression=WPI_META_SIZE="${rest#*|}"
UNRESOLVED line=497 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%|*} expression=WPI_META_ID="${rest%%|*}"
UNRESOLVED line=515 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=outcome="$1"
UNRESOLVED line=515 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=prefix="$2"
UNRESOLVED line=515 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=message="$3"
UNRESOLVED line=528 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=528 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=path="$2"
UNRESOLVED line=528 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=leaf_kind="$3"
UNRESOLVED line=528 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $4 expression=leaf_mode="$4"
UNRESOLVED line=528 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $5 expression=leaf_owner="$5"
UNRESOLVED line=529 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${6:-path_absent} expression=leaf_absent_reason="${6:-path_absent}"
UNRESOLVED line=529 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${7:-path_metadata_mismatch} expression=leaf_object_reason="${7:-path_metadata_mismatch}"
UNRESOLVED line=530 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${8:-fail} expression=outcome="${8:-fail}"
UNRESOLVED line=530 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${9:-path_binding_not_evaluable} expression=stop_context="${9:-path_binding_not_evaluable}"
UNRESOLVED line=531 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${10:-path_not_evaluable} expression=unreadable="${10:-path_not_evaluable}"
UNRESOLVED line=531 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${11:-} expression=leaf_owner_reason="${11:-}"
UNRESOLVED line=531 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${12:-with_path} expression=leaf_field_style="${12:-with_path}"
UNRESOLVED line=534 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_PATH_FIELD expression=walk_path_field="$WPI_PATH_FIELD"
UNRESOLVED line=541 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${path#/} expression=rest="${path#/}"
UNRESOLVED line=547 kind=coverage reason=assignment value is not statically known: loop variable component is dynamic expression=current="$current/$component"
UNRESOLVED line=550 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=expected_kind="$leaf_kind"
UNRESOLVED line=550 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $5 expression=expected_owner="$leaf_owner"
UNRESOLVED line=551 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${leaf_mode#0} expression=expected_mode="${leaf_mode#0}"
UNRESOLVED line=554 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_PATH_FIELD expression=leaf_fields=" $WPI_PATH_FIELD"
UNRESOLVED line=561 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=kind_token="$WPI_LINE"
UNRESOLVED line=576 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${9:-path_binding_not_evaluable} expression=deviation_reason="$stop_context detail=path_metadata_mismatch"
UNRESOLVED line=582 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${9:-path_binding_not_evaluable} expression=deviation_reason="$stop_context detail=path_metadata_mismatch"
UNRESOLVED line=591 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=file="$1"
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_DEVICE=(...)
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_FSTYPE=(...)
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_POINT=(...)
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_ROOT=(...)
UNRESOLVED line=593 kind=coverage reason=array assignment is outside the accepted scalar subset expression=WPI_MI_SOURCE=(...)
UNRESOLVED line=594 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG expression=diag="$WPI_READ_DIAG"
UNRESOLVED line=594 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG_FD expression=dfd="$WPI_READ_DIAG_FD"
UNRESOLVED line=595 kind=unresolved_path reason=dynamic shell parameter $1 expression="$file"
UNRESOLVED line=597 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=597 kind=coverage reason=read option value is not statically known: declared variable fd has no static value expression="$fd"
UNRESOLVED line=597 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=605 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${line#* - } expression=post="${line#* - }"
UNRESOLVED line=605 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${line%% - *} expression=pre="${line%% - *}"
UNRESOLVED line=611 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=seen_ids="$seen_ids$1 "
UNRESOLVED line=614 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=device="$3"
UNRESOLVED line=614 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $4 expression=root="$4"
UNRESOLVED line=614 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $5 expression=mount_point="$5"
UNRESOLVED line=617 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=fstype="$1"
UNRESOLVED line=617 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=source="$2"
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
UNRESOLVED line=621 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=records=$(( records + 1 ))
UNRESOLVED line=629 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=WPI_MOUNT_SNAPSHOT_SEQ=$(( WPI_MOUNT_SNAPSHOT_SEQ + 1 ))
UNRESOLVED line=630 kind=coverage reason=assignment value is not statically known: unpinned variable EV_DIR expression=snapshot="$EV_DIR/ro.mountinfo.$(printf '%04d' "$WPI_MOUNT_SNAPSHOT_SEQ").snapshot"
UNRESOLVED line=631 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LEAF_FD expression=outfd="$WPI_LEAF_FD"
UNRESOLVED line=632 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG expression=diag="$WPI_READ_DIAG"
UNRESOLVED line=632 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG_FD expression=dfd="$WPI_READ_DIAG_FD"
UNRESOLVED line=635 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=635 kind=coverage reason=read option value is not statically known: declared variable infd has no static value expression="$infd"
UNRESOLVED line=635 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=642 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$outfd"
UNRESOLVED line=644 kind=coverage reason=assignment value is not statically known: unpinned variable EV_DIR expression=WPI_LINE="$snapshot"
UNRESOLVED line=660 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=snapshot="$1"
UNRESOLVED line=662 kind=coverage reason=array assignment is outside the accepted scalar subset expression=points=(...)
UNRESOLVED line=671 kind=coverage reason=array assignment is outside the accepted scalar subset expression=root_candidates=(...)
UNRESOLVED line=677 kind=coverage reason=array assignment is outside the accepted scalar subset expression=roots=(...)
UNRESOLVED line=681 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ and this tool does not model which consumer splits it expression=seen_roots="$seen_roots$r "
UNRESOLVED line=682 kind=coverage reason=compound assignment is outside the accepted scalar subset expression=roots+=
UNRESOLVED line=682 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=685 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=WPI_PROBE_SEQ=$(( WPI_PROBE_SEQ + 1 ))
UNRESOLVED line=686 kind=coverage reason=assignment value is not statically known: unpinned variable EV_DIR expression=projection="$EV_DIR/ro.$(printf '%04d' "$WPI_PROBE_SEQ").mount_projection.tsv"
UNRESOLVED line=687 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LEAF_FD expression=pfd="$WPI_LEAF_FD"
UNRESOLVED line=691 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${WPI_MI_POINT[$i]} expression=mp="${WPI_MI_POINT[$i]}"
UNRESOLVED line=693 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${#mp} expression=len=${#mp}
UNRESOLVED line=696 kind=coverage reason=assignment value is not statically known: declared variable i has no static value expression=best="$i"
UNRESOLVED line=696 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${#mp} expression=best_len="$len"
UNRESOLVED line=703 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=shared=$(( shared + 1 ))
UNRESOLVED line=708 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=712 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${r%/} expression=rprefix="${r%/}/"
UNRESOLVED line=714 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${WPI_MI_POINT[$i]} expression=mp="${WPI_MI_POINT[$i]}"
UNRESOLVED line=716 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=subtree_records=$(( subtree_records + 1 ))
UNRESOLVED line=720 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=723 kind=unresolved_path reason=unpinned variable WPI_LEAF_FD expression="$pfd"
UNRESOLVED line=727 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=WPI_MOUNT_PROJECTION_DIGEST="$WPI_LINE"
UNRESOLVED line=733 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=733 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=reason="$2"
UNRESOLVED line=733 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=path="$3"
UNRESOLVED line=734 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=path_field="path=$path"
UNRESOLVED line=739 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=rendered="$WPI_LINE"
UNRESOLVED line=739 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rendered%% *} expression=digest="${rendered%% *}"
UNRESOLVED line=742 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rendered%% *} expression=WPI_LINE="$digest"
UNRESOLVED line=748 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=snapshot="$WPI_LINE"
UNRESOLVED line=750 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=751 kind=coverage reason=opaque command argument: unpinned variable WPI_MOUNT_PROJECTION_DIGEST expression="mount_topology_mismatch observed=$WPI_MOUNT_PROJECTION_DIGEST attested=$WPI_ATTESTED_MOUNTINFO_SHA256 format=normalised_path_projection_v2"
UNRESOLVED line=752 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_MOUNT_PROJECTION_DIGEST expression=WPI_MOUNT_BEFORE="$WPI_MOUNT_PROJECTION_DIGEST"
UNRESOLVED line=757 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_MOUNT_BEFORE expression=before="$WPI_MOUNT_BEFORE"
UNRESOLVED line=759 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=snapshot="$WPI_LINE"
UNRESOLVED line=762 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=763 kind=coverage reason=opaque command argument: unpinned variable WPI_MOUNT_BEFORE expression="mount_topology_changed before=$before after=$WPI_MOUNT_PROJECTION_DIGEST format=normalised_path_projection_v2"
UNRESOLVED line=767 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=name="$1"
UNRESOLVED line=767 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=path="$2"
UNRESOLVED line=769 kind=unresolved_path reason=dynamic shell parameter $2 expression="$path"
UNRESOLVED line=813 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${entry#*=} expression=pin_path="${entry#*=}"
UNRESOLVED line=813 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${entry%%=*} expression=pin_name="${entry%%=*}"
UNRESOLVED line=828 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=pin_count=$(( pin_count + 1 ))
UNRESOLVED line=828 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${entry%%=*} expression=pin_seen="$pin_seen$pin_name "
UNRESOLVED line=832 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=path="$WPI_LINE"
UNRESOLVED line=853 kind=coverage reason=opaque command argument: unpinned variable RUNID expression="$RUNID"
UNRESOLVED line=853 kind=coverage reason=opaque command rp0_require_safe_component has no registered argv grammar expression=rp0_require_safe_component
UNRESOLVED line=854 kind=coverage reason=opaque command argument: unpinned variable EV_STAGE_ID expression="$EV_STAGE_ID"
UNRESOLVED line=854 kind=coverage reason=opaque command rp0_require_safe_component has no registered argv grammar expression=rp0_require_safe_component
UNRESOLVED line=860 kind=coverage reason=opaque command  has no registered argv grammar expression=
UNRESOLVED line=885 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=rawpath="$WPI_LINE"
UNRESOLVED line=889 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=fdid="$WPI_LINE"
UNRESOLVED line=893 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=logid="$WPI_LINE"
UNRESOLVED line=903 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=903 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=label="$2"
UNRESOLVED line=903 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=root="$3"
UNRESOLVED line=907 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=elapsed_s=$(( WPI_CAP_ELAPSED_MS / 1000 ))
UNRESOLVED line=918 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=root="$1"
UNRESOLVED line=918 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=label="$2"
UNRESOLVED line=923 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=find_elapsed_s=$(( find_elapsed / 1000 ))
UNRESOLVED line=923 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_ELAPSED_MS expression=find_elapsed="$WPI_CAP_ELAPSED_MS"
UNRESOLVED line=923 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_OUT expression=out="$WPI_CAP_OUT"
UNRESOLVED line=924 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=925 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=926 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG expression=diag="$WPI_READ_DIAG"
UNRESOLVED line=926 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG_FD expression=dfd="$WPI_READ_DIAG_FD"
UNRESOLVED line=927 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=929 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=929 kind=coverage reason=read option value is not statically known: declared variable fd has no static value expression="$fd"
UNRESOLVED line=929 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=937 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=writable_count=$(( writable_count + 1 ))
UNRESOLVED line=939 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_PATH_FIELD expression=WPI_FIRST_WRITABLE_FIELD="$WPI_PATH_FIELD"
UNRESOLVED line=952 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=path="$1"
UNRESOLVED line=952 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=owner="$2"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=prefix="$1"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=absent_reason="$2"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=mismatch_reason="$3"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $4 expression=path="$4"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $5 expression=bytes="$5"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $6 expression=digest="$6"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $7 expression=label="$7"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${8:-path_metadata_mismatch} expression=object_reason="${8:-path_metadata_mismatch}"
UNRESOLVED line=966 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${9:-with_path} expression=field_style="${9:-with_path}"
UNRESOLVED line=970 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_META_SIZE expression=observed_size="$WPI_META_SIZE"
UNRESOLVED line=972 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=WPI_OBSERVED_DIGEST="$WPI_LINE"
UNRESOLVED line=990 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=resolved="$WPI_LINE"
UNRESOLVED line=1010 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1011 kind=unresolved_path reason=unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1012 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_OUT expression=version_file="$WPI_CAP_OUT"
UNRESOLVED line=1012 kind=unresolved_path reason=unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1012 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1013 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_ERR expression=version_file="$WPI_CAP_ERR"
UNRESOLVED line=1013 kind=unresolved_path reason=unpinned variable WPI_CAP_ERR expression="$WPI_CAP_ERR"
UNRESOLVED line=1013 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$WPI_CAP_OUT"
UNRESOLVED line=1041 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_OUT expression=out="$WPI_CAP_OUT"
UNRESOLVED line=1042 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG expression=diag="$WPI_READ_DIAG"
UNRESOLVED line=1042 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG_FD expression=dfd="$WPI_READ_DIAG_FD"
UNRESOLVED line=1043 kind=unresolved_path reason=unpinned variable WPI_CAP_OUT expression="$out"
UNRESOLVED line=1045 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1045 kind=coverage reason=read option value is not statically known: declared variable fd has no static value expression="$fd"
UNRESOLVED line=1045 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=1052 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=entries=$(( entries + 1 ))
UNRESOLVED line=1054 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${path##*/} expression=base="${path##*/}"
UNRESOLVED line=1065 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=ignored=$(( ignored + 1 ))
UNRESOLVED line=1074 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=count=$(( count + 1 ))
UNRESOLVED line=1085 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=WPI_MEMBER_DIGEST="$WPI_LINE"
UNRESOLVED line=1099 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=value="$1"
UNRESOLVED line=1105 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=line="$1"
UNRESOLVED line=1106 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${line#verify_lock: FAIL: } expression=detail="${line#verify_lock: FAIL: }"
UNRESOLVED line=1109 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${detail#missing-or-wrong=} expression=missing="${detail#missing-or-wrong=}"
UNRESOLVED line=1109 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${missing%%; unexpected=*} expression=missing="${missing%%; unexpected=*}"
UNRESOLVED line=1110 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${detail#*; unexpected=} expression=extras="${detail#*; unexpected=}"
UNRESOLVED line=1113 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${detail#missing-or-wrong=} expression=missing="${detail#missing-or-wrong=}"
UNRESOLVED line=1116 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${detail#unexpected=} expression=extras="${detail#unexpected=}"
UNRESOLVED line=1221 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=err="$WPI_LINE"
UNRESOLVED line=1227 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${err#verify_lock_driver: universe_unexpected } expression=fields="${err#verify_lock_driver: universe_unexpected }"
UNRESOLVED line=1228 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${fields#* } expression=udigest="${fields#* }"
UNRESOLVED line=1228 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${fields%% *} expression=ufmt="${fields%% *}"
UNRESOLVED line=1240 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${err#verify_lock_driver: distribution_identity_unestablished } expression=fields="${err#verify_lock_driver: distribution_identity_unestablished }"
UNRESOLVED line=1241 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${fields#* } expression=udigest="${fields#* }"
UNRESOLVED line=1241 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${fields%% *} expression=ufmt="${fields%% *}"
UNRESOLVED line=1264 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_MAINPID expression=service_path="/proc/$WPI_MAINPID/ns/net"
UNRESOLVED line=1269 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=caller="$WPI_LINE"
UNRESOLVED line=1274 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=service="$WPI_LINE"
UNRESOLVED line=1293 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=rest="$1"
UNRESOLVED line=1296 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*.} expression=o="$rest"
UNRESOLVED line=1296 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*.} expression=rest="${rest#*.}"
UNRESOLVED line=1296 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%.*} expression=o="${rest%%.*}"
UNRESOLVED line=1297 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=n=$(( n + 1 ))
UNRESOLVED line=1310 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=rest="$1"
UNRESOLVED line=1314 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*:} expression=piece="$rest"
UNRESOLVED line=1314 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*:} expression=rest="${rest#*:}"
UNRESOLVED line=1314 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%:*} expression=piece="${rest%%:*}"
UNRESOLVED line=1317 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=n=$(( n + 2 ))
UNRESOLVED line=1320 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=n=$(( n + 1 ))
UNRESOLVED line=1325 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=WPI_LINE="$n"
UNRESOLVED line=1331 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=s="$1"
UNRESOLVED line=1333 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s##*%} expression=zone="${s##*%}"
UNRESOLVED line=1333 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s%%%*} expression=s="${s%%%*}"
UNRESOLVED line=1342 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s#*::} expression=tail="${s#*::}"
UNRESOLVED line=1342 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${s%%::*} expression=head="${s%%::*}"
UNRESOLVED line=1343 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=hn="$WPI_LINE"
UNRESOLVED line=1361 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=token="$1"
UNRESOLVED line=1361 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=role="$2"
UNRESOLVED line=1363 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${token##*:} expression=port="${token##*:}"
UNRESOLVED line=1363 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${token%:*} expression=addr="${token%:*}"
UNRESOLVED line=1375 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${addr#[} expression=inner="${addr#[}"
UNRESOLVED line=1375 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${inner%]} expression=inner="${inner%]}"
UNRESOLVED line=1380 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${token##*:} expression=WPI_EP_PORT="$port"
UNRESOLVED line=1380 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${token%:*} expression=WPI_EP_ADDR="$addr"
UNRESOLVED line=1391 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG expression=diag="$WPI_READ_DIAG"
UNRESOLVED line=1391 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_READ_DIAG_FD expression=dfd="$WPI_READ_DIAG_FD"
UNRESOLVED line=1424 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_CAP_OUT_FD expression=fd="$WPI_CAP_OUT_FD"
UNRESOLVED line=1426 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $? expression=rc=$?
UNRESOLVED line=1426 kind=coverage reason=read option value is not statically known: unpinned variable WPI_CAP_OUT_FD expression="$fd"
UNRESOLVED line=1426 kind=unresolved_path reason=unpinned variable WPI_READ_DIAG_FD expression="$dfd"
UNRESOLVED line=1434 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest#*$'\n'} expression=rest="${rest#*$'\n'}"
UNRESOLVED line=1434 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${rest%%$'\n'*} expression=line="${rest%%$'\n'*}"
UNRESOLVED line=1437 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=consumed=$(( consumed + ${#line} + 1 ))
UNRESOLVED line=1442 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=state="$1"
UNRESOLVED line=1442 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $2 expression=recvq="$2"
UNRESOLVED line=1442 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $3 expression=sendq="$3"
UNRESOLVED line=1442 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $4 expression=localaddr="$4"
UNRESOLVED line=1442 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $5 expression=peer="$5"
UNRESOLVED line=1453 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_EP_ADDR expression=addr="$WPI_EP_ADDR"
UNRESOLVED line=1453 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_EP_PORT expression=port="$WPI_EP_PORT"
UNRESOLVED line=1455 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=total=$(( total + 1 ))
UNRESOLVED line=1457 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=port_rows=$(( port_rows + 1 ))
UNRESOLVED line=1462 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_EP_ADDR expression=wildcard_addr="$addr"
UNRESOLVED line=1466 kind=coverage reason=assignment value is not statically known: arithmetic expansion expression=count=$(( count + 1 ))
UNRESOLVED line=1485 kind=coverage reason=assignment value is not statically known: dynamic shell parameter $1 expression=field="$1"
UNRESOLVED line=1487 kind=coverage reason=assignment value is not statically known: unsupported parameter expansion ${entry#*:} expression=WPI_LINE="${entry#*:}"
UNRESOLVED line=1493 kind=coverage reason=assignment value is not statically known: unpinned variable EV_DIR expression=body="$EV_DIR/ro.status.body"
UNRESOLVED line=1514 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=WPI_BODY_SHA="$WPI_LINE"
UNRESOLVED line=1553 kind=coverage reason=assignment value is not statically known: unpinned variable WPI_LINE expression=record="$WPI_LINE"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
```

## Complete pre-repair transcript for family P10 (round-3 bytes, `0724967E…25F7`)

This is `RED_R3.txt` in full: the eighteen C-2 fixtures run by the same harness against
the committed round-3 blob `e600a107f2e2a790653cc544a94cd7436b7b070a`. It is the RED side
of the D026 pairs in §"Round 4". Seventeen of the eighteen sections end `COMMAND_RC=0`;
twelve of those are the silent sinks (the out-of-allowlist lexeme is absent from the
report), and five are the controls, which are expected to end `COMMAND_RC=0` in both
columns. The eighteenth, `c2_quoted_space`, already ended `COMMAND_RC=1` here and must keep
doing so after the repair.

```text
=== c2_list_prefix ===
PATHSCOPE shell=<QA>\c2_list_prefix.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_list_env ===
PATHSCOPE shell=<QA>\c2_list_env.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:env assignment
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_list_export ===
PATHSCOPE shell=<QA>\c2_list_export.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:export assignment
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_list_bare_first ===
PATHSCOPE shell=<QA>\c2_list_bare_first.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_list_space ===
PATHSCOPE shell=<QA>\c2_list_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_relative ===
PATHSCOPE shell=<QA>\c2_relative.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_empty_member ===
PATHSCOPE shell=<QA>\c2_empty_member.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_quoted_space ===
PATHSCOPE shell=<QA>\c2_quoted_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe dir/escape verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_escaped_space ===
PATHSCOPE shell=<QA>\c2_escaped_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/a b:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_command_text ===
PATHSCOPE shell=<QA>\c2_command_text.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_uri_forbid ===
PATHSCOPE shell=<QA>\c2_uri_forbid.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_uri_allow ===
PATHSCOPE shell=<QA>\c2_uri_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_env_quoted ===
PATHSCOPE shell=<QA>\c2_env_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_bare_soname ===
PATHSCOPE shell=<QA>\c2_bare_soname.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_allow_list ===
PATHSCOPE shell=<QA>\c2_allow_list.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib:/safe/lib64 verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_benign_scalars ===
PATHSCOPE shell=<QA>\c2_benign_scalars.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_benign_words ===
PATHSCOPE shell=<QA>\c2_benign_words.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_words_with_path ===
PATHSCOPE shell=<QA>\c2_words_with_path.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
```

## Determinism

The last **five** lines of the harness stdout above run each of `find_exec`,
`assign_prefix`, `c2_list_prefix`, `RP6-P0` and `RP7-WPI-RO` twice in memory and compare the
complete stdout byte for byte plus the rc. All five report `equal=True` with identical
digests, so ordering and output are stable. (Round 2 had three such pairs, round 3 four;
round 4 adds the `c2_list_prefix` pair so the C-2 member grammar is covered too. The Codex
round-3 re-audit flagged the stale "last three lines" wording as an optional nit — this
sentence closes it.) Determinism is not soundness; it is only the property that the recorded
transcripts can be re-derived.

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

Rounds 3 and 4 on the same bytes, with `real.constants` (measured this round):

```text
RP6-P0.sh  round 3: resolved_fs_path_count=7 resolved_net_endpoint_count=0
                    unresolved_path_count=3 unresolved_endpoint_count=0
                    coverage_issue_count=200 provenance_issue_count=0 parse_issue_count=0  rc 3
RP6-P0.sh  round 4: byte-identical to round 3 (same counts, same rows, same digest)        rc 3

RP7-WPI-RO round 3: resolved_fs_path_count=7 resolved_net_endpoint_count=0
                    unresolved_path_count=34 unresolved_endpoint_count=0
                    coverage_issue_count=336 provenance_issue_count=0 parse_issue_count=0  rc 3
RP7-WPI-RO round 4: resolved_fs_path_count=7 resolved_net_endpoint_count=0
                    unresolved_path_count=34 unresolved_endpoint_count=0
                    coverage_issue_count=337 provenance_issue_count=0 parse_issue_count=0  rc 3
```

The round-2 to round-3 rise in `coverage_issue_count` is the C-1 assignment repair making
previously invisible constructs speak. The single round-3 to round-4 addition is named
above. No round has ever moved either block off rc 3.

The single round-1 number `unresolved_count` is gone. It was an `Issue` cardinality and was
being read as a path-set cardinality. Nothing about these counts converts either block into
a PASS, and they remain a lower-bound diagnostic until a fresh T1 audit accepts the tool.
