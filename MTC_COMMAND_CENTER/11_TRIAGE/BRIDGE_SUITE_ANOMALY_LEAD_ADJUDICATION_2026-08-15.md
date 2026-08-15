# Lead adjudication — Bridge suite anomaly repairs — 2026-08-15

Status: **ACCEPTED AT T1. NOT MERGED. NOT A RELEASE.**

## Subject

Branch `codex/bridge-suite-anomaly-repairs-20260815`, in worktree `C:\P10FIX`.

| commit | contents |
|---|---|
| `678d4be2` | base — the WP-I branch tip at dispatch |
| `6c746b65` | the two repairs plus the implementer report |
| `7d4e9a96` | the independent T1 audit |

Changed by the repair, verified against `git diff --stat 678d4be2 6c746b65`:
`.gitattributes` (+1), `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py` (+9/-1),
and one new report. Nothing else — no product code, nothing under `WPI_*`.

## What was fixed

**A1** — `EVIDENCE_LEDGER.jsonl` records the Git-object (LF) hash of
`ledger_schema.json`, but `validate_ledger.py` hashes the working-tree file,
which is CRLF on Windows under `* text=auto`. Fix: one narrow `.gitattributes`
rule pinning that path to `eol=lf`.

**A2** — `test_invariants_preserve_risk_and_history` asserted
`schema_version == "2"` against a baseline that moved to 4. Fix: read the schema
version out of the fixture's source database and assert the manifest matches it,
so the test cannot go stale again and still fails if the bundle lies.

## Roster and results

| role | model | result |
|---|---|---|
| implementer | Codex `gpt-5.6-sol`, high, isolated | 1021 passed, twice |
| auditor | Claude `claude-opus-5`, fresh, no shared context | **PASS-WITH-NITS**, 4 nits, 0 required |

Cross-model as T1 requires. The auditor reproduced rather than trusted: it proved
A2's discriminating power by wrapping `wal.main` and running the real test, and
independently confirmed the A1 pin holds for a fresh clone.

The Lead separately verified A1 before the audit returned: in `C:\P10FIX` the
file is 867 bytes with SHA-256 `f4cdece5…`, matching the ledger, and a fresh
`git clone` of the branch produces the same 867 bytes and the same hash.

## Disposition

Accepted at T1. The four nits are backlog, not repairs, and changing the audited
bytes to address them would reopen the tier for no correctness gain.

**One nit needs an operational action rather than a code change.** NIT-1 is
correct and it bites right now: the blob for `ledger_schema.json` is identical in
`678d4be2` and `6c746b65`, so a pre-existing Windows checkout that merely fetches
this commit keeps its stale CRLF copy and A1 recurs there. `C:\P10BASE` is in
exactly that state. Anyone taking this commit into an existing Windows checkout
must run, once:

```bash
git checkout -- MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/ledger_schema.json
```

or `git add --renormalize .`. A plain fetch will not fix it. The Linux deploy
target clones fresh and was never affected. This instruction is recorded here and
in the morning handoff instead of being patched into the audited report.

## What this does not do

It does not merge, does not create a release candidate, and does not satisfy
deploy checklist item 9. That item needs the full suite green at the **exact
frozen release SHA in the locked environment**, and this result is provisional:
local pytest is 9.0.2 on Python 3.14.2 while `IBKR_PAPER_BRIDGE/requirements.lock`
pins `pytest==9.1.1`.

The release-integration design
(`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md`) assumes these two repairs are
correctly fixed and replays them semantically onto the integrated line. That
assumption is now backed by a cross-model T1 acceptance rather than by one
implementer's self-report.

No host, network, deployment, service, credential, broker/exchange, ARM, order,
TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or economic
action was authorized or performed.
