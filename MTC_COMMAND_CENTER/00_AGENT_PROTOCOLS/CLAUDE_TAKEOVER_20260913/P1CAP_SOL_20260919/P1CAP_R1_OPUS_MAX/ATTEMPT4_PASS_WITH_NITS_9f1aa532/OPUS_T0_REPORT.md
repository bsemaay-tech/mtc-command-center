# OPUS T0 REPORT — WP-P0-12 Path 1 capture tool, repair round 1 `9f1aa532`

Reviewer: exact `claude-opus-5`, xhigh, fresh independent T0 read. Fourth read of this tool in
the chain (`af921d75` base → `1029d6e9` NIT slice → `9f1aa532` repair). Brief:
`C:/tmp/OPUS_QUEUE_20260916/P1CAP/REVIEW_BRIEF.md`, ADDENDUM 2.

**No network call of any kind was made.** Every arm is offline: monkeypatched `Info` doubles, a
local `ruff` binary from the uv cache, and read-only inspection of the two real capture records.
No capture was re-run. No `git status/diff/add/commit/checkout` was run in any repository; all git
reads are `rev-parse`, `show <rev>:<path>` and `ls-tree -r <rev>`.

---

## 1. Verified identities (COMPUTED by me)

`git -c safe.directory=* -C C:/tmp/P1CAP_20260914 rev-parse HEAD`

```
9f1aa532d49a9856caf766d2480f3b7744ce86dd
```

Subject files — worktree bytes and committed blob bytes are **identical** (I hashed both: the
worktree file and `git show 9f1aa532:<path>` piped to a scratch copy):

| File | sha256 | bytes |
|---|---|---|
| `IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py` | `ed9c1e03d44b4fb8311d892aaed12bebdfe368abe383eaeb5cd63f494958a3ba` | 29 579 |
| `IBKR_PAPER_BRIDGE/tools/path1_sign_ownership.html` | `b43dbe39aaa9536fbc8f3e05d29ddc851ad3d2e3e271e1bee38b53fddc54e01f` | 2 289 |
| `IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py` | `20efa6fe55917bfea58ca04b57fcaae259e27d5e7ea4cb7c6731d057a08b1ecc` | 26 681 |

Predecessor bytes used for every control and mutant arm (`git show 1029d6e9:…`):

| File | sha256 | bytes |
|---|---|---|
| tool @ `1029d6e9` | `110146c16a701e4dc1663a81a60326cee6041bad1ae0d847a8c6d4dac56e9d9c` | 28 402 |
| tests @ `1029d6e9` | `c38861d3c5f9ece6f6d2dab430100dd7e86abc3f4e9239ed149514788128fcfa` | 24 740 |

### Real capture records (read-only; hashed by me, never re-run)

`--verify-existing` on **both** records with the HEAD tool: `CAPTURE_VERIFY_OK`, exit 0.
Every file equals its `.sha256` sidecar **and** the manifest's `response_sha256`.

| Record | File | sha256 | sidecar | manifest |
|---|---|---|---|---|
| r1 `p012-path1-20260914T1500Z-1900Z-r1` | `fills_pass1_page001.json` | `6cb8586c5b446f6807296fa81c8c2bc5f0d7d249a34b0d0c0980732d6fb18589` | EQUAL | EQUAL |
| r1 | `fills_pass2_page001.json` | `6cb8586c5b446f6807296fa81c8c2bc5f0d7d249a34b0d0c0980732d6fb18589` | EQUAL | EQUAL |
| r1 | `funding_pass1_page001.json` | `6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f` | EQUAL | EQUAL |
| r1 | `funding_pass2_page001.json` | `6f25ba294ae96dd333f6938bfe103f283559a960463ddfd2ce8757806563578f` | EQUAL | EQUAL |
| r1 | `account_state.json` | `ea77db9ab583be926f1dcfae35ef02e629fcb0102efbf0cc4965aae539d6e4fe` | EQUAL | EQUAL |
| r1 | `DERIVED_EXTRACTION.json` | `feb43cd26729b26c8b0419b6eb8d47135d345d1faff93163ee8597b3178047c7` | EQUAL | n/a (af921d75 manifest) |
| r1 | `CAPTURE_MANIFEST.json` | `c837cf1237e9c2d8dfdad250815ee17fbd28e1cd0f98b901ec508f9ed6c2c9cb` | EQUAL | — |
| r2 `p012-path1-20260917T0700Z-1100Z-r2` | `fills_pass1_page001.json` | `29e57b4df67b6ee7ae496f566cc9b2337ecd6530ca32694a91005f1ff292ecec` | EQUAL | EQUAL |
| r2 | `fills_pass2_page001.json` | `29e57b4df67b6ee7ae496f566cc9b2337ecd6530ca32694a91005f1ff292ecec` | EQUAL | EQUAL |
| r2 | `funding_pass1_page001.json` | `a68ce94be835153897bfab1b47fd95608c928d3437af7578a939fd91542ca434` | EQUAL | EQUAL |
| r2 | `funding_pass2_page001.json` | `a68ce94be835153897bfab1b47fd95608c928d3437af7578a939fd91542ca434` | EQUAL | EQUAL |
| r2 | `account_state.json` | `032ac4d02db797dac2a56d50c5110b568e60fd6283e04b47f1e3b9546b2d3577` | EQUAL | EQUAL |
| r2 | `DERIVED_EXTRACTION.json` | `819d41364385c403051141648d9bc272490478ca66f7aba3cfdfc809a55c09c5` | EQUAL | n/a |
| r2 | `CAPTURE_MANIFEST.json` | `a31b80a1a24f36b43a549ada878e487066ff629fc82c9d6aa0755e82fa93eb82` | EQUAL | — |

