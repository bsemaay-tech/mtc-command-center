# T0 review — WP-P0-12 Path 1 read-only own-account evidence capture tool

Reviewer: exact `claude-opus-5`, effort xhigh (Wednesday 2026-09-16 queue slot; executed 2026-09-17, attempt 2 after `ATTEMPT1_CAPPED_1247Z`).
Candidate: `af921d75226932b11c5f0279b2cbf0b0de5be9e0` on `feature/p012-path1-capture-20260914`.
Brief: `C:/tmp/OPUS_QUEUE_20260916/P1CAP/REVIEW_BRIEF.md`; launch instruction `opus/BRIEF.md`.
This report is my only output; scratch under `C:/tmp/OPUS_P1CAP_SCRATCH/opus_*`.
No network call of any kind was made by me. No capture was re-run. No git command other than
`rev-parse` and `show` was executed in any repository.

---

## 1. Verified identities (COMPUTED by me)

HEAD of the subject worktree (`git -c safe.directory=* -C C:/tmp/P1CAP_20260914 rev-parse HEAD`):

```
af921d75226932b11c5f0279b2cbf0b0de5be9e0
```

sha256 of the three subject files (worktree bytes, `IBKR_PAPER_BRIDGE/`):

| file | sha256 | lines |
|---|---|---|
| `tools/capture_own_account_evidence.py` | `00b3b8f69f0e48700ea6072e9930ddefcc48f3d28420860843c2cafaa3c62ddd` | 716 |
| `tools/path1_sign_ownership.html` | `b43dbe39aaa9536fbc8f3e05d29ddc851ad3d2e3e271e1bee38b53fddc54e01f` | 58 |
| `tests/test_capture_own_account_evidence.py` | `5d141fb1ad260dfee377660ddabef3e559c4c0d07506626f06c79287b6d4021f` | 543 |

Cross-checks:

- `git show af921d75:…/capture_own_account_evidence.py` hashes to the **same** `00b3b8f6…` as the
  worktree file — the checkout is not CRLF-mangled, so every line number below is the committed one.
- `git show e77af1c8:…/capture_own_account_evidence.py` → `a1ef5ee1c1241577e0c3c4edf52a07acb71f67dc36af050d9629fcd8c2ad475d`,
  which equals `subject/capture_own_account_evidence.py` in
  `P012_PATH1_CAPTURE_TOOL_REVIEW_20260915/PACKET_SHA256SUMS.txt` — my pre-fix tree is the exact
  artefact Gemini reviewed.
- `path1_sign_ownership.html` is byte-identical at `e77af1c8` and `af921d75` (`b43dbe39…` at both, and
  in the review packet) — the P1FIX correction did not touch it, as `DISPOSITION_P1FIX.md:6` states.

Real capture record `…/P012_PATH1_REAL_CAPTURE_20260915/r1/` — every file, bytes vs `.sha256`
sidecar vs manifest entry, recomputed by me with the Bridge interpreter
(`C:/tmp/OPUS_P1CAP_SCRATCH/opus_verify_real_capture.py`, section A):

| file | bytes | sha256 | sidecar | manifest `response_sha256` |
|---|---|---|---|---|
| `fills_pass1_page001.json` | 1605 | `6cb8586c5b446f6807296fa81c8c2bc5f0d7d249a34b0d0c0980732d6fb18589` | EQUAL | EQUAL |
| `fills_pass2_page001.json` | 1605 | `6cb8586c…` (identical) | EQUAL | EQUAL |
| `funding_pass1_page001.json` | 433 | `6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f` | EQUAL | EQUAL |
| `funding_pass2_page001.json` | 433 | `6f25ba29…` (identical) | EQUAL | EQUAL |
| `account_state.json` | 309 | `ea77db9ab583be926f1dcfae35ef02e629fcb0102efbf0cc4965aae539d6e4fe` | EQUAL | EQUAL |
| `DERIVED_EXTRACTION.json` | 2141 | `feb43cd26729b26c8b0419b6eb8d47135d345d1faff93163ee8597b3178047c7` | EQUAL | *not a manifest entry* |
| `CAPTURE_MANIFEST.json` | 3497 | `c837cf1237e9c2d8dfdad250815ee17fbd28e1cd0f98b901ec508f9ed6c2c9cb` | EQUAL | *self* |

All seven also verify against the record's own digest list
(`sha256sum -c ../SHA256SUMS_r1.txt` from `r1/` → seven `OK` lines, exit 0). The manifest's
`tool_sha256` on every entry is
`00b3b8f69f0e…` = the candidate file — **the real capture was produced by exactly this code**.
`sdk_version` `0.24.0` on every entry; my interpreter reports Python 3.12.12, hyperliquid-python-sdk
0.24.0, eth-account 0.13.7, requests 2.34.2.

Independent evidence that the stored pages are **original HTTP bytes** and not a re-serialisation
(section C): re-serialising each page canonically (`sort_keys=True`, compact) does **not** reproduce
the stored bytes — the stored files keep the venue's key order (`coin,px,sz,side,time,…`), while the
tool's own `json_bytes` (line 130-131) always sorts. `CAPTURE_MANIFEST.json` and
`DERIVED_EXTRACTION.json` *do* equal their canonical form, exactly as expected for the two files the
tool serialises itself. This corroborates `raw_bytes_source: http_response_content` from the outside.

---

## 2. Promise conformance — packet section 5

Source: `…/CLAUDE_TAKEOVER_20260913/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md`, section 5 (lines 40-44).

