# Troubleshooting

## Candidate ID çakışırsa

Aynı slug varsa `_V2` ekle. O da varsa `_V3` şeklinde artır.

## Registry bozulursa

Önce dosyayı yedekle. Candidate klasörlerindeki `01_candidate_metadata.yaml` dosyalarından registry yeniden kurulabilir. Eski satırları silme; düzeltmeyi ayrı notla yap.

## QuantLens raporu eksikse

Status `NEEDS_MORE_INFO` yap. Eksik entry, exit, risk, timeframe, market, repaint/lookahead veya source bilgilerini `05_risks_and_unknowns.md` içine yaz.

## Backtest data bulunamazsa

Backtest çalıştırma. Data bundle path, dataset_id ve sembol/timeframe eksiklerini yaz. Strategy Tester XLSX dosyalarını chart data gibi kullanma.

## Python prototype başarısız olursa

Hata mesajını candidate sonuç klasörüne yaz. Production runner dosyalarını düzeltmeye çalışma. Status `BACKTEST_FAILED` veya `NEEDS_MORE_INFO` olabilir.

## Parity riski çıkarsa

Status `PARITY_BLOCKED` yap. Repaint, lookahead, Pine/Python semantic farkı veya PineTS comparability eksikliği açık yazılmalı.

## Codex yanlışlıkla kod değiştirmeye kalkarsa

Durdur. Bu workflow'da `MTC_V2.pine` ve production Python runner dosyaları final integration aşamasına kadar değişmez. Önce plan ve risk raporu istenir.
