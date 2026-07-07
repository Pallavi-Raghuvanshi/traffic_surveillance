# ============================================================================
# homography_speed_estimator.py
# ============================================================================

from __future__ import annotations

from typing import Iterable

import cv2
import numpy as np

from core.schemas import BoundingBox

from speed.base_speed_estimator import (
    BaseSpeedEstimator,
)


class HomographySpeedEstimator(BaseSpeedEstimator):
    """
    Estimates object speed in km/h using a homography matrix.

    Workflow
    --------
    Bounding Box
        ↓
    Bottom-center
        ↓
    Homography Projection
        ↓
    World Coordinates (meters)
        ↓
    Distance (meters)
        ↓
    Speed (km/h)
    """

    def __init__(
        self,
        homography: np.ndarray,
        fps: float,
    ) -> None:

        if homography.shape != (3, 3):

            raise ValueError(
                "Homography matrix must be 3x3."
            )

        if fps <= 0:

            raise ValueError(
                "FPS must be greater than zero."
            )

        self._H = homography.astype(
            np.float32
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

    def _project(
        self,
        bbox: BoundingBox,
    ) -> np.ndarray:

        point = self._bottom_center(
            bbox
        )

        world = cv2.perspectiveTransform(

            point.reshape(
                1,
                1,
                2,
            ),

            self._H,
        )

        return world.reshape(
            2
        )

    def _distance(
        self,
        first: BoundingBox,
        second: BoundingBox,
    ) -> float:

        p1 = self._project(
            first
        )

        p2 = self._project(
            second
        )

        return float(

            np.linalg.norm(
                p2 - p1
            )
        )

    # ------------------------------------------------------------------ #
    # Estimate
    # ------------------------------------------------------------------ #

    def estimate(
        self,
        trajectory: Iterable[
            BoundingBox
        ],
    ) -> float:

        points = list(
            trajectory
        )

        if len(points) < 2:

            return 0.0

        total_distance = 0.0

        for previous, current in zip(

            points[:-1],

            points[1:],
        ):

            total_distance += self._distance(

                previous,

                current,
            )

        elapsed_time = (

            len(points) - 1

        ) / self._fps

        if elapsed_time <= 0:

            return 0.0

        speed_mps = (
            total_distance
            / elapsed_time
        )

        return speed_mps * 3.6