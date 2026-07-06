# ============================================================================
# speed_estimator_factory.py
# ============================================================================

from __future__ import annotations

from core.config import Config

from speed.base_speed_estimator import BaseSpeedEstimator
from speed.speed_estimator import SpeedEstimator

from calibration.homography import Homography


class SpeedEstimatorFactory:
    """
    Factory responsible for creating speed estimation algorithms.
    """

    @staticmethod
    def create(
        config: Config,
        fps: float,
    ) -> BaseSpeedEstimator:

        algorithm = (
            config["speed"]["algorithm"]
            .strip()
            .lower()
        )

        if algorithm == "homography":

            homography = Homography.load(
                config["paths"]["homography"]
            )

            return SpeedEstimator(
                homography=homography.matrix,
                fps=fps,
            )

        raise ValueError(
            f"Unsupported speed estimator: '{algorithm}'"
        )