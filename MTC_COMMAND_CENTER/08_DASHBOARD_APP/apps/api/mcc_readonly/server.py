from __future__ import annotations

import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .health import build_health_report
from .read_model import build_dashboard_snapshot_cached, build_read_model


class MCCReadOnlyHandler(BaseHTTPRequestHandler):
    mcc_root: Path | None = None

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path.rstrip("/") or "/"
        if route == "/dashboard":
            self._send_static_file("index.html")
            return
        if route.startswith("/web/"):
            self._send_static_file(route.removeprefix("/web/"))
            return
        if route == "/":
            self._send_json(
                {
                    "service": "mcc-readonly-api",
                    "mode": "read_only",
                    "endpoints": ["/dashboard", "/healthz", "/api/read-model", "/api/snapshot", "/api/report"],
                }
            )
            return
        if route == "/healthz":
            self._send_json(build_health_report(self.mcc_root))
            return
        if route == "/api/read-model":
            self._send_json(build_read_model(self.mcc_root))
            return
        if route == "/api/snapshot":
            query = parse_qs(parsed.query)
            force_refresh = query.get("refresh", ["0"])[0] in {"1", "true", "TRUE", "yes"}
            self._send_json(build_dashboard_snapshot_cached(self.mcc_root, force_refresh=force_refresh))
            return
        if route == "/api/report":
            self._send_report(parse_qs(parsed.query).get("path", [""])[0])
            return
        self._send_json({"error": "not found", "path": route}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        self._send_json({"error": "MVP-1 API is read-only"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    def do_PUT(self) -> None:
        self._send_json({"error": "MVP-1 API is read-only"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    def do_PATCH(self) -> None:
        self._send_json({"error": "MVP-1 API is read-only"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    def do_DELETE(self) -> None:
        self._send_json({"error": "MVP-1 API is read-only"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_static_file(self, rel_path: str) -> None:
        root = self._web_root()
        requested = (root / rel_path).resolve(strict=False)
        if not str(requested).startswith(str(root)):
            self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)
            return
        if not requested.exists() or not requested.is_file():
            self._send_json({"error": "not found", "path": rel_path}, status=HTTPStatus.NOT_FOUND)
            return

        content_type = mimetypes.guess_type(str(requested))[0] or "application/octet-stream"
        data = requested.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _web_root(self) -> Path:
        if self.mcc_root:
            return (self.mcc_root / "08_DASHBOARD_APP" / "apps" / "web").resolve(strict=False)
        return Path(__file__).resolve().parents[2] / "web"

    def _send_report(self, rel_path: str) -> None:
        if not rel_path:
            self._send_json({"error": "missing report path"}, status=HTTPStatus.BAD_REQUEST)
            return

        snapshot = build_dashboard_snapshot_cached(self.mcc_root)
        reports = snapshot.get("report_manifest", {}).get("reports", [])
        report = next((item for item in reports if item.get("path") == rel_path), None)
        if report is None:
            self._send_json({"error": "report is not in manifest", "path": rel_path}, status=HTTPStatus.NOT_FOUND)
            return

        root = self._mcc_root()
        reports_root = (root / "04_REPORTS").resolve(strict=False)
        target = (root / rel_path).resolve(strict=False)
        try:
            target.relative_to(reports_root)
        except ValueError:
            self._send_json({"error": "report path is outside 04_REPORTS", "path": rel_path}, status=HTTPStatus.FORBIDDEN)
            return

        if not target.exists() or not target.is_file():
            self._send_json({"error": "report file is missing", "path": rel_path}, status=HTTPStatus.NOT_FOUND)
            return

        try:
            content = target.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            self._send_json({"error": f"report is not valid utf-8: {exc}", "path": rel_path}, status=HTTPStatus.UNPROCESSABLE_ENTITY)
            return
        except OSError as exc:
            self._send_json({"error": f"report read error: {exc}", "path": rel_path}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        suffix = target.suffix.lower()
        content_type = "text/markdown" if suffix == ".md" else "text/plain"
        self._send_json(
            {
                "schema_version": "1.0",
                "mode": "read_only",
                "report": report,
                "path": rel_path,
                "content_type": content_type,
                "size_bytes": len(content.encode("utf-8")),
                "content": content,
            }
        )

    def _mcc_root(self) -> Path:
        if self.mcc_root:
            return self.mcc_root.resolve(strict=False)
        return Path(__file__).resolve().parents[4]


def make_server(host: str, port: int, mcc_root: str | Path | None = None) -> ThreadingHTTPServer:
    class Handler(MCCReadOnlyHandler):
        pass

    Handler.mcc_root = Path(mcc_root).resolve(strict=False) if mcc_root else None
    return ThreadingHTTPServer((host, port), Handler)


def serve(host: str = "127.0.0.1", port: int = 8765, mcc_root: str | Path | None = None) -> None:
    server = make_server(host, port, mcc_root)
    try:
        print(f"mcc-readonly-api listening on http://{host}:{port}")
        server.serve_forever()
    finally:
        server.server_close()
