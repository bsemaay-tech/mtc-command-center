# LEAD_ADJUDICATION — DD06_PROBE_GEMINI (gemini-3.8-flash-high DETECTION review of the Lead-written WP-P0-29 DD-06 testnet probe) — 2026-09-15 16:05Z

**Formal outcome (updated 20:02Z): COUNTED attempt 3 on slice 3 `1af85067` — PASS-WITH-NITS** (19:56:16-19:59:50Z, 214 s, envelope `status: SUCCESS`, exit 0; 34 native reads, 0 outside, 0 display mismatches, 27 distinct packet files; tasks 1-8 PASS again and the three new tasks 9-11 PASS: the r1 record matches the packet's promised abort semantics; `round_hl_price` bounds the control price to wire constraints (76974.0 → 69270.0); only a `statuses[].error` makes an ok-envelope REFUSED, so a genuine success of a fund-moving arm stays NOT_REFUSED; with spot USDC recorded, an r2 `DD06_REFUSALS_OBSERVED` reads soundly under §4). The two NITs are the same observational ones as attempt 2 (`_HEX40` prefix boundary; `_resting_oid` regex parse, fail-closed) — no change. Earlier history: **attempts 1-2 uncounted.** Both attempts ended with the CLI envelope `status: ERROR … UNAVAILABLE (code 503)` after the report; both are recovered from `%TEMP%\gemini_wrapper_failures\` and kept SUPPLEMENTAL (`RECOVERED_RESPONSE_attempt{1,2}_VOIDED.md`, envelopes, native-read audits). The findings were acted on regardless; a counted run is still owed before the T1 roster reads the branch.

| Attempt | HEAD | Window | Report | Reads (`native_read_audit.py`) | Verdict |
|---|---|---|---|---|---|
| 1 | `71cde24e` (slice 1) | 15:05:10-15:18:18Z (776 s model time; the CLI itself retried three times) | 9 916 chars, sentinel + JSON | 22 native reads, 0 outside, **9 display failures** (coverage incomplete; `LEAD_RED_ARM_m2.txt` not read) | REQUEST_CHANGES by content: F-1 REQUIRED, F-2 REQUIRED, F-3 NIT, F-4 NIT |
| 2 | `69377d6b` (slice 2; packet re-staged) | 15:43:04-15:59:34Z (979 s) | 12 954 chars, sentinel + JSON | 24 native reads, 0 outside, 12 display failures in the transcript; the report's own coverage list names every required file complete (probe 4 ranges, tests 3 ranges, packet, commit, stat, SDK signatures, settings, smoke, notes, decisions, all evidence files) | **PASS-WITH-NITS** (2 observational NITs); tasks 1-8 all PASS; F-1..F-4 of attempt 1 confirmed CLOSED |

## Attempt-1 findings → slice 2 (all applied in `69377d6b`, confirmed closed by attempt 2)
| # | Finding | Lead check | Disposition |
|---|---|---|---|
| F-1 REQUIRED | docstring folded withdraw3 into "own address"; a NOT-refused withdraw3 moves funds OFF the venue | correct — `withdraw_from_bridge` is `type: withdraw3` to the bridge chain (SDK source in the packet) | FIXED: docstring + packet say funds WOULD LEAVE the venue (to the owner's own bridge-chain address; testnet faucet money) |
| F-2 REQUIRED | any `status: err` / 4xx counted as a refusal — validation refusals (self-send, amount) would masquerade as DD-06 evidence | correct | FIXED: `classify_refusal_text` → AUTHORIZATION / VALIDATION / UNCLASSIFIED per arm; only AUTHORIZATION counts; otherwise `DD06_INCONCLUSIVE` with a finding; RED arm m3 |
| F-3 NIT | abort conditions lacked "control order filled → flatten by hand" | correct | FIXED in the packet |
| F-4 NIT | no explicit write-time guard for a surviving 0x-40-hex address | correct | FIXED: `write_record` refuses it |

## Attempt-2 NITs — disposition
| # | Finding | Lead check | Disposition |
|---|---|---|---|
| NIT-1 | `_HEX40` requires the `0x` prefix; an unprefixed 40-hex address in an atypical error body would survive | correct as stated; Gemini itself notes the prefix requirement is defensible (bare 40-hex collides with git SHAs and other hashes) | **NO CHANGE** — recorded; the venue's SDK renders addresses `0x`-prefixed; a bare-40-hex sweep would create false redactions in oids/hashes |
| NIT-2 | `_resting_oid` parses the oid from the redacted response text by regex; a shape change → `None` → `ABORTED_CONTROL_ARM_NOT_ACCEPTED` (fail-closed, safe) | correct; fail-closed is the intended behaviour | **NO CHANGE** — a structural parse before redaction is cleaner; noted for the T1 roster; not worth a third slice before the roster reads it |

## What the corroboration establishes / does not
- Tasks 1-8 PASS in attempt 2: no mainnet path; key custody sound; funds cannot leave silently (withdraw3 stated plainly); classification honest; state-left-behind handled by abort conditions; stop rule + RED arms verified; packet honest; scope exactly two files with the Bridge suite green (1612 passed).
- Attempts 1-2 uncounted (wrapper-voided); attempt 3 COUNTED (the route recovered at 19:45Z). Route history in `route-lessons-2026-09-15-night`.
- Execution word given 18:25Z; r1 ran 18:33Z and aborted at the control arm (tick size; slice 3 fixes it); **r2 waits for the owner's "r2 go"**; the T1 roster (exact flagship + this counted Gemini) applies before any merge.

Recorded by Claude Opus 5 Lead (session 5, `03c6c8`).
