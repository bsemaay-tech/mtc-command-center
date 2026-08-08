# GATE A — PRE-REGISTRATION ADDENDUM B: re-baseline to `ebada020` (2026-08-08)

Amends `GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md` and
`GATE_A_PREREGISTRATION_ADDENDUM_A_2026-08-02.md`. **Written before the run, not during it** — Gate A
is a pre-registered gate, and its expected values must be fixed in advance or a pass proves nothing.

**Why this addendum is mandatory.** The 2026-08-02 Gate A run FAILED at A-2. The four defects behind
that failure were repaired and integrated into `ebada020`, which both flagship auditors accepted on
2026-08-08 (`GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md`). The parent documents still
freeze the **superseded** artifact and still expect failures the repairs have since fixed. Executing
A-0 or A-3 against those numbers would produce a false FAIL or a meaningless PASS.

---

## B.1 Frozen inputs — supersede runbook §2 and Addendum A §A.4 in full

| Item | Superseded value (do not use) | **Authoritative value** |
|---|---|---|
| Artifact path | `C:\WPI_ARTIFACTS\1adf9ae51b0ddfe81057860aec5c23bb842f5a84` | `C:\WPI_ARTIFACTS\ebada020a59edf539f60acfbb3a6bf870c8679e9` |
| `RELEASE_SHA` | `1adf9ae51b0ddfe81057860aec5c23bb842f5a84` | `ebada020a59edf539f60acfbb3a6bf870c8679e9` |
| Manifest SHA-256 | `bfefea2f825c8ba8a4c2289cd6ed90c74b51b15bc603cd5589db8815493ced02` | `8FC30864BA342E53DCFC6B2938124F91D005F02671A332580A723F38FD4700C9` |
| Manifest entries | 7,060 | **7,059** |
| Files on disk | 7,061 | **7,060** (7,059 manifest entries + `RELEASE_SHA256SUMS`, which is self-excluded) |
| Total bytes | 1,051,904,669 | **1,033,359,158** |
| `origin/master` | `637307e8` | `637307e8` — unchanged, nothing Gate A is merged |
| Candidate branch | — | `codex/gate-a-integration` @ `ebada020…`, must stay equal to the artifact build SHA |
| Records branch | `feature/donchian-crypto-ladder` @ `ea85566b` | `feature/donchian-crypto-ladder` @ `e5bb6f70` |

Lead-measured 2026-08-08: `Get-FileHash RELEASE_SHA256SUMS` → `8FC30864…4700C9`; recursive file count
7,060; recursive byte sum 1,033,359,158; `RELEASE_SHA` file contents equal the source commit.
Independently verified in the same round by both flagships, including a full `sha256sum -c` over all
7,059 entries (exit 0, 7,059 OK, 0 non-OK).

**A-0 restated.** Recompute the manifest SHA-256 on the source side and confirm `8FC30864…4700C9`;
transfer as **one tar**, never as loose files; recompute on the host and confirm the same value.
**FAIL:** any mismatch, or a file count other than 7,060.

Transfer-as-one-tar is not a style preference — it is what made A-0 pass on 2026-08-02, where a
7,000-file loose copy was the failure mode. The `git -c core.eol=lf archive` build contract also
stands: a bare `git archive` on Windows reintroduces CRLF and reproduces the original A-2 FAIL.

## B.2 A-3 expected-failure set — supersedes runbook §A-3

The runbook expects "the KVM2 ledger-hash test and the `schema_version == "2"` test". **Both are now
fixed** — they were among the 23 failures the repairs closed. Using the old expectation would flag the
real survivors as new failures.

**Authoritative expectation on the locked Linux runtime (Ubuntu 24.04.4, CPython 3.12.3, host venv
`/opt/mtc-bridge/venvs/a1dd5b467b12421f632bf3d8462a7244b39b2287/bin/python`, pytest 9.1.1):**

```
2 failed, 1357 passed, 1 warning
```

The two permitted failures, and no others:

```
tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container
tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container
```

Both are CPython-version-dependent, both fail identically on parent `637307e8`, and both pass on
Windows CPython 3.14 (`1359 passed, 1 warning`). Measured twice independently: the Lead on
2026-08-03 and the `claude-opus-5` xhigh flagship on 2026-08-08 from its own LF export.

**FAIL:** any third failure, or any failure whose node ID is not one of those two. A different node ID
is a FAIL even if the count is still two.

Baseline for the comparison, on the same runtime: parent `637307e8` gives `25 failed, 1281 passed,
1 warning`. Candidate versus parent: **zero new failure node IDs, 23 fixed.**

## B.3 A-4 — declared risk before the run

A-4 ("starts DISARMED and stays that way") is the runbook's most important check. One known condition
bears on it directly and is declared here rather than discovered mid-run.

**Flagship NIT 1, Lead-reproduced at `ebada020`:** the credential-free DISARMED start mode is not
reachable from any shipped deploy artifact. `MTC_BRIDGE_START_MODE` and `--start-mode` appear only in
`bridge/app.py` and its own test — zero hits under `deploy/`. Both unit templates use
`ExecStart=… python -m bridge.app` with no start-mode argument
(`mtc-bridge-first-start.service.template:34`, `mtc-bridge-steady.service.template:37`), the env
template does not name the variable, and `resolve_start_mode(env={})` returns **credentialed**
(`tests/test_credential_free_disarmed.py:26`).

Consequence for A-4: the service under test will start in **credentialed** mode against an env file
that `install.sh` creates with every variable UNSET, so `resolve_hyperliquid_credentials()` runs with
no credentials present.

**A-4's FAIL condition is unchanged and is not being softened.** It still fails if the service arms,
attempts a broker connection, or reports an ambiguous state. What is pre-registered here is the
*expectation*: A-4 is expected to demonstrate `app_state` durably not `ARMED` and the ARM path
refusing, and it must additionally record explicitly **which** start mode the service actually
selected and whether any broker connection was attempted. If the credentialed path attempts a broker
connection, that is a genuine A-4 FAIL and must be reported as one — not explained away with NIT 1.

Whether an empty env file fails closed or crash-loops is **undetermined and must be settled by
execution, not on paper.** A-4 is where that gets settled.

Note the direction of the risk: A-4 passing does not close NIT 1. NIT 1 stays a binding follow-up
before any DISARMED VPS deploy, because "did not arm" is weaker than "cannot arm, having never held
credentials".

## B.4 Carried unchanged from Addendum A

- **A-4 method.** The unit installs masked, `Restart=no`, with no `[Install]` section. A-4 therefore
  requires `systemctl unmask` then `systemctl start` on the staging host. Pre-registered, not
  improvised.
- **A.6 stands.** Running Gate A on the disposable host does not spend, satisfy, substitute for or
  pre-approve any `KVM2-P4-xx` gate. KVM2 still gets exactly one clean install under its own
  authorizations. The active KVM2 host stays out of scope entirely.
- Stop at the first FAIL. Write `GATE_A_RESULT_2026-08-08.md` either way.

## B.5 Host state before A-0 — cleanup owed

`GATEA-STAGING` (`gatea@172.24.55.233`, Ubuntu 24.04.4, CPython 3.12.3, SQLite 3.45.1) is live and
already validated. The `claude-opus-5` flagship deliberately left its Linux evidence in the home
directory: `~/opus5-audit-20260808/` (`cand.log`, `parent.log`), `~/v2_*.tar`, `~/sub_*.tar`. **Remove
exactly those paths as A-0 prep** so the transfer step starts from a clean home. The locked venv is
root-owned and read-only — install nothing, modify nothing. Never read, print, copy, rotate or modify
key material.
