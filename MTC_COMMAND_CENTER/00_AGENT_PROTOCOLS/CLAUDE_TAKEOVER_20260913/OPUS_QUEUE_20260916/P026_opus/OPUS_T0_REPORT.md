# T0 review — WP-P0-26 completion-marker repair, candidate `e114ed314fa2545b5c64399ddb024e4d75289c14`

Reviewer: exact `claude-opus-5`, effort xhigh. Wednesday 2026-09-16 slot, lane 4 (run 2026-09-17).
Subject: `C:/tmp/P026_REPAIR_20260915` (read-only). No `git status/diff/add/commit/checkout` was run in any
repository; only `rev-parse`, `show <rev>:<path>` and `diff fcac0ac6 e114ed31` (read-only byte comparison).
Scratch for RED arms: `C:/tmp/OPUS_P026_SCRATCH/`. Nothing written outside this report directory and that scratch.

---

## 0. Verified identities (COMPUTED)

```
$ git -c safe.directory=* -C C:/tmp/P026_REPAIR_20260915 rev-parse HEAD
e114ed314fa2545b5c64399ddb024e4d75289c14          <-- matches the pinned candidate
$ python -c "import sys; print(sys.version)"       (pinned interpreter)
3.12.12 (main, Jan 27 2026, 23:45:36) [MSC v.1944 64 bit (AMD64)]
C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe
```

SHA-256 of the subject files at HEAD (computed by me, `Get-FileHash`):

| file | sha256 | bytes |
|---|---|---|
| `MTC_COMMAND_CENTER/tools/opsa/backup.py` | `e7f74464ac7a197c2154e98885f5f734a7e5ffabfaa915cf6bd91df06c232fce` | 14020 |
| `MTC_COMMAND_CENTER/tools/opsa/restore.py` | `9836bfe59f6268ed2bd90949f7ce19461bda7b791360e43de4f012e007f1222b` | 16585 |
| `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py` | `e2b3d386abdb42852fe005be9ac451bf7f89770d5892ec056c1738f0fd8063e1` | 14568 |
| `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | `141dbd0e6c2dc7d566f05aed4986e76b9afa40e198de33ca7278631adc27ec3e` | 44857 |
| `MTC_COMMAND_CENTER/tools/opsa/README.md` | `a5d626e75fa704e0e035727adac4efa30840507ed84f5a2f15aa0c4b1fe2cca7` | 6552 |
| `MTC_COMMAND_CENTER/tools/opsa/watchdog.py` | `0d4ba79dc4cedc32128a13943332f7574aa3a459cacaf399b81ee4dbe785376a` | 14700 |
| `MTC_COMMAND_CENTER/tools/opsa/heartbeat.py` | `38b43d72548de0496be40502b98b9ff8e7c019706d467da2a6c109d13ac507e6` | 4443 |
| `p030_closed_partition_backup_adapter.py` | `60a0e7af31d884ebfa349313cf0795422cb2622ef7325e729389e1b40d51bcd9` | 32173 |
| `check_p030_closed_partition_backup_adapter.py` | `ef777b3f46aa92b3eb84abe41b87d4d5d36fcbf7499514a5eb4df2fc90324d2a` | 84736 |

Cross-check against the Lead's own record `SHA256SUMS_d81b07f6_slice3.txt`: **all five recorded code hashes match
mine byte-for-byte** (`backup.py`, `restore.py`, `opsa_common.py`, `test_opsa.py`, the checker). `watchdog.py`
also matches the pre-change base hash recorded in `BASE_SHA256SUMS_fcac0ac6.txt` (`0d4ba79d…`) — the watchdog
half is genuinely untouched by this candidate.

Mandated commands, run by me with `-B` and `PYTHONDONTWRITEBYTECODE=1`:

| command | cwd | observed |
|---|---|---|
| `python -m unittest test_opsa -v` | `…/MTC_COMMAND_CENTER/tools/opsa` | `Ran 39 tests in 2.057s` … `OK` |
| `python check_p030_opsa_heartbeat_adapter.py` | worktree root | `Ran 10 tests in 0.111s` … `OK`, exit 0 |
| `python check_p030_closed_partition_backup_adapter.py` | worktree root | `Ran 45 tests in 4.324s` … `OK`, exit 0 — **with an ASCII `TEMP`**; see NIT-3 |
| `ruff check --select E9,F821,F811,F401,F841` (ruff 0.16.4) | worktree root | `All checks passed!` exit 0, on `tools/opsa` and on both repo-root adapter files |

Scope diffs (read-only):

```
$ git -c safe.directory=* diff fcac0ac6 e114ed31 --stat
 MTC_COMMAND_CENTER/tools/opsa/README.md       |   8 +-
 MTC_COMMAND_CENTER/tools/opsa/backup.py       | 103 +++++++-
 MTC_COMMAND_CENTER/tools/opsa/opsa_common.py  |  82 +++++++
 MTC_COMMAND_CENTER/tools/opsa/restore.py      | 102 ++++++--
 MTC_COMMAND_CENTER/tools/opsa/test_opsa.py    | 334 ++++++++++++++++++++++++--
 check_p030_closed_partition_backup_adapter.py |  97 +++++++-
 p030_closed_partition_backup_adapter.py       |  22 +-
 7 files changed, 692 insertions(+), 56 deletions(-)

