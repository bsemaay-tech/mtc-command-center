# T0 review — WP-P0-30 Shape-B archive exporter, candidate `45a7f50eac009646bde1d80bcf66b1d14e6d72e0`

Reviewer: exact `claude-opus-5`, xhigh. **Second** exact-Opus read (T0 repair round 1 of 3).
Attempt 1 (`153edee9`, 2026-09-16 11:21–12:07Z) returned REQUEST_CHANGES with 2 REQUIRED findings.
Everything below was executed by me on the pinned interpreter; no result is taken from a record.

---

## 1. Verified identities (COMPUTED)

| Item | Value | How |
|---|---|---|
| HEAD of `C:/tmp/P030_INTEGRATION_20260913` | `45a7f50eac009646bde1d80bcf66b1d14e6d72e0` | `git -c safe.directory=* -C C:/tmp/P030_INTEGRATION_20260913 rev-parse HEAD` |
| `p030_archive_exporter.py` sha256 (blob bytes, LF) | `1bb9fb66ff94c95c2d19b3ae04137a4afd8514785ab27141420d4a57d9da0d1f` | `git show HEAD:<path>` → `sha256sum`; 494 lines |
| `check_p030_archive_exporter.py` sha256 (blob bytes, LF) | `4e2d291360565754094cc5f61701505a3507a4b199206853960eccfed19bce9e` | same; 787 lines |
| Working-tree copy of the exporter | byte-identical to the blob (this checkout is **LF**, not CRLF) | `sha256(Path(subject.__file__).read_bytes())` = `1bb9fb66…` |
| Commits `f42fd540..45a7f50e` | `daf6a43b`, `153edee9`, `53b43c21`, `0be0a8aa`, `45a7f50e` | `git log --oneline` |
| Files changed `f42fd540..45a7f50e` | exactly 2, both new: `check_p030_archive_exporter.py` (+787), `p030_archive_exporter.py` (+494) | `git diff --stat f42fd540 45a7f50e` |
| `market_data_collector.py`, `p030_market_data_contracts.py`, `p030_closed_partition_backup_adapter.py` and their three `check_*.py` | **byte-identical** at `f42fd540` and at `45a7f50e` (6/6 SAME) | `git show <rev>:<path>` → `sha256sum` both sides |
| Interpreter | `Python 3.12.12` at `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` | `--version` |

`53b43c21` is claimed format-only. Ruff is **not installed** on this host (neither in the pinned venv
nor on PATH), so I could not run `ruff format --check`. I verified the claim **more strongly** instead:

```
AST 153edee9 vs 53b43c21 p030_archive_exporter.py:       IDENTICAL
AST 153edee9 vs 53b43c21 check_p030_archive_exporter.py: IDENTICAL
```

(`ast.dump(ast.parse(src), include_attributes=False)` on both blob pairs.) A reflow cannot change the
AST and an AST match excludes every semantic edit including implicit string-literal rejoins. **Format-only: CONFIRMED.**

---

## 2. Conformance table — Shape B (`OD-20260914-P030-BRIDGE-SHAPE-1`)

