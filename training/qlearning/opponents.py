"""Opponent factories used during training and evaluation."""

from agents import HeuristicAgent, MinimaxAgent, RandomAgent


def build_training_opponent(name: str, minimax_depth: int = 2):
    if name == "self":
        return None
    if name == "random":
        return RandomAgent()
    if name == "heuristic":
        return HeuristicAgent()
    if name == "minimax":
        return MinimaxAgent(depth=minimax_depth)
    raise ValueError(f"Unknown opponent: {name}")


def build_default_evaluation_opponents() -> list[tuple[str, object]]:
    return [
        ("Random", RandomAgent()),
        ("Heuristic", HeuristicAgent()),
    ]

