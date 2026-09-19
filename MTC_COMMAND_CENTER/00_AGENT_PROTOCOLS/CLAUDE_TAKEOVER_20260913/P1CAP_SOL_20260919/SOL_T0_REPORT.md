# Independent T0 Review — P1CAP NIT Slice `1029d6e9`

Reviewer: gpt-5.6-sol xhigh, the second independent flagship. I did not read any
`*OPUS_T*_REPORT.md` or any Lead adjudication of an Opus report before fixing this verdict. I made
no network call and did not re-run either real capture.

## Executive result

`1029d6e9` closes the seven stated NITs in their narrow form, except that NIT-2's ordering repair
does not enforce the requested start on later pages. Two independently executed RED arms show
successful captures where the tool must refuse:

1. **REQUIRED R-1:** a later page may contain a row before that page's `cursor`; the code checks
   only the original `start_ms`, then accepts a short page as terminal. Repeating the same malformed
   pagination in pass 2 makes re-query agree and permits an incomplete `CAPTURE_OK`.
2. **REQUIRED R-2:** SDK `API.post` represents a 2xx non-JSON response as an `{"error": ...}`
   dictionary. `account_state_query` accepts every dictionary, so that failed account-state query
   can also end in `CAPTURE_OK`.

There are also two evidence/style NITs: the r2 replay has a valid mutation fence despite the
package's original “no mutant” rationale, and both changed Python files fail the configured
`ruff format --check`.

## Verified identities

COMPUTED with the permitted immutable-revision commands and SHA-256 over committed bytes:

| Identity | Computed value |
|---|---|
| Worktree HEAD | `1029d6e921b28b66ea1480c80f31aa053a2e82f9` |
| `tools/capture_own_account_evidence.py` | `110146c16a701e4dc1663a81a60326cee6041bad1ae0d847a8c6d4dac56e9d9c` |
| `tools/path1_sign_ownership.html` | `b43dbe39aaa9536fbc8f3e05d29ddc851ad3d2e3e271e1bee38b53fddc54e01f` |
| `tests/test_capture_own_account_evidence.py` | `c38861d3c5f9ece6f6d2dab430100dd7e86abc3f4e9239ed149514788128fcfa` |

Scope was computed with
`git -c safe.directory=* -C C:/tmp/P1CAP_20260914 diff --name-status af921d75 1029d6e9 -- .`:
exactly the tool, its test module, and 15 new files under
`tests/fixtures/p012_path1_r2_capture/` (17 paths total). The base branch diff
`fcac0ac6..af921d75` is exactly the original three files. No protected path is touched.

### Real r1 capture hashes

Pinned Python 3.12 computed each digest from bytes and compared it to both the sidecar and, for
responses, the manifest entry:

| File | SHA-256 | Sidecar | Manifest |
|---|---|---:|---:|
| `CAPTURE_MANIFEST.json` | `c837cf1237e9c2d8dfdad250815ee17fbd28e1cd0f98b901ec508f9ed6c2c9cb` | EQUAL | not self-recorded |
| `DERIVED_EXTRACTION.json` | `feb43cd26729b26c8b0419b6eb8d47135d345d1faff93163ee8597b3178047c7` | EQUAL | old manifest: unrecorded |
| `fills_pass1_page001.json` | `6cb8586c5b446f6807296fa81c8c2bc5f0d7d249a34b0d0c0980732d6fb18589` | EQUAL | EQUAL |
| `fills_pass2_page001.json` | `6cb8586c5b446f6807296fa81c8c2bc5f0d7d249a34b0d0c0980732d6fb18589` | EQUAL | EQUAL |
| `funding_pass1_page001.json` | `6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f` | EQUAL | EQUAL |
| `funding_pass2_page001.json` | `6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f` | EQUAL | EQUAL |
| `account_state.json` | `ea77db9ab583be926f1dcfae35ef02e629fcb0102efbf0cc4965aae539d6e4fe` | EQUAL | EQUAL |

