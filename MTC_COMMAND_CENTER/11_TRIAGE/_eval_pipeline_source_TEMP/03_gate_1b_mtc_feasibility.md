# 2. Gate 1B — MTC Feasibility Gate

## Amaç

Bu aşama şu soruya cevap verir:

```text
Bu strateji MTC_v2 içinde temel seviyede temsil edilebilir mi?
```

Bu aşama backtestten önce yapılmalıdır.

---

# Gate 1B Değerlendirme

Bu gate iki şekilde kullanılabilir:

```text
Option A: Pass / Fail
Option B: 50 puan üzerinden skor
```

---

# Gate 1B Puanlama — 50 Puan

| Kriter | Puan |
|---|---:|
| Sinyal long / short / close / flat formatına indirgenebilir | 10 |
| Entry-only veya full strategy olduğu net | 8 |
| MTC_v2 risk engine ile çelişmiyor | 10 |
| Alert formatına çevrilebilir | 8 |
| State machine olarak modellenebilir | 8 |
| MTC standard parametre yapısına uyarlanabilir | 6 |
| **Toplam** | **50** |

---

# Gate 1B Karar Eşikleri

| Puan | Karar |
|---:|---|
| 40–50 | MTC_v2 için uygun. Prototype/backtest yapılabilir. |
| 30–39 | Uygun olabilir. Önce spec eksikleri giderilmeli. |
| 0–29 | MTC_v2 için uygun değil. Backtest yapılmamalı. |

---

# Gate 1B Pass / Fail Kriterleri

```text
PASS:
- Strateji MTC_v2 signal contract yapısına indirgenebilir.
- Entry, exit veya entry-only durumu net.
- MTC risk engine ile çelişmez.
- Bot/alert mantığına çevrilebilir.
- State mantığı kurulabilir.

FAIL:
- Strateji manuel karar ister.
- Sinyal formatı net değildir.
- Risk engine ile çelişir.
- State takip edilemez.
- Alert üretilemez.
```
