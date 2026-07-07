# ============================================================================
# faster_rcnn_detector.py
# ============================================================================

from __future__ import annotations

import cv2
import numpy as np

import torch

from torchvision.models.detection import (
    fasterrcnn_resnet50_fpn,
)

from torchvision.models.detection import (
    FasterRCNN_ResNet50_FPN_Weights,
)

from core.config import Config
from core.schemas import BoundingBox
from core.schemas import Detection

from detection.base_detector import BaseDetector


class FasterRCNNDetector(BaseDetector):
    """
    Faster R-CNN detector wrapper.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        detection_cfg = config["detection"]

        self.confidence = detection_cfg[
            "confidence"
        ]

        self.device = torch.device(
            detection_cfg["device"]
        )

        weights = (
            FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        )

        self.transforms = weights.transforms()

        self.model = (
            fasterrcnn_resnet50_fpn(
                weights=weights
            )
            .to(self.device)
            .eval()
        )

        self.class_names = weights.meta[
            "categories"
        ]

    def detect(
        self,
        frame: np.ndarray,
    ) -> list[Detection]:

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        image = self.transforms(
            rgb
        ).to(self.device)

        with torch.no_grad():

            prediction = self.model(
                [image]
            )[0]

        detections: list[Detection] = []

        for box, score, label in zip(

            prediction["boxes"],

            prediction["scores"],

            prediction["labels"],
        ):

            score = float(score)

            if score < self.confidence:
                continue

            x1, y1, x2, y2 = (
                box.cpu().numpy()
            )

            label = int(label)

            detections.append(

                Detection(

                    bbox=BoundingBox(
                        x1=float(x1),
                        y1=float(y1),
                        x2=float(x2),
                        y2=float(y2),
                    ),

                    confidence=score,

                    class_id=label,

                    class_name=self.class_names[
                        label
                    ],
                )
            )

        return detections

    def reset(
        self,
    ) -> None:

        pass