$ git -c safe.directory=* diff d81b07f6 e114ed31 --stat
 MTC_COMMAND_CENTER/tools/opsa/README.md | 8 +++++---
 1 file changed, 5 insertions(+), 3 deletions(-)      <-- README alone, as claimed

$ git -c safe.directory=* diff fcac0ac6 e114ed31 --summary
(empty)                                               <-- no file created, deleted or renamed
```

---

## 1. Packet conformance, clause by clause

Authority read from the packet itself (`C:/tmp/P026_LOCAL_SCOPE_DECISION_20260907.md`), not from a summary.

| Packet §4 clause (quoted) | Code | Verdict |
|---|---|---|
| "Each successful backup run emits a per-run immutable `RUN_MANIFEST.jsonl` (file list, sizes, hashes) plus `COMPLETE.json`" | `backup.py:240-283` `write_completion_evidence`; manifest = header + every `file`/`dir`/`skipped` record (`backup.py:255-258`); marker carries `files/bytes/skipped/dirs/run_manifest_sha256` (`backup.py:266-276`) | IMPLEMENTED-AS-WRITTEN |
| "written atomically and only after every readback hash passes" | Gate: `if not errors:` at `backup.py:220` — the evidence is written only on a zero-error run; a readback MISMATCH appends an error (`backup.py:197-200`) so it can never reach the writer. The per-run manifest is itself readback-verified before the marker is written (`backup.py:265-267`: re-hash from disk, compare to the in-memory digest). "Atomically": `write_once_bytes` = `open(path,"xb")` + write + flush + fsync (`opsa_common.py:153-165`), **no tmp + rename** | PARTIAL on the literal word, see NIT-2; the *guarantee the clause protects* is obtained (proved by arms A12/A13) |
| "A partial/interrupted run has no completion marker." | Arms A1, A4, A12: interrupted copy and readback-mismatch runs leave neither file; `run_end` reports `status: partial`, `completion_marker: none`, rc 1 | IMPLEMENTED-AS-WRITTEN |
| "Once written, manifest and marker are never rewritten." | `O_EXCL`; arm A11: `write_once_bytes` on an existing marker raises `FileExistsError`, bytes unchanged. `backup.py:261-263,279-281` convert that into a refusal, not an overwrite | IMPLEMENTED-AS-WRITTEN |
| "Restore consumes an explicit completed run ID and fails closed: no run without a matching `COMPLETE.json` + `RUN_MANIFEST.jsonl`" | `restore.py:146-152` (no id → rc 3; unknown id → rc 3), `restore.py:188-194` gate before any hash check or write; `verify_completion_evidence` `restore.py:71-112` | IMPLEMENTED-AS-WRITTEN |
| "no execution on hash mismatch" | Marker↔manifest digest: `opsa_common.py:217-221`. Per-file: `verify_backup_file` unchanged, still rc 1 (suite `test_restore_refuses_tampered_backup`, `test_check_only_detects_corruption_writes_nothing`) | IMPLEMENTED-AS-WRITTEN |
| "`--latest` (greatest-started-run selection) is removed; restore without an explicit run ID errors." | argparse `--run` required, `--latest` deleted (`restore.py:292-295`); `select_run(None)` raises (`restore.py:58-59`); API path prints and returns rc 3 (`restore.py:146-149`). CLI test asserts argparse rc 2 for `--latest` | IMPLEMENTED-AS-WRITTEN |
| "Additive only: every existing interface not named above stays as-is." | `git diff` shows no change to `run_start`/`file`/`dir`/`skipped`/`run_end` record shapes and none to `backup.py`'s argparse; heartbeat and watchdog untouched. Two stdout summary lines gained keys (`completion_marker` in backup's, `completion_marker` + `run_manifest_sha256` in restore's, `restore.py:200-201`) — additive keys on a human/JSON summary, no manifest record and no consumer parses them | IMPLEMENTED-AS-WRITTEN |
| §5 falsifications 1-4 | Present and green: `test_interrupted_run_has_no_completion_marker_and_restore_refuses`, `test_completed_run_restores_by_explicit_id_including_copied_run_directory`, `test_tampered_marker_or_run_manifest_is_refused`, `test_restore_without_explicit_run_id_fails_closed` | IMPLEMENTED-AS-WRITTEN |
| §5 falsifications 5-7 (watchdog) | Already on master in `53d33dbc`; the three tests run green in this suite; `watchdog.py` hash equals the base hash | out of this candidate's scope, verified present |
| §4 "no deletion primitive" | `NoDeleteGuaranteeTests::test_no_delete_calls_in_opsa_tools` passes; `write_once_bytes` adds no unlink/rmtree | IMPLEMENTED-AS-WRITTEN |

**On "atomically" (explicitly asked).** The clause's purpose is that no partial marker can be mistaken for a
complete one. That property holds, and I proved it rather than reasoned it:

- Crash **after** `RUN_MANIFEST.jsonl`, **before** `COMPLETE.json` (arm A12): restore refuses, rc 3,
  `"detail": "... no completion marker (COMPLETE.json absent)"`. The lone manifest is inert — nothing reads it
  unless the marker admits it first.
- Crash **inside** the `COMPLETE.json` write (arm A13, half the bytes on disk): refused, rc 3,
  `"completion marker unreadable: Expecting property name enclosed in double quotes: line 8 column 41"`.
- A torn marker also cannot be forged into consistency: the digest binding is one-directional (marker names the
  manifest's hash), so truncating the *manifest* instead breaks `run_manifest_sha256` (arm A2).

So the ordering (manifest first, marker last, marker carries the manifest's digest) buys the safety that
`O_EXCL` alone does not. What the implementation does **not** buy is atomic publication, and that has one real
residue — see NIT-2.

---

## 2. Fail-open hunt — my own RED arms

Scratch module `C:/tmp/OPUS_P026_SCRATCH/opus_red_arms.py` and `opus_crash_arms.py`, written by me (not copies of
the Lead's tests), importing the candidate's modules read-only. Command for every arm below:

```
cd C:/tmp/OPUS_P026_SCRATCH
set PYTHONDONTWRITEBYTECODE=1 ; TEMP=TMP=C:\tmp\OPUS_P026_SCRATCH\ascii_tmp
C:/tmp/P020_IMPL_.../.venv/Scripts/python.exe -B opus_red_arms.py "C:/tmp/P026_REPAIR_20260915/MTC_COMMAND_CENTER/tools/opsa"
C:/tmp/P020_IMPL_.../.venv/Scripts/python.exe -B opus_crash_arms.py
```

| arm | attack | observed | verdict |
|---|---|---|---|
| A1 | interrupted run (copy dies on file 2) restored by explicit id | backup rc=1, `COMPLETE.json=False RUN_MANIFEST=False`, restore **rc 3** `{"error": "run_not_complete", "detail": "… no completion marker (COMPLETE.json absent)"}`, target never created | REFUSED |
| A2 | `RUN_MANIFEST.jsonl` edited **after** the marker was written (one field) | **rc 3** `"per-run manifest hash mismatch (marker=b2ca2e9e14fe1f81… actual=fadd77d6e345afb9…)"` | REFUSED |
| A3 | another run's **valid, self-consistent** `COMPLETE.json` + `RUN_MANIFEST.jsonl` copied into run A's dir | **rc 3** `"completion marker names run 'opsa-…823.002Z'"` | REFUSED |
| A4 | readback MISMATCH (errors>0) run | `run_end` = `status: partial, errors: 1, completion_marker: none`, no files on disk, restore **rc 3** | REFUSED |
| **A5** | **Gemini F-01 shape**: hand-built, internally consistent, **digest-bound** pair for a run the tool never closed | `load_complete_marker` alone **accepts it** (`True`); `run_restore` **rc 3** `"global manifest run_end is status='partial' with 1 error(s); only a run the backup tool closed successfully may be restored"` | REFUSED — the F-01 fix is real and load-bearing |
| A6 | per-run manifest rebuilt listing **fewer** files, with `run_manifest_sha256` **and** `files` recomputed to stay consistent | **rc 3** `"per-run manifest file records differ from the global manifest"` | REFUSED |
| A7 | restore root copied **without** `runs/<id>/` evidence (the adapter shape) | **rc 3** `"… COMPLETE.json absent"` | REFUSED |
| A8 | run id given by **prefix** only | **rc 3** `error: run id not found in manifest: opsa-20260917T100823.` | REFUSED |
| **A9** | `COMPLETE.json` `readback` → `"MISMATCH"`, plus `bytes`, `skipped`, `dirs`, `run_manifest`, `finished_at` all falsified | **rc 0, file restored**, no warning; restore still prints `"completion_marker": "verified"` | **ACCEPTED → NIT-1** |
| A10 | dry run | `completion_marker: none`, `runs/` never created | NO MARKER |
| A11 | `write_once_bytes` over an existing marker | `FileExistsError`, bytes unchanged | IMMUTABLE |
| A12 | crash between the two writes | rc 3, `COMPLETE.json absent` | REFUSED |
| A13 | torn `COMPLETE.json` | rc 3, `completion marker unreadable`; **the tool's own writer cannot repair it** (`FileExistsError`) while the run's data is still on disk | REFUSED (see NIT-2) |
| A14 | store id literally `COMPLETE.json` | backup **rc 3**, `runs/` not created, `manifest.jsonl` not created, `error: invalid backup config: store id 'COMPLETE.json' is reserved …` | REFUSED before any write |

**A9 analysis (the one acceptance).** `verify_completion_evidence` validates `schema`, `run_id`,
`run_manifest_sha256`, and `files`; it checks `readback` on the **per-run manifest's file records**
(`restore.py:110`), never the marker's own `readback` field (`backup.py:275`). `bytes`, `skipped`, `dirs`,
`run_manifest`, `started_at`, `finished_at` are never read. This is **not** a fail-open for data integrity —
what a run is allowed to restore is decided by the digest-bound per-run manifest, the global `run_end`, and a
per-file SHA-256 check before every write, none of which A9 touches. It is a marker-honesty gap: the marker is
not self-authenticated, so it can carry false operational numbers while restore labels it `verified`. Graded NIT-1.

### Arm (c) — the ORIGINAL defect, reproduced on the pre-fix modules

`C:/tmp/OPUS_P026_SCRATCH/opus_prefix_arm.py` against `git show fcac0ac6:…/backup.py` and `…/restore.py`:

```
run 1 (clean) rc=0
run 2 (interrupted) rc=1  run_end={"run_id": "opsa-20260917T100936.924Z", "status": "partial", "files": 1, "errors": 1, …}
greatest run id (what --latest picks): opsa-20260917T100936.924Z  == run 2: True

