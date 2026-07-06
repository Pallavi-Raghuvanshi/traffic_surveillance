# ============================================================================
# pixel_speed_estimator.py
# ============================================================================

from __future__ import annotations

from typing import Iterable

import numpy as np

from core.schemas import BoundingBox
from speed.base_speed_estimator import BaseSpeedEstimator


class PixelSpeedEstimator(BaseSpeedEstimator):
    """
    Estimates vehicle speed in pixels/second.

    This estimator is primarily intended for development and
    debugging before camera calibration is available.
    """

    def __init__(
        self,
        fps: float,
    ) -> None:

        self._fps = fps

    @staticmethod
    def bottom_center(
        bbox: BoundingBox,
    ) -> np.ndarray:

        x = (bbox.x1 + bbox.x2) / 2.0
        y = bbox.y2

        return np.array(
            [x, y],
            dtype=np.float32,
        )

    def estimate(
        self,
        trajectory: Iterable[BoundingBox],
    ) -> float:

        trajectory = list(trajectory)

        if len(trajectory) < 2:
            return 0.0

        distance = 0.0

        for previous, current in zip(
            trajectory[:-1],
            trajectory[1:],
        ):

            p1 = self.bottom_center(previous)
            p2 = self.bottom_center(current)

            distance += np.linalg.norm(
                p2 - p1
            )

        duration = (
            len(trajectory) - 1
        ) / self._fps

        if duration <= 0:
            return 0.0

        return distance / duration