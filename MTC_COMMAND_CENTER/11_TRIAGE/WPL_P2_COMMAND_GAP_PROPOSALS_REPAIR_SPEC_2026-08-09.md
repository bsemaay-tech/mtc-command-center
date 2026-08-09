# WP-L Phase 2 command-gap proposals — bounded repair specification (2026-08-09)

## 0. Status and authority

This is a **Lead-owned specification only**. It does not edit the rejected proposal, create runnable
scripts, contact the host, or authorize implementation/execution. It translates findings F1-F9 from
`WPL_P2_COMMAND_GAP_PROPOSALS_AUDIT_2026-08-09.md` into a bounded future repair contract.

- source proposal: commit `779bd038957a192db47ff7ad68eb51304a2fba46`
- candidate authority: `2ce41e34bceb599d80af24c5c33d835820ec321b`
- future writable scope: **only**
  `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md`
- forbidden: product/deploy/runtime/tool/test/schema edits; host/SSH; script transfer; Git history rewrite;
  credentials; broker/TESTNET; ARM/orders; WP-V/KVM2/master; economic action
- new repair cycle bound: maximum three repair/re-audit rounds for this proposal task
- separation rule: this task may not edit, supersede, or reopen the exhausted `C:\PGRK` design loop

## 1. Acceptance floor

The repaired proposal is accepted only if all of the following hold:

1. Every code block is internally executable against candidate APIs; no acknowledged assumption remains
   on a PASS path.
2. Every predicate has three outcomes: true, false, and **could not evaluate**. The third is always STOP.
3. No evidence destination can overwrite an object or follow a live/dangling link.
4. No mutating command follows a failed, missing, unrecorded, or unadjudicated prerequisite.
5. Every pre/post claim has a genuine pre-mutation baseline; no post-mutation value is relabelled as pre.
6. C1 remains explicitly BLOCKED until its two independent design gaps are closed; editing prose cannot
   convert them into execution readiness.
7. C5 remains BLOCKED and contains no executable credential/network/broker procedure.
8. The repaired one-file commit receives fresh read-only review from the protected-scope audit roster;
   Lead reproduces every required claim before acceptance.

## 2. RP0 — shared evidence and predicate bootstrap (closes F1 and shared part of F9)

### Required design

Replace the fixed `/home/gatea/*.log` pattern with a fresh evidence directory per run:

- operator preregisters `<RUNID>` and expected script/predicate hashes locally;
- operator-side transport captures exact remote argv, transport stdout, stderr, and rc from the first
  byte, so failures before remote evidence allocation remain evidenced;
- remote parent `/home/gatea` must be observed as a canonical non-link directory with preregistered
  owner/mode before allocation; probe failure is STOP;
- allocate `/home/gatea/runkit/<RUNID>` with one plain `mkdir -m 0700`, never `mkdir -p`; any rc other
  than zero is STOP and the run ID is never reused;
- only after successful allocation may the script redirect to a leaf inside that newly owned directory;
- every leaf is created once; no append, truncation of an existing path, rename-aside, or retry in place;
- hash the closed evidence tree externally after script exit and bind the remote/local hashes.

This is the proposed reusable bootstrap channel. It specifies a possible closure route for the
pre-`<EVROOT>` contradiction recorded for the separate `C:\PGRK` draft, but it does **not** close,
reopen, or repair that draft.

### Predicate-status contract

- `pgrep`: rc `0` = matches; rc `1` = none; every other rc = STOP.
- `systemctl is-enabled`: capture stdout and rc separately; a preregistered token may PASS only when the
  command status is one of the documented token-producing statuses. Blank/unparsable output is STOP.
- pipelines: `pipefail` plus the complete component-status vector; empty output is never sufficient.
- path probes: distinguish absent, existing non-link, link (live or dangling), and probe error. A probe
  error is never converted to absent/unmasked.
- every STOP is recorded by the active evidence channel and terminates the stage immediately.

### Required falsifications

Before any host use, demonstrate RED on the old proposal and GREEN on the repaired helper for:

1. existing regular evidence leaf;
2. dangling evidence symlink;
3. parent path replaced by a symlink;
4. denied/path-probe error;
5. `pgrep` synthetic rc `2` with empty output;
6. `systemctl is-enabled` synthetic non-token error with empty output.

## 3. RP1 — B3 bounded filesystem admission (closes F2)

The repaired B3 proposal must:

- require release and venv roots exactly `0555 root:root`; `0444` is a mismatch;
- use the candidate's any-write-bit semantics (`/222`), not owner-write-only `0200`;
- either bound the sweep explicitly or state and budget the exact full-tree sweep; it may not call an
  unbounded recursive scan "bounded";
- reproduce install-manifest binding to candidate SHA and payload-manifest SHA using count/silent reads
  that do not print unrelated manifest content;
- preserve exact mode/owner checks for state/log/config/env/install-manifest/unit paths;
- fail closed on every `find`, `stat`, manifest read, parser, permission, or tool error.

Required RED/GREEN fixtures: root mode `0444`; one group-writable-only child (`0020`); one
other-writable-only child (`0002`); wrong candidate SHA; wrong payload-manifest SHA; unreadable manifest;
and failed `find` after emitting partial output.

## 4. RP2 — C1 graceful stop remains BLOCKED (closes F3 only through prior gap closure)

No runnable C1 code block is permitted while either item below is unresolved:

### `C1-GAP-A` — exact successful shutdown tuple

Pin the candidate's uvicorn/systemd SIGTERM result from the exact locked dependency and systemd mapping.
Freeze the accepted `ExecMainCode`, `ExecMainStatus`, and `Result` tuple before a stop. `Result=success`
alone, elapsed time alone, or an observed post-hoc tuple cannot close this gap.

### `C1-GAP-B` — safe active-writer pre-stop baseline

Specify and independently accept an exact method that captures candidate `wal_state_bundle` protected
invariants while the service is active without using warning-class `--allow-live-source` as proof and
without mutating/locking the production DB unsafely. The baseline must exist before `systemctl stop`.

### Once both gaps close

The future command design must require:

- monotonic high-resolution elapsed time strictly below the timeout boundary;
- exact frozen exit tuple;
- bounded journal window with no timeout/SIGKILL/result-signal markers;
- zero writer, listener, and cgroup survivors with fail-closed tool statuses;
- a post-stop quiescent bundle whose protected invariants hash and fields equal the genuine pre-stop
  baseline; `app_state` never `ARMED`;
- integrity/FK checks on a safe copy, not the production database;
- no recovery start in C1.

No "partial PASS" exists while either gap is open.

## 5. RP3 — C2 reboot scenarios (closes F4-F5)

Keep two preregistered scenarios; never branch after reboot on the state observed.

### Scenario A — terminal plain reboot branch

- pre-reboot state must be active + unmasked with exact `is-enabled=static`, canonical fragment, and no
  mask-path object/link;
- capture an accepted pre-reboot protected-invariant baseline by a method independently proven safe;
- after reboot require inactive + exact `static`, no mask-path object/link, no writer/listener/cgroup,
  `app_state != ARMED`, and protected-invariant equality;
- this branch is terminal. Reaching C1 later requires separately authorized recovery start plus a fresh
  Stage-B admission; neither is part of C2-A.

### Scenario B — stop+mask then reboot

- its pre-stop persistence predicate depends on RP2's genuine pre-stop baseline method;
- stop and mask are separate named mutations; exact `/dev/null` mask link and `is-enabled=masked` required;
- capture the post-stop/pre-reboot quiescent invariant baseline;
- after reboot require inactive + masked, exact link target, no writer/listener/cgroup, and equality to
  the post-stop/pre-reboot baseline;
- no start/unmask/recovery action is included.

Required falsifications: failed `is-enabled`; blank token; arbitrary symlink target; dangling link;
unexpected regular file at mask path; same-size DB content mutation; and wrong preregistered scenario.

## 6. RP4 — C3 restore-into-temp wrapper (closes F6)

The proposal must use the candidate public API correctly:

1. Re-verify the accepted bundle with candidate `verify` and exact expected hashes.
2. Allocate a fresh no-clobber restore root; never delete it in an EXIT trap. Preserve success and failure
   artifacts under distinct labels; publish nothing accepted on failure.
