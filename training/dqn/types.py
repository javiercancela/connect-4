"""Typed containers for DQN training data."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PendingTransition:
    state: np.ndarray
    action: int


@dataclass(frozen=True)
class ReplayBatch:
    states: np.ndarray
    actions: np.ndarray
    rewards: np.ndarray
    next_states: np.ndarray
    next_action_masks: np.ndarray
    dones: np.ndarray
