# Transcript Intake Workflow

## Bu workflow ne yapar?

YouTube transcript geldiginde once ayni video daha once islenmis mi kontrol edilir. Sonra kanal kalite durumu kontrol edilir. Video strateji iceriyorsa QuantLens candidate workflow'a gider. Strateji yok ama faydali trader bilgisi varsa Trader Wiki'ye kaydedilir.

## Duplicate kontrolu

- Ayni video tekrar verilirse Codex islemi tekrarlamaz.
- `video_id` ve `transcript_hash` kontrol edilir.
- Duplicate ise yeni candidate olusturulmaz.
- Onceki candidate/status/path bilgisi raporlanir.

## Kanal kalite takibi

- Her transcript intake sonrasi kanal kalite registry'si guncellenir.
- Surekli STOP/REJECT ureten kanal once `WATCHLIST`, sonra gerekirse `BLACKLISTED` olur.
- Tek kotu video ile kanal blacklist'e alinmaz.
- SALVAGE ve WIKI_ONLY tamamen negatif sayilmaz.

## Blacklist davranisi

- BLACKLISTED kanal yeni video geldiginde default olarak REJECTED sayilir.
- Kullanici ozellikle islenmesini isterse MANUAL_REVIEW onerilir.
- Blacklist sebebi raporda yazilir.

## Trader Wiki

Strateji olmayan ama faydali videolar cop degildir. Risk yonetimi, psikoloji, piyasa yapisi, sistem gelistirme, backtest/optimization veya execution/fees bilgisi varsa `WIKI_ONLY` olarak `11_TRADER_WIKI` altina kaydedilir.

## MTC_V2.pine ne zaman degisir?

Transcript intake, duplicate check, channel quality veya Trader Wiki asamalarinda `MTC_V2.pine` degismez.
