from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from src.chat_engine import ChatEngine


ENGINE = ChatEngine()


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _text(self, status: int, payload: str, content_type: str = "text/plain; charset=utf-8") -> None:
        body = payload.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._json(200, {"status": "ok"})
            return

        if self.path == "/":
            html = Path("web/index.html").read_text(encoding="utf-8")
            self._text(200, html, "text/html; charset=utf-8")
            return

        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/chat":
            self._json(404, {"error": "not_found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._json(400, {"error": "invalid_json"})
            return

        conversation_id = payload.get("conversation_id")
        message = payload.get("message")
        if not conversation_id or not message:
            self._json(400, {"error": "conversation_id_and_message_required"})
            return

        result = ENGINE.handle_message(conversation_id, message)
        self._json(200, result)


def run(host: str, port: int) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Server running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    run(args.host, args.port)
