# GATE A — POST-GATE ROADMAP AND AUTHORITY DISCOVERY (READ-ONLY, 2026-08-09)

> **Method:** read-only documentation discovery over repository records at starting HEAD `51e666b0`.
> **No staging command was run.** No SSH, no Gate-A script, no scan, no `sudo`, no service action, no
> package action, no Git command, no staging mutation, no credential read, no broker/exchange/network
> command. Every fact below is cited to an exact repository file and line range.
> **Model/effort:** `claude-opus-5`, effort `xhigh`.
> **Citation note:** all line numbers are as of HEAD `51e666b0`. The prepend written alongside this record
> shifts `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md` down by the length of its new checkpoint block;
> its two citations below (`:1452-1454` hard stop, `:1489-1492` budget) are quoted verbatim so they stay
> locatable by text.

---

## 1. Conclusions first

1. **WP-V is NOT the next step, and Gate-A PASS does not make it next.** Gate A A-0..A-9 PASS is
   **staging acceptance only**. The canonical plan places four whole units between Gate A and any
   deployment gate: WP-L Phase 2, WP-I staging verification, Audit 2, and WP-A.
2. **No record in this repository proves WP-L Phase 2, WP-I staging verification, Audit 2, or WP-A
   completed after the final Gate-A pass.** The retained-host evidence list is still open.
3. **The named expendable host `GATEA-STAGING` still exists and has not been discarded.** It is
   active/running, credential-free DISARMED, with only candidate
   `2ce41e34bceb599d80af24c5c33d835820ec321b` installed. Under the plan it must be retained until
   WP-A evidence is captured.
4. **Standing owner authorization for the programme exists** (`OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md:20-56`)
   and does cover WP-L/WP-I/WP-A/WP-R/WP-V, Ubuntu staging, the named expendable host, KVM2, and even
   pre-grants the WP-V / ARM / first-TESTNET approvals — **but only subject to every objective
   prerequisite passing.**
5. **Later, narrower operational constraints control the current transition** and have not been lifted
   by name. WP-V, KVM2, master merge, credentials, broker, ARM, orders, TESTNET/mainnet and economic
   action each need a new explicit named instruction.
6. **A budget blocker is open** (≈14–17 h remained; WP-A+WP-R+WP-V alone total 17 h; Gate-A repair work
   was unbudgeted). The exact current hour ledger is **not reconstructed**, and the accepted plan has a
   hard 50-hour ceiling with no silent overrun.
7. **The budget blocker does not require idling.** A read-only/local next safe unit exists and is
   authorized now — see §6.

---

## 2. Authority — what is and is not authorized right now

### 2.1 Standing programme authorization (broad)

`11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md:20-56` is standing owner authorization for,
among other items: WP-S, **WP-L, WP-I, WP-A, WP-R, WP-V**; Ubuntu staging; **using the named expendable
Ubuntu staging host**; discarding that host **only after all required evidence has been captured**;
**Ubuntu KVM2 VPS deployment**; Gate A, Gate B, WP-V and Gate C **when every documented prerequisite has
objectively passed**; DISARMED deployment and rollback testing; TESTNET configuration, ARM and first
TESTNET paper order; and continuing from one accepted work package to the next without asking again.

Lines 53-57 are explicit that the plan's three separate future owner gates — **the WP-V deployment
approval, the ARM gate, and the first TESTNET paper order** — are granted in advance, and that what is
waived is *the owner having to click approve*, **not any evidence requirement**. Every objective
prerequisite in the Gate A / Gate B / Gate C checklists still applies in full.

### 2.2 Narrower later constraints (controlling)

Two later records narrow the current transition window and were not superseded by a named lift:

- `11_TRIAGE/CODEX_TAKEOVER_HANDOFF_2026-08-02.md:261-263` — "Do not merge to `master`, touch KVM2,
  begin WP-V, or deploy beyond the disposable `GATEA-STAGING` host during this temporary window."
- `11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md:1452-1454` — "**Hard stop — unchanged, needs a new
  explicit instruction from Barış:** merge to master, WP-V / deployment, credential handling, broker or
  exchange access, ARM, orders, TESTNET, mainnet, KVM2, Pine/parity/MTC/trading changes, any economic
  action."

A generic autonomous-continuation instruction does **not** specifically name or lift those task-specific
high-risk stops. Conservative reading controls.

### 2.3 Conservative authority result

| Status | Actions |
|---|---|
| **Authorized now** | Continued read-only and local preparation; evidence reconstruction; scoped documentation; prerequisites planning. The standing prompt supports pre-WP-V programme work. |
| **NOT authorized now** | WP-V; KVM2; master merge; credential load; broker/exchange access; ARM; orders; TESTNET/mainnet; any economic action; deletion of the old payload archive. |