Both records: `fills`/`funding` pass1 vs pass2 are **byte-identical**; `ownership_evidence` is
`OWNERSHIP_EVIDENCE: VERIFIED` recovering `0x1E265F5E39957E08ed02A120ceFA33A9bd46AC49`; every real
row time lies inside `[start_ms, end_ms]`; no row sits at exactly `end_ms` (so the half-open rule
excluded nothing in either real run); the HEAD `fill_identity` accepts all 5 + 2 real fill rows
(every one carries a `tid`) and `funding_identity` yields 2 and 3 unique identities.

---

## 2. Scope — exactly two files, and the format pass hid nothing

Tree-level scope (`git ls-tree -r`, diffed offline). `1029d6e9` → `9f1aa532` changes exactly two
blobs and nothing else in 9 971 tracked paths:

```
-100644 blob 10e4167f…  IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py
+100644 blob ad130aaa…  IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py
-100644 blob cf877e8b…  IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py
+100644 blob 7240ab53…  IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py
```

No protected scope, no new files, no fixture change.

Because this commit folds a `ruff format` pass in with two behavioural edits, a scope claim of
"nothing else changed" is not readable from the diff by eye. I proved it mechanically: I ran
`ruff format` (0.16.8, the same version the PACKAGE session used, from the local uv cache — no
network) over the `1029d6e9` bytes and diffed the result against the committed `9f1aa532` bytes.

```
cwd: C:/tmp/OPUS_P1CAP_SCRATCH/r1
$ ruff.exe format --no-cache fmt/tools/…py fmt/tests/…py     ->  2 files reformatted
$ diff -u fmt/tools/capture_own_account_evidence.py tool_9f1aa532.py
$ diff -u fmt/tests/test_capture_own_account_evidence.py test_9f1aa532.py
```

The **only** residual differences are:

1. tool `:363-373` — the R-1 comment + `if t < start_ms:` → `if t < cursor:` + message rename.
2. tool `:473-482` — the R-2 comment + the new `if "assetPositions" not in parsed:` block.
3. tests `:251` — `"before requested start"` → `"before requested cursor"`.
4. tests `:392-420` — the two new tests.

Nothing untraceable to those four items. **The formatting pass carries no smuggled edit.**

---

## 3. Promise conformance (packet `P012_PATH1_REAL_CAPTURE_PACKET_20260914.md` §5)

