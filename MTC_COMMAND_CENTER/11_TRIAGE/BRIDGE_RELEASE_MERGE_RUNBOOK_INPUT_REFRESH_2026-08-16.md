# Bridge merge runbook — frozen-input refresh — 2026-08-16

Status: LEAD INPUT-REFRESH RECORD — supersedes ONLY the `W` row of the frozen
input table in `BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:31-37`. Every other
runbook byte, precondition, step, and stop rule stays exactly as written. The
runbook remains NOT executed and NOT authorized to execute.

## The drift and its identity

The runbook froze the repaired WP-I input as `W = 6c746b65411d5e646da407614f95f8a1174f3a5a`.
The current tip of `codex/bridge-suite-anomaly-repairs-20260815` is
`7d4e9a96e07b34a0c3d92315912d7818168b830b` — the **direct first child** of the
frozen commit. Its entire content is one added documentation file: the T1
cross-model audit verdict of the suite repairs themselves
(`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/BRIDGE_SUITE_ANOMALY_AUDIT_2026-08-15.md`,
373 insertions, no other path). It contains no product byte.

## Independent verification (not this record's own claim)

The read-only readiness lane verified, with fresh Git commands against the
snapshot (`BRIDGE_MERGE_READINESS_2026-08-16.md`, precondition table):

- `6c746b65` remains the direct first parent of `7d4e9a96`.
- The merge base against Gate-A is unchanged (`4d2228cf…`) for both values of W.
- The pinned `.gitattributes` blob OID is identical in G, old W, and current W.
- `git merge-tree B <W> G` produces a byte-identical output for both W values
  (SHA-256 `33bf43c964712e5d9aa163248104d70886ce47ba8d98fec35474b99ba4d9f942`),
  with markers confined to the two predicted WAL hunks.
- The three-way Bridge universe remains exactly 33 paths with the same
  classification (9 Gate-A-only, 1 WP-I-only, 2 changed-by-both, 21 WP-I-stale).

## The refresh

`W := 7d4e9a96e07b34a0c3d92315912d7818168b830b`, effective for any future
authorized execution of the runbook. Rationale: executing from the stale `W`
would strand the branch's own audit verdict outside the integration lineage;
the drift commit is documentation-only and every topology, fence, and
merge-shape check is invariant under the refresh, per the independent evidence
above.

If the branch tip moves again past `7d4e9a96`, this record is itself stale and
the runbook's drift-stop applies anew; a further dated refresh with fresh
independent verification is required. No standing "current tip is fine" rule is
created — the refresh names one exact OID.

## What this record does not do

It does not execute or authorize the merge, create the integration worktree or
branch, alter acceptance requirements (local matrix, two-flagship T0, fresh
candidate-bound A-0..A-9 for any integrated candidate), or touch any economic
or host gate. The one execution-time filesystem precondition MR1 could not
check read-only (`C:\BRIDGE_RELEASE_INTEGRATION_20260815` absent) remains to be
checked at execution time.
