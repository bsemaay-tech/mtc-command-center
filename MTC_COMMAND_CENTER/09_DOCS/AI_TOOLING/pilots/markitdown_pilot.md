# Pilot — MarkItDown (document → Markdown ingestion)

**Date:** 2026-06-21 · **By:** Claude Opus 4.8 · **Verdict:** ✅ KEEP for XLSX/Office batch ingestion; PDF value deferred (no PDFs in repo yet).

> **PROMOTED 2026-06-21 (Barış-approved item 1).** No longer a `C:\tmp` pilot. Permanent,
> reproducible install:
> - **Wrapper (committed):** `03_QUANTLENS/tools/markitdown_ingest.py` — self-bootstraps the
>   venv, converts a file/dir (default `00_INBOX/USER_INTAKE`) → `.md`. Dry-run by default;
>   `--apply` writes; `--out <dir>` to redirect; `--bootstrap` to (re)build the venv.
> - **Venv (git-ignored):** `03_QUANTLENS/tools/.venvs/markitdown/` (Python 3.13, markitdown
>   0.1.6). `.gitignore` entry: `MTC_COMMAND_CENTER/03_QUANTLENS/tools/.venvs/`. A fresh clone
>   rebuilds it automatically on first `--apply` (needs `py -3.13`).
> - **Composes with** `route_user_intake.py` (which only *moves* files): convert first, then
>   route, or convert in place — the wrapper never edits the router and never deletes sources.
> - Verified end-to-end: dry-run + `--apply --out C:/tmp/mtc_md_test` on the setup-guide XLSX
>   → 69 KB clean `.md`; `git check-ignore` confirms the venv is not tracked.

## What / install
Microsoft, MIT license. Converts PDF/DOCX/PPTX/XLSX/images → clean LLM-friendly Markdown. Local, no API key.
- Python **3.10–3.13** only. System Python is **3.14 (unsupported)** → used `py -3.13` (3.13.14).
- Isolated venv: `C:\tmp\mtc_markitdown_venv` (non-repo → no git noise during pilot).
- Install: `py -3.13 -m venv …` then `pip install "markitdown[pdf,docx,pptx,xlsx]"`. Installed **markitdown 0.1.6** + deps (pdfplumber, python-pptx, openpyxl, mammoth, onnxruntime — all 3.13 wheels OK).
- Run: `…/mtc_markitdown_venv/Scripts/python.exe -m markitdown <in> -o <out.md>`.

## Real test
Input: `01_MTC_PROJECT/05_PARITY/CASE_SETUP_GUIDE_L4_120_baseline.xlsx` (multi-row setup guide).
Output: `C:\tmp\markitdown_test_setupguide.md` (read-only conversion; source untouched).
Result: README sheet rendered as a clean Markdown table; all baseline settings, run order, audit notes captured and readable. Only noise = empty cells shown as `NaN` rows (cosmetic, strippable).

## Finding: no PDFs exist in the repo
`find . -iname "*.pdf"` → 0 hits. MTC docs are markdown/XLSX today. So MarkItDown's **immediate** value = XLSX/Office (backtest + parity exports); its **PDF/YouTube** value is future-facing (intake of external strategy docs/transcripts).

## Built-in overlap (honest)
Claude Code client has `pdf`/`docx`/`xlsx` skills for one-off conversions. MarkItDown's differentiator = **scriptable + batchable + wireable** into the existing intake pipeline (`03_QUANTLENS/tools/route_user_intake.py`, `00_INBOX/USER_INTAKE/`, `YT_TRANSCRIPT_COLLECTOR/`). For a single doc, the built-in skill is enough; for bulk/automated intake, MarkItDown wins.

## Acceptance — PASS (conditional)
XLSX→md is clean and scriptable. Keep for batch Office ingestion. Re-test the PDF path when a real strategy PDF lands in `00_INBOX/USER_INTAKE/`.

## Caveats / footprint
- **(Historical — resolved on promotion.)** During the pilot the venv lived in `C:\tmp`. Now
  permanent + git-ignored at `03_QUANTLENS/tools/.venvs/markitdown` (see PROMOTED block above).
- Requires the 3.13 interpreter — do **not** rely on the system 3.14.
- `NaN` empty-cell rows: add a post-filter if feeding to a token-sensitive model.

## Next (optional, approval-gated)
- Wire a thin wrapper so `route_user_intake.py` can call MarkItDown for non-md/non-txt drops.
- DONE: permanent venv location + `.gitignore` entry settled at promotion.
