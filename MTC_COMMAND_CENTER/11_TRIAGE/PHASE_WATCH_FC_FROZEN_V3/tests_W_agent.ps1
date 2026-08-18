# tests_W_agent.ps1 — FROZEN V3. W1-W4 Windows agent behavioral matrix.
# Fingerprints only; never displays or serializes key material.
$fp = 'PASTE-EXPECTED-FINGERPRINT-AT-APPLICATION'   # SHA256:... of mtc_watch_ro.pub
function Check([string]$label) {
    $rows = & 'C:\Windows\System32\OpenSSH\ssh-add.exe' -l 2>&1
    $ok = [bool]($rows | Where-Object { $_ -match [regex]::Escape($fp) })
    "{0}: {1}" -f $label, $(if ($ok) {'PASS - fingerprint present'} else {'FAIL - fingerprint absent'})
}
"W1: Restart-Service ssh-agent (run as admin), then:"; Check 'W1 after agent restart'
"W2: log off and back on, rerun this script:"; Check 'W2 after logoff/logon'
"W3: reboot, log on, rerun this script:"; Check 'W3 after reboot'
"W4: from the scheduled-task user context, rerun this script:"; Check 'W4 task context'
# Honest documented limit: the watch task runs only while the owner is logged on;
# after reboot the watch pauses until logon (missing daily summary = the signal).
