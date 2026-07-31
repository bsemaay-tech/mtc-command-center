# KVM2 Codex-only Cycle 3 — final R3 audit metadata sync

Work in `C:\LAB\Tradingview_LAB_CLEAN`. Read and obey `AGENTS.md` and
`MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`.

This is a documentation-only metadata sync after Cycle 3/R2 audit returned
`BLOCK: AUDITOR_TRANSPORT_UNAVAILABLE`. The R2 auditor verified both frozen
hashes but did not read/audit the document content because it attempted to
launch a nested Codex CLI inside its read-only sandbox; the nested process could
not reach the OpenAI Responses API. R2 issued no content findings.

Barış requires Codex-only work with no Claude-credit use. Do not invoke or
delegate to Claude, Cline, DeepSeek, Grok, OpenRouter, another provider, another
Codex process, or a subagent. This current CLI process is the bounded metadata
implementer.

Do not alter any substantive plan, task, gate, owner, evidence, stop condition,
crosswalk row, dependency, or authority. Do not run Git mutations, access the
VPS/runtime, install/deploy, use secrets, contact brokers/exchanges, or perform
network/trading actions.

Edit only:

- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_MASTER_PLAN_MULTI_MODEL_AUDIT_PROMPT_2026-07-25.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/DECISIONS.md`

Required metadata-only changes:

1. In the identical audit-cycle maps in master, companion, and D023, preserve
   R1 exact `gpt-5.6-sol`/`xhigh` `REQUEST_CHANGES`; add R2
   `BLOCK: AUDITOR_TRANSPORT_UNAVAILABLE` with hashes verified and no content
   audit/findings; set current state to R3, Codex-only, final permitted round
   under D023.
2. In master audit-plan prose, record the same R2 transport BLOCK and state R3
   is the final round; after any non-accepting R3 verdict, STOP and report.
3. Update the audit prompt to Cycle 3/R3. Explicitly say:
   - this current CLI process itself is the sole fresh canonical auditor;
   - it must directly hash/read/audit the files;
   - it must not invoke/spawn/delegate to another Codex CLI, subagent, nested
     audit, Claude, or other provider;
   - exact `gpt-5.6-sol`, `xhigh`, ephemeral/read-only, no resume/continue,
     no fallback;
   - R2 was transport-blocked before content audit and is not an acceptance.
4. After master and companion metadata is final, compute their fresh byte-level
   SHA-256 values. Set them as Cycle-3/R3 expected hashes in the audit prompt.
   Move the current R2 hashes to superseded history, labeled as R2 transport-
   blocked inputs.

Revalidate without substantive edits:

- exactly 84 unique standard-shape IDs;
- every task exactly one `  - Evidence:` and one `  - Stop:`;
- crosswalk rows 1–10 exactly once;
- master and companion each below 60,000 bytes;
- zero full `KVM2-P...` IDs in master;
- valid UTF-8 and no persisted runtime-only private source path;
- preparation-only / execution-blocked status unchanged.

Return only concise metadata changes, validation counts/sizes, and fresh hashes.
Do not claim an R3 audit verdict.
