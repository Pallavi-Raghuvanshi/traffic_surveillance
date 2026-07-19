# faster_rcnn_detector.py
# ============================================================================

from __future__ import annotations
import cv2
import numpy as np
import torch # tensors, GPU, Inference, models
from PIL import Image

from torchvision.models.detection import (
    FasterRCNN_ResNet50_FPN_Weights, # pretrained weights
    fasterrcnn_resnet50_fpn, # model architecture
)

from src.core.config import Config
from src.core.schemas import BoundingBox, Detection
from src.detection.base_detector import BaseDetector

class FasterRCNNDetector(BaseDetector):

    # Initialize the detector
    def __init__(self, config: Config) -> None:

        detection_cfg = config["detection"]
        self._confidence = detection_cfg["confidence"] # ignores detections below it
        self._device = torch.device(detection_cfg["device"]) # later runs automatically with torch.device()
        self._allowed_classes = {class_name.lower() for class_name in detection_cfg["classes"]}

        weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        self._transforms = weights.transforms() # preprocessing pipeline
        self._model = fasterrcnn_resnet50_fpn(weights=weights).to(self._device).eval()
        self._class_names = weights.meta["categories"]

    # detects objects in one frame  
    def detect(self, frame: np.ndarray) -> list[Detection]:
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Numpy array -> PIL image 
        image = Image.fromarray(rgb) 
        image = self._transforms(image).to(self._device) 
        # transformed image moved to the same device as the model

        with torch.no_grad(): # disable gradient
            prediction = self._model([image])[0]
        detections = []

        # Process each detection
        for box, score, label in zip(prediction["boxes"], prediction["scores"], prediction["labels"]):

            score = float(score.item())
            if score < self._confidence:
                continue

            label = int(label.item())
            class_name = self._class_names[label].lower()

            if class_name not in self._allowed_classes:
                continue

            x1, y1, x2, y2 = (box.cpu().numpy())

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
                    class_name=class_name,
                )
            )
            
        return detections

    def reset(self) -> None:
        """Stateless detector"""
        pass