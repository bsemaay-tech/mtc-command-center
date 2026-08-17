# Dispatch prompt — Bridge Help truth cycle 2 repair

## Dispatch status and model gate

This is a **T3 dispatch-only artifact**. Creating or reading it does not launch Claude, authorize a review, accept the Help feature, commit any file, or authorize deployment or trading activity.

Use this prompt only in one fresh exact Claude Max counterpart session after the reported 03:20 route reset:

- model: exact `claude-opus-5`;
- effort: `high`;
- fresh session; never resume or continue a prior implementation/audit session;
- no fallback, alias, substitution, or silent downgrade.

Before editing, verify that the exact model and effort are actually available. If not, return `BLOCK` with zero changed bytes. A reported reset time is not proof of route readiness.

## Role

You are the counterpart implementer for a narrowly bounded T1 Help/Wiki truth repair. Work only in:

```text
C:\BRIDGE_HELP_IMPL
```

The worktree contains a valuable **uncommitted six-file prior-agent candidate**. Preserve it. Do not treat non-HEAD content as corruption and do not replace it with another checkout.

Read completely before editing:

```text
C:\LAB\Tradingview_LAB_CLEAN\AGENTS.md
C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\BRIDGE_HELP_TRUTH_CYCLE2_GATE1_2026-08-17.md
C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\BRIDGE_HELP_TRUTH_CYCLE2_T1_STATUS_2026-08-17.md
```

Then inspect the actual current six-file diff and the minimum relevant source in `C:\BRIDGE_HELP_IMPL`. Do not trust this prompt as a substitute for source inspection.

## Frozen candidate identity before repair

At dispatch preparation, the isolated worktree was at:

```text
5a81fea1b81243f8217f9d5326476e0eea3bc555
```

Its six candidate files and SHA-256 values were:

| File | Bytes | SHA-256 |
|---|---:|---|
| `IBKR_PAPER_BRIDGE/bridge/static/app.css` | 12,477 | `cd4dcb7071ce8265f612507d4cf268a1cf18bcdcf7602392cef1a082c147726a` |
| `IBKR_PAPER_BRIDGE/bridge/static/app.js` | 22,340 | `50d5385e9b9f67eb7394bd0bf7a0823c28db00f30d4d26b44a3517c30c9935e3` |
| `IBKR_PAPER_BRIDGE/bridge/static/index.html` | 6,379 | `e3b2d9feb6ee21958d1fea123072fa8c8356cf5f902c5f2f7e0731fb25acfc2e` |
| `IBKR_PAPER_BRIDGE/bridge/static/help_map.json` | 109,116 | `dfe2c2811cb738bf66d79a15e97dd8a2cb7fcc0a9df6f6693e2bccd35ce3f1bf` |
| `IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py` | 22,551 | `9474ab37334dcf63374de2edcdfcc1993f16719be3670d894a0c4e351e158e07` |
| `IBKR_PAPER_BRIDGE/docs/31_HELP_SYSTEM_MAP_INDEX.md` | 9,364 | `d53ca4598a90a8c007cd5a6f2e83f08564078e2a9b006fdc3fbaec25c7dbbe27` |

Reproduce HEAD, scoped status, bytes, and all six hashes before editing. If any value differs, do not reset it. Report the drift and inspect whether the requested repair can still be applied safely to the newer candidate. Stop `BLOCK` if ownership or intent is ambiguous.

Expected scoped status at prompt creation:

```text
 M IBKR_PAPER_BRIDGE/bridge/static/app.css
 M IBKR_PAPER_BRIDGE/bridge/static/app.js
 M IBKR_PAPER_BRIDGE/bridge/static/index.html
 M IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py
?? IBKR_PAPER_BRIDGE/bridge/static/help_map.json
?? IBKR_PAPER_BRIDGE/docs/31_HELP_SYSTEM_MAP_INDEX.md
```

## Exact writable scope

You may edit only:

```text
IBKR_PAPER_BRIDGE/bridge/static/help_map.json
IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py
IBKR_PAPER_BRIDGE/docs/31_HELP_SYSTEM_MAP_INDEX.md
```

`docs/31` should change only where required to remove the same false runtime/config claim or keep its maintenance rule consistent with the corrected tests.

All other files are read-only. In particular, the already-correct prior-agent changes in `app.css`, `app.js`, and `index.html` must retain their exact pre-repair hashes.

## Required source-truth repair A — configuration visibility is not activation

The Help must state all of the following together and without contradiction:

1. `bridge/api/routes.py` loads `config/bridge.yaml`, stores that configuration in `app.state.bridge_config`, exposes it through `/api/config`, and includes it in the dashboard snapshot.
2. `bridge/static/app.js` reads `state.snapshot.config` and displays `config.llm.veto_enabled` as the LLM veto mode.
3. Those read/serve/display paths do **not** activate a real LLM gate.
4. `bridge/app.py` constructs `BridgeEngine(...)` without an `llm_gate` argument.
5. `bridge/engine/engine.py` therefore installs `NullLLMGate`.
6. Changing `regime_enabled` or `veto_enabled` in the YAML does not wire or construct `LLMGate`; the current running engine still uses `NullLLMGate`.
7. A future wired gate could suppress or select otherwise permitted trades and therefore change outcomes, but it could never originate or enlarge an order.

Remove inherited false or overbroad statements such as:

- “Nothing in the running code reads the `llm:` block.”
- “No code reads those switches.”
- descriptions of the entire LLM page as empty when it already displays configuration-derived veto state.

It remains accurate to say that no **active LLM gate result/directive/model-call feed** populates the placeholder tables. Make the distinction explicit: configuration display exists; gate activation and model execution do not.

## Required source-truth repair B — generic skipped decision versus unwritten LLM artifacts

