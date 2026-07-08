# ============================================================================
# pixel_speed_estimator.py
# ============================================================================

from __future__ import annotations

from typing import Iterable

import numpy as np

from core.schemas import BoundingBox

from speed.base_speed_estimator import (
    BaseSpeedEstimator,
)


class PixelSpeedEstimator(BaseSpeedEstimator):
    """
    Estimates object speed in pixels per second.

    The estimator measures the displacement of the
    bottom-center point of the bounding box across
    consecutive frames.

    This implementation is intended for debugging and
    development until camera calibration is available.
    """

    def __init__(
        self,
        fps: float,
    ) -> None:

        if fps <= 0:

            raise ValueError(
                "FPS must be greater than zero."
            )

        self._fps = fps

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _bottom_center(
        bbox: BoundingBox,
    ) -> np.ndarray:

        return np.asarray(

            (

                (bbox.x1 + bbox.x2) / 2.0,

                bbox.y2,
            ),

            dtype=np.float32,
        )

    # ------------------------------------------------------------------ #
    # Estimate
    # ------------------------------------------------------------------ #

    def estimate(
        self,
        trajectory: Iterable[BoundingBox],
    ) -> float:

        points = list(
            trajectory
        )

        if len(points) < 2:

            return 0.0

        total_distance = 0.0

        previous = self._bottom_center(
            points[0]
        )

        for bbox in points[1:]:

            current = self._bottom_center(
                bbox
            )

            total_distance += float(

                np.linalg.norm(
                    current - previous
                )
            )

            previous = current

        elapsed_time = (

            len(points) - 1

        ) / self._fps

        if elapsed_time <= 0:

            return 0.0

        return total_distance / elapsed_time