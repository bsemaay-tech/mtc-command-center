# L9 — KVM2 Phase-1 read-only baseline capture procedure (R29: P1-01 + P1-02)

- Lane: L9, dispatched from `C:\tmp\lane_kick\L9.md` (repo `C:\RO` detached at
  `25564449`, shared read-only; `L9.md:5-12`).
- Date of design: 2026-08-15.
- Status: **DESIGN ONLY. NOT EXECUTED. GRANTS NO HOST AUTHORITY.** This lane ran
  no host, network, SSH, git-write, or sub-agent action (`L9.md:59-60,63-78`).
- Scope: work-breakdown row **R29** — "Complete KVM2 Phase-1 P1-01/P1-02:
  reproduce the hardened-host baseline and issue its redacted manifest"
  (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:68`).
- Task definitions: KVM2-P1-01
  (`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:78-83`)
  and KVM2-P1-02
  (`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:84-87`).

## 0. Authority state this design sits inside

1. **No current grant permits executing this procedure.** The deploy list holds
   P1-01/P1-02/P1-03 "OPEN / BLOCKED until a separately authorized read-only
   host baseline is reproduced, redacted, and owner-accepted"
   (`...BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:25-27`), and the program index
   agrees: "No VPS access was authorized; dated facts were not refreshed"
   (`...KVM2_PROGRAM/INDEX.md:16`). The 2026-08-15 D2 read-only host grant is
   real but unspendable and **explicitly excludes the Hostinger KVM2 production
   server**; it names `GATEA-STAGING`, which "is not KVM2"
   (`...WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-41,54-58,60-61`).
2. Execution therefore requires a **new owner sentence** naming: KVM2; read-only
   baseline capture only; this procedure document's SHA-256; the exact argv
   allowlist (§2); a named operator; the transport credential by logical ID; and
   that it grants no install, secret, cutover, start, or other authority. Task
   definitions "do not authorize later actions; each operational gate needs
   distinct owner authority"
   (`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:10-12`).
3. **P1-03 (accept or reject the baseline) is the owner's, not this lane's**
   (`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:88-90`;
   catalogue row R30, `...DEPLOY_WORK_BREAKDOWN_2026-08-15.md:69`). This
   document produces material for that decision and renders no verdict.
4. **Raw-evidence retention is currently a hard blocker.** The program index
   states the retention owner, duration, deletion trigger, and encrypted-storage
   selection are OPEN owner decisions and "Until all four are recorded, Phase 1
   raw evidence collection is blocked"
   (`...KVM2_PROGRAM/INDEX.md:63-67`). This procedure cannot run before those
   four decisions exist, because its raw stream must land in that store.

## 1. Preconditions and session contract (all before any host contact)

| # | Precondition | Status today | What would settle it |
|---|---|---|---|
| P-1 | Owner authorization sentence (§0.2) | Not given | Owner decision |
| P-2 | Retention quartet recorded (owner, duration, trigger, store) | OPEN — `INDEX.md:63-67` | Owner decisions |
| P-3 | Evidence ledger machinery live and independently verified (P0-04/P0-04A; catalogue R27) | PREPARED LOCALLY, verification OPEN — `INDEX.md:15`; sole ledger row verdict OPEN, verifier "Codex Lead pending" — `...KVM2_PROGRAM/evidence/EVIDENCE_LEDGER.jsonl:1` | Phase-0 close records |
| P-4 | Preregistered **argv allowlist + output grammar** for this capture, committed and hashed before contact (same shape as the house Commit-1 pattern: producer, argv, environment, cwd, output grammar first — `...WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:44-48`) | Not written | This procedure frozen + committed under its own write authorization |
| P-5 | Owner-confirmed **expected privileged-user inventory** and **expected enabled-service/timer inventory** (inputs the P1-01 stop conditions need — §4) | UNKNOWN — no document read supplies them | Owner confirmation, or an explicit owner decision that capture #1 defines the reference inventory |
| P-6 | Transport credential named in the authorization; recorded only by logical ID | UNKNOWN | The P-1 sentence |

Design invariants holding throughout: **zero host-side tooling** (every host
command is stock Ubuntu 24.04; the sanitizer/checker run on the operator
workstation over the captured stream, so nothing is installed, downloaded, or
written on the host); **no interactive root shell** (elevation is per-command
`sudo -n`, which fails rather than prompts, from the fixed allowlist only); and
**no host filesystem writes** (no redirections to host files; all output leaves
through session stdout; host shell history disabled at session start).

## 2. Ordered capture procedure

Conventions: run in one SSH session as a non-root account; each line below is
executed verbatim as one entry of the preregistered argv allowlist (P-4); every
command's raw stdout/stderr and exit code are captured on the workstation.
`sanitize` = the preregistered workstation-side filter (§3), never a hand edit.

### S0 — Session envelope

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 0.1 | `HISTFILE=/dev/null; set +o history` | Session-local shell settings only; with `HISTFILE` pointing at `/dev/null`, bash writes no history file at exit | No command line — including the connection command — persists in host shell history |
| 0.2 | `date -u +%Y-%m-%dT%H:%M:%SZ` | Reads the clock | Capture-open timestamp (P1-02 requires it) |
| 0.3 | Probe set **P**, first run (S1, S3, S5, S6-enabled-only, S7, S8-dpkg, S11-`/opt`) | All members are the read-only commands below | S0 determinism baseline (§5) |

### S1 — OS, kernel, time sync

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 1.1 | `cat /etc/os-release` | File read | Distribution and version — snapshot claim C1 (Ubuntu 24.04) |
| 1.2 | `hostnamectl` | Status print via `systemd-hostnamed`; changes require explicit `set-*` verbs, none given | OS/virtualization facts; hostname field is reduced to a redaction marker by `sanitize` |
| 1.3 | `uname -srm` | Kernel info syscall; and `‑srm` is chosen over `‑a` precisely because it emits no hostname | Kernel release and arch (P1-01 "kernel") without emitting an identifier |
| 1.4 | `timedatectl` | Status print via `timedated`; no `set-ntp`/`set-time` verb used | NTP active and clock synchronized — claim C7 |

### S2 — SSH policy (elevated reads)

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 2.1 | `sudo -n sshd -T` | Extended **test mode**: parses configuration and prints the effective values, then exits — binds no port, spawns no daemon, does not reload or signal the running `sshd`, writes nothing. Root needed only to read root-only config/key files | Effective `passwordauthentication no`, `pubkeyauthentication yes`, `permitrootlogin no`, `kbdinteractiveauthentication no` — claim C3 ("Key-only SSH; root SSH disabled"). Note: the raw dump contains `hostkey` **paths**; the grammar (§3 L3) keeps only the five auth-policy fields, so no credential path can reach the manifest |

### S3 — Firewall (elevated read)

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 3.1 | `sudo -n ufw status verbose` | Query only — prints default policies and rules; `enable/disable/reload/default/rule` verbs are absent from the allowlist and not run | Default-deny incoming with only `22/tcp` ALLOW — claim C4; any additional allow rule is a manifest finding |

### S4 — Fail2ban and automatic updates

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 4.1 | `systemctl is-active fail2ban; systemctl is-enabled fail2ban` | Read-only manager queries; no `start/stop/reload/daemon-reload` verb present | Fail2ban present and enabled — claim C5 |
| 4.2 | `sudo -n fail2ban-client status` | One read-only status query over the local control socket; returns the jail list and changes no jail/config | At least the expected jail(s) exist (jail list emitted as names only) |
| 4.3 | `systemctl is-active unattended-upgrades; cat /etc/apt/apt.conf.d/20auto-upgrades` | Manager query + file read | `APT::Periodic::Unattended-Upgrade "1"` and an active unit — claim C6 |

### S5 — Listening sockets (elevated read)

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 5.1 | `sudo -n ss -tulpn` | Reads kernel socket tables over netlink; no socket is created, closed, or reconfigured | Full listening inventory — P1-01 "listening sockets"; no public non-SSH listener (stop check T1); no listener on 8790 in any form (crosswalk item 7 keeps 8790 loopback-only with UFW SSH-only — `...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:258`). `-l` lists listening sockets only, so the operator's own established SSH session is structurally absent from the output |

### S6 — Services and schedules

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 6.1 | `systemctl list-unit-files --type=service --state=enabled --no-pager` | Read-only enumeration of unit-file enablement state | Enabled-service inventory (P1-01 "enabled services") |
| 6.2 | `systemctl list-units --type=service --state=running --no-pager` | Read-only enumeration of the manager's current state | Running-service inventory (context for T4) |
| 6.3 | `systemctl list-timers --all --no-pager` | Read-only enumeration | Timer inventory — stop check T4 ("unexplained scheduled service") |

### S7 — Users and privilege (elevated reads)

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 7.1 | `getent passwd` | NSS query | Full account inventory (P1-01 "users"); raw external-only; grammar emits `{uid, gid, shell-class, home-present}` with names as `acct#n` |
| 7.2 | `awk -F: '$3==0 {print $1}' /etc/passwd` | File read | Exactly one UID-0 account (root) — input to stop check T3 |
| 7.3 | `getent group sudo admin wheel` | NSS query | Privileged-group membership — input to T3 |
| 7.4 | `sudo -n sh -c 'cat /etc/sudoers /etc/sudoers.d/* 2>/dev/null'` | Reads policy files only; no `visudo` write, no policy change | Sudo grant lines — input to T3 (grants outside the owner-confirmed set) |
| 7.5 | `sudo -n find /root /home -maxdepth 3 -name authorized_keys -printf '%m\n'` | Enumeration read; `-printf '%m\n'` prints **file modes only** — by construction no path and no key material is emitted | At least one authorized key exists, so key-only login is operationally configured, without emitting a credential path or value |

### S8 — Packages and toolchain

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 8.1 | `dpkg-query -W -f='${Package}\t${Version}\n'` | Reads the dpkg status database | Installed-package inventory (P1-01 "packages") |
| 8.2 | `python3 --version; git --version` | Version prints; no repo or interpreter state touched | Claims C10, C11 |
| 8.3 | `for c in pip pip3 docker; do command -v "$c" >/dev/null 2>&1 && printf '%s PRESENT\n' "$c" || printf '%s ABSENT\n' "$c"; done` | PATH lookup only | pip and Docker absent from PATH — claim C12 |
| 8.4 | `dpkg-query -W -f='${Package}\n' \| grep -E '^(docker\|containerd\|runc\|podman)' \|\| echo NO-CONTAINER-PACKAGES` | Reads dpkg database; grep is local | Container stack absent at the package layer — C12 (belt to 8.3's braces) |
| 8.5 | `systemctl list-unit-files 'mtc-bridge*' --no-pager; test ! -e /etc/mtc-bridge && echo /etc/mtc-bridge ABSENT; test ! -e /opt/mtc-bridge && echo /opt/mtc-bridge ABSENT` | Manager enumeration + existence tests (`test` writes nothing); the two paths are canonical role paths already published in repo deploy docs, not private identifiers | Bridge application absent — claim C13 |

### S9 — Pending security updates

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 9.1 | `apt-get -s dist-upgrade` | **Simulation mode**: computes and prints the would-be transaction — no download, no install, no lock write, no list refresh. `apt update`/`apt-get update` are explicitly **not on the allowlist** because they mutate `/var/lib/apt/lists` | Pending-update inventory; entries from `-security` suites satisfy P1-01 "pending security updates". Recorded scoping: the list is relative to the package cache as it exists at capture time; claim C6 is proven by configuration (4.3), not by this count |

### S10 — Disk, memory, swap

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 10.1 | `df -h /` | procfs/statfs read | Root filesystem size class — claim C8 (96G) |
| 10.2 | `free -h` | procfs read | RAM total — claim C9 (7.8 GiB) |
| 10.3 | `swapon --show` | Display-only invocation (no device argument, so it swaps nothing on or off) | Swap presence/size (P1-01 "swap") |

### S11 — `/opt` and close-out

| # | Command | Why it cannot mutate the host | What it proves |
|---|---|---|---|
| 11.1 | `ls -A /opt` | Directory read; empty output is itself the finding | `/opt` empty — claim C14 |
| 11.2 | Probe set **P**, second run | Same read-only commands | S0/S1 equality — non-mutation evidence (§5) |
| 11.3 | `date -u +%Y-%m-%dT%H:%M:%SZ` | Clock read | Capture-close timestamp |

## 3. Redaction architecture — structural, not a reminder

The deploy list is explicit that no public IP, credential, private-key path,
secret value, or connection command may appear in a committed document
(`...BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:22-23`), and P1-02 adds
usernames and credential paths to the forbidden set with the stop condition
"redaction cannot be proven"
(`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:85-87`). This design
enforces that mechanically, in six layers.

**L1 — Two-artifact split (binds to the existing P0-04 machinery).** Raw output
never enters the repo or chat; it is encrypted in the owner-selected external
store and referenced only by a `RAW-...` logical ID; only the sanitized manifest
is committed under the frozen program root
(`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:48-52`;
`...KVM2_PROGRAM/INDEX.md:57-62`). The committed artifact path follows the
frozen layout `evidence/sanitized/` — creating any file there is a repo write
needing its own authorization, per the P0-04A separate-write-authorization
pattern (`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:56-57`).

**L2 — Generation, not editing.** The sanitizer is a versioned script whose
SHA-256 is committed in the P-4 preregistration *before* contact. It runs on the
workstation over the raw stream; the manifest bytes are machine-generated and
hash-chained per section. A hand edit breaks the checker's recomputation, so
"redaction by after-the-fact editing" is structurally impossible.

**L3 — Default-deny field grammar.** For each section, only named fields
survive; everything else in the raw output is dropped. Address fields are
parsed and reduced to class labels `{loopback, link-local, private, public,
wildcard}` — **a literal address can never appear because no literal is ever
emitted**. Usernames become role labels (`root`, `acct#n`, `service-nologin`);
hostname fields become `<hostname-redacted>`; `hostkey` lines from 2.1 are not
in any allowlist, so no key path exists in the grammar; the transport appears
only as a logical ID, so no connection string exists in the grammar.

**L4 — Fail-closed residual scan, as a superset of the existing validator.**
The ledger validator already rejects IPv4 literals, Windows paths, `/home|/users|/root`
paths, credential-shaped values, and `ssh://`-style connection details
(`...KVM2_PROGRAM/evidence/validate_ledger.py:35-45,64-76`), and the manifest is
run through it via the canonical command
(`...KVM2_PROGRAM/INDEX.md:69-73`). But that denylist is **narrower than P1-02
requires** and must not be the only gate: it has no IPv6 literal pattern, and
its hostname pattern matches only `.local|.internal|.lan|.example|.invalid|.test`
suffixes — a provider FQDN would pass
(`...validate_ledger.py:38-41`). The manifest checker therefore extends the
same families with: IPv6 literals, general FQDN/hostname shapes, any
`/root`-prefixed path, address:port composites, and high-entropy tokens above a
committed length. Any hit fails the manifest closed.

**L5 — Canary rejection proof (the "redaction cannot be proven" stop, closed
by demonstration).** Before the sanitizer/checker pair is trusted on real data,
a contaminated fixture manifest — seeded with a canary IPv4, canary IPv6,
canary FQDN, canary `/home/<name>` path, canary key-path line, canary
`-----BEGIN ... PRIVATE KEY-----` block, and canary `ssh://` string — must be
**rejected** (RED), and the sanitized fixture must **pass** (GREEN), with the
commands and their real output recorded in the evidence. This is the D026
discipline — a check is not evidence until it is shown to fail on the defect it
guards (`AGENTS.md:113-121`) — and it extends the P0-04A rejection-test
requirement (private paths, public IPs, hostnames, credentials;
`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:59-63`) from ledger
rows, where fixtures already exist (`...KVM2_PROGRAM/INDEX.md:75-78`), to the
manifest artifact itself.

**L6 — Non-mutation evidence.** Every argv executed is on the committed P-4
allowlist; every rc and sanitized hash is recorded; no argv contains a host
write; and the S0/S1 probe comparison (§5) shows the deterministic surfaces
byte-identical before and after the session. Enforcement is evidentiary — the
design deliberately does **not** propose reconfiguring sudoers or any host
policy to "lock down" the session, because that would itself be a host mutation
outside a read-only grant.

### Manifest content (discharges P1-02's evidence list)

P1-02 requires "timestamp, command list, exit codes, hashes, findings"
(`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:85-86`). The manifest
schema:

```json
{
  "procedure_id": "KVM2-P1-BASELINE",
  "procedure_doc_sha256": "<hash of this frozen procedure>",
  "capture_opened_utc": "...", "capture_closed_utc": "...",
  "operator": "<named per P-1>", "authorization_logical_id": "RAW-...",
  "host_ref": "KVM2 (logical ID only)",
  "transport_ref": "<logical ID only>",
  "commands": [ {"seq": "2.1", "argv": ["sudo","-n","sshd","-T"], "rc": 0,
                 "sanitized_sha256": "...", "raw_logical_id": "RAW-..."} ],
  "findings": [ {"claim": "C3", "verdict": "RE-ESTABLISHED|DIFFERS|UNKNOWN",
                 "measured": "<sanitized field values>", "basis": "seq 2.1"} ],
  "stop_conditions": [ {"id": "T1..T4", "triggered": false, "basis": "seq ..."} ],
  "redaction": { "sanitizer_version": "...", "sanitizer_sha256": "...",
                 "canary_RED": {"logical_id": "RAW-...", "result": "REJECTED"},
                 "canary_GREEN": {"logical_id": "RAW-...", "result": "PASS"},
                 "residual_scan": "PASS", "ledger_validator": "PASS" },
  "determinism": { "probe_set": "P", "s0_sha256": "...", "s1_sha256": "...",
                   "equal": true }
}
```

The ledger row appended for it uses the existing schema: `task_id` KVM2-P1-02,
prerequisites `[KVM2-P1-01]`, `data_classification` `mixed` (publishable
manifest + restricted raw), `artifact_sha256` = manifest hash,
`restricted_raw_evidence_logical_id` = `RAW-...`
(`...KVM2_PROGRAM/evidence/ledger_schema.json:4-18,31,34-35`).

## 4. P1-01 stop conditions, mechanically evaluated

P1-01's stop set is "public non-SSH listener, password/root SSH, unknown
privileged user, or unexplained scheduled service"
(`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:82-83`).

| ID | Stop condition | Mechanical test | Input the test needs |
|---|---|---|---|
| T1 | Public non-SSH listener | From 5.1: any listening socket whose address class ∉ {loopback, wildcard-for-sshd} **or** whose port ∉ {22} while non-loopback → STOP | None beyond 5.1 |
| T2 | Password/root SSH | From 2.1: `passwordauthentication ≠ no` OR `kbdinteractiveauthentication ≠ no` OR `permitrootlogin ≠ no` → STOP | None beyond 2.1 |
| T3 | Unknown privileged user | From 7.2/7.3/7.4: UID-0 count > 1, or any sudo/admin/wheel member or sudoers grantee outside the **owner-confirmed expected set** → STOP | Precondition P-5 (currently UNKNOWN) |
| T4 | Unexplained scheduled service | From 6.1/6.3: any enabled service or timer outside the **owner-confirmed expected inventory** → STOP | Precondition P-5 (currently UNKNOWN) |

Any trigger halts the capture, is recorded as a finding, and goes to the owner
at P1-03; no install follows in any case, since P1-03 gates it
(`...KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:88-90`). T3/T4 are
designed to degrade honestly: without P-5 the manifest records the deltas as
`UNKNOWN — no confirmed expected set` rather than guessing an allowlist.

## 5. Non-mutation proof

Determinism probe set **P** = {8.1 package list, 6.1 enabled unit-files, 7.1
accounts, 7.3 privileged groups, 2.1 filtered sshd fields, 3.1 ufw status, 5.1
listeners, 11.1 `/opt` listing} — chosen because all outputs are stable in a
quiet window (timestamps, counters, and `free` values are excluded). P runs at
0.3 and 11.2; the manifest requires `s0_sha256 == s1_sha256` on the sanitized
bytes. Equal ⇒ the capture changed nothing it observed; unequal ⇒ recorded as a
drift finding with the diff, and P1-03 sees it. This complements, and does not
replace, the by-construction argument of §3 L6.

## 6. What the dated July snapshot would re-establish — and what it is worth

The snapshot is the historical, owner-supplied 2026-07-25 list that was never
refreshed because VPS access was not authorized
(`...BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:10-12`). Executing §2 as of a
capture time *t* would re-establish, at *t* and only at *t*:

| # | Snapshot claim (ibid., lines) | Re-established by |
|---|---|---|
| C1 | "Ubuntu 24.04" (:13) | 1.1 |
| C2 | "hardened" (:13) | Composite label — not a single fact; its measurable content is exactly C3–C6 plus T1–T4. The manifest re-establishes those components and reports the label only as their conjunction |
| C3 | "Key-only SSH; root SSH disabled" (:14) | 2.1 (+7.5 operational key presence) |
| C4 | "UFW default-deny with only SSH port 22 allowed" (:15) | 3.1 |
| C5 | "Fail2ban … enabled" (:16) | 4.1, 4.2 |
| C6 | "automatic security updates … enabled" (:16) | 4.3 (configuration), scoped by 9.1 |
| C7 | "time synchronization enabled" (:16) | 1.4 |
| C8 | "96G disk" (:17) | 10.1 |
| C9 | "7.8 GiB RAM" (:17) | 10.2 |
| C10 | "Python 3.12 … present" (:18) | 8.2 |
| C11 | "git present" (:18) | 8.2 |
| C12 | "pip, Docker … absent" (:19) | 8.3, 8.4 |
| C13 | "the bridge application [is] absent" (:19) | 8.5 |
| C14 | "`/opt` is empty" (:20) | 11.1 |

Measured-vs-snapshot comparisons are recorded as class-level `MATCH`/`DIFFERS`
without an invented drift threshold; materiality is the owner's call at P1-03.
C8–C14 are claims about a machine no one has re-observed for three weeks, and a
single capture is a point-in-time re-verification, not continuous assurance.

**Plain statement required by the lane: the dated July snapshot is not current
evidence of anything.** Its own carrying document says so — "The dated snapshot
is not current deployment evidence"
(`...BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:27`); the program index records
the same (`...KVM2_PROGRAM/INDEX.md:16`); and the 2026-08-15 readiness refresh
classifies every KVM2 fact as UNVERIFIED without authorized current access,
using no snapshot or adjacent fact to fill any gap
(`...BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:353-360,376-377`).

## 7. Estimate — **NO SOURCED ESTIMATE**

R29 remains **NO SOURCED ESTIMATE**, consistent with the catalogue's existing
assignment (`...DEPLOY_WORK_BREAKDOWN_2026-08-15.md:68`).

The one candidate source cannot be reused here: the readiness refresh's
critical-path row 4 prices **2–4 host hours** for a single bundled unit —
"Reproduce current KVM2 baseline; **install the exact SHA; prove Python 3.12
lock install including offline wheelhouse path; verify identity, paths, unit,
UFW, closed port, and masked/unstarted state**"
(`...BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:336-337`). That bundle
spans R29 (baseline) and R37 (install/verification), which is precisely why the
catalogue assigns it to neither row — "assigned to neither, preventing reuse"
(`...DEPLOY_WORK_BREAKDOWN_2026-08-15.md:180-183`). Carving any fraction of
2–4 h out for R29 alone would invent a split no source supplies, and the
standing rule after the refuted estimate is a sourced range or an explicit NO
SOURCED ESTIMATE — never an invented figure (`C:\tmp\lane_kick\L9.md:16-18`).

No other document read by this lane prices a timed read-only KVM2 baseline run.

**What would settle it:** (a) a timed execution of exactly §2 under the §0.2
authorization, recorded as elapsed hands-on operator time — which the catalogue
itself asks for ("obtain a timed read-only baseline run",
`...DEPLOY_WORK_BREAKDOWN_2026-08-15.md:68`); and (b) a scoping decision by the
Lead on whether the one-time local build of the sanitizer/checker/canary
fixtures (§3) is priced inside R29 or inside R27/P0-04A, whose ledger and
rejection-test machinery it extends
(`...DEPLOY_WORK_BREAKDOWN_2026-08-15.md:66`). This lane takes no position:
both timings are absent, and first-run overhead is UNKNOWN.

## 8. Sources read

- `C:\tmp\lane_kick\L9.md` (task specification)
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/INDEX.md`,
  `.../evidence/ledger_schema.json`, `.../evidence/validate_ledger.py`,
  `.../evidence/EVIDENCE_LEDGER.jsonl`
- `AGENTS.md` (D026), `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md` (orientation only)

## 9. Boundary statement

This lane designed the procedure only. It did not run it, did not contact any
host, granted no host authority, rendered no acceptance or gate verdict, and
performed no git write. Its sole output is this file
(`C:\tmp\lane_out\L9_KVM2_PHASE1.md`).
