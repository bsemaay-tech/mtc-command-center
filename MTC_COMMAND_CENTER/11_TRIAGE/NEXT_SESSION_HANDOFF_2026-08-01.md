# NEXT SESSION — HANDOFF PROMPT (2026-08-01)

Paste everything below the line as the next session's first message.

---

Repo: `C:\LAB\Tradingview_LAB_CLEAN`
Read `AGENTS.md`, then `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` (RESUME HERE),
then `MTC_COMMAND_CENTER/11_TRIAGE/WPS_S3STRUCT_ACCEPTANCE_RECORD_2026-08-01.md`.

You are Lead Orchestrator and acceptance authority. Codex CLI `gpt-5.6-sol` is the implementer.

## State — WP-S is DONE

- **S3-STRUCT ACCEPTED at `16cbc717`, MERGED to `origin/master` at `637307e8`** (2026-08-01).
  Both flagships accepting: `gpt-5.6-sol` xhigh PASS, `claude-opus-5` xhigh PASS-WITH-NITS, zero
  required findings. Ancestry verified for `16cbc717` and the accepted S2 `0c65a731`.
- Suite contract, from `C:/WPS/IBKR_PAPER_BRIDGE`:
  `python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly`
  Floor: **`2 failed, 1304 passed`**. The two failures (stale KVM2 ledger hash;
  `schema_version == "2"` vs default v4) are pre-existing on master and out of every allowlist.
  **Do not "fix" them.** A third failure is a required finding.
- **Audit 1 accepted → plan §23b step 7 no longer gates WP-L Phase 1.**
- DISARMED throughout. No broker, network, ARM, TESTNET, VPS or runtime action has occurred.

## The task — WP-L Phase 1, VERIFICATION ONLY (owner go-ahead still required before starting)

Finding **F-0-1** stands: the Linux package at `6fe0130f` is **already an ancestor of master and
byte-identical**. Nothing is ported. **No cross-branch Git operation occurs.** Phase 1 is confirming
that on real refs — not porting, not merging, not deploying.

Confirm and record: the `deploy/linux/` tree, lockfiles and the 35 Linux tests are reachable from
`origin/master` and byte-identical to `6fe0130f`; the Linux tests' current status; and whether
`test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate` (one of the two
known failures) is a stale fixture rather than a real defect.

**Do not start without Barış's explicit go-ahead.** Ask first.

## Owner actions outstanding

1. **Refresh `ZAI_GLM_CODING_PLAN_KEY`** in Windows Credential Manager. Auditor 4 returned
   `401 token expired or incorrect`. Its route is `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GlmAudit.ps1`
   → `C:\Users\BarışSemaay\bin\glm.ps1` → Z.AI. **NOT a Cline route — never ask for a Z.AI key in
   Cline, never duplicate the credential.**
2. Decide whether to schedule the TS-P1-010 deferrals (below) as a tracked task.

## TS-P1-010 deferred backlog — recorded, unscheduled

- Four of six new `except DurableRowFault` clauses are unexercised by the suite; the anti-downgrade
  property is proven at **2 of 6 sites**. Cheapest close: clean-ARMED parametrizations for a corrupt
  fill on a *sibling* cloid of the same trade, and a corrupt `fills.fee`/`funding` on the exit path.
- **The one genuinely unrouted read:** `_recover_applied_kill_flatten_lifecycles`
  (`orders.py:1649, 1653`, unguarded `int(order["trade_id"])` at `1701`) and `_kill_query_flatten`
  (`1307-1311`) convert raw rows outside the boundary; at `1654` a fault downgrades to
  `_KillEvidenceFault(AMBIGUOUS)` — same shape as round-3 R-1. Reachable only via `engine.kill()`,
  not from a queued event or `start()`.
- `BridgeEngine.start()` leg proved only by the matrix whose fixture starts `KILLED`.
- `_canonical_status`'s broad `except Exception: return str(raw_status)` never exercised.
- Containment handlers at `orders.py:2727-2728` and `3002-3007` never executed.
- int64 range check applied to `FINITE_FLOAT` columns · two reason codes for one storage-class fault ·
  asymmetric TEXT policy `INT64` vs `FINITE_FLOAT` · `trades.sl_initial`/`tp_initial` registry gap
  (`orders.py:3069-3071`, `:3186`) · raw reads in `record_kill_action_event`
  (`db.py:6162-6168`, `6665-6676`).

## Lessons that cost this cycle three rounds — apply them

1. **A generated matrix can pass while proving nothing.** It happened twice: once masked by
   `UPDATE trades SET entry_px=100.0`, once by a fixture that starts `KILLED` and re-derives it.
   **Always ask what would make the assertion fail**, and prove it by running new tests against the
   *predecessor* commit and observing them fail.
2. **"Prove the enumeration complete" needs its boundary named.** Round 3 proved completeness over the
   `Store` call graph and never entered `OrderManager` — exactly where the defect lived.
3. **Publish the Lead's reasoning in the audit brief so auditors can falsify it.** Two Lead arguments
   were broken that way, both correctly.
4. **Reproduce every auditor finding on real source before it binds** (D025 rule 2). Two Lead
   candidates did not reproduce and were dropped rather than spending a capped round.

## Operational hazards — each already cost a round or real money

1. Prefix every implementation dispatch with the role override, or Codex tries to delegate to Claude
   CLI, gets `ConnectionRefused`, and returns BLOCKED with zero edits.
2. **Codex cannot run Git.** The Lead does every Git operation.
3. A hook flips `HEAD` back to `master` between tool calls. Commit with one inline
   `checkout; add <explicit paths>; commit`.
4. `git checkout master` fails in the shared checkout — merge in a temporary worktree, push, remove.
5. Codex `--ephemeral -s read-only` cannot run pytest. Give auditors a dedicated `workspace-write`
   worktree at the frozen SHA, then verify `git status --porcelain` is empty.
6. `resilient_dispatch.sh` refuses to start unless the output path appears in the command args — a
   missing `-o` once re-ran five complete `xhigh` audits (~$25).
7. Frame audits as routine internal review and have them verify via the existing suite; a provider
   content filter once killed an audit triggered by a crash-simulation script.
8. **Auditor 3 (`cline-pass/deepseek-v4-flash`) has failed four dispatches across two cycles with no
   verdict** — two timeouts, a non-TTY approval gate (`--auto-approve false` refuses every tool), and
   a malformed provider stream. Budget it as opportunistic, never round-gating. Do **not** loosen
   `--auto-approve` to make it run.
9. Verify artifact identity from the committed blob, never the working copy — CRLF changes the
   on-disk hash.
10. `C:/WPSAUD6` and `C:/WPSAUD7` are deregistered from Git but their directories survive
    (ACL-locked `.pytest_cache`). Harmless residue — do not escalate privileges. `C:/WPSAUD5` is
    older residue at `732b37c3`.

## Standing safety boundaries — unchanged

DISARMED only. No ARM, order, broker, network, TESTNET, VPS or Ubuntu execution. No Ubuntu execution
of any kind before Gate A. Live-capital actions are never pre-authorised — if unsure whether
something counts, it counts: stop and ask. Never invent position size, leverage, daily-loss,
drawdown or liquidation thresholds, wallet selection, or credentials. Never print or send
credentials, wallet secrets, API keys, or private infrastructure data to any model.

Git delegation: commit, push, PR and merge to master are delegated to the Lead — act, then report.
Migration execution, deployment, P2RT, runtime, broker/TESTNET/mainnet, force-push, and starting a
new task still need Barış explicitly.
