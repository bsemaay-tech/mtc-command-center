# KVM2 deployment plan V6 (FINAL) — candidate `acdf4e37` — 2026-08-16

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
| **Final candidate** | `acdf4e379fb60ee319854acae19fd3eaf7db71a2` — tip of `integration/bridge-release-20260815` (pushed); lineage `62bf661b` → `be689537` → `a7460784` → `acdf4e37`. Replacement initial-release candidate; KVM2 empty and untouched. |
| Round-4 delta vs `a7460784` | 4 files, +373/−36: complete UFW verb coverage (`ALLOW/LIMIT × IN/FWD`, named profiles fail closed, independent 8790 substring backstop, numeric `22/tcp` SSH requirement), structural D026 fences (statement extraction; unclassified executable heads FAIL), `assert_mode_owner` numeric-owner+kind applied to the root-executed logrotate/cron assets before byte comparison, honest structural-boundary documentation. |
| Candidate test state | `1376 passed, 1 warning` — implementer 189.98 s AND Lead-independent 196.12 s. All round-3 mutations RED / final bytes GREEN (`RIC3_REPAIR_REPORT_2026-08-16.md`). |
| Payload | `C:\tmp\payload-acdf4e37`; `RELEASE_SHA256SUMS` sha256 `e74c59fec82d49090d5ba56d4bf18f1cc0dbdd93375c0c82c07ab44b211530bf` |
| **Command annex (the only executable text)** | `KVM2_PLAN_V6_COMMAND_ANNEX_2026-08-16.md` — 31283 B, sha256 `8cb02ff7fa13eb7e0ac602cfe0f1854b615cb079535ff91385e6c18efc5e5fce`. Lead-repinned from the implementer's inputs to the final identities (21 pin replacements, zero stale pins — verified by grep). Contains: fully isolated `scp`/`ssh` option sets (mirroring the launcher), full 40-hex paths, stages 1–3.5 with rc/stderr STOP rules, the verified never-started rollback-rehearsal branch (tar + sha256 against `rollback.sh`'s real input contract — confirmed non-JSON), the fail-closed D3 evidence contract (sqlite read-only persistence leg; auditd UID-scoped connect rule with active-rule proof, lost-counter equality, `NO_MATCHES` normalization, exact cleanup), and the complete tenancy/removal enumeration incl. cron asset, payload, audit rule, package disposition. |
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

## 3. §4 — the single authorization ask (present ONLY if the final pair accepts)

> "I authorize the one-attempt masked DISARMED installation of exact
> replacement release `acdf4e379fb60ee319854acae19fd3eaf7db71a2` onto
> Hostinger KVM2 (`srv1856225`) per KVM2_DEPLOYMENT_PLAN_V6_2026-08-16.md and
> its pinned command annex (sha256 `8cb02ff7…`) — that is: payload transfer,
> dry run, one bounded install, read-only verification, and Bridge-scoped
> operational evidence in the annex's stage-3 order (never-started state
> capture, rollback rehearsal including its rollback-manifest write, off-host
> encrypted backup + restore check, monitoring baseline, tenancy
> re-inventory). Allowed filesystem objects on KVM2: `/opt/mtc-bridge/**`,
> `/etc/mtc-bridge/**`, `/var/lib/mtc-bridge`, `/var/log/mtc-bridge`, the
> `mtc-bridge` user/group, the masked first-start unit + its mask symlink,
> `/etc/logrotate.d/mtc-bridge`, `/etc/cron.hourly/mtc-bridge-logrotate`,
> and `~/payload-acdf4e37` — nothing else. It also pre-authorizes, for the
> later D3 evidence window only, installing the distro `auditd` package and
> the one UID-scoped connect-audit rule exactly as the annex writes them,
> with the annex's removal commands. No service start, no enable, no secret,
> no firewall change, no TESTNET/mainnet, no broker, no ARM, no orders, no
> action on reserved Hermes/web identities, no public exposure of port 8790
> ever. The D3 matrix runs only after my separate first-start sentence. A
> failed attempt stops, removes exactly the annex's enumerated objects, and
> reports; any retry needs a new sentence."

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
