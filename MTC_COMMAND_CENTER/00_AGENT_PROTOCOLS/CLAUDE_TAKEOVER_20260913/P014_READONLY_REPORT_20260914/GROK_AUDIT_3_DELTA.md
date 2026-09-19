# GROK_P14C detection audit — corrected WP-P0-14 read-only report (fresh session)

Auditor: grok-4.6 (lane GKP14C). Subject copied to `C:\tmp\GROK_SCRATCH_GKP14C_20260914\pkg\` and verified there. Ledger copies for SQL: `C:\tmp\GROK_SCRATCH_GKP14C_20260914\verify\fixture-ledger*.sqlite`. This audit accepts nothing. No git. No network.

Authorized questions: **Q-A** (fixture ledger families / state / rejection reasons) and **Q-B** (trial-catalog contract types / refusal reasons / test count / whether catalog data exists). Fixture data only.

Interpreter used for all Python: `C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe` (CPython 3.12.12).

Input audit: `C:/tmp/CLAUDE_P0_RUN_20260913/laneGKP14B_grok_audit/GROK_P14B_REPORT.md` (4 open findings: prior-9, new-1, new-2, new-3). Claimed dispositions: `C:/tmp/P014_RO_20260914/DISPOSITION_FIX2.md` (all four marked FIXED). Those FIXED labels are not accepted; each row below is independent.

---

## 0. Prior findings (4 open from P14B)

| # | prior severity | this audit | evidence |
| --- | --- | --- | --- |
| prior-9 | CORRECTION | RESOLVED | Event-count half is now an executable command. `P014_READONLY_REPORT.md:19` cites `SELECT json_extract(canonical_event, '$.next_state') AS next_state, COUNT(*) FROM lifecycle_events GROUP BY 1` on `file:C:/tmp/P014_RO_20260914/fixture-ledger.sqlite?mode=ro`. Independent `?mode=ro` on a copy returns `CANDIDATE=1, CAPTURED=1, TRIAGED=1`. The old non-executable `SELECT next_state, COUNT(*) FROM lifecycle_events GROUP BY next_state` is gone from `P014_READONLY_REPORT.md`, `reproduce_report.py`, and `REPORT.md` (count=0). `reproduce_report.py:312-315` is `EVENT_COUNT_SQL`; `:321` is `conn.execute(EVENT_COUNT_SQL)`; `:371` prints that command. The report cites query text `:313` and print `:371`. DISPOSITION_FIX2’s “executed at :321” is accurate; its “:329 uses that query” is the caller `event_state_counts(LEDGER_PATH)`, not a remaining defect. 29-test half was already fixed in P14B and remains EQUAL (independent ast: 29 top-level `def test_*`). |
| new-1 | CORRECTION | RESOLVED | Same event-count command defect as prior-9. Cited command now matches the SQL the reproducer actually runs. Independent copy URI `file:///C:/tmp/GROK_SCRATCH_GKP14C_20260914/verify/fixture-ledger.sqlite?mode=ro`: the cited json_extract command returns 1/1/1; the old column command still raises `OperationalError: no such column: next_state`. `REPORT.md:33` (inside the verbatim fence) pastes the live command line. |
| new-2 | CORRECTION | RESOLVED | `P014_READONLY_REPORT.md:85` cites `trial_catalog.py:75` (`RESERVED_BOUNDARY_KEY = "RESERVED_BOUNDARY_KEY"`). Copied `trial_catalog.py:76` is still blank. Class citation `:72` remains EQUAL. |
| new-3 | NIT | RESOLVED | `P014_READONLY_REPORT.md:3` is the first paragraph and now contains fixture-only, recorded `accepted=false` (`P031_M1_SCOPE_AND_STATUS.md:718`), `authoritative` is `false` (`fixture-status-report.json:10`), and the `START_HERE.md:54` sequencing quote. |

No REGRESSED row. All four P14B-open findings are closed in the corrected files.

---

## 1. Scope

`P014_READONLY_REPORT.md` answers Q-A and Q-B and does not design Explorer, does not recommend product work, and does not ship product code. Explorer appears only as the deferred/not-this-work statement in the first paragraph and as the quoted `START_HERE.md:54` sequencing amendment.

