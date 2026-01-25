from typing import Optional
import numpy as np

from .constants import ROWS, COLS, PLAYER_1, PLAYER_2
from .board import Board
from .win_checker import WinChecker


class Connect4:
    def __init__(self):
        self._board = Board()
        self._current_player = PLAYER_1
        self._winner: Optional[int] = None
        self._game_over = False
        self._move_count = 0

    def reset(self) -> np.ndarray:
        self._board = Board()
        self._current_player = PLAYER_1
        self._winner = None
        self._game_over = False
        self._move_count = 0
        return self.get_board()

    def play(self, column: int) -> tuple[bool, Optional[int]]:
        if not self.is_valid_move(column):
            raise ValueError(f"Invalid move: column {column}")

        row = self._board.drop_piece(column, self._current_player)
        self._move_count += 1

        if WinChecker.check_win(self._board, row, column):
            self._winner = self._current_player
            self._game_over = True
            return True, self._winner

        if self._move_count == ROWS * COLS:
            self._game_over = True
            return True, None

        self._current_player = -self._current_player
        return True, None

    def is_valid_move(self, column: int) -> bool:
        if self._game_over:
            return False
        return self._board.is_column_available(column)

    def get_valid_moves(self) -> list[int]:
        if self._game_over:
            return []
        return self._board.get_available_columns()

    def get_board(self) -> np.ndarray:
        return self._board.get_grid()

    def get_state(self) -> np.ndarray:
        return self._board.get_grid() * self._current_player

    def get_state_flat(self) -> np.ndarray:
        return self._board.get_grid().flatten()

    def copy(self) -> "Connect4":
        new_game = Connect4()
        new_game._board = self._board.copy()
        new_game._current_player = self._current_player
        new_game._winner = self._winner
        new_game._game_over = self._game_over
        new_game._move_count = self._move_count
        return new_game

    @property
    def current_player(self) -> int:
        return self._current_player

    @property
    def winner(self) -> Optional[int]:
        return self._winner

    @property
    def is_game_over(self) -> bool:
        return self._game_over

    @property
    def is_draw(self) -> bool:
        return self._game_over and self._winner is None

    @property
    def move_count(self) -> int:
        return self._move_count

    def __str__(self) -> str:
        return str(self._board)

    def __repr__(self) -> str:
        return f"Connect4(move_count={self._move_count}, current_player={self._current_player}, game_over={self._game_over})"
