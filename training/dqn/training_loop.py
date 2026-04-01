"""Multi-episode DQN training orchestration."""

import os
import random
import time
from dataclasses import asdict

import numpy as np
import torch

from connect4 import PLAYER_1, PLAYER_2
from connect4.constants import COLS, ROWS

from .checkpoint import load_checkpoint, save_checkpoint
from .config import DQNTrainingConfig
from .console import log
from .episode_runner import train_episode
from .evaluator import evaluate_policy
from .hardware import detect_hardware_profile
from .network import DQNNetwork
from .opponents import build_default_evaluation_opponents, build_training_opponent
from .optimization import optimize_policy_network
from .replay_buffer import ReplayBuffer


def train_dqn(config: DQNTrainingConfig) -> DQNNetwork:
    _validate_config(config)

    if config.load is not None and not os.path.exists(config.load):
        raise FileNotFoundError(f"Checkpoint not found: {config.load}")

    torch.set_float32_matmul_precision("high")

    device = torch.device(config.device)
    hardware_profile = detect_hardware_profile()
    hidden_sizes = config.hidden_sizes
    policy_network = None
    target_network = None
    optimizer = None
    completed_before_run = 0
    training_steps = 0

    checkpoint = _load_training_checkpoint(config, device)
    if checkpoint is not None:
        hidden_sizes = tuple(checkpoint["hidden_sizes"])
        completed_before_run = int(checkpoint.get("episodes_completed", 0))
        training_steps = int(checkpoint.get("training_steps", 0))

    _set_random_seed(config.seed)

    policy_network = DQNNetwork(hidden_sizes=hidden_sizes).to(device)
    target_network = DQNNetwork(hidden_sizes=hidden_sizes).to(device)
    optimizer = torch.optim.AdamW(policy_network.parameters(), lr=config.learning_rate)

    if checkpoint is not None:
        policy_network.load_state_dict(checkpoint["policy_state_dict"])
        target_state_dict = checkpoint.get("target_state_dict") or checkpoint["policy_state_dict"]
        target_network.load_state_dict(target_state_dict)

        optimizer_state_dict = checkpoint.get("optimizer_state_dict")
        if optimizer_state_dict is not None:
            optimizer.load_state_dict(optimizer_state_dict)
    else:
        target_network.load_state_dict(policy_network.state_dict())

    policy_network.train()
    target_network.eval()

    opponent = build_training_opponent(config.opponent, config.minimax_depth)
    replay_buffer = ReplayBuffer(
        capacity=config.replay_capacity,
        state_size=ROWS * COLS,
        action_size=COLS,
    )

    _log_training_config(config, hidden_sizes, hardware_profile)
    if checkpoint is not None:
        log(
            "Resuming from "
            f"{completed_before_run:,} completed episodes and {training_steps:,} gradient steps."
        )

    start_time = time.time()
    run_wins = run_draws = run_losses = 0
    run_loss_sum = 0.0
    run_loss_updates = 0
    total_completed = completed_before_run

    try:
        for episode in range(1, config.episodes + 1):
            epsilon = config.epsilon_for_episode(episode)
            winner, learning_player = train_episode(
                policy_network=policy_network,
                replay_buffer=replay_buffer,
                opponent=opponent,
                epsilon=epsilon,
                draw_reward=config.draw_reward,
                device=device,
            )
            total_completed += 1
            run_wins, run_draws, run_losses = _update_interval_results(
                run_wins,
                run_draws,
                run_losses,
                winner,
                learning_player,
                opponent is None,
            )

            for _ in range(config.train_steps_per_episode):
                if len(replay_buffer) < max(config.batch_size, config.warmup_steps):
                    break

                loss = optimize_policy_network(
                    policy_network=policy_network,
                    target_network=target_network,
                    optimizer=optimizer,
                    replay_buffer=replay_buffer,
                    batch_size=config.batch_size,
                    gamma=config.gamma,
                    gradient_clip=config.gradient_clip,
                    device=device,
                )
                training_steps += 1
                run_loss_sum += loss
                run_loss_updates += 1

                if training_steps % config.target_sync_interval == 0:
                    target_network.load_state_dict(policy_network.state_dict())

            if episode % config.log_interval == 0:
                _log_progress(
                    episode=episode,
                    total_completed=total_completed,
                    start_time=start_time,
                    wins=run_wins,
                    draws=run_draws,
                    losses=run_losses,
                    epsilon=epsilon,
                    replay_size=len(replay_buffer),
                    average_loss=_average_loss(run_loss_sum, run_loss_updates),
                    is_self_play=opponent is None,
                )
                run_wins = run_draws = run_losses = 0
                run_loss_sum = 0.0
                run_loss_updates = 0

            if config.eval_interval > 0 and episode % config.eval_interval == 0:
                _run_evaluations(policy_network, device, config.eval_games)

            if config.save_interval > 0 and episode % config.save_interval == 0:
                save_checkpoint(
                    path=config.output,
                    policy_network=policy_network,
                    target_network=target_network,
                    optimizer=optimizer,
                    hidden_sizes=hidden_sizes,
                    episodes_completed=total_completed,
                    training_steps=training_steps,
                    config=asdict(config),
                )
                log(f"Saved checkpoint to {config.output}")

    except KeyboardInterrupt:
        log(f"Interrupted after {total_completed:,} episodes.")

    elapsed = time.time() - start_time
    log(f"Training finished in {elapsed:.1f}s ({total_completed:,} total episodes).")
    log(f"Replay buffer size: {len(replay_buffer):,} transitions.")

    save_checkpoint(
        path=config.output,
        policy_network=policy_network,
        target_network=target_network,
        optimizer=optimizer,
        hidden_sizes=hidden_sizes,
        episodes_completed=total_completed,
        training_steps=training_steps,
        config=asdict(config),
    )
    log(f"Saved final checkpoint to {config.output}")

    if config.eval_games > 0:
        log(f"Final evaluation ({config.eval_games} games each).")
        _run_evaluations(policy_network, device, config.eval_games)

    return policy_network