Both fill passes and both funding passes are byte-identical. Current `--verify-existing` prints
`CAPTURE_VERIFY_OK` for r1 and for the checked-in r2 fixture. R1 records mainnet, the declared owner
address, run `p012-path1-20260914T1500Z-1900Z-r1`, half-open 15:00–19:00Z, and
`OWNERSHIP_EVIDENCE: VERIFIED`. Its derived view contains five fills and two funding settlements;
exact decimal reconciliation is `0.320856 - 0.035831 - 0.001143 = +0.283882 USDC`.

The r2 fixture's manifest/page/derived/account-state sidecars also all equal their files; its five
manifest response digests equal the files, and its two query passes are byte-identical.

## Promise conformance

| Packet section 5 promise | Implementation | Result |
|---|---|---|
| CLI inputs address, product, UTC window | `capture_own_account_evidence.py:643-669,749-760` | EQUAL |
| Use only `Info.user_fills_by_time`, `Info.user_funding_history`, and `user_state` | `:302-335,428-459,671-717`; `make_info` at `:170-171` constructs only `CapturingInfo` | EQUAL |
| Preserve response bytes, SHA-256 sidecars, request/manifest provenance | `:91-102,135-150,273-299,720-745` | EQUAL |
| Preserve bytes before HTTP error handling and JSON parsing | SDK `hyperliquid/api.py:20-28`; override `capture_own_account_evidence.py:91-102` | EQUAL |
| Refuse failed queries while keeping error bytes | `:190-210,395-425` | DIFFERENT for 2xx non-JSON account state; see R-2 |
| Complete pagination with inclusive cursor restart, dedup, caps, and truncation refusal | `:302-393` | DIFFERENT: later-page rows are checked against original `start_ms`, not the actual `cursor`; see R-1 |
| Half-open `[start,end)` derived interval | `:360-373,734-740` | EQUAL for well-formed pages; completeness is still defeated by R-1 |
| Refuse re-query identity or content divergence | `:626-640,718-719` | EQUAL; repeated identical malformed pagination is outside this comparison and triggers R-1 |
| Never take a key and never write to the venue | key refusal is first statement of `run_capture` at `:644-645`; imports at `:31-35`; no exchange client; `:170-171` | EQUAL |
| File-source adapter/snapshot writer | No adapter is in this three-file tool scope; packet explicitly left the choice to a later builder/reviewer | DIFFERENT, declared future work rather than scope creep |

`CapturingInfo.post` uses the SDK's same URL, session, JSON payload, and timeout, but copies
`response.content` into `RawCapture` before `_handle_exception` and parsing. Each real manifest body
therefore equals the posted SDK payload and truthfully records `raw_bytes_source:
http_response_content`; the test-double fallback is separately labelled.

## F/L disposition and RED-on-pre-fix judgement

The exact pre-fix arm used `e77af1c8`'s tool, `af921d75`'s 21-test module, and a minimal path-only
`conftest.py` under `C:/tmp/SOL_P1CAP_SCRATCH/red_base_e77`:

```text
F..FFFFFF.F.FF....FF. [100%]
12 failed, 9 passed in 1.31s
```

| IDs | Current disposition / test | RED on `e77af1c8` for the right reason? |
|---|---|---|
| F-1 | CLOSED: `test_signature_without_run_id_refuses_before_network_and_writes_nothing` | Yes: missing code/token and no pre-network gate |
| F-2 | **PARTIAL / REQUIRED R-1**: original-start/end arms pass, but current-cursor enforcement is absent | Existing end/before-start/after-end tests are right REDs; they do not cover later-page `t < cursor` |
| F-3, L-4 | CLOSED: ownership is recovered before mkdir/client construction | Yes: wrong signature made two fill calls on e77 |
| F-4, L-3 | CLOSED: `test_funding_identity_includes_coin` | Yes: two coins collided under hash+time |
| F-5, L-5 (exclusive create) | CLOSED: `test_write_once_refuses_an_existing_output` plus code inspection of `xb`/`x` | The e77 failure was detail-only (`refusing to overwrite` vs `output exists`); it does not alone prove the race fix |
| F-6, L-5 (error bytes) | CLOSED for raised/non-2xx queries: `test_error_response_bytes_are_kept_before_refusal` | Yes: no `_ERROR.json` path on e77. New R-2 covers an unraised SDK parse failure |
| F-7, L-6 | CLOSED: manifest records HTTP vs test-double provenance | Yes: e77 `RawCapture` had no `source` |
| F-8 | CLOSED as coverage: fake session drives `CapturingInfo.post` success and non-2xx capture | The combined test fails on e77 only at the later F-7 provenance assertion; its pre-parse-byte assertions already pass |
| F-9, L-2 | CLOSED: multi-page boundary dedup and wrong-signature/no-write arms exist | Multi-page already passes e77; wrong-signature-before-network is the substantive RED |
| F-10, L-1 | Selected Ruff rules GREEN; **format NIT remains** | Not a pytest RED. Current `ruff format --check` reports both files would be reformatted |
| F-11 | CLOSED: `test_requery_content_mismatch_refuses` | Yes: e77 accepted changed row content. The identity-detail assertion was the other detail-only failure |

