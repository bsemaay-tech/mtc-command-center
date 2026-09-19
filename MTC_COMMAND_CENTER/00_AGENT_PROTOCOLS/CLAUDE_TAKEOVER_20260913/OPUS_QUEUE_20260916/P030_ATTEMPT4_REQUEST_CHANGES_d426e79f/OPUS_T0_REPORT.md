# T0 exact-Opus review (attempt 4) — WP-P0-30 Shape-B archive exporter, candidate `d426e79f`

Reviewer: exact `claude-opus-5`, xhigh. FIRST read of the NIT slice N1-N5/F8 (third exact-Opus read
of the package). All commands below were run by me on this host; no delegation, no sub-agents.

- Worktree (read-only): `C:/tmp/P030_INTEGRATION_20260913`, cwd for every checker run.
- Pinned interpreter: `C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe` → `Python 3.12.12`.
- Scratch (RED/mutant arms only): `C:/tmp/OPUS_P030_SCRATCH/attempt4/`.

---

## 1. Verified identities (COMPUTED)

```
$ git -c safe.directory=* -C C:/tmp/P030_INTEGRATION_20260913 rev-parse HEAD
d426e79f4c7813c6cdf40b6a1049ced6a58a5de5
$ git -c safe.directory=* show -s --format='%H parents=%P' d426e79f
d426e79f4c7813c6cdf40b6a1049ced6a58a5de5 parents=45a7f50eac009646bde1d80bcf66b1d14e6d72e0
```

The candidate's parent **is** `45a7f50e`, so `git show d426e79f` is the complete delta of the slice
(4 files, +157/−18 — matches the addendum).

The worktree checks text out as **CRLF**; the blob is LF. Both forms are given; the LF digest is the
authoritative one (permanent lesson: hash blobs, not CRLF checkouts). I verified that every
working-tree file, LF-normalised, is byte-equal to its `d426e79f` blob — nothing uncommitted.

| File | sha256 (blob / LF, authoritative) | sha256 (working tree, CRLF) |
|---|---|---|
| `p030_archive_exporter.py` | `8d55a8d6388fd173df4383658c8fe10c101993fde46bc4ad7cd6a2401f902686` | `F2BDD797A4D3079FF69D01E3E3D220A1D44864B8611FCBEDD98E710C954BE587` |
| `check_p030_archive_exporter.py` | `286dbc524cd00906421b252b1ba2eb1828474580a0c4dad332981b3c5134c800` | `803CA32C1D547FFD46EBD5CD75E4F4CCD9C1DC953B9439A4D9893EBF130AE474` |
| `p030_closed_partition_backup_adapter.py` | `f47dab5f5d930268529ac7c7eda20d9720996b04209057e0698319514ee35ffb` | `B38B78029848A2FE682FF34759D0E27A1C7D6CA7D0384BE37E36CCEED8739047` |
| `check_p030_closed_partition_backup_adapter.py` | `b71eccb10bd54f8a7740829d6b6cd896067da55c835f36b16d5e590f2fa1705d` | `AE709E54BB16BB7108372B6F46F254334A13F3BA79A21C12D4C0F6B984BEBD90` |
| `p030_market_data_contracts.py` (unchanged) | `433db0e6b2f86f8c0b3bd4375a0fbb1112f331a91284a6d4d1744760c2e3fca3` | — |
| `market_data_collector.py` (must be untouched) | `2819b248be23ce3c59c2d97fcb3968fef91966f635585287b292d466ce80018e` | — |

**Collector untouched — proven, not assumed:** the blob of `market_data_collector.py` is
`2819b248…` at the base `f42fd540`, at `45a7f50e` and at `d426e79f` — byte-identical at all three.

Pre-slice comparison bytes used throughout: `45a7f50e` blobs
(`p030_archive_exporter.py` `1bb9fb66…`, `check_p030_archive_exporter.py` `4e2d2913…`,
`p030_closed_partition_backup_adapter.py` `2cba917e…`, `check_…_adapter.py` `2dcd92dd…`).

---

## 2. Shape-B conformance table

Line numbers are the working-tree/blob line numbers (identical; only line endings differ).

