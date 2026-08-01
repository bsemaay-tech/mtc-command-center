# WP-I pre-Gate-A readiness record

- Date: 2026-08-01
- Work package: WP-I — Reproducible Deps, systemd, State, Rollback, Ubuntu Staging
- Status: **PRE-GATE-A / STATIC ONLY**
- Frozen source HEAD: `637307e83951ffe23e768ed8e50ddaf8712b0660`
- Overall readiness verdict: **BLOCK — NOT READY FOR FINAL GATE A**

WP-I's bounded local/static documentation and validation are complete at this
source, including the outbound-network SMALL-GAP artifact. The overall final
Gate A request remains blocked by missing objective evidence named in the plan:
there is no materialized candidate payload/path manifest at this frozen source
and no named expendable Ubuntu 24.04 staging host is recorded. Neither fact may
be invented inside this allowlist.

## 1. Gate-1 classification and scope

Gate 1 classifies this task **UNPROTECTED**. Only Markdown evidence and
discoverability text may change; the task cannot change order, broker, risk,
persistence, concurrency, migration, runtime, deployment, Pine, parity, or MTC
behavior.

Exact allowlist:

1. `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` — new.
2. `IBKR_PAPER_BRIDGE/deploy/linux/README.md` — discoverability only; its
   PREPARATION ONLY status and gate order are preserved.
3. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_READINESS_RECORD_2026-08-01.md` — new.

Any required edit outside this list is BLOCK. No Git state operation is
authorised.

## 2. Frozen identity and WP-L source status

`git rev-parse HEAD` reproduced
`637307e83951ffe23e768ed8e50ddaf8712b0660`. At inspection time this was also
the local `origin/master` value.

The upstream handoff identifies WP-L Phase 1 as accepted/source-frozen at this
HEAD. The named file
`MTC_COMMAND_CENTER/11_TRIAGE/WPL_PHASE1_VERIFICATION_RECORD_2026-08-01.md` is
**absent from this branch**. This record therefore uses the lead-supplied WP-L
status and evidence facts; it does not claim that the absent acceptance record
was inspected here. `WP-L Phase 2 — Ubuntu revalidation` has not occurred and
remains post-Gate-A work on the retained authorised staging host.

## 3. Plan section 18 requirement matrix

| Plan section 18 requirement | Local/static status at frozen HEAD | Exact evidence | Post-Gate-A Ubuntu proof owed |
|---|---|---|---|
| Reproducible dependency lock | **SATISFIED-STATIC** | `requirements.in` has 10 direct entries; `requirements.lock` has 56 exact pinned distributions; Git blob `47f53fa227bf0f18b9bf9bd77e060d8856961728`; raw blob SHA-256 `a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e`; `verify_lock.py` passes | Install on Ubuntu Python 3.12, then prove installed distributions exactly equal the lock |
| Hash- and artifact-bound install | **SATISFIED-STATIC** | `install.sh` binds release SHA and payload manifest, creates a per-SHA venv, and uses `--require-hashes --no-deps --only-binary=:all:`; offline mode adds `--no-index --find-links` | Execute exactly one authorised install path and capture output; no execution has occurred |
| systemd first-start safety | **SATISFIED-STATIC** | `mtc-bridge-first-start.service.template` has `Restart=no`, no `[Install]`, SIGTERM/45-second stop contract, hardening, and exact-SHA paths; installer installs it masked and does not start/enable/unmask | Verify masked/inactive install, one authorised DISARMED start, reboot DISARMED, and SIGTERM clean shutdown |
| Restart-on-failure profile | **SATISFIED-STATIC / GATED** | `mtc-bridge-steady.service.template` uses bounded `Restart=on-failure` and throttling; `install.sh` refuses to install it before its separate gate | Fault-injection and fresh acceptance are required before admission; the current first-start exercise must remain `Restart=no` |
| Runtime watchdog | **SATISFIED-STATIC** | `bridge/engine/bars.py:119-125,143-206` creates the bar-feed watchdog, checks WebSocket health/staleness, reconnects, and invokes the stale callback | Observe disconnect, reconnect, stale-data fail-safe, and no-order behavior on Ubuntu while DISARMED |
| State continuity and SQLite backup/restore | **SATISFIED-STATIC** | WP-0 maps `tests/test_wal_state_bundle.py` coverage, including create/verify round-trip, online-backup metadata, integrity, corruption, and hash mismatch; the unit routes state to `/var/lib/mtc-bridge/bridge.db` | Execute backup and restore on staging and prove state/risk/history continuity |
| Rollback procedure | **SATISFIED-STATIC** | `rollback.sh` requires state and release manifest hashes, stops/masks, preserves state, verifies exact rollback payload/venv, and never starts/enables/unmasks; focused rollback test passes | Execute and evidence rollback on staging; any recovery start remains separately gated |
| Expendable staging lifecycle | **DOCUMENTED / NOT EXECUTED** | Plan section 18 and deployment `README.md` retain one Gate-A-authorised host through `WP-L Phase 2 — Ubuntu revalidation`, WP-I staging verification, and WP-A; discard follows evidence capture | Identify the named Ubuntu 24.04 host before final Gate A, then execute only after that gate |
| Pinned/SBOM-equivalent inventory | **SATISFIED-STATIC** | `IBKR_PAPER_BRIDGE/deploy/linux/SECURITY_BASELINE.md` section 1 | Confirm exact installed inventory; a formal CycloneDX/SPDX SBOM is outside this minimum baseline |
| Repository/payload secret scan | **PARTIAL-STATIC** | Content-redacted high-confidence scan of every non-binary tracked blob at the frozen HEAD returned zero category/path hits; tracked source is payload-equivalent because `package.sh` uses `git archive` | Build the immutable candidate payload, record its exact path/hash manifest, and scan that built artifact before final Gate A can be declared ready |
| Outbound-network inventory | **SATISFIED-STATIC — SMALL-GAP CLOSED AS ARTIFACT ONLY** | `SECURITY_BASELINE.md` separates Hyperliquid TESTNET, optional Telegram, package-index installation, the local listener, mainnet, and unused settings | Capture actual Ubuntu DNS/HTTPS/WebSocket destinations; confirm no mainnet traffic and loopback-only bind |
| No public surface / no mainnet / no order / no secret value | **SATISFIED-STATIC WITH TEST-ENV CAVEAT** | `app.py` binds `127.0.0.1:8790` and constructs only `network="testnet"`; no credential value was intentionally inspected, printed, copied into output, or persisted; earlier unsanitized pytest collection inherited settings variables and may have loaded their values into `Settings()` in memory; no disclosure was observed; fresh tests used credential-scrubbed child environments | Reconfirm on the authorised host; any public bind, mainnet attempt, order, or secret disclosure is BLOCK |

## 4. Reproduced local evidence

Environment: Windows, Python 3.14.2. No Ubuntu or shell-script execution was
performed.

Focused deployment command:

```powershell
$start = [System.Diagnostics.ProcessStartInfo]::new()
$start.FileName = 'python'
$start.Arguments = '-m pytest -q -p no:cacheprovider --ignore=TSP1009B.pytest_tmp_s1r1 tests/test_linux_deployment.py::test_lock_is_exact_fully_hashed_and_contains_every_direct_dependency tests/test_linux_deployment.py::test_lock_generation_contract_targets_python_312_linux_with_hashes tests/test_linux_deployment.py::test_installer_uses_per_sha_venv_hashes_and_binary_wheels_only tests/test_linux_deployment.py::test_rollback_is_exact_preserves_state_and_never_starts'
$start.WorkingDirectory = 'C:\WPL\IBKR_PAPER_BRIDGE'
$start.UseShellExecute = $false
foreach ($name in @('HL_ACCOUNT_ADDRESS','HL_API_WALLET_KEY','HL_LIVE_ACK','ANTHROPIC_API_KEY','XAI_API_KEY','TELEGRAM_BOT_TOKEN','TELEGRAM_CHAT_ID')) {
  [void]$start.Environment.Remove($name)
}
$process = [System.Diagnostics.Process]::Start($start)
$process.WaitForExit()
if ($process.ExitCode -ne 0) { throw "Focused deployment tests failed with exit $($process.ExitCode)" }
```

Fresh credential-scrubbed child result: **4 passed in 0.68s**.

Secret-safety structural command:

```powershell
$start = [System.Diagnostics.ProcessStartInfo]::new()
$start.FileName = 'python'
$start.Arguments = '-m pytest -q -p no:cacheprovider --ignore=TSP1009B.pytest_tmp_s1r1 tests/test_linux_deployment.py::test_program_tree_has_no_private_host_ip_user_or_key_path tests/test_linux_deployment.py::test_env_template_contains_names_and_comments_but_no_definitions'
$start.WorkingDirectory = 'C:\WPL\IBKR_PAPER_BRIDGE'
$start.UseShellExecute = $false
foreach ($name in @('HL_ACCOUNT_ADDRESS','HL_API_WALLET_KEY','HL_LIVE_ACK','ANTHROPIC_API_KEY','XAI_API_KEY','TELEGRAM_BOT_TOKEN','TELEGRAM_CHAT_ID')) {
  [void]$start.Environment.Remove($name)
}
$process = [System.Diagnostics.Process]::Start($start)
$process.WaitForExit()
if ($process.ExitCode -ne 0) { throw "Secret-safety structural tests failed with exit $($process.ExitCode)" }
```

Fresh credential-scrubbed child result: **2 passed in 0.89s**.

The auditor's earlier **4 passed in 0.55s** and **2 passed in 0.53s** runs were
functionally passing but inherited the parent settings environment. Because
pytest collection imports `bridge.app`, which instantiates `Settings()`, those
runs may have loaded credential values into memory. No credential value was
intentionally inspected, printed, copied into output, or persisted, and no
disclosure was observed.

The content-redacted tracked-tree scan command and exact result are recorded in
`SECURITY_BASELINE.md`: nine high-confidence categories, zero category/path
hits. The targeted runtime source search returned
`ANTHROPIC_XAI_RUNTIME_CLIENT_HITS=0`. Local SDK constant inspection returned
TESTNET `https://api.hyperliquid-testnet.xyz` and the unselected mainnet base;
the mainnet branch is forbidden in this program.

