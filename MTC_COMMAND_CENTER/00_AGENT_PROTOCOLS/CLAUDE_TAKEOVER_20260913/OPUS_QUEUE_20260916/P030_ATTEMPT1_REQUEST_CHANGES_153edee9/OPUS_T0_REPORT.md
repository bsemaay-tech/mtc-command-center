# T0 review — WP-P0-30 Shape-B archive exporter, candidate `153edee97c008b36548cfb0c5bfaf5d7615a91d1`

Reviewer: exact `claude-opus-5`, xhigh — Wednesday 2026-09-16 slot. Fresh independent T0: no delegation, no
sub-agents, no other session resumed. One output file. RED-arm scratch copies under `C:/tmp/OPUS_P030_SCRATCH/`.
Every number below was computed by me on this host; nothing is carried over from a record.

Git commands used (read-only, no `status`/`diff`/`add`/`commit`/`checkout`): `rev-parse`, `show <rev>:<path>`,
`show --numstat <rev>`, `rev-list`, `check-attr`, `config --get`.

---

## 1. Verified identities (COMPUTED)

| Item | Value |
|---|---|
| `git -c safe.directory=* -C C:/tmp/P030_INTEGRATION_20260913 rev-parse HEAD` | `153edee97c008b36548cfb0c5bfaf5d7615a91d1` — matches the pin |
| sha256 `p030_archive_exporter.py` (worktree bytes) | `7571bafc053725ce6a0b5aee4527176c161e82a95e28a0ca53f65868417085fe` (12 608 B, 340 lines, **LF**) |
| sha256 `p030_archive_exporter.py` (blob `153edee9:`) | `7571bafc053725ce6a0b5aee4527176c161e82a95e28a0ca53f65868417085fe` — worktree **equals** blob |
| sha256 `check_p030_archive_exporter.py` (worktree bytes) | `8195157c490e3be6da5069ac6a5f9ff40e66001f26618bb2753f144c238024c5` (21 074 B, 466 lines, **CRLF**) |
| sha256 `check_p030_archive_exporter.py` (blob `153edee9:`) | `b0f0112a105094a4e2d177372d3542812b977c86f92a9044b5c7611e7286fe55` (20 608 B, 466 lines, LF) — blob authoritative |
| Commits `f42fd540..153edee9` | exactly two: `daf6a43b` (+323 exporter, +263 checker) and `153edee9` (**+19/−2** exporter, +203 checker) |
| Files touched since base `f42fd540` | exactly `p030_archive_exporter.py`, `check_p030_archive_exporter.py`. `market_data_collector.py`, the adapter and the contracts module are untouched |
| Interpreter | `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` → `Python 3.12.12 (main, Jan 27 2026) [MSC v.1944 64 bit (AMD64)]` |

Line arithmetic checks out for `+19/−2`: 323 − 2 + 19 = 340. (Two records state different deltas — finding 6.)

---

## 2. Mandated check runs

cwd for every run: `C:/tmp/P030_INTEGRATION_20260913`. Command form:
`<pinned python> <check>.py` (these checks are `unittest.main()` scripts, not pytest collectors; no
`-p no:cacheprovider` applies, and no `.pytest_cache` was created).

**`check_p030_archive_exporter.py` — OK (exit 0)**

```
Ran 20 tests in 0.362s

OK
D-13 RED RAW REFUSAL: prefix record is not canonical JSONL
D-13 GREEN EXPORTED CAPTURE: PASS
```

**`check_market_data_collector.py` — PASS (exit 0)**

```
REINTRODUCTION MUTANT (persisted WS-only filter removed): DETECTED
REINTRODUCTION MUTANT (persisted timestamp coerced): DETECTED
REINTRODUCTION MUTANT (persisted grid validation removed): DETECTED
REINTRODUCTION MUTANT (eth_account import): DETECTED
REINTRODUCTION MUTANT (os.environ read): DETECTED
REINTRODUCTION MUTANT (order call): DETECTED
NETWORK ATTEMPTS: 0
MARKET DATA COLLECTOR CHECK: PASS
```

