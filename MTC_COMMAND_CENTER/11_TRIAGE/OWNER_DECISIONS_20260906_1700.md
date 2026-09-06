# Owner decisions 2026-09-06 17:0x (chat, verbatim keys) — standing for this exact scope

| Id | Key | Owner answer | Effect |
|---|---|---|---|
| OD-20260906-9 | `PUBLIC_CAPTURE` | `AUTHORIZE, OPTION A`; `AUTHORIZED_SCOPE_SHA256 = 4f112ccf2346fb06f2255f8e15bd194a40c57b8a496b77939f3c5901ff14a88d` | The read-only public capture (6 requests, 4 URLs, capture-forward only, no history) is authorized once for exactly that scope digest. |
| OD-20260906-10 | `ANOTHER_SESSION` | `YES-CANNOT-PAUSE` | Other sessions (Codex desktop app, Claude desktop app) keep running git in the canonical repo; Lead must tolerate, not ask. |
| OD-20260906-11 | `GEMINI_OBJECT_FRESHEN_TOLERANCE` | `A` — "authorized only for Git objects that existed when the audit lane started and remain byte-identical. New objects, changed object bytes, refs, indexes, commits, worktree files, or repository-content changes must continue to abort the lane." | Helper change implemented exactly so (snapshot of loose-object SHA-256 before the run; a `Changed:.git\objects\xx\<38hex>` event is tolerated only if the path was in the snapshot and its bytes are identical afterwards). |
| — | standing rule | "Do not ask me again for repeated FETCH_HEAD or verified byte-identical object-freshening events." | Recorded. |
| — | P021 | "first provide plain-language choices, consequences, and one recommended answer … Ask me only for genuine risk appetite or business-policy choices." | `C:\tmp\OWNER_P021_DECISIONS_20260906_1600.md` is that packet; until answered, the design's provisional-v1 defaults (A / balanced) are recorded as provisional. |
| — | autonomy | "Continue every safe independent lane in parallel. A pending owner decision may block only the exact action requiring it." | Standing. Owner away ~3 h from 17:0x; no questions during that window. |

## Execution record — OD-20260906-9 (the one external operation)
- Run from a byte-verified copy of the frozen packet v3 (`C:\tmp\P012_CAPTURE_PACKET_AUDIT_V3_20260906_1630`, manifest 69bff94a…) at
  `C:\tmp\P012_PUBLIC_CAPTURE_RUN_20260906_1725`; `FROZEN_SCOPE.json` re-hashed to `4f112ccf…` immediately before the run.
- Command: `capture --frozen-scope FROZEN_SCOPE.json --authorized-scope-sha256 4f112ccf… --i-have-owner-authorization --authorization-instant-utc 2026-09-06T14:00:30Z`
  (the instant = the owner's chat line, 17:00:30 +03:00). Exit 0. `CAPTURE COMPLETE: 6 response(s)`; `verify` exit 0: 6/6 match.
- Output root `C:\tmp\P012_PUBLIC_CAPTURE_V1` (9 files, 1.9 MB): `CAPTURE_MANIFEST.json` (requests_authorized 6 = performed 6,
  `asserted_economic_values: []`, window rule CAPTURE_FORWARD_FROM_AUTHORIZATION_INSTANT, started 16:02:11Z, finished 16:02:23Z),
  `SOURCE_SET_MANIFEST.json` (+ .sha256), `raw/001-fees-doc.bin` … `raw/006-funding-history.bin`.
  Source-set identity SHA-256 `bfe75c4d3e07ce88887f463b745797933cc892ebe61958d8ce56000584bf8a03`.
- No credential, account, order, wallet, transfer, TESTNET, mainnet, PAYG or trading action; no number written into any record.
  The captured bytes are EVIDENCE ONLY; folding them into the I/C/F records is separate design-governed work (capture-forward
  intervals per OD-20260906-5/6) that gets its own audit.

## Helper change record — OD-20260906-11
`AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1` SHA-256 6434f7fe… → **5ce687a1b16d33a7dd55684bbe453a7a6231eda0ff458ccc66cee93a05255397**
(`C:\tmp\PRO_LANES_20260906\add_gemini_helper_freshen_tolerance.py`; PARSE_OK); launchers re-pinned. Objects that are new
(`Created`), or whose bytes differ, and every ref/index/content event still abort the lane.
