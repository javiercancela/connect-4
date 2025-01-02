import random
from game import Game


class Simulator:

  def run(self, total_games):
    for i in range(total_games):
      self.play_game()

  def play_game(self):
    game = Game()
    while game.get_winner() is None:
      valid_moves = game.get_valid_moves()
      move = random.choice(valid_moves)
      game.make_move(move)
      game.print_board()