"""Checkpoint persistence for DQN models."""

import os

import torch

from .network import DQNNetwork


def save_checkpoint(
    path: str,
    policy_network: DQNNetwork,
    hidden_sizes: tuple[int, ...],
    *,
    target_network: DQNNetwork | None = None,
    optimizer: torch.optim.Optimizer | None = None,
    episodes_completed: int = 0,
    training_steps: int = 0,
    config: dict | None = None,
) -> None:
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)

    payload = {
        "policy_state_dict": policy_network.state_dict(),
        "target_state_dict": target_network.state_dict() if target_network is not None else None,
        "optimizer_state_dict": optimizer.state_dict() if optimizer is not None else None,
        "episodes_completed": episodes_completed,
        "training_steps": training_steps,
        "hidden_sizes": tuple(hidden_sizes),
        "config": config,
    }
    torch.save(payload, path)


def load_checkpoint(path: str, device: torch.device) -> dict:
    return torch.load(path, map_location=device)


def load_policy_network(path: str, device: torch.device) -> tuple[DQNNetwork, dict]:
    checkpoint = load_checkpoint(path, device)
    hidden_sizes = tuple(checkpoint["hidden_sizes"])
    policy_network = DQNNetwork(hidden_sizes=hidden_sizes)
    policy_network.load_state_dict(checkpoint["policy_state_dict"])
    policy_network.to(device)
    policy_network.eval()
    return policy_network, checkpoint
