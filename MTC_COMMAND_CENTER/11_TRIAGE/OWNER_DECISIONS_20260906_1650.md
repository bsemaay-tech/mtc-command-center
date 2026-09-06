# Owner decision 2026-09-06 16:5x — GEMINI_FETCH_HEAD_TOLERANCE

Question: `C:	mp\OWNER_QUESTION_GEMINI_FETCH_HEAD_20260906_1620.md`. Owner answer (chat, 16:5x): **A**.

OD-20260906-8 `GEMINI_FETCH_HEAD_TOLERANCE = A`: add `Changed:.git\FETCH_HEAD` to the transient-event tolerance pattern of the owner's
Gemini read-only helper `AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1`, alongside the 2026-08-30 tolerance (`.impeccable`, `index.lock`).
Every other `.git` event (objects, refs, packed-refs, Deleted/Created FETCH_HEAD) and every repository-content event still fails closed.

Applied 16:5x by the Lead: helper SHA-256 846e560c… → 6434f7fe…; verified parse OK and match semantics in PowerShell and Python
(`C:	mp\PRO_LANES_20260906ix_gemini_helper_fetch_head.py`); hash re-pinned in `Invoke-GeminiPacketReview.ps1` and
`Invoke-S16GeminiLane.ps1`. To be recorded in the route ledger at the next between-waves git window.
