# LEAD_ADJUDICATION — P026_DELTA_GEMINI (gemini-3.8-flash-high DELTA review of WP-P0-26 slice 3, `8d4056c5..d81b07f6`) — 2026-09-15 11:58Z

| Attempt | Window | Outcome |
|---|---|---|
| 1 | 11:35:03Z – 11:43:57Z (534 s wall / 522 s model) | **VOIDED** by the wrapper: CLI envelope `status: ERROR`, `API error (attempt 1): UNAVAILABLE (code 503): No capacity available for model gemini-3.8-flash-high` after a COMPLETE report had streamed (14 514 chars, JSON verdict PASS, sentinel present; recovered from `%TEMP%\gemini_wrapper_failures\20260915T114357Z_40428.stdout.jsonl` as `RECOVERED_ENVELOPE.json` / `RECOVERED_RESPONSE_UTF8.md`; native reads 25/25, none outside — `NATIVE_READ_AUDIT_attempt1.json`). Kept SUPPLEMENTAL; archived `FAILED_ATTEMPTS/attempt1/`. The re-run prompt was annotated only with "a first attempt was voided by a 503; its content is not shown to you; review afresh" — the verdict was not disclosed. |
| 2 | 11:46:18Z – 11:54:49Z (511 s wall / 498 s model) | **COUNTED**: `exit=0 actual_exit=0`, `status: SUCCESS`, conversation `e1aca029-b881-4bad-ac54-49ddfe331401`, sentinel present; usage input 647 093 / output 22 799 / thinking 14 813; response 14 834 chars sha256 `9ab9db9a…`. Native reads 25, **0 outside the packet**, 0 failures; every REQUIRED file complete (`NATIVE_READ_AUDIT.json`). |

## Counted verdict: PASS — `closed: [F-01, F-02, F-03]`, `not_refused: []`, `findings: []`
- (a) F-01 CLOSED: the new rule quoted from `restore_d81b07f6.py:71-89` (exactly one `run_end`; status ok; `errors == []`; `files` equal to the marker's); F-02 CLOSED (`backup_d81b07f6.py:220-232`: evidence before `run_end`; failed write → error + partial; dry-run untouched; record shapes and CLI unchanged; a crash between the evidence write and the `run_end` append leaves marker + per-run manifest but no `run_end` → refused by F-01 with rc 3); F-03 CLOSED (docstring accurate; every restore path, including the adapter at its two `run_restore` calls, funnels through `verify_completion_evidence`).
- (b) Attack shape (e) variants — all **REFUSED** with line citations the Lead re-grepped: interrupted (`:75-76`), crashed (`:71-72`), duplicate `run_end` (`:71-72`), file-count mismatch (`:87-88`), `errors` absent (`None != []`) and `errors: 0` (`0 != []`) (`:75-76`), foreign `run_end` (`:71-72`), malformed line (refused at the `run_end` count or at the per-run/global record comparison, or reported as a malformed-line error).
- Tests: the new fence forges the pair the way an attacker would (digest-bound, matching global records, `readback: all_match`), covers both arms in both modes (4 subtests), RED evidence consistent (3 failures + the reworked partial-manifest test's error on the slice-2 modules); the reworked partial-manifest test proves the zero-file fence through a genuinely tool-closed empty run.
- Adapter checker change: correct consequence of F-01; the adapter's own envelope fence still asserted. Scope: five files inside the two rulings' ceiling; nothing added; no new primitive; record shapes unchanged. Report honesty: 39 / 45 / RED 3F+1E reproduced from the output tails.
- NOT VERIFIED (Gemini, kept): no execution; adapter/checker only via the diff and the earlier excerpts.

Comparison with the voided attempt 1: same verdict and the same closure table (the voided report had reached the same conclusions before the 503).

## Roster state for WP-P0-26 candidate `d81b07f6`
Gemini: detection of `8d4056c5` REQUEST_CHANGES → delta of `d81b07f6` PASS (counted). Lead: author, verifier, not acceptor. Exact Opus: Wednesday lane 4 (pinned `d81b07f6`). Exact Sol: Sep 19. Nothing is accepted by this file.

Recorded by Claude Opus 5 Lead (743291).
