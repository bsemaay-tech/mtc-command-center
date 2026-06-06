# Trading Strategy Evaluation Pipeline — Overview

## Amaç

Bu pipeline’ın amacı; YouTube, makale, gösterge, sosyal medya veya başka bir kaynaktan bulunan bir trading strateji adayını sistematik şekilde değerlendirmek, gereksiz kodlama/backtest zamanını azaltmak ve sadece uygun adayları MTC_v2 sürecine almaktır.

---

# Genel Akış

```text
0. Strategy Source Intake
1. Gate 1 — Candidate Intake Score / 100
2. Gate 1B — MTC Feasibility Gate / Pass-Fail veya 50 Puan
3. Prototype / Strategy Code
4. Repaint / Lookahead Verification
5. Gate 2 — Backtest Evidence Score / 100
6. Gate 3 — MTC Production Readiness Score / 100
7. Forward Test / Paper Trade
```

---

# Minimum Geçiş Kuralları

```text
Gate 1:
Minimum 75 / 100

Gate 1B:
Minimum 40 / 50 veya PASS

Repaint Verification:
REJECT_REPAINT olmamalı

Gate 2:
Minimum 75 / 100

Gate 3:
Minimum 75 / 100
```

---

# Final Pipeline Özeti

```text
0. Strategy Source Intake
   ↓
1. Gate 1 — Candidate Intake Score / 100
   Minimum: 75
   ↓
2. Gate 1B — MTC Feasibility Gate / 50 or Pass-Fail
   Minimum: 40/50 or PASS
   ↓
3. Prototype / Strategy Code
   ↓
4. Repaint / Lookahead Verification
   REJECT_REPAINT ise süreç durur
   ↓
5. Gate 2 — Backtest Evidence Score / 100
   Minimum: 75
   ↓
6. Gate 3 — MTC Production Readiness Score / 100
   Minimum: 75
   ↓
7. Forward Test / Paper Trade
```

---

# Genel Red Kuralları

Aşağıdakilerden biri varsa strateji otomatik olarak elenir veya arşive alınır:

```text
- İnsan yorumu gerektirir.
- Kodlanabilir değildir.
- Entry rule açık değildir.
- Trade lifecycle belirsizdir.
- Açık repaint / lookahead / future leak vardır.
- MTC_v2 signal contract yapısına indirgenemez.
- Backtest için gerekli veri yoktur.
- Komisyon/slippage sonrası sistem çöker.
- Buy & Hold’a göre hiçbir anlamlı avantaj üretmez.
- Out-of-sample test tamamen çöker.
- Parametreler küçük değişince sistem bozulur.
- Test süresi ve trade count yetersizdir.
- MTC production güvenliği sağlanamaz.
```
