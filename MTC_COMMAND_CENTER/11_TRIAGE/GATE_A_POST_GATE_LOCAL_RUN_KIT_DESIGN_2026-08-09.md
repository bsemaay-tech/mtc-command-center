# Gate A — Post-Gate LOCAL RUN-KIT **DESIGN CONTRACT** (Stage B read-only · C1 stop · C2 reboot · C3 WAL bundle · C4 rollback · C5 blocked)

> # ⛔ STATUS BANNER — READ BEFORE ANY OTHER LINE
>
> - **NOT EXECUTED.** Nothing in this document was run. Every command shape below is a *proposed
>   future* shape for a later implementer to author and a later authority to approve.
> - **NO HOST CONTACT.** This unit made no SSH, sudo, systemctl, reboot, service, curl, network,
>   broker, exchange, credential, ARM/order, package/install, or staging-host call of any kind.
>   `GATEA-STAGING` was not contacted. No product test was run. No Git mutation, staging or commit
>   occurred.
> - **THIS DOCUMENT IS NOT EXECUTION AUTHORITY.** It confers no permission to run anything. Every
>   stage below remains gated behind a separate, explicitly named human lift.
> - **The exact 50-hour balance is NOT REPRODUCIBLE**
>   (`GATE_A_50H_LEDGER_RECONSTRUCTION_2026-08-09.md`, state 5). Budget compliance for any
>   *server-executed* post-Gate work therefore cannot be proven.
> - **Consequently every host-touching and every mutating stage in this design is BLOCKED**, pending a
>   human budget re-plan or explicit ceiling extension **and** the per-stage authority lift named in
>   §11. That includes the read-only Stage B: read-only is not free, and §1 of the accepted matrix
>   holds it with everything else.
> - **`RK-C1` is BLOCKED FROM EXECUTION on design grounds as well**, independently of budget and
>   authority. Two of its gaps are **blocking**: the exact clean-stop `ExecMainStatus`/`Result` tuple
>   (`D-GAP-C1-1`, §5.2) and the exact safe **active-writer pre-stop capture method** (`D-GAP-C1-3`,
>   §5.4). Until both are closed and frozen in `RK-PRE`, `RK-C1` **may not be run and cannot obtain a
>   PASS** — not under a weakened warning-class baseline, not with no baseline at all, and never
>   against a post-stop "baseline". Everything downstream of it (`RK-C3`, `RK-C4`, `RK-C2/B`)
>   inherits that block.
> - **This is a design contract, not a run-kit.** It deliberately produces no runnable script. Its
>   purpose is to let a later implementer author one safely, and to let auditors preregister exact
>   behaviour without improvising on the server.

---

## 0. Unit record

| Field | Value |
|---|---|
| **Date** | 2026-08-09 |
| **Unit type** | Bounded **design-only** unit on a protected Bridge deployment / runtime / persistence / reboot / rollback evidence surface. **Read-only / local.** |
| **Model / route** | `claude-opus-5`, effort `xhigh`, fresh independent session (owner-specified exact model and effort) |
| **Worktree** | `C:\PGRK`, clean detached worktree |
| **Documentation / governance HEAD** | `4599b466def320cd4afeeb238e0e192303bd85c4` (`git status --short` empty at start and at end) |
| **Frozen / deployed product candidate** | `2ce41e34bceb599d80af24c5c33d835820ec321b` (**unchanged**) |
| **Merge base (divergent refs)** | `4d2228cf8985ce755c398cceff23f777a99d5404` |
| **Exact write** | **one new file only** — this document. |
| **Commands executed** | read-only Git and read-only local file reads only (`git status`, `git rev-parse`, `git log`, `git show`, `git grep`, `ls`). **No** Git mutation of any kind (no add/commit/push/checkout/switch/reset/stash/clean/branch/tag/worktree-mutation). |
| **Contaminated path** | `C:\tmp\postgate_runkit_design_claude` was **neither inspected nor reused**, per the task contract. |

### 0.1 Non-actions (explicit)

No AI_MEMORY file, handoff file, WP0 record, product file, deploy asset, runtime file, tool, test,
script or schema was read *for the purpose of editing* and **none was modified**. `AI_MEMORY` and
handoff updates are **Lead-owned after acceptance** and were deliberately not performed here (§13).

### 0.2 Mandatory routing record

```
Classification          : Tier 4 — protected Bridge deployment / runtime / persistence / reboot /
                          rollback evidence design (not ordinary coding, not bounded mechanics)
Protected               : YES. Bridge surface touching deployment, systemd runtime, SQLite
                          persistence, reboot safety and rollback. Gate 1 has NOT classified any of
                          it unprotected, so the standing Bridge default in AGENTS.md
                          (§GLM SUPPLEMENTAL ROUTING, "Bridge default") applies: protected → Tier 4.
Model + provider        : claude-opus-5, effort xhigh, Anthropic via Claude Code CLI.
                          This is an OWNER-SPECIFIED EXACT-MODEL request (AGENTS.md routing example
                          6: honour it, no silent fallback or downgrade). It is NOT a Z.AI route;
                          the GLM tier table is cited only as the classification instrument.
Cheaper-model rationale : No tier below flagship is admissible.
                          - Tier 1 (4.5-Air) and Tier 2 (4.7) are excluded by the Bridge default and
                            by the task's own protected classification.
                          - Tier 3 (GLM-5.1) is excluded twice: entitlement is not confirmed on the
                            Coding Plan (AGENTS.md), and the task is not "moderate debug".
                          - Tier 4 GLM-5.2 is the correct *tier* but is the wrong *model* here: the
                            accepted provenance repair records that GLM-5.2 authored the predecessor
                            matrix and produced defects G8/G9/G10 by reading product files from the
                            divergent documentation checkout. This unit's core obligation is exactly
                            the discipline that failed there (candidate-qualified provenance,
                            expected-vs-observed separation). AGENTS.md D025 rule 4 records the
                            related GLM-5.2 failure mode by name.
                          - Downgrading would also violate the owner's explicit instruction.
Exact paths (read)      : MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md
                          MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md
                          MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_TRANSITION_INVENTORY_2026-08-09.md
                          AGENTS.md, CLAUDE.md, MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md
                          at 2ce41e34…321b: IBKR_PAPER_BRIDGE/deploy/linux/{verify.sh,verify_lock.py,
                            install.sh,rollback.sh,COMMANDS.md,lib/common.sh,
                            env/mtc-bridge.env.template,systemd/mtc-bridge-first-start.service.template}
                            IBKR_PAPER_BRIDGE/bridge/app.py, IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py
Exact paths (write)     : MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_LOCAL_RUN_KIT_DESIGN_2026-08-09.md
                          (exactly one new file; no other path touched)
Context/tool budget     : single session; targeted `git show` / `git grep` at the candidate plus
                          bounded ranged reads of three accepted records. No full-repo scan, no
                          full-file read of any file over ~500 lines except by bounded ranges.
Fallback                : if claude-opus-5 at xhigh were unavailable, STOP as BLOCK and report to
                          Barış (AGENTS.md: "If exact model/effort unavailable: stop as BLOCK unless
                          Barış explicitly waives it"). Do not silently substitute a lesser model on
                          a protected design surface.
External API credits    : NO. No external API, no board run, no network call, no paid provider.
```

---

## 1. Binding provenance and epistemic contract (inherited, non-negotiable)

This design inherits and obeys the three accepted mitigations from the provenance repair.

| Rule | Source | Effect on this document |
|---|---|---|
| **G8 — path provenance** | matrix §3 G8 | Every product/deploy/runtime/tool/test fact is written commit-qualified as `2ce41e34…321b:<path>:<line>`, obtained by `git show`/`git grep` at the candidate. Bare `<path>:<line>` would be unverified and is not used for candidate facts. |
| **G9 — hash-input provenance** | matrix §3 G9 | Every hash names its input: *Git blob object ID (SHA-1)* / *raw blob content SHA-256 (LF)* / *worktree checkout SHA-256* / *observed host SHA-256*. No content hash is derived by hashing a Windows checkout. |
| **G10 — epistemic provenance** | matrix §3 G10 | Every hash and every host predicate carries **expected-from-source** vs **observed-on-host**. An expectation is written "expected …, to be compared against". An observation requires a captured command and its output. |

### 1.1 Epistemic tags used throughout

| Tag | Meaning |
|---|---|
| `[SRC]` | Established by read-only Git at the frozen candidate `2ce41e34…321b`. |
| `[REF-INV]` | Established at a blob that is byte-identical on the candidate and documentation refs (matrix §4b). Either citation valid; still written candidate-qualified. |
| `[GOV]` | Governance/evidence artifact, **not** candidate payload. `SECURITY_BASELINE.md` is `[GOV]` — it is **ABSENT** from the candidate (`git rev-parse 2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` → `fatal: … exists on disk, but not in '2ce41e34…'`). It may describe candidate analysis; it may never be cited as candidate source. |
| `[HOST-OBS]` | A value someone actually measured on `GATEA-STAGING` and recorded with its command/output. |
| `[SYSTEMD]` | External systemd semantics (documented systemd behaviour), not a candidate-source fact and not a host observation. Flagged wherever load-bearing. |
| `[EXPECT]` | Derived from `[SRC]`/`[REF-INV]`, **not observed**. Preregistered as a predicate *to be tested*. |
| `[GAP]` | Not established by any of the above. Carried openly as a named design gap (§10). **Never silently upgraded to an asserted host fact.** |

### 1.2 The four lock identities — kept distinct, permanently

| # | Kind | Value | Status |
|---|---|---|---|
| 1 | **Git blob object ID (SHA-1)** of `IBKR_PAPER_BRIDGE/requirements.lock` | `47f53fa227bf0f18b9bf9bd77e060d8856961728` | `[REF-INV]` — identical at `2ce41e34…321b`, `851d2aa5`, `f8a6bc0f`, `637307e8`. **Not a content hash.** |
| 2 | **Raw blob content SHA-256 (LF, 117 762 B)** | `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e` | `[EXPECT]` for the host. Established as the committed/packaged byte identity: `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/package.sh:78-83` exports LF-pinned. **Preregister as the *expected* value only.** |
| 3 | **Windows worktree checkout SHA-256 (CRLF, 119 274 B)** | `40873556a7f4586d77f165b985863138c9fc95b095da64ac52456b8c49098ec3` | ⛔ **NEVER CITE. NEVER A LINUX PREDICATE.** A local `core.autocrlf=true` artifact; `119 274 − 117 762 = 1 512` = the blob's exact line count. It does not appear anywhere in this design as an expected value, and any future run-kit that preregisters it is defective by construction. |
| 4 | **Observed installed-host value** — `sha256sum` of the installed lock, and `/etc/mtc-bridge/install_manifest.json` → `requirements_lock_sha256` | **NOT IN EVIDENCE** | ⛔ **Open read-only host predicate (B1a).** Never captured in any located record (repair-record §2.7g). Blocked with all host action. |

**Binding rule for every stage below:** value 2 is written as *expected*; value 4 is written as
*to be observed*; value 3 never appears as a predicate; value 1 is never called a content hash.

### 1.3 WP0 is correct and uneditable in this task

All 11 WP0-mapped test symbols exist at the frozen candidate (matrix §4, repair-record §5), including
`test_kill_restart_after_request_commit_keeps_killed_and_resumes_once` at
`2ce41e34…321b:IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py:2765`.
`WP0_SCOPE_BASELINE_RECORD_2026-07-31.md` lines 308 and 364 are correct as written. **G4 stays
withdrawn. No WP0 edit is proposed, implied, or permitted by this design.**

---

## 2. Cross-cutting design rules (bind every stage)

### 2.1 Stage IDs, classes and dependency order

Mutation classes, as in the accepted matrix §2: `local-static` (no host at all) ·
`read-only-host` (asserts only) · `mutating-host` (needs its own named authority) · `blocked`.

| Stage ID | Name | Class | Depends on | Status |
|---|---|---|---|---|
| `RK-PRE` | Local preregistration freeze + expectation-file hashing | `local-static` | — | Authorable **now**; produces no host contact |
| `RK-B0` | Evidence-root allocation + expectation pin (on host) | `read-only-host` | `RK-PRE` | Blocked (§11) |
| `RK-B1` | Python 3.12 + `verify_lock --check-installed` parity, `packages=56` | `read-only-host` | `RK-B0` | Blocked |
| `RK-B1a` | **Observed** installed `requirements.lock` byte identity + manifest field | `read-only-host` (root read) | `RK-B0` | Blocked — **currently NOT IN EVIDENCE** |
| `RK-B2` | Service identity: active, SHA/venv binding, `Restart=no`, `NRestarts=0`, `is-enabled=static`, unmasked | `read-only-host` | `RK-B0` | Blocked |
| `RK-B3` | Bounded stat/ownership/symlink subset of `verify.sh` (**not** wholesale) | `read-only-host` (root read) | `RK-B0` | Blocked |
| `RK-B4` | Effective systemd hardening + exact start-mode unit pin + env-file no-override (**name-only**) | `read-only-host` (root read) | `RK-B0` | Blocked |
| `RK-B5` | Status API DISARMED, all network/exchange/credential/ARM flags off | `read-only-host` | `RK-B0` | Blocked |
| `RK-B6` | Exactly one `127.0.0.1:8790` listener · UFW SSH-only · external-origin probe unreachable | `read-only-host` + external probe | `RK-B0` | Blocked |
| `RK-B7` | Closeout: evidence manifest, external SHA-256, local no-clobber retrieval | `read-only-host` | `RK-B1..B6` | Blocked |
| `RK-C1` | Graceful `systemctl stop` / no dangling state | `mutating-host` | `RK-B7` accepted | **BLOCKED TWICE** — budget/authority (§11) **and** design: `D-GAP-C1-1` and `D-GAP-C1-3` are open and **blocking**, so `RK-C1` may not be executed and cannot obtain PASS (§5.2, §5.4) |
| `RK-C2/A` | Reboot safety — **bounded C2-only branch**, plain reboot from active + unmasked | `mutating-host` | `RK-B7` accepted | Blocked (budget/authority) + carries `D-GAP-C2-1`. **Terminal branch:** it ends inactive + unmasked and **no Group C stage follows it** (§2.2) |
| `RK-C2/B` | Reboot safety — reboot from inactive + masked | `mutating-host` | `RK-C4` accepted | Blocked; inherits the `RK-C1` design block through Chain B |
| `RK-C3` | WAL bundle · verify · restore-into-temp · invariant comparison | `mutating-host` | `RK-C1` accepted (quiesced window) | Blocked; inherits the `RK-C1` design block |
| `RK-C4` | Rollback stop+mask **only** (no rebind) | `mutating-host` | `RK-C3` accepted | Blocked; inherits the `RK-C1` design block |
| `RK-C5` | Runtime broker egress capture | **blocked** | different start mode + credential + TESTNET/broker authority | **Not authorisable now** |
| `RK-REC` | Recovery start / unmask | `mutating-host` | separate authority unit | **Out of scope of this design** |

### 2.2 The two branches — one bounded and terminal, one full — and the ordering each imposes

`RK-C2` has two scenarios with *different starting states*. **A future execution must freeze exactly
one before the reboot and record the freeze in `RK-PRE`.** They are **not** two orderings of the same
stage set: Scenario A is a **bounded, terminal, `RK-C2`-only branch**, and only Chain B contains the
full Group C sequence.

```
Branch A (bounded C2-only plain reboot) — TERMINAL:
    RK-PRE → RK-B0..B7 → RK-C2/A (reboot from ACTIVE + UNMASKED)
    → the branch ENDS with the host INACTIVE + UNMASKED
      (no [Install], no auto-start — proven by checks 1..10 of §6.2).
    ⛔ NOTHING in Group C follows it. There is NO RK-C2/A → RK-C1 edge: after the reboot the
       service is inactive, and RK-C1's predicate — "one authorised graceful stop of the RUNNING
       service left no dangling state and did not mutate protected persistent state" — has no
       running service to stop and no live pre-stop baseline to take.

Chain B — the ONLY coherent full chain in this design:
    RK-PRE → RK-B0..B7 → RK-C1 → RK-C3 → RK-C4 → RK-C2/B (reboot from INACTIVE + MASKED) → [RK-REC]
             ^ every POST-stop DB capture in this chain happens with the writer already stopped.
               The RK-C1 PRE-stop baseline (§5.4) is NOT one of them: it must be taken with the
               writer ACTIVE — D-GAP-C1-3 — and Chain B schedules no pre-stop capture at all.
    ⛔ BLOCKED AT ITS FIRST GROUP-C STAGE. RK-C1 may not run until D-GAP-C1-1 (§5.2) and
       D-GAP-C1-3 (§5.4) are closed and frozen in RK-PRE. RK-C3, RK-C4 and RK-C2/B inherit that
       block by dependency.
```

**Reaching `RK-C1` after Branch A requires a recovery start, and this design does not include one.**
The path would be, in order: **(1)** a **separately authorised `RK-REC`** start/unmask — out of scope
here (§2.1, §11), never silently appended to `RK-C2/A` or to any other stage; **(2)** a **fresh,
accepted Stage B recapture** against the restarted service, because every `RK-B` assertion taken
before the reboot describes a *different process instance*, and `is-active`/`MainPID`/`NRestarts`/
`is-enabled`/binding/hardening/listener facts are not inherited across a reboot plus a restart; and
only then **(3)** `RK-C1`, still subject to its own blocking gaps. **No part of that path is
authorised, designed, costed or implied by this document, and no run-kit may assemble it implicitly
by running `RK-C2/A` and then continuing.**

**Which branch to freeze — the trade, stated plainly.** For the *reboot capture only*, Scenario B
avoids `D-GAP-C2-1`: in Branch A the pre-reboot persisted-state capture must be taken while the
service is ACTIVE, and no exact safe command for that is established (§6.4). Scenario B's pre-reboot
capture happens with the writer already stopped. Chain B pays for that with `RK-C1`, which is itself
blocked from execution (§5.2, §5.4), so **Chain B as a whole is not runnable today**, while Branch A
is bounded and self-contained — subject to budget/authority and to `D-GAP-C2-1` — and never touches
`RK-C1`. **Neither is a decision this unit is authorised to make**; both go to the Lead in §13 with
their costs stated.

### 2.3 Placeholder format and no-clobber allocation

Placeholders exist **only** where a value is intentionally allocated at a future freeze. Each has a
defined format and an allocation rule. **No placeholder may be filled by invention.**

| Placeholder | Format | Allocation rule | Filled by |
|---|---|---|---|
| `<RUNID>` | `RK-<STAGE>-<YYYYMMDD>T<HHMMSS>Z` (UTC, e.g. `RK-B-20260812T094500Z`) | `date -u +%Y%m%dT%H%M%SZ` at stage start; written to `<EVROOT>/00_runid.txt` as the first byte of the stage | future execution |
| `<EVROOT>` | `/home/gatea/runkit/<RUNID>` | `mkdir -p /home/gatea/runkit` **then** plain `mkdir "<EVROOT>"` — **never `-p` on the leaf**. POSIX `mkdir` fails with `EEXIST`, so the leaf is no-clobber by construction. Non-zero rc ⇒ **STOP** | future execution |
| `<LOCAL_EVROOT>` | `C:\WPI_ARTIFACTS\runkit\<RUNID>` | must exist **neither as a filesystem object nor as a symlink** (dangling included); create then copy. Any existing path, link or reparse point ⇒ **STOP**, never overwrite. A probe that cannot complete ⇒ **STOP**, never "assume absent" | future execution |
| `<PAYLOAD_MANIFEST_SHA256>` | 64 lowercase hex | **Read from accepted A-2 local evidence** (`C:\WPI_ARTIFACTS\2ce41e34…321b\RELEASE_SHA256SUMS` and the A-2 install capture) during `RK-PRE`, before any host step. **Never invented, never guessed, and never confused with the lock hash** | `RK-PRE` |
| `<HOST_IP>` | the staging host's external address | taken from the operator's existing SSH configuration at execution time. **Never written into a committed record** | future execution |
| `<OBSERVED_LOCK_SHA256>` | 64 lowercase hex | **output** of `RK-B1a`. Currently **NOT IN EVIDENCE** | `RK-B1a` |
| `<PRE_INVARIANTS_SHA256>`, `<PRE_BUNDLE_DB_SHA256>` | 64 lowercase hex | **outputs** of the pre-state capture of the frozen chain | `RK-C1`/`RK-C2` |
| `<BUNDLE_DB_SHA256>`, `<INVARIANTS_SHA256>` | 64 lowercase hex | **outputs** of `RK-C3` `create`, read from the capture report's `bundle_db_sha256` / `invariants_sha256` fields (`2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/COMMANDS.md:134-140` pattern `[REF-INV]`) | `RK-C3` |
| `<MANIFEST_FILE_SHA256>` | 64 lowercase hex | **output** of `RK-C3`: the **external** `sha256sum` of the bundle manifest *file*, not a value read from inside the JSON | `RK-C3` |

### 2.4 Universal no-clobber artifact contract

Every planned output of every stage obeys all of these:

1. **Path is inside `<EVROOT>`** (or `<LOCAL_EVROOT>` for retrieved copies), which is itself
   no-clobber-allocated per §2.3.
2. **Canonicalised and non-symlink.** Before writing, assert the target and every parent is not a
   symlink and canonicalises beneath `<EVROOT>` (`realpath -e`/`readlink -f` compared against
   `<EVROOT>`). This mirrors `assert_not_symlink` at
   `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/lib/common.sh:72-77` `[SRC]` and the canonical-path
   sweep at `…/verify.sh:45-52` `[SRC]`.
3. **Absent before write — and a dangling symlink is NOT absent.** Immediately before any write,
   rename or publication the destination must hold **no filesystem entry of any kind**, symlinks
   included. A dangling symlink satisfies `! -e` while still redirecting `>` and `mv -T` onto its
   target, so an `-e`-only check is not a no-clobber check. The assertion is made with the §2.5a
   `classify_path` helper and the required token is **`NONE`** — which that helper emits only when
   `os.lstat` raised `FileNotFoundError`, never as a fallthrough from a failure; `FILE` **or** `LINK`
   is a **STOP**, and a probe that does not complete is a **STOP** — never "assume absent". Any
   pre-existing target is a **STOP**, never an overwrite, never a rename-and-continue.
4. **SHA-256 recorded** for every produced artifact, computed with `sha256sum` on Linux
   (`sha256_of` pattern, `…/lib/common.sh:222` `[REF-INV]`), and labelled `observed-on-host`.
5. **Failure preserves everything.** On any FAIL/STOP, all `.cmd`/`.out`/`.err`/`.rc` files and all
   partial artifacts stay exactly where they are. Nothing is deleted, truncated, renamed to a
   published name, or retried in place.
6. **Never publish a partial artifact under an accepted name.** Staging→publish is atomic and
   one-way (§7.6).

### 2.5 Command / stdout / stderr / exit-status recording contract

Every host command in every stage is recorded as a four-file group:

```
<EVROOT>/<NN>_<slug>.cmd   # the exact argv, one line, written BEFORE execution
<EVROOT>/<NN>_<slug>.out   # stdout, verbatim
<EVROOT>/<NN>_<slug>.err   # stderr, verbatim
<EVROOT>/<NN>_<slug>.rc    # the integer exit status, written AFTER execution
```

`<NN>` is a zero-padded monotonically increasing sequence within the stage. Required properties:

- The `.cmd` file is written **before** the command runs, so an aborted command still leaves a record
  of what was attempted.
- **A non-zero rc is recorded, then adjudicated immediately — it is never carried forward.** The
  recording helper disables errexit **only for the single command invocation**, for exactly long
  enough to capture `$?` (and `PIPESTATUS`) into `.rc`, and re-enables it on the next line.
  Adjudication against the preregistered predicate table happens **at that point**, before the next
  command in the stage is composed. This is deliberately *not* `set -Eeuo pipefail`'s
  abort-on-first-failure — that would destroy the `.rc` evidence of the failing check itself — and it
  is equally *not* a licence to keep going.
- **⛔ What "recorded, not fatal" does NOT mean.** It does **not** license later checks to run after a
  failed prerequisite, and it does **not** license a stage to accumulate results and adjudicate at
  the end. **If adjudication of a recorded rc yields STOP, no later command in that stage or chain
  may execute** — not another check, not a "harmless" read, and above all **not a mutation**. Every
  mutation in this design sits behind a precondition, and **no mutation may follow a failed, an
  unadjudicated, or an unrecorded precondition.** The rc is captured so the failure is *evidenced*;
  the failure still halts the stage at that line (§2.5a `STOP`, §12 "After a STOP").
- **`|| true` is forbidden** on any fail-closed check. The candidate's own verifier uses `|| true`
  only because it accumulates `MTC_FAILURES` and exits non-zero at the end
  (`…/verify.sh:79-81,248-250,253-258` `[SRC]`); a run-kit that drops the accumulator and keeps the
  `|| true` converts a failure into a silent pass. Adjudication is by table, not by shell status.
