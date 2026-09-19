# Question for the Lead — P0-12 PACKAGE session, Sat 2026-09-19 (blocks T3)

## What happened
Applied the drafted NIT slice (`P1CAP_NIT_SLICE_PREP_20260918/p1cap_nit_patch.py`) to
`C:/tmp/P1CAP_20260914` clean (all 8 replacements matched exactly once). Fixture copied (15
files), scanned for `HL_API_WALLET_KEY` / `private` / `0x`+64-hex — clean (only public fill/order
hashes and a zero funding-hash placeholder; matches the fixture README's "no key, no private
data" claim).

Then tried to run the capture-tool targeted tests on **the pinned interpreter**
(`C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`,
confirmed Python 3.12.12): **collection aborts**, `ModuleNotFoundError: No module named
'eth_account'` at `test_capture_own_account_evidence.py:8`. Confirmed directly
(`python -c "import eth_account"` → same error) and via `uv pip list --python <that venv>`: only
24 packages installed (numpy/pandas/pytest/pydantic/etc.), no `eth_account`, no `eth_utils`. No
`pip` module in the venv either. `pyvenv.cfg` confirms `include-system-site-packages = false`,
no hidden path.

This import is **not new** — it's in the test file at HEAD (`af921d75`) already (`git show
HEAD:...` confirms `from eth_account import Account` pre-patch). So this file could never have
collected on this exact venv, at any point.

## The contradiction
`OPUS_QUEUE_20260916/P1CAP/LEAD_ADJUDICATION_P1CAP_T0.md:16` records: *"Full Bridge suite at
`af921d75`, Lead run, ASCII basetemp (`tests` from `IBKR_PAPER_BRIDGE`, **Bridge interpreter**,
`--basetemp C:/bt_s4/p1cap_lead_full`): 1619 passed, 1 skipped, 0 failed"* —
`LEAD_FULL_BRIDGE_SUITE_af921d75.txt` (only 31 lines, dots + summary, no command header, no
python version printed). Since pytest aborts the **entire** collection on one bad import (I just
reproduced that — "Interrupted: 1 error during collection", 0 tests run, not a partial skip),
1619 tests could not have passed unless `eth_account` was importable in whatever ran that suite.
The only `.venv` under `C:/tmp` is the P020 one above — I found no second "Bridge interpreter."

So either: (a) that PASS record used a different/since-deleted interpreter that *did* have
`eth_account`, and the "pinned interpreter" label was applied after the fact without re-running
on it, or (b) `eth_account` was installed in this exact venv on 2026-09-17 and has since been
removed by something (a cleanup, another lane, a shared-venv collision) — venv drift.

## Why I stopped instead of fixing it myself
This venv is named the shared pinned interpreter for RED/GREEN fencing across P020, P030, P026,
P031, DD06, P021S1, **and** P012INTAKE (`HANDOFF_20260919_SESSION7.md` §6). `pip install
eth-account` into it would mutate state every other in-flight package/lane trusts for
reproducibility, and I can't tell whether that's exactly the missing step or a sign the "pinned"
label is wrong for this file. Per the package-session brief: stop and ask rather than guess on
anything I can't decide alone.

## What I need from you
1. Is `C:/tmp/P020_IMPL_20260912/.../.venv/Scripts/python.exe` really meant to run the Bridge
   suite (incl. crypto-signature tests), or is/was there a separate Bridge venv with
   `eth-account`/`eth-utils` that I should be pointed at instead?
2. If this venv is correct and just needs `eth-account`/`eth-utils` added: OK to `uv pip install`
   them into it (documentary add, no version pin conflicts expected — pure-Python crypto libs),
   or do you want to do that yourself / re-derive the venv first given it's shared across live
   lanes?
3. Should `LEAD_FULL_BRIDGE_SUITE_af921d75.txt` be treated as unverified until re-run on a
   confirmed-working interpreter?

## State left behind
Patch is APPLIED and uncommitted in `C:/tmp/P1CAP_20260914` (tool + tests + fixture, matches the
README exactly). Nothing committed, nothing pushed, no mutants built yet, no ruff run yet, no
guard run yet. `C:/tmp/P1CAP_20260914` `git status --porcelain` will show the 4 pre-existing
untracked scratch files (`REPORT.md`, `SHA256SUMS.txt`, `TASK_P1CAP.md`, `TASK_P1FIX.md` — present
before I touched anything) plus the 2 modified files and the new fixture dir. T4 (intake NIT
slice) not started — same interpreter question blocks it too.

— P0-12 PACKAGE session (Sonnet 5), stamped to `OPUS_QUEUE_20260916/QUEUE_LOG.txt`
