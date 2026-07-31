# KVM2 master-plan repair — cycle 2, focused repair round 1

Use the required Claude Code counterpart in:

`C:\LAB\Tradingview_LAB_CLEAN`

Read and obey `AGENTS.md`. Preserve all unrelated dirty-worktree changes. Do not
run destructive Git commands, stage, commit, push, or touch runtime/VPS/code.

Edit only:

- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_MASTER_PLAN_MULTI_MODEL_AUDIT_PROMPT_2026-07-25.md`

The Codex lead independently found the following required repairs after the first
implementation pass. Fix all of them narrowly:

1. `KVM2-P0-04A` uses `Evidence (future execution):`; change it to the exact
   structural field `  - Evidence:` while preserving the future-execution meaning.

2. `KVM2-P5-03A` embeds `Evidence:` after prose. Give it a standalone exact
   `  - Evidence:` field. Every one of all 77 task blocks must match both exact
   line prefixes `  - Evidence:` and `  - Stop:`.

3. Master-plan source/canonical-file descriptions still say “71 task blocks” in
   two places. Change every stale task-count reference to 77 and verify there is
   no remaining `71 task` phrase.

4. P5-06 says its observation window starts at ARM authorization P5-05. Actual ARM
   execution is P5-05A. Change this dependency to final approved VPS ARM execution
   at P5-05A. Also require P5-05A pre-check evidence that the active service-unit
   hash equals the P5-03A frozen baseline.

5. Make the resource-control dependency explicit: P6-04 cannot execute until
   P6-03 controls are implemented and hashed. P6-05 must explicitly require
   P6-01, P6-02, P6-03, and P6-04 closed, including the P6-03/P6-04 dummy-workload
   test chain. Update the master authority-matrix row for admitting one lab service
   so it names P6-01 through P6-05 rather than skipping the controls/test.

6. P9-03 currently claims the optional service is installed and then removal is
   tested before P9-04 observes it, which can leave nothing to observe or imply a
   second unauthorized install. Make the lifecycle unambiguous: P9-03 performs the
   single bounded install/start and isolation proof; P9-04 performs the full
   observation and then tests disable/removal at the end before acceptance. Update
   task titles/evidence/stop conditions and the master Phase 9 summary if needed.
   No second install/start attempt is authorized.

7. Phase 9 P9-02 currently lets the same implementer produce and “audit” the
   optional-service manifest without the independent Gate 6 acceptance required
   for Phase 6 admission manifests. Require a fresh independent Gate 6 accepting
   verdict on the exact immutable P9-02 manifest before P9-02A owner admission.
   Gate 6 acceptance does not authorize install/start, network access, secrets, or
   any other action; those remain separate. Update the Phase 9 header, P9-02,
   P9-02A, and stop conditions consistently. Use the canonical exact-model roster
   in `AGENTS.md`; no fallback.

After edits:

- keep each plan file below 60,000 bytes;
- verify 77 unique task IDs, all with exact Evidence/Stop fields;
- verify crosswalk rows 1–10 exactly once;
- verify no full `KVM2-P...` ID in the master;
- compute fresh SHA-256 hashes for master and companion and update the audit
  prompt’s current immutable-input hashes;
- do not claim an audit verdict.

Return a concise validation summary.
