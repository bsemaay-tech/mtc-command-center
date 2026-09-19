# T0 independent review — P1CAP repair round 1 `9f1aa532`

Independent `gpt-5.6-sol` xhigh review. I did not read an Opus report or an adjudication of an
Opus report. I made no network call, did not rerun a capture, did not delegate, and did not mutate
the audited worktree. This report alone accepts nothing; the Lead assembles the roster.

## Verified identities

### Candidate and scope

`git -c safe.directory=* -C C:/tmp/P1CAP_20260914 rev-parse HEAD` returned:

```text
9f1aa532d49a9856caf766d2480f3b7744ce86dd
```

Computed SHA-256 over the committed bytes (the checkout bytes matched):

| File | SHA-256 |
|---|---|
| `IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py` | `ed9c1e03d44b4fb8311d892aaed12bebdfe368abe383eaeb5cd63f494958a3ba` |
| `IBKR_PAPER_BRIDGE/tools/path1_sign_ownership.html` | `b43dbe39aaa9536fbc8f3e05d29ddc851ad3d2e3e271e1bee38b53fddc54e01f` |
| `IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py` | `20efa6fe55917bfea58ca04b57fcaae259e27d5e7ea4cb7c6731d057a08b1ecc` |

Commit-to-commit scope, using only the permitted `git diff <sha> <sha> -- <paths>` form:

| Range | Scope observed |
|---|---|
| `fcac0ac6..af921d75` | Exactly the original three files: tool, HTML signer, tests. |
| `af921d75..1029d6e9` | Tool + tests modified; 15-file `p012_path1_r2_capture` fixture directory added. |
| `1029d6e9..9f1aa532` | Exactly tool + tests modified; `103 insertions, 20 deletions`, mostly `ruff format`, two fixes, and two tests. |
| `fcac0ac6..9f1aa532` | 18 added paths: the original three plus the 15-file fixture directory; no protected path. |

The repair hunk is exact at tool `:370-373` (`t < cursor`) and `:478-482`
(`"assetPositions" not in parsed`). The corresponding tests are at tests `:392-420`.

### Real captures and fixture

I computed each hash from the file bytes, compared it to the adjacent sidecar, and, for response
files, to `manifest.responses[].response_sha256`. Every comparison below was true.

| Capture | File | Computed SHA-256 | Sidecar | Manifest entry |
|---|---|---|---|---|
| r1 | `CAPTURE_MANIFEST.json` | `c837cf1237e9c2d8dfdad250815ee17fbd28e1cd0f98b901ec508f9ed6c2c9cb` | match | n/a |
| r1 | `DERIVED_EXTRACTION.json` | `feb43cd26729b26c8b0419b6eb8d47135d345d1faff93163ee8597b3178047c7` | match | n/a (old manifest) |
| r1 | `account_state.json` | `ea77db9ab583be926f1dcfae35ef02e629fcb0102efbf0cc4965aae539d6e4fe` | match | match |
| r1 | `fills_pass1_page001.json` | `6cb8586c5b446f6807296fa81c8c2bc5f0d7d249a34b0d0c0980732d6fb18589` | match | match |
| r1 | `fills_pass2_page001.json` | `6cb8586c5b446f6807296fa81c8c2bc5f0d7d249a34b0d0c0980732d6fb18589` | match | match |
| r1 | `funding_pass1_page001.json` | `6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f` | match | match |
| r1 | `funding_pass2_page001.json` | `6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f` | match | match |
| r2 | `CAPTURE_MANIFEST.json` | `a31b80a1a24f36b43a549ada878e487066ff629fc82c9d6aa0755e82fa93eb82` | match | n/a |
| r2 | `DERIVED_EXTRACTION.json` | `819d41364385c403051141648d9bc272490478ca66f7aba3cfdfc809a55c09c5` | match | n/a (old manifest) |
| r2 | `account_state.json` | `032ac4d02db797dac2a56d50c5110b568e60fd6283e04b47f1e3b9546b2d3577` | match | match |
| r2 | `fills_pass1_page001.json` | `29e57b4df67b6ee7ae496f566cc9b2337ecd6530ca32694a91005f1ff292ecec` | match | match |
| r2 | `fills_pass2_page001.json` | `29e57b4df67b6ee7ae496f566cc9b2337ecd6530ca32694a91005f1ff292ecec` | match | match |
| r2 | `funding_pass1_page001.json` | `a68ce94be835153897bfab1b47fd95608c928d3437af7578a939fd91542ca434` | match | match |
| r2 | `funding_pass2_page001.json` | `a68ce94be835153897bfab1b47fd95608c928d3437af7578a939fd91542ca434` | match | match |

