# CODEX APP TAKEOVER HANDOFF — CLAUDE QUOTA WINDOW (2026-08-02)

Paste everything below the line into a new Codex app task. It is deliberately standalone.

---

Repository: `C:\LAB\Tradingview_LAB_CLEAN`

You are the **Codex Lead Orchestrator, independent inspector, and temporary acceptance authority**
for the Gate A recovery programme. Work continuously and autonomously for as long as useful. Do not
stop merely to restate this handoff or ask about a routine decision that is already resolved below.

## 0. Read first; then distrust and verify

Read, in order:

1. `AGENTS.md`
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
4. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md`
5. `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-03.md`
6. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RESULT_2026-08-02.md`
7. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_RECON_DEFECT_LIST_2026-08-02.md`
8. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_REPAIR_VALIDATION_2026-08-02.md`
9. `MTC_COMMAND_CENTER/11_TRIAGE/DEFECT_3B_ROOT_CAUSE_2026-08-03.md`
10. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_3B_AUDIT_ROUND1_2026-08-03.md`
11. this handoff again after the canonical rules are loaded.

Do **not** trust this handoff blindly. Before acting, independently reproduce:

- canonical checkout branch, clean/dirty state, `HEAD`, `origin` refs, and ancestry;
- every relevant worktree, frozen SHA, and whether any process is still using it;
- current VM power state, current IP, SSH reachability, and target Python/SQLite versions;
- actual diffs and tests, not prose summaries;
- live account authentication/model availability before a new dispatch.

Use targeted `rg` and exact paths. Do not scan the frozen sibling repo
`C:\LAB\tradingview-lab`.

## 1. Temporary owner-authorized roster substitution

Claude Opus 5 quota is exhausted for approximately three hours. The owner explicitly authorizes
this **time-bounded emergency substitution** until Claude becomes available again, or until three
hours after this Codex task starts, whichever happens first:

- **Lead and acceptance authority:** this Codex app task, using `gpt-5.6-sol` with `xhigh` reasoning
  for all protected/re-audit decisions.
- **Implementer/coder:** a fresh isolated Codex CLI session on the `secondary` account through
  `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1`. Never use bare `codex`; never
  select, log out, or alter the desktop home `C:\Users\BarışSemaay\.codex`.
- **Cross-model auditor replacing unavailable Claude:** exact `GLM-5.2` through the Z.AI Coding Plan
  wrapper `C:\Users\BarışSemaay\bin\glm.ps1`, in a fresh session and an isolated audit worktree at
  the frozen candidate SHA.
- **Supplemental models when useful:** ClinePass `deepseek-v4-flash`, then `deepseek-v4-pro`, or the
  guarded DeepSeek/Grok driver. They may find issues but do not replace the Lead or the required
  GLM audit. Do not spend time on NVIDIA NIM unless its route is first proven end-to-end; it was not
  a verified launch route at handoff.

This temporarily overrides only the unavailable-counterpart and normal Claude flagship-floor rules.
It does **not** weaken D025 execution requirements, D026 RED/GREEN falsification, the three-round
limit, protected-surface scrutiny, evidence standards, or safety rails.

An isolated Codex subscription is quota/session isolation, **not cross-model independence**. A fresh
Codex session must not inherit implementer context and may supplement the Lead's inspection, but
GLM-5.2 is the cross-model auditor during this window.

For every commit accepted under this substitution, write the verdict exactly as:

`TEMPORARY OWNER-AUTHORIZED CODEX+GLM ACCEPTED — CLAUDE RETROSPECTIVE AUDIT OWED`

This label is honest provenance, not a normal canonical two-flagship claim. Continue the approved
programme after such acceptance; do not pause only because retrospective Claude review is owed.
When Claude returns, queue a fresh `claude-opus-5` xhigh audit of the frozen accepted SHA before final
merge to `master` or any KVM2 action. Never migrate a running job between accounts/models.

### Live routing facts measured immediately before this handoff

- `secondary`: logged in and is the launcher's default child route. The currently running build
  implementer accepted exact `gpt-5.6-sol` xhigh, but its process command line does not expose
  `CODEX_HOME`; re-check the parent launch record before attributing that run to an account.
- `free`: logged in, but a real probe returned that `gpt-5.6-sol` is not supported for that ChatGPT
  account. It cannot satisfy a flagship-model run; use only as a supplemental route with an explicitly
  available model if useful.
- `fourth`: logged in, but a real probe hit its usage limit and reported reset at
  `2026-08-08 08:49` local. Do not retry it in this window.
- desktop/default: reserved for this Codex app Lead. Never route a child CLI into it.
- GLM: a fresh real probe completed with canonical model `glm-5.2`, provider `firstParty`, exit 0,
  and no permission denials.

Quota is time-sensitive. Authentication alone does not reveal remaining quota. The reliable explicit
Codex wrapper form is:

```powershell
$args = @(
  'exec', '--ephemeral', '--sandbox', 'workspace-write',
  '-m', 'gpt-5.6-sol', '-c', 'model_reasoning_effort="xhigh"',
  '<prompt text or prompt-file content>'
)
& 'C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1' `
  -Account secondary -CodexArgs $args
```

