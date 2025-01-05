import numpy as np

COLUMNS = 7
ROWS = 6
EMPTY_VALUE = 0
DIRECTIONS = [
    (1, 0),  # vertical
    (0, 1),  # horizontal
    (1, 1),  # diagonal down-right
    (1, -1),  # diagonal down-left
]


class Board:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)

    def __str__(self):
        return "\n".join(
            [" ".join([str(cell) for cell in row]) for row in reversed(self.board)]
        )

    def make_move(self, player, column):
        row = self._get_next_available_row(column)
        if row is not None:
            self.board[row][column] = player

        return row

    def get_valid_moves(self):
        return [
            column
            for column in range(COLUMNS)
            if self.board[ROWS - 1][column] == EMPTY_VALUE
        ]

    def is_full(self):
        return all([cell != EMPTY_VALUE for row in self.board for cell in row])

    def check_win(self, player, played_row, played_column):

        def is_position_in_board(r, c):
            return 0 <= r < 6 and 0 <= c < 7

        for d_row, d_col in DIRECTIONS:  
            count = 1  # Count the current piece

            # We move along one of the directions
            row, column = played_row + d_row, played_column + d_col
            while is_position_in_board(row, column) and self.board[row][column] == player:
                count += 1
                row += d_row
                column += d_col

            # We move along the opposite direction
            row, column = played_row - d_row, played_column - d_col
            while is_position_in_board(row, column) and self.board[row][column] == player:
                count += 1
                row -= d_row
                column -= d_col

            if count >= 4:
                return True

        return False

    def get_board_state(self):
        return self.board.flatten()

    def _get_next_available_row(self, column):
        for row in range(ROWS):
            if self.board[row][column] == EMPTY_VALUE:
                return row
        return None
