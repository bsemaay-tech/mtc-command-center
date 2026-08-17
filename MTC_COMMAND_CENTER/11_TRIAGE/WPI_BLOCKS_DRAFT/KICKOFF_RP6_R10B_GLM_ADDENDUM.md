# ADDENDUM — RP6 round 10b, GLM dispatch 2026-08-11 13:50

Read and execute `KICKOFF_RP6_REPAIR_R10.md` (same directory) with these binding additions
from the Lead. You are GLM-5.2 via the Z.AI route, IMPLEMENTER. Codex remains auditor of
record.

1. **A round-10a PARTIAL exists and is your starting point.** Claude Pro died on its weekly
   cap mid-round-10. Partial bytes: `WPI_BLOCKS_DRAFT/RP6-P0.sh` SHA-256
   `a090ae736cbecd9973e8ae948b052504b21cbe8b61602f4b5ac592394fad0617`, 107252 B, commit
   `da78d99c` (current working tree). Context: `RP6_R10A_LEAD_NOTE_2026-08-11.md`. The
   partial is syntactically clean and the full fence set passes, BUT no report exists and
   F1–F4 are NOT confirmed closed.
2. **Your job: confirm or complete, never assume.** For each of F1–F4: verify against the
   partial bytes with executed evidence (never credit a comment or an existing diff as
   proof). Where the repair is present and provable, record the proof. Where absent or
   broken, repair from the partial (not from round 9) and prove it.
3. **F1 discipline:** run every published command in `SELF_QA_RP6.md` VERBATIM from a clean
   shell AND as the Lead-style extraction; any disagreement between the two forms is itself
   a finding to report. The published `R9_GRAMMAR` command must produce
   `R9_GRAMMAR_SUMMARY` in its real recorded output.
4. **Deliverables:** repaired/confirmed `RP6-P0.sh` + the missing round-10 report
   `RP6_R10_REPORT_2026-08-11.md` (per-finding dispositions F1–F4, including what the
   partial already contained vs what you added) + updated `SELF_QA_RP6.md` entries. If your
   session cannot execute, mark exactly those entries `PENDING-LEAD-EXECUTION`; never
   fabricate transcripts.
5. LF only, zero CR bytes (`tr -cd '\r' < f | wc -c` = 0). No commit — the Lead commits.
   Never `git checkout` a block file; use `git cat-file blob <sha>:<path>`.