| Shape-B promise | file:line | Verdict |
|---|---|---|
| Collector keeps writing its raw partitions; exporter is separate | `market_data_collector.py` byte-identical to base; exporter is a new module | **EQUAL** |
| Single byte read of the source; never re-read, never mutated | `p030_archive_exporter.py:201-218` (one `open("rb")`, `read()`, `tell()`); digest taken from the in-memory bytes at `:440`; `_source_rel` (`:130-198`) makes only metadata calls | **EQUAL** |
| Re-identification goes through the contracts module — no home-grown ids | imports `producer_payload_hash`/`observation_id`/`dataset_content_hash` (`:16-26`), used at `:281`, `:307`, `:396`. The three local regexes (`:66-68`) only *classify* a stored value (bare hex vs prefixed); all three `hashlib` uses (`:440`, `:444`, `:447`) are file digests, never identities | **EQUAL** |
| Output canonical: sorted keys, LF, one row per line | `:380-392` — `sort_keys=True`, `separators=(",",":")`, `ensure_ascii=False`, `allow_nan=False`, `+ "\n"`. Byte-for-byte the same dump parameters the adapter re-derives at `p030_closed_partition_backup_adapter.py:197-206` | **EQUAL** |
| Exclusive create | `:412` `staging_target.open("xb")`, `:464` `staging_receipt.open("xb")` — exclusive on the **staging** names. The published names are taken by `os.replace` after an existence check (`:476`, `:484`), which is *not* exclusive | **DIFFERENT (narrow)** — see finding N1 |
| Byte re-read equals what was written | `:424-434` re-reads and compares to `exported` — of the staging file. No re-read after publication (`os.replace` is atomic within the directory, so the published bytes are the verified bytes) | **EQUAL (with note)** |
| Receipt binds source digest → target digest → row counts | `:436-452`: `source_sha256`, `exported_sha256`, `source_record_count`, `exported_record_count`, `dataset_content_hash`, `exporter_sha256`, `exported_at_utc`, `identity_recomputed`. Observed live: `source_path=bars/HYPERLIQUID/BTC/15m/2026-02.jsonl`, `exported_sha256=58cbb2a4…`, `exporter_sha256=1bb9fb66…` (= the git blob digest) | **EQUAL** |
| Adapter's whole-second UTC `Z` rule | exporter `:105-127`, refusal at `:125-126` on `parsed.microsecond`; adapter `p030_closed_partition_backup_adapter.py:131-139` (`_utc_z` … `must use whole seconds`, `:138-139`). The exporter's parser (`fromisoformat(value[:-1] + "+00:00")`) is at least as strict as the adapter's `parse_utc_iso` (`MTC_COMMAND_CENTER/tools/opsa/opsa_common.py:90-99`), which additionally `.strip()`s and replaces every `Z` | **EQUAL** |
| Adapter's id-domain rule | exporter emits `p030obs-v1:` / `p030payload-v1:` via the contracts module; adapter requires `p030obs-v1` at `:212-213` (`_OBSERVATION_ID`) | **EQUAL** |
| Adapter's `source_path` canonicalisation rule | exporter `:149-197` vs adapter `_canonical_relative_posix` `:142-165` + `_refuse_source_links` `:168-178` + resolved containment `:250-253`. All clauses now present, including the percent-unquote loop added by `45a7f50e` (`:149-160`); the exporter additionally refuses `"\0"` and empty segments | **EQUAL** |
| Staging-then-publish idiom | matches the package's own convention: `opsa_common.py:102-110` `atomic_write_bytes` — "tmp file + os.replace so readers never see a torn file. On failure the tmp file is left on disk (no cleanup — a cleanup path would be a delete path)" | **EQUAL** |

---

## 3. Refusal-code table (reproduced from the bytes with an AST walk, not from any record)

Codes were extracted by walking every `ExportRefused(...)`/`_refuse(...)` call in the module blob;
tests were matched by scanning each `test_*` body for `caught.exception.code, "<code>"` and `self._refused("<code>"`.

**Both counts the brief asked me to reproduce came out exactly as claimed:**

| Revision | distinct codes | codes with no negative test |
|---|---|---|
| `daf6a43b` (lane O9EXP) | 16 | **11** — `contract_refused`, `invalid_timestamp`, `mixed_dataset_descriptor`, `receipt_exists`, `receipt_unwritable`, `short_read`, `source_fields_mismatch`, `source_line_noncanonical`, `source_outside_root`, `source_unreadable`, `target_unwritable` (matches Gemini K-04) |
| `153edee9` (O9FIX) | 16 | **0** (matches the O9FIX claim) |
| `45a7f50e` (candidate) | 16 | **0** |

No code was added, removed or renamed by the repair — `source_outside_root` was reused for every new
containment refusal, so the 16-code table stands.

