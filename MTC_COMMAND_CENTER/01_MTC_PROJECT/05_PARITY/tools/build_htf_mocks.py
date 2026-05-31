# -*- coding: utf-8 -*-
"""
Build HTF mock OHLCV files for PineTS request.security() from existing LTF (1h) mock klines.
- Input format: JSON array of Binance kline-like dicts with keys:
  openTime, open, high, low, close, volume, closeTime, quoteAssetVolume,
  numberOfTrades, takerBuyBaseAssetVolume, takerBuyQuoteAssetVolume, ignore
- Output format: same schema, aggregated to 2h/4h/1d buckets, with file names:
  {SYMBOL}-{tf}-{start}-{end}.json
- Alignment:
  * Buckets are aligned to UTC epoch multiples of tf_ms.
  * closeTime = bucket_start + tf_ms - 1 (inclusive end like Binance klines)
- Aggregation rules:
  * open  = first open
  * high  = max high
  * low   = min low
  * close = last close
  * volume, quoteAssetVolume, takerBuy* volumes = sum
  * numberOfTrades = sum

Usage (PowerShell):
  python "01_MASTER TEMPLATE_V2/05_PARITY/tools/build_htf_mocks.py" --symbol BTCUSDT.P --from-1h

Optionally pick a specific 1h file:
  python ".../build_htf_mocks.py" --input data/pinets_mock_binance/BTCUSDT.P-1h-1735603200000-1767139200000.json
"""
import argparse, json, os, re
from typing import List, Dict

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DATA_DIR = os.path.abspath(DATA_DIR)  # C:\LAB\tradingview-lab
MOCK_DIR = os.path.join(DATA_DIR, 'data', 'pinets_mock_binance')

RE_1H_FILE = re.compile(r"^(?P<sym>[^-]+)-1h-(?P<start>\d+)-(?P<end>\d+)\.json$")

def _load_klines(path: str) -> List[Dict]:
    with open(path, 'r', encoding='utf-8') as f:
        j = json.load(f)
    if not isinstance(j, list):
        raise ValueError('Expected JSON array of klines, got %r' % type(j))
    return j


def _bucket_start(ts_ms: int, tf_ms: int) -> int:
    return (ts_ms // tf_ms) * tf_ms


def _aggregate(bars: List[Dict], tf_ms: int) -> List[Dict]:
    if not bars:
        return []
    out = []
    i = 0
    n = len(bars)
    # assume input sorted by openTime asc
    while i < n:
        bt = _bucket_start(int(bars[i]['openTime']), tf_ms)
        be = bt + tf_ms
        j = i
        first = bars[i]
        o = float(first['open'])
        h = float(first['high'])
        l = float(first['low'])
        c = float(first['close'])
        vol = float(first['volume'])
        qvol = float(first.get('quoteAssetVolume', 0))
        ntr = int(first.get('numberOfTrades', 0))
        tb_base = float(first.get('takerBuyBaseAssetVolume', 0))
        tb_quote = float(first.get('takerBuyQuoteAssetVolume', 0))
        while j + 1 < n and int(bars[j+1]['openTime']) < be:
            j += 1
            b = bars[j]
            h = max(h, float(b['high']))
            l = min(l, float(b['low']))
            c = float(b['close'])
            vol += float(b['volume'])
            qvol += float(b.get('quoteAssetVolume', 0))
            ntr += int(b.get('numberOfTrades', 0))
            tb_base += float(b.get('takerBuyBaseAssetVolume', 0))
            tb_quote += float(b.get('takerBuyQuoteAssetVolume', 0))
        out.append({
            'openTime': bt,
            'open': _num(o),
            'high': _num(h),
            'low': _num(l),
            'close': _num(c),
            'volume': _num(vol),
            'closeTime': be - 1,
            'quoteAssetVolume': _num(qvol),
            'numberOfTrades': ntr,
            'takerBuyBaseAssetVolume': _num(tb_base),
            'takerBuyQuoteAssetVolume': _num(tb_quote),
            'ignore': '0',
        })
        i = j + 1
    return out


def _num(x):
    # keep few decimals; mimic typical JSON dumps without scientific notation
    if isinstance(x, int):
        return x
    return float(f"{float(x):.10f}")


def _write_klines(path: str, rows: List[Dict]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def _find_latest_1h(symbol: str) -> str:
    candidates = []
    for name in os.listdir(MOCK_DIR):
        m = RE_1H_FILE.match(name)
        if m and m.group('sym') == symbol:
            candidates.append(name)
    if not candidates:
        raise FileNotFoundError(f"No 1h mock files found for {symbol} under {MOCK_DIR}")
    # pick the one with max end
    def key(name):
        m = RE_1H_FILE.match(name)
        return int(m.group('end'))
    best = max(candidates, key=key)
    return os.path.join(MOCK_DIR, best)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', help='Path to 1h mock JSON file')
    ap.add_argument('--symbol', default='BTCUSDT.P')
    ap.add_argument('--tfs', default='2h,4h,1d', help='Comma list among 2h,4h,1d')
    args = ap.parse_args()

    in_path = args.input or _find_latest_1h(args.symbol)
    name = os.path.basename(in_path)
    m = RE_1H_FILE.match(name)
    if not m:
        raise ValueError(f"Input filename does not match pattern: {name}")
    sym = m.group('sym')
    start = int(m.group('start'))
    end = int(m.group('end'))

    bars = _load_klines(in_path)
    # ensure sorted
    bars.sort(key=lambda r: int(r['openTime']))

    tf_map = {
        '2h': 2*60*60*1000,
        '4h': 4*60*60*1000,
        '1d': 24*60*60*1000,
    }
    for tf in [t.strip() for t in args.tfs.split(',') if t.strip()]:
        if tf not in tf_map:
            raise SystemExit(f"Unsupported tf: {tf}")
        ms = tf_map[tf]
        agg = _aggregate(bars, ms)
        # drop leading/trailing partial buckets outside [start, end)
        agg = [r for r in agg if start <= int(r['openTime']) and int(r['closeTime']) < end]
        out_name = f"{sym}-{tf}-{start}-{end}.json"
        out_path = os.path.join(MOCK_DIR, out_name)
        _write_klines(out_path, agg)
        print(f"Wrote {tf}: {out_path} ({len(agg)} bars)")

if __name__ == '__main__':
    main()

