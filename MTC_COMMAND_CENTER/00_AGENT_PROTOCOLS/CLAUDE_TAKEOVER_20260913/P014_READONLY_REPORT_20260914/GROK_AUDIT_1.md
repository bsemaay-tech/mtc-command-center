# GROK_P14 detection audit — WP-P0-14 read-only report

Auditor: grok-4.6 (lane GKP14). Subject copied to `C:\tmp\GROK_SCRATCH_GKP14_20260914\pkg\` and verified there. This audit accepts nothing. No git. No network.

Authorized questions: **Q-A** (fixture ledger families / state / rejection reasons) and **Q-B** (trial-catalog contract types / refusal reasons / test count / whether catalog data exists). Fixture data only.

Interpreter used for all Python: `C:\tmp\P020_IMPL_20260912\01a0924d-2c4b-7da1-99e1-24e2a7c7685c\.venv\Scripts\python.exe` (CPython 3.12.12).

---

## 1. Scope

`P014_READONLY_REPORT.md` answers Q-A and Q-B and does not design Explorer, does not recommend product work, and does not ship product code. Sequencing is quoted from `START_HERE.md:54` as the task required.

`REPORT.md` is the execution wrapper the task also required (what was built, verbatim dump, interpreter, NOT VERIFIED, SHA256SUMS). That is in-scope for deliverable 3, not Q-A/Q-B creep.

Residual scope issue: the main report paraphrases Q-B docstrings and omits that `check_set_purpose` was derived because the fixture evidence blob does not store the key. Those are honesty/citation defects, not extra questions.

---

## 2. Citation table

Status is EQUAL / WRONG LINE / NOT FOUND against the copied files. Paths below are the subject originals; the pkg copies are byte-identical.

| citation | claimed fact | source line content | status |
| --- | --- | --- | --- |
| `fixture-status-report.json:2` | first-paragraph “scope line (`fixture-only`, `source_kind`, `authoritative`, `accepted`)” | `"actual_legacy_data": "ACTUAL/LEGACY DATA: NOT INCLUDED"` | WRONG LINE |
| `fixture-status-report.json:16` | `source_kind` is FIXTURE | `"source_kind": "FIXTURE"` (inside `derived_current_state`) | EQUAL (for `source_kind` only) |
| `fixture-status-report.json:17` | same parenthetical (`authoritative` / `accepted` / fixture-only) | `}` closing the derived-state object | WRONG LINE |
| `START_HERE.md:54` | P0-14 sequencing amendment preserved | `P0-14 \| Owner chose to defer Minimum Explorer behind core Bridge engineering with a small reproducible read-only report meanwhile. Preserve sequencing amendment; full package is not complete.` | EQUAL |
| `fixture-status-report.json:88-92` | three `unresolved_lifecycle_contracts` | L88 key; L89–L91 the three strings; L92 `]` | EQUAL (items are L89–L91) |
| SQL `SELECT * FROM lifecycle_events ORDER BY global_sequence` on `fixture-ledger.sqlite` | one candidate `QLC-20260912-demo0001`, last event `CANDIDATE` / `REGISTRAR` / `2026-09-12T20:00:02Z`, `failing_checks=[]` | independent `?mode=ro` SQL (below) | EQUAL |
| `trial_catalog.py:148` ArtifactKind | class + four enum members | `class ArtifactKind(str, Enum):` | EQUAL |
| `trial_catalog.py:72` BoundaryRefusalReason | class + `RESERVED_BOUNDARY_KEY` | `class BoundaryRefusalReason(str, Enum):` | EQUAL |
| `trial_catalog.py:278` CommitPartEntry | class | `class CommitPartEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:195` CompletedRunInput | class | `class CompletedRunInput(ContractModel):` | EQUAL |
| `trial_catalog.py:182` LineageOriginReceipt | class; fields claimed as `canonical_path_receipt_hash:Sha256` | `class LineageOriginReceipt(ContractModel):`; field at L192 is `canonical_path_receipt_hash: Sha256 \| None = None` | EQUAL as class line; fields column is false |
| `trial_catalog.py:465` NestedSchemaColumnEntry | class | `class NestedSchemaColumnEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:122` ProvisionalBoundaryPayload | class | `class ProvisionalBoundaryPayload(ContractModel):` | EQUAL |
| `trial_catalog.py:484` PublishedViewSchemaDocumentV1 | class | `class PublishedViewSchemaDocumentV1(ContractModel):` | EQUAL |
| `trial_catalog.py:78` ReservedBoundaryKeyRefusal | class | `class ReservedBoundaryKeyRefusal(Exception):` | EQUAL |
| `P014_READONLY_REPORT.md` `trial_catalog.py:237` RunCellDimensionsReceipt | alias assignment | L237 is the comment `# Compatibility name...`; assignment is L238 | WRONG LINE |
| `REPORT.md` verbatim `trial_catalog.py:1` RunCellDimensionsReceipt | alias assignment | L1 is the module docstring | WRONG LINE |
| `trial_catalog.py:222` RunCellDimensionsReceiptV1 | class | `class RunCellDimensionsReceiptV1(ContractModel):` | EQUAL |
| `trial_catalog.py:246` RunEnvelopeV1 | class | `class RunEnvelopeV1(ContractModel):` | EQUAL |
| `trial_catalog.py:398` SchemaColumnEntry | class | `class SchemaColumnEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:302` SelectedArtifactCommitEntry | class | `class SelectedArtifactCommitEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:294` SelectedArtifactMemberEntry | class | `class SelectedArtifactMemberEntry(ContractModel):` | EQUAL |
| `trial_catalog.py:157` SelectedArtifactPayloadReceipt | class | `class SelectedArtifactPayloadReceipt(ContractModel):` | EQUAL |
| `trial_catalog.py:175` SinkCapabilityClass | class | `class SinkCapabilityClass(str, Enum):` | EQUAL |
| `trial_catalog.py:137` TerminalTrialReceipt | class | `class TerminalTrialReceipt(ContractModel):` | EQUAL |
| `trial_catalog.py:168` WriterAdapterId | class | `class WriterAdapterId(str, Enum):` | EQUAL |
| `accepted=false` in first paragraph | fixture not accepted | no `accepted` key in `fixture-status-report.json`; true at `P031_M1_SCOPE_AND_STATUS.md:718` (`- \`accepted\`: \`false\``) which is **not cited** | NOT FOUND at the cited JSON lines |
| `fixture-only` as a JSON field | first paragraph | JSON has `"scope": "FIXTURE LEDGER DATA"` at L82 and `source_kind=FIXTURE`; no `fixture_only` key | NOT FOUND |
| `29` tests | `test_trial_catalog_types.py contains 29 tests` | 29 top-level `def test_*` via ast | EQUAL as function count; uncited in the main report |
| event counts CAPTURED/TRIAGED/CANDIDATE = 1 | Q-A list | SQL `next_state` counts | EQUAL; uncited in the event-count subsection |
| catalog data NONE FOUND | writer-named targets under the P013 worktree | independent walk (below): zero `trades.parquet` / `equity.parquet` / `intents.jsonl` / `levels.parquet` | EQUAL |