| # | code | trigger (exporter line) | negative test at `45a7f50e` | my own probe |
|---|---|---|---|---|
| 1 | `invalid_timestamp` | `:107`, `:114`, `:119`, `:126` — not a `Z` string, unparseable, naive, sub-second | `test_invalid_timestamp_refusals_including_sub_second` | `.500Z` and `.000001Z` → `invalid_timestamp`, **no target written** (K-03) |
| 2 | `source_outside_root` | `:146`, `:157`, `:174`, `:181`, `:194` | 4 tests (`test_source_outside_root_refusal`, `..`-traversal, junction, percent-escape) | `..` traversal, NTFS junction, `%2e%2e` → all `source_outside_root`; adapter refuses each on the same field |
| 3 | `source_unreadable` | `:209` | `test_source_unreadable_refusal` | missing file → refused; **source is a directory** → `source_unreadable` |
| 4 | `short_read` | `:213`, `:217` | `test_short_read_refusals` (both arms) | UTF-16 source → `short_read` |
| 5 | `empty_partition` | `:215`, `:378` | `test_empty_partition_refusal` | zero-byte source refused (`:378` is unreachable dead code — harmless) |
| 6 | `source_line_invalid` | `:230`, `:234`, `:243` | `test_malformed_line_refusal`, `test_source_line_invalid_for_overflow_and_nan_literals` | `1e999`, nested `-1e999`, `NaN`, `Infinity`, duplicate key, invalid UTF-8, top-level list → all `source_line_invalid`, nothing written (K-01) |
| 7 | `source_line_noncanonical` | `:258`, `:263` | `test_source_line_noncanonical_refusal` | UTF-8 BOM, bare `\r` inside the file → `source_line_noncanonical` |
| 8 | `source_fields_mismatch` | `:274` | `test_source_fields_mismatch_refusal` | short fixture rows refused |
| 9 | `contract_refused` | `:283`, `:309`, `:398` | `test_contract_refused_from_row_identity`, `…_from_slice_validation` | `open="not-a-decimal"` → `contract_refused`; duplicated row (slice-level) → `contract_refused`; **no target written** either time (K-02) |
| 10 | `identity_mismatch` | `:290`, `:298`, `:313`, `:318` | `test_prefixed_identity_mismatch_is_refused` | — |
| 11 | `mixed_dataset_descriptor` | `:341` | `test_mixed_dataset_descriptor_refusal` | — |
| 12 | `target_exists` | `:362`, `:405`, `:417`, `:485` | `test_target_exists_refusal`, `test_mid_write_failure…` | second run over a leftover staging partial → `target_exists`, leftover untouched |
| 13 | `receipt_exists` | `:365`, `:469`, `:477` | `test_receipt_exists_refusal` | — |
| 14 | `target_unwritable` | `:419`, `:489` | 3 tests | ENOSPC mid-write → `target_unwritable`; denied publish → `target_unwritable` |
| 15 | `target_verify_failed` | `:428`, `:431` | `test_target_reread_byte_identity_refusal` | tampered re-read → `target_verify_failed` |
| 16 | `receipt_unwritable` | `:472`, `:482` | `test_target_and_receipt_unwritable_refusals` | denied receipt write → `receipt_unwritable`; denied receipt publish → `receipt_unwritable` |

**K-01 / K-02 / K-03: CONFIRMED CLOSED by my own probes.** None of the four inputs the brief named
(`1e999` row, `NaN` literal, contracts-refused row, sub-second timestamp) can produce an EXPORTED row;
each refuses with the documented `ExportRefused.code` and leaves the filesystem untouched.

---

## 4. Repair round 1 — attempt-1 findings 1 and 2

All probes below are my own (`C:/tmp/OPUS_P030_SCRATCH/attempt2/probe_findings.py`), written without
reusing the shipped test bodies; only `check_market_data_collector`'s fixtures are reused to build a
**real** collector partition through `market_data_collector.MonthlyArchive`.

### Finding 1 — "a refusal after the target existed left a consumable/truncated partition": **CLOSED**

