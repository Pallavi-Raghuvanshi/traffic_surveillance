# ============================================================================
# hybrid_speed_estimator.py
# ============================================================================

from __future__ import annotations

from typing import Iterable

from core.config import Config
from core.schemas import BoundingBox

from speed.base_speed_estimator import (
    BaseSpeedEstimator,
)


class HybridSpeedEstimator(BaseSpeedEstimator):
    """
    Placeholder implementation for a hybrid speed estimator.

    Future versions may combine:

    - Homography-based estimation
    - Optical Flow
    - Kalman Filtering
    - Trajectory smoothing
    - Sensor fusion

    into a single robust speed estimation pipeline.

    The current implementation intentionally returns zero while
    preserving the project architecture.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        self.cfg = config[
            "speed"
        ][
            "hybrid"
        ]

    # ------------------------------------------------------------------ #
    # Estimate
    # ------------------------------------------------------------------ #

    def estimate(
        self,
        trajectory: Iterable[
            BoundingBox
        ],
    ) -> float:

        _ = list(
            trajectory
        )

        # TODO:
        #
        # 1. Estimate pixel displacement.
        # 2. Estimate optical-flow displacement.
        # 3. Fuse both estimates.
        # 4. Convert to km/h.
        #

        return 0.0