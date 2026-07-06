# ============================================================================
# rtdetr_detector.py
# ============================================================================

from __future__ import annotations

import numpy as np

from core.config import Config
from core.schemas import Detection

from detection.base_detector import BaseDetector


class RTDETRDetector(BaseDetector):
    """
    Wrapper for RT-DETR detector.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        detection_cfg = config["detection"]

        self.model_name = detection_cfg["model"]

        self.device = detection_cfg["device"]

        # TODO:
        # Load RT-DETR model

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