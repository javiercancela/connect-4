import torch.nn as nn

BOARD_SIZE = 6 * 7
POSSIBLE_MOVES = 7


class DQN01(nn.Module):

    def __init__(self, file_path="dqn01_model.pth"):
        super(DQN01, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(BOARD_SIZE, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, POSSIBLE_MOVES),
        )
        self.file_path = file_path

    def forward(self, state):
        return self.network(state)
