from __future__ import annotations

from core.config import Config

from detection.base_detector import BaseDetector

from detection.ultralytics_detector import (
    UltralyticsDetector,
)

from detection.rtdetr_detector import (
    RTDETRDetector,
)

from detection.faster_rcnn_detector import (
    FasterRCNNDetector,
)


class DetectorFactory:

    @staticmethod
    def create(
        config: Config,
    ) -> BaseDetector:

        algorithm = (
            config["detection"]["algorithm"]
            .strip()
            .lower()
        )

        if algorithm == "ultralytics":
            return UltralyticsDetector(
                config
            )

        if algorithm == "rtdetr":
            return RTDETRDetector(
                config
            )

        if algorithm == "faster_rcnn":
            return FasterRCNNDetector(
                config
            )

        raise ValueError(
            f"Unsupported detector: {algorithm}"
        )