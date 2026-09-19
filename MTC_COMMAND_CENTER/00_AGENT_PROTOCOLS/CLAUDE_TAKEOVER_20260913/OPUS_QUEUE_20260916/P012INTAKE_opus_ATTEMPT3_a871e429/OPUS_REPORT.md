# Exact review — WP-P0-12 funding intake slice 4 (ACCEPTING half), candidate `a871e429` (T0 repair round 1)

Reviewer: exact `claude-opus-5`, xhigh. Second exact-Opus read, T0 repair round 1 of 3.
Subject: `C:/tmp/P012_INTAKE_20260915`, branch `feature/p012-funding-intake-adapter-20260915`.
Report status: **COMPLETE**.

---

## 0. Verified identities

Pin note: `opus/BRIEF.md` line 3 still carries the superseded sentence "if HEAD is not
`9ef072a8…` your verdict must be BLOCK", while the same file's own title, `REVIEW_BRIEF.md`
§Subject and the 2026-09-17 ADDENDUM all re-pin the candidate to `a871e429`. I reviewed
`a871e429` and record the observed HEAD below; the stale line is a NIT against the brief, not
against the code.

| item | value |
|---|---|
| COMPUTED HEAD | `a871e42965322d4fc66e317ef7067d6fca28972c` |
| parent (`HEAD^`) | `9ef072a8cbc83915679d0cfc4fb142fba449c8e0` |
| grandparent | `b667dbcc` (format-only), then `4c802e9b`, base `fcac0ac6` |

Blob OIDs (`git ls-tree`, all paths under `IBKR_PAPER_BRIDGE/`):

| file | `4c802e9b` | `9ef072a8` | `a871e429` (HEAD) |
|---|---|---|---|
| `tools/export_mtc_funding.py` | `f12570e7…` | `216b9cc3…` | **`8f639009…`** |
| `tools/funding_intake_adapter.py` | (absent) | `e0737289…` | `e0737289…` (unchanged) |
| `tests/test_mtc_funding_export_real_capture.py` | (absent) | `84d6b3e0…` | **`53a864e4…`** |
| `tests/test_funding_intake_adapter.py` | — | `16a25244…` | `16a25244…` (unchanged) |
| `tests/test_mtc_funding_export.py` (carried fence) | `c9e6c31d…` | `c9e6c31d…` | `c9e6c31d…` |

**The carried fence holds.** `tests/test_mtc_funding_export.py` is the *same blob* at
`4c802e9b`, `9ef072a8` and `a871e429`; `git diff 4c802e9b a871e429 -- <that path>` is empty
(0 lines). The synthetic pinned-candidate bytes are therefore untouched by both the slice and
the repair, and they still pass (161 passed, 1 skipped, §7).

`git show a871e429 --stat`: exactly two files — `tests/…_real_capture.py` (+61) and
`tools/export_mtc_funding.py` (+47/-14). No third file, no record/doc file inside the repo.

### Environment and gates

| gate | result |
|---|---|
| `pytest tests/test_mtc_funding_export_real_capture.py tests/test_funding_intake_adapter.py tests/test_mtc_funding_export.py -q -p no:cacheprovider --basetemp C:/bt_opus_intake` (from the worktree, Bridge py312) | **232 passed, 1 skipped** — matches the addendum |
| `ruff check` on the four slice files | **exactly 5 findings**: UP035 (`export…:106`), ISC004 ×3 (`:285,:288,:290`), SIM101 (`:550`) |
| the same 5 on `4c802e9b`'s exporter | `UP035 :89`, `ISC004 :209,:212,:214`, `SIM101 :383` — **identical set, 0 new** |
| new-module collection | 60 tests (57 at `9ef072a8` + 3 repair items) |

---

## 7. Format-only commit `b667dbcc` — PROVEN, non-whitespace change: none

First attempt was contaminated: extracting the blobs with PowerShell `>` prepends a UTF-8 BOM,
which makes `ruff format --check` report "would be reformatted" for *both* revisions. Re-run on
raw bytes (`git show … > file` under Git Bash; `git hash-object` reproduces `f12570e7…`,
`bb73329b…`, `8f639009…`, so the extracted bytes are the blobs):

| check | result |
|---|---|
| `ruff format --check` on `4c802e9b:…export_mtc_funding.py` | `1 file would be reformatted` ✔ expected |
| `ruff format --check` on `b667dbcc:…` | `1 file already formatted` ✔ expected |
| `ruff format --check` on `a871e429:…` | `1 file already formatted` (the slice keeps the format) |
| `ast.parse` + `ast.dump` of both blobs | **identical** — the reformat is provably semantics-preserving |
| token stream (comments/NL/indent stripped) | 6665 → 6668: one `(`/`)` pair deleted (a redundantly parenthesised string constant) and five `,` inserted (magic trailing commas). No other token differs. |
| `pytest tests/test_mtc_funding_export.py` at `b667dbcc` bytes, scratch copy | 159 passed, 2 skipped, **1 failed** — see below |

