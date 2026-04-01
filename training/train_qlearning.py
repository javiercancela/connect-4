"""CLI entrypoint for tabular Q-learning training."""

import argparse

from training.qlearning import QLearningTrainingConfig, train_qlearning

VALID_OPPONENTS = {"self", "random", "heuristic", "minimax"}


def _parse_opponents(raw: str) -> tuple[str, ...]:
    opponents = tuple(o.strip() for o in raw.split(","))
    for o in opponents:
        if o not in VALID_OPPONENTS:
            raise argparse.ArgumentTypeError(
                f"Unknown opponent '{o}'. Choose from: {', '.join(sorted(VALID_OPPONENTS))}"
            )
    return opponents


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train a Tabular Q-learning agent for Connect-4",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=500_000,
        help="Training episodes",
    )
    parser.add_argument("--alpha", type=float, default=0.1, help="Initial learning rate")
    parser.add_argument("--alpha-end", type=float, default=0.01, help="Final learning rate")
    parser.add_argument("--gamma", type=float, default=0.95, help="Discount factor")
    parser.add_argument(
        "--epsilon-start",
        type=float,
        default=1.0,
        help="Initial exploration rate",
    )
    parser.add_argument(
        "--epsilon-end",
        type=float,
        default=0.05,
        help="Final exploration rate",
    )
    parser.add_argument(
        "--trace-decay",
        type=float,
        default=0.7,
        help="Eligibility trace decay (lambda). 0 disables traces",
    )
    parser.add_argument("--draw-reward", type=float, default=0.5, help="Reward for draws")
    parser.add_argument(
        "--opponent",
        type=str,
        default="self",
        help="Training opponent(s), comma-separated for schedule (e.g. random,heuristic,self)",
    )
    parser.add_argument(
        "--minimax-depth",
        type=int,
        default=2,
        help="Minimax opponent search depth",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models/qtable.pkl.gz",
        help="Output Q-table path",
    )
    parser.add_argument("--load", type=str, default=None, help="Load existing Q-table to continue")
    parser.add_argument(
        "--eval-interval",
        type=int,
        default=50_000,
        help="Evaluate every N episodes (0 to disable)",
    )
    parser.add_argument("--eval-games", type=int, default=200, help="Games per evaluation opponent")
    parser.add_argument(
        "--save-interval",
        type=int,
        default=0,
        help="Save checkpoint every N episodes (0 to disable)",
    )
    return parser


def parse_args() -> QLearningTrainingConfig:
    args = build_parser().parse_args()
    opponents = _parse_opponents(args.opponent)
    return QLearningTrainingConfig(
        episodes=args.episodes,
        alpha=args.alpha,
        alpha_end=args.alpha_end,
        gamma=args.gamma,
        epsilon_start=args.epsilon_start,
        epsilon_end=args.epsilon_end,
        trace_decay=args.trace_decay,
        draw_reward=args.draw_reward,
        opponents=opponents,
        minimax_depth=args.minimax_depth,
        output=args.output,
        load=args.load,
        eval_interval=args.eval_interval,
        eval_games=args.eval_games,
        save_interval=args.save_interval,
    )


def main() -> None:
    config = parse_args()
    train_qlearning(config)


if __name__ == "__main__":
    main()