| # | Promise (packet §5) | Candidate `file:line` | Verdict |
|---|---|---|---|
| 1 | "New read-only CLI in the Bridge tree (`IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py`)" | that path exists; `main` `:686-712` | EQUAL |
| 2 | "inputs = account address, product `BTC`, UTC window" | `build_parser:671-683` (`--address`, `--coin` default `BTC`, `--start/--end`), `parse_utc:115-119` refuses non-UTC | EQUAL |
| 3 | "calls the SDK's documented `Info.user_fills_by_time` and `Info.user_funding_history` exactly as the accepted broker does (`bridge/broker/hyperliquid.py:1566-1567, 1887, 1901`)" | `paged_query:320` picks the same two method names, called `(address, cursor, end_ms)` exactly as the broker does at `hyperliquid.py:1964-1966`; I opened all three cited broker lines — `:1564-1567` is the call-budget comment, `:1887`/`:1901` are the `method_name=` arguments. Page caps identical (`:36-37` = `HL_FILLS_PAGE_LIMIT` 2000 / `HL_INFO_PAGE_LIMIT` 500 vs broker `:1578`/`:1584`) | EQUAL |
| 4 | "plus `clearinghouseState`" | `account_state_query:426-458`, body `:434`; SDK `info.py:127` posts exactly `{"type":"clearinghouseState","user":…,"dex":…}` | EQUAL |
| 5 | "stores every native JSON object as immutable bytes with `sha256` sidecars and a manifest" | `write_once:134-149` (`open(path,"xb")`, sidecar `open(…, "x")`), `record_response:279-305`, manifest `:650-666` | EQUAL |
| 6 | "refuses on any non-2xx" | `CapturingInfo.post:97` calls `_handle_exception` (SDK `api.py:30-43`, raises for ≥400) → `call_info:199-208` → `CAPTURE_REFUSED_QUERY_FAILED`. A ≥400 with a non-JSON body still refuses; a 2xx/3xx body that is not a list also refuses (`paged_query:352-353`) | EQUAL |
| 7 | "…truncation (documented page caps: 2000 fills, 500 funding)" | tool **paginates** (`:386-390`) and refuses `CAPTURE_REFUSED_TRUNCATED` only when a full page cannot advance the cursor (`:388-389`) — strictly stronger than refusing at the cap, and identical in shape to the accepted broker (`hyperliquid.py:2025-2034`) | EQUAL (stronger) |
| 8 | "or re-query mismatch" | two full passes `:595-641`, `requery_check:550-564` now compares `{identity: row}` **content**, not just the identity set | EQUAL |
| 9 | "**never** takes a key" | no key argument in `build_parser`; `run_capture:568-569` refuses if `HL_API_WALLET_KEY` is merely *present* in the environment, even set to the empty string (arm `test_OK_main_refuses_an_empty_string_wallet_key_too`) | EQUAL |
| 10 | "never writes to the venue" | see §3 — no exchange import, no signing of anything but the offline EIP-191 recovery, `/info` is the only endpoint literal | EQUAL |
| 11 | §5:43 "Two RED/GREEN fixture suites: refusal on tampered bytes / mismatched re-query / truncated page" | `test_tampered_stored_bytes_vs_sidecar_refuses:322`, `test_requery_identity_mismatch_refuses:265` + `test_requery_content_mismatch_refuses:276`, `test_truncated_full_page_refuses:182` | EQUAL |
| 12 | §5:43 "…acceptance on a recorded fixture" | **no test replays the recorded capture.** Every acceptance arm uses a synthetic double whose `raw_bytes_source` is `…TEST_DOUBLE_ONLY`; the real r1 bytes are never exercised by the suite | DIFFERENT → NIT-4 |
| 13 | §5:42 "Adapter to the existing intake … a file-source input or a compatible snapshot writer is needed" | not present in this branch (3 files, §12) | NOT IN THIS CANDIDATE — deferred scope, see §14 |

---

## 3. Read-only by construction

