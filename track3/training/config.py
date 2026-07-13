from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TrainingConfig:
    """
    Configuration for OSNet fine-tuning.
    """

    dataset_root: Path

    batch_size: int = 32

    epochs: int = 60

    learning_rate: float = 3e-4

    weight_decay: float = 5e-4

    num_workers: int = 4

    checkpoint_dir: Path = Path("track3/checkpoints")

    save_every: int = 5

    optimizer: str = "adam"

    scheduler: str = "cosine"

    triplet_margin: float = 0.3