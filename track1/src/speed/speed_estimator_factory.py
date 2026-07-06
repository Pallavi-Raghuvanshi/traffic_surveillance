# ============================================================================
# speed_estimator_factory.py
# ============================================================================

from __future__ import annotations

from calibration.homography import Homography

from core.config import Config

from speed.base_speed_estimator import BaseSpeedEstimator

from speed.homography_speed_estimator import (
    HomographySpeedEstimator,
)

from speed.optical_flow_speed_estimator import (
    OpticalFlowSpeedEstimator,
)

from speed.hybrid_speed_estimator import (
    HybridSpeedEstimator,
)


class SpeedEstimatorFactory:

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

            return HomographySpeedEstimator(
                homography=homography.matrix,
                fps=fps,
            )

        if algorithm == "optical_flow":

            return OpticalFlowSpeedEstimator(
                config
            )

        if algorithm == "hybrid":

            return HybridSpeedEstimator(
                config
            )

        raise ValueError(
            f"Unsupported speed estimator: {algorithm}"
        )