import torch

from agents import DQNAgent
from connect4 import Connect4
from training.dqn.checkpoint import save_checkpoint
from training.dqn.network import DQNNetwork


class TestDQNAgent:
    def test_select_move_uses_highest_valid_q_value(self, tmp_path):
        checkpoint_path = tmp_path / "dqn_model.pt"
        network = DQNNetwork(hidden_sizes=(8,))

        with torch.no_grad():
            for parameter in network.parameters():
                parameter.zero_()

            network._model[-1].bias.copy_(
                torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], dtype=torch.float32)
            )

        save_checkpoint(
            path=str(checkpoint_path),
            policy_network=network,
            hidden_sizes=(8,),
        )

        game = Connect4()
        game._board._grid[:, 6] = 1

        agent = DQNAgent(checkpoint_path=str(checkpoint_path))
        move = agent.select_move(game)

        assert move == 5
