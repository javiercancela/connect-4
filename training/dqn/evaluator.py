"""Policy evaluation helpers for DQN checkpoints."""

import torch

from connect4 import Connect4, PLAYER_1, PLAYER_2

from .policy import canonicalize_state, choose_greedy_action, mirror_action


def evaluate_policy(
    policy_network,
    opponent,
    device: torch.device,
    num_games: int = 200,
) -> dict[str, int]:
    results: dict[str, int] = {"win": 0, "draw": 0, "loss": 0}

    for index in range(num_games):
        game = Connect4()
        dqn_player = PLAYER_1 if index % 2 == 0 else PLAYER_2

        while not game.is_game_over:
            if game.current_player == dqn_player:
                canonical_state, is_mirrored = canonicalize_state(game.get_state())
                valid_moves = game.get_valid_moves()
                canonical_moves = (
                    [mirror_action(m) for m in valid_moves] if is_mirrored else valid_moves
                )
                canonical_action = choose_greedy_action(
                    policy_network, canonical_state, canonical_moves, device
                )
                move = mirror_action(canonical_action) if is_mirrored else canonical_action
            else:
                move = opponent.select_move(game)

            game.play(move)

        if game.winner == dqn_player:
            results["win"] += 1
        elif game.winner is None:
            results["draw"] += 1
        else:
            results["loss"] += 1

    return results
