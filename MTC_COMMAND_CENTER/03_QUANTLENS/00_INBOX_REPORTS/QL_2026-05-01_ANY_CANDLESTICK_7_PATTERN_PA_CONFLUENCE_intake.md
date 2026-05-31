# QuantLens Intake Report

## Metadata
- Candidate ID: QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE
- Source URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_CANDLESTICK_7_PATTERNS_PA
- Title: Seven candlestick patterns with price action confluence
- Channel: UNKNOWN_CHANNEL
- Transcript hash: f1b081079871e2770315c4848206bf2081e8067bfa2282f5ebed392646801a73
- Intake date: 2026-05-01
- Intake status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE

## Kisa Ozet
Transcript, yedi mum formasyonunu ve bunlari support/resistance ile trendline confluence kullanarak trade fikrine cevirmeyi anlatir.

## Strateji Ozeti
- Tek mum: bullish pin bar, bearish pin bar, doji.
- Iki mum: bullish engulfing, bearish engulfing.
- Uc mum: morning star, evening star.
- Long ornekleri: support uzerinde morning star veya trendline yakininda bullish engulfing.
- Short ornegi: resistance uzerinde evening star.
- Stop: formasyonun/pin bar/doji/sinyal mumunun arkasinda.
- Target: sonraki resistance/support veya onceki swing high/low.

## Triage Karari
Kodlanabilir fakat genis bir candlestick playbook. Ilk prototipte tum yedi formasyon birlikte kullanilmamali. En temiz ilk varyant: support/resistance confluence ile bullish/bearish engulfing veya morning/evening star.

## Dokunulmayan Alanlar
- `01_PINE/MTC_V2.pine` degistirilmedi.
- Production Python runner degistirilmedi.
- Backtest veya optimization calistirilmadi.
- TradingView browser automation kullanilmadi.
