# NEXT SESSION — FULL HANDOFF (2026-08-02)

**Supersedes `NEXT_SESSION_HANDOFF_2026-08-01.md`.** Paste everything below the line as the new
session's first message. It is written to stand alone — no prior conversation needed.

---

Repo: `C:\LAB\Tradingview_LAB_CLEAN`

Read `AGENTS.md`, then `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (RESUME HERE), then
`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md`.

You are **Lead Orchestrator and acceptance authority**. Codex CLI `gpt-5.6-sol` is the implementer.
This role assignment supersedes the plan's §23c/§39-10 actor assignment and weakens no safety,
testing, scope, audit, model or evidence requirement.

## 1. FIRST ACTION — verify Hyper-V access, then build the staging VM

Barış added his user to the local **"Hyper-V Yöneticileri"** group (SID `S-1-5-32-578`) and has since
signed out and back in. Hyper-V is installed and `vmms` is Running; the only blocker was that the
old logon token lacked the group.

**Verify before assuming:**

```
Get-VM
```

and confirm the token now carries the group:

```
([Security.Principal.WindowsIdentity]::GetCurrent()).Groups | ? { $_.Value -eq 'S-1-5-32-578' }
```

- If `Get-VM` still fails with *"Bu görevi tamamlamak için gerekli izne sahip değilsiniz"*, the
  re-login did not take. Ask Barış to sign out/in again or reboot. **Do not add group memberships,
  change security settings, or elevate yourself — that is his action, not yours, even if he approves.**
- If it works: create **one expendable Ubuntu 24.04 LTS VM** as the staging host. It must be
  disposable — we will break it, wipe it and redo. Generation 2, enough disk for a ~1 GB artifact plus
  the OS.

**Alternative if Barış prefers:** he builds the VM himself in Hyper-V Manager and gives you the VM
name plus reachability (IP/SSH user). **Credentials stay owner-held — never ask for, accept, or paste
a password, key or token.**

## 2. Then run Gate A, exactly as pre-registered

`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md`
(commit `af071882`) fixes every check, expected output and pass/fail line **in advance**. Execute it;
do not renegotiate the criteria against whatever the run produces. Report in its §5 format.

Checks A-0 … A-9 cover: artifact hash before and after transfer · clean-host preconditions · install
from the immutable artifact only · the Linux + Bridge suite · **starts and stays DISARMED, ARM
refuses** (A-4, the whole point of the programme) · unclean-restart safety · reconcile completes ·
observability · loopback-only exposure · no secrets on disk.

**A-3 carries a prediction, recorded deliberately:** the KVM2 ledger-hash test may legitimately
**pass** on Linux, because WP-L Phase 1 diagnosed its Windows failure as a CRLF artefact. Record the
result either way — that is evidence, not a story told afterwards.

## 3. Program state — verified, not reported

| Item | Value |
|---|---|
| `origin/master` | `637307e8` |
| Records branch | `feature/donchian-crypto-ladder` @ `af071882` |
| WP-L branch | `codex/50h-wpl-verification` @ `d9d38d9b` |
| Candidate artifact | `C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84` (~1020 MB on disk) |
| Manifest SHA-256 | `bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02` |
| Manifest scope | 7,060 entries verified · 7,061 files · 1,051,904,669 bytes · nine secret categories, zero hits |
| Hours | 20.5 used / 29.5 remaining of 50 |

**Done:**
- **WP-S closed and merged.** S3-STRUCT accepted at `16cbc717`, merged at `637307e8`. Both flagships
  accepting (`gpt-5.6-sol` PASS, `claude-opus-5` PASS-WITH-NITS), zero required findings. Record:
  `11_TRIAGE/WPS_S3STRUCT_ACCEPTANCE_RECORD_2026-08-01.md`.
- **WP-L Phase 1** independently reproduced and accepted. The two test failures are the Windows CRLF
  ledger mismatch plus the pre-existing `schema_version == "2"` mismatch — **not** WP-L defects.
- **WP-I candidate** built, verified, credential-scrubbed tests 4/4 and 2/2.

**Not done:** anything on Linux. No Ubuntu deployment, service start, broker/order, ARM, TESTNET
order, mainnet, wallet, credential-value or live-capital action has occurred at any point.

## 4. Carry this caveat forward — WP-I's acceptance is weaker than WP-S's

WP-I's candidate acceptance rests on **a single owner-waived DeepSeek pass** (PASS-WITH-NITS), not on
the canonical two-flagship floor in `AGENTS.md`. The waiver was Barış's call and is valid, but it is
not the same standard WP-S met. **Audit 2 is where that gap closes** — plan for two flagship auditors
there. Do not describe WP-I as accepted on the normal floor.

## 5. Sequence, and when KVM2 comes

`Gate A → WP-L Phase 2 → WP-I staging → Audit 2 → WP-A → WP-V (KVM2 deployment)`, all DISARMED.

**KVM2 is the programme's deployment target, not a machine being avoided.** The objective is
*"deliver one Ubuntu KVM2 VPS deployed and verified DISARMED."* It is forbidden **as staging** only:
rehearsing the install on the target destroys the evidence the final deployment exists to produce —
after several half-finished attempts nobody can prove whether the working system is a clean install
or a survivor of leftovers. The programme's own line: *"a lab snapshot or agent uninstall is never
clean-host evidence."* Rehearse on the disposable VM; install on KVM2 once, cleanly.

Roughly 25 of the remaining 29.5 hours are this chain; KVM2 is the last ~8-hour slice.

Barış's standing authorisation already grants the WP-V deployment approval and the ARM gate in
advance — but every objective Gate A/B/C prerequisite still applies in full, and **the TESTNET phase
still needs its own pre-registration through one fresh Gate-5 audit before it may begin.** Tell him
before the KVM2 install starts even though the approval exists.

## 6. Standing safety boundaries — non-negotiable

- **DISARMED only.** No ARM, order, broker connection, network trading, TESTNET order, mainnet, or
  wallet action. Gate A touches no broker and sends no order.
- **No Ubuntu execution of any kind before Gate A.**
- **Live-capital actions are never pre-authorised.** If unsure whether something counts, it counts —
  stop and ask.
- Never invent position size, leverage, daily-loss, drawdown, liquidation thresholds, wallet
  selection, or credentials.
- Never print or send credentials, wallet secrets, API keys, or private infrastructure data to any
  model.
- **Do not modify system or security settings** (group membership, policy, elevation) even with
  owner approval — hand him the command instead.

**Git delegation:** commit, push, PR and merge to master are delegated to the Lead — act, then
report. Migration execution, deployment, P2RT, runtime, broker/TESTNET/mainnet, force-push and
starting a brand-new task still need Barış explicitly.

## 7. Auditor roster — real status

| Auditor | Status |
|---|---|
| `gpt-5.6-sol` xhigh | working; canonical |
| `claude-opus-5` xhigh | working; canonical. Hit a session limit once mid-cycle — plan around it |
| GLM-5.2 | **BLOCKED.** Route is `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GlmAudit.ps1` → `C:\Users\BarışSemaay\bin\glm.ps1` → Z.AI. **NOT Cline.** Re-probed 2026-08-02: `401 token expired or incorrect`. Owner must refresh `ZAI_GLM_CODING_PLAN_KEY` in Windows Credential Manager. **Never ask for a Z.AI key in Cline; never duplicate the credential.** |
| `cline-pass/deepseek-v4-flash` | unreliable — **four failed dispatches across two cycles, never once a verdict** (two timeouts, a non-TTY approval gate, a malformed provider stream). Opportunistic only, never round-gating. Do **not** loosen `--auto-approve` to make it run. |

Acceptance floor stays **both flagships accepting** plus no unresolved reproduced required finding.
An auditor that cannot execute the mandated suite must BLOCK — non-execution is never acceptance.

## 8. Lessons that cost the last cycle three rounds — apply them

1. **A generated test matrix can pass while proving nothing.** It happened twice: once masked by
   `UPDATE trades SET entry_px=100.0` (hiding the state every trade starts in), once by a fixture
   that starts `KILLED` and re-derives it, so the assertion restated the fixture. **Always ask what
   would make the assertion fail**, and prove it by running new tests against the *predecessor*
   commit and observing them fail.
2. **"Prove the enumeration complete" needs its boundary named.** Round 3 proved completeness over
   the `Store` call graph and never entered `OrderManager` — exactly where the defect lived.
3. **Publish the Lead's own reasoning in the audit brief so auditors can falsify it.** Two Lead
   arguments were broken that way, both correctly, and both would otherwise have shipped.
4. **Reproduce every auditor finding on real source before it binds.** Two Lead candidates did not
   reproduce and were dropped rather than spending a capped repair round.
5. **Fail-open is a different severity class than fail-closed.** One round produced an artifact that
   was *less* safe than its predecessor (ARM reachable after corruption). Watch for it when a fix
   changes exception types or handler ordering.

## 9. Operational hazards — each already cost a round or real money

1. **Prefix every implementation dispatch with the role override**, or Codex tries to delegate to
   Claude CLI, gets `ConnectionRefused`, and returns BLOCKED with zero edits.
2. **Codex cannot run Git** — `.git` is read-only for it. The Lead performs every Git operation.
3. **A hook flips `HEAD` back to `master`** between tool calls. Commit with one inline
   `checkout; add <explicit paths>; commit`.
4. **`git checkout master` fails** in the shared checkout — merge in a temporary worktree, push,
   remove it.
5. **Codex `--ephemeral -s read-only` cannot run pytest.** Give auditors a dedicated
   `workspace-write` worktree at the frozen SHA, then verify `git status --porcelain` is empty.
6. **`resilient_dispatch.sh` refuses to start unless the output path appears in the command args** —
   a missing `-o` once re-ran five complete `xhigh` audits (~$25).
7. **A provider content filter can kill an audit mid-run.** Frame audits as routine internal review of
   our own service and have them verify through the existing suite, not throwaway crash-simulation
   scripts.
8. **Verify artifact identity from the committed blob**, never the working copy — CRLF makes the
   on-disk hash differ. This already caused one false ledger-hash failure.
9. **Worktree residue:** `C:/WPSAUD6`, `C:/WPSAUD7` are deregistered from Git but their directories
   survive (ACL-locked `.pytest_cache`); `C:/WPSAUD5` is older residue. Harmless — do not escalate
   privileges over them.
10. **Bridge test contract**, from the relevant worktree's `IBKR_PAPER_BRIDGE`:
    `python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly`
    `--ignore` is mandatory (ACL-locked dir aborts collection). Never pass `--basetemp` inside
    `.pytest_cache` (623 errors once). Floor at master: **`2 failed, 1304 passed`** — the two
    pre-existing failures. **Do not "fix" them.** A third failure is a required finding.

## 10. Open owner actions

1. Confirm Hyper-V access works after re-login, or supply a staging VM another way.
2. Refresh `ZAI_GLM_CODING_PLAN_KEY` — needed for Audit 2's roster, not for Gate A.
3. Decide whether to schedule the TS-P1-010 deferred backlog (itemised in
   `11_TRIAGE/WPS_S3STRUCT_ACCEPTANCE_RECORD_2026-08-01.md`, including the one genuinely unrouted
   read in `_recover_applied_kill_flatten_lifecycles`, reachable only via `engine.kill()`).

Report in the repo-guard final format at the end of any task that touches the repo:
`branch / files changed / checks run / guard PASS|BLOCKED / commit / pushed / remaining dirty / next action`.
