# Chess Bot

>♟️ Chess Bot for [Chess.com](https://www.chess.com) on Python

Chess Bot consists of a local `server` on which Stockfish is launched,
as well as a `browser` with JavaScript injection, which is responsible
for processing changes in current position and sending the position
as a FEN to the `server` to receive a hint.

## Quick Start

```bash
pip install -r requirements.txt
cd bot
python main.py
```

You can change important Chess Bot parameters in
[config.ini](bot/config.ini).

## Global Dependencies

- Windows
- [Google Chrome Web Browser](https://www.google.com/chrome)
- [Python](https://www.python.org/downloads) (tested on v3.8.10)
