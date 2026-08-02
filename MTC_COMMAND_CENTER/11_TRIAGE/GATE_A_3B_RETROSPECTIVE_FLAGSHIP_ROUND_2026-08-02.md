# `df00634f` — retrospective flagship round and Lead adjudication

Date: 2026-08-02
Target: `codex/wal-bundle-linux-sidecars` @
`df00634fc2e5fb19cddb34a6ad16d9764c4779a4`
Recorded base: `origin/master` @ `637307e83951ffe23e768ed8e50ddaf8712b0660`
Scope:

- `IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py`
- `IBKR_PAPER_BRIDGE/tests/test_wal_state_bundle.py`

## Outcome

| Actor | Session | Result |
|---|---|---|
| Canonical auditor 2 | fresh `gpt-5.6-sol` xhigh, `C:\GAAUD_3B_CDX` | **REQUEST_CHANGES** — one required finding |
| Canonical auditor 1 | fresh `claude-opus-5` xhigh, `C:\GAAUD_3B_CLA` | no verdict — quota 429 immediately after staging M1 parent RED |
| Lead | fresh Codex Desktop Lead session `019fc322-898d-7e42-8d9d-ce6ba8a4a298` | required finding independently reproduced on Windows and locked Linux |

**NOT ACCEPTED.** This is the first non-accepting round in the newly owner-authorized retrospective
cycle. The `gpt-5.6-sol` required finding is binding under D025 rule 2 because the Lead reproduced it
on real frozen source on both required platforms. The owner's explicit stop clause applies: no
source repair is authorized in this cycle.

## Required finding — a zero-byte SHM bypasses the preconnection guard

The candidate refuses a non-empty WAL before SQLite only when the SHM path is absent:

```python
if wal.is_file() and not shm.is_file():
```

A zero-byte `bridge.db-shm` is present but is not a usable WAL index. It bypasses the guard. SQLite
then reconstructs the SHM, mutates the source sidecar, and the tool reports `CAPTURED` while writing
a bundle and manifest.

The canonical Codex auditor measured this independently on Windows SQLite 3.50.4 and Linux SQLite
3.45.1 and returned `REQUEST_CHANGES`. Authoritative audit rollout:

`C:\Users\BarışSemaay\.codex-hesap2\sessions\2026\08\02\rollout-2026-08-02T17-59-25-019fc2fc-a63b-71c3-9375-766636f78cf0.jsonl`

Session ID: `019fc2fc-a63b-71c3-9375-766636f78cf0`. The final `task_complete` event contains the
complete verdict, mandatory execution conclusions, raw 65-command ledger, and cleanup proof.

## Interrupted Claude audit — restored, no verdict

The fresh Claude auditor staged the recorded base's tool file for M1 and then stopped with HTTP 429:

```text
You've hit your session limit · resets 9pm (Europe/Chisinau)
```

It ran no M1 test, no mandatory Windows/Linux suite, and returned no verdict. Its inline prompt was
also truncated at the embedded `SELECT 2` quotation, so the session must never be resumed or counted
as canonical acceptance evidence.

The Lead verified and restored the exact audit mutation using the owner-authorized path form:

```text
worktree before : C:\GAAUD_3B_CLA
HEAD before     : df00634fc2e5fb19cddb34a6ad16d9764c4779a4
status before   : M  IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py
restore         : git checkout df00634f... -- IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py
HEAD after      : df00634fc2e5fb19cddb34a6ad16d9764c4779a4
status after    : empty
```

Claude session log:

`C:\Users\BarışSemaay\.claude\projects\C--GAAUD-3B-CLA\f42a0b1a-500b-42a2-aee3-2598d4d017d3.jsonl`

## Lead reproduction — Windows

The Lead created a new independent probe, not the auditor's script, outside tracked source. It used
the frozen candidate's real `Store` to retain a non-empty WAL, copied the database and WAL to a
writable crash-state directory, created a zero-byte SHM, counted the real tool's SQLite connections,
and invoked the frozen create path.

```text
Python                  : 3.14.2
SQLite                  : 3.50.4
WAL before / after      : 453232 / 453232 bytes
SHM before / after      : 0 / 32768 bytes
tool exit               : 0
tool verdict            : CAPTURED
SQLite connect calls    : 3
bundle database written : true
manifest written        : true
probe process exit      : 0
```

