# ============================================================================
# speed_estimator.py
# ============================================================================
# converts pixel movement into real-world speed

from __future__ import annotations

from typing import Iterable

import cv2
import numpy as np

from core.schemas import BoundingBox
from speed.base_speed_estimator import BaseSpeedEstimator


class SpeedEstimator(BaseSpeedEstimator):
    """
    Estimates vehicle speed using Homography transformation.

    Workflow
    --------
    Bounding Box
            ↓
    Bottom-center point
            ↓
    Homography Projection
            ↓
    World Coordinates (meters)
            ↓
    Distance
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

        self._H = homography.astype(np.float32)
        self._fps = fps

    @staticmethod
    def bottom_center(
        bbox: BoundingBox,
    ) -> np.ndarray:
        """
        Returns bottom-center of a bounding box. Approximate point where vehicle touches the ground.
        """

        x = (bbox.x1 + bbox.x2) / 2.0
        y = bbox.y2

        return np.array(
            [[x, y]],
            dtype=np.float32,
        )

    def project(
        self,
        bbox: BoundingBox,
    ) -> np.ndarray:
        """
        Project pixel coordinates to ground plane.
        """

        point = self.bottom_center(
            bbox,
        )

        world = cv2.perspectiveTransform(
            point.reshape(-1, 1, 2),
            self._H,
        )

        return world.reshape(2)

    def distance(
        self,
        box1: BoundingBox,
        box2: BoundingBox,
    ) -> float:
        """
        Real-world distance (meters).
        """

        p1 = self.project(box1)
        p2 = self.project(box2)

        return float(
            np.linalg.norm(
                p2 - p1
            )
        )

    def estimate(
        self,
        trajectory: Iterable[BoundingBox],
    ) -> float:
        """
        Estimate average speed from trajectory.

        Returns
        -------
        Speed in km/h.
        """

        trajectory = list(trajectory)

        if len(trajectory) < 2:
            return 0.0

        distance = 0.0

        for previous, current in zip(
            trajectory[:-1],
            trajectory[1:],
        ):

            distance += self.distance(
                previous,
                current,
            )

        time_seconds = (
            len(trajectory) - 1
        ) / self._fps

        if time_seconds <= 0:
            return 0.0

        speed_mps = (
            distance / time_seconds
        )

        return speed_mps * 3.6