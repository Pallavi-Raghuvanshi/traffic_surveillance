# ============================================================================
# base_speed_estimator.py
# ============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Iterable

from core.schemas import BoundingBox


class BaseSpeedEstimator(ABC):
    """
    Abstract interface for all speed estimation algorithms.

    Implementations may estimate speed using:

    - Pixel displacement
    - Homography
    - Optical Flow
    - Sensor fusion
    - Other future techniques

    Every implementation receives a trajectory consisting
    of bounding boxes belonging to a single tracked object
    and returns its estimated speed.
    """

    @abstractmethod
    def estimate(
        self,
        trajectory: Iterable[
            BoundingBox
        ],
    ) -> float:
        """
        Estimate object speed.

        Parameters
        ----------
        trajectory
            Ordered trajectory of a single tracked object.

        Returns
        -------
        float
            Estimated speed.

            PixelSpeedEstimator:
                pixels/second

            HomographySpeedEstimator:
                km/h
        """

        raise NotImplementedError