3. Open the bundle DB read-only as `sqlite3.Connection`.
4. Restore into a fresh destination using SQLite's backup API; no file-copy masquerading as restore.
5. Run `quick_check` and `foreign_key_check` on the restored connection.
6. Call `collect_invariants(restored_connection)` and then candidate `invariants_hash(invariants)`;
   do not reimplement canonical JSON.
7. Require restored invariant hash and protected fields equal the accepted bundle values.
8. Require source, bundle, and restored DB device/inode pairs all distinct; require no `-wal`/`-shm`
   sidecars in bundle/restore roots.
9. Record external manifest-file SHA separately from embedded DB/invariant hashes.

Required RED/GREEN: old path argument raises the reproduced `AttributeError`; wrong invariant; wrong DB
hash; pre-existing destination; dangling destination link; aliased inode; sidecar appearance; failed
backup; failed integrity/FK; and partial-output preservation.

## 7. RP5 — C4 stop+mask rollback (closes F7-F8)

Prerequisites, in order:

1. accepted C3 bundle manifest file plus its externally recorded file SHA;
2. rollback manifest path proven absent as both object and link immediately before use;
3. steady unit absent; candidate rollback script and state manifest re-hashed;
4. preregistered starting state captured and matched;
5. candidate `rollback.sh --dry-run` rc `0`, expected dry-run stop/mask lines, no state/mask/process/listener
   change, no rollback manifest, and C3 evidence unchanged;
6. only then the single real stop+mask-only invocation, with no `--to-release-sha` or
   `--to-manifest-sha256`.

Postconditions:

- inactive + `is-enabled=masked` + exact `/dev/null` link;
- no writer/listener/cgroup survivors with fail-closed statuses;
- rollback manifest newly created, `0640 root:root`, and every expected field/value validated;
- a fresh post-rollback candidate bundle verifies and its protected invariants equal the preregistered
  pre-rollback values. Filename/size equality is diagnostic only and never called byte equality.

Required RED/GREEN: pre-existing regular rollback manifest; dangling manifest link; dry-run that mutates;
same-size protected DB mutation; wrong state-manifest hash; wrong mask target; unexpected rebind flag;
and failed post-rollback invariant equality.

## 8. RP6 — C5 remains blocked

Retain only the authority statement: current credential-free DISARMED runtime constructs no broker and
cannot emit meaningful broker egress. No command, credential name/value procedure, alternate start mode,
TESTNET endpoint, network allow rule, ARM request, or order action may be added in this repair cycle.

## 9. Implementation and audit sequence

1. Counterpart flagship edits the one proposal document only and self-checks every code block against
   exact candidate source.
2. Lead verifies diff scope, candidate anchors, shell status maps, and all local falsifications.
3. Fresh protected-scope auditors inspect the frozen commit. Non-execution is not acceptance.
4. Any reproduced required finding returns to the same counterpart, maximum three rounds.
5. Only an accepted design may later authorize extracting scripts into a separate implementation task.
6. Host authority, budget lift, and per-mutation authorization remain separate later gates.

## 10. Stop conditions

Stop immediately if a repair:

- edits product/deploy/runtime/tool/test/schema files;
- weakens a pre/post equality to presence, size, monotonic-only, warning, or "recorded";
- treats blank/error output as absence/unmasked/no-process;
- uses `|| true` without a candidate accumulator that is itself adjudicated;
- runs C1 while either gap remains open;
- deletes partial evidence or retries in place;
- introduces host access, credentials, broker/TESTNET, ARM/orders, WP-V/KVM2/master, or economic action;
- describes this proposal repair as acceptance of the separate blocked `C:\PGRK` design.

## 11. Next steps

1. **Default:** freeze this specification and audit it as a documentation contract.
2. After specification acceptance, obtain/confirm a new bounded proposal-repair cycle and dispatch the
   one-file edit to the counterpart flagship.
3. Keep C1/C2 mutating designs blocked until their baseline and exit-contract prerequisites close.
4. Update all three continuity files before any implementation unit begins.
