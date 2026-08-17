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

Full evidence in `GATE_A_RESULT_2026-08-02.md`. Summary: in the **artifact**, 19 of 19 shell scripts,
both systemd unit templates, the logrotate policy and the env contract carry CRLF. `install.sh` dies
on line 37 with `$'\r': command not found`.

> **ROOT CAUSE CORRECTED 2026-08-02.** This originally read "root cause is the committed blob …
> present on `origin/master`". **Wrong**, and caught by an independent `gpt-5.6-sol` audit. The
> committed blobs are **LF-only**; the repository is clean. Proof without any pipe: blob sizes
> (`git cat-file -s`) are 19,908 / 8,153 / 3,489 / 867 against artifact sizes 20,342 / 8,373 / 3,580
> / 903 — each diff exactly that file's CR count — and `od` finds zero `0x0d` bytes in the blobs.
> The CRLF is introduced at **build time**: `package.sh:73` runs bare `git archive` while the repo
> has `core.autocrlf=true`. Demonstrated: `git archive` → 20,342 bytes;
> `git -c core.autocrlf=false -c core.eol=lf archive` → 19,908 = the blob size.
> The original measurement used `git cat-file blob … | grep -c $'\r'` through a Git Bash pipe that
> translated git's stdout — the exact trap this programme already documents.

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

**Therefore this installer cannot seal the venv it actually creates, on staging or on KVM2**, and
would have consumed the single bounded `KVM2-P4-02` attempt.

> **Scope corrected 2026-08-02** after `gpt-5.6-sol` audit. The original wording — "could never pass
> on *any* venv, always, on any host" — was overstated. A venv with no symlinks at all could pass;
> the claim is not universal.
>
> It survives for every path this installer takes, and the obvious escape does not work. Reproduced
> on the host, sealing exactly as `install.sh:317-319` does:
>
> ```
> default venv (what install.sh:291 creates): ASSERTION FIRES -> bin/python   (lrwxrwxrwx)
> --copies venv (the hypothetical escape)   : ASSERTION FIRES -> lib64 -> lib (lrwxrwxrwx)
> ```
>
> `--copies` removes the three `bin/*` symlinks but CPython still creates `lib64 -> lib` on 64-bit
> POSIX, so the assertion fires anyway. And `install.sh:290` does not pass `--copies`. The
> operational conclusion is unchanged; only the universal phrasing was wrong.

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

**Established:** the main database is stable across the capture (`changed_during_hash: False`); what
the tool reports as changed are SQLite's **`-wal` and `-shm` sidecar files**. `_file_snapshot`
brackets each component's read with `lstat()` and compares `_stable_metadata`
(`tools/wal_state_bundle.py:423`, which includes `ctime_ns`).

**A lead for the implementer, not a conclusion:** after a clean `close()` of a WAL-mode SQLite
database, only `bridge.db` exists on disk — the `-wal` and `-shm` files are created by whoever next
*opens* it. The capture opens the source in order to read it. So the sidecars plausibly transition
absent → present *during* the very window the tool brackets, which would explain the verdict without
any metadata subtlety at all. This was not proven here: a direct probe was blocked because
`wal_state_bundle.py` requires the full bridge schema and rejects a toy database. Someone should
confirm it against the real fixture before designing the fix.

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

The recorded hash **is** the LF hash — and it is exactly the committed blob's hash, since the blob is
LF (867 bytes, `f4cdece5…`). The *artifact copy* carries CRLF because `git archive` converted it, so
moving to Linux cannot fix it: the CRLF travels with the payload.

**Confirmed empirically, not merely inferred.** Normalising just that one file on the recon copy:

```
before :  903 bytes   sha256 b6580e31…
after  :  867 bytes   sha256 f4cdece5…   = exactly what EVIDENCE_LEDGER.jsonl records
test   :  1 passed in 0.35s
```

So this is **not an independent pre-existing failure at all** — it is defect 1, and a correctly built
payload makes it pass. One of the two failures the programme has carried as accepted baseline noise
simply disappears.

That puts the true Linux floor for a correctly-built payload at **25** failures, not 26: ~21
`wal_state_bundle` (3b) and 2 `order_state` gc-referents (3a), plus the `schema_version == "2"` case.

### 3d — the tests do catch CRLF; they were simply never run on Linux

`tests/test_linux_deployment.py` on the pristine tree: `4 failed, 30 passed`. On the normalised tree:
`1 failed, 33 passed`. The three that flip are exactly the tests that *invoke* the shell scripts. The
suite was Linux-correct all along and would have caught defect 1 on day one — it had only ever been
executed on Windows, where CRLF is native.

