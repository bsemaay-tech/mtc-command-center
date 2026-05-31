# Benim Yapabileceklerim vs Codex’e Kalacaklar

## Benim burada yapabildiklerim

Repo erişimi olmadan hazırlanabilen ve Codex kredisi tüketimini azaltan işler:

| İş | Durum |
|---|---|
| Multi-oracle mimari tasarımı | Hazırlandı |
| Karar matrisi | Hazırlandı |
| Lisans notları | Hazırlandı |
| JSON parity case/result/manifest şemaları | Hazırlandı |
| MTC Pine feature scanner | Hazırlandı |
| Normalized output formatları | Hazırlandı |
| PineTS/Python/PyneCore/vectorbt normalizer iskeletleri | Hazırlandı |
| Comparator scripti | Hazırlandı |
| Sentetik test case | Hazırlandı |
| Sentetik baseline/candidate örnekleri | Hazırlandı |
| Runbook | Hazırlandı |
| Codex’e verilecek daha kısa entegrasyon promptu | Hazırlandı |

## Codex’e kalması gereken işler

Bunlar kullanıcının Windows repo’sunda yapılmalı:

| İş | Neden Codex gerekli? |
|---|---|
| Gerçek repo dosyalarını bulmak | Ben kullanıcının lokal diskini göremem |
| Mevcut Python engine entrypoint’ini bağlamak | Repo içi path ve CLI bilinmeli |
| PineTS CLI’nin gerçek komutunu doğrulamak | Lokal kurulum, npm/node, PineTS versiyonu gerekli |
| Gerçek MTC v2 dosyasını scanner’dan geçirmek | Dosya lokal repo’da |
| Gerçek parity case’leri üretmek | Data/config/export dosyaları lokal |
| PyneCore’u Windows venv içinde kurup çalıştırmak | Lokal environment gerekli |
| TradingView export dosyalarını normalize etmek | Export formatı kullanıcı dosyalarında |
| İlk gerçek multi-oracle parity koşusunu çalıştırmak | Gerçek engine/data gerekir |

## En büyük kredi tasarrufu

Codex’e artık “bütün mimariyi tasarla ve sıfırdan yaz” denmeyecek.  
Bunun yerine “bu hazır starter kit’i repo’ya entegre et ve gerçek entrypoint’leri bağla” denecek.

Bu, Codex işini yaklaşık olarak şu hale indirir:

1. Dosyaları repo’ya kopyala.
2. Path’leri düzelt.
3. Mevcut Python engine wrapper’ını doldur.
4. PineTS komutunu bağla.
5. Gerçek MTC dosyasıyla test et.
6. Rapor üret.