- **⛔ `cmd && echo A || echo B` is forbidden for the same reason, and is a worse form of it.**
  `test … && echo PRESENT || echo ABSENT`, `if sudo test -e …; then …; else <benign token>; fi`, and
  every relative of them **erase the distinction between a false predicate and a failed probe**: a
  permission denial, a `sudo` policy rejection, a missing tool, an I/O error or a race all land in
  the same branch as the benign answer, and the group's `.rc` then records the status of `echo`,
  which is `0`. The result is a fabricated `ABSENT` / `NOTLINK` / `MISSING` / `NOT-MASKED` line that
  reads as a PASS. **A permission, tool or race error is a STOP, never a benign token.** Every
  existence, symlink, ownership, count, process-presence and listener predicate is instead expressed
  through the §2.5a helpers, which are **three-way**: true, false, or STOP.
- **Pipelines mask rc.** `a | b` reports only `b`'s status, so `ss … | awk …` exits `0` with empty
  output when `ss` failed — indistinguishable from "no listener". Every recorded pipeline runs under
  `set -o pipefail`, and the whole `PIPESTATUS` vector is written into `.rc` beside the final status.
  A non-zero member anywhere ⇒ **STOP**, never an empty-output PASS.
- **No `SKIP` disposition exists** anywhere in this design. A check that cannot be performed is a
  **STOP**, not a skip and not a pass. This is stated again per-stage because it is the single most
  likely way for a future run-kit to launder a gap into an apparent PASS.

### 2.5a Fail-closed predicate helpers — three-way, never two-way (binding)

Every predicate in this design has **three** outcomes, never two: **true**, **false**, and **STOP —
the predicate could not be evaluated**. The third is the one shell idioms destroy, so predicates are
expressed only through the helpers below. They are specified here once and referenced by every stage;
a run-kit that re-implements a predicate inline with `&&`/`||` violates §2.5 and §12(14).

**(H0) `STOP` — adjudication is immediate and terminal.**

```bash
# NOT EXECUTED — proposed shape only.
STOP() {                     # halt the stage HERE; nothing later runs, and no mutation follows
  printf 'STOP %s\n' "${1:-predicate not evaluable}" >&2   # stderr ONLY — no artifact is written
  exit 90                    # §2.5: the rc is already recorded; §12 "After a STOP" governs the rest
}
```

**⛔ `STOP` writes no artifact of its own, deliberately.** An earlier shape appended the reason to a
shared `${EVROOT}/99_stop.txt` with `>>`. That is an **unchecked write at the worst possible moment**:

- `>>` **creates** the file if it is absent and **follows a symlink** at that path if one is there, so
  a link planted (or left) at `99_stop.txt` redirects the write outside `<EVROOT>` entirely — the
  exact hazard §2.4(3) and §7.6 exist to prevent, committed by the helper that is supposed to be
  halting the run.
- It **appends to a prior run's or a prior stage's record**, so one stage's failure text lands in an
  artifact another stage already produced — evidence contamination, and §2.4(5) requires artifacts to
  stay exactly as they are after a STOP.
- Asserting `classify_path … = NONE` on `99_stop.txt` first cannot rescue it: the probe may itself be
  the thing that just failed, and a *second* STOP inside `STOP` recurses.

**`STOP` is never called from inside a command substitution.** `exit` within `$( … )` ends only the
subshell, so a helper that called `STOP` there would halt nothing. That is why `classify_path`,
`priv_rc` and `count_rc*` **return rc `2`** and the *caller* — running in the stage shell — calls
`STOP`.

**Nothing is lost by removing the write.** `STOP` is only ever called from inside a §2.5 recorded
group, whose four-file recorder is already capturing this process's **stderr into `.err`** and its
**exit status into `.rc`** (H4). The reason string and the status therefore land in the in-flight
group's own artifacts, correctly attributed to the command that failed, with no extra write, no
clobber risk and no symlink exposure. A run-kit that wants a run-level index of STOPs derives it by
reading the `.rc`/`.err` files after the fact — never by writing during the halt.

**(H1) `sudo_rc` — prove the privileged command actually ran.**
`sudo` itself exits `1` when its policy refuses, which is exactly the status `test`, `grep` and
`pgrep` use for a legitimate "false". Conflating them is how a permission failure becomes a PASS, so
every privileged command is run through a sentinel wrapper that re-encodes the *inner* status out of
the ambiguous range:

```bash
# NOT EXECUTED — proposed shape only.
sudo_rc() {                  # usage: out=$(sudo_rc <argv…>) ; rc=$?
  sudo sh -c 'set +e; "$@"; s=$?; [ "$s" -gt 60 ] && s=60; exit $((100 + s))' _ "$@"
}
priv_rc() {                  # usage: rc=$(priv_rc "$rc") || STOP  -> echoes the INNER status
  case "$1" in
    1[0-5][0-9]|160) printf '%s\n' "$(( $1 - 100 ))" ;;
    *)               return 2 ;;   # sudo policy / transport / exec failure => STOP, never a token
  esac
}
```

An rc outside `100..160` means the inner command **never ran to completion**. That is a **STOP**, and
it may not be mapped onto any predicate token.

**(H2) `classify_path` — one exception-aware probe, one token, dangling symlinks separated.**

**⛔ Why a shell probe cannot implement this predicate, even behind a sentinel.** `[ -L "$p" ]` and
`[ -e "$p" ]` are **two-way**: `test` answers *false* for a permission denial on a parent directory,
for `ENOTDIR`/`ELOOP`/`ENAMETOOLONG` path-resolution failures, for an I/O error on the underlying
device, and for a vanished mount **exactly as it answers false for a genuine absence**. An
`if [ -L ] … elif [ -e ] … else NONE` chain therefore *converts every inner failure into the token
`NONE`* — which is the PASS token for every no-clobber destination in this design — and it does so
**before** any sentinel is reached, so the sentinel then certifies the forgery. A wrapping
`sudo sh -c '…; exit 90'` proves only that `sh` ran to its last line; it is **not** evidence that
`test` ever evaluated the path, and treating it as such is the same two-way collapse one layer out.

The probe must instead come from a primitive that reports *why* it could not answer.
**`os.lstat` is that primitive:** it raises `FileNotFoundError` for "no such entry" and a *different*
`OSError` subclass for every other reason, so absence and non-answerability are structurally
distinct rather than both being "false". `lstat` — not `stat` — is also what separates a **dangling
symlink** from an absence: a dangling link raises `FileNotFoundError` under `stat` but returns an
`S_ISLNK` mode under `lstat`, and `>` / `mv -T` follow it onto its target.

**Prerequisite and ordering (binding).** The probe runs under the per-SHA venv interpreter
`${PY}` = `/opt/mtc-bridge/venvs/<SHA>/bin/python` — the interpreter §4.1 `RK-B1` asserts is exactly
`3.12` (`2ce41e34…321b:…/deploy/linux/verify.sh:104-115` `[SRC]`). **That assertion is a
prerequisite of every `classify_path` call in the run.** It is therefore recorded as the **first**
command of §4.0 `RK-B0`, *before* `RK-B0`'s own no-clobber probe, and §4.1 `RK-B1` predicate (1)
re-records the same assertion as its stage predicate. **No stage may call `classify_path` before that
assertion has been recorded and adjudicated PASS**; an interpreter that is missing, is not `3.12`, or
does not run is a **STOP**, and no probe is attempted on an unverified interpreter.

```bash
# NOT EXECUTED — proposed shape only.
PY=/opt/mtc-bridge/venvs/${SHA}/bin/python   # verified 3.12 by RK-B0 step 1 / RK-B1 predicate (1)
probe_path() {               # $1 = "" (unprivileged) | "sudo" ; $2 = absolute path
  # exit 90 = the probe RAN and adjudicated the path; the token on stdout is its answer
  # exit 91 = os.lstat raised a NON-FileNotFoundError OSError => the path was NOT adjudicated
  # any other status (sudo policy refusal 1, exec failure 126/127, signal, absent interpreter) => STOP
  ${1:+sudo} "${PY}" -c '
import os, stat, sys
try:
    st = os.lstat(sys.argv[1])
except FileNotFoundError:            # ENOENT ONLY — the single route to NONE
    sys.stdout.write("NONE\n"); raise SystemExit(90)
except OSError:                      # EACCES, EPERM, ENOTDIR, ELOOP, ENAMETOOLONG, EIO, ESTALE, …
    raise SystemExit(91)             # not answerable => STOP, never NONE
sys.stdout.write("LINK\n" if stat.S_ISLNK(st.st_mode) else "FILE\n")
raise SystemExit(90)
' "$2"
}
classify_path() {            # $1 = "" | "sudo" ; $2 = path -> LINK|FILE|NONE, or rc 2 = STOP
  local tok rc
  tok=$(probe_path "$1" "$2") ; rc=$?
  [ "$rc" -eq 90 ] || return 2                   # 91, or ANY other status => STOP
  case "$tok" in LINK|FILE|NONE) printf '%s\n' "$tok" ;; *) return 2 ;; esac
}
```

`except FileNotFoundError` is written **above** `except OSError` because it is a subclass of it;
reversing the two clauses would swallow the distinction the whole helper exists to make. The exit
statuses `90`/`91` belong to the **probe process** and are unrelated to `STOP`'s own exit status
(H0) — `classify_path` never propagates a probe status, it returns `2`.

**Privileged/unprivileged routing is unchanged and secret-free.** `${1:+sudo}` selects the route, as
before; `sudo` is invoked **without `-E`**, the probe reads no environment file, imports nothing from
the release tree, and its entire stdout is one of three fixed tokens — no path content, no stat
identity, no environment value can reach an artifact through it (§2.6). The one argument is a
canonical bridge or `<EVROOT>` path, never credential material.

| Token | Meaning | Used as |
|---|---|---|
| `NONE` | `os.lstat` raised `FileNotFoundError` — neither a filesystem object nor a symlink | the **only** admissible answer for a no-clobber destination (§2.4(3), §7.2, §7.6, §8.3) |
| `FILE` | `lstat` succeeded and the mode is not `S_ISLNK` | the required answer for a canonical path (§4.4) or an expected file (logrotate policy, §4.4) |
| `LINK` | `lstat` succeeded and `S_ISLNK` — **a symlink, live or dangling** | a **STOP** on every canonical path and every no-clobber destination; the expected answer **only** where a symlink is the asserted artifact (the `/dev/null` mask link, §8.5 post-assertion 1) |
| *no token*, rc `91`, or any rc ≠ 90 | a non-`FileNotFoundError` `OSError`, a `sudo` policy refusal, a missing/failed interpreter, or a signal — **the path was never adjudicated** | **STOP.** Never `NONE`, never `NOTLINK`, never `ABSENT` |

**Call form (binding).** `classify_path`'s **rc is adjudicated first, in its own step**, and only then
is the token compared:

```bash
tok=$(classify_path "" "$p") || STOP "probe did not complete: $p"
[ "$tok" = NONE ] || STOP "expected NONE, got $tok: $p"
```

`[ "$(classify_path …)" = NONE ] || STOP` is **not** an acceptable substitute: command substitution
discards the helper's rc, so a probe failure and a wrong token become the same event, and the STOP
record cannot say which occurred. Every call site below uses the two-step form.

**(H3) `count_rc` — "zero matches" and "could not read" are different answers.**
`grep -c` prints `0` and exits `1` when there is no match, and exits `≥ 2` when the file is
unreadable, missing, or the usage is wrong. Collapsing those into "0" is a **false PASS on every
predicate in this design whose expected count is `0`** — `[Install]` (§4.3), `MTC_BRIDGE_START_MODE=`
and `HL_LIVE_ACK=` in the env file, and credential material in the fragment (§4.5).

```bash
# NOT EXECUTED — proposed shape only.
count_rc() {                 # unprivileged form.  usage: n=$(count_rc grep -c … file) || STOP
  local out rc
  out=$("$@") ; rc=$?
  case "$rc" in 0|1) : ;; *) return 2 ;; esac     # rc >= 2 => unreadable / bad usage => STOP
  case "$out" in ''|*[!0-9]*) return 2 ;; esac    # not a bare integer => STOP
  printf '%s\n' "$out"
}
count_rc_priv() {            # privileged form — sudo's own rc 1 must not read as "zero matches"
  local out rc
  out=$(sudo_rc "$@") ; rc=$?
  rc=$(priv_rc "$rc") || return 2
  case "$rc" in 0|1) : ;; *) return 2 ;; esac
  case "$out" in ''|*[!0-9]*) return 2 ;; esac
  printf '%s\n' "$out"
}
```

`pgrep` is adjudicated by the same three-way rule with its own status map: `0` = matches found,
`1` = none, and **`2` (syntax) / `3` (fatal) are STOP** — never read as "no writer survived". Empty
output is not the predicate; the rc is.

**(H4) Recorded-command capture (the §2.5 four-file group).** The helper writes `.cmd`, runs the
command with errexit disabled **for that invocation only** and under `set -o pipefail`, with
**stdout redirected to `.out` and stderr to `.err`**, writes `.rc` (final status **plus** the full
`PIPESTATUS` vector), re-enables errexit, and **adjudicates immediately**. A STOP verdict calls
`STOP` and the stage ends at that line: nothing later in the stage or chain runs, and in particular
**no mutation runs** (§2.5). **This is what makes H0 side-effect-free viable:** `STOP`'s reason line
goes to stderr and therefore into this group's `.err`, and its exit status into this group's `.rc`,
attributed to the command that actually failed — so the halt needs no artifact write of its own.

**Binding rule.** No stage below may express an existence, symlink, count, process-presence or
listener predicate with `&&`/`||` branching, with `if test …; then … else <benign token>; fi`, or by
reading a token out of a command substitution whose own rc was not adjudicated **first**. Where a
stage shows `classify_path` / `count_rc` / `count_rc_priv` / `sudo_rc`, the helper **is** the
specification and the comment beside it names only the expected token.

### 2.6 Secrets and redaction rules (bind every stage, no exceptions)

**Never printed, never captured, never written to any artifact, never echoed into a `.cmd` file:**
secret *values*, environment-variable *contents*, authentication material, broker payloads, order
credentials, wallet keys, account addresses, API tokens, or the contents of
`/etc/mtc-bridge/mtc-bridge.env`.

Positive rules:

| Rule | Rationale / anchor |
|---|---|
| Env-file checks use **`grep -c` (count) or `grep -q` (silent) only** — **never** plain `grep`, `grep -n`, `grep -o`, `cat`, `less`, `head`, `tail`, `awk` or `sed` on the env file | plain `grep` on an assignment line prints the assignment, i.e. the secret. The candidate's verifier uses `grep -qE` for exactly this reason (`2ce41e34…321b:…/verify.sh:138,143` `[SRC]`) |
| **Variable *names* only** are ever asserted; the design never asserts, compares or records a value | `…/verify.sh:137` header: *"secret hygiene (names only; no value is ever read or printed)"* `[SRC]` |
| **Forbidden commands, absolutely:** `cat /etc/mtc-bridge/mtc-bridge.env`, `systemctl show --all`, `systemctl show -p Environment`, `systemctl cat` piped to an artifact without screening, `cat /proc/<pid>/environ`, `ps eww`, `env`, `printenv`, any `--dump`/`--all` form that can materialise EnvironmentFile-derived values | eliminates the whole class rather than trusting a filter |
| Start-mode pin is proven by **grepping the unit fragment file**, not by asking systemd for the process environment | the fragment is a root-owned 0644 file containing no credential material (`…/verify.sh:148-153` asserts exactly that) `[SRC]` |
| Every `.out`/`.err` file is **screened before local retrieval** with the A-9 secret-signature method; a hit is a **STOP**, and the artifact is preserved on the host, not copied down | A-9 precedent (`GATE_A_A9_PASS_FINAL_2026-08-09D.md`) `[GOV]` |
| `<HOST_IP>`, SSH aliases and operator-machine paths are never written into a committed record | matrix §6 command-block safety contract |

`wal_state_bundle.py` provides a second, independent layer here and it is load-bearing for C3/C4:
its manifest and every stdout report contain *hashes, counts, aggregates, UTC timestamps and file
base names only*, and a sanitization guard rejects the manifest before writing if any string field
looks like a path, address or key (`2ce41e34…321b:IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py:27-34`,
guard `_assert_sanitized` at `:188`, applied to the report at `:1266-1270`) `[SRC]`.

### 2.7 D026 statement for this design

`AGENTS.md` §D026 binds any future regression test offered as closure evidence for a named defect: it
must be shown **RED** against the pre-fix/reverted behaviour (or an equivalent deliberate
mutation/falsification) and **GREEN** with the fix, with commands and real output recorded.

**This design creates no test and closes no defect.** It cannot claim closure from the existing
eleven WP0-mapped tests: those are *existing coverage*, proven to *exist* by `git grep` at the
candidate — not executed here, and existence is weaker than a passing run, which is in turn weaker
than a RED-then-GREEN demonstration (matrix §5). If a future implementer offers, for example, a new
SIGTERM-shutdown regression test as closure for the OPEN predicate I-R4, **D026 applies to that test
in full** and this document supplies no part of the required demonstration.

### 2.8 Static / mutating / blocked classification is explicit

- **`local-static` (no host at all, authorable now):** `RK-PRE`, and the authoring of every wrapper
  and helper this design specifies.
- **`read-only-host` (asserts only, still budget-blocked):** `RK-B0`–`RK-B7`.
- **`mutating-host` (each needs its own named lift):** `RK-C1`, `RK-C2`, `RK-C3`, `RK-C4`.
  **`RK-C1` additionally carries a design block** — it is not executable and cannot PASS while
  `D-GAP-C1-1` or `D-GAP-C1-3` is open (§5.2, §5.4) — and `RK-C3`, `RK-C4` and `RK-C2/B` inherit that
  block through Chain B. `RK-C2/A` is the one Group C stage that is **not** downstream of `RK-C1`.
- **`blocked` (not authorisable at any current authority level):** `RK-C5`.
- **out of scope of this design:** `RK-REC` (recovery start / unmask).

---

## 3. `RK-PRE` — local preregistration freeze (`local-static`)

**Purpose.** Make every predicate below tamper-evident *before* any host contact, so that no
expectation can be edited after seeing a result.

**Prerequisites.** None beyond the repo and the accepted A-2 local evidence.

**Proposed shape (local, no host):**

1. Author a single `EXPECTATIONS.md` containing, verbatim and in full: the frozen chain (A or B), the
   complete predicate tables of §4–§8, every `[EXPECT]` value, the authority matrix (§11) and the
   stop conditions (§12).
2. Fill `<PAYLOAD_MANIFEST_SHA256>` from accepted A-2 evidence. Record *which file it was read from*
   and that file's own SHA-256.
3. Compute `sha256sum EXPECTATIONS.md` locally and record it in the accepting record.

**Output contract.** `EXPECTATIONS.md` + its externally recorded SHA-256, both no-clobber.

**PASS.** The file exists, its hash is recorded, and the frozen chain is stated unambiguously.

**Failure/STOP.** If `<PAYLOAD_MANIFEST_SHA256>` cannot be read from accepted evidence — **STOP**. Do
not proceed to any host stage with an unfilled or guessed manifest hash.

**Secrets.** None involved.

**Unresolved.** None.

---

## 4. Stage B — `RK-B`: one bounded, read-only, post-start design

> **Why this stage exists at all.** A wholesale post-start `verify.sh` run **will intentionally
> fail** and must not be prescribed. At the candidate `[SRC]`:
> `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:213-214` fails if the unit is ACTIVE
> (*"first-start unit is ACTIVE; it must not be running before KVM2-P4-07"*); `:207-211` asserts the
> unit is **masked**; `:243-247` fails on any `bridge.app` writer; `:248` asserts the control port is
> **closed**; and its own comment at `:240-242` states the scope: *"This verifier is specifically the
> masked/unstarted mode… this mode requires both zero writer processes and a completely closed port,
> including loopback."* Post-Gate the unit is active and unmasked, so four of those assertions are
> inverted by design. `COMMANDS.md:224-228` `[REF-INV]` says the same in prose and adds the binding
> instruction: do not wrap the verifier in `|| true` — use bounded evidence checks instead.
> `RK-B` is that bounded set.

### 4.0 `RK-B0` — evidence root and expectation pin

- **Purpose.** Allocate the no-clobber output root and pin the expectations on the host before any
  measurement.
- **Anchors.** §2.3, §2.4 (design-internal); no candidate anchor needed.
- **Mutation class.** `read-only-host` with respect to the *bridge*: it creates only a fresh directory
  under `/home/gatea/`, touching no bridge path, no unit, no DB, no config and no firewall.
- **Prerequisites.** `RK-PRE` complete; host access and budget lift (§11).
- **Proposed command shape:**
  ```bash
  # NOT EXECUTED — proposed shape only
  SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
  PY=/opt/mtc-bridge/venvs/${SHA}/bin/python

  # STEP 1 — the §2.5a H2 PREREQUISITE, and the first host command of the whole run: the probe
  # interpreter is verified BEFORE any classify_path call anywhere. Read-only, offline.
  ver=$("${PY}" -c 'import sys; print("%d.%d" % sys.version_info[:2])') || STOP "probe interpreter did not run"
  [ "$ver" = "3.12" ] || STOP "probe interpreter is '$ver', not 3.12"
  # RK-B1 predicate (1) re-records this same assertion as its own stage predicate (§4.1).

  RUNID="RK-B-$(date -u +%Y%m%dT%H%M%SZ)"
  EVROOT="/home/gatea/runkit/${RUNID}"
  mkdir -p /home/gatea/runkit            # parent only
  mkdir "${EVROOT}" || STOP              # NO -p: EEXIST here is a STOP, and so is any other rc
  tok=$(classify_path "" "${EVROOT}/00_runid.txt") || STOP "probe did not complete"
  [ "$tok" = NONE ] || STOP "00_runid.txt is $tok"    # §2.4(3): an existing object OR a link is a STOP
  printf '%s\n' "${RUNID}" > "${EVROOT}/00_runid.txt"
  # copy the frozen EXPECTATIONS.md up, then re-hash it on the host:
  sha256sum "${EVROOT}/EXPECTATIONS.md" || STOP   # rc must be 0; an unreadable file is a STOP,
                                                  # never an empty digest compared as a mismatch
  ```
- **No-clobber artifact contract.** `<EVROOT>` created by plain `mkdir`; `00_runid.txt` and
  `EXPECTATIONS.md` must not pre-exist.
- **PASS predicates.** The probe interpreter reports exactly `3.12` **before any `classify_path` call**
  (§2.5a H2 prerequisite); `mkdir` rc `0`; on-host `sha256sum EXPECTATIONS.md` **equals** the `RK-PRE`
  local value, proving the predicates were not altered in transit.
- **Failure / STOP.** A probe interpreter that is absent, does not run, or reports anything other than
  `3.12` → **STOP** before the first probe: every no-clobber assertion in every later stage depends on
  it, and an unverified interpreter makes every `NONE` token unfounded. `mkdir` rc ≠ 0 (root already
  exists) → **STOP**, allocate nothing else, do not reuse. Expectation-hash mismatch → **STOP**; the
  predicate set is not trustworthy.
- **Secrets/redaction.** None captured.
- **Unresolved.** None.

### 4.1 `RK-B1` — Python 3.12 + exact `verify_lock --check-installed` parity (`packages=56`)

- **Purpose.** Prove the per-SHA venv interpreter is Python 3.12 and its installed distribution set
  exactly equals the 56-entry hash-locked requirement set — offline, with no network.
- **Anchors.**
  - `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/verify.sh:104-115` `[SRC]` — the interpreter check
    is `"%d.%d" % sys.version_info[:2]` compared literally against `3.12`.
  - `…/verify.sh:116-121` `[SRC]` — the verifier invokes `verify_lock.py --lock … --check-installed`
    with the venv interpreter.
  - `2ce41e34…321b:IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py` (blob
    `8ccd6f329154422a85b8e7663e6a079dbd47b4fd`, `[REF-INV]`): `parse_lock` at `:28` rejects
    URLs/VCS/index overrides and requires exact `==` plus ≥1 `--hash=sha256:`; `--check-installed` at
    `:78`, compared at `:82-92` allowing only the bootstrap set; the PASS line at `:96-97` is
    `print(f"verify_lock: PASS: {mode}; packages={len(expected)}")` — **the count is computed from
    the lock actually parsed, not a hard-coded constant**, so `packages=56` is evidence rather than
    an echo.
  - Counts re-derived at the candidate in both repair rounds: **56** `==`-pinned entries, **1345**
    `--hash=sha256:` lines.
- **Mutation class.** `read-only-host`. No network: the verifier reads installed distribution
  metadata via `importlib.metadata` (`verify_lock.py:66-72` `[REF-INV]`) and never contacts an index.
