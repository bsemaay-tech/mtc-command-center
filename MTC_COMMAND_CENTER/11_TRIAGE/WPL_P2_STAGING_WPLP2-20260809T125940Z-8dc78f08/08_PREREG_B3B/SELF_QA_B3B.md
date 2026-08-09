# Stage 2B B3B self-QA

Result: **PASS for the preregistration template; execution remains locally
blocked until dispatch binds the unit and numeric service uid/gid and re-freezes
all dependent hashes.**

All commands below were local and read-only except creation of the deliverables
inside `08_PREREG_B3B/`. No ssh, scp, TCP probe, or other host contact occurred.
No Git command was run.

## Q1. Shell syntax

Command:

```powershell
$d='/mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/08_PREREG_B3B'; foreach($f in @('remote_setup_b3b.sh','remote_extract_verify_b3b.sh','run_b3b.sh','remote_close_tree_b3b.sh')){ bash -n "$d/$f"; "$f rc=$LASTEXITCODE" }
```

Real output:

```text
remote_setup_b3b.sh rc=0
remote_extract_verify_b3b.sh rc=0
run_b3b.sh rc=0
remote_close_tree_b3b.sh rc=0
```

An earlier invocation passed Windows paths directly to WSL bash and therefore
tested no file. It returned 127 for each path. That invocation is rejected as
evidence; Q1 is the corrected `/mnt/c/...` command and output above.

## Q2. PowerShell syntax and dry-run proof

Command:

```powershell
$p='C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\08_PREREG_B3B\transport_runner_b3b.ps1'; $tokens=$null; $errors=$null; [void][System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$tokens,[ref]$errors); "parse_errors=$($errors.Count)"; & $p | Select-String '^TR_(PLAN_ROWS|OP_PLANNED|DRY_RUN)'; "runner_rc=$LASTEXITCODE"
```

`Write-Host` uses the information stream, so the pipeline leaves the full
runner narration visible. Real output:

```text
parse_errors=0
TR_HEADER base_run=WPLP2B-20260809T210610Z-834380c5
TR_MODE execute=False confirm_supplied=False
TR_LOCATION dir=C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\08_PREREG_B3B
TR_PLAN path=C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\08_PREREG_B3B\TRANSPORT_PLAN_B3B.tsv sha256=2f50feae6a91d519bf824208907dbc2ab6153729dd57e90ade9156fb72f99f4a
TR_PLAN_ROWS count=7
TR_STDIN op=01 file=remote_setup_b3b.sh sha256=242b14ce848607ed1ae58a50d2effe03fcb13549867629578cf74d0e0a3b3866
TR_STDIN op=03 file=remote_extract_verify_b3b.sh sha256=68007732d8088f076575bd71a59e987e6f677602e272a4f36b19215e31d39750
TR_STDIN op=04 file=run_b3b.sh sha256=ae56c4a962ba28b1114b280823ae5c4661237c77085e67c443f780d6a7bd37b0
TR_STDIN op=05 file=remote_close_tree_b3b.sh sha256=5a9cfd5e8cec5960670fd46339f8fb15c355e2de23a34d878c0dc0e69cc50dcb
TR_PINNED path=C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\07_RUNKIT_B\runkit_b.tar sha256=888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b
TR_PROGRAM name=ssh resolved=C:\Windows\System32\OpenSSH\ssh.exe
TR_PROGRAM name=scp resolved=C:\Windows\System32\OpenSSH\scp.exe
TR_OP_PLANNED id=01 kind=ssh_stdin run_when=sequence_ok expect_rc=0 stdin=remote_setup_b3b.sh
TR_OP_ARGV id=01 argv=[ssh] [-i] [C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519] [-o] [BatchMode=yes] [-o] [StrictHostKeyChecking=yes] [-o] [IdentitiesOnly=yes] [-o] [ConnectTimeout=20] [gatea@172.24.55.233] [bash] [-s] [--] [/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5]
TR_OP_PLANNED id=02 kind=scp_up run_when=sequence_ok expect_rc=0 stdin=-
TR_OP_ARGV id=02 argv=[scp] [-i] [C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519] [-o] [BatchMode=yes] [-o] [StrictHostKeyChecking=yes] [-o] [IdentitiesOnly=yes] [-o] [ConnectTimeout=20] [runkit_b.tar] [gatea@172.24.55.233:/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/kit/runkit_b.tar]
TR_OP_PLANNED id=03 kind=ssh_stdin run_when=sequence_ok expect_rc=0 stdin=remote_extract_verify_b3b.sh
TR_OP_ARGV id=03 argv=[ssh] [-i] [C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519] [-o] [BatchMode=yes] [-o] [StrictHostKeyChecking=yes] [-o] [IdentitiesOnly=yes] [-o] [ConnectTimeout=20] [gatea@172.24.55.233] [bash] [-s] [--] [/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/kit/runkit_b.tar] [/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/kit/extracted] [888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b]
TR_OP_PLANNED id=04 kind=ssh_stdin run_when=sequence_ok expect_rc=0 stdin=run_b3b.sh
TR_OP_ARGV id=04 argv=[ssh] [-i] [C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519] [-o] [BatchMode=yes] [-o] [StrictHostKeyChecking=yes] [-o] [IdentitiesOnly=yes] [-o] [ConnectTimeout=20] [gatea@172.24.55.233] [bash] [-s] [--]
TR_OP_PLANNED id=05 kind=ssh_stdin run_when=always expect_rc=0 stdin=remote_close_tree_b3b.sh
TR_OP_ARGV id=05 argv=[ssh] [-i] [C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519] [-o] [BatchMode=yes] [-o] [StrictHostKeyChecking=yes] [-o] [IdentitiesOnly=yes] [-o] [ConnectTimeout=20] [gatea@172.24.55.233] [bash] [-s] [--] [/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/evidence/runkit/WPLP2B-20260809T210610Z-834380c5-B3B] [WPLP2B-20260809T210610Z-834380c5-B3B]
TR_OP_PLANNED id=06 kind=scp_down run_when=always expect_rc=0 stdin=-
TR_OP_ARGV id=06 argv=[scp] [-i] [C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519] [-o] [BatchMode=yes] [-o] [StrictHostKeyChecking=yes] [-o] [IdentitiesOnly=yes] [-o] [ConnectTimeout=20] [-r] [gatea@172.24.55.233:/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5/evidence/runkit/WPLP2B-20260809T210610Z-834380c5-B3B] [.]
TR_OP_PLANNED id=07 kind=local_bind run_when=always expect_rc=0 stdin=-
TR_OP_ARGV id=07 argv=[local_bind] [05] [06] [evidence\WPLP2B-20260809T210610Z-834380c5-B3B]
TR_DRY_RUN no_process_was_started no_connection_was_opened
TR_DRY_RUN to execute: -Execute -Confirm WPLP2B-20260809T210610Z-834380c5-B3B-EXECUTE
runner_rc=0
```

The dry-run branch exits before record-root creation and before the only
`Start-Process` call. It printed all seven planned operations and opened no
connection.

## Q3. Execute-path placeholder refusal

Command:

```powershell
$p='C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\08_PREREG_B3B\transport_runner_b3b.ps1'; & $p -Execute -Confirm 'WPLP2B-20260809T210610Z-834380c5-B3B-EXECUTE' 6>&1 | Where-Object {"$_" -like 'TR_STOP*'}; "runner_rc=$LASTEXITCODE"
```

Real output:

```text
TR_STOP reason=dispatch_placeholders_unresolved; execution_refused_before_record_creation_or_process_start
runner_rc=3
```

This is the final local guard before record creation and any `Start-Process`.

## Q4. Archive and block digest re-verification

Archive command:

```powershell
bash -lc "sha256sum /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/runkit_b.tar"
```

Real output:

```text
888bec17cbea99a781368b7c3747d6a9085840005a686000bedaadcacb44246b  /mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/runkit_b.tar
```

Member/digest command:

```powershell
$a='/mnt/c/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/runkit_b.tar'; bash -lc "tar -tf $a"; foreach($n in @('RP0-LIB.sh','RP0-BOOTSTRAP.sh','RP1-B3.sh','RP3-C2A-POST.sh','RP3-C2B-POST.sh','RP4-C3.py','RP5-C4A.sh','RP5-C4B.sh','RP5-C4C.sh','RPD-VERIFY.sh')){ bash -lc "tar -xOf $a $n | sha256sum" | ForEach-Object { $_ -replace '  -$', "  $n" } }
```