Also noted: the file contains **34** tests, not the 35 the runbook's A-3 states. Recording the
discrepancy rather than adopting whichever number is convenient.

---

---

## Defect 4 — the service cannot start without broker credentials, which Gate A forbids

**This is the most consequential finding, because it makes A-4 unexecutable as written.**

Starting the installed unit fails in 620 ms:

```
RuntimeError: Hyperliquid credentials not found: set both HL_ACCOUNT_ADDRESS
and HL_API_WALLET_KEY in the process environment or in HKEY_CURRENT_USER\Environment
  bridge/app.py:229  -> create_app(... start_runtime=True)
  bridge/app.py:114  -> runtime_broker = broker or _build_broker(root, dry_run)
  bridge/app.py:201  -> resolve_hyperliquid_credentials()
```

The unit's `ExecStart` is `python -m bridge.app` with **no** `--dry-run`, so a real
`HyperliquidBroker` is constructed at startup and credentials are mandatory.

### The contradiction

| Source | Requirement |
|---|---|
| Gate A runbook §0 | *"DISARMED only. No ARM. No order. **No broker credentials.**"* |
| Gate A runbook A-4 | *"**Start the service.** Confirm `app_state` is durably not `ARMED` …"* |
| The artifact | refuses to start unless `HL_ACCOUNT_ADDRESS` + `HL_API_WALLET_KEY` are present |

These cannot all hold. A-4 — described in the runbook as *"the most important check in the gate"* and
*"the whole point of the 50 hours"* — **cannot be executed under Gate A's own stated boundary.**

Note this is *not* a contradiction with `COMMANDS.md`, whose ordering is deliberate: Stage D
(`KVM2-P4-03`, secret provisioning) precedes Stage F (`KVM2-P4-06/07`, the one DISARMED start). The
conflict is between the artifact's startup requirement and **Gate A's** credential-free boundary.

### The one genuinely good thing this proved

The failure is **fail-closed**, and that is worth recording as evidence in its own right.
`app.py:106-110` initialises the store and writes `app_state=DISARMED` *before* `_build_broker` is
reached (`:113-114`). So a credential-absent start leaves the system durably DISARMED rather than in
an ambiguous state.

> **Qualified 2026-08-02** after `gpt-5.6-sol` audit: this holds for a **fresh or non-`KILLED`**
> database only. `app.py:109` reads `if store.get_meta("app_state") != "KILLED"` before writing
> DISARMED, so an existing `KILLED` state is deliberately preserved rather than overwritten — which
> is correct behaviour, not a defect. The original wording implied the DISARMED write was
> unconditional. It is not.

Observed:

```
db app_state = DISARMED          NRestarts = 0  (Restart=no held)
no listener on 8790              no broker connect/auth lines in the journal
```

That is a real, if partial, piece of A-4's substance: the system's behaviour under missing
credentials is safe.

### Why `--dry-run` is not the answer

`_build_broker` avoids credentials only when `dry_run=True`, in which case it wires
`MockBroker.from_csv(root/"tests"/"fixtures"/"BTC_1h.csv")`. Starting the production service against
a test fixture is not a legitimate DISARMED start and must not be used to manufacture an A-4 pass.

### Decision required from the owner — not the Lead's to make

Either:

- **(a)** give the bridge a genuine credential-free DISARMED start mode. A bridge that is DISARMED
  and cannot trade arguably should not need trading credentials merely to boot; or
- **(b)** re-scope A-4 to run after Stage D with TESTNET credentials provisioned — which breaches
  Gate A's §0 boundary and therefore needs explicit owner authorisation.

Both change the programme's plan, so neither was chosen here.

---

## Recon results for A-8 and A-9

Run for completeness while the host was available. Still **not** Gate A evidence.

**A-8 — loopback-only exposure.** No non-loopback listener on 8790. Host listeners are SSH (22) and
systemd-resolved (127.0.0.53/127.0.0.54:53) only. `ufw` active, default-deny inbound, SSH-only.

**A-9 — secret scan on the INSTALLED tree.** Zero hits across all nine signature categories, on both
`/opt/mtc-bridge/releases/1adf9ae5…` and `/etc/mtc-bridge`:

```
private_key_block 0   aws_access_key 0   github_token 0   slack_token 0   openai_token 0
anthropic_token 0     xai_token 0        telegram_bot_token 0            ethereum_private_key 0
TOTAL_CATEGORY_PATH_HITS=0   (both trees)

/etc/mtc-bridge/mtc-bridge.env  600 root:root   definition lines: 0   HL_LIVE_ACK lines: 0
```