**`check_p030_market_data_contracts.py` — PASS (exit 0)**

```
PROVENANCE MUTANT (dataset_content_hash): DETECTED
IDENTITY MUTANT (omitted predecessor): DETECTED
EVENT MUTANT (four-family allowlist): DETECTED
PROVENANCE MUTANT (file-hashes only): DETECTED
EVENT DETAIL COLLISION/TYPE MUTANTS: DETECTED
TYPE/CANONICALIZATION REFUSALS: PASS
NETWORK ATTEMPTS: 0
P030 MARKET DATA CONTRACTS CHECK: PASS
```

**`check_p030_closed_partition_backup_adapter.py` — FAILED on the first run (exit 1), OK on re-run (exit 0)**

First run, inherited `%TEMP%` (`C:\Users\BarışSemaay\AppData\Local\Temp\opus_p030`):

```
FAIL: test_isolated_config_redirect_after_check_never_reaches_restore (…) (defect='duplicate_backup_root')
  File "…\check_p030_closed_partition_backup_adapter.py", line 840, in redirect_after_check
    self.assertEqual(raw.count(anchor), 1)
AssertionError: 0 != 1
Ran 44 tests in 6.147s
FAILED (failures=1)
```

Re-run with `TMP=TEMP=C:\tmp\OPUS_P030_SCRATCH\tmp` (ASCII path), same commit, same interpreter:

```
Ran 44 tests in 2.998s

OK
```

Diagnosed to the byte, **not** a candidate defect and not a defect in a file this candidate touches:
`check_p030_closed_partition_backup_adapter.py:835` builds the anchor with `json.dumps(configured_root)`
(`ensure_ascii=True` → `\u0131`), while the adapter writes the isolated config with
`json.dumps(..., ensure_ascii=False, indent=2)` at `p030_closed_partition_backup_adapter.py:594-603`
(literal `ı`). Any host whose temp path contains a non-ASCII character fails that one subtest. See finding 8.

---

## 3. Conformance table — Shape B

Promise sources: `P030_BRIDGE_DESIGN_CHOICE_20260914.md` §B, and the adapter/contract rules the exporter must
agree with. All line numbers are HEAD `153edee9` blob lines (= worktree lines for the exporter).

