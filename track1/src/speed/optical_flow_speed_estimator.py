# ============================================================================
# optical_flow_speed_estimator.py
# ============================================================================

from __future__ import annotations

from core.config import Config
from core.schemas import BoundingBox

from speed.base_speed_estimator import BaseSpeedEstimator


class OpticalFlowSpeedEstimator(BaseSpeedEstimator):
    """
    Speed estimation using Optical Flow.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        self.cfg = config["speed"]["optical_flow"]

        # TODO
        # Initialize Optical Flow parameters

    def estimate(
        self,
        trajectory: list[BoundingBox],
    ) -> float:

        # TODO
        # Optical Flow based speed estimation

        return 0.0