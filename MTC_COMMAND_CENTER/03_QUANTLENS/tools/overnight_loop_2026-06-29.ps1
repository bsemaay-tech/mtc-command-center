# MTC overnight multi-asset sweep — supervisor loop (auto-resume, deadline-bounded)
# Generated 2026-06-29. Resumable via mega_walk_forward --resume checkpoint.
$ErrorActionPreference = "Continue"
$deadline = Get-Date "2026-06-30 08:30:00"
$done   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_multiasset_2026-06-29\_DONE.marker"
$ckpt   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_multiasset_2026-06-29\checkpoint.pkl"
$log    = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_multiasset_2026-06-29\loop.log"
$env:MEGA_BUNDLE_MANIFEST = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
$env:MEGA_OUTPUT_DIR      = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_multiasset_2026-06-29"
$env:MEGA_WORKERS         = "20"
$env:PYTHONUTF8           = "1"
$env:OMP_NUM_THREADS      = "1"
$env:MKL_NUM_THREADS      = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:NUMEXPR_NUM_THREADS  = "1"
Set-Location "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"

"[loop] start $(Get-Date -Format o) workers=20 deadline=$deadline" | Out-File -Append -Encoding utf8 $log
while ((Get-Date) -lt $deadline) {
    if (Test-Path $done) { "[loop] DONE marker present, exit $(Get-Date -Format o)" | Out-File -Append -Encoding utf8 $log; break }
    "[loop] launch attempt $(Get-Date -Format o)" | Out-File -Append -Encoding utf8 $log
    python mega_walk_forward.py --resume "$ckpt" --checkpoint-every 20 --partial-json "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_multiasset_2026-06-29\MEGA_walk_forward_partial.json" --symbol AAPL --symbol AAVEUSD --symbol AMD --symbol AMZN --symbol AVAXUSD --symbol BCHUSD --symbol BNO --symbol BTCUSD --symbol CPER --symbol DBC --symbol DIA --symbol DOGEUSD --symbol DOTUSD --symbol EEM --symbol EFA --symbol ETHUSD --symbol FXI --symbol GLD --symbol GOOGL --symbol HYG --symbol IEF --symbol IWM --symbol LINKUSD --symbol LQD --symbol LTCUSD --symbol META --symbol MSFT --symbol NFLX --symbol NVDA --symbol QQQ --symbol SHIBUSD --symbol SLV --symbol SOLUSD --symbol SPY --symbol TLT --symbol TSLA --symbol UNG --symbol UNIUSD --symbol USO --symbol VXX --symbol XLB --symbol XLC --symbol XLE --symbol XLF --symbol XLI --symbol XLK --symbol XLP --symbol XLRE --symbol XLU --symbol XLV --symbol XLY --tf 10m --tf 15m --tf 30m --tf 1h --tf 2h --tf 4h --tf 1d 2>&1 | Out-File -Append -Encoding utf8 $log
    $ec = $LASTEXITCODE
    "[loop] exit code=$ec at $(Get-Date -Format o)" | Out-File -Append -Encoding utf8 $log
    if ($ec -eq 0) { "ALL_DONE $(Get-Date -Format o)" | Out-File -Encoding utf8 $done; break }
    # crash / kill / power-return mid-run: brief backoff then resume from checkpoint
    Start-Sleep -Seconds 20
}
"[loop] supervisor finished $(Get-Date -Format o)" | Out-File -Append -Encoding utf8 $log