Independent SQL (copy `C:\tmp\GROK_SCRATCH_GKP14_20260914\verify\fixture-ledger.sqlite?mode=ro`):

- `lifecycle_current`: one row `QLC-20260912-demo0001`, `current_state=CANDIDATE`, `last_sequence=3`, `source_kind=FIXTURE`, `authoritative=0`.
- three events, `next_state` counts CAPTURED=1, TRIAGED=1, CANDIDATE=1.
- latest event global_sequence=3, `event_type=CANDIDATE`, timestamp `2026-09-12T20:00:02Z`, writer `REGISTRAR`, `failing_checks=[]`.
- evidence keys are `check_set_version`, `evaluation_run_hash`, `failing_checks`, `source_kind`. **`check_set_purpose` is absent** from stored evidence; SQL reads it as null. Latest event type `CANDIDATE` also derives to `None` under the reader’s `_check_set_purpose`. Restored and backup ledgers have the same 3 events / one CANDIDATE row.

---

## 3. Findings

| # | severity | file:line | what is wrong | why it matters |
| --- | --- | --- | --- | --- |
| 1 | CORRECTION | `REPORT.md:44` (verbatim fence L44 / dump line 23) vs live `reproduce_report.py` stdout | Claimed “verbatim” dump is not verbatim. Live stdout fields cell is `canonical_path_receipt_hash:Sha256 \| None=None`; the pasted row drops `\| None=None`, which also collapses a markdown column. 46/47 lines otherwise match when the script is run from `C:\tmp\P014_RO_20260914`. | Task required a paste of reproducer output. The one edited cell is the nullable hash field. |
| 2 | CORRECTION | `P014_READONLY_REPORT.md:31` and `REPORT.md:44`; source `trial_catalog.py:192` | `LineageOriginReceipt.canonical_path_receipt_hash` reported as required `Sha256`. Source is `Sha256 \| None = None`. The class docstring says the hash “is absent by design for screening”. | Hedge upgraded to a required identity field. |
| 3 | CORRECTION | `P014_READONLY_REPORT.md:3-4` citing `fixture-status-report.json:2` and `:17` | Those lines are `actual_legacy_data` and a closing brace. They do not contain `fixture-only`, `authoritative`, or `accepted`. `accepted` is **not in the JSON at all**. True `accepted: false` is `P031_M1_SCOPE_AND_STATUS.md:718`. `authoritative: false` is JSON L10. Scope string is JSON L82. | Invented/wrong citations for the honesty paragraph. |
| 4 | CORRECTION | `P014_READONLY_REPORT.md:36` `trial_catalog.py:237`; `REPORT.md` dump `trial_catalog.py:1` | Alias `RunCellDimensionsReceipt = RunCellDimensionsReceiptV1` is L238. L237 is a comment. L1 is the module docstring. Reproducer hardcodes `mod.body[0].lineno`. | Wrong line. The P014 “fix” is still off by one. |
| 5 | CORRECTION | `P014_READONLY_REPORT.md:23-45` Q-B purpose column | Task asked for purpose from the docstring. Several purposes are paraphrased, not quoted. Worst: `TerminalTrialReceipt` “reduced to what this slice may consume” becomes “preserved by slice”; `LineageOriginReceipt` drops the “absent by design” sentence. | Meaning changes; looks like a quote because a `file:line` sits next to it. |
| 6 | CORRECTION | `P014_READONLY_REPORT.md:17-20` vs `p031_lifecycle_ledger.py:1259-1267` | Unresolved list is the 3-item JSON snapshot. Copied reader source `_render_status_report` encodes **seven** contracts (adds REJECTED FAILED-GATE PURPOSE, ADMISSION WITHHELD CAPACITY TARGET, DEPLOYMENT REFRESH ENVELOPE, EVALUATION RUN CANDIDATE SCOPE). Reader CLI cannot be executed here (`ModuleNotFoundError: mtc_contracts`). Report does not say the reader was not run. | Task asked for the list the reader prints. Snapshot and current reader source disagree; that disagreement is hidden. |
| 7 | CORRECTION | `P014_READONLY_REPORT.md:10` `check_set_purpose` = `None`; `reproduce_report.py:89-93` | Stored evidence has no `check_set_purpose` key. Reproducer derives it from event shape (comment: “not persisted in this fixture evidence”). Main report presents `None` as a ledger field. | Missing key reported as an explicit null fact. |
| 8 | CORRECTION | `REPORT.md:17-18` | Interpreter recorded as `` `python` (CPython, standard library only) ``. Task required the interpreter used. Specified interpreter is the P020 venv `python.exe` (3.12.12). | Reproducer run is not pinned to a path. |
| 9 | CORRECTION | `P014_READONLY_REPORT.md:13-15` and `:49` | Event counts `1/1/1` and `29` tests have no `path:line` and no command. 29 is equal to ast `def test_*` count. | Unpriced numbers in the report the task said must be traceable. |
| 10 | NIT | `P014_READONLY_REPORT.md` L1 BOM; last byte CRLF. `REPORT.md` same. | UTF-8 BOM + one trailing CR. `SHA256SUMS.txt` is pure LF and hashes these bytes as-is, so the hashes still MATCH. | Harmless for hashing; not LF-clean markdown. |
| 11 | NIT | `reproduce_report.py` imports | Stdlib only (`ast`, `json`, `sqlite3`, `pathlib`, `collections`). Task named the first four; `collections.Counter` is extra but still stdlib. | Not a third-party dependency. |
| 12 | NIT | `test_trial_catalog_types.py` | 29 `def test_*`. Three are parametrized (5 + 6 + 3 cases). Pytest collection would be 40 if the suite imported. Suite was not collected (`mtc_contracts` missing). | 29 is defensible as “tests in the file”; collection count is higher. |

