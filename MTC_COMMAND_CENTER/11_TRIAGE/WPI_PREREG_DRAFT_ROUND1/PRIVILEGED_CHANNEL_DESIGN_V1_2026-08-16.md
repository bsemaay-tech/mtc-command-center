Status: PRIVILEGED CHANNEL DESIGN RECOMMENDATION V1 — DOCUMENTATION ONLY — NOT ACCEPTED — NO HOST ACTION TAKEN

# GATEA-STAGING privileged read-only channel design recommendation

Date: 2026-08-16  
Scope: `GATEA-STAGING` only  
Audit classification: T0 for the required later flagship review because this is a host/security/authentication design  
Execution state: not run; every command below is a proposal for the separately authorized later phase

This recommendation creates no acceptance and spends no authority. The owner authorized a later execution phase on `GATEA-STAGING` only, including configuration and controlled verification, but required design and T0 review first. Hostinger, `KVM2-Ubuntu-2404-Staging`, production, broker/exchange paths, ARM, orders, TESTNET/mainnet, trading logic, and master merge remain excluded. `MTC_COMMAND_CENTER/11_TRIAGE/HOST_CHANNEL_AUTHORIZATION_2026-08-16.md:20-34,44-66`

The corrected starting facts are controlling: `GATEA-STAGING` is the owner's local Generation-2 Hyper-V VM, is currently Off, uses the Default Switch, has no checkpoint, has checkpointing disabled, and has a stale recorded address. The private identity exists at `C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`; its contents are not an input to this design and must never be inspected or emitted. `C:\tmp\lane_kick\CH1.md:20-47`; `MTC_COMMAND_CENTER/11_TRIAGE/HOST_CHANNEL_AUTHORIZATION_2026-08-16.md:83-105`

The repository establishes narrow root authority and an ordinary `gatea` transport, but not a privileged route. It records three choices and five observations, plus a separate crossover blocker. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:5-14,172-195,230-236`

## 1. Three category-(c) decisions

### 1.1 Privileged route and SSH principal

**Choice:** create a dedicated, password-locked SSH account named `gatea-attest`, with no home directory and no ordinary interactive shell. Authenticate it with the already pinned identity at `C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`; the exact target is:

```text
gatea-attest@<DHCP_IPV4_OBSERVED_AFTER_START>
```

The address is deliberately `UNKNOWN` now. It becomes concrete only after the VM starts and the Hyper-V-reported address, Default-Switch subnet, VM NIC MAC, reachability, and existing host-key pin all agree. The stale `172.24.55.233` is used only as the lookup alias for the existing `known_hosts` pin, never as a network destination. `C:\tmp\lane_kick\CH1.md:35-42`

The private-key file is passed only as OpenSSH's `-i` path. No command may print it, hash it, derive a public key from it, copy it, replace it, or rotate it. The server-side public-key mapping is to be reused without creating a keypair. If reusing the existing server-side authorized-key object for the new principal cannot be done without exposing or replacing key contents, execution stops; it does not generate a new key.

**Rationale:** a separate principal lets the privileged channel have a forced command and a non-shell account without weakening or breaking the ordinary `gatea` transport used elsewhere. It also lets the root wrapper drop to a different capture UID that owns no key and has no sudo rule.

**Rejected alternatives:**

- `root@<address>`: rejected because direct root SSH unnecessarily exposes a root authentication endpoint and makes the pre-drop process able to lift in-VM controls.
- Ordinary `gatea` plus an arbitrary remote command: rejected because its outer account shell acts before the cleared inner environment. The transport records explicitly keep that boundary open and say that disclosure is not a control. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/run_ro.sh:45-66`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/STATUS_TRANSPORT.md:303-327`
- Ordinary `gatea` plus assumed generic sudo: rejected. The records prove only enumerated command-specific `NOPASSWD` families; generic `sudo -n -v` failed, and nothing maps ATT-01 to those families. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A7_PREFLIGHT_2026-08-09D.md:32-43`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:160-170`
- A second keypair, certificate, copied private key, or rotated key: excluded because it creates or handles new key material contrary to the owner fence.

### 1.2 Direct root versus exact wrapper/escalation chain

**Choice:** no direct-root login. The complete selected chain is:

```text
Windows OpenSSH client using -i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519
  -> GATEA-STAGING sshd, principal gatea-attest, publickey only
  -> Match User gatea-attest ForceCommand
  -> /usr/local/libexec/gatea-attest/v1/attest-login
       (root-owned, statically linked native account-shell gate; exact bytes pinned)
  -> /usr/bin/sudo -n -- /usr/local/libexec/gatea-attest/v1/attest-root
       (one exact NOPASSWD command; no arguments and no SETENV)
  -> private mount namespace + read-only enforcement
  -> permanent drop to numeric gatea-capture UID:GID, no groups/capabilities/sudo/key
  -> /usr/bin/python3 -I -S -B /usr/local/libexec/gatea-attest/v1/channel-attestation.py
       (one fixed, vetted, pinned read-only script; no caller-selected command or arguments)
```

`attest-login` is an account-shell gate, not a general shell. It accepts only sshd's exact `-c` invocation for the configured forced-command literal, rejects a nonempty `SSH_ORIGINAL_COMMAND`, records the initial environment/cwd/FD envelope without values being interpreted by a shell, clears the environment, closes every descriptor above 2, changes to `/`, and `execve`s the exact absolute sudo argv. Because it is static, no dynamic-loader or shell-startup hook precedes its checks.

The sudo policy names one absolute wrapper, exactly, for `gatea-attest` only. The existing `gatea` sudo families remain unchanged and are not treated as proof of this route. Their only relevance is that command-specific `NOPASSWD` is an already used host mechanism. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_D_2026-08-08/README.txt:157-171`; `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RUN_KIT_E_2026-08-09/README.txt:456-466`

The selected bootstrap for installing this chain is the Hyper-V console for the explicitly named VM, not an SSH privilege inference:

```powershell
$VmName = 'GATEA-STAGING'; if ($VmName -cne 'GATEA-STAGING') { throw 'SCOPE_STOP' }; & "$env:WINDIR\System32\vmconnect.exe" localhost $VmName
```

