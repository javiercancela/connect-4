import gzip
import os
import pickle
import random

import numpy as np

from connect4 import Connect4
from connect4.constants import COLS, ROWS


def state_to_key(state: np.ndarray) -> tuple[bytes, bool]:
    """Convert perspective-encoded board to canonical key using mirror symmetry.

    Returns (canonical_bytes_key, is_mirrored). The canonical form is the
    lexicographically smaller of the board and its horizontal mirror, which
    roughly halves the effective state space.
    """
    flat = state.flatten()
    mirror_flat = state[:, ::-1].flatten()
    key = flat.tobytes()
    mirror_key = mirror_flat.tobytes()
    if key <= mirror_key:
        return key, False
    return mirror_key, True


def map_action(action: int, is_mirrored: bool) -> int:
    """Map action between real and canonical action space. Self-inverse."""
    if is_mirrored:
        return COLS - 1 - action
    return action


class QLearningAgent:
    def __init__(self, qtable_path: str = "models/qtable.pkl.gz"):
        if not os.path.exists(qtable_path):
            raise FileNotFoundError(f"Q-table not found: {qtable_path}")
        with gzip.open(qtable_path, "rb") as f:
            self._q_table = pickle.load(f)

    def select_move(self, game: Connect4) -> int:
        state = game.get_state()
        state_key, is_mirrored = state_to_key(state)
        valid_moves = game.get_valid_moves()

        q_values = self._q_table.get(state_key)
        if q_values is None:
            return random.choice(valid_moves)

        best_q = float("-inf")
        best_moves = []

        for action in valid_moves:
            canonical_action = map_action(action, is_mirrored)
            q = q_values.get(canonical_action, 0.0)
            if q > best_q:
                best_q = q
                best_moves = [action]
            elif q == best_q:
                best_moves.append(action)

        return random.choice(best_moves)
