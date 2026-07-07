# ============================================================================
# rtdetr_detector.py
# ============================================================================

from __future__ import annotations

import numpy as np

from ultralytics import RTDETR

from core.config import Config
from core.schemas import BoundingBox
from core.schemas import Detection

from detection.base_detector import BaseDetector


class RTDETRDetector(BaseDetector):
    """
    RT-DETR detector wrapper.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        detection_cfg = config["detection"]

        self.model = RTDETR(
            detection_cfg["model"]
        )

        self.confidence = detection_cfg[
            "confidence"
        ]

        self.device = detection_cfg[
            "device"
        ]

    def detect(
        self,
        frame: np.ndarray,
    ) -> list[Detection]:

        results = self.model.predict(

            source=frame,

            conf=self.confidence,

            device=self.device,

            verbose=False,
        )

        detections: list[Detection] = []

        for result in results:

            for box in result.boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                )

                detections.append(

                    Detection(

                        bbox=BoundingBox(
                            x1=float(x1),
                            y1=float(y1),
                            x2=float(x2),
                            y2=float(y2),
                        ),

                        confidence=float(
                            box.conf.item()
                        ),

                        class_id=int(
                            box.cls.item()
                        ),

                        class_name=result.names[
                            int(box.cls.item())
                        ],
                    )
                )

        return detections

    def reset(
        self,
    ) -> None:

        pass