In the later phase, the operator may use the VM's local recovery/root console solely to install the accepted files. If a root console cannot be established without another credential, another VM, an offline broad-disk operation, or a weakened boot/security control, the phase stops. The owner authorized root on `GATEA-STAGING`; authorization is not evidence that the capability exists. No existing limited-sudo rule is to be exploited into a shell.

### 1.3 Category-1 mutation-denial control

**Choice:** `GATEA_RO_V1`, a layered root wrapper that becomes irreversible before the capture script begins:

1. Require exact executable hashes, numeric ownership `0:0`, non-symlink regular-file kind, and no group/other write bit for `attest-login`, `sudo`, `attest-root`, `/usr/bin/python3`, and `channel-attestation.py`.
2. Enter a new mount namespace, make propagation private, and use recursive `mount_setattr` read-only attributes over every visible filesystem mount. There is no writable tmpfs, home, state, or evidence directory in the capture namespace.
3. Close every inherited descriptor except 0, 1, and 2; prove 0 is SSH stdin and 1/2 are SSH stdout/stderr, with no other writable descriptor.
4. Set `PR_SET_NO_NEW_PRIVS`, install a Landlock ruleset handling every filesystem write/create/remove/rename/refer/truncate class supported by the accepted kernel contract, and deny network, mount, namespace, ptrace, BPF, keyring, and privilege-changing operations with the accepted syscall filter.
5. Clear supplementary groups and all capability sets/bounding/ambient state; set real/effective/saved GID and UID to the separately created locked `gatea-capture` account; require the numeric post-drop state, `NoNewPrivs=1`, zero capabilities, and the accepted namespace identities.
6. Execute only the fixed read-only script. It opens target inputs read-only, has no subprocess or socket API, and writes only to inherited fd 1/2.

