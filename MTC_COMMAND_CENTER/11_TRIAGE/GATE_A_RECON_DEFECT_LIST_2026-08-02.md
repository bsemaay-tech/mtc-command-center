# GATE A — RECONNAISSANCE DEFECT LIST (2026-08-02)

> **THIS IS NOT GATE A EVIDENCE.** Gate A failed at A-2 and stopped there, as the runbook requires
> (`GATE_A_RESULT_2026-08-02.md`, commit `55bf677f`). Nothing in this file may be cited as an
> A-2…A-9 result, and none of it substitutes for a real gate run on a corrected artifact.

## Why this exists

Gate A stopping at the first FAIL is correct, but stopping the *night* there would have been
wasteful: the implementer would repair CRLF, rebuild the payload, and we would discover the next
blocker tomorrow — one defect per cycle, with roughly 29.5 programme hours remaining.

So after the official gate stopped, a **line-ending-normalised copy** of the payload was driven
through the install path purely to find what else is broken. The pristine payload at `~/payload`
was left untouched, so A-0's verification still stands on its own.

Each recon patch is listed below. They exist only on the disposable staging host, in
`~/recon/`. **No repository file, no artifact file and no host file outside `~/recon` was edited to
make anything pass.**

---

## Defect 1 — CRLF line endings (this is the Gate A A-2 FAIL)

Full evidence in `GATE_A_RESULT_2026-08-02.md`. Summary: 19 of 19 shell scripts, both systemd unit
templates, the logrotate policy and the env contract are committed with CRLF. `install.sh` dies on
line 37 with `$'\r': command not found`. Root cause is the committed blob — `git archive` exported
exactly what was committed, and the defect is present on `origin/master`.

**Recon patch 1:** `sed -i 's/\r$//'` over 24 files (`*.sh`, `*.service`, `*.template`, `*.env`,
`logrotate/*`), then `RELEASE_SHA256SUMS` regenerated to match.

**Result after patch 1:** `install.sh --dry-run` **passes** —

```
PASS  payload tree contains ordinary directories and regular files only
PASS  release file inventory exactly matches RELEASE_SHA256SUMS
verify_lock: PASS: lock; packages=56
PASS  ufw active, default-deny inbound, SSH-only
PASS  control port 8790 is closed
PASS  entrypoint binds 127.0.0.1:8790 only
[mtc-bridge] dry-run PASS
```

So CRLF is the **only** blocker at the dry-run boundary. Every other precondition in the install
path is sound.

---

## Defect 2 — `assert_no_writable_paths` can never pass on any venv

The real install proceeds much further — the hash-locked pip install of all 56 pinned distributions
succeeds and `verify_lock: PASS: lock+installed; packages=56` — then dies at the sealing step:

```
PASS  immutable tree carries no write bit (/opt/mtc-bridge/releases/1adf9ae5…)
FAIL  writable path inside immutable release: /opt/mtc-bridge/venvs/1adf9ae5…/bin/python
[mtc-bridge] FATAL: sealed release or venv remains writable
### install exit=1 ###
```

### Diagnosis, verified on the host

`lib/common.sh:98`:

```bash
offenders="$(find "$root" -perm /222 -print -quit 2>/dev/null || true)"
```

There is no `-type` filter. Evidence:

| Query | Result |
|---|---|
| Symlinks in the venv | 4 — `bin/python`, `bin/python3`, `bin/python3.12`, `lib64`; all `lrwxrwxrwx` |
| `find "$venv" -perm /222` (as written) | matches all 4, filetype `l` |
| `find "$venv" \( -type f -o -type d \) -perm /222` | **empty** |
| Symlinks in the release tree | **0** |

Every genuine file and directory *was* sealed correctly to `0444`/`0555`. The only "offenders" are
symlinks, and **symlink permission bits are meaningless on Linux** — the kernel ignores them and
governs access by the target. `chmod` on a symlink changes the target, which is exactly why the
sealing step deliberately restricts its own `chmod` calls to `-type d` and `-type f`.

