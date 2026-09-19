# LEAD_ADJUDICATION - exact-Sol T0 read of WP-P0-26 `2e03a669` (Codex PRO `free`, gpt-5.6-sol xhigh; Sat 2026-09-19 13:57-14:20 UTC+3; adjudicated 14:2x)

**Verdict as written:** **BLOCK** - but read the report: *"Spec axis: 0 REQUIRED, 1 NIT. Standards axis: 0 hard violations, 0 smell findings. The audit is nevertheless blocked by the unavailable mandated Ruff module in the pinned interpreter."* and *"No REQUIRED code finding."* The reviewer reproduced every Lead count (OPS-A 39 OK; pre-fix suite 5F+4E; adapter 45 OK; slice-1 adapter 6F+3E; reserved-ID two subtest failures; hand-made evidence 3F+1E; NIT-1 mutants one failure each; Python 3.12.12), found the original defect RED on `fcac0ac6` and GREEN now, and ran Ruff 0.16.4 from the standalone `C:\tmp\wp_p0_04_tooling_20260825\Scripts\ruff.exe` - it passed. 246 lines, 23 min, exit 0; worktree clean after the lane.

**Why BLOCK:** the review brief asserts Ruff lives in the pinned venv and mandates `python -m ruff` there; that assertion is FALSE (the venv has no `ruff` module - the reviewer said so and the Lead confirms), and the brief's contract says an unrunnable mandated command = BLOCK. So the BLOCK is **procedural, caused by a brief defect**, not by the candidate.

**Lead disposition:**
- The mandated Ruff check is satisfied twice: the reviewer's standalone 0.16.4 pass, and the Lead's `uvx ruff@0.16.8` per-rule parity at `2e03a669` vs `e114ed31` (`P026_NIT_SLICE_20260918/LEAD_RUFF_PARITY_2e03a669.txt`: opsa_common TRY004x1 / restore I001+RUF100 / backup SIM102+I001+RUF100+RUF059 / test_opsa RUF100x5+SIM117+I001 - identical HEAD vs base).
- A BLOCK is not an accepting verdict and the Lead does not rewrite verdicts. **The Sol lane is re-run** with the corrected brief (addendum 2026-09-19 14:2x: Ruff not in the venv; standalone/uvx or the Lead record; missing linter is not a BLOCK reason) as soon as the Pro account is free (after the P021S1 → P030 → DD06 lanes, or on `secondary` after 18:47). The same addendum was added to the P030, DD06 and P021S1 briefs and to the Sol brief template so the remaining lanes do not repeat it.
- **NIT-1** (`restore.py:113-117` "every claim the marker makes about itself is checked" overstates: `bytes`/`size`-type informational marker fields are not validated; no fail-open) - real, carried to the P0-26 follow-up slice with the fifth-read NITs 1/2/3/5 and the evidence-doc note (`P26-EVID B`).

**Standing:** P0-26 `2e03a669` = exact-Opus PASS-WITH-NITS (on `505af399`, code blobs identical) + Gemini PASS + Lead reproduction + Sol content accepting but verdict BLOCK (procedural) → NOT merge-ready until the Sol re-read returns PASS/PASS-WITH-NITS. The Lead never accepts its own code.

Recorded by Claude Fable 5.1 Lead (session 7, `18c1b8`).