| Shape-B promise | Where I checked | Verdict |
|---|---|---|
| Collector never mutated; source read exactly once as bytes | `p030_archive_exporter.py:127-142` (`_read_source_once`), instrumented export: **1** open of the source partition for the whole call (target 2, own source file 1, receipt 1); source sha256 unchanged after export | **EQUAL** |
| Re-identification goes through the contracts module (no home-grown ids) | `:198` `producer_payload_hash(payload)`, `:212` `observation_id(observation)` → `p030_market_data_contracts.py:187-198`, `:219-222`. The exporter's own regexes `:64-66` are validators only, never id producers | **EQUAL** |
| Collector bare-hex ids accepted, wrong prefixed ids refused | `:202-206`, `:216-220`; collector emits bare hex from a different digest domain (`market_data_collector.py:66-81` `HashContract.digest` over the raw wire fields) | **EQUAL** (see limitation L-1) |
| Output canonical: sorted keys, LF, one row per line | `:274-286` `json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(",",":"), allow_nan=False) + "\n"` — byte-identical to the adapter's canonical form at `p030_closed_partition_backup_adapter.py:197-208` | **EQUAL** |
| Exclusive create + byte re-read equals what was written | `:293-307` (`open("xb")`, `read_bytes()`, compare) | **EQUAL** (but see finding 1 for what survives a failure) |
| Receipt binds source digest → target digest → row counts → dataset hash | `:309-331`; measured: `source_sha256` == sha256(source bytes) **True**, `exported_sha256` == sha256(target bytes) **True**, counts 2/2/2 consistent, and `dataset_content_hash` **recomputed by me from the target bytes** matches the receipt | **EQUAL** |
| Whole-second UTC `Z` timestamps, as the adapter requires | exporter `:97-113` vs adapter `:131-139`. 12-stamp matrix: identical accept/refuse on 11; the exporter is **stricter** on one (` 2026-09-14T00:00:00Z` with a leading space: exporter refuses, adapter accepts). No stamp is accepted by the exporter and refused by the adapter | **EQUAL (exporter ≥ adapter)** |
| Id domains the adapter enforces | exported `observation_id` matches `^p030obs-v1:[0-9a-f]{64}$` (adapter `:48`, `:212-213`); `producer_payload_hash` matches `p030payload-v1:` (contracts `:207-208`) | **EQUAL** |
| Slice-level contract rules (window, duplicates, descriptor) | `:290` `dataset_content_hash(_descriptor(rows), rows)` → contracts `:334-380`; `_descriptor` `:226-241` derives window from min/max of the rows | **EQUAL** |
| No network, no subprocess | imports are stdlib + the contracts module only (`:1-24`); export ran to completion with `socket.socket`, `socket.create_connection` and `subprocess.Popen` replaced by raising stubs — **0 attempts** | **EQUAL** |
| No writes outside the target path + receipt | full-tree diff around one export: created exactly `export-root/nested/out.jsonl` and `export-root/nested/out.jsonl.p030export.json`; nothing else created or changed (target parent dirs are created by `:294`) | **EQUAL** |
| **Source confined to `source_root`** | `:116-124` `_source_rel` uses `.absolute()` only — no `resolve()`, no symlink/junction refusal; the adapter enforces both (`:142-165`, `:168-178`, `:239-240`) and has three dedicated tests for it | **DIFFERENT — finding 2** |
| **Nothing consumable is left behind by a refusal** | `:293-339`: the target is created and fully written before the re-read and before the receipt; no staging name, no rename | **DIFFERENT — finding 1** |

---

## 4. Refusal-code table

Both counts reproduced **from the bytes** with an AST walk over each revision's blobs (`_refuse("code"…)` /
`ExportRefused("code"…)` on the exporter side; `assertEqual(exc.code, "X")` / `self._refused("X", …)` on the
checker side), not read out of any record:

| Revision | Distinct `ExportRefused` codes | Codes with a named negative test | Missing |
|---|---|---|---|
| `daf6a43b` (base) | **16** | **5** | **11** — matches Gemini's count exactly |
| `153edee9` (HEAD) | **16** | **16** | **0** — matches the Lead's claim |

The code set is identical at both revisions; O9FIX added no code, only the K-03 site (`:112`) and the wrapping.

| # | Code | Trigger (raised at, HEAD) | Negative test | My RED probe |
|---|---|---|---|---|
| 1 | `invalid_timestamp` | `:99,:103,:108` non-`Z`/unparseable, `:112` sub-second | `:306,:311` (6 arms) | `.500Z`, `.000001Z`, `.5Z` → refused "must use whole seconds"; `+00:00`, no-`Z`, `not-a-time`, `ZZ`, `-00:00Z`, `00:00:60Z`, int → refused. **No target, no receipt** in every arm |
| 2 | `source_outside_root` | `:122` | `:321` | fires for a sibling root; **does not fire** for `..` traversal or a junction — finding 2 |
| 3 | `source_unreadable` | `:135` | `:329` | missing file → refused |
| 4 | `short_read` | `:137` size mismatch, `:141` no trailing LF | `:336,:348` | both arms refused |
| 5 | `empty_partition` | `:139`, `:272` | `:196` | zero-byte source → refused |
| 6 | `source_line_invalid` | `:154` decode, `:158` non-object, `:165` non-finite walk | `:182,:362` | `1e999`, `-1e999` nested, `NaN`, `Infinity`, `-Infinity`, `1e999` inside a real collector row, lone-CR inside a line → all refused, **no target** |
| 7 | `source_line_noncanonical` | `:179`, `:183` | `:369` | `{"open": 1}` (spacing) → refused |
| 8 | `source_fields_mismatch` | `:191` | `:378` | extra field → refused |
| 9 | `contract_refused` | `:200` payload, `:214` observation, `:292` slice | `:387,:396,:403` | non-decimal `open`, duplicate rows, `bar_close_time == bar_open_time`, `PROXY` track with null `proxy_source` → all `ExportRefused("contract_refused")`, **no target** |
| 10 | `identity_mismatch` | `:204,:206,:218,:220` | `:259` | prefixed id disagreeing with bytes → refused |
| 11 | `mixed_dataset_descriptor` | `:240` | `:414` | second row with another venue → refused |
| 12 | `target_exists` | `:258` pre-check, `:299` `FileExistsError` | `:168` | occupied target → refused |
| 13 | `receipt_exists` | `:261`, `:337` | `:422` | pre-existing receipt → refused, target not created |
| 14 | `target_unwritable` | `:301` | `:438` | `Path.open` denied → refused, no target. **Mid-write `OSError` → refused but a truncated target survives** — finding 1 |
| 15 | `target_verify_failed` | `:305`, `:307` | `:219` | re-read differs → refused, **full-size target survives, no receipt** — finding 1 |
| 16 | `receipt_unwritable` | `:339` | `:449` | receipt open denied → refused, **full-size target survives, no receipt** (the test itself asserts this at `:450`) — finding 1 |

