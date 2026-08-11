# MORNING HANDOFF — 2026-08-11, covering the night of 2026-08-10

Written by the overnight Lead session. Live document — updated as the night continues.
Last update: ~22:20 local.

---

## 1. FOR BARIŞ — plain language, three minutes

**Nothing was touched on the rented test machine.** All work stayed on this computer. No
credentials, no orders, no merges to master.

**One decision is waiting for you, and it is all nine or none.** There are nine checks nobody
has built. They would look at how the machine's own start-up manager runs our program:
whether it is running, whether it was restarted, whether it was started from exactly the copy
we approved, and whether its safety settings are switched on.

The finished analysis recommends **building all nine**, and explains why a cheap subset does
not work: one of them is the only check that ties the *running* program to the copy we
approved. Without it we would know the right files are on the disk, and that something is
answering — but not that they are the same thing. Two others are the only proof that the
safety settings and start-up mode actually do anything rather than just being written in a
template.

**Honest price: three to six more build-and-check rounds, most likely four.** That is on top
of two files that have not yet been accepted even once.

Why it cannot wait: **the test machine is wiped after the next stage, and some of these facts
can never be checked afterwards.** After the next authorized restart, two of them become
unobservable forever.

Full analysis, ending in a page written for you:
`WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md`.

> **Correction, 01:45.** An earlier version of this handoff said the recommendation was to
> build five cheap rows and defer four. That came from a partial copy of the analysis this
> session committed before the writer had finished. The finished analysis reaches the
> opposite conclusion — the decision is binary — and it is the one above.

**A second thing you should know.** Another agent session was working in this repository at
the same time as this one, on the transport files. Nothing was lost — this session detected
it, stopped touching those files, and wrote down the evidence. But if you only meant one
session to run overnight, that is worth sorting out.

**The honest state:** the work is going well and slowly, in that order. Every round finds
real defects, which is the system doing its job. Nothing is close to being frozen or run.

---

## 2. Account state at the end of the night

| Account | State | Next window |
|---|---|---|
| Codex Pro (`free`) | worked all night, the main lane | open |
| Codex Plus (`fourth`) | second lane | open |
| Claude Pro | spent on RP7 round 5 | 01:40, then ~06:40 |
| GLM-5.2 | spent on RP6-P0 round 7 | 02:11, then ~07:11 |
| Claude Max | **not used at all** | reserved |

Max was deliberately not spent. The one moment it qualified under the emergency policy —
Codex unable to finish an RP7 review — it would have bought a *same-family* second opinion,
which is worth less than the independence the two-flagship contract exists to provide.
Reasoning recorded in `ROUTING_CONSTRAINT_CODEX_CANNOT_AUDIT_RP7_2026-08-10.md`.

---

## 2b. STATE AS OF ~10:15 on 2026-08-11 — supersedes §3 below where they differ

**A four-hour gap, stated plainly.** Work stopped at 04:32 and resumed at 08:49 when the
owner wrote. Wake-up timers had been armed only to 02:12; after the last round the Lead
ended a turn with nothing scheduled, so nothing woke it. Both lanes had reset at 06:40 and
07:12 and sat idle. That is a planning error, not an account limit.

| Artifact | State now | Next |
|---|---|---|
| **RP7** | round **8** delivered, `11621044…4141a4`, 99903 B. All four round-7 findings repaired, including the weakened assertion **and** the false justification corrected in place | Lead verification running; then Codex part-B round-9 review |
| **RP6-P0** | round **9b** committed, `08e0a935…`, 104683 B; Codex grammar-band review returned **REQUEST_CHANGES ×4**; round-10 kickoff written | GLM returns 13:50 |
| **Transport** | assessed: round 4 is **~a fifth done and non-operational** | needs a lane after RP6/RP7 |
| **Prover** | unsound, repair banked, untouched | after the blocks |

**Account windows:** Claude Pro spent on RP7 round 8 (next window ~13:50). GLM exhausted at
09:46, returns **13:50**. Both Codex lanes open. **Claude Max still untouched.**

### What the reviews caught since the handoff was first written

- RP7 round 7 **weakened a regression test** — changed an assertion pinning rc 0 to one
  accepting any status — and justified it with a statement about the old test that was
  false. The reviewer verified the claim instead of believing it. Round 8 repaired both the
  test and the report.
- RP6's `R9_GRAMMAR` **published command never ran the harness**: a filename after
  `bash --noprofile --norc` makes Bash run that file and ignore piped stdin. The Lead had
  reported that fence green by extracting the body a different way — true, and insufficient.
  **Lead practice corrected: run the published command verbatim as well, and treat any
  disagreement between the two as a finding.**
- RP6's round-9b relabelling sits on an **unreachable line**.
- Transport's close script requires a third argument **no plan byte passes**, and its clean
  launch self-STOPs, so its new STOP path is unreachable.

