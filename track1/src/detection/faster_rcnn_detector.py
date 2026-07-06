# ============================================================================
# faster_rcnn_detector.py
# ============================================================================

from __future__ import annotations

import numpy as np

from core.config import Config
from core.schemas import Detection

from detection.base_detector import BaseDetector


class FasterRCNNDetector(BaseDetector):
    """
    Wrapper for Faster R-CNN.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        detection_cfg = config["detection"]

        self.model_name = detection_cfg["model"]

        self.device = detection_cfg["device"]

        # TODO:
        # Load Faster R-CNN

    def detect(
        self,
        frame: np.ndarray,
    ) -> list[Detection]:

        # TODO

        return []

    def reset(
        self,
    ) -> None:

        pass