The single failure is **not** a `b667dbcc` defect. `test_prepare_staging_refuses_the_current_owned_mtc_production_parent`
(`tests/test_mtc_funding_export.py:1984-1997`) resolves `Path(__file__).resolve().parents[2]`
and asserts `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/economic_records/funding`
`is_dir()`; in any scratch copy that directory does not exist. Control: the *identical* module
run in the same scratch directory with the **unmodified HEAD exporter** fails exactly the same
test (159 passed, 2 skipped, 1 failed), and in the real worktree it is **161 passed, 1 skipped**.
Exporter-behaviour delta between `4c802e9b` and `b667dbcc`: zero.

Note `git diff --ignore-all-space 4c802e9b b667dbcc` is *not* empty (66/34 lines) — line
re-splitting defeats that flag. The AST equality above is the proof, not the diff stat.

---

## 1. Explicit admission, no toggle, fences intact — VERIFIED

From the bytes (`tools/export_mtc_funding.py`):

- `ACCEPTED_EVIDENCE_KINDS = (SYNTHETIC_EVIDENCE_KIND,)` (`:127`) — unchanged; the real kind is
  deliberately **not** in it (`:149`).
- Selection is by explicit name only: `build_funding_candidate(..., *, evidence_kind: str =
  SYNTHETIC_EVIDENCE_KIND)` (`:1440-1448`, keyword-only) → `_resolve_profile` (`:1425`), which
  maps only the two literal kind strings and otherwise raises
  `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`. CLI: `--evidence-kind` with
  `choices=sorted(_EVIDENCE_PROFILES)` (`:2122`+), and `--mode` exits (`SystemExit`).
- Nothing infers the kind from packet content. `_validate_coverage` (`:722-729`) reads
  `coverage["evidence_kind"]` **only to compare it** against the caller-named profile, and
  `_require_evidence_kind` (`:628-644`) returns the kind only when `kind == profile.kind`.
  I grepped the whole file for any assignment or branch that takes a profile from packet data:
  the only producers of a `_EvidenceProfile` are `_resolve_profile(evidence_kind)` and the two
  module constants. **No inference path exists.**
- Per-binding declaration is required too: `_validate_provenance` (`:849`) runs the same check
  for every binding, so one binding of the other kind refuses the whole packet.

Reproduced myself (reviewer-built packets, §2 harness):

| case | outcome |
|---|---|
| real packet, **no** `evidence_kind` argument (default profile) | refused `CANDIDATE_EVIDENCE_KIND_MISMATCH` |
| real packet, coverage declares `SYNTHETIC_FIXTURE`, caller declares real | refused `CANDIDATE_EVIDENCE_KIND_MISMATCH` |
| one binding's provenance declares the other kind | refused `CANDIDATE_EVIDENCE_KIND_MISMATCH` |
| unknown kinds `PRODUCTION`, `VERIFIED`, `real_capture_read_only`, `""` | refused `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE` |

The synthetic candidate bytes are structurally fenced by the byte-identical
`test_mtc_funding_export.py` (§0) and pass in the worktree.

---

## 2. D-1..D-6 fidelity — my own failing inputs

Harness: `C:/tmp/OPUS_P012INTAKE_SCRATCH/probe_d1_d6.py`, run against a scratch copy of the
HEAD tree (never the subject worktree), calling the pure
`build_funding_candidate(..., evidence_kind="REAL_CAPTURE_READ_ONLY")` with the new module's
fixtures. **23 cases, 0 unexpected outcomes.** Control (unmodified r1 fixture packet) →
`REAL_CAPTURE_CANDIDATE_BUILT`.