No BLOCKING finding: Q-A candidate row, event counts, 29-test function count, writer-target NONE FOUND, SHA256SUMS (all 13 MATCH, LF), twice-run byte-identical reproducer, first-paragraph fixture/non-authoritative/`accepted=false`/sequencing words, and REPORT.md NOT VERIFIED covering fixture-only / no live candidates / no catalog data / nothing accepted / no Explorer are all present and independently confirmed.

---

## 4. Reproducibility

| check | result |
| --- | --- |
| `reproduce_report.py` twice from `C:\tmp\P014_RO_20260914` | byte-identical. raw sha256 `0c523eec63b20f3659cae7a1b06a5ba7a81bb58a0c29ba46ad9bb5df86931605`, len 8662, 47 CR, 47 LF (Windows `print` CRLF) |
| same script twice from pkg copy | byte-identical. sha256 `fe959dabfdc0123af19decd897c653d2d5c79f2e5bc738a719f547ba31c4a0f9` (paths differ because `Path(__file__).parent` is pkg) |
| output vs `REPORT.md` fenced block (LF-normalized) | **not equal**: 1 of 47 lines differs (LineageOriginReceipt fields; finding 1) |
| stdlib only | YES |
| `SHA256SUMS.txt` | 13 LF, 0 CR, ends with LF. All 13 listed digests MATCH the files at the listed `C:\tmp\P014_RO_20260914\` paths. Covers the three deliverables and the copied inputs. |

---

## 5. Honesty

First paragraph of `P014_READONLY_REPORT.md` does state fixture-only, non-authoritative, `accepted=false`, and sequencing preserved. The **words** are there. The **citations** under them are wrong (findings 3).

`REPORT.md` NOT VERIFIED exists and covers: fixture data only; no catalog writer targets; no live/`accepted=true`/authoritative current-state; no Explorer. Required themes are present.

Hedges upgraded to facts: optional `canonical_path_receipt_hash` (finding 2); `accepted=false` pinned to JSON lines that do not contain it (finding 3); derived/missing `check_set_purpose` shown as a stored None (finding 7); paraphrased docstrings (finding 5).

---

## 6. Commands run (observed output)

Working copies: subject files copied into `C:\tmp\GROK_SCRATCH_GKP14_20260914\pkg\`. Ledger copies for SQL: `C:\tmp\GROK_SCRATCH_GKP14_20260914\verify\fixture-ledger*.sqlite`.

### SHA256SUMS (original paths)

`SHA256SUMS.txt` bytes=1461, CR=0, LF=13, ends_with_LF=True. All 13 lines MATCH. Representative:

```
1 MATCH 9baed5e76de1133380126a992401a33626a4eff896247cb719c43512aeed4207 p031_lifecycle_ledger.py
4 MATCH 823c7c90d18139472d5f89f8c9593b72515297136b165c9b3b71886196a63018 fixture-ledger.sqlite
5 MATCH 997977f8f393907fd116cc320f3c0d03750c0ea03422cc80ff6905a130cd6a0d fixture-ledger.restored.sqlite
6 MATCH 997977f8f393907fd116cc320f3c0d03750c0ea03422cc80ff6905a130cd6a0d fixture-ledger.backup.sqlite
11 MATCH 8220f233bb9dfbe7d4a518bd9095c2a0c7ff31bb35be5212011280d74ae3e071 P014_READONLY_REPORT.md
12 MATCH 00f904ecd946875d6e7d064870fb470ad7503f1d10bf99b477f8158873ee2dc0 reproduce_report.py
13 MATCH 94c7ff336d2637642a3267c3c5f960651c7e16e6ea20cad3f39f7363438b0fc0 REPORT.md
```

Restored and backup sqlite share one digest; primary ledger is a different digest. That is observed, not a mismatch.

### Read-only SQL

URI `file:///C:/tmp/GROK_SCRATCH_GKP14_20260914/verify/fixture-ledger.sqlite?mode=ro`

