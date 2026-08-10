# Self-QA - Stage-1 path-scope prover

Date: 2026-08-10  
Audit tier: T1 (local-only static analysis)  
Working directory: `C:\LAB\Tradingview_LAB_CLEAN`

The runs below used CPython 3.14.2 with `-B`; the source also parses with
`ast.parse(..., feature_version=(3, 12))`. A Python 3.12 executable is not installed on
this workstation. No shell input was executed and no host was contacted.

## Exact fixture setup

This is the literal PowerShell setup used for all four required runs. The fifth fixture
is an additional completeness check: a forbidden read inside a quoted command
substitution must not disappear merely because its output is assigned and unused.

```powershell
$QA = Join-Path ([System.IO.Path]::GetTempPath()) 'pathscope-prover-self-qa'
New-Item -ItemType Directory -Path $QA -Force | Out-Null
[System.IO.File]::WriteAllText((Join-Path $QA 'constants.env'), "ROOT=/safe`n")
[System.IO.File]::WriteAllText((Join-Path $QA 'allowlist.txt'), "/safe/**`n")
[System.IO.File]::WriteAllText((Join-Path $QA 'green.sh'), ('#!/bin/bash','leaf="$ROOT/input"','cat "$leaf"','' -join "`n"))
[System.IO.File]::WriteAllText((Join-Path $QA 'literal.sh'), ('#!/bin/bash','cat /etc/passwd','' -join "`n"))
[System.IO.File]::WriteAllText((Join-Path $QA 'assembled.sh'), ('#!/bin/bash','p="/etc"','q="mtc-bridge"','cat "$p/$q/x"','' -join "`n"))
[System.IO.File]::WriteAllText((Join-Path $QA 'dynamic.sh'), ('#!/bin/bash','p="$(printf /safe)"','cat "$p/x"','' -join "`n"))
[System.IO.File]::WriteAllText((Join-Path $QA 'nested.sh'), ('#!/bin/bash','unused="$(cat /etc/shadow)"','' -join "`n"))
$TOOL = 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_PREREG_DRAFT_ROUND1\pathscope_prover.py'
```

## GREEN - preregistered scalar expansion only

Exact command:

```powershell
python -B $TOOL "$QA\green.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
```

Real output:

```text
PATHSCOPE shell=C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-prover-self-qa\green.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/safe/input verdict=ALLOW rule=/safe/** sources=ROOT uses=line=3:cat
PATHSCOPE verdict=PASS rc=0 reason=closed_and_allowlisted
COMMAND_RC=0
```

## RED A - forbidden literal path

Exact command:

```powershell
python -B $TOOL "$QA\literal.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
```

Real output:

```text
PATHSCOPE shell=C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-prover-self-qa\literal.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/passwd verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
```

## RED B - forbidden path assembled from harmless tokens

This is the required falsification of a literal-only scanner.

Exact command:

```powershell
python -B $TOOL "$QA\assembled.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
```

Real output:

```text
PATHSCOPE shell=C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-prover-self-qa\assembled.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/mtc-bridge/x verdict=FORBID rule=- sources=NONE uses=line=4:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
```

## RED C - command substitution into a path is a STOP

Exact command:

```powershell
python -B $TOOL "$QA\dynamic.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
```

Real output:

```text
PATHSCOPE shell=C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-prover-self-qa\dynamic.sh
PATHSCOPE resolved_count=0 unresolved_count=1
UNRESOLVED line=3 reason=command substitution expression="$p/x"
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
COMMAND_RC=3
```

## Additional completeness falsification - nested primitive

Exact command:

```powershell
python -B $TOOL "$QA\nested.sh" "$QA\constants.env" "$QA\allowlist.txt"
"COMMAND_RC=$LASTEXITCODE"
```

Real output:

```text
PATHSCOPE shell=C:\Users\BarışSemaay\AppData\Local\Temp\pathscope-prover-self-qa\nested.sh
PATHSCOPE resolved_count=1 unresolved_count=0
PATH value=/etc/shadow verdict=FORBID rule=- sources=NONE uses=line=2:cat
PATHSCOPE verdict=REJECT rc=1 reason=path_outside_allowlist
COMMAND_RC=1
```

## Real committed RP6/RP7 inputs with current preregistration values

The constants file used the values printed in draft §2, direct `P0_VENV_ROOT` and
`P0_STATE_UID/GID` aliases of those §2 values, and the current draft §1 value
`REMOTE_BASE=/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>`. The allowlist file was
the exact §10.1 set in machine form:

```text
<WPI_RELEASE_ROOT>/**
<WPI_VENV_ROOT>/**
<WPI_UNIT_FRAGMENT>
terminal:<WPI_CONF_DIR>
terminal:<WPI_STATE_DIR>
terminal:<WPI_LOG_DIR>
<REMOTE_BASE>/**
127.0.0.1:8790
```

Exact input-file setup (continuing from the declared `$QA` above):

```powershell
$realConstants = @(
'WPI_CANDIDATE_SHA=2ce41e34bceb599d80af24c5c33d835820ec321b',
'WPI_RELEASE_ROOT=/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b',
'WPI_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b',
'WPI_UNIT_FRAGMENT=/usr/local/lib/systemd/system/mtc-bridge-first-start.service',
'WPI_UNIT_FRAGMENT_BYTES=3736',
'WPI_UNIT_FRAGMENT_SHA256=<PIN-BEFORE-DISPATCH: GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md; matrix B2 records it elided as 538c1c60...279bd>',
'WPI_EXPECTED_LOCK_SHA256=a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e',
'WPI_EXPECTED_LOCK_BYTES=117762',
'WPI_EXPECTED_PACKAGES=56',
'WPI_STATE_DIR=/var/lib/mtc-bridge',
'WPI_STATE_UID=999',
'WPI_STATE_GID=988',
'WPI_LOG_DIR=/var/log/mtc-bridge',
'WPI_CONF_DIR=/etc/mtc-bridge',
'WPI_CONTROL_ENDPOINT=http://127.0.0.1:8790/api/status',
'WPI_SWEEP_BUDGET_S=120',
'P0_VENV_ROOT=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b',
'P0_STATE_UID=999',
'P0_STATE_GID=988',
'REMOTE_BASE=/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>'
) -join "`n"
$realAllowlist = @(
'<WPI_RELEASE_ROOT>/**',
'<WPI_VENV_ROOT>/**',
'<WPI_UNIT_FRAGMENT>',
'terminal:<WPI_CONF_DIR>',
'terminal:<WPI_STATE_DIR>',
'terminal:<WPI_LOG_DIR>',
'<REMOTE_BASE>/**',
'127.0.0.1:8790'
) -join "`n"
[System.IO.File]::WriteAllText((Join-Path $QA 'real.constants'), $realConstants + "`n")
[System.IO.File]::WriteAllText((Join-Path $QA 'real.allowlist'), $realAllowlist + "`n")
```

Exact commands:

```powershell
python -B $TOOL 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP6-P0.sh' "$QA\real.constants" "$QA\real.allowlist"
"COMMAND_RC=$LASTEXITCODE"
python -B $TOOL 'MTC_COMMAND_CENTER\11_TRIAGE\WPI_BLOCKS_DRAFT\RP7-WPI-RO.sh' "$QA\real.constants" "$QA\real.allowlist"
"COMMAND_RC=$LASTEXITCODE"
```

Real output for RP6:

```text
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
```

Real output for RP7:

```text
PATHSCOPE verdict=REJECT rc=3 reason=input_parse_error line=7 detail=path contains an unresolved angle-bracket placeholder
COMMAND_RC=3
```

This is the honest Stage-1 result: the current `<REMOTE_BASE>` value is still an
allocation placeholder, so §10.1 does not yet expand to a closed host-path set. The
prover STOPs before claiming a per-block proof. It was not relaxed to admit the draft.

For diagnostic depth only, a second run replaced only that placeholder with the clearly
non-authoritative static value `/home/gatea/wpi_staging_STAGE1_STATIC_BINDING`. This is
not acceptance evidence. A concurrent session modified the RP6 working-tree file during
this task, so final downstream diagnostics used a `git archive HEAD` extraction and
verified `git hash-object` against the committed blobs before analysis: RP6
`efb1d1be1647509f2de3dd6df0b300027e770237`; RP7
`46444909599fe25f2b34d71b81fb0cfdbe5fb121`. The concurrent working-tree change was not
read into these recorded summaries and was never written by this task. The committed
blobs exposed:

```text
RP6-P0.sh: resolved_count=1 unresolved_count=37
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=331:redirection >,line=333:redirection >
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete

RP7-WPI-RO.sh: resolved_count=4 unresolved_count=65
PATH value=/dev/null verdict=FORBID rule=- sources=NONE uses=line=183:redirection >,line=624:redirection >,line=625:redirection >
PATH value=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/bin/python verdict=ALLOW rule=/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b/** sources=WPI_VENV_ROOT uses=line=763:test
PATH value=/proc/self/mountinfo verdict=FORBID rule=- sources=NONE uses=line=413:redirection <
PATH value=/proc/uptime verdict=FORBID rule=- sources=NONE uses=line=173:redirection <
PATHSCOPE verdict=REJECT rc=3 reason=static_resolution_incomplete
```

The unresolved counts are findings, not coverage claims. They include unsupported Bash
arrays, positional/local dataflow, opaque wrapper calls, and unpinned evidence paths. A
future freeze must remove those ambiguities or extend and audit the prover; the counts must
not be converted into a PASS by suppressing constructs.
