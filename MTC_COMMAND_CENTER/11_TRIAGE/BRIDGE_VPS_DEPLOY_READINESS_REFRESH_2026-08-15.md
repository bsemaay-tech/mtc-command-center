# Bridge VPS deploy readiness refresh — 2026-08-15

## Verdict and scope

**Overall verdict: BLOCKED.** The repository does not prove that the bridge at
this checkout is ready for a first Hostinger KVM2 start. Historical staging
evidence is materially newer than the 2026-07-26 checklist notes, but the
staging-accepted candidate is not contained in this checkout, the current WP-I
release freeze is stopped at an owner decision, and no current KVM2 facts were
collected.

Target used for every classification: **one hardened KVM2 service, first start
DISARMED, TESTNET-only, loopback-only; no live trading, no ARM, no mainnet.**
ARM and the later ten-day monitoring counter are not part of this finish line.

Gate-1 audit tier: **T2 — docs/evidence status refresh.** The kickoff explicitly
forbade another model, host access, network access, deployment actions, and all
product-code changes, so this report is the lane's self-contained verification
record.

Preflight command evidence before this file was created:

```text
git -C C:\BRDG rev-parse HEAD
ddc8a9c802cc45f66f449b02f18a07448afc5f70

git -C C:\BRDG status --porcelain
<empty>
```

The five classification labels below are mutually exclusive. `STALE-CLAIM`
means the old `Current:` note is wrong; it does **not** mean the item is ready.
Each such item states the corrected readiness consequence.

## Release-identity split that controls this refresh

Repository evidence records Gate-A staging acceptance for candidate
`2ce41e34bceb599d80af24c5c33d835820ec321b`: A-0 through A-9 passed, but the
record explicitly limits that result to staging and grants no merge or
production/deploy authority
(`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A9_PASS_FINAL_2026-08-09D.md:5-8,
56-65`). Read-only Git checks in this lane produced:

```text
git merge-base --is-ancestor 2ce41e34bceb599d80af24c5c33d835820ec321b HEAD
rc=1
```

The accepted staging candidate is therefore **not an ancestor of this checkout**.
The following current blobs also differ from their `2ce41e34` counterparts:

| Artifact | `HEAD` blob | accepted `2ce41e34` blob |
|---|---|---|
| `IBKR_PAPER_BRIDGE/deploy/linux/package.sh` | `150c18c36447ecc122332a992581ca6d9bba4007` | `add6478d33cce8d929d58f895407abe01d51da20` |
| `IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template` | `b175ced7f36df52ad2e55532264f36f49fdc8281` | `c18232549d96aa200d8c7f796e64de743288940c` |
| `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh` | `bce1f0e23e63f9a8d168c751aec99ac84d1334c7` | `5cfefd709202ff504ae7b7fc3504b8c0b00900b6` |
| `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` | `aaa2918229a1367ebf1fb6a458a4e65673dc180e` | `26c077e650ab88ba2086efa3a80790769bc055b1` |
| `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py` | `a1486d759d6df9fa11f4efed65e9ec764a558185` | `64e25888ba67a6b706bbf5c9d5e5feb8f12a98b2` |

This is not a cosmetic branch difference. The current unit still starts bare
`python -m bridge.app` and sets only the state DB environment
(`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:29-43`);
neither current source nor current deployment assets contain
`credential_free_disarmed`. The accepted staging run, by contrast, proved a
unit with `MTC_BRIDGE_START_MODE=credential_free_disarmed`, a loopback listener,
a DISARMED API, no broker attempt, and application-level ARM refusal
(`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A4_PASS_2026-08-08C.md:38-54`). Historical
Gate-A success cannot be transferred to the different bytes at `HEAD`.

## Ten-item refresh

### 1. Produce the exact release candidate — `STALE-CLAIM`

The 2026-07-26 statement “local preparation complete; commit/audit/acceptance
OPEN” is no longer an accurate description. The original Linux preparation is
committed (the current versions trace to commit `6fe0130f`), and a different
candidate, `2ce41e34`, later obtained both flagship acceptance and a complete
staging Gate-A pass
(`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md:3-20,
34-55`; `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A9_PASS_FINAL_2026-08-09D.md:5-8`).

