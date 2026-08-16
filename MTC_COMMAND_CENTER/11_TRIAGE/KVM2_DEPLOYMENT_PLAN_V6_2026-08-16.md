# KVM2 deployment plan V6 (FINAL) — candidate `be007fd8` — 2026-08-16

> **Night repin (owner overnight authorization):** candidate advanced to
> `be007fd8` by the owner-authorized UFW comment-normalization repair after the
> live fail-closed dry-run stop; all pins in §1/§3 are the final ones. §4 below
> is the HISTORICAL round-4 review contract as executed against `acdf4e37`;
> the UFW repair's own closure runs as a confirmation-only pass per the
> overnight authorization.

Status: **PLAN — NOT AUTHORIZED TO EXECUTE. SUPERSEDES V5.** Produced under
the owner's round-4 override (`OWNER_DECISION_ROUND4_FINAL_2026-08-16.md`):
this is the final package of the final round. V6 incorporates V2 §0 (tenancy
model), §2 (bootstrap/upgrade split), §6 (later gates), §8 (upgrade
procedure), V3 §D1–§D4 (dashboard scope/launcher/D3 matrix/Dashboard-V2
queue), V4 §2.1/§2.3–§2.6 and V5 §3 as context and constraints ONLY. **Every
executable command lives in the pinned command annex below; no earlier
version supplies a command.**

## 1. Final pins

