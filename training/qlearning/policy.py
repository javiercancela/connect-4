"""Action-selection policies for Q-learning training and evaluation."""

import random

from agents.qlearning_agent import map_action

from .q_values import get_q_value
from .types import QTable


def choose_epsilon_greedy_canonical_action(
    q_table: QTable,
    state_key: bytes,
    canonical_valid_moves: list[int],
    epsilon: float,
) -> int:
    if random.random() < epsilon:
        return random.choice(canonical_valid_moves)

    best_q = float("-inf")
    best_actions: list[int] = []
    for action in canonical_valid_moves:
        q_value = get_q_value(q_table, state_key, action)
        if q_value > best_q:
            best_q = q_value
            best_actions = [action]
        elif q_value == best_q:
            best_actions.append(action)

    return random.choice(best_actions)


def choose_greedy_actual_action(
    q_table: QTable,
    state_key: bytes,
    valid_moves: list[int],
    is_mirrored: bool,
) -> int:
    best_q = float("-inf")
    best_moves: list[int] = []

    for action in valid_moves:
        canonical_action = map_action(action, is_mirrored)
        q_value = get_q_value(q_table, state_key, canonical_action)
        if q_value > best_q:
            best_q = q_value
            best_moves = [action]
        elif q_value == best_q:
            best_moves.append(action)

    return random.choice(best_moves)

