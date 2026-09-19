# Exact review — WP-P0-12 funding intake slice 4 (ACCEPTING half), candidate `9ef072a8`

Reviewer: exact `claude-opus-5`, effort xhigh, independent (no delegation, no subagents, no other session). Brief: `C:/tmp/OPUS_QUEUE_20260916/P012INTAKE/REVIEW_BRIEF.md`. Owner authority read at source: `C:/CT13/DECISIONS.md:137` (`OD-20260916-P012-INTAKE-D1-D6-R-1`). Candidate is Lead-authored and disclosed; this is the first exact flagship read.

Everything below was run by me. Scratch under `C:/tmp/OPUS_P012INTAKE_SCRATCH/` (`h.py` harness, `mutants.py`, `fences.py`, `run_mutants.py`, `red/`, `mut/`, `fmt/`, `r1_s4/`). Git use was limited to `rev-parse`, `ls-tree`, `show`, `cat-file blob`, `hash-object` and `diff <sha> <sha>`; no command touched a working tree or an index.

Environment: Bridge interpreter `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe`, ruff `C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe`, every pytest run with `--basetemp` outside `C:/tmp` (the harness recreates `C:/tmp/.git`, which turns the exporter's staging-safety tests into phantom failures). Disclosure: beyond the brief-named `C:/bt_opus_intake` I created seven further pytest basetemp directories (`C:/bt_opus_{red,mut,ctl,tri,fmt,wt,m5}`) so each arm ran isolated; they hold nothing but pytest scratch.

**Subject integrity after the review.** Re-checked at the end: HEAD is still `9ef072a8…`, and the working-tree blob OIDs of all five files are byte-identical to their committed values (`216b9cc3`, `e0737289`, `84d6b3e0`, `16a25244`, `c9e6c31d`). Nothing I ran wrote into the worktree or the r1 capture directory.

**Focused suite at HEAD, as the brief specifies:** `229 passed, 1 skipped` — matches `LEAD_PYTEST_focused_post_commit_9ef072a8.txt`.

## 0. Verified identities

COMPUTED (`git -c safe.directory=* -C C:/tmp/P012_INTAKE_20260915 rev-parse HEAD`):

- HEAD = `9ef072a8cbc83915679d0cfc4fb142fba449c8e0` — matches the brief's candidate.
- HEAD^ = `b667dbcc1a38e795a19576dab93e7723e78ad620` (format-only commit) — matches.
- HEAD^^ = `4c802e9b68539c2ed0a422dc34efcb0e55ae3796` (non-accepting adapter) — matches.

Blob OIDs (`git ls-tree`):

| path | `4c802e9b` | `b667dbcc` | `9ef072a8` |
|---|---|---|---|
| `IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py` | `f12570e704821fdae26d2461e4b0ab6f2c6ca854` | `bb73329b1c3d715593560f90cb7e7fdba8e9efa8` | `216b9cc3909fde593a65434c8711ae976e299a33` |
| `IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py` | `a06d21ed607dba26ba256eeebd747cc681e285db` | (unchanged) | `e07372891d2abf0b4eef564e141f0ad94fb683e1` |
| `IBKR_PAPER_BRIDGE/tests/test_mtc_funding_export_real_capture.py` | (absent) | (absent) | `84d6b3e0fb9fa115d59ffd28b0344bfac7e8747d` |
| `IBKR_PAPER_BRIDGE/tests/test_funding_intake_adapter.py` | `4353ce843cff4e0b6770603ae3b8d354ac09193a` | (unchanged) | `16a25244885f977110179b645a0d76e041fa74ce` |
| `IBKR_PAPER_BRIDGE/tests/test_mtc_funding_export.py` | `c9e6c31d5529b639fddc352963d3932e9f6e961b` | `c9e6c31d5529b639fddc352963d3932e9f6e961b` | `c9e6c31d5529b639fddc352963d3932e9f6e961b` |

The pinned synthetic test module is byte-identical across all three revisions by blob OID.

## 1. Explicit admission, no toggle, fences intact — VERIFIED

**How the real profile is selected.** Two surfaces, both explicit, both named by the caller:

- CLI: `--evidence-kind`, `choices=sorted(_EVIDENCE_PROFILES)`, `default=SYNTHETIC_EVIDENCE_KIND` (`export_mtc_funding.py:2119-2128`). Observed: default `SYNTHETIC_FIXTURE`; `--evidence-kind PRODUCTION` is rejected by argparse (`SystemExit 2`, "invalid choice"). The string `--mode` does not occur anywhere in the file.
- Pure function: `evidence_kind` is **KEYWORD_ONLY** with default `'SYNTHETIC_FIXTURE'` (`:1421-1430`, confirmed by `inspect.signature`).

**No inference path.** `_resolve_profile` (`:1406-1418`) reads only the caller's argument; `_validate_coverage` (`:714-717`) looks at `coverage["evidence_kind"]` *only* to raise the mismatch before the shape check, never to select. Called with no `evidence_kind` argument at all against a packet that declares `REAL_CAPTURE_READ_ONLY`, the tool refuses `CANDIDATE_EVIDENCE_KIND_MISMATCH` — it does not adopt the packet's kind. No path anywhere infers the profile from packet content.

**Refusals I ran myself** (pure function, r1 packet + pinned synthetic fixtures from `test_mtc_funding_export.py`):

| Input | Observed |
|---|---|
| real packet, default profile | `CANDIDATE_EVIDENCE_KIND_MISMATCH` — "the evidence profile is named explicitly, never inferred" |
| pinned **synthetic** packet, real profile | `CANDIDATE_EVIDENCE_KIND_MISMATCH` (reverse direction) |
| real packet, one binding's `provenance.evidence_kind = SYNTHETIC_FIXTURE` | `CANDIDATE_EVIDENCE_KIND_MISMATCH`, naming the binding |
| `coverage.evidence_kind = "PRODUCTION_LIVE"` | `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE` |
| `provenance.evidence_kind = "PRODUCTION_LIVE"` | `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE` |
| caller `evidence_kind="PRODUCTION_LIVE"` / `None` | `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE` |
| pinned synthetic packet, default profile (control) | `SYNTHETIC_CANDIDATE_BUILT`, sha256 `6ca9299e…` |

**`ACCEPTED_EVIDENCE_KINDS` is textually unchanged** — `('SYNTHETIC_FIXTURE',)` at `:127`. See NIT-1: it no longer gates anything, and the message it feeds is now wrong under the real profile.

**Byte identity of the pinned synthetic module.** `git diff 4c802e9b 9ef072a8 -- IBKR_PAPER_BRIDGE/tests/test_mtc_funding_export.py` is empty; blob `c9e6c31d…` at all three revisions. Its pinned candidate bytes still pass: run alone in the worktree it is `161 passed, 1 skipped`, and it contributes those 162 cases to the focused run's `229 passed, 1 skipped`.

## 2. D-1..D-6 fidelity — my own failing inputs

Producer A = the packet field. Producer B = the tool's re-derivation and the bytes it re-derives from. Every refusal below is one I constructed and ran (`C:/tmp/OPUS_P012INTAKE_SCRATCH/mutants.py`), against the **real r1 packet with a fixture oracle locator**, whose unmutated form BUILDS (`REAL_CAPTURE_CANDIDATE_BUILT`) — so each refusal is attributable to my mutation alone.

| Rule | Owner's row text | Implementing lines | Producer A | Producer B (byte source) | My failing input → observed | Verdict |
|---|---|---|---|---|---|---|
| **D-1** | `source_event_digest` = sha256 over the exact captured bytes of the funding row, tagged `HL_USERFUNDING_ROW_V1`, written `<tag>:<hex>` | `:154`, `:296-298`, `:897-905`, `:1285-1296` | `bindings[i].source_event_digest` | `sha256(row.raw)` where `row.raw` is the exact byte span `text[index:end]` of element *i* of `coverage.funding_witness_passes[0]` (`:1059-1106`, `:1096`) | (a) digest over a canonical re-serialization of the row → `CANDIDATE_BINDING_INVALID` "does not hash the exact captured bytes of funding row 0"; (b) witness bytes **and** digest both the re-serialization → "source witness bytes are not the located row 0"; (c) untagged bare sha256 → "must be `HL_USERFUNDING_ROW_V1:<…>`" | **VERIFIED** |
| **D-2** | `funding_event_id` = `hl-funding:<account-short>:<coin>:<time_ms>` | `:155`, `:1152`, `:1303-1308`, `:1587-1602` | `bindings[i].funding_event_id`, `coverage.expected_event_ids` | `f"hl-funding:{coverage.account_scope}:{row.delta.coin}:{row.time}"` re-derived from the captured row | id built from the hour (`…:1789405200000`) instead of the stamp → `CANDIDATE_COVERAGE_INVALID`, "every row inside the captured funding pass needs a disposition under its D-2 identity … captured-but-uninventoried […041] / inventoried-but-not-captured […000]" | **VERIFIED** |
| **D-3** | keep the venue stamp verbatim as `event_timestamp`; `interval_hour_utc` = its floor, as the schedule key | `:271`, `:873-875`, `:957-974`, `:1309-1315` | `event_timestamp`, `interval_hour_utc` | `_millisecond_text(row.time_ms)` from the captured row; the hour is recomputed from the binding's own parsed instant *and* forced equal to the row stamp | (a) stamp rounded to `17:00:00Z` → "event_timestamp must be the venue stamp verbatim, `'2026-09-14T17:00:00.041Z'`"; (b) `interval_hour_utc` set to `18:00` → "must be the venue stamp floored to the hour, `'2026-09-14T17:00:00Z'`" | **VERIFIED** (naming caveat: see NIT-4) |
| **D-4** | production requires an oracle capture at each funding instant; `DERIVED_FROM_PAYMENT` only as labelled research evidence, never admitted | `:299`, `:878-894`, `:930-933` | `oracle_price_source` | *naming check only* — `<sha256>#/<pointer>`, and any `UNRESOLVED…` prefix or the substring `derived` is refused. The tool never opens the oracle capture (stated in `REAL_CAPTURE_EVIDENCE_LIMITATIONS[2]`) | (a) `"DERIVED_FROM_PAYMENT"` → `CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE`; (b) a prose label with no digest → same | **VERIFIED as a naming rule** (see NIT-5) |
| **D-5** | `REAL_CAPTURE_READ_ONLY` admitted only together with D-1 and a witness identity naming the ownership-signature record | `:301-307`, `:656-674`, `:769` | `coverage.witness_identity` | *naming check only* — three regexes (`run <id>`, `manifest_sha256=<hex>`, `ownership OWNERSHIP_EVIDENCE: VERIFIED <scope>`) plus scope equality with `coverage.account_scope` | (a) identity truncated before `; ownership` → `CANDIDATE_COVERAGE_INVALID` naming all three required tokens; (b) ownership scope `0xdead…beef` → "the ownership-signature record named by the witness is for `'0xdead…beef'`, not the witnessed account scope `'0x1E26…AC49'`" | **VERIFIED as a naming rule** (see NIT-5) |
| **D-6** | two byte-identical funding passes + hour-aligned window + 1-second end-boundary tolerance + an expected-count check fed by the fills pass of the same capture | `:156`, `:639-644`, `:677-708`, `:767-768`, `:1158-1264`, `:1607` | `coverage.funding_witness_passes`, `coverage.fills_witness`, `coverage.complete`, the window | all four re-derived: passes compared byte-wise; window floors checked; `end_limit = end + 1 s`; the hour grid and the expected payment set derived from the fills' `startPosition` chain | (i) window ending `18:30` → "must be aligned to a whole venue funding hour"; (ii) one pass → "at least two captured funding passes are required, got 1"; (ii-b) two non-identical passes → "the captured funding passes are not byte-identical"; (iii) a captured row dropped from the inventory → the D-2 disposition refusal; (iv) the closing fill removed so the position stays open → "expects payments at [17:00, 18:00, **19:00**] but the captured funding passes carry payments at [17:00, 18:00]"; (v) a row `szi` changed to `0.00059` (packet fully rebuilt around the mutated bytes) → "funding row 0 reports szi 0.00059 at 2026-09-14T17:00:00.041Z while the fills witness gives 0.00058" | **VERIFIED**, with the window-semantics gap in §3 |

**17 of 17** of my own inputs landed on the expected outcome. No rule is DECLARED-NOT-CHECKED. No rule DIVERGES-FROM-RULING.

The fills check is stronger than the ruling requires and I confirmed it: `_real_fills` (`:1158-1206`) re-chains every fill's `startPosition` against the running position, so a gap in the captured fills history cannot pass as continuity, and `opening` is taken from the venue's own `startPosition` of the earliest fill rather than assumed zero.

## 3. The 1-second end tolerance — reproduced, and one thing the owner has not ruled

Reproduction on the r1 bytes, window `[15:00, 18:00)`, the real `18:00:00.060Z` stamp:

| Stamp | Observed |
|---|---|
| `18:00:00.060Z` (the captured one, +0.060 s) | **accepted**, `REAL_CAPTURE_CANDIDATE_BUILT` |
| +0.999 s | accepted |
| **+1.000 s** | **refused** `CANDIDATE_BINDING_OUT_OF_INTERVAL` |
| +1.060 s | refused `CANDIDATE_BINDING_OUT_OF_INTERVAL` |

`end_limit = (end.seconds + 1, end.fraction)` with a strict `<` (`:1607`, `:1614`), so the admitted band is the half-open `[end, end+1 s)`. A stamp at exactly one second past the end is refused. The owner wrote "a 1-second end-boundary tolerance"; half-open is a defensible reading, but the boundary itself was chosen by the implementation, not by the row. → **NIT-2**.

**The grid.** For `[15:00, 18:00)` the grid is `range(start, end+1h, 1h)` = `15, 16, 17, 18` (`:1237`) — both endpoints inclusive. Combined with `position_at(hour)` using the position held *before* that hour (`:1222-1235`, `fill_ms < time_ms`), the grid is consistent with the venue's convention that the payment stamped at hour *H* settles `[H−1h, H)`. Including the end hour is exactly what the owner's tolerance is for, and I confirm it is the same one second, not a second mechanism.

**The start side is NOT stated anywhere, and it is not the owner's decision.** I searched all four files for any statement of which accrual interval a payment settles: the only occurrence is a test docstring, `tests/test_mtc_funding_export_real_capture.py:744` ("the 18:00:00.060Z payment settles the 17-18 interval"). Nothing in the exporter, the adapter, the candidate artifact or the report says it. I built the demonstrating case (position already open at the window start, payments at 15/16/17/18):

```
effective_interval : {'start_inclusive': '2026-09-14T15:00:00Z', 'end_exclusive': '2026-09-14T19:00:00Z', 'end_tolerance_seconds': 1}
completion_check   : ['15:00', '16:00', '17:00', '18:00']   (expected_funding_hours)
interval_hour_utc  : ['15:00', '16:00', '17:00', '18:00']
```

A candidate that declares the interval `[15:00, 19:00)` therefore witnesses the accrual intervals `[14:00,15:00) … [17:00,18:00)` — i.e. the accrual coverage is `[start − 1 h, end)`: the declared window **plus one hour before its declared start**. The start hour is mandatory, not optional: deleting the 15:00 payment from that same capture refuses with "expects payments at [15:00, 16:00, 17:00, 18:00] … carry payments at [16:00, 17:00, 18:00]".

Two consequences the roster and the owner should see (neither is a fence hole — both fail toward refusal — so neither blocks this candidate):

1. `interval_hour_utc` and `effective_interval` name a **payment-stamp** window while reading as an accrual window, and the witness silently reaches one hour before the declared start. Under D-3 the owner ruled the *value* (the floor of the stamp); the *meaning* of the window relative to accrual is unruled and stated nowhere in the artifacts. It needs one owner sentence. → **NIT-6**.
2. On the end side this interacts with the capture tool. r1's manifest requests `userFunding` with `endTime = 1789412400000` (= `19:00:00.000Z`), while the exporter's grid expects a payment at `19:00` whenever the position is still open then — and that payment is stamped 41-60 ms *past* the hour, outside the capture request bounds. My D-6 (iv) mutant is exactly this case and refuses. So a real capture whose window does not end flat is, as built, structurally un-witnessable: the exporter applies the tolerance, the capture request does not. The failure is conservative (refusal, never admission), but the accepting half cannot witness the general case today. → **NIT-6** (same recommendation: state the semantics, and extend the capture request past the tolerance before the next capture is run).

## 4. Real r1 dry run — reproduced byte for byte

Adapter run: `python IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py --run-dir C:/tmp/CLAUDE_P0_RUN_20260913/P012_PATH1_REAL_CAPTURE_20260915/r1 --out C:/tmp/OPUS_P012INTAKE_SCRATCH/r1_s4`

```
NONACCEPTING_INTAKE_DRAFT events=2 fills=5 complete=True export_tool_would_refuse=CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE real_packet=BUILT real_packet_tool_outcome_expected=CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE
b9a5f573790cc3cbfa3159bc1316ab1c99ddd9be6cb6f726eeee5359d74e5965  binding_packet_draft.json
e8b0176520ce05c12dc4ef65429c1d555da50e9a6ab618ac31e9fc37f285f931  retained_rows_expected.json
37d3b8ed8cefb6ca78cc6e09513faa0e620cb19d0ed8f6ddff1be6a7b37fb42e  intake_gap_report.json
f3bde0b7a1b008739df927c119fd5a654836b40af9149b58ed6e241fcd0c979b  binding_packet_real_capture.json
```

All four digests equal the record's `LEAD_INTAKE_r1_s4_stdout.txt` exactly, including `binding_packet_real_capture.json` = `f3bde0b7…` (the same value `LEAD_EXPORTER_r1_real_packet.txt` names as the packet sha256). The adapter is deterministic on these bytes.

Exporter, pure function, FIXTURE retained rows (2, built as `LEAD_EXPORTER_r1_real_packet.txt` describes — `Store._FUNDING_PAYLOAD_FIELDS` domain, `reconcile_digest`, `ATTRIBUTED`):

| Call | Observed |
|---|---|
| real profile, packet **as emitted** | `False` `CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE` — D-4, `oracle_price_source` is `UNRESOLVED:D-4` because r1 captured no oracle read |
| default (SYNTHETIC) profile, same packet | `False` `CANDIDATE_EVIDENCE_KIND_MISMATCH` |
| real profile + FIXTURE oracle locator | `True` `REAL_CAPTURE_CANDIDATE_BUILT` |

The built candidate's root keys, labels and completion check match the record exactly:

```
root keys         ['admission_status','artifact_kind','bridge_payload_digest_domain','evidence_kind',
                   'not_a_production_record','numeric_representation','real_capture_candidate',
                   'source_event_digest_domain','synthetic_only']
artifact_kind     REAL_CAPTURE_FUNDING_CANDIDATE_V1   synthetic_only False
admission_status  REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD
completion_check  {'expected_funding_hours': ['2026-09-14T17:00:00Z','2026-09-14T18:00:00Z'],
                   'observed_funding_hours': ['2026-09-14T17:00:00Z','2026-09-14T18:00:00Z'],
                   'opening_position': '0.0', 'position_source': 'coverage.fills_witness'}
```

(My candidate sha256 `661cf9e5…` differs from the Lead's `8eb1efe3…`; that is expected — my fixture retained payloads, oracle price and `schedule_id` are my own. The structure, labels and completion check are identical.)

None of the three MTC selection keys (`events`, `schedule_id`, `settlement_currency`) is present at the candidate root: the real candidate is structurally non-consumable exactly as the synthetic one is.

**No address leak.** The full mainnet address `0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49` appears in **none** of the six artifacts, either literally or inside the hex-encoded capture blobs (I decoded every `[0-9a-f]{64,}` string and searched the decoded bytes). Only the short form `0x1E26…AC49` is carried. The bare `0x`+40-hex regex is **not decisive** here and must not be used alone: a venue `0x`+64-hex transaction hash contains a 40-hex prefix, so the regex matches the fills' real tx hashes inside the embedded witness. What those matches are: the funding rows' zero hash, and — inside `coverage.fills_witness` — r1's **real** fill transaction hashes, order ids, trade ids, prices and fees, carried verbatim as the D-6 fills witness requires. That is real venue trading data embedded in the candidate by design; it is not the account identifier.

**Capture directory unchanged.** Per-file SHA-256 of all 14 files before and after the run: identical (`capture_before.txt` == `capture_after.txt`).

## 5. Overclaim and honest limits

**Nothing reads as accepted or production evidence.** On an accepted real-capture run the candidate carries `admission_status = REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD`, `synthetic_only: false`, `evidence_kind: REAL_CAPTURE_READ_ONLY`, and none of `events` / `schedule_id` / `settlement_currency` at the root. The report's `non_admission.statement` names `OD-20260914-P012-ADMISSION-Q3 ("Wait")` verbatim. The adapter's `real_capture_packet` block states "It admits NO production evidence" and names both the expected refusal and the gate order. I could not find a sentence anywhere in the four files or the emitted artifacts that claims admission, acceptance or production status. `REAL_CAPTURE_EVIDENCE_LIMITATIONS` is carried into the report on every real-profile run, refusals included.

**Are the Lead's stated limits visible in the artifacts themselves?** Three of four, with one qualification:

| Stated limit | Visible in an artifact? |
|---|---|
| D-4 is a naming check; the oracle capture is not opened or re-verified | **Yes** — `evidence_limitations[2]`, in the report on every real run |
| D-5 is a naming check; the manifest/ownership record is not re-opened | **Yes** — `evidence_limitations[1]` |
| `PRODUCTION_MODE_UNAVAILABLE` wording is stale for the real kind | **Partly** — the stale string `production_mode: "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"` is in the report; nothing in any artifact says it is stale. Disclosed only in the Lead record. → NIT-3 |
| No schema-v10 store carries the owner's events, so the CLI refuses at the snapshot step and every real run today uses FIXTURE retained rows | **No** — stated in `tests/test_mtc_funding_export_real_capture.py:14-18` (a test docstring) and the Lead record, not in the exporter docstring and not in any emitted artifact. `evidence_limitations` says nothing about the Bridge half of the join. → NIT-3 |

Two labels on an accepted real-capture run contradict their own content: `report_kind` stays `SYNTHETIC_FUNDING_CANDIDATE_REPORT_V1` and `inputs.synthetic_schedule_id` keeps the word "synthetic" while `synthetic_only` is `false`. Both err toward under-claiming, so neither is an overclaim; both are confusing in an evidence artifact. → NIT-3.

The adapter's gap report is honest about D-4: `decisions_applied` lists D-1, D-2, D-3, D-5, D-6 and deliberately omits D-4, which appears under `unresolved` with the reason "no oracle capture at the funding instants exists in this run". The `intake_gap_report.json` for r1 carries no oracle price at all, and the pinned adapter test asserts the back-derived price (`usdc/(szi·rate) ≈ 78758.6`) appears in no output — I confirmed `78758`/`78759` occur in none of the four emitted files.

## 6. Tests and RED evidence

**RED arm reproduced exactly.** Scratch copy of `IBKR_PAPER_BRIDGE` with `git cat-file blob f12570e7…` (the `4c802e9b` exporter) swapped in — blob id of the written file re-hashed to `f12570e704821fdae26d2461e4b0ab6f2c6ca854`, the new test module's blob unchanged at `84d6b3e0…`:

```
57 failed in 2.03s
```

All 57 cases of the new module are RED on the pre-slice bytes. Every new test therefore has a RED arm.

**Mutants reproduced.** Three of four, in a workspace pinned to the HEAD exporter blob `216b9cc3…`:

| Mutant | Edit I applied | Result | Lead's record |
|---|---|---|---|
| M1 | `REAL_END_TOLERANCE_SECONDS = 1 → 0` | 2 failed, 55 passed — `test_d6_one_second_end_tolerance_admits_the_venue_late_stamp`, `test_r1_with_a_named_oracle_capture_materializes_a_labelled_candidate` | identical |
| M2 | the row-`szi` cross-check disabled (`if at_stamp != row.szi` → `if False`) | 1 failed, 56 passed — `test_d6_a_row_position_that_disagrees_with_the_fills_refuses` | identical |
| M3 | D-1 compares a canonical re-serialization on **both** sides of `_verify_real_row_witness` | **11 failed**, 46 passed, including `test_d1_digest_must_hash_the_exact_captured_row_bytes_not_a_reserialization` | identical (11 failed, same names) |

A note on M3: my first attempt canonicalized only `_PassRow.raw` and produced **10** failures — the sharpened D-1 test survived, because the witness-bytes comparison caught it first. Canonicalizing both operands (the Lead's edit) reproduces 11/11. **So the sharpened test does discriminate on its own**, and the Lead's disclosure of the sharpening is accurate.

**What each new test catches.** Grouped (34 functions, 57 cases): explicit admission — the default profile never selects real, both mismatch directions, a foreign provenance kind, unknown kinds, the CLI's `choices`. D-1 — re-serialization, domain tag (untagged / wrong domain / upper-case hex), witness bytes not the located span, reuse of the Bridge payload digest. D-2 — four wrong identity forms, and a binding that locates the *other* captured row while its own D-1 still holds. D-3 — four stamp/hour-key forms, and the hour key as a required ninth field. D-5 — five identity forms. D-6 — window alignment, pass count and byte-identity, pass digest, both sides of the tolerance, a missing payment, a row `szi` disagreement, a gap in the fills chain, malformed fills, uninventoried rows, a foreign coin, an empty inventory, the closed coverage shape. Plus two CLI staging tests and a determinism test.

**Tests that could pass for the wrong reason.**

- `test_d6_a_stamp_more_than_one_second_past_the_end_is_out_of_interval` does **not** discriminate the tolerance *value*: it still passes with `REAL_END_TOLERANCE_SECONDS = 0` (M1 shows it among the 55 passing). Its partner `test_d6_one_second_end_tolerance_admits_the_venue_late_stamp` is what pins the value. The pair is correct; the name of the first suggests more than it proves.
- `test_the_real_profile_is_never_selected_by_default` asserts `ACCEPTED_EVIDENCE_KINDS == (SYNTHETIC_FIXTURE,)`. That constant no longer gates anything (NIT-1), so the assertion pins a name, not a behaviour. The *behaviour* is covered by the surrounding assertions.
- **The `completion_check` provenance block is asserted by no test at all**, and its no-fills branch is unreached by the suite. Three mutants of mine survive both exporter test modules (see REQUIRED-1).

**The carried production fence still holds, and now on both profiles.** `test_no_literal_evidence_kind_unlocks_production` exercises six literals under the default profile only. I ran all six under the **real** profile as well, in `coverage.evidence_kind`, in `provenance.evidence_kind`, and as the caller's argument — 18/18 refuse with `CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE`. `{"allow_production","production_enabled","approve","force"} ∩ dir(exporter) = ∅`.

**The two changed adapter assertions: a disclosed correction, not a silently changed fence.** The diff removes exactly two semantic assertions (a third removed line is a pure `ruff format` rewrap of the same assertion):

```
- assert intake["retained_rows"]["rows"][0]["payload_digest"] == "UNRESOLVED:D-1"
+ assert intake["retained_rows"]["rows"][0]["payload_digest"] == adapter.BRIDGE_DIGEST_UNAVAILABLE
- assert row["payload_digest"].startswith("UNRESOLVED:D-")
+ assert row["payload_digest"] == adapter.BRIDGE_DIGEST_UNAVAILABLE
```

Judged against the exporter's own rule: `CANDIDATE_DIGEST_DOMAIN_CONFLATION` (`:1617-1622`) refuses a binding that reuses the Bridge payload digest as a `source_event_digest`, and the docstring (`:61-63`) states `payload_digest` "is never renamed to, reused as, or compared equal to a `source_event_digest`". Labelling `payload_digest` with the **D-1** decision id placed it inside the `source_event_digest` domain — the conflation the exporter exists to refuse. `UNAVAILABLE:BRIDGE_OBSERVATION_REQUIRED` says the true thing: it is a Bridge observation and no store has observed these events. The replacement assertion is also **stronger** (an exact equality replacing a `startswith`). This is a correction in the right direction, disclosed in the commit and the record. Its documentary half was left behind → NIT-4.

## 7. Format-only commit — proved twice

`git diff --stat 4c802e9b b667dbcc` touches exactly one file: `IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py` (+90/−58).

**Ruff** (`ruff format --check --isolated`, on the blobs extracted with `git cat-file blob`):

| Blob | Result |
|---|---|
| `f12570e7…` (`4c802e9b`) | `1 file would be reformatted`, exit 1 |
| `bb73329b…` (`b667dbcc`) | `1 file already formatted`, exit 0 |

**AST identity** — the decisive test:

```
IDENTICAL ABSTRACT SYNTAX TREE: True
```

`ast.dump(ast.parse(before)) == ast.dump(ast.parse(after))`. The commit changes no semantics whatsoever.

**Every non-whitespace token difference, enumerated.** A token-stream diff (whitespace, indent and newlines ignored) shows exactly six changes, all canonical `ruff format` behaviour:

- one redundant parenthesis pair removed around a single string literal (`CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE = ( "…" )` → `= "…"`);
- five magic trailing commas added.

So the diff is **not literally whitespace-only** — the brief's "reflow only" is true in substance but not to the letter. Given AST identity, the commit message's own claim ("no semantic change") is the accurate one, and I do not raise this as REQUIRED: a magic trailing comma is not a change to the program. Recorded as NIT-7 for exactness.

**Ruff `check`** — the same five findings at all three revisions, by rule and location, so the slice introduces **0 new** findings:

| Rev | Findings |
|---|---|
| `4c802e9b` | UP035 @89, ISC004 @209/212/214, SIM101 @383 |
| `b667dbcc` | UP035 @89, ISC004 @207/210/212, SIM101 @385 |
| `9ef072a8` | UP035 @106, ISC004 @277/280/282, SIM101 @542 |

The other three slice files: no findings. This matches `LEAD_RUFF_s4.txt` exactly.

**GREEN arm at `b667dbcc` bytes.** I could not reproduce "161 passed" in a scratch copy, for a reason unrelated to the bytes: `test_prepare_staging_refuses_the_current_owned_mtc_production_parent` (`tests/test_mtc_funding_export.py:1984`) resolves `Path(__file__).parents[2]` to the repository root and asserts the sibling `MTC_COMMAND_CENTER/01_MTC_PROJECT/…/funding` directory exists, which a copy of `IBKR_PAPER_BRIDGE` alone does not have. I established equivalence by triangulation instead — the same scratch tree, the same command, only the exporter blob swapped:

| Exporter blob | `tests/test_mtc_funding_export.py` |
|---|---|
| `4c802e9b` | 1 failed, 159 passed, 2 skipped |
| `b667dbcc` | 1 failed, 159 passed, 2 skipped |
| `9ef072a8` (control) | 1 failed, 159 passed, 2 skipped |
| `9ef072a8` in the **real worktree** | **161 passed, 1 skipped** |

The single failure and the extra skip are identical at all three revisions including the pristine HEAD control, and both are explained by the copy's location (the extra skip says so itself: "MTC record loader is not present in this worktree"). Combined with AST identity, the format-only claim is proven.

## 8. Scope and safety — VERIFIED

- **Exactly four files.** `git diff --name-only b667dbcc 9ef072a8` returns the four the brief names and nothing else.
- **No `bridge/` runtime module touched.** All four paths are under `IBKR_PAPER_BRIDGE/tools/` and `IBKR_PAPER_BRIDGE/tests/`.
- **No new dependency, not even a stdlib one.** Diffing the import blocks between `b667dbcc` and `9ef072a8`: *no change* in either tool. The exporter imports stdlib plus the two pre-existing Bridge helpers (`bridge.engine.types`, `bridge.store.db`); the adapter is stdlib-only (`argparse, hashlib, json, sys, datetime, pathlib, typing`).
- **No env read, no network, no key.** Grep over both tools for `os.environ|getenv|requests|urllib|http|socket|subprocess|secret|api_key|private_key|wallet|sign(|eth_account|hyperliquid`: the only hits are the literal string `"Hyperliquid userFunding …"` in two `source_title` values and the docstring text about PRAGMAs. `os` is imported by the exporter solely for `os.path.abspath` in the staging-safety helpers.
- **No database write, no live copy.** Every write call in either tool: `open(path,"rb")` (read), `open(path,"xb")` (exclusive create, staging + adapter outputs), `tempfile.mkdtemp`, `scratch.rename`, `child.unlink`/`scratch.rmdir` (scratch cleanup), `out_dir.mkdir`, `write_text` (sidecars). No `INSERT`/`UPDATE`/`DELETE`/`CREATE TABLE`, no `conn.execute` outside the composed Store readers, no `shutil.copy`, no `Store(...)` instantiation, no `Store.initialize()`. The snapshot is opened `…?mode=ro&immutable=1` and `_ReadOnlySnapshot` composes the unbound Store methods so `Store.conn`'s WAL/foreign-key PRAGMAs are never executed. The real profile changes none of this.
- **Capture directory untouched** by the adapter run (per-file SHA-256 before/after, identical).

## Findings

### REQUIRED

**REQUIRED-1 — the D-6 `completion_check` states a provenance it does not have, on an accepting branch no test reaches.**
`IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py:1222-1232` (the `opening is None` fallback) and `:1259-1264` (the emitted `completion_check`); the same misstatement is in `:178-183` (`REAL_CAPTURE_EVIDENCE_LIMITATIONS[3]`).

When the fills witness carries no fill for the symbol, `_real_completion` abandons the fills and takes the position from the **payments' own `szi`**. The emitted artifact does not say so:

```
fills_witness = "5b5d"        (the exact bytes "[]"), five hourly payments, window [15:00,19:00)
-> accepted=True REAL_CAPTURE_CANDIDATE_BUILT
   completion_check = {'expected_funding_hours': [...5 hours...],
                       'observed_funding_hours': [...5 hours...],
                       'opening_position': None,
                       'position_source': 'coverage.fills_witness'}
```

Same outcome when the fills witness carries only another coin's fills. In that branch the per-row `szi` cross-check is also vacuous — every row is compared against a constant derived from all the rows' own `szi` — and the owner's D-6 ("an expected-count check fed by the fills pass of the same capture") is no longer fed by the fills pass, while `position_source` says it is.

I verified that nothing in the suite constrains this. Three mutants inside the ruled D-6 witness **survive the whole focused suite** — all three modules together, including `tests/test_funding_intake_adapter.py`, whose slice-4 tests round-trip a real packet through `build_funding_candidate` under the real profile. Run with an explicit pristine control, in the §7 scratch tree:

| Exporter | Result |
|---|---|
| **control** — pristine HEAD bytes | 1 failed, 227 passed, 2 skipped |
| the no-fills branch returns `Decimal(0)` instead of the rows' `szi` | 1 failed, 227 passed, 2 skipped — **no test fails** |
| `position_source` relabelled to `"THIS_LABEL_IS_WRONG"` | 1 failed, 227 passed, 2 skipped — **no test fails** |
| `opening_position` always reported `None` | 1 failed, 227 passed, 2 skipped — **no test fails** |

The single failure is identical in all four rows, the control included: it is the copy-location artifact of §7, not a mutant kill. No mutant changes the result by even one case.

`grep` confirms why: `grep -rn "opening_position\|position_source" tests/` returns **0 matches across the whole test tree**, and the only empty fills witness anywhere (`tests/test_mtc_funding_export_real_capture.py:900`) sits in the empty-inventory test, which refuses before `_real_completion` is ever reached.

This is not a fence hole — the branch still demands a payment at every grid hour, which is stricter than the fills-derived expectation — but it is a **false statement about its own evidence source inside an accepted evidence artifact**, on a path with zero test coverage, under the exact rule this slice was authorized to implement.

*Fix (small):* in the `opening is None` branch, emit a `position_source` that names the real producer (e.g. `"captured funding rows (the fills witness carries no fill for the symbol)"`), qualify `REAL_CAPTURE_EVIDENCE_LIMITATIONS[3]` for that case, and add two tests — one asserting the accepting no-fills branch and its labels, one asserting `completion_check`'s two provenance fields on the normal r1 path. Roughly ten lines plus two tests; it kills all three surviving mutants.

### NITs

**NIT-1 — `ACCEPTED_EVIDENCE_KINDS` no longer gates anything, and the message it feeds is now wrong.** `:127`, `:632-636`. The real gate is `_EVIDENCE_PROFILES`. Observed under the real profile: `coverage.evidence_kind = "PRODUCTION_LIVE"` → *"only `['SYNTHETIC_FIXTURE']` is accepted"* — false, the caller had admitted `REAL_CAPTURE_READ_ONLY`. The constant's value is correct as a statement of what is *accepted for production*; the message should name the caller's admitted profile.

**NIT-2 — the tolerance boundary is the implementation's choice, not the row's.** `:1607`, `:1614`. `end_limit` with a strict `<` makes the band half-open `[end, end+1 s)`: a stamp at exactly **+1.000 s** is refused (I pinned +0.999 accepted / +1.000 refused / +1.060 refused). Defensible, and it matches the venue's observed 41-60 ms lateness by a wide margin, but worth one sentence in the docstring so the next reader does not have to re-derive it.

**NIT-3 — labels and limits that are stale or missing on a real-capture run.** `:133`+`:1778` (`production_mode` prose stale for the real kind — Lead-disclosed, Gemini NIT-1, confirmed present in the artifact with nothing marking it stale); `:1781` (`report_kind` stays `SYNTHETIC_FUNDING_CANDIDATE_REPORT_V1` while `synthetic_only: false`); `:1762` (`inputs.synthetic_schedule_id` on a real run); and the "no schema-v10 store carries these events, so today's real runs use FIXTURE retained rows" limit, which lives only in a test docstring and the Lead record — not in `REAL_CAPTURE_EVIDENCE_LIMITATIONS`, which says nothing about the Bridge half of the join.

**NIT-4 — value changed, field left behind (adapter).** `IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py:59`. `DECISIONS["D-1"]` still reads "production `source_event_digest` byte domain **(also the retained payload_digest domain)**" after `:57`/`:460`/`:503` moved `payload_digest` out of that domain to `UNAVAILABLE:BRIDGE_OBSERVATION_REQUIRED`. The gloss is now contradicted by the owner's D-1 (which mentions only `source_event_digest`), by the corrected value, and by the exporter's `CANDIDATE_DIGEST_DOMAIN_CONFLATION` rule. It is emitted into every `intake_gap_report.json`.

**NIT-5 — D-4's `"derived"` substring blacklist can only produce false refusals.** `:885-886`. Demonstrated: a syntactically perfect oracle locator whose JSON pointer happens to be `#/derived/oraclePx` is **refused**; the same capture under `#/assetCtxs/1/oraclePx` is accepted. And the blacklist buys nothing — I fed the back-derived price `78758.6` with a valid-looking locator under a different pointer name and it was **admitted** (the tool never re-verifies the price, as `evidence_limitations[2]` says). The format check is the real guard; the substring test should go or be narrowed to the whole field value.

**NIT-6 — the window is a payment-stamp window and nothing says so; it needs one owner sentence.** See §3 for the reproduction. The accrual coverage is `[start − 1 h, end)`; a payment stamped `15:00:00.041Z` settling `[14:00,15:00)` is inside a `[15:00, …)` window and is *mandatory*. Separately, the exporter's +1 s tolerance is not mirrored in the capture request (`endTime = end_ms`), so a capture whose window does not end flat cannot satisfy D-6 at all. Neither is an owner decision today; both should become one before the next capture is commissioned. Related naming: `interval_hour_utc` names the **payment hour**, not the accrual interval it settles.

**NIT-7 — the draft packet's `UNRESOLVED:D-n` labels are stale after the ruling, inconsistently with the one that was updated.** `funding_intake_adapter.py:58-65`, `:429`, `:436`, `:443`, `:501-509`. `OD-20260916-P012-INTAKE-D1-D6-R-1` closed all six decisions, yet `binding_packet_draft.json` still carries `"source_event_digest": "UNRESOLVED:D-1"`, `"evidence_kind_status": "UNRESOLVED:D-5"`, `"funding_event_id_rule": "PROPOSED:D-2 …"`, and `DECISIONS` still phrases all six as open questions. One label in the same file (`payload_digest`) *was* updated for the ruling, so a reader cannot tell which labels are current. Also cosmetic in the same dict: `gap_report["unresolved_fields"]` now mixes decision ids (`"D-1"`, `"D-2"`, …) with a status string for one key.

**NIT-8 — small consistency items.** (a) `funding_intake_adapter.py:167-199` `array_spans` has no trailing-byte check, where the exporter's `_json_array_spans` (`:1098-1101`) refuses trailing bytes; the adapter is protected only by the manifest re-hash. (b) The adapter's `utc_z`/`hour_z` (`:117-121`, `:138-141`) use float arithmetic where the exporter's `_millisecond_text`/`_hour_text` use exact integers; I swept 14 450 stamps across the r1 window and the extremes and found **0 disagreements**, so this is not a live defect, only a divergence from the file's own exact-decimal discipline. (c) `git diff 4c802e9b b667dbcc` adds five magic trailing commas and removes one redundant parenthesis pair — AST-identical, but the commit is not literally whitespace-only.

## NOT VERIFIED

Things this review did **not** establish, and that nobody should read the verdict as covering:

1. **That any oracle price is the venue's oracle price at the funding instant.** D-4 is a naming check; the tool never opens the named capture. Any positive decimal under a syntactically valid `<sha256>#/pointer` is admitted (demonstrated). The artifact says so (`evidence_limitations[2]`) — but the claim is unverified, and no oracle capture tool exists yet.
2. **That the capture is of the owner's account.** D-5 is a naming check on free text, and `coverage.account_scope` is caller-supplied. A packet that consistently names a different account (ids, ownership clause, scope) cannot be detected by this tool; it never re-opens the manifest or the ownership-signature record. Stated in `evidence_limitations[1]`.
3. **The CLI end-to-end on a real capture.** Not runnable: no schema-v10 Bridge snapshot carries these events (the deployed store is v4). I exercised the CLI only through the module's own two CLI tests and the pure function with FIXTURE retained rows. Every "real-capture candidate built" result in this review, the Lead's included, rests on fixture Bridge evidence.
4. **`161 passed` at `b667dbcc` bytes in a scratch tree** — see §7; established by triangulation and AST identity instead, not by that literal count.
5. **The venue's exact `endTime` inclusivity for `userFunding`.** My NIT-6 end-side conclusion is reasoned from r1's manifest request body (`endTime = 1789412400000`) and the captured rows; I did not query the venue. The conclusion holds either way, since a payment stamped 41-60 ms past `endTime` is outside the request bounds under both readings.
6. **The `.impeccable/` subdirectory** inside the r1 capture directory (created 2026-09-17 10:00, after the capture) — not a capture artifact; excluded from my before/after hash set, and I did not inspect it.
7. **Anything about merge readiness of the branch as a whole**, the Bridge half of the join, or the P0-12 gate order. Production admission is not granted; `OD-20260914-P012-ADMISSION-Q3` "Wait" stands and nothing in this slice touches it.

## Summary

The slice does what the ruling authorized and does it well. The admission is explicitly named on both surfaces with no inference path and no `--mode`; all six rules are re-derived from the exact captured venue bytes and refuse every failing input I built (17/17); the carried synthetic fences are byte-identical and still green, on both profiles; the r1 dry run reproduces the Lead's four digests exactly; the format-only parent is AST-identical to its own parent; scope and safety are clean; and the two changed adapter assertions are a correction in the right direction, not a loosened fence.

One defect stands in the way: inside the ruled D-6 witness there is an accepting branch that no test reaches, and on that branch the accepted artifact names `coverage.fills_witness` as the source of a position the fills witness did not supply. Three mutants of that block survive the entire suite. In a package whose whole subject is evidence naming its true producer, that has to be fixed before merge — and it is a small fix.

VERDICT: REQUEST_CHANGES