If the kernel lacks the exact accepted `mount_setattr`, Landlock, privilege-drop, or syscall-filter behavior, the route is `STOP/UNEVALUATED`; it does not fall back to source inspection, DAC alone, a container label, `NOEXEC`, or a prose disclosure. The required V2 field demands success- and failure-path denial while fd 1/2 remain usable. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:31-49,139-170`

**Rejected alternatives:** checkpoint alone (rollback, not denial); read-only producer source alone (does not constrain sshd, the shell, loader, wrapper, or failure paths); DAC-only non-root (does not cover writable objects owned by the UID); a read-only bind of only one tree (leaves other mounts and kernel mutation interfaces); `sudo NOEXEC`/`LD_PRELOAD` (not a complete or independent control); and a general-purpose root shell followed by a voluntary promise to read only.

## 2. Independence solution

The single operator cannot prove personal independence to a second party. This design instead separates what the in-VM capture process can reach from what only the Windows host or earlier root configuration can reach. That is the limit already recorded by the owner. `MTC_COMMAND_CENTER/11_TRIAGE/HOST_CHANNEL_AUTHORIZATION_2026-08-16.md:68-81`

| Layer | Can the in-VM `gatea-capture` process reach or lift it? | ENFORCED | DISCLOSED / not proved |
|---|---|---|---|
| Pre-change Hyper-V Standard checkpoint named `GATEA-STAGING-CH1-PRECHANGE-V1` | **No.** It exists in the Windows hypervisor, outside every guest namespace, including guest root. | A restorable pre-change disk/configuration point and an external checkpoint ID/time. It prevents an in-VM process from deleting the rollback point or rewriting its identity. | It does not prevent guest mutation. The same Windows administrator/operator can delete or restore it; no second person certifies it. |
| Existing host-key pin and existing private identity path | **No** after connection. | OpenSSH refuses a host key that does not match the pre-existing `known_hosts` value; the caller cannot select `accept-new`. Only the specified identity path is offered. | The operator owns both files. This design does not establish when or by whom they were created. |
| Dedicated `gatea-attest` principal, sshd `ForceCommand`, restricted forwarding/PTY/user-rc policy, and exact static account shell | **No.** The authenticated UID cannot write root-owned sshd/account/sudo configuration. | The SSH client cannot choose a remote command, shell startup file, forwarding channel, agent, PTY, environment extension, or wrapper argv. A nonempty original command is rejected before sudo. | One operator installed and later certifies the configuration. Native sshd/PAM/login records are expected category-2 records. |
| Exact sudo rule and `attest-root` | **No** after the forced hop. | Only one no-argument absolute wrapper may run as root. The wrapper refuses a different argv, environment, cwd, file identity, descriptor envelope, or VM identity. | Root during configuration could have installed different bytes; exact-byte T0 review, hashes, and later read-back reduce but do not eliminate operator trust. |
| Private read-only mount view + Landlock/syscall restrictions + irreversible UID/capability drop | **No.** After `no_new_privs`, Landlock, namespace setup, capability bounding, and saved-ID drop, the capture process has no authority to remount, change policy, invoke sudo, or regain UID 0. | Category-1 filesystem mutation by the capture process is denied on success and failure paths; only fd 1/2 output remains writable. | This does not stop sshd/PAM/sudo/audit infrastructure outside the capture namespace from making their normal category-2 records. |
| External root observer and operator-side create-once evidence record | **No.** The observer is outside the capture process; the record is on Windows. | Runtime process state and the closed stdout/stderr/rc can be compared to independently frozen expectations. The capture cannot rewrite the local record or the Hyper-V checkpoint. | The one Windows operator can still alter local evidence after the fact; create-once, flush, hash, and independent re-read detect ordinary alteration but are not a second-party signature. |

The VM being local and disposable bounds the residual consequence: an unexpected configuration or crossover can stop, preserve evidence, and restore the checkpoint without involving Hostinger, KVM2, production, or an economic system. The checkpoint is therefore load-bearing rollback and evidence-integrity protection, but it is not mislabeled as proof that no write happened. `C:\tmp\lane_kick\CH1.md:49-63`

### Self-confirming test of the enforcement

The enforcement is not accepted because `attest-root` prints `read_only=true`. It is accepted only if the exact real top-level forced-command path is falsified:

- **Expected value:** the accepted `GATEA_RO_V1` policy, canary path, exact production wrapper hash, exact root-only mutant hash, and fd markers are frozen before the test by the reviewed procedure, not produced by the capture script.
- **RED:** from the Hyper-V console root session, run an explicitly identified, never-installed mutant of `attest-root` in which the recursive read-only/Landlock transition is disabled. Under the same numeric capture UID and against the dedicated predeclared canary, the deliberate create/append/rename/delete matrix must succeed. This RED is a controlled configuration test, not a read-only capture and not grant #6. It may touch only the canary and is covered by the checkpoint.
- **GREEN:** through the actual SSH target, actual forced command, production wrapper, and production script, the identical matrix must be denied with the accepted errno classes; canary bytes/inode must remain equal to the independently captured pre-GREEN state; stdout marker on fd 1 and stderr marker on fd 2 must both arrive intact; no fd above 2 may exist.
- **Failure:** RED cannot write, GREEN can write, either stream marker is absent, the canary cannot be re-read, the wrapper/mutant identity differs, or the real top-level path was not exercised. Any is STOP/BLOCK, never PASS.

This follows the project's rule that a check needs an independent expected value and a concrete world in which it goes red. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63,73-83`; inability to observe remains STOP rather than a host-state FAIL. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:48-107`

## 3. Eight-fact resolution map

All commands in this section are **later-phase proposals only**. The fixed observer and entry artifacts do not exist yet; their bytes and hashes are `UNKNOWN` until implemented, falsified, T0-reviewed, and frozen. A command therefore cannot be run merely from this document.

The notation below is fixed for the later run:

```text
VM_NAME=GATEA-STAGING
ENTRY=/usr/local/libexec/gatea-attest/v1/attest-login
ROOT_GATE=/usr/local/libexec/gatea-attest/v1/attest-root
OBSERVER=/usr/local/libexec/gatea-attest/v1/channel-observer
CAPTURE=/usr/local/libexec/gatea-attest/v1/channel-attestation.py
```

| Fact | Class and resolution | Exact read-only verification command after configuration | Independent expectation and red condition |
|---|---|---|---|
| SSH principal | **Choice:** `gatea-attest@<observed-DHCP-IPv4>`, publickey-only, using the existing Windows `-i` path. Concrete IP is `UNKNOWN` now. | Operator: `$VmName='GATEA-STAGING'; & $SshExe @SshPinnedOptions -i 'C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519' "gatea-attest@$VmIp"` with no remote command. | Expected principal comes from this accepted design; IP comes from the GATEA NIC/DHCP observation; host key comes from the pre-existing `known_hosts`; accepted-key fingerprint comes from client/server authentication records. Wrong user/IP/key, another auth method, or inability to bind them is STOP. |
| Account shell | **Observation:** exact path is selected as `/usr/local/libexec/gatea-attest/v1/attest-login`; numeric UID:GID and SHA-256 are `UNKNOWN` until installed and observed. | Root observer: `GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact account --principal gatea-attest` | Expected path/hash/owner/mode comes from the frozen Commit-1a artifact manifest; numeric UID:GID comes from the create-account record and is checked against `/etc/passwd`/kernel state. Missing, duplicate UID, different shell/blob/owner/mode, or unreadability is STOP. |
| Forced command | **Observation:** exact value selected as `/usr/bin/sudo -n -- /usr/local/libexec/gatea-attest/v1/attest-root`; both sshd Match policy and the account-shell argv gate must agree. | Root observer: `GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact forced-command --principal gatea-attest` | Expected literal and disabled forwarding/PTY/user-rc/auth-method policy come from the accepted config manifest; actual effective values come from complete `sshd -T -C ...`, account data, and sudoers parsing. Claimed `NONE`, ambiguity, extra args, caller command acceptance, or incomplete effective-config evaluation is STOP. |
| Wrapper mapping | **Choice:** the complete chain in §1.2; direct root is forbidden. | Root observer: `GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact process-chain --principal gatea-attest` while one certification session is held at its preregistered barrier. | Expected hop/path/hash/UID sequence comes from Commit 1a. Actual parent/child executable identities and numeric credentials come from the external `/proc/<pid>` observer, not the capture's prose. Missing/extra hop, PATH lookup, root retained at capture, or observer inability is STOP. |
| Pre-`env` environment | **Observation:** canonical sorted `name=value\0` bytes are `UNKNOWN` until the first target process is observed; the allowed-name/value-derivation universe is fixed in Commit 1a. Values must not be printed in clear. | Forced connection above emits canonical base64; external corroboration: `GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact pre-environment --session-id "$CHANNEL_CERT_RECORD_ID"` | Expected names and fixed values come from sshd/account config; dynamic connection fields derive from the independently observed Windows/VM addresses. Actual bytes come from the static entry process and external `/proc` snapshot. Unexpected `BASH_ENV`, `ENV`, loader, Python, function, locale, tmp, agent, or secret-bearing entry—or unreadability—is STOP. |
| Initial cwd | **Observation:** selected expected value `/` for the first account-shell process, before any `chdir`; actual value is `UNKNOWN` until observed. | `GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact initial-cwd --session-id "$CHANNEL_CERT_RECORD_ID"` | Expected `/` comes from the accepted account-home/entry contract. Actual comes from the entry gate plus an external `/proc/<pid>/cwd` lookup at the barrier. Any other path, symlink ambiguity, race, or inability is STOP. |
| Descriptor set | **Observation:** selected expectation is exactly `0=ssh-stdin,1=ssh-stdout,2=ssh-stderr,all_other_fds=closed`; actual is `UNKNOWN` until observed. | `GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact descriptors --session-id "$CHANNEL_CERT_RECORD_ID"` | Expected mapping is fixed by Commit 1a, not by the capture. Actual full `/proc/<pid>/fd` and `fdinfo` universe comes from the external observer and the entry gate. Extra FD, writable file/memfd/socket beyond 1/2, wrong access mode, enumeration race, or unreadability is STOP. |
| Mutation-denial control | **Choice:** `GATEA_RO_V1`—recursive read-only mount namespace, Landlock/syscall fence, no-new-privileges, zero capabilities/groups, permanent drop to `gatea-capture`, fixed script, output only on 1/2. | Production path: the forced SSH command with no caller command; external state: `GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact enforcement --session-id "$CHANNEL_CERT_RECORD_ID"`; D026 commands are the exact accepted RED-mutant and GREEN-production launch records. | Expected control identity and mutant come from the reviewed frozen procedure. Actual kernel state comes from the external observer and actual denial/canary result. Any write succeeds, policy is liftable, fd 1/2 fails, a capability survives, or the kernel feature cannot be evaluated: STOP/BLOCK. |

### `INFRASTRUCTURE_CROSSOVER_RESULT`

This is a ninth prerequisite, not one of the eight facts. Its only acceptable literal remains:

```text
NO_ROTATION_NO_OUT_OF_STORE_ACTION_NO_SIDE_EFFECT_HOOK
```

The operator must capture two read-only external snapshots around one clean GREEN forced-command session:

```text
GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact crossover --phase pre  --session-id "$CHANNEL_CERT_RECORD_ID"
GATEA_SCOPE=GATEA-STAGING /usr/local/libexec/gatea-attest/v1/channel-observer --expected-vm GATEA-STAGING --fact crossover --phase post --session-id "$CHANNEL_CERT_RECORD_ID"
```

The expected store/rule/hook universe comes from a force-inclusive, root-read authoritative inventory made before the session—not from the post-session directory listing. PASS requires: only enumerated native sshd/PAM/sudo/audit/login stores append; every store keeps the same device/inode; no rotation/vacuum/new sibling occurs; no audit action writes outside its native store; and every PAM/account-shell/sudo hook identity is the accepted non-side-effecting one. A missing backend, unreadable directory, incomplete event interval, changed rule/config hash, extra write, rotation, or hook is STOP/BLOCK. The V2 category split discloses ordinary native records but keeps every crossover category 1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:51-66`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:189-195`

### DHCP address and host-key binding

The later phase obtains the address without consulting KVM2 or the stale record:

```powershell
$VmName = 'GATEA-STAGING'
if ($VmName -cne 'GATEA-STAGING') { throw 'SCOPE_STOP' }
$Vm = @(Get-VM -Name $VmName -ErrorAction Stop)
$Nic = @(Get-VMNetworkAdapter -VMName $VmName -ErrorAction Stop)
if ($Vm.Count -ne 1 -or $Nic.Count -ne 1 -or $Nic[0].SwitchName -cne 'Default Switch') { throw 'VM_OR_NIC_STOP' }
$VmIPv4 = @($Nic[0].IPAddresses | Where-Object { $p=$null; [System.Net.IPAddress]::TryParse($_,[ref]$p) -and $p.AddressFamily -eq [System.Net.Sockets.AddressFamily]::InterNetwork -and -not [System.Net.IPAddress]::IsLoopback($p) })
if ($VmIPv4.Count -ne 1) { throw 'DHCP_IDENTITY_STOP' }
$VmIp = $VmIPv4[0]
```

The exact address has no predeclared value. Its independent constraints are: it is reported for the sole NIC of exact `GATEA-STAGING`; that NIC is on Default Switch; the address lies in the host's current Default-Switch prefix; after a bounded port-22 reachability probe, the Windows neighbor entry for `$VmIp` has the GATEA NIC's exact MAC; and the SSH host key matches the prior pin. Failure of any constraint is STOP. The address is never copied from `172.24.55.233`.

Before authentication, resolve the old alias in the existing public `known_hosts`, scan the new endpoint's public host key, compare algorithm+key/fingerprint sets in memory, and persist neither key text nor a new entry:

```powershell
$VmName = 'GATEA-STAGING'
$KnownHosts = "C:\HyperV\$VmName\ssh\known_hosts"
$OldHostKeyAlias = '172.24.55.233'
& "$env:WINDIR\System32\OpenSSH\ssh-keygen.exe" -F $OldHostKeyAlias -f $KnownHosts *> $null
if ($LASTEXITCODE -ne 0) { throw 'KNOWN_HOST_ALIAS_STOP' }
# The accepted verifier then compares the in-memory output of ssh-keygen -F with
# ssh-keyscan -T 5 -p 22 $VmIp by exact algorithm+public-key bytes; it emits only a verdict/fingerprint.
```

The authenticated OpenSSH call must still enforce the pin independently:

```text
-F NUL
-o BatchMode=yes
-o IdentitiesOnly=yes
-o PasswordAuthentication=no
-o KbdInteractiveAuthentication=no
-o StrictHostKeyChecking=yes
-o UserKnownHostsFile=C:\HyperV\GATEA-STAGING\ssh\known_hosts
-o GlobalKnownHostsFile=NUL
-o HostKeyAlias=172.24.55.233
-o CheckHostIP=no
-o UpdateHostKeys=no
-o ForwardAgent=no
-o ClearAllForwardings=yes
-o RequestTTY=no
-o PermitLocalCommand=no
-o EscapeChar=none
```

`CheckHostIP=no` does not weaken the key pin here: the deliberately stable old alias supplies the expected host key while the DHCP destination changes. `StrictHostKeyChecking=yes` makes mismatch or absence fatal. `accept-new`, `no`, an updated `known_hosts`, or accepting `ssh-keyscan` output without comparison is forbidden.

## 4. Preconditions before the first connection

These checks occur only in the later authorized phase, after checkpoint creation and VM start. Each command is read-only. Every inability is STOP.

| Precondition | Exact read-only command | PASS source and STOP condition |
|---|---|---|
| Exact VM object; never sibling | `$VmName='GATEA-STAGING'; $v=@(Get-VM -Name $VmName -ErrorAction Stop); if($v.Count -ne 1 -or $v[0].Name -cne 'GATEA-STAGING' -or $v[0].Generation -ne 2){throw 'VM_IDENTITY_STOP'}` | Expected name/generation is the verified local fact. Zero/multiple objects, other name, wrong generation, or read failure stops. The command never enumerates all VMs. |
| Pre-change checkpoint exists outside guest | `$VmName='GATEA-STAGING'; $cp=@(Get-VMSnapshot -VMName $VmName -Name 'GATEA-STAGING-CH1-PRECHANGE-V1' -ErrorAction Stop); if($cp.Count -ne 1){throw 'CHECKPOINT_STOP'}` | Expected name comes from this accepted plan and its separately recorded Hyper-V checkpoint ID. Missing/duplicate/wrong-parent/unreadable checkpoint stops. |
| Exact key path exists, metadata only | `$VmName='GATEA-STAGING'; $p="C:\HyperV\$VmName\ssh\gatea_ed25519"; if(-not (Test-Path -LiteralPath $p -PathType Leaf)){throw 'IDENTITY_PATH_STOP'}` | Expected literal comes from the verified local fact/operator record. No hash/content/public derivation is permitted. Missing, directory, or reparse ambiguity stops. |
| New address belongs to exact VM | Run the DHCP block in §3, then compare current Default-Switch prefix and exact GATEA NIC MAC to the exact neighbor row for `$VmIp`. | Independent sources are the exact VM NIC, host switch prefix, DHCP/integration report, and Windows neighbor table. Any disagreement/ambiguity stops. |
| VM reachable on SSH port | `$VmName='GATEA-STAGING'; if($VmName -cne 'GATEA-STAGING'){throw 'SCOPE_STOP'}; if(-not (Test-NetConnection -ComputerName $VmIp -Port 22 -InformationLevel Quiet)){throw 'REACHABILITY_STOP'}` | Expected endpoint is the address already bound to the exact GATEA NIC. False, timeout, or error stops. A reachable port alone is not host identity. |
| Existing `known_hosts` entry resolves | Run the exact `ssh-keygen -F 172.24.55.233 -f C:\HyperV\GATEA-STAGING\ssh\known_hosts` suppressed-output command in §3. | Expected pin is the pre-existing file/old alias. No match, conflicting normalized keys, unreadability, or resolver failure stops. |
| New endpoint presents the pinned host key | Run the accepted in-memory `ssh-keyscan` versus `ssh-keygen -F` comparison, followed by actual OpenSSH with `HostKeyAlias` and strict checking. | Expected key is pre-existing; observed key is new endpoint. Empty scan, no exact match, algorithm ambiguity, or SSH strict-check failure stops before any command is accepted. |

No precondition may be replaced with `Get-VM` without `-Name`, an all-adapter VM query, an ARP sweep, subnet scan, `accept-new`, or a connection to the sibling VM.

## 5. Ordered later execution outline — not run here

1. **[HOST-LOCAL][READ-ONLY] Scope gate.** Resolve only `Get-VM -Name 'GATEA-STAGING'`; require exact Generation 2, Off state, 4 vCPU, and sole NIC on Default Switch. If another target would be needed, mark it **FORBIDDEN** and stop. Expected facts: `C:\tmp\lane_kick\CH1.md:26-29,43-47`.

2. **[HOST-LOCAL][CONFIG] Enable checkpoints while Off.** Run only `Set-VM -Name 'GATEA-STAGING' -CheckpointType Standard`. Change: GATEA's Hyper-V `CheckpointType`, `Disabled` → `Standard`. Justification: an Off-VM Standard checkpoint is wholly outside the guest and does not depend on guest VSS/processes. Revert: after all evidence/rollback needs are closed and the checkpoint is intentionally disposed under later authority, run `Set-VM -Name 'GATEA-STAGING' -CheckpointType Disabled`; until then do not disable it.

3. **[HOST-LOCAL][CONFIG][VERIFICATION] Take checkpoint.** Require no existing checkpoint with the predeclared name, then run `Checkpoint-VM -Name 'GATEA-STAGING' -SnapshotName 'GATEA-STAGING-CH1-PRECHANGE-V1'`; read back exact name, ID, parent, creation time, and VM ID with `Get-VMSnapshot -VMName 'GATEA-STAGING' -Name 'GATEA-STAGING-CH1-PRECHANGE-V1'`. Change: one Hyper-V checkpoint for GATEA only. Revert/rollback: `Restore-VMSnapshot` is reserved for failed/unsafe execution; do not restore or delete automatically. Any later removal must name this exact GATEA checkpoint. The checkpoint covers all later guest configuration changes, not the Hyper-V `CheckpointType` change itself.

4. **[HOST-LOCAL][CONFIG] Start exact VM.** `Start-VM -Name 'GATEA-STAGING'`; then read `Get-VM -Name 'GATEA-STAGING'` and require Running. Change: power state only. Revert: final exact `Stop-VM -Name 'GATEA-STAGING'`, with Off read-back. No sibling enumeration.

5. **[HOST-LOCAL][READ-ONLY][VERIFICATION] Discover DHCP address.** Run the exact GATEA-only block in §3. Compare current Default-Switch prefix and the exact GATEA NIC MAC/neighbor row. Record the new address as an observation, never as a carry-forward of `172.24.55.233`.

6. **[HOST-LOCAL][READ-ONLY][VERIFICATION] Resolve and verify host key.** Resolve old alias `172.24.55.233` from `C:\HyperV\GATEA-STAGING\ssh\known_hosts`, scan only `$VmIp`:22, compare public host-key identity in memory, then require actual OpenSSH strict checking with `HostKeyAlias=172.24.55.233`. Do not print/persist key text, update `known_hosts`, or accept a new key.

7. **[READ-ONLY][VERIFICATION] Connect through existing ordinary `gatea` route for baseline only.** Use exact pinned OpenSSH options and `-i C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519` to run the reviewed baseline observer through `gatea@$VmIp`. The private key is consumed internally by OpenSSH only; no inspection command is run. This connection does not establish root or the final channel.

8. **[READ-ONLY][VERIFICATION] Observe the five category-(b) baseline facts.** Capture current `gatea` account shell, effective forced-command status, pre-`env` name universe without secret values, initial cwd, and complete FD mapping. Compare them to the existing ordinary-route contract only. If a fact is inaccessible it remains `UNKNOWN` and execution stops before overwriting relevant configuration. Baseline values are revert inputs, not privileged-channel proof.

9. **[HOST-LOCAL][CONFIG] Establish a GATEA-only recovery/root console.** Use `vmconnect.exe localhost GATEA-STAGING`; enter the VM's local recovery/root path without persistent weakening. If root requires a new credential, another key, another VM, offline broad-disk modification, Secure Boot weakening, or any excluded action, stop. Change: none if the recovery selection is temporary; any boot-entry edit is forbidden.

10. **[CONFIG] Install the accepted channel package under GATEA root.** Exact guest changes:

   - create locked `gatea-attest` and `gatea-capture` accounts with deterministic recorded numeric IDs, no home directories, no passwords, and no supplementary groups;
   - install root-owned, non-symlink, non-group/other-writable exact artifacts under `/usr/local/libexec/gatea-attest/v1/`: `attest-login`, `attest-root`, `channel-observer`, and `channel-attestation.py`;
   - add the exact `attest-login` path as `gatea-attest`'s account shell and, only if the effective PAM stack requires it, add that one exact path to `/etc/shells`;
   - install `/etc/sudoers.d/gatea-attest` granting only `gatea-attest` → root execution of `/usr/local/libexec/gatea-attest/v1/attest-root` with no arguments, `NOPASSWD`, no `SETENV`, fixed environment, and no other command;
   - install `/etc/ssh/sshd_config.d/90-gatea-attest.conf` with publickey-only authentication, the exact `ForceCommand`, no password/keyboard-interactive/PTY/forwarding/agent/X11/user-rc/environment extension, and the exact root-owned authorized-key object path;
   - reuse the already effective server-side public authorized-key object without reading, printing, copying, replacing, or rotating its contents. Prefer a same-inode root-owned link proven by device+inode metadata; if the filesystem/configuration cannot provide that safely, STOP—do not generate or copy a key;
   - create one dedicated canary object and exact baseline bytes solely for D026 under `/var/lib/gatea-attest-test/`; it must be writable by `gatea-capture` without `GATEA_RO_V1`, so DAC cannot make GREEN self-confirming;
   - validate full config with the accepted parser, `visudo -c`, exact file census/hashes, and complete `sshd -T -C` before any daemon reload; only then reload sshd and keep the recovery/root console open until the new path is proved.

   Revert: the Hyper-V checkpoint covers all guest changes. The granular revert manifest must also restore the exact observed account/passwd/group/shadow/shell and sshd/sudoers/authorized-key inode metadata, remove only the two new accounts and exact listed files/canary, validate sshd/sudoers, and reload sshd. No glob, recursive deletion, or inferred path is permitted.

11. **[READ-ONLY][VERIFICATION] Verify the eight facts and crossover pre-snapshot.** Run the exact observer commands in §3 from the recovery/root observer. Hash/read-back compares to Commit-1a expectations; same-producer agreement is not enough. Any `UNKNOWN`, unexpected config member, extra hook, missing backend, or parser inability stops.

12. **[READ-ONLY][VERIFICATION] Drop through the actual constrained route.** Connect as `gatea-attest@$VmIp` with no remote command. The actual chain must reach `gatea-capture`, not remain root. The external observer checks mount view, UID/GID, groups, capabilities, `NoNewPrivs`, Landlock/syscall state, cwd, environment, parent chain, and descriptors while the fixed script pauses at the accepted observation barrier.

13. **[READ-ONLY][VERIFICATION] Run the channel attestation capture.** Release the barrier and capture exact stdout, stderr, and rc on the Windows side. The guest script writes only fd 1/2; no target evidence file is created. This is channel-certification evidence under the host-channel authorization, not the one-shot grant-#6 ATT-01 record and not a Gate-A result.

14. **[CONFIG][VERIFICATION] Execute D026 RED/GREEN.** RED is the root-console-only, exact-hash mutant and touches only the predeclared canary; it is explicitly not a read-only operation. Reset the canary to its independently frozen baseline under root. GREEN uses the exact real SSH/forced-command/production-wrapper path. Require denied mutation plus usable fd 1/2, unchanged GREEN canary identity/bytes, and no extra FD. If RED/GREEN cannot both be executed exactly, the regression evidence is supplemental and the channel is not accepted. The checkpoint covers the controlled RED mutation.

15. **[READ-ONLY][VERIFICATION] Complete crossover post-snapshot.** Compare the force-inclusive pre/post native-store and hook inventories. Emit `INFRASTRUCTURE_CROSSOVER_RESULT=NO_ROTATION_NO_OUT_OF_STORE_ACTION_NO_SIDE_EFFECT_HOOK` only if the predicate in §3 is fully evaluable and passes. Ordinary bounded native appends are disclosed, not called absent.

16. **[HOST-LOCAL][CONFIG][VERIFICATION] Seal evidence outside the VM.** Before the socket opens, preallocate one exact local record path with create-new semantics. After closure, write the exact checkpoint ID, VM ID, DHCP/MAC binding, host-key match verdict/fingerprint, configuration/artifact hashes, all eight facts, crossover evidence identities, RED/GREEN commands/rc/stdout/stderr, and the capture streams; flush, close, reopen read-only, recount bytes, and rehash independently. Change: one exact operator-side evidence record only. Revert: never overwrite/delete it; an incomplete record gets terminal STOP and remains preserved.

17. **[HOST-LOCAL][CONFIG][VERIFICATION] Stop exact VM.** Close sessions, then `Stop-VM -Name 'GATEA-STAGING'`; require `Get-VM -Name 'GATEA-STAGING'` reports Off. Preserve the checkpoint and evidence. Do not restore/delete the checkpoint or disable checkpoints until the later acceptance/rollback decision.

No step targets anything outside `GATEA-STAGING`. Such a step would be **FORBIDDEN** and absent rather than conditionally allowed.

## 6. How this feeds the Option-A two-commit chain

The owner selected Option A, but the reviewed V1 two-commit design is not accepted: its flagship verdict is `REQUEST_CHANGES` with six required findings. This recommendation must not relabel it accepted. `MTC_COMMAND_CENTER/11_TRIAGE/OWNER_DECISIONS_2026-08-16_MORNING.md:28-38`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/TWO_COMMIT_CHAIN_CLAUDE_REVIEW_2026-08-16.md:1-15,151-153`