**Can K-01, K-02 or K-03 produce an EXPORTED row?** No. Every arm of all three refuses with the right code and
leaves no target and no receipt on disk. Independent RED arm (HEAD checker against the `daf6a43b` exporter,
scratch copy, worktree modules on `PYTHONPATH`) reproduces the three defects the delta fixes and nothing else:

```
ERROR: test_contract_refused_from_slice_validation      -> p030_market_data_contracts.ContractRefused: duplicate observation_id in dataset   (K-02: raw leak)
ERROR: test_source_line_invalid_for_overflow_and_nan_literals -> ValueError: non-finite JSON number                                          (K-01: raw leak)
FAIL : test_invalid_timestamp_refusals_including_sub_second   -> AssertionError: ExportRefused not raised                                     (K-03)
Ran 20 tests in 0.222s
FAILED (failures=1, errors=2)
```

The other 17 tests pass against the old exporter, so the new tests are load-bearing for exactly those three.

---

## 5. D-13 drill evidence

cwd `C:/tmp/P030_INTEGRATION_20260913`, pinned interpreter.

**The check goes through the real adapter, not a re-implementation.** `check_p030_archive_exporter.py:15`
imports `capture_stable_prefix` from `p030_closed_partition_backup_adapter`; at runtime I resolved it to
`C:\tmp\P030_INTEGRATION_20260913\p030_closed_partition_backup_adapter.py` and the collector partition is built
by the real `market_data_collector.MonthlyArchive.append_bar` through the real
`check_market_data_collector` fixtures (`:12-13`, `:23-49`).

**RED half (real):**

```
raw collector partition: adapter REFUSED -> prefix record is not canonical JSONL
raw line 0 head : b'{"observation_id":"251c62b69d85cef4ccd7b3b7d3366ad9352acb008d0075a7a8875f2e0cf8a884","producer_payload_hash":"9afee8eb53…'
exported line 0 : b'{"bar_close_time":1769906700000,"bar_open_time":1769905800000,"close":"104","env_lineage_id":"fixture-lineage","high":"1…'
```

The checker accepts either of two RED messages at `:78-84`. That is **not** a looseness defect: the Shape-B
design note itself specifies the RED outcome as `"observation_id must match p030obs-v1 identity"` *or*
`"prefix record is not canonical JSONL"` (`P030_BRIDGE_DESIGN_CHOICE_20260914.md` §B, D-13 GREEN paragraph).
The message that actually fires on this fixture is deterministic: the bare id is reached only after the
canonical-form check, so it is always `prefix record is not canonical JSONL`.

**GREEN half depends on the export** — I mutated the exported bytes in scratch and re-fed the real adapter:

```
GREEN (unmutated export)                              -> adapter ACCEPTED (record_count 2, dataset hash matches receipt)
MUTATION 'pretty-printed (non-canonical spacing)'     -> adapter REFUSED -> prefix record is not canonical JSONL
MUTATION 'key order unsorted'                         -> adapter REFUSED -> prefix record is not canonical JSONL
MUTATION 'CRLF line endings'                          -> adapter REFUSED -> prefix record is not canonical JSONL
MUTATION 'observation_id stripped of p030obs-v1'      -> adapter REFUSED -> observation_id must match p030obs-v1 identity
MUTATION 'one field value edited (close)'             -> adapter ACCEPTED
```

The last line is an **adapter** property, not an exporter defect: `capture_stable_prefix` takes
`dataset_content_hash` as a caller argument and only format-checks it (`:245-249`); it never recomputes it from
the rows. So D-13 GREEN proves *canonical form and id domain*, not *content binding*. Recorded in NOT VERIFIED.

Supporting behaviour I measured: a CRLF source partition is accepted and normalised to LF output (correct for
Shape B); a lone `\r` inside a line is refused (`source_line_invalid`); re-exporting an already exported
partition is byte-identical and yields the same `dataset_content_hash`.

---

## 6. Findings

### REQUIRED

**Finding 1 — a refusal raised after the target is created leaves a consumable partition on disk; a real mid-write failure leaves a *truncated* one that the adapter accepts.**
`p030_archive_exporter.py:293-307` writes the full target under its final name, then verifies, then
`:332-339` writes the receipt. Three refusal paths run after the target exists — `target_unwritable` (`:301`),
`target_verify_failed` (`:305,:307`), `receipt_unwritable` (`:339`) — and none of them removes or neutralises
the file. RED probe (scratch, `Path.open` wrapped so the target's `write` stores half the bytes and then raises
`OSError(28, "No space left on device")` — the ENOSPC/IO shape the code catches at `:300`):

```
refusal      : ExportRefused(target_unwritable) target partition is unwritable
target exists: True
target bytes : 616 (a complete export is 1232)
ends with LF : True
tail         : b'TIVE","venue":"HYPERLIQUID","venue_seq":null,"volume":"13"}\n'
receipt      : False
adapter      : ACCEPTED the truncated leftover
```

The leftover is one complete canonical row out of two, terminated with LF, so the real
`capture_stable_prefix` consumes it and stamps its own stable receipt over the halved partition:

```
truncated leftover bytes: 616
stable receipt record_count: 1
stable receipt last_observation_id: p030obs-v1:4d9dfaf05e808200630...
state: stable_prefix | high_water_bytes: 616
```

A silently halved archive partition, from a call that refused. The `target_verify_failed` and `receipt_unwritable` paths
leave the full 1232-byte file with no receipt (the checker asserts exactly that at `:450`
`self.assertTrue(target.exists())`). This is the brief's escalation trigger: a refusal path that leaves a
partial target.
Fix that respects the package invariant "no delete code path at all"
(`MTC_COMMAND_CENTER/tools/opsa/opsa_common.py:5-13`): write to a staging name the archive namespace does not
accept (e.g. `<target>.p030partial`), do the byte re-read and the receipt against that, and `os.replace` it
onto the final name only once both succeed — `os.replace` is a write, not a delete, and the adapter's own
`atomic_write_bytes` already uses that shape. Then `assertFalse(target.exists())` becomes true on every
refusal path, and the existing tests at `:439`/`:450` can be tightened to say so.

**Finding 2 — `source_root` containment is fail-open: `..` traversal and junction/symlink components are accepted, and the receipt records a path the adapter's own rule refuses.**
`p030_archive_exporter.py:116-124` computes the receipt's `source_path` with `Path(...).absolute()` and
`relative_to`, then refuses only when `relative_to` raises. `.absolute()` collapses neither `..` nor links.
Two RED probes:

```
declared source_root : …\escape\collector-root\bars
path handed in       : …\escape\collector-root\bars\..\..\outside\2026-02.jsonl   (bytes live OUTSIDE the root)
EXPORTER : ACCEPTED — receipt source_path = '../../outside/2026-02.jsonl'
adapter  : _canonical_relative_posix REFUSES that source_path -> "source_path must be a canonical relative POSIX path"
```

```
declared source_root : …\junc\root          ('link' is a real NTFS junction to …\junc\outside)
path handed in       : …\junc\root\link\2026-02.jsonl
EXPORTER : ACCEPTED — receipt source_path = 'link/2026-02.jsonl'      <- looks clean, bytes came from outside the root
ADAPTER  : _refuse_source_links REFUSES the same path -> "source JSONL must not be a symlink or junction component"
ADAPTER  : capture_stable_prefix REFUSES the same source
```

Byte count of the guards: the exporter has **0** `resolve()`/`is_symlink`/`is_junction` lines; the adapter has
16 (`:168-178` `_refuse_source_links`, `:239-241` resolve-after-validate, `:142-165`
`_canonical_relative_posix`, applied again to the persisted `source_path` at `:316`), and the adapter's suite
carries three dedicated tests for it (`test_capture_and_prebackup_refuse_real_junction_ancestor`,
`test_capture_refuses_caller_supplied_symlink_before_resolution`,
`test_capture_refuses_intermediate_symlink_or_junction_component`). The contracts module applies the same
rule to persisted partition paths (`p030_market_data_contracts.py:434-444`). So this is not a bar I invented —
it is the bar the two modules the exporter must agree with already enforce on the same field, and the exporter
is the one component that does not. Consequence: a receipt whose `source_path` either escapes the declared
root in plain sight or hides the escape behind a junction, i.e. a false provenance binding in the artefact
whose entire job is provenance binding. Fix: resolve both paths, refuse any link/junction component the way
`_refuse_source_links` does, and put the result through a canonical-relative-POSIX check before it is
persisted; all three are read-only checks, so the no-delete invariant is untouched.

### NIT

**Finding 3 (K-06, CONFIRMED).** `check_p030_archive_exporter.py:362` pins three arms (overflow, nested
overflow, NaN literal) with the single alternation `"non-finite|not parseable"`. The code assertion is exact
(`source_line_invalid`), so a regression that re-classified `1e999` as unparseable JSON would still pass. The
two messages differ by design (`:165-167` vs `:154-156`) and my probe shows which arm produces which, so
splitting the assertion is mechanical. The brief says this is the one change I may ask for — I do.

**Finding 4 (K-07, CONFIRMED, direction as the Lead adjudicated).** Computed both forms:
`check_p030_archive_exporter.py` blob = 20 608 B LF → `b0f0112a…`; the worktree checkout = 21 074 B CRLF →
`8195157c…`. The O9FIX packet's `SHA256SUMS.txt` records `8195157c…` (the checkout), while its own
`subject/check_p030_archive_exporter_HEAD.py` entry records `b0f0112a…` (the blob). Note for the record: the
*earlier* lane file `P030_EXPORTER_CANDIDATE_20260914/SHA256SUMS.txt` is **correct** — both of its digests
(`1389c1aa…`, `a47d2df5…`) are the LF blob hashes at `daf6a43b`, which I recomputed. So K-07 applies to the
O9FIX packet only, not to the candidate lane record.

**Finding 5 — the receipt's `exporter_sha256` is checkout-dependent, so it is not reproducible from the blob
on a fresh clone.** `p030_archive_exporter.py:315` hashes `Path(__file__).read_bytes()`. This repository has
`core.autocrlf=true`, and the exporter is `text: auto, eol: unspecified` (`git check-attr`), so a fresh
checkout on Windows materialises it as CRLF: the receipt would then record `df64dcdc…` instead of the blob's
`7571bafc…` (both computed). Today the file happens to be LF in this worktree — its sibling checker is already
CRLF here, which is exactly the accident this depends on. The checker cannot catch it (`:130-133` hashes the
same working file). `.gitattributes:11-15` already pins other hash-bearing paths with `text eol=lf` for
precisely this reason; adding `p030_archive_exporter.py text eol=lf` (or normalising newlines before hashing)
closes it. Related standing lesson: recorded-hash form ambiguity — pin the blob form.