| Shape-B promise | file:line | EQUAL / DIFFERENT |
|---|---|---|
| Collector keeps writing its raw partitions; the exporter is a separate component | `market_data_collector.py` blob identical at `f42fd540`, `45a7f50e`, `d426e79f` | EQUAL |
| Single byte read of the source partition | `p030_archive_exporter.py:220-237` (`stat` + one `open("rb")`, size cross-check, `short_read`/`empty_partition` refusals) | EQUAL |
| Source never mutated or re-read after that read | `p030_archive_exporter.py:399` is the only read; rows/hash/receipt all derive from `source_bytes` (`:401-406`, `:470`) — no second `open`, no write to the source tree | EQUAL |
| Re-identification goes through the contracts module | `:311` `producer_payload_hash`, `:337` `observation_id`, `:426` `dataset_content_hash` | EQUAL |
| No home-grown ids | `:66-68` regexes only *validate shape*; every emitted id comes from the contracts module (`:334`, `:353`) | EQUAL |
| Canonical output: sorted keys, LF, one row per line | `:410-422` (`sort_keys=True`, `separators=(",",":")`, `allow_nan=False`, `+ "\n"`) | EQUAL |
| Exclusive create + byte re-read equals what was written | `:442` `open("xb")` + `fsync`; `:455-464` re-read compare → `target_verify_failed` | EQUAL (both now happen on the staging name; see next row) |
| Nothing under the target's own name until verify + receipt succeeded | `:429-453` staging write, `:504-535` publish receipt then target | EQUAL |
| Publication never replaces an existing destination | `_publish` `:79-93` — `os.rename` on Windows (no-clobber, nothing unlinked); exists-check + `os.replace` on POSIX with the window documented | EQUAL on this host (Windows); POSIX window documented, not closed |
| `os.replace`/`os.rename` is the only publication path; no delete path anywhere | grep of the whole module for `unlink|os.remove|rmtree|shutil`: only two *comment* hits (`:84`, `:85`) | EQUAL |
| Receipt binds source bytes digest → target bytes digest → row counts | `ExportReceipt` `:37-63`; filled `:466-482` (`source_sha256`, `exported_sha256`, both counts, `dataset_content_hash`, `exporter_sha256` LF-normalised `:472-476`) | EQUAL |
| Adapter's whole-second UTC `Z` rule is what the exporter enforces | exporter `_utc_z` `:124-146` (`:144-145` `microsecond` → refuse) vs adapter `_utc_z` `p030_closed_partition_backup_adapter.py:136-144` (`:143-144`) | EQUAL |
| Adapter's canonical-relative-POSIX + no-link rule on the same field | exporter `_source_rel` `:149-217` (percent-escape loop `:169-179`, spelling `:180-196`, link/junction walk `:197-207`, resolved-form `:208-216`) vs adapter `_canonical_relative_posix` `:147-170` + `_refuse_source_links` `:173-183` | EQUAL (verified by probe: both refuse `..`, `%2e%2e` and a junction component — see §5(d)) |
| Id domains | exporter `:67-68` (`p030payload-v1:`, `p030obs-v1:`) vs adapter `:47-48` (`p030ds-v1:`, `p030obs-v1:`) | EQUAL |
| No network, no subprocess in the exporter module | imports `hashlib, json, math, os, re, dataclasses, datetime, pathlib, typing, urllib.parse` only (`:5-26`); `NETWORK ATTEMPTS: 0` in both sibling checkers | EQUAL |
| Writes confined to the target + receipt (+ their staging names) | `:441` `mkdir(parents=True, exist_ok=True)` of the target's parent, then only `staging_target`/`staging_receipt`/`target`/`receipt` | EQUAL |

---

## 3. Refusal-code table

**Counts reproduced from the bytes** with an AST walk over every `_refuse(...)` / `ExportRefused(...)`
call and every `self.assertEqual(caught.exception.code, "...")` / `self._refused("...", …)` in the
checker (script: `C:/tmp/OPUS_P030_SCRATCH/attempt4/codes.py`):

- at `daf6a43b`: **16 codes, 5 with a negative test → 11 of 16 missing** — Gemini's count reproduced exactly.
- at `d426e79f`: **16 codes, 16 with a negative test → 0 missing** — the O9FIX claim reproduced exactly.
- No asserted code exists that is not a real code (no test asserts a code the module cannot raise).

