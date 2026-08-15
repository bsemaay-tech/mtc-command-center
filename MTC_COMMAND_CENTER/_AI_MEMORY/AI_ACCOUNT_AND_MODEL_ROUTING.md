# AI ACCOUNT & MODEL ROUTING — operational index

> **Scope.** This file is an **operational index**: which account home, which wrapper, which credential *source name*. It is **not** a policy table. `AGENTS.md` remains the canonical authority for the audit roster, model tiers, protected-surface restrictions, and token discipline. Where the two ever disagree, `AGENTS.md` wins.

> **⚠️ USAGE FIGURES ARE A TIME-STAMPED SNAPSHOT — 2026-08-08.** Every "% remaining", plan tier, and reset time below was true only at the moment it was written. Quota moves continuously and rolls over on its own schedule. **Never route a task on the strength of a number in this file. Re-check the live account before you spend it** — via the account's live usage/dashboard view in the provider console. (`login status` does **not** report quota; see §1.) Treat a stale number as unknown, not as headroom.

> **No secrets here, ever.** This file names credential *sources* (Windows Credential Manager target names, environment variable names) and nothing else. Never store, echo, paste, or log a token, key, or `auth.json` value into this repo. The launcher does not read `auth.json`; neither should you.

---

## 1. OpenAI Codex — account homes

Account identity is selected **only** by the process-scoped `CODEX_HOME` environment variable, which points at a dedicated home directory whose own `auth.json` carries that account's session.

The **home → account** mapping in the table below is a **recorded setup fact** (how these homes were provisioned). It is *not* re-proven by any command in this file; treat it as documentation that can drift, and re-establish it out of band if it matters.

| Route | `CODEX_HOME` | Account | Plan | Status (2026-08-08 snapshot) | Use |
|---|---|---|---|---|---|
| **desktop / default** | `C:\Users\BarışSemaay\.codex` | `bs***y3@gmail.com` | Plus | Authenticated (owner probe 2026-08-08) | **Reserved for the Codex desktop/app side.** Not selectable from the launcher. |
| **secondary** ✅ | `C:\Users\BarışSemaay\.codex-hesap2` | `bs***y4@gmail.com` | Plus | Authenticated (owner probe 2026-08-08) | **Claude's default Codex CLI route.** |
| **free** ✅ | `C:\Users\BarışSemaay\.codex_OLD` | `bs***y2@gmail.com` | **ChatGPT Pro ($100/mo)** — owner-confirmed upgrade 2026-08-08; route name `free` is historical only | Authenticated (owner probe 2026-08-08) | **Usable, but coordinate before large dispatches.** The owner actively uses this same Pro account in the Codex Windows desktop app, so heavy CLI spend on this route competes directly with the owner's desktop usage. The rule below still applies to every future run: probe first, **never silently downgrade the model or effort, and never substitute a different model** for a mandated one. |
| **fourth** | `C:\Users\BarışSemaay\.codex-bsemaay` | `bsemaay@gmail.com` | Plus | Authenticated and usable (owner probe 2026-08-08) | Isolated launcher route; default remains `secondary`. |

> **History correction 2026-08-08 — dated status superseded by owner confirmation:**
>
> 1. `.codex_OLD` was recorded as Free and then corrected to Plus on 2026-08-08; the owner-confirmed current plan is **ChatGPT Pro ($100/mo)**, upgraded 2026-08-08. The route name `free` is historical only.
> 2. **`models_cache.json` in a home is not evidence of model availability.** `.codex_OLD`'s cache still lists no `GPT-5.6-Sol` because it was written while the account was Free. **A live probe overrides the cache** — do not conclude a model is unavailable from a stale cache file.
> 3. `.codex-bsemaay` was recorded as awaiting browser/device authorization on 2026-08-02; owner probe on 2026-08-08 confirmed it authenticated and usable.
> 4. **`secondary` is the documented default but was credit-exhausted** by the 2026-08-03 overnight run. Do not route a mandated flagship there on the strength of an old snapshot; snapshots in this file are dated and must be re-checked, as the warning above states.

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

# fourth (authenticated isolated route; owner-confirmed 2026-08-08)
& "C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1" -Account fourth login status

# historical `free` route name; owner-confirmed ChatGPT Pro 2026-08-08
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

**GLM-5.3 is live and selectable (probed 2026-08-15 ~23:15 +03).** Owner asked
for it after the recent launch. Verified with a real call, not a cache read:

```powershell
& 'C:\Users\BarışSemaay\bin\glm.ps1' -p "<prompt>" --model glm-5.3
# -> PROBE_OK glm-5.3, exit 0
```

The wrapper's existing isolation applies unchanged (fresh temporary
`CLAUDE_CONFIG_DIR` per invocation, key from Credential Manager). The standing
constraint also applies unchanged and decides where GLM-5.3 is useful: **GLM
cannot execute harnesses unattended here**, so its verdicts stay supplemental on
anything requiring a run, and it suits source-level review, design second
opinions, and cross-reading. Owner routing note 2026-08-15: use GLM as the audit
route once the Claude Pro 5-hour window is spent, before reaching for Max.