| Item | Value |
|---|---|
| **Final candidate** | `be007fd802bbfd2eb181d66038c374865d1562ee` — tip of `integration/bridge-release-20260815` (pushed); lineage `62bf661b` → `be689537` → `a7460784` → `acdf4e37` → `be007fd8` (UFW trailing-comment normalization, owner-authorized after the live fail-closed stop; suite `1381 passed`). Replacement initial-release candidate; KVM2 empty and untouched. |
| Round-4 delta vs `a7460784` | 4 files, +373/−36: complete UFW verb coverage (`ALLOW/LIMIT × IN/FWD`, named profiles fail closed, independent 8790 substring backstop, numeric `22/tcp` SSH requirement), structural D026 fences (statement extraction; unclassified executable heads FAIL), `assert_mode_owner` numeric-owner+kind applied to the root-executed logrotate/cron assets before byte comparison, honest structural-boundary documentation. |
| Candidate test state | `1381 passed, 1 warning` on final bytes (Lead-independent 167.07 s; prior `1376` chain preserved in history). All round-3 mutations RED / final bytes GREEN (`RIC3_REPAIR_REPORT_2026-08-16.md`). |
| Payload | `C:\tmp\payload-be007fd8`; `RELEASE_SHA256SUMS` sha256 `bde1ff7dcd46a8b104ffdaca7a146ba0eca1958dab577a5a8e926dc24ee0b0a3` |
| **Command annex (the only executable text)** | `KVM2_PLAN_V6_COMMAND_ANNEX_2026-08-16.md` — 32079 B, sha256 `37d892bad2eedc6216cba60725107455798fd91b74f41cc34906f6ad86e22e0b` (final night bytes: unit-guard cleanup repair, subordinated draft sentence, Stage-0 old-payload removal line, and the be007fd8/bde1ff7d repin — 21 identity replacements verified, the single remaining `acdf4e37` string being the Stage-0 removal target itself). Contains: fully isolated `scp`/`ssh` option sets (mirroring the launcher), full 40-hex paths, stages 1–3.5 with rc/stderr STOP rules, the verified never-started rollback-rehearsal branch (tar + sha256 against `rollback.sh`'s real input contract — confirmed non-JSON), the fail-closed D3 evidence contract (sqlite read-only persistence leg; auditd UID-scoped connect rule with active-rule proof, lost-counter equality, `NO_MATCHES` normalization, exact cleanup), and the complete tenancy/removal enumeration incl. cron asset, payload, audit rule, package disposition. |
| Launcher | `KVM2_RUNKIT/Open-BridgeDashboard.ps1` **v4** — 9277 B, sha256 `ac68196b4ae99e12892898c0a5bfb2d7d2249fc2bb476619a4c2bdaaebf2a1b5`. v3 + strict full-row `ssh-add -l` grammar (field-2 fingerprint only, malformed row = STOP); comment-injection false pass eliminated. |
| Host / access | unchanged: `srv1856225` = `152.239.123.231`, `baris`, pinned host key, owner-loaded agent |
| Retired pins | candidates `62bf661b`/`be689537`/`a7460784` + their payloads; launchers v1/v2/v3. Never installed. |

## 2. Round-3 finding closure (all eight)

R1 D026 arms → structural fences (unclassified heads fail; exact round-3
mutations RED). R2 UFW → verbs + profiles + backstop closed. R3 metadata →
asserted before bytes, numeric owner + kind, RED fixtures. R4 launcher →
strict grammar. R5 commands → complete isolated literal set in the annex.
R6 rehearsal → verified never-started tar branch. R7 evidence → executable
fail-closed contract in the annex. R8 boundary → complete enumeration in the
annex and restated in §3 below. Claude R1/R2 close with R2/R6. Details:
`RIC3_REPAIR_REPORT_2026-08-16.md`.

## 3. THE single authoritative authorization sentence (the only signable copy)

Corrected under `OWNER_DECISION_CONFIRMATION_PASS_2026-08-16.md`: this section
carries the ONE authoritative sentence (the annex's former draft copy is
explicitly subordinated and not for signature). Command annex of record:
`KVM2_PLAN_V6_COMMAND_ANNEX_2026-08-16.md`, 32079 bytes, sha256
`37d892bad2eedc6216cba60725107455798fd91b74f41cc34906f6ad86e22e0b`.

> "I authorize one attempt to transfer `~/payload-be007fd8` and perform the
> masked, never-started, credential-free DISARMED installation and read-only
> operational evidence for exact release
> `be007fd802bbfd2eb181d66038c374865d1562ee` on Hostinger KVM2
> (`srv1856225`), per KVM2_DEPLOYMENT_PLAN_V6_2026-08-16.md and its command
> annex of sha256
> `37d892bad2eedc6216cba60725107455798fd91b74f41cc34906f6ad86e22e0b`,
> limited exactly to `/opt/mtc-bridge/`, `/etc/mtc-bridge/`,
> `/var/lib/mtc-bridge/`, `/var/log/mtc-bridge/`, the `mtc-bridge` user and
> group, `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`, its
> `/etc/systemd/system/mtc-bridge-first-start.service` `/dev/null` mask,
> `/etc/logrotate.d/mtc-bridge`, `/etc/cron.hourly/mtc-bridge-logrotate`,
> `/home/baris/payload-be007fd8` (after first removing the superseded
> `/home/baris/payload-acdf4e37` per the annex Stage-0 line),
> `/home/baris/bridge-state-initial.tar.gz`,
> `/home/baris/bridge-state-initial.sha256`, and the named encrypted
> operator-side directories `C:\tmp\KVM2_BRIDGE_ENCRYPTED` and
> `C:\tmp\KVM2_BRIDGE_RESTORE_CHECK` on my Windows computer. This authorizes
> payload transfer, dry run, one bounded install, verifier execution, the
> tar-hash rollback rehearsal, encrypted-in-transit and encrypted-at-rest
> backup/restore comparison, monitoring, and read-only re-inventory only. A
> later separate D3 sentence may additionally authorize
> `/home/baris/mtcbridge-d3-evidence`, installation of baseline-absent distro
> `auditd` and transaction-added `libauparse0`, one exact numeric-UID
> `connect` audit rule keyed `mtcbridge_net` with the rule removed and the
> packages purged under the recorded baseline/simulation gates, and the
> temporary `auditd` service start/stop that evidence window requires. No
> Bridge service start, any service enable, secret, firewall change, public
> 8790, TESTNET or mainnet action, broker, ARM, order, trading action,
> Hermes/web identity or path, other
> user/group/service/package/container/port, or retry is authorized. On
> failure, stop, remove only the exact listed objects with the annex's
> commands, re-inventory to the clean baseline, and report; any retry needs a
> new sentence."

## 4. Final-pair review contract (owner's materiality standard, verbatim in force)

Subjects: THIS file + the pinned annex + launcher v4 + candidate `acdf4e37`.
Both reviewers: verify closure of the eight round-3 findings, candidate
scope, full suite (`1376 passed, 1 warning`), pins, and the exact initial
KVM2 deployment boundary. **A newly discovered finding may block ONLY if the
Lead reproduces it and demonstrates it materially affects the exact initial
deployment** (root trust, SSH authentication, public exposure,
DISARMED/keyless safety, installation integrity, rollback/removal, or
another directly applicable T0 safety property). Generalized future-mutation
cases, documentation polish, and proof-strength improvements that do not
affect the exact initial keyless DISARMED deployment are recorded as
disclosed follow-up work. No fifth round exists.