Corrected fact: **there is still no accepted release candidate for the current
product tree at `ddc8a9c…`.** `2ce41e34` is not in its ancestry, and the current
Stage-1 freeze is blocked by a fresh Pathscope `REQUEST_CHANGES`. The latest
boundary record says the lane is stopped, lists three required findings, and
states that Stage-1 freeze, Audit 2, and WP-A remain blocked
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OWNER_BOUNDARY_2026-08-15.md:3-8,
29-52,59-75`).

The owner input needed before local release work can continue is one of the four
sentences in
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:108-124`.
The evidence-backed recommendation is:

> Option C: I authorize the Pathscope accounting-layer redesign, followed by one
> fresh flagship execution audit.

After that decision, closure evidence must be: an accepted Pathscope result; a
clean frozen current-product SHA containing the accepted deployment/WAL repairs;
exact blob and payload hashes; a full exact-SHA local suite; and the tier-required
independent acceptance. Until then, current release SHA is **UNVERIFIED / not
frozen**.

### 2. Make Python reproducible — `STALE-CLAIM`

The blanket 2026-07-26 statement that Ubuntu installation was unverified is
stale. Current local facts are:

- `requirements.in` contains the ten direct dependencies and says the lock is
  the only Linux install input
  (`IBKR_PAPER_BRIDGE/requirements.in:1-24,26-35`).
- The actual `requirements.lock` declares `uv pip compile --generate-hashes
  --python-version 3.12 --python-platform linux`
  (`IBKR_PAPER_BRIDGE/requirements.lock:1-3`).
- This lane ran the offline parser against the actual lock: `verify_lock: PASS:
  lock; packages=56`; lock SHA-256 is
  `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3`.
  The verifier rejects unpinned/unhashed entries and contacts no network
  (`IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py:1-7,28-63,75-98`).
- The installer creates a per-SHA venv, installs the lock, and compares the
  installed distribution set with it
  (`IBKR_PAPER_BRIDGE/deploy/linux/install.sh:300-309`).
- A real Ubuntu 24.04 staging install did succeed for the historical accepted
  candidate, including Python 3.12, 56 locked packages, exact venv equality,
  and a verified masked install
  (`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RESULT_2026-08-08.md:121-156`).

Corrected readiness consequence: the ordinary Ubuntu install path is proven for
the historical candidate, but the documented fully offline `--wheelhouse` path
(`IBKR_PAPER_BRIDGE/deploy/linux/README.md:58-69`) has no executed evidence in
the reviewed artifacts, and no install has been run for a frozen current-product
SHA. Those two facts are **UNVERIFIED**. Item 2 is therefore not closed for the
current release.

### 3. Harden the service boundary — `STALE-CLAIM`

The old note says only structural assets existed and Ubuntu verification plus
independent acceptance were open. That is stale for `2ce41e34`: the accepted
staging install proved the dedicated paths/ownership, root-owned `0600` env file,
exact-SHA unit, masked/inactive state, `Restart=no`, throttling, logrotate,
loopback source, closed port before start, and unchanged UFW
(`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RESULT_2026-08-08.md:121-150`). The later
first-start test proved active/running DISARMED service behavior and loopback-only
listening (`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A4_PASS_2026-08-08C.md:38-54`).

Corrected readiness consequence: those proofs do **not** cover the current
blobs. The current unit has substantial hardening—dedicated user, exact release
paths, graceful stop, `Restart=no`, append logs, empty capabilities, strict
filesystem protection, restricted system calls, and only state/log writable
paths
(`IBKR_PAPER_BRIDGE/deploy/linux/systemd/mtc-bridge-first-start.service.template:21-34,
45-59,61-91`)—but it lacks the accepted credential-free start-mode pin. The
current package builder also uses an unpinned plain `git archive` pipeline
(`IBKR_PAPER_BRIDGE/deploy/linux/package.sh:46-87`), whereas the accepted blob is
different. Local integration/re-audit and exact-current-SHA Ubuntu proof are
still required.

### 4. Provision only a VPS-specific TESTNET agent wallet — `NEEDS-OWNER`