The correct integration is a separately authorized host-channel node, **H-C**, after verified Commit 1a and before Commit 1b input join. This directly answers review REQ-1, which found that K26/K27 required a privileged host action for which the V1 chain had no edge. H-C has its own exact authority binding (the owner host-channel authorization plus the accepted design hash), checkpoint/safe-close contract, GATEA-only scope, and evidence record. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/TWO_COMMIT_CHAIN_CLAUDE_REVIEW_2026-08-16.md:34-46`

Recommended order:

```text
Commit 1a verified
  -> H-C configure/certify privileged channel under its own authority
  -> fresh separately authorized Gate-A A-0..A-9 and sealed final record
  -> local Step 9 join of candidate record + H-C root-channel evidence
  -> Commit 1b verified
  -> grant #6 bound only to exact 1b
  -> final ATT-01 through the still-configured certified channel
```

If operational constraints require Gate-A before H-C, that is permissible only if H-C never restarts or touches the Bridge/service and an independent post-H-C recheck proves every perishable candidate field still equals the fresh Gate-A record immediately before Commit 1b and again before ATT-01. Any drift is STOP and the stale record cannot be repaired. H-C is never silently folded into Gate-A authority.

| Destination | What lands there | What must not land there |
|---|---|---|
| **Commit 1a** | Accepted category-(c) choices; exact fixed paths; account/forced-command/wrapper/control schemas; exact config templates; exact source bytes and hashes of `attest-login`, `attest-root`, observer, capture script, and D026 mutant specification; checkpoint requirement; expected environment/cwd/FD/mount/UID/capability grammars; host-key-alias policy; force-inclusive store/hook inventory procedure; H-C authority/safe-close binding fields. | No DHCP address, observed UID/GID, runtime environment, cwd/FD result, live config hash, crossover verdict, MainPID, start time, active/restart state, or other live final observation. Option A keeps live values out of 1a. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_TWO_COMMIT_CHAIN_DESIGN_V1_2026-08-16.md:16-24,120-148` |
| **H-C sealed channel record** | Exact checkpoint/VM/NIC/address/host-key binding; server-side identity mapping; numeric account hops; shell/forced-command/sudo/process chain; pre-environment/cwd/FD observations; installed blob/config identities; mount/Landlock/drop state; D026 RED/GREEN; category-2 native-record disclosure; crossover evidence and literal result; safe close/Off state. | No candidate/Gate-A PASS, no grant-#6 binding, no WP-I authority, and no statement that a checkpoint proves no mutation. |
| **Fresh Gate-A final record** | Only the fresh candidate-bound A-0..A-9 and final candidate/service/process fields required by the accepted Gate-A contract, plus its own authority/use/path identity. | H-C facts are not sourced from the Gate-A producer and Gate-A authority is not broadened to configure/prove this channel. Candidate binding remains solely from the fresh record. The V1 design's intended separation is at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_TWO_COMMIT_CHAIN_DESIGN_V1_2026-08-16.md:162-180,197-217`. |
| **Commit 1b** | Concrete `STAGE1_ROOT_CHANNEL_BINDING.tsv` fields derived from the sealed H-C record and independent checks: `SSH_TARGET`, key binding, numeric identities, shell/forced-command/wrapper/process chain, pre/post environment, initial cwd, stdin/FD mapping, exact remote/outer route, `TARGET_MUTATION_DENIAL_CONTROL`, and `INFRASTRUCTURE_CROSSOVER_RESULT`; concrete candidate row only from the fresh Gate-A record; operator tool digests measured at 1b/use time. | No value accepted merely because the 1b builder and recorder repeat it. No procedure byte changes. Operator-tool digests should not be frozen in 1a; the review requires paths in 1a and fresh digests in 1b/use-time checks. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/TWO_COMMIT_CHAIN_CLAUDE_REVIEW_2026-08-16.md:96-106` |

This channel recommendation closes only the architectural subject of REQ-1 by defining H-C. It does not silently close review REQ-2 through REQ-6. The repaired chain still has to add independent checks for volatile candidate fields; bind outer argv parameters to committed rows; derive one immutable 1b OID without later `HEAD`; predeclare the Gate-A record path/use ordinal; and keep volatile operator-tool digests out of 1a. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/TWO_COMMIT_CHAIN_CLAUDE_REVIEW_2026-08-16.md:48-106,137-147`