The Help must state all of the following together and without contradiction:

1. `NullLLMGate.check()` returns verdict `SKIPPED` with reason `llm disabled`.
2. After risk passes, `BridgeEngine` maps that verdict to stage `LLM_SKIPPED` and calls `store.insert_decision(...)` with a generic decision row containing the reason.
3. Therefore “nothing is logged” and “nothing is written today” are false when applied to the whole LLM stage.
4. The generic `LLM_SKIPPED` decision is **not** a directive record and is **not** a model-call record.
5. The `directives` and `llm_calls` schema tables exist, but the current dormant/null-gate path writes no directive rows and no model-call rows.
6. `llm_directive_id` belongs to the **`trades` row/schema**, not the `decisions` row. Do not say every decision records it as null.
7. Current order/trade persistence passes `llm_directive_id=None`; this does not turn the generic `LLM_SKIPPED` decision into an active directive.
8. Store/directive/model-call relationships for a future real gate remain planned, while the existing generic decision-stage evidence is operational.

Update every affected occurrence in `help_map.json`, including component details, Store wording, connection labels, evidence/rationale, and readiness prose. Do not fix only the first visible paragraph while leaving contradictions elsewhere.

## Truth that must remain unchanged

Preserve the already-correct Dashboard V1 wording and its tests:

- seven pages today: the **six original pages plus Help**;
- the Next Bar card shows the next bar's **UTC time**, not a live countdown;
- the server sends an initial WebSocket snapshot;
- `connectWs()` has no automatic close/error reconnect handler, so the browser does **not** automatically reconnect;
- the readiness gap is stated once rather than duplicated.

Do not broaden this repair into layout, controls, authentication, mobile design, reconnect implementation, Dashboard V2, or any runtime behavior change.

## D026 RED/GREEN requirement

The inherited tests currently encode the wrong wording, so a green-only edit is not closure evidence.

1. First change only `test_dashboard_static.py` to express the corrected source truth. Add or revise focused tests that positively require:
   - config load/serve/dashboard display **and** null-gate non-activation;
   - generic `LLM_SKIPPED` decision persistence **and** no directive/model-call records;
   - `llm_directive_id` as a trade-row field.
2. The tests must also reject the inherited false phrases/claims, including “nothing reads,” whole-stage “does not log anything/nothing is written,” and decision-row `llm_directive_id` attribution.
3. Run only the new/changed focused tests against the still-inherited `help_map.json`/`docs/31` wording. Record the real command, failing assertions, and exit code. This is the required **RED**.
4. Then repair `help_map.json` and, where necessary, `docs/31`.
5. Re-run the exact same focused tests and record the real command/output as **GREEN**.

Do not simulate RED by editing production/runtime source, removing fixtures, or weakening assertions. The RED must fail for the named inherited wording and the GREEN must pass for the corrected wording.

## Required validation after GREEN

Run from `C:\BRIDGE_HELP_IMPL` and report exact commands, outputs, exit codes, test counts, warnings, and durations:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py -q
node --check IBKR_PAPER_BRIDGE/bridge/static/app.js
git diff --check
python -m pytest IBKR_PAPER_BRIDGE/tests -q
```

For the full suite, classify every failure against the reproduced baseline rather than merely quoting a total. The current status record says the prior implementer observed **1,058 passed plus two pre-existing failures**: the canonical deployment-ledger fixture hash and WAL schema-version expectation (`4 != 2`). The round-1 read-only auditor could run 526 tests, reproduced the deployment-ledger failure, and had 533 temp-dependent setup errors caused by its sandbox. Reproduce the current writable-worktree baseline now; do not assume either old execution environment is identical.

Any new product failure is a blocker. Do not repair an unrelated failure or edit outside the allowlist.

Also verify structurally:

- `help_map.json` parses as JSON and retains unique component/area IDs and valid targets/sources;
- the existing six-original-pages-plus-Help/UTC/no-auto-reconnect tests still pass;
- no dependency, remote script, HTML injection, control authority, or economic action was added;
- only the three allowed files changed during this repair;
- `app.css`, `app.js`, and `index.html` hashes remain exactly equal to the frozen values above.

## Required final report

Return a compact implementation report containing:

1. exact model, effort, fresh-session evidence, worktree HEAD, and start/end times;
2. before and after `git status --short` for the complete worktree and the six candidate paths;
3. before and after byte counts and SHA-256 values for all six candidate files;
4. the exact changed-file list and a concise diff summary for each allowed file;
5. D026 RED and GREEN commands, real outputs, exit codes, and why the RED discriminates each inherited defect;
6. focused-suite, Node, diff-check, and full-suite commands/results;
7. classification of every full-suite failure as baseline, environment-caused, or new;
8. explicit confirmation that the three read-only candidate files retained their hashes;
9. explicit confirmation that no prohibited action occurred;
10. one implementation status: `READY_FOR_LEAD_INSPECTION` or `BLOCK`.

Do not return `PASS`; acceptance belongs to the Lead and the final permitted fresh T1 auditor.

## Prohibited actions

Do not:

- run `git checkout`, `git reset`, `git stash`, `git clean`, or any equivalent restoration/cleanup;
- stage, commit, amend, rebase, merge, create/delete refs, or transfer files;
- edit any file outside the three-file allowlist;
- deploy, contact Hostinger/KVM2/GATEA-STAGING, start/stop a service, or access credentials/secrets;
- ARM, DISARM, KILL, submit/cancel an order, contact a broker/exchange, or perform any economic action;
- change Bridge runtime, trading logic, risk logic, Pine, parity, MTC strategy behavior, configuration, schemas, or release identity;
- launch the final T1 audit yourself;
- conceal or overwrite prior-agent uncommitted work.

Stop and return `BLOCK` if the repair cannot be completed inside these rails.