`REPORT.md` is the execution wrapper the task required (what was built, verbatim dump, interpreter, NOT VERIFIED, SHA256SUMS). `DISPOSITION_FIX2.md` is extra vs the original three deliverables, as `DISPOSITION_FIX1.md` was; it is not Q-A/Q-B creep.

---

## 2. Citation table

Status is EQUAL / WRONG LINE / NOT FOUND against the copied files. Paths below are the subject originals; the pkg copies are byte-identical.

| citation | claimed fact | source line content | status |
| --- | --- | --- | --- |
| `P031_M1_SCOPE_AND_STATUS.md:718` | recorded `accepted: false` | `- \`accepted\`: \`false\`` | EQUAL |
| `fixture-status-report.json:10` | `authoritative` is false | `"authoritative": false,` | EQUAL |
| `START_HERE.md:54` | P0-14 sequencing amendment preserved | `P0-14 \| Owner chose to defer Minimum Explorer behind core Bridge engineering with a small reproducible read-only report meanwhile. Preserve sequencing amendment; full package is not complete.` | EQUAL |
| `fixture-status-report.json:16` | `source_kind` is FIXTURE | `"source_kind": "FIXTURE"` (inside `derived_current_state`) | EQUAL |
| `fixture-status-report.json:82` | JSON `scope` is `FIXTURE LEDGER DATA` | `"scope": "FIXTURE LEDGER DATA",` | EQUAL |
| JSON has no `accepted` / `fixture_only` keys | honesty bullets | top-level keys checked; neither present | EQUAL |
| `SELECT json_extract(canonical_event, '$.next_state') AS next_state, COUNT(*) FROM lifecycle_events GROUP BY 1` on `fixture-ledger.sqlite?mode=ro` | CANDIDATE/CAPTURED/TRIAGED = 1 | command runs on a copy; returns those three rows | EQUAL |
| `PRAGMA table_info(lifecycle_events)` has no `next_state` | `next_state` lives in the blob | columns are `global_sequence, event_id, writer_class, writer_id, writer_sequence, candidate_id, canonical_event, canonical_evidence, previous_digest, digest` | EQUAL |
| `reproduce_report.py:313` | query text the reproducer executes | `"SELECT json_extract(canonical_event, '$.next_state') AS next_state, "` (assignment `:312-315`; `execute` at `:321`) | EQUAL |
| `reproduce_report.py:371` | prints that command | `print(f"command: {sql_counts}")` | EQUAL |
| `SELECT * FROM lifecycle_events ORDER BY global_sequence` on `fixture-ledger.sqlite?mode=ro` | one candidate `QLC-20260912-demo0001`, last event `CANDIDATE` / `REGISTRAR` / `2026-09-12T20:00:02Z`, `failing_checks=[]` | command runs; values are inside `canonical_event` / `canonical_evidence` blobs, not SQL columns | EQUAL as blob contents |
| `SELECT * FROM lifecycle_current` | `current_state=CANDIDATE`, `last_sequence=3`, `source_kind=FIXTURE`, `authoritative=0` | those are real columns; one row matches | EQUAL |
| `reproduce_report.py:353` | purpose cell text `not persisted in this fixture evidence` | `purpose_cell = "not persisted in this fixture evidence"` | EQUAL |
| `reproduce_report.py:98-101` | derivation of `check_set_purpose` from event shape | loop calling `check_set_purpose(...)` | EQUAL |
| `fixture-status-report.json:88-92` | three `unresolved_lifecycle_contracts` | L88 key; L89–L91 the three strings; L92 `]` | EQUAL (items L89–L91) |
| `p031_lifecycle_ledger.py:1259-1267` | seven-item reader source list | L1259 key+`[`; L1260–L1266 the seven strings; L1267 `],` | EQUAL (items L1260–L1266) |
| `p031_lifecycle_ledger.py:25` | CLI import of `mtc_contracts` | `from mtc_contracts.execution import LifecycleEvent, LifecycleWriterClass` | EQUAL |
| `trial_catalog.py:39-63` | `__all__` public names; 19 types after excluding 4 | `__all__ = [` at L39 through `]` at L63; 23 names; exclude the four named; 19 remain | EQUAL |
| `trial_catalog.py:237` | alias purpose comment | `# Compatibility name for the provisional type; no digest API is attached to either name.` | EQUAL |
| `trial_catalog.py:148` ArtifactKind | class + four enum members | `class ArtifactKind(str, Enum):` | EQUAL |
| `trial_catalog.py:72` BoundaryRefusalReason | class | `class BoundaryRefusalReason(str, Enum):` | EQUAL |
| `trial_catalog.py:75` `RESERVED_BOUNDARY_KEY` member | enum member | `RESERVED_BOUNDARY_KEY = "RESERVED_BOUNDARY_KEY"` | EQUAL |
| `trial_catalog.py:278` CommitPartEntry | class | `class CommitPartEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:195` CompletedRunInput | class | `class CompletedRunInput(ContractModel):` | EQUAL |
| `trial_catalog.py:182` LineageOriginReceipt | class; fields include optional hash | `class LineageOriginReceipt(ContractModel):`; field at L192 | EQUAL as class line; fields match L192 |
| `trial_catalog.py:192` | `canonical_path_receipt_hash: Sha256 \| None = None` | exact source text | EQUAL |
| `trial_catalog.py:186-187` | hash “absent by design for screening” | sentence wraps across L186–L187 | EQUAL |
| `trial_catalog.py:465` NestedSchemaColumnEntry | class | `class NestedSchemaColumnEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:122` ProvisionalBoundaryPayload | class | `class ProvisionalBoundaryPayload(ContractModel):` | EQUAL |
| `trial_catalog.py:484` PublishedViewSchemaDocumentV1 | class | `class PublishedViewSchemaDocumentV1(ContractModel):` | EQUAL |
| `trial_catalog.py:78` ReservedBoundaryKeyRefusal | class | `class ReservedBoundaryKeyRefusal(Exception):` | EQUAL |
| `trial_catalog.py:238` RunCellDimensionsReceipt | alias assignment | `RunCellDimensionsReceipt = RunCellDimensionsReceiptV1` | EQUAL |
| `trial_catalog.py:222` RunCellDimensionsReceiptV1 | class | `class RunCellDimensionsReceiptV1(ContractModel):` | EQUAL |
| `trial_catalog.py:246` RunEnvelopeV1 | class | `class RunEnvelopeV1(ContractModel):` | EQUAL |
| `trial_catalog.py:398` SchemaColumnEntry | class | `class SchemaColumnEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:302` SelectedArtifactCommitEntry | class | `class SelectedArtifactCommitEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:294` SelectedArtifactMemberEntry | class | `class SelectedArtifactMemberEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:157` SelectedArtifactPayloadReceipt | class | `class SelectedArtifactPayloadReceipt(ContractModel):` | EQUAL |
| `trial_catalog.py:175` SinkCapabilityClass | class | `class SinkCapabilityClass(str, Enum):` | EQUAL |
| `trial_catalog.py:137` TerminalTrialReceipt | class | `class TerminalTrialReceipt(ContractModel):` | EQUAL |
| `trial_catalog.py:168` WriterAdapterId | class | `class WriterAdapterId(str, Enum):` | EQUAL |
| `test_trial_catalog_types.py` 29 `def test_*` | test count | independent ast: 29 top-level `def test_*` | EQUAL |
| `test_trial_catalog_types.py:169-177` | 5 parametrize cases | decorator L169; cases L172–L176; `],` L177 | EQUAL (items L172–L176) |
| `test_trial_catalog_types.py:121-144` | 6 `_completed_run_members` | function L121; dict L122–L144; six keys | EQUAL |
| `test_trial_catalog_types.py:194` | used by T18 parametrize | `@pytest.mark.parametrize("member", sorted(_completed_run_members()))` | EQUAL (decorator; `def` is L195) |
| `test_trial_catalog_types.py:621` | 3 parametrize cases | `@pytest.mark.parametrize("ambiguous", ["period", b"period", bytearray(b"period")])` | EQUAL |
| `P013_HANDOFF.md:50` | full catalog writer excluded / nonaccepted | `Still excluded and nonaccepted: full catalog writer, selection/artifact/address pipeline,` | EQUAL |
| catalog data NONE FOUND | writer-named targets under P013 worktree | independent walk: zero `trades.parquet` / `equity.parquet` / `intents.jsonl` / `levels.parquet` | EQUAL |

