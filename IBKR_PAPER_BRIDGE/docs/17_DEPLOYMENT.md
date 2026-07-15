# 17_DEPLOYMENT — Köprüyü başka makineye / VPS'e kurma (P2 host taşıma)

Tarih: 2026-07-13. Amaç: Barış'ın planı — gece ev PC (shakedown), gündüz iş PC (~6 gün),
paralelde VPS kiralanınca kalıcı taşınma. Bu doküman herhangi bir modelin veya Barış'ın tek
başına uygulayabileceği kadar ayrıntılıdır. **TESTNET-ONLY; mainnet üçlü kilidi her makinede
geçerli.**

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
`data/bridge.db` TAŞINMAZ — her host kendi taze DB'siyle yeni run açar; eski DB eski makinede
arşiv olarak kalır (P2 raporu için kesitleri birleştirilir).

## 3. VPS kurulumu (Linux, ~$5/ay — Hetzner CX11 / DO 1GB yeterli)

1. Ubuntu 24.04; `apt install python3.12 python3-pip git`.
2. Repo'yu klonla → `pip install -r IBKR_PAPER_BRIDGE/requirements.txt`.
3. Env: `/etc/systemd/system/mtc-bridge.service`:
   ```ini
   [Unit]
   Description=MTC Crypto Paper Bridge (Hyperliquid TESTNET)
   After=network-online.target
   [Service]
   WorkingDirectory=/opt/Tradingview_LAB_CLEAN/IBKR_PAPER_BRIDGE
   Environment=PYTHONUTF8=1
   EnvironmentFile=/etc/mtc-bridge.env    # HL_ACCOUNT_ADDRESS, HL_API_WALLET_KEY(vps agent), TELEGRAM_*
   ExecStart=/usr/bin/python3 -m bridge.app
   Restart=always
   RestartSec=10
   [Install]
   WantedBy=multi-user.target
   ```
   `chmod 600 /etc/mtc-bridge.env`. Not: Linux'ta winreg yok — env dosyası zorunlu (E1 fallback
   sadece Windows; process env yeterli olduğu için sorun değil).
4. `systemctl enable --now mtc-bridge`.
5. **Güvenlik**: sunucu 127.0.0.1'e bind'li — dışarıdan erişim YOK (doğru). İzleme için SSH
   tüneli: `ssh -L 8790:127.0.0.1:8790 user@vps` → tarayıcıda localhost:8790. Login+2FA
   olmadan portu asla dışa açma (mimari §13 kuralı). UFW: sadece SSH.
6. ARM: tünel üzerinden dashboard/API (yukarıdaki komutun aynısı).

## 4. P2 sayacı kuralı (dürüst kayıt)

- Ev gecesi + taşınmalar = **shakedown**, P2 sayacına DAHİL DEĞİL.
- **P2 gün 0 = stabil hostta (iş PC veya VPS) son ARM anı.** Host değişirse sayaç yeniden
  başlar (PREREG "kesintisiz ≥10 gün" ruhu). VPS'e erken geçmek bu yüzden avantaj.
- Her ARM/DISARM/taşınma `GLOBAL_HANDOFF.md`'ye tarihli not.
