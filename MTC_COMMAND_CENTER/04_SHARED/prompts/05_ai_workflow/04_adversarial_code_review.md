# Focused independent review — G5

Lead: read `../../../00_AGENT_PROTOCOLS/REVIEW_POLICY.md` and the recorded scope. That file alone
defines the tier/roster. Highest consequence wins, including binding policy/evidence changes.
T2/T3 use the specified self-check; do not automatically dispatch auditors. Preserve explicitly
designated existing contracts. Required fresh model/effort unavailable means blocked acceptance,
not a silent substitute. Findings or diff size do not automatically add reviewers.

Freeze one packet: authority and scope, base/head, real diff/files, relevant rules and acceptance
criteria, exact QA commands/cwd/environment and raw evidence pointers. Review the actual source,
not an implementer's summary. For required review inspect scope/protected impact, behavioral
correctness, edges, dependencies, safety, and whether tests can detect the claimed defect.
Reproduce applicable evidence independently; identify each new test's verified/unverified RED/GREEN.
Use independent expected results and preserve carried regression fences. Source-only findings
and Gemini's SUPPLEMENTAL_UNEXECUTED report do not replace executed acceptance evidence.

Report only actionable findings: path:line, concrete trigger, consequence, evidence, minimum fix.
Record exact reviewer/model/effort, source identity and executed versus unexecuted checks.
Use PASS / PASS-WITH-NITS (optional only) / REQUEST_CHANGES / BLOCK. Lead compares required
auditors and reproduces findings; an implementer does not self-accept.

Repair the same scoped issue, not the whole architecture. Round counters are internal checkpoints
under AUTONOMY_AUTHORIZATION, never automatic owner re-asks or blind reruns. Use the same frozen
packet for applicable G6; retain its actual auditor obligations. G7 records truthful progress at
any point and ACCEPTED only after proof. Ordinary local commits do not require acceptance.
