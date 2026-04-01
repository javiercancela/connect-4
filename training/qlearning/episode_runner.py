"""Single-episode Q-learning transition updates."""

import random

from connect4 import Connect4, PLAYER_1, PLAYER_2
from agents.qlearning_agent import map_action, state_to_key

from .policy import choose_epsilon_greedy_canonical_action
from .q_values import get_q_value, set_q_value
from .types import QTable


def train_episode(
    q_table: QTable,
    opponent,
    alpha: float,
    gamma: float,
    epsilon: float,
    draw_reward: float,
    trace_decay: float = 0.0,
) -> int | None:
    """Run one training episode and return winner (1, -1, or None)."""
    game = Connect4()
    is_self_play = opponent is None

    ql_player = random.choice([PLAYER_1, PLAYER_2]) if not is_self_play else None
    pending: dict[int, tuple[bytes, int]] = {}
    use_traces = trace_decay > 0
    traces: dict[int, list[tuple[bytes, int]]] = {}

    while not game.is_game_over:
        player = game.current_player
        is_qlearning_turn = is_self_play or (player == ql_player)

        if is_qlearning_turn:
            state = game.get_state()
            state_key, is_mirrored = state_to_key(state)
            valid_moves = game.get_valid_moves()
            canonical_valid_moves = [map_action(action, is_mirrored) for action in valid_moves]

            if player in pending:
                previous_state_key, previous_action = pending[player]
                max_q_next = max(
                    get_q_value(q_table, state_key, action)
                    for action in canonical_valid_moves
                )
                old_q = get_q_value(q_table, previous_state_key, previous_action)
                td_error = gamma * max_q_next - old_q

                if use_traces:
                    _apply_traces(q_table, traces[player], alpha, td_error, gamma, trace_decay)
                else:
                    set_q_value(q_table, previous_state_key, previous_action, old_q + alpha * td_error)

            canonical_action = choose_epsilon_greedy_canonical_action(
                q_table,
                state_key,
                canonical_valid_moves,
                epsilon,
            )
            action = map_action(canonical_action, is_mirrored)
            pending[player] = (state_key, canonical_action)

            if use_traces:
                if player not in traces:
                    traces[player] = []
                traces[player].append((state_key, canonical_action))

            game.play(action)
            continue

        action = opponent.select_move(game)
        game.play(action)

    for player, (state_key, action) in pending.items():
        if game.winner == player:
            reward = 1.0
        elif game.winner is None:
            reward = draw_reward
        else:
            reward = -1.0

        old_q = get_q_value(q_table, state_key, action)
        td_error = reward - old_q

        if use_traces and player in traces:
            _apply_traces(q_table, traces[player], alpha, td_error, gamma, trace_decay)
        else:
            set_q_value(q_table, state_key, action, old_q + alpha * td_error)

    return game.winner


def _apply_traces(
    q_table: QTable,
    history: list[tuple[bytes, int]],
    alpha: float,
    td_error: float,
    gamma: float,
    trace_decay: float,
) -> None:
    """Propagate TD error backward through visited state-action pairs."""
    decay = 1.0
    for state_key, action in reversed(history):
        old_q = get_q_value(q_table, state_key, action)
        set_q_value(q_table, state_key, action, old_q + alpha * td_error * decay)
        decay *= gamma * trace_decay
