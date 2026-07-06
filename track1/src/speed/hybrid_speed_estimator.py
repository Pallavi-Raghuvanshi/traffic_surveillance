# hybrid_speed_estimator.py

from __future__ import annotations

from core.config import Config
from core.schemas import BoundingBox

from speed.base_speed_estimator import BaseSpeedEstimator


class HybridSpeedEstimator(BaseSpeedEstimator):
    """
    Placeholder implementation for a hybrid speed estimator.

    Future versions may combine homography-based estimation with
    optical flow or other techniques.
    """

    def __init__(self, config: Config) -> None:
        self.config = config["speed"]["hybrid"]

    def estimate(
        self,
        trajectory: list[BoundingBox],
    ) -> float:
        """
        Placeholder implementation.
        """
        return 0.0