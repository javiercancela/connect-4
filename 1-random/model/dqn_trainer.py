from data.connect4_dataset import Connect4Dataset
from torch.utils.data import DataLoader
import torch
import torch.optim as optim
import torch.nn as nn

from model.dqn_nn import DQN
import time

# Hyperparameters
BATCH_SIZE = 64
LR = 1e-3
GAMMA = 0.99
EPOCHS = 10


class DQNTrainer:
    def __init__(self):
        self.dataloader = DataLoader(
            Connect4Dataset(), batch_size=BATCH_SIZE, shuffle=True
        )
        self.model = DQN()
        self.optimizer = optim.Adam(self.model.parameters(), lr=LR)
        self.loss_function = nn.MSELoss()

    def train(self):
        for epoch in range(EPOCHS):
            start_time = time.time()
            total_loss = 0
            for states, actions, rewards in self.dataloader:
                states = states.clone().detach().to(dtype=torch.float32)
                actions = actions.clone().detach().to(dtype=torch.long)
                rewards = rewards.clone().detach().to(dtype=torch.float32)

                # Predict Q-values
                q_values = self.model(states)
                q_value = q_values.gather(1, actions.view(-1, 1)).squeeze()

                # Compute target Q-values
                with torch.no_grad():
                    max_next_q_values = q_values.max(1)[0]
                    targets = rewards + GAMMA * max_next_q_values

                # Compute loss and optimize
                loss = self.loss_function(q_value, targets)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()

            elapsed_time = time.time() - start_time
            print(
                f"Epoch {epoch + 1}/{EPOCHS}, Loss: {total_loss / len(self.dataloader)}, Time: {elapsed_time:.2f} seconds"
            )

        torch.save(self.model.state_dict(), self.model.file_path)
        print(f"Model saved as {self.model.file_path}")
