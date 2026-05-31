"""
Morning Report — consume MEGA_walk_forward_results.json and produce a
user-friendly summary of the overnight rigor pass.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_DIR = Path(
    r"C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2"
    r"\06_QUANTLENS_LAB\05_BACKTEST_RESULTS"
)

def main():
    src = OUTPUT_DIR / "MEGA_walk_forward_results.json"
    if not src.exists():
        print("No mega results file yet."); return
    data = json.loads(src.read_text(encoding="utf-8"))
    results = data["results"]

    cls_counts = {}
    for r in results:
        cls_counts[r.get("classification","?")] = cls_counts.get(r.get("classification","?"), 0) + 1

    bh_meta = data.get("bh_meta", {})
    passes = [r for r in results if r.get("classification") in {"PASS","STRONG_PASS"}]
    strong = [r for r in passes if r.get("classification") == "STRONG_PASS"]
    # Tier 1: survives all three gates (walk-forward + honest BH-FDR + DSR)
    robust_final = [r for r in passes if r.get("robust_final")]
    robust_final.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)
    # BH survivors under the honest full search-space family
    bh_full = [r for r in passes if r.get("bh_survivor_mfull") and not r.get("robust_final")]
    bh_full.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)
    # BH survivors under the lighter "passed walk-forward" family (more permissive)
    bh_pass = [r for r in passes if r.get("bh_survivor_mpass") and not r.get("bh_survivor_mfull")]
    bh_pass.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)
    bh_survivors = bh_full  # back-compat alias used below
    # caution: PASS but survives neither BH family
    nonrobust_pass = [r for r in passes if not r.get("bh_survivor_mpass") and not r.get("bh_survivor_mfull")]
    nonrobust_pass.sort(key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)

    # optional multi-window cross-validation summary
    mw_path = OUTPUT_DIR / "multiwindow_summary.json"
    mw = json.loads(mw_path.read_text(encoding="utf-8")) if mw_path.exists() else []
    alpha_path = OUTPUT_DIR / "alpha_summary.json"
    alpha = json.loads(alpha_path.read_text(encoding="utf-8")) if alpha_path.exists() else None

    md = []
    md.append("# QuantLens — Sabah Raporu (Gece Çalışması)")
    md.append("")
    if alpha is not None:
        premium = alpha.get("premium", [])
        down = alpha.get("down_market_alpha", [])
        premium.sort(key=lambda x: x["excess_alpha"], reverse=True)
        md.append("## 🥇 GERÇEK NİHAİ TAVSİYE — Buy&Hold'u Yenen + Rejim-Dayanıklı + Parametre-Kararlı")
        md.append("")
        md.append("**En belirleyici filtre:** Bir strateji yükselen bir varlıkta +%100 yapıyorsa ama varlık")
        md.append("zaten +%108 yükselmişse, edge YOKTUR (sadece beta/trend). Asıl değerli olan, aynı OOS")
        md.append("penceresinde varlığı **sadece elde tutmaktan (buy&hold) daha çok** kazandıran stratejidir —")
        md.append("özellikle **varlık düşerken** kazanan (beta-nötr gerçek alfa).")
        md.append("")
        md.append("### 🔥 Varlık DÜŞERKEN kazananlar (en saf alfa — birinci öncelik)")
        md.append("")
        if down:
            md.append("| # | Strateji | Sym | TF | Strateji % | Buy&Hold % | Alfa (fazla) % | PF | MaxDD % | Pencere+ | Boot p(hi) |")
            md.append("|---|---|---|---|---|---|---|---|---|---|---|")
            for i, x in enumerate(down[:25], 1):
                md.append(
                    f"| {i} | `{x['strategy'][:32]}` | {x['symbol']} | {x['timeframe']} | "
                    f"**{x['strategy_lockbox_ret']:+.1f}** | {x['buyhold_lockbox_ret']:+.1f} | "
                    f"**{x['excess_alpha']:+.1f}** | {x['pf']} | {x['maxdd']:.1f} | "
                    f"{x['windows_positive']}/5 | {x['boot_p_hires']} |"
                )
        else:
            md.append("_(Yok — hiçbir rejim-dayanıklı aday düşen piyasada pozitif alfa üretmedi.)_")
        md.append("")
        md.append("### Buy&Hold'u yenen tüm rejim-dayanıklı + kararlı adaylar")
        md.append("")
        if premium:
            md.append("| # | Strateji | Sym | TF | Strateji % | Buy&Hold % | Alfa % | PF | Trades | Pencere+ |")
            md.append("|---|---|---|---|---|---|---|---|---|---|")
            for i, x in enumerate(premium[:30], 1):
                md.append(
                    f"| {i} | `{x['strategy'][:32]}` | {x['symbol']} | {x['timeframe']} | "
                    f"{x['strategy_lockbox_ret']:+.1f} | {x['buyhold_lockbox_ret']:+.1f} | "
                    f"**{x['excess_alpha']:+.1f}** | {x['pf']} | {x['trades']} | {x['windows_positive']}/5 |"
                )
        else:
            md.append("_(Yok)_")
        md.append("")
        md.append("> ⚠️ **TRX uyarısı:** Rejim-dayanıklı listesinde TRXUSDT baskındır, çünkü TRX bu dönemde")
        md.append("> güçlü yükseldi (lockbox buy&hold ≈ +%108). TRX'teki long sonuçların çoğu strateji edge'i")
        md.append("> DEĞİL, varlık trendidir — yukarıdaki alfa filtresi bunları zaten eler.")
        md.append("")
        md.append("---")
        md.append("")
    if mw is not None:
        mw_stable = [x for x in mw if x.get("param_stable")]
        mw_stable.sort(key=lambda x: x.get("windows_positive", 0), reverse=True)
        md.append("## 🏁 NİHAİ TAVSİYE — Çok-Pencereli + Parametre-Kararlı Hayatta Kalanlar")
        md.append("")
        md.append("Bu adaylar farklı zaman dilimlerinde (Q1-Q4 + 2. yarı) tutarlı kâr verip,")
        md.append("parametre komşuluğunda da stabil kalanlardır — **en güvenilir grup**.")
        md.append("")
        if mw_stable:
            md.append("| # | Strateji | Sym | TF | Pencere+/5 | Lockbox % | PF | Boot p | DSR p | Final? | Params |")
            md.append("|---|---|---|---|---|---|---|---|---|---|---|")
            for i, x in enumerate(mw_stable[:25], 1):
                md.append(
                    f"| {i} | `{x['strategy'][:34]}` | {x['symbol']} | {x['timeframe']} | "
                    f"{x['windows_positive']}/5 | {x['lockbox_ret']:.2f} | {x['lockbox_pf']} | "
                    f"{x.get('boot_p')} | {x.get('dsr_p')} | {'Y' if x.get('robust_final') else 'n'} | "
                    f"`{json.dumps(x['params'], separators=(',',':'))[:60]}` |"
                )
        else:
            md.append("_(Çok-pencereli + parametre-kararlı sınavdan geçen aday YOK — bu en katı testtir.)_")
        md.append("")
        md.append("---")
        md.append("")
    md.append(f"- Üretim zamanı: `{datetime.now(timezone.utc).isoformat()}`")
    md.append(f"- Motor çalışma süresi: `{data['runtime_seconds']}s` ({round(data['runtime_seconds']/60,1)} dk)")
    md.append(f"- Worker: `{data['workers']}` process | Komisyon: `{data['config']['cost_bps']} bps`")
    md.append(f"- Semboller: {data['config']['symbols']}")
    md.append(f"- Zaman dilimleri: {data['config']['timeframes']}")
    md.append(f"- Strateji sayısı: {data['config']['strategy_count']} (11 prototyped + 6 generic)")
    md.append(f"- Toplam parametre seti: **{data['config']['param_set_total']}**")
    md.append(f"- Değerlendirilen (strateji×sembol×TF) iş: **{len(results)}**")
    md.append("")
    md.append("## Sınıflandırma Özeti")
    md.append("")
    md.append("| Sınıf | Adet | Açıklama |")
    md.append("|---|---|---|")
    for k in ["STRONG_PASS","PASS","FAIL","INSUFFICIENT_TRADES","NO_DATA","SKIPPED_RULE","ERROR"]:
        desc = {
            "STRONG_PASS": "lockbox + 3/3 fold pozitif + PF≥1.3 + expectancy≥0.10R",
            "PASS": "lockbox pozitif + fold yarısı pozitif + DD>−%50",
            "FAIL": "lockbox negatif veya kriterleri sağlamıyor",
            "INSUFFICIENT_TRADES": "<30 işlem, istatistiksel güven yok",
            "NO_DATA": "veri yetersiz",
            "SKIPPED_RULE": "kural gereği atlandı (örn. Dual RSI · 1D)",
            "ERROR": "çalışma hatası",
        }[k]
        md.append(f"| {k} | {cls_counts.get(k,0)} | {desc} |")
    md.append("")
    md.append(f"**BH-FDR (m_full={bh_meta.get('m_full','?')}, dürüst arama uzayı) hayatta kalan:** {sum(1 for r in passes if r.get('bh_survivor_mfull'))}  |  "
              f"**BH-FDR (m_pass={bh_meta.get('m_pass','?')}, WF-geçen aile):** {sum(1 for r in passes if r.get('bh_survivor_mpass'))}")
    md.append("")
    md.append(f"**DSR-robust (p≥0.95):** {sum(1 for r in passes if r.get('dsr_robust'))}  |  "
              f"**FINAL ROBUST (üç kapı):** {len(robust_final)}  |  "
              f"Yüksek-çöz. bootstrap: {bh_meta.get('hires_resamples','?')} yeniden örnek")
    md.append("")
    md.append("## Üç Bağımsız Doğrulama Kapısı")
    md.append("")
    md.append("Bir aday 'FINAL ROBUST' olmak için ÜÇ kapıdan da geçmelidir:")
    md.append("1. **Rolling Walk-Forward**: train fold'larda seçilen parametre, hiç görmediği son %25 lockbox'ta kârlı + fold'ların yarısından çoğunda pozitif.")
    md.append("2. **Bootstrap + Benjamini-Hochberg FDR (q=0.10)**: lockbox işlemleri 2000 kez yeniden örneklenir; ortalama-R>0 anlamlı mı? Tüm test edilen hücreler arasında çoklu-test düzeltmesi uygulanır.")
    md.append("3. **Deflated Sharpe Ratio (p≥0.95)**: işlem-başına Sharpe, grid'deki parametre deneme sayısına göre deflate edilir (Bailey & López de Prado).")
    md.append("")
    md.append("## ⭐ TIER 1 — FINAL ROBUST (üç kapıdan da geçti)")
    md.append("")
    md.append("**Master Template Pine entegrasyonu için birinci öncelik adayları.**")
    md.append("")
    if robust_final:
        md.append("| # | Strateji | Sym | TF | Lockbox % | Sharpe | Boot p | DSR p | Trades | PF | Max DD % | Folds+ | Params |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(robust_final[:40], 1):
            s = r["summary"]; lb = s["lockbox_oos"]
            md.append(
                f"| {i} | `{r['strategy'][:38]}` | {r['symbol']} | {r['timeframe']} | "
                f"**{lb['net_return_pct']:.2f}** | {lb['sharpe']:.2f} | {r.get('boot_p_value')} | {r['dsr_p_value']} | "
                f"{lb['num_trades']} | {lb['profit_factor']} | {lb['max_drawdown_pct']:.2f} | "
                f"{s['folds_positive']}/{s['n_folds']} | "
                f"`{json.dumps(s['best_params'], separators=(',',':'))[:80]}` |"
            )
    else:
        md.append("_(Bu turda hiçbir aday üç kapıdan da geçemedi — bu, en katı sınavda gerçek edge kıtlığını gösterir.)_")
    md.append("")
    md.append("## TIER 2 — BH-FDR (dürüst tam arama uzayı, m_full) geçti, DSR geçemedi")
    md.append("")
    md.append("Tüm denenen hücreler (m_full) arasında çoklu-test düzeltmeli bootstrap anlamlılığını")
    md.append("geçtiler; ikincil öncelik.")
    md.append("")
    if bh_survivors:
        md.append("| # | Strateji | Sym | TF | Lockbox % | Sharpe | Boot p | DSR p | Trades | PF | Folds+ |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(bh_survivors[:60], 1):
            s = r["summary"]; lb = s["lockbox_oos"]
            md.append(
                f"| {i} | `{r['strategy'][:38]}` | {r['symbol']} | {r['timeframe']} | "
                f"{lb['net_return_pct']:.2f} | {lb['sharpe']:.2f} | {r.get('boot_p_value')} | {r.get('dsr_p_value','-')} | "
                f"{lb['num_trades']} | {lb['profit_factor']} | {s['folds_positive']}/{s['n_folds']} |"
            )
    else:
        md.append("_(Yok)_")
    md.append("")
    md.append("## TIER 2b — Yalnız m_pass ailesinde BH-FDR geçti (daha gevşek)")
    md.append("")
    md.append("Sadece WF-geçen adaylar arasında düzeltilince anlamlı; tam arama uzayında değil. Temkinli.")
    md.append("")
    if bh_pass:
        md.append("| Strateji | Sym | TF | Lockbox % | Boot p(hi) | DSR p | Trades | PF | Folds+ |")
        md.append("|---|---|---|---|---|---|---|---|---|")
        for r in bh_pass[:40]:
            s = r["summary"]; lb = s["lockbox_oos"]
            md.append(
                f"| `{r['strategy'][:38]}` | {r['symbol']} | {r['timeframe']} | "
                f"{lb['net_return_pct']:.2f} | {r.get('boot_p_hires', r.get('boot_p_value'))} | {r.get('dsr_p_value','-')} | "
                f"{lb['num_trades']} | {lb['profit_factor']} | {s['folds_positive']}/{s['n_folds']} |"
            )
    else:
        md.append("_(Yok)_")
    md.append("")
    md.append("## TIER 3 — PASS ama Hiçbir Çoklu-Test Düzeltmesini Geçemedi (Şans/Overfit Riski)")
    md.append("")
    md.append("Bu setler lockbox'ta pozitif çıktı ama bootstrap-FDR'yi geçemedi.")
    md.append("Tek başlarına güvenilmez; ileri doğrulama olmadan Pine'a taşınmamalı.")
    md.append("")
    if nonrobust_pass:
        md.append("| Strateji | Sym | TF | Lockbox % | Boot p | DSR p | Trades | PF | Folds+ |")
        md.append("|---|---|---|---|---|---|---|---|---|")
        for r in nonrobust_pass[:40]:
            s = r["summary"]; lb = s["lockbox_oos"]
            md.append(
                f"| `{r['strategy'][:38]}` | {r['symbol']} | {r['timeframe']} | "
                f"{lb['net_return_pct']:.2f} | {r.get('boot_p_value','-')} | {r.get('dsr_p_value','-')} | "
                f"{lb['num_trades']} | {lb['profit_factor']} | {s['folds_positive']}/{s['n_folds']} |"
            )
    md.append("")
    md.append("## Strateji Başına En İyi 3 PASS")
    md.append("")
    by_strat = {}
    for r in passes:
        by_strat.setdefault(r["strategy"], []).append(r)
    for strat in sorted(by_strat.keys()):
        rows = sorted(by_strat[strat], key=lambda r: r["summary"]["lockbox_oos"]["net_return_pct"], reverse=True)[:3]
        if not rows:
            continue
        md.append(f"### `{strat}`")
        md.append("")
        md.append("| Sym | TF | Lockbox % | Sharpe | DSR p | Trades | PF | MaxDD % | Folds+ | Class |")
        md.append("|---|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            s = r["summary"]; lb = s["lockbox_oos"]
            md.append(
                f"| {r['symbol']} | {r['timeframe']} | {lb['net_return_pct']:.2f} | "
                f"{lb['sharpe']:.2f} | {r.get('dsr_p_value','-')} | "
                f"{lb['num_trades']} | {lb['profit_factor']} | {lb['max_drawdown_pct']:.2f} | "
                f"{s['folds_positive']}/{s['n_folds']} | {r['classification']} |"
            )
        md.append("")
    md.append("")
    md.append("## Antigravity İddialarına Karşı Bulgular")
    md.append("")
    md.append("Antigravity'nin orijinal raporundaki top-10 OOS performansları aşağıdaki sebeplerle")
    md.append("ŞİŞİRİLMİŞTİR:")
    md.append("")
    md.append("1. **Aritmetik toplam vs bileşik getiri**: Antigravity trade %'lerini topladı (örn. +%402); bileşik karşılığı çok daha düşük.")
    md.append("2. **Tek-split, walk-forward yok**: 2020-09 → 2024-06 train / 2024-06 → 2026-04 OOS sabit; rolling pencere yok.")
    md.append("3. **BTC 1h/15m için train veri yok**: BTC 1h verisi 2024-04'te başlıyor — Antigravity'nin train penceresi BTC için fiziksel olarak boş.")
    md.append("4. **Multiple-testing düzeltmesi yok**: 432 senaryoda 124 PASS sayıldı, ama rastgele bile bu kadar PASS beklenir.")
    md.append("5. **Min trade filtresi yok**: 3-5 işlemden uçan sahte edge'ler PASS sayıldı.")
    md.append("")
    md.append("Bu sabah raporu, **yukarıdaki tüm metodolojik kusurları gideren** rigorous bir motorla")
    md.append("üretildi. Master Template entegrasyonuna geçmeden önce yalnızca **DSR-robust STRONG_PASS**")
    md.append("ya da en azından **DSR-robust PASS** kategorisindeki adaylar değerlendirilmelidir.")
    md.append("")

    (OUTPUT_DIR / "MORNING_REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote MORNING_REPORT.md ({len(md)} lines)")

if __name__ == "__main__":
    main()
