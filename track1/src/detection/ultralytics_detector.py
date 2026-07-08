# ============================================================================
# ultralytics_detector.py
# ============================================================================

from __future__ import annotations

import numpy as np
from ultralytics import YOLO

from core.config import Config
from core.schemas import BoundingBox
from core.schemas import Detection

from detection.base_detector import BaseDetector


class UltralyticsDetector(BaseDetector):
    """
    Wrapper around Ultralytics detection models.

    Supported models include:

    - YOLO11
    - YOLO26
    - Future Ultralytics detectors
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        detection_cfg = config[
            "detection"
        ]

        model_path = detection_cfg[
            "model"
        ]

        if not model_path:

            raise ValueError(
                "Detection model path is required."
            )

        self._model = YOLO(
            model_path
        )

        self._confidence = detection_cfg[
            "confidence"
        ]

        self._iou = detection_cfg[
            "iou"
        ]

        self._device = detection_cfg[
            "device"
        ]

        self._allowed_classes = {

            class_name.lower()

            for class_name in detection_cfg[
                "classes"
            ]
        }

    # ------------------------------------------------------------------ #
    # Detection
    # ------------------------------------------------------------------ #

    def detect(
        self,
        frame: np.ndarray,
    ) -> list[Detection]:

        results = self._model.predict(

            source=frame,

            conf=self._confidence,

            iou=self._iou,

            device=self._device,

            verbose=False,
        )

        detections: list[
            Detection
        ] = []

        for result in results:

            names = result.names

            for box in result.boxes:

                class_id = int(
                    box.cls.item()
                )

                class_name = names[
                    class_id
                ].lower()

                if (

                    class_name

                    not in self._allowed_classes

                ):

                    continue

                xyxy = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                )

                detections.append(

                    Detection(

                        bbox=BoundingBox(

                            x1=float(
                                xyxy[0]
                            ),

                            y1=float(
                                xyxy[1]
                            ),

                            x2=float(
                                xyxy[2]
                            ),

                            y2=float(
                                xyxy[3]
                            ),
                        ),

                        confidence=float(
                            box.conf.item()
                        ),

                        class_id=class_id,

                        class_name=class_name,
                    )
                )

        return detections