# Trading Bot Dashboard (prototype)

Day/Swing trading bot terminal UI — static prototype, mock data only.
No broker, exchange, VPS or live connection; all controls are inert.

## Run

Open `index.html` directly in a browser, or serve the folder:

```
python -m http.server 8080 --directory MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/trading_bot_dashboard
```

then visit http://localhost:8080/.

## Files

- `index.html` — page skeleton: topbar, event banner, tabs, panels
- `styles.css` — dark terminal theme (design tokens in `:root`)
- `app.js` — renderers, canvas charts (candles + equity curve), tab logic
- `mock_data.js` — seeded synthetic data; its shape is the read-model contract
- `ARCHITECTURE.md` — full UI schema, page map, data contract, open points
