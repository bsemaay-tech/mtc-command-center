# B3-GAP-ENV Option 1 repair cycle — Lead closure record (2026-08-09 night)

Cycle: Claude Max implements ↔ Codex `gpt-5.6-sol` xhigh audits, ≤3 rounds (T0).
Outcome: **BLOCK at round 3 — cycle stopped per contract, no round 4 without owner
authorization.** All artifacts committed: rounds 1–3 (`a287bbf6`, `0a4e2a94`,
`dca3bbf3`), audits 1–3 (`853e5d23`, `00dcbe00`, this commit).

## What the cycle achieved (verified by independent auditor fixtures)

The repaired design is materially stronger than both the accepted original and every
intermediate round. Closed with RED/GREEN evidence across the cycle:

- Unprivileged scope honestly narrowed: env-file/manifest checks moved out of B3;
  EACCES boundary probe (visible=FAIL, ENOENT=FAIL as more-open-than-accepted,
  ambiguous/multi-line diagnostics=STOP).
- Root-side RPD-VERIFY: structural JSON binding via pinned isolated `/usr/bin/python3
  -I` under `env -i` (PYTHONPATH/cwd hijack fixtures refused), duplicate-key and
  non-JSON-constant rejection, oversize/encoding fail-closed; literal-path
  conf-dir assertion + mount-boundary predicate; numeric-only ownership (0:0 and
  preregistered service uid/gid); deploy-channel namespace/rootfs attestation inputs
  replacing local inference; no temp files anywhere; every sanitization step
  adjudicated under the 0/1/3 contract.

## The two surviving REQUIRED findings (audit 3)

1. **Mount-reader read-error arm** (`round3/RP1-B3.sh:430-462`,
   `RPD-VERIFY.sh:430-462`): an empty nonzero `read` (e.g. `Is a directory` on the
   mounts source) is classified as EOF → false no-mount PASS rc 0. Fix is mechanical:
   distinguish empty-nonzero-read-with-zero-records as STOP.
2. **QA documentation under D026** (`round3/SELF_QA.md`): several closure tests lack
   the exact executable RED/GREEN commands (outputs are present, commands described in
   prose); one subcount label wrong (9 vs 11). Documentation-only; the auditor's own
   independent reruns produced the missing evidence for the code paths themselves.

Neither survivor invalidates the closed items: audit 3's regression sweep confirms
every previously-closed item still holds in round 3.

## Consequences tonight

- The repaired blocks are NOT accepted; Stage 1B runkit re-freeze does NOT run.
- B3 remains blocked (now on cycle-BLOCK rather than the original gap).
- C1/C2/C3/C4/C5 unchanged (BLOCKED). R4-5 evidence unaffected (banked).

## OWNER DECISION NEEDED (plain language)

The B3 redesign went through three build-and-attack rounds. The attacker (a second
AI auditing adversarially) now confirms almost everything is fixed; exactly two small
issues remain — one tiny code fix and one bookkeeping fix in the test write-up. The
rulebook we froze says three rounds is the limit, so I stopped and am asking:

- **Option A (recommended): authorize ONE bounded extra round** limited strictly to
  the two named fixes + a closure audit on just those two. Roughly half an hour of
  delegated work; no host contact involved.
- **Option B: leave it blocked** and fold the two fixes into the next work package's
  cycle whenever you schedule it.

Default if you say nothing: it stays blocked (Option B) — nothing runs on the staging
machine either way without your separate go-ahead.

## AUTHORIZATION UPDATE — 2026-08-09 ~21:35 local

Barış authorized **Option A** in-session (direct answer to the Lead's question:
"Yes, run round 4"). Bounded round 4 dispatched to Claude Max per
`ROUND4_KICKOFF_PREPARED_NOT_DISPATCHED.md` (scope: exactly the two audit-3
survivors). On closure-audit PASS: Stage 1B runkit re-freeze proceeds. Host-execution
authorization is NOT included — running the repaired B3 against staging remains a
separate future owner decision.

## Round 4 audit → doc-only round 5 (standing-authority auto-continue)

Audit 4 (`audit4/AUDIT4_REPORT.md`) verdict BLOCK, but the split is decisive:

- **Finding 1 (CODE — mount read-error arm): CLOSED, independently verified.** Both
  blocks STOP rc 3 on the directory-source fixture; unterminated-record arm still
  STOPs; regression sweep confirms the executable diff is confined to the intended
  branch and no audit-3 CLOSED path was weakened. Round-4 script hashes recorded:
  `RP1-B3.sh 6f3ea022…`, `RPD-VERIFY.sh 3b9e78e8…`.
- **Finding 2 (DOCUMENTATION — D026 exact-command recording in `SELF_QA.md`):
  survives.** Several closure tests are recorded as parameterized recipes + value
  tables (`<FIX>`, `STUB_CASE=<CASE>`, dependence on prior `arm.sh` state) rather than
  literal exact commands. The auditor confirms these are reproducible but not
  "exact executable" per D026. This is a QA-writeup defect, not a code defect.

**Decision (Lead, under `STANDING_AUTONOMY_AUTHORITY_2026-08-09.md`): auto-continue with
a DOC-ONLY round 5, not owner escalation.** The standing grant explicitly makes the
round limit a quality cadence and directs auto-continuation on NARROW survivors
(mechanical fixes, QA/doc gaps); a survivor escalates to the owner only if it is
architectural or needs a hard gate. This survivor is neither — it is `SELF_QA.md`
prose. The AUDIT4 kickoff's "no round 5, escalate" line predates and is overridden by
the standing grant for this class of survivor. Round 5 scope is locked to
`SELF_QA.md` ONLY; `RP1-B3.sh`, `RPD-VERIFY.sh`, `DESIGN_NOTES.md` stay byte-identical
to round 4 (verified by hash after). If a round-5 re-audit still finds a REQUIRED
code defect (not doc), THAT escalates. Audit-4 nit 2 (over-broad mid-table wording)
folded into the same round.

## Round 5 audit → tight doc round 6 (last mechanical layer)

Audit 5 (`audit5/AUDIT5_REPORT.md`) BLOCK, but strictly narrower and converging:
**code freeze PASS** (all three non-QA files byte-identical, hashes match), **nit 2 +
arithmetic PASS**. Round 5 closed the command-level placeholders; the sole survivor is
the section-4 shared declaration block those commands source — `QA=<prose>` (not
runnable Bash), `B="<repo>/..."` (a repo-root placeholder the kickoff did not permit),
and the line-381 shared capture recipe. Every actual closure command still reproduces
correctly (the auditor independently re-ran five and confirmed). Under standing
authority this is the narrowest doc survivor and it is converging (round 4:
command-level placeholders → round 5: setup block only), so round 6 is authorized —
scoped to making the section-4 declaration block copy-paste runnable and nothing else.
**Convergence stop set: if audit 6 BLOCKs again on the same D026 exact-command class,
escalate to owner** — that would indicate the QA-authoring approach cannot satisfy
literal-D026 in this MSYS harness, a tooling-limit judgment that belongs to the owner,
not another auto-round. Code stays frozen at the round-4 hashes.
