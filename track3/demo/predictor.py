from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from track3.data.transforms import test_transform
from track3.models.osnet import OSNetModel


class VehicleReIDPredictor:

    def __init__(
        self,
        checkpoint_path: str | Path,
    ):

        self.device = (
            torch.device("cuda")
            if torch.cuda.is_available()
            else torch.device("cpu")
        )

        checkpoint = torch.load(
            checkpoint_path,
            map_location=self.device,
        )

        classifier_weight = checkpoint["model.classifier.weight"]

        num_classes = classifier_weight.shape[0]

        self.model = OSNetModel(
            num_classes=num_classes,
            loss="softmax",
        )

        self.model.load_state_dict(checkpoint)

        self.model.eval()

    @torch.inference_mode()
    def embedding(
        self,
        image_path: str | Path,
    ) -> np.ndarray:

        image = Image.open(image_path).convert("RGB")

        tensor = test_transform(image)

        tensor = tensor.unsqueeze(0)

        tensor = tensor.to(self.device)

        embedding = self.model(tensor)

        embedding = F.normalize(
            embedding,
            dim=1,
        )

        return embedding.squeeze(0).cpu().numpy()

    def compare(
        self,
        image1: str | Path,
        image2: str | Path,
    ) -> dict:

        start = time.perf_counter()

        embedding1 = self.embedding(image1)

        embedding2 = self.embedding(image2)

        similarity = float(
            np.dot(
                embedding1,
                embedding2,
            )
        )

        elapsed = time.perf_counter() - start

        return {

            "similarity": similarity,

            "percentage": similarity * 100,

            "prediction":
                "Same Vehicle"
                if similarity >= 0.80
                else "Different Vehicle",

            "embedding_dimension": 512,

            "device": str(self.device).upper(),

            "model": "OSNet x1.0",

            "checkpoint": Path(image1).parent.parent.parent
            / "checkpoints"
            / "best_model.pth",

            "inference_time": elapsed,
        }