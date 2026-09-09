# Claude startup prompt — supplemental AI routing

Read these files before choosing a supplemental route:

1. `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/AGENTS.md`
2. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
3. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md`
4. `MTC_COMMAND_CENTER/11_TRIAGE/AI_PROVIDER_ROUTING_RECOMMENDATION_2026-08-29.md`

Apply OD-20260829-1 and OD-20260829-2 exactly. For every T0, T1, or T2 Gate 5/Gate 6 model audit,
dispatch fresh Gemini 3.7 Flash High through its read-only launcher concurrently with the other
required auditors, using the same review packet. Compare findings; do not treat Gemini as the
acceptance auditor or as proof that a mandated suite ran.

For bounded, unprotected supplemental work: use OpenCode Go GLM-5.3-Flash first; use OpenCode Go
Kimi K3 only for difficult architecture, long-context investigation, or a stalled first attempt.
Use OpenCode Go DeepSeek V4 Pro as the supplemental deep-adversarial reviewer for evidence-backed
architecture review, difficult bug analysis, requirements-versus-implementation verification, and
failure-mode discovery. Prefer that included Go allowance before OpenRouter PAYG V4 Pro unless Go
quota exhaustion or intentional provider diversity requires the OpenRouter route. For cheap
high-volume mechanical analysis or drafts, use OpenRouter DeepSeek V4 Flash. Use paid OpenRouter
Hy3 for high-volume different-family review/diversity work. Never use a deprecated free alias as
an automated production route. Treat every OpenRouter price and revision as a dated snapshot and
refresh it before making a cost decision.

Before dispatch, verify the live route/quota without exposing any credential. Keep all provider
profiles process-scoped: do not use bare Codex, alter `CODEX_HOME`, read or print secrets, switch a
running job, or modify global environment settings. Supplemental routes do not gain protected-path,
trading, deployment, Git, credential, or final-acceptance authority. A write task still needs an
explicit worktree and exact allowed-path contract.

In the final routing record state: task classification; chosen provider/model; exact paths and
authority; why this route was suitable; why a cheaper route was not used when escalating; live
preflight result; fallback; and whether any external API credit was spent.
