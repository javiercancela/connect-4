"""Policy evaluation helpers for trained Q-tables."""

from connect4 import Connect4, PLAYER_1, PLAYER_2
from agents.qlearning_agent import state_to_key

from .policy import choose_greedy_actual_action
from .types import QTable


def evaluate_policy(q_table: QTable, opponent, num_games: int = 200) -> dict[str, int]:
    """Evaluate a greedy policy against an opponent."""
    results: dict[str, int] = {"win": 0, "draw": 0, "loss": 0}

    for index in range(num_games):
        game = Connect4()
        ql_player = PLAYER_1 if index % 2 == 0 else PLAYER_2

        while not game.is_game_over:
            if game.current_player == ql_player:
                state = game.get_state()
                state_key, is_mirrored = state_to_key(state)
                valid_moves = game.get_valid_moves()
                move = choose_greedy_actual_action(q_table, state_key, valid_moves, is_mirrored)
            else:
                move = opponent.select_move(game)

            game.play(move)

        if game.winner == ql_player:
            results["win"] += 1
        elif game.winner is None:
            results["draw"] += 1
        else:
            results["loss"] += 1

    return results

