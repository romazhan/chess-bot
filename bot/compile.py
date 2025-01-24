import PyInstaller.__main__
import shutil, sys, os


_COMPILE_DIST_DIR_PATH = '.'
_COMPILE_TMP_DIR_PATH = './.tmp'
_COMPILE_EXE_FILENAME = 'ChessBot.exe'

def _main() -> None:
    if os.path.exists(_COMPILE_EXE_FILENAME):
        os.remove(_COMPILE_EXE_FILENAME)

    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--distpath', _COMPILE_DIST_DIR_PATH,
        '--workpath', _COMPILE_TMP_DIR_PATH,
        '--specpath', _COMPILE_TMP_DIR_PATH,
        '--name', _COMPILE_EXE_FILENAME
    ])

    shutil.rmtree(_COMPILE_TMP_DIR_PATH)

if __name__ == '__main__':
    os.chdir(os.path.dirname(sys.argv[0]) or '.')

    _main()
