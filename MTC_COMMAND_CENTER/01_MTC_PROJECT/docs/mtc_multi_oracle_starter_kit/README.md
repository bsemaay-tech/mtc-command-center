# MTC v2 Multi-Oracle Parity Starter Kit

Bu paket, Codex kredisi tüketmeden hazırlanabilecek **repo-bağımsız** altyapıyı içerir.

Amaç:

- PineTS’i bırakmak değil, **PineTS’i signal/indicator oracle** olarak doğrulamak.
- Mevcut Python parity/backtest engine’i ana motor olarak tutmak.
- PyneCore’u deneysel strategy execution oracle olarak hazırlamak.
- vectorbt’i hızlı signal-array / parameter sweep doğrulayıcı olarak konumlandırmak.
- TradingView export geldiğinde final referans olarak karşılaştırmaya dahil etmek.

## Bu pakette neler var?

```text
docs/
  WHAT_I_CAN_DO_VS_CODEX.md
  AI_FREE_PINETS_ALTERNATIVES_DECISION_MATRIX.md
  FREE_ORACLE_LICENSE_NOTES.md
  MULTI_ORACLE_PARITY_RUNBOOK.md
  CODEX_NEXT_PROMPT_REPO_INTEGRATION.md

tools/
  mtc_runtime_compat_scan.py

parity_oracles/
  schema/
    parity_case.schema.json
    parity_result.schema.json
    parity_manifest.schema.json
  normalizers/
    common.py
    normalize_pinets.py
    normalize_python_engine.py
    normalize_pynecore.py
    normalize_vectorbt.py
    normalize_tradingview_export.py
  compare/
    parity_compare.py
  engines/
    pinets_runner.py
    python_engine_runner.py
    pynecore_runner.py
    vectorbt_runner.py
    backtestingpy_runner.py
  run_multi_oracle_case.py

examples/
  synthetic_case/BTCUSDT_15m_CORE_001.json
  synthetic_outputs/baseline_python/
  synthetic_outputs/candidate_pinets/

tests/
  test_synthetic_compare.py
```

## Hızlı test

Windows PowerShell:

```powershell
cd mtc_multi_oracle_starter_kit

python tools/mtc_runtime_compat_scan.py --pine examples/synthetic_case/example_mtc_strategy.pine --out-dir reports

python parity_oracles/compare/parity_compare.py `
  --baseline-dir examples/synthetic_outputs/baseline_python `
  --candidate-dir examples/synthetic_outputs/candidate_pinets `
  --level L2 `
  --out-md reports/synthetic_L2_compare.md `
  --out-json reports/synthetic_L2_compare.json
```

## Codex’e ne verilecek?

`docs/CODEX_NEXT_PROMPT_REPO_INTEGRATION.md` dosyasındaki promptu ver.

Bu prompt artık Codex’e devasa sıfırdan sistem kurdurmaz. Sadece:
1. Bu paketi senin gerçek repo’ya kopyalar.
2. Mevcut Python engine entrypoint’ini bulur.
3. PineTS CLI gerçek komutunu bağlar.
4. PyneCore POC’u lokal dener.
5. Gerçek MTC dosyası üzerinde scanner/comparator çalıştırır.