The repository contains names and storage rules only. It requires a VPS-specific
TESTNET agent key and account address in a root-owned `0600` env file, never the
main wallet key
(`IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template:1-20`;
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/SECRET_INVENTORY.md:6-10,20-21`).
`HL_LIVE_ACK` must be absent
(`IBKR_PAPER_BRIDGE/deploy/linux/env/mtc-bridge.env.template:30-35`).

Required owner artifact: a newly created/revocable **KVM2-specific Hyperliquid
TESTNET agent wallet**, with `HL_ACCOUNT_ADDRESS` and `HL_API_WALLET_KEY`
provisioned through an approved secret channel directly into
`/etc/mtc-bridge/mtc-bridge.env` at `root:root 0600`. No value belongs in this
report, the repository, chat, shell history, or plaintext backup. Repository
status of that secret is necessarily **UNVERIFIED**.

### 5. Choose the risk-state continuity policy — `NEEDS-OWNER`

This old claim remains accurate. The canonical state document still says the
choice is open, recommends WAL-consistent migration, and says fresh reset is not
selected
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md:1-6`).
It specifies online SQLite backup, integrity/foreign-key checks, invariant
hashes, and fail-closed comparison before first start
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md:7-26`).
No later owner selection was found in the bounded search.

Required owner sentence:

> I select WAL-consistent migration for the KVM2 cutover and authorize its
> adversarial staging specification; fresh-database reset is not approved.

If Barış instead wants a reset, he must explicitly select it and approve a
fail-closed specification covering lost daily-loss, consecutive-loss, order,
and foreign-position evidence. Silence is not a selection.

### 6. Execute the exact single-writer cutover proof — `NEEDS-HOST`

The repository defines the invariant but cannot prove today's runtime state.
The migration runbook requires the old task to be DISARMED, stopped, and
disabled, with no concurrent writer, and it keeps the P3-01 state choice open
(`IBKR_PAPER_BRIDGE/docs/17_DEPLOYMENT.md:63-74`). The ordered checklist itself
requires fresh raw empty positions/orders, Windows wrapper/child termination,
port 8790 closure, old-agent revocation, and a second raw exchange check before
the VPS start
(`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:115-121`).

All of the following are **UNVERIFIED** from this repository: current Windows
task state, wrapper/child process state, Windows port 8790, current exchange
orders/positions, fresh reconcile, old-agent revocation, final WAL capture and
transfer, and absence of a second writer. Closing this item requires separately
authorized access to the Windows runtime, exchange-side read-only evidence, and
KVM2. Any failed or ambiguous observation must stop the cutover.

### 7. Keep the control plane private — `STALE-CLAIM`

The old note's “no host or listener was accessed” is false as a general current
statement. The source still binds Uvicorn to `127.0.0.1:8790`
(`IBKR_PAPER_BRIDGE/bridge/app.py:214-234`), and the verifier contains read-only
checks for default-deny/SSH-only UFW and non-loopback listeners
(`IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:150-178,181-205`). On the staging
candidate, A-8 proved one `127.0.0.1:8790` listener, no wildcard/non-loopback
listener, successful UFW inspection, reachable port 22, and unreachable public
port 8790
(`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A8_PASS_2026-08-09D.md:34-54,67-86`).

Corrected readiness consequence: local design and historical staging proof are
strong, but **current KVM2 UFW and listener state are UNVERIFIED**, and the
staging proof covered different release bytes. Item 7 cannot close until the
accepted current SHA is installed and the same assertions reproduce on KVM2.

### 8. Complete operations evidence — `NEEDS-HOST`

Substantial local machinery exists:

- The installer records release SHA, payload-manifest hash, unit hash, lock
  hash, state/log/env paths, and false install-time action flags
  (`IBKR_PAPER_BRIDGE/deploy/linux/install.sh:399-425`).
- Log rotation is daily, bounded to 30 generations/64 MiB, compressed, and
  non-restarting (`IBKR_PAPER_BRIDGE/deploy/linux/logrotate/mtc-bridge:1-25`).
- Rollback is designed to stop/mask, preserve state, verify a prior exact
  release, and never start/enable/unmask
  (`IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh:3-29,112-183`).

There is also a current local contract defect: the canonical release-evidence
tool still defines its lock input as `requirements.txt`
(`IBKR_PAPER_BRIDGE/tools/release_evidence.py:54`), and the contract explicitly
says no separate lockfile exists
(`IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md:73-88`), although
`requirements.lock` now exists and is the actual installer input. That contract,
tool/schema, and tests need a local accepted update before their manifest can be
used as current dependency evidence.

Host-dependent evidence remains absent: executed rollback, encrypted off-host
backup, isolated restore, unit/logrotate behavior on KVM2, health/restart-loop/
reconcile-freshness/disk-log monitoring, and retention/recovery credentials.
The recovery contract itself says these backup/restore requirements remain open
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md:28-43`),
and maintenance remains specification-only
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/MAINTENANCE.md:1-8,23-28`).
This item cannot be closed without authorized host execution; backup provider,
retention, and monitoring-credential choices also need owner input.

### 9. Pass exact-SHA test matrices before first start — `STALE-CLAIM`

The old “58 targeted / 276 full” count is stale. The old readiness record still
contains those builder counts
(`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/audits/READINESS_STATUS.md:21-34`),
but later accepted-candidate audits executed a 1,360-test full suite
(`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md:10-20,
52-68`), and Gate A later recorded A-0 through A-9 PASS for that same candidate
(`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A9_PASS_FINAL_2026-08-09D.md:5-8,56-65`).
The owner has since declared that the official record must be the full Bridge
suite at the future frozen SHA and that older counts are non-referent
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-13.md:29-36`).