def _validate_config(config: DQNTrainingConfig) -> None:
    if config.episodes <= 0:
        raise ValueError("episodes must be positive")
    if config.batch_size <= 0:
        raise ValueError("batch_size must be positive")
    if config.replay_capacity <= 0:
        raise ValueError("replay_capacity must be positive")
    if config.log_interval <= 0:
        raise ValueError("log_interval must be positive")
    if config.target_sync_interval <= 0:
        raise ValueError("target_sync_interval must be positive")
    if config.train_steps_per_episode < 0:
        raise ValueError("train_steps_per_episode cannot be negative")


def _load_training_checkpoint(config: DQNTrainingConfig, device: torch.device) -> dict | None:
    if config.load is None:
        return None

    log(f"Loading checkpoint from {config.load}")
    return load_checkpoint(config.load, device)


def _set_random_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _log_training_config(
    config: DQNTrainingConfig,
    hidden_sizes: tuple[int, ...],
    hardware_profile,
) -> None:
    gpu_fragment = (
        f"{hardware_profile.gpu_name} ({hardware_profile.gpu_memory_gb:.1f} GB)"
        if hardware_profile.gpu_name is not None
        else "none"
    )
    log("DQN training config:")
    log(f"  Device: {config.device}")
    log(f"  CPU cores: {hardware_profile.cpu_count}")
    log(f"  GPU: {gpu_fragment}")
    log(f"  Episodes: {config.episodes:,}")
    log(f"  Opponent: {config.opponent}")
    log(f"  Hidden sizes: {hidden_sizes}")
    log(f"  Learning rate: {config.learning_rate}")
    log(f"  Gamma: {config.gamma}")
    log(f"  Epsilon: {config.epsilon_start} -> {config.epsilon_end}")
    log(f"  Batch size: {config.batch_size:,}")
    log(f"  Replay capacity: {config.replay_capacity:,}")
    log(f"  Warmup steps: {config.warmup_steps:,}")
    log(f"  Train steps/episode: {config.train_steps_per_episode}")
    log(f"  Target sync interval: {config.target_sync_interval:,}")
    log(f"  Output: {config.output}")


def _update_interval_results(
    wins: int,
    draws: int,
    losses: int,
    winner: int | None,
    learning_player: int | None,
    is_self_play: bool,
) -> tuple[int, int, int]:
    if is_self_play:
        if winner == PLAYER_1:
            return wins + 1, draws, losses
        if winner == PLAYER_2:
            return wins, draws, losses + 1
        return wins, draws + 1, losses

    if winner == learning_player:
        return wins + 1, draws, losses
    if winner is None:
        return wins, draws + 1, losses
    return wins, draws, losses + 1


def _log_progress(
    episode: int,
    total_completed: int,
    start_time: float,
    wins: int,
    draws: int,
    losses: int,
    epsilon: float,
    replay_size: int,
    average_loss: float,
    is_self_play: bool,
) -> None:
    elapsed = time.time() - start_time
    episodes_per_second = total_completed / elapsed if elapsed > 0 else 0.0
    total = wins + draws + losses

    if total == 0:
        result_fragment = "No interval games recorded"
    elif is_self_play:
        result_fragment = (
            f"P1/D/P2 {100 * wins / total:.0f}/"
            f"{100 * draws / total:.0f}/"
            f"{100 * losses / total:.0f}%"
        )
    else:
        result_fragment = (
            f"Agent/D/Opp {100 * wins / total:.0f}/"
            f"{100 * draws / total:.0f}/"
            f"{100 * losses / total:.0f}%"
        )

    loss_fragment = f"{average_loss:.4f}" if average_loss == average_loss else "n/a"
    log(
        f"Episode {episode:>9,} | "
        f"{result_fragment} | "
        f"Replay {replay_size:>9,} | "
        f"Loss {loss_fragment:>7} | "
        f"Eps {epsilon:.3f} | "
        f"{episodes_per_second:.0f} ep/s"
    )


def _average_loss(loss_sum: float, loss_updates: int) -> float:
    if loss_updates == 0:
        return float("nan")
    return loss_sum / loss_updates


def _run_evaluations(policy_network, device: torch.device, num_games: int) -> None:
    for name, opponent in build_default_evaluation_opponents():
        results = evaluate_policy(policy_network, opponent, device=device, num_games=num_games)
        wins = results["win"]
        draws = results["draw"]
        losses = results["loss"]
        log(
            f"  vs {name:>10}: "
            f"W {wins:>3}  D {draws:>3}  L {losses:>3}  "
            f"({100 * wins / num_games:.1f}% win)"
        )
