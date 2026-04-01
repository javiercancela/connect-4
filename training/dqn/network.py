"""Neural network used by the DQN trainer and agent."""

import torch
from torch import nn

from connect4.constants import COLS, ROWS


class DQNNetwork(nn.Module):
    def __init__(self, hidden_sizes: tuple[int, ...]):
        super().__init__()

        layers: list[nn.Module] = []
        input_size = ROWS * COLS

        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(input_size, hidden_size))
            layers.append(nn.ReLU())
            input_size = hidden_size

        layers.append(nn.Linear(input_size, COLS))
        self._model = nn.Sequential(*layers)

    def forward(self, states: torch.Tensor) -> torch.Tensor:
        return self._model(states)