## 7. Check inventory

“Independent” below means independent of the producer being checked, not a second human. Every command/procedure records rc, stdout, stderr, exact input identities, and first divergence. Unreadable or unevaluable input is STOP.

| ID | Check | Expected-value source | Independent of producer? | What makes it fail/stop |
|---|---|---|---|---|
| CH1-K01 | Exact Hyper-V VM identity/scope | Verified local facts and accepted GATEA-only scope | Yes—host VM configuration is outside guest | Missing/multiple/wrong VM, generation/NIC/switch mismatch, all-VM query, or inability → STOP. |
| CH1-K02 | Pre-change checkpoint | Accepted exact name plus Hyper-V read-back/ID | Yes—outside guest/capture | Missing/duplicate/wrong VM/parent/ID, created after guest change, or unreadability → STOP. |
| CH1-K03 | Identity-path existence without content access | Recorded literal path | Yes relative to path check | Missing/non-file/reparse ambiguity, or any attempted content/hash/public derivation → STOP. This does not prove which key it contains. |
| CH1-K04 | DHCP endpoint belongs to GATEA | Exact GATEA NIC/VM ID, current switch prefix, NIC MAC and neighbor table | Yes relative to DHCP/IP producer | Zero/multiple IPs, stale subnet, MAC mismatch, unreachable port, or ambiguity → STOP. |
| CH1-K05 | Host key at new address | Pre-existing `known_hosts` entry under stable old alias | Yes—expectation predates DHCP/scan | No resolvable pin, scan mismatch, strict SSH mismatch, conflicting keys, or blind-accept option → STOP. |
| CH1-K06 | Pinned key maps to selected principal/route | Owner-selected principal, effective sshd config, same server-side authorized-key object identity, and client/server accepted fingerprint records | Yes relative to capture script | Other principal/route/auth method, object mismatch, key-content handling, or inability to bind fingerprint → STOP. |
| CH1-K07 | Account shell/numeric identity | Commit-1a manifest plus account-creation record | Yes relative to account observer | Wrong/duplicate UID:GID, shell path/hash/kind/owner/mode mismatch, unlocked password/home/supplementary group, or unreadability → STOP. |
| CH1-K08 | Forced command and no interactive alternatives | Accepted config manifest and full effective sshd/sudo/account parse | Yes relative to SSH caller | Different/ambiguous command, accepted original command, forwarding/PTY/user-rc/env path enabled, broad sudo, or incomplete parse → STOP. |
| CH1-K09 | Complete executed wrapper chain | Commit-1a ordered hop/hash/UID list | Yes; actual chain comes from external `/proc` observer | Missing/extra hop, PATH lookup, hash or UID mismatch, wrong namespace, or race/inability → STOP. |
| CH1-K10 | Pre-environment | Commit-1a name/value-derivation universe plus independently observed connection/account fields | Yes; actual is entry process + external observer | Unexpected/missing entry, secret-bearing value, loader/shell/Python hook, encoding mismatch, disagreement, or unreadability → STOP. |
| CH1-K11 | Initial cwd | Accepted literal `/` plus account-home/entry contract | Yes relative to runtime producer | Actual not `/`, symlink/namespace ambiguity, disagreement with external `/proc`, or inability → STOP. |
| CH1-K12 | Complete FD mapping | Accepted exact 0/1/2 contract | Yes relative to capture output | Extra FD, wrong access/target, writable target beyond 1/2, enumeration incomplete, or stream mismatch → STOP. |
| CH1-K13 | Read-only mount and irreversible privilege state | Commit-1a kernel-policy contract | Yes; state externally observed | Any visible writable mount, Landlock/filter absent, `NoNewPrivs!=1`, group/capability/root ID survives, control can be lifted, or feature unknown → STOP/BLOCK. |
| CH1-K14 | D026 category-1 denial and fd usability | Frozen production/mutant hashes, independent canary baseline, exact matrix and stream markers | Yes | RED cannot write, GREEN can write, canary changes in GREEN, fd1/fd2 marker missing, other FD exists, or real top-level path not run → STOP/BLOCK. |
| CH1-K15 | Infrastructure crossover | Pre-session force-inclusive native-store/rule/hook universe and external pre/post snapshots | Yes relative to capture | Rotation/vacuum/new sibling, out-of-store write, side-effect hook, changed config/rule, incomplete interval, or unreadability → STOP/BLOCK. |
| CH1-K16 | Category-2 disclosure precision | V2's accepted category split and actual native-store inventory | Yes relative to capture claim | A native append is claimed absent, or a crossover is mislabeled as disclosure → STOP. |
| CH1-K17 | Evidence create-once/close/identity | Preallocated Windows path, OS create-new result, expected field universe, independent post-close re-read | Yes for closed-byte identity; **No** for truth of producer-supplied facts | Collision/overwrite, incomplete stream/rc, flush/close/reopen/hash mismatch, missing field, or producer hash used as correctness proof → STOP/quarantine. |
| CH1-K18 | Candidate stability across H-C if H-C follows Gate-A | Fresh Gate-A raw evidence and independent immediate re-observation | Yes relative to H-C | PID/starttime/state/restart/exe/ns/cwd/cmdline drift or inability → STOP; never edit the fresh record. |
| CH1-K19 | Final Off state and checkpoint preservation | Accepted phase plan plus Hyper-V state/checkpoint read-back | Yes—outside guest | VM not Off, checkpoint missing/changed, wrong VM, or inability → STOP/quarantine. |
| CH1-K20 | Scope conservation | Owner fence and force-inclusive command/evidence target inventory | Yes relative to individual commands | Any Hostinger/KVM2/production/broker/ARM/order/trading/master target, wildcard VM action, unenumerated host, or unexplained member → FORBIDDEN/STOP. |

