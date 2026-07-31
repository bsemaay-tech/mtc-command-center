# 10 — Phase Execution Protocol

This protocol governs every later implementation prompt for a TS task. It does not authorize any task by itself.

## Mandatory session sequence

1. Read repository `AGENTS.md`, `_AI_MEMORY\START_HERE.md`, `AI_RULES.md`, `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `DO_NOT_TOUCH.md`, `ACTIVE_FILES.md`, and `SESSION_LOCK.md`.
2. Read this roadmap README, the exact backlog task, governing ADRs, gap rows, risk rows, test strategy and release gate.
3. Run `git status --short`, branch/commit checks, and TS-P0-001 drift check when available.
4. Confirm exact scope, allowlist, explicit out-of-scope items, acceptance criteria, tests, rollback and human approvals.
5. Protect the working runtime: treat `C:\P2RT`, scheduler, bridge process, DB, credentials, testnet/paper state and external services as no-touch unless separately authorized.
6. Create/switch to a `codex/` or task-approved branch/worktree when appropriate. Do not move the deployed runtime merely to create a branch.
7. Route bounded mechanical work through Cline first and the guarded cheap harness second, per `AGENTS.md`; audit results yourself. Never delegate unresolved architecture or safety-policy decisions.
8. Modify only the approved files. Preserve all unrelated dirty/untracked work; never reset, stash or checkout over it.
9. Add/update tests before or with implementation. For required red/green proof, record the focused pre-change failure without altering protected runtime state.
10. Run targeted tests from the exact required working directory.
11. Run broader tests only when justified by blast radius and authorized environment. No backtest, download, server, broker/testnet/paper action or artifact generation without explicit approval.
12. Run static/import checks, secret/diff scans and `git diff --check` appropriate to the task.
13. Review the diff against scope, ADRs, invariants, security, proposed-ADR boundaries and rollback.
14. Obtain independent adversarial review for safety-critical, protected, migration, security, order, risk, reconciliation or deployment work.
15. Update governing docs and D/M/R records. `SESSION_LOG.md` is retired and must remain untouched.
16. Re-run `git status --short`; prove no unexpected runtime/protected/unrelated changes.
17. Report unresolved risks, failed/skipped evidence, deployment status and the exact next task.
18. Stop after one defined task unless Barış explicitly authorizes more.

## Session stop conditions

Stop immediately and report if:

- `C:\P2RT` commit/status, bridge process, scheduler, API, database, positions/orders, credential source or testnet/paper state changes unexpectedly.
- A change touches Pine, parity, `MTC_V2`, protected `02_MTC_BACKTEST`, `07_ADAPTERS`, `06_SCHEMAS`, or `.git` outside approved scope.
- A Proposed ADR must be treated as Accepted to continue.
- External state is ambiguous, a submission is unknown, exposure is nonzero when zero is required, or cleanup cannot be proven.
- Tests fail outside the task scope, the diff includes unrelated changes, or required rollback is not viable.
- A secret-looking value appears in output/diff/report.
- The cheap-agent output cannot be independently verified.

## Change-scope rules

- One task, one primary invariant, one rollback story.
- No opportunistic refactor, dependency upgrade, formatting sweep or planning-document rewrite.
- For shared files used by multiple agents, commit/approval handoff before another agent edits the same file, as required by repo policy.
- Stage exact paths only if staging is authorized; never `git add .` or `-A`.
- No commit, push, PR, deploy, restart, testnet call, ARM, paper action or live action unless the prompt explicitly requests it.

## Evidence rules by work type

| Work type | Minimum evidence |
| --- | --- |
| Documentation only | Links, table/heading validation, internal consistency, `git diff --check`, status |
| Pure state/risk logic | Red/green focused tests, property boundaries, restart serialization, broader relevant suite |
| Exchange adapter | Mocks + recorded fixtures first; exact error taxonomy; testnet only after separate approval |
| Database/schema | Migration/rollback/backup on temp copies; compatibility; no active DB mutation |
| Security/dependency | Lock/SBOM/scans, known-bad fixture, redaction, outbound inventory, license review |
| Dashboard/read model | Source/age/mode/commit contract, stale/missing tests, denied write verbs, visual verification |
| Deployment | Release manifest, clean isolated runtime, tests at deployed commit, health/rollback proof; no execution unless approved |

## Standard implementation-task report template

```markdown
# <TASK_ID> — <TITLE> — Run Report

Date/time/timezone:
Agent/model:
Branch/commit before:
Branch/commit after:
Repository path:
Runtime path and read-only identity:

## Authorization and scope
- User authorization:
- Governing ADRs:
- Allowed files:
- Forbidden/out-of-scope:
- External actions authorized: none | exact bounded action

## Baseline
- `git status --short` before:
- Runtime drift result:
- Relevant pre-change behavior/failure:

## Changes
- Files changed:
- Invariant implemented:
- No unrelated changes statement:

## Validation
| Command | CWD | Result | Evidence |
| --- | --- | --- | --- |

- Targeted tests:
- Broader tests:
- Failure/restart/reconcile tests:
- Static/security/diff checks:
- Tests not run and why:

## Safety and external state
- Runtime modified: no/yes with authorization
- Scheduler/process/DB/config/credentials modified: no/yes with authorization
- Exchange/testnet/paper/live action: none or exact evidence
- Positions/orders proof if applicable:

## Review and rollback
- Independent reviewer:
- Findings/disposition:
- Rollback procedure:
- Rollback tested:

## Documentation and memory
- Docs updated:
- GLOBAL_HANDOFF/NEXT_STEPS/ACTIVE_FILES updated:
- SESSION_LOG unchanged:

## Final state
- `git status --short` after:
- Gate result: PASS/FAIL/BLOCKED
- Unresolved risks:
- Deployment status:
- Exact next task:
```

## Phase completion review

A phase closes only when every required task and gate has current evidence, open High/Critical risks are accepted or mitigated by the proper owner, rollback is tested, and the canonical roadmap/backlog/memory reflect the result. Completing code is not the same as completing a phase.

