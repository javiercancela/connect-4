COLUMNS=7
ROWS=6
EMPTY_VALUE='-'
DIRECTIONS = [(1, 0),  # vertical
              (0, 1),  # horizontal
              (1, 1),  # diagonal down-right
              (1, -1)] # diagonal down-left



class Board:
    def __init__(self):
        self.board = [[EMPTY_VALUE for _ in range(COLUMNS)] for _ in range(ROWS)]

    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in reversed(self.board)])


    def make_move(self, player, column):
        row = self._get_row(column)
        if row is None:
            return None, None

        self.board[row][column] = player

        return row, column

    def get_valid_moves(self):
        return [column for column in range(COLUMNS) if self.board[0][column] == EMPTY_VALUE]

    def get_last_move(self):
        return self.last_move
        
    def is_full(self):
        return all([cell != EMPTY_VALUE for row in self.board for cell in row])

    def _get_row(self, column):
        for row in range(ROWS):
            if self.board[row][column] == EMPTY_VALUE:
                return row
        return None

    def check_win(self, player, played_row, played_column):
        
        # Check if the new position is inside the board
        def valid(r, c):
            return 0 <= r < 6 and 0 <= c < 7

        for drow, dcol in DIRECTIONS: # Check all directions
            count = 1  # Count the current piece

            # We move along one of the directions
            row, column = played_row + drow, played_column + dcol 
            while valid(row, column) and self.board[row][column] == player:
                count += 1
                row += drow
                column += dcol

            # We move along the opposite direction
            row, column = played_row - drow, played_column - dcol 
            while valid(row, column) and self.board[row][column] == player:
                count += 1
                row -= drow
                column -= dcol

            if count >= 4:
                return True
        
        return False


