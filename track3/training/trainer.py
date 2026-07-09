from __future__ import annotations

import csv
import time
from pathlib import Path

import torch
from torch.optim import Adam
from torch.utils.data import DataLoader
from tqdm import tqdm

from track3.models.osnet import OSNetModel
from track3.training.losses import ReIDLoss
from track3.training.validator import Validator
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.amp import GradScaler, autocast

class Trainer:

    def __init__(
        self,
        model: OSNetModel,
        train_loader: DataLoader,
        dataset_root: str,
        learning_rate: float = 3e-4,
        checkpoint_dir: str = "track3/checkpoints",
    ) -> None:

        self.model = model
        self.device = model.device
        self.train_loader = train_loader
        self.scaler = GradScaler("cuda")
        self.loss_fn = ReIDLoss()

        self.optimizer = Adam(
            self.model.parameters(),
            lr=learning_rate,
        )
        self.scheduler = CosineAnnealingLR(
            self.optimizer,
            T_max=60,  # total epochs
            eta_min=1e-6,
        )
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.best_rank1 = 0.0

        self.validator = Validator(
            model=self.model,
            dataset_root=dataset_root,
        )

        self.log_file = self.checkpoint_dir / "training_log.csv"

        with open(self.log_file, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "epoch",
                    "loss",
                    "rank1",
                    "rank5",
                    "mAP",
                    "time_seconds",
                ]
            )

    def train_one_epoch(self) -> float:

        self.model.train()

        running_loss = 0.0

        progress = tqdm(
            self.train_loader,
            desc="Training",
        )

        for batch in progress:

            images = batch["image"].to(self.device)

            labels = batch["vehicle_id"].to(self.device)

            self.optimizer.zero_grad()
            logits = self.model(images)
            print("Images:", images.shape)
            print("Logits:", logits.shape)
            print("Labels min:", labels.min().item())
            print("Labels max:", labels.max().item())
            print("NaN logits:", torch.isnan(logits).any().item())
            loss = self.loss_fn(
                logits,
                labels,
            )

            loss.backward()

            self.optimizer.step()

            running_loss += loss.item()

            progress.set_postfix(loss=f"{loss.item():.4f}")

        return running_loss / len(self.train_loader)

    def save(
        self,
        epoch: int,
        rank1: float,
    ) -> None:

        checkpoint_path = self.checkpoint_dir / f"osnet_epoch_{epoch}.pth"

        torch.save(
            self.model.state_dict(),
            checkpoint_path,
        )

        if rank1 > self.best_rank1:

            self.best_rank1 = rank1

            torch.save(
                self.model.state_dict(),
                self.checkpoint_dir / "best_model.pth",
            )

            print("New best model saved.")

    def train(
        self,
        epochs: int,
    ) -> None:

        for epoch in range(1, epochs + 1):

            start_time = time.time()

            loss = self.train_one_epoch()

            metrics = self.validator.validate()

            elapsed = time.time() - start_time

            print("\n" + "=" * 50)

            print(f"Epoch {epoch}/{epochs}")

            print(f"Loss   : {loss:.4f}")

            print(f"Rank-1 : {metrics['rank1']*100:.2f}%")

            print(f"Rank-5 : {metrics['rank5']*100:.2f}%")

            print(f"mAP    : {metrics['mAP']*100:.2f}%")

            print(f"Time   : {elapsed:.2f} s")

            print("=" * 50)

            with open(self.log_file, "a", newline="") as file:

                writer = csv.writer(file)

                writer.writerow(
                    [
                        epoch,
                        loss,
                        metrics["rank1"],
                        metrics["rank5"],
                        metrics["mAP"],
                        elapsed,
                    ]
                )

            if epoch % 5 == 0 or epoch == 1:

                metrics = self.validator.validate()

                self.save(
                    epoch,
                    metrics["rank1"],
                )