| Promise (§5) | file:line at `9f1aa532` | Verdict |
|---|---|---|
| read-only CLI in the Bridge tree | `tools/capture_own_account_evidence.py` (single file, argparse CLI `:773-818`) | EQUAL |
| inputs = address, product `BTC`, UTC window | `:776-784` (`--address`, `--coin` default `BTC`, `--start/--end`), `:116-124` UTC parse | EQUAL |
| calls `Info.user_fills_by_time` / `user_funding_history` as the broker does | `:316` method selection; `:317` `HL_FILLS_PAGE_LIMIT`=2000 / `HL_INFO_PAGE_LIMIT`=500 (`:37-38`, same constants as `bridge/broker/hyperliquid.py`) | EQUAL |
| plus `clearinghouseState` | `:436-482` `account_state_query`, body `{"type":"clearinghouseState","user":…,"dex":""}` `:444` | EQUAL |
| stores every native JSON object as immutable bytes + sha256 sidecars + manifest | `:135-150` `write_once` (exclusive `xb` create + `x` sidecar), `:275-301` `record_response`, `:750-768` manifest | EQUAL |
| refuses on any non-2xx | inherited `API._handle_exception` at `:98`, wrapped `:190-209` → `CAPTURE_REFUSED_QUERY_FAILED`; error bytes kept as `<name>_ERROR.json` `:403-433` | EQUAL |
| refuses on truncation | `:396-399` raw-row stop condition + `CAPTURE_REFUSED_TRUNCATED` on a stalled cursor | EQUAL |
| refuses on re-query mismatch | `:648-662` `requery_check` (identity set **and** row content), driven `:740-741` | EQUAL |
| **never takes a key** | `:666-667` first executable statement of `run_capture` | EQUAL |
| **never writes to the venue** | no `hyperliquid.exchange`, no `Exchange`, no `cancel/transfer/withdraw/sign_l1_action/usd_transfer` anywhere in the file; only `Info` read methods; the sole `eth_account` use is `Account.recover_message` `:564-566` | EQUAL |

Verified mechanically (`arms/standing_r1.txt` §A). The three `order` substring hits in the file
are `:231`, `:356`, `:360` — all comments/messages about *time order*, no order-placing code.

---

## 4. R-1 / R-2 disposition, with my own RED-on-pre-fix judgement

### The fix sites, read from the committed bytes

| Finding | Committed location | Text |
|---|---|---|
| R-1 | `tools/capture_own_account_evidence.py:370-373` | `if t < cursor:` → `REFUSED_MALFORMED, f"{kind} row before requested cursor ({ident})"` |
| R-2 | `tools/capture_own_account_evidence.py:478-482` | `if "assetPositions" not in parsed:` → `REFUSED_MALFORMED, "account state missing assetPositions (not a clearinghouseState object)"` |

Both match the ADDENDUM's cited line numbers exactly.

### Is `cursor` the right bound? (proved, not assumed)

The R-1 comment claims `cursor` still holds this page's request floor at the point of the check.
Reading `paged_query:304-400`: `cursor` is initialised to `start_ms` `:319`; it is the value sent
as `startTime` in both the recorded manifest body `:325` and the SDK call args `:330`; it is
advanced **only** at `:400`, after the row loop ends `:395` and after the short-page return
`:396-397`. So at `:370` `cursor` is exactly the floor the API was asked for. Confirmed.

The window lower bound is preserved *a fortiori*: `page_max` is initialised to `cursor` `:350` and
only ever grows `:378`, and `cursor = page_max` runs only after `if page_max <= cursor: raise`
`:398-399`. So `cursor` is strictly increasing and `cursor >= start_ms` always — hence
`t >= cursor >= start_ms`. The new bound is **strictly tighter and never looser** than the old
one. This is the "while retaining the original interval bound" condition Sol's fix note asked for.

One property worth recording for the evidence chain: the manifest records each page's actual
request floor, and the R-1 check uses that same value, so a later reader can audit the floor from
the record itself. My 4-page arm's manifest:

```
fills_pass1_page001.json  recorded startTime=1789210800000 endTime=1789214400000
fills_pass1_page002.json  recorded startTime=1789210801000 endTime=1789214400000
fills_pass1_page003.json  recorded startTime=1789210802000 endTime=1789214400000
fills_pass1_page004.json  recorded startTime=1789210803000 endTime=1789214400000
```

### R-2's premise verified against the SDK, not against a description

`hyperliquid/api.py:20-27` (`API.post`): `_handle_exception(response)` runs first and
`api.py:30-32` returns without raising for `status_code < 400`; the parse then falls back to
`return {"error": f"Could not parse JSON: {response.text}"}`. `CapturingInfo.post:91-102`
reproduces that fallback verbatim (`json.loads(raw.decode("utf-8"))` raises `UnicodeDecodeError`
⊂ `ValueError` for a non-UTF-8 body, so the fallback is preserved). A **2xx response with a
non-JSON body** — a CDN/proxy interstitial is the realistic shape — therefore produces a plain
`dict` that the old `isinstance(parsed, dict)` gate accepted. The premise is real.