The assertion passes on the release tree only because `assert_regular_directory_tree` guarantees the
release contains no symlinks at all. A venv created by `python -m venv` **always** contains symlinks.

**Therefore this installer could never have sealed any venv, on staging or on KVM2.** It is not
environment-specific and would have consumed the single bounded `KVM2-P4-02` attempt.

### Suggested fix (implementer's call, not applied to the repo)

```bash
offenders="$(find "$root" \( -type f -o -type d \) -perm /222 -print -quit 2>/dev/null || true)"
```

If symlink *targets* matter for the venv, that is a separate assertion — that no symlink resolves
outside the venv root — and should be written as one rather than conflated with write bits.

**Recon patch 2:** the one-line change above, applied only to the recon copy, manifest regenerated.

---

### Result after patch 2 — the install path is otherwise sound

With patches 1 and 2 applied, `install.sh` completes end-to-end (`EXIT=0`) and `verify.sh` returns
**28 of 28 PASS**:

```
verify_lock: PASS: lock+installed; packages=56
PASS  immutable tree carries no write bit (releases/1adf9ae5…)
PASS  immutable tree carries no write bit (venvs/1adf9ae5…)
PASS  unit declares Restart=no / User=mtc-bridge / ProtectSystem=strict / NoNewPrivileges=yes
PASS  unit has no [Install] section and cannot be enabled
PASS  first-start unit is masked / not active / not enabled
PASS  entrypoint binds 127.0.0.1:8790 only    PASS  control port 8790 is closed
PASS  ufw active, default-deny inbound, SSH-only
[mtc-bridge] VERIFY PASS — installed, masked, unstarted, unarmed
```

End state: `/etc/mtc-bridge` `750 root:root`, env file `600 root:root` with **0 definition lines** and
**0 `HL_LIVE_ACK` lines**. The deployment assets are fundamentally sound; only defects 1 and 2 block
them.

---

## Defect 3 — the suite floor on the real runtime is 26 failures, not 2

The programme's recorded floor is **`2 failed, 1304 passed`**. On the staging host, using the
hash-locked venv that will run the service:

| Tree | Result |
|---|---|
| Windows floor at master (recorded) | `2 failed, 1304 passed` |
| Linux, pristine CRLF payload | `29 failed, 1277 passed` |
| Linux, normalised payload | **`26 failed, 1280 passed`** |

All three collect 1,306 tests, so this is like-for-like. **24 failures beyond the known two.**

### 3a — the baseline was never measured on the deployment Python

This is the headline. The Windows development machine has **Python 3.14.2 and 3.13, and no 3.12**.
The locked runtime is **Python 3.12** (`requirements.lock` was compiled
`--python-version 3.12 --python-platform linux`; the installed venv is 3.12.3).

Direct evidence, `test_order_state.py::test_gc_referents_of_*` (2 failures):

```python
# Python 3.14.2
gc.get_referents(SomeEnum.MEMBER) -> ['str', 'str', 'EnumType', 'int', 'EnumType']   # no dict -> PASSES
# Python 3.12.3
                                  -> exposes the member __dict__ with _sort_order_    # -> FAILS
```

This is a **Python-version** difference, not a Linux one. It means the accepted `2 failed, 1304
passed` floor describes an interpreter the service will never run on.

### 3b — `wal_state_bundle` always reports drift on Linux (~21 failures, safety-relevant)

Every failure carries the same verdict:

```
'failures': ['source_changed_during_capture'],  'verdict': 'INVALID',  'exit_code': 2
'changed_components': ['wal', 'shm']            'changed_during_hash': False   (for the db itself)
```

The main database is stable across the capture. What drifts are SQLite's **`-wal` and `-shm` sidecar
files**, which are necessarily touched on Linux merely by opening a WAL-mode database. `_file_snapshot`
brackets each component's read with `lstat()` and compares `_stable_metadata`
(`tools/wal_state_bundle.py:423`, including `ctime_ns`), so the capture trips its own drift detector.

