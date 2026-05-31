# QuantLens Intake Report

## Metadata
- Candidate ID: QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR
- Source URL: https://youtu.be/mieguyQOe5k?si=V61DTOH71OOUmZ6d
- Video ID: UNKNOWN_VIDEO_2026-05-01_TWO_CANDLE_THEORY_SR
- Title: Two candle theory sentiment with support and resistance
- Channel: UNKNOWN_CHANNEL
- Transcript hash: 742fbc7184cfe33487fe568b9c9ca695c5a33aaccd5d0028a1b299794f449203
- Intake date: 2026-05-01
- Intake status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE

## Kisa Ozet
Transcript, klasik mum formasyonlarini ezberlemek yerine son iki mumla piyasa duyarliligini okumayi anlatir. Ana model iki parcadan olusur: mevcut mumun kapanisinin kendi range'i icindeki konumu ve mevcut kapanisin onceki mum range'ine gore yeri.

## Strateji Ozeti
- `close_position`: mevcut mum range'i uc esit bolgeye ayrilir; kapanis ust uc, orta uc veya alt uc olarak siniflandirilir.
- `close_comparison`: mevcut kapanis onceki mumun high seviyesinin ustunde, low seviyesinin altinda veya onceki mum range'i icinde mi diye bakilir.
- Iki siniflandirma birlestirilerek dokuz mum duyarliligi uretilir.
- `high close bull candle` en guclu bullish durumdur.
- `low close bear candle` en guclu bearish durumdur.
- Range mumlari taraflar arasi dengeyi ve hafif bias'i gosterir.
- Islem fikirleri support/resistance ile filtrelenir.

## Entry Fikirleri
- Long: resistance kirilimi sirasinda `high close bull candle` ve onceki bullish takip/follow-through.
- Long alternatif: support bolgesinde bearish mumun hemen ardindan guclu bullish recovery.
- Short: support kirilimi sirasinda `low close bear candle` ve bearish follow-through.
- Short alternatif: uptrend exhaustion sonrasi low-close range serisi ve ilk guclu bearish follow-through.

## Exit / Risk Fikirleri
- Ornek long stop: kirilim mumunun low seviyesi altinda.
- Ornek short stop: kirilim mumunun high seviyesi ustunde.
- Hedef: ornekte `1:1.5` risk-reward.
- Aktif cikis: trade icindeyken duyarlilik tersine donerse pozisyondan cik.

## Triage Karari
Kodlanabilir bir price-action sentiment adayidir. Ancak discretionary yorumlar fazla oldugu icin ilk prototip sadece mekanik iki mum state machine + support/resistance kirilim varyanti olmali.

## Dokunulmayan Alanlar
- `01_PINE/MTC_V2.pine` degistirilmedi.
- Production Python runner degistirilmedi.
- Backtest veya optimization calistirilmadi.
- TradingView browser automation kullanilmadi.
