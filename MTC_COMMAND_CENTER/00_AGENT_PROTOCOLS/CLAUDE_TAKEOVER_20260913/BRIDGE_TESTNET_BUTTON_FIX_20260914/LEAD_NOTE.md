# Bridge Toolkit button 5 (TESTNET Secret Provisioning, KVM2-P4-03) — launcher defect found by the owner's first click, fixed 2026-09-14 13:25Z

**Symptom (owner, chat 13:1xZ):** "terminal açılıp hemen kapanıyor" — the window opened and closed instantly.

**Root cause (Lead, reproduced):** `C:\LAB\BRIDGE_TOOLKIT\bin\testnet_provision.ps1` line 30 read
`Write-Host "  1/3 copying the wizard to $HostUser@$HostAddr:$Remote ..."`. PowerShell parses `$HostAddr:` as a drive/scope-qualified variable and the whole file fails to PARSE: `Variable reference is not valid. ':' was not followed by a valid variable name character.` `powershell -File` prints that and exits before executing a single statement, so the script's own "Press Enter to close" pauses are never reached and the console window closes at once. RED: `RED_true_original_head.ps1.txt` (the original head up to line 30) → real parser 1 error, `powershell -File` exits at line 26 with the message above. GREEN: fixed file → real parser 0 errors; the head runs through the banner and the prerequisite checks.

**Why the audit missed it:** the wizard security review (Gemini 3.8, documentary, `BRIDGE_TESTNET_WIZARD_GEMINI_AUDIT_20260914.md`) cannot execute anything, and the Lead never launched the button before presenting it — the same class as "a reviewer that cannot read the subject": a launcher that was never run once is not verified to start. Rule going forward: every owner-facing button gets one Lead dry-launch through the real entry point (with the network step stubbed or the prerequisites deliberately missing) before it is presented.

**Fixes applied (Toolkit lives outside the repository; copies here as `.txt`):**
1. `bin\testnet_provision.ps1`: `${HostAddr}:` delimiter (parse error gone); the best-effort remote cleanup line (`… 2>$null | Out-Null`) now runs under `$ErrorActionPreference='Continue'` inside try/catch — under `'Stop'` a native command's redirected stderr line throws (`RemoteException`, verified with an unresolvable host) and would end the script before its final message; file made pure ASCII (the em dash in the header comment removed; the file has no BOM and PowerShell 5.1 read it as ANSI).
2. `5 - TESTNET Secret Provisioning (KVM2).cmd`: `echo.` + notice + `pause` after the PowerShell call, so any future start-up message stays readable instead of a vanishing window.
No change to what the wizard does on the host (stages 1-4 unchanged, writes only `/etc/mtc-bridge/mtc-bridge.env`, no restart, no ARM). Backups: `C:\tmp\btn5.cmd.BAK_20260914`; the pre-fix `.ps1` text is reconstructed in `RED_true_original_head.ps1.txt` (the on-disk backup `C:\tmp\testnet_provision.ps1.BAK_20260914_preParseFix` was taken after the first edit and is NOT the original — recorded to keep the evidence honest).

Owner asked to retry the button; "provisioned" still awaited. No host contact by the Lead for this fix.
