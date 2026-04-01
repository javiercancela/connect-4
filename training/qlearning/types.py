"""Shared type aliases for Q-learning training."""

from typing import TypeAlias


QTable: TypeAlias = dict[bytes, dict[int, float]]

