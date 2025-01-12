import torch.nn as nn

BOARD_SIZE = 6 * 7
POSSIBLE_MOVES = 7


class DQN(nn.Module):

    def __init__(self):
        super(DQN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(BOARD_SIZE, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, POSSIBLE_MOVES),
        )
        self.file_path = str(__file__).replace("dqn_nn.py", "dqn_model.pth")

    def forward(self, state):
        return self.network(state)
