"""Replay buffer with fixed-size numpy storage."""

import numpy as np

from .types import ReplayBatch


class ReplayBuffer:
    def __init__(self, capacity: int, state_size: int, action_size: int):
        self._capacity = capacity
        self._states = np.zeros((capacity, state_size), dtype=np.float32)
        self._actions = np.zeros(capacity, dtype=np.int64)
        self._rewards = np.zeros(capacity, dtype=np.float32)
        self._next_states = np.zeros((capacity, state_size), dtype=np.float32)
        self._next_action_masks = np.zeros((capacity, action_size), dtype=np.bool_)
        self._dones = np.zeros(capacity, dtype=np.bool_)
        self._next_index = 0
        self._size = 0

    def add(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray | None,
        next_action_mask: np.ndarray | None,
        done: bool,
    ) -> None:
        index = self._next_index
        self._states[index] = state
        self._actions[index] = action
        self._rewards[index] = reward
        self._dones[index] = done

        if next_state is None:
            self._next_states[index].fill(0.0)
        else:
            self._next_states[index] = next_state

        if next_action_mask is None:
            self._next_action_masks[index].fill(False)
        else:
            self._next_action_masks[index] = next_action_mask

        self._next_index = (index + 1) % self._capacity
        self._size = min(self._size + 1, self._capacity)

    def sample(self, batch_size: int) -> ReplayBatch:
        indices = np.random.choice(self._size, size=batch_size, replace=False)
        return ReplayBatch(
            states=self._states[indices],
            actions=self._actions[indices],
            rewards=self._rewards[indices],
            next_states=self._next_states[indices],
            next_action_masks=self._next_action_masks[indices],
            dones=self._dones[indices],
        )

    def __len__(self) -> int:
        return self._size
