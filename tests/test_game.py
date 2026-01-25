import numpy as np
import pytest

from connect4 import Connect4, Board, PLAYER_1, PLAYER_2


class TestConnect4Init:
    def test_new_game_has_empty_board(self):
        game = Connect4()
        board = game.get_board()
        assert np.all(board == 0)

    def test_new_game_player_1_starts(self):
        game = Connect4()
        assert game.current_player == PLAYER_1

    def test_new_game_not_over(self):
        game = Connect4()
        assert not game.is_game_over
        assert game.winner is None

    def test_new_game_all_moves_valid(self):
        game = Connect4()
        valid_moves = game.get_valid_moves()
        assert valid_moves == [0, 1, 2, 3, 4, 5, 6]


class TestConnect4Play:
    def test_play_valid_move(self):
        game = Connect4()
        success, winner = game.play(3)
        assert success is True
        assert winner is None
        assert game.get_board()[0, 3] == PLAYER_1

    def test_play_switches_player(self):
        game = Connect4()
        assert game.current_player == PLAYER_1
        game.play(0)
        assert game.current_player == PLAYER_2
        game.play(1)
        assert game.current_player == PLAYER_1

    def test_play_invalid_column_raises(self):
        game = Connect4()
        with pytest.raises(ValueError):
            game.play(7)
        with pytest.raises(ValueError):
            game.play(-1)

    def test_play_full_column_raises(self):
        board = Board()
        board._grid[:, 0] = [1, -1, 1, -1, 1, -1]
        assert not board.is_column_available(0)

    def test_pieces_stack(self):
        game = Connect4()
        game.play(3)
        game.play(3)
        game.play(3)

        board = game.get_board()
        assert board[0, 3] == PLAYER_1
        assert board[1, 3] == PLAYER_2
        assert board[2, 3] == PLAYER_1


class TestConnect4Win:
    def test_horizontal_win(self):
        game = Connect4()
        game.play(0)
        game.play(0)
        game.play(1)
        game.play(1)
        game.play(2)
        game.play(2)
        success, winner = game.play(3)

        assert game.is_game_over
        assert winner == PLAYER_1
        assert game.winner == PLAYER_1

    def test_vertical_win(self):
        game = Connect4()
        game.play(0)
        game.play(1)
        game.play(0)
        game.play(1)
        game.play(0)
        game.play(1)
        success, winner = game.play(0)

        assert game.is_game_over
        assert winner == PLAYER_1

    def test_diagonal_up_right_win(self):
        game = Connect4()
        game.play(0)
        game.play(1)
        game.play(1)
        game.play(2)
        game.play(6)
        game.play(2)
        game.play(2)
        game.play(3)
        game.play(6)
        game.play(3)
        game.play(6)
        game.play(3)
        success, winner = game.play(3)

        assert game.is_game_over
        assert winner == PLAYER_1

    def test_diagonal_up_left_win(self):
        game = Connect4()
        game.play(6)
        game.play(5)
        game.play(5)
        game.play(4)
        game.play(4)
        game.play(3)
        game.play(4)
        game.play(3)
        game.play(3)
        game.play(0)
        success, winner = game.play(3)

        assert game.is_game_over
        assert winner == PLAYER_1

    def test_no_moves_after_win(self):
        game = Connect4()
        game.play(0)
        game.play(1)
        game.play(0)
        game.play(1)
        game.play(0)
        game.play(1)
        game.play(0)

        assert game.get_valid_moves() == []
        assert not game.is_valid_move(2)


class TestConnect4Draw:
    def test_is_draw_property(self):
        game = Connect4()
        assert not game.is_draw

        game.play(0)
        game.play(1)
        game.play(0)
        game.play(1)
        game.play(0)
        game.play(1)
        game.play(0)

        assert not game.is_draw


class TestConnect4Utilities:
    def test_copy_creates_independent_game(self):
        game = Connect4()
        game.play(3)
        game.play(4)

        copy = game.copy()

        assert np.array_equal(copy.get_board(), game.get_board())
        assert copy.current_player == game.current_player
        assert copy.move_count == game.move_count

        game.play(5)
        assert game.move_count == 3
        assert copy.move_count == 2

    def test_reset_clears_game(self):
        game = Connect4()
        game.play(0)
        game.play(1)
        game.play(2)

        board = game.reset()

        assert np.all(board == 0)
        assert game.current_player == PLAYER_1
        assert game.move_count == 0
        assert not game.is_game_over

    def test_get_state_perspective(self):
        game = Connect4()
        game.play(0)

        state = game.get_state()
        assert state[0, 0] == -1

    def test_get_state_flat(self):
        game = Connect4()
        flat = game.get_state_flat()
        assert flat.shape == (42,)

    def test_str_representation(self):
        game = Connect4()
        game.play(3)
        s = str(game)
        assert "X" in s
        assert "." in s

    def test_repr(self):
        game = Connect4()
        r = repr(game)
        assert "Connect4" in r
        assert "move_count=0" in r


class TestConnect4ValidMoves:
    def test_is_valid_move(self):
        game = Connect4()
        assert game.is_valid_move(0)
        assert game.is_valid_move(6)
        assert not game.is_valid_move(-1)
        assert not game.is_valid_move(7)

    def test_move_count_increments(self):
        game = Connect4()
        assert game.move_count == 0
        game.play(0)
        assert game.move_count == 1
        game.play(1)
        assert game.move_count == 2


class TestBoard:
    def test_drop_piece(self):
        board = Board()
        row = board.drop_piece(3, PLAYER_1)
        assert row == 0
        assert board.get_cell(0, 3) == PLAYER_1

    def test_pieces_stack_in_column(self):
        board = Board()
        assert board.drop_piece(0, PLAYER_1) == 0
        assert board.drop_piece(0, PLAYER_2) == 1
        assert board.drop_piece(0, PLAYER_1) == 2

    def test_is_column_available(self):
        board = Board()
        assert board.is_column_available(0)
        board._grid[:, 0] = 1
        assert not board.is_column_available(0)

    def test_get_available_columns(self):
        board = Board()
        assert board.get_available_columns() == [0, 1, 2, 3, 4, 5, 6]
        board._grid[:, 3] = 1
        assert board.get_available_columns() == [0, 1, 2, 4, 5, 6]

    def test_is_full(self):
        board = Board()
        assert not board.is_full()
        board._grid[:, :] = 1
        assert board.is_full()

    def test_copy(self):
        board = Board()
        board.drop_piece(0, PLAYER_1)
        copy = board.copy()

        assert np.array_equal(board.get_grid(), copy.get_grid())
        board.drop_piece(1, PLAYER_2)
        assert not np.array_equal(board.get_grid(), copy.get_grid())
