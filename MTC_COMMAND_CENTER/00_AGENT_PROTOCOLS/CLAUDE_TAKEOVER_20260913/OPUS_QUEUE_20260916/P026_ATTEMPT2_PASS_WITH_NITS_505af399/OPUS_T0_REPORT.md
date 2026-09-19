# T0 review report — WP-P0-26 OPS-A completion-marker repair, candidate `505af399` (SECOND exact-Opus read: the NIT slice)

Reviewer: exact `claude-opus-5`, effort xhigh. One session, no delegation, no subagents, no other session resumed.
Brief: `C:/tmp/OPUS_QUEUE_20260916/P026/opus/BRIEF.md` + `C:/tmp/OPUS_QUEUE_20260916/P026/REVIEW_BRIEF.md` incl. the ADDENDUM 2026-09-18.
Run: 2026-09-19, 08:57–09:3x UTC+3. All commands below were executed by me in this session; every output quoted is the observed output, not a paraphrase.

**Result: PASS-WITH-NITS — 0 REQUIRED, 5 NITs.** This report accepts nothing.

---

## 1. Verified identities (COMPUTED)

### HEAD

```
> git -c safe.directory=* -C C:/tmp/P026_REPAIR_20260915 rev-parse HEAD
505af399db1152910661b40e7e20fa517852e05d
```

Matches the pin in the BRIEF and the REVIEW_BRIEF addendum. No BLOCK on this ground.

Branch history (read-only `git log`, no working-tree git command was run; no `status`/`add`/`commit`/`checkout` at any point):

