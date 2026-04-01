import torch

from training.dqn import DQNTrainingConfig, train_dqn
from training.dqn.checkpoint import load_checkpoint


class TestDQNTraining:
    def test_train_dqn_saves_checkpoint(self, tmp_path):
        checkpoint_path = tmp_path / "dqn_model.pt"
        config = DQNTrainingConfig(
            episodes=4,
            learning_rate=1e-3,
            epsilon_start=0.3,
            epsilon_end=0.1,
            opponent="random",
            output=str(checkpoint_path),
            eval_interval=0,
            eval_games=0,
            save_interval=0,
            log_interval=2,
            batch_size=2,
            replay_capacity=64,
            warmup_steps=1,
            train_steps_per_episode=1,
            target_sync_interval=1,
            hidden_sizes=(16,),
            device="cpu",
            seed=1,
        )

        policy_network = train_dqn(config)
        checkpoint = load_checkpoint(str(checkpoint_path), torch.device("cpu"))

        assert checkpoint_path.exists()
        assert tuple(checkpoint["hidden_sizes"]) == (16,)
        assert checkpoint["episodes_completed"] == 4
        assert checkpoint["training_steps"] > 0
        assert policy_network is not None
