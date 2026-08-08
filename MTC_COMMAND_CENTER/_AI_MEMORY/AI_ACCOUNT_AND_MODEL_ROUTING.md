# AI ACCOUNT & MODEL ROUTING — operational index

> **Scope.** This file is an **operational index**: which account home, which wrapper, which credential *source name*. It is **not** a policy table. `AGENTS.md` remains the canonical authority for the audit roster, model tiers, protected-surface restrictions, and token discipline. Where the two ever disagree, `AGENTS.md` wins.

> **⚠️ USAGE FIGURES ARE A TIME-STAMPED SNAPSHOT — 2026-08-02.** Every "% remaining", plan tier, and reset time below was true only at the moment it was written. Quota moves continuously and rolls over on its own schedule. **Never route a task on the strength of a number in this file. Re-check the live account before you spend it** — via the account's live usage/dashboard view in the provider console. (`login status` does **not** report quota; see §1.) Treat a stale number as unknown, not as headroom.

> **No secrets here, ever.** This file names credential *sources* (Windows Credential Manager target names, environment variable names) and nothing else. Never store, echo, paste, or log a token, key, or `auth.json` value into this repo. The launcher does not read `auth.json`; neither should you.

---

## 1. OpenAI Codex — account homes

Account identity is selected **only** by the process-scoped `CODEX_HOME` environment variable, which points at a dedicated home directory whose own `auth.json` carries that account's session.

The **home → account** mapping in the table below is a **recorded setup fact** (how these homes were provisioned). It is *not* re-proven by any command in this file; treat it as documentation that can drift, and re-establish it out of band if it matters.

| Route | `CODEX_HOME` | Account | Plan | Remaining (2026-08-02 snapshot) | Use |
|---|---|---|---|---|---|
| **desktop / default** | `C:\Users\BarışSemaay\.codex` | `bs***y3@gmail.com` | Plus | 72% | **Reserved for the Codex desktop/app side.** Not selectable from the launcher. |
| **secondary** ✅ | `C:\Users\BarışSemaay\.codex-hesap2` | `bs***y4@gmail.com` | Plus | 99% | **Claude's default Codex CLI route.** |
| **free** ✅ | `C:\Users\BarışSemaay\.codex_OLD` | `bs***y2@gmail.com` | **Plus** (upgraded 2026-08-08 — the label "free" is now only a route name) | available 2026-08-08 | **Verified flagship-capable 2026-08-08.** `login status` = logged in; a live probe returned header `model: gpt-5.6-sol / reasoning effort: xhigh` and completed. Carried the whole binding D025 flagship audit of `ebada020`. The rule below still applies to every future run: probe first, **never silently downgrade the model or effort, and never substitute a different model** for a mandated one. |
| **fourth** | `C:\Users\BarışSemaay\.codex-bsemaay` | `bsemaay@gmail.com` | Plus | **0%** until reset **2026-08-08 08:49 local** | Isolated home directory exists; **browser/device authorization was still pending when this file was written.** The wrapper supports the route, but it is not a verified logged-in route. |

> **Correction 2026-08-08 — this table said `free` was plan Free. It is not, and two other things here can mislead:**
>
> 1. **The account was upgraded to ChatGPT Plus**, so a "Free tier" reading of this route is wrong. `gpt-5.6-sol` at `xhigh` is proven live on it.
> 2. **`models_cache.json` in a home is not evidence of model availability.** `.codex_OLD`'s cache still lists no `GPT-5.6-Sol` because it was written while the account was Free. **A live probe overrides the cache** — do not conclude a model is unavailable from a stale cache file.
> 3. **`secondary` is the documented default but was credit-exhausted** by the 2026-08-03 overnight run. Do not route a mandated flagship there on the strength of the "99%" snapshot above; snapshots in this file are dated and must be re-checked, as §15 already warns.

### Hard rules

- **Never log out of, or switch, the desktop account** (`C:\Users\BarışSemaay\.codex`). Desktop app state lives there.
- **The launcher must never offer or route to `.codex`.** It is absent from the allowlist and additionally rejected by an explicit guard.
- **Never migrate a running Codex job between homes.** A job's session, rollout, and auth belong to the home it started under. Finish it or restart it cleanly; do not repoint `CODEX_HOME` mid-flight.
- **Default stays `secondary`** even though `fourth` is wired up.
- Canonical Codex **model/effort** rules (e.g. `gpt-5.6-sol`, effort `high`/`xhigh`) live in `AGENTS.md` §CANONICAL AUDIT ROSTER. This file records **homes and launcher only**.

### Launcher (mandatory for Claude)

`C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1`

Sets `CODEX_HOME` for the child invocation only, restores or removes the prior process value in `finally`, preserves the child exit code, fails clearly when the selected home or the CLI is missing, and resolves the CLI to the installed `C:\Users\BarışSemaay\AppData\Roaming\npm\codex.ps1` (with a `Get-Command` fallback restricted to real executables/scripts). It reads no credential.