| Probe | Result |
|---|---|
| Mid-write ENOSPC (half the bytes, then `OSError(28)`) | `ExportRefused('target_unwritable')`; `target` **absent**, receipt **absent**; the 616-byte remnant sits only at `p.jsonl.p030partial` (source is 1182 B) |
| Second run against the same target | `ExportRefused('target_exists')` — *"a staging partial (.p030partial) from an earlier refused export exists"*; the leftover is **not** adopted, overwritten or removed |
| Receipt-write refusal (`PermissionError` on the staging receipt) | `ExportRefused('receipt_unwritable')`; target **absent**, receipt **absent**; only the staging partial remains |
| Verify refusal (re-read tampered) | `ExportRefused('target_verify_failed')`; target **absent**, receipt **absent** |
| Receipt-**publish** refusal (`os.replace` → receipt denied) | `ExportRefused('receipt_unwritable')`; target **absent**, receipt **absent**; both staging files remain |
| Publication order | `os.replace` calls observed, in order: `('p.jsonl.p030export.json.p030partial' → 'p.jsonl.p030export.json')`, then `('p.jsonl.p030partial' → 'p.jsonl')` — **receipt first, target second**, exactly as documented at `:474-475` |
| `os.replace` is the only publication path | module contains exactly 2 `os.replace(` calls and no `os.rename(` |
| No delete code path | token scan of the module: no `unlink`, `rmtree`, `os.remove`, `rmdir`, `shutil`, `truncate`, `"wb"` |
| Successful export writes exactly two files | `['p.jsonl', 'p.jsonl.p030export.json']` — nothing else, no staging residue |

There is **no path** left on which a refusal puts bytes under the target's own name. The finding is closed.
One residual, which I raise as N2 below rather than as a re-open: the leftover's *bytes* are still
adapter-acceptable; only its *name* protects it.

### Finding 2 — "`source_root` containment fail-open": **CLOSED** (symlink arm not testable on this host)

| Probe | Exporter | Adapter on the same path |
|---|---|---|
| `…/bars/../../outside/2026-02.jsonl`, root `…/bars` | `ExportRefused('source_outside_root')` — *"must be a canonical relative POSIX path inside source_root"*; **no target written** | refuses: *"source_path must be a canonical relative POSIX path"* |
| NTFS junction component (`mklink /J`, created successfully on this host) | `ExportRefused('source_outside_root')` — *"must not contain a symlink or junction component"* | refuses: *"source JSONL must not be a symlink or junction component"* |
| `%2e%2e` percent-escaped segment (the `45a7f50e` parity tweak) | `ExportRefused('source_outside_root')` | refuses: *"source_path must be a canonical relative POSIX path"* |
| POSIX symlink component | **NOT VERIFIED** — `os.symlink` fails on this host with `WinError 1314` (no `SeCreateSymbolicLinkPrivilege`). The check is the same expression as the junction arm (`:180` `current.is_symlink() or current.is_junction()`), which I did exercise |
| Root that is itself a junction (resolved-form gate) | exporter refuses, adapter refuses — parity holds |

At `45a7f50e` the resolved-form gate (`:189-197`) is present and non-strict, so a missing leaf still
reports `source_unreadable` rather than a containment error — I confirmed that ordering with the
missing-file probe.

### RED arm (mandated): the repaired checker against the pre-repair exporter

`cwd = C:/tmp/OPUS_P030_SCRATCH/attempt2/redarm25`, `PYTHONPATH=C:\tmp\P030_INTEGRATION_20260913`,
exporter = `53b43c21` blob, checker = `0be0a8aa` blob:

```
Ran 25 tests in 0.313s
FAILED (failures=3, errors=4)
ERROR: test_mid_write_failure_publishes_nothing_under_the_target_name
ERROR: test_publish_failure_of_the_target_leaves_receipt_without_partition
ERROR: test_target_and_receipt_unwritable_refusals
ERROR: test_target_reread_byte_identity_refusal
FAIL:  test_dotdot_traversal_is_refused_even_when_lexically_under_root
FAIL:  test_exporter_sha256_is_the_lf_form_on_any_checkout
FAIL:  test_junction_component_is_refused_like_the_adapter
```

**7 of 25 — the Lead's recorded RED arm reproduced exactly, test-for-test.** With the `45a7f50e`
checker (26 tests) against the same pre-repair exporter: `FAILED (failures=4, errors=4)` = 8 of 26,
the extra failure being `test_percent_encoded_segments_are_refused_like_the_adapter`. Every new test
is load-bearing: none of them passes against the pre-repair bytes.