Corrected readiness consequence: the current checkout has **no future frozen
SHA**, and this lane did not execute a current-HEAD suite. Current exact-SHA test
status is therefore **UNVERIFIED**. More seriously, the current deployment test
still asserts the old checklist's “local candidate uncommitted” and open-audit
text (`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:470-496`) and does not
assert the accepted start-mode pin
(`IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py:148-170`). A green current
suite would not by itself prove the required DISARMED first-start property.

Closure evidence must bind one newly frozen current-product SHA to: the complete
local Bridge suite; targeted deployment/WAL tests with D026 RED/GREEN for each
new defect closure; clean payload build and hashes; a fresh Ubuntu matrix; and
the target first-start properties. Historical `2ce41e34` evidence is useful
regression evidence, not closure evidence for different bytes.

### 10. Close final gates — `NEEDS-OWNER`

There is no accepted current candidate to audit or deploy, and the Pathscope
owner boundary prevents the next freeze. Even after that local blocker closes,
Gate-A history explicitly says staging acceptance does not authorize master
merge, credential loading, production promotion, ARM, or economic action
(`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A9_PASS_FINAL_2026-08-09D.md:5-8,64-79`).
The deployment guide also keeps install, secrets, cutover, first start, and ARM
as separate owner gates (`IBKR_PAPER_BRIDGE/docs/17_DEPLOYMENT.md:9-12`).

For this task's narrower finish line, Barış must ultimately provide separate,
unambiguous authorization sentences for:

1. installation/configuration of the exact accepted SHA while the unit remains
   masked and unstarted;
2. TESTNET-only KVM2 secret provisioning;
3. the ordered single-writer cutover/state migration; and
4. exactly one first DISARMED, TESTNET-only, loopback-only start.

The final first-start sentence should name the frozen SHA and say explicitly:

> I authorize exactly one first DISARMED, TESTNET-only, loopback-only KVM2 start
> of accepted release SHA `<40-hex>` after every preceding gate passes. ARM,
> mainnet, orders, and live trading remain forbidden.

No ARM sentence and no ten-day ARM monitoring window are required for the
finish line assessed here.

## `LOCAL-CLOSABLE` items

**None.** No whole checklist item can be closed today using local work alone:
items 1, 4, 5, and 10 reach owner gates; items 2, 3, 6, 7, 8, and 9 ultimately
require new exact-SHA host evidence; and items classified `STALE-CLAIM` need the
corrected local/host/owner sequence stated above. Consequently there is no
per-item `LOCAL-CLOSABLE` hour/evidence row to report. Local work still exists
inside the mixed critical path and is estimated below.

## Critical path to one DISARMED KVM2 first start

