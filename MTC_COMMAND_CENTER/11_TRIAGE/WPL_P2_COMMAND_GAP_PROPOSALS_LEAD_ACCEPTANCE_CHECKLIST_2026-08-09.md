# WP-L P2 proposal repair — Lead acceptance and falsification checklist (2026-08-09)

## 0. Status and authority

This is a Lead-owned **future verification checklist**, not implementation and not acceptance. It may be
used only after a fresh Claude flagship implementer edits exactly
`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_2026-08-09.md` from the audited prompt.

Frozen authorities:

- candidate: `2ce41e34bceb599d80af24c5c33d835820ec321b`;
- accepted repair specification: `9ac60ac652f4a221316465cdbc24516aa391f5ce`;
- audited dispatch prompt checkpoint: `fbb5ca61a1a2bc368fd7b9bbf7f356d440e5bf20`;
- rejected proposal baseline: `779bd038957a192db47ff7ad68eb51304a2fba46`;
- required findings: F1-F9 in `WPL_P2_COMMAND_GAP_PROPOSALS_AUDIT_2026-08-09.md`.

No checklist item authorizes host/SSH, script transfer, service mutation, reboot, credentials, broker,
TESTNET, ARM/orders, WP-V/KVM2/master/old-payload, economic action, or `C:\PGRK` reopening. Any proposed
host command is inspected or falsified against local stubs/fixtures only.

## 1. Freeze and scope before content review

Record exact values, never aliases:

```text
implementation_base_sha : <HEAD before counterpart edit>
proposal_blob_before    : <git rev-parse HEAD:<proposal path>>
proposal_sha_after      : <frozen implementation commit>
proposal_blob_after     : <git rev-parse <sha>:<proposal path>>
candidate_sha           : 2ce41e34bceb599d80af24c5c33d835820ec321b
repair_round            : 1/3, 2/3, or 3/3
```

Required Lead checks:

1. `git status --short` before inspection shows no unrelated counterpart changes.
2. `git diff --name-status <implementation_base_sha> -- <frozen implementation commit>` names exactly
   the proposal document with status `M`.
3. `git diff --check <implementation_base_sha>..<frozen implementation commit>` passes.
4. No product/deploy/runtime/tool/test/schema/prompt/handoff/memory file changed in the implementation.
5. No hidden worktree/process is allowed to keep editing the frozen file during review.

Any scope failure is `BLOCK`; do not repair it by silently discarding another agent's work.

## 2. Candidate-anchor reproduction

Lead reads each exact candidate blob, not the live branch copy, and records line/symbol evidence for:

- `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py`: `collect_invariants(connection)`,
  `invariants_hash(invariants)`, verify/create public API, protected fields, DB/hash semantics;
- `IBKR_PAPER_BRIDGE/deploy/linux/common.sh`: any-write-bit `/222` predicate;
- `IBKR_PAPER_BRIDGE/deploy/linux/verify.sh`: exact `0555`, ownership, candidate/payload manifest binding,
  ancillary path requirements;
- `IBKR_PAPER_BRIDGE/deploy/linux/rollback.sh`: dry-run behavior, symlink guard, stop/mask operations,
  unconditional rollback-manifest creation, no-rebind field behavior;
- first-start systemd template: no `[Install]`, restart/timeout/final-signal settings and canonical unit
  path assumptions.

If any proposal claim depends on a source line outside these anchors, add that exact blob/line to the
frozen evidence package before adjudication. Drift or an unpinned assumption is `REQUEST_CHANGES`.

## 3. Shared RP0 evidence/predicate checks — F1 and F9

Static requirements:

- preregistered run ID and expected script/predicate hashes exist before remote allocation;
- operator-side transport captures exact argv, stdout, stderr, and rc from byte zero;
- canonical non-link parent owner/mode check precedes one-shot `mkdir -m 0700` without `-p`;
- redirect begins only inside the newly allocated root; each leaf is create-once/no-clobber;
- closed tree receives external remote/local hash binding;
- path, `pgrep`, `systemctl is-enabled`, and pipeline contracts have true/false/error outcomes; error STOPs.

Local falsification matrix (old proposal = RED; repaired helper/design = GREEN):

| Fixture | Required old result | Required repaired result |
|---|---|---|
| existing regular evidence leaf | demonstrates overwrite/follow risk | STOP before redirect |
| dangling evidence symlink | old existence guard bypasses | STOP as link |
| parent replaced by symlink | unsafe/undetected | STOP before allocation |
| denied path probe | may collapse to absent | STOP as unevaluable |
| synthetic `pgrep` rc 2 + empty output | may become no-process | STOP with rc recorded |
| synthetic `is-enabled` error + blank output | may become unmasked/token | STOP with rc/stdout recorded |

No fixture may touch `/home/gatea`; use a fresh local temporary root and command stubs. Preserve RED/GREEN
commands and outputs in the evidence package. Text claiming the fixtures exist is not D026 evidence.

## 4. RP1/B3 checks — F2

Require exact `0555 root:root` for release and venv roots, candidate `/222` semantics, explicit scan
scope/budget, candidate SHA plus payload-manifest SHA binding, exact ancillary checks, and fail-closed
`find`/`stat`/manifest/parser/tool handling.

