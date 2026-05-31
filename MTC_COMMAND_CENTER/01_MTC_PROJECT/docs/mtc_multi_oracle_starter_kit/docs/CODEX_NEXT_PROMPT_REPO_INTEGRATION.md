# Codex Next Prompt — Repo Integration Only

```text
RAPOR BAŞLADI
Model Numarası: CODEX-MTC-MULTI-ORACLE-INTEGRATION-ONLY

You are working inside the user's MTC v2 / tradingview-lab repo.

USER CONTEXT
- User does not know coding.
- A starter kit has already been prepared outside the repo.
- Your job is not to redesign the architecture.
- Your job is to integrate the starter kit into the real repo and connect real paths/entrypoints.
- Ask no questions.
- Do not delete existing files.
- Make backups before modifying existing files.
- Prefer additive changes.
- No live trading.
- No exchange API keys.
- No real orders.
- Offline parity/backtest only.

INPUT
The starter kit folder is named:
mtc_multi_oracle_starter_kit

TASK 1 — COPY STARTER KIT
Copy these folders/files into the repo if they do not already exist:
- docs/
- tools/mtc_runtime_compat_scan.py
- parity_oracles/
- examples/
- reports/
- tests/

If target files already exist, do not overwrite blindly. Create backups or merge carefully.

TASK 2 — REPO INVENTORY
Create:
docs/MULTI_ORACLE_PARITY_REPO_INVENTORY.md

Run:
python --version
pip --version
node --version
npm --version
git status --short

Search for:
MASTER_TEMPLATE_CORE.pine
MTC_V2
strategy("MTC
request.security
strategy.entry
strategy.exit
parity
backtest
optimization

Document:
- real Pine file path
- real Python engine entrypoint if found
- real data folders
- real TradingView export files
- existing test commands

TASK 3 — RUN MTC SCANNER
Run:
python tools/mtc_runtime_compat_scan.py --pine <REAL_MTC_PINE_FILE> --out-dir reports

Expected outputs:
reports/mtc_runtime_compat_scan.md
reports/mtc_runtime_compat_scan.json

TASK 4 — CONNECT PYTHON ENGINE RUNNER
Edit:
parity_oracles/engines/python_engine_runner.py

Goal:
- If an existing Python MTC engine CLI exists, wrap it.
- If no clear CLI exists, document exactly why.
- Do not invent false commands.
- Generate a stub normalized output only if clearly marked as synthetic/stub.

TASK 5 — CONNECT PINETS RUNNER
Edit:
parity_oracles/engines/pinets_runner.py

Goal:
- Detect whether pinets-cli is available.
- Document exact command/version.
- If PineTS currently works in user repo, wire the known command.
- If full strategy cannot run, keep PineTS as signal/indicator oracle only.
- Create or document MTC signal-export adapter requirement.

TASK 6 — PYNECORE POC
Create isolated venv under:
experiments/pynecore_oracle_poc/

Try:
python -m venv .venv-pynecore
.venv-pynecore\Scripts\python -m pip install --upgrade pip
.venv-pynecore\Scripts\pip install "pynesys-pynecore[cli,providers]"

Run or create:
scripts/ma_cross_strategy.py
scripts/security_mtf_poc.py

Save result:
experiments/pynecore_oracle_poc/reports/pynecore_poc_result.md

If install/run fails, save full error and continue.

TASK 7 — TEST COMPARATOR
Run synthetic comparator from starter kit:
python parity_oracles/compare/parity_compare.py --baseline-dir examples/synthetic_outputs/baseline_python --candidate-dir examples/synthetic_outputs/candidate_pinets --level L2 --out-md reports/synthetic_L2_compare.md --out-json reports/synthetic_L2_compare.json

Then, if real normalized outputs exist, run real comparison.

TASK 8 — FINAL REPORT
Create:
reports/MULTI_ORACLE_PARITY_IMPLEMENTATION_REPORT.md

Include:
- Files copied
- Files modified
- Commands run
- Scanner result summary
- PineTS availability
- Python engine availability
- PyneCore POC result
- Comparator test result
- What can be compared today
- What cannot be compared today
- Recommended next Codex prompt

FINAL VERDICT:
### VERDICT: APPROVED_FOR_POC
or
### VERDICT: CHANGES_NEEDED

Use APPROVED_FOR_POC if:
- starter kit copied
- scanner ran
- comparator synthetic test passed
- at least Python or PineTS runner status is documented

Use CHANGES_NEEDED otherwise.

RAPOR BİTTİ
```
