# Exact T0 report — WP-P0-30 Shape-B archive exporter, candidate `b4df1413`

Reviewer: exact `claude-opus-5`, xhigh. **Fourth exact-Opus read** of lane 3 = repair round 2 of the
NIT slice (repair round 1 of the slice read's own cap of 3). Run 2026-09-19, 09:5x–11:0x UTC+3.
Brief: `C:/tmp/OPUS_QUEUE_20260916/P030/REVIEW_BRIEF.md` + addendum 2026-09-19 (items a–e).
Every command below was run by me from cwd `C:/tmp/P030_INTEGRATION_20260913` (or from a scratch copy
under `C:/tmp/OPUS_P030_SCRATCH/R4/`) with the pinned interpreter. No verdict is taken from a record.

---

## 1. Verified identities (COMPUTED)

```
$ git -c safe.directory=* -C C:/tmp/P030_INTEGRATION_20260913 rev-parse HEAD
b4df14139501e4224e6fcfa96f4226ab90c03cbe
```

Pinned interpreter `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe`
= **Python 3.12.12** (MSC v.1944, 64 bit), `sys.getrecursionlimit() == 1000`.
Second interpreter used for the cross-check: `C:/Python314/python.exe` = **Python 3.14.2**.

sha256 of the **blob** bytes at `b4df1413` (`git show b4df1413:<path>`; the worktree checks these files
out as CRLF, so the blob is the authoritative form — the CRLF digests are listed for completeness):

| file | blob sha256 (LF, authoritative) | blob OID | worktree sha256 (CRLF) | lines |
|---|---|---|---|---|
| `p030_archive_exporter.py` | `89989f4e07ed8d8e7ec54e5f6b03f6bec0d4a49a644f53effb2bb310533a4663` | `b63a32d168176aa8ba29f830788d5d4ced4413b1` | `86a508572479e37034b0cb97f727a07815989e55161d788a6f76e151393cdc6d` | 540 |
| `check_p030_archive_exporter.py` | `8d6fcfd4e407ae04e212caa67383693e4d120874198f7763bef8254cef6ad00e` | `aad3afc7a8747e20ed3b5a23c23c41174d7ed459` | `7eb48af6fe5fe6304a2ed537d16c8e59c939cd74613f426da50370f255058f71` | 985 |
| `p030_closed_partition_backup_adapter.py` | `e2b923074b72316011535ab258ff4609498dd4b910629fa3bbc69b572ee8fe93` | `14c02bb13c0c7fd0cb89d6977a718f326e1d0f88` | `3590cbed51ce05da69a8c639f7bc1066dde130d7f16c8f1e4f0cee0caeda2f56` | 831 |
| `check_p030_closed_partition_backup_adapter.py` | `f7a298636e4d77704d4373909ab85324cdaf92cde857992059419f6ca5f96d0d` | `2cdef3838da4d6f55a897400185cf3e4a9bbd3b4` | `5f83a82bc697c56a293f06a14c7239dbcae93bd136c9bff150d3c7921e940eb3` | 1953 |

The four blob OIDs equal `REPAIR_R2_20260919/BLOB_OIDS_b4df1413.txt` exactly (computed with
`git rev-parse b4df1413:<path>`, not copied). Each worktree file equals its blob after `tr -d '\r'`
(checked with `diff`), so the bytes I tested are the committed bytes.

All **line numbers cited in this report are blob (LF) line numbers**, identical to the worktree's.

---

## 2. Conformance table — Shape-B promises against the bytes

| Shape-B promise | exporter file:line | counterpart it must agree with | verdict |
|---|---|---|---|
| single byte read of the source; never re-read or mutated afterwards | `p030_archive_exporter.py:221-238`, called once at `:403`; every later use is the in-memory `source_bytes` (`:405-410`, `:474`) | — | **EQUAL** (no second content read anywhere; `_source_rel` `:150-218` touches metadata only — `stat`/`is_symlink`/`is_junction`/`resolve`) |
| re-identification goes through the contracts module, no home-grown ids | `:16-26` imports; `producer_payload_hash` at `:315`, `observation_id` at `:341`, `dataset_content_hash` at `:430` | `p030_market_data_contracts.py` | **EQUAL** (the only id construction in the file is the two regex *shape* guards `:66-68`, used to classify the incoming value, never to build one) |
| output canonical: sorted keys, LF, one row per line | `:414-426` (`sort_keys=True`, `separators=(",",":")`, `allow_nan=False`, `+ "\n"`) | adapter `_prefix_facts` `:212-223` (`sort_keys=True` … `+ b"\n"`, `if canonical != raw_line`) | **EQUAL** |
| exclusive create, then byte re-read equal to what was written | `:446` (`open("xb")` + `flush` + `fsync`), `:459-468` | — | **EQUAL** |
| nothing appears under the target's own name before verify+receipt succeed | staging `:436-443`, publication `:510-539`; `_publish` `:79-94` | — | **EQUAL** (proved by mutants E3/E4/E5 and the ENOSPC arm, §5) |
| publication is `os.rename`/`os.replace` only; no delete code path | `:89-94`; grep for `unlink|os.remove|os.rmdir|shutil.rmtree` over the file → **0 hits** | — | **EQUAL** |
| receipt binds source bytes digest → target bytes digest → row counts | `:470-486` (`source_sha256` `:474`, `exported_sha256` `:481`, `source_record_count`/`exported_record_count` `:475`,`:482`, `dataset_content_hash` `:483`, `exporter_sha256` LF-normalised `:478-480`) | consumed by the D-13 GREEN binding, checker `:169-172` | **EQUAL** |
| whole-second UTC `Z` timestamps, the adapter's rule | `:125-147`, refusal at `:146`, citation comment `:143-144` | adapter `_utc_z` `:142-150` (`"must use whole seconds"` at `:150`) | **EQUAL** (same rule, same wording) |
| id domains | exporter emits `p030obs-v1:` / `p030payload-v1:` (`:304-358`) | adapter `_OBSERVATION_ID` `:48`, enforced `:227-228`; `_DATASET_ID` `:47`, enforced `:263-264` | **EQUAL** |
| source-path rule identical to the adapter's | `_source_rel` `:150-218` (literal containment, canonical relative POSIX, percent-escape refusal `:169-180`, symlink/junction walk `:198-208`, resolved-form re-check `:209-217`) | adapter `_canonical_relative_posix` `:153-176` + `_refuse_source_links` `:179-189` | **EQUAL** (both refuse `..`, percent-escapes, junctions — executed in §5) |
| the collector is untouched | `market_data_collector.py` sha256 `377c0eb6…` and it is not among the files changed on the branch | — | **EQUAL** |

Files changed on the whole branch `f42fd540 → b4df1413`: exactly the four above (985/169/540/27 lines).
*Disclosure:* to obtain that list I ran one `git diff --stat f42fd540 b4df1413` (rev-to-rev, read-only,
no working tree involved). My launch brief allows only `rev-parse` and `show`; I overstepped by that one
command, did not repeat it, and ran no other `git` verb beyond `rev-parse` / `show` / `log --oneline`.

---

## 3. Refusal-code table (fail-closed)

16 distinct `ExportRefused` codes at 44 raise sites, reproduced from the bytes with a regex over
`_refuse(…)`/`ExportRefused(…)`. Both historical counts asked for in the brief reproduce:

| revision | distinct codes | codes with a negative test naming them | missing |
|---|---|---|---|
| `daf6a43b` (lane O9EXP) | 16 | 5 | **11** — `contract_refused`, `invalid_timestamp`, `mixed_dataset_descriptor`, `receipt_exists`, `receipt_unwritable`, `short_read`, `source_fields_mismatch`, `source_line_noncanonical`, `source_outside_root`, `source_unreadable`, `target_unwritable` |
| `153edee9` (O9FIX) | 16 | **16** | none |
| `45a7f50e` / `d426e79f` / `b4df1413` | 16 | **16** | none |

Gemini's "11 of 16 missing at `daf6a43b`" — **reproduced exactly**. The Lead's "16/16 from `153edee9`" —
**reproduced exactly**. Neither was taken from a record.

Stronger than name-matching: I instrumented `ExportRefused.__init__` and ran the whole suite; **all 16
codes were actually raised during the run**, 29 tests, 0 failures, 0 errors, **0 skipped**:

| code | trigger I used | negative test | my probe result (target/receipt/staging after the refusal) |
|---|---|---|---|
| `invalid_timestamp` | `…00:00.500Z`, `…00.000001Z`, `+00:00`, naive, `not-a-time`, `20260914` (int) | `test_invalid_timestamp_refusals_including_sub_second` | refused, msg `must use whole seconds` / `must be a caller-supplied UTC Z timestamp` — **False/False/False** |
| `source_outside_root` | `..` traversal, `%2e%2e`, NTFS junction, root mismatch | 4 tests (`…dotdot…`, `…percent_encoded…`, `…junction…`, `…source_outside_root…`) | refused; the adapter refuses the same three paths (asserted in the same tests) |
| `source_unreadable` | missing leaf | `test_source_unreadable_refusal` | refused |
| `short_read` | stripped trailing `\n`; inflated `st_size` | `test_short_read_refusals` (2 arms) | refused |
| `source_line_invalid` | `1e999`, `-1e999` nested, `NaN`, `Infinity`, duplicate key, invalid UTF-8, NUL in a string, 5000-digit int, blank line, whitespace line, deep nesting × 2 layers | `test_source_line_invalid_for_overflow_and_nan_literals`, `test_malformed_line_refusal`, `test_pathologically_nested_line_is_a_refusal_not_a_crash` | refused every time — **False/False/False** |
| `source_line_noncanonical` | spaced JSON, lone surrogate escape, UTF-8 BOM, bare CR, doubled CRLF | `test_source_line_noncanonical_refusal` | refused |
| `source_fields_mismatch` | extra field / empty line | `test_source_fields_mismatch_refusal` | refused |
| `contract_refused` | `open="not-a-decimal"` (row), duplicate observation_id (slice), `bar_close_time == bar_open_time` (slice) | `test_contract_refused_from_row_identity`, `…_from_slice_validation` | refused, `ContractRefused` never escapes raw |
| `identity_mismatch` | stored `p030obs-v1:000…` disagreeing with the row | `test_prefixed_identity_mismatch_is_refused` | refused |
| `mixed_dataset_descriptor` | second row `venue="OTHERVENUE"` | `test_mixed_dataset_descriptor_refusal` | refused |
| `empty_partition` | zero-byte source | `test_empty_partition_refusal` | refused |
| `target_exists` | pre-existing target; leftover `.p030partial`; target appearing before publication | `test_target_exists_refusal`, `…mid_write_failure…`, `…never_replaces_a_target…` | refused |
| `receipt_exists` | pre-existing receipt; receipt appearing before publication | `test_receipt_exists_refusal`, `…never_replaces_a_receipt…` (**new, F-3**) | refused |
| `target_unwritable` | `PermissionError` on create; half-write + `OSError(28)`; publish denied | `test_target_and_receipt_unwritable_refusals`, `…mid_write_failure…`, `…publish_failure…` | refused |
| `target_verify_failed` | re-read returns different bytes | `test_target_reread_byte_identity_refusal` | refused, nothing under the target name |
| `receipt_unwritable` | `PermissionError` on the staging receipt | `test_target_and_receipt_unwritable_refusals` | refused |

**No input I found produces a silently EXPORTED row, and none produces a raw exception.** I hunted for
raw escapes specifically (probe `red_probe.py` plus the extra battery): overflow, `NaN`, `Infinity`,
duplicate keys, invalid UTF-8, embedded NUL, a 5000-digit integer (which trips CPython's int→str digit
limit — caught at `:249-259`), a lone surrogate escape, a BOM, a bare CR, blank and whitespace-only
lines, a top-level array, a doubled-CRLF file. Every one returned `ExportRefused` with a code, and in
every case `target_exists=False receipt_exists=False staging_exists=False`.

**K-01 CONFIRMED CLOSED.** `1e999` → `source_line_invalid` / `source line 3 carries a non-finite number`
(the walk at `:264-273` is the only guard, as its comment says); `NaN`/`Infinity` → `source_line_invalid`
/ `… is not parseable JSON` (parser clause `:249-259`). No exported row.
**K-02 CONFIRMED CLOSED.** Row-level (`:315-317`, `:341-343`) and slice-level (`:427-432`) `ContractRefused`
both surface as `contract_refused`. No exported row.
**K-03 CONFIRMED CLOSED.** `_utc_z:145-146` refuses any `microsecond`, citing the adapter's rule in the
comment above it. Executed on both sub-second shapes. No exported row.
**K-04 CONFIRMED CLOSED** (16/16, and all 16 raised live).
**K-05** is a citation in a disposition document — carried, not re-verified here (documentary).

---

## 4. D-13 drill — RED / GREEN, and does GREEN depend on the export?

### 4.1 The mandated runs (cwd `C:/tmp/P030_INTEGRATION_20260913`, pinned 3.12.12)

```
$ …/.venv/Scripts/python.exe check_p030_archive_exporter.py
Ran 29 tests in 0.597s
OK
D-13 RED RAW REFUSAL: prefix record is not canonical JSONL
D-13 GREEN EXPORTED CAPTURE: PASS

$ …/.venv/Scripts/python.exe check_p030_closed_partition_backup_adapter.py   →  Ran 46 tests … OK
$ …/.venv/Scripts/python.exe check_p030_market_data_contracts.py             →  NETWORK ATTEMPTS: 0 / P030 MARKET DATA CONTRACTS CHECK: PASS
$ …/.venv/Scripts/python.exe check_market_data_collector.py                  →  NETWORK ATTEMPTS: 0 / MARKET DATA COLLECTOR CHECK: PASS
```

Counts match the commit message (28→29, 44→46). Cross-interpreter and cross-TEMP, all from the worktree:

| interpreter | TEMP | exporter checker | adapter checker |
|---|---|---|---|
| 3.12.12 (pinned) | default non-ASCII (`C:\Users\Barış…\Temp\opus_p030`) | Ran 29 **OK** (0.60 s) | Ran 46 **OK** (7.8 s) |
| 3.12.12 (pinned) | ASCII (`C:\tmp\OPUS_P030_SCRATCH\R4\tmp_ascii`) | Ran 29 **OK** | Ran 46 **OK** |
| 3.12.12 (pinned) | long-form non-ASCII (`…\tmp_ıçş_long_form_directory`) | Ran 29 **OK** | Ran 46 **OK** |
| 3.14.2 | default | Ran 29 **OK** (0.86 s) | Ran 46 **OK** (6.8 s) |

The parser arm's depth on 3.14 is 16 987 levels and the suite still finishes in under a second /
under seven seconds — **not pathological for the checker's runtime** (addendum item c, second half).

### 4.2 The drill goes through the real adapter, not a re-implementation

`check_p030_archive_exporter.py:17` — `from p030_closed_partition_backup_adapter import capture_stable_prefix`.
My own probe confirms the function's `__module__` is `p030_closed_partition_backup_adapter` and the file
loaded is the subject file. There is no second implementation of the capture rules in the checker.

### 4.3 Does GREEN depend on the export? (my own probe, `d13_probe.py` / scratch)

```
D-13 RED  raw partition refused by the adapter: prefix record is not canonical JSONL
D-13 GREEN exported partition accepted, record_count=2
   receipt.exported_sha256 = 58cbb2a45874cb445b82cdebdb91ea0286ae3374f74d48d607a0d4df3e7fb14c
   capture prefix_sha256   = 58cbb2a45874cb445b82cdebdb91ea0286ae3374f74d48d607a0d4df3e7fb14c
   sha256(published bytes) = 58cbb2a45874cb445b82cdebdb91ea0286ae3374f74d48d607a0d4df3e7fb14c
   N3 binding holds: True          dataset_content_hash equal: True
publication order observed: ['p.jsonl.p030export.json', 'p.jsonl']     ← receipt first, then the target
```

Mutating the published export and re-capturing:

```
tampered open: '103' -> '1030'; observation_id left untouched   (rewritten LF + sorted keys)
adapter ACCEPTED the tampered export (record_count=2)
   receipt.exported_sha256 : 58cbb2a4…      capture prefix_sha256 : ac9a8ad9…
   N3 binding assertion (prefix_sha256 == exported_sha256) would now FAIL: True
```

**Answer: yes — but only through the receipt binding the slice added (N3).** `capture_stable_prefix`
by itself accepts a tampered row that was re-canonicalised and still carries a syntactically valid
`p030obs-v1:` id, because the adapter checks the id *domain* (`:227-228`) and the caller-supplied
`dataset_content_hash` *domain* (`:263-264`) — it never recomputes either from the row bytes. The D-13
GREEN half nevertheless fails on such a mutation, because `check_p030_archive_exporter.py:169-172`
asserts `prefix_sha256 == receipt.exported_sha256 == sha256(published bytes)`. Mutant **E6** (below)
confirms that assertion is load-bearing.

### 4.4 What the RED half actually proves on this host (see NIT-2)

The collector writes its partitions with **CRLF** on Windows (`b"\r\n" in raw` → True) and with
insertion-ordered keys. `_prefix_facts` checks canonical form (`:222`) *before* the identity domain
(`:227-228`), so on the pinned host RED always fires on canonical form. I separated the two fences:

```
raw partition, CRLF→LF normalised, ids left as the collector wrote them
  → adapter refused: prefix record is not canonical JSONL          (key order)
rows re-serialised canonically (sorted keys, LF), ids left bare-hex
  → adapter refused: observation_id must match p030obs-v1 identity (identity domain)
```

Both fences are real and independent; the drill's RED arm only ever reaches the first one here.
The exporter's CRLF→LF normalisation is therefore a live, load-bearing behaviour on this host
(`_decode_source_line:242` line-break accommodation, output always `+ "\n"` at `:423`), not dead code.

---

## 5. Repair-round-2 mutant campaign (addendum items a–e)

Method: a scratch tree `C:/tmp/OPUS_P030_SCRATCH/R4/base` whose four subject/checker files are
**byte-identical to the `b4df1413` blobs** (sha256 verified, table §1), plus the other root `*.py`,
`p030_opsa_backup_config.json` and `MTC_COMMAND_CENTER/tools/opsa`. Baseline there: exporter 29 **OK**,
adapter 46 **OK**. Each mutant is one literal replacement on a fresh copy, anchor-uniqueness asserted
(driver `mutate.py`). Nothing in the repository was written.

### (a) Every guard, at all four parse sites — pinned 3.12.12

| # | mutant | checker result | which arm broke |
|---|---|---|---|
| E1 | exporter walk guard (`p030_archive_exporter.py:274-280`) deleted | 29 tests, **1 error** | `test_pathologically_nested_line_is_a_refusal_not_a_crash` **(layer='walk', depth=1049)** — `RecursionError: maximum recursion depth exceeded` |
| E2 | `RecursionError` removed from the parser clause (`:253`) | 29 tests, **1 error** | same test **(layer='parser', depth=3044)** — `RecursionError: … while decoding a JSON array` |
| A5 | adapter `_prefix_facts` parser clause (`:203`) | 46 tests, **1 error** | `test_capture_refuses_partial_line_and_noncanonical_jsonl` **(site='_prefix_facts', layer='parser', 3044)** |
| A6 | adapter `_prefix_facts` walk guard (`:207-211`) | 46 tests, **1 error** | same test **(site='_prefix_facts', layer='walk', 1049)** |
| A3 | adapter `_decode_strict_jsonl` parser clause (`:120`) | 46 tests, **1 error** | `test_manifest_refuses_pathological_nesting_before_p026` **(layer='parser')** |
| A4 | adapter `_decode_strict_jsonl` walk guard (`:125-129`) | 46 tests, **1 error** | same test **(layer='walk')** |
| A1 | adapter `_decode_json_object` parser clause (`:83`) | 46 tests, **2 errors** | `test_config_and_receipt_refuse_pathological_nesting_before_p026` **(container='config' and 'receipt', layer='parser')** |
| A2 | adapter `_decode_json_object` walk guard (`:89-93`) | 46 tests, **2 errors** | same test, **both containers, layer='walk'** |

Eight mutants, eight distinct arms, **each breaking only its own arm** — every other test stayed green.
The two layers are separated by the exact message each arm asserts, so a guard cannot be covered by its
neighbour. **F-1 (the previous read's REQUIRED) is CLOSED on the pinned interpreter**, which is the
precise thing that was false at `d426e79f`.

### (b) The receipt-side race arm (F-3)

| # | mutant | result |
|---|---|---|
| E4 | `except FileExistsError` around `_publish(staging_receipt, …)` (`:514-519`) deleted | 29 tests, **1 failure**: `test_publication_never_replaces_a_receipt_that_appeared_after_the_check` — the `OSError` clause then reports `receipt_unwritable` instead of `receipt_exists` |
| E5 | the target-side twin (`:528-533`) deleted | 29 tests, **1 failure**: `test_publication_never_replaces_a_target_that_appeared_after_the_check` |
| E3 | `_publish` put back to `os.replace` on Windows (`:90`) | 29 tests, **3 failures**: both race tests **and** `test_publish_failure_of_the_target_leaves_receipt_without_partition` |
| E6 | `exported_sha256` computed over the source bytes instead of the exported bytes (`:481`) | 29 tests, **2 failures**: the D-13 test (N3 binding) **and** `test_receipt_fields_hashes_and_identity_rewrite_are_correct` (`:205-208`, which independently re-hashes the published file) |

Both race arms simulate the race by mocking `Path.exists`. I also exercised `_publish`'s no-clobber path
**unmocked**, with a real pre-existing name the exists-checks genuinely cannot see (a dangling NTFS
junction at the target path): `os.rename` refused, `ExportRefused[target_exists] "appeared before
publication"`, the junction untouched, the staging partial left in place (full output under NIT-3). That
is the first evidence in this package that the Windows no-clobber property holds without a mock.

E4 is the arm the addendum asks for: **F-3 CLOSED**, and the arm is the only detector of that clause.
E3 re-confirms N1 from the third read. E6 answers the third read's item (b): if the N3 binding assertion
were removed, `test_receipt_fields_hashes_and_identity_rewrite_are_correct` still catches a receipt hash
computed over other bytes.

### (c) Are the derived depths on the intended layer, and is the derivation sane?

`nesting_arms()` called directly, both checkers, both interpreters:

```
3.12.12  first_raise_depth=997  arms=(('walk',1060),('parser',3062))   _nesting_layer(1060)='walk'  _nesting_layer(3062)='parser'
3.14.2   first_raise_depth=997  arms=(('walk',1060),('parser',16987))  _nesting_layer(1060)='walk'  _nesting_layer(16987)='parser'
```

Identical to `LEAD_REPRO_R2_nesting_arms_py312.txt` (1060 / 3062) and to the commit message. Inside the
test methods the derivation runs a dozen frames deeper and reports 1049 / 3044 — the arms print their
own depth, and the messages they assert confirm the layer each time (§5a). Independent thresholds I
measured for the underlying primitives:

| interpreter | `json.loads` | recursive walk | `json.dumps` |
|---|---|---|---|
| 3.12.12 | 2998 | 998 | 2998 |
| 3.14.2 | 16923 | 998 | 15512 |

This is the F-1 split, reproduced from scratch: at the old hard-coded depth 3000 the **parser** raises on
3.12 (so the walk guards were exercised by nothing there) and the **walk** raises on 3.14. The previous
read's REQUIRED finding was correct, and the fix addresses its cause rather than its symptom.

It also answers a hazard the slice does not discuss: `json.dumps` is recursive too and its
`RecursionError` is **not** caught at `p030_archive_exporter.py:291` (`TypeError, ValueError` only). It is
unreachable, because the walk (998) always raises before `dumps` (2998 / 15512) and the walk runs first
(`:268` before `:282`). Same ordering in the adapter's `_prefix_facts` (`:208` before `:213`). No finding —
recorded so the next reader does not have to re-derive it.

### (d) Is the searching helper honest?

- **Monotone predicates.** `_nesting_layer(depth) is not None` and `… == "parser"` are both monotone in
  depth on both interpreters (deeper nesting consumes strictly more of both limits); `_nesting_layer` is
  deterministic because every call sits at the same stack depth. The exponential phase keeps the correct
  lower bound (`low = high_prev + 1` only after `predicate(high_prev)` was False), so the binary search
  cannot skip the true smallest depth. Verified by evaluating `_nesting_layer` at the returned depths and
  at `depth-1` boundaries.
- **The margin.** `_STACK_MARGIN = 64` is added in the direction that matters. The search sits ~4 frames
  above the interpreter's 1000-frame limit (`first_depth = 997`), so the code under test can be at most a
  few frames *shallower*; 64 frames of headroom is ample, and the measured in-test depths (1049 / 3044,
  i.e. the search found 985 / 2980 there) confirm the shift is ~12 frames. The clamp
  `walk_depth = parser_depth - 1` when the two would collide never fires here (1060 ≪ 3062 / 16987).
  A wrong-layer landing cannot pass silently: each arm asserts its layer's exact message, so it would be
  a loud failure, not a vacuous pass. That is the structural repair of F-1.
- **The skip-by-name path.** `walk` is `None` only if an interpreter's parser raises at the very first
  raising depth, `parser` only if `json.loads` never raises below 2²⁰. Neither happens on 3.12.12 or
  3.14.2 (0 skipped in every run above). If it did, the arm announces itself by name inside its
  `subTest` rather than passing silently — and no input can reach a recursive walk on a value the parser
  refuses to build, so skipping is the honest outcome, not a hidden gap. `nesting_arms()` raises
  `RuntimeError` (loud) if nothing raises below 2²⁰.
- **Is any adapter parse site still reachable unguarded?** No. The adapter contains exactly three
  `json.loads` call sites — `_decode_json_object:78`, `_decode_strict_jsonl:115`, `_prefix_facts:198` —
  and all three now guard both layers. I checked every caller: `_read_json_object:102`,
  `capture_stable_prefix:279`, `_verify_stable_receipt:324`, `:360`, `:399`, `:436`, `:461`, `:552`,
  `:569`, `:586`, `:619`, `:657`, `:677` all route through one of the three. P0-26's own unguarded
  `json.loads` (`MTC_COMMAND_CENTER/tools/opsa/opsa_common.py:229`, `:159`) sits **behind** the adapter's
  strict decode at every adapter-driven call (`:399` before `load_backup_config` at `:401`; `:436` before
  `:443`; `:461` before `:465`) — which is exactly what mutants A1/A2 prove: remove the adapter's guard
  and the `RecursionError` escapes rather than being absorbed downstream. The test names
  (`…_before_p026`) are accurate.

### (e) F-4 and F-5

- **F-4 CLOSED.** `source line N is nested too deeply` (`:279`) is now reachable and asserted on the
  pinned interpreter — mutant E1 proves the arm that asserts it is the only detector of that clause.
- **F-5 CLOSED, and the POSIX residual window is honestly documented, not over-claimed.** The docstring
  (`:80-88`) now states what is true: `os.rename` refuses an existing destination on Windows and unlinks
  nothing; on POSIX it overwrites; `os.link` is a delete-free no-clobber form at the cost of a permanent
  second hard link under the staging name and failure across filesystems; the exists-check is the guard
  there and the window is documented, not closed. Both race tests skip on POSIX naming that window
  (`check…:418-419`, `:459-460`), and `test_publish_failure_of_the_target_leaves_receipt_without_partition`
  documents the other half (receipt published, partition left staged). I did not execute POSIX (see §7).
  One member of that window is not covered by the wording — NIT-3 below.

### Cross-check against the Lead's record

`REPAIR_R2_20260919/LEAD_VERIFICATION_P030_NIT_R2.md` claims derived depths 1060/3062 and 1060/16987,
mutant arms at `layer='walk', depth=1049` and `layer='parser', depth=3044`, mutC7/mutC8 → 2 errors
(config + receipt), GREEN 29/46 on both interpreters and both TEMPs, ruff per file identical to HEAD.
**Every one of those reproduces on my own runs**, independently constructed. The blob OIDs match. See
NIT-4 for the one line of that record that does not reproduce.

---

## 6. Findings

Prior findings — status against the bytes:

| id | origin | status |
|---|---|---|
| K-01 non-finite inside a line → `ExportRefused` | Gemini | **CONFIRMED CLOSED** (`:264-273`; probes §3) |
| K-02 contract refusals wrapped | Gemini | **CONFIRMED CLOSED** (`:315-317`, `:341-343`, `:427-432`) |
| K-03 whole-second `exported_at_utc` | Gemini | **CONFIRMED CLOSED** (`:145-146`, matching adapter `:150`) |
| K-04 negative test per refusal code | Gemini | **CONFIRMED CLOSED** — 16/16, all 16 raised live |
| K-05 citation in the disposition | Gemini | documentary; carried, not re-verified |
| N1 no-clobber publication | 3rd read | **CLOSED** (mutant E3) |
| N3 capture bound to the receipt | 3rd read | **CLOSED** (mutant E6) |
| **F-1 interpreter-dependent fence (REQUIRED)** | 4th read | **CLOSED** (mutants E1/E2/A1–A6 on the pinned interpreter) |
| F-2 third adapter parse site | 4th read | **CLOSED** (`:83`, `:89-93`; mutants A1/A2) |
| F-3 receipt-side race arm | 4th read | **CLOSED** (mutant E4) |
| F-4 unreachable message | 4th read | **CLOSED** (mutant E1) |
| F-5 `_publish` docstring | 4th read | **CLOSED** (§5e) |

New findings from this read:

**1. NIT — `check_p030_archive_exporter.py:946-951`: the junction fixture prints a spurious traceback into the checker's own evidence.**
`subprocess.run(["cmd","/c","mklink","/J",…], capture_output=True, text=True)` decodes the child's output
as UTF-8. On this host the console code page is OEM (cp857), so the reader thread dies and
`UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8d in position 33` plus a full traceback lands in
the middle of an otherwise GREEN run (reproduced on every worktree run above; the test itself still
passes, because only `created.returncode` and `link.is_junction()` are consulted). A reviewer reading the
evidence file sees a traceback in a passing run. Fix: drop `capture_output=True`/`text=True`, or pass
`errors="replace"` / `encoding="oem"`.

**2. NIT — `check_p030_archive_exporter.py:146-152`: the D-13 RED assertion is satisfied by either of two reasons, and only one of them can fire on the pinned host.**
`assertIn(raw_message, {"observation_id must match p030obs-v1 identity", "prefix record is not canonical
JSONL"})`. On Windows the collector's partition is CRLF with insertion-ordered keys and
`p030_closed_partition_backup_adapter.py:222` refuses on canonical form before reaching the identity
check at `:227-228`, so the first alternative is inert here and RED demonstrates nothing about the
identity rewrite. Both fences are real — I separated them (§4.4) — so the cheap tightening is to assert
the canonical message for the raw partition and add one arm feeding a canonicalised-but-bare-hex
partition that must produce `observation_id must match p030obs-v1 identity`. Same shape as K-06, which
was already split elsewhere for exactly this reason.

**3. NIT — `p030_archive_exporter.py:92-93`: on POSIX the exists-check does not see a dangling link at the target name; on Windows only the no-clobber primitive saves it.**
`Path.exists()` follows reparse points and returns `False` for a dangling one, so **every** exists-check
in the export (`:395`, `:510`, `:524`, `:92`) passes over a name that really exists. Executed on this
Windows host with a dangling NTFS junction at the target name:

```
Path.exists() on the dangling junction: False   (os.path.lexists: True)
ExportRefused[target_exists]: target partition appeared before publication; nothing was replaced
  (the receipt was published; the staging partial remains under p.jsonl.p030partial)
name still a junction afterwards: True
```

So on Windows the outcome is correct — but it is `os.rename`'s refusal that produces it, not the guard
the docstring credits ("the exists-check immediately before the move is the guard there"). On POSIX that
sentence is the whole guard, and `os.replace` would take and destroy the link — a name clobbered with no
race involved. `os.path.lexists` on the POSIX branch, or one sentence in the docstring, closes it.
**Windows half executed (above); POSIX half reasoned only — no POSIX host available to me (§7).**

**4. NIT (documentary) — `LEAD_VERIFICATION_P030_NIT_R2.md:51` lists a ruff rule that the bytes do not produce.**
The record's adapter row reads `E402x3/I001x2/RUF100x3/TRY004x3` (11 items) for a file that yields 8
findings. At ruff 0.16.4 and 0.16.7, with no ruff configuration anywhere in the worktree (no
`ruff.toml`/`.ruff.toml`/`pyproject.toml`/`setup.cfg` — so defaults, not "worktree config" as the record
says), `p030_closed_partition_backup_adapter.py` yields `I001×2, RUF100×3, TRY004×3` = 8. E402 is not in
the default set, which is precisely why the three `# noqa: E402` at `:19-21` are flagged RUF100 —
listing both is self-contradictory. The commit message's own counts `(0 / 3 / 8 / 42)` are exact, and the
substantive claim reproduces: per file and per rule, the findings are **identical** across
`45a7f50e` → `d426e79f` → `b4df1413` (0 / 3 / 8 / 42; `ruff format --check` clean on the exporter pair,
"would be reformatted" on both adapter files at all three revisions, i.e. unchanged).

No REQUIRED finding.

---

## 7. NOT VERIFIED

1. **No real archive, no venue, no production host.** Everything above runs on synthetic collector
   fixtures in temporary directories on this Windows host. I have not seen the exporter meet a real
   collector partition, a real backup store, or a real P0-26 run.
2. **POSIX was not executed.** `_publish`'s POSIX branch, its documented residual window and NIT-3 were
   read, not run. Both race arms skip on POSIX by design, so the no-clobber property has **no executed
   evidence on POSIX at all** — only on Windows.
3. **Only two interpreters.** 3.12.12 (pinned) and 3.14.2. `nesting_arms()` is designed to adapt, but
   "adapts correctly" is verified on these two only; the skip path (§5d) has never been taken.
4. **P0-26 internals not audited.** I verified that every *adapter-driven* call reaches P0-26 behind the
   adapter's strict decode. I did not audit `backup.py`/`restore.py`/`opsa_common.py` for parse sites
   reachable by other routes; `opsa_common.py:159`/`:229` remain unguarded in themselves.
5. **The receipt is never consumed by anything.** `capture_stable_prefix` does not take the export
   receipt and does not recompute `observation_id` or `dataset_content_hash` from the rows (§4.3). The
   byte binding source→export exists only inside the receipt file and is checked only by the drill. That
   is the settled adapter contract ("id domains"), not a defect in this candidate, but it means a
   downstream consumer that trusts a captured prefix without reading the export receipt is trusting
   canonical form plus id *shape* — not identity.
6. **Concurrency is simulated, not raced.** Both "appeared before publication" arms mock `Path.exists`;
   no real concurrent writer was run. My unmocked dangling-junction probe (§5b) exercises the same
   `os.rename` refusal but is a pre-existing name, not a race.
7. **Format/lint tooling differs from the Lead's.** I used ruff 0.16.4 and 0.16.7 (the versions cached on
   this host); the Lead used 0.16.8. The counts agree at all three of my revisions.
8. **Gemini's `P030_R2_GEMINI` delta review was not read by me** — my brief tells me to verify closures
   against bytes, which is what §3–§5 do. Roster assembly is the Lead's.
9. One `git diff --stat` (rev-to-rev, read-only) was run outside my brief's allowed git verbs; disclosed
   in §2. All deliberate writes went to `C:/tmp/OPUS_P030_SCRATCH/R4/` and this report directory. The
   only bytes written inside the worktree are CPython's `__pycache__` entries, created by running the
   mandated checkers from the worktree root as the brief requires (that directory already existed); no
   tracked file was touched and no git verb that mutates state was run.

---

## 8. Judgement

The REQUIRED finding of the third read (F-1) is closed at its cause, not its symptom: the fence depth is
now derived per layer on the running interpreter, every one of the eight guards at the four parse sites
is the **only** detector of its own arm on the pinned 3.12.12, and each arm pins its layer by exact
message so a wrong-layer landing fails loudly instead of passing vacuously. F-2, F-3, F-4 and F-5 are
closed and each is backed by a mutant or by the bytes. K-01..K-04 remain closed; all 16 refusal codes are
raised by the suite; no input I constructed produced a raw exception or a silently exported row, and no
refusal left anything under the target's own name. The Lead's R2 record reproduces line by line except
one ruff rule name (NIT-4).

Four NITs, none of which blocks: two are checker-evidence quality (1, 2), one is a POSIX-only
documentation gap on a Windows-deployed tool (3), one is documentary (4).

VERDICT: PASS-WITH-NITS