**Finding 6 — record/citation errors in the two documents that close K-05 (a citation-offset NIT).**
All recomputed from the blobs at `153edee9`:

| Record | Claim | Computed |
|---|---|---|
| `DISPOSITION_O9FIX.md:3` | exporter delta `+17/−2` | **+19/−2** (323 − 2 + 19 = 340 ✓) |
| `…/GEMINI/LEAD_ADJUDICATION.md:26` | exporter delta `+21/−2` | **+19/−2** |
| `DISPOSITION_O9FIX.md:11` | `ArchiveExporterRefusalCodeTests` at `check_…:266-462` | class spans **263-451**; `454` is `class _StatWithSize` |
| `DISPOSITION_O9FIX.md:48` | `observed_size != expected_size` branch at `p030_archive_exporter.py:131` | the branch is at **:136**; `:131` is the `path.open("rb")` line |

Every other citation I spot-checked in those records is exact (K-01 `:159-167`, K-02 `:287-292`,
K-03 `:109-112`, K-05's corrections `:223` and `check_…:151-153`, the three new test line numbers).

**Finding 7 — `test_target_and_receipt_unwritable_refusals` reads as a stronger guarantee than the code gives.**
`check_p030_archive_exporter.py:439` asserts `assertFalse(target.exists())` after `target_unwritable`. That
holds only because the mock at `:432-435` denies `Path.open` outright, so the file is never created. A genuine
write failure after a successful open leaves the truncated file of finding 1. Tighten once finding 1 is fixed.

**Finding 8 — environment, out-of-scope file: the adapter check fails on any host with a non-ASCII temp path.**
`check_p030_closed_partition_backup_adapter.py:835` vs `p030_closed_partition_backup_adapter.py:594-603`
(`ensure_ascii` mismatch), evidence in §2. Not caused by this candidate (that file is unchanged since before
`f42fd540`), but it means the Lead's recorded "`check_p030_closed_partition_backup_adapter.py` OK" is
reproducible only with an ASCII `%TEMP%` — worth a one-line fix (`json.dumps(configured_root,
ensure_ascii=False)`) so the roster's future runs on this host do not read as a regression.

### Gemini findings, dispositions

| Finding | My verdict | Basis |
|---|---|---|
| K-01 overflow/non-finite → `ExportRefused("source_line_invalid")` | **CONFIRMED CLOSED** | 6 RED arms all refuse with that code, no target; RED arm on the old exporter reproduces the raw `ValueError` |
| K-02 contract refusals → `ExportRefused("contract_refused")` | **CONFIRMED CLOSED** | 4 RED arms (row-level ×2, slice-level ×2) all refuse with that code; RED arm on the old exporter reproduces the raw `ContractRefused` |
| K-03 sub-second `exported_at_utc` refused, like the adapter | **CONFIRMED CLOSED, EXTENDED** | 12-stamp matrix against the adapter's own `_utc_z`: identical on 11, exporter stricter on 1, never looser |
| K-04 16/16 refusal codes have named negative tests | **CONFIRMED** | both counts reproduced from the bytes: 5/16 at `daf6a43b` (11 missing, = Gemini), 16/16 at `153edee9` |
| K-05 citation corrected | **CONFIRMED for the cited lines, EXTENDED** | the corrections are exact; three new citation/count errors in the same record — finding 6 |
| K-06 alternation regex | **CONFIRMED** | finding 3 |
| K-07 hash form | **CONFIRMED for the O9FIX packet; REFUTED for the candidate lane's `SHA256SUMS.txt`** | finding 4 |

### Limitations of the design, not defects of this candidate

- **L-1.** The exporter cannot verify the collector's bare-hex ids, because the collector's digest is taken over
  the raw wire record with its own field tuple (`market_data_collector.py:66-81`, `:215`), a different domain
  from `p030payload-v1`/`p030obs-v1`. A post-write edit of a collector partition is therefore re-identified into
  a fully valid archive row. That is inherent to Shape B as chosen (design note §B) and the receipt's
  `source_sha256` is the only handle on it; I flag it so nobody reads "identity_recomputed: true" as
  "source verified".
- **L-2.** `identity_recomputed` is a constant `True` at `:320` — it is a schema marker, not a measurement.

---

## 7. NOT VERIFIED

- **No real archive, no host, no deployment.** Everything ran on the fixture partition built by
  `check_market_data_collector` — 2 rows, one venue/symbol/interval/month, `venue_seq: null`, NATIVE track.
  Behaviour at real partition sizes, on PROXY track, with `CORRECTION` observations or `supersedes_*` chains,
  and across month boundaries is untested here and by the candidate's own suite.
- **Ruff not reproduced.** `ruff` is not installed in the pinned venv and not on PATH for me; the Lead's
  `LEAD_RUFF_O9FIX.txt` "All checks passed!" stands unchecked. Both files import and execute cleanly under
  3.12.12, which excludes syntax/name errors but not lint findings.
- **Repo guard not run** (it touches git state; out of my permitted command set). `LEAD_GUARD_O9FIX.txt`
  "RESULT: PASS" stands unchecked.
- **The Gemini attempt-2 report itself was not re-read**; I verified its closures against bytes independently.
  Note for the Lead: this brief describes the delta review as VOIDED/SUPPLEMENTAL, but
  `…/P030_O9FIX_20260915/GEMINI/LEAD_ADJUDICATION.md:3` records attempt 2 (20:00-20:03Z) as **COUNTED
  PASS-WITH-NITS**. The brief is stale on that point.
- **Content binding beyond canonical form is not proven by D-13 GREEN**: the adapter accepts an exported
  partition whose field values were edited, because `capture_stable_prefix` never recomputes
  `dataset_content_hash` from the rows (`p030_closed_partition_backup_adapter.py:245-249`). Closing that would
  be a change to the adapter, which is out of this candidate's scope.
- **Concurrency not exercised.** `open("xb")` makes creation atomic, but two exporters racing on one target,
  and a reader consuming the target between the write and the receipt, were not probed.
- **Windows only.** Junction/`..` probes and the `xb`/`os.replace` behaviour were measured on
  Windows 11 / NTFS; POSIX symlink behaviour of finding 2 is inferred from the code, not measured.
- **`short_read`'s first arm is the only realistic one**: the second arm stubs `Path.stat` to over-report size,
  which no real filesystem produces on demand (the Lead says the same); I did not find a real-world input that
  reaches `:136`.

---

## 8. Summary

The Shape-B contract is met on every promise the brief asked me to check except containment: the source is read
once and never mutated, identities come only from the contracts module, the output is byte-identical to the
adapter's canonical form, the receipt binds source → target → counts → dataset hash and I recomputed all four,
there is no network, no subprocess and no write outside the target and its receipt, and the collector is
untouched. K-01..K-05 are closed by the bytes, and both refusal-code counts (5/16 and 16/16) reproduce exactly.
The Lead-built O9FIX delta is load-bearing and sharp: its new tests fail on the old exporter for precisely the
three fixed defects and pass on everything else.

Two things block acceptance. A refusal that happens after the target has been written leaves the artefact
behind, and a genuine mid-write failure leaves a *truncated* partition that the real backup adapter accepts —
the exact "partial write surfaces as a silently exported partition" case this review exists to catch. And the
`source_root` containment check is fail-open against `..` and against junction/symlink components, so the
receipt's `source_path` can lie about where the bytes came from; the adapter and the contracts module both
refuse those same inputs on the same field, with dedicated tests, so the exporter is the only component in the
line that does not. Both fixes are small, local to `p030_archive_exporter.py`, and compatible with the
package's no-delete invariant.

My report alone accepts nothing; the Lead assembles the roster.

VERDICT: REQUEST_CHANGES
