"""Q-table value access helpers."""

from .types import QTable


def get_q_value(q_table: QTable, state_key: bytes, action: int) -> float:
    entry = q_table.get(state_key)
    if entry is None:
        return 0.0
    return entry.get(action, 0.0)


def set_q_value(q_table: QTable, state_key: bytes, action: int, value: float) -> None:
    entry = q_table.get(state_key)
    if entry is None:
        q_table[state_key] = {action: value}
        return
    entry[action] = value

