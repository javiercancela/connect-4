import random
from game import Game


class Simulator:
  def __init__(self):
    self.all_states = []

  def run(self, total_games):
    for i in range(total_games):
      self.play_game()

    print(self.all_states)

  def play_game(self):
    game = Game()
    while game.get_winner() is None:
      valid_moves = game.get_valid_moves()
      move = random.choice(valid_moves)
      game.make_move(move)

    result = game.get_winner() if game.get_winner() != 2 else -1
    for state, move in zip(*game.get_game_states_and_moves()):
      self.all_states.append((state, move, result))

  def get_all_states(self):
    return self.all_states