--- restore --latest (run_id=None) on the PRE-FIX tool ---
{"mode": "restore", "run_id": "opsa-20260917T100936.924Z", …, "records_selected": 1, "manifest_malformed_lines": 0}
RESTORED ledger_store/ledger.jsonl sha256=23b78293d521dee3…
{"mode": "restore", …, "status": "ok", "verified_against_manifest": 1, "restored": 1, "errors": 0, …}
rc=0
files written into the restore target: ['ledger_store/ledger.jsonl']

PRE-FIX --latest selected the interrupted run:  True
PRE-FIX reported success (rc 0) for it:         True
PRE-FIX restored a SHORT store (1 of 2 files):  True
```

That is packet §3 verbatim — "`restore.py --latest` selects the greatest *started* run, not a verified complete
run … could therefore ship a partial run as if complete". The pre-fix tool rebuilt an evidence store that was
**missing a file** and called it `status: ok`. The same tool also accepts the partial run by explicit id
(rc 0), which is why removing `--latest` alone would not have been enough — the completion gate is the fix.

---

## 3. D026 evidence — RED on the pre-fix behaviour

My own arm, independent of the Lead's: the **candidate's** `test_opsa.py` (39 tests) + the candidate's
`opsa_common.py` (so the module imports) + the **pre-fix** `backup.py` and `restore.py` from `fcac0ac6`,
staged at `C:/tmp/OPUS_P026_SCRATCH/red_mix`:

```
$ python -B -m unittest test_opsa -v
Ran 39 tests in 1.314s
FAILED (failures=8, errors=5)
```

39 tests **ran**, so the module imported cleanly — no import error is masking a fence.

| new refusal | test | RED on pre-fix? | GREEN now |
|---|---|---|---|
| interrupted run has no marker; restore refuses | `test_interrupted_run_has_no_completion_marker_and_restore_refuses` | **FAIL** ×3 sub-arms (`AssertionError: 0 != 3`, `True is not false`) | ok |
| restore without an explicit run id | `test_restore_without_explicit_run_id_fails_closed` | **FAIL** (`0 != 3`) | ok |
| completed run restores by explicit id, incl. copied root | `test_completed_run_restores_by_explicit_id_including_copied_run_directory` | **ERROR** `FileNotFoundError` — the marker it copies does not exist on the pre-fix tool | ok |
| tampered marker / per-run manifest | `test_tampered_marker_or_run_manifest_is_refused` | **ERROR** `FileNotFoundError` — nothing to tamper | ok |
| partial manifest cannot yield zero-record success | `test_partial_run_declaring_files_but_having_no_records_fails_closed` | **ERROR** ×3 `JSONDecodeError` — no marker to read | ok |
| **hand-made evidence for an un-closed run (F-01)** | `test_hand_made_completion_evidence_cannot_revive_a_run_the_tool_did_not_close` | **FAIL** ×3 (`0 != 3`, `True is not false`) — the pre-fix restore **verified and restored** the un-closed run | ok |
| roundtrip now asserts the evidence exists | `test_roundtrip_byte_identical` | **FAIL** (`False is not true`) | ok |
| reserved store ids | `test_backup_rejects_store_ids_reserved_for_completion_evidence_without_writes` | RED on the slice-1 `opsa_common` — Lead's `LEAD_RED_ARM_old_common_reserved_ids.txt`: `AssertionError: 1 != 3` ×2 subtests; I re-confirmed the GREEN behaviour myself (arm A14) | ok |
| adapter carries the run's own evidence | `test_isolated_restore_carries_the_runs_own_completion_evidence` | **ERROR** on the slice-1 adapter: `AttributeError: module 'p030_closed_partition_backup_adapter' has no attribute 'COMPLETE_MARKER_NAME'` (my own run) | ok |

**The brief's item-3 question — are the 4 errors in the Lead's RED run real arms or masked fences?** Real arms.
In the Lead's record (`LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt`, 37 tests, `failures=5, errors=4`) the four
ERRORs are named per test (`test_completed_run_restores…`, `test_partial_run_declaring_files…` ×2,
`test_tampered_marker…`) and 37 tests still ran — a module-level import failure would have produced one error
and zero tests. My own 39-test run reproduces the same shapes with the same causes (`FileNotFoundError` /
`JSONDecodeError` on evidence files the pre-fix tool never writes). The count differs (5+4 at slice 1 vs 8+5 at
slice 3) only because slice 3 added the F-01 fence and reworked the partial-manifest test; both are consistent.

---

## 4. Contract-change blast radius

Consumer sweep of the whole worktree (read-only `Grep` for `run_restore`, `select_run`, `import restore`,
`restore.py`, `"runs"`, `runs/<`):

| consumer | kind | effect of the stricter contract |
|---|---|---|
| `p030_closed_partition_backup_adapter.py:716,746` | **code** — the only non-test caller of `restore.run_restore` anywhere | Was the blocker; fixed in slice 2/3, verified below |
| `check_p030_closed_partition_backup_adapter.py` | test for the above | Updated in-scope; 45 OK |
| `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | the package's own suite | 39 OK |
| `p030_opsa_heartbeat_adapter.py` / its checker | imports `opsa_common` only, never `restore` | unaffected; checker exit 0 |
| `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md:120,152,477` | **document** — the D026 restore-drill procedure | **left behind** — see NIT-4 |
| `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/LANE_REPORT.md:39` | document | describes "`--latest`/`--run` selection" — stale prose |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/docs/backup_restore_runbook.md` | document | **not** a consumer — it documents `02_MTC_BACKTEST/scripts/backup_restore.py`, an unrelated tool |
| `IBKR_PAPER_BRIDGE/**`, `_deepseek_driver/**` | code | their `runs` are database tables / other directories; no OPS-A coupling |

**No other code consumer exists on master.** `select_run` and `load_complete_marker` have no callers outside
`restore.py` and the suite.

### Is the slice-2/3 adapter resolution technically sound?

`_isolated_restore_inputs` (`p030_closed_partition_backup_adapter.py:566-596`) now reads
`runs/<run_id>/COMPLETE.json` and `RUN_MANIFEST.jsonl` with `read_bytes()`, raising
`ValueError("P026 completion evidence is unavailable")` on `OSError`, and writes the **same bytes** into the
isolated `runs/<run_id>/`. Judgement on each of the brief's three questions:

1. **Could the adapter path ever restore a run the bare `restore.py --run` would refuse?** No. The adapter's
   isolated root carries (a) the run's marker bytes, (b) the run's per-run manifest bytes, (c) a *validated
   snapshot* of the global manifest (`_restore_manifest_snapshot`, re-verified against the real file both
   before and after the restore at `:723-736,753-758`). Every input to `verify_completion_evidence` is
   therefore byte-identical to what the bare tool would read, so the verdict is identical. The only possible
   divergence is in the strict direction: if the snapshot were ever a *subset*, `per_run_files != global_files`
   would refuse. It cannot be more permissive, because none of the three inputs is synthesised.
2. **Does the copied evidence keep its digest binding?** Yes, and it is fenced, not assumed:
   `test_isolated_restore_carries_the_runs_own_completion_evidence` (`check_…:1194-1261`) asserts
   `seen["marker"] == original_marker` and `seen["manifest"] == original_run_manifest` **as bytes**, observed
   from inside the patched `run_restore` call, plus `isolated_root.samefile(root/"backups")` is False — so the
   isolation the adapter exists for is still real. It then tampers the marker two ways (broken
   `run_manifest_sha256`; a foreign `run_id`) and requires the adapter path to refuse with
   `P026 check-only failed; restore withheld` and an **empty** target. A byte copy preserves a SHA-256 binding
   trivially; the test proves it *is* a byte copy.
3. **Does the mutant test still detect the isolation mutant for the right reason?**
   `test_shared_archive_reversion_mutant_is_detected` (`check_…:1153-1192`) replaces
   `isolated_config = {**config, "backup_root": str(isolated_root)}` with `isolated_config = config`. Under the
   new gate the mutant is caught earlier than before, so the test accepts a third message —
   **but only conditionally**: `if str(refused.exception) == "P026 restore failed"` it *requires*
   `"per-run manifest file records differ from the global manifest"` in the captured stderr. A generic restore
   failure will not pass it. The detection is still causally tied to the mutation: with isolation removed the
   restore reads the *shared* archive, which the parent test mutates after validation, and the per-run/global
   disagreement is exactly the footprint of that shared read. Right reason.

The reserved-store-id guard (`opsa_common.py:321-323`) is a genuine companion defect the Lead found while
writing the adapter fix: a store named `COMPLETE.json` would have written store files at the marker's own path
inside `runs/<run_id>/`. Arm A14 confirms it is refused at config load, before `runs/` or `manifest.jsonl` exist.

---

## 5. Scope and protected paths

- `git diff fcac0ac6 e114ed31 --stat` = **exactly 7 files**: five under `tools/opsa/` (`backup.py`,
  `restore.py`, `opsa_common.py`, `test_opsa.py`, `README.md`) plus the two repo-root adapter files.
- `git diff fcac0ac6 d81b07f6 --stat` = the **6-file code scope**; `git diff d81b07f6 e114ed31 --stat` = README
  alone (+5/−3). The docs-only claim holds at byte level.
- `--summary` is empty → **no file added, deleted or renamed**. Packet §2's "0 ADD" is kept.
- Nothing under `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, `MTC_V2` — the 7-file diff is over the whole tree.
- `watchdog.py` and `heartbeat.py` hashes equal the recorded base hashes; heartbeat emission unchanged.
- Global `manifest.jsonl` record shapes unchanged (no `+`/`-` line touches a `run_start`/`run_end` record; the
  `file`/`dir`/`skipped` dicts are byte-identical, merely bound to a name before `append_jsonl`).
- `backup.py` CLI unchanged (no `add_argument` diff).

**Authority ledger** — three owner decisions, verified in `C:/CT13/DECISIONS.md`, not taken from the brief:

| files | authority |
|---|---|
| `backup.py`, `restore.py`, `opsa_common.py`, `test_opsa.py` | packet §2 + `OD-20260915-P026-REPAIR-LEAD-1` ("A", ~08:34Z) |
| `p030_closed_partition_backup_adapter.py`, `check_p030_closed_partition_backup_adapter.py` | `OD-20260915-P026-ADAPTER-LEAD-1` ("A", ~10:50Z) |
| `README.md` | `OD-20260915-P026-README-A-1` (exact words `B A`, ~18:25Z) |

The README needed its own row: packet **§6 explicitly excludes** "`config.example.json` and `README.md`
updates" from this decision. With `OD-20260915-P026-README-A-1` it is authorised; without it the commit would
have been a ceiling breach. The decision row's own description (`+5/−3`, no code or test bytes) matches the
diff I ran. No scope finding.

---

## 6. Lead authorship

It does not change my verdict, and here is why that is a measurement rather than a courtesy: every claim in
this report is anchored to bytes I hashed or commands I ran, and the two pieces of evidence that carry the most
weight — the original defect (arm c) and the F-01 fail-open (arm A5) — were reproduced with code I wrote, not
with the author's tests. Where I re-ran the author's own arms they reproduced exactly (§7).

What authorship *does* change is how much the fixture suite can be credited on its own. The suite was written
by the author of the code, and the one REQUIRED defect in this package's history (Gemini F-01: a hand-made,
digest-bound pair reviving a run the tool never closed) was **not** caught by it — it was caught by an outside
detection pass, and it was a real fail-open, not a style point. My A5 arm now confirms the fix, and my A9 arm
found the one remaining unvalidated surface, which the author's suite also does not cover. That pattern —
author-written fences miss the shapes the author did not imagine — is the argument for keeping **exact Sol**
in the roster rather than accepting on my report plus Gemini's. Nothing beyond that roster is needed.

---

## 7. Report honesty — `LEAD_VERIFICATION_P026_REPAIR.md` vs the bytes

| claim (record line) | my check | result |
|---|---|---|
| slice 3: `Ran 39 tests … OK` (l.82) | ran it | **reproduced** — `Ran 39 tests in 2.057s … OK` |
| slice 3: adapter checker `Ran 45 tests … OK`, exit 0 (l.83) | ran it | **reproduced** (ASCII `TEMP`; NIT-3) |
| heartbeat checker exit 0 (l.84) | ran it | **reproduced** — `Ran 10 tests … OK` |
| Ruff `All checks passed!` (l.85) | ran ruff 0.16.4 | **reproduced**, exit 0, on `tools/opsa` **and** the two adapter files |
| slice 1: `Ran 37 tests … OK` (l.18) | read `LEAD_UNITTEST_312.txt` | matches the artifact (it is the slice-1 file, not a stale claim about the candidate) |
| slice 1 RED: `FAILED (failures=5, errors=4)` (l.19) | read the artifact + ran my own equivalent | artifact matches; my 39-test equivalent gives `failures=8, errors=5`, consistent with the two fences added after slice 1 |
| slice 2 RED (a): new checker vs the `6ac9cfb7` adapter = `Ran 45 tests, FAILED (failures=6, errors=3)` (l.59) | **re-ran it myself** on a clean staging of `git show 6ac9cfb7:…adapter.py` | **reproduced exactly**: `Ran 45 tests in 3.595s`, `FAILED (failures=6, errors=3)` = the brief's "9 of 45" |
| slice 2 RED (b): reserved-id `AssertionError: 1 != 3` per subtest (l.60) | read the artifact | matches |
| slice 3 RED: `Ran 39 tests, FAILED (failures=3, errors=1)` (l.87) | read the artifact | matches (`LEAD_RED_ARM_slice2_restore_backup_new_tests.txt`) |
| slice 1 checker vs slice 1 adapter `Ran 44 … failures=7, errors=2`; base `Ran 44 … OK` (l.24) | read both artifacts | match |
| slice 2 `Ran 38 … OK`, slice 2/3 checker `45 … OK` (l.53,54,83) | read the artifacts | match |
| recorded hashes `SHA256SUMS_d81b07f6_slice3.txt` | hashed the files myself | **all five match** |
| repo guard `RESULT: PASS`, `[protected] none` (l.22,58,86 + `LEAD_GUARD_readme.txt`) | read the artifacts | consistent; the README run shows the single `M README.md` entry |
| interpreter statements (3.12.12, pinned venv) | ran `sys.version` | correct |

**Two corrections, neither the Lead's fault:**

1. The **review brief** (§Subject, line 14) says "Ruff 0.16.4 is in the same venv". It is not — the pinned venv
   has no `ruff` module and no `Scripts/ruff.exe`. The Lead's own record names the real location
   (`C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe`, `ruff 0.16.4`), which I used. The record is right; the
   brief is wrong. Not a code issue.
2. The brief's "expect 45 OK, exit 0" for the closed-partition checker is **environment-dependent** — see NIT-3.
   My first run of the mandated command failed 1 of 45. I did not accept that at face value in either
   direction: I isolated the cause, and proved it reproduces identically on the untouched base tree.

No claim in `LEAD_VERIFICATION_P026_REPAIR.md` was overstated against the bytes. The record's self-correction at
09:59Z ("it is 13 refusals / 9 failing tests") is itself accurate.

---

## 8. Author-disclosed residual (README) — graded

**Closed, no finding.** The brief's item 8 describes `README.md:61,63` still showing `restore.py … --latest`.
That residual was fixed by `e114ed31`, which is the commit under review. Verified at byte level:

```
$ grep -n 'latest|RUN_MANIFEST|COMPLETE|--run' MTC_COMMAND_CENTER/tools/opsa/README.md
60: # 4. Isolated integrity proof (no writes). A restore names ONE explicit run id (there is no --latest:
61: #    the newest run may be the interrupted one); the run must carry runs/<run_id>/COMPLETE.json +
62: #    RUN_MANIFEST.jsonl written by backup.py, or restore.py refuses it (rc 3, run_not_complete):
63: python restore.py --config opsa_config.json --run opsa-20260101T000000.000Z --check-only
65: python restore.py --config opsa_config.json --run opsa-20260101T000000.000Z --to D:/recovered
```

Both usage lines now name an explicit `--run`, the marker pair is named, and the only surviving occurrence of
the string `--latest` is the sentence explaining that the flag no longer exists. Accurate against the code.

**The document the stricter contract still leaves behind** (the brief invited me to name any other): NIT-4.

---

## Findings

### NIT-1 — `COMPLETE.json` is not self-authenticated; restore labels it `verified` anyway
`MTC_COMMAND_CENTER/tools/opsa/restore.py:71-112` (gate) and `:200` (the `"completion_marker": "verified"`
label); marker payload written at `MTC_COMMAND_CENTER/tools/opsa/backup.py:268-276`.

Only `schema`, `run_id`, `run_manifest_sha256` and `files` are validated. `readback`, `bytes`, `skipped`,
`dirs`, `run_manifest`, `started_at` and `finished_at` are never read. Arm A9 falsified all six of the first
group at once — including flipping `readback` from `all_match` to `MISMATCH` — and the restore completed
**rc 0**, wrote the file, and printed `"completion_marker": "verified"`.

Not a data-integrity fail-open: the restore decision rests on the digest-bound per-run manifest, the global
`run_end`, and a per-file SHA-256 check before every write, none of which A9 can touch. The harm is that an
operator reading `COMPLETE.json` during a real recovery — the document this package exists to produce — may be
reading numbers the tool never checked, under a line that says `verified`. Two cheap remedies, either suffices:
assert `marker["readback"] == "all_match"` and `marker["run_manifest"] == RUN_MANIFEST_NAME` (two lines beside
the existing `files` check at `restore.py:103-107`), or narrow the label to `"pair_verified"` so it claims only
what was checked. The same applies to the per-run manifest's `dir`/`skipped` records, which are digest-bound but
never compared to the global manifest (only `file` records are, `restore.py:99-102`) — harmless today because
restore replays the *global* records, worth one comment.

### NIT-2 — "atomically" is O_EXCL, not atomic publication; a torn marker permanently strands a good run
`MTC_COMMAND_CENTER/tools/opsa/opsa_common.py:153-165` (`write_once_bytes`), used at `backup.py:260,278`.
Packet §4: "written atomically".

The safety property is obtained (arms A12/A13, §1) — no partial marker can be mistaken for a complete one. The
residue is the opposite failure: arm A13 shows a half-written `COMPLETE.json` leaves a run whose **data is
intact on disk** but which `restore.py` will refuse forever, and which the tool's own writer cannot repair —
`write_once_bytes` raises `FileExistsError` by design, and the package has no delete primitive
(`NoDeleteGuaranteeTests`), so nothing in OPS-A can clear the torn file. Recovery would require manual
intervention on the backup store, exactly when an operator is already mid-incident.

I am **not** recommending a blind change: the obvious tmp-plus-rename fix is genuinely constrained here, because
the POSIX form needs an `unlink` of the temp file and that would collide with the no-delete guarantee, while
`os.replace` would destroy the immutability `O_EXCL` buys. The right call is the owner's: either accept the
residue and **document it** (one line in the README's restore section: a run with an unreadable marker must be
re-backed-up under a new run id, its data is not lost), or take a separately-scoped change that writes
`COMPLETE.json.tmp` + fsync + `Path.rename` onto a non-existent target (atomic on Windows, fails if the target
exists, adds no delete call). Either way the clause's *purpose* is met today.

### NIT-3 — the P0-30 checker's config anchor is ASCII-only; the adapter writes UTF-8 (pre-existing on master)
`check_p030_closed_partition_backup_adapter.py:837` builds
`anchor = f'  "backup_root": {json.dumps(configured_root)},'` with the default `ensure_ascii=True`, while
`p030_closed_partition_backup_adapter.py:607` writes the isolated config with `ensure_ascii=False`. When the
temp path contains a non-ASCII character the anchor never matches and
`test_isolated_config_redirect_after_check_never_reaches_restore` fails on `assertEqual(raw.count(anchor), 1)`
→ `AssertionError: 0 != 1`.

This is the first result I got from the mandated command, and it is worth being precise about attribution:

```
TEMP=C:\Users\BarışSemaay\AppData\Local\Temp\opus_p026   (contains U+0131)
  candidate tree : Ran 45 tests ... FAILED (failures=1)   exit 1
  BASE tree      : Ran 44 tests ... FAILED (failures=1)   exit 1   <-- same test, same assertion
TEMP=C:\tmp\OPUS_P026_SCRATCH\ascii_tmp                  (ASCII)
  candidate tree : Ran 45 tests ... OK                    exit 0
```

The base tree is `git show fcac0ac6:` for both the adapter and the checker with the base `tools/opsa` — nothing
from this candidate. **Inherited from master, not introduced, not regressed.** The Lead's records show
`C:\Users\BARSEM~1\AppData\Local\Temp\…` — the 8.3 short name, which is pure ASCII — which is why the Lead's run
was green and honest. Named here because the candidate legitimately modifies this file and the one-line fix
(`json.dumps(configured_root, ensure_ascii=False)`, matching the writer) belongs with it; and because any future
reviewer running the mandated command on a profile with a non-ASCII name will see a red gate for a
non-existent defect.

### NIT-4 — the D026 restore-drill document still instructs `--latest`; its commands no longer run
`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md:120,152,477`
(and stale prose at `.../LANE_REPORT.md:39`).

This is the package's restore-drill evidence, and it does not present itself as history only — its scope fence
says "the drill is reproducible from the commands below" (`:10`). Under this candidate those commands exit 2
(argparse: `--latest` is gone), and the 2026-08-24 run they name has no `COMPLETE.json`, so even the rewritten
form would be refused. Failure is **safe** (rc 2/rc 3, nothing restored, no data risk), which is why this is a
NIT and not a blocker.

It should not be fixed by rewriting the recorded output — that would be falsifying past evidence. The correct
repair is a dated note at the top of Part A: the restore contract changed on this branch, `--latest` was
removed, a reproduction must name an explicit `--run <id>` of a run backed up by the current tool, and the
recorded transcript below is the pre-change tool. Owner's call whether that rides in the merge PR (it is
outside every authority row cited above).

### NIT-5 — dead condition
`MTC_COMMAND_CENTER/tools/opsa/backup.py:237`: `return RC_OK if not errors and status == "ok" else RC_ERROR`.
`status` is assigned `"ok" if not errors else "partial"` at `:227`, so `and status == "ok"` can never change the
result. Harmless; delete it or keep it as documentation of intent.

**REQUIRED findings: none.**

---

## NOT VERIFIED

1. **Real-world crash atomicity.** Arms A12/A13 *simulate* the crash window by removing/truncating the marker
   after a clean run. I did not kill a live `backup.py` process mid-`write_once_bytes`, and I did not test on a
   filesystem other than local NTFS. The fsync-then-visible ordering is asserted from the code, not measured.
2. **Concurrency.** Two `backup.py` runs against one backup root at the same time, and a restore racing a
   backup, were not exercised. Run ids are millisecond timestamps, so a collision is unlikely but not excluded
   by any lock I found; `append_jsonl` ordering under concurrent appends is untested.
3. **The `_restore_manifest_snapshot` internals** of the P0-30 adapter were read, not independently re-derived;
   my claim that the isolated global manifest can only be equal-or-stricter rests on reading `:619-623` and
   `:723-736` plus the byte-equality fence, not on a mutation arm of my own against that function.
4. **Scale.** Every arm used a 2-file fixture store. Behaviour with thousands of files (the per-run manifest is
   built entirely in memory at `backup.py:255-258` before a single byte is written) is untested — a very large
   run holds every record in RAM before the evidence exists.
5. **Gemini's delta review** of `8d4056c5..d81b07f6` exists under the records directory; I did not read it
   before forming my findings, by design, and have not reconciled my NITs against it.
6. **The watchdog half** (`53d33dbc`) was not reviewed here beyond confirming `watchdog.py` is byte-unchanged
   and its three tests pass.
7. **`git diff --check`** (whitespace) is claimed in the Lead's record; I did not run it, as the brief permits
   only the one `diff` form I used.
8. **Non-ASCII store ids and paths** inside the backup fixtures (as opposed to the temp root) were not tested,
   though NIT-3 shows the area is live.

---

VERDICT: PASS-WITH-NITS