Thus the documented “two REDs fail only by detail assertion” qualification is accurate: the
existing-output message and identity-mismatch detail. The other ten failures expose missing behavior
or data, although F-8's combined test reaches an F-7 assertion rather than proving a new F-8
behavioral delta.

## NIT-slice disposition

| NIT | Byte/test inspection | Own mutation result | Disposition |
|---|---|---|---|
| 1 | All top-level sidecars are walked and derived digest is manifest-bound at `:579-623,725-745` | responses-only verifier: `DID NOT RAISE` on tampered derived view | CLOSED |
| 2 | Within-page descending times refuse at `:349-359` | removed check: `DID NOT RAISE` | Narrow NIT CLOSED, but F-2 remains PARTIAL because cross-page `t < cursor` is accepted (R-1) |
| 3 | Account-state bytes are recorded before non-dict refusal at `:428-463` | moved shape check earlier: `account_state.json` absent | Narrow NIT CLOSED; R-2 is a distinct accepted-dictionary failure |
| 4 | r2 sidecars and real-byte derivation replay at test `:454-478` | `af921d75` full product-code revert: `1 passed`; deleting only `closedPnl` projection: `1 failed, 31 passed` | Product/test CLOSED; supplied “no mutant” rationale is false (NIT N-1) |
| 5 | Missing `tid` refuses at `:222-234` | restored fallback: `DID NOT RAISE` | CLOSED |
| 6 | Signature file/read/recovery failures become named refusals at `:515-555,569-623` | removed both guards: four raw-exception failures | CLOSED |
| 7 | Manifest stores exact message, signature, and `binds` at `:537-566` | old two-field result: `KeyError: 'message'` | CLOSED |

The Python `ownership_message` (`:108-113`) and HTML `buildMessage` (`path1_sign_ownership.html:31-33`)
are character-for-character equal for r1: 135 characters and identical code points. Offline EIP-191
recovery from the recorded signature returns the manifest address. The auxiliary
`OWNERSHIP_MESSAGE_r1.txt` is 139 bytes rather than the 135 signed UTF-8 bytes (file encoding/line
ending wrapper); it was not used as the recovered message byte source.

## Own RED arms

All commands used Python 3.12.12, removed `HL_API_WALLET_KEY`, set
`PYTHONDONTWRITEBYTECODE=1`, used `-p no:cacheprovider`, and wrote only under the named scratch root.

### Current focused GREEN

```text
cwd: C:/tmp/P1CAP_20260914/IBKR_PAPER_BRIDGE
command: C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest tests/test_capture_own_account_evidence.py -q -p no:cacheprovider --basetemp C:/tmp/SOL_P1CAP_SCRATCH/basetemp_current_1029d6e9
................................ [100%]
32 passed in 1.90s
```

### Seven stated NIT mutants

Each cwd was `C:/tmp/SOL_P1CAP_SCRATCH/mutants/<name>` and each command selected the named test from
`tests/test_capture_own_account_evidence.py` with its own scratch basetemp.