**Do not infer WP-V authority from Gate-A PASS, and do not infer it from generic "continue" wording.**
Those are two distinct inference errors and both are rejected here.

---

## 3. Prerequisites — the canonical sequence after Gate A

`09_DOCS/ROADMAPS/TRADING_SYSTEM/TRADING SYSTEM — 50-HOUR ACCELERATED IMPLEMENTATION PLAN.md` §23a,
"Gated Exit Evidence — Three Sequential Gates", gives the exact order. Each approval authorises only the
named action; **no approval carries forward.** Steps 3–11:

| # | Step |
|---|---|
| 3 | **One named expendable Ubuntu staging action** (authorised only by Gate A): initial WP-I staging deploy + smoke test; retain that host for WP-L Phase 2 — Ubuntu revalidation of all ported paths; then complete WP-I staging verification. The host is **not** discarded at this step. |
| 4 | **Audit 2 (Gate-5)** immediately after WP-L Phase 2 + WP-I staging verification — freeze the exact checkpoint SHA/artifact and obtain an accepting Linux-port/staging verdict **before** WP-A. |
| 5 | **WP-A** 3 h Ubuntu invariant verification **on the retained host**, capturing all required staging evidence. |
| 6 | **Discard the expendable staging host** only after WP-A completes and all required staging evidence has been captured. |
| 7 | **Freeze the exact final release SHA/artifact** (accepted WP-S / WP-L / WP-I / WP-A + any contingency repairs). |
| 8 | **Audit 3 (Gate-5) + Gate-6** as artifact- and evidence-level reviews on that frozen SHA/artifact; no Ubuntu execution, no live host. |
| 9 | **Gate B** (PRE-PRODUCTION-DEPLOY) — requires staging/systemd/SQLite/rollback/WP-A/security/final-SHA/audit evidence; requests the separate WP-V deployment approval. |
| 10 | **WP-V** production deployment — only after that deployment approval. |
| 11 | **Gate C** POST-DEPLOY acceptance. |

The operational runbook states the same immediate sequence in one line —
`11_TRIAGE/GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md:137`:

> `Gate A verification → WP-L Phase 2 → WP-I staging → Audit 2 → WP-A`, all DISARMED.

The same runbook records **why Audit 2 matters beyond sequencing**: Audit 2 **restores the canonical
flagship acceptance floor**. WP-I's candidate acceptance currently rests on a single owner-waived
DeepSeek pass rather than two flagship auditors; that waiver was the owner's call and is valid, but it is
a weaker basis than WP-S received, and **Audit 2 is where that gap closes**.

---

## 4. Current state — what is done, what is owed

### 4.1 Done

- Gate A **A-0..A-9 PASS**, final staging acceptance. **Scope: staging acceptance only.**
- Product candidate remains `2ce41e34bceb599d80af24c5c33d835820ec321b`, unchanged.
- Repo starting HEAD for this discovery: `51e666b0`.

### 4.2 Owed — no completion record exists

`11_TRIAGE/WPL_PHASE1_VERIFICATION_RECORD_2026-08-01.md:17` — "WP-L Phase 1 is **verification only**; no
Ubuntu execution was performed. All Ubuntu evidence below is **owed later** (WP-L Phase 2 — Ubuntu
revalidation / WP-A)."

`11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md:45-46` — "`WP-L Phase 2 — Ubuntu revalidation` has not
occurred and remains post-Gate-A work on the retained authorised staging host."

`11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md:154-168`, "Evidence still owed after final Gate A":

- Retain the one authorised staging host through, in order, **WP-L Phase 2 → WP-I staging verification → WP-A**.
- Prove the lock installs on Ubuntu Python 3.12 and the installed distribution set **exactly equals the
  56-entry lock**.
- Prove **masked/inactive installation, DISARMED start, reboot DISARMED**, and **SIGTERM** clean shutdown
  with no dangling state.
- Prove **SQLite backup/restore** and risk/history continuity.
- Execute **rollback**, preserve state, prove zero writers, keep any recovery start behind its separate gate.
- Capture **actual egress**, confirm TESTNET-only destinations, optional Telegram disposition,
  loopback-only `127.0.0.1:8790`, and **no mainnet traffic**.
- Execute **WP-A's DISARMED restart/reconnect/stale-data invariants** and capture the evidence **before**
  discarding the host.

Note the same record's line 150-152: Gate A itself authorises only one named expendable Ubuntu staging
action; it does **not** mean staging, Ubuntu proof, or WP-A had already occurred.

### 4.3 The host

