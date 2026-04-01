"""Persistence helpers for Q-learning tables."""

import gzip
import os
import pickle

from .types import QTable


def save_qtable(q_table: QTable, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with gzip.open(path, "wb") as file_handle:
        pickle.dump(q_table, file_handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_qtable(path: str) -> QTable:
    with gzip.open(path, "rb") as file_handle:
        return pickle.load(file_handle)

