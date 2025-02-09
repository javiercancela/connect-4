import random
from game_engine.game import Game
from model.monte_carlo_agent import MonteCarloAgent


class TestMCRandom:
    def __init__(self):
        self.agent = MonteCarloAgent(player_id=1)
        self.game = None

    def play_game(self):
        self.game = Game()
        random.seed()
        while self.game.get_winner() is None:
            if self.game.get_turn() == 1:
                self.agent.record_state(self.game)
                move = self.agent.choose_action(self.game)
            else:
                valid_moves = self.game.get_valid_moves()
                move = random.choice(valid_moves)
            self.game.make_move(move)
        self.teach_agent()
    
    def teach_agent(self):
        if self.game.get_winner() == 1:
            reward = 1
        elif self.game.get_winner() == 2:
            reward = 0
        else:
            reward = 0.5
        self.agent.update_value_function(reward)


    def get_winner(self):
        return self.game.get_winner()
