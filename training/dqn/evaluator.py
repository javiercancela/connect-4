"""Policy evaluation helpers for DQN checkpoints."""

import torch

from connect4 import Connect4, PLAYER_1, PLAYER_2

from .policy import choose_greedy_action, flatten_state


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
                move = choose_greedy_action(
                    policy_network,
                    flatten_state(game.get_state()),
                    game.get_valid_moves(),
                    device,
                )
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