No PASS token, self-produced hash, same-process environment echo, source-code scan, or checkpoint existence substitutes for the checks above. The binding record cannot pass merely because its launcher and recorder agree. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:197-214`

## 8. Honest residuals for the owner

1. One person still configures, runs, and certifies the design. The mechanisms constrain the capture process; they do not make the Windows administrator independent of themselves.
2. The Hyper-V checkpoint permits rollback and is unreachable from inside the VM, but it neither prevents writes nor proves that no write occurred. The Windows operator can still delete it.
3. Reachability, the current DHCP address, server-side key mapping, UID/GID allocation, exact shell/wrapper hashes, kernel support, native auth/audit stores, PAM stack, and crossover result are all `UNKNOWN` until the later phase observes them. Any one may block execution.
4. Recovery-console root capability is authorized but not established. If Ubuntu recovery, encryption, Secure Boot, or another control prevents a bounded GATEA-only root console, the design stops; it does not exploit sudo or weaken the host.
5. Reusing the server-side authorized-key object without exposing/copying key contents may be infeasible across filesystems or effective sshd policy. That is a hard STOP; the design does not create a replacement key.
6. Native sshd, PAM, sudo, audit, journal, and login-accounting records will normally change. Those bounded category-2 records are disclosed. Only a complete no-crossover result makes them non-blocking.
7. `GATEA_RO_V1` constrains the capture process, not pre-enforcement sshd/PAM/sudo. Exact configuration, external observation, and crossover checks are still required for those earlier processes.
8. The deliberate RED arm writes a dedicated canary. It is a separately authorized controlled configuration test, not evidence that the capture is intrinsically read-only. The checkpoint and exact canary reset bound that mutation.
9. A successful canary matrix is discriminating evidence for the enforcement mechanism, not proof about every possible Linux side effect. The read-only mount universe, Landlock/syscall policy, privilege drop, exact source review, and crossover observation must all pass as separate checks.
10. fd 1/2 remain writable by design. They lead to the SSH channel and operator evidence, not a guest filesystem object; the complete FD check must prove that statement.
11. The local create-once evidence file is not a cryptographic statement from an independent person. It detects ordinary alteration and is outside the VM, but the Windows operator can still replace local evidence with sufficient privilege.
12. The channel does not prove anything about Hostinger, KVM2, production, broker/exchange systems, ARM, orders, TESTNET/mainnet, Pine, parity, MTC, trading, or economic safety; none is contacted or evaluated.
13. Owner selection of Option A is not acceptance of the current V1 chain artifact. This recommendation supplies the missing H-C node for review REQ-1 only. REQ-2 through REQ-6, an integrated repaired runbook, exact executable artifacts, D026 evidence, and required T0 accepting verdicts remain prerequisites before any final Commit 1b or grant-#6 capture.

Final documentary disposition: **DESIGN RECOMMENDATION ONLY; NOT ACCEPTED; NO HOST/VM/NETWORK/SSH/KEY/CONFIGURATION ACTION TAKEN.**