| rule | owner's row (OD-20260916-P012-INTAKE-D1-D6-R-1) | implementing lines | producer A (packet) | producer B (tool re-derivation, byte source) | my failing input → observed | verdict |
|---|---|---|---|---|---|---|
| **D-1** | `source_event_digest` = sha256 over the exact captured funding-row bytes, tagged `HL_USERFUNDING_ROW_V1:<hex>` | `:905-913` (shape), `:1296-1315` (re-derivation), `:1636-1641` (domain conflation) | `binding.source_event_digest`, `coverage.source_witnesses[event_id]` | `hashlib.sha256(row.raw)` where `row.raw` is the **exact byte span** of the located element of `coverage.funding_witness_passes[0]` (`_json_array_spans :1067`) | digest over `json.dumps(sort_keys, compact)` of row 0 → `CANDIDATE_BINDING_INVALID` "does not hash the exact captured bytes of funding row 0"; witness carrying the re-serialized bytes → `CANDIDATE_BINDING_INVALID` "not the located row 0" | **VERIFIED** |
| **D-2** | `funding_event_id` = `hl-funding:<account-short>:<coin>:<time_ms>` | `:1160` (derivation), `:1322-1327` (equality), `:1606-1621` (every captured row dispositioned) | `binding.funding_event_id`, `coverage.expected_event_ids` | rebuilt from `coverage.account_scope` + the row's own `delta.coin` + the row's own `time` | id built from the hour (`…:1789405200000`) → `CANDIDATE_COVERAGE_INVALID` (captured-but-uninventoried); same with inventory kept honest → `CANDIDATE_BINDING_UNKNOWN_EVENT` | **VERIFIED** |
| **D-3** | venue stamp verbatim as `event_timestamp` + `interval_hour_utc` = floor | `:1328-1334` (verbatim), `:972-982` (floor) | `binding.event_timestamp`, `binding.interval_hour_utc` | `_millisecond_text(row.time_ms)` and `_hour_text(floor)` from the captured row | stamp rounded to `17:00:00Z` → `CANDIDATE_BINDING_INVALID` "must be the venue stamp verbatim '…T17:00:00.041Z'"; `interval_hour_utc` ceiled → `CANDIDATE_BINDING_INVALID` "must be … floored to the hour"; subsecond dropped → same refusal | **VERIFIED** |
| **D-4** | production requires an oracle capture at each funding instant; a payment-derived price is never admitted | `:886-902` | `binding.oracle_price_source`, `binding.oracle_price` | none — the locator is checked for *shape* (`<sha256>#/<pointer>`), not opened | `oracle_price_source="DERIVED_FROM_PAYMENT"` → `CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE` ✔. **But**: a price I back-derived as `usdc/(szi·rate)` and pasted under a well-formed fixture locator was **ACCEPTED** | **VERIFIED as a naming check; DECLARED limit** (see NIT-5) |
| **D-5** | `REAL_CAPTURE_READ_ONLY` admitted only with D-1 and a witness identity naming the ownership-signature record | `:664-682` | `coverage.witness_identity` | none — three regex tokens (`run <id>`, `manifest_sha256=<hex>`, `ownership OWNERSHIP_EVIDENCE: VERIFIED <scope>`) and a scope equality | identity with no ownership token → `CANDIDATE_COVERAGE_INVALID`; ownership for `0xdead...beef` → refused, message names both scopes; `OWNERSHIP_EVIDENCE: PENDING` → refused | **VERIFIED as a naming check; DECLARED limit** (`evidence_limitations[1]`: "this tool does not re-open them") |
| **D-6** | two byte-identical funding passes + hour-aligned window + 1-second end tolerance + a fills-based expected-count check | `:685-716`, `:647-652`, `:1626`, `:1217-1283` | `coverage.funding_witness_passes`, `coverage.fills_witness`, `coverage.complete` | the pass bytes are parsed (never grepped) and the position is recomputed from the fills; the two passes are compared byte-wise | window ending `18:30` → refused (hour alignment); one pass only → refused ("at least two"); two passes differing in one `usdc` digit → refused ("not byte-identical"); captured row absent from the inventory → refused; fills leaving the position open at 16:00 with no 16:00 payment → refused, message prints expected vs observed hours; fills that never reach the rows' `szi` → refused ("row 0 reports szi 0.00058 … fills witness gives 0.00016"); non-contiguous `startPosition` chain → refused | **VERIFIED** |

No rule is DECLARED-NOT-CHECKED in the sense of a fence that does not act; no rule
DIVERGES-FROM-RULING. D-4 and D-5 verify *names*, not the referenced artifacts — that limit is
stated in the artifact's own `evidence_limitations` (§5), so it is disclosed, not hidden.

---

## 3. The 1-second end tolerance — reproduced, and the exact boundary

On the r1 bytes with a `[15:00, 18:00)` window (the 18:00:00.060Z payment is 60 ms past the
end hour):

| input | outcome |
|---|---|
| r1 as captured, `[15:00, 18:00)` | **accepted**, `REAL_CAPTURE_CANDIDATE_BUILT` |
| same capture, second payment re-stamped `18:00:01.060Z` (+1.060 s) | **refused** `CANDIDATE_BINDING_OUT_OF_INTERVAL` |
| same capture, second payment re-stamped `18:00:01.000Z` (exactly +1.000 s) | **refused** `CANDIDATE_BINDING_OUT_OF_INTERVAL` |

So the admitted band is `[start, end + 1s)` — strict on the upper side (`:1626` `end_limit`,
`:1633` `<`). That is a defensible reading of "1-second end tolerance", and it is the tighter
one, but the exporter's own docstring (`_real_completion`, `:1226-1227`) says only "the venue
stamps its payment inside the 1-second tolerance" and never says whether exactly +1.000 s is
in or out. Carried NIT-2 stands (below).

**The grid.** `grid = range(start.seconds, end.seconds + 1, 3600)` (`:1252`) includes the END
hour. For `[15:00, 18:00)` the expected-payment hours are 15,16,17,**18**. That is exactly
D-6 (i) as the owner wrote it *given* the tolerance: the payment that closes the 17-18 interval
is stamped just past 18:00 and must be demanded, otherwise the window's last hour could be
silently dropped. VERIFIED against the ruling.