### Attempt-1 NITs 3, 5, 7

| NIT | Status | Evidence |
|---|---|---|
| 3 (= Gemini K-06): split the `non-finite\|not parseable` alternation | **APPLIED** | `check_p030_archive_exporter.py:407-419` — one exact message per arm: `1e999`→`"non-finite"`, `NaN`→`"not parseable"`, nested→`"non-finite"` |
| 5: `exporter_sha256` must not depend on a CRLF checkout | **APPLIED and verified** | `p030_archive_exporter.py:442-446`; live receipt value `1bb9fb66…` **equals the git blob digest**; the test forces a CRLF read and gets the same digest |
| 7: unwritable/verify tests must assert nothing under the target name | **APPLIED** | `check_…:239-242`, `:540-541`, `:561-563` |
| 4, 6, 8 | out of scope for this commit per the addendum; 8 is still live on this host — see N5 |

---

## 5. D-13 drill evidence

Command, cwd `C:/tmp/P030_INTEGRATION_20260913`, pinned interpreter:

```
> C:/tmp/P020_IMPL_20260912/.../python.exe check_p030_archive_exporter.py
...
Ran 26 tests in 0.396s

OK
D-13 RED RAW REFUSAL: prefix record is not canonical JSONL
D-13 GREEN EXPORTED CAPTURE: PASS
```

Sibling checkers, same cwd and interpreter:

```
check_p030_market_data_contracts.py        → NETWORK ATTEMPTS: 0 / P030 MARKET DATA CONTRACTS CHECK: PASS  (exit 0)
check_market_data_collector.py             → NETWORK ATTEMPTS: 0 / MARKET DATA COLLECTOR CHECK: PASS       (exit 0)
check_p030_closed_partition_backup_adapter.py → Ran 44 tests … OK (exit 0)  [only with an ASCII TEMP — see N5]
```

**The drill really goes through the adapter, not a re-implementation.** `check_p030_archive_exporter.py:16`
imports `capture_stable_prefix` from `p030_closed_partition_backup_adapter`; both halves call it. I
re-ran both halves myself against a freshly exported partition:

| Arm | Result |
|---|---|
| RED — raw collector partition through `capture_stable_prefix` | refused: *"prefix record is not canonical JSONL"* |
| GREEN — exported partition | accepted; `record_count=2`, `dataset_content_hash=p030ds-v1:2dee3d5d…` equal to the export receipt's |
| GREEN depends on the export? mutant: pretty-printed rows | adapter refuses — *"prefix record is not canonical JSONL"* |
| mutant: `p030obs-v1:` prefix stripped | adapter refuses — *"observation_id must match p030obs-v1 identity"* |
| mutant: final newline dropped | adapter refuses — *"high-water prefix must end with newline"* |
| mutant: **one byte changed inside a price string** | **adapter ACCEPTS** — see N3 |

So GREEN depends on the export's *canonical form and id domains*, but not on the exported *identities*.

---

## 6. Boundary

- **No network:** the exporter imports only `hashlib, json, math, os, re, dataclasses, datetime, pathlib, typing, urllib.parse.unquote` plus the contracts module. `urllib.parse` is pure string parsing. Both sibling collectors report `NETWORK ATTEMPTS: 0`.
- **No subprocess in the subject.** The *checker* shells out once (`check_…:748-749`, `cmd /c mklink /J`) to build a junction — this is the package's own precedent: `check_p030_closed_partition_backup_adapter.py:265-266` does the identical thing. Not a deviation.
- **Writes:** across every probe, a successful run created exactly `<target>` and `<target>.p030export.json`; every refusal created at most `<target>.p030partial` (+ `<receipt>.p030partial`). The one other write is `target_jsonl.parent.mkdir(parents=True, exist_ok=True)` (`:411`), inside the guarded block — a refused run can leave an empty directory behind, which is inert.
- **Collector untouched:** byte-identical to `f42fd540`; the whole `f42fd540..45a7f50e` diff is the two new files.

---

## 7. Report honesty (records vs bytes)