That is five instances in two days of one disease: **evidence that looks conclusive and
establishes nothing.**

## 3. Per-artifact state

### RP7-WPI-RO.sh — round 5 committed, round 6 scoped and ready

- Round-4 bytes reviewed by Codex → **BLOCK: 3**. The headline: `python3` was accepted,
  projected, required and documented, but the production `wpi_main` loop bound only nine
  tools — so the program producing both accepting claims was never verified. The Lead
  reproduced that independently before making it binding scope.
- **Round 5 (Claude Pro) closed all five items**; Lead verified the RED→GREEN flip itself.
  Bytes `393a16ce…b0ee`, 77179 B, commit `1143a9ff`.
- Independent delta review: `+93/-7` exactly, no unexplained hunks, **no weakened checks**.
- Codex review of round 5, band B (rows 20–24 + evidence) → **BLOCK: 4**. Two HIGH: a
  malformed listener record is silently normalised into a PASS; truncated status-parser
  records become FAILs instead of STOPs. Plus: the published QA command **returns 0 even when
  both fences fail**.
- Round-6 kickoff written: `KICKOFF_RP7_REPAIR_R6.md`. **Fire at 01:40 on Claude Pro.**

### RP6-P0.sh — round 7 committed as a draft round, round 8 ready

- Round-6 bytes reviewed by Codex → REQUEST_CHANGES ×5. Round 7 (GLM) closed corrections
  1–3 with genuine RED/GREEN, verified by the Lead running every harness.
- Bytes `fa852d7e…83cd`, 103071 B, commit `d9d7420f`.
- **Not a clean round.** Two legacy fences exit rc 1 because their synthesised arms
  `sed`-slice the block and no longer define the ten new frozen constants round 7 added.
  Correction 5 is therefore half closed — markers migrated, but the fences still line-slice.
- One unclassified token change in the non-executable-tool path is explicit re-audit scope.
- Round-8 kickoff written: `KICKOFF_RP6_REPAIR_R8.md`, evidence-only, block frozen
  byte-identical. **Fire at 02:11 on GLM.**

### Transport set — owned by the other session

This session dropped it after detecting concurrent edits. See
`CONCURRENT_SESSION_NOTICE_2026-08-10_2130.md`. Four items this session had added to its
kickoff (`T5`–`T8`) are recorded there and still stand whoever picks them up — most
importantly that `run_p0.sh` wires **none** of the five `P0_ATTESTED_*` inputs RP6 requires,
so the composition would STOP before any host observation even with every literal filled.

### §10.2 path-scope prover — unsound, repair banked

- Codex T1 → **REQUEST_CHANGES: 9**, four CRITICAL. Complete Bash fragments reach filesystem
  and network primitives while it prints nothing and returns `PASS rc=0`.
- Repair kickoff banked: `KICKOFF_PATHSCOPE_REPAIR_R2.md`.
- Separately, a design note established that **even a repaired prover cannot close either
  block alone** — the paths come from wrapper + RP0-LIB + RP0-BOOTSTRAP + block together.
  Recommendation: one entrypoint-driven whole-program proof per stage, with an
  allocate → render → freeze order. `SEC102_COMPOSITE_DESIGN_CODEX_2026-08-10.md`.

---

## 4. Freeze blocker map

Nothing here was known yesterday morning. All of it must close before Stage-1 freeze.

1. Both flagships accept RP6-P0, RP7 and the transport set — **all three still open**.
2. **§8.2 rows 1–9 implemented by no executable — owner decision.** (§1 above.)
3. The §10.2 prover is unsound — repair banked.
4. §10.2 needs a composite whole-program proof, not a per-block one — design accepted.
5. §10.1 needs 11 extensions plus an access-qualifier grammar; 3 families unresolved.
6. The attestation / preregistration / commit order is circular — two-commit fix drafted.
7. `run_p0.sh` wires none of the five `P0_ATTESTED_*` inputs.
8. The close-script's preregistered contract and its actual bytes disagree.
9. `REMOTE_BASE` must be allocated **before** the RO block is frozen — and the composite
   design independently reached the same ordering conclusion.
10. The Audit-2 readiness package is an obsolete assembly aid (NEEDS-UPDATE: 20).

---

## 5. Ledger

24.9 h remains the last ratified balance. ~4.4 h was booked for 2026-08-10 daytime and is
**still unratified**. Tonight's hours are booked on top and are also unratified. The Lead has
not treated any of it as approved.

---

## 6. Recommended next steps

1. **Answer the rows 1–9 question** (§1). It gates the freeze and it is the only thing here
   that cannot be decided without you.
2. Confirm whether two agent sessions should be running at once, and which owns transport.
3. Ratify or adjust the time ledger.
4. Let the queue run: RP7 round 6 → re-review; RP6 round 8 → re-review; prover round 2.
5. Only after all three artifacts are accepted: preregistration freeze, then the host run.
