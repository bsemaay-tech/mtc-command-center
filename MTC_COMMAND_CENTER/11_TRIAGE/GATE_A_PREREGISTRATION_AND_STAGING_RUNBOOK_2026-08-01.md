# GATE A — PRE-REGISTRATION AND STAGING RUNBOOK (2026-08-01)

**Written before any host exists, deliberately.** Every check, every expected output and every
pass/fail line below is fixed *now*, so that when a machine appears we execute rather than improvise
— and so nobody can quietly adjust the criterion to match whatever the run produced.

This cycle already paid for that lesson twice: a generated test matrix passed while proving nothing,
once masked by an `UPDATE` that set the value under test, once by a fixture that pre-satisfied its own
assertion. **A check that cannot fail is not evidence.** Each check below therefore states what a
FAIL looks like, not only a PASS.

---

## 0. What Gate A is and is not

**Is:** proof that the immutable candidate installs and runs on a clean Ubuntu 24.04 host in a
**DISARMED** state — process starts, state survives restart, reconcile completes, health is
observable, and nothing can trade.

**Is not:** a trading test, a performance test, a TESTNET order, or a production deployment. Gate A
touches no broker, sends no order, and never arms.

**Hard boundary for the whole runbook:** DISARMED only. No ARM. No order. No broker credentials. No
TESTNET. No mainnet. No wallet. If a step seems to require a credential value, **stop and ask** — do
not improvise one, and never paste a secret into a session.

---

## 1. Host requirements — the one thing currently blocking

| Requirement | Value |
|---|---|
| OS | Ubuntu 24.04 LTS, clean install |
| Disposability | **Must be expendable.** We will break it, wipe it, and redo. |
| Reachability | Reachable from the operating session |
| Forbidden | The active KVM2 host. It is doing live work; a first-ever install must not land there. |

Acceptable sources, cheapest first: a Hyper-V VM on this Windows machine (Hyper-V is present; VM
inventory access is currently denied and would need enabling) · a new VirtualBox or QEMU VM · a
short-lived scratch VPS · a second idle VPS already owned.

**Credentials stay owner-held.** Provide reachability, not secrets.

---

## 2. Inputs, frozen

| Item | Value |
|---|---|
| Candidate artifact | `C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84` |
| Manifest SHA-256 | `bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02` |
| Manifest entries | 7,060 verified · 7,061 files · 1,051,904,669 bytes |
| Secret scan | nine categories, zero hits |
| `origin/master` | `637307e8` |
| WP-L branch | `codex/50h-wpl-verification` @ `d9d38d9b` |
| Records branch | `feature/donchian-crypto-ladder` @ `ea85566b` |

**A-0 — identity before transfer.** Recompute the manifest SHA-256 on the source side and confirm it
equals `bfefea2f…`. Recompute again on the host after transfer and confirm it still equals it.
**FAIL:** any mismatch, or a file count other than 7,061. Do not proceed on a mismatch — a corrupted
transfer that boots looks exactly like a good one until it doesn't.

> Note: hash the artifact as transferred, not the working tree. CRLF differences have already caused
> one false hash mismatch in this programme (the WP-L Phase 1 ledger failure), so line-ending
> normalisation must be identical on both sides.

---

## 3. Gate A checks — each with its FAIL condition

Run in order. Stop at the first FAIL and report; do not continue past a failed check.

### A-1 Clean-host preconditions
Ubuntu 24.04 confirmed; Python version matches the lockfile; the artifact's own dependency lock
resolves with no network fetch beyond the declared set.
**FAIL:** OS or Python mismatch, or any undeclared dependency pulled at install time.

### A-2 Install from the immutable artifact only
Install exclusively from the transferred artifact — no `git clone`, no ad-hoc `pip install`, no file
edited by hand on the host.
**FAIL:** any step that requires editing a file on the host to make it work. That means the artifact
is not self-contained, which is the thing WP-I exists to prove.

### A-3 Linux test suite
Run the 35 Linux tests plus the Bridge suite on the host.
**Expected:** the known pre-existing failures only — the KVM2 ledger-hash test and the
`schema_version == "2"` test. Both fail identically on `origin/master`, and the ledger one is a
Windows CRLF artefact that **may legitimately pass on Linux**.
**FAIL:** any third failure. Also record explicitly whether the ledger test passes here — if it does,
that confirms the CRLF diagnosis rather than a real defect, and it should be written down as such.

### A-4 Starts DISARMED, and stays that way
Start the service. Confirm `app_state` is durably **not** `ARMED`, that the ARM path refuses, and
that no broker connection is attempted.
**FAIL:** the service arms, attempts a broker connection, or reports an ambiguous state.
**This is the most important check in the gate.** A pass here is the whole point of the 50 hours.

### A-5 Restart safety
Stop the service uncleanly (kill, not graceful). Restart. Confirm state is intact, the database is
consistent, and it comes back DISARMED.
**FAIL:** lost state, a corrupted database, a failure to start, or coming back in any other state.

### A-6 Reconcile completes
Confirm the reconcile path runs to completion on startup against an empty/mock broker surface.
**FAIL:** reconcile raises, hangs, or leaves queued events unconsumed. Note that four rounds of S3
work went into exactly this path — an unhandled exception here must never wedge startup silently.

### A-7 Observability
Confirm health/status is readable and reports the true state, and that logs are written where the
runbook says.
**FAIL:** health reports a state that contradicts the database, or logs are absent.

### A-8 Loopback-only exposure
Confirm the service binds to loopback/private only and is not reachable from outside the host.
**FAIL:** any public listener.

### A-9 No secrets on disk
Re-run the secret scan on the installed host tree.
**FAIL:** any hit in the nine categories.

---

## 4. What happens after Gate A

`Gate A verification → WP-L Phase 2 → WP-I staging → Audit 2 → WP-A`, all DISARMED.

**Audit 2 must restore the canonical acceptance floor.** WP-I's candidate acceptance currently rests
on a single owner-waived DeepSeek pass, not on two flagship auditors. That waiver was the owner's
call and is valid, but it is a weaker basis than WP-S received, and Audit 2 is where the gap closes.
Auditor 4 (GLM-5.2) also needs its route confirmed working — it returned `401 token expired or
incorrect` during the S3-STRUCT cycle.

---

## 5. Reporting format for the Gate A run

```
host             : <OS, source, expendable yes/no>
artifact hash    : <source> / <after transfer>  (must both equal bfefea2f…)
A-1 preconditions: PASS | FAIL <why>
A-2 install      : PASS | FAIL <why>
A-3 suite        : <literal final pytest line> ; ledger test on Linux: PASS|FAIL
A-4 disarmed     : PASS | FAIL <why>
A-5 restart      : PASS | FAIL <why>
A-6 reconcile    : PASS | FAIL <why>
A-7 observability: PASS | FAIL <why>
A-8 loopback     : PASS | FAIL <why>
A-9 secrets      : PASS | FAIL <why>
actions taken    : <every command run on the host>
NOT done         : <anything skipped, and why>
```

**No ARM, order, broker, TESTNET, mainnet, wallet, credential-value or live-capital action occurs at
any point in Gate A.** If any step appears to require one, that is a blocker to report, not a step to
take.
