from game_engine.board import Board
from game_engine.evaluator import Evaluator

PLAYER_ONE = 1
PLAYER_TWO = 2


class Game:
    def __init__(self):
        self.player_turn = PLAYER_ONE
        self.board = Board()
        self.winner = None
        self.game_info = []
        self.evaluator = Evaluator()

    def get_turn(self):
        return self.player_turn

    def make_move(self, column):
        row = self.board.make_move(self.player_turn, column)
        is_valid_move = row is not None
        if is_valid_move:
            self._check_game_status(row, column)
            if self.winner is None:
                move_score = self.evaluator.get_score(
                    self.player_turn, self.board.board_positions
                )
            else:
                move_score = self.get_winner() if self.get_winner() != 2 else -1

            self.game_info.append((self.board.get_board_state(), column, move_score))
            self._switch_turn()

        return is_valid_move

    def get_winner(self):
        return self.winner

    def print_board(self):
        print(self.board)

    def get_valid_moves(self):
        return self.board.get_valid_moves()

    def get_game_info(self):
        return self.game_info

    def get_threats(self):
        return self.evaluator.get_existing_threats()

    def _switch_turn(self):
        self.player_turn = PLAYER_ONE if self.player_turn == PLAYER_TWO else PLAYER_TWO

    def _check_game_status(self, row, column):
        if self.board.check_win(self.player_turn, row, column):
            self.winner = self.player_turn
        elif self.board.is_full():
            self.winner = 0
