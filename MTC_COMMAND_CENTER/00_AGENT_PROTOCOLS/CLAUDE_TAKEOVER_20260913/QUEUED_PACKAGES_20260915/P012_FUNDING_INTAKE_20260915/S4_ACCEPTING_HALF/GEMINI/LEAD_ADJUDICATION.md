# LEAD_ADJUDICATION — P012_INTAKE_S4_GEMINI (detection review of slice 4, the ACCEPTING half) — 2026-09-16 11:2x UTC+3 (08:2xZ)

Reviewer: gemini-3.8-flash-high, read-only, `SUPPLEMENTAL_UNEXECUTED`. Subject: `9ef072a8` on `feature/p012-funding-intake-adapter-20260915` (parent `b667dbcc` format-only). Lead = author of the candidate (disclosed); this adjudication compares and reproduces, it does not accept.

## Attempts
| # | When (Z) | Outcome | Record |
|---|---|---|---|
| 1 | 07:50:25-07:54:54 | **FAIL at the stdin transport** — launcher error `Stdin transport failed: … "Boru sonlandı."` (pipe ended); REVIEW.log 152 B; no CLI conversation directory created (the probe one minute earlier was OK) → nothing to recover; treated as a transient CLI start failure | `FAILED_ATTEMPTS/attempt1_STDIN_TRANSPORT/` |
| 2 | 08:02:35-08:07:26 | **COUNTED** — `status: SUCCESS`, exit 0, 279 s, 1 turn; usage input 664 226 / output 39 908 / thinking 21 733 tokens; envelope conversation `2016bdb3-…` (`CID.txt`) | `REVIEW.log` (28 061 B, sha256 `d2122535…`), `REPORT_RESPONSE_UTF8.md`, `LEAD_TERMINAL.json` |

## Native read audit (attempt 2)
`NATIVE_READ_AUDIT_attempt2_COUNTED.json`: **66 native reads, 0 failures, 0 outside the packet**, every displayed range content-matched. Every REQUIRED file was read completely: the semantic patch (19 ranges, 1-2900), the new test module (7 ranges), the adapter at HEAD (4 ranges), the verification record, both commit messages, the diff stat, the blob OIDs, the r1 real packet and gap report, the derived view, the DECISIONS rows, the owner packet, the carried-fences file at the two required ranges (1-70, 1330-1375), every `LEAD_*.txt`, the format-only patch (3 ranges, complete), and nine cited ranges of the exporter at HEAD.

## Verdict as returned
`PASS-WITH-NITS`; `rules: D-1..D-6 = VERIFIED`; `fence_changes: []`; `fabricated_fields: []`; `required_scope_unread: []`; two NITs, no REQUIRED finding, "no changes requested".

## Comparison with the Lead's own verification (`LEAD_VERIFICATION_P012_INTAKE_S4.md`)
| Point | Gemini | Lead | Disposition |
|---|---|---|---|
| Explicit admission; no inference path; both mismatch directions; unknown kinds | §1: confirmed from the patch, cites `_resolve_profile`, `_require_evidence_kind`, `_load_packet`; fences byte-unchanged | same | CONCORDANT |
| D-1..D-6 producers + failing inputs | §2 table: VERIFIED ×6 with the implementing hunks and the discriminating tests named per rule | §0 contract table | CONCORDANT |
| Real candidate labels / non-admission / limitations | §3: 9 root keys, no MTC selection key, limitations name the oracle and Q3 | §1, §3 | CONCORDANT |
| Adapter real packet field table | §4: every value COPIED / TOOL-RULE / DERIVED-UNDER-RULING / UNRESOLVED; `fabricated_fields: []`; no ~78758 price anywhere | real r1 dry run | CONCORDANT |
| `payload_digest` label change | §5: correct against `FundingEventRecord.digest` (domain `MTC_BRIDGE_FUNDING_PAYLOAD_V1`) and the conflation rule; a DISCLOSED correction, not a silent fence change | §1 (adapter row) | CONCORDANT |
| RED / mutants | §6: 57/57 RED; M1/M2/M3/M4 catching tests as in the Lead files; the sharpened M3 test discriminates on its own | §2 | CONCORDANT |
| Leakage / scope / format-only commit | §7: short address only; synthetic tx hashes; stdlib imports; 4 files; format-only patch = reflow only (3 ranges) | §1, §3 | CONCORDANT |
| Honest limits | §8: limits visible in artifacts | §3 | PARTLY — see correction 1 |

## Lead corrections of the reviewer's text (none affects the verdict)
1. §8 item 1 cites `export_mtc_funding.py` docstring lines 27-31 as stating the "no schema-v10 store with the owner's events" limit. Those lines state the production-mode limit, not the store limit; the store limit is stated in the new test module's docstring (lines 14-18) and in the Lead record §3, not in the exporter's docstring. **Follow-up wording item** for the same future cleanup as NIT-1: add one sentence to the exporter docstring ("the CLI still needs a schema-v10 snapshot that has retained the events; none exists for the owner's account today"). Not changed now — a new commit would move HEAD and re-pin every lane; the roster reads the record.
2. NIT-2 reads the three pre-existing ISC004 findings in `EVIDENCE_LIMITATIONS` as "left unfixed to preserve synthetic candidate byte pins". Parenthesizing implicit concatenations does not change the strings, so the pins were not the reason; they were left because they pre-exist on `4c802e9b` and lie outside the slice (the Lead fixed the five ISC004 in the NEW tuple). Disposition unchanged: no change requested.

## NITs
| # | Finding | Disposition |
|---|---|---|
| NIT-1 | `PRODUCTION_MODE_UNAVAILABLE = "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"` prose stale for the real kind; kept because the carried fence pins it and production admission is genuinely still unavailable (Q3) | already disclosed in the Lead record §3; no change now; wording follow-up bundled with correction 1 above |
| NIT-2 | pre-existing ISC004 ×3 in the synthetic limitations tuple | pre-existing on `4c802e9b`; outside the slice; no change |

## Standing
Counted Gemini read exists for `9ef072a8`. The candidate stays UNMERGED and UNACCEPTED: the Lead never accepts its own code; T1 roster = Wednesday optional lane 8 (`OPUS_QUEUE_20260916/P012INTAKE`, re-pinned) or the Friday Sol lane generated from it. Production admission is not granted (`OD-20260914-P012-ADMISSION-Q3` "Wait").

Recorded by Claude Opus 5 Lead (session 6, `4a8233`).
