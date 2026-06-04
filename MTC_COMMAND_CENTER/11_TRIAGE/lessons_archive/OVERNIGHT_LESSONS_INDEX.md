# Overnight Lessons — Archive Index

> **Living runbook (her gece zorunlu pre-read):**
> [`11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`](../BACKTEST_OPTIMIZATION_RUNBOOK.md)
>
> Bu klasör ham gözlem arşivi. Runbook konsolide bilgi.

## Arşiv

| Tarih | Dosya | Süre | Ana ders (1 satır) |
|---|---|---|---|
| 2026-04-27 | `01_MTC_PROJECT/docs/optimization/OPTIMIZATION_LESSONS_LEARNED_20260427.md` | — | Worker scaling benchmark, MTC V2 için 16 sabit |
| 2026-05-01 | `01_MTC_PROJECT/reports/optimization/12h_backtesting_session/POST_RESUME_RESULT_AND_LESSONS_20260501.md` | 12h | Resume registry dedup, idempotent output dir |
| 2026-05-XX | `01_MTC_PROJECT/reports/optimization/worker_scaling_benchmark/WORKER_BENCHMARK_LESSONS_UPDATE_REPORT.md` | — | Thread pinning OMP/MKL/OPENBLAS/NUMEXPR |
| 2026-05-31 | [`OVERNIGHT_LESSONS_2026-05-31.md`](OVERNIGHT_LESSONS_2026-05-31.md) | 8h | Estimation 30× yanlış, DSR crypto kalibrasyon, cross-symbol agg |
| 2026-06-01 | [`OVERNIGHT_LESSONS_2026-06-01.md`](OVERNIGHT_LESSONS_2026-06-01.md) | 5.5h kayıp | OUTPUT_DIR legacy crash, wakeup zinciri kopması |
| 2026-06-03 | [`OVERNIGHT_LESSONS_2026-06-03.md`](OVERNIGHT_LESSONS_2026-06-03.md) | 11h / 21 iter | İlk sıfır-crash gece; DSR search-space inflation (confirmation grid gerek); morning generator legacy path (A16) |
| 2026-06-04 | [`OVERNIGHT_LESSONS_2026-06-04.md`](OVERNIGHT_LESSONS_2026-06-04.md) | 11.5h / 20 iter | 2. sıfır-crash gece (3.44M eval); morning report down-market sayım hatası (A18, 78≠8); gece-sonu konvansiyonu atlandı (G5); Codex çalıştırdı |

## Convention

Her gece sonu:
1. Yeni `OVERNIGHT_LESSONS_YYYY-MM-DD.md` bu klasöre eklenir
2. Bu index güncellenir (yeni satır)
3. Yeni anti-pattern → `BACKTEST_OPTIMIZATION_RUNBOOK.md` bölüm 8 tablosuna merge
4. Yeni guideline → runbook ilgili bölümüne merge
5. Runbook CHANGELOG'a 1 satır

Dated dosyalar **silinmez** — provenance + audit trail.
