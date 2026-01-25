import random
from connect4 import Connect4


class RandomAgent:
    def select_move(self, game: Connect4) -> int:
        valid_moves = game.get_valid_moves()
        return random.choice(valid_moves)
