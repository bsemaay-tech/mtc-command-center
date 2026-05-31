# 11_TRIAGE — Manual backfill triage

Workspace for finding and supplying verified YouTube URLs and transcripts to
candidates that the read-only audit marks as REJECTED, wiki-only, or
missing coverage. Read-only philosophy is preserved: nothing here touches
MTC_v2 core, Pine, or live trading.

## Quick workflow

1. **Generate worklist + per-strategy .md notes**:
   ```
   python 11_TRIAGE/generate_worklist.py
   ```
   Produces:
   - `11_TRIAGE/<YYYY-MM-DD>_rejected_worklist.xlsx` — first column is the
     stable `stg_code` (Stg001..StgNNN), second column is the matching
     `md_file`. Auto-filter + frozen header on.
   - `11_TRIAGE/strategies/stgNNN.md` — one file per candidate. Header line
     plus `Video name:` and `Video Url:` lines (pre-filled when known) and
     an embedded transcript under `## Transcript` (or a link if oversized).
   - `11_TRIAGE/strategies/_stg_code_map.json` — persisted
     `candidate_id -> Stg###` map. Re-runs keep the same code for the same
     candidate; existing .md files are never overwritten.

2. **Triage offline** — open the xlsx, sort by `stg_code`, fill in any blank
   `Video Url:` lines in `strategies/stgNNN.md` with verified YouTube links.
   Do not invent URLs.

3. **Ingest** — when a batch is ready, ask Claude (CLI) to ingest
   `11_TRIAGE/strategies/`. Claude will:
   - Append rows with newly filled `Video Url:` to
     `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/12_LLM_WIKI/manual_backfill/<date>/quantlens_source_map.csv`
     (auto-picked up by the audit reader's `12_LLM_WIKI/**/quantlens_source_map.csv` glob).
   - Copy `## Transcript` bodies to
     `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/00_INBOX_REPORTS/Transcrips/<title>.md`
     when the .md adds transcript content the canonical path didn't already have.

4. **Re-audit + re-generate**:
   ```
   python -m mcc_readonly audit
   python 11_TRIAGE/generate_worklist.py
   ```
   The worklist shrinks as candidates gain coverage; resolved rows drop off.

## Notes

- Coverage classifications in the xlsx:
  - `NO_URL_NO_TRANSCRIPT` — highest priority, fully blocked.
  - `HAS_URL_NO_TRANSCRIPT` — URL exists, transcript needed.
  - `HAS_TRANSCRIPT_NO_URL` — transcript exists, URL needed.
  - `HAS_BOTH` — both present but candidate is still REJECTED for a
    different reason (read `blocked_reason` and `recommended_next_step`).
- The QuantLens lab is git-ignored, so URL backfills there persist locally
  but do not enter MCC commits.
- Generated xlsx files in this folder are reproducible — do not commit them.
