"""Gradient update helpers for the DQN trainer."""

import torch
import torch.nn.functional as F
from torch.nn.utils import clip_grad_norm_

from .replay_buffer import ReplayBuffer


def optimize_policy_network(
    policy_network,
    target_network,
    optimizer: torch.optim.Optimizer,
    replay_buffer: ReplayBuffer,
    batch_size: int,
    gamma: float,
    gradient_clip: float,
    device: torch.device,
) -> float:
    batch = replay_buffer.sample(batch_size)

    states = torch.as_tensor(batch.states, dtype=torch.float32, device=device)
    actions = torch.as_tensor(batch.actions, dtype=torch.long, device=device)
    rewards = torch.as_tensor(batch.rewards, dtype=torch.float32, device=device)
    next_states = torch.as_tensor(batch.next_states, dtype=torch.float32, device=device)
    next_action_masks = torch.as_tensor(batch.next_action_masks, dtype=torch.bool, device=device)
    dones = torch.as_tensor(batch.dones, dtype=torch.bool, device=device)

    current_q_values = policy_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)

    with torch.no_grad():
        next_q_values = target_network(next_states)
        masked_next_q_values = next_q_values.masked_fill(~next_action_masks, float("-inf"))
        max_next_q_values = masked_next_q_values.max(dim=1).values
        max_next_q_values = torch.where(
            dones,
            torch.zeros_like(max_next_q_values),
            max_next_q_values,
        )
        targets = rewards + gamma * max_next_q_values

    loss = F.smooth_l1_loss(current_q_values, targets)

    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    clip_grad_norm_(policy_network.parameters(), max_norm=gradient_clip)
    optimizer.step()

    return float(loss.item())
