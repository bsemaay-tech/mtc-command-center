# Scope, plan and QA brief — G1/G2/G4

Lead: reuse the existing task record. Read selected INPUTS/TESTS and classify with
`../../../00_AGENT_PROTOCOLS/REVIEW_POLICY.md`. Clarify only unresolved consequential choices,
with recommendations; inspect code for facts. Stop questioning when the brief is executable.

Record these together, scaling length to consequence:

- Outcome and value: one smallest complete path through existing modules, not a broad rewrite.
- Authority/ownership: worktree, branch, owner, exact writable/forbidden paths, live dependencies,
  protected impact, applicable decision rows and retained package contract.
- Plan: affected interfaces, dependencies, relevant edge/failure cases and recoverable rollback.
- Completion example: concrete input/action -> expected result, from an independent requirement.
  Example for an authorized read-only status slice: a frozen refused event displays REFUSED and
  its reason without invoking an order path; confirm the actual displayed result.
- QA: exact command, cwd, runtime/environment, expected output and meaningful user/system path.
  Mark observed results only after execution. Define what constitutes sufficient evidence.
- Review tier and required contract; builder route/budget/stop condition if delegated.
- Next action and real owner decision, if any. Settled approvals are not new questions.

For small work this is the entire plan. Read prompt 02 only for unresolved architectural detail.
The Lead checks consequential design before G3; this is not a new owner meeting. Ordinary low-risk
builders need not be paired flagships; protected implementation/acceptance boundaries remain.

Write-back: update selected HANDOFF only if current state changes. Factual progress is permitted
before acceptance; no new root memory journal. Follow `AUTONOMY_AUTHORIZATION.md` for repairs.
