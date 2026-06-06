# Final Decision Matrix and Strategy Status

# Final Decision Matrix

| Gate 1 | Gate 1B | Gate 2 | Gate 3 | Karar |
|---:|---|---:|---:|---|
| 75+ | PASS | 75+ | 75+ | Forward test / paper trade |
| 75+ | PASS | 75+ | <75 | Strateji iyi; MTC entegrasyonu eksik |
| 75+ | PASS | <75 | — | Backtest sonucu zayıf; üretime alınmaz |
| 75+ | FAIL | — | — | MTC’ye uygun değil; backtest yapılmaz |
| <75 | — | — | — | Kodlama/backtest için zayıf aday |
| 85+ | PASS | 85+ | 85+ | Güçlü aday; kontrollü forward test |
| 60–74 | PASS/FAIL | — | — | Spec iyileştirilmeden işleme alınmaz |

---

# Strategy Status Etiketleri

```text
IDEA:
Sadece fikir aşamasında.

SPEC_DRAFT:
Kurallar çıkarılmış ama eksikler var.

SPEC_READY:
Kurallar net, Gate 1 değerlendirmesine hazır.

BACKTEST_READY:
Gate 1 ve Gate 1B geçildi.

PROTOTYPE_CODED:
İlk kod yazıldı.

REPAINT_VERIFIED:
Kod repaint/lookahead açısından doğrulandı.

BACKTEST_PASSED:
Gate 2 geçildi.

MTC_READY:
Gate 3 geçildi.

FORWARD_TEST:
Paper trade / demo test aşamasında.

REJECTED:
Elendi.

ARCHIVED:
Şu an kullanılmayacak ama fikir olarak saklanacak.
```

---

# Final Status Akışı

```text
IDEA
  ↓
SPEC_DRAFT
  ↓
SPEC_READY
  ↓
BACKTEST_READY
  ↓
PROTOTYPE_CODED
  ↓
REPAINT_VERIFIED
  ↓
BACKTEST_PASSED
  ↓
MTC_READY
  ↓
FORWARD_TEST
```

---

# Reject / Archive Akışı

```text
Any Gate Hard Fail
  ↓
REJECTED

Low-priority but potentially useful idea
  ↓
ARCHIVED
```