| Record claim | My check | Verdict |
|---|---|---|
| `LEAD_VERIFICATION_P030_R1.md:22` — RED arm "7 of 25 fail … traversal, junction, LF-digest by behaviour; the four staging-dependent tests error" | reproduced: 3 failures + 4 errors, same 7 test names | **TRUE** |
| `…:21` — "Ran 25 tests … OK" at `0be0a8aa`; 26 at `45a7f50e` | 26 tests OK at HEAD | **TRUE** |
| `…:13` — `53b43c21` format-only, no semantic change | AST-identical on both files | **TRUE** (verified more strongly than `ruff format --check`) |
| `…:15` — "no new refusal code (the 16-code table stands)" | 16 codes at `daf6a43b`, `153edee9` and `45a7f50e` | **TRUE** |
| `…:14` — "no delete code path" | token scan: none | **TRUE** |
| `…:24` — ruff "three pre-existing findings only … 0 new" | `LEAD_RUFF_R1.txt` records I001, SIM117, RUF059 and "Found 3 errors" | **TRUE** — and this **refutes** Gemini `P030_R1_NIT_1`, which reported "Found 5 errors" from that same file |
| `…:23` — "Sibling checkers: `check_p030_closed_partition_backup_adapter.py` OK" | OK **only** with an ASCII `TEMP`; on this host's default `TEMP` it FAILS | **HOST-CONDITIONAL** — see N5 |
| Gemini delta review §1.7 — "Leftovers never consumable: leftovers carry `.p030partial`, which the backup adapter and consumers reject (expecting `.jsonl`)" | the adapter has **no** extension rule (`capture_stable_prefix` `:254-259` checks only `is_file()` and the reserved receipt name); it **accepted** a `.p030partial` leftover | **REFUTED** — see N2 |
| Gemini delta review `P030_R1_NIT_3` (os.replace TOCTOU) | reproduced by execution | **TRUE** — see N1 |
| `p030_archive_exporter.py:71-73` — a leftover staging file "is never consumable as a partition" | refuted as written; true only in the weaker sense "no archive *name* ends in this suffix" | **OVER-CLAIM** — see N2 |

The candidate's own commit messages (`0be0a8aa`, `45a7f50e`) disclose the Lead as the builder and list
closures that all hold against the bytes. The one number in `0be0a8aa`'s message I could check
independently — "7 of 25 fail" — is exact.

---

## 8. Findings

**No REQUIRED findings.** Attempt 1's two REQUIRED findings are both closed by the bytes and by my probes.

### N1 — NIT — `os.replace` publication can overwrite a target created inside the check→replace window
`p030_archive_exporter.py:484-487` (and the same shape for the receipt at `:476-479`).
At `153edee9` the target was created with `open("xb")`, which could never clobber. The repair replaced
that with `if target_jsonl.exists(): _refuse(...)` followed by `os.replace`, which **does** clobber.
Reproduced: with a foreign writer creating the target between the check and the call, the export
returned success and the intruder's bytes were gone. The window is microseconds and needs a
non-exporter writer, so this is not a realistic data-loss path for a single-writer archive tool — but
the code comment at `:407-408` ("this tool never overwrites or removes it") is stronger than the bytes.
Cheap fix on this Windows-targeted package: publish with `os.rename`, which raises `FileExistsError`
on Windows when the destination exists, restoring the no-clobber guarantee at the publication step with
no delete path added (the existence pre-checks stay for POSIX). Independently raised by the Gemini
delta review as `P030_R1_NIT_3`; I confirmed it by execution rather than by reading.

### N2 — NIT — "a leftover staging partial is never consumable" is an over-claim; only the name protects it
`p030_archive_exporter.py:71-73` (comment), `0be0a8aa` commit message, Gemini delta §1.7.
The ENOSPC probe's remnant was 616 of 1232 bytes — the exporter's two rows are 616 bytes each, so the
cut landed exactly on a line boundary and the leftover is a **complete, canonical, LF-terminated
one-row prefix**. Pointed at it explicitly, the real adapter **accepted** it and wrote a stable-prefix
receipt. `capture_stable_prefix` (`p030_closed_partition_backup_adapter.py:220-290`) has no extension
or name rule beyond the reserved `_P030_STABLE_PREFIX.json`, so the claim that consumers "reject
(expecting `.jsonl`)" is false as stated. In practice nothing in this package globs for partitions, so
a caller would have to name the `.p030partial` file on purpose — the hazard is far below attempt-1's
finding 1, where the garbage sat under the exact name a consumer would pass. Either weaken the comment
to what the bytes support ("no archive *name* ends in this suffix") or make the remnant structurally
non-consumable (e.g. stage in a sibling directory, or write a leading marker line).