| Mutant | Exact observed result |
|---|---|
| NIT-1: return after response-only sidecar loop | `1 failed`; tampered derived view: `DID NOT RAISE CaptureRefused` |
| NIT-2: remove ascending-page check | `1 failed`; `DID NOT RAISE CaptureRefused` |
| NIT-3: shape check before `record_response` | `1 failed`; `account_state.json` does not exist |
| NIT-5: restore hash+oid+time fallback | `1 failed`; `DID NOT RAISE CaptureRefused` |
| NIT-6: remove signature read/recovery guards | `4 failed`; raw `JSONDecodeError`, `binascii.Error`, `ValueError`, `FileNotFoundError` |
| NIT-7: remove message/signature/binds | `1 failed`; `KeyError: 'message'` |
| NIT-4: delete `closedPnl` projection only | `1 failed, 31 passed`; r2 fill derivation differs |

The separately required “revert product code to `af921d75`” NIT-4 check produced `1 passed in
0.68s`, as expected: af is the code that created the fixture. That does not mean no mutation fence
exists; the isolated `closedPnl` deletion proves one does.

### Independent current-code falsification

```text
cwd: C:/tmp/SOL_P1CAP_SCRATCH/mutants/base
command: C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest tests/test_independent_review_arms.py -q -p no:cacheprovider --basetemp C:/tmp/SOL_P1CAP_SCRATCH/basetemp_independent_arms
FF [100%]
FAILED test_second_page_row_before_current_cursor_refuses - DID NOT RAISE CaptureRefused
FAILED test_account_state_sdk_parse_error_sentinel_refuses - DID NOT RAISE CaptureRefused
2 failed in 0.70s
```

The cursor arm returns the same malformed page pattern on both passes: first page is full at
`[t0,t1]`; the next request starts at `t1`, but the API double returns a short `[t0]` page. Because
`:362` compares `t0` only to original `start_ms`, and `:388-389` treats the short raw page as the
end, both passes agree and the capture succeeds. A row later than `t1` can therefore be omitted
without detection.

The account-state arm returns the exact dictionary shape used by SDK `API.post` after 2xx JSON
parse failure. `record_response` correctly preserves it, but `:460` considers it a valid account
state solely because it is a dictionary.

### Positive boundary arms

```text
command: ... pytest tests/test_independent_review_arms.py -q ... -k 'exact_start or full_raw_page'
.. [100%]
2 passed, 2 deselected in 0.66s
```

These independently confirm exact `start` and `end-1` inclusion, exact `end` exclusion, and that a
raw full page ending with an excluded `end` row advances to a short `[end]` page before stopping.

### Lint/format and broader suite

```text
C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe check --select E9,F821,F811,F401,F841,RUF100 ...
All checks passed!

C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe format --check ...
2 files would be reformatted
```

The exact full `tests` scope in the only launcher-permitted scratch tree completed as
`1597 passed, 33 failed, 1 skipped`. All 33 failures are `test_mtc_funding_export.py` rejecting its
staging directory with `CANDIDATE_STAGING_UNSAFE`; the permitted scratch root itself contains
`.git`, which that unrelated exporter intentionally refuses. I did not count these as candidate
regressions. The supplied external-basetemp record says `1630 passed, 1 skipped`; I did not write a
new basetemp outside the launcher-permitted directories to reproduce it.

## Window walk

| Row/page case | Expected | Observed |
|---|---|---|
| `time == start` | include | GREEN, independent positive arm |
| `time == end-1` | include | GREEN, independent positive arm |
| `time == end` | retain raw bytes, exclude identity/derived | GREEN, focused test + independent arm |
| `time == end+1` | refuse malformed | GREEN, focused test |
| `time < original start` | refuse malformed | GREEN, focused test |
| Full page, inclusive boundary repeated on next page | dedup identical identity and continue | GREEN, `test_multi_page_success_dedups_the_inclusive_boundary` |
| Full raw page whose max is excluded `end` | `page_max=end`; query `[end,end]`; stop only on short raw page | GREEN, independent positive arm |
| Full page with no cursor progress | refuse truncated | GREEN, `test_truncated_full_page_refuses` |
| Descending rows within a page | refuse malformed | GREEN, NIT-2 test |
| Later-page row before that page's cursor but after original start | refuse malformed | **RED: accepted; REQUIRED R-1** |

