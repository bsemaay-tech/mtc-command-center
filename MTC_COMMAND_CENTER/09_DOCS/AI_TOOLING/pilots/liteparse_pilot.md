# Pilot — LiteParse (local PDF/layout parser)

**Date:** 2026-06-21 · **By:** Claude Opus 4.8 · **Verdict:** ⏸️ DEFER — do **not** promote/commit yet.
Overlaps already-kept MarkItDown on text PDFs; its real differentiator (scanned-PDF OCR +
spatial layout) cannot be proven because the repo has **0 PDFs**, and that path needs heavy
system installs (Tesseract / LibreOffice / ImageMagick). Re-evaluate when a real — especially
scanned — strategy PDF lands in `00_INBOX/USER_INTAKE/`.

## What / install
`run-llama/liteparse` — Apache-2.0, local Rust-backed PDF/Office/image parser with spatial text
extraction; output JSON / text / Markdown. PyPI: `liteparse`. No Python runtime deps, but:
- Office (xlsx/docx) → needs **LibreOffice**; images → **ImageMagick**; scanned PDFs → **Tesseract**.
- Python **>=3.10**; system Python is **3.14 (unsupported)** → used `py -3.13` (3.13.14).
- Ephemeral venv (non-repo, no git noise): `C:\tmp\mtc_liteparse_venv`.
- Install: `py -3.13 -m venv C:\tmp\mtc_liteparse_venv` then
  `…/Scripts/python.exe -m pip install liteparse fpdf2`.
- **Windows wheel note:** pip backtracked **2.1.1 → 2.0.0** (no win/py3.13 wheel for 2.1.1).
  2.0.0 imports + parses fine. Pin `liteparse==2.0.0` on this stack if ever promoted.
- No CLI (`-m liteparse` fails) — Python API only:
  `LiteParse(output_format="markdown", ocr_enabled=False).parse(path).text`.
  Default `ocr_enabled` auto-triggers OCR and **crashes without Tesseract** — must pass
  `ocr_enabled=False` for text PDFs.

## Real test — A/B vs MarkItDown
No real MTC PDF exists (`find . -iname "*.pdf"` → 0). Used a **synthetic** table PDF
(`C:\tmp\liteparse_synth.pdf`, fpdf2: title + 5-col parity-case table) as a mechanics-only A/B.

| | LiteParse 2.0.0 | MarkItDown 0.1.6 |
|---|---|---|
| Table reconstructed | ✅ `\| Case \| Symbol \| … \|` | ✅ (aligned) |
| Output quality (text PDF) | clean | clean — **equivalent** |
| Extra metadata | per-item x/y/font/confidence (`text_items`) | none |
| Out-of-box on text PDF | needs `ocr_enabled=False` or crashes | works as-is |
| System deps | Tesseract/LibreOffice/ImageMagick for OCR/Office/img | none for PDF/Office/xlsx core |
| CLI | none (API only) | `python -m markitdown <in>` |

**Outcome:** on a text PDF the two are equivalent. LiteParse only pulls ahead on **scanned/image
PDFs** (OCR + spatial layout) — a case the repo has zero of, and which requires system installs.

## §6 checklist
- [x] repo maintained — yes (run-llama, v2.1.1, active)
- [x] license — Apache-2.0 ✅
- [~] Windows compatible — yes for **2.0.0**; 2.1.1 has no win/py3.13 wheel (pin 2.0.0)
- [x] Python req — >=3.10 (used py3.13)
- [x] local-only — yes (optional HTTP OCR server is opt-in)
- [x] secrets/privacy — none; fully local (this is its only edge over a cloud parser)
- [x] git noise — venv in `C:\tmp` (ephemeral); no repo artifacts written
- [x] modifies files — read-only conversion
- [!] **overlaps existing (§2)** — YES: MarkItDown (kept) + built-in `pdf` skill. Equal on text PDF. **Not justified** until a scanned-PDF need appears.
- [x] denylist — no pine/parity/MTC_V2/schema touch

## Acceptance — NOT MET (blocked, not failed)
Gate = "better tables/layout on a **real PDF**." No real PDF exists → gate cannot be evaluated.
On the only testable input (synthetic text PDF) it ties MarkItDown. Per §6, a tool that
"overlaps existing" is **not promoted** without an explicit Barış override.

## Decision
- **DEFER.** Keep MarkItDown as the single ingestion path for now.
- Ephemeral venv left at `C:\tmp\mtc_liteparse_venv` (safe to delete; rebuild from steps above).
- **Re-open when:** a real scanned/image strategy PDF lands → then A/B LiteParse(+Tesseract) vs
  MarkItDown on that real doc; promote only if it visibly wins on tables/layout.
