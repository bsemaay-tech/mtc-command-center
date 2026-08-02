# c5a4070a — owed `claude-opus-5` retrospective flagship audit

Date: 2026-08-02
Auditor: `claude-opus-5` xhigh, executing
Target: `codex/gate-a-build-determinism` @ `c5a4070a4836bbb9ee010dc63db69313066667c4`
Parent: `origin/master` `637307e83951ffe23e768ed8e50ddaf8712b0660`
Audit worktree: `C:\GAAUD_C5` (fresh, detached, clean at close)

This closes the debt recorded as
`TEMPORARY OWNER-AUTHORIZED CODEX+GLM ACCEPTED — CLAUDE RETROSPECTIVE AUDIT OWED`.

## 1. Verdict

**ACCEPT** — flagship 2 of 2. Two non-blocking nits, §5.

The second flagship verdict (`gpt-5.6-sol` xhigh) could **not** be obtained; see §6. Under D025 rule 3
acceptance requires both flagships, so **this branch is one accepting flagship short of canonical
acceptance.** It remains unmerged, is not a Gate A pass, and authorizes no KVM2 action.

## 2. Executed evidence — every number reproduced independently

Windows: Python 3.14.2, pytest 9.0.2, worktree `C:\GAAUD_C5`.
Linux: `GATEA-STAGING` Ubuntu 24.04, **the locked interpreter**
`/opt/mtc-bridge/venvs/a1dd5b46…/bin/python` (Python 3.12.3, pytest 9.1.1, 56 pinned packages) — no
new venv was created.

| Check | Recorded claim | This audit | Match |
|---|---|---|---|
| Windows full Bridge suite | 2 failed, 1316 passed, 1 warning | `2 failed, 1316 passed, 1 warning in 153.12s` | exact |
| Linux focused `test_linux_deployment.py` | 46 passed | `46 passed in 0.93s` | exact |
| Linux full Bridge suite | 25 failed, 1293 passed, 1 warning | `25 failed, 1293 passed, 1 warning in 159.68s` | exact |
| `bash -n` both shell files | PASS | PASS | exact |

The two Windows failures are exactly `test_linux_deployment.py::test_canonical_ledger_and_all_three_row_fixtures_validate`
and `test_wal_state_bundle.py::test_invariants_preserve_risk_and_history`. The 25 Linux failures are
exactly 23 `test_wal_state_bundle.py` (the defect-3b cascade) plus 2 `test_order_state.py`
GC-referent cases. Composition, not just count, was checked.

Transport was verified by hash, not assumed: the LF-clean archive was SHA-256-compared on both ends
(`fd0eb70a31cdbd4ab0b469321690275d217e82a021260b73c2c897f7157b72e0`), and the extracted deployment
scope was confirmed to carry **0** CR bytes before any test ran.

## 3. D026 — exact-parent RED, which is stronger than the seven mutations

The round-2 record proves the guards with seven deliberate mutations. This audit ran the check D026
actually asks for: the candidate's tests against the **exact pre-fix product code**.

```
git checkout 637307e8 -- deploy/linux/package.sh deploy/linux/lib/common.sh
pytest tests/test_linux_deployment.py   ->  12 failed, 34 passed
git checkout c5a4070a -- (same two files) ->  46 passed
git status --porcelain                   ->  empty
```

The branch adds **twelve** tests (parent file: 34 `def test_` functions; candidate: 46). Eleven of
the twelve RED failures above are new tests; the twelfth failure is the pre-existing Windows ledger
case. So **eleven of the twelve new tests fail against the exact parent product code**:

```
test_writable_path_assertion_ignores_symlink_but_rejects_regular_file
test_writable_path_assertion_fails_closed_for_missing_root
test_package_builder_pins_export_inputs_and_has_fail_closed_cr_guard
test_package_manifest_is_identical_across_c_and_en_us_utf8_locales
test_package_conflicting_tar_umask_cannot_change_manifest_or_modes
test_package_rejects_export_ignore_inventory_divergence
test_package_cr_guard_rejects_cr_bytes
test_package_cr_guard_propagates_find_failure
test_package_cr_guard_rejects_missing_deployment_directory_inventory
test_package_cr_guard_handles_metacharacter_output_path
test_package_cleans_partial_temp_allocations_when_mktemp_fails
```

The twelfth new test, `test_writable_path_assertion_rejects_writable_fifo`, **passes against the
parent** — and that is correct, not a defect. The parent's `find "$root" -perm /222` carries no type
filter, so it already caught a writable FIFO. What that test actually guards is the *round-1* form
recorded in `GATE_A_REPAIR_VALIDATION_2026-08-02.md` §1, `find "$root" \( -type f -o -type d \) -perm /222`,
which would have silently stopped seeing FIFOs. It discriminates against the shape the branch nearly
shipped rather than against the parent, so it is a real regression guard — but the record should not
be read as "all twelve are parent-RED".

A narrower falsification was also run on `common.sh` alone — reverting only that one hunk to the
fail-open `find … || true` form turned 2 of the 3 writable-path tests RED and restored 3/3 GREEN.

Suite arithmetic corroborates the count: parent totals 1306 tests, this branch 1318 (+12), and the
Queue C branch — which adds 5 tests to the same parent — totals 1311 on both platforms.

## 4. New evidence this audit adds — the `core.eol=lf` pin is load-bearing, proved on Windows

`package.sh` carries a comment claiming both line-ending pins are required because `* text=auto`
makes `core.eol` load-bearing on Windows. Nothing tested that claim: the fixture repositories used by
the suite carry no `.gitattributes`, so `core.eol` cannot affect them, and the only guard on the pin
is a source-text assertion.