### N3 — NIT — the D-13 GREEN arm does not depend on the exported identities; a one-line assert would fix that
`check_p030_archive_exporter.py:54-94`.
I mutated one byte inside a price string of an exported partition (`"open":"…` → `"open":"9…`) and the
adapter still accepted it: `_prefix_facts` (`:181-217`) checks canonical form and that `observation_id`
matches the `p030obs-v1:` **regex**, never re-derives identity, and `dataset_content_hash` is supplied
by the caller and only regex-checked (`:245-249`). So GREEN, as written, proves "exported bytes are
canonical and carry prefixed ids", not "the adapter validates what the exporter produced".
Verified fix: the stable receipt's `prefix_sha256` equals the export receipt's `exported_sha256` exactly
on a clean GREEN (`58cbb2a4…` = `58cbb2a4…`) and differs on the price mutant (`0ddef851…`). One
assertion in the GREEN arm binds the captured bytes to the export receipt and detects this class.

### N4 — NIT — one raw-exception path survives: `RecursionError` on pathologically nested JSON
`p030_archive_exporter.py:229` and `:242` catch `(UnicodeDecodeError, json.JSONDecodeError, ValueError)`.
A source line with ~3000 nested arrays makes `json.loads` raise `RecursionError` (a `RuntimeError`, not
a `ValueError`), which escapes as a raw exception instead of `ExportRefused`. Per the brief's rule this
is a NIT, not REQUIRED: I confirmed the filesystem is untouched (no target, no receipt, no staging — the
failure happens before any write). The adapter shares the same exposure (`:109-118`), so this is a
parity-preserving gap, not a divergence. Not reachable from collector output.

### N5 — NIT (carry-forward of attempt-1 NIT 8; unchanged file, outside the candidate) — the sibling adapter checker fails on this host
`check_p030_closed_partition_backup_adapter.py:835-840`, byte-identical at `f42fd540` and at HEAD.
On this host `check_p030_closed_partition_backup_adapter.py` **fails**:

```
FAIL: test_isolated_config_redirect_after_check_never_reaches_restore (defect='duplicate_backup_root')
  File "…\check_p030_closed_partition_backup_adapter.py", line 840
    self.assertEqual(raw.count(anchor), 1)
AssertionError: 0 != 1
Ran 44 tests … FAILED (failures=1)
```

Cause, diagnosed from the bytes: the bound config is serialised with `ensure_ascii=False`
(`p030_closed_partition_backup_adapter.py:594-603`) while the test builds its anchor with a default
`json.dumps` (`ensure_ascii=True`), so every non-ASCII character in the path is escaped in the anchor
and literal in the file. The owner's default `TEMP` is `C:\Users\Barış…`, which contains `ı` and `ş`.
Re-running with an ASCII `TEMP` gives `Ran 44 tests … OK (exit 0)`. This cannot be caused by the
candidate (both files are byte-identical to the base) and the Lead already logged it as out of scope
(`LEAD_VERIFICATION_P030_R1.md:16`, F8). I raise it only because `LEAD_VERIFICATION_P030_R1.md:23`
records the sibling checkers as plainly "OK": that line needs the ASCII-`TEMP` precondition, or the
roster will carry a green claim that does not reproduce on the owner's own machine.

### Status of the earlier findings