The current CLI returned `CAPTURE_VERIFY_OK` separately for real r1, real r2, and the checked-in
r2 fixture. The 14 fixture artifacts other than `README.md` are byte-identical to real r2; with
the README the fixture contains the stated 15 files. Both real captures have five response
entries, `raw_bytes_source: http_response_content`, mainnet URL, SDK `0.24.0`, and list-valued
`assetPositions`. Fills pass 1/pass 2 and funding pass 1/pass 2 are byte-identical in each capture.

r1 has five BTC fills and two BTC funding events. Its derived values reconcile to approximately
`+0.2839 USDC` after close PnL, fees, and funding. r2 has two BTC fills and three BTC funding
events. I did not reinterpret either capture as fresh venue truth.

## Promise conformance

| Packet promise | Implementation | Result |
|---|---|---|
| Section 5 line 41: read-only CLI accepts address, product BTC, UTC window | Parser at tool `:773-785`; window/address used at `:665-739`; `coin` only copied to manifest at `:757` | **DIFFERENT** — address/window are bound, but `--coin` is not bound to returned native rows (NIT-2). |
| Calls `Info.user_fills_by_time`, `Info.user_funding_history`, and clearinghouse state as the broker does | Tool `:316-337`, `:436-456`, `:693-739`; SDK `info.py:86-128,230-270,430-446` | **EQUAL** |
| Store original native response bytes with SHA-256 sidecars and a manifest | Tool `:91-102`, `:135-150`, `:275-301`, `:747-769` | **EQUAL** on capture; `--verify-existing` has the missing-manifest-sidecar NIT-1. |
| Refuse non-2xx while preserving bytes | Tool captures before `_handle_exception` at `:91-102`; `recorded_call` stores `<name>_ERROR.json` at `:403-433`; SDK reference `api.py:20-43` | **EQUAL** |
| Refuse truncation at caps 2000/500 | Tool `:37-38`, `:396-400` | **EQUAL** |
| Re-query twice and refuse identity or row-content divergence | Tool `:648-662`, calls `:693-741` | **EQUAL** — parsed-content divergence refuses; harmless JSON serialization-only differences are retained, not rejected. |
| Never take a key and never write to the venue | Key refusal is the first statement of `run_capture` at `:665-667`; imports `Info`, not `Exchange`; `make_info` returns `CapturingInfo` at `:170-171` | **EQUAL** |
| Section 5 line 42: adapter into the existing production intake | No adapter or snapshot writer is in this branch | **DIFFERENT** — remains separate downstream admission work, not silently supplied by this tool. |
| Section 4 line 36: the packet's proposed one-line message includes address, run id, and UTC date | Tool `:108-113`; HTML `:31-34` | **DIFFERENT** — tool and HTML are character-for-character equal, but bind address + run id only; owner item F below. |
| Section 4 line 37: endpoint/request/response provenance and two queries | Tool `:275-301`, `:693-741`; real manifests | **EQUAL** |
| Section 4 line 38: screenshots bind screen order ids to API order ids | Not produced by these three files | **DIFFERENT** — external session evidence, not invented by the tool. |

### HTTP-byte comparison with SDK `API.post`

Both construct `payload = payload or {}`, post to `base_url + url_path` through the same session
with `json=payload` and `timeout=self.timeout`, then call `_handle_exception`. The subclass adds
`raw = bytes(response.content)` and appends `RawCapture(url_path, dict(payload), raw)` before
exception handling and before decoding (tool `:91-102`; SDK `api.py:20-28`). Thus the manifest
body is the payload actually posted, and the raw bytes precede both error handling and JSON
parsing. The focused test drives `CapturingInfo.post` itself at tests `:607-634`.