| Claim | Evidence |
|---|---|
| No `hyperliquid.exchange` import | imports are `argparse, hashlib, importlib.metadata, json, os, re, sys, dataclasses, datetime, pathlib, typing, eth_account, eth_account.messages, hyperliquid.info, hyperliquid.utils.constants` (`:19-34`). My arm walks the AST: no import whose name contains `exchange`; no `Name`/`Attribute` containing `exchange` or `order`; none of `sign_l1_action`/`sign_inner`/`place_order`/`bulk_orders` (arm `test_OK_the_only_endpoint_string_in_the_module_is_info`). The shipped `test_tool_imports_no_write_capable_exchange_client:539` only greps two strings; my AST arm is the stronger form and agrees. |
| Only `/info` is ever posted | the only endpoint-shaped string constants in the module are `"/info"` and `"/"` (the latter is the literal prefix of the JSON-pointer f-string `f"/{index}"`, `:377`). The only SDK methods named anywhere are `user_fills_by_time`, `user_funding_history`, `user_state` (arm `test_OK_only_read_methods_of_the_sdk_are_called`); all three post `/info` in SDK `info.py:262`, `:445-446`, `:127`. |
| `make_info` builds only an `Info` subclass | `:169-170` returns `CapturingInfo`, which subclasses `Info` (`:78`). `CapturingInfo.__init__:81-88` passes `skip_ws=True` and stub `meta`/`spot_meta`, so `Info.__init__` takes the no-network branch. I proved it: with `requests.adapters.HTTPAdapter.send` monkeypatched to raise, constructing `CapturingInfo` succeeds and `ws_manager is None` (arm `test_OK_no_http_is_performed_when_the_client_is_constructed`). |
| Nothing is signed but the offline ownership check | the only `eth_account` use is `Account.recover_message` (`:527`) — recovery, not signing. No private key is read anywhere. |
| Key refusal is the first statement | `run_capture:568-569` is the first statement of the function. (`main`'s `--print-ownership-message` and `--verify-existing` branches run before it, but neither constructs a client, opens a socket, or writes a file.) |
| Nothing is deleted or overwritten | grep of the whole module for `unlink|rmtree|remove(|rmdir|truncate|"w"|'w'|"wb"|shutil|subprocess|eval|exec|os.system|requests.` returns exactly two hits: `:137` `open("xb")` and `:143` `open("x")`. There is no destructive call in the file. |

**No path to a write endpoint exists.** Arm `test_OK_nothing_is_written_outside_out` additionally shows a
completed capture creates exactly one new entry (`--out`) in its parent and touches nothing else.

---

## 4. Bytes are original

`CapturingInfo.post` (`:90-101`) against `API.post` (SDK `api.py:20-28`), line by line:

| API.post | CapturingInfo.post | Same? |
|---|---|---|
| `payload = payload or {}` | `:91` identical | yes |
| `url = self.base_url + url_path` | `:93` `self.base_url + url_path` inline | yes |
| `self.session.post(url, json=payload, timeout=self.timeout)` | `:92-94` same session, same `json=`, same `timeout=` | yes |
| — | `:95-96` `raw = bytes(response.content)`; append `RawCapture(url_path, dict(payload), raw)` | **capture inserted here** |
| `self._handle_exception(response)` | `:97` — after the capture | yes, and the capture precedes it |
| `return response.json()` | `:99` `json.loads(raw.decode("utf-8"))` | parses the *captured* bytes |
| `except ValueError: return {"error": …}` | `:100-101` identical | yes (`UnicodeDecodeError` ⊂ `ValueError`, so a non-UTF-8 body falls into the same branch) |

Verified mechanically by arm `test_OK_capturing_info_post_matches_api_post_apart_from_the_capture`:
`_captures.append` appears before both `_handle_exception` and `json.loads` in the source. So the
bytes are taken **before** any error handling and **before** any parsing — error responses are
captured too (arm `test_OK_error_bytes_are_captured_before_handle_exception_raises`: a 500 body is in
`CaptureRefused.error_capture` with `source == http_response_content`).

Manifest request body == posted payload: `record_response:294` writes `capture.body`, and
`capture.body` is `dict(payload)` taken inside `post` from the object handed to `requests`
(`:96`). Arm `test_OK_posted_payload_is_exactly_what_the_manifest_records` asserts
`capture.body == session.calls[0]["json"] == request_body("fills", …)` and that the literal payload is
`{"type":"userFillsByTime","user":…,"startTime":…,"endTime":…,"aggregateByTime":False}` — which is
exactly what the real manifest records. The `request_body` helper (`:262-276`) is therefore a
*prediction* that matched; the manifest always stores the real thing.

`raw_bytes_source` (`:296`) tells the truth: `RawCapture.source` defaults to `http_response_content`
(`:75`) and only `consume_capture`'s test-double fallback (`:186`) sets
`reserialized_parsed_json_TEST_DOUBLE_ONLY`. On the real path `make_info` always returns a
`CapturingInfo`, which always has `pop_capture`, so the fallback is unreachable (`:183-186`). The r1
manifest says `http_response_content` on all five entries, and the non-canonical key order of the
stored bytes (§1) independently confirms it. *Caveat, not a defect:* a monkeypatched `make_info`
(tests only) can construct a `RawCapture` with the default label, so the label is trustworthy
because `make_info` is the only constructor on the CLI path — not because the label is
unforgeable in-process.

---

## 5. Window and pagination

The intake rule (one complete **half-open** interval; `REAL_OBSERVATION_INTAKE.md:31` as cited twice
in `P012_ACCEPTANCE_AMENDMENT_20260913.md:175` and `:211`) versus the API's **inclusive** `endTime`
(SDK `info.py:436`, "End time in milliseconds, inclusive") is resolved at `paged_query:355-371`.
The file's own docstring (`:7-10`) and `WINDOW_SEMANTICS` (`:52`) state the rule, and the manifest
carries it (`:661`).

### Window walk (my arms, single fill at each offset; `--start 2026-09-12T11:00:00Z`, `--end …12:00:00Z`)

| row time | offset | in raw bytes | in derived view | outcome |
|---|---|---|---|---|
| 1789210799999 | `start-1` | n/a | n/a | `CAPTURE_REFUSED_MALFORMED: fills row before requested start (tid:9)` |
| 1789210800000 | `start` | yes (1 row) | `[9]` | included |
| 1789210800001 | `start+1` | yes | `[9]` | included |
| 1789214399999 | `end-1` | yes | `[9]` | included |
| 1789214400000 | `end` | yes (1 row) | `[]` | **excluded from the view, kept in the bytes** |
| 1789214400001 | `end+1` | n/a | n/a | `CAPTURE_REFUSED_MALFORMED: fills row after requested end (tid:9)` |

Command (cwd `C:/tmp/OPUS_P1CAP_SCRATCH/opus_arms`):
`env -u HL_API_WALLET_KEY C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe -m pytest tests/test_opus_red_arms.py -q -s -p no:cacheprovider --basetemp <user-temp>/btarms2`
(`test_OK_window_walk`, 6 parametrisations). This is the intake's `[start, end)` exactly, with the
inclusive-`endTime` row preserved as bytes — `:369-371`.

### Pagination walk

| scenario | tool behaviour | arm |
|---|---|---|
| full page, last rows share a ms with the next page, cursor **can** advance | cursor windows `(start,end) → (t1,end) → (t2,end)`; identities `[1,2,3,4]`, boundary rows de-duplicated by identity (`:372-385`) | `test_OK_page_boundary_shared_millisecond_completes_when_it_can_advance` |
| full page where **every** row sits on the cursor ms (more rows at one ms than fit a page) | `CAPTURE_REFUSED_TRUNCATED: fills cursor stalled` — refuses rather than dropping the tail (`:388-389`) | `test_OK_page_boundary_shared_millisecond_dedups_without_loss` |
| full page whose max row is the **excluded** `end_ms` row | `page_max` advances to `end_ms` (`:368` runs before the `:369-371` half-open skip), next query is `(end_ms, end_ms)`, returns the excluded row, short page terminates; derived `[1]` | `test_OK_page_max_advances_past_an_excluded_end_row` |
| page 2 returns a row **before** the cursor but inside the window | accepted (the range check is against `start_ms`, not the cursor — `:360`), de-duplicated by identity | `test_OK_rows_before_the_cursor_but_inside_the_window_are_accepted` |
| stop condition | `len(parsed) < limit` counts **raw** rows (`:386`), not de-duplicated ones — correct; a page of pure duplicates still counts as full | (exercised by the two boundary arms) |
| `start == end` | allowed; half-open ⇒ empty derived view, `CAPTURE_OK` | `test_OK_zero_length_window_is_empty_not_refused` |
| `end < start` | `CAPTURE_REFUSED_MALFORMED: end before start` (`:574-575`) | — |
| **full page returned newest-first** | **rows silently lost, no refusal** — see NIT-2 | `test_RED_descending_page_order_silently_drops_rows` |

Millisecond conversion `ms()` (`:122-123`) uses `int(timestamp()*1000)`. I probed 1030 sub-second
values across one second: **0 mismatches** (`test_OK_ms_conversion_is_exact_for_sub_second_boundaries`),
so no float truncation moves a boundary. `parse_utc` refuses naive and non-zero-offset timestamps.

---

## 6. Identities and re-query

`fill_identity` (`:221-240`): `tid:<int>` when `tid` is present, else `hash-oid-time:<h>:<oid>:<t>`.
`funding_identity` (`:248-259`): `hash-time-coin:<h>:<t>:<coin>`, refusing when the coin is missing.

Collision analysis, against what the real venue actually returned:

| identity | collision requires | observed in r1 | tool behaviour on a collision |
|---|---|---|---|
| `tid:<n>` | the venue reusing a trade id | all 5 fills carry a distinct `tid` (5/5 distinct) | identical content → de-duplicated; different content → `CAPTURE_REFUSED_MALFORMED … identity conflict` (`:379-383`) |
| `hash-oid-time` (no-`tid` fallback) | two partial fills of one order in one transaction at the same ms | never used — the venue sent `tid` on every row | different content → refuses (arm `test_OK_no_tid_fills_that_differ_refuse_instead_of_merging`); **byte-identical rows collapse into one** (arm `test_RED_no_tid_fills_with_identical_content_collapse_into_one`) → NIT-5 |
| `hash-time-coin` | two funding rows, same coin, same ms | the real funding hash is `0x0000…0000` on **both** rows, so identity is effectively `time+coin`; the two rows differ by time (17:00:00.041Z, 18:00:00.060Z) | different content → refuses (arm `test_OK_funding_identity_is_time_plus_coin_when_the_hash_is_zero`) |

Re-query: `requery_check:550-564` builds `{identity: row}` for both passes and refuses
`CAPTURE_REFUSED_REQUERY_MISMATCH` when an identity is present in only one pass **or** when the row
content differs. A divergence looks like
`fills row content differs: tid:1` (arm `test_OK_requery_divergence_in_content_names_the_row` asserts the
exact string) or `fills identity only in one pass: tid:2`. In r1 the two passes are **byte-identical**
(`fills_pass1 == fills_pass2`, `funding_pass1 == funding_pass2`; §1 and section D of my verification
script), so the check passed on equality of bytes, not merely of identities.

One by-design gap, stated because a reader could over-read "both passes agree": rows at exactly
`end_ms` never enter `rows_by_id`, so a divergence *in an excluded row* is not refused — it remains
visible in the stored bytes, which then differ between passes
(arm `test_RED_a_row_at_end_ms_may_differ_between_passes_without_refusal`). For r1 this is moot: the
pass files are byte-identical.

---

## 7. Ownership evidence

`ownership_message` (`:107-112`) versus the HTML page (`path1_sign_ownership.html:31-34`):

```
tool : "P012 Path 1 own-account evidence capture\naddress: " + lower(address) + "\nrun_id: " + run_id
page : "P012 Path 1 own-account evidence capture\naddress: " + address.trim().toLowerCase() + "\nrun_id: " + run.trim()
```

I extracted the JS string literals, rebuilt the message for a concrete address/run id and compared it
character by character with the Python output — **EQUAL**
(arm `test_OK_ownership_message_matches_the_html_page_character_for_character`; both sides print
`'P012 Path 1 own-account evidence capture\naddress: 0xabcdef…\nrun_id: p012-path1-20260914T1500Z-1900Z-r1'`).
No trailing newline on either side. The only asymmetry is `trim()`: the page trims the run id, the
tool does not. That fails **closed** — a run id with a stray space refuses with
`CAPTURE_REFUSED_OWNERSHIP_SIGNATURE` and `fill_calls == 0`
(arm `test_OK_signature_over_a_trailing_space_run_id_fails_closed`).

The page uses `personal_sign` (`:47-50`) = EIP-191, and refuses to sign when the connected account is
not the requested address (`:44-46`). The tool verifies with
`Account.recover_message(encode_defunct(text=…))` (`:527-529`) — the matching EIP-191 recovery — and
refuses on any mismatch (`:530-532`).

Order of operations (`run_capture:567-591`): key check → address shape → timestamps → **run-id gate
(`:578-582`) → signature verification (`:587`)** → `out_dir.mkdir()` (`:589`) → `make_info()` (`:591`).
So the signature is verified before any network object exists and before any file is created. Proven
by the shipped arms `test_signature_without_run_id_refuses_before_network_and_writes_nothing:480`
and `test_wrong_ownership_signature_refuses_before_network_and_writes_nothing:504`, both asserting
`fake.fill_calls == 0` **and** `not out.exists()`; both are RED on `e77af1c8` (§9).

`NOT_PROVIDED` is recorded, never invented: with no `--ownership-signature`, `ownership_result:523-524`
returns `{"status": "OWNERSHIP_EVIDENCE: NOT_PROVIDED"}` and no `recovered_address` key is
fabricated.

**Real capture, independently re-verified by me** (section G of `opus_verify_real_capture.py`):
recovering `sig_r1.txt` over `ownership_message("0x1E26…AC49", "p012-path1-20260914T1500Z-1900Z-r1")`
yields `0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49` — equal to the manifest's `address` and to its
recorded `recovered_address`. `OWNERSHIP_EVIDENCE: VERIFIED` is true.

---

## 8. Write discipline and errors

- **Exclusive create for every file and sidecar:** `write_once:134-149` uses `open(path,"xb")` for the
  payload and `open(sidecar,"x")` for the digest, mapping `FileExistsError` to
  `CAPTURE_REFUSED_MALFORMED: output exists: <name>`. I proved this is a *behavioural* fix rather than
  a message change: with an existence check that lies (a lost race), the pre-fix `path.exists()` form
  overwrites while `open("xb")` still refuses and the old bytes survive
  (arm `test_RED_write_once_is_atomic_where_the_pre_fix_check_was_not`, RED on `e77af1c8`).
- **Re-running a capture into a populated directory refuses** and leaves the previous directory
  listing unchanged (arm `test_OK_rerun_into_the_same_directory_refuses`) — a prior capture cannot be
  silently replaced.
- **Nothing outside `--out`:** arm `test_OK_nothing_is_written_outside_out` (a sentinel file beside the
  out dir is untouched; exactly one new entry appears).
- **Nothing is deleted:** no destructive call exists in the module (§3).
- **Error bytes are kept:** `call_info:199-208` attaches the popped capture to
  `CaptureRefused.error_capture` (with `status=<code>` in the detail when the SDK exception carries
  one), and `recorded_call:393-423` writes it as `<name>_ERROR.json` + sidecar + manifest entry
  *before* re-raising with `…; error bytes kept as <name>_ERROR.json`.
- **Bytes before validation** in `paged_query`: `record_response` (`:343`) runs before the
  `isinstance(parsed, list)` check (`:352`), so a malformed page is still stored
  (arm `test_OK_malformed_page_shape_keeps_the_response_bytes`). `account_state_query` inverts that
  order → NIT-3.
- `verify_sidecars:536-547` re-checks each response file against both its sidecar and the manifest;
  the shipped `test_tampered_stored_bytes_vs_sidecar_refuses:322` exercises it. Its coverage is
  incomplete → NIT-1.

---

## 9. D026 evidence — F/L disposition and RED-on-pre-fix

I rebuilt the pre-fix tree myself (`git show e77af1c8:…` + the af921d75 test module + a 6-line
`conftest.py`) and ran it:

```
cwd C:/tmp/OPUS_P1CAP_SCRATCH/opus_prefix
env -u HL_API_WALLET_KEY C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe \
  -m pytest tests/test_capture_own_account_evidence.py -q -p no:cacheprovider --tb=line \
  --basetemp <user-temp>/btred_final
→ 12 failed, 9 passed in 0.85s
```

This reproduces the Lead's `12 failed / 9 passed` exactly. Per-arm judgement — "right reason" means
the pre-fix failure is the defect the finding names, not an incidental assertion:

| F/L | Arm | Pre-fix failure (verbatim) | RED for the right reason? |
|---|---|---|---|
| F-1 | `test_signature_without_run_id_…` | `AttributeError: module … has no attribute 'REFUSED_RUN_ID_REQUIRED'` | **Yes** — the refusal did not exist at all |
| F-1 / F-3 / L-4 | `test_wrong_ownership_signature_…` | `assert 2 == 0` (`fake.fill_calls`) | **Yes** — the strongest arm on the branch: pre-fix the venue was queried twice *before* the signature was checked |
| F-2 | `test_capture_writes_manifest_…` | `AttributeError: … no attribute 'WINDOW_SEMANTICS'` | Yes (window semantics absent from the manifest). Note this arm also carries the F-7 assertion at `:172`, which the earlier failure masks |
| F-2 | `test_half_open_window_excludes_row_at_end_…` | `assert [1, 2] == [1]` | **Yes** — pre-fix the inclusive-`endTime` row entered the derived view |
| F-2 | `test_row_before_requested_start_refuses` | `Failed: DID NOT RAISE CaptureRefused` | **Yes** — out-of-range rows were silently admitted |
| F-2 | `test_row_after_requested_end_refuses` | `Failed: DID NOT RAISE CaptureRefused` | **Yes** |
| F-4 / L-3 | `test_funding_identity_includes_coin` | `CaptureRefused: CAPTURE_REFUSED_MALFORMED: funding identity conflict` raised inside `run_capture` | **Yes** — pre-fix a legitimate two-coin funding capture was *refused* because `hash+time` collided |
| F-5 / L-5 | `test_write_once_refuses_an_existing_output` | `assert 'output exists' in 'refusing to overwrite x.json'` | **Detail-only** (Gemini's NIT, confirmed). The shipped arm cannot tell `exists()`-then-write from `open("xb")`. I built the arm that can (§8) and it *is* RED pre-fix, so the finding is real even though its shipped arm does not prove it |
| F-6 / L-5 | `test_error_response_bytes_are_kept_…` | `assert 'fills_pass1_page001_ERROR.json' in 'RuntimeError'` | **Yes** — the file assertions two lines later would also fail; the error bytes were dropped |
| F-7 / L-6 | `test_capturing_info_post_keeps_pre_parse_bytes_…` | `AttributeError: 'RawCapture' object has no attribute 'source'` | Yes for F-7. Note the preceding assertion (`capture.raw == ok_bytes`) **passed** pre-fix: byte capture already worked, so this arm is RED for the provenance label, not for the capture |
| F-8 | (same arm) | — | **Coverage finding, not a behavioural one.** `CapturingInfo.post` was simply never exercised before; there is no pre-fix behaviour to be RED about |
| F-9 / L-2 | `test_multi_page_success_dedups_…` | **PASSES pre-fix** | Coverage finding. Multi-page walking already worked; the arm fences it. The wrong-signature half of F-9 is the `fill_calls == 0` arm above, which is genuinely RED |
| F-10 / L-1 | — | — | Verified directly, not via RED: ruff 0.16.4 `check --isolated --select E9,F821,F811,F401,F841,RUF100` → `All checks passed!`; `format --isolated --check` → `2 files already formatted`; `py_compile` OK |
| F-11 | `test_requery_content_mismatch_refuses` | `Failed: DID NOT RAISE CaptureRefused` | **Yes** — pre-fix a row whose `px` changed between passes under the same `tid` passed unnoticed. This is the most consequential silent-acceptance defect that P1FIX closed |
| F-11 | `test_requery_identity_mismatch_refuses` | `assert 'only in one pass' in 'fills'` | **Detail-only** (Gemini's second NIT, confirmed) — the pre-fix tool already refused, just with a useless message |

Gemini's delta NIT is therefore accurate and complete: exactly two of the twelve are detail-only, and
I have named them. No arm is RED for a wrong or incidental reason.

**My own arms discriminate too:** running my 43-arm module against the pre-fix tool gives
`13 failed, 30 passed` — including `test_RED_write_once_is_atomic_where_the_pre_fix_check_was_not`,
which is the F-5 proof the shipped suite lacks.

### Mandated test run (candidate)

```
cwd C:/tmp/P1CAP_20260914/IBKR_PAPER_BRIDGE
env -u HL_API_WALLET_KEY C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe \
  -m pytest tests/test_capture_own_account_evidence.py -q -p no:cacheprovider \
  --basetemp <user-temp>/bt
→ 21 passed in 1.02s
```

`HL_API_WALLET_KEY` was absent from my process environment before the run and was additionally
stripped per command with `env -u`; no environment variable value was printed at any point.

### Full Bridge suite (not mandated; run for regression assurance)

```
same cwd/interpreter, -q -p no:cacheprovider --basetemp <user-temp>/btfull
→ 1 failed, 1648 passed, 1 skipped, 1 warning in 187.57s
FAILED tests/test_linux_deployment.py::test_canonical_ledger_artifact_fresh_autocrlf_checkout_matches_recorded_identity
```

Re-run in isolation: **`1 passed in 0.73s`**. The failure is a non-zero exit from a `git add`
subprocess inside a throwaway `git init` directory (`tests/test_linux_deployment.py:450`); it does not
reproduce alone, and it cannot be caused by this candidate, which adds three files that
`test_linux_deployment.py` neither imports nor reads (§12 proves nothing else in the tree changed).
I did not diagnose it further because doing so requires a `git add`, which my brief forbids.
Recorded here as an environment observation, not as a finding against the candidate.

---

## 10. My own RED arms

Module: `C:/tmp/OPUS_P1CAP_SCRATCH/opus_arms/tests/test_opus_red_arms.py` (43 arms) against a scratch
copy of the candidate tool (`sha256 00b3b8f6…`, identical to the worktree file).

```
cwd C:/tmp/OPUS_P1CAP_SCRATCH/opus_arms
env -u HL_API_WALLET_KEY C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe \
  -m pytest tests/test_opus_red_arms.py -q -p no:cacheprovider --basetemp <user-temp>/btarms3
→ 43 passed in 1.26s
```

`test_OK_*` arms confirm intended behaviour; `test_RED_*` arms assert the *current* behaviour and are
the evidence for the findings below. Selected captured output:

```
WALK before start t=1789210799999 -> REFUSED CAPTURE_REFUSED_MALFORMED: fills row before requested start (tid:9)
WALK at start     t=1789210800000 -> derived=[9] raw_rows=1
WALK at end       t=1789214400000 -> derived=[]  raw_rows=1
WALK after end    t=1789214400001 -> REFUSED CAPTURE_REFUSED_MALFORMED: fills row after requested end (tid:9)
cursor windows: [(…800000, …400000), (…801000, …400000)] -> CAPTURE_REFUSED_TRUNCATED fills cursor stalled
derived tids: [3, 4] cursor windows: [(1789210800000, …), (1789210800004, …)]   # descending page, rows at t1/t2 never requested
sub-ms probes: 1030 mismatches: 0
CAPTURE_VERIFY_OK
exit: 0 | sidecar says: fa2ea563cc943937 | actual: fea1332c58b5cdf1                # tampered derived view passes verification
files after refusal: ['fills_pass1_page001.json', 'fills_pass1_page001.json.sha256', 'funding_pass1_page001.json', 'funding_pass1_page001.json.sha256']   # account_state bytes absent
raised: binascii.Error                                                              # malformed signature escapes as a raw exception
raw rows: 2 derived rows: 1                                                         # identical no-tid fills collapse
manifest coin: BTC derived coins: ['BTC', 'ETH']
endpoint-shaped literals: ['/', '/info']
SDK methods referenced: ['user_fills_by_time', 'user_funding_history', 'user_state']
```

Arm `test_OK_real_capture_manifest_is_reproducible_from_the_stored_bytes` replays the **real r1
bytes** through the candidate's `fill_derived`/`funding_derived` and reproduces
`DERIVED_EXTRACTION.json` **byte-for-byte** (`feb43cd2…`), with `tool_sha256()` equal to the
manifest's. Independently, my verification script computes from the raw pages
`fees=0.035831  closedPnl=0.320856  funding=-0.001143  net=+0.283882 USDC`, matching the +0.2839 USDC
the brief states. The manifest window `start_ms 1789398000000 / end_ms 1789412400000` converts to
`2026-09-14T15:00:00Z` / `2026-09-14T19:00:00Z`, matching the declared window, and every captured row
falls strictly inside it. The five fills / two settlements match the owner's declaration (four buys
totalling 0.00058 BTC at 16:03:30.942Z, 16:05:15.271Z, 16:06:11.269Z, 16:14:34.869Z; one close of
0.00058 at 18:08:43.372Z; funding at 17:00:00.041Z and 18:00:00.060Z — 41 ms and 60 ms past the
hour, consistent with the known Hyperliquid stamping offset).

---

## 11. Lead authorship of `af921d75`

The correction was written by the Lead under owner ruling `OD-20260915-P012-P1FIX-LEAD-1` ("A") and is
disclosed as such in `DISPOSITION_P1FIX.md:1-4`. I read the full pre-fix→post-fix delta of the tool
(413 diff lines, `C:/tmp/OPUS_P1CAP_SCRATCH/opus_tool_delta.diff`) hunk by hunk and mapped every hunk
to a finding:

- Every behavioural hunk traces to F-1/F-2/F-3/F-4/F-5/F-6/F-7/F-11 (docstring `:7-14`,
  `REFUSED_RUN_ID_REQUIRED` `:47`, `WINDOW_SEMANTICS` `:52`, `RAW_SOURCE_*` `:54-55`,
  `CaptureRefused.error_capture` `:61-67`, `RawCapture.source` `:75`, `write_once` `:134-149`,
  `consume_capture` fallback label `:186`, `call_info` error capture `:199-208`, `funding_coin` /
  `funding_identity` `:243-259`, `raw_bytes_source` in the manifest `:296`, range refusals and the
  half-open `continue` `:360-371`, `recorded_call` `:393-423`, `requery_check` `:550-564`, the run-id
  gate and the hoisted `ownership_result` `:576-587`, the manifest window block `:656-662`).
- The remaining hunks are `ruff format` reflow (F-10): line wrapping in `info_base_url`,
  `consume_capture`, `request_body`, `ownership_result`, `verify_sidecars`, `account_state_query`.
- Two changes are *adjacent* to, rather than named by, the eleven findings, and I judge both benign:
  (a) the removal of `# noqa: BLE001` at the old `except Exception` — required by `RUF100` once that
  rule is selected, so it belongs to F-10; (b) `getattr(args, "ownership_signature", None)` /
  `getattr(args, "run_id", None)` at `:576-577` instead of direct attribute access — a test
  affordance that makes a `Namespace` lacking those attributes behave as "no signature" rather than
  raising. On the CLI path argparse always sets both, so it changes nothing observable; I note it
  only so the roster does not have to rediscover it.

**Nothing in `af921d75` is beyond the eleven findings plus L-1..L-6 and the formatter.** I found no
smuggled behaviour, no scope creep, and no weakening of an existing guarantee.

Does my verdict need anything beyond Sol and me? My view: no additional reviewer is required for the
*code*. What my review cannot supply — and no offline reviewer can — is observation of the venue's
real multi-page behaviour (§14). If the roster wants that closed, it needs a live paged capture, not
another code review. The Lead correctly does not accept its own code; this report accepts nothing on
its own either.

---

## 12. Scope

Proven by recursive **tree-OID descent** from the root trees of `fcac0ac6` and `af921d75`, using only
`git rev-parse <rev>:<path>` and `git show <rev>:<path>` (script
`C:/tmp/OPUS_P1CAP_SCRATCH/opus_scope_tree_walk.py`). Equal subtree OIDs prove whole subtrees are
byte-identical, so the walk descends only where they differ:

```
root tree fcac0ac6 = a95a77b47dde2b6de95eed97b2880faedb8f49e3
root tree af921d75 = 0ecbc7d7a91f4450dfc6282dc4d702a04e80a03c

IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py   -  61e55ce7  ADDED
IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py        -  71d04ee7  ADDED
IBKR_PAPER_BRIDGE/tools/path1_sign_ownership.html              -  6e786231  ADDED

total changed paths: 3
```

Exactly three files, all **added**; nothing in the repository is modified or deleted; no protected
scope is touched. (I did not run `git diff --stat` as the brief's example suggests, because the same
brief forbids `git diff`; the tree-OID descent is a stronger proof and stays inside the two permitted
commands.)

---

## 13. Findings

No REQUIRED finding. Seven NITs, each with a concrete arm.

**NIT-1 — `verify_sidecars` does not cover every file it wrote; `CAPTURE_VERIFY_OK` over-promises.**
`tools/capture_own_account_evidence.py:536-547` iterates only `manifest["responses"]`, so
`DERIVED_EXTRACTION.json` and `CAPTURE_MANIFEST.json` — both of which *do* have `.sha256` sidecars
written by `write_once` — are never checked. After tampering with a fee in the derived view,
`cae.main(["--verify-existing", out])` returns 0 and prints `CAPTURE_VERIFY_OK` while the sidecar says
`fa2ea563…` and the file hashes to `fea1332c…`
(arm `test_RED_verify_existing_ignores_the_derived_view_and_the_manifest`). Bounded impact: the
evidentiary payload is the original bytes, which *are* fully covered, and the derived view is exactly
reproducible from them (I reproduced r1's byte-for-byte, §10). Recommendation: have `verify_sidecars`
walk every `*.sha256` in the directory, or record the derived-extraction digest in the manifest.

**NIT-2 — a newest-first page would be silently truncated.** `paged_query:368-390` advances the cursor
to the page maximum and stops when a page is short. Fed a full page in descending time order, the tool
jumps the cursor to the newest row, never requests the older rows, and returns `CAPTURE_OK` with a
short derived view and no refusal (arm `test_RED_descending_page_order_silently_drops_rows`: cursor
windows `(start,end) → (t4,end)`, derived `[3,4]`, rows at `t1`/`t2` never fetched). This is the same
design as the already-accepted broker (`bridge/broker/hyperliquid.py:2025-2034`), the SDK documents
`startTime`-based ascending paging, and the real r1 page **is** ascending (five fills in increasing
time), so nothing about r1 is affected — r1 returned 5 rows against a 2000 page cap and never
paginated at all. Recommendation (one line): refuse when a page's row times are not
non-decreasing, or require `min(page_times) >= cursor` before accepting the page.

**NIT-3 — a malformed `account_state` response discards its own bytes.**
`account_state_query:448-449` validates `isinstance(parsed, dict)` *before* calling `record_response`
at `:450`, the opposite order from `paged_query` (`:343` writes, `:352` validates). A non-object
`clearinghouseState` therefore refuses with no `account_state.json` on disk
(arm `test_RED_account_state_malformed_response_discards_the_response_bytes`; the two fills/funding
pages from the same run *are* on disk). For a tool whose premise is "a failed query is never
evidence-free" this asymmetry should be removed: move `record_response` above the shape check.

**NIT-4 — packet §5:43's "acceptance on a recorded fixture" is not in the suite.** All 21 arms use
synthetic doubles; the recorded r1 bytes are never replayed, so a future regression in
`fill_derived`/`funding_derived`/identity would not be caught by the repository's own tests. I wrote
the missing arm (`test_OK_real_capture_manifest_is_reproducible_from_the_stored_bytes`, §10) and it
passes today; recommendation: check a copy of the r1 page bytes in as a fixture and keep that arm.

**NIT-5 — the no-`tid` identity path can merge two genuinely distinct fills.** `fill_identity:229-240`
falls back to `hash+oid+time`; two byte-identical partial fills of one order in one transaction at the
same millisecond collapse to one derived row while both remain in the stored bytes
(arm `test_RED_no_tid_fills_with_identical_content_collapse_into_one`: `raw rows: 2 derived rows: 1`).
Differing rows refuse instead of merging, so the failure mode is undercount, never a fabricated row.
Not reached in r1 — the venue returned `tid` on all five fills. Recommendation: when `tid` is absent,
include the row's position within the page in the identity, or refuse the no-`tid` shape outright.

**NIT-6 — malformed ownership/verify inputs escape as raw exceptions instead of refusal codes.**
`read_signature:513` (`json.loads` on a file that starts with `{`), `ownership_result:527`
(`Account.recover_message` on a non-signature) and `verify_sidecars:537-539` (a missing or unreadable
manifest) are not wrapped, and `main:708` only catches `CaptureRefused`. A junk signature file raises
`binascii.Error`, a truncated JSON signature raises `json.JSONDecodeError`, and
`--verify-existing <missing-dir>` raises `FileNotFoundError` — each a traceback and exit code 1
instead of a named refusal and exit 2 (arms `test_RED_malformed_signature_escapes_as_an_uncaught_exception`,
`test_RED_malformed_signature_json_escapes_too`, `test_RED_verify_existing_on_a_bad_directory_escapes_too`).
It fails closed — nothing is written, no network object is built — so this is ergonomics and log
hygiene, not safety.

**NIT-7 — the ownership attestation binds the address and the run id only, and the signature itself is
not stored in the record.** `ownership_message:107-112` covers `address` and `run_id`, not the window,
the network or the captured bytes; and `ownership_result:533` returns only
`{status, recovered_address}`, so `CAPTURE_MANIFEST.json` asserts `VERIFIED` without carrying the
artefact that would let a third party re-verify it from the output directory alone. The r1 package is
nevertheless complete, because the Lead recorded `sig_r1.txt` and its sha256 in `run.log` outside the
tool and I re-verified the recovery independently (§7). Recommendation: include `start`/`end`/`network`
in the signed message and copy the signature (and the exact signed text) into the manifest, so the out
directory stands alone as an admission record.

**Two observations that are not findings against the candidate:**

- `OWNERSHIP_MESSAGE_r1.txt` in the real-capture record holds **CRLF** line endings and a trailing
  newline, so it is not the signed byte string. Recovering with those bytes yields
  `0x1e10A1f77A9d53e9d546b88C908f7F1392230324` — a different address
  (section H of `opus_verify_real_capture.py`). A reviewer who verifies the signature using that file
  will wrongly conclude the ownership evidence fails. The record, not the tool, should carry the
  LF-exact message (the tool's `--print-ownership-message` emits it correctly).
- `--coin` is a declaration, not a filter: the manifest records `coin: BTC` while any non-BTC row in
  the window enters the derived view (arm `test_RED_coin_is_recorded_but_never_enforced`). Every
  derived row carries its own `coin`, so nothing is misattributed at row level, and r1 contains BTC
  only. Worth a sentence in whatever intake document consumes `native_instrument`.

---

## 14. NOT VERIFIED

- **I made no network call of any kind.** Nothing in this report observes the live venue; the real
  capture was read as an existing record and never re-run.
- **The real API's pagination beyond one page is unobserved.** r1 returned 5 fills and 2 funding rows
  against caps of 2000 and 500, so no second page was ever requested. Page-size behaviour at the cap,
  ordering across pages, and the inclusive-boundary replay are asserted from the SDK docstrings, the
  accepted broker and my synthetic arms — not from a live paged response. NIT-2 lives entirely in this
  unobserved region.
- **Completeness of the venue's answer is unprovable from inside.** Two byte-identical passes prove the
  endpoint is stable and that nothing was altered between them; they cannot prove the endpoint listed
  every fill that existed. No independent venue source (web UI export, second endpoint) was
  cross-checked.
- **The ownership signature proves control of the private key at signing time**, not that the human
  holding it is the owner; that rests on the owner's self-attestation (`OD-20260914-P012-ADMISSION-Q1`).
- **`REAL_OBSERVATION_INTAKE.md` itself was not readable** — the `sources/` packet directory that held
  it no longer exists, so its sha256 `40c969dd…` (`PACKET_SHA256SUMS.txt`) could not be re-checked.
  I verified the half-open rule at `:31` through two independent citations of it in
  `P012_ACCEPTANCE_AMENDMENT_20260913.md:175` and `:211`, not from the file's own bytes.
- **The intake adapter promised at packet §5:42** (file-source input or a compatible snapshot writer
  for `tools/export_mtc_funding.py --mode PRODUCTION`) is **not in this candidate**. The captured
  evidence therefore cannot yet enter the MTC intake; that is deferred scope, not a defect of the
  tool, but admission depends on it.
- **One full-suite failure** (`test_linux_deployment.py::test_canonical_ledger_artifact_fresh_autocrlf_checkout_matches_recorded_identity`)
  was not root-caused: it passes in isolation, it cannot be reached by the three added files, and
  diagnosing it needs a `git add`, which my brief forbids.
- **Ruff was run from `C:/tmp/wp_p0_04_tooling_20260825/Scripts/ruff.exe` (0.16.4) with `--isolated`**,
  because the Bridge interpreter has no `ruff` module; the repository's own ruff configuration, if
  any, was therefore not applied.
- This report accepts nothing. Exact Sol has not reviewed the tool; the Lead assembles the roster.

---

VERDICT: PASS-WITH-NITS
