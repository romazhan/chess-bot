#-*- coding: utf-8 -*-
from configparser import ConfigParser as _conf

from models.engine import Engine as _Engine
from models.server import start_server as _start_server,\
    stop_server as _stop_server
from models.browser import start_browser as _start_browser,\
    stop_browser as _stop_browser

import time as _time,\
    sys as _sys,\
    os as _os


def _main(c: _conf) -> None:
    print('[*] starting...')

    engine = _Engine({
        'Path': c['ENGINE'].get('PATH'),
        'Hash': c['ENGINE'].getint('HASH'),
        'Depth': c['ENGINE'].getint('DEPTH'),
        'UCI_Elo': c['ENGINE'].getint('ELO'),
        'Threads': c['ENGINE'].getint('THREADS'),
        'Contempt': c['ENGINE'].getint('CONTEMPT'),
        'Maximum Thinking Time': c['ENGINE'].getint('MOVE_MAX_TIME'),
        # 'Ponder': True # perhaps there is no point due to the constant change of position on FEN
    })

    server_addr = _start_server(engine, c['SERVER'].getint('PORT'))

    _start_browser({
        'hint_lighting': c['BROWSER'].getListStr('HINT_LIGHTING'),
        'start_url': c['BROWSER'].get('START_URL'),
        'server_addr': server_addr
    })

    stop_command = c['SURFACE'].get('STOP_COMMAND')
    print(f'\n[*] input "{stop_command}" to stop the server and browser')

    while True:
        if input('>>> ').lower() == stop_command:
            raise KeyboardInterrupt


if __name__ == '__main__':
    ROOT = _os.path.dirname(_sys.argv[0])
    ROOT and _os.chdir(ROOT)

    c = _conf(converters={'ListStr': lambda l: [
        v.strip() for v in l.strip('[]').split(',')
    ]})
    not c.read('./config.ini') and _sys.exit('config.ini not found')

    def stop_all(msg: str, code: int = 0) -> None:
        _stop_server(), _stop_browser()

        print(f'\n{msg}')
        _sys.exit(code)

    try:
        _main(c)
    except KeyboardInterrupt:
        stop_all('[!] server|browser stopped by the user')
    except Exception as e:
        error = f'[{_time.strftime("%Y-%m-%d %H:%M")}]: {e}'

        with open(c['SURFACE'].get('ERROR_LOG'), 'a', encoding='utf-8') as f:
            f.write(f'{error}\n')

        stop_all(error, 1)