Assumption: Barış selects the recommended Pathscope Option C. Estimates are
hands-on competent-implementer time, not calendar/queue/quota time.

| Order | Minimum closure work | Local hours | Owner hours | Host hours | Proof required |
|---:|---|---:|---:|---:|---|
| 1 | Owner selects Pathscope disposition; implement and independently accept Option C | 6–10 | 0.1 | 0 | Accounting invariant, full fixture/harness execution, D026 evidence, fresh accepting audit |
| 2 | Integrate the accepted package/unit/verifier/WAL fixes into the current product line; repair the release-evidence lock contract; remove stale test assumptions; freeze one exact SHA; build/hash payload; run full local suite and tier-required audits | 12–20 | 0 | 0 | Clean SHA, exact diff/blob/payload identities, current lock+unit+manifest hashes, full-suite output, accepting verdicts |
| 3 | Owner selects WAL continuity, backup/retention/monitoring choices, and provisions the KVM2-specific TESTNET agent artifact | 0 | 0.4–0.9 | 0 | Dated owner decisions plus secret provision confirmation with no value disclosed |
| 4 | Reproduce current KVM2 baseline; install the exact SHA; prove Python 3.12 lock install including offline wheelhouse path; verify identity, paths, unit, UFW, closed port, and masked/unstarted state | 0 | 0.1 | 2–4 | Sanitized baseline, installer/verifier logs, installed-distribution equality, hashes, zero writer/listener |
| 5 | Execute rollback, encrypted backup/isolated restore, logrotate, and monitoring checks on the accepted install | 0 | 0.1 | 3–6 | Rollback manifest, restore hashes/semantic invariants, rotation evidence, active monitoring evidence |
| 6 | Perform the ordered single-writer cutover and accepted state migration | 0 | 0.1 | 1.5–3 | Fresh raw empty orders/positions, Windows task/process/port proof, revoked old agent, WAL bundle/invariant hashes, destination equality |
| 7 | Owner authorizes one first start; start once and observe the hardened service | 0 | 0.05–0.2 | 1–2 | Active service, `Restart=no`, zero restart loop, DISARMED API/DB, TESTNET-only configuration, exactly one loopback listener, no public 8790, reconcile-ready/no-order evidence |
| **Total** |  | **18–30** | **0.85–1.5** | **7.5–15** |  |

**Combined hands-on estimate: approximately 27–47 hours.** Option B (accept
Pathscope with disclosure) would reduce local work, but it deliberately removes
a safety proof and is not the Lead recommendation recorded in the repository.
Any host drift, failed test, new audit finding, or unavailable backup/monitoring
provider can increase the range.

## What cannot be known from the repository

The following are genuinely **UNVERIFIED** without owner answers or separately
authorized current host/runtime access:

- whether KVM2 still matches the 2026-07-25 Ubuntu, SSH, UFW, fail2ban, update,
  time-sync, disk/RAM, Python/git, `/opt`, pip, Docker, and application snapshot;
- whether any bridge release, venv, service user, unit, env file, state DB, logs,
  firewall rule, process, or listener currently exists on KVM2;
- whether KVM2 port 8790 is private today and whether port 22 is the only allowed
  inbound surface;
- whether a KVM2-specific TESTNET wallet exists, is securely provisioned, or has
  been revoked/rotated; secret values must not be inferred or searched for here;
- Barış's Pathscope choice, P3-01 risk-state choice, backup provider/retention/
  recovery-key choices, monitoring provider/credentials, and the four separate
  deployment-gate authorizations;
- current Windows scheduled-task, wrapper, child-process, writer, DB, and port
  state;
- current reconcile freshness and raw exchange orders/positions, and whether the
  old-host agent has been revoked;
- whether a WAL-consistent source bundle can be captured now and whether its
  risk/history invariants match the future KVM2 destination;
- whether rollback, encrypted off-host backup, isolated restore, log rotation,
  disk/log/restart monitoring, and alert delivery work on KVM2; and
- whether the future frozen current-product SHA passes the full local and Ubuntu
  matrices and starts once in the required DISARMED/TESTNET/loopback-only state.

No dated VPS snapshot, adjacent staging fact, or historical candidate result was
used to fill any of those gaps.
