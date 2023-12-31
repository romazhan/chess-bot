#-*- coding: utf-8 -*-
from configparser import ConfigParser

from models.engine import Engine
from models.server import (
    start_server, stop_server
)
from models.browser import (
    start_browser, stop_browser
)

import time, sys, os


_CONFIG_FILE_PATH = './config.ini'

def _main(confdad: ConfigParser) -> None:
    print('[*] starting...')

    engine = Engine({
        'Path': confdad['ENGINE'].get('PATH'),
        'Hash': confdad['ENGINE'].getint('HASH'),
        'Depth': confdad['ENGINE'].getint('DEPTH'),
        'UCI_Elo': confdad['ENGINE'].getint('ELO'),
        'Threads': confdad['ENGINE'].getint('THREADS'),
        'Contempt': confdad['ENGINE'].getint('CONTEMPT'),
        'Maximum Thinking Time': confdad['ENGINE'].getint('MOVE_MAX_TIME'),
        # 'Ponder': True # perhaps there is no point due to the constant change of position on FEN
    })

    server_addr = start_server(engine, confdad['SERVER'].getint('PORT'))

    start_browser({
        'hint_lighting': confdad['BROWSER'].getliststr('HINT_LIGHTING'),
        'start_url': confdad['BROWSER'].get('START_URL'),
        'server_addr': server_addr
    })

    stop_command = confdad['SURFACE'].get('STOP_COMMAND')
    print(f'\n[*] input "{stop_command}" to stop the server and browser')

    while True:
        if input('>>> ').lower() == stop_command:
            raise KeyboardInterrupt

if __name__ == '__main__':
    ROOT = os.path.dirname(sys.argv[0])
    ROOT and os.chdir(ROOT)

    confdad = ConfigParser(converters={
        'liststr': lambda l: [
            v.strip() for v in l.strip('[]').split(',')
        ]
    })
    assert confdad.read(_CONFIG_FILE_PATH), f'{_CONFIG_FILE_PATH} not found'

    def stop_all(msg: str, code: int = 0) -> None:
        stop_server(), stop_browser()

        print(f'\n{msg}')
        sys.exit(code)

    try:
        _main(confdad)
    except KeyboardInterrupt:
        stop_all('[!] server|browser stopped by the user')
    except Exception as e:
        e_message = f'[{time.strftime("%Y-%m-%d %H:%M")}]: {str(e) or "@empty"}'

        with open('error.log', 'a', encoding='utf-8') as f:
            f.write(f'{e_message}\n')

        stop_all(e_message, 1)