I confirmed the guard is adequate for **every** call site at these bytes, not just the one
patched (`arms/residual_r1.txt` §D, pristine HEAD bytes):

| Info call returning the sentinel `{"error": "Could not parse JSON: …"}` | Outcome |
|---|---|
| a fills page | `CAPTURE_REFUSED_MALFORMED` — `fills response is not a list` (pre-existing gate `:348-349`) |
| a funding page | `CAPTURE_REFUSED_MALFORMED` — `funding response is not a list` |
| account state | `CAPTURE_REFUSED_MALFORMED` — `account state missing assetPositions …` (**new** `:478`) |
| account state `{}` | `CAPTURE_REFUSED_MALFORMED` — same |
| account state `{"marginSummary": {...}}` (plausible but wrong) | `CAPTURE_REFUSED_MALFORMED` — same |

`assetPositions` against reality: present in **both** real mainnet captures (r1 and r2 top-level
keys are identically `['assetPositions','crossMaintenanceMarginUsed','crossMarginSummary','marginSummary','time','withdrawable']`),
and the test file's default `FakeInfo` state was **already** `{"assetPositions": []}` at
`1029d6e9` (`tests:61`) — so the new requirement breaks no existing double. The only two doubles
that omit it (`tests:383` a list, `tests:413` the sentinel) are the two intentional refusal cases.

### RED-on-pre-fix, judged by me

| # | Fence test | RED on the unpatched `1029d6e9` tool? | Right reason? |
|---|---|---|---|
| R-1 | `test_second_page_row_before_current_cursor_refuses` (`tests:392-405`) | **YES** — `Failed: DID NOT RAISE CaptureRefused` | Yes: the pre-fix code accepts the stale row and completes the capture |
| R-2 | `test_account_state_parse_failure_sentinel_refuses` (`tests:408-420`) | **YES** — `Failed: DID NOT RAISE CaptureRefused` | Yes: the pre-fix `isinstance(dict)` gate admits the sentinel |

Both are test-first fences. I did not take the PACKAGE session's `LEAD_RED_R1_R2_prefix.txt` as my
evidence — my own mutant arms below reproduce the same RED independently.

### Carried items from my `1029d6e9` read

| Prior NIT | Status at `9f1aa532` | Evidence |
|---|---|---|
| **NIT-A** `ruff format` regressed | **CLOSED** — verified independently | §6 below |
| **NIT-B** record error re NIT-4's mutant | CLOSED in the record last round | `LEAD_ADJUDICATION_P1CAP_NIT_T0.md` |
| **NIT-C** `verify_sidecars` misses an unlisted payload file | **still open** (not claimed) | reproduced, §5 arm C |
| **NIT-D** malformed manifest → raw exception, exit 1 | **still open** (not claimed) | reproduced, §5 arm D |
| **NIT-E** dead `else` limb in `fill_derived` | **still open** (not claimed) | `:502-505`, §5 arm E |
| **NIT-F** signed text binds address+run_id only | carried **owner decision**, unchanged | `:575-585`, manifest `binds` field |

---

## 5. My own RED arms (built by me, run by me)

Interpreter: `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe` (3.12.12, SDK 0.24.0,
eth_account 0.13.7). `HL_API_WALLET_KEY` confirmed **absent** from my process environment before
every run (`'HL_API_WALLET_KEY' in os.environ` → `False`; no environment value was ever printed)
and `unset` again on each command line. `--basetemp` under `%LOCALAPPDATA%/opus_p1cap_bt/`.

Scratch tree: a fresh copy of `bridge/ tools/ tests/ config/` at
`C:/tmp/OPUS_P1CAP_SCRATCH/r1/mut` (94 files); both subject files hash-identical to HEAD.
Mutator: `C:/tmp/OPUS_P1CAP_SCRATCH/r1/mutate_r1.py` (restores from the pristine `git show` copy
before each arm).

**Control arm** (pristine scratch tree, must be green):

```
cwd: C:/tmp/OPUS_P1CAP_SCRATCH/r1/mut
$ python -m pytest tests/test_capture_own_account_evidence.py -q -p no:cacheprovider --basetemp …/ctrl
..................................                                       [100%]
34 passed in 1.40s
```

**Mutants.** I deliberately made the R-1 mutant revert *only the comparison operand*, leaving the
comment and the message text untouched, so the arm cannot pass or fail on wording — it tests the
code. R-1b and R-2b are subtler reverts that keep the identifier/shape of the fix in place.

