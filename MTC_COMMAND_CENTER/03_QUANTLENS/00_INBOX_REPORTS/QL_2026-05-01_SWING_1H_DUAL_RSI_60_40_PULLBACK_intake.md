# QuantLens Intake Report

## Metadata
- Candidate ID: QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK
- Source URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_DUAL_RSI_60_40_SWING
- Title: Dual RSI 60/40 swing pullback strategy
- Channel: UNKNOWN_CHANNEL
- Transcript hash: 0085bb9a34bfa64ce8e0d99b3532a28da703023088af74d8171f22417860337a
- Intake date: 2026-05-01
- Intake status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE

## Kisa Ozet
Transcript, iki RSI kullanan trend-pullback stratejisini anlatir. Gunluk `RSI(7)` 60/40 seviyeleriyle ust zaman dilimi trendini belirler. `1h` grafikte ikinci `RSI(7)` pullback entry zamanlamasi icin kullanilir.

## Strateji Ozeti
- HTF trend: daily `RSI(7) > 60` ise long-only, daily `RSI(7) < 40` ise short-only.
- Sideways filtre: daily RSI `40-60` arasindaysa islem yok.
- Long setup: `1h RSI(7) < 40` ile pullback/oversold; sonra RSI tekrar `40` ustune cikar.
- Short setup: `1h RSI(7) > 60` ile pullback/overbought; sonra RSI tekrar `60` altina iner.
- Price action confluence: support/resistance, doji, engulfing, stall/reversal mumlari.
- Risk: swing low/high stop, `2R` target.

## Triage Karari
Kodlanabilir ve onceki genis RSI playbook'ten daha dar bir adaydir. Ilk prototipte candle pattern isimleri opsiyonel confirmation olarak ayrilmali; ana iskelet `daily RSI regime + 1h RSI pullback reclaim/reject` olmalidir.

## Dokunulmayan Alanlar
- `01_PINE/MTC_V2.pine` degistirilmedi.
- Production Python runner degistirilmedi.
- Backtest veya optimization calistirilmadi.
- TradingView browser automation kullanilmadi.
