import numpy as np

from .constants import ROWS, COLS, EMPTY, PLAYER_1, PLAYER_2


class Board:
    def __init__(self):
        self._grid = np.zeros((ROWS, COLS), dtype=np.int8)

    def drop_piece(self, column: int, player: int) -> int:
        row = self._find_drop_row(column)
        self._grid[row, column] = player
        return row

    def _find_drop_row(self, column: int) -> int:
        for row in range(ROWS):
            if self._grid[row, column] == EMPTY:
                return row
        raise ValueError(f"Column {column} is full")

    def is_column_available(self, column: int) -> bool:
        if not 0 <= column < COLS:
            return False
        return self._grid[ROWS - 1, column] == EMPTY

    def get_available_columns(self) -> list[int]:
        return [col for col in range(COLS) if self.is_column_available(col)]

    def is_full(self) -> bool:
        return len(self.get_available_columns()) == 0

    def get_grid(self) -> np.ndarray:
        return self._grid.copy()

    def get_cell(self, row: int, col: int) -> int:
        return self._grid[row, col]

    def copy(self) -> "Board":
        new_board = Board()
        new_board._grid = self._grid.copy()
        return new_board

    def __str__(self) -> str:
        symbols = {PLAYER_1: "X", PLAYER_2: "O", EMPTY: "."}
        lines = []
        for row in range(ROWS - 1, -1, -1):
            line = " ".join(symbols[self._grid[row, col]] for col in range(COLS))
            lines.append(line)
        lines.append("-" * (COLS * 2 - 1))
        lines.append(" ".join(str(i + 1) for i in range(COLS)))
        lines.append("")
        lines.append("X = Player 1  O = Player 2")
        return "\n".join(lines)