## F/L disposition and RED-on-pre-fix judgement

The historical prefix used the exact `e77af1c8` tool (`a1ef5ee1c1241577e0c3c4edf52a07acb71f67dc36af050d9629fcd8c2ad475d`)
with the exact `af921d75` tests (`5d141fb1ad260dfee377660ddabef3e559c4c0d07506626f06c79287b6d4021f`).
It produced exactly `12 failed, 9 passed`.

| Item | Current disposition | Code/test | RED on `e77af1c8` for the right reason? |
|---|---|---|---|
| F-1 | CLOSED: signature requires explicit run id; verification precedes mkdir/network | Tool `:674-689`; tests `:698-754` | YES. Missing constant/gate and wrong signature made two fill calls. |
| F-2 | CLOSED: half-open `[start,end)` plus range refusals and manifest semantics | Tool `:350-400`, `:758-764`; tests `:226-262` | YES. End row was included; before/after rows did not refuse; semantics field was absent. |
| F-3 | CLOSED: ownership recovery runs before network object/file | Tool `:674-689`; tests `:698-754` | YES. Wrong signature reached both fill passes pre-fix. |
| F-4 | CLOSED: funding identity includes coin and refuses absent coin | Tool `:239-255`; tests `:289-319` | YES. BTC/ETH same hash/time collided pre-fix. |
| F-5 | CLOSED in code: exclusive `xb` for data and `x` for sidecar | Tool `:135-150`; test `:552-562` | **NO (detail-only).** Pre-fix already refused the existing file; the test failed only because its detail said `refusing to overwrite`, so it does not prove the TOCTOU change. Code inspection proves `xb`. |
| F-6 | CLOSED: error response bytes retained as `<name>_ERROR.json` | Tool `:190-210`, `:403-433`; test `:575-604` | YES. Pre-fix dropped the capture and named no error file. |
| F-7 | CLOSED: `raw_bytes_source` is explicit | Tool `:55-56`, `:71-76`, `:174-187`, `:292`; tests `:146-179,607-634` | YES for provenance. Pre-fix capture lacked `source`. |
| F-8 | CLOSED: direct `CapturingInfo.post` test exists | Tests `:607-634` | Coverage-only, not a clean product RED: pre-fix stopped on the new F-7 `source` assertion before its non-2xx arm; core pre-parse capture already existed. |
| F-9 | CLOSED: multi-page success and wrong-signature arms | Tests `:193-223,722-754` | MIXED. Multi-page already passed pre-fix; wrong-signature ordering was correctly RED. |
| F-10 | CLOSED: specified Ruff selection and format clean | Both Python files | YES via tooling: pre-fix tool had `RUF100`, `F841`, and was unformatted. |
| F-11 | CLOSED: compare `{identity: row}` content | Tool `:648-662`; tests `:265-286` | YES for content (`DID NOT RAISE`). The identity-mismatch arm itself was **detail-only** (`fills` vs `only in one pass`). |
| L-1 | CLOSED with F-10 | Both Python files | Tooling RED as above. |
| L-2 | CLOSED with F-9 | Tests `:193-223,722-754` | Wrong signature right-reason; multi-page coverage-only. |
| L-3 | CLOSED with F-4 | Tool `:239-255`; tests `:289-319` | YES. |
| L-4 | CLOSED with F-1/F-3 | Tool `:674-689`; tests `:698-754` | YES. |
| L-5 | CLOSED with F-5/F-6 | Tool `:135-150,190-210,403-433` | F-6 YES; F-5 detail-only as stated. |
| L-6 | CLOSED with F-7 | Tool `:55-56,71-76,174-187,292` | YES for the provenance field. |

No material `af921d75` behavior lies beyond the eleven F items and six L items; extra changes are
supporting comments, fixtures, and tests. Lead authorship does not accept the code. The later
PACKAGE-authored NIT slice and repair are disclosed and independently fenced below. No additional
specialist is indicated beyond the required two exact flagships, Gemini corroboration, and Lead
reproduction; all roster members and owner gates remain separate.

