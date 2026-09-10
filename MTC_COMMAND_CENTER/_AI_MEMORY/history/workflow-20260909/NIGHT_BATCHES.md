# Gece Batch Kuyruğu — launch reçeteleri (2026-06-06, Claude)

> Altyapı: `03_QUANTLENS/tools/night_runner.sh` (smoke→sweep→tail→release) +
> `mcc_night_tail.sh` (CPCV15+PBO+eval+Gate2+all-gate+**C1 Gate3 enrich**+scorecard_v2+
> alpha+morning+**D1 dashboard verify**). Determinizm: her sweep BİR kez. Biter → makineyi bırak.

## KRİTİK KURAL — D009: scipy hang, OpenBLAS thread init deadlock (REVISED 2026-06-07)

**D009-revised (kesin teşhis 2026-06-07, DeepSeek v4 Pro):** scipy 1.17.1'in OpenBLAS 0.3.30'u
(DYNAMIC_ARCH, NO_AFFINITY, Haswell, MAX_THREADS=24) thread-pool init sırasında asılı kalıyor.
MSYS2 PATH değil — OpenBLAS thread init deadlock. `import scipy` çalışır, `import scipy.sparse`/`scipy.stats` asılır.
`OPENBLAS_NUM_THREADS=1` işe yaramaz (env var okunmadan önce init asılır).

**TEK GÜVENİLİR ÇÖZÜM:** `run_python_clean.py` + `_scipy_shim.py`:
- `_scipy_shim.py`: pure-Python `norm.ppf()`/`norm.cdf()` (Acklam algorithm, hata < 1.15e-9)
- `run_python_clean.py`: her script'ten önce shim'i otomatik inject eder
- Kullanım: `python run_python_clean.py script.py [args...]`

**Template:** `sweep_new_only_2026-06-07.sh`, `overnight_remaining_2026-06-07.sh`

**ÇALIŞMAYAN yöntemler (hepsi MSYS2 PATH kalıtır):**
- `python script.py` bash'ten → D009 hang
- `powershell.exe -NoProfile -Command "python ..."` bash'ten → PowerShell de MSYS2 PATH alır
- Claude Code PowerShell tool'dan `python` → aynı
- `cmd.exe /c python` → aynı

---

## Hazır batch'ler (onaysız, düşük risk)

### Tam 43-strateji enriched gece (genuinely-new değil — bugünküyle aynı; sadece yeniden-gating için)
```bash
cd MTC_COMMAND_CENTER/03_QUANTLENS/tools
bash night_runner.sh --runner overnight_v2_runner.py --run-id night_$(date +%F) --workers 18 --deadline-h 10
```
> NOT: engine değişmediyse sonuç heavy_tier_2026-06-05 ile aynı (determinizm). Yalnız
> Gate3 enrichment (C1) yeni → mevcut run'a `mcc_night_tail.sh` koşmak yeterli, sweep gereksiz.

### Mevcut tüm run'lara C1+gating uygula (sweep YOK — hızlı, gerçek katkı)
```bash
cd MTC_COMMAND_CENTER/03_QUANTLENS/tools
for d in ../05_BACKTEST_RESULTS/*/; do
  [ -f "$d/MEGA_walk_forward_results.json" ] && bash mcc_night_tail.sh "$(cygpath -w "$d" 2>/dev/null || echo "$d")" "$(basename "$d")"
done
```

### Yeni strateji gece (B2 — kodlanmış strateji + sweep + tam gating)
```bash
bash night_runner.sh --runner strat_extra_runner.py --run-id ok_$(date +%F) --workers 8 \
  -- --strategy QL_OLIVER_KELL_PRICE_CYCLE --tf 2h --tf 4h --tf 1D
```

## Otonom-uygun batch tanımları (plan WS → batch)

| Batch | İş | Durum |
|---|---|---|
| **N1 (A1)** | spec→producer_spec.json üret (06_PROMOTED_TO_PARITY boş → "Not defined yet" kökü). DeepSeek/Grok dispatch + audit. | SCOPED — producer_spec generation tasarımı gerek |
| **N2 (B2)** | STG057/054/047 kodla+sweep+gating. STG057 threshold Barış pre-reg. | KISMİ — STG056 DONE |
| **N3 (C1)** | Gate3 enrich tüm run'lara. | TOOL DONE (`enrich_gate3_evidence.py`) — yukarıdaki for-loop |
| **N4 (D1/D2)** | auto-export DONE; cpcv/pbo/alpha/morning UI-link (Codex A5/D4) kaldı. | KISMİ — D1 DONE |
| **N5** | 86 walk-forward-candidate'tan objektif-codeable alt küme audit. | TODO |
| **N6** | heavy-validation tier (derin CPCV) yeni stratejilerde. | TOOL DONE (`heavy_night_*.sh`) |

## Otonom BAŞLATILAMAZ (Barış pre-reg/onay)
- B3 confirmation grid · C2/C3 entegrasyon adapter · E Pine/parity.

## Kritik kural — PBO cap (D008, 2026-06-07)

`probabilistic_pbo.py --max-combinations 0` = YASAK. C(44,22) ≈ 7.3B → MemoryError.
Her script'te `--max-combinations 100000` kullan. 100k örnek PBO dağılımını stabilize etmek için fazlasıyla yeterli.

## Launch mekaniği (uzun gece)
```bash
# background + harness completion notify:
bash night_runner.sh --runner overnight_v2_runner.py --run-id night_X --workers 18 &
echo $! > overnight_runs/night.pid
# + background waiter (heartbeat 'complete' olana kadar bekler) → harness uyandırır
```
