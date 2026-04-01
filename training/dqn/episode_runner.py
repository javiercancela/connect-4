"""Single-episode experience collection for DQN training."""

import random

import torch

from connect4 import Connect4, PLAYER_1, PLAYER_2

from .policy import build_action_mask, canonicalize_state, choose_epsilon_greedy_action, mirror_action
from .replay_buffer import ReplayBuffer
from .types import PendingTransition


def train_episode(
    policy_network,
    replay_buffer: ReplayBuffer,
    opponent,
    epsilon: float,
    draw_reward: float,
    device: torch.device,
) -> tuple[int | None, int | None]:
    game = Connect4()
    is_self_play = opponent is None
    learning_player = random.choice([PLAYER_1, PLAYER_2]) if not is_self_play else None
    pending: dict[int, PendingTransition] = {}
    empty_mask = build_action_mask([])

    while not game.is_game_over:
        player = game.current_player
        is_learning_turn = is_self_play or player == learning_player

        if is_learning_turn:
            canonical_state, is_mirrored = canonicalize_state(game.get_state())
            valid_moves = game.get_valid_moves()
            canonical_moves = (
                [mirror_action(m) for m in valid_moves] if is_mirrored else valid_moves
            )

            previous_transition = pending.get(player)
            if previous_transition is not None:
                replay_buffer.add(
                    state=previous_transition.state,
                    action=previous_transition.action,
                    reward=0.0,
                    next_state=canonical_state,
                    next_action_mask=build_action_mask(canonical_moves),
                    done=False,
                )

            canonical_action = choose_epsilon_greedy_action(
                policy_network=policy_network,
                state_vector=canonical_state,
                valid_moves=canonical_moves,
                epsilon=epsilon,
                device=device,
            )
            pending[player] = PendingTransition(state=canonical_state, action=canonical_action)
            real_action = mirror_action(canonical_action) if is_mirrored else canonical_action
            game.play(real_action)
            continue

        action = opponent.select_move(game)
        game.play(action)

    for player, transition in pending.items():
        replay_buffer.add(
            state=transition.state,
            action=transition.action,
            reward=_terminal_reward(game.winner, player, draw_reward),
            next_state=None,
            next_action_mask=empty_mask,
            done=True,
        )

    return game.winner, learning_player


def _terminal_reward(winner: int | None, learning_player: int, draw_reward: float) -> float:
    if winner == learning_player:
        return 1.0
    if winner is None:
        return draw_reward
    return -1.0
