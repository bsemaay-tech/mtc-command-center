# WP-P0-19 — Pine de-fang T0 authorization package

**Date:** 2026-08-25

**Design package:** WP-P0-19, T2, design only

**Future implementation package:** WP-P0-23, T0, gate G2

**Prepared on:** `feature/wp-p0-19-pine-defang-design-20260825` at starting HEAD `46f5bafbf82f3366c8bc7ee08f6f0eee08d46138`

**Freeze source:** annotated tag `legacy/pine-controller/2026-08-25`, tag object `3075bd66547f5ade903a570cb54a49e3ef197328`, peeled commit `77a10e6573d93f8aaf777010ea507bbec0a7668b`

## 1. Decision the owner is being asked to make

This document does **not** authorize or perform the change. It gives the owner an exact,
bounded choice for the later WP-P0-23 package:

- **AUTHORIZE:** permit WP-P0-23 to make only the changes in section 3, under T0/G2,
  followed by its required T0 audit and acceptance record.
- **REFUSE / DEFER:** make no source, configuration, guard, or CI change. The existing Pine
  controller and its two alert emissions remain active; F-8 remains open.

Authorization of this package is not deployment, TradingView publication, paper/testnet,
live, broker, credential, or trading authorization. WP-P0-23 may not push, deploy, publish a
Pine revision, create a TradingView alert, or contact a host or venue under this decision.

## 2. Exact intended end state

