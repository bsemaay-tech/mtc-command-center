# QuantLens Lab

## Amac

Bu klasor, Gemini QuantLens tarafindan YouTube strateji videolarindan uretilen raporlari MTC_V2 icin arsivlemek, siniflandirmak, Python prototype/backtest asamasina hazirlamak ve basarili adaylari parity-first Pine/Python entegrasyon surecine tasimak icin kullanilir.

Transcript intake ayrica duplicate video kontrolu, kanal kalite takibi ve Trader Wiki bilgi arsivi saglar.

## Workflow

```text
YouTube video
↓
Gemini QuantLens report
↓
Codex candidate intake
↓
Python prototype
↓
Multi-symbol walk-forward validation
↓
Backtest pass/promising decision
↓
Parity promotion
↓
Pine/Python feature-gated integration
↓
Final archive / approved list
```

```text
YouTube transcript
↓
Duplicate check
↓
Channel quality check
↓
If strategy exists: QuantLens candidate workflow
↓
If no strategy but useful knowledge: Trader Wiki
↓
If duplicate: stop and report previous record
```

## En onemli klasorler

- `00_INBOX_REPORTS`: Ham QuantLens raporlari.
- `01_TRIAGED_CANDIDATES`: Incelenmis adaylar.
- `04_PYTHON_PROTOTYPES`: Izole prototype asamasina hazir adaylar.
- `05_BACKTEST_RESULTS`: Validation ve walk-forward ciktilari.
- `06_PROMOTED_TO_PARITY`: Feature contract ve parity hazirlik paketleri.
- `11_TRADER_WIKI`: Strateji olmayan ama faydali trader/yatirim bilgileri.
- `_registry`: Ana takip CSV/JSONL dosyalari.
- `_prompts`: Codex'e dogrudan verilecek promptlar.
- `_user_guide`: Baris icin kisa kullanim rehberi.

## Hizli baslangic

1. YouTube videosunu Gemini QuantLens'e ver.
2. STOP raporu gelirse birak.
3. Rapor uygunsa `06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md` ile Codex'e ver.
4. Transcript dogrudan verilecekse `06_QUANTLENS_LAB\_prompts\00_quantlens_transcript_intake_prompt.md` kullan.
5. Candidate ID ve status icin `_registry\quantlens_candidate_registry.csv` kontrol edilir.
6. Video/kanal tekrar kontrolu icin `_registry\youtube_video_index.csv` ve `_registry\channel_quality_registry.csv` kontrol edilir.
7. Gece kucuk batch icin `05_quantlens_nightly_batch_prompt.md` kullanilir.

## Yapay zeka ilk ne okumali?

Once `06_QUANTLENS_LAB\_user_guide\06_WHAT_AI_SHOULD_READ_FIRST.md` dosyasini oku.

## Production code safety warning

Bu lab klasoru production kod degildir. Intake, duplicate check, channel quality, Trader Wiki, prototype, backtest result ve parity promotion asamalarinda `01_PINE/MTC_V2.pine` ve production Python runner dosyalari degismez. Pine/Python entegrasyon sadece final integration asamasinda, default OFF ve feature-gated planla yapilabilir.
