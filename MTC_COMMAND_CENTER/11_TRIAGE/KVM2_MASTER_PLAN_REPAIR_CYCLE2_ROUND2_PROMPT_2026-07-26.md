# KVM2 master-plan repair — cycle 2, focused repair round 2

Use the required Claude Code counterpart in:

`C:\LAB\Tradingview_LAB_CLEAN`

Read and obey `AGENTS.md`. Preserve every unrelated dirty-worktree change. Do
not run destructive Git commands, stage, commit, push, touch runtime/VPS/code,
access a broker/exchange, or perform network/deployment actions.

Edit only:

- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_MASTER_PLAN_MULTI_MODEL_AUDIT_PROMPT_2026-07-25.md`

The fresh independent `claude-opus-5` xhigh Gate 5 + Gate 6 audit of the exact
round-5 hashes returned `REQUEST_CHANGES`. Apply these nine required repairs
narrowly. Do not implement its optional findings in this round.

1. **Mechanical TESTNET interlock**
   - Add explicit proof that `HL_LIVE_ACK` is absent from the systemd unit,
     `EnvironmentFile`, and running process environment to P4-03, P4-07,
     P4-08B, and P5-05A.
   - Presence in any form is a Stop condition.
   - Restore this requirement to canonical crosswalk item 4.
   - Evidence must never print or persist unrelated environment secrets.

2. **ARMED crash/recovery authority**
   - Add one owner-controlled task before the P5-06 counter can start that
     freezes a bounded post-crash recovery procedure for an ARMED TESTNET
     window: named authorizer/executor, one attempt per explicit authorization,
     restart DISARMED, raw exchange reconcile before any re-ARM decision,
     open-position/order handling, and P5-04 window reclassification.
   - Require a hashed injected-crash staging drill proving the sequence.
   - P5-05A and P5-06 must require this task closed.
   - Require the P2-10 maintenance/reboot/update contract applied and verified
     on KVM2 before the P5-06 counter starts.
   - No automatic re-ARM or retry is authorized.

3. **Phase 8 owner and network gate**
   - Make Phase 8 preparation/design produce an immutable manifest before any
     build/start.
   - Add a distinct `[AI: Barış]` owner admission task citing that manifest
     hash before P8-02 can execute.
   - Any new listener, firewall/private-network/public-access change requires a
     separate fresh network/security gate and owner acceptance.
   - The builder cannot self-authorize or self-close the admission gate.
   - Avoid a circular dependency: design/manifest first, owner/network gate
     second, bounded build/start third, independent proof last.

4. **Destructive reprovision and purchase authorization**
   - Separate preparation-only evidence from execution evidence for both
     Option A and Option B.
   - Preparation tasks may create only manifests/checklists and must not claim
     post-wipe, first-boot, purchase, or new-host facts.
   - Add distinct `[AI: Barış]` gates that name the exact destructive target or
     commercial decision, cite recovery proof and immutable manifest, authorize
     exactly one bounded action, and identify the executor.
   - Post-action evidence may appear only after that owner gate.
   - Update master authority rows so the named owner tasks are the required
     gates. Selecting Option A/B never authorizes wipe or purchase by itself.

5. **Canonical operations evidence / log rotation**
   - Add a bounded persistent-log rotation, retention, and compression policy
     plus config hash to P2-04.
   - Require a forced-rotation test before first start in P4-07.
   - Expand crosswalk item 8 to retain every canonical close requirement:
     release/baseline manifest, rollback SHA and tested rollback, systemd-unit
     hash, encrypted backup plus restore check, rotated persistent logs, and
     monitoring/heartbeat, with the real closing tasks cited.

6. **Final exchange-side cutover proof**
   - In P4-05 and crosswalk item 6, replace the ambiguous local/VPS empty-state
     reconfirmation with a second timestamped raw exchange-side positions and
     orders query executed from the VPS after old-host authority revocation.
   - Capture the two raw responses bracketing revocation without secrets.

7. **Master/companion precedence wording**
   - Replace the false claim that no task ID appears in the master.
   - State that no task *definition* appears there; shorthand task references
     are cross-references only.
   - The execution companion governs task text. Any master/companion
     cross-reference conflict is a BLOCK until reconciled.
   - Preserve the rule that no full `KVM2-P...` ID appears in the master.

8. **Carry-forward requirements**
   - P2-12 and P3-05 must disclose and explicitly accept P2-09's exact verdict
     (`VERIFIED` or `BLOCKED/UNVERIFIED`).
   - Assign raw restricted-evidence retention and deletion policy to P0-04,
     including owner, duration, deletion trigger, and Stop condition, before
     Phase 1 begins.

9. **Shared-namespace isolation vectors**
   - Add shared `/tmp` and `/dev/shm`, journald access through
     `systemd-journal`/`adm`, abstract AF_UNIX sockets, and kernel keyrings to
     Invariant 7 and P5-10(c).
   - Require `PrivateTmp=yes` where appropriate for bridge and lab units.
   - Add matching P6-01 negative tests and P6-02 denial assertions.
   - Evidence must prove the lab identity cannot read bridge journals, reach a
     bridge abstract socket, or share the bridge temporary namespace.

Structural constraints after the repair:

- Keep both plan files below 60,000 bytes. The companion is already close to
  the limit. Tighten redundant prose inside the three-file whitelist without
  weakening any authority, safety, evidence, or Stop gate. If this cannot be
  done safely, stop and report the blocker instead of deleting protections.
- Recompute the actual task-definition count after any added/split tasks.
- Every task definition must have one exact `  - Evidence:` line and one exact
  `  - Stop:` line; task IDs must be unique.
- Update every master/companion/audit-prompt task-count reference to the actual
  count.
- Keep canonical crosswalk rows 1–10 exactly once.
- Keep zero full `KVM2-P...` IDs in the master.
- Preserve preparation-only status and all authorization separations.
- Compute fresh SHA-256 hashes for master and companion and update the audit
  prompt's current immutable-input hashes. Move prior current hashes to clearly
  superseded entries.
- Do not claim an audit verdict.

Return a concise validation summary listing changed task IDs, final task count,
structural checks, sizes, and fresh hashes.