| Arm | Mutation (one hunk) | Result | Sole failure |
|---|---|---|---|
| **R-1** | `if t < cursor:` → `if t < start_ms:` (message/comments untouched) | **1 failed, 33 passed** | `test_second_page_row_before_current_cursor_refuses` — `Failed: DID NOT RAISE CaptureRefused` (`tests:402`) |
| **R-1b** | `if t < cursor:` → `if t < min(cursor, start_ms):` | **1 failed, 33 passed** | same test, same reason |
| **R-2** | delete the `assetPositions` guard `:478-482` | **1 failed, 33 passed** | `test_account_state_parse_failure_sentinel_refuses` — `Failed: DID NOT RAISE CaptureRefused` (`tests:415`) |
| **R-2b** | replace the guard with `if not parsed:` (a weaker shape check the sentinel passes) | **1 failed, 33 passed** | same test, same reason |

Every arm fails for exactly the reason claimed, and each kills exactly one test — no collateral.
Logs: `C:/tmp/OPUS_P1CAP_SCRATCH/r1/arms/R-1.txt`, `R-1b.txt`, `R-2.txt`, `R-2b.txt`.

**Arm C (NIT-C, still open).** After a clean capture I dropped `fills_pass1_page999.json` (no
sidecar, no manifest entry) into the output directory → `verify_sidecars` returns normally, i.e.
`CAPTURE_VERIFY_OK`. Bounded: the five recorded responses, the manifest and the derived view all
remain bound, so an unlisted extra file is inert.

**Arm D (NIT-D, still open).** A manifest whose `responses` entries are strings →
`TypeError: string indices must be integers, not 'str'` out of `verify_sidecars:617`; through
`main` that is an uncaught traceback and **exit 1**, not the named refusal + exit 2 NIT-6 set out
to guarantee. It never prints `CAPTURE_VERIFY_OK`, so this is log hygiene, not a safety gap.

**Arm E (NIT-E, still open).** `fill_derived:502-505` still carries the `else: out["hash"]/["oid"]`
limb, unreachable since `fill_identity:222-236` refuses any fill without an integer `tid`.

**CLI arms at these bytes** (offline, `arms/standing_r1.txt` §D):

| Command | exit | stdout/stderr |
|---|---|---|
| `--print-ownership-message run-9 --address 0xabab…` | 0 | the three-line message |
| `--print-ownership-message run-9 --address nope` | 2 | `CAPTURE_REFUSED_BAD_ADDRESS` |
| `--verify-existing <r1 record>` | 0 | `CAPTURE_VERIFY_OK` |
| `--verify-existing <r2 fixture>` | 0 | `CAPTURE_VERIFY_OK` |
| `--network mainnet` (args missing) | 2 | `CAPTURE_REFUSED_MALFORMED / missing address,start,end,out` |
| full capture with `HL_API_WALLET_KEY` set **in the child env only** | 2 | `CAPTURE_REFUSED_KEY_PRESENT`; **out dir not created** |

**Ownership evidence.** `ownership_message():108-113` vs the offline page
`path1_sign_ownership.html:32-33`: the page builds
`"P012 Path 1 own-account evidence capture\naddress: " + address.trim().toLowerCase() + "\nrun_id: " + run.trim()`;
the tool builds the identical string. Rendered for the same inputs they are **character-identical**
(verified programmatically). The tool's message for the r1 record's own address and run id equals
the recorded `OWNERSHIP_MESSAGE_r1.txt` bytes exactly (after normalising the record file's CRLF
line endings, a storage artifact — the LF form is what the manifest's `VERIFIED` recovery proves
was signed).

Ordering (`arms/standing_r1.txt` §B): `:666` key refusal → `:668` address refusal → `:676-680`
run-id-required → `:685` `ownership_result(...)` → `:687` `out_dir.mkdir` → `:689`
`make_info(base_url)`. Signature verification precedes both the first file and the network object.

---

## 6. Mandated runs and lint

All from `cwd: C:/tmp/P1CAP_20260914/IBKR_PAPER_BRIDGE`, pinned interpreter, `-p no:cacheprovider`.

| Run | Result |
|---|---|
| `pytest tests/test_capture_own_account_evidence.py -q` | **34 passed in 1.24s** |
| `pytest -q` (full collection from the Bridge root) | **1662 passed, 1 skipped, 1 warning in 141.31s** |