- **Prerequisites.** `RK-B0`.
- **Proposed command shape:**
  ```bash
  # NOT EXECUTED — proposed shape only. Read-only, offline.
  SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
  /opt/mtc-bridge/venvs/${SHA}/bin/python -c 'import sys; print("%d.%d" % sys.version_info[:2])'
  # expect stdout exactly: 3.12

  /opt/mtc-bridge/venvs/${SHA}/bin/python \
      /opt/mtc-bridge/releases/${SHA}/IBKR_PAPER_BRIDGE/deploy/linux/verify_lock.py \
      --lock /opt/mtc-bridge/releases/${SHA}/IBKR_PAPER_BRIDGE/requirements.lock \
      --check-installed
  # expect stdout exactly: verify_lock: PASS: lock+installed; packages=56
  ```
- **No-clobber artifact contract.** `01_pyver.{cmd,out,err,rc}`, `02_verify_lock.{cmd,out,err,rc}`.
- **PASS predicates (all required).** (1) interpreter output is exactly `3.12` — **this is also the
  §2.5a H2 prerequisite**, first recorded as step 1 of `RK-B0` and re-recorded here as this stage's
  own predicate, because every `classify_path` token in every stage rests on it; (2) `verify_lock` rc
  is `0`; (3) stdout is exactly `verify_lock: PASS: lock+installed; packages=56` — the mode token
  `lock+installed` **and** the count `56` both matter; `lock` alone would mean `--check-installed`
  was not honoured.
- **Failure / STOP.** rc `1` with `missing-or-wrong=` or `unexpected=` (`verify_lock.py:86-92`) ⇒
  **STOP** — install/product drift on a protected surface. A count other than 56 ⇒ **STOP**. A
  Python version other than 3.12 ⇒ **STOP**. Do not re-run, do not repair in place, preserve
  evidence.
- **Secrets/redaction.** None; the output is a mode token and an integer. Distribution *names* may
  appear in a failure message — that is package metadata, not a secret, and is retained.
- **Unresolved.** None. This stage is fully specified from `[SRC]`/`[REF-INV]` anchors.

### 4.2 `RK-B1a` — **observed** installed lock byte identity (currently NOT IN EVIDENCE)

- **Purpose.** Close the fourth lock identity (§1.2 row 4) by *observing* the installed bytes, and
  compare them against the *expected* value `a1881296…`.
- **Anchors.**
  - **Expected value `[EXPECT]`:** `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`
    — raw blob content SHA-256, LF, 117 762 B, derived by
    `git cat-file blob 47f53fa227bf0f18b9bf9bd77e060d8856961728 | sha256sum`.
  - **Why the payload is LF `[SRC]`:** `2ce41e34…321b:…/deploy/linux/package.sh:78-83` exports with
    `git -c core.autocrlf=false -c core.eol=lf … archive`; its own comment at `:79-81` names the
    Windows CRLF hazard.
  - **Where the host records it `[REF-INV]`:** `…/deploy/linux/install.sh:401` computes
    `LOCK_SHA="$(sha256_of "${DEST}/IBKR_PAPER_BRIDGE/requirements.lock")"` and `:416` writes it into
    `/etc/mtc-bridge/install_manifest.json` as `"requirements_lock_sha256"`.
    `install.sh:431-433` prints the release SHA and the **unit** SHA-256 and **never the lock hash**,
    which is precisely why it is absent from the A-2 install capture.
  - **Re-verification path `[SRC]`:** `…/verify.sh:82-91` re-checks every release file against
    `RELEASE_SHA256SUMS`.
- **⛔ Current state — NOT IN EVIDENCE.** No located Gate-A evidence records either the observed
  `sha256sum` of the installed lock or the host manifest's `requirements_lock_sha256`
  (repair-record §2.7g). This stage is a **new capture**, not a re-check of something already known.
- **Mutation class.** `read-only-host`; the manifest read additionally needs root
  (`/etc/mtc-bridge/install_manifest.json` is `0640 root:root`, asserted at `…/verify.sh:128` `[SRC]`
  and observed in the transition inventory `[HOST-OBS]`).
- **Prerequisites.** `RK-B0`; root for the second command.
- **Proposed command shape:**
  ```bash
  # NOT EXECUTED — proposed shape only. Read-only.
  SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
  sha256sum /opt/mtc-bridge/releases/${SHA}/IBKR_PAPER_BRIDGE/requirements.lock
  # expected (to be COMPARED against, not restated):
  #   a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e

  wc -c /opt/mtc-bridge/releases/${SHA}/IBKR_PAPER_BRIDGE/requirements.lock
  # expected: 117762   (a CRLF-converted copy would be 119274 — see the disposition table)

  # corroboration, root read, field-only, no other manifest content printed.
  # rc is adjudicated three-way (§2.5a H1): inner rc 0 with exactly one 64-hex field is the only
  # PASS; inner rc 1 (field absent) is a STOP; any other inner rc, or a sudo/exec failure, is a STOP.
  # ⛔ "no line came back, so there is nothing to compare" is not a disposition.
  sudo_rc grep -o '"requirements_lock_sha256": *"[0-9a-f]\{64\}"' \
       /etc/mtc-bridge/install_manifest.json
  ```
- **No-clobber artifact contract.** `03_lock_sha256.{cmd,out,err,rc}`, `04_lock_bytes.{cmd,out,err,rc}`,
  `05_manifest_lock_field.{cmd,out,err,rc}`. The observed value is written into the record explicitly
  labelled **observed-on-host**, alongside the expected value labelled **expected-from-source**.
- **PASS predicates.** (1) observed `sha256sum` **equals** `a1881296…`; (2) byte count is `117762`;
  (3) the manifest field, once read, equals the same observed value. All three, or it is not a PASS.
- **Failure disposition — deliberately *not* a reflex STOP.**

  | Observation | Disposition |
  |---|---|
  | Observed = `a1881296…`, manifest field agrees | **PASS.** Identity 4 becomes `[HOST-OBS]` for the first time. |
  | Observed ≠ `a1881296…` | **INVESTIGATE READ-ONLY.** Weigh **both** a wrong expected value **and** genuine drift. Re-walk the derivation chain (blob → LF-pinned export → manifest-verified install) before escalating a STOP *or* dismissing one. Do **not** auto-classify in either direction. |
  | Observed = `40873556…` | Would mean a CRLF-converted file reached the host — a **real packaging defect**, and a **STOP**. Note this is the *only* legitimate appearance of that value anywhere: as a failure signature, never as an expectation. |
  | Manifest field ≠ observed `sha256sum` | **STOP.** The installed tree and its install-time record disagree. |
  | Manifest unreadable / permission failure | **STOP** — not SKIP. Record the rc and stop. |
- **Secrets/redaction.** The `grep -o` form prints **only** the single 64-hex field and never any
  other manifest content. Plain `cat` of the manifest is not used (it contains absolute paths, which
  the §2.6 rules keep out of committed records).
- **Unresolved.** Until this stage runs, identity 4 stays **open**. Nothing downstream may treat
  `a1881296…` as a host-verified fact.

### 4.3 `RK-B2` — service identity, binding, restart policy, and `is-enabled = static`

- **Purpose.** Prove the running unit is the accepted first-start unit: active, bound to the exact
  release SHA and per-SHA venv, `Restart=no`, `NRestarts=0`, **unmasked**, no `[Install]`, and
  `systemctl is-enabled` reporting exactly **`static`**.
- **Anchors.**
  - `2ce41e34…321b:…/systemd/mtc-bridge-first-start.service.template` `[SRC]` (blob `c1823254…`):
    `Restart=no` `:55`; `Type=exec` `:30`; `ExecStart=/opt/mtc-bridge/venvs/@RELEASE_SHA@/bin/python
    -m bridge.app` `:34`; `WorkingDirectory=/opt/mtc-bridge/releases/@RELEASE_SHA@/IBKR_PAPER_BRIDGE`
    `:33`; `StartLimitBurst=3` `:27`; and the explanatory comment at `:11` — *"No [Install] section —
    `systemctl enable` is structurally impossible, so this unit can never be pulled in at boot."*
    The file contains **no** `[Install]` section.
  - `…/verify.sh:178-187` `[SRC]` — the SHA-binding and per-SHA-venv greps.
  - `…/verify.sh:198-202` `[SRC]` — `[Install]` must be absent.
  - `…/verify.sh:218-221` `[SRC]` — the `is-enabled` case accepts `masked|disabled|static`.
  - `…/lib/common.sh:23-25` `[SRC]` — real fragment lives in `/usr/local/lib/systemd/system`; the
    mask symlink lands in `/etc/systemd/system` (`MTC_MASK_DIR`, `:24`), which is why masking never
    destroys the fragment.
  - Unit fragment SHA-256 `538c1c6038b475e87fb0e9b9c35fd4ebd8451b40ff93538f8fea5aa0b49279bd`,
    3736 B, root mode `644` — `[HOST-OBS]`, transition inventory `:44-45`.
  - Current runtime: active/running, `Restart=no`, `NRestarts=0`, MainPID `189813` — `[HOST-OBS]`,
    transition inventory `:35-36`.
- **⛔ Why the preregistered `is-enabled` value is exactly `static`, and nothing else.**
  The candidate's verifier accepts three tokens because it runs in the *masked, pre-start* mode. For
  the **active, unmasked, first-start unit** only one of them can be correct:

  | Token | Verdict for this stage | Reason |
  |---|---|---|
  | **`static`** | ✅ **the only accepted value** | `[SYSTEMD]` semantics: a unit file with no `[Install]` section and no mask reports `static`. The absence of `[Install]` is `[SRC]`-established (template `:11`, `verify.sh:198-202`); the unmasked state is the accepted post-Gate state. |
  | `masked` / `masked-runtime` | ⛔ **STOP** | contradicts the accepted active+unmasked baseline. |
  | `disabled` | ⛔ **STOP** | `[SYSTEMD]`: `disabled` implies the unit *has* an `[Install]` section and is merely not linked. That would be **template drift** on the exact property the design relies on for boot safety. Accepting it — as the pre-start verifier's broader case does — would mask a real defect here. |
  | `enabled` / `enabled-runtime` | ⛔ **STOP** | boot activation. |
  | `generated` / `transient` | ⛔ **STOP** | a generator or transient route could activate at boot outside the fragment. |
  | `indirect` | ⛔ **STOP** | activation via an `Also=`/alias chain. |
  | `alias` / `linked` / `linked-runtime` | ⛔ **STOP** | the name resolves somewhere other than the accepted fragment. |
  | anything else, or a non-zero rc with an unparsable token | ⛔ **STOP** | never SKIP, never PASS. |
- **Mutation class.** `read-only-host`. `systemctl is-active`, `is-enabled`, `show` and `cat` do not
  start, stop, enable, unmask or reload anything.
- **Prerequisites.** `RK-B0`.
- **Proposed command shape:**
  ```bash
  # NOT EXECUTED — proposed shape only. All read-only.
  SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
  U=mtc-bridge-first-start.service
  FRAG=/usr/local/lib/systemd/system/${U}

  systemctl is-active   "${U}"                       # expect: active
  systemctl is-enabled  "${U}"                       # expect EXACTLY: static
  systemctl show -p Restart      --value "${U}"      # expect: no
  systemctl show -p NRestarts    --value "${U}"      # expect: 0
  systemctl show -p Type         --value "${U}"      # expect: exec
  systemctl show -p FragmentPath --value "${U}"      # expect: ${FRAG}
  systemctl show -p Transient    --value "${U}"      # expect: no
  systemctl show -p Names        --value "${U}"      # expect: ${U} only
  systemctl show -p MainPID,ExecMainPID --value "${U}"   # recorded, both non-zero

  # Count predicates go through count_rc (§2.5a H3): grep rc 0/1 are real counts, rc >= 2 is a STOP.
  # ⛔ A bare `grep -c` would report an unreadable fragment as an empty result that a reader records
  #    as "0" — which is the PASS token for the [Install] check. That is a manufactured PASS.
  count_rc grep -c "releases/${SHA}/"          "${FRAG}" || STOP   # expect: >= 1
  count_rc grep -c "venvs/${SHA}/bin/python"   "${FRAG}" || STOP   # expect: >= 1
  count_rc grep -c '^\[Install\]'              "${FRAG}" || STOP   # expect EXACTLY: 0
  sha256sum "${FRAG}" || STOP                        # expect: 538c1c60…279bd (3736 B)
  wc -c     "${FRAG}" || STOP                        # expect: 3736

  # unmasked proof — the inverse of verify.sh:207-211. One §2.5a H2 probe, rc adjudicated first,
  # token compared second. A two-way shell form here would print the PASS token for a permission
  # error, a vanished /etc/systemd/system, or a race, and record rc 0 for the echo.
  tok=$(classify_path "" "/etc/systemd/system/${U}") || STOP "mask-path probe did not complete"
  [ "$tok" = NONE ] || STOP "mask path is $tok"        # expect EXACTLY: NONE
  #   NONE => unmasked, the accepted post-Gate state
  #   LINK => masked, or a dangling link occupying the mask path   => STOP
  #   FILE => a real file has replaced the mask path               => STOP
  #   rc 2 => the probe did not complete                           => STOP, never read as NONE
  ```
- **No-clobber artifact contract.** One four-file group per command under `<EVROOT>`; the fragment
  SHA-256 recorded as **observed-on-host** against the **observed-on-host** baseline `538c1c60…279bd`
  (this is one of the few comparisons where *both* sides are observations).
- **PASS predicates (all required).** `is-active` = `active`; `is-enabled` = `static` exactly;
  `Restart` = `no`; `NRestarts` = `0`; `Type` = `exec`; `FragmentPath` = the canonical fragment;
  `Transient` = `no`; `Names` contains only the unit name; both release-SHA and venv-SHA greps ≥ 1;
  `[Install]` count exactly 0; fragment SHA-256 = `538c1c60…279bd` and size = 3736; mask-path token
  exactly `NONE`.
- **Failure / STOP.** Any mismatch ⇒ **STOP** (service drift). `NRestarts` ≠ 0 is particularly severe:
  with `Restart=no` `[SRC]`, a non-zero restart count means something restarted the unit outside the
  accepted path. **Any `systemctl`, `grep`, `sha256sum`, `wc` or mask-path probe that fails to
  complete — non-zero rc, unparsable output, permission denial — is a STOP in its own right**, never
  an absent value and never a count of `0` (§2.5a).
- **Secrets/redaction.** `systemctl show -p Environment` and `systemctl show --all` are **forbidden**
  (§2.6). `systemctl cat` is not used for capture; the fragment is grepped by count instead.
- **Unresolved.** The `static` expectation rests on `[SYSTEMD]` semantics plus the `[SRC]` absence of
  `[Install]`. It has never been observed on this host — no located record captures an `is-enabled`
  value for the running unit. It is therefore preregistered as `[EXPECT]`, and the *first* observation
  will make it `[HOST-OBS]`. This is stated so a future reader does not mistake it for a re-check.

### 4.4 `RK-B3` — bounded stat / ownership / symlink checks (not wholesale verification)

- **Purpose.** Reproduce the *permission and ownership* assertions of the candidate verifier without
  running the verifier, and without the expensive whole-tree sweeps.
- **Anchors (all `[SRC]`, candidate `verify.sh` blob `5cfefd7092…` and `common.sh` blob `db11010a…`).**

  | Path | Expected mode / owner | Anchor |
  |---|---|---|
  | `/opt/mtc-bridge/releases/<SHA>` | `0555 root:root` | `verify.sh:79` |
  | `/opt/mtc-bridge/venvs/<SHA>` | `0555 root:root` | `verify.sh:105` |
  | `/var/lib/mtc-bridge` | `0750 mtc-bridge:mtc-bridge` | `verify.sh:124` |
  | `/var/log/mtc-bridge` | `0750 mtc-bridge:mtc-bridge` | `verify.sh:125` |
  | `/etc/mtc-bridge` | `0750 root:root` | `verify.sh:126` |
  | `/etc/mtc-bridge/mtc-bridge.env` | `0600 root:root` | `verify.sh:127` |
  | `/etc/mtc-bridge/install_manifest.json` | `0640 root:root` | `verify.sh:128` |

  Comparison method mirrors `assert_mode_owner` (`common.sh:80-93`): `stat -c '%a'` and
  `stat -c '%U:%G'`, expected mode compared with the leading `0` stripped.
  Symlink sweep mirrors `verify.sh:45-52` + `assert_not_symlink` (`common.sh:72-77`) over the same
  canonical path list.
  Install-manifest binding mirrors `verify.sh:129-135`.
- **⛔ Deliberately EXCLUDED from `RK-B3`, with reasons.**

  | Excluded check | Anchor | Why excluded |
  |---|---|---|
  | `assert_no_writable_paths` whole-tree `find … -perm /222` | `common.sh:95-105` | unbounded sweep over a ~1 GB release tree and the venv; this stage is explicitly *bounded*. Offer separately if a later authority wants it. |
  | `assert_exact_payload_tree` (full inventory diff) | `common.sh:124-150` | same reason; and it is already A-2 evidence for this release. |
  | `sha256sum --strict -c RELEASE_SHA256SUMS` (whole payload) | `verify.sh:88-92` | whole-payload rehash; expensive and duplicative. **Note:** the installed `requirements.lock` is a *member* of that manifest, and `RK-B1a` covers exactly that member — which is the one whose host value is missing from evidence. |
  | `cmp` of installed unit vs rendered template | `verify.sh:188-197` | requires writing a rendered temp file; `RK-B2`'s fragment SHA-256 against the observed `538c1c60…279bd` baseline achieves the same binding more cheaply and without a write. |
  | anything in `verify.sh` §6 mask/active/§8 port-closed | `verify.sh:207-217,248` | **inverted post-start by design** — running them would manufacture failures (G2). |
- **Mutation class.** `read-only-host` (root read for `/etc/mtc-bridge/**`).
- **Prerequisites.** `RK-B0`.
- **Proposed command shape:**
  ```bash
  # NOT EXECUTED — proposed shape only. Read-only.
  SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
  for p in /opt/mtc-bridge /opt/mtc-bridge/releases /opt/mtc-bridge/venvs \
           /opt/mtc-bridge/releases/${SHA} /opt/mtc-bridge/venvs/${SHA} \
           /var/lib/mtc-bridge /var/log/mtc-bridge /etc/mtc-bridge \
           /etc/mtc-bridge/mtc-bridge.env /etc/mtc-bridge/install_manifest.json \
           /usr/local/lib/systemd/system \
           /usr/local/lib/systemd/system/mtc-bridge-first-start.service \
           /etc/logrotate.d/mtc-bridge ; do
    # ⛔ NOT `sudo test -L "$p" && echo SYMLINK || echo NOTLINK`. That form printed the PASS token
    #    NOTLINK for a denied sudo, a vanished path, a dangling symlink and a race alike, with rc 0.
    tok=$(classify_path sudo "$p") || STOP "probe failed: $p"
    [ "$tok" = FILE ] || STOP "expected FILE, got $tok: $p"   # LINK => STOP; NONE => STOP
    # the stat identity is captured into a variable and its rc adjudicated BEFORE anything is
    # emitted — a failed or raced stat must never be papered over by a successful printf
    ident=$(sudo_rc stat -c '%n %a %U:%G' "$p") ; rc=$(priv_rc $?) || STOP "stat did not run: $p"
    [ "$rc" -eq 0 ] || STOP "stat rc $rc: $p"
    [ -n "$ident" ] || STOP "empty stat output is not evidence: $p"
    printf '%s\n' "$ident"
  done

  # install-manifest binding (mirrors verify.sh:129-135), quiet form, no content printed.
  # count_rc_priv (§2.5a H3): grep rc 0/1 are counts; rc >= 2, or a sudo policy refusal, is a STOP.
  count_rc_priv grep -cF "\"release_sha\": \"${SHA}\"" \
       /etc/mtc-bridge/install_manifest.json || STOP                                         # expect 1
  count_rc_priv grep -cF "\"release_manifest_sha256\": \"<PAYLOAD_MANIFEST_SHA256>\"" \
       /etc/mtc-bridge/install_manifest.json || STOP                                         # expect 1

  # logrotate policy present (mirrors verify.sh:234-238)
  # ⛔ NOT `sudo test -f … && echo PRESENT || echo MISSING`: MISSING would also be printed when the
  #    read was refused, which is a different fact and a STOP, not a policy-absent finding.
  tok=$(classify_path sudo /etc/logrotate.d/mtc-bridge) || STOP "logrotate probe did not complete"
  [ "$tok" = FILE ] || STOP "logrotate policy is $tok"   # expect token: FILE
  ```
- **No-clobber artifact contract.** One group per command; the `stat` sweep output is a single
  artifact listing path/mode/owner triples only.
- **PASS predicates.** Every path classifies as **`FILE`**; every mode/owner equals the table above,
  read from a `stat` whose rc was adjudicated `0` before the line was emitted; both manifest-binding
  counts are exactly `1`; the logrotate policy classifies as `FILE`.
- **Failure / STOP.** Any `LINK` on a canonical path ⇒ **STOP** (`common.sh:72-77` treats this as
  fatal, `die`, not a soft failure) — **and `LINK` covers a dangling symlink, which an `-e`-only
  probe would have called absent**. Any `NONE` ⇒ **STOP**. Any mode/owner drift ⇒ **STOP**. Manifest
  binding count ≠ 1 ⇒ **STOP**. **A probe or `stat` that does not complete, a `sudo` refusal, or a
  `grep` rc ≥ 2 ⇒ STOP** — never a `NOTLINK`/`MISSING` token, never a count of `0`, never a SKIP.
- **Secrets/redaction.** The env file is only `stat`-ed and, in `RK-B4`, `grep -c`-ed. It is never
  opened for content here. `grep -cF` on the manifest prints a count, not a line.
- **Unresolved.** `<PAYLOAD_MANIFEST_SHA256>` must be filled in `RK-PRE` from accepted A-2 evidence.
  It is **not** established in this unit and must never be confused with the lock hash (§2.3).

### 4.5 `RK-B4` — effective hardening + exact start-mode pin + env-file no-override (name only)

- **Purpose.** Prove the sandboxing directives are *effective on the running unit* (not merely
  declared in a template), that `MTC_BRIDGE_START_MODE=credential_free_disarmed` is pinned in the
  hashed unit, and that the env file carries no override — **without reading a single value**.
- **Anchors.**
  - Template directives `[SRC]`, `2ce41e34…321b:…/systemd/mtc-bridge-first-start.service.template`:
    `Environment=MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db` `:40`;
    **`Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed` `:42`**;
    `EnvironmentFile=/etc/mtc-bridge/mtc-bridge.env` `:45`;
    `KillSignal=SIGTERM` `:48`, `KillMode=mixed` `:49`, `TimeoutStartSec=120` `:50`,
    `TimeoutStopSec=45` `:51`, `FinalKillSignal=SIGKILL` `:52`, `Restart=no` `:55`,
    `RestartSec=30` `:56`;
    `NoNewPrivileges=yes` `:64`, `CapabilityBoundingSet=` (empty) `:65`, `AmbientCapabilities=`
    (empty) `:66`, `PrivateTmp=yes` `:67`, `PrivateDevices=yes` `:68`, `PrivateUsers=no` `:69`,
    `ProtectSystem=strict` `:70`, `ProtectHome=yes` `:71`, `ProtectProc=invisible` `:72`,
    `ProcSubset=pid` `:73`, `ProtectClock=yes` `:74`, `ProtectHostname=yes` `:75`,
    `ProtectKernelTunables=yes` `:76`, `ProtectKernelModules=yes` `:77`, `ProtectKernelLogs=yes` `:78`,
    `ProtectControlGroups=yes` `:79`, `RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX` `:80`,
    `RestrictNamespaces=yes` `:81`, `RestrictRealtime=yes` `:82`, `RestrictSUIDSGID=yes` `:83`,
    `LockPersonality=yes` `:84`, `SystemCallArchitectures=native` `:85`,
    `SystemCallFilter=@system-service` `:86`, `SystemCallErrorNumber=EPERM` `:87`, `UMask=0077` `:88`,
    `RemoveIPC=yes` `:89`, `ReadWritePaths=/var/lib/mtc-bridge /var/log/mtc-bridge` `:93`.
  - Required needle list `[SRC]`, `…/verify.sh:160-171` — includes
    `MTC_BRIDGE_START_MODE=credential_free_disarmed` at `:171`.
  - Env-file override rejection `[SRC]`, `…/verify.sh:143-147`: **fails** if any
    `MTC_BRIDGE_START_MODE=` assignment (bare or `export`) appears in the env file.
  - `HL_LIVE_ACK` absence `[SRC]`, `…/verify.sh:138-142`.
  - Unit carries no credential material `[SRC]`, `…/verify.sh:148-153`.
  - Env template documents the rule `[SRC]`,
    `…/deploy/linux/env/mtc-bridge.env.template:40-42`: *"MTC_BRIDGE_START_MODE is set by the unit
    itself (Environment=) … it must stay ABSENT — verify.sh rejects any MTC_BRIDGE_START_MODE
    assignment here."*
  - Application side `[SRC]`, `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py`: mode constant `:32`;
    `resolve_start_mode` CLI-then-env with a closed valid set `:35-52`; `--dry-run` rejected with the
    mode `:113-114`; a supplied broker rejected `:115-116`; flags pinned `:138-148`; broker
    construction gated off at `:149`.