`GATEA-STAGING` is the named clean expendable host, provenance proven in
`11_TRIAGE/GATE_A_STAGING_HOST_PROVENANCE_2026-08-02.md:105-117` (Gen 2, Secure Boot on, 4 vCPU / 4 GB
static, 40 GB fresh VHDX, checkpoints disabled, Nothing/TurnOff start-stop action, Default Switch, seed
ISO sha256 `a83d6cc2…54af2`, VM-only ed25519 keypair with **no password**).

The current transition inventory proves it **still exists and remains safely active/running,
credential-free DISARMED, with only candidate `2ce41e34…321b` installed. It has not been discarded.**

Therefore step 6 (discard) has **not** been reached, and the host required by steps 3–5 is still
available — which is the fortunate case, not the blocked one.

---

## 5. Blockers

### 5.1 BLOCKER 1 — authority (transition-scope)

WP-V / KVM2 / master merge / credentials / broker / ARM / orders / TESTNET / mainnet / economic action
are stopped by `CODEX_TAKEOVER_HANDOFF_2026-08-02.md:261-263` and
`NEXT_SESSION_HANDOFF_2026-08-08.md:1452-1454` until a **new explicit instruction names them**. The
broad standing prompt does not resolve this, because it conditions those actions on every objective
prerequisite having passed — and §4.2 shows they have not.

### 5.2 BLOCKER 2 — budget

`11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md:1489-1492`: "≈14–17 h of the 50-hour plan remained before
this session; WP-A (3 h), WP-R (6 h) and WP-V (8 h) total 17 h and are all still ahead. The A-4 repair,
its artifact rebuild and its flagship round are **again unbudgeted work**, as the Gate A repair queue
was. **Re-plan with Barış before committing to the remainder** rather than absorbing it silently."

**The exact current hour ledger is not reconstructed.** The accepted plan carries a hard 50-hour ceiling
and no silent overrun is permitted. WP-A + WP-R + WP-V alone (17 h) already meet or exceed the upper end
of the remaining estimate **before** counting WP-L Phase 2, WP-I staging verification, or Audit 2.

**This blocker does not require idling.** It bounds what may be *committed to*, not what may be
*prepared*.

---

## 6. Next safe unit — autonomous, read-only/local

1. **Reconstruct package-by-package hour accounting.** Classify Gate-A repair work against contingency
   versus outside-budget. **Do not invent hours.** Where a figure is not evidenced, record it as
   unevidenced rather than estimating it into the ledger.
2. **Build a post-Gate preregistration / gap matrix** covering **WP-L Phase 2 + WP-I staging
   verification + Audit 2 + WP-A**, from the existing records and the exact candidate/service state.
3. **No server execution until that package proves** its command scope, evidence outputs, stop
   conditions, and budget/authority fit.
4. **Keep `GATEA-STAGING` retained and credential-free DISARMED. Do not discard it.**

Prefer continuing independent safe units over asking routine questions.

---

## Next steps

1. **[AI: Any]** Reconstruct the package-by-package hour ledger from repository evidence; classify
   Gate-A repair/rebuild/audit work as contingency versus outside-budget; mark unevidenced figures as
   unevidenced. Read-only.
2. **[AI: Any]** Write the post-Gate preregistration/gap matrix for WP-L Phase 2 + WP-I staging
   verification + Audit 2 + WP-A: per item, the exact command scope, exact evidence output path, the
   preregistered PASS/FAIL predicate, the stop condition, and its budget/authority fit. Read-only/local.
3. **[AI: Any]** Keep `GATEA-STAGING` retained, active, credential-free DISARMED; take no service,
   package, credential, or network action against it.
4. **[AI: Barış]** Re-plan the remaining hours against the 50-hour ceiling before any further execution
   is committed to.
5. **[AI: Barış]** A named explicit lift is required before WP-V, KVM2, master merge, credential load,
   broker/exchange access, ARM, orders, TESTNET/mainnet, economic action, or old-payload deletion.

**Default path:** execute steps 1–3 autonomously in that order, then report; do not touch staging.

## Stop conditions

- Any request to execute **WP-V, KVM2, master merge, ARM, credentials, broker, orders, or economic
  action** without an explicit named lift.
- Any required WP-L Phase 2 / WP-I / WP-A evidence that would need a **product repair** to satisfy —
  that changes the frozen-SHA and re-audit picture (plan §23a repair loop) and is not a documentation unit.
- Any **budget claim that cannot be evidenced** — record it as unevidenced and stop rather than estimate.
- Any **service drift** on `GATEA-STAGING` from active/running, credential-free DISARMED, single
  loopback `127.0.0.1:8790` listener, candidate `2ce41e34…321b` only.

---

**Scope statement:** this record is read-only discovery. It asserts no Gate, grants no authority,
performs no cutover, and **ran no staging command**.
