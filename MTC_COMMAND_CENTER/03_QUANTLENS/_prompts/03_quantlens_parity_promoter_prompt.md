# QuantLens Parity Promoter Prompt

Bu prompt, `BACKTEST_PASSED` veya `BACKTEST_PROMISING` adayları parity-first hazırlık paketine taşımak için kullanılır.

## Görev

Candidate metadata ve backtest sonuçlarını oku. Feature type belirle, feature contract hazırla, Python reference logic dokümanı yaz, Pine integration planı ve PineTS parity test planı hazırla.

## Feature Type

Şunlardan birini veya birkaçını açık seç:

- producer
- entry_gate
- guard
- confirmation
- exit_rule
- SL/TP
- trailing/BE
- sizing

## Kesin Kurallar

- `01_PINE/MTC_V2.pine` değiştirme.
- Production Python runner değiştirme.
- Kod yazma; bu aşama plan ve contract üretir.
- Repaint/lookahead tekrar kontrol edilir.
- PineTS lifecycle row yoksa lifecycle parity claim yapılmaz.
- TradingView export final release audit olarak kalır.

## Output

```text
06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\<CandidateID>\
├─ 00_backtest_summary.md
├─ 01_feature_contract.yaml
├─ 02_python_reference_logic.md
├─ 03_pine_integration_plan.md
├─ 04_parity_test_plan.md
├─ 05_expected_risks.md
└─ 06_go_no_go.md
```

Parity riski çözülemiyorsa registry status `PARITY_BLOCKED`.
Hazırlık başarılıysa registry status `READY_FOR_PINE_INTEGRATION`.