Lead-provided broader focused result: **1 failed, 34 passed**. Its sole failure
is the Windows CRLF working-copy hash of `ledger_schema.json` differing from the
canonical Git blob; it is not classified as a WP-I defect and is not converted
to a passing result here.

## 5. Final Gate A readiness check

WP-I local/static preparation is complete with the test-environment caveat
above, and the outbound-network SMALL-GAP is closed as an artifact only. No
credential disclosure was observed. Final Gate A still requires every
objective item in the plan's PRE-STAGING checklist.

| Missing objective prerequisite | Exact evidence | Disposition |
|---|---|---|
| Exact candidate release artifact path manifest | No materialized payload or recorded payload path/manifest hash exists at this frozen source. `COMMANDS.md` remains a command template without a resolved candidate payload path or manifest hash, and this work was forbidden from running `package.sh`. The source SHA alone is not the artifact-path manifest required by Gate A. | **BLOCK** until the Lead builds/identifies the immutable candidate locally, records its exact path and manifest SHA-256, and completes the after-build secret scan without exposing values |
| Named expendable Ubuntu 24.04 staging host identified, not deployed | No host identity was supplied or found in the reviewed WP-0, plan, README, or COMMANDS evidence. Inventing a hostname, IP, user, or credential is forbidden. | **BLOCK** until the owner/Lead records the non-secret host identifier. Identification is not deployment and authorises no access or execution |

Accordingly, the only honest verdict is **BLOCK — NOT READY FOR FINAL GATE A**.
This verdict does not allege a WP-I code defect. It preserves the distinction
between locally complete static preparation and the two missing gate inputs.
Gate A itself would authorise only one named expendable Ubuntu staging action;
it would not mean that staging, Ubuntu proof, or WP-A had already occurred.

## 6. Evidence still owed after final Gate A

- Retain the one authorised staging host through, in order,
  `WP-L Phase 2 — Ubuntu revalidation`, WP-I staging verification, and WP-A.
- Prove the lock installs on Ubuntu Python 3.12 and the installed distribution
  set exactly equals the 56-entry lock.
- Prove masked/inactive installation, DISARMED start, reboot DISARMED, and
  SIGTERM clean shutdown with no dangling state.
- Prove SQLite backup/restore and risk/history continuity.
- Execute rollback, preserve state, prove zero writers, and keep any recovery
  start behind its separate gate.
- Capture actual egress and confirm TESTNET-only destinations, optional
  Telegram disposition, loopback-only `127.0.0.1:8790`, and no mainnet traffic.
- Execute WP-A's DISARMED restart/reconnect/stale-data invariants and capture the
  evidence before discarding the host.

## 7. Hour accounting

The last reproducible program ledger remains **20.5 h used / 29.5 h
remaining**. Exact WP-L and WP-I actual booking is not reproducible from this
branch and is deferred to **Lead Gate-7**. No hours are invented or silently
charged by this record.

## 8. Static completion statement

Changed artifacts are limited to the exact three-path allowlist. No Ubuntu,
SSH, network, broker, VPS, systemd, install, rollback, ARM, TESTNET, mainnet,
order, live-capital, secret-value, or Git-state action was performed.