**The start side is NOT covered by any owner decision.** A payment stamped `15:00:00.041Z` is
inside a window starting `15:00:00Z` *by stamp*, but it is the payment **for the 14:00-15:00
interval** — an interval the window does not cover. Symmetrically, the window's first hour
(15:00-16:00) is settled by a payment stamped `16:00:00.0xx`, which the grid does demand. So
the tool's window is "payments stamped in `[start, end+1s)`", i.e. it covers the intervals
`(start-1h, end-1h]` shifted by the venue's stamp convention. Nothing in the owner's row, in
the exporter docstrings, or in the candidate artifact states which of the two the window means.
On r1 this is invisible (the capture starts at 15:00Z and the position opens at 16:03Z, so the
15:00:00.0xx row does not exist). **It needs one owner sentence** before any window whose start
hour carries a payment. Re-raised below as NIT-6 (carried); it is a specification gap, not a
code defect, and I do not raise it to REQUIRED because the tool refuses nothing incorrectly on
any capture that exists today.

---

## 6a. Mutation evidence on the repaired block (addendum a/b/c) — all caught

Scratch copy of the HEAD tree, three modules; baseline for the two changed modules = **71
passed**. Each mutant applied alone, then restored.

| mutant | edit | result |
|---|---|---|
| (a) the no-fill branch returns zero | `position_at`: `return payments_position` → `return Decimal(0)` | **2 failed**, both `test_d6_without_a_fill_for_the_symbol_the_position_source_is_the_payments[empty-fills-witness|another-coin-only]`; 69 passed |
| (b) `position_source` relabelled | the conditional → `REAL_POSITION_SOURCE_FILLS` always | **2 failed**, the same two; 69 passed |
| (c) `opening_position` always `None` | `"opening_position": None` | **1 failed**, `test_d6_the_completion_check_names_the_fills_witness_as_the_position_source`; 70 passed |
| restore | — | **71 passed** |

Each mutant turns at least one of the two new tests RED and **nothing else**, exactly as the
addendum requires. The REQUIRED-1 branch from the first read is now covered.

## 6b. Four further mutants of the D-1/D-2/D-6 fences — all caught

| mutant | result |
|---|---|
| `REAL_END_TOLERANCE_SECONDS = 1 → 0` | 4 failed (incl. `test_d6_one_second_end_tolerance_admits_the_venue_late_stamp`) |
| D-1 digests a canonical re-serialization instead of the row bytes | 14+ failed, incl. `test_d1_digest_must_hash_the_exact_captured_row_bytes_not_a_reserialization` |
| D-2 identity built from the hour instead of the stamp | 12+ failed, incl. all four `test_d2_event_id_must_rederive_from_scope_coin_and_stamp` cases |
| pass-to-pass byte comparison disabled (`if False:`) | **exactly 2 failed**: `test_d6_two_byte_identical_funding_passes_are_required[passes1|passes2]` — a narrow, well-aimed pair |

## 6c. RED arm on the pre-slice bytes

Scratch copy of the HEAD tree with `git show 4c802e9b:…/tools/export_mtc_funding.py` swapped
in: `tests/test_mtc_funding_export_real_capture.py` → **60 failed** (60/60 collected). The new
module is entirely dependent on the slice; none of it can pass against the pre-slice exporter.

---

## 4. Real r1 dry run — reproduced byte-for-byte

I ran the adapter myself against the read-only capture
`C:/tmp/CLAUDE_P0_RUN_20260913/P012_PATH1_REAL_CAPTURE_20260915/r1/`:

```
python IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py \
  --run-dir C:/tmp/CLAUDE_P0_RUN_20260913/P012_PATH1_REAL_CAPTURE_20260915/r1 \
  --out     C:/tmp/OPUS_P012INTAKE_SCRATCH/r1_s4

NONACCEPTING_INTAKE_DRAFT events=2 fills=5 complete=True
  export_tool_would_refuse=CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE
  real_packet=BUILT real_packet_tool_outcome_expected=CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE
b9a5f573790cc3cbfa3159bc1316ab1c99ddd9be6cb6f726eeee5359d74e5965  binding_packet_draft.json
e8b0176520ce05c12dc4ef65429c1d555da50e9a6ab618ac31e9fc37f285f931  retained_rows_expected.json
37d3b8ed8cefb6ca78cc6e09513faa0e620cb19d0ed8f6ddff1be6a7b37fb42e  intake_gap_report.json
f3bde0b7a1b008739df927c119fd5a654836b40af9149b58ed6e241fcd0c979b  binding_packet_real_capture.json
```

All four digests equal the record's `LEAD_INTAKE_r1_s4_stdout.txt` **exactly**. A second run
into a different directory produced byte-identical files (`cmp` on all four) — the adapter is
deterministic and reads no clock.