| # | Code | Trigger (site) | Negative test | My probe result |
|---|---|---|---|---|
| 1 | `target_exists` | target present `:392`; staging leftover `:435`; pre-publish re-check `:521`; `xb` collision `:447`; publication race `:525` | `check:169-184`, `:669-676`, `:339-378` | Pre-existing target refused, foreign bytes intact; leftover `.p030partial` refused on the second run; race arm refuses and **does not replace** (§5(a)) |
| 2 | `receipt_exists` | receipt present `:395`; pre-publish re-check `:507`; `xb` collision `:499`; publication race `:511` | `check:567-581` | Refused; target never created |
| 3 | `invalid_timestamp` | non-`Z`/non-str `:126`; unparseable `:133`; naive `:138`; **sub-second `:145`** | `check:398-425` | `2026-09-14T00:00:00.500Z` → `invalid_timestamp`, nothing written |
| 4 | `source_outside_root` | not under root `:165`; percent-escape `:176`; non-canonical spelling `:193`; symlink/junction `:200`; resolved escape `:213` | `check:427-437`, `:747-765`, `:776-801`, `:803-839` | `..` traversal, `%2e%2e`, NTFS junction all refused; the adapter refuses the same three paths |
| 5 | `source_unreadable` | `OSError` on stat/open `:228` | `check:439-444` | Missing file refused |
| 6 | `short_read` | size mismatch `:232`; no trailing LF `:236` | `check:446-471` (both arms) | Both refused |
| 7 | `empty_partition` | zero bytes `:234`; no rows `:408` | `check:202-216` | Refused |
| 8 | `source_line_invalid` | parse/decode/duplicate-key/**RecursionError** `:256`; non-object `:260`; non-finite number `:269`; **deep-nesting in the walk `:274`** | `check:186-200`, `:473-485`, `:380-396` | `1e999`, `-1e999` nested, `NaN`, `Infinity`, duplicate key, depth 1200 and depth 3000 all refused; **nothing** under the target dir in every case |
| 9 | `source_line_noncanonical` | `dumps` raises `:288`; bytes differ `:293` | `check:487-492` | `{"open": 1}` refused |
| 10 | `source_fields_mismatch` | missing/extra fields `:304` | `check:494-507` | Refused |
| 11 | `contract_refused` | payload hash `:313`; observation id `:339`; slice hash `:428` | `check:509-522`, `:524-550` | Row-level (`open="not-a-decimal"`) and slice-level (duplicate obs id, `bar_close_time`) both refused, nothing written |
| 12 | `identity_mismatch` | prefixed payload hash `:320`; neither-form `:328`; prefixed obs id `:343`; neither-form `:348` | `check:269-294` | Refused |
| 13 | `mixed_dataset_descriptor` | descriptor field disagrees `:371` | `check:552-565` | Refused |
| 14 | `target_unwritable` | staging `OSError` `:449`; publish `OSError` `:531` | `check:583-607`, `:631-677`, `:679-710` | ENOSPC mid-write → refusal; **no target, no receipt**; half bytes only under `.p030partial` |
| 15 | `target_verify_failed` | re-read `OSError` `:457`; bytes differ `:461` | `check:218-249` | Refused; target name never taken |
| 16 | `receipt_unwritable` | staging `OSError` `:501`; publish `OSError` `:517` | `check:609-629` | Refused; target name never taken (staging partial remains) |

**K-01..K-03 RED probes (brief §2) — can any of them produce an EXPORTED row?** No.
`C:/tmp/OPUS_P030_SCRATCH/attempt4/probe_k123_and_window.py`, cwd `…/attempt4/base`:

```
K-01 overflow 1e999                -> ExportRefused(source_line_invalid) files under target dir: []
K-01 nested -1e999                 -> ExportRefused(source_line_invalid) files under target dir: []
K-01 NaN literal                   -> ExportRefused(source_line_invalid) files under target dir: []
K-01 Infinity literal              -> ExportRefused(source_line_invalid) files under target dir: []
duplicate JSON key                 -> ExportRefused(source_line_invalid) files under target dir: []
K-02 contracts-refused row         -> ExportRefused(contract_refused)    files under target dir: []
K-02 slice: duplicate obs id       -> ExportRefused(contract_refused)    files under target dir: []
K-03 sub-second timestamp          -> ExportRefused(invalid_timestamp)   files under target dir: []
K-03 offset timestamp              -> ExportRefused(invalid_timestamp)   files under target dir: []
```

I also swept the recursion boundary (depths 985-1000) looking for a window where `json.loads` and the
non-finite walk both succeed but the canonical `json.dumps` raises `RecursionError` unguarded
(`:277-291` catches only `TypeError`/`ValueError`). **No such window exists on this interpreter**: the
walk refuses from depth 997 upward, `dumps` succeeds below it. At HEAD I could not produce a raw
exception from `export_partition` at any depth.

---

## 4. D-13 evidence

cwd `C:/tmp/P030_INTEGRATION_20260913`, pinned interpreter, exact output tails:

```
$ …/python.exe check_p030_archive_exporter.py
Ran 28 tests in 0.591s

OK
D-13 RED RAW REFUSAL: prefix record is not canonical JSONL
D-13 GREEN EXPORTED CAPTURE: PASS

$ …/python.exe check_p030_closed_partition_backup_adapter.py     (TEMP = C:\Users\BarışSemaay\AppData\Local\Temp\opus_p030 — the long-form NON-ASCII TEMP)
Ran 44 tests in 7.809s

OK

$ …/python.exe check_p030_market_data_contracts.py
TYPE/CANONICALIZATION REFUSALS: PASS
NETWORK ATTEMPTS: 0
P030 MARKET DATA CONTRACTS CHECK: PASS

$ …/python.exe check_market_data_collector.py
OFFLINE COLLECTOR LIFECYCLE (success + wait error): PASS
NETWORK ATTEMPTS: 0
MARKET DATA COLLECTOR CHECK: PASS
```

**The RED half is the real adapter, not a re-implementation:** `check_p030_archive_exporter.py:17`
imports `capture_stable_prefix` from `p030_closed_partition_backup_adapter` and calls it on the raw
collector partition (`:62-79`); the refusal text printed (`prefix record is not canonical JSONL`)
comes from `p030_closed_partition_backup_adapter.py:198`.

**GREEN depends on the export — my own mutation probe** (`probe_green_dependence.py`, cwd `…/base`):
export, then tamper with the published bytes and re-run the adapter capture.

```
untouched (control)                    -> CAPTURED  prefix_sha256==receipt.exported_sha256: True
one digit flipped in a value           -> CAPTURED  prefix_sha256==receipt.exported_sha256: False
pretty-printed (non-canonical)         -> ADAPTER REFUSED: prefix record is not canonical JSONL
keys re-ordered (unsorted)             -> ADAPTER REFUSED: prefix record is not canonical JSONL
trailing newline stripped              -> ADAPTER REFUSED: high-water prefix must end with newline
CRLF line endings                      -> ADAPTER REFUSED: prefix record is not canonical JSONL
identity prefix stripped (bare hex)    -> ADAPTER REFUSED: observation_id must match p030obs-v1 identity
```

This is the exact justification for N3 and it is real: the adapter alone accepts a **value-tampered**
row (it checks canonical form and the id *domain*, not id correctness), so before N3 the GREEN arm
could have passed on bytes that were not the exported bytes. With N3 (`check:96-99`) the capture is
pinned to `receipt.exported_sha256` **and** to `sha256(published bytes)`.

---

## 5. Mutants required by the addendum

All mutants are scratch copies under `C:/tmp/OPUS_P030_SCRATCH/attempt4/` (`base/` = unmutated copy
of the 25 root modules + `MTC_COMMAND_CENTER/tools/opsa` + `p030_opsa_backup_config.json`;
`base` runs **28 OK** and **44 OK**, so the harness itself is sound).

### (a) `_publish` back to `os.replace` on Windows — **race test must fail: it does**

`mutA/p030_archive_exporter.py:79-93` → `os.replace(staging, final)` unconditionally.

```
=== mutA === FAIL: test_publication_never_replaces_a_target_that_appeared_after_the_check
             FAIL: test_publish_failure_of_the_target_leaves_receipt_without_partition
             Ran 28 tests → FAILED (failures=2)
    AssertionError: ExportRefused not raised        (check_p030_archive_exporter.py:365)
```

Two failures — matches the Lead's record. I also ran the destructive form directly
(`probe_clobber.py`), which shows what the test only implies:

```
=== base ===  OUTCOME: ExportRefused(target_exists) target partition appeared before publication;
                       nothing was replaced (… staging partial remains under partition.jsonl.p030partial)
              FOREIGN INTACT: True    TARGET BYTES: b'{"foreign": true}\n'
=== mutA ===  OUTCOME: NO REFUSAL
              FOREIGN INTACT: False   TARGET BYTES: b'{"bar_close_time":1769906700000,…'
```

**N1 APPLIED and detected.** On this host the no-clobber guarantee is real (`os.rename` refuses,
nothing is unlinked). Publication order is receipt-then-target (`:504-535`), `_publish` is the only
publication path, and there is no delete code path anywhere in the module.

### (b) D-13 binding removed / receipt hash over other bytes

- `mutB1` = exporter `:477` computes `exported_sha256` over `source_bytes`
  → **2 failures**: the D-13 arm *and* `test_receipt_fields_hashes_and_identity_rewrite_are_correct`.
- `mutB2` = `mutB1` + the N3 assertions (`check:94-99`) deleted
  → **1 failure**: `test_receipt_fields_hashes…` (`check:132-135`) still catches it.

So the mutant the addendum names is **not** uniquely caught by N3 — the receipt-fields test catches it
either way. To find out whether N3 has independent value I built the mutant that only N3 can see:

- `mutB5` = adapter `:274` reports `prefix_sha256` over `prefix[:-1]` (the adapter stays internally
  self-consistent; the *exporter's* receipt no longer matches the capture)
  → **1 failure, and it is the N3 line**:

```
File "…/mutB5/check_p030_archive_exporter.py", line 96, in test_exported_collector_fixture_is_accepted_by_stable_prefix_adapter
    self.assertEqual(stable["prefix_sha256"], receipt.exported_sha256)
AssertionError: '50c1779f…' != '58cbb2a4…'
```

**N3 APPLIED and it is the sole detector of a producer/consumer byte divergence** — which is exactly
the binding the D-13 drill is for. (The record's characterisation of the mutant is imprecise, not
false; noted, not filed as a finding.)

### (c) Either walk guard removed — **the nesting arm does NOT error. This is finding F-1.**

| Mutant | What was removed | Suite result |
|---|---|---|
| `mutC1` | exporter walk guard `p030_archive_exporter.py:273-276` | exporter checker **Ran 28 — OK (mutant survives)** |
| `mutC2` | exporter parser clause `RecursionError` `:252` | exporter checker **1 error** (the nesting arm) |
| `mutC3` | adapter `_prefix_facts` walk guard `:201-205` | adapter checker **Ran 44 — OK (survives)** |
| `mutC4` | adapter `_decode_strict_jsonl` walk guard `:119-123` | adapter checker **Ran 44 — OK (survives)** |
| `mutC5` | adapter `_prefix_facts` parser clause `RecursionError` `:197` | adapter checker **1 error** |

Why: on this interpreter (`sys.getrecursionlimit() == 1000`) the depth at which each stage fails is

```
depth  50…990 : loads=OK  walk=OK   dumps=OK
depth 1000,1500: loads=OK  walk=RecursionError
depth 3000     : loads=RecursionError          ← both checkers' nesting arms use depth 3000
```

and through the real entry points (`probe_nesting.py`, cwd per mutant dir):

```
                       exporter                               adapter
base   depth=1200  ExportRefused(source_line_invalid)   ValueError(prefix record is not canonical JSONL)
base   depth=3000  ExportRefused(source_line_invalid)   ValueError(prefix record is not canonical JSONL)
mutC1  depth=1200  RAW RecursionError                   (guarded)
mutC1  depth=3000  ExportRefused(source_line_invalid)   (guarded)
mutC2  depth=3000  RAW RecursionError                   (guarded)
mutC3  depth=1200  (guarded)                            RAW RecursionError
```

**The shipped code is correct at every depth I measured** — nothing fails open, no raw exception
escapes `export_partition` or `capture_stable_prefix` at HEAD. What fails is the *evidence*: the
commit message's D026 line states

> the exporter walk guard removed -> RecursionError escapes (1 error); the adapter walk guard removed -> 1 error

and the addendum adds "a first parser-clause mutant SURVIVED". Both are **the inverse of what
reproduces here**: the parser clause is the guard the depth-3000 tests exercise, and the walk guard —
in all **three** places it exists — is exercised by nothing. See finding F-1.

### (d) Refusal codes, staging/verify/publish order, receipt fields, `exporter_sha256`, adapter rules — unchanged from `45a7f50e`

`git show d426e79f` is the whole delta (parent verified in §1). Inside it:

- refusal-code *set* unchanged (16 before and after; the slice adds two new raise **sites** reusing
  `target_exists` `:525` and `receipt_exists` `:511`, no new code);
- order unchanged: stage `:429-453` → re-read/verify `:454-464` → build receipt `:466-492` → stage
  receipt `:493-503` → publish receipt `:504-519` → publish target `:520-535`. Only `os.replace(…)`
  → `_publish(…)` plus the two `FileExistsError` arms changed;
- `ExportReceipt` fields and `as_dict()` (`:37-63`) untouched; `exporter_sha256` still the
  LF-normalised form (`:472-476`), asserted by `check:712-745` (CRLF-checkout simulation passes);
- adapter canonical-prefix rules untouched: `_canonical_relative_posix` `:147-170`,
  `_refuse_source_links` `:173-183`, the canonical re-serialisation compare in `_prefix_facts` and
  the `p030obs-v1` domain check are byte-identical to `45a7f50e`; the only adapter changes are the
  four `RecursionError` clauses. Verified against the `45a7f50e` blobs, not against the diff summary.
- containment parity still holds by probe: `..` traversal, `%2e%2e`, and an NTFS junction are refused
  `source_outside_root` by the exporter **and** refused by `capture_stable_prefix` on the same path
  (`check:747-765`, `:776-801`, `:803-839`, all green on this host — the junction arm did not skip).

**N5/F8 verified both ways.** Same adapter checker, same host, only the bytes and `TEMP` differ:

```
45a7f50e bytes, TEMP=C:\Users\BarışSemaay\…\Temp\opus_p030 (non-ASCII):
    FAIL: test_isolated_config_redirect_after_check_never_reaches_restore (defect='duplicate_backup_root')
    AssertionError: 0 != 1                 Ran 44 → FAILED (failures=1)      ← RED reproduced
45a7f50e bytes, TEMP=C:\tmp\OPUS_P030_SCRATCH\ascii_temp (ASCII):   Ran 44 → OK   (the defect hides)
d426e79f bytes, TEMP=…non-ASCII…:                                   Ran 44 → OK   ← GREEN
```

`check_p030_closed_partition_backup_adapter.py:850-860` is the fix and it is the honest one (anchor
and replacement both `ensure_ascii=False`, matching the writer). Also confirmed: exporter checker is
**26 tests at `45a7f50e`** → **28 at `d426e79f`**.

### (e) Is the POSIX residual window honestly documented, or over-claimed?

Honest, with one imprecision. `_publish` `:79-93` says plainly that on POSIX the exists-check
immediately before the move "is the guard there and the remaining window is documented, not closed",
the test skips on POSIX with that reason (`check:345-346`), and the commit message repeats it. Nothing
claims a guarantee the bytes do not deliver, and on this host (`os.name == "nt"`) the window does not
exist at all — proven in (a).

The imprecision is the parenthetical "the no-clobber forms (link + unlink, renameat2) either add a
delete path or are not portable": `os.link(staging, final)` alone is POSIX-portable and no-clobber
(`FileExistsError` if the destination exists) and needs **no** unlink if one accepts a leftover
staging hardlink — which is precisely the leftover this package already accepts everywhere else. So a
delete-free POSIX no-clobber form does exist; it costs a hardlink and fails across filesystems. Filed
as NIT F-5 (wording), not as a design objection.

---

## 6. Findings

Severity rule I applied (from the brief): REQUIRED = a wrong input can produce an exported row or
leave a consumable partition under an archive name, **or** an acceptance-bearing claim in the
candidate is not reproducible from the bytes. A raw exception with no partial left behind is a NIT.

### F-1 — REQUIRED — the N4 guard is untested at all three sites, and the slice's own mutation evidence is inverted

- `p030_archive_exporter.py:273-276` (walk guard), `p030_closed_partition_backup_adapter.py:119-123`
  and `:201-205` (walk guards) — deleting **any** of the three leaves both checkers fully green
  (`mutC1`: 28 OK; `mutC3`, `mutC4`: 44 OK).
- The cause is the depth the two new arms use: `check_p030_archive_exporter.py:386` and
  `check_p030_closed_partition_backup_adapter.py:175` both pick `depth = 3000`, where `json.loads`
  raises first, so only the **parser** clause is exercised (`mutC2`/`mutC5` → 1 error each).
- Consequently the commit message's D026 evidence — "the exporter walk guard removed -> RecursionError
  escapes (1 error); the adapter walk guard removed -> 1 error" — does not reproduce, and the
  addendum's "a first parser-clause mutant SURVIVED and is recorded as superseded" is the opposite of
  what happens here. Two of the five recorded mutant outcomes are inverted. (I could not read
  `P030_NIT_SLICE_20260918/LEAD_VERIFICATION_P030_NIT.md` — it does not exist on this host, see §7 —
  so I am reporting against the commit message, which is in the bytes.)
- **Not** a behavioural defect: at HEAD every depth refuses correctly, and the guarded code is right.
  The defect is that the slice's stated detection does not exist, on a guard that a future refactor
  can delete silently — the "delete it and the suite stays green" shape.
- Minimal repair: in both checkers add (or move) a nesting arm to a depth inside the walk's window —
  derived rather than hard-coded, e.g. raise the depth until `json.loads` succeeds and assert the
  refusal there; depth 1200 works on this interpreter. Then correct the D026 claim in the record so
  the second flagship is not handed an inverted mutation result.

### F-2 — NIT — the adapter has a *third* parse site with no `RecursionError` guard; the parity claim says "both"

`p030_closed_partition_backup_adapter.py:76-88` (`_decode_json_object`): neither `:83` (parser) nor
`:87` (walk) is guarded. It is reachable from the public API — `load_runnable_config` →
`_load_strict_config:393` → `_read_json_object` — and from the stable-prefix receipt reads (`:318`,
`:580`) and the isolated-config reads (`:430`, `:455`, `:613`). Probe (`probe_config_nesting.py`):

```
load_runnable_config depth=  900 -> ValueError(backup config is not runnable)
load_runnable_config depth= 1200 -> RAW RecursionError
load_runnable_config depth= 3000 -> RAW RecursionError
```

The commit message claims parity "in both parse sites of the closed-partition backup adapter" — there
are three. NIT because these paths are read-only (no partial is left) and the adapter is a consumer,
not the archive writer. Repair: the same two clauses at `:83`/`:87`, or say explicitly that the
config/receipt reader is out of scope for N4.

### F-3 — NIT — the receipt-side no-clobber arm is untested

`p030_archive_exporter.py:510-515` (the `receipt_exists` "appeared before publication" arm) has no
test: `mutD1` deletes it and the suite stays green (28 OK). Fail-closed either way — with the arm
removed the `FileExistsError` falls through to `except OSError` `:516` and surfaces as
`receipt_unwritable` — so the consequence is a wrong refusal *code*, not an overwrite. Repair: one
arm mirroring `check:339-378` with the receipt path mocked absent.

### F-4 — NIT — the exporter's `RecursionError` message is unreachable

`p030_archive_exporter.py:275` (`"source line {n} is nested too deeply"`) can only be produced in the
walk window (~997-1500 here); no test asserts it and the single nesting test asserts only
`"source line 3"`, which both arms produce. This is the message-level half of F-1; if F-1's arm is
added with an exact per-arm message (the K-06 pattern already used at `check:477-485`), F-4 closes
with it.

### F-5 — NIT — `_publish`'s POSIX docstring over-states the alternatives

`p030_archive_exporter.py:85-86`: "link + unlink, renameat2 — either add a delete path or are not
portable". `os.link` alone (no unlink, leftover staging hardlink) is a delete-free POSIX no-clobber
publication in the same shape this package already tolerates. Repair: one clause naming the real cost
(a permanent hardlink, and cross-filesystem failure) instead of implying no delete-free form exists.

### Status of the earlier findings

| Item | Verdict |
|---|---|
| K-01 (non-finite inside a line → `ExportRefused`, not raw `ValueError`) | **CONFIRMED CLOSED** — `1e999`, nested `-1e999`, `NaN`, `Infinity` all `source_line_invalid`, nothing written |
| K-02 (contract refusals → `contract_refused`) | **CONFIRMED CLOSED** — row-level and slice-level both wrapped (`:313`, `:339`, `:428`) |
| K-03 (sub-second `exported_at_utc` refused like the adapter) | **CONFIRMED CLOSED** — `:144-145` mirrors adapter `:143-144`; probed |
| K-04 (16 refusal codes with negative tests) | **CONFIRMED CLOSED** — 16/16 reproduced from the bytes; 11/16 missing at `daf6a43b` reproduced too |
| K-05 (report citation) | record-side only — see §7 |
| Attempt-1 finding 1 (refusal left a consumable partition) | **CONFIRMED CLOSED and still closed under the new publication path** — ENOSPC, verify-failure, receipt-failure and publish-failure all leave nothing under the target name |
| Attempt-1 finding 2 (`source_root` containment fail-open) | **CONFIRMED CLOSED** — `..`, `%2e%2e`, junction all refused, adapter agrees |
| N1 (no-clobber publication) | **APPLIED**, detected by `check:339-378` (mutant (a)) |
| N2 (staging comment claims only what the bytes support) | **APPLIED** — `:69-76` now says the name is the only protection; consistent with what I observe (a leftover `.p030partial` is not resolved as a partition by any consumer, though the P026 directory walk would copy it as an ordinary file — the comment does not claim otherwise) |
| N3 (capture bound to the receipt) | **APPLIED**, and the sole detector of a producer/consumer byte divergence (mutant (b)) |
| N4 (deep nesting refused) | **APPLIED IN CODE, NOT IN TESTS** — see F-1, F-2, F-4 |
| N5 / F8 (ASCII-independent checker anchor) | **APPLIED**, RED at `45a7f50e` under the non-ASCII `TEMP`, GREEN at HEAD |

---

## 7. NOT VERIFIED

- **No real archive, no production host.** Everything above ran against collector fixtures in `TEMP`
  on this Windows host. No live partition, no real backup root, no P026 run against real data.
- **POSIX behaviour.** `os.name == "nt"` here: the POSIX branch of `_publish` (`:91-93`) and the
  documented residual window were read, not executed. `check:345-346` skips there. A POSIX host must
  re-run this before anyone relies on the no-clobber property off Windows.
- **Symlink component.** I probed the NTFS **junction** arm (it ran, did not skip). A true symlink
  component needs developer mode/elevation and was not created.
- **Ruff.** Not installed in the pinned venv and not on this host's PATH, so
  "ruff findings per file identical to HEAD (0/3/8/42)" and the `ruff format --check` reflow proof of
  `53b43c21` are **unverified by me**. I read the formatting difference as cosmetic in the diff only.
- **Lead records for this slice.** `…/P030_NIT_SLICE_20260918/LEAD_VERIFICATION_P030_NIT.md` and the
  `P030_NIT_GEMINI` report named in the addendum **do not exist on this host** (searched all of
  `C:/CT13` for `*NIT*` and for the filename). F-1 is therefore stated against the commit message's
  own D026 line, which is in the bytes; if the Lead's file records something different, the
  discrepancy still needs resolving before the Sol read.
- **K-05** (a citation in `laneO9FIX_build/DISPOSITION_O9FIX.md`) is a record-side item; not re-checked.
- **Checker-side `subprocess`.** `check_p030_archive_exporter.py:8,815-820` shells out to
  `cmd /c mklink /J` to build the junction fixture. Pre-existing at `45a7f50e`, inside `TEMP`, and it
  skips cleanly when junctions are unavailable — flagged, not judged.
- **Adapter identity semantics.** `capture_stable_prefix` checks the `p030obs-v1` *domain* and
  canonical form but does not recompute identities, and it echoes the caller-supplied
  `dataset_content_hash` (my §4 probe: a value-tampered row is still captured). That is the adapter's
  unchanged, previously-reviewed contract and is out of scope here; it is the reason N3 matters.
- My verdict accepts nothing on its own; the Lead assembles the roster (exact Sol still outstanding).

VERDICT: REQUEST_CHANGES
