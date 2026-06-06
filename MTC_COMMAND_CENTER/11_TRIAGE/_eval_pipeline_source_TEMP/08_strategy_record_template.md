# Final Strategy Record Template

```yaml
strategy_id:
strategy_name:
source_type:
source_url:
market:
timeframe:
direction:
  long:
  short:
strategy_type:
  entry_only:
  full_strategy:
  mtc_exit_delegated:

gate_1_candidate_intake:
  score:
  result:
  notes:

gate_1b_mtc_feasibility:
  score:
  result:
  notes:

repaint_verification:
  preliminary_status:
  verified_status:
  notes:

gate_2_backtest_evidence:
  score:
  result:
  test_period:
  trade_count:
  benchmark_result:
  notes:

gate_3_mtc_production_readiness:
  score:
  result:
  notes:

final_status:
decision:
next_action:
```

---

# Kullanım Notu

Bu şablon her strateji adayı için ayrı kayıt olarak kullanılabilir.

Önerilen dosya adı formatı:

```text
strategy_record_<strategy_id>.yaml
```

veya markdown içinde saklanacaksa:

```text
strategy_record_<strategy_id>.md
```
