"""Configuration model for Q-learning training."""

from dataclasses import dataclass


@dataclass(frozen=True)
class QLearningTrainingConfig:
    episodes: int = 500_000
    alpha: float = 0.1
    alpha_end: float = 0.01
    gamma: float = 0.95
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    trace_decay: float = 0.7
    draw_reward: float = 0.5
    opponents: tuple[str, ...] = ("self",)
    minimax_depth: int = 2
    output: str = "models/qtable.pkl.gz"
    load: str | None = None
    eval_interval: int = 50_000
    eval_games: int = 200
    save_interval: int = 0

    def alpha_for_episode(self, episode: int) -> float:
        progress = episode / self.episodes
        return self.alpha + (self.alpha_end - self.alpha) * progress

    def epsilon_for_episode(self, episode: int) -> float:
        progress = episode / self.episodes
        return self.epsilon_start + (self.epsilon_end - self.epsilon_start) * progress

    def opponent_for_episode(self, episode: int) -> str:
        if len(self.opponents) == 1:
            return self.opponents[0]
        phase_size = self.episodes / len(self.opponents)
        phase_index = min(int((episode - 1) / phase_size), len(self.opponents) - 1)
        return self.opponents[phase_index]

