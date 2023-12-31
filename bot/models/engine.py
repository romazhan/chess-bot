#-*- coding: utf-8 -*-
from __future__ import annotations

from stockfish import Stockfish


class Engine(Stockfish):
    _params: dict[str, any]
    _max_thinking_time: int

    def __init__(self, params: dict[str, any]) -> None:
        self._params = {**params} # copying the first level
        self._max_thinking_time = params['Maximum Thinking Time']

        path, depth = params['Path'], params['Depth']
        del params['Maximum Thinking Time'], params['Path'], params['Depth']

        super().__init__(path=path, depth=depth, parameters=params)

    def get_best_move_time(self) -> str | None:
        return super().get_best_move_time(self._max_thinking_time)

    def restart(self) -> None:
        self.__init__(self._params)
