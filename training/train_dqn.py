"""CLI entrypoint for DQN training."""

import argparse

from training.dqn import DQNTrainingConfig, build_recommended_config, train_dqn


def build_parser() -> argparse.ArgumentParser:
    default_config = build_recommended_config()

    parser = argparse.ArgumentParser(
        description="Train a Deep Q-Network agent for Connect-4",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--episodes", type=int, default=default_config.episodes, help="Training episodes")
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=default_config.learning_rate,
        help="Optimizer learning rate",
    )
    parser.add_argument("--gamma", type=float, default=default_config.gamma, help="Discount factor")
    parser.add_argument(
        "--epsilon-start",
        type=float,
        default=default_config.epsilon_start,
        help="Initial exploration rate",
    )
    parser.add_argument(
        "--epsilon-end",
        type=float,
        default=default_config.epsilon_end,
        help="Final exploration rate",
    )
    parser.add_argument(
        "--draw-reward",
        type=float,
        default=default_config.draw_reward,
        help="Reward for drawn games",
    )
    parser.add_argument(
        "--opponent",
        type=str,
        default=default_config.opponent,
        choices=["self", "random", "heuristic", "minimax"],
        help="Training opponent",
    )
    parser.add_argument(
        "--minimax-depth",
        type=int,
        default=default_config.minimax_depth,
        help="Minimax opponent search depth",
    )
    parser.add_argument("--output", type=str, default=default_config.output, help="Output checkpoint path")
    parser.add_argument("--load", type=str, default=None, help="Resume from a checkpoint")
    parser.add_argument(
        "--eval-interval",
        type=int,
        default=default_config.eval_interval,
        help="Evaluate every N episodes (0 to disable)",
    )
    parser.add_argument("--eval-games", type=int, default=default_config.eval_games, help="Games per evaluation opponent")
    parser.add_argument(
        "--save-interval",
        type=int,
        default=default_config.save_interval,
        help="Save checkpoint every N episodes (0 to disable)",
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=default_config.log_interval,
        help="Log progress every N episodes",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=default_config.batch_size,
        help="Replay samples per gradient update",
    )
    parser.add_argument(
        "--replay-capacity",
        type=int,
        default=default_config.replay_capacity,
        help="Maximum replay buffer size",
    )
    parser.add_argument(
        "--warmup-steps",
        type=int,
        default=default_config.warmup_steps,
        help="Replay size required before training starts",
    )
    parser.add_argument(
        "--train-steps-per-episode",
        type=int,
        default=default_config.train_steps_per_episode,
        help="Gradient updates performed after each episode",
    )
    parser.add_argument(
        "--target-sync-interval",
        type=int,
        default=default_config.target_sync_interval,
        help="Gradient steps between target network copies",
    )
    parser.add_argument(
        "--hidden-sizes",
        type=int,
        nargs="+",
        default=list(default_config.hidden_sizes),
        help="Hidden layer sizes for the Q-network",
    )
    parser.add_argument("--device", type=str, default=default_config.device, help="Torch device")
    parser.add_argument(
        "--gradient-clip",
        type=float,
        default=default_config.gradient_clip,
        help="Gradient norm clipping value",
    )
    parser.add_argument("--seed", type=int, default=default_config.seed, help="Random seed")
    return parser


def parse_args() -> DQNTrainingConfig:
    args = build_parser().parse_args()
    return DQNTrainingConfig(
        episodes=args.episodes,
        learning_rate=args.learning_rate,
        gamma=args.gamma,
        epsilon_start=args.epsilon_start,
        epsilon_end=args.epsilon_end,
        draw_reward=args.draw_reward,
        opponent=args.opponent,
        minimax_depth=args.minimax_depth,
        output=args.output,
        load=args.load,
        eval_interval=args.eval_interval,
        eval_games=args.eval_games,
        save_interval=args.save_interval,
        log_interval=args.log_interval,
        batch_size=args.batch_size,
        replay_capacity=args.replay_capacity,
        warmup_steps=args.warmup_steps,
        train_steps_per_episode=args.train_steps_per_episode,
        target_sync_interval=args.target_sync_interval,
        hidden_sizes=tuple(args.hidden_sizes),
        device=args.device,
        gradient_clip=args.gradient_clip,
        seed=args.seed,
    )


def main() -> None:
    config = parse_args()
    train_dqn(config)


if __name__ == "__main__":
    main()
