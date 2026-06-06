# Overnight Lessons — 2026-06-01 (gece çalışması 2026-05-31 → 06-01)

## Özet
- **Hedef:** 2 worker × 1M case overnight, 174 yeni transcript değerlendir + mevcut 39 strateji backtest loop.
- **Sonuç:** 3 iter crash + 1 iter yarıda kesildi (manuel restart). ~5.5 saat veri kaybı.
- **Kök neden:** `mega_walk_forward.py` `OUTPUT_DIR` legacy frozen path'e işaret ediyordu (`C:\LAB\tradingview-lab\...` read-only).

## Bulgular

### B1 — OUTPUT_DIR legacy path crash (kritik)
`mega_walk_forward.py:37` hardcoded:
```python
OUTPUT_DIR = Path(r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\05_BACKTEST_RESULTS")
```
LEGACY_FREEZE_POLICY altında bu dizin `-r--r--r--` (read-only). Hesap %94'te bitiyordu, `json.dump` `PermissionError`. Her iter ~75dk çalışıp en son anda patlıyordu.

**Fix uygulandı (2026-06-01 04:06):**
```python
_env_out = os.environ.get("MEGA_OUTPUT_DIR")
OUTPUT_DIR = Path(_env_out) if _env_out else Path(__file__).resolve().parent.parent / "05_BACKTEST_RESULTS"
```
Default: `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/` (writable).

**Ders:** Migration sonrası HER `OUTPUT_DIR` / `DATA_BUNDLE_PATH` / hardcoded path'i smoke-check yap. Önceki başarılı runlar legacy path henüz dondurulmamışken yapıldı.

### B2 — Wakeup zinciri kesintisi
`ScheduleWakeup` 00:01 için kuruldu, fire ettikten sonra (veya hiç fire etmediğinde) yeni schedule atılmadı. 4+ saat sessizlik. İlk crash 00:00 civarında olsa fix anında uygulanırdı, ~5.5 saat kazanılırdı.

**Ders:** Wakeup zincirinin tek-nokta-arızası var. **Çift mekanizma:** wakeup + Windows zamanlanmış görev (taskschd) paralel kontrol.

### B3 — Auto-restart sessiz veri kaybı
Loop EC!=0 algıladı, restart yaptı, log'a yazdı — ama iter'in **%94 yapılmış hesap sonucu** bellekte ölüp gitti. Restart safe ama veri kurtarmaz.

**Ders:** Crash'te `results` listesini pickle olarak `overnight_runs/_resume_iter_<N>.pkl` yaz, restart başında yükle. Veya en azından kısmi JSON'u atomik temp-rename ile yazıp recovery'de pick up et.

### B4 — Heartbeat granülaritesi
`_heartbeat.json` sadece iter-arası güncelleniyor. İter içinde 75dk sessiz. Anormallik tespiti gecikiyor.

**Ders:** mega_walk_forward.py'nin periodik `[N/total] elapsed=Xs counts=...` print'ini parse edip her dakika heartbeat'e ekle.

### B5 — Worker sayısı erken kararlaştı
2 worker = fan-friendly ama gece sessiz odada 20 worker da problem değildi (Barış uyuyordu, fan sesi ona ulaşmıyordu). Pragmatik strateji: ilk 30dk 2 worker (smoke), sorun yoksa otomatik 20'ye yükselt.

**Ders:** Worker sayısı dinamik olabilir. Loop iter başında env okusun, runtime değişimi destekle.

## Yarın için aksiyon listesi

### A1 — Smoke test gate (G6 zorunlu)
Loop launch'tan önce 1 dummy iter çalıştır:
```bash
MEGA_WORKERS=2 timeout 120 python overnight_v2_runner.py > /tmp/smoke.log
grep -q "JSON written" /tmp/smoke.log || abort
```
JSON yazımı kanıtlanmadan loop başlatma.

### A2 — Windows zamanlanmış görev (taskschd)
`tools/monitor_overnight.ps1` her 30dk:
- `_heartbeat.json` mtime > 60dk → ALERT (UTF8 log + balloon notification)
- exit code 1 son 3 iter'de → ALERT
- disk doluluk %90 → ALERT
- Log'u `overnight_runs/_external_monitor.log`'a yaz

Kurulum komutu (admin gerekir):
```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools\monitor_overnight.ps1"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Minutes 30)
Register-ScheduledTask -TaskName "MCC_Overnight_Monitor" -Action $action -Trigger $trigger -Description "30dk overnight loop health check"
```

### A3 — Wakeup zinciri + harici monitor BİRLİKTE
Bağımsız iki kanal. Biri kopsa diğeri devam. Wakeup raporu task scheduler log'una da yansısın.

### A4 — Path audit script
`tools/audit_hardcoded_paths.py` — bütün repo'da `C:\LAB\tradingview-lab\` veya benzer legacy işaretleri grep'le, listele. CI'a ekle.

### A5 — Resumable iter
`mega_walk_forward.py`'a `--resume <pickle>` argümanı. Crash sonrası kayıp veri minimize.

## Bu gece kurtarılan / kaybedilen

| Metrik | Değer |
|---|---|
| Toplam iter denemesi | ~5 (iter 1-4 crash, iter 5 manuel kesinti) |
| Başarılı JSON kayıt | 0 |
| Veri kaybı süresi | ~5.5 saat hesaplama |
| Loop framework çalıştı mı? | Evet — auto-restart, heartbeat, log dönüşü tüm OK |
| Tek arızalı bileşen | OUTPUT_DIR + monitör zinciri |

## Kod patch listesi (uygulanmış)
- `mega_walk_forward.py:37-42` — OUTPUT_DIR env override + CLEAN repo default
- `mega_walk_forward.py:742-746` — MEGA_WORKERS env override
- `11_TRIAGE/overnight_loop_2026-05-31.sh` (yeni, tools/ kopyası kullanıldı) — auto-restart + heartbeat + 8h cap

## Karar referansları
- Legacy freeze policy: `docs/migration_manifests/LEGACY_FREEZE_POLICY.md` (commit `dcdf913`)
- Path rewrite policy: `docs/migration_manifests/PATH_REWRITE_POLICY.md`
- OUTPUT_DIR audit'in path rewrite kapsamına alınması gerek (deferred listesinden çıkar)