- **⛔ Start-mode asymmetry (inherited, restated so no future step assumes it away).** The **steady**
  profile template carries **no** `MTC_BRIDGE_START_MODE` pin (matrix §A4 round-2 finding; steady
  blob `121229ea5b…`, `[REF-INV]`, `Restart=on-failure`). The three-layer enforcement is a property of
  the **first-start unit only**. This is not a defect — the steady profile is gated, never installed,
  never enabled — but no future admission preregistration may assume the pin carries over.
- **Mutation class.** `read-only-host` (root read for the env file).
- **Prerequisites.** `RK-B0`.
- **Proposed command shape:**
  ```bash
  # NOT EXECUTED — proposed shape only. Read-only. NO VALUE IS EVER PRINTED.
  U=mtc-bridge-first-start.service
  FRAG=/usr/local/lib/systemd/system/${U}

  # (a) EFFECTIVE hardening, as systemd resolved it on the running unit.
  #     Explicit property list — never `--all`, never `-p Environment`.
  systemctl show "${U}" \
    -p NoNewPrivileges -p CapabilityBoundingSet -p AmbientCapabilities \
    -p PrivateTmp -p PrivateDevices -p PrivateUsers \
    -p ProtectSystem -p ProtectHome -p ProtectProc -p ProcSubset \
    -p ProtectClock -p ProtectHostname -p ProtectKernelTunables \
    -p ProtectKernelModules -p ProtectKernelLogs -p ProtectControlGroups \
    -p RestrictAddressFamilies -p RestrictNamespaces -p RestrictRealtime \
    -p RestrictSUIDSGID -p LockPersonality -p SystemCallArchitectures \
    -p UMask -p RemoveIPC -p ReadWritePaths \
    -p KillSignal -p KillMode -p TimeoutStopUSec -p FinalKillSignal \
    -p Restart -p StartLimitBurst -p User -p Group -p WorkingDirectory
  # rc must be 0 and every requested property must be present in the output; a truncated or
  # non-zero `systemctl show` is a STOP, never "the property is unset" (§2.5a).

  # (b) EXACT start-mode pin, proven from the hashed fragment (never from the process env).
  count_rc grep -c '^Environment=MTC_BRIDGE_START_MODE=credential_free_disarmed$' "${FRAG}" || STOP   # 1
  count_rc grep -c '^Environment=MTC_BRIDGE_STATE_DB=/var/lib/mtc-bridge/bridge.db$' "${FRAG}" || STOP # 1
  count_rc grep -cE '^[[:space:]]*Environment=.*HL_(API_WALLET_KEY|ACCOUNT_ADDRESS|LIVE_ACK)' \
       "${FRAG}" || STOP                   # expect: 0

  # (c) ENV FILE — NAME ONLY. Count form. A value is never produced by these commands.
  # ⛔ These two are the sharpest instance of the collapsed-predicate defect in the whole design:
  #    the PASS token IS `0`, and a bare `sudo grep -c` on a 0600 root file returns rc >= 1 with no
  #    usable stdout on a permission failure, a missing file or a bad pattern. Reading that as "0"
  #    would report "no override present" when what actually happened is "the check never ran".
  #    count_rc_priv (§2.5a H3) admits ONLY inner rc 0 or 1 with a bare integer on stdout; every
  #    other outcome — including a `sudo` policy refusal, which also exits 1 — is a STOP.
  #    Secret hygiene is unchanged: only an integer ever crosses the boundary.
  count_rc_priv grep -cE '^[[:space:]]*(export[[:space:]]+)?MTC_BRIDGE_START_MODE=' \
       /etc/mtc-bridge/mtc-bridge.env || STOP      # expect EXACTLY: 0
  count_rc_priv grep -cE '^[[:space:]]*(export[[:space:]]+)?HL_LIVE_ACK=' \
       /etc/mtc-bridge/mtc-bridge.env || STOP      # expect EXACTLY: 0
  ```
- **No-clobber artifact contract.** One group per command. The `systemctl show` output is a
  `Key=Value` list of *security directives only* and contains no credential material.
- **PASS predicates.**
  - Every effective property equals its template value. Note the two representation differences that
    are **not** drift: `TimeoutStopSec=45` surfaces as `TimeoutStopUSec=45s` (or the µs form)
    `[SYSTEMD]`, and empty `CapabilityBoundingSet=`/`AmbientCapabilities=` surface as an empty or
    full-mask-cleared value `[SYSTEMD]`. The run-kit compares *semantics*, and the exact rendered
    strings are recorded verbatim.
  - Fragment start-mode pin count exactly `1`; state-DB pin count exactly `1`; credential-material
    count exactly `0`.
  - Env-file `MTC_BRIDGE_START_MODE` count exactly `0` and `HL_LIVE_ACK` count exactly `0`.
- **Failure / STOP.** Any hardening drift ⇒ **STOP**. Start-mode pin count ≠ 1 ⇒ **STOP** (the hashed
  unit no longer pins the mode). Env-file count ≠ 0 ⇒ **STOP** — this is the override the candidate's
  own verifier fails on, and it would mean the pinned mode can be defeated from a 0600 file.
  **A permission failure, a `sudo` policy refusal, a missing env file, a `grep` rc ≥ 2, or any
  non-integer stdout ⇒ STOP** — not SKIP, and emphatically **not recorded as a count of `0`**, which
  is the very token these two checks accept as their PASS.
- **Secrets/redaction.** This is the highest-risk stage for leakage and it is constrained hardest:
  count-only greps, an explicit property allowlist, and the §2.6 forbidden-command list. **At no
  point is any variable value, env-file line, or process environment read, printed, captured or
  transmitted.**
- **Unresolved.** The precise rendered strings systemd returns for a handful of properties are
  `[SYSTEMD]` representation details that have never been observed on this host. They are recorded
  verbatim on first run and become the baseline; they are **not** preregistered as exact strings
  where the representation is ambiguous (`D-GAP-B4-1`).

### 4.6 `RK-B5` — status API remains DISARMED with every flag off

- **Purpose.** Confirm the running app reports the credential-free DISARMED posture with all
  network / exchange / credential / ARM flags off.
- **Anchors `[SRC]`, `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py`.** The reported flags are not
  incidental — they are *set by the deployed start mode*:
  - `:137` `app.state.credential_free_disarmed = credential_free_disarmed`;
  - `:138-148` pins `mode="credential_free_disarmed"`, `network="disabled"`,
    `exchange_conn="disabled"`, `exchange_enabled=False`, `credential_lookup="disabled"`,
    **`arm_enabled=False`**;
  - `:136` `app.state.bridge_engine = None`;
  - `:149` `if start_runtime and not credential_free_disarmed:` — broker construction is **never
    reached**, so `_build_broker`'s credential resolution (`:244`) and `network="testnet"` selection
    (`:246`) do not run. **No broker is constructed; ARM and orders are unavailable.**
  - `:133-134` on startup: `if store.get_meta("app_state") != "KILLED": store.set_meta("app_state",
    "DISARMED")`.
  - `:288` `uvicorn.run(runtime_app, host="127.0.0.1", port=8790, reload=False)`.
  - `:124` CORS origins are the two loopback forms only.
  - Endpoint form `/api/status` per `…/deploy/linux/COMMANDS.md:220` `[REF-INV]`.
  - `[HOST-OBS]`: transition inventory `:36-37` — credential-free DISARMED, `state_version=1`, all
    credential/network/exchange/ARM flags off, no credentials, broker or orders.
- **Mutation class.** `read-only-host`. **Only a `GET` is permitted.** No `POST`, no `PUT`, no
  `X-Confirm` header — the app's CORS config admits `GET/POST/PUT` and an `X-Confirm` header
  (`app.py:125-126` `[SRC]`), and a mutating call would change runtime and possibly persisted state.
- **Prerequisites.** `RK-B0`.
- **Proposed command shape:**
  ```bash
  # NOT EXECUTED — proposed shape only. GET only, on-host, over loopback.
  curl -sS --max-time 10 -X GET http://127.0.0.1:8790/api/status
  ```
  **Run it on the host over loopback.** Do **not** create an SSH tunnel for this stage: the tunnel
  form (`COMMANDS.md:230-234` `[REF-INV]`) opens an operator-machine path to 8790 that would
  invalidate `RK-B6`'s external-origin probe if the two overlapped (§4.7).
- **No-clobber artifact contract.** `NN_status.{cmd,out,err,rc}`; the JSON body is screened per §2.6
  before local retrieval.
- **PASS predicates (STOP-bearing).** `mode` = `credential_free_disarmed`; `network` = `disabled`;
  `exchange_conn` = `disabled`; `exchange_enabled` = `false`; `credential_lookup` = `disabled`;
  `arm_enabled` = `false`; the reported application state is `DISARMED`; HTTP rc `0` and a 200.
- **Recorded but non-STOP-bearing.** `state_version`, expected `1` `[HOST-OBS]` corroboration from
  the transition inventory. It is recorded, not adjudicated: this unit established only that the
  single increment site in `app.py` (`:160`, inside the `publish` closure) lives in the branch that
  **does not run** in this mode, and did not enumerate increment sites elsewhere in the API surface.
  A different value is **investigate read-only**, not a STOP (`D-GAP-B5-1`).
- **Failure / STOP.** Any flag on, `arm_enabled` true, `mode` other than
  `credential_free_disarmed`, or an application state other than `DISARMED` ⇒ **STOP**, investigate
  read-only, and do not proceed to any Group C stage. Connection refused or a non-200 ⇒ **STOP**
  (contradicts `RK-B2`'s active service and `RK-B6`'s listener).
- **Secrets/redaction.** In this mode no credential is resolved and none can appear in the payload
  (`app.py:149` `[SRC]`). The §2.6 screen is still applied before retrieval — belt and braces, since
  the screen is what makes the claim checkable rather than assumed.
- **Unresolved.** `D-GAP-B5-1` (state_version writer set) — see §10.

### 4.7 `RK-B6` — exactly one loopback listener · UFW SSH-only · external probe unreachable

- **Purpose.** Prove the control plane is reachable **only** from the host's own loopback: exactly one
  listener at `127.0.0.1:8790`, no wildcard or non-loopback listener, UFW active and SSH-only, and
  the port unreachable from an external origin.
- **Anchors.**
  - `[SRC]` `2ce41e34…321b:…/lib/common.sh:197-208` `assert_no_public_control_listener` — non-loopback
    listener on `:8790` is a failure; the awk filter admits `127.0.0.1:` and `[::1]:`.
  - `[SRC]` `…/lib/common.sh:210-220` `assert_control_port_closed` — **this one must NOT be used
    post-start**: it fails if *any* listener exists on 8790, which is the correct pre-start
    assertion and the wrong post-start one (`verify.sh:248`, and its scope comment at `:240-242`).
  - `[SRC]` `…/lib/common.sh:184-194` `assert_loopback_only_source` — static proof the entrypoint
    binds `127.0.0.1:8790` and contains no `0.0.0.0` / `host="::"`; corroborated by
    `app.py:288` `[SRC]`.
  - `[SRC]` `…/lib/common.sh:155-181` `assert_ufw_ssh_only` — fail-closed on: ufw not installed
    (`:156-157`), not active (`:161-164`), default incoming not deny (`:165-168`), any `ALLOW IN` rule
    outside `22|22/tcp|22/udp|OpenSSH` (`:169-176`), **or any mention of port 8790 at all**
    (`:177-179`).
  - `[SRC]` `…/lib/common.sh:29-30` — `MTC_BIND_HOST=127.0.0.1`, `MTC_BIND_PORT=8790`.
  - `[HOST-OBS]` A-8 evidence and transition inventory `:36`: `listener_count=1`, `127.0.0.1:8790`
    only, UFW `rc=0`, host-side `port8790_ok=False`.
- **Mutation class.** `read-only-host` for the on-host checks; the external probe is an
  **outbound TCP connect from the operator machine** and carries the same authority requirement.
- **Prerequisites.** `RK-B0`. **Additionally and critically:** assert that **no SSH local forward to
  8790 is active** at probe time. A live `ssh -L 8790:127.0.0.1:8790` (the `COMMANDS.md:233` form)
  would make the probe *succeed* against the operator's own machine and manufacture a false alarm —
  or, worse, a false sense of what the probe measured. Freeze this: **`RK-B5` uses on-host loopback,
  no tunnel is opened for any Stage B step, and the probe asserts the absence of a local forward
  before connecting.**
- **Proposed command shape:**
  ```bash
  # NOT EXECUTED — proposed shape only.

  # --- on host, read-only ---
  set -o pipefail                                # §2.5: a pipeline reports only its LAST member
  ss -H -ltn || STOP                             # full capture, verbatim; rc must be 0
  # ⛔ A bare `ss … | awk …` returns awk's rc. A failed or missing `ss` therefore yields empty output
  #    with rc 0 — byte-identical to the "no listener on 8790" result, which is a PASS token in
  #    §5.5, §6.2(9) and §8.5(5). pipefail + PIPESTATUS adjudication is what separates them.
  ss -H -ltn | awk '$4 ~ /:8790$/ { print $4 }'  # expect EXACTLY one line: 127.0.0.1:8790
  # required: final rc 0 AND every PIPESTATUS member 0; any non-zero member => STOP (§2.5a H4)
  sudo_rc ufw status verbose                     # priv_rc must yield 0; adjudicated by the table
                                                 # below. A sudo refusal is a STOP, not "no rules".

  # --- from the operator machine, external origin ---
  # 0. assert no local forward to 8790 exists in this session first (STOP if one does)
  # 1. TCP connect to <HOST_IP>:8790 with a bounded timeout — the A-8 TcpClient method.
  #    expect: connection refused or timeout. A successful connect is a HARD STOP.
  ```
- **No-clobber artifact contract.** Full `ss` capture, the derived 8790 filter, the ufw status text,
  and the probe result, each a four-file group. `<HOST_IP>` is **not** written into any committed
  record (§2.6).
- **PASS predicates.**
  - The 8790 filter returns **exactly one** line and it is exactly `127.0.0.1:8790`.
  - No `0.0.0.0:8790`, no `[::]:8790`, no VM-IP-bound listener.
  - `ufw`: installed, `Status: active`, `Default: deny (incoming)`, every `ALLOW IN` rule in
    `{22, 22/tcp, 22/udp, OpenSSH}`, **and no occurrence of `8790` anywhere in the status text**.
  - External-origin connect to `<HOST_IP>:8790` **fails** (refused or timed out).
- **⛔ Fail-closed dispositions — every one is a STOP, none is a SKIP or a PASS.**

  | Condition | Disposition |
  |---|---|
  | more than one listener on 8790 | **STOP** |
  | zero listeners on 8790 | **STOP** (contradicts `RK-B2` active + `RK-B5` responding) |
  | `ss` **absent, failing, or any non-zero `PIPESTATUS` member** | **STOP** — the empty output of a failed `ss` is not evidence of zero listeners, and must never be adjudicated as one |
  | any wildcard / non-loopback listener on 8790 | **STOP** |
  | `[::1]:8790` present in addition to `127.0.0.1:8790` | **STOP and investigate read-only.** It would pass `common.sh:202-203`'s loopback filter, but it violates the *exactly one* predicate and contradicts `app.py:288`'s single IPv4 bind. Do not silently accept it on the strength of the verifier's broader filter. |
  | `ufw` **not installed** | **STOP** — never SKIP. Mirrors `common.sh:156-157`. |
  | `ufw` **inactive** | **STOP** |
  | `ufw` default incoming not `deny` | **STOP** |
  | any non-SSH `ALLOW IN` rule | **STOP** |
  | `ufw` status mentions `8790` | **STOP** — the control plane must never be firewall-visible |
  | `ufw` **permission failure** / non-zero rc / unparsable output | **STOP** — never SKIP, never assume |
  | external probe **succeeds** | **HARD STOP** — the control plane is externally reachable |
  | external probe **cannot be run** (no operator path, tooling missing, ambiguous result, or a local forward is open) | **STOP** — inability to probe is a failure of this stage, not an exemption from it |
- **Secrets/redaction.** `ss -H -ltn` output contains local socket addresses only. `<HOST_IP>` stays
  out of committed records. The ufw status text is retained verbatim (it contains rules, not secrets).
- **Unresolved.** None in the predicate set. The external probe method is inherited from A-8
  `[HOST-OBS]` precedent rather than from candidate source — noted so its provenance is not
  overstated.

### 4.8 `RK-B7` — closeout, evidence manifest, retrieval

- **Purpose.** Make the whole stage's evidence tamper-evident and retrievable without clobbering
  prior evidence.
- **Mutation class.** `read-only-host`.
- **Proposed shape:**
  ```bash
  # NOT EXECUTED — proposed shape only.
  set -o pipefail
  cd "${EVROOT}" || STOP                 # ⛔ never `cd … && find …`: a failed cd must STOP, not
                                         #    silently skip the manifest build and leave no trace
  tok=$(classify_path "" "${EVROOT}/SHA256SUMS") || STOP "probe did not complete"
  [ "$tok" = NONE ] || STOP "SHA256SUMS is $tok"   # §2.4(3): an existing object OR a link is a STOP
  find . -type f ! -name SHA256SUMS -print0 | sort -z \
    | xargs -0 sha256sum > "${EVROOT}/SHA256SUMS"
  # required: final rc 0 AND every PIPESTATUS member 0. A `find` that hit an unreadable directory,
  # or an `xargs` that stopped early, produces a SHORTER manifest that still looks well-formed —
  # that is a STOP, never a smaller-but-valid manifest.
  sha256sum "${EVROOT}/SHA256SUMS" || STOP   # the EXTERNAL hash of the manifest file itself
  ```
  Then screen every `.out`/`.err` per §2.6, and copy the tree to `<LOCAL_EVROOT>`, whose destination
  must classify as **`NONE`** — neither a filesystem object nor a symlink (§2.3, §2.4(3)) — checked
  immediately before the copy. Record the external `SHA256SUMS` hash in the accepting record.
- **PASS.** Every artifact hashed; `SHA256SUMS` external hash recorded locally; local copy verified
  against it after transfer; secret screen clean.
- **Failure / STOP.** Secret-signature hit ⇒ **STOP**; preserve on host, do **not** copy down.
  `<LOCAL_EVROOT>` classifying as `FILE` **or** `LINK` ⇒ **STOP**, allocate a new `<RUNID>` rather
  than overwriting — a dangling link at that path is *not* an absent destination. A destination probe
  that cannot complete ⇒ **STOP**, never "assume absent and copy". Any non-zero rc from `cd`,
  `find`, `sort`, `xargs`, `sha256sum` or any `PIPESTATUS` member ⇒ **STOP**.
- **Unresolved.** None.

---

## 5. `RK-C1` — graceful stop / no dangling state (`mutating-host`)

**Predicate under test.** WP0 **I-R4 is explicitly OPEN**: *"No test asserts SIGTERM/lifespan shutdown
leaves no dangling state."* One authorised `systemctl stop` must show: exit within
`TimeoutStopSec=45`, **no SIGKILL escalation**, no restart, zero surviving `bridge.app`
writers/listeners, DB integrity intact, and protected persistent state unchanged.

**Authority.** Requires an explicitly named lift for **stop** — and **only** stop. The recovery start
is `RK-REC`, a **distinct later authorised action** that is *not* silently included here and is not
designed in this document.

**⛔ Execution block, independent of authority and budget.** Even with every lift granted, `RK-C1`
**must not be executed** while either of its two blocking gaps is open: `D-GAP-C1-1` (§5.2 — the exact
clean-stop `ExecMainStatus`/`Result` tuple) and `D-GAP-C1-3` (§5.4 — the exact safe active-writer
pre-stop capture method, or an independently accepted equivalent). Both must be **closed, accepted and
frozen in `RK-PRE` before the stop**. There is no reduced, weakened or baseline-free variant of this
stage that may be run instead, and no such variant may report PASS.

### 5.1 Anchors

| Fact | Anchor |
|---|---|
| `KillSignal=SIGTERM` `:48`, `KillMode=mixed` `:49`, `TimeoutStopSec=45` `:51`, `FinalKillSignal=SIGKILL` `:52`, `Restart=no` `:55`, `Type=exec` `:30` | `[SRC]` `2ce41e34…321b:…/systemd/mtc-bridge-first-start.service.template` |
| **The shutdown path performs no database write in this mode.** `lifespan` (`app.py:89-100`) calls `await engine.stop()` **only if** `app.state.bridge_engine is not None`; in credential-free DISARMED mode `:136` sets it to `None` and `:149` never replaces it. The `finally` branch therefore only logs *"Crypto Paper Bridge shutting down"*. | `[SRC]` `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py:89-100,136,149` |
| The process is `uvicorn.run(...)` under `python -m bridge.app` | `[SRC]` `app.py:288`; template `ExecStart` `:34` |
| A-5 proved **SIGKILL** + restart + state integrity + DISARMED — **not** graceful SIGTERM | `[GOV]` matrix G5 |
| `ExecMainStatus=9` / `Result=signal` is the recorded signature of the A-5 **SIGKILL** case | `[HOST-OBS]` `GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md:89,397` |

**Why the "no DB write on shutdown" anchor matters:** it is what makes strict pre/post equality of
protected persistent state a *sound* predicate for this stop, rather than an over-tight one that
would fail on a legitimately-writing shutdown. It is established from candidate source, and it is
the reason §5.4 can require equality rather than mere monotonicity for the protected subset.

### 5.2 ⛔ Do **not** hard-code `ExecMainCode=0` — and what to preregister instead

`ExecMainCode` is the `waitid` `si_code` `[SYSTEMD]`, not an exit status:

| `ExecMainCode` | Meaning `[SYSTEMD]` |
|---|---|
| `0` | **no main process has exited yet** — i.e. the *running* representation. This is why the A-5 records show `ExecMainCode=0; ExecMainStatus=0` for an **active** service (`GATE_A_A5_REPAIR_PREREGISTRATION_2026-08-09E.md:102`, `GATE_A_A5_FAIL_2026-08-09D.md:133`) `[HOST-OBS]`. |
| `1` (`CLD_EXITED`) | the main process **exited normally**; `ExecMainStatus` is then its exit status. **A clean Python/systemd stop is expected to land here.** |
| `2` (`CLD_KILLED`) | killed by a signal; `ExecMainStatus` is the signal number — the A-5 SIGKILL signature `ExecMainStatus=9`. |

**Preregistering `ExecMainCode=0` as a post-stop predicate would therefore be wrong twice:** it is the
*running* representation, and a clean exit surfaces as `CLD_EXITED`, not as `0`.

**⛔ `D-GAP-C1-1` — the exact clean-stop `ExecMainStatus` / `Result` tuple is an open preregistration
gap, and it BLOCKS the stage.** Whether uvicorn's graceful SIGTERM shutdown returns exit status `0`
(⇒ `Result=success`) or a non-zero status (⇒ `Result=exit-code`, unit enters `failed`) **is not
establishable from candidate source**: `app.py:288` hands control to `uvicorn.run` and the exit
contract lives in the pinned third-party dependency, not in the candidate tree. No located immutable
evidence records a *graceful stop* of this unit — A-5 recorded a SIGKILL. **This field is therefore
marked as a gap, not invented.**

**⛔ `exit-code` is NOT an accepted result, and there is no "accepted-pending-gap" set.** A non-zero
main-process exit status is precisely what a **failed** application shutdown looks like: an unhandled
exception on the way down, a lifespan-teardown error, or an abnormal uvicorn exit path — and systemd
then places the unit in `failed`. Admitting `exit-code` while the correct value is unknown would let a
failed shutdown be recorded as a PASS for a stage whose entire subject is *whether the shutdown was
clean*. The gap is therefore **blocking**, not tolerated:

| Field | Preregistered disposition |
|---|---|
| `ExecMainCode` | **must not be `2` (`CLD_KILLED`)**; a clean stop must land on `1` (`CLD_EXITED`). Recorded verbatim. **Never hard-code `0`** — that is the *running* representation (table above), and preregistering it would be wrong twice over. |
| `ExecMainStatus` | **must not be `9`** (SIGKILL) and must not be any signal number. Its exact accepted value **is** `D-GAP-C1-1`: recorded verbatim, and **not adjudicable** until the gap closes. |
| `Result` | **`signal`, `timeout`, `watchdog`, `core-dump`, `start-limit-hit` and `exit-code` are each a STOP.** The one accepted value is whatever is frozen when `D-GAP-C1-1` closes — `success` **if and only if** the pinned dependency's SIGTERM contract is shown to be exit status `0`. **No value is accepted before that freeze.** |
| `NRestarts` | must remain `0`. |

