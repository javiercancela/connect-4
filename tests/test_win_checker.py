from connect4 import Board, WinChecker, PLAYER_1, PLAYER_2


class TestWinChecker:
    def test_no_win_on_empty_board(self):
        board = Board()
        assert not WinChecker.check_win(board, 0, 0)

    def test_horizontal_win(self):
        board = Board()
        for col in range(4):
            board.drop_piece(col, PLAYER_1)
        assert WinChecker.check_win(board, 0, 3)

    def test_vertical_win(self):
        board = Board()
        for _ in range(4):
            board.drop_piece(0, PLAYER_1)
        assert WinChecker.check_win(board, 3, 0)

    def test_diagonal_up_right_win(self):
        board = Board()
        board._grid[0, 0] = PLAYER_1
        board._grid[1, 1] = PLAYER_1
        board._grid[2, 2] = PLAYER_1
        board._grid[3, 3] = PLAYER_1
        assert WinChecker.check_win(board, 3, 3)

    def test_diagonal_up_left_win(self):
        board = Board()
        board._grid[0, 6] = PLAYER_1
        board._grid[1, 5] = PLAYER_1
        board._grid[2, 4] = PLAYER_1
        board._grid[3, 3] = PLAYER_1
        assert WinChecker.check_win(board, 3, 3)

    def test_three_in_row_not_win(self):
        board = Board()
        for col in range(3):
            board.drop_piece(col, PLAYER_1)
        assert not WinChecker.check_win(board, 0, 2)

    def test_win_in_middle(self):
        board = Board()
        board._grid[0, 0] = PLAYER_1
        board._grid[0, 1] = PLAYER_1
        board._grid[0, 3] = PLAYER_1
        board._grid[0, 2] = PLAYER_1
        assert WinChecker.check_win(board, 0, 2)
