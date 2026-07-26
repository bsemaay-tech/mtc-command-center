# 17_DEPLOYMENT — Köprüyü başka makineye / VPS'e kurma (P2 host taşıma)

Tarih: 2026-07-13; KVM2 Linux bölümü 2026-07-26'da güvenli paketle değiştirildi.
Amaç: Barış'ın planı — gece ev PC (shakedown), gündüz iş PC (~6 gün),
paralelde VPS kiralanınca kalıcı taşınma. Bu doküman herhangi bir modelin veya Barış'ın tek
başına uygulayabileceği kadar ayrıntılıdır. **TESTNET-ONLY; mainnet üçlü kilidi her makinede
geçerli.**

> **KVM2 authority warning:** This document is guidance, not execution
> authorization. The current lower-level authority is
> `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`.
> Install, secrets, cutover, first start, and ARM are separate owner gates.

## 2026-07-13 P2 runtime isolation requirement

The active P2 process must not run from the shared research worktree because parallel agents can
switch its branch between supervisor restarts. Use a short isolated Git worktree such as
`C:\P2RT`, pin and review its commit, and point Task Scheduler directly to that worktree's
`IBKR_PAPER_BRIDGE\tools\run_bridge_p2.ps1`. The wrapper resolves its runtime root from
`$PSScriptRoot`; do not reintroduce a hardcoded shared-checkout root.

## 0. Güvenlik kuralı — her makineye AYRI API cüzdanı

Ana cüzdan private key'i HİÇBİR makineye konmaz. Her host için Hyperliquid testnet arayüzünden
**yeni bir named agent/API wallet** üret (ör. `MTC-bridge-work`, `MTC-bridge-vps`) ve o makineye
sadece o agent'ın key'ini koy. Sebep: makinelerden biri ele geçerse sadece o agent revoke edilir;
API cüzdanı zaten para çekemez. `HL_ACCOUNT_ADDRESS` her yerde aynı (ana hesap adresi).

## 1. Windows iş PC kurulumu (~20 dk)

1. **Repo**: `git clone <repo>` veya USB/zip ile `C:\LAB\Tradingview_LAB_CLEAN` yolunu birebir
   koru (Task Scheduler scripti mutlak yol kullanıyor). Branch: `feature/ibkr-bridge-final`.
2. **Python 3.11+** kur; sonra repo kökünden:
   `pip install -r IBKR_PAPER_BRIDGE/requirements.txt`
3. **Env değişkenleri** (Windows "Kullanıcı ortam değişkenleri" — chat'e asla yazma):
   - `HL_ACCOUNT_ADDRESS` = ana hesap adresi (0x + 40 hex)
   - `HL_API_WALLET_KEY` = O MAKİNENİN agent key'i (0x + 64 hex)
   - `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` = aynı değerler
   - `HL_LIVE_ACK` = ASLA tanımlama.
4. **Doğrulama** (repo kökünden):
   ```powershell
   $env:PYTHONUTF8='1'
   python -m pytest IBKR_PAPER_BRIDGE/tests -q        # 110+ passed beklenir
   ```
5. **Süpervizör görevi** (yönetici GEREKMEZ):
   ```powershell
   $action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\LAB\Tradingview_LAB_CLEAN\IBKR_PAPER_BRIDGE\tools\run_bridge_p2.ps1"'
   $trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
   $settings = New-ScheduledTaskSettingsSet -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Days 365) -StartWhenAvailable
   Register-ScheduledTask -TaskName 'MTC-Bridge-P2' -Action $action -Trigger $trigger -Settings $settings -Force
   Start-ScheduledTask -TaskName 'MTC-Bridge-P2'
   ```
6. **Kontrol**: 60 sn sonra `http://127.0.0.1:8790/api/status` → `mode: paper`,
   `exchange_conn: hyperliquid`, `reconcile_ready: true`, `state: DISARMED`.
7. **Güç ayarları**: uyku/hibernate KAPALI; Windows Update etkin saatleri mesaiye ayarla.
8. **ARM**: dashboard (`http://127.0.0.1:8790`) → ARM; veya:
   ```powershell
   $v = (Invoke-RestMethod http://127.0.0.1:8790/api/status).state_version
   Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8790/api/arm -Headers @{ 'X-Confirm' = "$v" }
   ```
   Telegram'a `state -> ARMED` düşer.

## 2. Taşınma ritüeli (ev → iş, iş → VPS)

Eski makinede: (1) dashboard'dan **DISARM** (açık pozisyonun SL/TP'si borsada kalır — güvenli);
(2) `Stop-ScheduledTask MTC-Bridge-P2` + görevi devre dışı bırak (`Disable-ScheduledTask`) —
iki makine AYNI ANDA çalışmamalı (duplicate-order koruması var ama tek-yazar ilkesi esas);
(3) kapat. Yeni makinede: kur (yukarısı) → başlat → `reconcile_ready` bekle → ARM.
Eski Windows shakedown taşımalarında taze DB kullanılmış olabilir. KVM2 kesiminde
bu kural geçerli değildir: P3-01 risk-state seçimi hâlâ **OPEN**. Önerilen yol,
eski writer tamamen durdurulduktan sonra `tools/wal_state_bundle.py` ile
WAL-tutarlı migration'dır. Taze DB/reset ancak owner tarafından ayrıca seçilip
daily-loss, consecutive-loss, order ve foreign-position belirsizliğinde
fail-closed test edilirse kullanılabilir.

## 3. KVM2 Linux deployment package (preparation only)

The old global-pip, root service, `Restart=always`, and `enable --now` recipe has
been retired. Do not use it.

Canonical inert assets:

- `deploy/linux/README.md` — architecture, paths, safety and gate order;
- `deploy/linux/COMMANDS.md` — later separately authorized exact commands;
- `requirements.in` plus exact transitive `requirements.lock` hashes;
- `deploy/linux/package.sh` — clean exact-SHA payload;
- `deploy/linux/install.sh` — exact SHA plus payload-manifest hash, Python 3.12
  per-SHA venv, binary wheels, service installed masked/disabled/unstarted;
- `deploy/linux/verify.sh` — read-only exact-release assertions;
- `deploy/linux/rollback.sh` — stop/mask/preserve state, never start or ARM;
- `tools/wal_state_bundle.py` — WAL-consistent capture and verification.

Target boundaries: root-owned read-only release and venv trees under
`/opt/mtc-bridge`, dedicated non-login `mtc-bridge`, state under
`/var/lib/mtc-bridge`, logs under `/var/log/mtc-bridge`, root-owned `0600` env
contract, and `127.0.0.1:8790` with SSH-only inbound firewall. The first-start
unit is separate, `Restart=no`, has no enable target, and is installed masked.
The restart-enabled steady template is separate and is never installed by the
installer.

No asset here authorizes package installation on KVM2, secret provisioning,
Windows quiesce, cutover, first start, TESTNET exchange mutation, ARM, or
deployment. P2-09 and P3-03 Ubuntu evidence, independent audit, and owner gates
remain open.

## 4. P2 sayacı kuralı (dürüst kayıt)

- Ev gecesi + taşınmalar = **shakedown**, P2 sayacına DAHİL DEĞİL.
- **P2 gün 0 = stabil hostta (iş PC veya VPS) son ARM anı.** Host değişirse sayaç yeniden
  başlar (PREREG "kesintisiz ≥10 gün" ruhu). VPS'e erken geçmek bu yüzden avantaj.
- Her ARM/DISARM/taşınma `GLOBAL_HANDOFF.md`'ye tarihli not.
