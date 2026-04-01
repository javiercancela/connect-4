"""Configuration model for Q-learning training."""

from dataclasses import dataclass


@dataclass(frozen=True)
class QLearningTrainingConfig:
    episodes: int = 500_000
    alpha: float = 0.1
    gamma: float = 0.95
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    draw_reward: float = 0.5
    opponent: str = "self"
    minimax_depth: int = 2
    output: str = "models/qtable.pkl.gz"
    load: str | None = None
    eval_interval: int = 50_000
    eval_games: int = 200
    save_interval: int = 0

    def epsilon_for_episode(self, episode: int) -> float:
        progress = episode / self.episodes
        return self.epsilon_start + (self.epsilon_end - self.epsilon_start) * progress

