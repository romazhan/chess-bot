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

    def get_best_move_by_fen(self, fen: str) -> str:
        try:
            self.set_fen_position(fen)

            return super().get_best_move_time(self._max_thinking_time) or ''
        except Exception as e:
            print(f'[engine][error]: {e}')
            self.restart()

            return self.get_best_move_by_fen(fen) # ? infinite recursion

    def restart(self) -> None:
        self.__init__(self._params)