Real output:

```text
RP0-LIB.sh
RP0-BOOTSTRAP.sh
RP1-B3.sh
RP3-C2A-POST.sh
RP3-C2B-POST.sh
RP4-C3.py
RP5-C4A.sh
RP5-C4B.sh
RP5-C4C.sh
RPD-VERIFY.sh
4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48  RP0-LIB.sh
e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33  RP0-BOOTSTRAP.sh
6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc  RP1-B3.sh
e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27  RP3-C2A-POST.sh
26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412  RP3-C2B-POST.sh
0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5  RP4-C3.py
a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2  RP5-C4A.sh
10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e  RP5-C4B.sh
de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8  RP5-C4C.sh
3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c  RPD-VERIFY.sh
```

The archive has 10 listed members, in the frozen order, and all ten streamed
member digests match `BLOCK_IDENTITIES_B.tsv`. No member was extracted to disk.
An earlier loop-construction attempt failed before producing a digest set and
is rejected as evidence; the two successful commands above are the accepted
re-verification.

## Q5. Plan schema, ordering, rc contract, and ASCII

Command:

```powershell
$d='C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\08_PREREG_B3B'; $p=Join-Path $d 'TRANSPORT_PLAN_B3B.tsv'; $rows=Get-Content -LiteralPath $p -Encoding UTF8; "rows=$($rows.Count) ops=$($rows.Count-1)"; for($i=0;$i -lt $rows.Count;$i++){"row=$($i+1) fields=$(($rows[$i] -split "`t").Count)"}; Import-Csv -LiteralPath $p -Delimiter "`t" | ForEach-Object {"op=$($_.op_id) run_when=$($_.run_when) expect_rc=$($_.expect_rc) kind=$($_.kind)"}; foreach($f in @('remote_setup_b3b.sh','remote_extract_verify_b3b.sh','run_b3b.sh','remote_close_tree_b3b.sh','TRANSPORT_PLAN_B3B.tsv','transport_runner_b3b.ps1','PREREGISTRATION_B3B.md')){$bytes=[IO.File]::ReadAllBytes((Join-Path $d $f)); "$f non_ascii=$(($bytes|Where-Object {$_ -gt 127}).Count)"}
```

Real output:

```text
rows=8 ops=7
row=1 fields=9
row=2 fields=9
row=3 fields=9
row=4 fields=9
row=5 fields=9
row=6 fields=9
row=7 fields=9
row=8 fields=9
op=01 run_when=sequence_ok expect_rc=0 kind=ssh_stdin
op=02 run_when=sequence_ok expect_rc=0 kind=scp_up
op=03 run_when=sequence_ok expect_rc=0 kind=ssh_stdin
op=04 run_when=sequence_ok expect_rc=0 kind=ssh_stdin
op=05 run_when=always expect_rc=0 kind=ssh_stdin
op=06 run_when=always expect_rc=0 kind=scp_down
op=07 run_when=always expect_rc=0 kind=local_bind
remote_setup_b3b.sh non_ascii=0
remote_extract_verify_b3b.sh non_ascii=0
run_b3b.sh non_ascii=0
remote_close_tree_b3b.sh non_ascii=0
TRANSPORT_PLAN_B3B.tsv non_ascii=0
transport_runner_b3b.ps1 non_ascii=0
PREREGISTRATION_B3B.md non_ascii=0
```

## Q6. New-path collision check

Command:

```powershell
$newRemote='/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5'; $newRecord='C:\WPI_ARTIFACTS\WPLP2B_TRANSPORT_WPLP2B-20260809T210610Z-834380c5'; $existing=@('/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08','C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08','C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08-R45B'); foreach($old in $existing){$candidate=if($old.StartsWith('/')){$newRemote}else{$newRecord}; "new=[$candidate] existing=[$old] equal=$($candidate -eq $old) prefix_collision=$($candidate.StartsWith($old) -or $old.StartsWith($candidate))"}
```

Real output:

```text
new=[/home/gatea/wpl_p2b_staging_WPLP2B-20260809T210610Z-834380c5] existing=[/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08] equal=False prefix_collision=False
new=[C:\WPI_ARTIFACTS\WPLP2B_TRANSPORT_WPLP2B-20260809T210610Z-834380c5] existing=[C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08] equal=False prefix_collision=False
new=[C:\WPI_ARTIFACTS\WPLP2B_TRANSPORT_WPLP2B-20260809T210610Z-834380c5] existing=[C:\WPI_ARTIFACTS\WPLP2_TRANSPORT_WPLP2-20260809T125940Z-8dc78f08-R45B] equal=False prefix_collision=False
```

The check is a pure string comparison. It does not inspect either host or
operator artifact root.

## Q7. Support artifact digests and sizes

Command:

```powershell
$d='C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\08_PREREG_B3B'; foreach($f in @('remote_setup_b3b.sh','remote_extract_verify_b3b.sh','run_b3b.sh','remote_close_tree_b3b.sh','TRANSPORT_PLAN_B3B.tsv','transport_runner_b3b.ps1')){$x=Get-Item -LiteralPath (Join-Path $d $f); "$((Get-FileHash -LiteralPath $x.FullName -Algorithm SHA256).Hash.ToLowerInvariant())  $f  bytes=$($x.Length)"}
```

Real output:

```text
242b14ce848607ed1ae58a50d2effe03fcb13549867629578cf74d0e0a3b3866  remote_setup_b3b.sh  bytes=3244
68007732d8088f076575bd71a59e987e6f677602e272a4f36b19215e31d39750  remote_extract_verify_b3b.sh  bytes=6155
ae56c4a962ba28b1114b280823ae5c4661237c77085e67c443f780d6a7bd37b0  run_b3b.sh  bytes=2295
5a9cfd5e8cec5960670fd46339f8fb15c355e2de23a34d878c0dc0e69cc50dcb  remote_close_tree_b3b.sh  bytes=4305
2f50feae6a91d519bf824208907dbc2ab6153729dd57e90ade9156fb72f99f4a  TRANSPORT_PLAN_B3B.tsv  bytes=3486
a94e91146b6c9091b38895f78d1379661b33ada5177176d9ede2da372ea39791  transport_runner_b3b.ps1  bytes=14343
```

## Q8. Final scope result

- Produced artifacts are confined to `08_PREREG_B3B/`.
- Dry run returned 0 and printed seven operations.
- Placeholder execute attempt returned 3 before record creation/process start.
- Every planned op expects rc 0; ops 05-07 are `always`.
- No staging host contact, Git mutation, service action, credential read, ARM,
  order, broker/exchange, TESTNET/mainnet, deployment, or root action occurred.

## Q9. Checksum manifest peer verification

Command:

```powershell
$d='C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08\08_PREREG_B3B'; $sum=Join-Path $d 'PREREG_B3B_SHA256SUMS.txt'; $ok=$true; foreach($line in Get-Content -LiteralPath $sum){$want,$name=$line -split '  ',2; if($name -eq 'SELF_QA_B3B.md'){continue}; $got=(Get-FileHash -LiteralPath (Join-Path $d $name) -Algorithm SHA256).Hash.ToLowerInvariant(); $match=$want -eq $got; if(-not $match){$ok=$false}; "$name match=$match"}; $bytes=[IO.File]::ReadAllBytes($sum); "manifest_peer_files_excluding_selfqa_match=$ok"; "manifest_non_ascii=$(($bytes|Where-Object {$_ -gt 127}).Count)"
```

Real output:

```text
PREREGISTRATION_B3B.md match=True
TRANSPORT_PLAN_B3B.tsv match=True
remote_close_tree_b3b.sh match=True
remote_extract_verify_b3b.sh match=True
remote_setup_b3b.sh match=True
run_b3b.sh match=True
transport_runner_b3b.ps1 match=True
manifest_peer_files_excluding_selfqa_match=True
manifest_non_ascii=0
```

The manifest lists every other produced file. It cannot include its own digest:
a digest manifest cannot contain a stable SHA-256 of its own complete bytes.
The manifest's own SHA-256 is printed in the final handoff.
