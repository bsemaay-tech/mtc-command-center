# Review checklist — use at the task boundary

Canonical review count/effort: `../00_AGENT_PROTOCOLS/REVIEW_POLICY.md`, read for classification
or audit. Follow selected TESTS and OUTPUTS; this checklist adds no auditors or repeated gate.

- Actual diff matches approved paths/behavior; protected scope is authorized; foreign edits safe.
- Completion example observed; exact command/cwd/environment and independently expected result
  recorded. Failed commands are visible. Required defect RED/GREEN and carried fences preserved.
- Only the applicable tier/explicit package reviews ran; required findings independently resolved.
  Self-check, supplemental report and executed acceptance are clearly distinguished.
- Relevant manual/visual/integration behavior checked; actual outcome and limitations stated.
- Current stage HANDOFF updated truthfully, including pending/blocked state. DECISIONS and other
  trackers only if facts changed; retired session journals remain retired.
- Before an authorized commit: exact staged paths, scoped checks, normal guard/hooks, feature
  branch. Ordinary local commits may precede acceptance; push/merge and protected CI stay separate.
- NEXT ACTION and WAITING FOR OWNER/Nothing are explicit; no unnecessary owner re-ask.
