import torch.nn as nn

class DQN(nn.Module):
  def __init__(self, input_dimensions, output_dimensions):
    super(DQN, self).__init__()
    self.network = nn.Sequential(
      nn.Linear(input_dimensions, 128),
      nn.ReLU(),
      nn.Linear(128, 128),
      nn.ReLU(),
      nn.Linear(128, output_dimensions)
    )

  def forward(self, state):
    return self.network(state)
