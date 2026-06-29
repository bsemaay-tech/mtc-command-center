# 08 — Backtest Launch (Gate 0 + Gate 6 = HARD)

> **Bu prompt'u kullan:** HER backtest. Üç senaryo da aynı gate'ler:
> - **In-day single strategy** ("BTC 1h'de bu RSI stratejisini test et")
> - **Sprint** (1-3 saat, mevcut grid sweep)
> - **Overnight** (6-12 saat, full research sweep)
>
> Süre değişir, kalite eşiği değişmez. 5dk run dahi 4-gate (rolling WF + bootstrap+BH-FDR + DSR + multi-window) + buy&hold karşılaştırması olmadan promotable değil.
>
> **MTC V2 BIG_OVERNIGHT için:** `01_MTC_PROJECT/docs/optimization/BIG_OVERNIGHT_OPTIMIZATION_RUNBOOK.md`'a git, oradan devam et. Aşağıdaki adımlar QuantLens research içindir.

## Gate 0 — ZORUNLU PRE-READ (iki dosya)

1. `AGENTS.md` (repo kökü)
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
4. **`MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`** ← CANONICAL kurallar (4 gate, classification, promotion, antigravity, morning report)
5. **`MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`** ← operasyonel yürütme (tool komutları, worker, monitor)
6. `MTC_COMMAND_CENTER/11_TRIAGE/lessons_archive/` en yeni 1 dosya

Atlama YASAK. Skip yaparsan A1-A15 anti-pattern'lerinden birini tekrarlarsın.

## Gate 1 — Scope

- **Senaryo:** in-day single / sprint / overnight?
- Kapsam ne? (1 strateji × 1 sembol / mevcut grid sweep / yeni transcript triage)
- Worker sayısı (runbook §5 tablo: in-day 4-8, sprint 16-20, overnight 16, parity gece 16)
- Süre bütçesi (`--time-budget-minutes` / loop `DEADLINE`)
- OUTPUT_DIR (CLEAN repo default — env override gerek mi)

### Gate 1.5 — In-day single strategy minimum akış (kısa)
Aşağıdakileri ATLAMA bile in-day 5dk run'da:
```bash
# Veri validation (rules §3)
python -c "from tools.data_check import verify_actual_range; verify_actual_range('BTC','1h')"

# KANONİK tek-koşu (data MEGA_BUNDLE_MANIFEST ile bağlanır — AGENTS.md "DATA & LAUNCH")
python tools/mega_walk_forward.py --strategy <id> --symbol <SYM> --tf <tf>
#    walk_forward_processor.py = alt-seviye/custom; varsayılan tek-koşu DEĞİL

# 4-gate (rules §8)
python tools/finalize_bootstrap_bh.py --result <result.json>   # bootstrap + BH-FDR + DSR
python tools/multiwindow_oos.py --result <result.json>          # Q1-Q4 + param neighborhood
python tools/alpha_vs_buyhold.py --result <result.json>         # ZORUNLU buy&hold

# Classification + promotion (rules §6 + §9)
python tools/generate_morning_report.py --single-candidate <id>
```
Single-strategy ≠ "hızlı için 4-gate atla". Süre az, gate'ler aynı.

## Gate 2 — Plan

User'la `AskUserQuestion` ile netleştir:
- Yalnız ingest+analyze mı, backtest mi, ikisi mi?
- Crash/sapma davranışı (raporla / auto-restart / durdur+uyar)
- Worker policy (sessiz / hızlı / dinamik)

## Gate 3 — Implementation (smoke gate dahil)

### 3.1 Path audit
```python
import mega_walk_forward as mw, os
assert mw.OUTPUT_DIR.exists() and os.access(str(mw.OUTPUT_DIR), os.W_OK)
```

### 3.2 Smoke test (HARD — runbook §2.4)
```bash
MEGA_WORKERS=2 MEGA_OUTPUT_DIR=/tmp/smoke timeout 120 python overnight_v2_runner.py 2>&1 | tail -10
# Bekle: "all jobs done" + JSON timestamp güncel
```
JSON yazımı kanıtlanmadan loop başlatma.

### 3.3 Loop script
`03_QUANTLENS/tools/overnight_loop_YYYY-MM-DD.sh` (referans: `_sprint.sh`)
- Zorunlu: env vars, deadline cap, heartbeat, auto-restart, timestamped output kopyala
- `loop.pid` dosyasına PID yaz (kill için)

### 3.4 Launch
```bash
bash overnight_loop_YYYY-MM-DD.sh > overnight_runs/loop_master.out 2>&1 &
echo $! > overnight_runs/loop.pid
```
**Background, not foreground.** UI session kapansa loop devam etmeli.

## Gate 4 — Monitor (ÇİFT KANAL)

### 4a. taskschd (admin PS, tek sefer):
```powershell
& "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools\register_overnight_monitor.ps1"
```
30dk fire, heartbeat freshness + crash zinciri + disk + balloon notif.

### 4b. Wakeup zinciri (AI session):
- `ScheduleWakeup` 1800s, prompt = monitor tick (runbook §6.3)
- Her wakeup'ta TEKRAR `ScheduleWakeup` 1800s. Zincir kopmasın.
- Deadline geçti → final raporu hazırla, zincir sonlandır.

İki kanal bağımsız. Biri kopsa diğeri devam. **A2 anti-pattern**.

## Gate 5 — Cross-model review

QuantLens research = parity touch DEĞİL → Gate 5 opsiyonel (ama önerilir).
MTC V2 / Pine üzerinde değişiklik varsa Gate 5 **zorunlu** (Codex / Gemini'ye review attır).

## Gate 6 — QA (post-loop)

```bash
ls overnight_runs/MEGA_results_iter_*.json | wc -l   # ≥1 iter geçmeli
grep -c "DEADLINE REACHED" overnight_runs/loop_*.log # 1
cat overnight_runs/_heartbeat.json | grep -E '"crashes":\s*[0-2]'  # ≤2 OK, 3+ structural sorun
```

Aggregate analyzer:
```bash
python aggregate_overnight_iters.py
```

## Gate 7 — Handoff (zorunlu)

1. `lessons_archive/OVERNIGHT_LESSONS_YYYY-MM-DD.md` yaz (ham gözlem, B-numaralı bulgular)
2. Yeni anti-pattern → `BACKTEST_OPTIMIZATION_RUNBOOK.md` §8 tablosuna ekle
3. `lessons_archive/OVERNIGHT_LESSONS_INDEX.md` yeni satır
4. `_AI_MEMORY/GLOBAL_HANDOFF.md` + `SESSION_LOG.md` güncelle
5. `NEXT_STEPS.md` yarın yapılacaklar

## WRITE-BACK

Bu prompt biterken zorunlu dosya güncellemeleri:
- `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_YYYY-MM-DD.md` (yeni)
- `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_INDEX.md` (satır ekle)
- `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` (anti-pattern merge, CHANGELOG)
- `_AI_MEMORY/GLOBAL_HANDOFF.md`
- `_AI_MEMORY/SESSION_LOG.md`
- `_AI_MEMORY/NEXT_STEPS.md`