Use `--sandbox read-only` for source-only audit; give the narrowest execution access that actually
allows the mandatory suite and SSH evidence. Do not give a child the canonical checkout as a writable
workspace.

## 2. Auditor execution contract — especially GLM

An auditor that cannot execute the mandated tests returns **BLOCK**. Reading the diff and repeating
the Lead's numbers is supplemental only, whatever verdict label it prints.

The existing `Invoke-GlmAudit.ps1` injects a strict read-only preamble that forbids creating any
file. That can make pytest/SSH evidence impossible. For an executing GLM audit, call `glm.ps1`
directly with a task prompt that:

- makes tracked source and Git history read-only;
- allows test-created files only in one exact disposable `--basetemp`/scratch path;
- permits read-only SSH to `GATEA-STAGING` using only the named local key path;
- forbids editing, staging, committing, branch switching, deployment, service start, credentials,
  broker access, ARM, and orders;
- requires raw commands, exit codes, meaningful output, final verdict, and final audit-worktree
  cleanliness proof.

Never paste or print a key value. The allowed local source is
`C:\HyperV\GATEA-STAGING\ssh\gatea_ed25519`; discover the current VM IP rather than trusting the old
`172.24.55.233`. If GLM still cannot execute, record BLOCK and do not convert its opinion into
acceptance. The Lead independently reproduces every required finding on real source before it binds.

For each regression test offered as closure evidence, require and audit:

1. **RED** against the exact parent/reverted defect, or a behaviorally equivalent deliberate
   mutation;
2. **GREEN** with the fix;
3. the exact commands and real output in the evidence record.

String matching a source literal is not behavioral closure evidence.

## 3. Verified starting anchors — re-check them

At handoff creation:

- canonical checkout `C:\LAB\Tradingview_LAB_CLEAN` was clean on
  `feature/donchian-crypto-ladder` at `5802b07e6c2b6110bd3398a5033535f7d73c0b57`, matching origin;
- `origin/master` was `637307e83951ffe23e768ed8e50ddaf8712b0660`;
- build branch/worktree:
  `codex/gate-a-build-determinism` / `C:\GATEAFIX` at pushed `7be1c429f70ed17c3f38a14d43e514495b2b64bd`;
- defect-3b branch/worktree:
  `codex/wal-bundle-linux-sidecars` / `C:\GA3B` at pushed
  `df00634fc2e5fb19cddb34a6ad16d9764c4779a4`;
- detached audit worktrees existed at `C:\GAAUD_CODEX`, `C:\GAAUD_CLAUDE`, and `C:\GAAUD_3B`;
- `GATEA-STAGING` is the retained disposable Ubuntu host;
- `KVM2-Ubuntu-2404-Staging` remains powered off and quarantined; the real KVM2 path remains out of
  scope.

At handoff creation a Codex CLI process was **actively editing `C:\GATEAFIX`** for build repair
round 2. Its tracked diff touched only:

- `IBKR_PAPER_BRIDGE/deploy/linux/package.sh`
- `IBKR_PAPER_BRIDGE/tests/test_linux_deployment.py`

Do not launch another writer, clean the worktree, switch it, or kill that process. Rediscover the
process and wait for its atomic result. If it has exited, collect its output and inspect all residue
before deciding whether anything is stale. Existing uncommitted changes belong to that implementer.

## 4. Execution queue — proceed automatically

### Queue A — collect and adjudicate defect 3b round 1 repair

Candidate `df00634f` keeps the correct table-reading attachment fix and adds fail-closed protection
for the crashed-writer state. The prior `f1ac2565` audit found a severe regression: writable SQLite
silently created `-shm` and accepted a hot WAL, while the test was vacuous. Read the round-1 audit
record and independently inspect the new diff.

Required closure evidence on Linux/Python 3.12.3/SQLite 3.45.1 includes:

- full `tests/test_wal_state_bundle.py` green (last reported: `45 passed, 0 failed`);
- real crashed-writer source `db + non-empty -wal + no -shm` rejected before any connection opens,
  with no tool-created `-shm` and no bundle;
- deliberate mutation from the real table read to constant `SELECT 2` makes both new guard tests
  RED and restores the 25-failure symptom;
- genuine concurrent-writer detection remains active;
- schema/manifest version unchanged;
- clean source and audit worktrees.

Dispatch a fresh GLM-5.2 executing audit and perform the Lead's own independent audit. A fresh
isolated Codex read-only audit may supplement this if it can run the Linux suite. Apply D025/D026.
If accepted, record/commit/push the temporary acceptance record. If non-accepting, send one focused
repair prompt to the same Codex implementer and respect the branch's own maximum-three-round count.

After 3b, run the full locked Python 3.12 suite. The expected remaining known floor is two
`order_state` gc-referent failures, not zero by assumption. Record the actual floor. Do not alter
tests merely to make the count green; scope defect 3a separately if the gate contract requires more
than a re-established baseline.

### Queue B — collect build repair round 2, then audit it