**Why this matters beyond a test count:** `wal_state_bundle.py` is the tool `COMMANDS.md` Stage E uses
to capture the WAL-consistent state bundle for the **KVM2 ordered single-writer cutover**, and that
stage states explicitly *"Do **not** pass `--allow-live-source`: for a cutover the writer must already
be quiesced, so any source drift during capture is a stop condition, not a warning."* As written, the
cutover therefore **cannot produce a valid state bundle on Linux at all**.

Not yet discriminated: whether 3b is caused purely by Linux filesystem semantics or partly by the
3.12/3.14 difference (Python changed Windows `st_ctime` semantics across those versions). The
discriminating experiment is to run `tests/test_wal_state_bundle.py` on Linux under 3.14, or on
Windows under 3.12. Stating this rather than guessing.

### 3c — the ledger-hash failure is defect 1, not a separate baseline failure

Prediction **P3** (Addendum A §A.3) said the KVM2 ledger-hash test *may legitimately pass on Linux*
because WP-L Phase 1 diagnosed its Windows failure as a CRLF artefact.

**P3 is falsified as stated: the test fails on Linux too.** But the underlying CRLF diagnosis is
*confirmed*, and more precisely than before:

```
MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
  recorded in ledger : f4cdece5098d4e915431f9fd916005bbc3d79ea5af89a0535e3e21d668bda90e
  actual raw sha256  : b6580e31c0a794a83455ce1cfc4efb17a061a34bbe0e9c5b7df1feeb3064114a
  LF-normalised      : f4cdece5…   ← equals the recorded value
  CR bytes in file   : 36
```

The recorded hash **is** the LF hash; the committed file carries CRLF. Moving to Linux cannot fix it,
because the CRLF travels with the file. So this is not an independent pre-existing failure at all —
it is the same repo-wide CRLF defect as #1, and **fixing #1 should make it pass**, removing one of the
two failures the programme has been carrying as accepted baseline noise.

### 3d — the tests do catch CRLF; they were simply never run on Linux

`tests/test_linux_deployment.py` on the pristine tree: `4 failed, 30 passed`. On the normalised tree:
`1 failed, 33 passed`. The three that flip are exactly the tests that *invoke* the shell scripts. The
suite was Linux-correct all along and would have caught defect 1 on day one — it had only ever been
executed on Windows, where CRLF is native.

Also noted: the file contains **34** tests, not the 35 the runbook's A-3 states. Recording the
discrepancy rather than adopting whichever number is convenient.

---

## Repair notes for the implementer

**The runtime-baseline contract is NOT at risk from renormalisation.**
`docs/RUNTIME_BASELINE_CONTRACT.md` lines 67–68 state that file hashes *"normalize CRLF to LF for
text files … before hashing"*, precisely because repo and runtime worktrees are checked out under
different `autocrlf` settings. Changing committed line endings therefore does not move
`source_tree_hash` and does not break TS-P0-001. This was checked before proposing the repair, because
the obvious fear — that renormalising would invalidate the runtime baseline — would otherwise have
made the fix look far more dangerous than it is.

**Scope the renormalisation deliberately.** A repo-wide `git add --renormalize .` would produce an
enormous diff across parity fixtures and generated data. The minimum correct scope is the files Linux
actually parses: `IBKR_PAPER_BRIDGE/deploy/linux/**`, plus any `*.sh` intended to run on Linux.
`.gitattributes` needs explicit `eol=lf` rules for those paths — `* text=auto` alone is what failed
here, because it normalises at `git add` time and these files were staged on Windows before it
applied.

**A rebuild changes the programme's anchors.** A corrected payload produces a new `RELEASE_SHA` and a
new `RELEASE_SHA256SUMS` SHA-256. Every record quoting `1adf9ae5…` / `bfefea2f…` becomes historical,
and Gate A must re-run from A-0.

## Safety

No ARM, no order, no broker connection, no TESTNET, no mainnet, no wallet action, no credential
value. The env file was never populated and `HL_LIVE_ACK` was never set. All work is confined to the
disposable `GATEA-STAGING` VM. KVM2 was not touched.
