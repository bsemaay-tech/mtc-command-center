# LEAD_NOTE — P012 production-admission decision packet record (2026-09-14)

Owner order: `OD-20260914-P012-RISK-PACKET-1` ("prepare the P012 risk packet"). Chain, all on the owner's other subscriptions (Claude MAX = orchestration only):

| Step | Route | Time (Z) | Result | Record |
|---|---|---|---|---|
| Write | Codex Pro Spark `gpt-5.3-codex-spark` (lane P12RISK) | 10:07-10:09 | 7 sections, 10 + 27 rows, 6 decisions; lane died on the Spark WEEKLY cap before SHA256SUMS; file transcoded cp1254 -> UTF-8 by the Lead | `TASK.md`, `LEAD_NOTE_SPARK_LANE.md` |
| Audit 1 | Gemini 3.8 read-only (attempt 2; attempt 1 = GUARD abort from the Lead's own staging race) | 10:22-10:26 | **REQUEST_CHANGES**: 3 BLOCKING (B3/F-13 conflation; invented matrix `:404`; "owner confirmed as qualified reviewer" hedge upgrade), 4 CORRECTION (17 wrong-line citations, paraphrased cells, external citations, typo), 2 NIT | `GEMINI_AUDIT_1/` |
| Correction | Codex Plus `gpt-5.5` high (lane P12FIX) | 10:32-10:46 | packet 120 -> 290 lines, 235 absolute citations reopened, 7 decisions (reviewer WHO question), Table C added | `TASK_FIX1.md`, `DISPOSITION_FIX1.md`, `SHA256SUMS.txt` |
| Delta audit, attempt 1 | Gemini 3.8 read-only (root `..._GEMINI_B`; all 11 cited sources staged, 18 files) | 12:35-12:41 | model completed (PASS) but the wrapper rejected the result envelope after five transient backend `INTERNAL 500` retries were recorded as error steps — **not counted**; report recovered from the CLI transcript as supplemental | `GEMINI_AUDIT_B/` (`LEAD_TERMINAL_ATTEMPT1.md`) |
| Delta audit, attempt 2 | Gemini 3.8 read-only (root `..._GEMINI_B2`, same staged packet) | 12:49-12:53 | **PASS** — F-01..F-09 all RESOLVED; Table A 10/10, Table B 27/27; 115/115 citations EQUAL; new findings none; 30/30 native reads byte-verified | `GEMINI_AUDIT_B2/` (`LEAD_ADJUDICATION.md`) |
| Lead check | Lead (mechanical, real source files) | 12:31 | 235 citations: 177 quote-EQUAL, 57 table cells without a quote (covered by the auditor's verbatim-cell check), 0 wrong | `GEMINI_AUDIT_B/LEAD_CITATION_CHECK.md` |

Presentable: **yes** (`OWNER_PRESENTATION.md`). The packet's seven owner questions are OPEN; their answers will be recorded as `OD-20260914-P012-ADMISSION-Q1..Q7` rows when given. Nothing here accepts WP-P0-12, admits venue facts, or authorizes host/venue/ARM action.

Route finding (owner decision pending, "D10"): the Gemini wrapper (`Invoke-GeminiProReadOnly.ps1` sha256 `66c749a0…`) discards the raw stdout when it rejects a result envelope and pins the envelope to exactly six members; a completed review can therefore be voided by a transient backend error. Proposed repair: persist raw stdout on any post-run failure; tolerate an error-class member when `status` is `SUCCESS` and the sentinel is present (report it on stderr) — the same pattern as the 2026-09-08 ERROR-step repair.

Digests: see `SHA256SUMS.txt` (packet + disposition) and `GEMINI_AUDIT_B2/PACKET_SHA256SUMS_B.txt` (the 18 staged files the auditor read).