**Current state (2026-08-08): WORKING.** Snapshot: 5-hour quota 0% used; weekly quota 51% used, resetting Aug 9 at 11:26; MCP quota 0% used, resetting Aug 26 at 11:26. The plan auto-renews Aug 26 at $16.20. Route remains `glm.ps1` plus Credential Manager target `ZAI_GLM_CODING_PLAN_KEY`.

---

## 3. Cline

| Item | Value |
|---|---|
| Profile | `cline-pass` |
| First attempt (supplemental / audit) | `cline-pass/deepseek-v4-flash` |
| Stronger reasoning | `cline-pass/deepseek-v4-pro` |

Cline is **not a flagship substitute**. It may fill only a tier-authorized secondary/T2 slot or an explicitly designated four-auditor slot. For audits it must run in an **isolated worktree** at the frozen SHA, and cleanliness must be proven afterwards (`git status --porcelain` empty). Auditor count/cadence and any explicit four-auditor contract remain as written in `AGENTS.md`.

**Current state (2026-08-08):** the Cline CLI harness is installed and verified at version 3.0.51; it remains the first-choice sub-delegation harness per `AGENTS.md`. The separate ClinePass subscription is **PAUSED** because of an unpaid invoice and has 0 credits (owner-confirmed 2026-08-08), so it is not usable as capacity. Consequently D025 canonical auditor 3 (`cline-pass/deepseek-v4-flash`) is **BLOCKED** until the subscription is reactivated and a live probe passes. This does not mean the Cline harness itself is broken.

---

## 4. DeepSeek driver (fallback)

| Item | Value |
|---|---|
| Harness | `_deepseek_driver\ds_agent.py` (repo-relative) — canonical checkout `C:\LAB\Tradingview_LAB_CLEAN\_deepseek_driver\ds_agent.py` |
| Provider id | `deepseek` |
| Credential **env name** | `DEEPSEEK_API_KEY` |
| Authority | `_deepseek_driver\README.md` (canonical `C:\LAB\Tradingview_LAB_CLEAN\_deepseek_driver\README.md`) — read it before dispatching. |

> Paths are repo paths. Do **not** hardcode a temporary worktree root (`C:\AIROUTE`, `C:\G5R`, …); resolve from the checkout you are working in, or from the canonical checkout above.

**Current state (2026-08-08): WORKING.** Balance snapshot: approximately $2.90. Route remains `_deepseek_driver` with credential environment name `DEEPSEEK_API_KEY`.

---

## 5. Grok / xAI

Same driver as above.

| Item | Value |
|---|---|
| Harness | `_deepseek_driver\ds_agent.py` (canonical `C:\LAB\Tradingview_LAB_CLEAN\_deepseek_driver\ds_agent.py`) |
| Provider id | `grok` / `xai` |
| Model | `grok-4` |
| Credential **env name** | `XAI_API_KEY` |

**Current state (2026-08-08): NOT USABLE.** A 2026-08-08 model-list probe returned HTTP 403 (access/key/project issue). Keep the configuration, but do not re-probe routinely until the owner repairs access.

---

## 6. NVIDIA NIM (via local LiteLLM translation)

| Item | Value |
|---|---|
| Endpoint | `http://localhost:4000` (local LiteLLM translation layer) |
| Proxy config | `C:\Users\BarışSemaay\nvidia-litellm\config.yaml` |
| Credential **env name** | `NVIDIA_API_KEY` |
| Self-starting launcher | `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-NvidiaNim.ps1` |

Standalone TOML files — **templates / config snapshots**, recording the intended model per route. They live under the **desktop home**, which the launcher refuses:

| File | Model |
|---|---|
| `C:\Users\BarışSemaay\.codex\nvidia.config.toml` | `z-ai/glm-5.2` |
| `C:\Users\BarışSemaay\.codex\nvidia-deepseek.config.toml` | `deepseek-ai/deepseek-v4-flash-0731` |
| `C:\Users\BarışSemaay\.codex\nvidia-minimax.config.toml` | `minimaxai/minimax-m3` |

> **Verified Claude-compatible launch command (2026-08-10):**
> `$a=@('--print','<PROMPT>','--no-session-persistence','--output-format','text'); & 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-NvidiaNim.ps1' -Route deepseek -ClaudeArguments $a`
> Use `-Route minimax` for MiniMax M3. `-Route glm` works but the measured cold/translated response took about two minutes; prefer the separate Z.AI GLM helper for routine GLM work.
>
> Facts as observed 2026-08-02:
>
> - `C:\Users\BarışSemaay\.codex\config.toml` contains **no `[profiles.*]` entries** (its sections are `marketplaces.*`, `plugins.*`, `features`, `desktop`, `windows`, `projects.*`, `memories`, `mcp_servers.*`, `shell_environment_policy.set`).
> - Current Codex help shows `-c, --config <key=value>` — a **key=value override**, parsed as TOML. There is **no path-taking config flag**; "point Codex at one of these TOML files with `--config <path>`" is not a thing.
> - Current Codex help also shows `-p, --profile <CONFIG_PROFILE_V2>`, described as layering `$CODEX_HOME/<name>.config.toml` over the base user config — i.e. profiles v2 resolve to **files under the selected `CODEX_HOME`**, not to `[profiles.*]` sections. The files above sit in `C:\Users\BarışSemaay\.codex`, and that home is **not selectable from the mandatory launcher** (§1 hard rules), so this does not yield a usable route as things stand.
>
> **Codex-side consequence:** the TOML profiles remain configuration snapshots rather than the canonical invocation path. The verified operational route is the Claude-compatible helper above; a separate Codex-profile launch still requires its own fresh end-to-end proof.