`SECURITY_BASELINE.md` states its own scan *"excludes … an after-build scan of the immutable
payload."* This is that missing scan, and it is clean.

**A-5 could not run** — it requires a running service, which defect 4 prevents.

---

## A correction to my own method, recorded deliberately

The A-4 script contained the exact flaw this programme keeps paying for. It handled one vacuous-pass
trap (a wrong `x-confirm` header returns 409, which resembles a real ARM refusal) but left another
open: when the service failed to start, `curl` returned `http=000` (connection refused) and the
script logged `PASS ARM did not succeed`.

**That "PASS" is worthless** — nothing was listening, so nothing was tested. It is not counted as
evidence anywhere in this file, and the ARM-refusal path remains **untested**. Recording this because
"always ask what would make the assertion fail" is the programme's own rule, and a check that passes
because the target is absent is precisely the failure mode it warns about.

---

## Defect 5 — the build is not reproducible, and that is the real disease

Raised by the `gpt-5.6-sol` audit as *"the most important missed defect"*, and it is right. Defects 1
and 5-as-symptoms are downstream of this:

**The same `RELEASE_SHA` produces different payload bytes, and therefore a different
`RELEASE_SHA256SUMS` hash, depending on the builder's line-ending configuration.**

```
git archive 1adf9ae5 …/install.sh                       ->  20,342 bytes   manifest hash bfefea2f…
git -c core.autocrlf=false -c core.eol=lf archive …     ->  19,908 bytes   different manifest entirely
```

That silently breaks the artifact model the whole programme rests on. `--release-sha` and
`--manifest-sha256` are supposed to bind a payload to a commit; if the commit alone does not
determine the bytes, two "identical" builds are not identical, and a manifest hash recorded on one
machine is meaningless on another.

The durable repair is therefore not "strip the CRLF" but **pin export behaviour** so that a given
`RELEASE_SHA` always yields byte-identical output — via explicit `eol=lf` attributes, an
`autocrlf`-independent `git archive` invocation in `package.sh`, or building only on Linux. Ideally
`package.sh` should also *assert* the property: re-export and compare, or verify a known manifest
hash, so a misconfigured builder fails loudly instead of shipping a subtly different payload.

### A scope trap in the narrow fix

An `eol=lf` rule covering only `IBKR_PAPER_BRIDGE/deploy/linux/**` would fix the installer but **not**
the ledger failure (3c) — `ledger_schema.json` lives under
`MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/`. Any fix scoped to the deployment directory
alone leaves that test failing and leaves other payload files environment-dependent. Whatever is
chosen must cover everything the payload contains, not just the scripts that happen to be executed.

## Repair notes for the implementer

**The runtime-baseline contract is NOT at risk from renormalisation.**
`docs/RUNTIME_BASELINE_CONTRACT.md` lines 67–68 state that file hashes *"normalize CRLF to LF for
text files … before hashing"*, precisely because repo and runtime worktrees are checked out under
different `autocrlf` settings. Changing committed line endings therefore does not move
`source_tree_hash` and does not break TS-P0-001. This was checked before proposing the repair, because
the obvious fear — that renormalising would invalidate the runtime baseline — would otherwise have
made the fix look far more dangerous than it is.

**Do NOT renormalise committed content.** *(Corrected — the original text here called for
`git add --renormalize`, which was based on the wrong root cause.)* The committed bytes are already
LF and correct. The fix belongs in the build:

```bash
# package.sh:73 — export without line-ending conversion
git -c core.autocrlf=false -c core.eol=lf archive "${RELEASE_SHA}" ...
```

Optionally add explicit `eol=lf` attributes for `IBKR_PAPER_BRIDGE/deploy/linux/**` and the other
Linux-parsed paths so the export is deterministic whatever a builder's local `core.autocrlf` is.
That changes attributes, not content.

**A rebuild still changes the programme's anchors.** Fixing `package.sh` requires a commit, so expect
both `RELEASE_SHA` and the `RELEASE_SHA256SUMS` SHA-256 to move; records quoting `1adf9ae5…` /
`bfefea2f…` become historical, and Gate A must re-run from A-0.

**TS-P0-001 was never at risk** — and now doubly so, since committed content is not being touched at
all. (`RUNTIME_BASELINE_CONTRACT.md` lines 67-68 normalise CRLF to LF before hashing in any case.)

## Safety

No ARM, no order, no broker connection, no TESTNET, no mainnet, no wallet action, no credential
value. The env file was never populated and `HL_LIVE_ACK` was never set. All work is confined to the
disposable `GATEA-STAGING` VM. KVM2 was not touched.
