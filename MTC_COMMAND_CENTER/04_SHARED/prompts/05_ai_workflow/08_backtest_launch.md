# 08 - Backtest Launch

> WORKFLOW MAPPING: The numbered sections below are backtest-domain Stages, not replacements for repository Gates G1-G7. Lead/Implementer ownership and acceptance follow `AGENTS.md` and `AI_RULES.md`.

> **Bu prompt'u kullan:** HER backtest. Uc senaryo da ayni gate'ler:
> - **In-day single strategy** ("BTC 1h'de bu RSI stratejisini test et")
> - **Sprint** (1-3 saat, mevcut grid sweep)
> - **Overnight** (6-12 saat, full research sweep)
>
> Sure degisir, kalite esigi degismez. 5dk run dahi 4-gate (rolling WF + bootstrap+BH-FDR + DSR + multi-window) + buy&hold karsilastirmasi olmadan promotable degil.
>
> **MTC V2 BIG_OVERNIGHT icin:** `01_MTC_PROJECT/docs/optimization/BIG_OVERNIGHT_OPTIMIZATION_RUNBOOK.md`'a git, oradan devam et. Asagidaki adimlar QuantLens research icindir.

## Backtest Stage 0 - ZORUNLU PRE-READ (iki dosya)

1. `AGENTS.md` (repo koku)
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. `MTC_COMMAND_CENTER/_AI_MEMORY/COMPONENT_ROUTER.md` -> route to `03_QUANTLENS` component chain: `03_QUANTLENS/AGENTS.md` -> `03_QUANTLENS/_AI_MEMORY/START_HERE.md` -> `CURRENT.md` -> `NEXT_STEPS.md`. Root volatile memory not required for single-component backtest tasks.
4. `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
5. **`MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`** <- CANONICAL kurallar (4 gate, classification, promotion, antigravity, morning report)
6. **`MTC_COMMAND_CENTER/11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`** <- operasyonel yurutme (tool komutlari, worker, monitor)
7. `MTC_COMMAND_CENTER/11_TRIAGE/lessons_archive/` en yeni 1 dosya

Atlama YASAK. Skip yaparsan A1-A15 anti-pattern'lerinden birini tekrarlarsin.

## Backtest Stage 1 - Scope

- **Senaryo:** in-day single / sprint / overnight?
- Kapsam ne? (1 strateji x 1 sembol / mevcut grid sweep / yeni transcript triage)
- Worker sayisi (runbook 5 tablo: in-day 4-8, sprint 16-20, overnight 16, parity gece 16)
- Sure butcesi (`--time-budget-minutes` / loop `DEADLINE`)
- **Runtime <-> budget kontrolu (A22, ZORUNLU - "just start"ta bile):** Stage-0'da en yeni `lessons_archive/*` oku. Birkac hucre smoke ile runtime'i tahmin et. Sweep budget'tan KISA bitecekse: YA heavy-validation tier ekle (+-2 grid, 50k bootstrap, multi-seed DSR, CPCV-all, PBO, +sembol/TF) YA DA makineyi birak (idle box'i keep-awake'te tutma). Deterministik sweep'i tekrar kosma = sifir bilgi (A19).
- OUTPUT_DIR (CLEAN repo default - env override gerek mi)

### Backtest Stage 1.1 - Held-out-data virginity (MANDATORY)

`RESEARCH_RUN_REGISTRY.json` is a dashboard index, not a complete evidence inventory. Before
freezing any held-out strategy/symbol/timeframe/window scope, recursively scan prior result JSONs
under both `03_QUANTLENS/05_BACKTEST_RESULTS/` and `03_QUANTLENS/research/` for the same strategy,
symbol, timeframe, and observation window. Disclose every hit in the pre-registration. A hit
requires an amended scope and fresh written approval before execution; never silently replace or
drop a cell. Registry lookup alone never proves virginity.

### Backtest Stage 1.5 - In-day single strategy minimum akis (kisa)
Asagidakileri ATLAMA bile in-day 5dk run'da:
```bash
# Veri validation (rules 3)
python -c "from tools.data_check import verify_actual_range; verify_actual_range('BTC','1h')"

# KANONIK tek-kosu (data MEGA_BUNDLE_MANIFEST ile baglanir - AGENTS.md "DATA & LAUNCH")
python tools/mega_walk_forward.py --strategy <id> --symbol <SYM> --tf <tf>
#    walk_forward_processor.py = alt-seviye/custom; varsayilan tek-kosu DEGIL

# 4-gate (rules 8)
python tools/finalize_bootstrap_bh.py --result <result.json>   # bootstrap + BH-FDR + DSR
python tools/multiwindow_oos.py --result <result.json>          # Q1-Q4 + param neighborhood
python tools/alpha_vs_buyhold.py --result <result.json>         # ZORUNLU buy&hold

# Classification + promotion (rules 6 + 9)
python tools/generate_morning_report.py --single-candidate <id>
```
Single-strategy != "hizli icin 4-gate atla". Sure az, gate'ler ayni.

## Backtest Stage 2 - Plan

User'la `AskUserQuestion` ile netlestir:
- Yalniz ingest+analyze mi, backtest mi, ikisi mi?
- Crash/sapma davranisi (raporla / auto-restart / durdur+uyar)
- Worker policy (sessiz / hizli / dinamik)

## ⛔ STOP — Barış Approval Required Before Stage 3

**Explicit Barış approval is required before any backtest, optimization, artifact generation, or execution may begin.** This is in addition to all inherited component rules (root `DO_NOT_TOUCH.md`, `03_QUANTLENS/AGENTS.md`). Do not proceed to Stage 3 or beyond without a recorded approval in the current session.

## Backtest Stage 3 - Implementation (smoke gate dahil)

### 3.1 Path audit
```python
import mega_walk_forward as mw, os
assert mw.OUTPUT_DIR.exists() and os.access(str(mw.OUTPUT_DIR), os.W_OK)
```

### 3.2 Smoke test (HARD - runbook 2.4)
```bash
MEGA_WORKERS=2 MEGA_OUTPUT_DIR=/tmp/smoke timeout 120 python overnight_v2_runner.py 2>&1 | tail -10
# Bekle: "all jobs done" + JSON timestamp guncel
```
JSON yazimi kanitlanmadan loop baslatma.

### 3.3 Loop script
`03_QUANTLENS/tools/overnight_loop_YYYY-MM-DD.sh` (referans: `_sprint.sh`)
- Zorunlu: env vars, deadline cap, heartbeat, auto-restart, timestamped output kopyala
- `loop.pid` dosyasina PID yaz (kill icin)

### 3.4 Launch
```bash
bash overnight_loop_YYYY-MM-DD.sh > overnight_runs/loop_master.out 2>&1 &
echo $! > overnight_runs/loop.pid
```
**Background, not foreground.** UI session kapansa loop devam etmeli.

## Backtest Stage 4 - Monitor (CIFT KANAL)

### 4a. taskschd (admin PS, tek sefer):
```powershell
& "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools\register_overnight_monitor.ps1"
```
30dk fire, heartbeat freshness + crash zinciri + disk + balloon notif.

### 4b. Wakeup zinciri (AI session):
- `ScheduleWakeup` 1800s, prompt = monitor tick (runbook 6.3)
- Her wakeup'ta TEKRAR `ScheduleWakeup` 1800s. Zincir kopmasin.
- Deadline gecti -> final raporu hazirla, zincir sonlandir.

Iki kanal bagimsiz. Biri kopsa digeri devam. **A2 anti-pattern**.

## Backtest Stage 5 - Cross-model review

Repository Gate 5 remains mandatory for every repository change/write task, including trivial typo/doc work. Use the exact `AGENTS.md` CANONICAL AUDIT ROSTER: Claude audit equals `claude-opus-4-8` plus `xhigh`; Codex audit equals `gpt-5.6-sol` plus `high` for an ordinary review or `xhigh` for protected surfaces and every re-audit after `REQUEST_CHANGES` or `BLOCK`. Every audit round uses a fresh independent session. Verdicts are `PASS` / `PASS-WITH-NITS` / `REQUEST_CHANGES` / `BLOCK`, with at most 3 repair/re-audit rounds. MTC V2, Pine, parity, trading, and other protected-surface changes still require explicit Barış approval before implementation.

## Backtest Stage 6 - QA (post-loop)

```bash
ls overnight_runs/MEGA_results_iter_*.json | wc -l   # >=1 iter gecmeli
grep -c "DEADLINE REACHED" overnight_runs/loop_*.log # 1
cat overnight_runs/_heartbeat.json | grep -E '"crashes":\s*[0-2]'  # <=2 OK, 3+ structural sorun
```

Aggregate analyzer:
```bash
python aggregate_overnight_iters.py
```

## Backtest Stage 7 - Handoff (zorunlu)

1. `lessons_archive/OVERNIGHT_LESSONS_YYYY-MM-DD.md` yaz (ham gozlem, B-numarali bulgular)
2. Yeni anti-pattern -> `BACKTEST_OPTIMIZATION_RUNBOOK.md` 8 tablosuna ekle
3. `lessons_archive/OVERNIGHT_LESSONS_INDEX.md` yeni satir
4. `03_QUANTLENS/_AI_MEMORY/CURRENT.md` guncelle (component G7)
5. `03_QUANTLENS/_AI_MEMORY/NEXT_STEPS.md` yarin yapilacaklar
6. Cross-component ise: once her etkilenen component'in `_AI_MEMORY/CURRENT.md` + `NEXT_STEPS.md` guncelle; SONRA root `_AI_MEMORY/GLOBAL_HANDOFF.md`'a tek ozlu koordinasyon satiri ekle.

## WRITE-BACK

Bu prompt biterken zorunlu dosya guncellemeleri:

**Component-scoped (03_QUANTLENS route):**
- `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_YYYY-MM-DD.md` (yeni)
- `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_INDEX.md` (satir ekle)
- `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` (anti-pattern merge, CHANGELOG)
- `03_QUANTLENS/_AI_MEMORY/CURRENT.md` (always)
- `03_QUANTLENS/_AI_MEMORY/NEXT_STEPS.md` (always)

**Cross-component:** update `03_QUANTLENS/_AI_MEMORY/CURRENT.md` + `NEXT_STEPS.md` first, then every additional affected component's `_AI_MEMORY/CURRENT.md` + `NEXT_STEPS.md` (+ `DECISIONS.md` / `ACTIVE_FILES.md` if applicable); root `_AI_MEMORY/GLOBAL_HANDOFF.md` one concise coordination entry last.

**Global/policy:** root `_AI_MEMORY/GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `DECISIONS.md`, `ACTIVE_FILES.md`, `PROJECT_MEMORY.md` as applicable.
