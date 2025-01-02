from board import Board


class Game:
  def __init__(self):
    self.player_turn = 'X'
    self.board = Board()
    self.winner = None

  def get_turn(self):
    return self.player_turn
  
  def switch_turn(self):
    self.player_turn = 'X' if self.player_turn == 'O' else 'O'

  def _check_game_status(self, row, column):
    if self.board.check_win(self.player_turn, row, column):
      self.winner = self.player_turn
    elif self.board.is_full():
      self.winner = 'Tie'

  def make_move(self, column):
    row, column = self.board.make_move(self.player_turn, column)
    if row is not None:
      self._check_game_status(row, column)
      self.switch_turn()
      return True
    return False
  
  def get_winner(self):
    return self.winner

  def print_board(self):
    print(self.board)