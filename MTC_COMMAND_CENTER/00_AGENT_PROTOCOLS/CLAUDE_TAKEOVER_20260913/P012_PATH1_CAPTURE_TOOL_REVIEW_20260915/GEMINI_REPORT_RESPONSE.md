# DETECTION REVIEW REPORT — WP-P0-12 "Path 1" Read-Only Own-Account Evidence Capture Tool
**Candidate Commit**: [`e77af1c8`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/sources/COMMIT_MSG_e77af1c8.txt#L1-L44) (2026-09-15)  
**Reviewer Role**: `gemini-3.8-flash-high` DETECTION Reviewer (First Roster Slot)  
**Evidence Class**: `SUPPLEMENTAL_UNEXECUTED` (Strictly read-only; no execution, no network, no write, no subprocess)  
**Packet Root**: `C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/`

---

## 1. Verified Packet Identities (QUOTED from Lead-Computed `PACKET_SHA256SUMS.txt`)

All digests below are quoted directly from [`PACKET_SHA256SUMS.txt`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/PACKET_SHA256SUMS.txt#L1-L16) and match the lane manifests byte-for-byte:

| File Path | SHA-256 Digest (Lead-Computed / Quoted) |
|---|---|
| `REVIEW_BRIEF.md` | `68b8422cc8e8e591e529e7842d2a27e864d4d34cecb5bec4ce281cf0ac76c435` |
| `sources/COMMIT_MSG_e77af1c8.txt` | `3d77e7e3a878b699fbcf69fe86ebe1918ffc8b84a0149038a895162950848b20` |
| `sources/export_mtc_funding_py_excerpt.md` | `47eb371322e037439158bf67720b7b450d7f26838bd6ae8d9fa92d3a354501a4` |
| `sources/hyperliquid_broker_excerpt.md` | `e6dfc884916446add8f5f3b5fc3c3d536877730e62dfc21b21740d748b1ad3e3` |
| `sources/hyperliquid_sdk_api_excerpt.md` | `696c7fc3c5bd8e23e69bf8d76243f55d6d765908e9ea56129b50e3b5bc669c8d` |
| `sources/hyperliquid_sdk_info_excerpt.md` | `f0209a9664e880b20db8fc529c295fe8a520cfd22367c35c60e25111cdf8ef25` |
| `sources/LEAD_VERIFICATION_P1CAP.md` | `ea75c0042702b4d7c0448d244da5c5d8fc31e9819a332457a2ddbe2bd477d9d8` |
| `sources/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md` | `a1433099c7c9219f1772ca1a7b6304d9109f9dafef6fa08ff5c48a633c2059f2` |
| `sources/REAL_OBSERVATION_INTAKE.md` | `40c969dd962649e2f993db55048eba7b1257e7c9e88a5289315488d87147476a` |
| `sources/REPORT_P1CAP.md` | `1617d2474d7f4afdbbb7e7672601f5f69155b337d65c0e91ac6ff3d45aed1c37` |
| `sources/SHA256SUMS_P1CAP.txt` | `1c8c569ea55d30a0657650a1335596607d05b7bff1c4145e66b374753d965e79` |
| `sources/TASK_P1CAP.md` | `f05dbecb8c84883cb53cb9cb2eac528317193b783f1f236ec6f74e66437b44d4` |
| `subject/capture_own_account_evidence.py` | `a1ef5ee1c1241577e0c3c4edf52a07acb71f67dc36af050d9629fcd8c2ad475d` |
| `subject/path1_sign_ownership.html` | `b43dbe39aaa9536fbc8f3e05d29ddc851ad3d2e3e271e1bee38b53fddc54e01f` |
| `subject/test_capture_own_account_evidence.py` | `d1d2ad20b46d0ec20fac1b15e63f9837d961609d88d234d1a55a6b75f37953b3` |

---

## 2. Checklist Items 1–12 Detailed Analysis

### Item 1: Read-Only by Construction
- **Imports Enumerate**: [`capture_own_account_evidence.py:8-26`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L8-L26) imports only `argparse`, `hashlib`, `importlib.metadata`, `json`, `os`, `re`, `sys`, `dataclasses.dataclass`, `datetime.UTC`, `datetime.datetime`, `pathlib.Path`, `typing.Any`, `eth_account.Account`, `eth_account.messages.encode_defunct`, `hyperliquid.info.Info`, and `hyperliquid.utils.constants`. It contains **no** import of `hyperliquid.exchange`, `Exchange`, `requests`, `urllib`, `socket`, or `subprocess`.
- **Attributes Reached on `Info`/`API`**:
  - `CapturingInfo.__init__` ([`:60-65`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L60-L65)) invokes `super().__init__(base_url, skip_ws=True, meta={"universe": []}, spot_meta={"tokens": [], "universe": []})`. Bypasses WebSocket startup and metadata network fetching.
  - `CapturingInfo.post` ([`:68-80`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L68-L80)) accesses `self.session.post`, `self.base_url`, `self.timeout`, `self._captures.append`, and `self._handle_exception`.
  - `CapturingInfo.pop_capture` ([`:81-82`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L81-L82)) accesses `self._captures.pop()`.
  - `call_info` ([`:154-160`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L154-L160)) accesses `info._captures`, `getattr(info, method_name)(*args)`, and `info.pop_capture()`.
  - The only methods invoked on `Info` are `user_fills_by_time`, `user_funding_history`, and `user_state` (each calling `post("/info", ...)`). No write, order, cancel, transfer, or signing path exists.
- **Key Refusal**: [`capture_own_account_evidence.py:414-415`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L414-L415):
  ```python
  if "HL_API_WALLET_KEY" in os.environ:
      raise CaptureRefused(REFUSED_KEY_PRESENT)
  ```
  Line 414 is the very first executable statement of `run_capture`. In `main()` ([`:520-537`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L520-L537)), only argument parsing, missing argument checks, and offline actions run before `run_capture`. `make_info` is constructed at line 425. **Nothing network-capable is constructed prior to line 414.**

### Item 2: Bytes Are Original
- **`CapturingInfo.post` vs SDK `API.post`**:
  - `API.post` ([`hyperliquid_sdk_api_excerpt.md:20-28`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/sources/hyperliquid_sdk_api_excerpt.md#L23-L32)):
    `payload = payload or {}`, `url = self.base_url + url_path`, `response = self.session.post(url, json=payload, timeout=self.timeout)`, `self._handle_exception(response)`, then `return response.json()`.
  - `CapturingInfo.post` ([`capture_own_account_evidence.py:68-79`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L68-L79)):
    `payload = payload or {}`, `response = self.session.post(self.base_url + url_path, json=payload, timeout=self.timeout)`, `raw = bytes(response.content)`, `self._captures.append(RawCapture(url_path, dict(payload), raw))`, `self._handle_exception(response)`, then `return json.loads(raw.decode("utf-8"))`.
  - Line-by-line comparison confirms identical URL composition, session, payload, and timeout semantics. `raw` is explicitly captured from `response.content` **prior** to `_handle_exception` and **prior** to JSON decoding.
- **Trace of `consume_capture`**:
  - In a real run, `make_info` instantiates `CapturingInfo(base_url)` ([`:425`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L425)).
  - In `consume_capture` ([`:140-144`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L140-L144)), `pop = getattr(info, "pop_capture", None)` is callable on `CapturingInfo`, returning `pop()` (the pre-parse `response.content`).
  - If `pop` is absent (as occurs in the test suite where `FakeInfo` is used), line 144 falls back to `RawCapture(endpoint, body, json_bytes(parsed))`, re-serializing parsed JSON.
  - Manifest entries ([`:231-243`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L231-L243)) do **not** record whether the bytes came from `response.content` or from fallback re-serialization (Confirming Lead L-6).

### Item 3: Pagination and Truncation
- **Hand Simulation 1: Page of exactly the limit sharing one millisecond with rows beyond**:
  - Suppose `limit = 2000`. Page 1 returns 2000 rows. The last rows share timestamp `T`. `page_max` becomes `T`.
  - In iteration 2, `cursor = T`. Query is repeated at `startTime = T`.
  - The SDK/API returns rows starting at `T`. Deduplication via `rows_by_id[ident]` ([`:286-297`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L286-L297)) prevents duplicate insertion.
  - If there are $\ge 2000$ rows in millisecond `T` alone, page 2 returns 2000 rows all at time `T`. `page_max` remains $T \le \text{cursor}$, triggering line 301: `raise CaptureRefused(REFUSED_TRUNCATED, f"{kind} cursor stalled")`. It fails closed on stall.
- **Hand Simulation 2: Final page of exactly the limit**:
  - If total rows matching is an exact multiple of 2000 (e.g. 2000 rows), Page 1 returns 2000 rows (`len == limit`).
  - `page_max` ($T_2 > \text{cursor}$) advances `cursor` to $T_2$.
  - Page 2 queries `startTime = T_2`. It receives the remaining row(s) at $T_2$. Since there are no further rows, `len(parsed) < limit`, line 298 triggers, and `paged_query` terminates successfully.
- **Hand Simulation 3: Rows outside the requested window**:
  - **Defect Detected**: In `paged_query` ([`:283-297`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L283-L297)), the tool **does not filter** returned rows by `start_ms` or `end_ms`. It trusts the API output unconditionally.
  - In `hyperliquid_sdk_info_excerpt.md:145`, `endTime` is documented as **inclusive**. However, MTC funding intake requires half-open intervals `[start_inclusive, end_exclusive)` ([`REAL_OBSERVATION_INTAKE.md:31`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/sources/REAL_OBSERVATION_INTAKE.md#L31)). If a funding event occurs exactly at `end_ms`, it is returned by the venue API and included in `DERIVED_EXTRACTION.json`, mis-windowing the interval.
- **`request_body` vs SDK Posted Body**:
  - `request_body("fills", ...)` ([`:208-215`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L208-L215)) produces `{"type": "userFillsByTime", "user": address, "startTime": start_ms, "endTime": end_ms, "aggregateByTime": False}`. Matches SDK `user_fills_by_time` ([`hyperliquid_sdk_info_excerpt.md:127-132`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/sources/hyperliquid_sdk_info_excerpt.md#L127-L132)) exactly.
  - `request_body("funding", ...)` ([`:216`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L216)) produces `{"type": "userFunding", "user": address, "startTime": start_ms, "endTime": end_ms}`. Matches SDK `user_funding_history` ([`hyperliquid_sdk_info_excerpt.md:154`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/sources/hyperliquid_sdk_info_excerpt.md#L154)) exactly.
  - In `record_response` ([`:234`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L234)), `capture.body` comes directly from `CapturingInfo.post(..., payload)`, which is the actual dictionary posted by the SDK.

### Item 4: Identities and Re-Query Semantics
- **`fill_identity` Collision Analysis**:
  - [`capture_own_account_evidence.py:175-195`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L175-L195): returns `f"tid:{tid}"` if present, else `f"hash-oid-time:{h}:{oid}:{t}"`.
  - If `tid` is absent and an aggressive market order matches against multiple resting limit orders within the same millisecond with `aggregateByTime: False`, multiple partial fills share the exact same `hash`, `oid`, and `time`. Because their prices, sizes, or fees differ, line 294-295 raises `CaptureRefused(REFUSED_MALFORMED, "fills identity conflict")`.
- **`funding_identity` Collision Analysis (Lead L-3)**:
  - [`capture_own_account_evidence.py:197-204`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L197-L204): returns `f"hash-time:{h}:{t}"`, omitting `coin`.
  - If an account holds positions across multiple coins (e.g. BTC and ETH) settled during the same hourly funding block, both events share the same transaction hash and millisecond timestamp. Line 295 will raise `CaptureRefused(REFUSED_MALFORMED, "funding identity conflict")`. Latent for a single-coin account, but confirmed.
- **Re-Query Comparison Semantics**:
  - Lines 475-478 compare only `{row["identity"] for row in fills_1} != {row["identity"] for row in fills_2}`.
  - It checks identity set equality; it does **not** check row dictionary equality between pass 1 and pass 2.
  - Both passes' raw response bytes, sidecars, and manifest entries are persisted to disk (`fills_pass1_page001.json`, `fills_pass2_page001.json`, etc.).

### Item 5: Ownership Evidence
- **Character-by-Character Message Comparison**:
  - Python [`capture_own_account_evidence.py:85-90`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L85-L90):
    ```python
    "P012 Path 1 own-account evidence capture\n"
    f"address: {address.lower()}\n"
    f"run_id: {run_id}"
    ```
  - JavaScript [`path1_sign_ownership.html:31-34`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/path1_sign_ownership.html#L31-L34):
    ```javascript
    "P012 Path 1 own-account evidence capture\naddress: " +
      address.value.trim().toLowerCase() + "\nrun_id: " + run.value.trim()
    ```
  - Header, line break `\n`, lowercase `address: <0x...>`, line break `\n`, and `run_id: <id>` match **character-by-character**.
- **Verification Order (Lead L-4)**:
  - `ownership_result` is invoked at line 495, **after** all 5 network passes and `DERIVED_EXTRACTION.json` are written.
  - An invalid signature raises `REFUSED_BAD_SIGNATURE` at line 399, aborting before `CAPTURE_MANIFEST.json` is written at line 498, leaving orphan files without a manifest.
- **`--run-id` Default Defect**:
  - Line 426: `run_id = args.run_id or datetime.now(UTC).strftime("p012-path1-%Y%m%dT%H%M%SZ")`.
  - When `--ownership-signature` is provided on the command line but `--run-id` is omitted, the CLI does not require `--run-id`. It dynamically generates a timestamp.
  - The signed message (signed in advance with a specific run ID) will **never** match the freshly generated run ID, causing line 399 to raise `REFUSED_BAD_SIGNATURE`. This defect makes the signature unverifiable unless `--run-id` is passed.

### Item 6: The HTML Page
- Inspected [`path1_sign_ownership.html:1-58`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/path1_sign_ownership.html#L1-L58):
  - Exactly 58 lines.
  - **No** external script tags (`<script src="...">` absent). Single inline `<script>` ([`:23-56`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/path1_sign_ownership.html#L23-L56)).
  - **No** external URLs, network requests, `fetch`, `XMLHttpRequest`, or WebSocket calls.
  - The only `window.ethereum.request` methods called are:
    1. `eth_requestAccounts` ([`:42`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/path1_sign_ownership.html#L42))
    2. `personal_sign` ([`:48`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/path1_sign_ownership.html#L48))
  - No transaction submission (`eth_sendTransaction`), contract deployment, or gas expenditure.

### Item 7: Write Discipline
- **`write_once` TOCTOU (Lead L-5)**:
  - [`capture_own_account_evidence.py:113-116`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L113-L116) checks `if path.exists(): raise ...` before `path.write_bytes(data)`.
  - Classic Time-of-Check to Time-of-Use race condition. Exclusive creation requires `open(path, "xb")`.
- **`verify_sidecars` Coverage**:
  - [`capture_own_account_evidence.py:403-411`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L403-L411) iterates over `manifest["responses"]` and asserts that actual bytes SHA-256 equals the `.sha256` sidecar and the manifest record.
  - Note: `DERIVED_EXTRACTION.json` has a `.sha256` sidecar written by `write_once` ([`:484`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L484)), but is not in `manifest["responses"]`, so `verify_sidecars` skips it.
  - Files are written strictly inside `--out`; no files outside `--out` are touched; no delete operations exist.

### Item 8: Error-Path Byte Loss
- **`call_info` Error Path (Lead L-5)**:
  - [`capture_own_account_evidence.py:157-162`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L157-L162):
    ```python
    except Exception as exc:  # noqa: BLE001
        captures = getattr(info, "_captures", [])
        if len(captures) > before:
            raw = info.pop_capture()
            raise CaptureRefused(REFUSED_QUERY_FAILED, type(exc).__name__) from exc
        raise CaptureRefused(REFUSED_QUERY_FAILED, type(exc).__name__) from exc
    ```
  - When the SDK raises `ClientError` or `ServerError` (via `_handle_exception`), `raw` is popped from `_captures` at line 160, but is never written to disk, hashed, or preserved in any report. Error response bytes are permanently lost.
  - Refusal code is generic `CAPTURE_REFUSED_QUERY_FAILED`.

### Item 9: Tests and the RED-Arm Map
- **Demanded Arms Mapping**:
  All 7 demanded arms from Task 4 exist in `subject/test_capture_own_account_evidence.py`:
  1. Truncated full page -> `test_truncated_full_page_refuses` ([`:129`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L129))
  2. Re-query mismatch -> `test_requery_identity_mismatch_refuses` ([`:140`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L140))
  3. Tampered stored bytes vs sidecar -> `test_tampered_stored_bytes_vs_sidecar_refuses` ([`:150`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L150))
  4. Non-2xx/exception -> `test_sdk_exception_refuses_query_failed` ([`:162`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L162))
  5. Malformed address -> `test_malformed_address_refuses_before_sdk` ([`:172`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L172))
  6. Key present in environment -> `test_wallet_key_environment_refuses_before_sdk` ([`:183`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L183))
  7. Network URL constant matching -> `test_requested_network_records_matching_sdk_constant` ([`:195`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L195))
- **Missing Test Arms (Lead L-2 + Extension)**:
  - Missing RED test for an invalid ownership signature (only GREEN recovery at line 204).
  - Missing test for multi-page pagination success (only 1-page stall refusal at line 129).
  - **Critical Test Gap**: `CapturingInfo.post` ([`capture_own_account_evidence.py:68-80`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L68-L80)) is **never driven by any test**. `patch_info` ([`test_capture_own_account_evidence.py:99`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L99)) replaces `make_info` with `FakeInfo`, which does not subclass or call `CapturingInfo`. Every test runs through the re-serialization fallback in `consume_capture`.

### Item 10: Network Constants
- `info_base_url` ([`capture_own_account_evidence.py:121-123`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L121-L123)):
  `constants.TESTNET_API_URL if network == "testnet" else constants.MAINNET_API_URL`.
  Matches broker implementation ([`hyperliquid_broker_excerpt.md:88`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/sources/hyperliquid_broker_excerpt.md#L88)). Verified in test at [`test_capture_own_account_evidence.py:195-202`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L195-L202).

### Item 11: Lint Items (Lead L-1)
- `tests:5`: `import os` unused (`F401`).
- `tool:157`: `# noqa: BLE001` unused directive (`RUF100`).
- `tool:160`: `raw = info.pop_capture()` assigned but never used (`F841`).
- Format drift detected under `ruff format --check`.
- Classified as NIT.

### Item 12: Scope Boundary and DERIVED Extraction Field Coverage
- **Scope Boundary**: Staged commit `e77af1c8` touches strictly 3 new files. `export_mtc_funding.py`, `bridge/broker/hyperliquid.py`, and core modules remain untouched. The file-source adapter is a proposal in `REPORT_P1CAP.md`, not committed code.
- **Extraction Field Coverage**:
  - `fill_derived` ([`:330-355`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L330-L355)) covers every intake field: `coin`, `fee`, `feeToken`, `time`, `crossed`, `side`, `px`, `sz`, `capture_sha256`, `json_pointer`, `tid` or `hash`+`oid`, and `closedPnl` if present.
  - `funding_derived` ([`:358-376`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L358-L376)) covers `hash`, `time`, `coin`, `usdc`, `fundingRate`, `szi`, `capture_sha256`, and `json_pointer`.

---

## 3. Output Tables

### (a) Promise-Conformance Table

| Section 5 Promise | Implementation Location (file:line) | Conformance Status | Notes |
|---|---|---|---|
| Read-only CLI path under Bridge tree | `subject/capture_own_account_evidence.py:1` | **EQUAL** | CLI named and placed as promised |
| Inputs: address, product, UTC window, out dir | `subject/capture_own_account_evidence.py:507-515` | **EQUAL** | `--address`, `--coin`, `--start`, `--end`, `--out` |
| Same read-only Info calls as broker (`user_fills_by_time`, `user_funding_history`) | `subject/capture_own_account_evidence.py:259, 269` | **EQUAL** | Matches broker calls |
| Account state (`clearinghouseState`) | `subject/capture_own_account_evidence.py:313-315` | **EQUAL** | Calls `user_state(address)` |
| Immutable original bytes + SHA-256 sidecars + manifest | `subject/capture_own_account_evidence.py:112-118, 220-244, 485-498` | **EQUAL** | Stored write-once with sidecars |
| Refuse on non-2xx | `subject/capture_own_account_evidence.py:75, 157-162` | **EQUAL** | Refuses `REFUSED_QUERY_FAILED` |
| Refuse on truncation at documented page caps (2000 fills, 500 funding) | `subject/capture_own_account_evidence.py:27-28, 260, 300-301` | **EQUAL** | Constants 2000 and 500 match broker |
| Re-query fills/funding and compare identities | `subject/capture_own_account_evidence.py:430-478` | **DIFFERENT** | Compares identity sets, not row equality |
| Never take key, never write to venue | `subject/capture_own_account_evidence.py:24, 414-415` | **EQUAL** | No exchange import, key hard-refusal |
| Adapter into `export_mtc_funding.py --mode PRODUCTION` | `sources/REPORT_P1CAP.md:65-72` | **EQUAL** | Proposal only; no code written |
| Self-contained offline signing page (no external script/URL) | `subject/path1_sign_ownership.html:1-58` | **EQUAL** | 58 lines, pure local HTML/JS |
| Ownership signature verification offline | `subject/capture_own_account_evidence.py:389-401` | **EQUAL** | Recovers address via `eth_account` |

---

### (b) Lead Findings L-1 .. L-6 Evaluation Table

| Lead Hypothesis | Finding Status | File:Line Evidence | Analysis |
|---|---|---|---|
| **L-1**: Ruff lint findings + format drift | **CONFIRMED** | `subject/test_capture_own_account_evidence.py:5`<br>`subject/capture_own_account_evidence.py:157, 160` | Unused `os` import in tests; unused `noqa` in tool:157; unused `raw` assignment in tool:160; format drift under `ruff format --check`. |
| **L-2**: No RED test for wrong ownership signature; no multi-page success test | **CONFIRMED & EXTENDED** | `subject/test_capture_own_account_evidence.py:129, 204`<br>`subject/test_capture_own_account_evidence.py:53-80, 99` | Confirmed. EXTENDED: `FakeInfo` test double bypasses `CapturingInfo` entirely; `CapturingInfo.post` is completely unexercised by tests. |
| **L-3**: `funding_identity` = `hash:time` only; multi-coin collision | **CONFIRMED** | `subject/capture_own_account_evidence.py:197-204` | Omits `coin`. Multiple positions settled in same block collide and raise `REFUSED_MALFORMED`. |
| **L-4**: Ownership signature verified after 5 network passes | **CONFIRMED & EXTENDED** | `subject/capture_own_account_evidence.py:430-474, 495`<br>`subject/capture_own_account_evidence.py:426` | Confirmed. EXTENDED: When `--ownership-signature` is supplied without `--run-id`, dynamic `run_id` defaults, making signature verification guaranteed to fail after network queries. |
| **L-5**: `write_once` TOCTOU; `call_info` drops raw error bytes | **CONFIRMED** | `subject/capture_own_account_evidence.py:113-116`<br>`subject/capture_own_account_evidence.py:159-161` | `exists()` then `write_bytes()` is TOCTOU (`open(path, 'xb')` required); `raw` is popped and discarded on error. |
| **L-6**: Manifest does not record `raw_bytes_source` | **CONFIRMED** | `subject/capture_own_account_evidence.py:140-145, 231-243` | Fallback re-serialization in test double cannot be distinguished from network bytes in manifest. |

---

### (c) RED-Arm Map

| Demanded Arm (Task 4 / Lead) | Test Function Name | File:Line | Status |
|---|---|---|---|
| Truncated full page | `test_truncated_full_page_refuses` | `subject/test_capture_own_account_evidence.py:129` | **PRESENT** |
| Re-query identity mismatch | `test_requery_identity_mismatch_refuses` | `subject/test_capture_own_account_evidence.py:140` | **PRESENT** |
| Tampered stored bytes vs sidecar | `test_tampered_stored_bytes_vs_sidecar_refuses` | `subject/test_capture_own_account_evidence.py:150` | **PRESENT** |
| Non-2xx SDK exception | `test_sdk_exception_refuses_query_failed` | `subject/test_capture_own_account_evidence.py:162` | **PRESENT** |
| Malformed address | `test_malformed_address_refuses_before_sdk` | `subject/test_capture_own_account_evidence.py:172` | **PRESENT** |
| Wallet key in environment | `test_wallet_key_environment_refuses_before_sdk` | `subject/test_capture_own_account_evidence.py:183` | **PRESENT** |
| Testnet/mainnet URL constant matching | `test_requested_network_records_matching_sdk_constant` | `subject/test_capture_own_account_evidence.py:195` | **PRESENT** |
| Wrong ownership signature (Lead L-2) | — | — | **MISSING** |
| Multi-page pagination success (Lead L-2) | — | — | **MISSING** |
| `CapturingInfo.post` execution test | — | — | **MISSING** |

---

### (d) Numbered Findings with Severity and One-Line Repair

1. **Finding 1 (REQUIRED)**: [`subject/capture_own_account_evidence.py:426, 530-536`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L426)
   - **Severity**: **REQUIRED**
   - **Defect**: When `--ownership-signature` is provided without `--run-id`, `run_id` defaults to a fresh dynamic UTC timestamp, guaranteeing a signature verification failure (`REFUSED_BAD_SIGNATURE`) and rendering the signed evidence unverifiable.
   - **One-line Repair**: `if args.ownership_signature and not args.run_id: raise CaptureRefused(REFUSED_MALFORMED, "--run-id is required when --ownership-signature is provided")`.

2. **Finding 2 (REQUIRED)**: [`subject/capture_own_account_evidence.py:283-297`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L283-L297)
   - **Severity**: **REQUIRED**
   - **Defect**: `paged_query` does not filter rows against the requested window bounds. Since Hyperliquid's `endTime` query parameter is inclusive, events at `end_ms` are returned and admitted, mis-windowing the declared half-open funding interval `[start_inclusive, end_exclusive)`.
   - **One-line Repair**: In `paged_query`, filter rows by timestamp: `t = row_time(row); if t < start_ms or (t >= end_ms if kind == "funding" else t > end_ms): continue`.

3. **Finding 3 (NIT - Lead L-4)**: [`subject/capture_own_account_evidence.py:430-474, 495`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L430)
   - **Severity**: **NIT**
   - **Defect**: Ownership signature is verified after all 5 network passes and `DERIVED_EXTRACTION.json` are written, leaving orphan files without a manifest on failure.
   - **One-line Repair**: Invoke `ownership_result(args.address, args.run_id, args.ownership_signature)` at the start of `run_capture` before line 430.

4. **Finding 4 (NIT - Lead L-3)**: [`subject/capture_own_account_evidence.py:197-204`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L197-L204)
   - **Severity**: **NIT**
   - **Defect**: `funding_identity` omits `coin` (`hash-time:{h}:{t}`), causing collisions if multiple coins settle in the same block.
   - **One-line Repair**: `return f"hash-time-coin:{h}:{t}:{row.get('coin', delta.get('coin', ''))}"`.

5. **Finding 5 (NIT - Lead L-5)**: [`subject/capture_own_account_evidence.py:113-116`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L113-L116)
   - **Severity**: **NIT**
   - **Defect**: `write_once` uses `path.exists()` before `write_bytes()` (TOCTOU race).
   - **One-line Repair**: Replace with `with open(path, "xb") as f: f.write(data)`.

6. **Finding 6 (NIT - Lead L-5)**: [`subject/capture_own_account_evidence.py:157-162`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L157-L162)
   - **Severity**: **NIT**
   - **Defect**: `call_info` pops `raw` on exception and drops the response bytes without recording them.
   - **One-line Repair**: Record the error response bytes and sidecar to disk or capture manifest before re-raising.

7. **Finding 7 (NIT - Lead L-6)**: [`subject/capture_own_account_evidence.py:140-145, 231-243`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L140-L145)
   - **Severity**: **NIT**
   - **Defect**: Manifest entries do not record the byte provenance (`network_response_content` vs `reserialized_json`).
   - **One-line Repair**: Add `"raw_bytes_source": "response_content"` (or `"reserialized_json"`) to manifest entries.

8. **Finding 8 (NIT - Lead L-2 Extension)**: [`subject/test_capture_own_account_evidence.py:53-80, 99`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L53-L80)
   - **Severity**: **NIT**
   - **Defect**: `FakeInfo` test double does not subclass or invoke `CapturingInfo`, leaving `CapturingInfo.post` completely unexecuted by unit tests.
   - **One-line Repair**: Add a unit test driving `CapturingInfo.post` with a mock session to verify byte capture before JSON decoding.

9. **Finding 9 (NIT - Lead L-2)**: [`subject/test_capture_own_account_evidence.py:129, 204`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L129)
   - **Severity**: **NIT**
   - **Defect**: Missing unit tests for invalid signature refusal and multi-page pagination success.
   - **One-line Repair**: Add `test_ownership_signature_mismatch_refuses` and `test_paged_query_multi_page_success`.

10. **Finding 10 (NIT - Lead L-1)**: [`subject/test_capture_own_account_evidence.py:5`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/test_capture_own_account_evidence.py#L5), [`subject/capture_own_account_evidence.py:157, 160`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L157)
    - **Severity**: **NIT**
    - **Defect**: Ruff F401 unused `import os`; RUF100 unused `noqa: BLE001`; F841 unused variable `raw`; format drift.
    - **One-line Repair**: Remove unused import, unused variable, unnecessary noqa, and run `ruff format`.

11. **Finding 11 (NIT)**: [`subject/capture_own_account_evidence.py:475-478`](file:///C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P1CAP_20260915/subject/capture_own_account_evidence.py#L475-L478)
    - **Severity**: **NIT**
    - **Defect**: Re-query verification asserts identity set equality, but does not verify row dictionary content equality across passes.
    - **One-line Repair**: Assert `{r["identity"]: r["row"] for r in fills_1} == {r["identity"]: r["row"] for r in fills_2}`.

---

### (e) EXACT Read Coverage with Ranges and Continuations

All reads were native `view_file` calls (at most 150 lines per view; zero terminal commands, zero external fetches):

1. `C:/LAB/Tradingview_LAB_CLEAN/AGENTS.md`: lines 1–64 (complete)
2. `REVIEW_BRIEF.md`: lines 1–34 (complete)
3. `PACKET_SHA256SUMS.txt`: lines 1–16 (complete)
4. `subject/capture_own_account_evidence.py`:
   - lines 1–150
   - lines 151–300 (continuation 1)
   - lines 301–450 (continuation 2)
   - lines 451–549 (continuation 3, complete)
5. `subject/path1_sign_ownership.html`: lines 1–59 (complete)
6. `subject/test_capture_own_account_evidence.py`:
   - lines 1–150
   - lines 151–225 (continuation 1, complete)
7. `sources/hyperliquid_sdk_api_excerpt.md`: lines 1–48 (complete)
8. `sources/hyperliquid_sdk_info_excerpt.md`:
   - lines 1–150
   - lines 151–160 (continuation 1, complete)
9. `sources/hyperliquid_broker_excerpt.md`: lines 1–99 (complete)
10. `sources/LEAD_VERIFICATION_P1CAP.md`: lines 1–44 (complete)
11. `sources/REPORT_P1CAP.md`: lines 1–72 (complete)
12. `sources/TASK_P1CAP.md`: lines 1–21 (complete)
13. `sources/REAL_OBSERVATION_INTAKE.md`: lines 1–49 (complete)
14. `sources/P012_PATH1_REAL_CAPTURE_PACKET_20260914.md`: lines 1–60 (complete)
15. `sources/export_mtc_funding_py_excerpt.md`: lines 1–84 (complete)
16. `sources/COMMIT_MSG_e77af1c8.txt`: lines 1–44 (complete)
17. `sources/SHA256SUMS_P1CAP.txt`: lines 1–5 (complete)

---

### (f) NOT VERIFIED

- **No Execution**: Neither `test_capture_own_account_evidence.py`, the Bridge test suite, nor any Python script was executed.
- **No Network Activity**: No network call to Hyperliquid mainnet or testnet was initiated.
- **No Real Account State**: The owner's live account balance, position, margin configuration, and trade history were not accessed or inspected.
- **No Real Venue Pagination**: The live behavior of Hyperliquid's `userFillsByTime` and `userFunding` pagination under millisecond boundaries was not tested against the real exchange API.
- **No Production Admission**: No funding candidate, production booking, or schema activation occurred.

---

### (g) Machine-Readable Verdict Object

```json
{
  "part": "P1CAP_GEMINI",
  "verdict": "REQUEST_CHANGES",
  "evidence_class": "SUPPLEMENTAL_UNEXECUTED",
  "required": [
    "Finding 1: subject/capture_own_account_evidence.py:426, 530-536: Default dynamic run_id when --ownership-signature is supplied without --run-id guarantees signature verification failure and makes evidence unverifiable.",
    "Finding 2: subject/capture_own_account_evidence.py:283-297: Unfiltered paged_query combined with inclusive endTime in SDK mis-windows half-open [start_inclusive, end_exclusive) funding intervals."
  ],
  "nits": [
    "Finding 3: subject/capture_own_account_evidence.py:430-474, 495: Ownership signature verified after 5 network queries, writing orphan files on failure (Lead L-4).",
    "Finding 4: subject/capture_own_account_evidence.py:197-204: funding_identity omits coin, causing collisions on multi-coin funding settlements (Lead L-3).",
    "Finding 5: subject/capture_own_account_evidence.py:113-116: write_once uses exists() check before write_bytes() (TOCTOU; Lead L-5).",
    "Finding 6: subject/capture_own_account_evidence.py:157-162: call_info drops HTTP error response bytes on exception (Lead L-5).",
    "Finding 7: subject/capture_own_account_evidence.py:140-145, 231-243: Manifest entries lack raw_bytes_source provenance (Lead L-6).",
    "Finding 8: subject/test_capture_own_account_evidence.py:53-80, 99: CapturingInfo.post is never exercised in tests due to FakeInfo mock (Lead L-2 extension).",
    "Finding 9: subject/test_capture_own_account_evidence.py:129, 204: Missing RED unit test for bad signature and missing multi-page success test (Lead L-2).",
    "Finding 10: subject/test_capture_own_account_evidence.py:5, subject/capture_own_account_evidence.py:157, 160: Lint items (F401, RUF100, F841) and ruff format drift (Lead L-1).",
    "Finding 11: subject/capture_own_account_evidence.py:475-478: Re-query verification checks identity sets only, omitting row dictionary content comparison."
  ],
  "lead_findings": {
    "L-1": "CONFIRMED",
    "L-2": "EXTENDED",
    "L-3": "CONFIRMED",
    "L-4": "EXTENDED",
    "L-5": "CONFIRMED",
    "L-6": "CONFIRMED"
  },
  "missing_red_arms": [
    "Wrong ownership signature (Lead L-2)",
    "Multi-page pagination success (Lead L-2)",
    "CapturingInfo.post execution unit test"
  ],
  "required_scope_unread": []
}
```

VERDICT: REQUEST_CHANGES
GEMINI_READ_ONLY_OK
