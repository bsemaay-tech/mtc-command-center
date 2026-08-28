# Bridge outputs

- Minimal scoped code/docs plus exact self-QA evidence; no runtime mutation unless separately
  authorized.
- Closure package for each defect: named defect, RED command/output, GREEN command/output, and
  durable-state inspection where persistence is involved.
- Deployment/run-kit outputs include candidate hash, manifest, backups, rollback proof, and explicit
  distinction between repository, staged, deployed, and running identity.
- Current-only state in `HANDOFF.md`. Historical Bridge decisions/evidence stay in their indexed
  docs/triage records; never convert old status into current authority.
