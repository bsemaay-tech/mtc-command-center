# KICKOFF — B3-GAP-ENV repair round 3 (FINAL round)

Same implementer, same contract. Round 2 received REQUEST_CHANGES with a complete and
final repair list (audit contract: no new required items may be added in the next
audit beyond regressions you introduce). This is the LAST repair round — an
incomplete round 3 ends the cycle in BLOCK and escalates to the owner. Write the four
revised deliverables into `round3/` next to this file. ASCII only. English only. Do
not touch any file outside `round3/`.

## Inputs (read these, nothing else)

- This file; `audit2/AUDIT2_REPORT.md` (BINDING: findings A2-F1..A2-F8 and the
  "Final complete repair list for round 3", items 1-8); `ROUND2_KICKOFF.md`;
  `round2/` (your baseline); `../01_RUNKIT/RP0-LIB.sh` (context only).

## Required changes — exactly the audit's final list

1. **A2-F1**: pin the interpreter (`/usr/bin/python3 -I`), require it to exist at the
   pinned absolute path (STOP otherwise), scrub `PYTHONPATH`, `PYTHONHOME`,
   `PYTHONSTARTUP`, user-site and loader-injection variables via `env -i` with an
   explicit minimal environment for the child, set a safe cwd; add module-hijack
   RED/GREEN regressions (PYTHONPATH json.py shadow + cwd shadow).
2. **A2-F2**: replace the visible-PID-1 inference with preregistered deploy-channel
   attestation inputs: required env vars `RPD_EXPECT_NS_USER`, `RPD_EXPECT_NS_MNT`,
   `RPD_EXPECT_ROOTFS_ID` (format: the exact `readlink /proc/*/ns/*` token and a
   `stat -c '%d:%i' /` identity), guarded like the other preregistered inputs;
   compare self against them; never print `bound=initial` from local inference alone.
   Document in DESIGN_NOTES that the deploy channel mints these at provisioning time.
3. **A2-F3**: new required inputs `B3_SVC_UID`/`B3_SVC_GID` (numeric, guarded);
   STATE_DIR/LOG_DIR ownership compared numerically against them; names diagnostic
   only.
4. **A2-F4**: `parse_constant` callback that raises; NaN/Infinity/-Infinity fixtures
   RED/GREEN.
5. **A2-F5**: both mount readers process a populated final record on nonzero read,
   validate field count per record, STOP on malformed/truncated/read-error input;
   unterminated-record falsification test.
6. **A2-F6**: reject raw boundary diagnostics containing CR/LF or more than one error
   class BEFORE sanitizing; require exactly one C-locale diagnostic shape; ambiguous
   = STOP rc 3; two-line EACCES+ENOENT fixture must land STOP.
7. **A2-F7**: exact three-way QA counts (the audit computed 35 A / 90 B as the
   corrected split for round 2 — recount for round 3 honestly); every closure test
   for items 1-6 carries the exact command and real RED (round-2 code) and GREEN
   (round-3 code) output per D026.
8. **A2-F8**: deliver exactly four files; no hidden files or caches (the Lead will
   also scrub tool-generated caches after you finish — your obligation is not to
   create any).

Do not weaken anything that audit 2 verified CLOSED (its §1 table with RED/GREEN
evidence). DESIGN_NOTES gets a per-item "how addressed" section including the two new
preregistered-input families (namespace attestation, service uid/gid) and their
provenance contract.
