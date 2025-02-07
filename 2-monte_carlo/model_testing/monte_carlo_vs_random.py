import random
from game_engine.game import Game
from model.monte_carlo_agent import MonteCarloAgent


class TestMCRandom:
    def __init__(self):
        self.agent = MonteCarloAgent(player_id=1)
        self.agent.load_value_function()
        self.game = None

    def play_game(self):
        self.game = Game()
        random.seed()
        while self.game.get_winner() is None:
            valid_moves = self.game.get_valid_moves()
            if self.game.get_turn() == 1:
                self.agent.record_state(self.game)

                # Make move
                move = self.agent.choose_action(self.game)
                self.game.make_move(move)

            else:
                move = random.choice(valid_moves)
                self.game.make_move(move)

    def get_winner(self):
        return self.game.get_winner()
