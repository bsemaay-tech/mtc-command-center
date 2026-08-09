# Open questions for the Audit 2 dispatcher

These decisions remain with the dispatching Lead. This readiness assembly makes no audit
or acceptance decision.

## 1. GLM-5.2 supplemental detection or omission

Context: the checklist records an earlier four-auditor wording, while the newer owner
decision keeps Audit 2 two-flagship. DeepSeek V4 Flash is recorded as unavailable because
the ClinePass subscription is paused. The two flagship verdicts remain the acceptance floor.

Options:

1. Omit GLM-5.2 and run only the two owner-mandated flagship sessions.
2. Add GLM-5.2 as supplemental detection, without changing the acceptance floor or allowing
   an unexecuted suite to count as acceptance.

Recommendation: choose option 1 unless the owner explicitly adds supplemental GLM-5.2 at
dispatch. It follows the newer binding two-flagship directive and avoids silently reviving
the earlier roster wording.

## 2. How to keep the two flagship sessions independent

Options:

1. Use two separately created audit-only worktrees at the same full frozen SHA; issue each
   a fresh standalone prompt; seal both initial verdicts before sharing either output.
2. Use one shared worktree but separate fresh sessions.
3. Let the second auditor see the first verdict before reviewing.

Recommendation: option 1. Record the resolved worktree path, `git rev-parse HEAD`, and empty
`git status --porcelain` before and after each session. Do not use resume/continue or share
implementer context. Option 3 is not independent.

## 3. Missing mandated suite command and exact baseline

Context: the permitted inputs require a mandated command and baseline but do not provide
the command, exact counts, exact two failing test IDs, or accepted failure signatures.

Options:

1. Stop dispatch until an authoritative freeze-time source supplies and pins every field in
   `AUDIT2_AUDITOR_SESSION_INPUTS.md` section 5.
2. Let each auditor choose a plausible suite or infer the anomaly set.

Recommendation: option 1. Option 2 makes results incomparable and violates the rule that an
auditor unable to execute the mandated suite must return BLOCK.

## 4. Unlocated D026 RED demonstrations

Context: R4-5 has an exact RED/GREEN location. The B3 repair findings are described in the
closure record and candidate files are indexed, but the permitted inputs do not map each
named test to its RED command and real output.

Options:

1. Before dispatch, add a verified per-test map to exact file sections and commands, then
   require each auditor to reproduce RED and GREEN.
2. Leave the mappings absent and label every unlocated test supplemental, so none supports
   a closure claim.
3. Treat the presence of audit/self-QA files as sufficient.

Recommendation: option 1 if those tests are needed to support closure; otherwise option 2.
Option 3 is not D026 evidence.

## 5. Freeze-time ledger ratification

Context: the owner ratified a 29.5 h remaining baseline at WP-L P2 start. WP-L P2 booked
2.6 h and reports about 26.9 h remaining, explicitly subject to owner adjustment. WP-I has
not closed, so its final consumption is unknown.

Options:

1. After WP-I close, book its hours prospectively, produce one exact freeze-time source,
   and obtain owner ratification before dispatch.
2. Use the provisional 26.9 h figure as final.

Recommendation: option 1. It preserves the prospective-ledger rule and gives auditors one
reproducible source figure.

## 6. Freeze-time blocked registry and B3 chronology

Context: the draft checklist records original B3 as BLOCKED-UPSTREAM. The later unit closure
record preserves that original STOP as history and separately records repaired B3B PASS.
Other items remain open.

Options:

1. Produce a freeze-time registry that states both events in order: original B3 STOP,
   repaired B3B PASS, and the still-open RPD-VERIFY, C1, C2-A/B, C3, C4-A/B/C, C5, WP-I
   F3/F4, and `bridge.env` naming risk.
2. Copy the older checklist wording without the later B3B result.
3. Remove the original B3 STOP because B3B later passed.

Recommendation: option 1. It preserves chain of custody without softening or erasing either
the historical STOP or the current open items.

## 7. Access to create-once transport evidence at audit time

Context: the checklist requires recomputation from three create-once roots under
`C:\WPI_ARTIFACTS`. This assembly did not contact a host or read those roots.

Options:

1. At dispatch, hand each auditor an immutable, read-only evidence snapshot plus the exact
   root identity and recomputation instructions.
2. Grant separately authorized read-only access to the create-once roots.
3. Rely only on copied digest strings in repository documents.

Recommendation: option 1 where operationally possible, otherwise option 2 under explicit
authority. Option 3 does not satisfy the required recomputation.

## 8. Freeze identity and unchanged-bits statement

Options:

1. Generate both at freeze from the exact isolated checkpoint and attach the recomputation
   commands and outputs.
2. Reuse the current candidate identity without proving how it relates to the freeze SHA.

Recommendation: option 1. Record the full freeze SHA, candidate SHA, artifact/manifest
hashes, and either a verified unchanged statement or an exact diff before dispatch.