### NIT slice and repair disposition

| Item | Disposition at `9f1aa532` | Independent mutation result |
|---|---|---|
| NIT-1 sidecar/derived coverage | CLOSED for present sidecars and manifest-derived digest; residual NIT-1 below | Responses-only mutant: `DID NOT RAISE`. |
| NIT-2 ascending page order | CLOSED at tool `:351-362` | Check-removed mutant: `DID NOT RAISE`. |
| NIT-3 retain malformed account-state bytes | CLOSED at tool `:446-472` | Record-after-shape mutant: `account_state.json` absent. |
| NIT-4 real-r2 replay | CLOSED at tests `:504-537` | `af921d75` product code still passes, as expected; a one-line `fill_derived` fee mutant fails at the exact derived-view equality. The PACKAGE verification record now correctly says a mutant was possible. |
| NIT-5 refuse tid-less fill | CLOSED at tool `:222-236` | Fallback mutant: `DID NOT RAISE`. |
| NIT-6 named signature/verification errors | CLOSED at tool `:534-571,598-615` | Reverted `read_signature`: JSON decode and missing file escape raw (`2 failed, 2 passed`), matching the PACKAGE record. |
| NIT-7 store message/signature/binds | CLOSED at tool `:556-585` | Field-removal mutant: `KeyError: 'message'`. |
| R-1 later-page row floor | CLOSED at tool `:363-373`; test `:392-405` | Revert to `start_ms`: `DID NOT RAISE CaptureRefused`. |
| R-2 2xx non-JSON account-state sentinel | CLOSED at tool `:468-482`; test `:408-420` | Remove key check: `DID NOT RAISE CaptureRefused`. |
| NIT-A / formatting | CLOSED | Current Ruff: `All checks passed!`; `2 files already formatted`. |

Why the earlier re-read could miss R-1/R-2 is visible from the old cases: R-1 sits outside a
page-one boundary table. A test for a row before the original `start_ms`, plus a valid inclusive
restart at exactly `cursor`, does not exercise a later *short* page containing a timestamp in
`[start_ms,cursor)`. R-2 sits outside the former non-dict malformed-state case: the SDK's actual
2xx parse-failure fallback is a dict, so `isinstance(parsed, dict)` looked sufficient until that
specific sentinel was driven.

## Independent RED arms and commands

All writes were under `C:/tmp/SOL_P1CAP_SCRATCH/sol_t0_9f1aa532_01`; every command removed
`HL_API_WALLET_KEY` without printing any environment value.

| Purpose | CWD and command | Exact observed result |
|---|---|---|
| Current focused GREEN | CWD `C:/tmp/P1CAP_20260914/IBKR_PAPER_BRIDGE`; `python -m pytest tests/test_capture_own_account_evidence.py -q -p no:cacheprovider --basetemp .../basetemp_current_2` | `34 passed in 1.25s` |
| Original D026 prefix | CWD `.../prefix_e77_af_tests`; same pytest module command | `12 failed, 9 passed in 1.25s` |
| R-1 mutant | CWD `.../mut_r1`; pytest `::test_second_page_row_before_current_cursor_refuses` | `Failed: DID NOT RAISE CaptureRefused`; `1 failed in 0.74s` |
| R-2 mutant | CWD `.../mut_r2`; pytest `::test_account_state_parse_failure_sentinel_refuses` | `Failed: DID NOT RAISE CaptureRefused`; `1 failed in 0.75s` |
| Independent window/residual arms | CWD `.../arms`; `python -m pytest tests/test_sol_arms.py -q ...` | `9 passed in 0.92s` |
| Residual probes by name | CWD `.../arms`; pytest `-k 'missing_manifest_sidecar or account_state_member_type or coin_argument' -vv ...` | All three named observations `PASSED`; `3 passed, 6 deselected in 0.47s` |
| NIT-4 af revert | CWD `.../af_nit4`; pytest `::test_real_r2_capture_bytes_replay` | `1 passed in 0.42s` |
| NIT-4 derivation mutant | CWD `.../mut_nit4`; same test | Equality diff shows `fee: MUTATED_FEE` vs `0.019839`; `1 failed in 0.59s` |
| NIT-1/2/3/5/7 mutants | Each `.../mut_nitN`; corresponding single test | Each failed at the claimed fence: no refusal; no refusal; missing account-state file; no refusal; missing `message`. |
| NIT-6 exact mutant | CWD `.../mut_nit6`; two signature test groups | Raw `JSONDecodeError` and `FileNotFoundError`; `2 failed, 2 passed, 30 deselected in 0.61s` |
| Ruff | CWD Bridge; specified `ruff check --select E9,F821,F811,F401,F841,RUF100 ...` then `ruff format --check ...` | `All checks passed!`; `2 files already formatted` |
| Compile | CWD committed scratch copy; `python -m py_compile capture_own_account_evidence.py test_capture_own_account_evidence.py` | `PY_COMPILE_OK` |
| Existing captures | CWD Bridge; CLI `--verify-existing` for r1, r2, fixture | `CAPTURE_VERIFY_OK` three times |

