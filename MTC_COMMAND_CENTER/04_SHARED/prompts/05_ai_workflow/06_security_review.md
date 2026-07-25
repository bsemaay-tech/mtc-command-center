# 06 - Security Review  (Gate 6)

## Mandatory audit model/effort (AGENTS.md CANONICAL AUDIT ROSTER)

**Claude auditor:** exact model `claude-opus-4-8`, effort `xhigh` (always for Gate 6).
Example fresh-session CLI: `claude -p --model claude-opus-4-8 --effort xhigh --no-session-persistence`

**Codex auditor:** exact model `gpt-5.6-sol`, effort `xhigh` (always for Gate 6 - security surface mandates xhigh).
Example fresh-session CLI: `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c 'model_reasoning_effort="xhigh"' "<audit prompt>"`

**If exact model/effort unavailable: stop as BLOCK unless Barış explicitly waives.**

**Fresh independent session required** - never resume the implementer session. Provide only: scope contract, actual diff/files, repo rules.

Use **only if the change touches a security-relevant surface**:

- Secrets / tokens / credentials handling.
- Authentication / authorization.
- Network calls (HTTP, websocket, MCP).
- File system writes outside the repo.
- `eval`, `exec`, dynamic import, `subprocess`, shell strings.
- External process invocation (`os.system`, `Popen`, `Invoke-Expression`).
- Deserialization of untrusted input (pickle, yaml.unsafe_load).

Skip for pure docs, Pine plotting, cosmetic changes, or anything purely
internal to the parity suite that does not shell out.

## Prompt

```
You are running Gate 6 (Security Review) for Tradingview_LAB_CLEAN.

Actor: **Lead Orchestrator** — the lead runs the exact canonical audit (see `AGENTS.md` CANONICAL AUDIT ROSTER) or invokes an exact-roster fresh audit instance. Human/Fable/Gemini review is advisory and cannot satisfy G6. The auditor must not be the implementer of the change under review. Lead retains final acceptance authority regardless of who runs the check.

Read:
- The diff.
- The Gate 1 scope contract.

Check, and report findings as
`path:line: <severity>: <problem>. <fix>.`:

1. SECRETS: any token, key, password, or credential introduced or
   logged.
2. INJECTION: shell, SQL, OS command, Pine string injection from
   untrusted input.
3. SSRF / NETWORK: requests to attacker-controllable URLs, missing
   timeouts, missing TLS verification.
4. PATH TRAVERSAL: writes / reads with user-controlled paths.
5. UNSAFE DESERIALIZATION: pickle, yaml.unsafe_load, eval, exec on
   untrusted data.
6. SUBPROCESS: shell=True, unquoted args, missing input validation.
7. PERMISSIONS: code that escalates, weakens ACLs, or disables hooks
   / signing.
8. SUPPLY CHAIN: new dependency added - is it pinned, signed,
   trusted?

Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK + one-paragraph reasoning.
PASS-WITH-NITS: accepting - optional nits only; no required repair.
REQUEST_CHANGES: non-accepting - includes required repair(s).
BLOCK: workflow cannot safely continue.

Never recommend live-trading wiring. Never recommend disabling
commit hooks. Never recommend force-pushing as a fix.
```

## WRITE-BACK

- **Component-scoped findings:**
  - Fixed: note in `<component>/_AI_MEMORY/CURRENT.md`.
  - Deferred: log in `<component>/_AI_MEMORY/NEXT_STEPS.md` with severity tag.
  - Sticky security decision: log in `<component>/_AI_MEMORY/DECISIONS.md`.
- **Cross-component findings:** update every affected relevant component per the above rules first; then add one concise root coordination entry to root `GLOBAL_HANDOFF.md` / `NEXT_STEPS.md` / `DECISIONS.md` as appropriate.
- **Global/policy findings:** note in root `GLOBAL_HANDOFF.md` (fixed), root `NEXT_STEPS.md` (deferred), root `DECISIONS.md` (sticky decision).
