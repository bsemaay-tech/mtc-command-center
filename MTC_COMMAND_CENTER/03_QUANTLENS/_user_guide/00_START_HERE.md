# QuantLens Lab Start Here

## Bu workflow nedir?

QuantLens Lab, YouTube strateji videolarindan gelen Gemini QuantLens raporlarini MTC_V2 icin kontrollu aday kayitlarina donusturur. Amac once arsiv, sonra triage, sonra Python prototype, sonra bounded validation, sonra parity-first entegrasyon hazirligidir.

Transcript intake artik duplicate detection, kanal kalite takibi ve Trader Wiki ayrimini da yapar.

## Baris'in gorevi nedir?

1. YouTube videosu bul.
2. Gemini QuantLens'e ver.
3. STOP raporu gelirse birak.
4. Uygun rapor gelirse Codex'e intake promptuyla ver.
5. Gece icin nightly batch promptunu calistir.
6. Sabah registry ve backtest sonuclarini Codex'e ozetlet.

## Yapay zekanin gorevi nedir?

Raporu arsivlemek, duplicate kontrolu yapmak, kanal kalite registry'sini guncellemek, aday klasoru olusturmak, riskleri siniflandirmak, deney plani hazirlamak ve sadece uygun asamada bounded validation veya parity hazirligi onermek.

## Yeni YouTube videosu geldiginde ne yapilir?

Video once Gemini QuantLens'e verilir. QuantLens STOP derse workflow biter. Rapor uygunsa Codex'e `06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md` ile verilir.

Transcript dogrudan verilecekse `06_QUANTLENS_LAB\_prompts\00_quantlens_transcript_intake_prompt.md` kullanilir. Ayni videoyu yanlislikla tekrar vermek sorun degildir; sistem duplicate kontrolu yapar ve onceki kaydi raporlar.

Strateji yok ama faydali trader/yatirim bilgisi varsa video cope atilmaz; `11_TRADER_WIKI` altina `WIKI_ONLY` notu olarak kaydedilir.

## QuantLens raporu geldikten sonra ne yapilir?

Codex raporu `00_INBOX_REPORTS` icine kaydeder, Candidate ID uretir, candidate klasoru acar ve registry gunceller.

## Gece calisma nasil baslatilir?

`05_quantlens_nightly_batch_prompt.md` kullanilir. Limit verilmezse kucuk guvenli batch secilir.

## Sabah sonuc nasil kontrol edilir?

`_registry\quantlens_candidate_registry.csv`, `_registry\youtube_video_index.csv`, `_registry\channel_quality_registry.csv`, `05_BACKTEST_RESULTS\nightly_summary_YYYY-MM-DD.md` ve ilgili candidate sonuc klasorleri Codex'e ozetletilir.

## Hangi dosya/klasor ne ise yarar?

- `00_INBOX_REPORTS`: Ham QuantLens raporlari.
- `01_TRIAGED_CANDIDATES`: Incelenmis adaylar.
- `02_REJECTED`: Uygunsuz raporlar.
- `03_SALVAGE_IDEAS`: Sadece fikir olarak kullanilabilecek parcalar.
- `04_PYTHON_PROTOTYPES`: Izole prototype adaylari.
- `05_BACKTEST_RESULTS`: Bounded validation ve walk-forward sonuclari.
- `06_PROMOTED_TO_PARITY`: Parity hazirligina yukselen adaylar.
- `07_PINE_INTEGRATION_PLANS`: Kod degil, entegrasyon planlari.
- `08_PARITY_RESULTS`: PineTS/Python/TradingView karsilastirma sonuclari.
- `09_APPROVED_FOR_MTC`: Default OFF ve feature-gated onay adaylari.
- `11_TRADER_WIKI`: Strateji olmayan ama faydali trader/yatirim bilgileri.
- `_registry`: Ana takip dosyalari.
- `_prompts`: Codex'e dogrudan verilecek promptlar.
- `_templates`: Aday ve sonuc sablonlari.
- `_skills`: Tekrarlanabilir Codex skill talimatlari.

## MTC_V2.pine ne zaman degisir?

Sadece final Pine integration asamasinda. O asamaya kadar hicbir intake, prototype, backtest, Trader Wiki, duplicate check veya parity promotion isi `MTC_V2.pine` degistirmez.