**Consequence — the stage is blocked, not degraded.** While `D-GAP-C1-1` is open there is no
preregistered pass value for the stop's own outcome, so **`RK-C1` must not be executed and cannot
obtain a PASS.** §5.3 does not rescue it: those three legs prove **no SIGKILL escalation**, which is a
strictly weaker claim than **the application shut down successfully**. A process that exits non-zero
on its own — promptly, quietly, and without systemd ever having to escalate — satisfies all three legs
of §5.3 while failing the predicate this stage exists to test.

**Closing `D-GAP-C1-1` (route, NOT executed here).** Determine the pinned uvicorn version's SIGTERM
exit contract from the 56-entry lock plus that version's own source, together with the documented
systemd mapping from that exit status onto `ExecMainCode`/`ExecMainStatus`/`Result` — a *local,
offline* determination from pinned dependency and systemd evidence, requiring no host and no
product-test execution. Freeze the resulting exact tuple in `RK-PRE`. If it cannot be established that
way, **it stays unresolved and `RK-C1` stays blocked.** It is never closed by running one stop and
back-filling whatever that stop produced: that would adjudicate the predicate against its own outcome
(§12 stop condition 9).

### 5.3 Proving no SIGKILL escalation under `KillMode=mixed` — three independent legs

Final inactivity is **insufficient**: a unit SIGKILLed at the 45 s boundary is also inactive.
`KillMode=mixed` `[SRC]` sends `KillSignal` to the main process and, at the final timeout, `SIGKILL`
to everything remaining in the cgroup. All three legs are required:

1. **Elapsed time.** Wrap the blocking `systemctl stop` in a UTC clock read
   (`date -u +%s.%N` before and after). **PASS: elapsed ≤ 45 s**, and a healthy graceful stop is
   expected to be far below it. Elapsed ≥ 45 s is a **STOP** on its own — it means the timeout was
   reached and `FinalKillSignal=SIGKILL` `:52` fired.