1. The **one maintained active Pine source** remains
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine`.
2. That file is transformed **in place**. No `MTC_V2_VIEW.pine`, visualization copy, renamed
   alert-capable original, or second maintained active Pine source is created.
3. A comment at its head says `VISUALIZATION ONLY — NOT A CONTROLLER`; its existing strategy
   title and all calculation, order-simulation, plotting, table, label, and render logic remain
   unchanged.
4. Its 13 `wt_*` UI inputs and the complete L25 WunderTrading dispatch block are absent.
   Consequently it compiles without dangling `wt_*` references and contains no `alert(`.
5. Across the whole checked-out repository, every `.pine` file is scanned and **zero** files
   contain the literal byte sequence `alert(`. The allowlist is literally empty.
6. The matching 13 `wt_*` defaults and their validation logic are absent from the canonical
   Python configuration. The optimization-only `integrations_disabled` compatibility switch
   remains accepted as an empty no-op so existing optimization profiles do not emit removed,
   now-unknown keys.
7. The original controller remains recoverable from the immutable freeze tag. It does not
   remain in the active tree.

## 3. Exact WP-P0-23 file and current-line authorization list

Line numbers below are against starting HEAD `46f5bafb…`. Deletions shift later line numbers;
implement from the named current anchors, not from post-edit numbers. `NEW — entire file`
means the owner authorizes creation of exactly that file to satisfy the stated contract.

| File | Current lines / anchor | Exact authorized transformation | Why required |
|---|---:|---|---|
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine` | insert after line 1 | Add comment header `// VISUALIZATION ONLY — NOT A CONTROLLER`. Do not change line 7's `strategy(...)` declaration or title. | Makes the active file's non-controller role explicit without changing rendering. |
| same | 176–188 | Delete the 13 `wt_*` input declarations, and nothing adjacent. | Removes the Pine integration UI surface. |
| same | 2007–2028 | Delete the complete `SECTION 9 - WUNDERTRADING ALERT DISPATCH (L25)` header and body. The two `alert()` emissions are current lines 2020 and 2028. | Deleting only 2020/2028 or only the inputs would leave dead or uncompilable dispatch code. This bounded block is the complete routing surface. |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py` | 225–238 | Delete the `# L25 - WunderTrading` comment and all 13 `wt_*` defaults. | Removes the 13 canonical Python keys. |
| same | 568–584 | Delete the complete `# L25 - WunderTrading` validation block. | Required fallout: validation otherwise indexes defaults that were removed and makes ordinary config validation fail. |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/tools/optimization_parameter_mapper.py` | 48–57 | Replace the `integrations_disabled` dictionary, which currently emits eight removed `wt_*` keys, with the exact compatibility no-op `"integrations_disabled": {},`. | Active optimization callers still pass this bundle flag. An empty bundle consumes the legacy flag without emitting unknown config keys or widening the change across seven callers. |
| same | 87 | Replace the stale note about integration bundles being fixed off with a note that `integrations_disabled` is a compatibility no-op after Pine de-fanging. | Prevents the mapper metadata from claiming a live integration surface still exists. |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/tests/test_optimizer_post_run_patches.py` | after current line 54 | Add an assertion that `overrides` contains no key whose name starts with `wt_`, before the existing `validate_config(merged)` call. | Locks the necessary mapper fallout and keeps the existing end-to-end validation meaningful. |
| `MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py` | **NEW — entire file** | Add the fail-closed, cross-platform repository scanner specified in section 6. | Single guard implementation used locally and by CI. |
| `MTC_COMMAND_CENTER/tools/repo_guard.ps1` | insert between current lines 155 and 157, before the unpushed-commit check | Invoke `python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py`; print its output; add a blocking reason when it is nonzero or cannot execute. Renumber following comments only as needed. | Makes the same invariant part of the canonical local repo guard. Inability to execute is BLOCK, never PASS. |
| `.github/workflows/pine-defang-guard.yml` | **NEW — entire file** | Add the required GitHub Actions job specified in section 6. | The repository currently has no root-level workflow; nested historical workflows are not a root CI gate. This creates the real CI carrier. |

No other file or line is authorized by this package. In particular, it does not authorize
changes to other Pine files, plot/order logic, `strategy(...)`, parity fixtures, core trading
logic, the seven `tw_*` keys, deployment files, hosts, or TradingView state.

### Why the mapper lines are named

A repo-wide non-document sweep found one additional Python producer of removed `wt_*` names:
`optimization_parameter_mapper.py:48-57`. `validate_config()` rejects unknown keys at
`config.py:249-253`. Removing the defaults while leaving that producer unchanged would make
the active `integrations_disabled=True` optimization profiles emit invalid configuration.
Keeping the flag as an empty compatibility no-op is the smallest bounded repair: it avoids
touching its seven active callers and emits none of the retired keys.

## 4. The 13-to-13 removal mapping

Every Pine input has exactly one matching Python default. The Python validation column names
the current validation lines that must disappear where a validator exists; the five alert
code strings have no dedicated type check today.

| # | Pine input and current line | Python default and current line | Python validation at current HEAD |
|---:|---|---|---|
| 1 | `wt_enter_long_code` — `MTC_V2.pine:176` | `config.py:226` | none |
| 2 | `wt_exit_long_code` — `MTC_V2.pine:177` | `config.py:227` | none |
| 3 | `wt_enter_short_code` — `MTC_V2.pine:178` | `config.py:228` | none |
| 4 | `wt_exit_short_code` — `MTC_V2.pine:179` | `config.py:229` | none |
| 5 | `wt_exit_all_code` — `MTC_V2.pine:180` | `config.py:230` | none |
| 6 | `wt_order_type` — `MTC_V2.pine:181` | `config.py:231` | `config.py:569-571` |
| 7 | `wt_amount_type` — `MTC_V2.pine:182` | `config.py:232` | `config.py:572-574` |
| 8 | `wt_amount` — `MTC_V2.pine:183` | `config.py:233` | `config.py:575` |
| 9 | `wt_leverage` — `MTC_V2.pine:184` | `config.py:234` | `config.py:576` |
| 10 | `wt_use_tp` — `MTC_V2.pine:185` | `config.py:235` | `config.py:577,581-582` |
| 11 | `wt_use_sl` — `MTC_V2.pine:186` | `config.py:236` | `config.py:578,583-584` |
| 12 | `wt_reduce_only` — `MTC_V2.pine:187` | `config.py:237` | `config.py:579` |
| 13 | `wt_place_cond_orders` — `MTC_V2.pine:188` | `config.py:238` | `config.py:580` |

After the authorized edit, a repo-wide non-document `wt_*` sweep may find historical evidence
or prose, but it must find no live source occurrence in `MTC_V2.pine`, `config.py`, or the
mapper's bundle values. The acceptance-bearing checks are the exact source assertions in
section 9.

## 5. Explicit `tw_*` exclusion — mandatory authority boundary

The following seven keys are **OUT OF SCOPE** for WP-P0-19 and WP-P0-23. They belong to the
kernel consolidation chain WP-P0-09 → WP-P0-10 → WP-P0-11 → WP-P0-12:

| Key | Status from brief F-8a |
|---|---|
| `tw_audit_semantics_mode` | behaviourally active; changes quantity rounding |
| `tw_reversal_reentry_mode` | behaviourally active; gates re-entry |
| `tw_reversal_reentry_delay_bars` | behaviourally active; changes re-entry timing |
| `tw_margin_call_mode` | behaviourally active; changes the margin-call branch |
| `tw_margin_call_split_entries` | `[DRIFT/UNKNOWN]`; required, validated, read and stamped, with no located behavioural branch |
| `tw_be_semantics_mode` | behaviourally active; changes break-even trigger bar/type |
| `tw_trailing_semantics_mode` | behaviourally active; changes trailing trigger bar/type |

These are **not inert cleanup**. Six have verified economic consumers. The seventh has an
unresolved behavioural status and cannot be deleted on an absence-of-evidence claim. WP-P0-23
must prove the seven declarations at `config.py:58-64`, required-key checks at `:282-288`, and
their later validation/consumers remain byte-unmodified by its diff.

## 6. Empty-allowlist CI guard specification

### 6.1 Scanner contract

`MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py` must:

1. Resolve the Git root with `git rev-parse --show-toplevel`; inability to resolve it is a
   nonzero **BLOCK**, not a clean result.
2. Walk the entire checked-out repository root recursively, excluding only `.git` metadata.
   It must include tracked and untracked `.pine` files and paths containing spaces.
3. Read each `.pine` file as bytes and search for the literal ASCII byte sequence `alert(`.
   This deliberately catches code, comments, mixed case only when exact, and any location in
   the file. It is a simple policy invariant, not a Pine parser.
4. Use an explicit immutable allowlist whose value is empty. There is no path, generated-file,
   example, archive, or comment exception.
5. Print every violating repository-relative path in deterministic ordinal order and exit
   nonzero if at least one exists.
6. Exit nonzero on enumeration, stat, open, or read failure and name the unevaluated path.
   Zero matches because scanning failed is never PASS.
7. Print a terminal line such as `PINE_ALERT_GUARD PASS files=<n> matches=0 allowlist=0` only
   after all candidate files were read successfully. A violation terminal line must include
   `matches=<n>` and return nonzero.

The policy predicate is equivalent to the following independent repository-root check:

```powershell
$hits = @(rg -l -F --glob '*.pine' 'alert(' .)
if ($LASTEXITCODE -notin 0,1) { throw "pine scan could not be evaluated: rc=$LASTEXITCODE" }
if ($hits.Count -ne 0) { $hits; throw "pine alert allowlist is empty" }
```

The Python scanner, not shell-specific grep behavior, is the CI authority. The independent
`rg` command is an audit cross-check.

### 6.2 CI carrier

`.github/workflows/pine-defang-guard.yml` must:

- trigger on every `pull_request` and every push (no path filter that could omit a new `.pine`);
- use `actions/checkout@v4` and `actions/setup-python@v5` with Python 3.11 or newer;
- run only `python MTC_COMMAND_CENTER/tools/check_no_pine_alerts.py` for this job;
- have a bounded timeout of five minutes;
- grant read-only repository contents permission;
- expose no secret and perform no network action other than standard GitHub runner actions;
- fail the job on any nonzero scanner exit.

The local `repo_guard.ps1` call and CI job must invoke the same scanner. There must not be a
second implementation with a different scope or allowlist.

### 6.3 D026 RED/GREEN proof required from WP-P0-23

The implementation evidence must record literal commands, stdout/stderr, and exit codes for
all three arms below. Specifications or asserted outcomes do not count.

1. **RED — exact pre-fix behavior.** Run the new scanner before deleting the existing dispatch
   block. It must return nonzero and name
   `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine` with two matches.
2. **RED — arbitrary-tree falsification.** After the real source is clean, create one temporary
   `.pine` probe under the checked-out repository but outside `01_PINE`, containing the literal
   `alert(`. The scanner must return nonzero and name that exact probe. This proves the guard is
   repo-wide rather than hard-coded to the controller path. Remove the probe and prove `git
   status --short` contains no residue.
3. **GREEN — repaired state.** Run the identical scanner after removal. It must return zero and
   report `matches=0 allowlist=0`. Independently run the `rg` cross-check and record an empty
   result with `rg` exit 1 (the documented no-match status), not mistake exit 1 for tool failure.

A test that merely asserts the scanner's source contains `alert(`, or a test that scans only a
fixture directory, is supplemental and does not satisfy D026.

## 7. In-place Pine transformation plan

The implementation order is intentionally narrow:

1. Reconfirm the tag and current protected-file blob identities from section 8 before editing.
2. Capture the **before** render evidence in section 7.1 from the tag-frozen source.
3. Add only the non-executable visualization-only header comment after `//@version=6`.
4. Delete current lines 176–188.
5. Delete current lines 2007–2028 as one unit. This removes the two calls and every variable
   whose sole purpose is to construct their payloads.
6. Make the exact Python, mapper, test, scanner, repo-guard, and CI changes in section 3.
7. Compile the active Pine source in TradingView. A compile warning/error is non-acceptance.
8. Produce the D026 evidence, render-identity evidence, configuration tests, exact-scope diff,
   and rollback walk. Then submit the complete package to the T0 audit. Do not publish or deploy.

### 7.1 Render-identity acceptance criteria

Use a duplicated TradingView chart layout so both scripts see the same provider bars:

- symbol: `BINANCE:BTCUSDT.P`;
- timeframe: `60` minutes;
- reference dataset identity:
  `MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/01_TW_CHART_DATA/BINANCE_BTCUSDT.P, 60_consolidated_stable.csv`;
- tracked blob: `fc5bf84369bc163a3d51bef0993bcfb9a64a2fa7`;
- SHA-256: `0e6c540065690ba1ce00f4d03ad65881569d974d50e02bdd305f1048604d9a99`;
- 24,524 data rows plus header, from Unix time `1685314800` through `1773597600`;
- before source: `MTC_V2.pine` blob
  `96cb361eafc04cd7e57fe2e138696c2ffd4f46e1` from the freeze tag;
- after source: the WP-P0-23 candidate;
- inputs: every surviving input identical between the two instances; the 13 removed `wt_*`
  inputs in the before instance remain at their committed defaults (all codes empty and the
  remaining values as lines 181–188 declare).

Acceptance requires all of the following:

1. Both versions compile on the same Pine v6 engine and load the complete fixed interval.
2. Exported chart data have the same timestamps and byte-equivalent values, including `na`
   positions, for every series emitted by the script after excluding only platform-generated
   instance-name metadata. Column names and column count must otherwise match.
3. Strategy Tester order/trade count and every order timestamp, direction, quantity, and price
   are identical. The de-fang change removes routing side effects, not simulated strategy orders.
4. With the same viewport, theme, scale, timezone, symbol session, and input vector, before/after
   screenshots show identical candles, plot locations, colors, fills, shapes, labels, tables,
   and strategy order markers. The added source comment is not a rendered difference.
5. A machine-readable comparison reports zero differing cells and zero missing/extra render
   series. A screenshot alone is supplemental; numeric export identity is acceptance-bearing.
6. The after source exposes none of the 13 WunderTrading inputs and cannot create a Pine alert
   through an `alert()` call. This expected UI removal is not treated as a render mismatch.

Any unexplained render, simulated-order, or export difference is `REQUEST_CHANGES`; it is not
waived because the source diff appears limited to alert code.

## 8. Rollback from the freeze tag — walked in design

### 8.1 Evidence that the rollback source is usable now

Read-only checks performed for this design established:

- the requested annotated tag exists and peels to `77a10e6573d93f8aaf777010ea507bbec0a7668b`;
- tag and HEAD Pine blobs are both `96cb361eafc04cd7e57fe2e138696c2ffd4f46e1`;
- tag and HEAD config blobs are both `e472d0ac3e6df99c17e90195b620feae12acfd1f`;
- `git diff --exit-code legacy/pine-controller/2026-08-25 HEAD -- <the two protected paths>`
  returned zero;
- tag content contains exactly two `alert(` calls, 13 `wt_*` Pine inputs, and 13 `wt_*`
  Python defaults.

The brief's older example tag `legacy/mtc-v2-pine-controller-2026-08-21` is **not** the rollback
authority for this package. WP-P0-02 supplied the merged, owner-named
`legacy/pine-controller/2026-08-25`, and this design uses that exact ref.

### 8.2 Exact emergency restore walk for WP-P0-23

This walk must be rehearsed in a disposable branch/worktree after the candidate commit and its
real output recorded. It must never be run in an armed/live window.

```powershell
$tag = 'legacy/pine-controller/2026-08-25'
$pine = 'MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine'
$config = 'MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/config.py'

git rev-parse "refs/tags/$tag^{commit}"
git status --short
git restore --source=$tag --worktree -- $pine $config
git diff -- $pine $config
git hash-object $pine
git hash-object $config
rg -n -F --glob '*.pine' 'alert(' .
git status --short
```

Expected restored hashes are the two tag blobs above. The `rg` command must name the restored
controller with two matches. The empty-allowlist guard must therefore turn **RED** after an
emergency controller restore: that is an intentional, visible indication that the second order
path has been reinstated, not a reason to weaken or delete the guard.

The rehearsal then returns the disposable worktree to the candidate commit and reruns the guard
GREEN. A real rollback requires a new owner authorization naming the emergency reason, an exact
restore commit, and the normal audit/acceptance path before any publication. Restoring source
bytes does not itself create TradingView alerts or deploy anything.

## 9. WP-P0-23 acceptance checklist

All items are cumulative:

- [ ] Owner explicitly authorized WP-P0-23 at T0/G2 against this exact file/line package.
- [ ] Freeze tag resolves to the recorded commit and protected blobs before the first edit.
- [ ] Diff touches only the files and anchors in section 3.
- [ ] Exactly one maintained active Pine source exists: `MTC_V2.pine`.
- [ ] Pine compiles; lines 176–188 and 2007–2028 are gone; no dangling `wt_*` reference exists.
- [ ] Repo-wide scanner and independent `rg` check find zero `.pine` files containing `alert(`;
  allowlist size is zero.
- [ ] D026 pre-fix RED, arbitrary-tree RED, and repaired GREEN all ran with real recorded output.
- [ ] The 13 Python defaults and the complete L25 validation block are gone.
- [ ] The mapper consumes `integrations_disabled` as an empty no-op and emits no `wt_*` key;
  its existing validation test is GREEN with the new assertion.
- [ ] All seven `tw_*` declarations, validators, and consumers are untouched.
- [ ] Render identity passes every criterion in section 7.1 on the fixed chart/dataset.
- [ ] Rollback was walked in a disposable worktree and restored both exact tag blob hashes;
  the expected post-restore guard RED was recorded.
- [ ] Required T0 auditors and Lead independent acceptance completed with no unresolved
  reproduced required finding.
- [ ] No push, deployment, TradingView publication, alert creation, host/venue action, or
  credential action was inferred from source acceptance.

## 10. Divergence-alarm specification — later WP-V4-07, not WP-P0-23

WP-P0-23 must not implement this alarm. It is the separate T1 package WP-V4-07 and depends on
accepted WP-P0-23. Its bounded design contract is:

- **Subject:** compare the visualization-only Pine output with canonical-kernel output for the
  same closed bars, symbol, timeframe, dataset identity, configuration identity, and version.
- **Threshold:** one or more differing values on any agreed comparison series on a fully closed
  bar is `DRIFT`; missing identity, missing data, or inability to compare is `UNKNOWN`, never
  PASS. No tolerance is applied to discrete signals; any numeric tolerance must be named per
  series before implementation and may not conceal a discrete mismatch.
- **Schedule:** run after each newly closed source bar plus a 15-second ingestion allowance;
  perform one daily full-window reconciliation. Duplicate results for the same comparison
  identity are deduplicated.
- **Notification path:** persist a structured divergence incident to the canonical incident/read
  model, show it on the dashboard exception strip, and send it through the platform's one
  notification-only owner channel. The channel carries no key and no control. Repository records
  say no active live alerting is currently proven, so WP-V4-07 must bind and delivery-test that
  single channel rather than assume Telegram or any other route is live.
- **Failure behavior:** alarm only. It submits no order, intent, ARM, DISARM, KILL, FLATTEN, or
  configuration change. Pine remains a non-controller.
- **Falsification:** a deliberate one-bar output mutation must create the structured incident,
  dashboard exception, and delivered notification; removing it must clear only after a fresh
  successful comparison. Acknowledging a notification does not clear the underlying fault.

The exact external notification channel is a named implementation prerequisite for WP-V4-07;
it is not invented or activated by this design package.

## 11. Owner decision record

Choose one; absence of a choice means **not authorized**.

- [ ] **AUTHORIZE WP-P0-23** exactly as sections 2–9 specify, under T0/G2. This still grants no
  push, deployment, TradingView publication, host/venue, credential, testnet, or live authority.
- [ ] **REFUSE / DEFER WP-P0-23.** Leave the active controller unchanged.

Owner: ____________________  Date/time: ____________________  Exact candidate/base acknowledged: ____________________
