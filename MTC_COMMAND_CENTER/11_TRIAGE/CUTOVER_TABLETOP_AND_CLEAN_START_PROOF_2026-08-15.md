# L12 — Cutover tabletop and the start-clean safety proof

- Lane: L12. Date of record: 2026-08-15 (night).
- Repository read: `C:\RO`, detached at `25564449` (per the L12 kickoff; confirmed by the
  session's clean-git snapshot whose HEAD commit is `25564449` "docs: dashboard after the
  owner's five decisions"). No git command was run and nothing in the repo was written.
- Status: **PLANNING / REHEARSAL MATERIAL ONLY. NO AUTHORITY.** This document grants no
  host, network, deployment, service, credential, broker/exchange, ARM, order,
  TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, or economic action, and it
  is not an acceptance of any gate. It produces material for the Lead and the owner
  (WBS:212-212 boundary style).
- Suggested audit tier for this artifact, for the Lead to classify (not decided here):
  **T2 — documentation/evidence** per `AGENTS.md:37-37`.
- Citation keys used throughout (all paths relative to `C:\RO`):

| Key | Path |
|---|---|
| `DEC` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` |
| `TASKS` | `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md` |
| `LIST` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md` |
| `WBS` | `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md` |
| `RR` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md` |
| `SC` | `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/recovery/STATE_CONTINUITY.md` |
| `DEP` | `IBKR_PAPER_BRIDGE/docs/17_DEPLOYMENT.md` |
| `WSC` | `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md` |
| `WAL` | `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py` |
| `WALT` | `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` |
| `DDP` | `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md` |

## Part 0 — What D5 changed and what it did not change

D5 selects a **fresh-database reset** at cutover, a deliberate owner override of the
recommended WAL-consistent migration (`DEC:89-96`). It does not waive anything else:

1. The destination starts with no inherited daily-loss counter, no consecutive-loss
   counter, no order history and no foreign-position record (`DEC:100-101`).
2. Checklist item 5's clause survives the choice: a fresh reset must still **"preserve or
   block on"** lost daily-loss, consecutive-loss, order and foreign-position evidence —
   either carried forward in some retrievable form, or the service refuses to start rather
   than silently lose it. "Start clean" is not "start blind" (`DEC:102-107`;
   `LIST:116-118,124-128`).
3. The single-writer cutover proof of item 6 is unchanged and mandatory: raw empty
   positions and raw empty orders captured before and after the old writer is stopped,
   "whatever happens to the database" (`DEC:108-110`).
4. Deploy item 4 (KVM2 TESTNET wallet) stays deferred and blocks the first start; nothing
   may proceed past the point that requires it (`DEC:80-87`).

Two framing facts for everything below:

- The 2026-08-15 readiness refresh had already specified exactly this branch: "If Barış
  instead wants a reset, he must explicitly select it and approve a fail-closed
  specification covering lost daily-loss, consecutive-loss, order, and foreign-position
  evidence" (`RR:190-193`). D5 is that explicit selection; Part 2 below is the
  fail-closed specification material it requires.
- The deployment guide's older rule already permitted a fresh DB only if separately
  selected by the owner **and** fail-closed tested against daily-loss, consecutive-loss,
  order and foreign-position ambiguity (`DEP:68-73`, Turkish original). Part 2 satisfies
  the second half of that sentence.

---

## Part 1 — The cutover tabletop (row R39 / task P4-04)

### 1.1 Authority boundaries of this tabletop

- Source task: **KVM2-P4-04** — "document walkthrough/tabletop only — no process,
  service, scheduler, listener, network, secret, exchange, or writer mutation"
  (`TASKS:294-296`). Its stop conditions: any live mutation; an unresolved abort/PC-off/
  dual-writer case; a procedure implying permanent Windows dependency; the tabletop cited
  as P4-04A quiesce or P4-05 cutover authority (`TASKS:300-303`). **This document is not
  authority for P4-04A or P4-05.**
- The ordered proof being rehearsed is checklist item 6 (`LIST:132-138`) with the fuller
  P4-05 detail (`TASKS:313-330`).
- In the work breakdown this is row R39, placed **before** R40 (quiesce) and R42
  (cutover) in **both** contested orderings (`WBS:103-104` Ordering A;
  `WBS:124` Ordering B), so the tabletop's position does not depend on the unsettled
  plan-authority question (`WBS:19-26`).
- Actors follow the governing docs: the cutover proof itself is `[AI: Barış]`
  (`LIST:132`; `TASKS:313`); the tabletop production is `[AI: Claude]` (`TASKS:294`).
  The tabletop facilitator does not touch hosts; live bridge state is owner-controlled
  evidence (no AI task may call the unauthenticated control API to collect facts,
  `TASKS:28-33`).

### 1.2 The invariant the whole procedure exists to prove

Writer-state lattice (the property, not a status claim):

```
S1  one writer    : old Windows bridge (DISARMED, sole exchange authority)
S2  zero writers  : old task stopped+disabled, processes gone, 8790 closed,
                    old-host agent revoked, flatness reconfirmed from exchange
S3  one writer    : first VPS DISARMED start (separate P4-06/P4-07 authority)
```

**Zero dual-writer interval** means: the only legal transitions are S1→S2→S3, every
transition is evidenced in a timestamped ordered record (`TASKS:324-325`), and no abort
path may ever create S1' (Windows recovered) while any VPS writer authority exists —
P4-04 requires "VPS authority absent before any owner-controlled DISARMED Windows
recovery" (`TASKS:297-298`).

"VPS authority absent" is checkable, not assumed. Grounded composition of that check
(the actual current state of KVM2 is **UNKNOWN** — see §1.6): the service must be
installed disabled/masked and unstarted with no TESTNET secret provisioned per the
install contract (`TASKS:278-284`), and D4 has deferred the KVM2-specific wallet, so no
VPS credential exists for the bridge to sign anything with (`DEC:80-87`). A VPS with a
masked unit, no process, no `127.0.0.1:8790` listener, and no provisioned wallet
structurally cannot write. Each element is an evidence check in the abort walks, never an
inference.

### 1.3 The tabletop script

Spine = item 6's exact order (`LIST:133-138`), with the P4-05 state-policy tail
(`TASKS:318-325`) executed under the D5 reset branch. Every step is a **paper action**:
the tabletop walks who would do what, what evidence would exist afterwards, and what
would stop the procedure. Nothing is executed.

Outcome vocabulary (applies to every check in every step, per DDP Pattern 1 — "STOP is
not a result", `DDP:48-107`, rule at `DDP:101-107`):

- **PASS** — expected state observed.
- **FAIL** — deviant state positively observed.
- **STOP** — the observation itself did not happen (probe error, unreadable evidence,
  ambiguous output). Per item 6, "any failed **or ambiguous** check stops the cutover"
  (`LIST:137-138`); FAIL and STOP are equally blocking, and the record must say which
  one fired.

| # | Step (item 6 order) | Actor | Evidence produced | Pass condition | Stops the cutover when | Abort path |
|---|---|---|---|---|---|---|
| T0 | Preconditions: P4-04A closed; P4-05 authorization exists; destination release identity frozen (exact SHA/config to be recorded in T1); R41 operations evidence already executed under Ordering A (`WBS:103-104`; `RR:337-341`) | Owner/Lead | Owner sentences; frozen-SHA record | all present and cited | any precondition absent, or this tabletop cited as one of them | AB-0 (below): no cutover; nothing has happened yet |
| T1 | Record exact SHA/config (`LIST:133`) | Owner | recorded destination release SHA + config identity in the ordered record | identity recorded and unambiguous | no frozen accepted SHA exists (current status: **UNKNOWN/open**, `RR:82-102`, `WBS:23-24`) | AB-0 |
| T2 | Confirm DISARMED (`LIST:133`; `TASKS:314`) | Owner (owner-controlled live state, `TASKS:28-33`) | DISARMED proof of the running old bridge | state == DISARMED positively observed | state is ARMED (FAIL) or state cannot be observed (STOP) | AB-1 |
| T3 | Obtain a fresh reconcile (`LIST:133`; `TASKS:314`) | Owner | reconcile-freshness evidence (documented status surface: `mode`, `exchange_conn`, `reconcile_ready`, `state`, `DEP:53-54`) | reconcile fresh | stale/absent reconcile, or status unreadable | AB-1 |
| T4 | Capture **raw empty positions and raw empty orders** (first capture, before stop/revocation) (`LIST:134`; `TASKS:315`; `DEC:108-110`) | Owner | timestamped raw exchange-side captures, no secrets (`TASKS:318-319`) | both empty | any non-empty position/order (FAIL) — flatten scope belongs to P4-04A, not here (`TASKS:306-308`); capture unreadable/ambiguous (STOP) | AB-1 |
| T5 | Stop and disable the Windows task (`LIST:134`; `TASKS:315`) | Owner | task state evidence: stopped **and** disabled (`DEP:65-67` ritual; disable is what prevents a logon restart, `DEP:49-49`) | stopped + disabled both observed | only stopped, or state ambiguous | AB-2 |
| T6 | Prove wrapper and child processes gone and port 8790 closed (`LIST:135`; `TASKS:315`) | Owner | process inventory + port-state evidence (runtime root is the isolated P2RT worktree wrapper, `DEP:14-20`; no P2RT mutation is authorized by any of this, `LIST:169-170`) | zero wrapper/children; 8790 closed on old host | any survivor process or open port (FAIL); cannot observe (STOP) | AB-2 |
| T7 | Revoke the old-host agent (`LIST:136`; `TASKS:316`) | Owner | revocation record (name only; per-machine agent-wallet model in `DEP:22-27`) | revocation confirmed | revocation unconfirmed or unprovable | AB-2 |
| T8 | Reconfirm raw empty positions and orders (second timestamped capture, post-revocation, taken VPS-side; pre/post-revocation responses captured without secrets) (`LIST:136-137`; `TASKS:316-319`) | Owner | second timestamped raw captures + pre/post responses, sanitized | both empty again | any non-empty or changed result (FAIL); unreadable (STOP) | AB-2 |
| T9 | Apply the accepted state policy — **D5 reset branch** of the P4-05 tail (`TASKS:319-325`): (a) final source capture + SHA-256 (the Part 2 archive); (b) execute the conservative reset; (c) `integrity_check` passed; (d) semantic checks on daily-loss, consecutive-loss, foreign positions/orders, corrupt/unknown state; (e) source and destination artifact hashes + timestamped ordered record | Owner + executor | archive bundle + manifest + two externally recorded SHA-256; raw-capture hashes; pristine-destination evidence; ordered record | archive captured and verified; reset executed; destination pristine; all hashes bound | capture fails (exit 2/3, `WAL:54-59`), verify fails, any mismatch or **unknown** evidence (`TASKS:325`) | AB-2 / AB-3 |
| T10 | Cutover proof complete — the item-6 record now exists in order; the first VPS service start becomes *permissible*, and remains separately gated by P4-06/P4-07 (`LIST:137-138`; `TASKS:331-348`) | Owner/Lead | complete ordered timestamped record | every T1–T9 outcome PASS | record incomplete or any step unrecorded | AB-2 / AB-3 |

### 1.4 Abort walks (the part P4-04 exists for)

P4-04 requires walking "failed mid-cutover and PC-off aborts: VPS authority absent before
any owner-controlled DISARMED Windows recovery, state/evidence preserved, zero
dual-writer interval" (`TASKS:296-299`).

**AB-0 — abort before T1.** Nothing has happened. Record the decision; no host state
exists to preserve. The procedure implies no permanent Windows dependency because no
procedure ran.

**AB-1 — abort at T1–T4 (old writer still running, still the only writer).** State S1
unchanged. Abort action: stop the procedure, preserve all evidence gathered, escalate to
owner. Do **not** stop the Windows task as a "cleanup" — every mutation needs its own
authority. Dual-writer risk: none (S1 throughout). Windows recovery: not needed (it never
left). The plan does not imply permanent Windows dependency because AB-1 leaves the
pre-cutover world intact, not because Windows must survive long-term.

**AB-2 — abort at T5–T8 (old writer stopped or being stopped; VPS never started).**
State S2. This is the delicate box: zero writers, and the only exits are (i) forward to
T9/T10 under new authority, or (ii) backward to a Windows DISARMED recovery. The abort
path is:

1. Freeze: no further steps; preserve everything (including negative results) in the
   ordered record — "state/evidence preserved" (`TASKS:298`).
2. Prove VPS authority absent (masked/inactive unit, no process, no listener, no
   provisioned wallet per `TASKS:278-284` and `DEC:80-87`) — this must be evidenced
   **before** any Windows recovery is contemplated (`TASKS:297-298`).
3. Only then may the owner choose an owner-controlled **DISARMED** Windows recovery
   (re-enable task, confirm DISARMED before anything else, per the migration ritual's
   disarm-first order, `DEP:65-68`). Recovery while ARMED, or while any doubt about VPS
   authority exists, is prohibited by the same clause.
4. Escalate: each abort is a new decision; P4-04A's "exactly one quiesce" discipline
   means a re-quiesce needs a new authorization (`TASKS:304-312`).

Dual-writer invariant in AB-2: the only way to violate it is to start the VPS (or give
it authority) while re-enabling Windows. The abort path forbids both simultaneously by
construction: recovery requires proven VPS-authority-absence first; VPS start requires
the complete T1–T9 record.

**AB-3 — abort at T9 (reset/archive phase fails).** State S2. Critical special case: if
the capture fails with the hot-WAL-without-`-shm` error — a crashed writer's exact
leftover — the tool fails closed and states that recovery "needs a read-write connection
and therefore a separate owner authorization — it is never done silently by this tool"
(`WAL:215-239`, especially `WAL:230-236`). The abort path: leave the source trio
untouched, record the failure, escalate. Bypassing it (opening read-write, deleting the
WAL, copying the trio by hand) is exactly the naive-copy failure mode the tool exists to
prevent — silently losing committed trades or resetting risk history (`WAL:5-12`). The
old database is also the last copy of the paper period until an archive exists (see
Part 3).

**PC-1 — PC powers off before T5 (writer dies uncleanly mid-procedure).** S1 collapses
to S2 without an orderly stop. Consequences walked: (a) no dual-writer interval is
created — the writer died, nothing replaced it; (b) the database may be left with a hot
WAL, which makes a later read-only archival capture fail closed (`WAL:230-236`) — AB-3's
escalation applies; (c) the ordered record must show the last completed step
(timestamped), which is the only honest account of what state the world is in; (d) owner
chooses: investigate/recover Windows DISARMED (after proving VPS authority absent,
`TASKS:297-298`), or authorize a read-write recovery path as a new decision. A power
button is not an abort procedure; this walk exists so the decision is pre-made, not
improvised.

**PC-2 — PC powers off at T5–T8 (after stop/disable).** A disabled task does not come
back with power (`DEP:49-49`, `Disable-ScheduledTask` semantics). State remains S2;
evidence already captured is preserved; walk is AB-2 unchanged. The point of walking
this: the procedure's truth does not depend on the old machine surviving once it is
stopped — which is also why the archive question (Part 3) matters.

**PC-3 — PC powers off after T9 (archive exists, reset done).** S2 with evidence
secured off the old machine's liveness. Proceed by new authority (T10 → P4-06/P4-07);
the old machine's fate is now decoupled from the evidence record.

**WR — Windows-recovery branch, walked as its own scenario.** Question: does any abort
path imply a *permanent* Windows dependency (P4-04 stop condition, `TASKS:302-303`)?
Answer walked: Windows recovery is a **fallback**, never the steady state. The steady
state is S3 (VPS writer) reached through T10. Recovery exists only to exit S2 backward
when the forward path is blocked, and requires proof of VPS-authority-absence first. If
the forward path is abandoned permanently, the plan's end state is the KVM2 topology
(Phase 10/11), not a restored Windows bridge — Phase 11 exists to close the lifecycle
and archive evidence (`TASKS:847-860`).

### 1.5 How this tabletop is run, and how it could fail (D026 / DDP Pattern 10)

- Run: Lead facilitates; owner adjudicates the abort branches. Inputs: this script plus
  the governing documents. Output: an adjudication record — every step and abort walk
  marked walked, every STOP/FAIL/abstention named, open questions listed, dated. Any
  **live** rehearsal (staging a fake quiesce, injecting a failure on a disposable host)
  needs a separate future bounded owner authorization (`TASKS:299-300`).
- Falsifiability (DDP Pattern 10 — "evidence that cannot fail", `DDP:614-687`): a walked
  tabletop that cannot name an observation that would have stopped it is theater. Each
  row above therefore carries an explicit Stops-when column, and the adjudication record
  must record at least one deliberately-walked blocking case per phase class (a FAIL at
  T4, a STOP at T6, an AB-3 hot-WAL failure, a PC-1). A walkthrough in which nothing was
  ever allowed to fail is not closure evidence.
- Claim discipline (DDP Pattern 9, `DDP:546-613`): the tabletop's output claim is
  exactly "the procedure was walked and every branch reached a disposition" — **not**
  "the cutover is safe" and not "any current runtime state is known" (see §1.6).

### 1.6 What this tabletop cannot establish (UNKNOWN, honestly)

Per the readiness refresh's bounded UNVERIFIED list, all of the following are unknown
from the repository and none is inferred here (`RR:349-377`, especially `RR:206-211,
366-370`): current Windows task/wrapper/child/writer/DB/port state; current reconcile
freshness and raw exchange orders/positions; old-agent revocation state; whether a
WAL-consistent source bundle can be captured now; any current KVM2 fact (install,
listener, UFW, wallet existence). The tabletop rehearsing these checks is not evidence
that they would pass; it is evidence that the procedure knows what to do when they fail.

---

## Part 2 — Proving "start clean" is not "start blind"

### 2.1 The requirement, verbatim

Checklist item 5: the owner must select and test "a conservative, explicitly approved
fresh-database reset that **preserves or blocks on** lost daily-loss, consecutive-loss,
order, and foreign-position evidence" (`LIST:116-118`). D5 records that this clause is
"not waived by the choice" and that a fresh reset must be proven either to carry the
four evidence classes forward in some retrievable form, or to refuse to start rather
than silently lose them (`DEC:102-107`; `LIST:124-128`).

### 2.2 Evidence inventory — the four classes mapped to capture mechanisms

What the existing WAL bundle tooling captures (it was built for the migration path, but
its capture output is exactly an archival record; the tool's own header binds it to
"KVM2 P2-06 / P4-05", `WAL:1`):

| Clause class | Captured by `wal_state_bundle` | Where |
|---|---|---|
| Daily-loss | full `risk_days` ledger per row (`trading_date`, `day_start_equity`, `realized_pnl_engine`, `realized_pnl_broker`, `max_intraday_dd`, `consecutive_losses_end`, `auto_rearms_used`) plus per-environment `realized_pnl_latest_date` / `latest_trading_date` | `WAL:383-402`, `WAL:319-380` |
| Consecutive-loss | per-(mode, network) `consecutive_closed_losses` streak re-derived from closed-trade PnL ordering, plus `risk_days.consecutive_losses_end` | `WAL:319-353` |
| Order | full `orders`/`fills` history inside the bundle DB, plus sanitized invariants: `counts.orders`, `live_orders` (statuses OPEN/SUBMITTED/PENDING), `max_ids` (decision/event/trade) | `WAL:106-121`, `WAL:273-299` |
| Foreign-position | **not** in the DB invariants — by design. "Foreign exchange positions/orders are not inferred from SQLite; they remain separate raw exchange-side cutover checks under owner control" (`SC:24-26`) | covered by the item-6 raw captures T4/T8 |

So three of the four classes are machine-captured and hash-bound by the existing tool;
the fourth is carried by the already-mandatory raw exchange-side captures of item 6
(`LIST:134,136-137`; `DEC:108-110`). The archive design below binds all of it into one
record.

Two honest observations about coverage:

- The invariants surface reads only counts/aggregates/timestamps/enum state and
  deliberately excludes `runs.config_json`, `events.detail`, `decisions.payload_json`,
  `directives.raw_response` as identifier-carrying (`WAL:262-268`). The **bundle DB
  itself** nonetheless contains the complete history (it is an online-backup snapshot of
  the whole database, `WAL:14-16`), so nothing is lost — only the sanitized summary is
  narrowed.
- The monitoring-window meta keys (`window_started_ts` etc., `WSC:19-24`) are inside
  the bundle DB but are **not** enumerated in the sanitized invariants (only
  `schema_version` and `app_state` meta keys are read, `WAL:302-303,314-316`). Item 5's
  clause does not name window state, so this is not a compliance gap — but the owner
  should know the paper period's window/interruption evidence lives in the archived DB,
  not in the manifest summary.

### 2.3 The design: ARCHIVE (preserves) + GATE (blocks on)

The clause is a disjunction, but the honest design satisfies **both** prongs, because
each alone has a hole: an archive nobody checks before start can be silently missing
when needed, and a start-refusal without an archive destroys the evidence while refusing.
The two prongs close each other's holes.

**Prong A — capture before the reset (the "preserves" half).**

All of it is offline, read-only tooling against the source; running it against a live
runtime worktree needs its own separate owner authorization (`WAL:36-42`), which the
cutover authorization (P4-05) would supply at execution time.

- A1. Preconditions: writer quiesced and single-writer/flat evidence accepted — i.e.
  after T5–T8 of Part 1 (`SC:9-11`; `TASKS:318-319`).
- A2. Capture: `python IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py create --source
  <old bridge.db> --out-dir <archive dir>` — **without** `--allow-live-source`; the
  CLI help itself states "Never use this for a cutover capture: the writer must already
  be quiesced" (`WAL:46-48`; `WAL:1066-1073`; `SC:10-11`). Required outcome: exit 0,
  verdict `CAPTURED`, `changed_during_capture` false. Exit 2 (drift/corruption) or 3
  (input error) blocks the reset (`WAL:54-59`; `WAL:683-686`). The tool never copies the
  db/-wal/-shm trio and never mutates the source (`WAL:14-16`, `WAL:36-42`).
- A3. Externally record the two authoritative hashes — `bundle_db_sha256` and
  `invariants_sha256` from the create report (`WAL:747-755`) — into the owner-held
  cutover record, out-of-band from the archive itself. This is not optional ceremony:
  `verify` **requires** both externally recorded expected hashes and refuses to run
  without them (`WAL:969-981`; `WALT:829-849`), which is what makes the archive
  verifiable by someone who does not trust the archive's own metadata.
- A4. Bind the foreign-position evidence: add the T4/T8 raw exchange-side empty
  captures (sanitized, no secrets, `TASKS:318-319`) and their SHA-256 values into the
  same cutover record, cross-checked against the bundle: the bundle's `live_orders`
  invariant must be 0, matching the raw empty-orders capture. A bundle showing
  `live_orders > 0` against a raw empty capture is a mismatch and blocks ("any mismatch
  or unknown evidence blocks the cutover", `TASKS:325`).
- A5. Verify the archive at rest: `wal_state_bundle.py verify --bundle-dir <archive>
  --expect-bundle-sha256 <A3 value> --expect-invariants-sha256 <A3 value>` on the copy
  at its final storage location, after transport (copy corruption is caught by the
  `bundle_db_hash_not_expected` check, `WAL:1012-1013`). Required outcome: exit 0,
  verdict `VALID`. Verify re-derives every invariant from the bundle DB and fails closed
  on drift, tamper, sidecars, or unsanitized fields (`WAL:969-1049`; `SC:16-21`).
- A6. Only then execute the reset (fresh destination database) and record destination
  pristine-state evidence: `integrity_check` ok, bridge schema present (`WAL:90-104`
  fails closed on a schema without the required tables), expected-empty invariants,
  `app_state` DISARMED — the reset-branch reading of P4-05's "SQLite `integrity_check`
  passed; semantic checks … corrupt/unknown state" (`TASKS:322-324`).
- A7. Produce the timestamped ordered record binding: source provenance hashes, bundle
  hash, invariants hash, raw-capture hashes, destination pristine evidence
  (`TASKS:324-325`).

**Prong B — the start gate (the "blocks on" half).**

The refusal-to-start is enforced at the existing first-start gate, not by new product
code (this lane may change no product code, and no owner decision authorizes any):

- B1. P4-06 (owner) authorizes exactly one first DISARMED start **citing the verified
  archive record** — the reset-branch instance of "the exact accepted destination state
  artifact from P4-05" (`TASKS:331-336`, `TASKS:342-344`).
- B2. P4-07 (executor) verifies before starting: archive present, `verify` re-run
  against the externally recorded hashes exits 0, destination pristine-state evidence
  matches the ordered record. P4-07's existing stop condition — "the P4-05 destination
  state artifact absent, unverified, or hash-mismatched before start" (`TASKS:346-348`)
  — is the refusal mechanism. A missing, corrupt, or unverifiable archive therefore
  **stops the first start** with no code change.
- B3. Classification at the gate: absent/unreadable/mismatching archive is either FAIL
  (positively wrong) or STOP (cannot evaluate) — and both block, mirroring item 6's
  "failed or ambiguous" rule (`LIST:137-138`) and DDP Pattern 1's refusal to launder an
  inability to evaluate into a verdict (`DDP:48-107`).

**One wording gap the owner/Lead must settle (not decidable here):** P4-07 says the
destination state artifact is "verified **loaded** (recorded hash matched)"
(`TASKS:343-344`) — migration language. Under D5 nothing is loaded; the artifact is the
**verified archive of what was discarded**, plus the pristine-destination record. The
P4-06/P4-07 authorization sentences should say so explicitly when they are eventually
written, so the gate checks the right thing for the branch actually taken. Proposing that
rewording is material for the Lead; it is not an acceptance.

**Optional harder variant (flagged, not proposed as decided work):** in-process
enforcement — the service itself refusing to start without a local archive marker file.
That is a product-code change on a protected surface, outside this lane and outside any
current authorization; if the owner wants it, it enters a future candidate and carries
D026 RED/GREEN obligations (`AGENTS.md:111-133`). The gate design above satisfies the
clause without it.

### 2.4 What the existing tooling already proves, and what it does not

Already demonstrated by the committed suite (so the archive's trust properties are not
aspirational):

- Risk/history invariants survive capture — daily-loss ledger, streak, realized PnL,
  open trade, live order all re-read from the manifest (`WALT:315-336`).
- WAL-resident rows are not lost — a capture against a hot WAL yields the complete
  trade count in a single self-contained file (`WALT:289-313`).
- The source is never mutated, and recorded sidecar state is arrival truth
  (`WALT:372-385`).
- Drift during capture fails closed with no half-trusted artifact left behind
  (`WALT:481-507`, `WALT:580-601`).
- Tampering with the bundle and re-signing the manifest is still caught by re-derived
  invariants (`WALT:771-792`); byte-level corruption by hash (`WALT:761-768`); manifest
  edits by the integrity hash (`WALT:751-758`).
- Verification demands the two externally recorded hashes and fails on mismatch
  (`WALT:811-826`, `WALT:829-849`).
- Sanitization is enforced, not promised (`WALT:339-346`, `WALT:362-369`).

Not covered by the tooling, covered by procedure instead (each is a design seam, named
so the Lead can attack it):

1. **Foreign-position evidence binding** (A4) is procedural — the tool cannot see the
   exchange. The seam is the ordered record; its falsification is below.
2. **The gate** (B1–B3) lives in owner sentences and the P4-07 checklist, not in code.
   Its strength is exactly the strength of the existing no-start-without-verified-
   artifact stop condition (`TASKS:346-348`).
3. **Retrievability over time** — `verify` proves the archive is readable and correct
   when run; nothing automatically re-runs it later. The storage class choice (Part 3)
   is what makes future re-verification possible at all.
4. **Hot-WAL crash state** can make capture impossible without new authority
   (`WAL:230-236`) — this is correct fail-closed behavior, but it means the archive
   step can block the cutover, which is the intended direction of the clause.

### 2.5 D026 falsification plan for the new bindings

The four bindings this design adds beyond the existing tested tool behavior, each with
the observation that would prove it false (DDP Pattern 10, `DDP:614-687`;
`AGENTS.md:111-133`):

| Binding | Falsification (must be shown to fail before it is trusted) |
|---|---|
| Archive absence blocks start | In the tabletop/gate rehearsal, present the P4-07 precheck with no archive record → the gate must stop; a start that proceeds is the defect. |
| Archive corruption blocks start | Present a truncated/re-signed archive → `verify` exit 2 (already RED-proven for the tool at `WALT:761-792`); the gate must treat exit ≠ 0 as blocking, not retry. |
| Wrong archive blocks start | Present a *different* period's bundle with its own valid hashes → the expected-hash comparison against the cutover record's A3 values must fail (`bundle_db_hash_not_expected` / `invariants_hash_not_expected`, `WAL:1012-1013,1039-1040`). |
| DB-vs-exchange cross-check | A bundle whose `live_orders > 0` against a raw empty-orders capture must be adjudicated FAIL at A4, not averaged away. |

Any future code that implements these (e.g., a gate script) owes a RED/GREEN
demonstration with commands and real output recorded; until then these walk-forward
bindings are rehearsal-level, and are labeled as such (`AGENTS.md:111-133`).

### 2.6 UNKNOWNs

- Whether a WAL-consistent bundle can be captured from the current old-host database at
  all (depends on unverified runtime state; `RR:369-370`).
- The paper period's actual row counts, dates, and streaks — this design specifies the
  *form* of the evidence; the *values* exist only after a real capture, and no figure is
  invented here.
- Whether the owner wants in-process enforcement (product code; separate decision).
- The P4-06/P4-07 rewording (§2.3, B-note) — an owner/Lead drafting decision.

---

## Part 3 — Recommendation: archive off-host, or leave on the old machine?

The open sub-question D5 itself created (`DEC:112-116`; `LIST:129-131`). The Lead's
current view: archive, because it is the only record of the paper period
(`DEC:114-115`). This lane's recommendation: **archive off-host**, for the reasons
below — recorded as material for the owner, who decides with one sentence either way.

**For archiving off-host:**

1. After the reset, the destination deliberately carries nothing
   (`DEC:100-101`); without an archive the old machine's disk becomes the *only* copy
   of the paper period — every trade, the loss ledgers, the order history.
2. The old machine is being demoted from writer precisely because its reliability is in
   question — the tabletop's own PC-off scenarios (PC-1/PC-2) exist because that host
   can lose power or die mid-procedure. A sole copy on the least-trusted machine is the
   weakest possible home for the only record (`TASKS:296-299` context).
3. The KVM2 programme's own recovery contract already requires evidence-class backups
   to be "encrypted off-host, versioned/retention-locked", with the write credential
   unable to delete versions (`SC:36-39`); archiving the pre-cutover state is the same
   discipline applied once, at the moment the data is most at risk.
4. Phase-11 teardown contemplates revoking and clearing the old world after evidence is
   secured — "deletion occurs before recovery and audit evidence is secured" is an
   explicit stop condition (`TASKS:855-856`); leaving the only copy in the path of that
   teardown inverts the intended order.
5. Cost is marginal: the tooling exists and is tested (§2.4); the incremental work is
   one capture, one verify, one copy — no new machinery.
6. The archive is sanitized by construction (hashes, counts, aggregates, timestamps,
   base names only; no paths, addresses, keys, or env values — `WAL:27-34`,
   `WALT:339-346`), so it travels without dragging secrets along. The two externally
   recorded hashes are tiny and belong in the owner's own record (`WAL:969-981`).

**For leaving it on the old machine (the honest counter-case):**

1. No new storage destination, no encryption-key custody, no off-PC key-recovery test —
   the recovery contract's own requirements for off-host backups are a real burden
   (`SC:36-39`), and doing them properly for one archival copy may exceed the owner's
   appetite tonight.
2. The sub-question is explicitly "not a blocker for the work that precedes cutover"
   (`DEC:116-117`) — deferring costs nothing on the critical path, and the machine is
   not scheduled for decommission on any date this lane found (**UNKNOWN**; no sourced
   teardown date exists in the documents read).
3. Fewer copies of economic history in fewer places is itself a property; even a
   sanitized archive is a full trade history.
4. If the old machine simply stays intact and offline, the data remains retrievable in
   principle — though "in principle" is exactly what `verify` with recorded hashes
   converts into "provably" (`WAL:969-1049`).

**Why archiving still wins:** the counter-case's strongest point (2) argues for
*deferring the decision about where*, not for *not capturing* — and the capture itself
(A2–A5) is already required by this design before the reset, at which point the marginal
cost of putting the verified bundle somewhere better than the machine being retired is
one copy operation. The asymmetry is total: archiving can be undone (delete the copy);
not archiving cannot be undone after the old machine goes.

**What would settle it:** one owner sentence, e.g. of the shape — "Archive the
pre-cutover risk-state bundle and raw cutover captures off-host, encrypted, before the
fresh start; the recorded bundle and invariants hashes live in the cutover record." —
or the explicit opposite. Proposed wording only; no authorization is implied or granted
here.

---

## Part 4 — Consequence for the work breakdown (no invented figures)

- **R39 remains `NO SOURCED ESTIMATE`.** This document supplies what R39's source row
  calls the frozen tabletop script (`WBS:78`); the row's own condition for pricing is a
  **timed** execution of that script plus evidence write-up, which has not happened. No
  hour figure is offered or implied by anything above.
- The Part 2 specification slots into R34's owner-approval surface (P3-01's
  adversarial staging-test spec, `WBS:73`; `TASKS:197-207`) and executes inside R42's
  cutover row (`WBS:81`; sourced 1.5–3 h host labour at `RR:339-339` — that figure is
  the sourced execution window only, not a price for this document's work).
- The off-host archive destination/provider choice, if accepted, belongs with the R38
  owner-choice cluster (`WBS:77`) and the R41 operations package ordering
  (`WBS:80,103-110`).
- Nothing in this document opens a gate, accepts an artifact, or authorizes a host,
  secret, service, cutover, start, ARM, merge-to-master, or economic action
  (`WBS:210-212`; `LIST:165-174`).