2. **Bounded journal evidence.** `journalctl -u mtc-bridge-first-start.service --since "<pre-stop
   UTC>" --until "<post-stop UTC>" --no-pager -o short-iso -n 200` — bounded by both a time window
   and a line cap.
   - **Required present:** the stop transition lines (`Stopping …` / `Stopped …`).
   - **Required ABSENT (each is a STOP):** any `state 'stop-sigterm' timed out`,
     `Killing process … with signal SIGKILL`, `Main process exited, code=killed, status=9/KILL`,
     `Failed with result 'timeout'`, or `Failed with result 'signal'`.
   - Journal text is screened per §2.6 before retrieval (A-9 proved zero secret-signature hits in
     this service's logs `[GOV]`, which is corroboration, not a licence to skip the screen).
3. **Zero surviving writer / process.** `pgrep -f '[b]ridge\.app'` returns nothing (the exact bracket
   idiom of `…/verify.sh:243` `[SRC]`, which avoids matching the `pgrep` invocation itself);
   `ss -H -ltn` shows **no** listener on 8790; and the unit's cgroup
   (`systemctl show -p ControlGroup --value`) holds no processes.
   **⛔ Adjudicate the rc, not the emptiness.** All three of these predicates PASS on *empty output*,
   which is exactly what a failed tool also produces. `pgrep` rc `1` (no match) is the required
   answer; rc `0` means a writer survived ⇒ **STOP**; **rc `2` (syntax) or `3` (fatal) is a STOP**,
   never "no writer". `ss` runs under `pipefail` with every `PIPESTATUS` member adjudicated (§4.7).
   `systemctl show` must exit `0` with a parsed value; a blank cgroup line from a failed call is a
   **STOP**, not an empty cgroup (§2.5a H3).

Together: exited well inside the window **and** no escalation message **and** nothing survived. Any
one leg missing ⇒ the escalation claim is unproven ⇒ **STOP**.

**⛔ What these three legs do NOT prove.** They establish that **systemd never had to escalate** — no
`stop-sigterm` timeout, no `FinalKillSignal`, no survivors. They say **nothing** about whether the
application's own shutdown *succeeded*: a process that exits non-zero of its own accord does so
quickly, leaves no survivor, and produces no escalation line. Successful shutdown is adjudicated by
the exit tuple of §5.2, which is `D-GAP-C1-1` and blocking. **No run-kit may present the §5.3 legs as
a substitute for the missing exit tuple, and no PASS may be assembled from them alone.**

### 5.4 Pre-stop freeze and post-stop equality for protected persistent state

**Pre-stop freeze — and why no chain ordering makes it free.** The `RK-C1` predicate under test is
*the stop did not mutate protected persistent state*. That is a **difference** predicate: it needs a
baseline captured **while the service is still ACTIVE**, i.e. strictly before the `systemctl stop`.
Record it as `<PRE_BUNDLE_DB_SHA256>` and `<PRE_INVARIANTS_SHA256>` using the `RK-C3` method (§7).

**⛔ A post-stop capture can never serve as this baseline — in any chain, under any label.** In
**Chain B** the `RK-C3` capture is ordered *after* `RK-C1` (§2.2), so it is not a pre-stop capture at
all; comparing the post-stop invariants against it compares the post-stop state **with itself**. That
comparison is **vacuously equal** and proves nothing about the stop. Chain B therefore does not make
this stage "trivially clean" — it removes the *baseline*, not the *requirement*. **A post-stop
baseline is invalid and is forbidden outright** (§12 stop condition 9); it may not be re-labelled a
"reference capture", a "post-quiesce baseline" or anything else and then compared.

**⛔ `D-GAP-C1-3` — the pre-stop baseline needs a live-writer capture, and none is established.** The
capture-while-ACTIVE problem of `D-GAP-C2-1` (§6.4: the tool's own *"never use this for a cutover
capture"* rule for `--allow-live-source`, plus read-only WAL access requiring `-shm` write) binds
`RK-C1` **intrinsically**, not as a property of the frozen branch: the baseline must be taken
immediately before the stop, when the service is by definition still ACTIVE. Chain B — the only chain
that contains `RK-C1` at all (§2.2) — schedules no pre-stop capture whatsoever. Routes, mirroring
§6.4 — none executed here, none supplying a command:

| Route | Admissible? | Effect |
|---|---|---|
| **(a)** close the gap offline: analyse the tool's hot-WAL/shm gates (`2ce41e34…321b:…/tools/wal_state_bundle.py:237,270,318,342` `[SRC]`) against the deployment's SQLite version, then preregister an **exact safe active-writer capture command** and freeze it in `RK-PRE` | ✅ **admissible — this is what unblocks `RK-C1`** | equality becomes **adjudicable in full**; the protected pre/post equality requirement is satisfied as written |
| **(d)** an **independently accepted equivalent that proves the same pre/post persistence property** — e.g. a prior accepted immutable capture carrying a recorded `invariants_sha256` whose intervening window is *shown* (not assumed) writer-free | ✅ **admissible if it exists — also unblocks `RK-C1`** | equality adjudicable against that baseline. **This design locates no such capture and asserts none exists**; it must be produced and accepted on its own merits, never assumed into being |
| **(b)** take the baseline with `--allow-live-source`, labelled warning-class provenance | ⛔ **NOT admissible as an execution route** | the tool's own contract says a live-source capture is not a cutover or comparison proof (§6.4(1)). It may be captured as diagnostic material while closing route (a), but **`RK-C1` stays blocked and may not obtain a PASS on it.** A weakened baseline does not buy a weakened PASS |
| **(c)** take **no** pre-stop baseline and run the stop anyway | ⛔ **NOT admissible — this is the laundering route** | it deletes the stage's central predicate and reports the remainder as an outcome. There is no "PASS for the legs that could be run". **`RK-C1` stays blocked** |
| ⛔ **post-stop "baseline"** | ⛔ **never, under any name** | vacuously equal; proves nothing about the stop (§12 stop condition 9) |

**⛔ The protected pre/post equality requirement is mandatory and may not be negotiated downward.** It
may not be dropped, demoted to "recorded only", relaxed to a warning-class comparison, replaced by the
§5.3 legs, or satisfied by the absolute `app_state` row alone. **`RK-C1` is blocked from execution
until route (a) or route (d) is established, accepted and frozen in `RK-PRE`** — together with the
`D-GAP-C1-1` tuple of §5.2 — **and it can obtain a PASS only under that freeze.** Choosing a route
after the fact, from what some capture turned out to show, would adjudicate the predicate against its
own outcome: the same defect §6.1 forbids for the reboot scenario.

**Post-stop verification (after the stop, writer now quiesced):** re-capture with `RK-C3` and compare
against the frozen route (a)/(d) baseline.

| Invariant field (`collect_invariants`, `2ce41e34…321b:…/tools/wal_state_bundle.py:457-467` `[SRC]`) | Post-stop predicate |
|---|---|
| `app_state` (`:459`, from `meta`) | ∈ {`DISARMED`, `KILLED`} and **never `ARMED`** |
| `live_orders` (`:462`, `orders.status IN ('OPEN','SUBMITTED','PENDING')`, `:144`) | **equal** to the pre-stop value |
| `open_trades` (`:461`, `trades.exit_ts IS NULL`) | **equal** |
| `closed_trades` (`:463`) | **equal** |
| `counts.orders`, `counts.trades`, `counts.fills` (`:429-432`, `COUNT_TABLES` `:129-142`) | **equal** |
| `max_ids.trade_id` (`:453`) | **equal** |
| `environments` (`:465`, per-environment realized PnL / consecutive losses) | **equal** |
| `risk_days` (`:466`, the risk-day ledger) | **equal** |
| `invariants_sha256` (`invariants_hash`, `:561`) | **equal** — the single-value form of all of the above |
| `counts.events`, `counts.decisions`, `max_ids.event_id`, `max_ids.decision_id` | recorded; **strict equality expected** given §5.1's no-write-on-shutdown anchor, but a *monotonic non-decrease* is treated as **investigate read-only**, not an immediate STOP (`D-GAP-C1-2`) |

**⛔ Baseline dependence of the rows above.** Every row whose predicate is **equal** (or
non-decrease) is a *difference* predicate and is adjudicable **only** against a route (a) or route (d)
pre-stop baseline. There is no admissible route under which these rows are simply dropped and the
stage runs anyway: **absent such a baseline the stage does not execute at all.** The `app_state` row
is the one **absolute** predicate here — it reads a single persisted value and needs no baseline — but
it is a fraction of the stage, and **a PASS may never be reported on the strength of the absolute rows
alone.**

**Why equality is legitimate here and not over-tight:** §5.1 establishes from candidate source that
in credential-free DISARMED mode the shutdown path performs no engine stop and no database write.
**The run-kit must additionally guarantee no API mutation between freeze and verification:** only
`GET /api/status` may be issued in that window, and the run-kit records that fact explicitly.
**This establishes that equality is the *right* predicate; it does not supply the baseline the
predicate needs.** Soundness of the predicate and availability of a baseline are separate questions,
and `D-GAP-C1-3` is about the second one.

**DB integrity on a safe copy — never on the active/production file.** Run
`PRAGMA quick_check` and `PRAGMA foreign_key_check` **on the bundle's copy**, not on
`/var/lib/mtc-bridge/bridge.db`. The candidate tool already runs `PRAGMA integrity_check` and
`PRAGMA foreign_key_check` on both ends (`…/wal_state_bundle.py:405-411`, and the create/verify call
sites `[SRC]`); `quick_check` is the bounded complement and is run by the `RK-C3` wrapper against the
restored temporary copy. **The production database is never the subject of a test.**

### 5.5 `RK-C1` command shape, artifacts, dispositions

```bash
# NOT EXECUTED — proposed shape only. Requires an explicit named STOP authority + budget lift,
# AND is BLOCKED from execution until D-GAP-C1-1 (§5.2) and D-GAP-C1-3 (§5.4) are closed and frozen.
U=mtc-bridge-first-start.service

# pre-stop record
date -u +%Y-%m-%dT%H:%M:%SZ                  > "${EVROOT}/10_prestop_utc.out"
systemctl show "${U}" -p ActiveState -p SubState -p MainPID -p NRestarts \
                      -p ExecMainCode -p ExecMainStatus -p Result -p ControlGroup
curl -sS --max-time 10 -X GET http://127.0.0.1:8790/api/status   # GET only
# ... RK-C3 pre-state capture — LIVE WRITER: see D-GAP-C1-3 (§5.4). NO command is supplied here.
#     It exists only once route (a) or route (d) of §5.4 is established, accepted and frozen in
#     RK-PRE. There is no "run it without a baseline" variant: absent that freeze, NOTHING BELOW
#     THIS LINE RUNS AT ALL.

# ⛔ MUTATION GATE (§2.5). Every command above must have been RECORDED and ADJUDICATED PASS before
#    this line is reached. A failed, unadjudicated or unrecorded precondition forbids the mutation
#    outright — there is no "record the rc and stop anyway", and no "the read failed, so proceed".
# THE SINGLE AUTHORISED MUTATION — exactly one attempt, no retry
T0=$(date -u +%s.%N)
sudo systemctl stop "${U}"
T1=$(date -u +%s.%N)

# post-stop record
systemctl is-active "${U}"                    # expect: inactive
systemctl show "${U}" -p ActiveState -p SubState -p NRestarts \
                      -p ExecMainCode -p ExecMainStatus -p Result -p ControlGroup
pgrep -f '[b]ridge\.app'
# required: rc 1 (no match) AND no output. rc 0 => a writer survived => STOP.
# ⛔ rc 2 (syntax) or 3 (fatal) also print nothing — they are STOPs, never "no writer survived".
set -o pipefail
ss -H -ltn | awk '$4 ~ /:8790$/ { print $4 }'
# required: rc 0, every PIPESTATUS member 0, and no output. A failed `ss` in a bare pipeline yields
# exactly this empty output with rc 0, which is why the PIPESTATUS vector is adjudicated (§2.5).
journalctl -u "${U}" --since "<T0 UTC>" --until "<T1 UTC>" --no-pager -o short-iso -n 200
# required: rc 0. An empty journal capture from a failed/denied journalctl must NOT be adjudicated
# as "none of the escalation lines are present" — that is the §5.3 leg-2 PASS token (STOP instead).
# ... RK-C3 post-state capture + invariant comparison
```

- **Artifacts.** Four-file groups for every command, plus `10_prestop_utc.out`, an elapsed-time
  record derived from `T1 − T0`, the journal capture, and the pre/post invariant hashes. All under
  `<EVROOT>` per §2.4.
- **⛔ Execution gate — reached before any PASS predicate is even evaluable.** `RK-C1` must not be run
  while `D-GAP-C1-1` (§5.2) or `D-GAP-C1-3` (§5.4) is open. The list below is **preregistered for the
  post-closure state**; it is not a menu from which a runnable subset may be selected today, and a
  run-kit that executes the stop and then reports whichever items it managed to evaluate has violated
  this contract.
- **PASS (all required, none optional).** elapsed ≤ 45 s; `is-active` = `inactive`; `NRestarts` = `0`;
  `ExecMainCode` = `1` (`CLD_EXITED`), never `2`, never hard-coded `0`; `ExecMainStatus` = the exact
  value frozen when `D-GAP-C1-1` closed, and never `9` or any other signal number; `Result` = the
  single value frozen with it — **`exit-code` is not accepted, pending or otherwise**; journal shows
  the stop transition and **none** of the escalation lines; zero `bridge.app` processes; zero
  listeners on 8790; empty cgroup; `quick_check`/`foreign_key_check` clean on the safe copy;
  `app_state` never `ARMED`; **and** the protected invariant subset of §5.4 **equal** against the
  frozen route (a)/(d) pre-stop baseline. **There is no partial PASS, no "PASS for the legs that could
  be run", and no PASS that omits the equality rows or the exit tuple.**
- **Failure / STOP.** Any of: elapsed ≥ 45 s; a SIGKILL/timeout journal line; `ExecMainCode=2` or
  `ExecMainStatus=9`; `Result` ∈ {`signal`, `timeout`, `watchdog`, `core-dump`, `start-limit-hit`,
  **`exit-code`**}; `Result` anything other than the frozen accepted value; `NRestarts` ≠ 0; a
  surviving writer or listener; integrity/foreign-key failure; any protected-invariant drift **against
  the frozen pre-stop baseline** (drift against a post-stop self-comparison is not a finding — it is a
  malformed comparison, and reporting either its agreement or its disagreement is a defect). On any
  of these: **preserve all evidence, change nothing, do not retry the stop, do not start the
  service.** Treat it as a candidate repair need feeding the re-audit picture, not a documentation
  outcome.
- **Explicitly NOT included.** The recovery start. `RK-REC` is a separate authority unit; this design
  neither performs nor authorises it, and a run-kit that appends a start to this stage violates the
  authority envelope.
- **Secrets/redaction.** Journal text screened per §2.6 before retrieval; only `GET` on the API.
- **D026.** If a new SIGTERM-shutdown regression test is later offered as closure for I-R4, it must be
  demonstrated RED-then-GREEN with real recorded output. This stage produces operational evidence,
  **not** D026 closure, and must not be described as closing I-R4 by itself.
- **Unresolved.** **`D-GAP-C1-1` (exact clean-stop `ExecMainStatus`/`Result` tuple) and `D-GAP-C1-3`
  (no established active-writer pre-stop baseline method) are both BLOCKING**: while either is open
  `RK-C1` is not executable and cannot PASS. `D-GAP-C1-3` closes only by route (a) or route (d) of
  §5.4 — the weakened (b) and baseline-free (c) routes are not execution routes, and a post-stop
  baseline is invalid. `D-GAP-C1-3` shares its root cause with `D-GAP-C2-1` but is **not** discharged
  by any chain freeze. `D-GAP-C1-2` (exact shutdown-write set for the non-protected count fields)
  remains open and non-blocking: those rows are investigate-read-only, and the protected subset still
  requires strict equality.

---

## 6. `RK-C2` — reboot safety (`mutating-host`)

### 6.1 Two mutually exclusive scenarios — freeze exactly one before the reboot

| | **Scenario A — plain reboot (bounded `RK-C2`-only branch)** | **Scenario B — reboot after the authorised stop+mask** |
|---|---|---|
| Starting state | **active + unmasked** (the current accepted state) | **inactive + masked** (after `RK-C1`, `RK-C3` and `RK-C4`, or an explicitly authorised mask) |
| Ordering | **terminal branch** after `RK-B7`: `RK-PRE → RK-B0..B7 → RK-C2/A`, and **nothing in Group C follows it** (§2.2). **There is no `RK-C2/A → RK-C1` edge** | runs **after** `RK-C4`, as the last stage of Chain B (§2.2) |
| Expected post-reboot unit state | **inactive + UNMASKED**, `is-enabled` = `static` | **inactive + MASKED**, `is-enabled` = `masked` |
| State the branch/chain leaves behind | host **inactive + unmasked**. Reaching `RK-C1` afterwards would need a separately authorised `RK-REC` start **and** a fresh accepted Stage B recapture (§2.2) — neither is included, implied or costed here | host **inactive + masked**; `RK-REC` remains a separate authority unit |
| Pre-reboot persisted-state capture | ⛔ taken while the writer is ACTIVE → **`D-GAP-C2-1`** | ✅ taken with the writer already stopped → no gap **for this capture** |
| `RK-C1` **pre-stop** baseline (§5.4) | **not applicable — Branch A contains no `RK-C1`** | ⛔ live-writer capture → **`D-GAP-C1-3`**; Chain B schedules no pre-stop capture at all, which removes the baseline rather than the gap |
| Executability today | blocked by budget/authority and carries `D-GAP-C2-1`, but is **self-contained** and does not depend on the `RK-C1` gaps | additionally **blocked at `RK-C1`** — the chain cannot start until `D-GAP-C1-1` and `D-GAP-C1-3` close (§5.2, §5.4) |
| Recommendation | the only branch reachable without closing the `RK-C1` gaps; bounded evidence only | **preferred freeze for the reboot capture itself**; it closes nothing for `RK-C1` |

**A reboot does not create a mask.** Mask state is preserved across reboot, not manufactured by it
(matrix G1). A masked post-reboot state is valid **only** if a separately authorised pre-reboot step
masked the unit first. The future execution **must record the frozen scenario in `RK-PRE` before the
reboot** and must not decide it afterwards from what it observes — that would be adjudicating a
predicate against its own outcome.

**The safety predicate is DISARMED-by-absence** — no process, no listener, no order — **NOT** an
auto-restarted DISARMED service. Do not infer an auto-restart promise, and do not yet label the
absence of `[Install]`/auto-start as a product defect (matrix G1).

**⛔ Scenario A ends the run.** Because no `[Install]` exists and nothing auto-starts, the host is left
**inactive + unmasked** when `RK-C2/A` completes. That is a valid terminal state and it is where the
branch stops. A run-kit **must not** continue into `RK-C1`, `RK-C3` or `RK-C4` from there, and **must
not** start or unmask the service to make continuation possible — that start is `RK-REC`, a separate
authority unit that this design neither performs nor authorises (§2.2, §11).

### 6.2 Proving no boot activation, broadly

The claim is *the unit cannot be pulled in at boot by any route*. Unit state alone does not prove it;
all of the following are required.

| # | Check | Expected | Anchor |
|---|---|---|---|
| 1 | `systemctl is-active` | `inactive` | — |
| 2 | `systemctl is-enabled` | `static` (A) / `masked` (B) — the §4.3 rejection table applies unchanged | `[SRC]` `verify.sh:218-221`; `[SYSTEMD]` |
| 3 | no `[Install]` in the fragment | `grep -c '^\[Install\]'` = `0` | `[SRC]` template `:11`; `verify.sh:198-202` |
| 4 | no reverse dependency | `systemctl list-dependencies --reverse --all <U>` names only the unit; `systemctl show -p WantedBy -p RequiredBy -p UpheldBy --value` all empty | `[SYSTEMD]` |
| 5 | no `.wants` / `.requires` symlink anywhere | `find /etc/systemd/system /usr/local/lib/systemd/system /usr/lib/systemd/system /run/systemd -name 'mtc-bridge*' -print` returns only the expected set (fragment; plus the `/dev/null` mask symlink in scenario B). **`find` rc must be `0`:** a permission denial or a missing search root makes `find` exit non-zero while still printing a *shorter* list, and a short list is the PASS shape here — so a non-zero rc is a **STOP**, never "no extra symlink found" (§2.5a) | `[SRC]` `common.sh:23-25` for the two canonical dirs |
| 6 | no generated / transient / alias / linked route | `systemctl show -p FragmentPath -p SourcePath -p Names -p Following -p Transient --value`: `FragmentPath` = `/usr/local/lib/systemd/system/mtc-bridge-first-start.service`; `Transient=no`; `Names` = the single unit name; `Following` empty; **nothing** under `/run/systemd/generator*` | `[SYSTEMD]` |
| 7 | no timer / socket / path activation unit | `systemctl list-units --all --type=timer --type=socket --type=path` shows no `mtc-bridge*`; and the `find` in (5) surfaces no `mtc-bridge*.timer|.socket|.path` | `[SYSTEMD]` |
| 8 | steady profile absent | `classify_path` on **both** `/usr/local/lib/systemd/system/mtc-bridge-steady.service` and `/etc/systemd/system/mtc-bridge-steady.service` must return **`NONE`**. `FILE` or `LINK` (a dangling link included — it is still an installed unit name) ⇒ **STOP**; a probe that does not complete ⇒ **STOP** | `[SRC]` `verify.sh:224-231` |
| 9 | zero surviving writer / listener | `pgrep -f '[b]ridge\.app'` **rc 1** with no output (rc 0 ⇒ writer survives ⇒ STOP; **rc 2/3 ⇒ STOP**, never "none"); `ss -H -ltn` under `pipefail` with every `PIPESTATUS` member `0` and nothing on 8790. **Empty output is not the predicate — the rc is** (§2.5a H3) | `[SRC]` `verify.sh:243-247`; `common.sh:197-220` |
| 10 | `NRestarts` = `0` | — | `[SRC]` template `Restart=no` `:55` |

Any check that cannot be performed ⇒ **STOP**, never SKIP. **Note the shape of the risk here: nine of
these ten checks PASS on an empty or short result, which is precisely what a denied, missing or
crashed tool also produces.** Each is therefore adjudicated on its recorded rc through the §2.5a
helpers, never on the emptiness of its stdout.

### 6.3 Persisted DB must not be ARMED — and no order effect

**Persisted state, not inferred state.** After the reboot the service is not running, so the DB is
quiesced and can be captured cleanly with the `RK-C3` method. Read `invariants.app_state` from the
bundle manifest (`collect_invariants` `:459` reads it from the `meta` table `[SRC]`; `create_app`
`:133-134` is what writes `DISARMED` on a start `[SRC]`).

- **PASS:** `app_state` ∈ {`DISARMED`, `KILLED`} and **never `ARMED`**.
- **STOP:** `app_state` = `ARMED`, or unreadable.
- **⛔ Do not infer an auto-restarted DISARMED service.** The predicate is *persisted state is not
  ARMED* **plus** *DISARMED-by-absence* (checks 1, 9 above) — not "the service came back up
  DISARMED", which would be a different and unauthorised claim.

**Pre/post persisted order-state comparison (required — not process absence, not API state).**
Freeze the pre-reboot invariants and compare the post-reboot invariants field by field:

| Field | Predicate | `[SRC]` anchor in `…/tools/wal_state_bundle.py` |
|---|---|---|
| `counts.orders` | **equal** | `:429-432` over `COUNT_TABLES` `:129-142` |
| `counts.trades`, `counts.fills` | **equal** | as above |
| `live_orders` | **equal** | `:434-440`, statuses `OPEN`/`SUBMITTED`/`PENDING` `:144` |
| `open_trades` | **equal** | `:441-443` (`trades.exit_ts IS NULL`) |
| `closed_trades` | **equal** | `:444-448` |
| `max_ids.{trade_id, decision_id, event_id}` | **equal** | `:450-455` |
| `environments` | **equal** | `:465` / `_environment_invariants` `:475` |
| `risk_days` | **equal** | `:466` / `_risk_day_invariants` `:539` |
| `app_state` | as above | `:459` |
| `invariants_sha256` | **equal** — the single-value summary | `invariants_hash` `:561` |

Equality of `invariants_sha256` across the reboot **is** the "no order effect" proof: it is derived
from the persisted `orders`/`trades`/`fills`/`risk_days` tables, not from process presence and not
from the status API. Strict equality is sound here because between the freeze and the re-read the
service is either stopped (Scenario B) or is running in a mode that constructs no broker, runs no
engine and issues no order (`app.py:136,149` `[SRC]`), and the run-kit issues only `GET`.

### 6.4 ⛔ `D-GAP-C2-1` — the named design gap in Scenario A

**Statement.** In Scenario A the pre-reboot capture must read `/var/lib/mtc-bridge/bridge.db` while
the service is ACTIVE. **No exact safe command for that is established**, for two independent
reasons:

1. **The tool's own contract.** `create` without `--allow-live-source` fails closed on source drift;
   `--allow-live-source` downgrades drift to a warning and the tool's own help says *"Never use this
   for a cutover capture: the writer must already be quiesced"*
   (`…/wal_state_bundle.py:1222-1228` `[SRC]`). A live-source capture is a **warning-class
   provenance record, not a cutover or comparison proof**.
2. **Read-only access to a live WAL database.** A read-only SQLite connection to a WAL database
   generally requires write access to the `-shm` file `[SYSTEMD]`-class external semantics (SQLite,
   not systemd). The tool opens the source read-only (`_connect_readonly` `:342` `[SRC]`) and has
   explicit hot-WAL / usable-shm gates (`_wal_is_hot` `:237`, `_shm_holds_usable_wal_index` `:270`,
   `_shm_is_structurally_usable` `:318` `[SRC]`), **none of which has ever been exercised against
   this host.**

**What is *expected but not established*:** in credential-free DISARMED mode no engine exists
(`app.py:136,149` `[SRC]`), so the live database has no active writer beyond `Store.initialize()` and
the one-time `set_meta("app_state","DISARMED")` at startup (`app.py:130-134` `[SRC]`). A capture run
**as the `mtc-bridge` user** (so any tool-materialised sidecar keeps correct ownership) would
therefore be *expected* to succeed without drift. **That is an expectation, not a fact, and it is not
converted into one here.**

**Resolution routes for the implementer (all local/offline, none executed here):**
(a) freeze **Chain B** instead, where the gap does not arise **for the reboot capture** — noting two
    things: it closes nothing for `RK-C1`, whose pre-stop baseline still needs a live-writer capture
    (`D-GAP-C1-3`, §5.4), and Chain B cannot start at all until the `RK-C1` gaps close, so this route
    trades `D-GAP-C2-1` for the `RK-C1` execution block rather than removing a blocker;
(b) close the gap by offline analysis of the tool's hot-WAL/shm gates against the deployment's
    SQLite version, then preregister the exact command;
(c) accept a `--allow-live-source` capture **explicitly labelled warning-class provenance**, and
    correspondingly **weaken the Scenario A pre/post predicate** to what a warning-class baseline can
    support — recording that weakening in the accepting record rather than presenting it as a full
    proof.

**Until one of these is chosen and recorded, Scenario A's pre-reboot capture command is a `[GAP]`,
and this design does not supply one.**

### 6.5 `RK-C2` command shape, artifacts, dispositions

```bash
# NOT EXECUTED — proposed shape only. Requires an explicit named REBOOT authority + budget lift.
# Scenario (A or B) must already be frozen in RK-PRE.

# 1. pre-reboot: full RK-B2/B4/B6 subset re-capture + RK-C3 pre-state capture
#    (Scenario A: see D-GAP-C2-1 — no command is supplied here)
# 2. THE SINGLE AUTHORISED MUTATION:
sudo systemctl reboot
# 3. on return, read-only only — checks 1..10 of §6.2, then the RK-C3 post-state capture
#    and the field-by-field invariant comparison of §6.3
# 4. SCENARIO A ONLY: the branch ENDS HERE, with the host inactive + unmasked. Do not continue
#    into RK-C1/C3/C4, and do not start or unmask anything to make continuation possible (§2.2).
```

- **Artifacts.** Pre- and post-reboot four-file groups under two distinct no-clobber roots
  (`<EVROOT>` for pre, a freshly allocated `<EVROOT>` for post — the reboot ends the session, so the
  post root is separately allocated and both are retrieved).
- **PASS.** All ten checks of §6.2 pass for the frozen scenario; `app_state` not `ARMED`; every field
  in §6.3 equal; `invariants_sha256` equal.
- **Failure / STOP.** Any writer, any listener, `app_state` = `ARMED`, a mask-state mismatch against
  the **frozen** scenario, any boot-activation route found, or any invariant drift ⇒ **STOP**,
  preserve everything, start nothing.
- **Secrets/redaction.** §2.6 applies unchanged; the bundle manifest is sanitised by construction
  (`…/wal_state_bundle.py:27-34,188` `[SRC]`).
- **Explicitly NOT included (Scenario A).** Any continuation past the post-reboot checks: no
  `RK-C1`, no recovery start, no unmask, no Stage B "top-up" against a service that is not running.
  Branch A is terminal by design (§2.2, §6.1).
- **Unresolved.** `D-GAP-C2-1` (Scenario A pre-capture). Also noted: the `[SYSTEMD]` expectations for
  checks 4, 6, 7 have never been observed on this host and become `[HOST-OBS]` only on first run.

---

## 7. `RK-C3` — WAL bundle · verify · restore-into-temp (`mutating-host`)

### 7.1 Hard boundaries, stated first

- **⛔ The candidate CLI has exactly two subcommands: `create` and `verify`. There is NO `restore`
  subcommand.** `[SRC]` `2ce41e34…321b:…/tools/wal_state_bundle.py:1216` (required subparser),
  `:1218` (`create`), `:1232` (`verify`). Any future run-kit, prompt or record claiming a `restore`
  subcommand is wrong. The restore step below is a **wrapper this design specifies and a future
  implementer must author**, not an existing capability.
- **No active-DB destructive test.** `/var/lib/mtc-bridge/bridge.db` is never overwritten, restored
  into, migrated, vacuumed, repaired, or otherwise mutated by any step here.
- **No direct db/wal/shm trio copy.** The tool exists precisely because that copy is unsafe: it uses
  the SQLite online backup API rather than copying the trio (`:14-16` `[SRC]`), and fails closed on
  sidecar presence in the bundle (`FORBIDDEN_SIDECARS` `:87` `[SRC]`). The run-kit must not
  reintroduce a trio copy anywhere, including in the restore wrapper.

### 7.2 Prerequisites (all required before the first command)

| # | Prerequisite | Check |
|---|---|---|
| 1 | **Quiesced writer or safe source copy.** Applies to every capture taken with the service down: in Chain B the writer is already stopped by `RK-C1`, and the `RK-C2` post-reboot capture is quiesced in both scenarios. **It does NOT apply to the two live-writer captures**, neither of which has a command in this design: the `RK-C1` pre-stop baseline of §5.4 (`D-GAP-C1-3`, blocking) and the Branch A pre-reboot capture of §6.4 (`D-GAP-C2-1`) | `systemctl is-active` = `inactive`; `pgrep -f '[b]ridge\.app'` empty |
| 2 | **Output directory and files absent — including as dangling symlinks.** `<EVROOT>/bundle.staging` must not exist; `bridge.db`, `bundle_manifest.json` and `.bundle_manifest.json.tmp` must not exist within it | plain `mkdir` (no `-p` on the leaf), then **`classify_path` on each** with required token **`NONE`**. `FILE` **or** `LINK` ⇒ **STOP** — `test -e` alone calls a dangling symlink absent while a subsequent write follows it onto its target. A probe that does not complete ⇒ **STOP** |
| 3 | **Non-symlink and canonicalised beneath `<EVROOT>`** | `classify_path` on each (`NONE` for a destination, `FILE` for an existing input; **`LINK` is always a STOP**), plus a `realpath` prefix check whose **rc is adjudicated** — a failed `realpath` is a STOP, never an unverified path admitted on empty output |
| 4 | **No `--force`.** The flag exists (`:1230` `[SRC]`) and bypasses the "output directory already holds a bundle" guard at `:740-741`. **It is forbidden in every run-kit invocation.** | absent from argv |
| 5 | **Source / destination / bundle / restore paths all distinct.** The tool already rejects source↔output aliasing and output↔output aliasing (`_resolve_capture_paths` `:678-715` `[SRC]`), covering `bridge.db`, `-wal`, `-shm`, the manifest and the manifest temp. The run-kit adds the *restore* path, which the tool does not know about, to the same distinctness assertion | explicit `realpath` comparison across all four roles |
| 6 | **Run as `mtc-bridge`, not root.** A root-run capture could materialise root-owned `-wal`/`-shm` sidecars inside the `0750 mtc-bridge:mtc-bridge` state directory (`verify.sh:124` `[SRC]`), a real mutation of the protected state dir. Record sidecar presence and ownership **before and after** the capture and require **no change at all** | `sudo -u mtc-bridge …`; the **absence-tolerant, fail-closed per-path sidecar recorder** of §7.3 steps (0)/(2), whose before/after records must be **byte-identical**. The recorder is three-way: a probe or `stat` that does not complete is a **STOP**, never a forged `PRESENT`/`ABSENT` line, and the capture in step (1) may not run unless step (0) was adjudicated PASS |
| 7 | **`<EVROOT>/bundle.staging` writable by `mtc-bridge`** | created root, then `chown mtc-bridge:mtc-bridge`, mode `0750` |

### 7.3 Capture, verify, restore-into-temp — proposed shape

```bash
# NOT EXECUTED — proposed shape only. Requires an explicit named authority + budget lift.
SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
TOOL=/opt/mtc-bridge/releases/${SHA}/IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py
PY=/opt/mtc-bridge/venvs/${SHA}/bin/python
SRC=/var/lib/mtc-bridge/bridge.db
STAGING="${EVROOT}/bundle.staging"
RESTORE="${EVROOT}/restore"          # second temporary DB — never the source, never the bundle

# (0) sidecar + ownership RECORD BEFORE — per-path, absence-tolerant, and FAIL-CLOSED.
#     ⛔ NEVER `stat SRC SRC-wal SRC-shm` in one invocation: an ABSENT -wal/-shm is the NORMAL
#        quiesced state, `stat` returns non-zero for it, and a merged 2>&1 record would mix an
#        error string into the evidence and make the before/after comparison meaningless.
#     ⛔ AND NEVER `if sudo test -e "$p"; then printf 'PRESENT %s\n' "$(sudo stat …)"; else ABSENT`.
#        That earlier form carried TWO fatal collapses:
#          (i) `sudo test -e` is two-way. A denied sudo, an unreadable parent, a vanished mount or a
#              race all take the `else` branch and forge an `ABSENT` line — evidence of a state that
#              was never observed. It also called a DANGLING symlink absent (`! -e`, still `-L`).
#         (ii) the `stat` ran inside a command substitution, so its failure was swallowed: `printf`
#              still returns 0, and the recorder emitted `PRESENT` followed by an EMPTY identity.
#              A before/after `cmp` of two such lines compares equal, so a real state-dir mutation
#              that broke `stat` would have been reported as "no change at all".
#     Three-way per path (§2.5a): PRESENT (probe FILE + stat rc 0) / ABSENT (probe NONE) /
#     STOP (anything else). The stat identity is captured into a variable and adjudicated BEFORE a
#     line is emitted, so no PRESENT line can ever be forged from a failed stat.
sidecar_record() {                       # $1 = output file (probed NONE by the caller, §2.4(3))
  local p tok ident rc
  for p in "${SRC}" "${SRC}-wal" "${SRC}-shm" ; do
    tok=$(classify_path sudo "$p") || STOP "sidecar probe did not complete: $p"
    case "$tok" in
      NONE) printf 'ABSENT %s\n' "$p" >> "$1" ;;          # normal quiesced state — evidence, not error
      LINK) STOP "symlink in the protected state dir: $p" ;;   # never a benign token
      FILE)
        ident=$(sudo_rc stat -c '%n %s %a %U:%G %d:%i' "$p") ; rc=$(priv_rc $?) \
          || STOP "sidecar stat did not run: $p"
        [ "$rc" -eq 0 ] || STOP "sidecar stat rc $rc (failure or race): $p"
        [ -n "$ident" ] || STOP "empty stat identity is not evidence: $p"
        printf 'PRESENT %s\n' "$ident" >> "$1" ;;
      *)    STOP "unparsable sidecar token '$tok': $p" ;;
    esac
  done
}
tok=$(classify_path "" "${EVROOT}/NN_sidecars-before.out") || STOP "record-path probe did not complete"
[ "$tok" = NONE ] || STOP "before-record destination is $tok"
sidecar_record "${EVROOT}/NN_sidecars-before.out"

# (1) CAPTURE into staging — no --force, no --allow-live-source.
#     ⛔ MUTATION GATE (§2.5): step (0) must have completed and been adjudicated PASS. If the
#        recorder called STOP, the stage is already over and this line never runs — a capture must
#        never proceed on an unrecorded or partially-recorded before-state.
sudo -u mtc-bridge "${PY}" "${TOOL}" create \
     --source "${SRC}" --out-dir "${STAGING}" \
     > "${EVROOT}/NN_capture-report.json"

# (2) sidecar + ownership RECORD AFTER — same recorder, same path order
tok=$(classify_path "" "${EVROOT}/NN_sidecars-after.out") || STOP "record-path probe did not complete"
[ "$tok" = NONE ] || STOP "after-record destination is $tok"
sidecar_record "${EVROOT}/NN_sidecars-after.out"

# (2b) the two records must match EXACTLY, byte for byte.
#      A sidecar that was ABSENT and is now PRESENT, one that has disappeared, or any change to a
#      recorded stat identity (size, mode, owner, device:inode) is a STOP — state-dir mutation.
cmp "${EVROOT}/NN_sidecars-before.out" "${EVROOT}/NN_sidecars-after.out"
# rc 0 = identical (the only PASS); rc 1 = differ => STOP; rc >= 2 = cmp could not compare
# (missing/unreadable record) => STOP. ⛔ Never treat an rc >= 2 as "no difference detected".
# A recorder that called STOP leaves a truncated record and no comparison is ever made: the stage
# has already ended at that line, so two short files can never be compared into a false equality.

# (3) read the two hashes OUT of the capture report (COMMANDS.md:134-140 pattern).
#     ⛔ Each extraction's rc is adjudicated and each value shape-checked BEFORE it is used: an
#        unreadable, truncated or key-missing report makes the substitution empty, and an empty
#        --expect-*-sha256 handed to `verify` in step (4) is an unfounded expectation, not a check.
BUNDLE_DB_SHA256=$("${PY}" -c 'import json,sys;print(json.load(open(sys.argv[1],encoding="utf-8"))["bundle_db_sha256"])'   "${EVROOT}/NN_capture-report.json") \
  || STOP "bundle_db_sha256 could not be read from the capture report"
INVARIANTS_SHA256=$("${PY}" -c 'import json,sys;print(json.load(open(sys.argv[1],encoding="utf-8"))["invariants_sha256"])' "${EVROOT}/NN_capture-report.json") \
  || STOP "invariants_sha256 could not be read from the capture report"
case "${BUNDLE_DB_SHA256}"  in *[!0-9a-f]*|'') STOP "bundle_db_sha256 is not 64 lowercase hex" ;; esac
case "${INVARIANTS_SHA256}" in *[!0-9a-f]*|'') STOP "invariants_sha256 is not 64 lowercase hex" ;; esac
[ ${#BUNDLE_DB_SHA256}  -eq 64 ] || STOP "bundle_db_sha256 length ${#BUNDLE_DB_SHA256}"
[ ${#INVARIANTS_SHA256} -eq 64 ] || STOP "invariants_sha256 length ${#INVARIANTS_SHA256}"

# (4) VERIFY the staged bundle against those preregistered hashes
sudo -u mtc-bridge "${PY}" "${TOOL}" verify \
     --bundle-dir "${STAGING}" \
     --expect-bundle-sha256     "${BUNDLE_DB_SHA256}" \
     --expect-invariants-sha256 "${INVARIANTS_SHA256}" \
     > "${EVROOT}/NN_verify-report.json"

# (5) EXTERNAL sha256 of the MANIFEST FILE — a separate output, not a value from inside the JSON
sha256sum "${STAGING}/bundle_manifest.json"      # -> <MANIFEST_FILE_SHA256>

# (6) RESTORE INTO A SECOND TEMPORARY DB — via the wrapper this design specifies (does not exist yet)
#     Wrapper contract (pseudocode, to be authored OUTSIDE the 0555 release tree):
#       import sys; sys.path.insert(0, "<release>/IBKR_PAPER_BRIDGE/tools")
#       import wal_state_bundle as w
#       src = sqlite3.connect("file:<STAGING>/bridge.db?mode=ro", uri=True)
#       dst = sqlite3.connect("<RESTORE>/bridge.db")          # fresh path, must not pre-exist
#       src.backup(dst)                                        # online backup API, NOT a file copy
#       assert quick_check(dst) == "ok" and foreign_key_check(dst) == 0
#       inv  = w.collect_invariants(dst)                       # PUBLIC entry point, :417
#       hsh  = w.invariants_hash(inv)                          # PUBLIC entry point, :561
#       assert hsh == INVARIANTS_SHA256
#       emit {restored_invariants_sha256, quick_check, foreign_key_violations, stat identities}

# (7) inode / file-identity distinctness — all three must differ.
#     rc must be 0 AND exactly three lines must come back. `stat` on a multi-path argv prints only
#     the paths it could reach and exits non-zero; a two-line result read as "all distinct" would
#     hide the case where one of the three is missing or unreadable => STOP.
stat -c '%n %d:%i' "${SRC}" "${STAGING}/bridge.db" "${RESTORE}/bridge.db" || STOP "identity stat did not run"
```

### 7.4 Anchors for every element above

| Element | Anchor |
|---|---|
| bundle file names `bridge.db` / `bundle_manifest.json` / `.bundle_manifest.json.tmp` | `[SRC]` `:80-81`, `:695` |
| online backup, not a trio copy | `[SRC]` `:14-16` |
| sidecar rejection | `[SRC]` `FORBIDDEN_SIDECARS` `:87` |
| `PRAGMA integrity_check` / `foreign_key_check` on both ends | `[SRC]` `:405-411` |
| `collect_invariants` is public and takes a connection | `[SRC]` `:417` |
| `invariants_hash` is public | `[SRC]` `:561` |
| `--force` gate | `[SRC]` `:740-741`, flag `:1230` |
| alias rejection across source/output roles | `[SRC]` `:678-715` |
| `verify` re-derives and fails closed on drift / hash mismatch | `[SRC]` `:1180-1205` |
| exit codes `0` / `2` / `3` | `[SRC]` `:54-58` |
| verdict `VALID` / `INVALID` | `[SRC]` `:1199-1205` |
| report sanitisation guard applied before printing | `[SRC]` `:188`, `:1266-1270` |
| capture-report → expected-hash extraction pattern | `[REF-INV]` `…/deploy/linux/COMMANDS.md:124-140` |
| existing test coverage (existence only, not execution) | `[SRC]` `tests/test_wal_state_bundle.py:856` `test_bundle_never_contains_a_wal_shm_trio`; `:882` `test_invariants_preserve_risk_and_history` |

### 7.5 PASS predicates

1. `create` rc `0`; capture report present and parseable.
2. Source sidecar/ownership records **byte-identical** before and after — `PRESENT`/`ABSENT` lines and
   stat identities alike (prerequisite 6, recorder at §7.3(0)/(2)), compared with a `cmp` whose rc is
   adjudicated three-way (`0` equal / `1` differ ⇒ STOP / `≥ 2` could-not-compare ⇒ STOP).
   `-wal`/`-shm` recorded `ABSENT` in **both** records is a normal quiesced result and is **not** a
   failure and **not** a SKIP; a sidecar newly `PRESENT`, newly gone, or with a changed identity is a
   **STOP**. **Every `PRESENT` line carries a non-empty stat identity that was adjudicated rc `0`
   before the line was written** — a `PRESENT` line with an empty identity is impossible by
   construction, because a failed or raced `stat` calls `STOP` instead of emitting a line.
3. `verify` rc `0` and `verdict` = `VALID`, with `failures` empty.
4. `<MANIFEST_FILE_SHA256>` recorded as a **separate** output — the external `sha256sum` of
   `bundle_manifest.json`, distinct from `bundle_db_sha256` and `invariants_sha256`, which are values
   *inside* the JSON. This is the value `rollback.sh` will later require (`:57-62` `[REF-INV]`), so
   recording only the embedded hashes would leave `RK-C4` unable to run.
5. `<BUNDLE_DB_SHA256>` and `<INVARIANTS_SHA256>` recorded.
6. Restore wrapper: `quick_check` = `ok`; `foreign_key_check` violations = `0`; restored
   `invariants_hash` **equals** `<INVARIANTS_SHA256>`; protected invariants (§5.4 table) equal.
7. **Distinct file identity:** `stat -c '%d:%i'` differs across source, bundle DB, and restored DB —
   all three. Equality of any pair ⇒ **STOP**: it would mean the "restore" aliased the source or the
   bundle.
8. No sidecar present in the bundle or restore directories.

### 7.6 Atomic / no-clobber publication semantics

- Everything is produced into `<EVROOT>/bundle.staging` and `<EVROOT>/restore`, **never** directly
  into a published name.
- **Publication happens only after step (4) returns `VALID` and step (6) matches.** Then, and only
  then, an atomic same-filesystem rename: `mv -T "${EVROOT}/bundle.staging" "${EVROOT}/bundle"`.
  `mv -T` is required so an existing directory is not silently moved *into*.
- **⛔ The destination assertion is `NONE`, not `! -e`, and it is made immediately before the `mv`.**

  ```bash
  # NOT EXECUTED — proposed shape only. The last thing before the rename, with nothing in between.
  tok=$(classify_path "" "${EVROOT}/bundle") || STOP "publication probe did not complete"
  [ "$tok" = NONE ] || STOP "publication destination is $tok"   # FILE or LINK => STOP
  mv -T "${EVROOT}/bundle.staging" "${EVROOT}/bundle" || STOP   # rc != 0 => STOP, never retried
  ```

  A `test -e`-only precondition is **not** a no-clobber precondition: **a dangling symlink at
  `${EVROOT}/bundle` satisfies `! -e` and `mv -T` publishes straight through it onto the link's
  target**, outside `<EVROOT>` and outside the evidence tree entirely. The required token is `NONE`;
  **`FILE` and `LINK` (live or dangling) are each a STOP**, and a probe that does not complete is a
  **STOP** — publication never proceeds on an unverified destination. The `mv` itself is adjudicated:
  a non-zero rc is a **STOP**, never retried, and never followed by a copy-based fallback.
- **Publication is a mutation and inherits the §2.5 mutation gate.** It may not run while any earlier
  predicate in the stage is failed, unadjudicated or unrecorded.
- **On any failure, publication never happens.** Staging stays exactly where it is under its staging
  name. It is **not** renamed to the accepted name, not partially copied to the accepted name, and
  not deleted. The tool's own `discard()` (`:748-752` `[SRC]`) removes half-written outputs *within
  its own out-dir* on a rejected capture — that is the tool's fail-closed behaviour and the run-kit
  does not fight it; the run-kit's obligation is to preserve the surrounding `.cmd`/`.out`/`.err`/`.rc`
  record and any diagnostic temp material **outside** the tool's out-dir.
- **Failure preservation, precisely.** Command logs, exit statuses and diagnostic temp material are
  preserved safely under `<EVROOT>` and retrieved for analysis. **A partial bundle or a partial
  restore is never published, never renamed to an accepted name, and never cited as output.**

### 7.7 Dispositions and remaining gaps

- `create` rc `2` (drift / corruption / bad schema) ⇒ **STOP**; rc `3` (invalid input / bad usage) ⇒
  **STOP** and fix the invocation locally, do not improvise on the host.
- `verify` `verdict=INVALID` for any reason in `failures` ⇒ **STOP**.
- **Any** difference between the before and after sidecar records ⇒ **STOP** (state-dir mutation): a
  newly `PRESENT` `-wal`/`-shm`, a sidecar that has vanished, or a changed size/mode/owner/inode. The
  comparison is exact-match on the whole record, so no case has to be enumerated in advance. An
  `ABSENT` line is evidence, never an error and never a SKIP; a recorder that aborts on an absent
  sidecar is defective and must not be used.
- **⛔ Equally, a recorder that CONTINUES past a failed probe or a failed `stat` is defective and must
  not be used.** Absence-tolerance means tolerating the *answer* "the sidecar is not there"; it never
  means tolerating "the question could not be asked". `sudo` denied, path unreadable, `stat` raced,
  probe unparsable ⇒ **STOP** with no line emitted — never an `ABSENT` line, and never a `PRESENT`
  line with an empty identity. The latter is the more dangerous of the two: two such lines `cmp`
  equal, so a swallowed `stat` failure would be reported as *proof that nothing changed*.
- `cmp` rc ≥ 2 (a record missing or unreadable) ⇒ **STOP** — never adjudicated as "no difference".
- **D026.** The two existing `wal_state_bundle` tests are *existing coverage*, not new closure
  evidence for a newly named defect, and their existence was proven by `git grep`, not by execution.
- **⛔ `D-GAP-C3-1`.** The restore wrapper **does not exist**. Its contract is specified above; a
  future implementer must author it, outside the `0555` release tree, and it is subject to normal
  review. This design does not create it and does not claim it works.
- **⛔ `D-GAP-C3-2`.** The exact `PRAGMA quick_check` invocation form against the restored copy is
  specified semantically (`quick_check` must return `ok`); the wrapper author must confirm the
  return-shape handling matches the tool's own `_integrity_check` convention (`:405-411` `[SRC]`).

---

## 8. `RK-C4` — rollback: stop + mask **only** (`mutating-host`)

### 8.1 Hard boundaries, stated first

- **⛔ Release rebind remains impossible.** A meaningful rebind needs a second already-installed
  immutable release; only the candidate `2ce41e34…321b` is installed — the old `ebada020…` install and
  its venv are **already absent** (`[HOST-OBS]`, transition inventory `:38-43`). **Do not invent a
  target release. `--to-release-sha` and `--to-manifest-sha256` must not appear in any invocation.**
  The script's own guard rejects one without the other (`rollback.sh:63-68` `[REF-INV]`), and with
  neither supplied the stop+mask path runs cleanly.
- **Recovery / unmask / start is `RK-REC`** — a separate future authority unit, explicitly not part of
  this stage. The script says so itself: it *"never … start, enable, unmask or arm any service — the
  post-rollback recovery start is a separate authorization (KVM2-P4-08A) and a separate bounded
  execution (KVM2-P4-08B)"* (`rollback.sh:16-19` `[REF-INV]`, restated at `:185`).

### 8.2 Prerequisites

| # | Prerequisite | Anchor / check |
|---|---|---|
| 1 | **Accepted `RK-C3` state-manifest FILE** (`<STAGING→published>/bundle_manifest.json`) | `rollback.sh:57,60` `[REF-INV]` requires the file and its existence |
| 2 | **Its externally recorded SHA-256** `<MANIFEST_FILE_SHA256>` | `rollback.sh:58-62` `[REF-INV]` — the script re-hashes the file and dies on mismatch. This is why §7.5(4) records it as a separate output |
| 3 | **⛔ NO-CLOBBER PRECONDITION on `/etc/mtc-bridge/rollback_manifest.json`** | see §8.3 — **this is the most important addition in this stage** |
| 4 | Steady unit absent | `rollback.sh:72-77` `[REF-INV]` dies if a steady unit is installed |
| 5 | Root | `rollback.sh:54` `[REF-INV]` |
| 6 | Invoked from the **installed release path**, so `lib/common.sh` resolves | `rollback.sh:34-36` `[REF-INV]` sources `${SCRIPT_DIR}/lib/common.sh` |
| 7 | **Starting unit state preregistered in `RK-PRE` and captured immediately before the rehearsal.** In the coherent Chain B, `RK-C4` is reached after `RK-C1` and `RK-C3`, so the expected starting state is **inactive + unmasked** — *not* active | §8.4 step 1; `[SRC]` `verify.sh:207-211` (mask symlink), `:218-221` (`is-enabled`) |

### 8.3 ⛔ The no-clobber precondition — and why the run-kit must supply it

**Finding (candidate-verified).** `rollback.sh` writes `/etc/mtc-bridge/rollback_manifest.json` with a
plain `cat > "${MTC_ROLLBACK_MANIFEST}" <<EOF` at `:160` `[REF-INV]`. The only guard on that path is
`assert_not_symlink` at `:71`. **There is no existence check and no no-clobber guard: a second run
silently overwrites the first run's rollback manifest**, destroying the record of the earlier
rollback.

**Required run-kit precondition (immediately before the invocation, with no command in between):**

```bash
# NOT EXECUTED — proposed shape only.
# ⛔ NOT `sudo test -e … && echo EXISTS || echo ABSENT` and NOT a separate `test -L` beside it.
#    That pair collapsed the predicate twice over, on the single most consequential precondition in
#    the stage — the one standing between an authorised rollback and the destruction of a prior
#    rollback record:
#      (i) a denied sudo, an unreadable /etc/mtc-bridge, or a race printed the PASS token ABSENT
#          with rc 0, licensing the mutation on a precondition that was never actually evaluated;
#     (ii) `-e` is FALSE for a DANGLING symlink, so the pair reported "ABSENT" and "SYMLINK" in two
#          separate outputs that a reader may adjudicate independently — while rollback.sh:160's
#          `cat > "${MTC_ROLLBACK_MANIFEST}"` would follow that link and write through it to an
#          arbitrary target outside /etc/mtc-bridge.
#    One probe, one token, adjudicated once (§2.5a H2):
tok=$(classify_path sudo /etc/mtc-bridge/rollback_manifest.json) \
  || STOP "no-clobber precondition could not be evaluated"   # probe failure => STOP, never ABSENT
[ "$tok" = NONE ] || STOP "rollback manifest destination is $tok"
#   NONE => the ONLY admissible answer: neither a filesystem object nor a symlink
#   FILE => a prior rollback manifest exists                       => STOP
#   LINK => a symlink, LIVE OR DANGLING, occupies the path         => STOP
#           (rollback.sh:71 assert_not_symlink would die on a live one; a dangling one is exactly
#            what an `-e`-only check misses, so the run-kit catches BOTH here, first)
```

**Disposition if the token is anything but `NONE`, or if the probe cannot complete: STOP.** Preserve
whatever is there, report it, and obtain a separate decision. A separately named future output path
may be substituted **only** by explicit authority and must itself be no-clobber, asserted the same
way. **Under no circumstances does the run-kit overwrite, move, follow a link to, or
back-up-and-replace the existing manifest as part of this stage.**

**⛔ This precondition gates a mutation, so §2.5 applies at its strongest:** the real `rollback.sh`
invocation (§8.5) may not run while this predicate is failed, unadjudicated or unrecorded. There is
no "record the rc and proceed", and a probe failure is never resolved by assuming absence.

### 8.4 Mandatory dry-run rehearsal first — against the correct starting state

`rollback.sh` supports `--dry-run` (`:48` `[REF-INV]`), and every mutation is routed through `run()`
(`common.sh:42-48` `[REF-INV]`), with the post-stop assertion block (`:91-101`) and the manifest write
(`:158-181`) both gated on `MTC_DRY_RUN != 1`. A dry run therefore **prints** `[dry-run] systemctl
stop …` / `[dry-run] systemctl mask …` and **mutates nothing**.

**⛔ The starting state is inactive + unmasked — not active.** In the only coherent full chain
(Chain B, §2.2) `RK-C4` is reached **after** `RK-C1` has stopped the service and after `RK-C3`, so the
unit is already **inactive and unmasked** when the rehearsal runs. A rehearsal predicate of *"service
still active afterwards"* is therefore unsatisfiable by construction: it would fail a correct dry run,
and it would invite an implementer to "fix" the failure by starting the service — precisely the
unauthorised `RK-REC` action this design excludes (§8.1). The rehearsal predicate is
**state-preservation against the captured starting state**, not activity.

**Required sequence:**

1. **Preregister and capture the actual starting unit state**, immediately before the rehearsal:
   `systemctl is-active` (**expected `inactive`** in Chain B), `systemctl is-enabled` (**expected
   `static`** — unmasked; §4.3 rejection table applies unchanged), the mask path
   `/etc/systemd/system/mtc-bridge-first-start.service` classifying as **`NONE`** (§2.5a H2 — not an
   `-e`-only "absent", which a dangling link would satisfy), `pgrep -f '[b]ridge\.app'` **rc 1** with
   no output, and no listener on 8790 under `pipefail`. The expected triple is frozen in `RK-PRE`;
   the observed triple is recorded as the rehearsal baseline. **Observed ≠ frozen ⇒ STOP** — the
   chain is not where the design says it is, and the rehearsal would be rehearsing something else.
   **Any of these predicates that cannot be evaluated ⇒ STOP**, never a benign token: every one of
   them PASSes on empty output, so a denied or crashed tool would otherwise read as a clean baseline.
2. **Run the rehearsal** and require: rc `0`; both `[dry-run]` lines present; the state-manifest hash
   check passed (which is what proves prerequisites 1–2 are correct).
3. **Re-assert the starting state afterwards, unchanged**: `is-active` = `inactive`, `is-enabled` =
   `static`, mask path still classifying **`NONE`**, still no writer and no listener — each read
   through the same §2.5a helper as step 1, so a probe failure cannot masquerade as "unchanged". The
   dry run moved nothing, so the after-record must equal the before-record exactly.
4. **Re-assert the `/etc/mtc-bridge/rollback_manifest.json` token is still `NONE`** (§8.3), using
   `classify_path`, not `test -e`. A dry run **creates no rollback manifest** (`:158-181` is gated on
   `MTC_DRY_RUN != 1`); a `FILE` or `LINK` token here means the run was not dry, and is a **STOP**. A
   probe that cannot complete is also a **STOP** — it is not evidence that the dry run stayed dry.
5. **Re-assert the `RK-C3` evidence intact and unconsumed**: the published bundle directory and
   `bundle_manifest.json` still present and unmodified, and the file re-hashed to the same
   `<MANIFEST_FILE_SHA256>`. The rehearsal *reads* that evidence and must leave it byte-identical.

Only then may the real invocation be attempted. A dry-run failure, an unexpected starting state, any
state change across the rehearsal, an appearing rollback manifest, or any change to the `RK-C3`
evidence ⇒ **STOP**; do not proceed to the real run to "see what happens".

**The real invocation is what changes state:** from **inactive + unmasked** to **inactive + masked**
(§8.5 post-assertions 1–3). Its `systemctl stop` is a no-op on an already-inactive unit — routed
through `run()` and followed by the still-active check at `:88-90` `[REF-INV]`, which holds — and the
**mask** is the real mutation this stage performs.

### 8.5 The authorised invocation and post-assertions

```bash
# NOT EXECUTED — proposed shape only. Requires KVM2-P4-08-class authority + budget lift.
SHA=2ce41e34bceb599d80af24c5c33d835820ec321b
RB=/opt/mtc-bridge/releases/${SHA}/IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh

# starting state in Chain B: INACTIVE + UNMASKED — captured and compared per §8.4 step 1
systemctl is-active  mtc-bridge-first-start.service     # expect: inactive; rc adjudicated, not
systemctl is-enabled mtc-bridge-first-start.service     # expect: static (i.e. unmasked)  inferred
# unmasked proof — §2.5a H2 only: one exception-aware probe, rc adjudicated first, token second.
# The PASS answer here is the "nothing is there" answer, which is exactly the answer a two-way shell
# predicate manufactures out of a permission error, a vanished directory or a race — and which an
# -e-only form also returns for a DANGLING link at the mask path. Neither form is admissible.
tok=$(classify_path "" /etc/systemd/system/mtc-bridge-first-start.service) \
  || STOP "mask-path probe did not complete"     # probe failure => STOP, never NONE
[ "$tok" = NONE ] || STOP "mask path is $tok"
# expect token EXACTLY: NONE (unmasked).  LINK => masked or dangling => STOP.  FILE => STOP.

# rehearsal (non-mutating) — followed by §8.4 steps 3..5: state unchanged, no rollback manifest,
# RK-C3 evidence byte-identical
sudo bash "${RB}" --state-manifest-file "<M>" --state-manifest-sha256 "<MANIFEST_FILE_SHA256>" --dry-run

# ⛔ MUTATION GATE (§2.5, §8.3). The §8.3 no-clobber token must be NONE, the §8.4 steps 1..5 must all
#    have been recorded and adjudicated PASS, and the starting-state triple must equal the RK-PRE
#    freeze. Any failed, unadjudicated or unrecorded precondition forbids the line below outright.
# THE SINGLE AUTHORISED MUTATION — no --to-* flags, ever.
# This is the step that moves the unit from inactive+unmasked to inactive+MASKED.
sudo bash "${RB}" --state-manifest-file "<M>" --state-manifest-sha256 "<MANIFEST_FILE_SHA256>"
```

**Post-assertions (all read-only, all required):**

| # | Assertion | Expected | Anchor |
|---|---|---|---|
| 1 | mask symlink present | `classify_path` returns **`LINK`** — the one place in this design where `LINK` is the expected token — **and** `readlink -f` resolves to exactly `/dev/null` with rc `0`. `NONE` or `FILE` ⇒ **STOP** (the mask was not created). A `LINK` whose target does not resolve to `/dev/null`, or a `readlink` that fails, ⇒ **STOP**: a dangling or misdirected link at the mask path is not a mask | `[SRC]` `verify.sh:207-211`; `[REF-INV]` `rollback.sh:86` |
| 2 | `systemctl is-active` | `inactive` — already inactive on entry in Chain B, so this is state **preserved**, not a transition the stage caused | `[REF-INV]` `rollback.sh:88-90` dies if still active |
| 3 | `systemctl is-enabled` | `masked` — the one unit-state change this stage makes (`static` → `masked`) | `[SRC]` `verify.sh:218-221`; §4.3 rejection table |
| 4 | zero `bridge.app` writers | `pgrep -f '[b]ridge\.app'` exits **`1`** with no output. rc `0` ⇒ **STOP** (writer survives); **rc `2`/`3` ⇒ STOP**, never read as "zero writers" — they print nothing too | `[REF-INV]` `rollback.sh:94-98` |
| 5 | zero listeners on 8790 | `ss -H -ltn` under `set -o pipefail`, rc `0` and every `PIPESTATUS` member `0`, with no `:8790` line. A failed `ss` produces the identical empty result ⇒ **STOP**, not a PASS | `[REF-INV]` `rollback.sh:93` (`assert_control_port_closed`) |
| 6 | state directory preserved | `/var/lib/mtc-bridge` classifies **`FILE`** (never `LINK`), `0750 mtc-bridge:mtc-bridge`, `bridge.db` classifies `FILE` with unchanged mode/owner — each `stat` identity adjudicated rc `0` before it is recorded (§2.5a) | `[REF-INV]` `rollback.sh:103-110` (*"assertion-only: risk history is evidence, never cleanup"*); `[SRC]` `verify.sh:124` |
| 7 | rollback manifest created correctly | `0640 root:root`; `schema_version` `1.0.0`; **`"rollback_release_sha": ""`** and **`"rollback_release_manifest_sha256": ""`** (empty, because no `--to-*` was passed); `state_bundle_manifest_sha256` = `<MANIFEST_FILE_SHA256>`; `first_start_unit_state` `masked`; `service_active` false; `service_enabled` false; `service_started_by_this_script` false; `state_dir_preserved` true; `secrets_touched` false; `firewall_modified` false | `[REF-INV]` `rollback.sh:160-181` |
| 8 | **post-rollback invariant equality** | see §8.6 | — |

### 8.6 Required post-rollback state proof — equality, not path existence

**Path existence is not sufficient.** The stage must re-run the `RK-C3` capture+verify (into a
**freshly allocated** no-clobber root, never the `RK-C3` root) against the now-quiesced, masked
service, and require:

- `verify` `verdict` = `VALID`;
- the recomputed `invariants_sha256` **equals** the preregistered pre-rollback `<INVARIANTS_SHA256>`;
- every field in the §5.4 protected-invariant table equal;
- `app_state` never `ARMED`.

This is legitimate because rollback stops and masks but performs no database operation
(`rollback.sh:103-110` is assertion-only `[REF-INV]`), so any drift here would be real.

### 8.7 Dispositions, secrets, gaps

- `rollback.sh` `die` on the state-manifest hash (`:61-62`) ⇒ **STOP**: either the wrong manifest file
  or the wrong recorded hash. Do **not** recompute the hash from the file and re-run — that would
  defeat the check's entire purpose.
- Still-active after stop (`:88-90`) ⇒ **STOP**, *"escalate, do not retry blindly"* — the script's own
  words, and the run-kit must honour them.
- Writer-absence check failure (`:99-100`) ⇒ **STOP**, *"preserve evidence and stop"*.
- **Rehearsal dispositions (§8.4):** starting state ≠ the `RK-PRE`-frozen state ⇒ **STOP**; any unit
  state change across the dry run ⇒ **STOP**; a rollback manifest present after the dry run ⇒
  **STOP**; any change to the `RK-C3` bundle/manifest evidence ⇒ **STOP**. **Never** start or unmask
  the service to satisfy a rehearsal predicate — that is `RK-REC` and it is out of scope (§8.1).
- **No-clobber precondition dispositions (§8.3):** token `FILE` ⇒ **STOP** (a prior rollback manifest
  exists); token `LINK` ⇒ **STOP** (live *or* dangling — `rollback.sh:160`'s `cat >` would write
  through it); **probe could not complete ⇒ STOP**, never adjudicated as absent. The mutation of
  §8.5 does not run in any of these cases (§2.5 mutation gate).
- Any post-assertion mismatch, or any invariant drift ⇒ **STOP**, preserve everything.
- **Secrets.** The script never touches a secret, the firewall, or the exchange (`:20-22`
  `[REF-INV]`). The rollback manifest holds hashes and booleans only; it is captured with a
  field-targeted read, not a bulk `cat` (§2.6).
- **Unresolved.** None specific to C4 beyond its dependence on `RK-C3` and `D-GAP-C3-1` (the restore
  wrapper). The no-clobber gap in the script itself is a **finding**, recorded here and handled by a
  run-kit precondition; **this design proposes no edit to `rollback.sh`.**

---

## 9. `RK-C5` — runtime broker egress: **BLOCKED, and stays blocked**

- **Predicate (unchanged).** Observed runtime egress reaches only
  `api.hyperliquid-testnet.xyz` (and optionally `api.telegram.org`); **no** `api.hyperliquid.xyz`
  (mainnet); loopback-only `127.0.0.1:8790`.
- **⛔ Why it cannot be captured from the current runtime — at any authority level.** The deployed
  start mode **constructs no broker at all.** `[SRC]`
  `2ce41e34…321b:IBKR_PAPER_BRIDGE/bridge/app.py:149`
  (`if start_runtime and not credential_free_disarmed:`) gates broker construction off entirely, so
  `_build_broker`'s credential resolution (`:244`) and `network="testnet"` selection (`:246`) never
  run; `:138-148` pins `network="disabled"`, `exchange_conn="disabled"`, `exchange_enabled=False`,
  `credential_lookup="disabled"`, `arm_enabled=False`; `:136` leaves `bridge_engine = None`.
  **A process that constructs no broker cannot generate broker egress.** This is a structural
  blocker, not a permission blocker: no amount of authority makes the current runtime emit the
  traffic.
- **What a future capture would require** (all absent, all separately authorised, none requested
  here): a **different, separately authorised start mode**; **credential authority**;
  **TESTNET-network / broker authority**. It **does not require ARM** — the Lead's standing
  correction stands — and any such capture **must remain DISARMED and must place no order**.
  ARM remains forbidden.
- **⛔ No executable credential or network procedure is provided now**, deliberately. Supplying one
  would be an operational credential/network procedure for an unauthorised action. This section
  records the blocker and its shape; it does not lower the barrier.
- **`SECURITY_BASELINE.md` is `[GOV]`, not candidate payload** (§1.1). It may be cited as governance
  evidence describing candidate analysis; it may never be cited as candidate source for this or any
  other predicate. The static egress inventory it carries is *a reading of what the code could
  reach* — it is not a runtime capture and does not describe the deployed start mode.
- **Mutation class.** `blocked`. **Authority/budget:** not authorisable now.
- **Failure disposition (if it ever runs).** Any mainnet attempt ⇒ **hard BLOCK**.

---

## 10. Design-gap register — open items, never converted to host facts

| ID | Gap | Where | Status / closure route (none executed) |
|---|---|---|---|
| `D-GAP-B1a-1` | **The observed installed-host lock hash and `install_manifest.json` → `requirements_lock_sha256` are NOT IN EVIDENCE.** Identity 4 of §1.2 | `RK-B1a` | Open. One bounded read-only host read closes it. Blocked with all host action. **`a1881296…` is its expected, not confirmed, value.** |
| `D-GAP-B2-1` | `is-enabled = static` has never been **observed** for the running unit; it is `[EXPECT]` from `[SRC]` no-`[Install]` + `[SYSTEMD]` semantics | `RK-B2` | Closes on first observation. Recorded as an expectation, not a re-check. |
| `D-GAP-B4-1` | Exact rendered strings systemd returns for a few hardening properties (`TimeoutStopUSec` units, empty capability sets) are `[SYSTEMD]` representation details never observed on this host | `RK-B4` | Compare semantics, record strings verbatim, baseline on first run. |
| `D-GAP-B5-1` | The complete set of `state_version` increment sites was not enumerated; only `app.py:160` was located, and it sits in the branch that does not run in this mode | `RK-B5` | `state_version` is recorded, **not** STOP-bearing. Closes by an offline read of the API surface. |
| `D-GAP-C1-1` | **Exact clean-stop `ExecMainStatus` / `Result` tuple is not establishable from candidate source** (the exit contract lives in the pinned uvicorn dependency), and no immutable evidence records a graceful stop of this unit | `RK-C1` | **BLOCKING.** No predicate invented, and **`exit-code` is explicitly NOT accepted** — a non-zero exit is what a *failed* shutdown looks like, so admitting it would launder a failure into a PASS. While the gap is open `RK-C1` **may not be executed and cannot obtain PASS**. The §5.3 legs prove *no escalation*, not *successful shutdown*, and may not substitute. Closes only by offline determination of the pinned uvicorn version's SIGTERM exit contract plus the documented systemd mapping, frozen in `RK-PRE` — never by running a stop and back-filling its output. |
| `D-GAP-C1-2` | The exact set of tables a graceful shutdown may legitimately write is established as *empty* for this mode from `app.py:89-100,136,149`, but only for the shutdown path — non-protected count fields are treated as monotonic rather than strictly equal out of caution | `RK-C1` | Protected subset requires equality; the rest is investigate-read-only. |
| `D-GAP-C1-3` | **The `RK-C1` pre-stop baseline requires an exact safe active-writer capture method, and none is established.** Same root cause as `D-GAP-C2-1`, but intrinsic to `RK-C1` rather than chain-dependent: the baseline must be taken while the service is still ACTIVE, and Chain B — the only chain containing `RK-C1` — orders the `RK-C3` capture *after* the stop, so it supplies no pre-stop baseline at all. Comparing the post-stop capture against itself is **vacuous, not clean** | `RK-C1` | **BLOCKING; no command supplied.** Only two admissible routes (§5.4): **(a)** close the gap offline and freeze an exact safe active-writer capture command in `RK-PRE`, or **(d)** an independently accepted equivalent proving the same pre/post persistence property (a located prior accepted capture with a recorded `invariants_sha256`, window *shown* writer-free — none is located and none is asserted). **(b)** warning-class `--allow-live-source` and **(c)** no baseline are **rejected as execution routes**: a weakened or absent baseline does not buy a weakened PASS, and a post-stop baseline is invalid in every form. The protected pre/post equality requirement stays mandatory. |
| `D-GAP-C2-1` | **No exact safe command established for capturing persisted state while the service is ACTIVE** (Branch A pre-reboot). Two independent reasons: the tool's own "never for a cutover capture" rule for `--allow-live-source`, and read-only WAL access requiring `-shm` write access | `RK-C2` Scenario A (the bounded, terminal `RK-C2`-only branch, §2.2) | **Named gap; no command supplied.** Three resolution routes in §6.4. Chain B avoids it **for the reboot capture only**, but Chain B cannot start until the `RK-C1` gaps close, so that route trades one blocker for another. It does **not** avoid `D-GAP-C1-3`. |
| `D-GAP-C3-1` | **The restore-into-temp wrapper does not exist.** The candidate CLI has only `create` and `verify` | `RK-C3` | Contract specified in §7.3(6). A future implementer must author it outside the `0555` release tree. This design does not create it and does not claim it works. |
| `D-GAP-C3-2` | The `PRAGMA quick_check` return-shape handling in the future wrapper is specified semantically, not syntactically | `RK-C3` | Wrapper author confirms against `_integrity_check` (`:405-411`). |
| `D-GAP-C4-1` | `rollback.sh:160` writes `/etc/mtc-bridge/rollback_manifest.json` with an unconditional `cat >` and has **no** built-in no-clobber guard | `RK-C4` | Handled by a **run-kit precondition** (§8.3), not by editing the script. Recorded as a finding for the Lead. |
| `D-GAP-C5-1` | Runtime broker egress is structurally uncapturable in the deployed mode | `RK-C5` | Stays blocked; requires a different start mode plus credential and TESTNET/broker authority. |

**Binding rule:** none of the above may be silently upgraded. A gap becomes a fact only when a
captured command and its real output are recorded, labelled `observed-on-host`.

**Blocking vs non-blocking.** Two of these gaps are **blocking** — `D-GAP-C1-1` and `D-GAP-C1-3` —
meaning the stage they name **must not be executed and cannot obtain PASS** while they are open, and
`RK-C3`, `RK-C4` and `RK-C2/B` inherit that block through Chain B (§2.2). The rest are carried openly
and bound how a result is *adjudicated or labelled*, not whether the stage may run. **A blocking gap
is never discharged by running the stage and reporting whatever the run produced.**

---

## 11. Authority matrix

| Stage | Mutation class | Authority required (beyond the current envelope) | Budget | Status now |
|---|---|---|---|---|
| `RK-PRE` | `local-static` | none | none | **authorable now** |
| `RK-B0`–`RK-B7` | `read-only-host` (root reads in B1a/B3/B4) | host access lift | **budget lift required** (50 h balance NOT REPRODUCIBLE) | **BLOCKED** |
| `RK-B6` external probe | outbound TCP from operator machine | same host-access lift; A-8 precedent | same | **BLOCKED** |
| `RK-C1` | `mutating-host` | explicit named **stop** lift — stop only, recovery start **excluded** | required | **BLOCKED TWICE.** Budget/authority **and** design: `D-GAP-C1-1` and `D-GAP-C1-3` are blocking (§5.2, §5.4). Granting every lift does **not** make it runnable, and no weakened, baseline-free or post-stop-baseline variant may be run or reported as PASS |
| `RK-C2/A` | `mutating-host` | explicit named **reboot** lift | required | **BLOCKED** (budget/authority) + carries `D-GAP-C2-1`. **Terminal branch** — ends inactive + unmasked; continuing into `RK-C1` from it requires `RK-REC` **and** a fresh accepted Stage B, neither of which is authorised here (§2.2) |
| `RK-C2/B` | `mutating-host` | explicit named **reboot** lift **+** the **mask** lift (via `RK-C4`) | required | **BLOCKED**; inherits the `RK-C1` design block through Chain B |
| `RK-C3` | `mutating-host` (reads the live DB file under SQLite locking) | explicit named lift | required | **BLOCKED**; inherits the `RK-C1` design block |
| `RK-C4` | `mutating-host` | KVM2-P4-08-class **rollback** lift | required | **BLOCKED**; inherits the `RK-C1` design block |
| `RK-C5` | `blocked` | different start mode **+** credential **+** TESTNET/broker authority | required | **NOT AUTHORISABLE NOW** |
| `RK-REC` | `mutating-host` | KVM2-P4-08A authorisation + a single P4-08B attempt | required | **out of scope of this design** |
| ARM / orders / mainnet / master merge / WP-V / KVM2 / credentials | — | — | — | **FORBIDDEN** |

**⛔ Authority is necessary, not sufficient.** Two rows above carry a *design* block that no lift can
clear: `RK-C1` (and, by dependency, `RK-C3`, `RK-C4`, `RK-C2/B`) stays unexecutable until
`D-GAP-C1-1` and `D-GAP-C1-3` are closed, accepted and frozen in `RK-PRE`. **The only Group C work
reachable by granting lifts alone is the bounded terminal branch `RK-PRE → RK-B0..B7 → RK-C2/A`**,
and even that carries `D-GAP-C2-1` for its pre-reboot capture.

**Standing constraints that bound all of the above** (matrix §1): the broad programme authorisation
(`OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md`) is conditional on every objective prerequisite
passing, and two narrower later constraints — `CODEX_TAKEOVER_HANDOFF_2026-08-02.md:261-263` and the
`NEXT_SESSION_HANDOFF_2026-08-08.md` hard stop — were **not lifted by name** and continue to bind
merge-to-master, WP-V/deployment, KVM2, credentials, broker/exchange, ARM, orders, TESTNET/mainnet,
Pine/parity/MTC/trading, and any economic action.

---

## 12. Stop conditions (explicit)

**Global — halt the entire chain immediately, preserve all evidence, mutate nothing further:**

1. The frozen candidate SHA observed on the host is **not** `2ce41e34…321b` (candidate drift).
2. `RK-B0`'s on-host `EXPECTATIONS.md` hash ≠ the `RK-PRE` local value (predicates not trustworthy).
3. Any evidence-root allocation collision (`mkdir` `EEXIST`, or `<LOCAL_EVROOT>` exists).
4. Any secret-signature hit in any captured artifact.
5. Any check that **cannot be performed** — tooling missing, permission denied, ambiguous output,
   external probe impossible. **STOP, never SKIP, never PASS.**
6. Any attempt by a run-kit step to use `--force`, `--to-release-sha`, `--to-manifest-sha256`,
   `--allow-live-source` (**forbidden outright in `RK-C1`** — §5.4 route (b) is not an execution
   route; the sole remaining warning-class exception is the explicitly-labelled §6.4(c) route for the
   Branch A pre-reboot capture), `|| true` on a fail-closed check, or a `restore` subcommand that
   does not exist.
7. `40873556…` appearing anywhere as an *expected* value.
8. Any step that would start, unmask, enable, arm, provision a credential, change the firewall, or
   place an order.
9. **Any pre/post comparison whose "pre" value was captured after the mutation it is meant to
   bracket.** Such a comparison is vacuous, not clean; reporting it as agreement is a false PASS. A
   genuine pre-mutation baseline is the only admissible input — for `RK-C1` that means a route
   (a)/(d) baseline, and absent one **the stage does not run** (§5.4).
10. **Any stage executed, or any PASS reported for it, while a gap marked BLOCKING in §10 is open** —
    currently `RK-C1` (`D-GAP-C1-1`, `D-GAP-C1-3`) and, by dependency, `RK-C3`, `RK-C4`, `RK-C2/B`.
    Running the stage to "see what it produces" is itself the violation.
11. **`Result=exit-code`, any non-zero `ExecMainStatus`, or any unfrozen exit tuple treated as a clean
    stop** (§5.2) — and equally, `ExecMainCode=0` hard-coded as a post-stop expectation.
12. **Any `RK-C2/A → RK-C1` continuation**, or any start/unmask used to make one possible; and any
    `RK-C4` rehearsal predicate that requires the service to be **active** after the dry run, or any
    start used to satisfy one (§2.2, §8.4).
13. **`stat` invoked across the `bridge.db` / `-wal` / `-shm` trio in a single command**; an absent
    sidecar treated as an error, a SKIP or a silent pass instead of a recorded `ABSENT` line; **or a
    `PRESENT` line emitted from a `stat` whose rc was not adjudicated `0` first** — a swallowed
    `stat` failure yields two identity-free `PRESENT` lines that `cmp` equal, i.e. a state-dir
    mutation reported as proof of no change (§7.3).
14. **Any fail-closed predicate expressed two-way instead of three-way.** Specifically:
    `test … && echo <token> || echo <token>`; `if sudo test -e …; then … else <benign token>; fi`;
    a token read out of a command substitution whose own rc was not adjudicated first; a `grep -c`
    whose rc ≥ 2 is recorded as a count of `0`; a `pgrep` rc `2`/`3` read as "no process"; a bare
    `a | b` pipeline whose `PIPESTATUS` is not adjudicated; a path probe whose "absent" answer comes
    from anything other than a `FileNotFoundError` (a `test`-based probe answers *false* for a
    permission, `ENOTDIR`/`ELOOP` or I/O failure, and an outer `exit 90` sentinel does not repair
    that); or `cd X && <work>` in place of `cd X || STOP`. **A permission, policy, tooling or race
    failure is a STOP — never `ABSENT`, `NOTLINK`, `MISSING`, `NOT-MASKED`, `NONE`, `0`, or empty
    output read as a clean result** (§2.5, §2.5a).
15. **Any mutation that follows a failed, unadjudicated or unrecorded precondition** — the `RK-C1`
    stop, the `RK-C3` capture and publication, the `RK-C4` real invocation, and the `RK-C2` reboot
    each sit behind a gate, and "the rc was recorded" is not permission to continue (§2.5).
16. **Any no-clobber destination admitted on an `-e`-only check.** A dangling symlink is `! -e` and
    still `-L`; `>` and `mv -T` follow it onto its target. The required token is `NONE` from §2.5a
    `classify_path`, asserted immediately before the write or rename, with `FILE`, `LINK` and a
    non-completing probe each a **STOP** (§2.4(3), §7.6, §8.3).

**Stage-specific STOPs** are listed in each stage's failure disposition (§4.1–§4.8, §5.5, §6.5, §7.7,
§8.7) and are not repeated here.

**After a STOP:** preserve every `.cmd`/`.out`/`.err`/`.rc` file and every partial artifact exactly
where it is; do not retry the failed step; do not start or unmask anything; do not publish any
staged artifact; report to the Lead with the captured evidence.

---

## 13. What this unit did not do, and what remains for the Lead

- **No AI_MEMORY or handoff update was made.** Those are **Lead-owned after acceptance**
  (`GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `NEXT_SESSION_HANDOFF_2026-08-08.md`). The residual
  propagation of the withdrawn G4 symbol claim and the wrong lock hash in those three files remains
  outside this unit's write scope and stays with the Lead (matrix §7).
- **No WP0 edit** was proposed or performed; WP0 is correct and uneditable in this task (§1.3).
- **No product, deploy, runtime, tool, test, script or schema file was modified.** In particular,
  the `rollback.sh` no-clobber finding (`D-GAP-C4-1`) is recorded as a finding and handled by a
  run-kit precondition — **no edit to the script is proposed here.**
- **No run-kit, wrapper or script was authored.** This document is the design contract that a later
  implementer will build from; `D-GAP-C3-1` names the one wrapper that must be written.
- **Open for a human decision, in this order:**
  1. the budget re-plan or explicit 50 h ceiling extension (blocks everything host-touching);
  2. the choice between **Branch A** and **Chain B** (§2.2), which is now a choice between two
     *different scopes*, not two orderings:
     - **Branch A** — `RK-PRE → RK-B0..B7 → RK-C2/A`, bounded and **terminal**, ending inactive +
       unmasked. Reachable once the budget and reboot lifts are granted; carries `D-GAP-C2-1` for its
       pre-reboot capture; yields reboot-safety evidence only, and **no** stop, WAL-bundle or
       rollback evidence. Extending it to `RK-C1` afterwards would require a separately authorised
       `RK-REC` start **plus** a fresh accepted Stage B recapture — a different, unbudgeted, uncosted
       unit that this design does not include.
     - **Chain B** — the full `RK-C1 → RK-C3 → RK-C4 → RK-C2/B` sequence, which **cannot start** until
       the two blocking `RK-C1` gaps are closed;
  3. **whether to fund closing the `RK-C1` blockers**, which is the prerequisite for any Group C work
     beyond Branch A: `D-GAP-C1-1` (offline determination of the pinned uvicorn SIGTERM exit contract
     and its systemd mapping, §5.2) and `D-GAP-C1-3` **via route (a) or route (d) only** (§5.4) — an
     exact safe active-writer capture method, or an independently accepted equivalent proving the same
     pre/post persistence property. **Routes (b) and (c) are not on the menu:** neither a warning-class
     baseline nor no baseline may be used to run `RK-C1` or to report a PASS for it. Both closures are
     local/offline and need no host;
  4. the per-stage authority lifts of §11, each named explicitly rather than inferred from the
     standing programme authorisation — noting that lifts alone unblock only Branch A.

---

## 14. Self-QA record for this unit

| Check | Result |
|---|---|
| `git diff --check` | clean — no whitespace/conflict errors introduced |
| Exactly one new path, no other modification | ✅ only `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_LOCAL_RUN_KIT_DESIGN_2026-08-09.md` is added; `git status --short` shows one untracked file and nothing else |
| Nothing staged or committed | ✅ no `git add`, `commit`, `push`, `checkout`, `switch`, `reset`, `stash`, `clean`, `branch`, `tag`, or worktree mutation was run |
| All product facts candidate-qualified, ref-invariant, or governance-labelled | ✅ every product/deploy/runtime/tool/test citation is written `2ce41e34…321b:<path>:<line>` and tagged `[SRC]` or `[REF-INV]`; `SECURITY_BASELINE.md` is tagged `[GOV]` and is never cited as candidate source; external systemd/SQLite semantics are tagged `[SYSTEMD]` rather than passed off as candidate facts |
| No `40873556…` Linux predicate | ✅ the token occurs in exactly four places, none of them a predicate: §1.2 row 3 (**never cite**), §4.2's disposition table (a *failure signature*, i.e. the value that would indicate a CRLF file reached the host), §12 stop condition 7 (which forbids it as an expected value), and this self-QA row. It is never preregistered, never expected, and never a Linux predicate anywhere |
| No installed-host hash claimed observed | ✅ `a1881296…` is labelled `[EXPECT]` at every occurrence; the observed installed-host value is labelled **NOT IN EVIDENCE** in §1.2, §4.2 and §10 |
| No C5 execution, and no credential/network procedure supplied | ✅ §9 records the structural blocker and explicitly declines to provide an executable procedure |
| No WP0 edit, no AI_MEMORY edit, no handoff edit | ✅ §1.3, §13 |
| No host contact, no product test, no mutating command | ✅ §0 — read-only Git and local reads only |
| Every stage carries purpose · anchors · mutation class · prerequisites · command shape · no-clobber contract · PASS predicates · failure/STOP · secrets rule · unresolved | ✅ §4.0–§4.8, §5, §6, §7, §8, §9 |
| No design gap silently converted to an asserted host fact | ✅ twelve gaps carried openly in §10, each with its closure route and none executed; two of them (`D-GAP-C1-1`, `D-GAP-C1-3`) are marked **blocking** and gate execution rather than merely labelling a result |
| No difference predicate rests on a baseline captured after its own mutation | ✅ `RK-C1`'s pre-stop baseline is named as `D-GAP-C1-3` (§5.4); an after-stop capture compares the post-stop state with itself, so a post-stop baseline is invalid in every form. §12 stop condition 9 forbids the pattern generally. `RK-C2`'s pre-reboot freeze is unaffected: it is genuinely taken before the reboot |
| `RK-C1` cannot be run or passed through a weakened route | ✅ blocked from execution until `D-GAP-C1-1` **and** `D-GAP-C1-3` are closed and frozen in `RK-PRE` (banner, §2.1, §2.8, §5 authority note, §5.2, §5.4, §5.5 execution gate, §10, §11, §12(10)). Route (b) (warning-class baseline) and route (c) (no baseline) are rejected as execution routes; only route (a) — an exact safe active-writer capture method — or route (d) — an independently accepted equivalent proving the same pre/post persistence property — unblocks it. The protected pre/post equality requirement is retained as mandatory and is not relaxed anywhere |
| No gapped exit result can produce a PASS | ✅ `exit-code` is removed from every accepted set and is an explicit STOP (§5.2, §5.5, §12(11)); the `Result`/`ExecMainStatus` tuple is adjudicable only against the value frozen when `D-GAP-C1-1` closes; the warning against hard-coding `ExecMainCode=0` is retained (§5.2); §5.3 now states in terms that the three no-SIGKILL legs prove *no escalation*, not *successful application shutdown*, and may not substitute for the missing tuple |
| `RK-C4` dry-run predicate matches its real starting state | ✅ in Chain B `RK-C4` follows `RK-C1`/`RK-C3`, so the unit is **inactive + unmasked** on entry; §8.2(7) and §8.4 preregister and capture that starting state, require it unchanged across the dry run, require **no** rollback manifest and byte-identical `RK-C3` bundle/manifest evidence, and place the `static → masked` transition on the real invocation only. The impossible "service still active" requirement is gone, and §8.7 + §12(12) forbid starting the service to satisfy a rehearsal predicate |
| No absent-sidecar `stat` failure path | ✅ the trio is never stat-ed in one command; §7.3(0)/(2) specify a per-path recorder emitting `PRESENT <stat identity>` or `ABSENT <path>`, with a byte-exact before/after `cmp` (§7.3(2b), §7.2(6), §7.5(2), §7.7). A newly appearing, vanished or changed sidecar is a STOP; `ABSENT` in both records is normal evidence, never an error and never a SKIP. **Absence-tolerance is scoped to the *answer*, not the *question*.** Stated exactly, because an earlier wording said the recorder "always continues" and that is wrong: the recorder continues **only** on a genuine `NONE` — i.e. `os.lstat` raised `FileNotFoundError` and nothing else — and it **terminates** on `LINK` (a symlink in the protected state dir), on a probe that did not complete (rc `91` or any status ≠ `90`), on a `stat` whose inner rc is not `0`, and on an empty stat identity. Three of its four exits are STOPs |
| **No fail-closed predicate collapsed into a benign token (repair class R2)** | ✅ **repaired throughout.** `test … && echo … \|\| echo …` and `if sudo test -e …; then … else <token>; fi` are removed from every command shape and forbidden by name (§2.5, §12(14)). §2.5a introduces four helpers — `STOP`, `sudo_rc`/`priv_rc` (a sentinel that separates `sudo`'s own rc 1 from a command's legitimate "false"), `classify_path` (one **exception-aware** `os.lstat` probe → `LINK`/`FILE`/`NONE`, with `FileNotFoundError` the sole route to `NONE`), and `count_rc`/`count_rc_priv` (grep rc 0/1 = count, rc ≥ 2 = STOP) — and every predicate now has three outcomes. Repaired sites: §4.0 (B0 `mkdir`/`sha256sum`), §4.2 (B1a manifest `grep -o`), §4.3 (B2 `[Install]`/SHA counts + mask probe), §4.4 (B3 symlink sweep, `stat` identities, manifest counts, logrotate), §4.5 (B4 fragment and **env-file counts whose PASS token is `0`**), §4.7 (B6 `ss` pipeline + `ufw`), §4.8 (B7 `cd`/`find`/`xargs`), §5.3 leg 3 and §5.5 (`pgrep` rc 2/3, `ss`, `journalctl`), §6.2 checks 5/8/9, §7.3(0)/(2)/(7), §8.3, §8.4(1)(3)(4), §8.5 (mask probe, post-assertions 1/4/5/6) |
| **No `stat` failure hidden inside a command substitution (repair class R2)** | ✅ the C3 recorder no longer writes `printf 'PRESENT %s\n' "$(sudo stat …)"`, where `printf`'s own rc 0 masked a failed or raced `stat` and produced a `PRESENT` line with an empty identity — two of which `cmp` equal, reporting a real state-dir mutation as proof of no change. The identity is now captured into a variable, its inner rc recovered through `priv_rc` and required to be `0`, and required non-empty, **before** any line is emitted (§7.3(0), §7.5(2), §7.7, §12(13)) |
| **"Recorded, not fatal" cannot license continuation past a failed prerequisite (repair class R2)** | ✅ §2.5 now states the contract in three parts: errexit is disabled **only** for the single invocation, long enough to write `.rc` (plus `PIPESTATUS`); adjudication is **immediate**; and a STOP verdict means **no later command in that stage or chain executes — above all no mutation**. Explicit mutation gates are placed at §5.5 (the `systemctl stop`), §7.3(1) (the capture), §7.6 (publication) and §8.5 (the real `rollback.sh` invocation), and §12(15) forbids the pattern globally |
| **No-clobber publication rejects a dangling symlink (repair class R2)** | ✅ §2.4(3) now requires the destination to be **neither `-e` nor `-L`**, asserted with `classify_path` and the token `NONE`. §7.6 places that assertion immediately before `mv -T` with nothing in between, states why an `-e`-only check fails (a dangling link publishes *through* the link, outside `<EVROOT>`), and adjudicates the `mv` rc as STOP-on-failure with no retry and no copy fallback. The same token discipline is applied at §2.3 (`<LOCAL_EVROOT>`), §4.0, §4.8, §7.2(2)(3) and §8.3, and §12(16) forbids the `-e`-only form globally |
| **Residual fail-closed defects closed (repair class R3)** | ✅ four items, each checkable in the text. **(1) H2 distinguishes `FileNotFoundError` from every other `OSError`.** The probe is `os.lstat` under the interpreter `RK-B1` proves is `3.12` (asserted first, as `RK-B0` step 1, before any probe runs); `except FileNotFoundError` is written above `except OSError` because it is a subclass; `NONE` is emitted on ENOENT **alone**; every other `OSError` (EACCES, EPERM, ENOTDIR, ELOOP, EIO, ESTALE…) exits `91`; a `sudo` policy refusal, a missing interpreter, an exec failure or a signal leaves some other status; and `classify_path` returns `2` = STOP for every status ≠ `90`. The former `sh -c '[ -L ]/[ -e ]; exit 90'` shape is **gone**: `test` answered *false* for permission, path-resolution and I/O failures, so the helper emitted `NONE` — the PASS token of every no-clobber destination — and the outer sentinel then certified it, proving only that `sh` reached its last line. **(2) `STOP` performs no unchecked artifact write.** It is `printf … >&2` + `exit 90`; the `>> "${EVROOT}/99_stop.txt"` append is removed, because `>>` creates through and follows a symlink at that path and appends into evidence another stage already wrote. Nothing is lost: the §2.5 recorder captures the reason in `.err` and the status in `.rc` for the exact command that failed (§2.5a H0). **(3) The last executable legacy two-way predicate is gone.** §8.5's mask check is now the H2 token flow requiring exactly `NONE`, with probe failure an explicit STOP; `rg` confirms every surviving `test … && echo … \|\| echo …` string sits inside a quoted `⛔ NOT` explanation and none is a command. **(4) Publication rejects an existing object *and* a dangling link.** §7.6 requires token `NONE` immediately before `mv -T`, so `FILE` and `LINK` (live or dangling) each STOP, and the helper's **rc is adjudicated in its own step before the token is compared** — `[ "$(classify_path …)" = NONE ]` is banned by name in §2.5a, and the two-step form is used at §4.0, §4.3, §4.4, §4.8, §7.3(0)/(2), §7.6, §8.3 and §8.5 alike. §7.3(3)'s two hash extractions are likewise rc-adjudicated and shape-checked (64 lowercase hex) before either can become an `--expect-*-sha256` argument |
| Pipeline and multi-path rc masking | ✅ every recorded pipeline runs under `set -o pipefail` with the whole `PIPESTATUS` vector written into `.rc`; `ss \| awk`, `find \| sort \| xargs`, `cd && find`, multi-path `stat` and `cmp` each carry an explicit rc disposition (§2.5, §4.7, §4.8, §5.5, §6.2(5)(9), §7.3(7), §7.7). Note the shape of the hazard this closes: nearly every Group B/C predicate PASSes on **empty output**, which is exactly what a denied or crashed tool produces |
| Chain coherence — no `RK-C2/A → RK-C1` edge | ✅ Scenario A is a bounded, terminal `RK-C2`-only branch ending inactive + unmasked (§2.1, §2.2, §6.1, §6.2, §6.5(4), §10, §11); reaching `RK-C1` afterwards is documented as requiring a separately authorised `RK-REC` start **plus** a fresh accepted Stage B recapture, and that recovery start is never silently included (§2.2, §6.1, §6.5, §11, §13). Chain B is stated as the only coherent full chain and is itself blocked at `RK-C1` |
| Mandatory routing record present | ✅ §0.2 |

**Final `git status --short`:** one untracked path — this file. Nothing else added, modified,
deleted, staged or committed.
