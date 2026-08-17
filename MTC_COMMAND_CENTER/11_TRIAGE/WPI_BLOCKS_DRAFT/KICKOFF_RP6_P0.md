# KICKOFF — build the WP-I P0 preflight block (RP6-P0), design draft

Authorized private-repo test-infrastructure design work. **Build only — this block will
NOT be executed by this task and no host will be contacted.** WP-I has no host-contact
authority and no budget lift, so nothing here may be run against `GATEA-STAGING`; local
`bash -n` and local fixture runs in a temp directory are the only execution permitted.
Write ONLY into this directory. ASCII only. English only. No git mutation.

## What P0 is for

WP-I runs in two stages. P0 establishes the premises every later claim rests on: who the
process is, which tools exist, and whether the facilities the RO checks depend on are
actually reachable *from this login*. The RO stage is admissible only if P0 confirmed
those premises. Folding them together would let a run assert a result whose precondition
it never checked — which is precisely the failure that stopped the B3 block on first host
contact.

P0 is the most stable part of WP-I: whatever the RO scope is eventually cut to, the
preconditions are needed first. That is why it is being built before the authority lands.

## Inputs (read these, nothing else)

- This file.
- `../DESIGN_DEFECT_PATTERNS_2026-08-10.md` — **binding**. Ten patterns distilled from
  24 required findings. Your block must not instantiate any of them. Pattern 1 (an
  inability to evaluate must STOP, never FAIL) governs every arm you write.
- `../WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — sections 1, 2 and 8.1 give
  P0's identity, its preregistered inputs, and the readiness rows this block must
  implement. The expectation table is authoritative for reason strings.
- `../WPI_PREREG_DRAFT_ROUND1/WPI_CHECK_FEASIBILITY.tsv` — which checks are unprivileged.
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/RP1-B3.sh` — the accepted
  repaired block. Match its conventions: `set -Eeuo pipefail`, `LC_ALL=C` on every
  producer, an ERR trap that converts an unadjudicated command status into a reasoned
  STOP, no temp files, numeric identity only, local no-temp path classifiers.
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/07_RUNKIT_B/RP0-LIB.sh` and
  `RP0-BOOTSTRAP.sh` — the library and evidence bootstrap this block sources. Do not
  modify them; where a library helper is unsuitable, implement a local replacement and
  comment which helper you are deliberately not using and why.

## Deliverable — `RP6-P0.sh`, plus `DESIGN_NOTES_RP6.md` and `SELF_QA_RP6.md`

`RP6-P0.sh` must open with
`# ===== BLOCK-ID: RP6-P0 ===== [EXECUTABLE PROPOSAL BLOCK]` and carry the same rc
contract as the accepted blocks: **0 = PASS, 1 = FAIL (a probe ran and observed deviant
state), 3 = STOP (could not evaluate)**. It must implement, at minimum:

1. **Executing identity** — numeric uid and the full numeric gid list, recorded as
   evidence. No name-based comparison anywhere (Pattern 8).
2. **Tool inventory** — every tool the RO stage will invoke must resolve, at a pinned
   absolute path where the design requires one. A missing tool is a STOP naming the tool,
   never a silent skip and never a FAIL.
3. **System-manager readiness** — `systemctl` must not merely exist: it must execute,
   reach the intended system manager over its bus from this login's PID and mount
   namespace, pass authorization, and return a parseable response. Anything short of that
   is `P0_STOP reason=system_manager_unreachable`, because otherwise a denied bus later
   reads as "unit not active" (Pattern 1 + the WP-I audit's F3).
4. **Interpreter executability** — the venv interpreter must be provably executable by
   this login before any parity claim depends on running it; an exec denial is a STOP with
   its own reason, never a version or parity FAIL (the WP-I audit's F1).
5. **Namespace identity** — record this login's network, PID and mount namespace
   identities as evidence, so a later listener claim can be bound to the same namespace as
   the service rather than assumed (the WP-I audit's F2). P0 records; it does not
   adjudicate the binding.
6. **Evidence discipline** — allocate the evidence leaf through the accepted RP0
   bootstrap, create-once, and emit a terminal claim line stating exactly what P0
   establishes and what it does not.

Every probe must capture status and diagnostics and adjudicate them **before** any stdout
is interpreted (Pattern 6). No angle-bracket placeholder may remain in the delivered
script.

`SELF_QA_RP6.md` must record, for every arm, the exact executable command and its real
output from a local fixture run — literal commands, no recipes, no unfilled placeholders,
each block runnable as written after a stated prerequisite block. Report three separate
exact counts: arms actually driven, arms driven against stubs, and arms not driven.

## Hard constraints

- No host contact. No ssh, no scp, no network. No git mutation. Nothing outside this dir.
- Preregister and implement no mutating action of any kind.
- Do not implement Group C, and do not implement anything the feasibility table marks
  DEFER-ROOT-SIDE — name those in the design notes as out of scope for P0.
- This is a DRAFT block: it is not frozen, not hashed into any kit, and carries no
  authority to run.