**Current state (2026-08-10): WORKING through the self-starting Claude-compatible helper.** The launcher fixes the Windows Turkish-codepage LiteLLM crash with process-scoped UTF-8 settings, starts the proxy hidden when needed, verifies health, and restores all parent-process environment values. End-to-end Claude CLI probes passed for `deepseek-ai/deepseek-v4-flash-0731` and `minimaxai/minimax-m3`; direct and translated GLM-5.2 probes passed but the translated call was slow. NVIDIA retired `deepseek-ai/deepseek-v4-pro` on 2026-08-07, so it was replaced by Flash. Kimi K2.6 was listed by the model endpoint but returned HTTP 404 in a real completion and is deliberately not exposed by the launcher.

---

## 7. Standing constraints

- `AGENTS.md` is canonical for: audit roster, model tiers, protected-surface restrictions, token discipline. This file duplicates none of it.
- Account selection is **process-scoped `CODEX_HOME` only**. No global env edits, no `codex login` juggling on a shared home.
- **Never store or print token / key / `auth.json` values.** Name the credential source, never the secret.
- Every usage number in §1 is a **2026-08-08 snapshot** and must be freshly checked before it is relied on.

---

## 8. Claude accounts (Pro + Max)

| Account | Subscription state (2026-08-10) | CLI profile / isolation | Operational status (2026-08-10) |
|---|---|---|---|
| Claude Pro — `bsemaay3@gmail.com` | Pro, approximately $20/mo; live CLI status | Default profile at `%USERPROFILE%\.claude` is authenticated | `claude-opus-5` with `--effort xhigh` returned the exact smoke marker on 2026-08-10. |
| Claude Max — `bsemaay3@gmail.com` | Max, approximately $100/mo; live CLI status | **Mandatory launcher:** `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-ClaudeMax.ps1`. It scopes `CLAUDE_CONFIG_DIR` to `C:\Users\BarışSemaay\.claude-max` for the child invocation and restores the prior value afterward. | Isolated helper authentication returned `subscriptionType: max` on 2026-08-10; no paid inference probe was needed for this refresh. |

Never authenticate Max into the default `.claude` profile, and never log the Pro profile out. A purchased/active subscription, a configured isolated CLI profile, and a verified working CLI route are distinct states; the table records each separately.

---

## 9. Installed local AI tooling & router decision (2026-08-08)

### Verified local inventory

- `cline` 3.0.51 (npm).
- `opencode` (npm), installed but unvalidated as a worker harness.
- `9router` (npm), installed but unconfigured.
- `litellm` under `~\.local\bin`; NVIDIA helper self-starts its localhost proxy when needed.
- Codex CLI and Claude CLI installed.
- GLM wrapper at `C:\Users\BarışSemaay\bin\glm.ps1`; it is not on `PATH` as `glm`.
- OmniRoute is **not installed**.

### Other API routes

- **OpenRouter — NOT USABLE (2026-08-08).** Effective balance is -$1.4393 ($10.00 purchased, $11.4393 used), so paid calls and likely free calls are blocked. Keep its configuration as a dormant future fallback; do not delete it.
- **FreeModel — NOT READY (2026-08-08).** Pro runs until Sep 4 with manual renewal and no auto-charge, but the account is not verified. It is outside active routing.

### Lead router decision (2026-08-08)

OmniRoute, or any new aggregation router, will **not** be installed:

1. Every premium subscription route (four Codex accounts, Claude Pro, Claude Max, and the GLM Coding Plan) is native-client-only. A third-party router cannot aggregate them without unsupported authentication behavior and Terms-of-Service risk.
2. The only live API providers a router could pool are NVIDIA NIM direct and DeepSeek (approximately $2.90). Two providers do not justify a new always-on, key-holding daemon.
3. Provider fallback already exists in the repository through `_deepseek_driver/provider.py` (`deepseek` / `grok` / `openrouter` with per-call fallback), Cline profiles, `glm.ps1`, and the allowlisted Codex launcher.
4. `9router` and `litellm` stay installed but **DORMANT**. They are candidates for a future dedicated setup task only if a concrete gap is demonstrated, such as a NIM-backed worker harness. Reopening this decision requires a flagship-led evaluation; it is not the default.
