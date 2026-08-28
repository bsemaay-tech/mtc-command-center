# Governance stage outputs

- G1 scope contract with whitelist, forbidden paths, acceptance criteria, and audit tier.
- G2 implementation plan when required; G3 minimal diff; G4 commands and real output.
- Evidence package compact enough for a fresh independent reviewer.
- Current state in this stage's `HANDOFF.md`; sticky owner decisions in root `DECISIONS.md`.
- `_AI_MEMORY/PROJECT_MEMORY.md` if a stable repo fact changed.
- Git commits with exact staged paths—never `git add .`; push only when authorized; never merge from
  an implementer lane unless the task explicitly grants it.

Handoff sections use `## [MODEL_NAME] YYYY-MM-DD — Topic`. Current tasks identify an executor as
`[AI: Claude|DeepSeek|Any|Barış]` when the tracker supports those tags. A completed work unit ends
with practical next actions, exact paths/commands, unresolved authorization, test evidence, and SHA.
At every close-out, rotate stale detail to the stage's grep-on-demand history and keep `HANDOFF.md`
current-only and at or below its 4 KiB hard cap.

Before releasing the write-lane claim, reconcile current `master`, the work branch, and the durable
tracker. Preserve rescue refs until explicitly dispositioned. Never infer liveness from clean Git,
push state, age, or mtime.