The running implementer is repairing build round 2 on top of `7be1c429`. Required items are already
in its prompt: bind the CR guard's deployment-directory arm; non-vacuous FIFO and missing-root tests;
non-vacuous CRLF/metacharacter test; behavioral two-locale, `tar.umask`, and inventory-divergence
tests; early partial-`mktemp` cleanup; honest GNU dependencies; D026 RED/GREEN for every new test;
focused and full floors; clean residue.

When it finishes:

1. inspect the exact diff and process output;
2. reproduce RED/GREEN and relevant builds yourself, including Linux evidence;
3. remove only exact, verified, task-created residue after proving its path; never broad-clean;
4. commit and push only explicit accepted files;
5. freeze the SHA and dispatch GLM-5.2 plus a fresh isolated Codex audit session;
6. reproduce every required finding before sending a repair.

This branch is currently in **repair round 2 of 3**. If its round-2 audit is non-accepting, one final
focused repair/re-audit round 3 is permitted. If round 3 is non-accepting, STOP this branch and report;
never enter round 4. A test-quality defect in evidence claimed by this same repair counts in its
round. Only a demonstrably unrelated, pre-existing baseline issue may be tracked separately.

### Queue C — implement defect 4 after an implementer slot is free

The owner already selected and confirms: **add an explicit credential-free DISARMED start mode.**
Do not ask this again and do not move A-4 after Stage D.

First independently scope the actual startup path. Corrected root location: the credential raise is
in `settings.py:113`; `HyperliquidBroker.__init__` stores empty strings and does not raise there.

Protected-surface requirements:

- the mode is explicit and fail-closed, not the silent new default for normal operation;
- no broker object that can connect or trade is constructed in credential-free mode;
- no broker/exchange/network connection and no credential lookup are attempted;
- service/API can start and truthfully report DISARMED;
- ARM requests are rejected without credentials and without economic effect;
- ordinary credentialed behavior and all existing safety gates remain unchanged;
- tests show RED on the parent behavior and GREEN on the repair;
- no fake credential is used to make A-4 pass.

Use the secondary Codex CLI as implementer in a fresh dedicated branch/worktree, one writer only.
Use GLM-5.2 as executing cross-model auditor and the Codex app Lead as independent acceptance
authority. If GLM implements any fallback task, it cannot audit that same task; preserve role
separation and use a fresh independent model/session for review.

### Queue D — integrate, rebuild once, rerun Gate A from A-0

Proceed only after build, 3b, defect 4, and the real Python-3.12 floor are accepted and recorded.
Create a clean integration branch/worktree from the verified base and bring in only the exact
accepted commits. Do not merge to `master` during the temporary roster window.

The owner authorizes one corrected candidate rebuild and a full Gate A rerun on `GATEA-STAGING`:

- old release `1adf9ae51b0ddfe81057860aec5c23bb842f5a84` and manifest
  `bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02` remain historical;
- build once from a clean, frozen integration SHA and record new release/manifest hashes;
- transfer and verify identity, then rerun the preregistered Gate A from **A-0**;
- do not reuse earlier A-3...A-9 reconnaissance as gate evidence;
- A-4 PASS requires a live service in the explicit credential-free DISARMED mode and a real ARM
  rejection; connection-refused is FAIL, never PASS;
- stop at the first preregistered failure and preserve exact evidence.

Commit/push scoped branches and evidence records as each atomic unit is accepted. Do not merge to
`master`, touch KVM2, begin WP-V, or deploy beyond the disposable `GATEA-STAGING` host during this
temporary window.

## 5. Safety rails and hard stops

- DISARMED only. No broker connection, order, cancel, fill, TESTNET, mainnet, wallet, ARM transition,
  or live-capital action.
- Never request, read, print, copy, or log broker/API/wallet credential values. An SSH private key may
  be used by path only; never display its contents.
- Do not start, modify, install to, delete, or power on KVM2 or
  `KVM2-Ubuntu-2404-Staging`.
- No destructive Git, no force push, no broad cleanup, no `git add .`/`git add -A`.
- Never allow concurrent writers in the same worktree or uncommitted same-file handoff between
  agents.
- A canonical/substitute auditor that cannot execute required evidence is BLOCK.
- A third non-accepting repair/re-audit result stops that task.
- Stop for the owner only on live-capital authority, a genuine destructive/identity ambiguity,
  exhausted repair round, or a blocker that survives safe alternatives. Batch non-blocking questions
  into the durable record and continue other independent queue items.

## 6. Durable work and handback

Use `codeburn status` at takeover and handback. After every accepted atomic unit, update the relevant
`11_TRIAGE` evidence record plus `_AI_MEMORY/GLOBAL_HANDOFF.md` and `_AI_MEMORY/NEXT_STEPS.md`, commit
explicit files, run the repo guard, and push. Report real commands, outputs, exit codes, model, account
route, frozen SHA, round number, safety boundary, elapsed wall time, and measurable calls/cost; never
invent token totals.

When Claude becomes available, finish the current atomic operation, do not migrate it mid-flight,
then write a standalone retrospective-audit handoff listing every temporarily accepted frozen SHA and
the exact unreviewed evidence. Continue productive independent work until that boundary or a hard stop.
