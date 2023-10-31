#-*- coding: utf-8 -*-
from __future__ import annotations

from undetected_chromedriver import Chrome as _Chrome,\
    ChromeOptions as _ChromeOptions
from selenium.common.exceptions import\
    NoSuchWindowException as _NoSuchWindowException
from threading import Thread as _Thread

import time as _time,\
    gc as _gc


_browser = None


_pelmeni = 'return window.__PELMENI__;'

_cook = lambda server_addr, hint_lighting: '''
    const chessBoard = document.body.querySelector('wc-chess-board');

    if(!chessBoard) {
        return window.__PELMENI__ = undefined;
    }

    window.__PELMENI__ = 'yum-yum, juicy';

    const getBestMoveByFen = async fen => {
        const res = await fetch("''' + server_addr + '''", {
            method: 'POST',
            body: JSON.stringify({fen})
        });

        return await res.text();
    };

    const getSqrNumsFrom = m => {
        const getSqrNum = s => `${s.charCodeAt(0) - 96}${s.charAt(1)}`;
        return [getSqrNum(`${m[0]}${m[1]}`), getSqrNum(`${m[2]}${m[3]}`)];
    };

    const highlightSqr = (sqrNum, color) => {
        const sqr = chessBoard.querySelector(`.piece.square-${sqrNum}`);
        if(sqr) {
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
            if(piece) {
                piece.style.backgroundColor = '';
            }
        });

        const hintLightingShift = [
            "#''' + hint_lighting[0] + '''", "#''' + hint_lighting[1] + '''", 1
        ];

        const game = chessBoard.game;

        const suggestMove = async () => {
            const bestMove = await getBestMoveByFen(game.getFEN());
            if(bestMove) {
                const [sqrNumFrom, sqrNumTo] = getSqrNumsFrom(bestMove);

                const hintColor = hintLightingShift[hintLightingShift[2] ^= 1];

                clearHintLights();
                highlightSqr(sqrNumFrom, hintColor);
                highlightSqr(sqrNumTo, hintColor);
            }
        };

        (() => {
            let inProgress = false;

            game.on('Move', async () => {
                if(inProgress) {
                    return;
                }

                inProgress = true;
                suggestMove().then(() => inProgress = false);
            });
        })();
    })();
'''


def _observe(server_addr: str, hint_lighting: list[str]) -> None:
    while True:
        if not _browser:
            break

        try:
            if not _browser.execute_script(_pelmeni):
                _browser.execute_script(_cook(server_addr, hint_lighting))
        except _NoSuchWindowException:
            stop_browser()
            break
        except Exception as e:
            if not _browser:
                break

            stop_browser()
            raise Exception(f'[browser][observe][error]: {str(e).splitlines()[0]}')
        finally:
            _gc.collect()

        _time.sleep(1.7)


def start_browser(params: dict[str, str | list[str]]) -> None:
    global _browser

    try:
        chrome_options = _ChromeOptions()
        chrome_options.headless = False

        _browser = _Chrome(options=chrome_options)

        _browser.get(params['start_url'])
        _browser.maximize_window()

        _Thread(target=_observe, args=(
            params['server_addr'],
            params['hint_lighting']
        )).start()
    except _NoSuchWindowException:
        stop_browser()


def stop_browser() -> None:
    global _browser

    if _browser:
        _browser.close()
        _browser = None
