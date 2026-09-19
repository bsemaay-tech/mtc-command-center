# LEAD_TERMINAL — WP-P0-12 Path 1 real read-only capture of the owner's own Hyperliquid mainnet account, run `p012-path1-20260917T0700Z-1100Z-r2` — 2026-09-17 15:5x UTC+3 (12:58Z)

**Owner's part (his trading, his money, his word `O-3 now`; the Lead opened and closed nothing):** BTC perp long 0.0006 opened 10:28:49 UTC+3 @ 76,543.0 (isolated 1x, ≈45.9 USDC), closed 13:23:45 @ 76,315.0 (PnL −0.1368 USDC, taker fees 0.019839 + 0.01978); three funding events paid while open (11:00, 12:00, 13:00 UTC+3). A first attempt was a resting limit order at 75,644 (never filled) — cancelled and replaced by a market order on the Lead's public-read check. Signature over the run message made on the reviewed page `path1_sign_ownership.html` (sha256 `b43dbe39…`, served on `http://127.0.0.1:8791` from 13:25 to 15:5x; server stopped afterwards; nothing left the PC) with the owner's own wallet; pasted in chat; `sig_r2.txt` (132 chars, sha256 `b7f17449…`, public data).

**Ownership evidence:** the exact signed string is `ownership_message(address, run_id)` — 135 bytes, LF, no trailing newline, sha256 `81a0c120690bbe2ec1be9fbd233e6888fd3044c97317cfaa468892e119f586d6` (base64 in `OWNERSHIP_MESSAGE_r2_EXACT_BYTES.md`; no CRLF display file this time — lesson of r1). Offline recovery by the Lead → `0x1E26…AC49`; the tool recovered the same before its first network call: manifest `ownership_evidence = {status: "OWNERSHIP_EVIDENCE: VERIFIED", recovered_address: 0x1E26…AC49}`.

**Capture (tool `capture_own_account_evidence.py` at `af921d75`, sha256 `00b3b8f6…`; Bridge interpreter; `HL_API_WALLET_KEY` removed from the child env; public Info API only):** window 2026-09-17T07:00:00Z → 11:00:00Z (half-open; `start_ms` 1789628400000 / `end_ms` 1789642800000), run 12:58:03-12:58:06Z after the window closed; `CAPTURE_OK`; `--verify-existing` → `CAPTURE_VERIFY_OK`; `sha256sum -c SHA256SUMS_r2.txt` → 7 OK.
| File | bytes | sha256 (first 16) | source |
|---|---|---|---|
| `fills_pass1_page001.json` / `fills_pass2_page001.json` | 638 / 638 | `29e57b4df67b6ee7` / identical | `http_response_content` |
| `funding_pass1_page001.json` / `funding_pass2_page001.json` | 655 / 655 | `a68ce94be8351538` / identical | `http_response_content` |
| `account_state.json` | 309 | `032ac4d02db797da` | `http_response_content` (no position after close) |
| `DERIVED_EXTRACTION.json` (`DERIVED_VIEW_NOT_ORIGINAL_BYTES`) | — | sidecar | derived |
| `CAPTURE_MANIFEST.json` | — | sidecar | self |
Derived: fills 07:28:49.887Z B 0.0006 @ 76,543.0 (fee 0.019839) and 10:23:45.800Z A 0.0006 @ 76,315.0 (fee 0.01978); funding 08:00:00.011Z usdc −0.000371 rate 0.0000081083 szi 0.0006; 09:00:00.001Z −0.000439 / 0.0000095561; 10:00:00.041Z −0.000569 / 0.0000124143. Venue lateness 1-41 ms past the hour (r1: 41-60 ms).

**Oracle evidence at the funding instants (`P012_ORACLE_CAPTURE_20260917/reads/`, reader started 10:00 UTC+3 on `O-3 now`, host clock):**
| Funding instant | read H−2 s (oraclePx) | read H+2 s | Δ (owner O-2 limit 0.05 %) | position witnessed H+3 s |
|---|---|---|---|---|
| 08:00:00.011Z | 76,456.0 @ 07:59:58.000 | 76,463.0 @ 08:00:02.000 | 0.0092 % | BTC szi 0.0006 |
| 09:00:00.001Z | 76,572.0 @ 08:59:58.003 | 76,575.0 @ 09:00:02.000 | 0.0039 % | BTC szi 0.0006 |
| 10:00:00.041Z | 76,472.9 @ 09:59:58.000 | 76,472.9 @ 10:00:02.001 | 0 | BTC szi 0.0006 |
Cross-check (design note §2): |usdc| = szi × rate × oracle holds if the venue TRUNCATES usdc to 6 decimals (0.0006 × 0.0000081083 × 76,456 = 0.00037197 → 0.000371; 0.0006 × 0.0000095561 × 76,572 = 0.00043904 → 0.000439; 0.0006 × 0.0000124143 × 76,472.9 = 0.00056962 → 0.000569) — the O-1 adapter fill must allow truncation, not rounding.

**Intake dry run (adapter + exporter at `a871e429`, `LEAD_INTAKE_r2_stdout.txt`, `intake_r2_a871e429/`, `LEAD_EXPORTER_r2_dry_run.txt`):** adapter `events=3 fills=2 complete=True real_packet=BUILT`; exporter under the real profile on the packet as emitted → `CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE` (D-4 unfilled: the adapter's oracle fill is the O-1 slice the owner said `wait`); with the three D-4 locators filled BY HAND from the real H−2 s reads (`<sha256 of the read>#/1/0/oraclePx`) → **`REAL_CAPTURE_CANDIDATE_BUILT`**, `completion_check` expected == observed == [08:00, 09:00, 10:00], `opening_position 0.0`, `position_source coverage.fills_witness`, admission `REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD` (by construction; Q3 "Wait" stands) — the first real capture to pass D-1..D-6 end to end; NONACCEPTING Lead dry run (hand-filled locators; FIXTURE retained rows for the Bridge half, as for r1: no schema-v10 store has observed these events). Candidate bytes `LEAD_DRY_RUN_r2_candidate_hand_filled_D4.json` (sha256 `5da216b7…`).

**What this is and is not:** research/engineering evidence under `OD-20260913-P012-SCOPE-1`; no production admission (`OD-20260914-P012-ADMISSION-Q3` "Wait"); the owner self-attests ownership (`OD-20260914-P012-ADMISSION-Q1`). To make D-4 tool-filled: `O-1 build` (the oracle-capture/adapter-fill slice, T1). Records here + CT13 `CLAUDE_TAKEOVER_20260913/P012_PATH1_REAL_CAPTURE_20260917/`.

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
