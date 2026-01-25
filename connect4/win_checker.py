from .constants import ROWS, COLS, WIN_LENGTH
from .board import Board


class WinChecker:
    DIRECTIONS = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal up-right
        (1, -1),  # diagonal up-left
    ]

    @staticmethod
    def check_win(board: Board, row: int, col: int) -> bool:
        player = board.get_cell(row, col)
        if player == 0:
            return False

        for dr, dc in WinChecker.DIRECTIONS:
            count = 1 + WinChecker._count_in_direction(board, row, col, dr, dc, player) \
                      + WinChecker._count_in_direction(board, row, col, -dr, -dc, player)
            if count >= WIN_LENGTH:
                return True
        return False

    @staticmethod
    def _count_in_direction(board: Board, row: int, col: int, dr: int, dc: int, player: int) -> int:
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board.get_cell(r, c) == player:
            count += 1
            r += dr
            c += dc
        return count