**The capture directory is unchanged.** My own recursive content digest of the capture
(excluding the harness's `.impeccable/`) is `b5774ef0…` before the run and `b5774ef0…` after.

Exporter pure function on `binding_packet_real_capture.json`, with FIXTURE retained rows built
as the record describes (the adapter's own `retained_rows_expected.json` cannot be fed
directly: its `payload_digest` is the honest `UNAVAILABLE:BRIDGE_OBSERVATION_REQUIRED` label
and the exporter refuses a non-digest):

| call | result | matches the record |
|---|---|---|
| REAL profile, packet **as emitted** | refused **`CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE`** — "D-4: … must name an oracle capture at the funding instant as `<sha256>#<json-pointer>`; a price derived from the payment is research evidence only" | yes |
| DEFAULT (synthetic) profile, same packet | refused `CANDIDATE_EVIDENCE_KIND_MISMATCH` | yes |
| REAL profile + a FIXTURE oracle locator | **`REAL_CAPTURE_CANDIDATE_BUILT`** | yes |

The accepted candidate: `artifact_kind REAL_CAPTURE_FUNDING_CANDIDATE_V1`, `synthetic_only
false`, `admission_status REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD`, root keys
carry **none** of `events` / `schedule_id` / `settlement_currency` (they are `bound_events` and
`candidate_schedule_id` inside `real_capture_candidate`), and
`completion_check = {'expected_funding_hours': ['…17:00:00Z','…18:00:00Z'],
'observed_funding_hours': [same], 'opening_position': '0.0', 'position_source':
'coverage.fills_witness'}` — identical to the record's pre-repair line, confirming the repair
did not move the r1 path. My candidate digest is `28eda37d…` vs the record's `8eb1efe3…`
because I used my own `--schedule-id`; the schedule id is part of the signed body, so that
difference is expected and not a divergence.

**Address containment — proven, not assumed.** The full 40-hex mainnet address does exist in
the capture (`CAPTURE_MANIFEST.json`, one file). Searching the four adapter outputs and my
built candidate for it, case-insensitively, and for its 8-hex prefix: **0 hits**. The only
`0x`+long-hex tokens reaching any output are the venue's 64-zero hash; decoding every hex
witness blob (`fills_witness`, both `funding_witness_passes`, both `source_witnesses`) and
re-scanning for `0x` + exactly 40 hex returns nothing. The account appears only as the short
form `0x1E26…AC49`.

---

## 5. Overclaim and honest limits — nothing reads as accepted or production

Nothing in the real path claims admission. Every stale label I found errs toward
**under**-claiming (it says "synthetic" where the truth is "real but non-admitted"), never the
other way.

| artifact / field | value on a REAL run | reading |
|---|---|---|
| `candidate.admission_status` | `REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD` | correct |
| `candidate.not_a_production_record` | names `OD-20260914-P012-ADMISSION-Q3 ("Wait")` and "must never be installed as an MTC funding schedule" | correct |
| `candidate.synthetic_only` | `false` | correct, and it is the one field that must not lie |
| production selection keys at the root | absent (`bound_events`, `candidate_schedule_id` instead) | structurally non-consumable, as claimed |
| `report.evidence_kind` / `report.synthetic_only` | `REAL_CAPTURE_READ_ONLY` / `False` | correct |
| `report.production_mode` | `UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN` | **stale reason** — for this profile the digest domain *is* resolved (`HL_USERFUNDING_ROW_V1`). The verdict ("unavailable") is right; the stated cause is false. NIT-3 |
| `report.report_kind` | `SYNTHETIC_FUNDING_CANDIDATE_REPORT_V1` | **stale label** on a real run. NIT-3 |
| `report.inputs.synthetic_schedule_id` | the real schedule id | **stale key name**. NIT-3 |
| `bound_events[*].binding_notes.settlement_rate_source` / `settlement_time_source` | `SYNTHETIC_BINDING_ONLY` | **stale label inside the accepted real candidate**, and asserted by no test. NIT-7 (mine) |
| CLI `--help` description (`:2125-2129`) | "Stage a SYNTHETIC_ONLY MTC funding candidate…" | stale once `--evidence-kind` exists. NIT-8 |
| adapter `intake_gap_report.json → real_capture_packet` | `status BUILT`, `statement "It admits NO production evidence: OD-20260914-P012-ADMISSION-Q3 (Wait) and the gate order Q6 stand."`, D-4 listed under `unresolved`, D-1/2/3/5/6 under `decisions_applied` | correct and honest — D-4 is *not* claimed as applied |

**Are the Lead's stated limits visible in the artifacts themselves?**

| Lead's disclosed limit | visible where | verdict |
|---|---|---|
| D-4 and D-5 are *naming* checks | `evidence_limitations[1]`: "named by digest in the witness identity (D-5); **this tool does not re-open them**"; `[2]`: "named by digest and JSON pointer (D-4); **this tool does not re-open it and does not re-verify the price**" | **VISIBLE**, verbatim, in the candidate's own report |
| no schema-v10 store carries these events | `retained_rows_expected.json → payload_digest = UNAVAILABLE:BRIDGE_OBSERVATION_REQUIRED`, plus the gap report's `unresolved_fields` | **VISIBLE** |
| the repaired D-6 position-source split | `evidence_limitations[3]` now says "or, when the fills witness carries no fill for the symbol, the constant position the payments themselves report (`completion_check.position_source` names which)" | **VISIBLE** — the repair also fixed the limitation text, not just the field |
| `PRODUCTION_MODE_UNAVAILABLE` wording is stale for the real kind | nowhere | **NOT VISIBLE** — disclosed only in the Lead's prose. NIT-3 |

One further honest-limits gap I found myself (NIT-9): the exporter never cross-checks the
**Bridge payload** against the captured venue row. I fed a real packet whose retained row says
`amount_usdc -999.0, funding_rate 0.5, position_szi 42.0` while the captured row says
`-0.000571 / 0.0000125 / 0.00058`; the candidate was **built and accepted**, carrying both
numbers side by side. That is defensible — the two are independent observations in distinct
digest domains (`CANDIDATE_DIGEST_DOMAIN_CONFLATION` exists to keep them distinct), and D-1..D-6
do not ask for the comparison — but the artifact already emits
`binding_notes.bridge_effective_ts_equals_binding_event_timestamp` for the *time* field (I
confirmed it correctly flips to `false` for a 30-minute ledger skew), so a reader may
reasonably read the absence of a value-agreement flag as agreement. It should either emit the
same kind of note for the value fields or say in `evidence_limitations` that the Bridge payload
is not compared with the venue row.

---

## 6d. What each new test catches, and the tests that can pass for the wrong reason

Grouped (60 tests in the new module; mutation evidence in §6a/§6b):

| test group | wrong implementation it catches |
|---|---|
| `test_the_real_profile_is_never_selected_by_default`, `…_refuses_a_packet_that_does_not_say_so`, `test_one_binding_of_another_kind…`, `test_an_unknown_declared_kind…`, `test_the_cli_names_the_profile_explicitly…`, `test_the_synthetic_profile_still_refuses_a_real_packet_by_kind` | any inference of the profile from packet content; a `--mode` toggle; a real kind leaking into `ACCEPTED_EVIDENCE_KINDS`; per-binding declaration dropped |
| `test_d1_*` (4) | digesting a re-serialization instead of the captured bytes (mutant e: 14 RED); a missing domain tag; a locator that does not point at the located span; reuse of the Bridge payload digest |
| `test_d2_*` (2, 4 params) | identity from the hour / another scope / another coin (mutant f: 12 RED); a binding that locates the wrong captured row |
| `test_d3_*` (2, 2 params), `test_raw_rate_and_the_payer_convention…` | a rounded or re-spelled stamp; a ceiled hour key; a missing ninth field; a rate/payer that contradicts the row |
| `test_d5_witness_identity…` | a witness with no ownership record, or one for another scope |
| `test_d6_*` (14, incl. the 2 repair tests) | a single pass; passes not compared (mutant g: **exactly 2** RED); an unaligned window; a lost end tolerance (mutant d: 4 RED); an undispositioned captured row; a foreign coin; a position/payment mismatch; a non-contiguous fills history; the repaired position-source branch (mutants a/b/c) |
| `test_cli_*` (2) | staging a real candidate without the named profile |

**Tests that could pass for the wrong reason** — I name three:

1. `test_an_unknown_declared_kind_is_unavailable_not_a_profile:330` and
   `test_the_real_candidate…:432` assert `report["production_mode"] ==
   exporter.PRODUCTION_MODE_UNAVAILABLE`. Both sides are the same module constant, so the
   assertion pins the *spelling* and can never notice that
   `UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN` states a reason that is false for the real
   profile. It is green today for a wording that NIT-3 says is wrong.
2. `test_r1_with_a_named_oracle_capture_materializes_a_labelled_candidate:410` asserts only
   that `events/schedule_id/settlement_currency` are absent from the **root**. Nothing asserts
   that the nested `bound_events[*].binding_notes` labels are truthful; that is how
   `settlement_rate_source: SYNTHETIC_BINDING_ONLY` survives on real evidence (NIT-7).
3. `tests/test_funding_intake_adapter.py:132-135` asserts the adapter's declared export-tool
   refusal code against a **hard-coded string literal**, never against a live exporter call —
   see NIT-A, where I show the declared code is not the one the tool produces. Ten lines below,
   the slice *does* do it the right way for the real packet
   (`test_real_packet_refuses_under_d4…:383-393` calls `build_funding_candidate` for real), so
   the correct pattern was available and was not applied to the older claim.

**The two changed adapter assertions (`payload_digest` label) — a disclosed correction, not a
silently changed fence.** `UNRESOLVED:D-1` → `UNAVAILABLE:BRIDGE_OBSERVATION_REQUIRED`
(`funding_intake_adapter.py:57,459-460`). Judged against the exporter's own rule: the retained
row's `payload_digest` is the **Bridge normalized reconcile digest**
(`BRIDGE_PAYLOAD_DIGEST_DOMAIN`), not a D-1 source-event digest, and the exporter refuses a
binding that conflates the two (`CANDIDATE_DIGEST_DOMAIN_CONFLATION`, `export_mtc_funding.py:1636-1641`,
docstring "the two byte domains are distinct"). The old label asserted D-1 membership for a
value from the other domain — the new label names the true blocker (no store has observed these
events). Test side: `:122-125` moved from a literal to the module constant (equal strength);
`:138-147` moved from `startswith("UNRESOLVED:D-")` to **exact equality** (strictly stronger),
and it still holds `source_event_digest == "UNRESOLVED:D-1"` for the binding field (`:116`), so
the D-1 fence itself is untouched. Correction, and in the right direction.

---

## 8. Scope and safety — VERIFIED

| claim | evidence |
|---|---|
| exactly four files in the slice | `git show 9ef072a8 --name-only`: `tools/export_mtc_funding.py`, `tools/funding_intake_adapter.py`, `tests/test_mtc_funding_export_real_capture.py`, `tests/test_funding_intake_adapter.py`. The repair touches two of them. |
| no `bridge/` runtime module | no path under `IBKR_PAPER_BRIDGE/bridge/` in either commit |
| stdlib-only additions | import lists of both blobs are byte-identical between `4c802e9b` and `a871e429` for the exporter (`diff` of the import lines: empty) — the slice added **no** import. The adapter imports only `argparse, hashlib, json, sys, datetime, pathlib, typing`. |
| no env read | the only `os.` uses in the exporter are `os.path.abspath` (`:1964`, `:1979`); `grep -E 'os\.environ|getenv|\.env'` over both tools: no match |
| no network | `grep -E 'requests|urllib|http|socket|subprocess'`: no match in either tool |
| no key | `grep -E 'api_key|secret|private_key'`: no match |
| never writes or copies a database | the only sqlite access is `sqlite3.connect(f"{…}?mode=ro&immutable=1", uri=True)` (`:1869` URI, `:1875` connect) through `_ReadOnlySnapshot`, which deliberately bypasses `Store.__init__`/`Store.conn` because those write (WAL pragma). File writes are `open(path, "xb")` only (`_write_new_file :2058-2062`). The adapter writes only into `--out`, via `mkdir(parents=True)` (fails if it exists) and `"xb"`. |
| the r1 capture is untouched | content digest identical before and after my run (§4) |

---

## Findings

### REQUIRED

**None.** The round-1 repair closes lane-8 REQUIRED-1 completely: the accepting `opening is
None` branch now resolves the position once before the grid walk, labels its true producer
(`REAL_POSITION_SOURCE_PAYMENTS`), qualifies `REAL_CAPTURE_EVIDENCE_LIMITATIONS[3]`, and is
covered by two tests that my own three mutants (a/b/c) each turn RED with no collateral
failures. No refusal code, no message and no synthetic byte changed.

### NIT

| # | file:line | finding |
|---|---|---|
| NIT-1 (carried) | `tools/export_mtc_funding.py:640-644` | the unknown-kind refusal message says "only `['SYNTHETIC_FIXTURE']` is accepted" even when the caller named the REAL profile. The code is right, the sentence is stale; it should name the caller's profile and the known profiles. |
| NIT-2 (carried) | `tools/export_mtc_funding.py:1224-1227`, `:1626` | the 1-second tolerance is a **half-open** band: I measured `+1.060 s` refused **and `+1.000 s` exactly refused**. Neither the docstring nor `effective_interval.end_tolerance_seconds: 1` says whether the boundary instant is in or out. One sentence would settle it. |
| NIT-3 (carried) | `tools/export_mtc_funding.py:1797` (`production_mode`), `:1800` (`report_kind`), `:1781` (`inputs.synthetic_schedule_id`) | three synthetic-era labels on a real run; the first also states a *reason* that is false for the real profile (its digest domain is resolved). Safe direction, wrong words. |
| NIT-4 (carried) | `tools/funding_intake_adapter.py:531` | the D-1 gloss in the gap report is a one-line restatement of the ruling; it is accurate, but the file also carries the pre-slice `UNRESOLVED:D-n` labels in the draft packet (carried NIT-7 of round 1) — worth one sweep when the adapter is next touched. |
| NIT-5 (carried) | `tools/export_mtc_funding.py:893` (inside `:886-902`) | D-4 rejects a source containing the substring `"derived"` (case-folded). A substring blacklist is not a fence: **I built a price back-derived as `usdc/(szi·rate)`, pasted a well-formed `<sha256>#/pointer` locator, and the candidate was ACCEPTED.** This is the declared limit ("this tool … does not re-verify the price"), so it is honest — but the blacklist gives an impression of protection it does not provide and should be described as cosmetic, not relied on. |
| NIT-6 (carried) | — (specification) | **the window's start side has no owner decision.** A payment stamped `15:00:00.041Z` sits inside a window starting `15:00:00Z` by stamp, yet it settles the *14-15* interval. The end side was ruled (D-6 (i)); the start side was not. Invisible on r1 (the position opens at 16:03Z) but it will bite the first capture whose start hour carries a payment. **It needs one owner sentence** — see §3. |
| NIT-7 (mine) | `tools/export_mtc_funding.py:131`, `:1661-1662` | `binding_notes.settlement_rate_source` / `settlement_time_source` emit `SYNTHETIC_BINDING_ONLY` **inside the accepted real-capture candidate**, on values taken verbatim from the venue row. No test asserts these on the real path. Same family as NIT-3 but deeper in the artifact. |
| NIT-8 (mine) | `tools/export_mtc_funding.py:2125-2129` | the CLI `--help` still describes the tool as staging "a SYNTHETIC_ONLY MTC funding candidate", one argument above `--evidence-kind`. |
| NIT-9 (mine) | `tools/export_mtc_funding.py:1652-1671`, `:171-196` | the Bridge payload is never compared with the captured venue row: a retained row claiming `amount_usdc -999.0 / funding_rate 0.5 / position_szi 42.0` against a captured row of `-0.000571 / 0.0000125 / 0.00058` **builds an accepted candidate**. Defensible by design (distinct digest domains, not asked for by D-1..D-6), but the artifact already flags time agreement (`bridge_effective_ts_equals_binding_event_timestamp`, which I confirmed flips to `false` on a 30-minute skew) and flags nothing for the values. Either add the note or state the non-comparison in `evidence_limitations`. |
| NIT-A (mine, **pre-existing — not introduced by this candidate**) | `tools/funding_intake_adapter.py:48`, `:512-513`, `:612`; `tests/test_funding_intake_adapter.py:132-135` | the adapter declares, in `intake_gap_report.json` and on stdout, that the export tool refuses the **draft** packet with `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE` ("only SYNTHETIC_FIXTURE evidence is accepted"). I ran the real draft packet through the exporter: at HEAD it refuses with **`CANDIDATE_EVIDENCE_KIND_MISMATCH`** (default profile) or `CANDIDATE_COVERAGE_INVALID` (real profile). I then checked whether the slice caused it — **it did not**: the *pre-slice* exporter (`4c802e9b`) also refuses that packet with `CANDIDATE_COVERAGE_INVALID`, because the draft's coverage carries two extra keys (`witness_reasons`, `witness_rule`); the declared code only appears if those two keys are removed. So the claim was already wrong at `004a0711`. Producer A = the adapter constant; producer B = the exporter's actual refusal; nothing compares them, and the only test compares one literal to another. Cheap fix, and the correct pattern already exists ten lines below in the same test file. |

### NOT VERIFIED

- **The four Lead mutants were not reproduced by their own edits.** `LEAD_MUTANT_M1..M4` name
  the edits; I wrote seven mutants of my own instead (§6a/§6b), including the same classes
  (tolerance, D-1 canonicalisation, D-2 identity, pass comparison). I did not diff my edits
  against theirs.
- **The full Bridge suite (1669/1696 passed) was not re-run.** I ran the three named modules
  (232 passed, 1 skipped) plus the scratch arms. A regression outside those modules would not
  have been seen by me.
- **The CLI end-to-end real path was not exercised against a live schema-v10 store** — none
  exists (the deployed store is schema v4). The two CLI tests in the new module use fixtures;
  `_read_snapshot_rows` raising `FUNDING_PAYLOAD_SCHEMA_INACTIVE` on a real v4 snapshot is
  read from the code, not observed.
- **Gemini's detection report on `9ef072a8`** (`S4_ACCEPTING_HALF/GEMINI/`) was not read; this
  is an independent read by construction.
- **The owner's decision row** was taken from `REVIEW_BRIEF.md` §Context as transcribed; I did
  not open `C:/CT13/DECISIONS.md` to re-read `OD-20260916-P012-INTAKE-D1-D6-R-1` verbatim.
  Every D-rule judgement above is therefore against the brief's quotation of the row, not
  against the row's own bytes.

### Housekeeping

Everything I built lives under `C:/tmp/OPUS_P012INTAKE_SCRATCH/` (`probe_d1_d6.py`,
`probe_r1.py`, `mutate.py`, `blobs2/`, three scratch trees, `r1_s4/`, `r1_s4b/`,
`r1_candidate_opus.json`); this report is the only file I wrote under
`C:/tmp/OPUS_QUEUE_20260916/P012INTAKE/opus/`. No mutation was ever applied inside the subject
worktree — only to the scratch copy — and every mutant was restored (232/71 green after each).
Git commands used: `rev-parse`, `log`, `ls-tree`, `show`, `diff`, `hash-object`, `cat-file`
only; no `status`/`add`/`commit`/`checkout`/`stash`/`push` in any repository. Running the
brief's mandated pytest command from the worktree will have created `__pycache__` directories
there; I did not remove them (that would need a write to the subject) and could not inspect the
working tree's cleanliness without `git status`, which the brief forbids.

### Summary

The repair is exactly what the addendum describes and nothing more: two files, `+94/-14`, no
refusal code or message altered, the synthetic candidate's test module the same blob it has been
since `4c802e9b`, and the previously unreachable-by-tests accepting branch now both honest and
covered. The D-1..D-6 fences hold against 23 failing inputs I built myself, seven mutants die,
the r1 dry run reproduces the record byte-for-byte and still refuses at D-4, and the owner's
mainnet address reaches no output. The remaining items are labelling staleness (NIT-1,3,7,8), two
declared limits that should be described as naming checks rather than fences (NIT-5, NIT-9), one
inherited false claim in the adapter's gap report (NIT-A), and one genuine specification gap
that needs the owner, not the Lead: **the window's start side (NIT-6)**.

VERDICT: PASS-WITH-NITS