Independent SQL (copy `C:\tmp\GROK_SCRATCH_GKP14C_20260914\verify\fixture-ledger.sqlite?mode=ro`):

- `lifecycle_current`: one row `QLC-20260912-demo0001`, `current_state=CANDIDATE`, `last_sequence=3`, `source_kind=FIXTURE`, `authoritative=0`.
- three events; `json_extract(canonical_event,'$.next_state')` counts CAPTURED=1, TRIAGED=1, CANDIDATE=1.
- latest event `global_sequence=3`, `event_type=CANDIDATE`, timestamp `2026-09-12T20:00:02Z`, writer `REGISTRAR`, `failing_checks=[]`.
- evidence keys: `check_set_version`, `evaluation_run_hash`, `failing_checks`, `source_kind`. **`check_set_purpose` is absent**.
- restored and backup ledgers: 3 events, one current CANDIDATE row. Restored and backup share digest `997977f8…`; primary ledger is `823c7c90…`.

37 absolute `C:/tmp/P014_RO_20260914/...:line` citations in `P014_READONLY_REPORT.md` were range-checked; all exist and point at the claimed construct. Zero WRONG LINE / NOT FOUND.

---

## 3. Findings

| # | severity BLOCKING / CORRECTION / NIT | file:line | what is wrong | why it matters |
| --- | --- | --- | --- | --- |

