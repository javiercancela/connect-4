"""State preparation and action selection helpers for DQN."""

import random

import numpy as np
import torch

from connect4.constants import COLS


def flatten_state(state: np.ndarray) -> np.ndarray:
    return state.astype(np.float32, copy=False).reshape(-1)


def build_action_mask(valid_moves: list[int]) -> np.ndarray:
    mask = np.zeros(COLS, dtype=np.bool_)
    mask[valid_moves] = True
    return mask


def choose_epsilon_greedy_action(
    policy_network,
    state_vector: np.ndarray,
    valid_moves: list[int],
    epsilon: float,
    device: torch.device,
) -> int:
    if random.random() < epsilon:
        return random.choice(valid_moves)

    return choose_greedy_action(policy_network, state_vector, valid_moves, device)


def choose_greedy_action(
    policy_network,
    state_vector: np.ndarray,
    valid_moves: list[int],
    device: torch.device,
) -> int:
    state_tensor = torch.as_tensor(
        state_vector,
        dtype=torch.float32,
        device=device,
    ).unsqueeze(0)

    with torch.inference_mode():
        q_values = policy_network(state_tensor).squeeze(0).detach().cpu()

    best_value = torch.max(q_values[valid_moves]).item()
    best_moves = [move for move in valid_moves if float(q_values[move]) == best_value]
    return random.choice(best_moves)
