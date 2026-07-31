# KVM2 repair cycle 2 — final repair round 3, Stage A

Work in `C:\LAB\Tradingview_LAB_CLEAN`. Read and obey `AGENTS.md`. Preserve all
unrelated dirty-worktree changes. Do not run Git mutations or access any VPS,
runtime, broker, exchange, secret, or network system.

Edit only:

`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`

The fresh `claude-opus-5` xhigh round-7 Gate 5 + Gate 6 re-audit returned
`REQUEST_CHANGES`. This is repair round 3 of 3. Apply all six required repairs
below. Do not implement optional findings.

1. **Gate live Phase-6 control changes**
   - Add `KVM2-P6-00A [AI: Barış]` before P6-01.
   - It cites the accepted P5-10 design hash, names executor, authorizes exactly
     one bounded Phase-6 control implementation campaign limited to P6-01 and
     P6-03, and confirms the separate network/security gate is closed.
   - Any failed substep halts the campaign; retry requires a new P6-00A.
   - P6-01 must record bridge PID, unit hash, loopback listener, restart count,
     reconciliation freshness, and exchange connectivity before and after,
     unchanged. Regression invokes P5-10(e) rollback and halts Phase 6.

2. **Authorize Windows-writer quiesce**
   - Add `KVM2-P4-04A [AI: Barış]` before P4-05.
   - Require a distinct owner sentence and exactly one bounded Windows-writer
     quiesce: DISARM; natural flat or an explicitly authorized instrument-scoped
     flatten action with attempt count; raw exchange-side positions/orders flat
     proof; single writer preserved; no VPS start.
   - Stop if flat is not achieved, more than one attempt occurs, flatten lacks
     explicit authorization, or a second writer appears.
   - P4-05 requires P4-04A closed.

3. **Fix P2-10 dependency order**
   - Make P2-10 contract-definition only; it must not claim an executed reboot
     drill before the immutable candidate exists.
   - Add `KVM2-P4-07A [AI: Barış]` after P4-07 and before later ARM steps:
     separate owner sentence, exactly one bounded maintenance/reboot drill on
     KVM2 while DISARMED, using the exact installed candidate; hashed pre/post
     package manifests and unit hashes; restart DISARMED; reconcile proof; no
     automatic ARM.
   - P5-05A and P5-06 require P4-07A closed. Remove any impossible Phase-2
     executed-drill requirement.

4. **Freeze raw-metric sampling/retention**
   - P5-04 defines raw metric sampling interval, raw-series retention covering
     the full window, and storage location class sufficient for P5-08
     percentiles.
   - P5-06 retains and hash-records samples at that interval for the whole
     window. Deviation in sampling or retention is a Stop.
   - P5-08 cites the retained raw series.

5. **Resolve P6-03 define/implement ambiguity**
   - Title and text must explicitly define **and implement** the resource
     controls under P6-00A.
   - Record SHA-256 for slice/cgroup/kill-switch unit files.
   - Require the same pre/post unchanged bridge assertions and rollback trigger
     as P6-01.
   - P6-04 prerequisite must use the same implemented-and-hashed wording.

6. **Restore canonical crosswalk item 10**
   - Crosswalk row 10 must include separate P4-01 install/deploy
     authorization.
   - State that the monitoring counter starts only at P5-05A ARM execution,
     never at install, deploy, cutover, or first DISARMED start.

Hard constraints:

- The final companion remains below 60,000 bytes. It currently has little
  headroom; compress redundant explanatory prose and table wording only. Never
  weaken authority, safety, dependency, evidence, or Stop semantics.
- Expected final task count is 84 after adding P4-04A, P4-07A, and P6-00A.
- All 84 IDs must be unique and match
  `KVM2-P<phase>-<number><optional-letter>`.
- Every task has exactly one line beginning `  - Evidence:` and one beginning
  `  - Stop:`.
- Crosswalk rows 1–10 appear exactly once.
- Keep preparation-only status. Do not update the master/audit prompt or claim
  an audit verdict in Stage A.

Return concise validation: changed IDs, 84/84 structure, crosswalk, bytes, hash.
