"""Hardware detection and local training recommendations."""

import os
from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class HardwareProfile:
    device: str
    cpu_count: int
    gpu_name: str | None
    gpu_memory_gb: float
    hidden_sizes: tuple[int, ...]
    batch_size: int
    replay_capacity: int
    warmup_steps: int
    train_steps_per_episode: int
    target_sync_interval: int


def detect_hardware_profile() -> HardwareProfile:
    cpu_count = os.cpu_count() or 1

    if torch.cuda.is_available():
        properties = torch.cuda.get_device_properties(0)
        gpu_memory_gb = properties.total_memory / (1024**3)

        if gpu_memory_gb >= 14:
            return HardwareProfile(
                device="cuda",
                cpu_count=cpu_count,
                gpu_name=properties.name,
                gpu_memory_gb=gpu_memory_gb,
                hidden_sizes=(512, 256, 128),
                batch_size=2048,
                replay_capacity=300_000,
                warmup_steps=5_000,
                train_steps_per_episode=2,
                target_sync_interval=2_000,
            )

        if gpu_memory_gb >= 8:
            return HardwareProfile(
                device="cuda",
                cpu_count=cpu_count,
                gpu_name=properties.name,
                gpu_memory_gb=gpu_memory_gb,
                hidden_sizes=(384, 192, 96),
                batch_size=1024,
                replay_capacity=200_000,
                warmup_steps=4_000,
                train_steps_per_episode=2,
                target_sync_interval=2_000,
            )

        return HardwareProfile(
            device="cuda",
            cpu_count=cpu_count,
            gpu_name=properties.name,
            gpu_memory_gb=gpu_memory_gb,
            hidden_sizes=(256, 128),
            batch_size=512,
            replay_capacity=100_000,
            warmup_steps=2_000,
            train_steps_per_episode=1,
            target_sync_interval=1_000,
        )

    batch_size = 512 if cpu_count >= 12 else 256
    return HardwareProfile(
        device="cpu",
        cpu_count=cpu_count,
        gpu_name=None,
        gpu_memory_gb=0.0,
        hidden_sizes=(256, 128),
        batch_size=batch_size,
        replay_capacity=100_000,
        warmup_steps=2_000,
        train_steps_per_episode=1,
        target_sync_interval=1_000,
    )