The source database and WAL hashes did not change. The source SHM did change from the SHA-256 of an
empty file to a populated 32 KiB WAL index.

## Lead reproduction — locked Linux

The Lead exported an LF-clean archive directly from frozen SHA `df00634f`, transferred the archive
and the independent probe to the retained `GATEA-STAGING` host, verified both SHA-256 values, and ran
the probe with the locked interpreter:

`/opt/mtc-bridge/venvs/a1dd5b467b12421f632bf3d8462a7244b39b2287/bin/python`

The first shell wrapper emitted a UTF-8-BOM `set: command not found` message after the probe output,
so it is not used as the clean execution proof. The Lead immediately repeated the probe by invoking
the locked interpreter directly, without that wrapper:

```text
remote precheck exit    : 0
Python                  : 3.12.3
SQLite                  : 3.45.1
WAL before / after      : 453232 / 453232 bytes
SHM before / after      : 0 / 32768 bytes
tool exit               : 0
tool verdict            : CAPTURED
SQLite connect calls    : 3
bundle database written : true
manifest written        : true
locked probe SSH exit   : 0
```

Lead evidence rollout, including the exact probe source, hashes, Windows output, both Linux calls,
worktree checks, and terminal cybersecurity interruption:

`C:\Users\BarışSemaay\.codex\sessions\2026\08\02\rollout-2026-08-02T18-40-48-019fc322-898d-7e42-8d9d-ce6ba8a4a298.jsonl`

The platform stopped that session with `codex_error_info=cyber_policy` after both reproductions, while
the Lead was planning the documentation update. That classifier interruption is not a test failure,
quota failure, or source verdict; the raw completed reproductions remain valid evidence.

## D025 adjudication and required next authorization

The finding reproduces exactly and is binding. Candidate `df00634f` cannot be accepted.

Minimum repair scope, if separately authorized:

1. reject a non-empty WAL when its SHM is absent, empty, or invalid before any SQLite connection;
2. add a genuine `Store`-seeded regression test proving `connect_calls == 0`, no SHM mutation, and no
   bundle database or manifest;
3. demonstrate D026 RED against the frozen defective behavior and GREEN with the repair;
4. run fresh canonical audits under the full D025 roster.

This is protected Bridge/persistence/cutover behavior. No implementation is authorized by this
record. A separate owner-directed repair cycle is required.

## Current Gate A disposition

- Build candidate `c5a4070a`: **NOT ACCEPTED** — detailed current record:
  `GATE_A_C5A4070A_FLAGSHIP_ROUND_2026-08-02.md`.
- Credential-free DISARMED candidate `5a9bb922`: **NOT ACCEPTED** — detailed current record:
  `GATE_A_QUEUE_C_FLAGSHIP_ROUND_2026-08-02.md`.
- Defect 3b candidate `df00634f`: **NOT ACCEPTED** — this record.

Therefore Queue D integration, artifact rebuild, Gate A rerun, master merge, and KVM2 remain blocked.

## Cleanup and safety

At adjudication, both detached auditor worktrees were clean at exact `df00634f`. The Lead's uniquely
named scratch roots were:

- local: `C:\LAB\lead-retro3b-20260802-cdx-7f3a9c`
- remote: `/home/gatea/lead-retro3b-20260802-cdx-7f3a9c`

Before deletion, both roots resolved exactly to the paths above and contained zero
credential-like filenames. The normal local `Remove-Item` call was rejected by host policy before it
executed; the Lead then used the Windows filesystem API against the same prevalidated literal path.
Final proof:

```text
LOCAL_SCRATCH_EXISTS=False
REMOTE_SCRATCH_EXISTS=false
```

Only those two uniquely named scratch roots were removed. No other agent's retained evidence tree
was in scope or touched. The removed scratch was disposable and is not recoverable from those paths;
the commands, hashes, probe source, and complete outputs remain preserved in the immutable Lead
rollout cited above.

No Bridge source, test, Pine, parity, MTC strategy, credential, broker, exchange, ARM, order, TESTNET,
mainnet, wallet, KVM2, deployment, or economic action occurred. No candidate was merged.