| Finding | Status |
|---|---|
| Attempt-1 REQUIRED 1 (consumable/truncated partition after a refusal) | **CONFIRMED CLOSED** (9 probes, §4) |
| Attempt-1 REQUIRED 2 (`source_root` containment fail-open) | **CONFIRMED CLOSED** for `..`, junction, percent-escape and the resolved-form gate; symlink arm NOT VERIFIED on this host |
| Attempt-1 NIT 3 / 5 / 7 | **APPLIED** (verified in the bytes and, for 5, at runtime) |
| Gemini K-01 (overflow → `source_line_invalid`) | **CONFIRMED CLOSED** (`1e999`, nested `-1e999`) |
| Gemini K-02 (contract refusals wrapped) | **CONFIRMED CLOSED** (row-level and slice-level) |
| Gemini K-03 (whole-second `exported_at_utc`) | **CONFIRMED CLOSED** (`.500Z`, `.000001Z`) |
| Gemini K-04 (11 of 16 codes untested) | **CONFIRMED** at `daf6a43b` (11/16 reproduced) and **CLOSED** at `153edee9`/`45a7f50e` (0/16) |
| Gemini K-05 (citation) | documentary; corrected per `LEAD_VERIFICATION_P030_R1.md:34` — not re-derived by me |
| Gemini K-06 (alternation regex) | **CLOSED** (attempt-1 NIT 3, applied) |
| Gemini K-07 (`SHA256SUMS.txt` hashed a CRLF checkout) | out of this commit; note that at `45a7f50e` `exporter_sha256` is now LF-normalised, so the receipt value equals the blob digest on any checkout |
| Gemini `P030_R1_NIT_1` (ruff "5 errors") | **REFUTED** — `LEAD_RUFF_R1.txt` reads "Found 3 errors" |
| Gemini `P030_R1_NIT_2` (percent-unquote parity) | **CLOSED** by `45a7f50e`; verified by probe, exporter and adapter refuse `%2e%2e` alike |
| Gemini `P030_R1_NIT_3` (os.replace TOCTOU) | **EXTENDED** — reproduced by execution; see N1 |

---

## 9. NOT VERIFIED

1. **No real archive, no host.** Everything ran against synthetic collector partitions built from `check_market_data_collector`'s fixtures on this workstation. No real market-data month, no GATEA-STAGING or any other host, no P026 store on real hardware.
2. **POSIX symlink component.** `os.symlink` fails here with `WinError 1314` (no privilege). The junction arm exercises the same expression (`:180`), but a genuine symlink was never created.
3. **Ruff.** Not installed in the pinned venv or on PATH, so `ruff format --check` and `ruff check` could not be run. The format-only claim was verified by AST equality instead; the lint claim rests on `LEAD_RUFF_R1.txt`, which I read but did not reproduce.
4. **True concurrency.** N1 was reproduced by injecting a writer at the exact instruction boundary, not by two real processes racing. The size of the real window was not measured.
5. **Non-Windows behaviour.** `os.replace`, `is_junction()` and `PureWindowsPath` semantics were exercised on Windows 11 only. On POSIX, `os.rename` (the N1 fix) would clobber silently, so N1's remedy is Windows-specific.
6. **TOCTOU between containment check and read.** `_source_rel` validates a path and `_read_source_once` re-opens it by name; a swap in between is not detected. The adapter has the identical shape (`:220-260`), so this is parity, not divergence — but neither component was probed for it.
7. **Collector-side tamper detection.** The collector's bare hashes come from an injected `IdentityPolicy` (`market_data_collector.py:58-87`) whose fields/algorithm are not recorded in the row, so the exporter cannot recompute them; it accepts any bare hex and re-identifies (`:294-301`). A row mutated between collection and export is therefore exported with fresh, self-consistent P030 identities and no refusal. The receipt's `source_sha256` + `identity_recomputed: true` is the only audit hook. I found no available invariant that would let the exporter detect this, so I raise it as a limitation, not a finding.
8. **`53b43c21`'s "old 20 tests pass at those bytes".** I did not run the 20-test checker at `53b43c21`; AST equality with `153edee9` plus the 26-test GREEN at HEAD covered the semantic claim.
9. **Gemini K-05 and the F6 record corrections** were not re-derived from the `153edee9` blobs.

My report alone accepts nothing; the Lead assembles the roster. Exact Sol has not yet read this candidate.

VERDICT: PASS-WITH-NITS