```
lifecycle_current: candidate_id=QLC-20260912-demo0001 current_state=CANDIDATE last_sequence=3 source_kind=FIXTURE authoritative=0
events:
  seq=1 type=CAPTURED next=CAPTURED ts=2026-09-12T20:00:00Z writer=REGISTRAR failing_checks=[] evidence_keys=[check_set_version, evaluation_run_hash, failing_checks, source_kind]
  seq=2 type=TRIAGED  next=TRIAGED  ts=2026-09-12T20:00:01Z writer=REGISTRAR failing_checks=[] check_set_version=fixture-worthiness.v1
  seq=3 type=CANDIDATE next=CANDIDATE ts=2026-09-12T20:00:02Z writer=REGISTRAR failing_checks=[]
event_counts_per_next_state: CAPTURED=1 TRIAGED=1 CANDIDATE=1
restored/backup: 3 events, current CANDIDATE
```

### Reproducer

From original cwd, two runs identical (sha `0c523eec63b20f3659cae7a1b06a5ba7a81bb58a0c29ba46ad9bb5df86931605`). Compared to `REPORT.md` ` ```text ` fence (file lines 22–68): `total_diff_lines 1` (LineageOriginReceipt fields). `Q-B test_count: 29` and `NONE FOUND` match.

### Catalog data search (read-only, no git)

Walk of `C:\tmp\P013_CONTRACT_V2_20260912`: 10022 files. Hits named `trades.parquet` / `equity.parquet` / `intents.jsonl` / `levels.parquet`: **NONE FOUND**. Same NONE FOUND under `MTC_COMMAND_CENTER\contracts`. Other `.parquet`/`.jsonl`/`.csv`/`.tsv` files exist elsewhere in the worktree (backtest history, triage, docs); they are not the contract writer targets.

### Test count

`ast` on copied `test_trial_catalog_types.py`: **29** top-level `def test_*`.

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
- Whether the original author used this exact P020 venv interpreter is not recorded in `REPORT.md`.
- Other parquet/jsonl/csv files in `C:\tmp\P013_CONTRACT_V2_20260912` were not interpreted as trial-catalog writer output; only ArtifactKind filenames were treated as “files the contract would write”.
- Nothing in the subject is accepted. This audit accepts nothing.

---

GROK_P14_VERDICT: CORRECTIONS_NEEDED
