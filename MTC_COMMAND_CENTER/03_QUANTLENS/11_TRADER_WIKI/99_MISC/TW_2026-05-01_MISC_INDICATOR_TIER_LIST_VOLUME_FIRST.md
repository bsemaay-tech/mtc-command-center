# Trader Wiki Note

## Metadata
- Wiki ID: TW_2026-05-01_MISC_INDICATOR_TIER_LIST_VOLUME_FIRST
- Source URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_INDICATOR_TIER_LIST_VOLUME_FIRST
- Title: Indicator tier list and volume-first technical analysis
- Channel: UNKNOWN_CHANNEL
- Date: 2026-05-01
- Topic: 99_MISC
- Usefulness Score: 6
- Tags: indicators, volume, moving-average, donchian-channel, rsi-divergence, bollinger-bands, technical-analysis

## Kisa Ozet
- Video, popüler indikatörleri pratik değer açısından sıralıyor.
- Ana fikir: çoğu indikatör aynı fiyat verisini gecikmeli şekilde yeniden paketler; volume farklıdır çünkü katılım ve conviction ölçer.
- Tam bir trade sistemi vermediği için strategy candidate değil, Trader Wiki notu olarak saklandı.

## Ana Dersler
- `MACD`: gecikmeli sinyalin gecikmeli türevi olarak eleştiriliyor.
- `SMA`: özellikle `50/200` günlük veya haftalık ortalamalar kurumsal takip nedeniyle pratik destek/direnç alanı olabilir.
- `Stochastics`: trendde tavana/dibe yapışabilir, choppy piyasada whipsaw üretebilir.
- `RSI`: overbought/oversold tek başına zayıf; divergence kullanımında daha anlamlı.
- `Bollinger Bands`: yön değil volatilite alarmı verir; ayrıca direction sinyali gerekir.
- `Donchian Channels`: son `20` seans high/low kırılımı, piyasanın yeni bir şey yaptığını gösterir.
- `Fibonacci`: ekonomik gerekçe zayıf olsa da psikolojik/pattern etkisiyle retracement zone olarak izlenebilir.
- `Volume`: fiyat türevi değil; katılım, conviction ve momentum kalitesi hakkında farklı veri sağlar.

## MTC_V2 / Algo Trading Icin Baglanti
- Aynı fiyat serisinden türeyen çok sayıda indikatörü üst üste koymak gerçek bağımsız confirmation üretmeyebilir.
- Volume temelli confirmation, fiyat türevli confirmation'lardan ayrı değerlendirilmelidir.
- Donchian breakout ve HTF MA temasları araştırma fikri olarak saklanabilir, ancak tek başına strategy değildir.
- RSI divergence gibi fikirler repaint/pivot timing açısından ayrı audit gerektirir.

## Uygulanabilir Notlar
- Future candidate triage sırasında "bağımsız veri kaynağı mı, yoksa aynı fiyatın gecikmeli türevi mi?" sorusu eklenebilir.
- Volume divergence / exhaustion notları ayrı bir prototype konusu yapılacaksa açık entry/exit/stop/target kuralları gerektirir.
- Donchian ve HTF MA kavramları strategy değil, filter/guard veya context layer olarak düşünülmeli.

## Riskli veya Supheli Iddialar
- MACD gecikme ve indicator tier iddiaları kaynak/veri olmadan genelleme içeriyor.
- Charlie Munger atfı ve 200-day moving average performans iddiası bu intake sırasında doğrulanmadı.
- Volume zayıflaması her zaman reversal getirmez; trend devamı veya düşük likidite rejimleri farklı sonuç verebilir.
- Fibonacci "golden zone" davranışı sistematik test olmadan üretim sinyali sayılmamalı.

## Kaynak Transcript Notu
- Transcript arsiv path: inline user-provided transcript in chat, no local raw transcript file.
- Video index kaydi: `06_QUANTLENS_LAB/_registry/youtube_video_index.csv`
