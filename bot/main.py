from configparser import ConfigParser
from src.engine import Engine
from src.server import (
    start_server,
    stop_server
)
from src.browser import (
    start_browser,
    stop_browser
)
import time, sys, os


_CONFIG_FILE_PATH = './config.ini'
_ERROR_FILE_PATH = './error.log'

def _main(confdad: ConfigParser) -> None:
    print('[*] starting...')

    engine = Engine({
        'Path': confdad['ENGINE'].get('path'),
        'Hash': confdad['ENGINE'].getint('hash'),
        'Depth': confdad['ENGINE'].getint('depth'),
        'UCI_Elo': confdad['ENGINE'].getint('elo'),
        'Threads': confdad['ENGINE'].getint('threads'),
        'Contempt': confdad['ENGINE'].getint('contempt'),
        'Maximum Thinking Time': confdad['ENGINE'].getint('move_max_time')
    })

    server_addr = start_server(engine, confdad['SERVER'].getint('port'))

    start_browser(
        use_existing_profile=confdad['BROWSER'].getboolean('use_existing_profile'),
        start_url=confdad['BROWSER'].get('start_url'),
        server_addr=server_addr,
        hint_lighting=confdad['SURFACE'].gettuplestr('hint_lighting')
    )

    stop_commands = confdad['SURFACE'].gettuplestr('stop_commands')
    print(f'\n[*] input {'|'.join(stop_commands)} to stop the server and browser')

    while True:
        if input('>>> ').strip().lower() in stop_commands:
            raise KeyboardInterrupt

def _stop_all(msg: str, code: int = 0) -> None:
    stop_server(), stop_browser()

    print(f'\n{msg}')
    sys.exit(code)

if __name__ == '__main__':
    ROOT = os.path.dirname(sys.argv[0])
    ROOT and os.chdir(ROOT)

    confdad = ConfigParser(converters={
        'tuplestr': lambda s: tuple(
            v.strip() for v in s.strip('()').split(',')
        )
    })
    assert confdad.read(_CONFIG_FILE_PATH), f'{_CONFIG_FILE_PATH} not found'

    try:
        _main(confdad)
    except KeyboardInterrupt:
        _stop_all('[!] server|browser stopped by the user')
    except Exception as unknown_error:
        unknown_error_message = f'[{time.strftime('%d.%m.%Y, %H:%M:%S')}]: {str(unknown_error) or '__empty__'}'

        with open(_ERROR_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write(f'{unknown_error_message}\n')

        _stop_all(unknown_error_message, code=1)