The full-suite count differs from the PACKAGE session's `1632 passed, 1 skipped` because it ran
`pytest tests` and I ran bare `pytest`: my collection adds 30 tests from
`tools_v2/analysis_package/tests/test_generator.py` and
`tools_v2/observability/tests/test_export_audit_pack.py` (1 663 vs 1 633 collected). Those are
unrelated to this change and all pass. My run is a strict superset of theirs — no discrepancy.

**Lint (ruff 0.16.8, run from the local uv cache — no network):**

| Arm | Result |
|---|---|
| `ruff check` (defaults), HEAD, both files | `All checks passed!` exit 0 |
| `ruff format --check`, HEAD, both files | **`2 files already formatted`** exit 0 |
| `ruff format --check`, `1029d6e9`, both files | `2 files would be reformatted` exit 1 |

**NIT-A from my `1029d6e9` read is CLOSED**, verified against the bytes with the same ruff version
the PACKAGE session used.

Under the repo's one strict ruff config (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/pyproject.toml`,
which does not govern the Bridge) HEAD reports a single pre-existing `SIM300` Yoda condition at
`tests:367` — present at `1029d6e9` too, unchanged. The PACKAGE session's parity record's `I001`
finding does not reproduce at the file's real path; it is an isort first-party-resolution artifact
of checking the file outside the tree. Either way, parity holds: nothing new.

---

## 7. Window walk (my own arm, `residual_r1.py`, output `arms/residual_r1.txt`)

Window `[1789210800000, 1789214400000)` = `[START, END)`; page limit 2 where multi-page. Run
against the **pristine HEAD bytes**.

| Case | Outcome under `9f1aa532` |
|---|---|
| row at `start-1` | `CAPTURE_REFUSED_MALFORMED / fills row before requested cursor (tid:1)` |
| row at `start` | kept |
| row at `end-1` | kept |
| row at `end` (API `endTime` inclusive) | **stored in the bytes, excluded from the derived view**, no refusal |
| row at `end+1` | `CAPTURE_REFUSED_MALFORMED / fills row after requested end (tid:1)` |
| 3-page ascending pass, each restart repeating the row **at** the cursor | **OK**, tids `[1,2,3]`, windows `(start,end) → (t1,end) → (t2,end)` |
| 4-page ascending pass, boundary repeated each time | **OK**, tids `[1,2,3,4]`, windows `(start,end) → (t1,end) → (t2,end) → (t3,end)` |
| terminal short page holding **only** the row at the cursor | **OK**, tids `[1,2]` |
| **later short page repeating a row at `t0 < cursor`** (the R-1 case) | `CAPTURE_REFUSED_MALFORMED / fills row before requested cursor` — **new; silently accepted at `1029d6e9`** |
| page boundary splits one millisecond (3 rows share `t1`) | `CAPTURE_REFUSED_TRUNCATED / fills cursor stalled` |
| a NEW row at exactly the cursor on a **full** terminal page | `CAPTURE_REFUSED_TRUNCATED / fills cursor stalled` |

**Control for the two TRUNCATED rows** — the brief asks whether the tightened floor rejects
anything a well-formed pass should accept. It does not. I replayed the same three fixtures against
the `1029d6e9` tool loaded side-by-side in one process (`arms/evidence_r1.txt` §2):

| Case | `1029d6e9` | `9f1aa532` | |
|---|---|---|---|
| millisecond split across a page boundary | `CAPTURE_REFUSED_TRUNCATED / fills cursor stalled` | same | **SAME** |
| NEW row at exactly the cursor on a full page | `CAPTURE_REFUSED_TRUNCATED / fills cursor stalled` | same | **SAME** |
| plain 3-page ascending pass | `OK tids=[1,2,3]` | `OK tids=[1,2,3]` | **SAME** |

Both TRUNCATED outcomes are the **pre-existing** `page_max <= cursor` stall guard `:398-399`,
unchanged by R-1. They fail closed: a burst larger than one page inside a single millisecond makes
the capture impossible rather than silently short. **R-1 rejects nothing a well-formed pass
returns; it only refuses responses that violate the floor the tool itself requested.**

Divergence semantics unchanged: `requery_check:648-662` compares `{identity: row}` for both the
identity set and row content, so a value changed between passes refuses with
`CAPTURE_REFUSED_REQUERY_MISMATCH / … row content differs: <identity>`, and an identity present in
only one pass with `… only in one pass: <identity>`. In both real records the two passes hash
identically, so no divergence exists there.

---

