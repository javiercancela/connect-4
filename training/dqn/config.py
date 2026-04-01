"""Configuration model for DQN training."""

from dataclasses import dataclass

from .hardware import HardwareProfile, detect_hardware_profile


@dataclass(frozen=True)
class DQNTrainingConfig:
    episodes: int = 150_000
    learning_rate: float = 1e-4
    gamma: float = 0.99
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    draw_reward: float = 0.25
    opponent: str = "self"
    minimax_depth: int = 2
    output: str = "models/dqn_model.pt"
    load: str | None = None
    eval_interval: int = 10_000
    eval_games: int = 100
    save_interval: int = 25_000
    log_interval: int = 2_000
    batch_size: int = 2048
    replay_capacity: int = 300_000
    warmup_steps: int = 5_000
    train_steps_per_episode: int = 2
    target_sync_interval: int = 2_000
    hidden_sizes: tuple[int, ...] = (512, 256, 128)
    device: str = "cuda"
    gradient_clip: float = 5.0
    seed: int = 7

    def epsilon_for_episode(self, episode: int, total_episodes: int | None = None) -> float:
        total = total_episodes if total_episodes is not None else self.episodes
        if total <= 1:
            return self.epsilon_end

        progress = (episode - 1) / (total - 1)
        return self.epsilon_start + (self.epsilon_end - self.epsilon_start) * progress


def build_recommended_config(profile: HardwareProfile | None = None) -> DQNTrainingConfig:
    hardware_profile = profile or detect_hardware_profile()
    return DQNTrainingConfig(
        batch_size=hardware_profile.batch_size,
        replay_capacity=hardware_profile.replay_capacity,
        warmup_steps=hardware_profile.warmup_steps,
        train_steps_per_episode=hardware_profile.train_steps_per_episode,
        target_sync_interval=hardware_profile.target_sync_interval,
        hidden_sizes=hardware_profile.hidden_sizes,
        device=hardware_profile.device,
    )