No BLOCKING, CORRECTION, or NIT finding: Q-A candidate row, executable json_extract event counts 1/1/1, 29-test function count, writer-target NONE FOUND, SHA256SUMS (all 15 MATCH, LF), twice-run byte-identical reproducer, REPORT.md fence equal to live orig-cwd stdout (LF-normalized), stdlib-only reproducer, REPORT.md NOT VERIFIED covering fixture-only / no live candidates / no catalog data / nothing accepted / no Explorer, and the first-paragraph honesty words (fixture / accepted=false / non-authoritative / sequencing) are all independently confirmed.

---

## 4. Reproducibility

| check | result |
| --- | --- |
| `reproduce_report.py` twice from `C:\tmp\P014_RO_20260914` | byte-identical. raw sha256 `b10e191ba0708bd812eb178ece53ac81707c0aa3d783db2bafd65e7444bea82a`, len 10464, 66 CR, 66 LF, 66 CRLF (Windows `print`) |
| same script twice from pkg copy | byte-identical. sha256 `d869fe47a37d5ecf626dcc503f55a2360a168ef506a0287413149cc29dedf173`, len 10976 (paths differ because `Path(__file__).parent` is pkg) |
| output vs `REPORT.md` fenced block (LF-normalized) | **equal**: 0 of 66 lines differ. `fence_equals_stdout_lf` True. Raw bytes differ only by CRLF (stdout) vs LF (markdown fence) |
| Q-B table in `P014_READONLY_REPORT.md` vs live orig-cwd rows | 19/19 byte-identical |
| stdlib only | YES (`ast`, `json`, `sqlite3`, `pathlib`; plus `from __future__ import annotations`) |
| `SHA256SUMS.txt` | 15 LF, 0 CR, ends with LF. All 15 listed digests MATCH the files at the listed `C:\tmp\P014_RO_20260914\` paths. Covers the three deliverables, the copied inputs, `DISPOSITION_FIX1.md`, and `DISPOSITION_FIX2.md`. |

---

## 5. Honesty

First paragraph of `P014_READONLY_REPORT.md` states fixture data only, recorded `accepted=false`, `authoritative` is `false`, and the `START_HERE.md:54` sequencing quote, with citations. It also states the report is not an acceptance. Prior new-3 is RESOLVED.

`REPORT.md` NOT VERIFIED exists and covers: fixture data only; no catalog writer targets; no live candidates; nothing accepted; no Explorer. Required themes are present.

Hedges upgraded to facts: the optional hash is not upgraded (still `Sha256 \| None=None` plus the “absent by design” docstring quote). Derived `check_set_purpose` is still presented as not persisted, with derivation cited. Docstrings are quoted collapsed, not paraphrased (Q-B 19/19 match live reproducer). Event-count SQL is now the command that actually returns 1/1/1. No remaining upgrade found.

---

## 6. Commands run (observed output)

Working copies: subject files copied into `C:\tmp\GROK_SCRATCH_GKP14C_20260914\pkg\`. Ledger copies for SQL: `C:\tmp\GROK_SCRATCH_GKP14C_20260914\verify\fixture-ledger*.sqlite`. Pkg copies are byte-identical to `C:\tmp\P014_RO_20260914\` originals.

### SHA256SUMS (original paths)

`SHA256SUMS.txt` bytes=1681, CR=0, LF=15, ends_with_LF=True. All 15 lines MATCH.

```
MATCH 9baed5e76de1133380126a992401a33626a4eff896247cb719c43512aeed4207 C:\tmp\P014_RO_20260914\p031_lifecycle_ledger.py
MATCH d52cab5d4a8f459107c1bd8b36ff4eb926246cc5636d469e496a37aee0b5e20a C:\tmp\P014_RO_20260914\P031_M1_SCOPE_AND_STATUS.md
MATCH b890d7fc30862e4aefb014219266a9b78ae03564cc77b53751c3cb1556c5093a C:\tmp\P014_RO_20260914\START_HERE.md
MATCH 823c7c90d18139472d5f89f8c9593b72515297136b165c9b3b71886196a63018 C:\tmp\P014_RO_20260914\fixture-ledger.sqlite
MATCH 997977f8f393907fd116cc320f3c0d03750c0ea03422cc80ff6905a130cd6a0d C:\tmp\P014_RO_20260914\fixture-ledger.restored.sqlite
MATCH 997977f8f393907fd116cc320f3c0d03750c0ea03422cc80ff6905a130cd6a0d C:\tmp\P014_RO_20260914\fixture-ledger.backup.sqlite
MATCH d22960653159a1ef1bb58cad3d8d4ad6c3d71017d0426592058711dbbb8b3d2e C:\tmp\P014_RO_20260914\fixture-status-report.json
MATCH 900ecf600292decc24d83d33cd2d362af850944ba8399f9a8fadfcb82a883512 C:\tmp\P014_RO_20260914\trial_catalog.py
MATCH d5c6d92f33e8b16579023e5cf4a1910335b0ad618d95c28714dd3fb0880eff08 C:\tmp\P014_RO_20260914\test_trial_catalog_types.py
MATCH 76c049e8dfb3d9c9330b6ee710113db0c632d9ddc99da3fcf5b74f849dfd8e1b C:\tmp\P014_RO_20260914\P013_HANDOFF.md
MATCH c75c2fd87a6e27ae55fa0c0a19c9c18f79d40cb9dfb5bf53ed560921631278ad C:\tmp\P014_RO_20260914\P014_READONLY_REPORT.md
MATCH 391ee84d9515755df36a90e0469f0d29a20b1bd7926c55d5b2ffb4b7c35b7016 C:\tmp\P014_RO_20260914\reproduce_report.py
MATCH 204f811ae07fb433e46bf98f3854a7f8d7a91942eaa97a0f0ec329186b6b1848 C:\tmp\P014_RO_20260914\REPORT.md
MATCH 07514277502cee4d44675207718a90112e8edfa4555eebbd20931e80a19244af C:\tmp\P014_RO_20260914\DISPOSITION_FIX1.md
MATCH d5431d3ab7b43422554b8f04a5a433951d8c16c4d4fccfc89733eced1ffd8f4e C:\tmp\P014_RO_20260914\DISPOSITION_FIX2.md
```

Restored and backup sqlite share one digest; primary ledger is a different digest. That is observed, not a mismatch.

Deliverable files: UTF-8 no BOM, LF-only (`P014_READONLY_REPORT.md` 13210 bytes / 89 LF; `REPORT.md` 12197 / 101 LF; `reproduce_report.py` 16174 / 447 LF).

### Read-only SQL

URI `file:///C:/tmp/GROK_SCRATCH_GKP14C_20260914/verify/fixture-ledger.sqlite?mode=ro`