## 8. Why my `1029d6e9` read missed R-1 and R-2

Answerable from my own archived report (`ATTEMPT3_PASS_WITH_NITS_1029d6e9/OPUS_T0_REPORT.md`), and
worth recording because the two misses have different causes.

**R-1 — a coverage gap in my own matrix.** My §7 window-walk table had a row for the lower bound
(`row before start`) and several rows for multi-page behaviour (`inclusive cursor restart`,
`full page whose last row shares a ms`, `full page whose last row is at end`). But the lower-bound
arm was **single-page only**, where `cursor == start_ms` and the defect is invisible by
construction; and every multi-page arm placed its later-page rows **at or after** the advanced
cursor. The one cell that catches R-1 — a later page carrying a row in `[start_ms, cursor)` — is
the product of the two axes, and I never crossed them. My table walked each dimension separately.

**R-2 — a reasoning gap, not a coverage gap, and the sharper miss.** I had both halves of the bug
in my own report and failed to join them. At line 159 I verified `CapturingInfo.post` against
`API.post` and wrote explicitly that "`UnicodeDecodeError ⊂ ValueError`, so the SDK's
`except ValueError` fallback is preserved" — I *saw* the `{"error": …}` fallback and recorded it
as a byte-fidelity property. Separately, in my `M3` mutant I checked that `account_state`'s bytes
are recorded before the shape check, and I accepted `isinstance(parsed, dict)` as an adequate gate
without ever asking the joining question: *which dicts can `CapturingInfo.post` itself
manufacture?* The two facts sat in different sections of one report. The lesson I would carry
forward: when a transport wrapper has a documented failure-mode return value, that value belongs
in every consumer's shape-check analysis, not only in the wrapper's fidelity section.

Both gaps are mine; neither was a misreading of the bytes. Sol's independent second-flagship read
found them, and the roster rule worked exactly as designed.

---

## 9. Authorship scrutiny (PACKAGE session, Claude Sonnet 5)

The repair was written by the P0-12 PACKAGE session, disclosed, on the owner's standing ruling. I
treated it as third-party code: my own scratch tree, my own mutants (including two subtler
variants the PACKAGE session did not build), my own lint binary, my own control replay against the
predecessor bytes, and the mechanical proof in §2 that the folded `ruff format` pass carries no
smuggled edit. I read the PACKAGE session's `LEAD_RED_*.txt` and `LEAD_VERIFICATION_*.md` only
after forming my own results, and no claim in this report rests on them.

**Is anything in `9f1aa532` beyond the two findings it closes?** No. §2 proves the commit is
exactly: R-1 fix, R-2 fix, one assertion string rename that follows R-1's message, two new fence
tests, and a pure `ruff format` reflow (which also closes my own carried NIT-A). Sol's R-2 note
offered two fixes — make the parse failure a named failed query, **or** validate the account-state
schema strongly enough to reject the sentinel; the slice took the second, which Sol explicitly
sanctioned. Nothing was widened.

---

## 10. Findings

**No REQUIRED finding.** One new NIT, three carried NITs, one record NIT, one carried owner item.

**NIT-1 (new, low) — R-2 is fixed at the consumer, not at the source that manufactures the
sentinel.** `CapturingInfo.post:99-102` still converts a JSON parse failure on a 2xx response into
a success-shaped `{"error": …}` dict. At these bytes that is harmless: I proved all five Info call
sites reject it (two by the pre-existing `isinstance(parsed, list)` gate at `:348-349`, one by the
new `assetPositions` gate at `:478`). The residual risk is forward-looking — a sixth Info call that
returns a dict would silently re-open the same hole, and the guard is a per-call-site shape check
rather than an invariant. Sol's first suggested fix (raise `CAPTURE_REFUSED_QUERY_FAILED` inside
`post` on parse failure, keeping the raw bytes that `post` has already captured) would make it
structural. Not blocking: the current tool has no uncovered path.

**NIT-2 (carried, was NIT-C, bounded) — `CAPTURE_VERIFY_OK` still does not notice a payload file
with neither a manifest entry nor a sidecar.** `verify_sidecars:598-645` walks the manifest's
`responses` and then every `*.sha256`; a file with neither is invisible (arm C). The five recorded
responses, the manifest and the derived view are all bound, so an unlisted extra file is inert
evidence, and the docstring `:599-603` describes exactly this scope without over-claiming.

