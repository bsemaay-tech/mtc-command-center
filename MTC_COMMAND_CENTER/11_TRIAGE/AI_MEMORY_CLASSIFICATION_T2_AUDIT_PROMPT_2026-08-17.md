# AI-memory classification — normal T2 audit prompt

**Date:** 2026-08-17
**Artifact class:** T3 dispatch-only prompt. Creating this file does not launch
or consume the review.

```text
ROLE AND AUDIT CONTRACT

Perform the one normal T2 documentation/evidence review of the exact current
working-copy classification reports below. Use one fresh independent reviewer,
medium effort: GLM-5.2 is preferred under AGENTS.md; DeepSeek is acceptable.
Do not use multiple reviewers or a continued/implementer session. This is the
single T2 round. A failed or incomplete reviewer run is not acceptance and does
not authorize a silent retry.

EXACT CANDIDATE PATHS

1. MTC_COMMAND_CENTER/11_TRIAGE/AI_MEMORY_FILE_CLASSIFICATION_BATCH1_2026-08-17.md
2. MTC_COMMAND_CENTER/11_TRIAGE/AI_MEMORY_FILE_CLASSIFICATION_BATCH2_2026-08-17.md

Both are current untracked working-copy candidates. Review those exact bytes;
do not substitute HEAD, a temp copy, summary, prior report or memory.

REQUIRED AUTHORITIES AND BOUNDARIES

- AGENTS.md
- MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md
- MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md
- The current files under MTC_COMMAND_CENTER/_AI_MEMORY, including ignored and
  hidden MTC_COMMAND_CENTER/_AI_MEMORY/.impeccable/hook.cache.json
- Targeted incoming references under AGENTS.md, MTC_COMMAND_CENTER and
  IBKR_PAPER_BRIDGE where needed to reproduce classifications/dependencies
- MTC_COMMAND_CENTER/11_TRIAGE/AI_MEMORY_ROTATION_GATE1_2026-08-17.md and
  AI_MEMORY_ROTATION_T2_STATUS_2026-08-17.md only to verify the rotation boundary

SCOPE TO REPRODUCE INDEPENDENTLY

1. Enumerate the current _AI_MEMORY filesystem independently. Include hidden
   and ignored files, especially `.impeccable/hook.cache.json`; do not rely on
   `git ls-files` alone.
2. Prove or disprove the set equation: 62 total files = 43 Batch-1 substantive
   classifications + 19 Batch-2 classifications, with missing 0, duplicate 0
   and every current path classified exactly once.
3. Independently reproduce the reported aggregate inventory:
   - total: 62 files, 1,289,332 bytes, 16,124 physical lines;
   - Batch 1: 43 files, 773,240 bytes, 8,721 lines;
   - Batch 2: 19 files, 516,092 bytes, 7,403 lines.
   State the exact line-count convention used. If concurrent working-copy drift
   changes a result, report the observed identity and discrepancy; do not edit
   a report to make it match.
4. Reconcile every row/path and verdict. Verify the combined verdict counts and
   that KEEP, HOLD, ROTATE-CANDIDATE and ARCHIVE-CANDIDATE are used consistently.
   In particular, ARCHIVE-CANDIDATE never means delete or summarize.
5. Reproduce the material factual/dependency claims behind the verdicts using
   targeted source checks: current authority links; stale counts/role wording;
   retired SESSION_LOG/ACTIVE_FILES instructions; incoming references; generated
   indexes; June historical cohorts; and the ignored cache's non-authority role.
6. Verify current active-lock truth and boundaries from SESSION_LOCK.md. The
   reports must not authorize moving a file with active ownership, and must keep
   the stable live lock protocol/current table in place.
7. Verify the dependency-preserving no-loss order:
   - separately accept or reject the six-file rotation;
   - repair current memory authorities before retiring ACTIVE_FILES dependencies;
   - rotate ACTIVE_FILES losslessly only after semantic reconciliation;
   - refresh generated indexes from their real sources;
   - archive June cohorts verbatim with manifests, hashes and link repair;
   - consider closed SESSION_LOCK history only after quiescence.
8. Verify that decisions, provenance, gates, rejected findings, unresolved work,
   identities, hashes, commands and evidence links are never deleted, silently
   summarized, deduplicated or treated as closed merely because they are moved.

SEPARATE SIX-FILE ROTATION BOUNDARY

This audit reviews only the two classification reports. It does not review,
accept, reject, repair, commit or authorize the separate six-file lossless
rotation. Batch 2 must classify those six current files as HOLD pending their
own governed review/decision. Reproducing rotation hashes as classification
context is not acceptance of the rotation itself.

PRE/POST IDENTITY AND CLEANLINESS PROOF

Before reading substantively:

- record `git status --short` for both candidate paths;
- record SHA-256 and byte/physical-line counts for both candidates;
- record a full-repository `git status --short` snapshot;
- record the current SESSION_LOCK rows relevant to AI-memory work without
  modifying or claiming them.

After review, repeat the same scoped status, candidate hashes/counts and full
status snapshot. Candidate before/after hashes must be identical. Explain any
unrelated concurrent status drift; do not repair, revert or absorb it. Also
state explicitly whether your run created or changed any path.

PROHIBITED ACTIONS

Read-only review only. Do not edit, create, delete, rename, move, archive,
compact, regenerate, stage or commit any file. Do not checkout, reset or stash.
Do not claim/release locks, change AI-memory, execute a proposed repair/package,
contact hosts, read credentials/secrets, deploy, run trading or strategy
compute, touch docs/30, Bridge/dashboard code, or Help/Wiki work. Do not treat a
classification verdict as authorization to carry it out.

REQUIRED FORMAL OUTPUT

Return a concise audit report containing:

1. reviewer model/route, freshness and medium-effort evidence;
2. exact candidate paths plus pre/post status, hash, byte and line proof;
3. the independently enumerated 62=43+19 set reconciliation, listing every
   missing, duplicate or extra path if the equation fails;
4. reproduced aggregate counts and any discrepancy;
5. findings on classifications, dependencies, no-loss order, active locks and
   the separate-rotation boundary;
6. required findings separated from optional nits;
7. exactly one verdict:
   - PASS: no required changes.
   - PASS-WITH-NITS: accepting; optional nits only, zero required repair.
   - REQUEST_CHANGES: one or more required repairs; this prompt authorizes no
     repair or additional audit round.
   - BLOCK: the audit could not safely or completely execute.

PASS/PASS-WITH-NITS accepts only the truth and consistency of these two reports.
It does not accept any proposed archive/rotation/repair, the six-file rotation,
or any implementation, host, deployment, strategy or Help/Wiki action.
```
