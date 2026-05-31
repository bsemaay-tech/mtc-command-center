# QuantLens Intake Report

## Metadata
- Candidate ID: QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP
- Source URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_BOLLINGER_BANDS_BREAKOUT_REVERSAL_PULLBACK
- Title: Bollinger Bands 20/2 breakout reversal and pullback setups
- Channel: UNKNOWN_CHANNEL
- Transcript hash: 19fc0518715c9aa3f259a52428a394cb766b7282cdfc64d072a29bc1bbc3f24b
- Intake date: 2026-05-01
- Intake status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE

## Kisa Ozet
Transcript, Bollinger Bands `20 SMA` ve `2` standart sapma ayarlariyla volatilite rejimi okuma ve uc setup anlatir: breakout, reversal ve trend pullback.

## Strateji Ozeti
- Dar band: dusuk volatilite, range/sideways ortam.
- Genis band: yuksek volatilite, trend/momentum ortam.
- Breakout: dar band/range sonrasi guclu mumun upper/lower band disinda kapanmasi.
- Reversal: dar/range ortamda upper band temasindan short, lower band temasindan long.
- Pullback: uptrendde fiyat upper-middle band arasinda kalirken middle band pullback long; downtrendde middle-lower band arasinda kalirken middle band pullback short.
- Ek confluence: support/resistance, candlestick pattern, trendline.

## Triage Karari
Kodlanabilir ama uc farkli rejim/setup ayni aday icinde. Ilk prototip tek varyanta indirilmeli. En temiz ilk varyant: Bollinger squeeze/range breakout veya middle-band trend pullback.

## Dokunulmayan Alanlar
- `01_PINE/MTC_V2.pine` degistirilmedi.
- Production Python runner degistirilmedi.
- Backtest veya optimization calistirilmadi.
- TradingView browser automation kullanilmadi.
