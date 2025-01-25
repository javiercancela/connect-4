import random
import torch
from game_engine.game import Game


class TestRandomRandom:
    def __init__(self):
        self.game = None

    def play_game(self):
        self.game = Game()
        random.seed()
        while self.game.get_winner() is None:
            valid_moves = self.game.get_valid_moves()
            move = random.choice(valid_moves)
            self.game.make_move(move)

    def get_winner(self):
        return self.game.get_winner()