> **Calling convention — bare Codex flags DO NOT WORK (verified 2026-08-08).** PowerShell tries to bind `-m` / `-c` as script parameters before `ValueFromRemainingArguments` sees them, so
>
> ```powershell
> # FAILS: "A positional parameter cannot be found that accepts argument 'exec'"
> & .\Invoke-CodexForClaude.ps1 -Account free exec --sandbox read-only -m gpt-5.6-sol -c "model_reasoning_effort=xhigh" prompt
> ```
>
> Build an array and pass it explicitly instead:
>
> ```powershell
> $a = @('exec','--sandbox','read-only','-m','gpt-5.6-sol','-c','model_reasoning_effort=xhigh', $promptText)
> & .\Invoke-CodexForClaude.ps1 -Account free -CodexArgs $a
> ```
>
> **Two more traps paid for in the same session.** Codex refuses commands as `blocked by policy` under `sandbox: read-only` outside a trusted project dir — for an isolated audit worktree, `--dangerously-bypass-approvals-and-sandbox` clears it and the run header should then read `sandbox: danger-full-access`. And outside a git repo, `exec` aborts with *"Not inside a trusted directory and --skip-git-repo-check was not specified"*, so a scratch-dir probe needs `--skip-git-repo-check`.
>
> **A prompt containing double quotes cannot be passed as an argv element.** PowerShell 5.1 does not escape embedded double quotes when handing an argument to a native exe, so the prompt is word-split and Codex dies with e.g. `error: unexpected argument 'DISARMED,' found`. Markdown prompts using only backticks survive by luck; any prompt quoting shell or code will not.
>
> **Piping the prompt on stdin does NOT work through this launcher** — it is a `[CmdletBinding()]` script with no pipeline-bound parameter, so the pipeline object fails to bind, stdin never reaches the child, and Codex reports `No prompt provided via stdin`. Do not "fix" this by calling `codex` directly with a hand-set `CODEX_HOME`; the launcher is mandatory.
>
> **Working pattern: keep the rich prompt in a file and pass a short, quote-free pointer as the prompt.** Codex reads the file itself.
>
> ```powershell
> $short = 'Read the file C:\tmp\my_prompt.md in full. It is your complete task specification. Execute it exactly as written.'
> $a = @('exec','--dangerously-bypass-approvals-and-sandbox','-m','gpt-5.6-sol','-c','model_reasoning_effort=high', $short)
> & .\Invoke-CodexForClaude.ps1 -Account free -CodexArgs $a
> ```
>
> This also keeps the dispatched specification on disk as a reviewable artefact, which is worth having independently of the quoting problem.

```powershell
# default route (secondary) — any Codex args are forwarded verbatim
& "C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1" --version

# safe probe: is the selected CODEX_HOME logged in at all? (does NOT reveal which account)
& "C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1" login status

# explicit secondary
& "C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1" -Account secondary login status

# fourth (quota-reset / pending-auth route)
& "C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1" -Account fourth login status

# free fallback
& "C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1" -Account free --version

# a real bounded run on the default route
& "C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1" exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c "model_reasoning_effort=high" <audit_prompt_file>
```

`-Account` is allowlisted to `secondary` (default) · `fourth` · `free`. Anything else — including `desktop` — is refused at parameter binding.

**What `login status` does and does not prove.** It is the cheap, safe liveness check for a route: it reports whether the **selected `CODEX_HOME` is logged in**, and it touches nothing. As observed, its output does **not** print the account email and does **not** report quota or plan tier. So it can tell you "this route is usable / this route is not authorized"; it cannot tell you *which* account you are about to spend or *how much* of it is left.

To establish **identity or remaining quota**, use the live method instead — the account's usage/dashboard view in the provider console (or an equivalent live usage readout) for that account. The home→account rows in the table above are recorded setup facts, not output of `login status`.

---

## 2. GLM (Z.AI Coding Plan)

| Item | Value |
|---|---|
| Wrapper | `C:\Users\BarışSemaay\bin\glm.ps1` |
| Plan | Z.AI Coding Plan |
| Credential **source name** | Windows Credential Manager target `ZAI_GLM_CODING_PLAN_KEY` |
| Isolation | The wrapper creates a **fresh temporary `CLAUDE_CONFIG_DIR` per invocation** and deletes it afterwards, so no ambient Claude account/session state shadows the Coding Plan credential. |
| Audit helper | `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GlmAudit.ps1` |

Canonical GLM **model tiers and the cheapest-capable decision tree** live in `AGENTS.md` §GLM SUPPLEMENTAL ROUTING. Do not copy that table here. Do **not** ask for or paste a Z.AI key anywhere — the wrapper pulls it from Credential Manager and never prints it.