```
lifecycle_current: candidate_id=QLC-20260912-demo0001 current_state=CANDIDATE last_sequence=3 source_kind=FIXTURE authoritative=0
events:
  seq=1 type=CAPTURED next=CAPTURED ts=2026-09-12T20:00:00Z writer=REGISTRAR failing_checks=[] evidence_keys=[check_set_version, evaluation_run_hash, failing_checks, source_kind]
  seq=2 type=TRIAGED  next=TRIAGED  ts=2026-09-12T20:00:01Z writer=REGISTRAR failing_checks=[]
  seq=3 type=CANDIDATE next=CANDIDATE ts=2026-09-12T20:00:02Z writer=REGISTRAR failing_checks=[]
cited command SELECT json_extract(canonical_event, '$.next_state') AS next_state, COUNT(*) FROM lifecycle_events GROUP BY 1
  CANDIDATE=1 CAPTURED=1 TRIAGED=1
old command SELECT next_state, COUNT(*) FROM lifecycle_events GROUP BY next_state
  OperationalError: no such column: next_state
restored/backup: 3 events, current CANDIDATE; digest 997977f8… (primary 823c7c90…)
```

### Reproducer

From original cwd, two runs identical (sha `b10e191ba0708bd812eb178ece53ac81707c0aa3d783db2bafd65e7444bea82a`). Compared to `REPORT.md` ` ```text ` fence: LF-normalized `diff_count 0`. `Q-B test_count: 29` and `NONE FOUND` match. Q-B table rows in `P014_READONLY_REPORT.md` equal live orig rows 19/19.

From pkg cwd, two runs identical (sha `d869fe47a37d5ecf626dcc503f55a2360a168ef506a0287413149cc29dedf173`); paths differ vs orig stdout because `__file__` parent is pkg.

### Catalog data search (read-only, no git)

Walk of `C:\tmp\P013_CONTRACT_V2_20260912`: 10022 files. Hits named `trades.parquet` / `equity.parquet` / `intents.jsonl` / `levels.parquet`: **NONE FOUND**. Other `.parquet` (144) / `.jsonl` (33) files exist elsewhere in the worktree; they are not the contract writer targets.

### Test count

`ast` on copied `test_trial_catalog_types.py`: **29** top-level `def test_*`. Parametrized defs at L179 (5 cases, decorator L169), L195 (6 members, decorator L194), L622 (3 cases, decorator L621). `29 - 3 + 14 = 40` if collected.

### Ledger reader CLI

```
python p031_lifecycle_ledger.py report <copied-sqlite>
File "...\p031_lifecycle_ledger.py", line 25, in <module>
    from mtc_contracts.execution import LifecycleEvent, LifecycleWriterClass
ModuleNotFoundError: No module named 'mtc_contracts'
exit 1
```

---

## 7. NOT VERIFIED

- Fixture data only. No live candidate, no production ledger, no accepted catalog run was in the authorized inputs. This audit did not look for live systems.
- Copied `p031_lifecycle_ledger.py report` could not be executed (`mtc_contracts` missing). The seven-item unresolved list in that file’s `_render_status_report` is source text, not a printed report for this fixture.
- Pytest was not collected or run. 29 is the `def test_*` count only.
- Worktree HEADs quoted in TASK.md were not verified (git forbidden).
- Whether the original author used this exact P020 venv interpreter is recorded in `REPORT.md` but not independently proven as the historical process; this audit did use that interpreter.
- Other parquet/jsonl files in `C:\tmp\P013_CONTRACT_V2_20260912` were not interpreted as trial-catalog writer output; only ArtifactKind filenames were treated as “files the contract would write”.
- Nothing in the subject is accepted. This audit accepts nothing.

---

GROK_P14C_VERDICT: CLEAN
