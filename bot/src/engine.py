from typing import Dict, Any
from stockfish import Stockfish


class Engine(Stockfish):
    __slots__ = (
        '_params',
        '_max_thinking_time'
    )

    def __init__(self, params: Dict[str, Any]) -> None:
        self._params = {**params} # copying the first level
        self._max_thinking_time = params['Maximum Thinking Time']

        path, depth = params['Path'], params['Depth']
        del params['Maximum Thinking Time'], params['Path'], params['Depth']

        super().__init__(
            path=path,
            depth=depth,
            parameters=params
        )

    def get_best_move_time(self) -> str | None:
        return super().get_best_move_time(self._max_thinking_time)

    def restart(self) -> None:
        self.__init__(self._params)