I also executed full pytest discovery from the Bridge. Exact result:

```text
33 failed, 1629 passed, 1 skipped, 1 warning in 179.38s (0:02:59)
```

All 33 failures were `tests/test_mtc_funding_export.py` and emitted the same guard:

```text
export_mtc_funding: CANDIDATE_STAGING_UNSAFE: the staging directory must not be inside another Git checkout or worktree
```

The mandated scratch root contains a pre-existing `.git` directory. The report directory also has
a `.git` marker, and the launch instruction forbids writing to an unrelated user-temp root. I did
not delete a foreign marker or bypass the exporter's safety check. The focused 34-test module and
all 1,629 non-refusing tests ran successfully; the PACKAGE record's clean-root full result remains
quoted evidence, not my executed result.

## Window walk

| Case | Expected/observed at `9f1aa532` | Evidence |
|---|---|---|
| Row at `start_ms - 1` | `CAPTURE_REFUSED_MALFORMED`, before requested cursor | Current test `:243-251`; independent arm |
| Row exactly at `start_ms` | Included | Independent boundary arm |
| Row at `end_ms - 1` | Included | Independent boundary arm |
| Row exactly at `end_ms` | Original bytes retained; excluded from identity set/derived view | Tool `:378-381`; current test `:226-240`; independent arm |
| Row at `end_ms + 1` | `CAPTURE_REFUSED_MALFORMED`, after requested end | Current test `:254-262`; independent arm |
| Later page row exactly at its new `cursor` | Accepted; inclusive restart is legitimate | Independent two-page and three-page arms |
| Later short page row in `[start_ms,cursor)` | Refused by R-1 repair | Tool `:363-373`; test `:392-405`; R-1 mutant goes GREEN incorrectly |
| Three-page pass, last rows sharing a millisecond with next page | Accepts equal-time boundary rows, deduplicates identities, advances when a later timestamp appears | Independent 3-row-limit arm: derived tids `[1,2,3,4]`, requested floors `start,t1,t2` |
| Full page with no timestamp progress | `CAPTURE_REFUSED_TRUNCATED` | Tool `:396-400`; independent stalled-cursor arm |
| Full page reaches excluded `end_ms`, next short page repeats `end_ms` | `page_max` advances to end; second request floor is end; row remains excluded | Independent end-cursor arm |

The stop condition uses raw `len(parsed)`, not deduplicated count. Identity dedup retains exact
replays and refuses conflicting content. `fill_identity` is now `tid` only; `funding_identity` is
`hash + time + coin`. Re-query compares complete `{identity: row}` maps. A missing identity or any
parsed row-content difference refuses; the real r1/r2 passes are byte-identical.

## Ownership, write discipline, and read-only construction

