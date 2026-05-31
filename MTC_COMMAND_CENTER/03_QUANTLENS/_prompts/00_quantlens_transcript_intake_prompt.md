# QuantLens Transcript Intake Prompt

Bu prompt, YouTube transcript veya video kaynak metni verildiginde duplicate kontrolu, kanal kalite kontrolu, strateji aday workflow'u ve Trader Wiki ayrimini yonetir.

## Kesin Kurallar

- `01_PINE/MTC_V2.pine` dosyasini degistirme.
- Production Python runner dosyalarini degistirme.
- Backtest veya optimization calistirma.
- Mevcut workflow'u bozma.
- Mevcut dosyalari overwrite etme; once oku.
- Secret, API key, webhook, broker hesabi veya exchange key yazma.
- Buyuk CSV, data bundle, cache veya optimization result olusturma.

## Girdi

Kullanicidan gelen video URL, transcript, baslik, kanal adi, kanal id veya QuantLens notlarini oku. Kanal bilgisi yoksa `UNKNOWN_CHANNEL` kullan ve blacklist karari verme.

## Is Akisi

1. URL normalize et ve `video_id` cikar:
   - `youtu.be/<id>`
   - `youtube.com/watch?v=<id>`
   - `youtube.com/shorts/<id>`
   - `si`, `t`, `list` gibi tracking parametrelerini yok say.
2. `normalized_url` uret:

```text
https://www.youtube.com/watch?v=<video_id>
```

3. Transcript metnini normalize et:
   - lowercase
   - fazla bosluklari temizle
   - timestamp satirlarini mumkunse temizle
   - noktalama farklarina asiri duyarlı olma
4. SHA256 veya benzeri `transcript_hash` uret.
5. `_registry/youtube_video_index.csv` icinde duplicate kontrolu yap.
6. `channel_blacklist.yaml` ve `channel_quality_registry.csv` ile kanal kalite kontrolu yap.
7. Transcriptte kodlanabilir trade stratejisi varsa mevcut candidate workflow'a devam et.
8. Strateji yok ama faydali trader/yatirim bilgisi varsa `WIKI_ONLY` olarak isle.
9. STOP / REJECT / SALVAGE / CANDIDATE durumlarinda video index ve channel quality registry guncellenir.
10. Her durumda finalde hangi dosyalarin olustugunu, hangilerine dokunulmadigini ve next action'i raporla.

## Duplicate Detection

Kontrol sirasi:

1. `video_id` indexte varsa islemi tekrar yapma.
2. `video_id` yok ama `transcript_hash` ayniysa olasi duplicate olarak islemi durdur.
3. Ayni kanal + ayni baslik + benzer transcript varsa `MANUAL_REVIEW` veya `POSSIBLE_DUPLICATE` raporla ve yeni candidate olusturma.

Duplicate durumunda:

- Yeni candidate olusturma.
- Candidate registry'ye yeni strateji kaydi yazma.
- Onceki `candidate_id`, status, folder path, first_seen_at ve last_seen_at bilgisini goster.
- `last_seen_at` ve `process_count` guncellenebilir.

Final duplicate formati:

```text
## Duplicate Video Detected

- Video daha once islendi.
- Previous Candidate ID:
- Previous Status:
- Previous Folder:
- First Seen:
- Last Seen:
- Yeni islem yapilmadi.
- MTC_V2 dosyalarina dokunulmadi.
```

## Channel Watchlist / Blacklist

Quality states:

- `UNKNOWN`
- `GOOD`
- `WATCHLIST`
- `BLACKLISTED`
- `MANUAL_REVIEW`

Kurallar:

- STOP ve REJECT kotu icerik sayilir.
- SALVAGE notr/faydali sayilir.
- CANDIDATE iyi sayilir.
- WIKI_ONLY faydali sayilir.
- Son 3 videodan en az 2 tanesi STOP veya REJECT ise `WATCHLIST`.
- Toplam en az 5 video islenmis, en az 4 STOP/REJECT ve hic CANDIDATE yoksa `BLACKLISTED`.
- Hem kotu videolar hem SALVAGE/CANDIDATE varsa `MANUAL_REVIEW`.
- En az 3 faydali cikti varsa `GOOD`.
- Tek kotu video ile kanal blacklist'e alinmaz.

Blacklist davranisi:

- Kanal `channel_blacklist.yaml` icinde BLACKLISTED ise transcript analizinden once uyar.
- Default davranis otomatik `REJECTED`.
- Kullanici o videoyu ozellikle istediyse `MANUAL_REVIEW` oner.
- Blacklist sebebini raporda yaz.

## Trader Wiki / WIKI_ONLY

`WIKI_ONLY` su durumda kullanilir:

- Kodlanabilir buy/sell stratejisi yok.
- Ama risk, position sizing, psikoloji, drawdown, piyasa yapisi, spread/slippage, backtest, optimization, algo sistem veya trader hatalari acisindan faydali bilgi var.

`WIKI_ONLY` durumunda:

- Candidate olusturma.
- Normal strategy candidate registry'ye strateji gibi ekleme.
- `11_TRADER_WIKI` altinda not olustur.
- `_registry/youtube_video_index.csv` icine `status = WIKI_ONLY` yaz.
- `channel_quality_registry.csv` icinde `wiki_count` artir.

Dosya adi:

```text
TW_YYYY-MM-DD_<TOPIC_SLUG>_<SHORT_VIDEO_SLUG>.md
```

Topic mapping:

- Risk / position sizing -> `01_RISK_MANAGEMENT`
- Psychology / discipline -> `02_TRADING_PSYCHOLOGY`
- Market structure / liquidity -> `03_MARKET_STRUCTURE`
- System design / algo workflow -> `04_SYSTEM_DEVELOPMENT`
- Backtest / optimization / overfit -> `05_BACKTESTING_AND_OPTIMIZATION`
- Fees / spread / slippage / execution -> `06_EXECUTION_AND_FEES`
- Diger -> `99_MISC`

Trader Wiki not formati:

```markdown
# Trader Wiki Note

## Metadata
- Wiki ID:
- Source URL:
- Video ID:
- Title:
- Channel:
- Date:
- Topic:
- Usefulness Score: [1-10]
- Tags:

## Kisa Ozet
- [...]

## Ana Dersler
- [...]
- [...]
- [...]

## MTC_V2 / Algo Trading Icin Baglanti
- [...]

## Uygulanabilir Notlar
- [...]

## Riskli veya Supheli Iddialar
- [...]

## Kaynak Transcript Notu
- Transcript arsiv path:
- Video index kaydi:
```

## Siniflandirma Secenekleri

- `STOP`
- `REJECT`
- `SALVAGE`
- `CANDIDATE`
- `WIKI_ONLY`
- `DUPLICATE`
- `NEEDS_MORE_INFO`

## Codex Status Onerisi

- `REJECTED`
- `SALVAGE_ONLY`
- `READY_FOR_PYTHON_PROTOTYPE`
- `NEEDS_MORE_INFO`
- `WIKI_ONLY`
- `DUPLICATE`