The stop condition correctly counts raw rows (`len(parsed)`) rather than admitted derived rows.
Dedup is by `tid` for fills and `hash+time+coin` for funding. A duplicate identity with different
row content refuses. Re-query compares complete `{identity: row}` maps; a one-pass-only identity or
any content divergence refuses. The real capture's two passes are byte-identical. A divergence
would be `CAPTURE_REFUSED_REQUERY_MISMATCH`, naming either the one-pass identity or the first content
difference.

## Standards

- The stage's D026 rule is satisfied for NITs 1, 2, 3, 5, 6, and 7 by independent equivalent
  mutations, and the r2 replay does have a real NIT-4 mutation fence.
- The candidate violates its own F-10 formatting evidence: the configured Ruff selected-rule check
  is clean, but `ruff format --check` identifies both changed Python files as unformatted.
- No new hard dependency, speculative abstraction, exchange client, protected-scope edit, or
  baseline smell requiring a separate finding was found. The small `_sidecar_digest` helper is
  justified by repeated failure normalization.

## Spec

- The core read-only, original-byte, ownership-before-network, write-once, sidecar, provenance,
  re-query, and half-open behavior matches the packet for well-formed responses.
- The explicit F-2 requirement to refuse a row earlier than the **cursor start** is missing on later
  pages; the implementation checks the original interval start instead.
- The account-state parse-error sentinel makes the success claim broader than the completed
  observation. A successful capture must require a genuine account-state object, not merely any
  dictionary returned by the SDK's parse-error fallback.

## Authorship and acceptance boundary

Inspection of `e77af1c8..af921d75` found no material Lead-authored behavior beyond F-1..F-11 and
L-1..L-6: the remaining changes are their tests, comments, and formatting. Inspection of
`af921d75..1029d6e9` found no behavior beyond the seven stated NIT closures and the r2 fixture.
Lead/PACKAGE authorship receives no presumption of correctness; the independent mutations above
drive the actual verdict.

This report accepts nothing by itself. Because two REQUIRED defects remain, the next candidate
needs a narrow correction, GREEN versions of both independent RED arms, the format pass, and fresh
review/reproduction. No extra reviewer can substitute for those changes.

## Findings

1. **REQUIRED R-1 — later-page lower-bound violation can be accepted as complete.**
   `capture_own_account_evidence.py:323,348-392` sends `cursor` as the request start but checks each
   row only against original `start_ms` at `:362`. A short later page containing older rows is
   accepted as terminal at `:388-389`; the same malformed sequence on pass 2 defeats re-query.
   Fix: require `t >= cursor` on every page (while retaining the original interval bound) and keep
   the executed RED arm.
2. **REQUIRED R-2 — 2xx non-JSON account-state response is treated as success.**
   `capture_own_account_evidence.py:99-102` returns the SDK-compatible `{"error": ...}` dictionary
   on parse failure; `:450-463` records it and rejects only non-dictionaries. The run can write a
   final manifest and print `CAPTURE_OK` without a parsed account state. Fix: make parse failure a
   named failed query whose raw bytes are retained, or validate the account-state schema strongly
   enough to reject the sentinel; keep the executed RED arm and assert the bytes/sidecar remain.
3. **NIT N-1 — NIT-4's “no mutant” evidence rationale is false.**
   `test_capture_own_account_evidence.py:454-478` is the sole fence on the existing
   `fill_derived` `closedPnl` branch at tool `:483-489`; deleting that branch gives exactly
   `1 failed, 31 passed`. The product closure is good; correct the evidence characterization.
4. **NIT N-2 — formatting check is not green.**
   Configured `ruff format --check` says both changed Python files would be reformatted. Apply the
   formatter and retain the selected-rule check.

## NOT VERIFIED

- No network call was made by this reviewer; neither mainnet capture was re-run.
- Real Hyperliquid pagination beyond one page remains unobserved. The checked-in r1/r2 captures
  each contain one page per query, so multi-page behavior is established only with test doubles.
- The full Bridge suite was not reproduced in a non-Git external basetemp because the launcher
  restricted writes to the report and named scratch directories; the in-scope scratch location
  triggers an unrelated exporter's Git-worktree safety refusal.
- Current venue behavior, funding cadence, and any production admission/owner acceptance are not
  established by this review.

VERDICT: REQUEST_CHANGES
