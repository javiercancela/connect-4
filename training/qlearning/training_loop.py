"""Multi-episode training loop orchestration."""

import os
import time

from connect4 import PLAYER_1

from .config import QLearningTrainingConfig
from .episode_runner import train_episode
from .evaluator import evaluate_policy
from .opponents import build_default_evaluation_opponents, build_training_opponent
from .persistence import load_qtable, save_qtable
from .types import QTable


def train_qlearning(config: QLearningTrainingConfig) -> QTable:
    q_table = _initialize_qtable(config.load)

    opponents = _build_training_opponents(config.opponents, config.minimax_depth)

    _print_training_config(config)

    start_time = time.time()
    wins = draws = losses = 0
    episode = 0

    try:
        for episode in range(1, config.episodes + 1):
            epsilon = config.epsilon_for_episode(episode)
            alpha = config.alpha_for_episode(episode)
            opponent_name = config.opponent_for_episode(episode)

            winner = train_episode(
                q_table=q_table,
                opponent=opponents[opponent_name],
                alpha=alpha,
                gamma=config.gamma,
                epsilon=epsilon,
                draw_reward=config.draw_reward,
                trace_decay=config.trace_decay,
            )

            if winner == PLAYER_1:
                wins += 1
            elif winner is None:
                draws += 1
            else:
                losses += 1

            if episode % 10_000 == 0:
                _print_progress(episode, start_time, wins, draws, losses, epsilon, alpha, len(q_table))

            if config.eval_interval > 0 and episode % config.eval_interval == 0:
                _run_evaluations(q_table, config.eval_games)

            if config.save_interval > 0 and episode % config.save_interval == 0:
                save_qtable(q_table, config.output)

    except KeyboardInterrupt:
        print(f"\n\nInterrupted at episode {episode:,}.")

    elapsed = time.time() - start_time
    print(f"\nTraining finished in {elapsed:.1f}s ({episode:,} episodes)")
    print(f"  Q-table size: {len(q_table):,} states")

    save_qtable(q_table, config.output)
    print(f"  Saved to {config.output}")

    print(f"\nFinal evaluation ({config.eval_games} games each):")
    _run_evaluations(q_table, config.eval_games)

    return q_table


def _build_training_opponents(
    names: tuple[str, ...], minimax_depth: int
) -> dict[str, object | None]:
    opponents: dict[str, object | None] = {}
    for name in names:
        if name not in opponents:
            opponents[name] = build_training_opponent(name, minimax_depth)
    return opponents


def _initialize_qtable(load_path: str | None) -> QTable:
    if load_path and os.path.exists(load_path):
        print(f"Loading Q-table from {load_path}")
        q_table = load_qtable(load_path)
        print(f"  {len(q_table):,} states loaded")
        return q_table
    return {}


def _print_training_config(config: QLearningTrainingConfig) -> None:
    opponent_label = " -> ".join(
        "self-play" if o == "self" else o for o in config.opponents
    )
    print("\nTraining config:")
    print(f"  Episodes:      {config.episodes:,}")
    print(f"  Opponents:     {opponent_label}")
    print(f"  Alpha:         {config.alpha} -> {config.alpha_end}")
    print(f"  Gamma:         {config.gamma}")
    print(f"  Epsilon:       {config.epsilon_start} -> {config.epsilon_end}")
    print(f"  Trace decay:   {config.trace_decay}")
    print(f"  Draw reward:   {config.draw_reward}")
    print(f"  Output:        {config.output}")
    print()


def _print_progress(
    episode: int,
    start_time: float,
    wins: int,
    draws: int,
    losses: int,
    epsilon: float,
    alpha: float,
    num_states: int,
) -> None:
    elapsed = time.time() - start_time
    episodes_per_second = episode / elapsed
    total = wins + draws + losses
    print(
        f"  Episode {episode:>9,} | "
        f"States: {num_states:>9,} | "
        f"P1/D/P2: {100 * wins / total:.0f}/"
        f"{100 * draws / total:.0f}/"
        f"{100 * losses / total:.0f}% | "
        f"Eps: {epsilon:.3f} | "
        f"Alpha: {alpha:.4f} | "
        f"{episodes_per_second:.0f} ep/s"
    )


def _run_evaluations(q_table: QTable, num_games: int) -> None:
    for name, opponent in build_default_evaluation_opponents():
        results = evaluate_policy(q_table, opponent, num_games)
        wins, draws, losses = results["win"], results["draw"], results["loss"]
        print(
            f"    vs {name:>10}: "
            f"W {wins:>3}  D {draws:>3}  L {losses:>3}  "
            f"({100 * wins / num_games:.1f}% win)"
        )
    print()

