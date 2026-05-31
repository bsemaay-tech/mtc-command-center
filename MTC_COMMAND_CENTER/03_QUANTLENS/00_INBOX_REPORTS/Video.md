============================================================
QUANTLENS RAPORU
============================================================

## 1. Karar Kartı

Candidate Name Suggestion:
- FRAMA Channel Trend Follower

Candidate Slug Suggestion:
- FRAMA_CHANNEL_EMA_TREND

URL:
- [https://youtu.be/f5zHBomRNnI](https://youtu.be/f5zHBomRNnI)

Video Başlığı:
- One of the Most Profitable Indicators I've Tested (FRAMA Channel)

Sınıf:
- SALVAGE

QuantLens Kararı:
- ŞÜPHELİ

Nihai Eylem:
- SALVAGE_ONLY

Varlık:
- Crypto / Stocks[cite: 4]

Timeframe:
- Primary: 5m, 30m, 1H, Daily[cite: 4]
- HTF: Yok

Strateji Tipi:
- Trend-following[cite: 2]

Ticari Değer:
- 4 — Strateji temel bir EMA filtresi ve adaptif kanal kırılımından ibaret. Kullanılan "Swing High/Low" stop mantığı algoritmik olarak tanımlanmadığı için backtest sonuçları yanıltıcıdır[cite: 7].

Zorluk:
- 4 — EMA ve Opposite Signal Exit MTC_V2'de zaten mevcuttur[cite: 5]. Sadece FRAMA (Fractal Adaptive Moving Average) mantığının Python/Pine tarafında baştan yazılması gerekir[cite: 4].

Ana Gerekçe:
- "Swing Low / Swing High" noktalarının (pivot left/right bars vb.) matematiksel olarak nasıl belirlendiği açıklanmamış. Bu durum bariz bir "hindsight" (geçmişi bilme) ve repaint riskidir[cite: 7].
- Komisyon ve slippage detayları tamamen yok sayılmış; %900 gibi uçuk kâr iddiaları pazar gürültüsüdür[cite: 7].
- Trend filter (200 EMA) ve Opposite Signal çıkışı zaten MTC_V2'de var olan modüllerdir[cite: 5]. Bütünleşik bir strateji olarak değersizdir, ancak FRAMA indikatörü Producer olarak değerlendirilebilir[cite: 2].

Kritik Riskler:
- Repaint: Şüpheli (Pivot/Swing mantığı belirsiz)[cite: 3, 7]
- Lookahead: Şüpheli[cite: 3]
- Overfit: Var (Filtrelenmiş backtest verisi)[cite: 7]
- Kapalı Kaynak: Yok[cite: 4]
- SL/Risk Yönetimi: Zayıf (Belirsiz Swing kuralları)[cite: 4, 7]
- Spread/Slippage Hassasiyeti: Yüksek (Özellikle 5m timeframe için)[cite: 3, 7]


## 2. Net Strateji Özeti

İndikatörler:
- FRAMA Channel (Fractal Adaptive Moving Average, parametreler videoda "default" denilerek gizlenmiş/belirtilmemiş)[cite: 4]
- 200 EMA[cite: 4]

Long Mantığı:
- Fiyat FRAMA Channel üst bandını yukarı kırmalı[cite: 4].
- Fiyat 200 EMA'nın üzerinde olmalı[cite: 4].

Short Mantığı:
- Fiyat FRAMA Channel alt bandını aşağı kırmalı[cite: 4].
- Fiyat 200 EMA'nın altında olmalı[cite: 4].

Exit:
- SL: Long için "en son swing low", Short için "en son swing high" (Algoritma UNKNOWN)[cite: 4].
- TP: Yok[cite: 4].
- BE: Yok[cite: 4].
- Trailing: Yok[cite: 4].
- Opposite Exit: Pozisyon, zıt bir sinyal (indicator flip) gelene kadar açık kalır[cite: 4].

Sinyal Zamanlaması:
- UNKNOWN (Videoda "fiyat kırdığında" deniyor, bar kapanışı teyidi açıkça belirtilmemiş)[cite: 4].

Order Fill Varsayımı:
- UNKNOWN[cite: 4].

Eksikler:
- FRAMA Channel "default" parametrelerinin sayısal değerleri.
- Swing Low/High tespiti için gerekli geriye dönük bar sayıları (pivot mantığı).
- Bar close onayı olup olmadığı[cite: 4].


## 3. MTC_V2 Modül Kararı

Producer:
- Var: FRAMA Channel breakout mantığı[cite: 2].

Entry Gate / Filter:
- Var: 200 EMA (MTC_V2'de halihazırda destekleniyor)[cite: 5].

Guard:
- Yok[cite: 2].

Confirmation Layer:
- Yok[cite: 2].

Exit Rule:
- Var: Opposite signal exit (MTC_V2'de halihazırda destekleniyor)[cite: 5].

SL/TP Method:
- Var: Swing SL (Ancak eksik kurallı)[cite: 4].

Trailing / BE Method:
- Yok[cite: 4].

Position Sizing / Money Management:
- Yok[cite: 4].

MTC_V2’ye tam strateji olarak alınmalı mı?
- Hayır[cite: 4].

Neden?
- Stratejinin ana koruma mekanizması (Swing SL) belirsizdir[cite: 7].
- Kurallar yetersizdir ve iddia edilen kâr oranları aldatıcıdır[cite: 7].
- Stratejideki filtre ve çıkış kuralları (EMA ve Opposite Exit) sistemimizde zaten çalışmaktadır[cite: 5].


## 4. Kurtarılacak Fikirler

Kurtarılacak Fikir 1:
- Tür: Producer[cite: 2]
- Ad: FRAMA Channel Breakout
- Mantık: Fraktal yapıya göre adaptif olarak hızlanan/yavaşlayan bir hareketli ortalama bandı çizip, bu bantların kırılımını raw sinyal (`long_raw`, `short_raw`) olarak kullanmak[cite: 1, 8].
- MTC_V2 Önerisi: Klasik hareketli ortalama kesişimleri veya Bollinger bantları yerine yatay piyasada (chop) daha az sahte sinyal üreten alternatif bir Producer olarak backlog'a eklenebilir[cite: 2, 5].
- Öncelik: P3[cite: 4]


## 5. Doğrulanmamış Video İddiaları

- Win Rate: ~%37 (Daily) [DOĞRULANMADI][cite: 3]
- Profit Factor: UNKNOWN [DOĞRULANMADI][cite: 3]
- Drawdown: UNKNOWN [DOĞRULANMADI][cite: 3]
- Aylık Getiri: UNKNOWN [DOĞRULANMADI][cite: 3]
- Backtest Süresi: Maksimum tarihsel veri ("thousands of trades") [DOĞRULANMADI][cite: 3]


## 6. Sonraki Adım

Codex Status Önerisi:
- SALVAGE_ONLY

Codex’e Verilecek Kısa Not:
- Tam stratejiyi reddet (kurallar eksik, SL belirsiz). Sadece FRAMA Channel mantığını (Fractal Adaptive Moving Average) araştırıp, yatay piyasa gürültüsünü filtreleme potansiyeli olan yeni bir "Producer" modülü olarak Python prototipinde bağımsız test et.