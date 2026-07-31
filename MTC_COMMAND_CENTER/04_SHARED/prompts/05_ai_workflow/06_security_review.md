# 06 — Security Review  (Gate 6)

## Mandatory audit model/effort (AGENTS.md §CANONICAL AUDIT ROSTER)

**Claude auditor:** exact model `claude-opus-5`, effort `xhigh` (always for Gate 6).
Example fresh-session CLI: `claude -p --model claude-opus-5 --effort xhigh --no-session-persistence`

**Codex auditor:** exact model `gpt-5.6-sol`, effort `xhigh` (always for Gate 6 — security surface mandates xhigh).
Example fresh-session CLI: `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c "model_reasoning_effort=xhigh" <audit_prompt_file>`

**If exact model/effort unavailable: stop as BLOCK unless Barış explicitly waives.**

**Fresh independent session required** — never resume the implementer session. Provide only: scope contract, actual diff/files, repo rules.

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

Actor: **Lead or designated independent reviewer** — must not be the
implementer of the change under review. Independence is required because
this gate follows implementer self-QA. Lead retains final acceptance
authority regardless of who runs the check.

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
8. SUPPLY CHAIN: new dependency added — is it pinned, signed,
   trusted?

Verdict: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK + one-paragraph reasoning.
PASS-WITH-NITS: accepting — optional nits only; no required repair.
REQUEST_CHANGES: non-accepting — includes required repair(s).
BLOCK: workflow cannot safely continue.

Never recommend live-trading wiring. Never recommend disabling
commit hooks. Never recommend force-pushing as a fix.
```

## WRITE-BACK

- If a finding is fixed in the same sprint: note in `GLOBAL_HANDOFF.md`.
- If a finding is deferred: log in `NEXT_STEPS.md` with severity tag.
- If a sticky security decision was made: log in `DECISIONS.md`.
