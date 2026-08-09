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
