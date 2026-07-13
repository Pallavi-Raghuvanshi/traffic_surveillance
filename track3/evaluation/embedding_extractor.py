from __future__ import annotations

from typing import Tuple

import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from track3.models.osnet import OSNetModel


class EmbeddingExtractor:
    """
    Extract embeddings from an OSNet model.
    """

    def __init__(self, model: OSNetModel):

        self.model = model
        self.device = model.device

        self.model.eval()

    @torch.inference_mode()
    def extract(
        self,
        dataloader: DataLoader,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

        embeddings = []
        labels = []
        camera_ids = []

        for batch in tqdm(
            dataloader,
            desc="Extracting Embeddings",
        ):

            images = batch["image"].to(self.device)

            outputs = self.model(images)

            embeddings.append(outputs.cpu().numpy())

            labels.append(batch["vehicle_id"].numpy())

            camera_ids.append(batch["camera_id"].numpy())

        embeddings = np.concatenate(
            embeddings,
            axis=0,
        )

        labels = np.concatenate(
            labels,
            axis=0,
        )

        camera_ids = np.concatenate(
            camera_ids,
            axis=0,
        )

        return (
            embeddings,
            labels,
            camera_ids,
        )