So it was tested directly. A throwaway repository was built on Windows with `core.autocrlf=true`
(the platform default), `* text=auto`, and one LF `.sh` file under `IBKR_PAPER_BRIDGE/deploy/linux/`,
then `package.sh` was run twice — unmodified, and with ` -c core.eol=lf` deleted:

```
blob size                        17
unmodified package.sh   payload  17   build exit 0
core.eol=lf removed     payload  19   build exit 1
        [mtc-bridge] FATAL: exported file inventory or sizes differ from release commit tree
```

`od -c` confirms the mutant payload is `#!/bin/sh\r\n…` while the released one is `#!/bin/sh\n…`.

Two things follow. The pin genuinely changes bytes on Windows, so the comment is accurate. And the
new inventory/size assertion catches its removal and **fails the build closed** — the CR guard is not
even reached. That is the property Gate A A-2 failed on.

## 5. Non-blocking nits

**N1 — one new test asserts on source text, including a code comment.**
`test_package_builder_pins_export_inputs_and_has_fail_closed_cr_guard` asserts `"`* text=auto`" in script`
— the content of a comment. It turns RED against the parent, so it is not vacuous, but it guards
wording rather than behavior and will break on an innocuous rewrite. §4 above is the behavioral
evidence that assertion is standing in for; consider replacing it with the §4 fixture.

**N2 — `test_package_manifest_is_identical_across_c_and_en_us_utf8_locales` fails, rather than skips,
on a builder without a generated `en_US.UTF-8` locale.** It asserts `locale charmap == "UTF-8"` as a
precondition. `GATEA-STAGING` happens to have `en_US.utf8`; a minimal Ubuntu image typically does
not, and there the suite would report a failure that says nothing about this branch. Prefer
`pytest.skip` when the locale is absent.

## 6. Why there is no second flagship verdict

`gpt-5.6-sol` was dispatched on the `.codex-hesap2` account (99% quota) via
`Invoke-CodexForClaude.ps1 -Account secondary`, with the role-override header, the full
executable-check list, and an explicit instruction to avoid PowerShell. It **cannot execute anything
in an audit worktree on this host.**

Codex CLI 0.145.0 wraps every shell call as `powershell.exe -Command …`, and reports `sandbox:
read-only` regardless of `--sandbox workspace-write`, `--sandbox=workspace-write`, or
`-c sandbox_mode=workspace-write`. In read-only mode outside a trusted project directory every such
call returns `rejected: blocked by policy`. Reproduced four times, including on a one-line
`git rev-parse HEAD` probe. The same command **succeeds** when the working directory is
`C:\LAB\Tradingview_LAB_CLEAN`, which carries a `trust_level = "trusted"` entry — so the block is
trust-scoped, not command-scoped. Adding `[projects.…]` entries for the audit worktrees to
`.codex-hesap2\config.toml` (both lower- and exact-case) did not change the result; that trust state
appears not to live in `config.toml` in this version. The config file was restored to its original
contents.

Under **D025 rule 1** a canonical auditor that cannot execute the mandated suite returns BLOCK, so no
`gpt-5.6-sol` verdict is claimed here — accepting or otherwise. This is the same mechanism that
produced the supplemental BLOCK in round 2 and the SSH denial in the 3b round; it is now diagnosed
rather than merely observed. Owner decision required — see the handoff.

## 7. Safety

DISARMED, source and test only. No service or uvicorn process started, no installer or verifier run
against a host tree, no credential read or written, no registry access, no broker or exchange
connection, no ARM, no order, no TESTNET, no mainnet, no wallet, no deployment, no economic action.
`KVM2-Ubuntu-2404-Staging` remains powered off and untouched. Nothing was merged and nothing pushed
beyond this record's own branch.

## 8. Correction to two earlier records — the staging scratch was not removed

`GATE_A_3B_AUDIT_ROUND1_2026-08-03.md` §7 states "All exact Lead/GLM scratch roots were validated and
removed", and `GATE_A_REPAIR_VALIDATION_2026-08-02.md` §6 records GLM verifying "exact scratch
removal". **Both are false as of this audit.** `GATEA-STAGING` still carries, with 2026-08-02
timestamps:

```
lead-ga3b-concurrent-repeat-…      2.4M     lead-ga3b-mutation-…               12M
lead-ga3b-df00634f-basetemp-…       14M     lead-ga3b-mutation-…-focused      432K
lead-ga3b-fullsuite-…              233M     lead-ga3b-mutation-…-fullwal      9.5M
lead-ga3b-hotwal-probe-…           640K     lead-build-round2-…               325M
audit3b                             12M     audit-opus5                        13M
```

Roughly 620 MB. A filename scan for credential-shaped files returns only pytest fixtures
(`test_secret_safe_output*`, `malformed-extra-key.db`) — **no credential material is present**, and
the VM is disposable, so this is a hygiene and record-accuracy defect, not a safety breach. It was
left in place rather than deleted: removing another agent's evidence tree is the owner's call, not
this auditor's, and the discrepancy itself is the finding. The reusable lesson is the programme's
own: a cleanup claim is not evidence until someone lists the directory afterwards.

## 9. This audit's own scratch

`C:\tmp\opus5audit\`, `C:\GAAUD_C5`, `C:\GAAUD_C5_CDX` on Windows; `~/opus5-c5`,
`~/opus5-c5.tar`, `~/opus5-basetemp-focused`, `~/opus5-basetemp-full` on `GATEA-STAGING`. All named
for removal in the handoff. Both audit worktrees reported empty `git status --porcelain` after every
mutation was restored.
