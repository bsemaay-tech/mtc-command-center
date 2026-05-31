# Golden Visual Cases

No exact chart data from the transcript is bundled in the repo. These golden cases are synthetic and are intended to verify visual behavior only.

| case | expected behavior |
|---|---|
| `GC_LONG_001` | A long pulse appears only after downside capitulation and a confirmed prior-bar-high break. |
| `GC_SHORT_001` | A short pulse appears only after upside exhaustion and a confirmed prior-bar-low break. |
| `GC_NONE_001` | Compression/range-bound bars around VWAP produce no signal. |
| `GC_AMBIG_001` | A weak bounce under VWAP without capitulation is rejected. |
| `GC_EXIT_001` | Debug exit fires when prior-bar-low trailing stop is breached. |