| SHA | Date (UTC+3) | Author | Subject |
|---|---|---|---|
| `505af399` | 2026-09-18 11:51:38 | Claude Opus 5 | NIT slice (this read's subject) |
| `e114ed31` | 2026-09-15 21:39:22 | Codex GPT-5 | README-only (owner item 7 "A") |
| `d81b07f6` | 2026-09-15 14:29:33 | Claude Opus 5 Lead | slice 3 (Gemini F-01/F-02/F-03) |
| `8d4056c5` | 2026-09-15 13:59:53 | Claude Opus 5 Lead | slice 2 (adapter + reserved store ids) |
| `6ac9cfb7` | 2026-09-15 11:46:33 | Claude Opus 5 Lead | slice 1 (completion evidence + explicit-run restore) |
| `fcac0ac6` | 2026-09-13 11:10:49 | bsemaay-tech | base (`origin/master`, PR #191) |

### sha256 of the subject files

Blob bytes (canonical — `git show <rev>:<path>` piped to sha256, so no CRLF-checkout ambiguity), plus the worktree checkout digest for the record:

| File | sha256 (blob @ `505af399`) | bytes | sha256 (worktree checkout) |
|---|---|---|---|
| `MTC_COMMAND_CENTER/tools/opsa/backup.py` | `625fc2fde9a2153fd73ef322003ac3dfbaa194f0dd4203bbbfaf73bd414da11e` | 14048 | `01e732150efba155e4ea7a481c97cca340ed8f6801086bf0a3dd0bc647aa01f2` |
| `MTC_COMMAND_CENTER/tools/opsa/restore.py` | `26af8a5e79ca44e72c35b822cddefd555acef07453741091b922916b16fdc8af` | 17529 | `beb8e79063d21adb0429f5d0e58111058887abe6f3b18d5d9b5355c476aa43f6` |
| `MTC_COMMAND_CENTER/tools/opsa/opsa_common.py` | `e2b3d386abdb42852fe005be9ac451bf7f89770d5892ec056c1738f0fd8063e1` | 14568 | `e2b3d386abdb42852fe005be9ac451bf7f89770d5892ec056c1738f0fd8063e1` |
| `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | `78ed10e76117d6e857503c9550755819054a374d856a12603639ad2aa49ac493` | 45873 | `c125d536ab0850bbd7b0f50532e8975c3ec8a4eeb4f7782f000586bebd2c8988` |
| `MTC_COMMAND_CENTER/tools/opsa/README.md` | `3627e07b817e305efb81346fa35eb370900e073c788f62b885bad47cc0220d2a` | 6785 | `82113f8a8e9bb630594e59111be7d56b1a793e0d9198f0320f4fcd7a8e6b0744` |
| `MTC_COMMAND_CENTER/tools/opsa/watchdog.py` | `0b5130c967a6ad9a5a31bd5bc186ff1c1888fbc3d63439930c2e5245a6defb68` | 14404 | `0d4ba79dc4cedc32128a13943332f7574aa3a459cacaf399b81ee4dbe785376a` |
| `MTC_COMMAND_CENTER/tools/opsa/heartbeat.py` | `3970bde53eed012fa146f809d1ee775a2a6c2972d1d5b8c42d11fe74759f1ea0` | 4331 | `38b43d72548de0496be40502b98b9ff8e7c019706d467da2a6c109d13ac507e6` |
| `p030_closed_partition_backup_adapter.py` | (unchanged since `d81b07f6`) | 32173 (wt) | `60a0e7af31d884ebfa349313cf0795422cb2622ef7325e729389e1b40d51bcd9` |
| `check_p030_closed_partition_backup_adapter.py` | (unchanged since `d81b07f6`) | 84736 (wt) | `ef777b3f46aa92b3eb84abe41b87d4d5d36fcbf7499514a5eb4df2fc90324d2a` |
| `…/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md` | — | 46780 (wt) | `65baee7d39b9416b46eb14d4070e1c62df381bfa449bb7604ceb3d5afd87bfec` |

**`watchdog.py` and `heartbeat.py` blob digests at `505af399` are byte-identical to `fcac0ac6`** — proof (not assertion) that the watchdog half is untouched by this branch.

### Interpreter and tools

```
> C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe -B -c "import sys; print(sys.version)"
3.12.12 (main, Jan 27 2026, 23:45:36) [MSC v.1944 64 bit (AMD64)]
```

`PYTHONDONTWRITEBYTECODE=1` and `-B` on every invocation; `TEMP`/`TMP` set to the ASCII path `C:\tmp\OPUS_P026_SCRATCH\read2_tmp` as the addendum requires.

**Correction to the REVIEW_BRIEF (§Subject, line 14):** ruff is **not** in the pinned venv —
`python -m ruff` → `No module named ruff`, and `…/.venv/Scripts/` contains no `ruff.exe`.
Ruff 0.16.4 lives at `C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe`, which is exactly what
`LEAD_VERIFICATION_P026_REPAIR.md:50` states. The Lead record is right; the brief line is wrong.
Not a finding against the candidate.

---

## 2. Scope of the NIT slice

```
> git -c safe.directory=* -C C:/tmp/P026_REPAIR_20260915 diff e114ed31 505af399 --stat
 .../WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md |  9 +++++++++
 MTC_COMMAND_CENTER/tools/opsa/README.md                |  6 +++++-
 MTC_COMMAND_CENTER/tools/opsa/backup.py                |  2 +-
 MTC_COMMAND_CENTER/tools/opsa/restore.py               | 18 +++++++++++++++---
 MTC_COMMAND_CENTER/tools/opsa/test_opsa.py             | 17 ++++++++++++++-
 5 files changed, 46 insertions(+), 6 deletions(-)

> git … diff e114ed31 505af399 --name-status     → all five lines start with "M"  (0 added)
> git … diff e114ed31 505af399 --check           → clean (rc 0)
> git … diff d81b07f6 e114ed31 --stat            → MTC_COMMAND_CENTER/tools/opsa/README.md | 8 +++++---   (README alone ✔)
> git … diff fcac0ac6 505af399 --name-status     → 8 files, every one "M", 0 added
```

Exactly five files, `+46/−6`, as the addendum declares. Nothing under `02_MTC_BACKTEST`,
`07_ADAPTERS`, `01_PINE`, `MTC_V2`. Whole-branch scope vs `fcac0ac6` is eight files: the four
`tools/opsa/` code+test files, `tools/opsa/README.md`, the two repo-root P0-30 files named by
`OD-20260915-P026-ADAPTER-LEAD-1`, and `11_TRIAGE/…/RESTORE_DRILL_EVIDENCE.md` (see NIT-4 on that
last one's authority).

Ruff parity, measured by me on both revisions (`ruff check --no-cache --isolated --statistics`):

| File | findings @ `e114ed31` | findings @ `505af399` |
|---|---|---|
| `restore.py` | 2 | 2 |
| `backup.py` | 4 | 4 |
| `test_opsa.py` | 7 | 7 |

and the mandated selection is clean at HEAD:

```
> cd C:/tmp/P026_REPAIR_20260915
> ruff check --no-cache --select E9,F821,F811,F401,F841 MTC_COMMAND_CENTER/tools/opsa
All checks passed!     (exit 0)
```

---

## 3. Mandated commands — executed

| Command | cwd | Observed | Expected by the brief |
|---|---|---|---|
| `python -B -m unittest test_opsa -v` | `…/P026_REPAIR_20260915/MTC_COMMAND_CENTER/tools/opsa` | `Ran 39 tests in 1.794s` / `OK`, exit 0 | 39 OK ✔ |
| `python -B check_p030_opsa_heartbeat_adapter.py` | `…/P026_REPAIR_20260915` | `Ran 10 tests in 0.089s` / `OK`, exit 0 | exit 0 ✔ |
| `python -B check_p030_closed_partition_backup_adapter.py` | `…/P026_REPAIR_20260915` | `Ran 45 tests in 4.602s` / `OK`, exit 0 | 45 OK, exit 0 ✔ |

Raw logs: `C:/tmp/OPUS_P026_SCRATCH/read2_unittest.txt`, `read2_hb_adapter.txt`, `read2_cp_adapter.txt`.

---

## 4. Packet §4 conformance, clause by clause

Authority read in full: `C:/tmp/P026_LOCAL_SCOPE_DECISION_20260907.md` (rev 2).

| Packet §4 clause (quoted) | Code | Verdict |
|---|---|---|
| "Each successful backup run emits a per-run immutable `RUN_MANIFEST.jsonl` (file list, sizes, hashes) plus `COMPLETE.json`" | `backup.py:240-283` (`write_completion_evidence`); records carry `rel`/`size`/`sha256`/`readback` (`:202-207`) | **IMPLEMENTED-AS-WRITTEN** |
| "…written **atomically** and only after every readback hash passes" | `opsa_common.write_once_bytes:153-165` = `open(path,"xb")` + `write` + `flush` + `os.fsync`; no tmp, no rename. Gate on `if not errors:` at `backup.py:220`, and `write_completion_evidence:251-252` refuses again if `errors` | **IMPLEMENTED — letter differs, guarantee obtained.** See §4.1 below |
| "A partial/interrupted run has no completion marker." | `backup.py:215-226`; verified ARM-1, ARM-4, ARM-12 | **IMPLEMENTED-AS-WRITTEN** |
| "Once written, manifest and marker are never rewritten." | `O_EXCL` in `write_once_bytes`; `FileExistsError` propagates (`backup.py:261-262, 279-280`); asserted at `test_opsa.py:330-334` | **IMPLEMENTED-AS-WRITTEN** |
| "Restore consumes an explicit completed run ID and fails closed: no run without a matching `COMPLETE.json` + `RUN_MANIFEST.jsonl`" | `restore.py:158-164` (no id → rc 3), `:197-206` (the single gate, before any hash read or write), `verify_completion_evidence:72-124` | **IMPLEMENTED-AS-WRITTEN** |
| "…no execution on hash mismatch" | `restore.py:253-258` (pre-restore) and `:277-282` (post-write); rc 1; arm (e) of `test_opsa.py:396-404` | **IMPLEMENTED-AS-WRITTEN** |
| "`--latest` (greatest-started-run selection) is removed; restore without an explicit run ID errors." | `--latest` gone from argparse (`restore.py:300-312`, `--run required=True`); `select_run(None)` raises `ValueError` (`:59-60`); `run_restore(run_id=None)` → rc 3 (`:158-161`). CLI observed rc 2 for both `--latest` and a missing `--run` (ARM-13) | **IMPLEMENTED-AS-WRITTEN** |
| "Additive only: every existing interface not named above stays as-is." | `backup.py` CLI identical to `fcac0ac6` (`--config/--dry-run/--store`); the five global-manifest record literals (`run_start`/`skipped`/`dir`/`file`/`run_end`) are field-for-field identical to `fcac0ac6:backup.py:105,135,142,184,197`; `watchdog.py`/`heartbeat.py` blobs byte-identical to base | **IMPLEMENTED-AS-WRITTEN** |

### 4.1 "Atomically" vs `write_once_bytes` — does the guarantee obtain?

The clause's purpose is that **no partial marker can be mistaken for a complete one**. It does.

* **Exclusive create.** `open(path,"xb")` cannot silently overwrite an existing marker, so a
  second run can never re-publish evidence for a run id that already has it. A tmp+rename
  publication would give atomicity but would need a cleanup path on failure — a delete path,
  which the package's first invariant forbids (`opsa_common.py:5-12`). The trade is deliberate
  and, for this package, correct.
* **A torn marker cannot read as complete.** `write_once_json` emits one JSON object with
  `sort_keys=True, indent=2`; the closing `}` is the last byte, so every strict prefix fails
  `json.loads` → `RunNotComplete("completion marker unreadable")`. I confirmed this empirically
  (ARM-10: a half-truncated marker gives `completion marker unreadable: Unterminated string
  starting at: line 8 column 13 (char 209)`, rc 3). A marker torn at a byte boundary that
  happened to yield valid JSON would still have to carry the right `schema`, `run_id`,
  `run_manifest_sha256`, and — new in this slice — `readback` and `run_manifest`.
* **Crash between the manifest write and the marker write** (the clause's stated worry) leaves
  `runs/<id>/RUN_MANIFEST.jsonl` and the copied files, and **no** `COMPLETE.json`. Observed
  directly (ARM-12): `backup rc=1 status='partial' completion='failed: cannot write
  COMPLETE.json: …' leftovers=['RUN_MANIFEST.jsonl', 'ledger_store']`, restore rc 3
  `no completion marker (COMPLETE.json absent)`, and the next backup gets a **new** run id and
  completes normally. The stranded run's data is left in place — the package has no delete
  primitive (`NoDeleteGuaranteeTests`, `test_opsa.py:834-860`, scanning all five tool modules
  for ten call-site needles). That is exactly what the NIT-2 README paragraph now documents,
  under `OD-20260918-P026-N2-DOC-1`.

---

## 5. RED / GREEN per refusal — and a branch-kill sweep

### 5.1 The four packet §5 falsifications for this half

| Packet §5 requirement | Test | RED on the pre-fix modules? | GREEN at `505af399`? |
|---|---|---|---|
| 1. interrupted run has no `COMPLETE.json`, refused by restore | `test_interrupted_run_has_no_completion_marker_and_restore_refuses` | **YES** — `AssertionError: 0 != 3` ×2 subtests + `True is not false` | YES |
| 2. completed run restores by explicit id, incl. a copied run dir | `test_completed_run_restores_by_explicit_id_including_copied_run_directory` | **YES** — `FileNotFoundError: …COMPLETE.json` | YES |
| 3. tampered/mismatched marker or manifest refused; hash mismatch refused | `test_tampered_marker_or_run_manifest_is_refused` | **YES** — `json.decoder.JSONDecodeError` (the pre-fix tool prints no structured refusal at all) | YES |
| 4. restore without an explicit run id fails closed; greatest-started-run selection gone | `test_restore_without_explicit_run_id_fails_closed` | **YES** — `AssertionError: 0 != 3` | YES |
| (F-01, slice 3) hand-made evidence cannot revive an unclosed run | `test_hand_made_completion_evidence_cannot_revive_a_run_the_tool_did_not_close` | **YES** on the pre-fix modules AND on the slice-2 modules | YES |
| (NIT-1, this slice) the marker's own claims | new arms (d2) in `test_tampered_marker_or_run_manifest_is_refused` | **YES on `e114ed31`** — see 5.2 arm E | YES |

### 5.2 My RED arms against earlier revisions (cwd = a scratch copy per arm; driver `C:/tmp/OPUS_P026_SCRATCH/read2_red_prefix.py`)

| Arm | Module set | Suite | Observed |
|---|---|---|---|
| A | `fcac0ac6` `backup.py`+`restore.py`, HEAD `opsa_common.py` | HEAD (39) | `FAILED (failures=8, errors=5)` |
| B | `fcac0ac6` all three | HEAD (39) | `Ran 1 test` / `FAILED (errors=1)` — a **collection ImportError** |
| C | `6ac9cfb7` `opsa_common.py`, rest HEAD | HEAD (39) | `FAILED (failures=2)` — only `test_backup_rejects_store_ids_reserved_for_completion_evidence_without_writes` (both subtests) |
| D | `8d4056c5` `backup.py`+`restore.py` | HEAD (39) | `FAILED (failures=4, errors=1)` |
| **E** | **`e114ed31` `backup.py`+`restore.py`** | HEAD (39) | **`FAILED (failures=1)` — exactly `test_tampered_marker_or_run_manifest_is_refused`** |

**Arm E is the decisive D026 evidence for this slice**: the immediately preceding candidate fails
the new arms and nothing else. Arm B shows what an import error looks like, which matters for the
brief's warning — **arm A's five errors are not import errors**. Their terminating exceptions are:

```
FileNotFoundError: …\runs\opsa-…\COMPLETE.json            (the pre-fix tool writes no marker)
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)   ×3
      (the test parses the last stderr line as the structured run_not_complete report;
       the pre-fix restore prints plain text there — the refusal does not exist)
FileNotFoundError: …\runs\opsa-…\RUN_MANIFEST.jsonl
```

and the eight failures are `AssertionError: 0 != 3` (pre-fix restore returns OK where the fence
demands rc 3) / `True is not false` / `False is not true`. Every one fails for the right reason;
**no fence is masked**.

Reconciliation with the Lead's records (brief item 7): `LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE.txt`
records `Ran 37 tests … FAILED (failures=5, errors=4)` — that arm was run against the **slice-1**
suite (37 tests). My arm A uses the 39-test NIT-slice suite, which adds the slice-2/3 and NIT-1
arms, hence 8+5. Likewise `LEAD_RED_ARM_slice2_restore_backup_new_tests.txt` records
`failures=3, errors=1` and my arm D gives `4, 1` — the extra failure is the NIT-1 arm, which did
not exist when the Lead ran it. Both differences are fully accounted for. `LEAD_RED_ARM_old_common_reserved_ids.txt`
(`failures=2`) and `LEAD_RED_ARM_old_adapter_new_checker.txt` (`failures=6, errors=3` = the
brief's "9 of 45") reproduce exactly.

### 5.3 Addendum (a)/(e): the NIT-slice mutants (driver `read2_mutate.py`; cwd = `C:/tmp/OPUS_P026_SCRATCH/read2_opsa`)

| Mutant | Observed |
|---|---|
| baseline (pristine scratch copy) | `Ran 39 tests` / `OK` |
| **(a1)** `if False and marker.get("readback") != "all_match":` | `FAILED (failures=1)` — `test_tampered_marker_or_run_manifest_is_refused` |
| **(a2)** `if False and marker.get("run_manifest") != RUN_MANIFEST_NAME:` | `FAILED (failures=1)` — same test |
| **(a3)** both killed at once | `FAILED (failures=1)` |
| control: `marker = {}` (gate bypassed entirely) | `FAILED (failures=7, errors=3)` |

Both NIT-1 checks are individually load-bearing. ✔ addendum (a).

**NIT-5 deadness (addendum (e)) — confirmed, by reading, not by a mutant.** `backup.py:227` is
`status = "ok" if not errors else "partial"`, and `errors` is not mutated between `:227` and the
return at `:237`; therefore `not errors` ⟺ `status == "ok"` at that point, and `and status == "ok"`
was unreachable-as-a-discriminator. A mutant cannot demonstrate deadness (any behavioural mutant
just changes the return: my inverted probe produced 10 failures, which proves the *return* is
covered, not that the removed clause was live). The `run_end` record still carries `"status"`
(`:229-232`) — the field is not lost. ✔

### 5.4 Branch-kill sweep over the whole gate (my own; driver `read2_branch_sweep.py` + `read2_unfenced_probe.py`)

I disabled each of the 16 refusals in `load_complete_marker` + `verify_completion_evidence` one at
a time and ran the 39-test suite:

| Branch | file:line | Killed by a test? |
|---|---|---|
| marker absent | `opsa_common.py:203-204` | ✔ `test_interrupted_run_…` |
| **per-run manifest absent** | `opsa_common.py:205-206` | ✖ |
| **marker is not a JSON object** | `opsa_common.py:211-212` | ✖ |
| **marker schema** | `opsa_common.py:213-214` | ✖ |
| marker names another run | `opsa_common.py:215-216` | ✔ `test_tampered_…` |
| manifest digest binding | `opsa_common.py:219-221` | ✔ `test_tampered_…` |
| exactly one `run_end` | `restore.py:82-84` | ✔ `test_hand_made_…` |
| `run_end` ok / no errors | `restore.py:86-90` | ✔ `test_hand_made_…`, `test_partial_run_…` |
| **per-run malformed lines** | `restore.py:92-93` | ✖ |
| **per-run header** | `restore.py:94-96` | ✖ |
| per-run vs global file records | `restore.py:102-103` | ✔ `test_tampered_…` |
| declared `files` is a non-bool int == count | `restore.py:104-107` | ✖ (subsumed by the next row) |
| `run_end.files == declared` | `restore.py:108-110` | ✖ (subsumed by the previous row) |
| **per-record `readback == "match"`** | `restore.py:111-112` | ✖ |
| NIT-1 marker `readback` claim | `restore.py:118-120` | ✔ `test_tampered_…` |
| NIT-1 marker `run_manifest` claim | `restore.py:121-123` | ✔ `test_tampered_…` |

I then proved, for each unfenced row, that the guarded state is **reachable** and that the branch
is the **sole** guard (HEAD refuses it; with that one branch killed the same state is accepted):

```
G4 marker schema
    HEAD   : rc=3 "run …: completion marker schema mismatch: 'mtc.opsa_run_complete/v99'"
    KILLED : rc=0 ''                      <-- restore ACCEPTS and restores
R3 per-run malformed lines
    HEAD   : rc=3 'run …: per-run manifest has malformed lines'
    KILLED : rc=0 ''
R4 per-run header
    HEAD   : rc=3 'run …: per-run manifest header missing or names another run'
    KILLED : rc=0 ''
R8 per-record readback
    HEAD   : rc=3 'run …: per-run manifest carries a non-matching readback record'
    KILLED : rc=0 ''
G2 per-run manifest absent
    HEAD   : rc=3 'run …: no per-run manifest (RUN_MANIFEST.jsonl absent)'
    KILLED : UNCAUGHT FileNotFoundError
G3 marker not a JSON object
    HEAD   : rc=3 'run …: completion marker is not a JSON object'
    KILLED : UNCAUGHT AttributeError: 'list' object has no attribute 'get'
R7 run_end files == declared
    HEAD   : rc=3 'completion marker declares files=99, per-run manifest lists 2'
    KILLED : rc=3 'completion marker declares files=99, per-run manifest lists 2'   (subsumed — not a hole)
```

This is **NIT-1** below. The code is correct today — every one of these states is refused — but
four of them have no regression fence.

---

## 6. Fail-open hunt — my own RED arms (item 2 and addendum (b)/(c))

Driver `C:/tmp/OPUS_P026_SCRATCH/read2_arms.py` and `read2_arms2.py`, run with the pinned
interpreter, `TEMP=C:\tmp\OPUS_P026_SCRATCH\read2_tmp`; full transcript in
`read2_arms_output.txt` / `read2_arms2_output.txt`. Each arm builds its own fixture store and
backup root; nothing touches the worktree.

| # | Shape probed | Observed |
|---|---|---|
| ARM-1 | interrupted run, restored by explicit id | backup rc=1, marker=False, run_manifest=False; restore **rc=3** `run_not_complete` / `no completion marker (COMPLETE.json absent)`; target never created ✔ |
| ARM-2 | `RUN_MANIFEST.jsonl` edited after the marker was written | **rc=3** `per-run manifest hash mismatch (marker=4b915884… actual=a632a4b7…)`; untampered control rc=0 ✔ |
| ARM-3 | **the ORIGINAL defect** on the `fcac0ac6` modules: `--latest` with an interrupted newest run | **DEFECT REPRODUCED** — `--latest rc=0 run_id='opsa-…317Z' status='ok'`, restored `['ledger_store/ledger.jsonl','ledger_store/sub/second.bin']` out of 3 source files. The interrupted run was shipped as complete, silently missing a file. |
| ARM-3b | the candidate on that same run, by explicit id | **rc=3** `no completion marker (COMPLETE.json absent)` ✔ |
| ARM-4 | run with `errors>0` (missing store) | backup rc=1, `completion_marker='none'`, no marker, no per-run manifest; restore **rc=3** ✔ |
| **ARM-5** | **addendum (b): partial run + hand-made marker carrying NEITHER `readback` NOR `run_manifest`** | **rc=3**, detail = `global manifest run_end is status='partial' with 1 error(s); only a run the backup tool closed successfully may be restored` — **the `run_end` reason fires, not the NIT-1 checks**. Gate order confirmed ✔ |
| ARM-5b | the same field-less marker on a run the tool DID close successfully | **rc=3** `completion marker declares readback=None; the backup tool writes 'all_match'` — the NIT-1 check is what stops it, exactly where it should ✔ |
| ARM-6 | another (genuinely complete) run's marker + manifest copied in | **rc=3** `completion marker names run 'opsa-…570Z'` ✔ |
| ARM-7 | re-digested per-run manifest listing FEWER files than the global manifest | **rc=3** `per-run manifest file records differ from the global manifest` ✔ |
| ARM-8 | run ids matching only by prefix/suffix (`…738`, `…738ZX`, id with `Z` stripped) | all three **rc=3** `run id not found in manifest` ✔ (selection is exact equality, `restore.py:66`) |
| ARM-9 | backup root copied WITHOUT `runs/` | **rc=3** `no completion marker (COMPLETE.json absent)` ✔ |
| ARM-10 | torn/truncated `COMPLETE.json` (NIT-2's documented rule) | **rc=3** `completion marker unreadable: Unterminated string…`; run-dir files unchanged; a re-backup gets a **new** run id and writes its marker ✔ |
| ARM-11 | dry run | rc=0, backup root **not created**, no evidence ✔ |
| ARM-12 | crash between the manifest write and the marker write | see §4.1 — `status='partial'`, only `RUN_MANIFEST.jsonl` left, restore rc=3, next run takes a new id ✔ |
| ARM-13 | CLI: `--latest`, and `--run` omitted | both **rc=2** `restore.py: error: the following arguments are required: --run`; explicit `--run` rc=0 ✔ |
| ARM-16 | `--store` filter with a per-run manifest missing the other store | **rc=3** `per-run manifest file records differ from the global manifest` — the gate reads the FULL global record set (`restore.py:201` passes `records`, not `selected`), so a store filter cannot narrow it ✔ |
| ARM-17 | `COMPLETE.json` replaced by a directory | **rc=3** `run_not_complete` ✔ |
| **ARM-15** | per-run manifest rewritten with non-UTF-8 bytes AND the marker digest re-bound | **`UnicodeDecodeError` escapes uncaught**; CLI `rc=1` with a traceback instead of the structured rc-3 refusal. Target never created. → **NIT-2** |
| **ARM-14** | a WHOLE forged run: attacker-written `manifest.jsonl` lines (`run_start`/`file`/`run_end ok`) + a self-consistent `runs/<id>/` evidence pair | **rc=0, restored** the attacker's bytes. See §9 "design limit" — not a finding against this candidate |

### Addendum (c): does any restore path bypass `verify_completion_evidence`?

No. `run_restore` is the only restoring function; the gate at `restore.py:200-206` sits **after**
manifest-field and path-confinement validation and **before** the mode banner, every
`verify_backup_file` call, every `mkdir`, and every `copyfile`. `--check-only` does not skip it
(both ARM-5 and ARM-17 were run in check-only mode). `select_run` and `verify_backup_file` are
helpers called only from `run_restore`; `main()` delegates to it. The P0-30 adapter also calls
`restore.run_restore` (twice: check-only, then restore) and therefore passes the same gate.
Only `RunNotComplete` is caught at `:202`; anything else propagates — which is where NIT-2 lives.

---

## 7. Contract-change blast radius (item 4)

Consumers of `restore.py` / `select_run` / `runs/<run_id>/` anywhere in the worktree (read-only
`Grep` over the whole tree):

| Consumer | Uses | Broken by the stricter contract? |
|---|---|---|
| `p030_closed_partition_backup_adapter.py` | `import restore`; `restore.run_restore` ×2 (`:716`, `:746`); reads `runs/<run_id>/` in `_isolated_restore_inputs` (`:563-632`) | **No — handled by slice 2.** Both adapter checks exit 0 at HEAD (45 OK / 10 OK) |
| `check_p030_closed_partition_backup_adapter.py` | drives the adapter; fence `test_isolated_restore_carries_the_runs_own_completion_evidence` (`:1194-1261`) | No |
| `p030_opsa_heartbeat_adapter.py` / its checker | `opsa_common` + `heartbeat` only; never restore | No |
| `MTC_COMMAND_CENTER/tools/opsa/test_opsa.py` | the suite itself | No |
| `MTC_COMMAND_CENTER/11_TRIAGE/.../RESTORE_DRILL_EVIDENCE.md` | a recorded drill using `--latest` | **Yes — a document.** Partly addressed by NIT-4; one command left behind → NIT-3 |
| `MTC_COMMAND_CENTER/tools/opsa/README.md` | usage lines | No — fixed by `e114ed31` + this slice |
| `02_MTC_BACKTEST/scripts/backup_restore.py` + its runbook/checklist | a **different**, tarball-based tool; no import of or reference to `tools/opsa` | No |
| `mtc_cli/commands/audit.py`, dashboard readers, `_deepseek_driver` | matched only on the unrelated word "runs" | No |

No other code consumer exists. No CI job runs the adapter checker (P0-27 reconciliation R10), so
master is unaffected until merge.

### Is the slice-2 resolution technically sound? — Yes, and I verified it three ways

1. **Could the adapter path restore a run the bare `restore.py --run` would refuse?** No, and it
   is strictly *stricter*. `_isolated_restore_inputs` copies the run's own `COMPLETE.json` and
   `RUN_MANIFEST.jsonl` **byte-for-byte** (`:572-573`, `:594-595`) and the validated global
   `manifest.jsonl` byte-for-byte (`:601`) into the temp root; the same
   `verify_completion_evidence` then runs on the same bytes, so its verdict is identical. On top
   of that the adapter applies `_complete_p026_run` (`:471-528`): exactly one `run_start` with
   `dry_run is False`, exactly one `run_end` with `status == "ok"` and `errors == []`, no record
   kinds other than `run_start`/`file`/`run_end`, `files`/`bytes` arithmetic, every record in the
   named store, every `readback == "match"`, and the file set exactly
   `{_P030_STABLE_PREFIX.json, snapshot_rel}`. Missing evidence is fail-closed
   (`ValueError("P026 completion evidence is unavailable")`, `:574-575`) — never fabricated.
2. **Does the digest binding survive the copy?** Yes — `run_manifest_sha256` is taken over the
   `RUN_MANIFEST.jsonl` bytes, which are copied unchanged, so the binding is preserved by
   construction. I falsified the alternative: I mutated the adapter to **fabricate** a fresh
   consistent pair (rebuilt manifest + re-digested marker) instead of copying, and ran the
   *unmodified* checker against it:
   ```
   ### adapter checker [fabricated_evidence] rc=1
   FAIL: test_isolated_restore_carries_the_runs_own_completion_evidence
   Ran 45 tests … FAILED (failures=1, errors=1)
   ```
   (the second error is an artefact of my scratch copy, which lacks
   `p030_opsa_backup_config.json` → `test_committed_configuration_is_explicitly_non_runnable`
   raises `FileNotFoundError`; it appears identically in my scratch **baseline** run, so it is
   not caused by the mutant. In the real worktree the checker is 45 OK.)
   The fence is real and load-bearing.
3. **Does the mutant test still detect the isolation mutant for the right reason?**
   `test_shared_archive_reversion_mutant_is_detected` (`:1153-1192`) now accepts the generic
   `"P026 restore failed"` **only if** restore's stderr contains
   `per-run manifest file records differ from the global manifest` (`:1188-1192`). That is the
   correct narrowing: a broken restore can no longer pass the mutant by failing for any reason.

---

## 8. Documentation judgement (addendum (d)) and the author-disclosed residual (item 8)

**README NIT-2 paragraph (`README.md:63-66`) — honest.** Every clause checks out against the bytes
and against my arms: `write_once_bytes` is `O_EXCL` and not atomic (`opsa_common.py:153-165`); a
torn/unreadable marker is treated as not complete (ARM-10, rc 3); the data stays in place and the
package has no delete primitive (`NoDeleteGuaranteeTests` scans all five tool modules for
`os.remove(`, `os.unlink(`, `.unlink(`, `os.rmdir(`, `.rmdir(`, `shutil.rmtree(`, `.rmtree(`,
`shutil.move(`, `os.truncate(`, `send2trash(`); the adapter's `tempfile.TemporaryDirectory`
cleanup is in the P0-30 file, not in "this package"); "never restored from" is exactly the rc-3
refusal. **"re-backed-up under a NEW run id"** does not over-claim an automatic retry: I checked
that it is the tool's own per-run id behaviour (`run_id_for`, ms precision) and confirmed it
operationally in ARM-10 (the next `backup.py` invocation produced a different run id and wrote its
marker). The phrasing is passive and describes what the operator's next backup does; I would not
call it a finding, though "and the store is re-backed-up by the next run, which takes a new run
id" would remove the last trace of ambiguity.

**`RESTORE_DRILL_EVIDENCE.md` NIT-4 note (lines 22-29) — honest, but not complete.** The three
factual claims hold: `--latest` is removed and now exits 2 (ARM-13, observed rc 2); the 2026-08-24
run carries no `COMPLETE.json` (sound by construction — `fcac0ac6:backup.py` writes no marker at
all; the recorded manifest at lines 89-94 shows only `run_start`/`dir`/`file`/`run_end`); the
transcript is kept unchanged, which is right — a recorded drill must never be rewritten. The
incompleteness is NIT-3.

**Item 8 (the author-disclosed README residual) is CLOSED.** `README.md:60-69` now names an
explicit `--run <run_id>` and the `COMPLETE.json` + `RUN_MANIFEST.jsonl` pair; no `--latest`
survives anywhere in `tools/opsa/`. I graded it myself rather than accepting the disclosure: I
grepped the whole worktree for `--latest` and the only survivors are in
`RESTORE_DRILL_EVIDENCE.md` (NIT-3) and inside `fcac0ac6` blobs.

---

## 9. Lead authorship (item 6)

The candidate is Lead-authored and disclosed in the commits, in `LEAD_VERIFICATION_P026_REPAIR.md`,
in `LEAD_VERIFICATION_P026_NIT.md` and in the brief. **It does not change my verdict**, for one
concrete reason: I did not take a single claim on trust. Every count in the Lead's records was
re-derived from the bytes or re-run here (§3, §5.2, §2 ruff parity), the two NIT-1 fences were
re-killed with my own mutants rather than by reading the Lead's `LEAD_RED_P026_NIT1a/b` files, and
the original defect was reproduced from the `fcac0ac6` blobs by me (ARM-3). Where my numbers
differ from the Lead's (arm A, arm D) I traced the difference to the suite size at the time of the
Lead's run and said so, rather than reporting a discrepancy.

What authorship *does* require is unchanged and is already the plan: this report accepts nothing,
and the roster still needs the second flagship (exact Sol, 2026-09-19) on these same bytes. I need
nothing beyond that. One process point belongs to the owner, not to me: NIT-4 below.

---

## 10. Report honesty (item 7) — the Lead's records vs the bytes

| Lead claim | Checked against | Result |
|---|---|---|
| `Ran 37 tests … OK` (`LEAD_UNITTEST_312.txt`, slice 1) | file read | correct for slice 1 |
| `Ran 39 tests … OK` (`LEAD_UNITTEST_312_slice3.txt`; `LEAD_GREEN_test_opsa.txt`) | my own run at HEAD | **reproduced: `Ran 39 tests … OK`** |
| `FAILED (failures=5, errors=4)` RED on the pre-fix modules | my arm A | consistent — the Lead's arm ran the **37-test** slice-1 suite; the 39-test suite gives 8+5, the extra arms being slice-2/3 + NIT-1 |
| `Ran 45 tests … OK`, exit 0 for the closed-partition checker | my own run | **reproduced** |
| `9 of 45` RED on the slice-1 adapter (`LEAD_RED_ARM_old_adapter_new_checker.txt`) | file read: `FAILED (failures=6, errors=3)` | **6+3 = 9 ✔** |
| reserved-id test RED on the slice-1 `opsa_common` | my arm C | **reproduced: `FAILED (failures=2)`**, and *only* that test |
| hand-made-evidence test RED `3 F + 1 E` on the slice-2 modules | my arm D | **reproduced** (`failures=3, errors=1` in the Lead's file; my run on the newer suite adds the NIT-1 failure → 4+1) |
| NIT-1a / NIT-1b mutants each `1 failed` | my (a1)/(a2) mutants | **reproduced independently** |
| "Ruff … per file identical to HEAD: restore 2, backup 4, test_opsa 7" | my own ruff runs on both revisions | **exact** |
| "Ruff 0.16.4 from `C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe`" (`LEAD_VERIFICATION…:50`) | located the binary; `ruff 0.16.4` | **correct** (the REVIEW_BRIEF's "same venv" wording is the inaccurate one) |
| "`watchdog.py` untouched" | blob digests at `fcac0ac6` and `505af399` | **identical bytes ✔** |
| NIT-3 "fixed on the P0-30 branch, deliberately not touched here" | `check_p030_closed_partition_backup_adapter.py` unchanged since `d81b07f6` | consistent; I did not review `d426e79f` (out of scope for this lane) |
| Scope "exactly five files, +46/−6" | `--stat` + `--name-status` | **exact, 0 added** |

I found **no misstatement** in the Lead's verification records. The one inaccuracy I found is in
the REVIEW_BRIEF itself (ruff location), and it did not obstruct any mandated command.

---

## 11. Findings

### NIT-1 — four refusals in the completion gate are sole guards with no test: delete any one and the 39-test suite stays green

`opsa_common.py:213-214` (marker `schema`), `restore.py:92-93` (per-run `_malformed` lines),
`restore.py:94-96` (per-run manifest header), `restore.py:111-112` (per-record `readback == "match"`).

Reproduction is in §5.4: for each of the four, HEAD refuses the state with a clean rc-3
`run_not_complete`, and with that single `if` neutralised the same state is **accepted and
restored with rc 0** — while `python -m unittest test_opsa` still reports `Ran 39 tests … OK`.
Two further branches (`opsa_common.py:205-206` per-run manifest absent, `:211-212` marker not a
JSON object) are likewise untested and degrade to an uncaught `FileNotFoundError` / `AttributeError`
when removed. (`restore.py:104-107` and `:108-110` are mutually subsuming, so their "unfenced"
status is not a hole.)

**Why this is a NIT and not REQUIRED:** the shipped code is correct — every one of these states is
refused today, which I verified directly. None of them is reachable from anything the tools
themselves can produce: `backup.py` never writes a wrong-schema marker, never writes a headerless
or malformed per-run manifest, and never writes a completion pair at all for a run in which any
readback mismatched (`backup.py:196-200` makes that an error, and `:220`/`:251-252` refuse the
evidence when `errors` is non-empty). Reaching them requires an actor who can write inside
`runs/<run_id>/` and re-bind the marker digest — the same actor as §9's design limit. And all four
packet-§5 falsifications, plus the Gemini F-01 fence, plus this slice's own two new branches, are
fenced and RED-verified. What is missing is regression protection, not behaviour.

I record plainly that a reviewer could defensibly grade this REQUIRED on the "sole guard, zero
tests" precedent. I did not, for the reasons above; the call between "fix in this slice" and "one
test in the merge PR" is the Lead's and the owner's.

**Fix (small, one test):** extend `test_tampered_marker_or_run_manifest_is_refused` with a
table-driven arm over the four states — marker `schema` bumped; a junk line appended to the per-run
manifest (digest re-bound); the header line dropped (digest re-bound); every per-run `file` record
set to `readback: "MISMATCH"` (digest re-bound) — each asserting rc 3 and the matching detail
fragment. My probe `C:/tmp/OPUS_P026_SCRATCH/read2_unfenced_probe.py` already builds all four
states and can be lifted almost verbatim.

### NIT-2 — the gate's per-run manifest read is unguarded: a non-UTF-8 `RUN_MANIFEST.jsonl` raises an uncaught `UnicodeDecodeError` instead of the package's structured rc-3 refusal

`restore.py:91` — `run_records = read_jsonl(run_manifest_path(run_dir))` sits outside any
`try`, and `opsa_common.read_jsonl:232` opens with `encoding="utf-8"`. `load_complete_marker`
cannot filter this case: it hashes the manifest *bytes*, so a tamperer who rewrites the manifest
with non-UTF-8 bytes and re-binds `run_manifest_sha256` passes the digest check and reaches the
decode. Observed (ARM-15):

```
in-process: UNCAUGHT UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 2
CLI:        rc=1, last stderr line = "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff …"
target_created=False
```

Not a fail-open — nothing is restored and the target is never created. It is a violation of the
package's own invariant 3 ("inability to evaluate is its own outcome … tools never report OK when
they could not actually check", `opsa_common.py:15-17`, README §4), and it hands the operator rc 1
(the "restore failed / hash mismatch" class) plus a traceback where the contract promises rc 3
`run_not_complete`. Introduced by the repair's own new read (slice 1); the same exposure on the
*global* manifest (`restore.py:154`) predates the repair entirely and is untouched by it.

**Fix (one line):** wrap `:91` as
`try: run_records = read_jsonl(...)` / `except (OSError, UnicodeDecodeError) as exc: raise RunNotComplete(f"run {run_id}: per-run manifest unreadable: {exc}") from exc`
— mirroring what `load_complete_marker:207-210` already does for the marker.

### NIT-3 — the NIT-4 note covers Part A only; one `--latest` command survives unmarked in section C4

`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md:486`
(`python restore.py --config "$S/config.json" --latest --check-only`), in section
`## C4. Nit 4 — --check-only no longer reports dirs_recreated it did not create`.

The dated note (lines 22-29) is placed under `## Part A` (line 20) and says "**The commands below** that pass
`--latest` now exit 2". Read from its position that scopes it to Part A, which contains the other
two occurrences (`:129`, `:161`). A reader who lands in C4 — a section specifically about
`--check-only`, i.e. the very command an operator would copy — gets no warning. The transcript
must of course stay unchanged; the fix is either one more dated marker line above C4, or changing
the Part-A note's wording to "every `--latest` command in this document".

(Gemini's NIT-slice pass read only lines 1-40 of this file — see its own coverage list, item 10 —
so it could not have seen this.)

### NIT-4 — authority record: `RESTORE_DRILL_EVIDENCE.md` is the eighth file on the branch and no owner decision names it

The scope packet §2 fixes a five-file ceiling (all under `tools/opsa/`) and §7 makes drifting
outside it a stop-and-report condition; §6 explicitly excludes "`config.example.json` and
`README.md` updates". Every previous step outside that ceiling was covered by its own recorded
decision: `OD-20260915-P026-ADAPTER-LEAD-1` (the two repo-root P0-30 files),
`OD-20260915-P026-README-A-1` (`tools/opsa/README.md`), and `OD-20260918-P026-N2-DOC-1` for the
NIT-2 text ("closed by DOCUMENTING the current behaviour (README / runbook text)").
`MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md` is neither a
README nor a runbook — it is a triage drill transcript — and I found no row naming it in
`C:/CT13/DECISIONS.md`, nor an `OWNER_ANSWERS_20260918*` file. The Lead's own first-read
adjudication had put NIT-4 at "rides with the follow-up slice **unless the owner wants it in the
merge PR**" (`LEAD_ADJUDICATION_P026_T0.md:20`), i.e. the Lead itself had deferred the question.

The change itself is additive, behaviour-free, factually honest (§8) and safe; I am not asking for
it to be reverted. I am asking that the pattern the packet established be kept: one owner
one-liner naming the file, recorded as an OD row, before the merge PR — or drop that one hunk to
the follow-up slice. Left as is, the branch carries a file outside every recorded authorization.

### NIT-5 — docs still advertise a 900-second silence bound; the owner ratified 300

`MTC_COMMAND_CENTER/tools/opsa/README.md:74` and `MTC_COMMAND_CENTER/tools/opsa/watchdog.py:38`
both show `--silence-seconds 900`. The packet §4 required the 900-second **default** and its false
#39 provenance to go, and they did — `watchdog.py:240-246` has `required=True`, no default, and a
comment retiring the provenance claim, so the code is conformant. But
`OD-20260914-P030-P026-CONFIG-1` (O-3) ratified **300 s**, and the usage examples still put 900 in
front of the operator. Pre-existing (both lines are byte-identical to `fcac0ac6`), outside the
restore contract and outside this slice's five files — I name it only because item 8 asks for any
document the contract leaves behind, and because the README is a file this branch already edits.

---

## 12. Design limit — recorded, not a finding

**The global `manifest.jsonl` has no root of trust.** ARM-14: an actor who can write inside
`backup_root` can append a complete forged run (`run_start` + `file` records + `run_end status=ok
errors=[]`), create `runs/<forged_id>/` with attacker bytes, and write a fully self-consistent
`RUN_MANIFEST.jsonl` + `COMPLETE.json` pair. Every gate check passes — because they all check
*internal consistency*, and the forgery is internally consistent — and restore returns **rc 0**
and writes the attacker's bytes:

```
rc=0 summary={'mode': 'restore', 'run_id': 'opsa-29991231T235959.999Z', 'status': 'ok',
              'verified_against_manifest': 1, 'restored': 1, 'errors': 0}
restored_bytes=b'ATTACKER CONTENT - not the real evidence\n'
```

This is **out of scope and not a defect of this candidate**: the packet asks for completion
identity against *partial and interrupted runs* and *tampering with an existing marker*, not for
authenticity against an actor with write access to the evidence store, which would need a signing
key or an off-store digest anchor — neither requested nor permitted by §4/§6. I checked
specifically for an over-claim and found none: `restore.py`'s docstring says a run without
evidence "or with a tampered marker/manifest" is refused (true), and `write_completion_evidence`
says the digest lets restore "prove the pair belongs together" (pair binding — accurate, and not a
claim of authenticity). If the owner ever wants that boundary visible to operators, one README
sentence would do it; I am not raising it as a finding here.

---

## 13. NOT VERIFIED

1. **The 2026-08-24 drill run's absence of `COMPLETE.json` was not observed directly.** The
   drill's `_drill_scratch/` directory no longer exists in the worktree. The NIT-4 note's claim is
   sound by construction (`fcac0ac6:backup.py` contains no marker-writing code at all, and the
   recorded manifest lines 89-94 show only the five original record kinds) but it is an inference,
   not a reading of that run's directory.
2. **`d426e79f` (the P0-30 branch where NIT-3 of the first read was fixed) was not reviewed.** I
   verified only that `check_p030_closed_partition_backup_adapter.py` is unchanged on this branch
   since `d81b07f6` and that its ASCII-anchor behaviour is not this candidate's concern. Whether
   the two branches' edits to that file collide at merge is a merge-time question I cannot settle
   from here.
3. **Real-root behaviour is unverified.** Every arm ran under the ASCII scratch temp. The owner's
   `<BACKUP_ROOT>` (`OD-20260914-P030-P026-ROOTS-1`) is a OneDrive-synced path containing `İ` and
   `ş`, with Files-On-Demand placeholders. Nothing in this read says the tools behave correctly
   there; the first read's NIT-3 (the checker's ASCII anchor) is direct evidence that non-ASCII
   paths have already bitten this package once.
4. **No concurrency testing.** Two `backup.py` processes running against one `backup_root`, or a
   restore racing a backup, were not exercised. `append_jsonl` does one `write`+`flush`+`fsync`
   per record with no lock; ms-precision run ids make a run-dir collision unlikely but not
   impossible in principle.
5. **Windows-only.** All arms ran on Windows 11 / NTFS. `O_EXCL`, `fsync` and `Path.rename`
   semantics on the Linux deploy targets named in the packet's excluded templates are untested
   here.
6. **The adapter checker in my scratch copy cannot reach `p030_opsa_backup_config.json`**, so
   `test_committed_configuration_is_explicitly_non_runnable` errors there. That is an artefact of
   my copy (it appears in my scratch *baseline* too); the worktree run is 45 OK. I did not
   reconstruct that fixture.
7. **Gemini's `P026_NIT_GEMINI` PASS was read, not re-executed.** Its traces agree with mine on
   the gate order and on NIT-5; its coverage list shows it read only lines 1-40 of
   `RESTORE_DRILL_EVIDENCE.md` and did not run mutants, which is why NIT-1 and NIT-3 are new here.
   I formed every conclusion from the bytes first.
8. **No drill, no host, no network, no credential, no scheduling, no deployment** was performed or
   attempted; no acceptance of WP-P0-26 follows from this report. Nothing in the worktree was
   modified; no `git status`/`add`/`commit`/`checkout` was run in any repository.

---

## 14. Summary

The NIT slice does exactly what it claims. NIT-1 of the first read is closed correctly and — the
part that matters — **placed last**, so the `run_end` fence that answered Gemini's F-01 keeps its
precedence; I confirmed that with a partial run carrying a field-less hand-made marker (ARM-5) and
with the mirror case on a successfully closed run (ARM-5b). Both new checks are individually
load-bearing under mutation. NIT-5 is genuinely dead code, removed without losing the `status`
field from the `run_end` record. Both documentation changes are honest, and the README residual
that the first read disclosed is closed. The original defect still reproduces on the `fcac0ac6`
modules exactly as the packet §3 describes, and the repaired tool refuses that same run. Scope is
five files, nothing added, ruff at parity, 39/45/10 green on the pinned interpreter.

The five NITs are: four sole gate refusals with no regression test (NIT-1, the substantive one),
an unguarded decode in the gate that turns an evaluation failure into a traceback (NIT-2), one
stale `--latest` command left outside the new drill note (NIT-3), an out-of-ceiling documentation
file with no owner decision naming it (NIT-4, a process point for the owner), and a stale
900-second example in docs the owner has since re-ratified at 300 (NIT-5, pre-existing).

None of them is a defect that ships. None of them blocks the second flagship read.

VERDICT: PASS-WITH-NITS