RED/GREEN fixtures: root `0444`; child `0020`; child `0002`; wrong candidate SHA; wrong payload hash;
unreadable manifest; `find` that emits partial output then fails; ancillary path mode/owner drift. A test
that only checks the final stdout string, `returncode == 0`, or an unreachable exception branch is
supplemental, not closure evidence.

## 5. RP2/C1 and RP3/C2 checks — F3-F5

C1 must have no runnable stop block. It must separately name and leave open:

- exact candidate/locked-dependency `ExecMainCode`, `ExecMainStatus`, `Result` tuple;
- independently accepted safe active-writer protected-invariant baseline method.

The future-only C1 design must require strict elapsed `< timeout`, exact tuple, bounded journal, no
SIGKILL/timeout markers, zero writer/listener/cgroup with error adjudication, genuine pre/post protected
equality, `app_state != ARMED`, safe-copy integrity/FK checks, and no recovery start. Its deferred
falsification list becomes executable only after both gaps close. Any runnable `systemctl stop` while a
gap is open is `BLOCK`.

C2 must preserve two preregistered branches:

- A: exact active+unmasked+static pre-state, safe pre-reboot invariant baseline, terminal post-reboot
  inactive+static+unmasked equality; no implicit later C1 route;
- B: depends on RP2 baseline, separate stop and exact `/dev/null` mask mutations, post-stop/pre-reboot
  quiescent baseline, post-reboot inactive+masked equality; no start/unmask/recovery.

Required local predicate falsifications: failed/blank `is-enabled`; arbitrary/dangling/wrong-object mask
path; same-size DB mutation; wrong preregistered scenario. Reboot and service mutations remain unrun.

## 6. RP4/C3 checks — F6

Static/API requirements:

1. candidate bundle verify plus expected hashes occurs first;
2. restore root is fresh/no-clobber and success/failure artifacts are preserved;
3. source opens read-only as `sqlite3.Connection`;
4. exact restore primitive is `src_conn.backup(dst_conn)` into a fresh destination;
5. `quick_check` and `foreign_key_check` run on restored connection;
6. exact calls are `collect_invariants(restored_connection)` then candidate `invariants_hash(invariants)`;
7. restored hash/protected fields equal accepted bundle values;
8. source/bundle/restored device+inode pairs differ and bundle/restore sidecars are absent;
9. external manifest-file SHA is separately recorded.

Local RED/GREEN: old string/path argument reproduces `AttributeError`; wrong invariant; wrong DB hash;
pre-existing destination; dangling destination link; aliased inode; sidecar appearance; failed backup;
failed integrity/FK; partial-output preservation. Use temporary SQLite fixtures only. Prove at least one
same-size protected-value mutation is detected by invariants, not filename or size.

## 7. RP5/C4 and RP6/C5 checks — F7-F8 and authority floor

C4 prerequisites must be ordered and fail closed: accepted C3 manifest+external SHA; rollback-manifest
object/link absence immediately before use; steady unit absence; candidate rollback/state hashes;
preregistered start state; mutation-free candidate dry run; then one stop+mask-only invocation with no
rebind SHA arguments.

Require: inactive; exact `is-enabled=masked`; exact `/dev/null` link; zero writer/listener/cgroup with
error adjudication; newly created `0640 root:root` rollback manifest; every field validated including
empty no-rebind fields; fresh post-rollback bundle verifies and protected invariants equal the genuine
pre-rollback values. Filename/size is diagnostic only.

Local RED/GREEN with command/systemd stubs: pre-existing regular manifest; dangling manifest link;
dry-run mutation; same-size protected mutation; wrong state-manifest hash; wrong mask target; unexpected
rebind flag; failed post-rollback invariant equality. Do not run the real rollback script or `systemctl`.

C5 must contain only the authority statement. Any executable credential/network/broker/alternate-start/
TESTNET/ARM/order procedure is `BLOCK`.

## 8. Verdict and repair accounting

For each F1-F9 record one of: `CLOSED with reproduced evidence`, `OPEN`, or `UNREPRODUCED finding`.
Unexecuted claimed falsification is never `CLOSED`. Any open reproduced required finding yields
`REQUEST_CHANGES`; inability to safely execute a mandated local falsification yields `BLOCK`.

After Lead reproduction, freeze the one-file implementation commit and send only the scope contract,
actual diff/file, candidate anchors, local RED/GREEN outputs, and repo rules to fresh canonical auditors.
Acceptance still requires both flagship auditors plus no unresolved reproduced finding. A secondary
auditor's unexecuted PASS is supplemental. Maximum three repair/re-audit rounds; never enter round 4.

## 9. Next steps

1. Dispatch the audited Claude repair prompt when an exact account route has capacity.
2. Freeze the returned one-file diff before any second agent can touch it.
3. Execute this checklist locally without host actions and preserve RED/GREEN evidence.
4. If Lead finds a required defect, send one focused same-counterpart repair prompt and increment round.
5. If Lead accepts, start fresh protected-scope audits; no script extraction or host action follows
   automatically.
