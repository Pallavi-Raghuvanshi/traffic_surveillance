# ============================================================================
# ultralytics_detector.py
# ============================================================================

from __future__ import annotations

from ultralytics import YOLO
import numpy as np

from core.config import Config
from core.schemas import BoundingBox
from core.schemas import Detection

from detection.base_detector import BaseDetector


class UltralyticsDetector(BaseDetector):
    """
    Wrapper around Ultralytics detectors.

    Supports:
    - YOLO11
    - RT-DETR
    - Future Ultralytics models
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        detection_cfg = config["detection"]

        self.model = YOLO(
            detection_cfg["model"]
        )

        self.confidence = detection_cfg["confidence"]

        self.iou = detection_cfg["iou"]

        self.device = detection_cfg["device"]

        self.allowed_classes = {
            name.lower()
            for name in detection_cfg["classes"]
        }

    def detect(
        self,
        frame: np.ndarray,
    ) -> list[Detection]:

        results = self.model.predict(
            frame,
            conf=self.confidence,
            iou=self.iou,
            device=self.device,
            verbose=False,
        )

        detections: list[Detection] = []

        for result in results:

            names = result.names

            for box in result.boxes:

                class_id = int(box.cls)

                class_name = names[
                    class_id
                ].lower()

                if (
                    class_name
                    not in self.allowed_classes
                ):
                    continue

                bbox = BoundingBox(

                    x1=float(box.xyxy[0][0]),

                    y1=float(box.xyxy[0][1]),

                    x2=float(box.xyxy[0][2]),

                    y2=float(box.xyxy[0][3]),
                )

                detections.append(

                    Detection(

                        bbox=bbox,

                        confidence=float(
                            box.conf
                        ),

                        class_id=class_id,

                        class_name=class_name,
                    )
                )

        return detections