---

## 3. Cline

| Item | Value |
|---|---|
| Profile | `cline-pass` |
| First attempt (supplemental / audit) | `cline-pass/deepseek-v4-flash` |
| Stronger reasoning | `cline-pass/deepseek-v4-pro` |

Cline is **not a flagship substitute**. For audits it must run in an **isolated worktree** at the frozen SHA, and cleanliness must be proven afterwards (`git status --porcelain` empty). Implementation authority and the four-auditor acceptance rule remain as written in `AGENTS.md`.

---

## 4. DeepSeek driver (fallback)

| Item | Value |
|---|---|
| Harness | `_deepseek_driver\ds_agent.py` (repo-relative) — canonical checkout `C:\LAB\Tradingview_LAB_CLEAN\_deepseek_driver\ds_agent.py` |
| Provider id | `deepseek` |
| Credential **env name** | `DEEPSEEK_API_KEY` |
| Authority | `_deepseek_driver\README.md` (canonical `C:\LAB\Tradingview_LAB_CLEAN\_deepseek_driver\README.md`) — read it before dispatching. |

> Paths are repo paths. Do **not** hardcode a temporary worktree root (`C:\AIROUTE`, `C:\G5R`, …); resolve from the checkout you are working in, or from the canonical checkout above.

---

## 5. Grok / xAI

Same driver as above.

| Item | Value |
|---|---|
| Harness | `_deepseek_driver\ds_agent.py` (canonical `C:\LAB\Tradingview_LAB_CLEAN\_deepseek_driver\ds_agent.py`) |
| Provider id | `grok` / `xai` |
| Model | `grok-4` |
| Credential **env name** | `XAI_API_KEY` |

---

## 6. NVIDIA NIM (via local LiteLLM translation)

| Item | Value |
|---|---|
| Endpoint | `http://localhost:4000` (local LiteLLM translation layer) |
| Proxy config | `C:\Users\BarışSemaay\nvidia-litellm\config.yaml` |
| Credential **env name** | `NVIDIA_API_KEY` |

Standalone TOML files — **templates / config snapshots**, recording the intended model per route. They live under the **desktop home**, which the launcher refuses:

| File | Model |
|---|---|
| `C:\Users\BarışSemaay\.codex\nvidia.config.toml` | `z-ai/glm-5.2` |
| `C:\Users\BarışSemaay\.codex\nvidia-deepseek.config.toml` | `deepseek-ai/deepseek-v4-pro` |
| `C:\Users\BarışSemaay\.codex\nvidia-minimax.config.toml` | `minimaxai/minimax-m3` |

> **⚠️ There is currently NO verified launch command for these routes.** Nothing below has been probed end to end; do not treat it as an invocation recipe.
>
> Facts as observed 2026-08-02:
>
> - `C:\Users\BarışSemaay\.codex\config.toml` contains **no `[profiles.*]` entries** (its sections are `marketplaces.*`, `plugins.*`, `features`, `desktop`, `windows`, `projects.*`, `memories`, `mcp_servers.*`, `shell_environment_policy.set`).
> - Current Codex help shows `-c, --config <key=value>` — a **key=value override**, parsed as TOML. There is **no path-taking config flag**; "point Codex at one of these TOML files with `--config <path>`" is not a thing.
> - Current Codex help also shows `-p, --profile <CONFIG_PROFILE_V2>`, described as layering `$CODEX_HOME/<name>.config.toml` over the base user config — i.e. profiles v2 resolve to **files under the selected `CODEX_HOME`**, not to `[profiles.*]` sections. The files above sit in `C:\Users\BarışSemaay\.codex`, and that home is **not selectable from the mandatory launcher** (§1 hard rules), so this does not yield a usable route as things stand.
>
> **Consequence:** using NVIDIA NIM is a *setup* task, not a copy-paste task. A future route must be **configured separately** — the intended config placed under a launcher-selectable `CODEX_HOME`, or expressed as `-c` overrides — and then **freshly probed end to end** (LiteLLM listener up on `http://localhost:4000`, intended model id answering) before anything is dispatched to it. Do not invent or guess a command; record the one that is proven to work, once one exists.

**Last known result (2026-08-02 snapshot, re-verify):** the NVIDIA DeepSeek tool cycle passed; the MiniMax continuation hit **HTTP 429**.

---

## 7. Standing constraints

- `AGENTS.md` is canonical for: audit roster, model tiers, protected-surface restrictions, token discipline. This file duplicates none of it.
- Account selection is **process-scoped `CODEX_HOME` only**. No global env edits, no `codex login` juggling on a shared home.
- **Never store or print token / key / `auth.json` values.** Name the credential source, never the secret.
- Every usage number in §1 is a **2026-08-02 snapshot** and must be freshly checked before it is relied on.
