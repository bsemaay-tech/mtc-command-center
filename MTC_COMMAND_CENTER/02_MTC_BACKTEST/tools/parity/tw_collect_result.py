from __future__ import annotations

import json
import os
import socket
import struct
import base64
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR = REPO_ROOT / "MTC_COMMAND_CENTER" / "01_MTC_PROJECT" / "05_PARITY" / "_nightly"
CDP_URL = "ws://[::1]:9222/devtools/page/D0968DC0DD3140AE9F6A7D85CEDAEB8E"


def _ws_connect():
    parsed = urlparse(CDP_URL)
    host, port, path = parsed.hostname, parsed.port, parsed.path
    key = base64.b64encode(os.urandom(16)).decode()
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: [{host}]:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    ).encode()
    s = socket.create_connection((host, port), timeout=10)
    s.sendall(req)
    resp = b""
    while b"\r\n\r\n" not in resp:
        resp += s.recv(4096)
    return s


def _ws_send(s, obj, msg_id):
    payload = json.dumps({"id": msg_id, **obj}).encode()
    header = bytearray([0x81])
    l = len(payload)
    if l < 126:
        header.append(0x80 | l)
    elif l < (1 << 16):
        header.append(0x80 | 126)
        header.extend(struct.pack("!H", l))
    else:
        header.append(0x80 | 127)
        header.extend(struct.pack("!Q", l))
    mask = os.urandom(4)
    header.extend(mask)
    s.sendall(header + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))


def _ws_recv(s):
    b1, b2 = s.recv(2)
    l = b2 & 0x7F
    if l == 126:
        l = struct.unpack("!H", s.recv(2))[0]
    elif l == 127:
        l = struct.unpack("!Q", s.recv(8))[0]
    if b2 >> 7:
        mask = s.recv(4)
    data = b""
    while len(data) < l:
        data += s.recv(l - len(data))
    if b2 >> 7:
        data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
    return json.loads(data)


def _runtime_eval(expr: str) -> object:
    s = _ws_connect()
    try:
        msg_id = 1
        _ws_send(s, {"method": "Runtime.enable"}, msg_id)
        while True:
            m = _ws_recv(s)
            if m.get("id") == msg_id:
                break
        msg_id += 1
        _ws_send(
            s,
            {
                "method": "Runtime.evaluate",
                "params": {"expression": expr, "returnByValue": True},
            },
            msg_id,
        )
        while True:
            m = _ws_recv(s)
            if m.get("id") == msg_id:
                return m.get("result", {}).get("result", {}).get("value")
    finally:
        s.close()


def _extract_metrics(text: str) -> dict:
    want = ["Total P&L", "Max equity drawdown", "Total trades", "Profit factor", "Net P&L", "Sharpe ratio", "Sortino ratio"]
    metrics = {}
    parts = [line.strip() for line in text.splitlines() if line.strip()]
    for key in want:
        if key in parts:
            idx = parts.index(key)
            metrics[key] = parts[idx + 1] if idx + 1 < len(parts) else ""
    return metrics


def collect_case(case: dict) -> dict:
    text = _runtime_eval(
        "(() => Array.from(document.querySelectorAll('*')).map(el => (el.innerText||'').trim()).filter(Boolean).join('\\n'))()"
    ) or ""
    metrics = _extract_metrics(str(text))
    raw = {
        "case_no": case["case_no"],
        "symbol": "BINANCE:BTCUSDT.P",
        "interval": "60",
        "source": "manual-loaded TradingView chart",
        "status": "OK",
        "metrics": metrics,
    }
    return raw


def main() -> int:
    raise SystemExit("Use run_planned_cases.py to orchestrate cases.")


if __name__ == "__main__":
    raise SystemExit(main())