**NIT-3 (carried, was NIT-D, log hygiene) — a structurally malformed manifest still escapes as a
raw exception.** `verify_sidecars:616-623` indexes `entry["file"]` without checking the entry is a
dict; entries that are strings give `TypeError` and **exit 1** through `main`, not the named
refusal + exit 2 NIT-6 guaranteed (arm D). It fails loudly and never prints `CAPTURE_VERIFY_OK`,
so it is not a safety gap. Fix: validate each entry, or wrap the loop in
`except (TypeError, KeyError) → REFUSED_BAD_SIDECAR`.

**NIT-4 (carried, was NIT-E, harmless) — dead branch.** `fill_derived:502-505` still carries the
`else: out["hash"]; out["oid"]` limb; since `fill_identity:222-236` refuses any fill without an
integer `tid`, no row can reach it through `paged_query`. It advertises a row shape the tool no
longer accepts.

**NIT-5 (new, record only) — two inaccurate citations in the PACKAGE session's verification
document.** `C:/tmp/CLAUDE_P0_RUN_20260913/P1CAP_NIT_SLICE_20260919/LEAD_VERIFICATION_P1CAP_R1_REPAIR.md`
cites the R-1 fix at `capture_own_account_evidence.py:362-370` and the R-2 fix at `:464-473`,
both labelled "post-format". Against the committed `9f1aa532` bytes the fixes are at `:370-373`
and `:478-482`; the cited `:464-473` range covers the *old* `isinstance(parsed, dict)` check and
the first comment line, and does not contain the `assetPositions` guard at all. The queue's own
`REVIEW_BRIEF.md` ADDENDUM 2 has the correct numbers. Record-only; `9f1aa532` is untouched. Also
cosmetic, in the same class: `test_row_before_requested_start_refuses` (`tests:243`) keeps its old
name while asserting the new `"before requested cursor"` text — accurate behaviour, stale name.

**NIT-F (carried, open by design — an owner decision, not a NIT against this candidate).** The
signed text still binds **address + run_id only**; `start`/`end`/`network` are not signed
(`:575-585`, and the manifest says so with `binds: "address+run_id"`). I continue to agree with the
handling: changing the signed text would invalidate the owner's existing r1 and r2 signatures and
is his call. The `binds` field keeps the manifest honest about what `VERIFIED` does and does not
attest — it proves the address signed *that run id*, **not** that the captured rows are what the
venue returned.

**Observation (not a finding).** The `assetPositions` requirement is an empirical invariant, not a
contract one: it holds for both real mainnet captures of the owner's account and for every test
double, and a hypothetical clearinghouseState shape without it would fail closed (a refusal, never
false evidence). Fine as written; noted so a future account-type change is recognised rather than
debugged.

---

## 11. NOT VERIFIED

- **No network call of any kind was made by me.** Nothing in this report observes the live
  Hyperliquid API. Every `Info` behaviour is asserted against monkeypatched doubles and against the
  two stored real captures.
- **The real API's pagination behaviour beyond one page is unobserved.** Both real records
  (r1 and r2) returned a single page for each of fills and funding, so the entire multi-page cursor
  path — including the R-1 fix itself — has never run against the venue. Every multi-page claim here
  rests on doubles that model the documented `endTime`-inclusive, ascending-order contract.
- **The venue's true row ordering and duplicate semantics are assumed, not measured.** The
  ascending-order refusal (`:355-361`) and the `page_max` cursor arithmetic encode the SDK's
  documented behaviour; a venue that violated it would be refused, not mis-parsed, but I cannot
  confirm which of the two it does.
- **`assetPositions` is not verified against the venue's schema documentation**, only against two
  real responses from the owner's own account and the SDK's call shape.
- **I did not re-verify the r2 fixture's provenance** beyond its self-consistency (bytes ↔ sidecars
  ↔ manifest ↔ derived view reproducible by `fill_derived`/`funding_derived`). That it is the
  output of a real 2026-09-17 mainnet run is taken from the record, not independently attested.
- **Sol's concurrent re-read of these same bytes is in progress and unread by me.** Its report file
  `C:/tmp/SOL_QUEUE_20260919/P1CAP/sol/SOL_T0_REPORT.md` currently holds only a skeleton; I read
  Sol's *archived* `1029d6e9` report and the PACKAGE session's adjudication of it, but nothing from
  the live lane. My verdict is independent of it.
- **My report alone accepts nothing.** The Lead assembles the roster.

---

VERDICT: PASS-WITH-NITS
