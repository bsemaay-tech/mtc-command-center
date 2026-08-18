# tests_T_ssh_lockdown.ps1 — FROZEN V3. T1-T10 falsification matrix, run from
# Windows AFTER provisioning, BEFORE the watcher uses the account. Uses only the
# dedicated agent-loaded key (never reads key material). Every test prints
# PASS/FAIL against its expected outcome; any FAIL means rollback per
# provisioning-commands.sh.
$ErrorActionPreference = 'Continue'
$ssh  = 'C:\Windows\System32\OpenSSH\ssh.exe'
$scp  = 'C:\Windows\System32\OpenSSH\scp.exe'
$sftp = 'C:\Windows\System32\OpenSSH\sftp.exe'
$dst  = 'mtc-watch@152.239.123.231'
$kh   = Join-Path $env:USERPROFILE '.ssh\known_hosts'
$base = @('-F','NUL','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',"-o","UserKnownHostsFile=$kh",'-o','IdentitiesOnly=yes','-o','ConnectTimeout=15')
function T([string]$name, [scriptblock]$run, [scriptblock]$judge) {
    $out = & $run 2>&1 | Out-String; $code = $LASTEXITCODE
    $ok = & $judge $out $code
    "{0}: {1}  (exit={2})" -f $name, $(if ($ok) {'PASS'} else {'FAIL'}), $code
}
T 'T1 forced check1 works'      { & $ssh @base $dst check1 }                          { param($o,$c) $c -eq 0 -and $o -match 'active' }
T 'T2 bare login refused'       { & $ssh @base $dst }                                  { param($o,$c) $c -ne 0 -and $o -match 'refused' }
T 'T3 arbitrary cmd refused'    { & $ssh @base $dst 'id; uname -a' }                   { param($o,$c) $c -ne 0 -and $o -match 'refused' -and $o -notmatch 'uid=' }
T 'T4 PTY refused'              { & $ssh @base -tt $dst check1 }                       { param($o,$c) $o -notmatch 'pty allocated' -and ($c -ne 0 -or $o -match 'PTY|refused|not permit') }
T 'T5 local forward refused'    { & $ssh @base -L 19999:127.0.0.1:8790 $dst check1 }   { param($o,$c) $o -match 'forwarding.*(disabled|failed|administratively)' -or $c -ne 0 }
T 'T6 remote forward refused'   { & $ssh @base -R 19998:127.0.0.1:80 $dst check1 }     { param($o,$c) $o -match 'forwarding.*(disabled|failed|administratively)' -or $c -ne 0 }
T 'T7a scp refused'             { & $scp @base "${dst}:/etc/passwd" $env:TEMP }        { param($o,$c) $c -ne 0 }
T 'T7b sftp refused'            { & $sftp @base $dst }                                 { param($o,$c) $c -ne 0 }
T 'T8 unknown id refused'       { & $ssh @base $dst check99 }                          { param($o,$c) $c -ne 0 -and $o -match 'refused: unknown check id' }
T 'T10 password auth refused'   { & $ssh @base -o PreferredAuthentications=password -o PubkeyAuthentication=no $dst check1 } { param($o,$c) $c -ne 0 }
# T9 (foreign key refused) requires a second throwaway keypair the owner generates
# for the test; run manually: ssh with that key must fail authentication.