- Tool `ownership_message` and HTML `buildMessage()` produce the same three lines character for
  character for a valid CLI address/run id. Independent EIP-191 recovery using the retained r1 and
  r2 signature files returned `OWNERSHIP_EVIDENCE: VERIFIED` and each recovered address matched
  the manifest address. No signature value was printed in my transcript.
- With a signature, run id is mandatory and ownership verifies before `Path.mkdir`, `make_info`,
  or any query (tool `:674-689`). Tests prove `fill_calls == 0` and absent output directory on
  missing/wrong binding. Without a signature, the manifest honestly records
  `OWNERSHIP_EVIDENCE: NOT_PROVIDED`.
- Every produced data file and sidecar uses exclusive creation (`xb` / `x`) at tool `:135-150`.
  No cleanup deletes evidence. Query exceptions with captured HTTP bytes create
  `<name>_ERROR.json` and its sidecar before refusal (`:403-433`). All writes are beneath the
  supplied output path after it is created.
- `CapturingInfo` imports only `hyperliquid.info.Info`; it has no `Exchange` import or write-method
  reachability. The signer HTML calls `eth_requestAccounts` and `personal_sign`, not a venue
  endpoint. The signature is an offline ownership proof, not a transaction.

## Findings

1. **NIT — `--verify-existing` accepts an incomplete capture after the manifest sidecar is
   removed.** Tool `:616-645` requires sidecars for response entries, then iterates only sidecars
   that still exist. There is no positive requirement that `CAPTURE_MANIFEST.json.sha256` exists.
   My arm deleted that one sidecar and `verify_sidecars` returned normally, so CLI `:796-799`
   would print `CAPTURE_VERIFY_OK`. The real captures are unaffected (their sidecars exist and
   match), but verification should require the manifest and derived sidecars explicitly.

2. **NIT — `--coin` is an unbound label.** Parser `:779` accepts a requested coin and manifest
   `:757` records it, but queries/derivation `:693-746` neither filter nor refuse native rows of a
   different coin. My offline arm requested `BTC`, returned only native `ETH` fills/funding, and
   completed with `manifest.coin == "BTC"` while the derived rows said `ETH`. Native rows remain
   truthful and downstream intake must compare them, so this is not a false raw capture, but the
   manifest field should be renamed as a request or bound to the native inventory.

3. **NIT — malformed timestamp syntax escapes as an unhandled `ValueError` instead of a named
   refusal.** `parse_utc` at tool `:116-120` does not wrap `datetime.fromisoformat`; `main` catches
   only `CaptureRefused` at `:810-814`. The offline CLI arm returned `RC=1` with
   `ValueError: Invalid isoformat string: 'not-a-time'`. This occurs before output or network, so
   it cannot create false evidence, but it is inconsistent with the tool's fail-closed error
   vocabulary.

Owner item (not a code finding): the signed text and manifest truthfully say
`binds: "address+run_id"` (tool `:575-585`). They do not bind network, window, or coin, and differ
from the packet's proposed UTC-date-bearing text. Changing the signed domain would invalidate
existing signatures; the owner explicitly retained that decision. Do not infer more from the
signature than address control for that run id.

No REQUIRED finding remains. R-1 and R-2 are closed without rejecting legitimate rows exactly at
the advancing cursor, and both real account-state fixtures carry `assetPositions`. Validation is
deliberately narrow (presence, not a full clearinghouse-state schema); the raw bytes remain the
evidence.

## NOT VERIFIED

- No network call was made by me, as required. I did not rerun r1/r2 or observe the owner's
  current account state.
- Real Hyperliquid pagination beyond one page remains unobserved. Every real page here is short;
  all multi-page conclusions come from SDK documentation plus offline fakes/mutants.
- I did not verify browser screenshots, human order/fill association, current venue cadence,
  current fee tier, or any production-admission decision.
- The full-suite clean-root result was not reproduced under this launcher's allowed write roots;
  my exact environmental result is recorded above. I did reproduce the mandated focused suite,
  historical prefix, all six original NIT mutants, NIT-4 replay/mutant, R-1/R-2 mutants, hashes,
  sidecars, Ruff, format, and compilation.

VERDICT: PASS-WITH-NITS
