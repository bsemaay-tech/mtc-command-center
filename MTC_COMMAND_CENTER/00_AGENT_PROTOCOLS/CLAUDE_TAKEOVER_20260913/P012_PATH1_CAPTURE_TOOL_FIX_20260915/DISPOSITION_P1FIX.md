# P1FIX Disposition — Lead-authored (owner `OD-20260915-P012-P1FIX-LEAD-1`: "A")

Worktree `C:/tmp/P1CAP_20260914`, branch `feature/p012-path1-capture-20260914`, starting HEAD `e77af1c8` → new HEAD: see `LEAD_VERIFICATION_P1FIX.md`.
Author: Claude Opus 5 Lead (session 743291). Every Codex home hit its weekly usage limit on 2026-09-15 (Plus until Sep 19 18:47 local, `free` until Sep 19 11:10, `third` until Oct 6); OpenCode Go hung; the Gemini coder wrapper needs PowerShell 7 (absent). The owner chose "A": the Lead writes the correction and discloses it; acceptance keeps the full independent roster (Gemini delta, exact Opus after 2026-09-16 20:00Z, exact Sol after the Codex reset); the Lead never accepts its own code.

Files changed (2): `IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py` (+230/−48 incl. `ruff format`), `IBKR_PAPER_BRIDGE/tests/test_capture_own_account_evidence.py` (+353/−… ; 10 → 21 tests). No other file; `path1_sign_ownership.html` unchanged (its message is already byte-identical to `ownership_message`).

| Finding | Disposition | Where (candidate) | Test |
|---|---|---|---|
| **F-1 (REQUIRED)** run_id defaulted when a signature is supplied | FIXED — `CAPTURE_REFUSED_RUN_ID_REQUIRED` before any network object or file; run_id defaults only without a signature | `run_capture`: run-id gate + `ownership_result(...)` moved to the start (before `out_dir.mkdir`/`make_info`) | `test_signature_without_run_id_refuses_before_network_and_writes_nothing` (fill_calls 0, out dir absent) |
| **F-2 (REQUIRED)** no window filter; SDK endTime inclusive vs intake half-open | FIXED — `paged_query`: `t < start_ms` → `CAPTURE_REFUSED_MALFORMED "row before requested start"`, `t > end_ms` → `"row after requested end"`, `t == end_ms` EXCLUDED (half-open) but stored in the original bytes; manifest `window.{start_ms,end_ms,semantics}` = `half_open_start_inclusive_end_exclusive_ms` | `WINDOW_SEMANTICS`, `paged_query` | `test_half_open_window_excludes_row_at_end_but_keeps_inside_rows`, `test_row_before_requested_start_refuses`, `test_row_after_requested_end_refuses`, manifest window asserted in the first test |
| F-3 / L-4 signature verified after the network passes | FIXED (with F-1) — verified first; a wrong signature or a signature over another run_id refuses `CAPTURE_REFUSED_OWNERSHIP_SIGNATURE` with nothing written | `run_capture` | `test_wrong_ownership_signature_refuses_before_network_and_writes_nothing` (two arms) |
| F-4 / L-3 funding identity omits coin | FIXED — `hash-time-coin:{h}:{t}:{coin}`; missing coin → `CAPTURE_REFUSED_MALFORMED "funding identity has no coin"` | `funding_coin`, `funding_identity` | `test_funding_identity_includes_coin` |
| F-5 / L-5 `write_once` TOCTOU | FIXED — `open(path, "xb")` for the payload and `open("x")` for the sidecar; existing file → `CAPTURE_REFUSED_MALFORMED "output exists"` | `write_once` | `test_write_once_refuses_an_existing_output` |
| F-6 / L-5 error bytes dropped | FIXED — `call_info` attaches the popped capture to `CaptureRefused.error_capture` (detail carries `status=<code>`); `recorded_call` stores it as `<name>_ERROR.json` + sidecar + manifest entry before re-raising | `call_info`, `recorded_call` | `test_error_response_bytes_are_kept_before_refusal`, `test_capturing_info_post_keeps_pre_parse_bytes_and_error_bytes` |
| F-7 / L-6 manifest lacks `raw_bytes_source` | FIXED — every entry carries `raw_bytes_source`: `http_response_content` (CapturingInfo) or `reserialized_parsed_json_TEST_DOUBLE_ONLY` (fallback, test doubles only; `make_info` always returns `CapturingInfo`) | `RawCapture.source`, `consume_capture`, `record_response` | asserted in the first test (TEST_DOUBLE) and in the CapturingInfo test (HTTP) |
| F-8 `CapturingInfo.post` never exercised | FIXED — unit test with a fake session: URL = base_url + "/info", posted JSON == recorded body, pre-parse bytes captured, non-2xx → bytes captured BEFORE `_handle_exception` raises | — | `test_capturing_info_post_keeps_pre_parse_bytes_and_error_bytes` |
| F-9 / L-2 missing RED arms | FIXED — wrong signature; multi-page success (two full pages + short page, inclusive-restart dedup, cursor windows asserted) | — | `test_wrong_ownership_signature_…`, `test_multi_page_success_dedups_the_inclusive_boundary` |
| F-10 / L-1 lint + format | FIXED — Ruff `--select E9,F821,F811,F401,F841,RUF100` clean; `ruff format` applied to both files (`--check` clean) | both files | — |
| F-11 re-query compares identity sets only | FIXED — `requery_check` compares `{identity: row}` maps; refusal names the first identity only in one pass or with differing content | `requery_check` | `test_requery_content_mismatch_refuses`, `test_requery_identity_mismatch_refuses` (detail asserted) |
| L-2 (Lead) | as F-9 | | |
| L-3 / L-4 / L-5 / L-6 (Lead) | as F-4 / F-3 / F-5+F-6 / F-7 | | |

## Evidence (pinned Bridge deps interpreter `C:/tmp/P012_FUNDING_PY312_20260911/Scripts/python.exe` = Python 3.12.12; `-p no:cacheprovider`; `--basetemp` under the user temp dir)
- Focused module: `21 passed` (`LEAD_FOCUSED_PY312.txt`).
- **RED on the pre-fix tool** (`git show e77af1c8:…/capture_own_account_evidence.py`, sha256 `a1ef5ee1…`, scratch tree + this test module): **`12 failed, 9 passed`** — the 12 failures are exactly the new arms (manifest window/raw_bytes_source, half-open window, before/after range, re-query detail and content, funding coin, exclusive write, error bytes, CapturingInfo error capture, run-id gate, wrong signature before network); the 9 passing tests fence behaviour that already existed (`LEAD_RED_ARMS_PREFIX_TOOL.txt`).
- Full Bridge suite on 3.12 with a clean basetemp: `LEAD_FULL_SUITE_PY312.txt`.
- Ruff 0.16.4 check clean; `ruff format --check` clean; `py_compile` OK; repo guard: `LEAD_GUARD.txt`.
- `SHA256SUMS.txt` (LF) beside this file.

## NOT VERIFIED
- No network call was made; no real capture exists; the real API's pagination and the exact `userFunding` row shape (coin under `delta`) are asserted from the SDK docstrings and the broker's usage, not from a live response.
- Not reviewed: Gemini delta detection next; exact Opus after the weekly reset; exact Sol after the Codex reset. NONACCEPTING.
