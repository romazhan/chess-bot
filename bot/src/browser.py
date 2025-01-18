from typing import Iterable
from threading import Thread
from undetected_chromedriver import (
    Chrome,
    ChromeOptions
)
from selenium.common.exceptions import (
    NoSuchWindowException,
    InvalidSessionIdException
)
import time, gc


_browser = None

_pelmeni = 'return window.__PELMENI__;'

_cook = lambda server_addr, hint_lighting: '''
    const chessBoard = document.body.querySelector('wc-chess-board');

    if (!chessBoard) {
        return window.__PELMENI__ = undefined;
    }
    window.__PELMENI__ = 'yum-yum, juicy';

    const getBestMoveByFen = async (fen, signal) => {
        return await fetch("''' + server_addr + '''", {
            method: 'POST',
            body: JSON.stringify({fen}),
            signal
        }).then(r => r.text()).catch(e => {
            if (e.name === 'AbortError') {
                return null;
            }

            throw e;
        });
    };

    const getSqrNumsFrom = m => {
        const getSqrNum = s => `${s.charCodeAt(0) - 96}${s.charAt(1)}`;
        return [
            getSqrNum(`${m[0]}${m[1]}`), getSqrNum(`${m[2]}${m[3]}`)
        ];
    };

    const highlightSqr = (sqrNum, color) => {
        const sqr = chessBoard.querySelector(`.piece.square-${sqrNum}`);
        if (sqr) {
            return sqr.style.backgroundColor = color;
        }

        const newSqr = document.createElement('div');
        newSqr.className = `piece square-${sqrNum}`;
        newSqr.style.backgroundColor = color;
        newSqr.style.zIndex = '-1';

        chessBoard.appendChild(newSqr);
    };

    const clearHintLights = () => {
        chessBoard.querySelectorAll('.piece').forEach(p => p.style.backgroundColor = '');
    };

    (() => {
        chessBoard.addEventListener('mousedown', e => {
            const piece = e.target.closest('.piece');
            if (piece) {
                piece.style.backgroundColor = '';
            }
        });

        const hintLightingShift = [
            "#''' + hint_lighting[0] + '''", "#''' + hint_lighting[1] + '''", 1
        ];

        const game = chessBoard.game;

        const suggestMove = async (signal, hintColor) => {
            const bestMove = await getBestMoveByFen(game.getFEN(), signal);
            if (bestMove) {
                const [sqrNumFrom, sqrNumTo] = getSqrNumsFrom(bestMove);

                clearHintLights();
                highlightSqr(sqrNumFrom, hintColor);
                highlightSqr(sqrNumTo, hintColor);
            }
        };

        (() => {
            const fetchAborters = [];

            game.on('Move', async () => {
                if (fetchAborters.length) {
                    fetchAborters.forEach(c => c.abort());
                    fetchAborters.length = 0;
                }

                const fetchAborter = new AbortController();
                fetchAborters.push(fetchAborter);
                suggestMove(
                    fetchAborter.signal,
                    hintLightingShift[hintLightingShift[2] ^= 1]
                );
            });
        })();
    })();
'''

def _observe(server_addr: str, hint_lighting: Iterable[str]) -> None:
    while True:
        if not _browser:
            break

        try:
            if not _browser.execute_script(_pelmeni):
                _browser.execute_script(_cook(server_addr, hint_lighting))
        except NoSuchWindowException:
            stop_browser()
            break
        except Exception as e:
            if not _browser:
                break

            stop_browser()
            raise Exception(f'[browser][observe][error]: {str(e).splitlines()[0]}')
        finally:
            gc.collect()

        time.sleep(1.75)

def start_browser(
    use_existing_profile: bool,
    start_url: str,
    server_addr: str,
    hint_lighting: Iterable[str] = ('e2859a', 'bd7873')
) -> None:
    global _browser

    chrome_options = ChromeOptions()
    if use_existing_profile:
        chrome_options.add_argument('--user-data-dir')

    _browser = Chrome(options=chrome_options)

    _browser.get(start_url)
    _browser.maximize_window()

    Thread(target=_observe, args=(
        server_addr,
        hint_lighting
    )).start()

def stop_browser() -> None:
    global _browser

    if _browser:
        try:
            _browser.close()
        except (NoSuchWindowException, InvalidSessionIdException):
            pass
        finally:
            _browser = None
