from typing import Any
from threading import Thread
from http.server import (
    HTTPServer,
    BaseHTTPRequestHandler
)
from .engine import Engine
import json


_engine, _server, _server_thread = None, None, None

class _HttpRequestHandler(BaseHTTPRequestHandler):
    __slots__ = ()

    def log_message(self, *_: Any) -> None:
        pass

    def send_error(self, *_: Any) -> None:
        pass

    def do_headers(self) -> None:
        self.send_header('Access-Control-Allow-Origin', 'https://www.chess.com')

    def do_POST(self) -> None:
        self.send_response(200)
        self.do_headers()
        self.end_headers()

        fen = json.loads(self.rfile.read(
            int(self.headers.get('Content-Length'))
        ))['fen']

        try:
            self.wfile.write(_engine.get_best_move_by_fen(fen).encode('utf-8'))
            self.connection.shutdown(1)
        except ConnectionAbortedError:
            pass

def start_server(engine: Engine, port: int = 667) -> str:
    global _engine, _server, _server_thread

    host = '127.0.0.1'

    _engine = engine
    _server = HTTPServer((host, port), _HttpRequestHandler)
    _server_thread = Thread(target=_server.serve_forever)

    _server_thread.start()

    return f'http://{host}:{port}'

def stop_server() -> None:
    if _server_thread.is_alive():
        global _engine
        del _engine

        _server.shutdown()
