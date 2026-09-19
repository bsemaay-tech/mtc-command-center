# WP-P0-12 — oracle capture at funding instants (the step D-4 needs) — design note, 2026-09-16 11:4x UTC+3

Prepared by the Claude Opus 5 Lead (session 6, `4a8233`). Documentary only: no code, no capture, no owner word assumed. Context: slice 4 (`9ef072a8`) admits a real read-only capture under D-1..D-6 **except** D-4 — the r1 capture carries no oracle price at its two funding instants, so the exporter refuses it with `CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE`. That refusal is correct and permanent for r1: the venue's Info API serves no oracle-price history, so an instant that was not captured live cannot be captured later. The first admissible real funding evidence therefore needs a NEW capture window with oracle reads scheduled at the funding hours.

## 1. What the venue offers (public, unauthenticated Info API — no key, no credential surface)
| Endpoint | Carries | Not carried |
|---|---|---|
| `userFunding` (already captured) | `time`, `coin`, `usdc`, `szi`, `fundingRate`, `nSamples` | the oracle price the payment used |
| `fundingHistory` (per coin) | `time`, `fundingRate`, `premium` per hour | oracle price |
| `metaAndAssetCtxs` | per asset AT QUERY TIME: `oraclePx`, `markPx`, `funding` (current hourly rate), `premium`, `openInterest`, `dayNtlVlm` | history — one snapshot per call |
| `candleSnapshot` | OHLC of the mark/mid | oracle |
Consequence: the only source of the oracle price at a funding instant is a `metaAndAssetCtxs` read made AT that instant. The venue stamps the payment 31-60 ms past the hour (r1: +41 ms, +60 ms).

## 2. Proposed capture rule (owner decision before any code)
- **Two reads bracketing the hour:** one at `H − 2 s` and one at `H + 2 s` (wall clock of the capture host, recorded), both raw response bytes kept with `response_sha256`, both listed in the manifest like the funding passes.
- **Admitted value:** the `oraclePx` of the coin from the read AT OR BEFORE the venue stamp that is closest to it (normally the `H − 2 s` read), if and only if the two bracketing reads agree within the venue's oracle update granularity (owner-set tolerance, e.g. 0.05 %); otherwise the instant is `UNRESOLVED:D-4` and stays out. Rationale: the oracle updates roughly every few seconds; disagreement means the instant fell across an update and neither read can be called "the" price.
- **Corroboration, never admission:** the payment-derived price `|usdc| / (|szi| × |fundingRate|)` (r1: ≈ 78 758.6) must agree with the admitted oracle price within the rounding of `usdc` (6 decimals) — a cross-check between two independent producers (the oracle read and the venue's own payment arithmetic); the derived value itself is research evidence only (D-4 as ruled).
- **Locator in the packet:** `oracle_price_source = <sha256 of the oracle response file>#/<json pointer to the coin's oraclePx>` — the shape slice 4 already requires; the adapter fills `oracle_price` from the located value. Option for a later slice: carry the oracle response bytes in the packet (`coverage.oracle_witnesses`) so the exporter can re-open and re-verify them the way it re-verifies the funding pass (today it names the capture, it does not open it — stated in `REAL_CAPTURE_EVIDENCE_LIMITATIONS`).

## 3. Tool shape (engineering slice, T1; Lead builder disclosed or Codex Fri; ~2-3 h)
`capture_own_account_evidence.py` gains a scheduled mode (or a sibling `capture_oracle_at_funding.py`): given the window and the coin, it sleeps to each whole hour inside the window, performs the two bracketing `metaAndAssetCtxs` reads, writes them write-once beside the funding/fills passes, extends `CAPTURE_MANIFEST.json` and `DERIVED_EXTRACTION.json` (`oracle_derived` rows: `time_ms`, `coin`, `oraclePx`, `markPx`, `capture_sha256`, `json_pointer`), and the intake adapter fills D-4 from them. No credential (Info API is public); no host contact needed (the owner PC can run it; KVM2 optional); tests: fixture responses with a real-shaped `oraclePx`, the agreement tolerance RED/GREEN, the derived-price cross-check RED/GREEN, the "no read at the instant → UNRESOLVED" arm.

## 4. What the owner would have to do
A new capture window needs a position open on the owner's own account across at least two funding hours (that is how r1 was made). The Lead cannot and does not open positions; the owner does, if and when he wants the first admissible evidence. Until then P0-12 keeps its research/engineering scope (`OD-20260913-P012-SCOPE-1`) and Q3 "Wait".

## 5. One-liners (when convenient; default = nothing moves)
| # | Question | Words |
|---|---|---|
| O-1 | Build the oracle-capture slice (tool + adapter fill + tests; no capture run)? | `O-1 build` / `O-1 wait` |
| O-2 | Bracketing tolerance for the two reads | `O-2 0.05%` (recommended) or another number |
| O-3 | Next capture window | `O-3 <date/time UTC+3>` when you next hold a position; the Lead schedules the reads |
