#-*- coding: utf-8 -*-
from .engine import Engine as _Engine

from http.server import HTTPServer as _HttpServer,\
    BaseHTTPRequestHandler as _BaseHttpRequestHandler
from threading import Thread as _Thread

import json as _json


_engine, _server, _server_thread = None, None, None


class _HttpRequestHandler(_BaseHttpRequestHandler):
    def log_message(self, *_: any) -> None:
        pass

    def send_error(self, *_: any) -> None:
        pass

    def do_headers(self) -> None:
        self.send_header('Access-Control-Allow-Origin', 'https://www.chess.com')

    def do_POST(self) -> None:
        self.send_response(200)
        self.do_headers()
        self.end_headers()

        fen = _json.loads(self.rfile.read(
            int(self.headers.get('Content-Length'))
        ))['fen']

        def get_best_move(fen: str) -> str:
            try:
                _engine.set_fen_position(fen)
                return _engine.get_best_move_time() or ''
            except Exception as e:
                print(f'[server][engine][error]: {e}')
                print(f'[server][engine]: restarting...')

                _engine.restart()
                return get_best_move(fen) # ? infinite recursion

        self.wfile.write(get_best_move(fen).encode('utf-8'))
        self.connection.shutdown(1)


def start_server(engine: _Engine, port: int = 667) -> str:
    global _engine, _server, _server_thread

    host = '127.0.0.1'

    _engine = engine
    _server = _HttpServer((host, port), _HttpRequestHandler)
    _server_thread = _Thread(target=_server.serve_forever)

    _server_thread.start()

    return f'http://{host}:{port}'


def stop_server() -> None:
    if _server_thread.is_alive():
        global _engine
        del _engine

        _server.shutdown()
