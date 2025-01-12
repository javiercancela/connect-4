import random
import torch
from game_engine.game import Game
from model.dqn01_nn import DQN01


class TestDQN01Random:
    def __init__(self):
        self.model = DQN01()
        self.model.load_state_dict(torch.load(self.model.file_path, weights_only=True))
        self.model.eval()
        self.game = None

    def play_game(self):
        self.game = Game()
        random.seed()
        while self.game.get_winner() is None:
            valid_moves = self.game.get_valid_moves()
            if self.game.get_turn() == 1:
                state = torch.tensor(
                    self.game.board.get_board_state(), dtype=torch.float32
                ).unsqueeze(0)
                q_values = self.model(state)
                move = max(valid_moves, key=lambda x: q_values[0, x].item())

                if move in valid_moves:
                    self.game.make_move(move)
                else:
                    print(f"Invalid move: {move}")
                    break
            else:
                move = random.choice(valid_moves)
                self.game.make_move(move)

    def get_winner(self):
        return self.game.get_winner()
