import os

import torch

from connect4 import Connect4

from training.dqn.checkpoint import load_policy_network
from training.dqn.policy import canonicalize_state, choose_greedy_action, mirror_action


class DQNAgent:
    def __init__(self, checkpoint_path: str = "models/dqn_model.pt", device: str = "cpu"):
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"DQN checkpoint not found: {checkpoint_path}")

        self._device = torch.device(device)
        self._policy_network, _ = load_policy_network(checkpoint_path, self._device)

    def select_move(self, game: Connect4) -> int:
        canonical_state, is_mirrored = canonicalize_state(game.get_state())
        valid_moves = game.get_valid_moves()
        canonical_moves = (
            [mirror_action(m) for m in valid_moves] if is_mirrored else valid_moves
        )
        canonical_action = choose_greedy_action(
            self._policy_network, canonical_state, canonical_moves, self._device
        )
        return mirror_action(canonical_action) if is_mirrored else canonical_action
