# Chess Bot

>♟️ Chess Bot for [Chess.com](https://www.chess.com) on Python

Chess Bot consists of a local `server` on which Stockfish is launched,
as well as a `browser` with JavaScript injection, which is responsible
for processing changes in current position and sending the position
as a FEN to the `server` to receive a hint.

## Quick Start

```bash
pip install -r requirements.txt
cp config.ini.example bot/config.ini
python bot/main.py
```

You can change important Chess Bot parameters in `config.ini`.

## Compilation

```bash
python bot/compile.py
```

## Global Dependencies

- Windows
- [Python](https://www.python.org/downloads/release/python-3131/) (tested on v3.13.1)
- [Google Chrome](https://www.google.com/chrome/) (tested on v132.0.6834.84)
