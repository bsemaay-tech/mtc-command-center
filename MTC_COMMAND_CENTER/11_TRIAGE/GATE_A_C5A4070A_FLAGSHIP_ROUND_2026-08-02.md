# c5a4070a — canonical flagship round under the narrow owner authorization

Date: 2026-08-02
Authorization: owner-granted, narrow — `--dangerously-bypass-approvals-and-sandbox` for **fresh,
audit-only** flagship sessions on the frozen Gate A candidates only. No implementation, no commit /
checkout-branch / reset / stash / clean / merge / push, no deletion outside each auditor's own exact
scratch, no credential inspection, no broker / ARM / TESTNET / mainnet / KVM2 / economic action.

Target: `codex/gate-a-build-determinism` @ `c5a4070a4836bbb9ee010dc63db69313066667c4`

## 1. Outcome

| Auditor | Session | Verdict |
|---|---|---|
| `claude-opus-5` xhigh | fresh, no-resume, `C:\GAAUD_C5_CLA` | **ACCEPT** — no required findings |
| `gpt-5.6-sol` xhigh | fresh, `C:\GAAUD_C5_CDX` | **REQUEST_CHANGES** — three required findings |
| `claude-opus-5` (Lead) | recovery session, `C:\GAAUD_C5` | Lead verification only — not a flagship verdict |

**NOT ACCEPTED.** D025 rule 3 needs accepting verdicts from *both* flagships. This is the **first
non-accepting result** in this branch's cycle. No repair is authorized; the findings are reported,
not implemented.

The bypass authorization did what it was supposed to: `sandbox: danger-full-access`, and Codex
executed the full mandated Windows and Linux evidence for the first time in this programme.

## 2. What both flagships agree on — independently measured, no drift

| Leg | `claude-opus-5` fresh | `gpt-5.6-sol` |
|---|---|---|
| Windows full suite | `2 failed, 1316 passed, 1 warning` | `2 failed, 1316 passed, 1 warning` (second run — see F3) |
| Linux L0 CR bytes in deploy scope | `0` | `0` |
| Linux focused | `46 passed` | `46 passed` |
| Linux full suite | `25 failed, 1293 passed, 1 warning` / 1318 | `25 failed, 1293 passed, 1 warning` |
| Failure composition | 23 `test_wal_state_bundle` + 2 `test_order_state`, name-by-name | identical |
| D026 exact-parent | 12 added, **11 RED** | 12 added, **11 RED** |
| The one GREEN new test | `..._rejects_writable_fifo` — anti-over-correction guard, not vacuous | same conclusion |
| Archive SHA-256 both ends | `fd0eb70a…` | `fd0eb70a…` |

Both also built the **real** payload from the frozen SHA, not a fixture, and got the same manifest
hash — `4a9846e232c1ad1744a67d4f7e66221afca8549fda64516a03feaad59306e693` — with `gpt-5.6-sol`
additionally showing it is unchanged under hostile `core.autocrlf=true`, `core.eol=crlf`,
`tar.umask=0077`. That is the determinism claim, proved twice by different agents.

## 3. The three required findings, each reproduced by the Lead on real source

**D025 rule 2** makes a required finding binding *after* the Lead reproduces it. All three reproduce.

### F1 — the locale test rejects a valid minimal builder

`tests/test_linux_deployment.py:507` asserts `locale charmap == "UTF-8"` as a precondition, so on a
builder without a generated `en_US.UTF-8` it **fails** instead of skipping.

Lead reproduction on the locked interpreter, simulating a minimal builder by pointing `LOCPATH` at an
empty directory:

```
locale generated (staging as-is) : UTF-8            -> 1 passed
LOCPATH=<empty dir>              : ANSI_X3.4-1968   -> 1 failed
                                   AssertionError, test_linux_deployment.py:507
```

The product does not need that locale — `package.sh:163` forces `export LC_ALL=C`. So the test
demands an environment capability the thing under test deliberately does not depend on, and a clean
Ubuntu builder would report a false failure. **Confirmed binding.**

### F2 — a test asserts on the wording of a code comment

`tests/test_linux_deployment.py:494` asserts ``"`* text=auto`" in script``. Lead reproduction —
edited the comment only, changed no executable line:

