import os

import torch

from connect4 import Connect4

from training.dqn.checkpoint import load_policy_network
from training.dqn.policy import choose_greedy_action, flatten_state


class DQNAgent:
    def __init__(self, checkpoint_path: str = "models/dqn_model.pt", device: str = "cpu"):
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"DQN checkpoint not found: {checkpoint_path}")

        self._device = torch.device(device)
        self._policy_network, _ = load_policy_network(checkpoint_path, self._device)

    def select_move(self, game: Connect4) -> int:
        return choose_greedy_action(
            self._policy_network,
            flatten_state(game.get_state()),
            game.get_valid_moves(),
            self._device,
        )
