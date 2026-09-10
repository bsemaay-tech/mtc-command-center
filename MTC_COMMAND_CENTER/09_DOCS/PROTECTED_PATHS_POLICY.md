# Protected Paths Policy

Protected targets:

```text
MTC_V2.pine
01_MASTER TEMPLATE_V2/01_PINE/
01_MASTER TEMPLATE_V2/00_PYTHON/
01_MASTER TEMPLATE_V2/05_PARITY/
Existing TradingView export archives
Canonical feature contracts
MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md
```

Modification gate:

1. Diagnosis report exists.
2. Patch plan exists.
3. Risk report exists.
4. User approval is recorded.
5. Commit message contains `APPROVED-PATCH-PLAN: <task_id>`.
6. Verification report is produced.

**The `APPROVED-PATCH-PLAN` trailer is a required practice, validated by hand. It is not currently
enforced by any mechanism.**

A script exists at `09_DOCS/hooks/protected_paths_hook.py` that implements the check, and it is
correct — given a commit message and a staged file list it finds the trailer and confirms the
`task_id` against an `APPROVED` or `COMPLETED` event in `02_TASKS/TASK_HISTORY.json`. **But it is
installed nowhere and invoked by nothing.** Measured 2026-09-10 under `HIST-2026-0032`:

| where a hook would have to live | measured |
|---|---|
| the repository's shared common gitdir `hooks/` | only `.sample` files |
| `core.hooksPath` (canonical repo and the `P012BATCH` worktree) | unset |
| any CI workflow under `.github/` | no reference to it |
| every other mention of it in the repository | documentation |

Worktrees share the common gitdir's hooks, so this is not a per-worktree gap — **it is repository
wide.** The requirement in step 5 above has therefore never been mechanically enforced, which is why
commits `d3a3fb88`, `fa7b92a3` and `2f1008ab` were able to modify canonical feature contracts with no
trailer and draw no objection. Nothing was watching.

### And installing it would not cover the paths this policy is used for

A second, independent gap, measured the same day by calling the script's own
`protected_patterns()` and `touches_protected()`:

```
patterns: MTC_V2.pine
          01_MASTER TEMPLATE_V2/{01_PINE,00_PYTHON,05_PARITY}/
          MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md
```

Tested against the files this policy has actually been invoked for:

| path | `touches_protected()` |
|---|---|
| `…/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json` | **no** |
| `…/corrected_vnext/verify_bceg.py` (the harness) | **no** |
| `…/core/economic_records/costs/HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json` | **no** |
| `09_DOCS/PROTECTED_PATHS_POLICY.md` | **no** |
| `02_TASKS/TASK_HISTORY.json` | **no** |

**So even installed, the script would not have guarded a single one of them.** The
`APPROVED-PATCH-PLAN` discipline applied to `contracts/` throughout the WP-P0-12 cycle rests on a
Lead ruling of 2026-09-09, not on anything this script implements.

**Worse, the policy cannot fix that by listing them.** `protected_patterns()` extends its defaults
with `[line for line in policy if line.startswith("01_MASTER")]` — **only** lines beginning
`01_MASTER`. Any other surface written into this document is silently ignored, and the current list
contains those three directories twice for exactly that reason. **Do not add a protected surface to
this file and assume it takes effect.**

**Until that changes, whoever commits to a protected path must validate the trailer themselves:** read
`02_TASKS/TASK_HISTORY.json` and confirm there is an event whose **`task_id`** equals the trailer value
and whose `event_type` is `APPROVED` or `COMPLETED`. Note that the script keys on `task_id`, **not**
`event_id` — the trailer is a value like `WP-P012-R30-REPAIR6`, not `HIST-2026-0024`.

**Do not cite this hook as a control that is in force.** If asked whether a protected-path commit was
guarded, the accurate answer is "by hand". Wiring it into CI, and/or installing it locally via
`core.hooksPath`, were both put to the owner on 2026-09-10 and **deliberately not chosen** — a
misconfigured gate on protected paths can block legitimate work, and a local hook silently affects
every worktree including other sessions' lanes. Enforcement remains an open decision.
