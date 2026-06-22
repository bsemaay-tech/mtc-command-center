# Pilot — Claude-Video (`bradautomates/claude-video`)

**Date:** 2026-06-22 · **By:** Claude Opus 4.8 · **Branch:** `feature/claude-video-pilot` ·
**Verdict:** ⏸️ DEFER / DO-NOT-INSTALL the tool. The frame-analysis value (catch settings the
transcript misses) **only triggers when the video shows real platform UI / indicator config**.
For animated explainer / price-action videos the transcript already carries 100% of the strategy,
so frames add ~nothing. When frames *are* worth it, the pipeline is **trivially reproducible with
tools already on the machine** — no third-party repo needed.

## What
`bradautomates/claude-video` — extracts frames (ffmpeg) + audio transcript (Whisper/captions) from
a video so Claude can analyse it as image + text. Backlog thesis (E1): for trading-strategy videos
it should "capture indicator settings / SL-TP lines / TradingView panel values that the transcript
alone misses." Proposed A/B: **transcript-only vs transcript+frames on one strategy video.**

## Evaluation method (real input, Barış-supplied)
Video: TradingLab — *"Stop Taking Trades Until You See This (Pullback)"*
(`youtu.be/Ju-cTa_dHAk`, 9m52s / 592s). Pullback + supply/demand structure strategy → directly
relevant to MTC's pullback family (e.g. `8EMA_PULLBACK`).

Reproduced the claude-video pipeline **manually, without installing the repo** (all ephemeral in
`C:\tmp\claude_video_pilot`, nothing in the MTC tree):
1. `yt-dlp.exe` (single-file binary, no pip) → 720p mp4 (24 MB) + English **auto-caption** (vtt).
   No Whisper needed → zero transcription cost.
2. `ffmpeg` (already installed, `Gyan.FFmpeg` 8.1.1) → 24 frames @ 1 per 25 s, 1280px, 716 KB total.
3. Cleaned vtt → transcript (1855 words). **A/B:** extracted the strategy from transcript-only,
   then from a 12-frame even sample, and compared.

## A/B result

**Transcript-only already yields the full, unambiguous strategy:**
- Trend = HH/HL (up) vs LH/LL (down).
- **Valid low/high (BOS-style):** a low only counts if it broke the prior high; trend flips only
  when a candle **closes** beyond the valid level (wick-through = trap, invalid).
- **Zone = the candle that *started* a sharp impulse** (rectangle high→low); gradual move = invalid.
- **Entry** on pullback into the zone; **SL** just beyond the zone; **TP** at prior low/high.
- Worked Nvidia example: $90k, SL 2% = $1,800, TP 20% = $18,000 (≈1:10 R:R).

**Frames added essentially zero strategy information.** The 12 sampled frames are an **animated
explainer**: schematic candles, coloured supply/demand rectangles, and meme cutaways (caveman
"BUY LOW SELL HIGH", Princess Bride, thumbs-up). There is **no real TradingView chart, no indicator
panel, no numeric settings, no ticker/timeframe overlay** to recover — because the strategy uses
**no indicators** (pure price-action structure). Frames only re-confirmed visuals the transcript
already described (zone = impulse candle; quiz answer "C").

## Decisive finding — value is conditional on content type
The backlog's value thesis ("captures settings the transcript missed") is **content-gated**:
- **Indicator-config screencast** (real platform UI: EMA length, RSI period, drawn SL/TP prices,
  timeframe selector) → frames *can* recover numbers absent from speech. **Value: HIGH.**
- **Animated explainer / pure price-action** (this video) → no on-screen settings exist; transcript
  is already complete. **Value: ~ZERO.**
This one is the second class, so the pilot's honest result is *no incremental value here* — not a
failure of the idea, a mismatch of input.

## Second finding — the tool itself is unnecessary
The whole pipeline ran with **ffmpeg (already present) + a one-file `yt-dlp.exe` + auto-captions +
Claude's native image Read**. The `bradautomates/claude-video` repo adds no capability we lack and
would be another dependency to vet/maintain. Whisper (a heavy install) was avoidable because
YouTube auto-captions exist.

## §6 checklist
- [x] real input used — yes (Barış-supplied YouTube strategy video)
- [x] Windows / install — pipeline = ffmpeg (installed) + `yt-dlp.exe` (single binary, `C:\tmp`)
- [x] local-only — download + frames + captions all local; only Claude vision is API
- [x] read-only to repo — all artifacts in `C:\tmp\claude_video_pilot`; nothing written to MTC tree
- [!] **incremental value (this input)** — none; transcript-complete, no on-screen settings
- [!] **tool needed?** — no; pipeline reproducible with already-installed tools
- [x] denylist — no pine/parity/MTC_V2/schema/broker touch
- [x] cost discipline — auto-captions (no Whisper); 12 frames (not 24) read on vision

## Decision
- **DEFER / do-not-install** `bradautomates/claude-video`.
- **On-demand pipeline (use only when a video shows real platform UI / indicator settings):**
  `yt-dlp` (video + `--write-auto-sub`) → `ffmpeg -vf "fps=1/N,scale=1280:-1"` (sparse frames) →
  Claude reads transcript first, then frames **only to fill numeric gaps** (indicator periods,
  drawn price levels, timeframe). Whisper only if a video has no captions.
- **Re-open / actually frame-analyse** when the input is an **indicator-configuration screencast**
  — that is the only class where frames beat transcript for MTC strategy ingestion.
- For *this* video, route the (already complete) transcript through normal user-intake
  (`route_user_intake.py`); it needs no frame step.
- `C:\tmp\claude_video_pilot` is ephemeral/deletable.