```
-# Both line-ending pins are required: the repository's `* text=auto`
+# Both line-ending pins are required: the repository's text-auto attribute

bash -n            : OK          (product behaviour identical)
pytest -k pins_export_inputs : 1 failed   test_linux_deployment.py:494
restore            : 1 passed,  git status --porcelain empty
```

A test that fails on a comment rewrite while product behaviour is unchanged constrains prose, not
behaviour. **Confirmed binding.** Both flagships and the Lead independently reached this.

Note the tension the owner should see: this was previously recorded as non-blocking nit **N1** and
the owner's standing direction is to leave the nits alone and not invalidate the frozen SHA. A
flagship has now raised it as a *required* finding. Those two positions need reconciling — that is an
owner call, not an auditor one.

### F3 — a new test is not deterministic in the mandated Windows suite

`gpt-5.6-sol`'s **first** W1 run:

```
FAILED tests/test_linux_deployment.py::test_package_cr_guard_propagates_find_failure
3 failed, 1315 passed, 1 warning in 155.90s
```

with the subprocess returning `1` and **empty stdout and stderr**. It passed alone, passed in the
focused module, and the repeated full suite gave the expected `2 failed, 1316 passed`.

Lead reproduction attempt — **not reproduced**, and the attempt was not token:

- 40 consecutive focused repeats of that exact test, run under concurrent load: **0 failures**;
- Windows full suite at this SHA, this session: **7 runs, 6 clean** — Lead ×1, fresh `claude-opus-5`
  ×1, `gpt-5.6-sol` ×1 (its second run), plus 3 dedicated back-to-back repeats, every one
  `2 failed, 1316 passed, 1 warning` with the same two names. The single failure is
  `gpt-5.6-sol`'s first run.

Observed rate ≈ 1 in 7 full-suite runs, never once outside the full suite. The signature — `rc=1`
with **no stdout and no stderr** — is consistent with a Windows `bash.exe` spawn failure under
process pressure rather than a logic defect in the guard, because `run_bash` shells out once per
test and the test asserts on `stderr` content it never received.

**Recorded as unreproduced with the evidence**, per D025 rule 2 — not silently dropped, and not
accepted as a defect in the branch either. It still matters: a mandated floor that intermittently
reports an extra failure cannot serve as a pass/fail gate, so the *floor* needs hardening even if
the *branch* is innocent. Whether that belongs to this candidate is an owner call.

## 4. Non-blocking nits added by the fresh `claude-opus-5` session

1. **`[ "${LF_REQUIRED_COUNT}" -gt 0 ]` (`package.sh:159-160`) is unreachable.** The second `find`
   pass reads a superset of the first, so the DEPLOY guard always fires first. Measured: deleting the
   DEPLOY guard is the only way to make the LF guard fire. Redundancy dressed as a guard.
2. **Symlink diagnostic is misleading** — a tree symlink dies with `exported file inventory or sizes
   differ`, not the specific symlink message, because the inventory check precedes
   `assert_regular_directory_tree`.
3. **CR guard covers 14 of 462 payload files.** Benign only because the size-inventory comparison is
   a universal CR backstop — CRLF changes byte size, so every file is covered by size even though 448
   are outside the CR guard. That is the real answer to "is the CR scope sufficient": alone no,
   combined yes. One shebang-bearing file sits outside it,
   `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/validate_ledger.py`.
4. **`sha256sum` is required but not GNU-verified**, unlike `find/sort/grep/realpath/xargs`; a BSD
   `shasum` on `PATH` would emit a different manifest format.
5. Flagged but **not measured**, so not a finding: `bash_mode(...) == "644"` is asserted on extracted
   files, and GNU tar applies the extracting process's umask for non-root.

## 5. Cleanup and safety

Both auditors returned `git rev-parse HEAD` = `c5a4070a…` and empty `git status --porcelain`, and
each removed **only** its own scratch. The fresh `claude-opus-5` session explicitly verified that
`audit3b`, `audit-opus5`, `lead-build-round2-…` and all six `lead-ga3b-*` trees were still present
afterwards — the retained-evidence instruction held. No commit, branch checkout, reset, stash, clean,
merge or push occurred; no credential value was read; no broker, ARM, order, TESTNET, mainnet, KVM2
or economic action occurred.
