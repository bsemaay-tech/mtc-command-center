# LEAD_TERMINAL — WP-P0-12 Path 1 real read-only capture of the owner's own Hyperliquid mainnet account, run `p012-path1-20260914T1500Z-1900Z-r1` — 2026-09-15 07:15:52-07:15:54Z

**Result: CAPTURE_OK; CAPTURE_VERIFY_OK. Evidence class: NONACCEPTING real observation (the capture tool `af921d75` is Gemini-delta-reviewed but not yet accepted by the exact roster; the intake adapter into `export_mtc_funding.py` is not built). No order was placed or touched; the tool made five read-only Info API calls (`https://api.hyperliquid.xyz`, SDK 0.24.0) with the API-wallet key variable removed from its process environment (it refuses otherwise).**

## Ownership evidence
The owner signed the printed message (`OWNERSHIP_MESSAGE_r1.txt`: address lower-cased + run_id) with his own wallet on the reviewed offline page `path1_sign_ownership.html` (sha256 `b43dbe39…`, served on `http://127.0.0.1:8791` for the signing minute because browsers do not inject wallet providers into `file://` pages; server stopped afterwards; nothing left the PC). Signature file `sig_r1.txt` (sha256 `2b7a9eb4…`, 132 bytes, public data). Verified offline by the Lead and again by the tool before its first network call: `OWNERSHIP_EVIDENCE: VERIFIED`, recovered `0x1E26…AC49`. (Q1 of the admission packet: the owner self-attests; this signature binds the attestation to the address and this run — it is not a certification.)

## Capture (window 2026-09-14T15:00:00Z → 19:00:00Z, half-open, `start_ms` 1789398000000 / `end_ms` 1789412400000)
| File | bytes | sha256 (first 16) | source |
|---|---|---|---|
| `fills_pass1_page001.json` / `fills_pass2_page001.json` | 1605 / 1605 | `6cb8586c5b446f68` / identical | `http_response_content` |
| `funding_pass1_page001.json` / `funding_pass2_page001.json` | 433 / 433 | `6f25ba294ae96dd3` / identical | `http_response_content` |
| `account_state.json` | 309 | `ea77db9ab583be92` | `http_response_content` |
| `DERIVED_EXTRACTION.json` | 2141 | `feb43cd26729b26c` | derived view |
| `CAPTURE_MANIFEST.json` | 3497 | `c837cf1237e9c2d8` | manifest |
Every file has a `.sha256` sidecar; `--verify-existing` → `CAPTURE_VERIFY_OK`. Both passes byte-identical (re-query content check passed). One page each (far below the 2000/500 caps).

## Lead reading of the derived view against the owner's declared activity (`P012_PATH1_REAL_CAPTURE_PACKET_20260914.md`)
| Declared | Captured (UTC) | Match |
|---|---|---|
| T2 taker buy | 16:03:30.942 BTC B 0.00016 @ 78462.0, fee 0.005423 USDC, crossed True, tid 261929593852405 | ✔ |
| T3 taker buy | 16:05:15.271 BTC B 0.00013 @ 78451.0, fee 0.004405 USDC, crossed True | ✔ |
| duplicate taker buy | 16:06:11.269 BTC B 0.00013 @ 78438.0, fee 0.004405 USDC, crossed True | ✔ |
| T1 maker buy | 16:14:34.869 BTC B 0.00016 @ 78410.0, fee 0.001806 USDC, **crossed False** | ✔ (maker fee visibly lower) |
| position 0.00058 BTC held through two settlements | funding 17:00:00.041Z −0.000571 USDC, 18:00:00.060Z −0.000572 USDC, rate 0.0000125, szi 0.00058 | ✔ (settlement stamps 41 ms / 60 ms past the hour — same venue offset class as the 2026-09-08 capture) |
| close after 18:02Z | 18:08:43.372 BTC A 0.00058 @ 78993.0, fee 0.019792 USDC, closedPnl +0.320856 | ✔ |
| net ≈ +0.28 USDC | closedPnl 0.320856 − fees 0.035831 − funding 0.001143 = **+0.283882 USDC** | ✔ |
| account after | `assetPositions` 0, `withdrawable` 0.0 (owner withdrew) | consistent with the owner's statement |
All five fills carry `feeToken` USDC and native `px`/`sz` strings; the derived view carries `capture_sha256` + JSON pointer per row so every value re-locates in the original bytes.

## Status and next
- This is the FIRST real own-account observation for Path 1. It does not admit anything: `OD-20260914-P012-ADMISSION-Q3` ("Wait") keeps C-10 blocked; weeks of captures are the owner's stated bar; the file-source adapter into `export_mtc_funding.py --mode PRODUCTION` is a proposal only (`REPORT_P1CAP.md`).
- Intake per `REAL_OBSERVATION_INTAKE.md` requires the complete exact-once inventory for the declared interval and the retained `FundingEventRecord` fields — the derived view holds `coin`, `usdc`, `fundingRate`, `szi`, `time`, `hash`; the mapping to `event_id`/`amount_usdc`/`effective_ts`/`source=HL_USER_FUNDING`/`position_szi`/`n_samples` is the adapter's job (not built; Codex or owner-scoped later).
- Records: this dir copied to CT13 `P012_PATH1_REAL_CAPTURE_20260915/`; the tool acceptance roster continues (exact Opus Wed, exact Sol Sep 19).

Recorded by Claude Opus 5 Lead (743291).
