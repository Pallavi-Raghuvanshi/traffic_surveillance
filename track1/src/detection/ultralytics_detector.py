# ultralytics_detector.py
# ============================================================================

from __future__ import annotations
import numpy as np
from ultralytics import YOLO, RTDETR

from core.config import Config
from core.schemas import BoundingBox, Detection
from detection.base_detector import BaseDetector


class UltralyticsDetector(BaseDetector):
    """
    Supported models:
    - RTDETR
    - YOLO11
    - YOLO26
    - Future Ultralytics detectors
    """

    def __init__(self, config: Config) -> None:

        detection_cfg = config["detection"]
        backend = detection_cfg["backend"] # YOLO / RT-DETR
        model_path = detection_cfg["model"]

        if backend == "yolo":
            self._model = YOLO(model_path)
        elif backend == "rtdetr":
            self._model = RTDETR(model_path)
        else:
            raise ValueError(f"Unsupported Ultralytics backend: {backend}")

        self._backend = backend
        self._confidence = detection_cfg["confidence"]
        self._iou = detection_cfg["iou"]
        self._device = detection_cfg["device"]
        self._allowed_classes = {class_name.lower() for class_name in detection_cfg["classes"]}

    def detect(self, frame: np.ndarray) -> list[Detection]:

        if self._backend == "yolo":
            results = self._model.predict(
                source=frame,
                conf=self._confidence,
                iou=self._iou,
                device=self._device,
                verbose=False,
            )
        else: # RT-DETR
            results = self._model.predict(
                source=frame,
                conf=self._confidence,
                device=self._device,
                verbose=False,
            )

        detections = []

        # Process each prediction
        for result in results:
            for box in result.boxes:    

                xyxy = (box.xyxy[0].cpu().numpy())
                class_id = int(box.cls.item())
                class_name = result.names[class_id].lower()
                if (class_name not in self._allowed_classes):
                    continue # tracker focused only on vehicles.

                detections.append(
                    Detection(
                        bbox=BoundingBox(
                            x1=float(xyxy[0]),  # left
                            y1=float(xyxy[1]),  # top
                            x2=float(xyxy[2]),  # right
                            y2=float(xyxy[3])), # bottom
                        confidence=float(box.conf.item()),
                        class_id=class_id,
                        class_name=class_name,
                    )
                )

        return detections
    
    def reset(self) -> None:
        """Stateless detector"""
        pass