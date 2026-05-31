# QuantLens Python Experiment Runner Prompt

Bu prompt, `READY_FOR_PYTHON_PROTOTYPE` statüsündeki adayları izole Python prototype ve bounded validation sürecine sokmak için kullanılır.

## Görev

Registry'den uygun adayı seç, candidate metadata ve experiment planını oku, eksik kritik bilgi varsa `NEEDS_MORE_INFO` yap. Üretim runner davranışını bozmadan izole prototype/adapter planla ve bounded validation sonuçlarını kaydet.

## Kesin Kurallar

- `01_PINE/MTC_V2.pine` değiştirme.
- Production engine veya runner davranışını değiştirme.
- Önce izole prototype/adapter yaklaşımı kullan.
- Büyük exhaustive grid ilk adım olamaz.
- Veri kullanımı manifest-first olmalı; dataset_id ve source_type raporlanmalı.
- Commission/slippage varsayımları açık yazılmalı.

## Aday Seçimi

- Kullanıcı `candidate_id` verdiyse onu seç.
- Vermezse registry'deki ilk `READY_FOR_PYTHON_PROTOTYPE` adayı seç.
- Eksik strateji kuralı, eksik risk bilgisi veya veri yoksa status `NEEDS_MORE_INFO`.

## Validation Beklentisi

- Bounded validation yap.
- Multi-symbol öner: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT ve mevcut data bundle'da bulunan uygun semboller.
- Walk-forward, OOS, robustness ve sensitivity kontrolleri yap.
- Net profit tek başına pass kriteri değildir.
- Trade count düşükse sonuç güvenilmezdir.

## Output

Sonuçları şuraya kaydet:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\<CandidateID>\
├─ backtest_config.yaml
├─ symbol_results.csv
├─ walk_forward_results.csv
├─ robustness_summary.md
├─ pass_fail_decision.md
└─ next_action.md
```

Registry status değerlerinden birini kullan:

- `BACKTEST_FAILED`
- `BACKTEST_PROMISING`
- `BACKTEST_PASSED`
- `NEEDS_MORE_INFO`
