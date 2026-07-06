# ============================================================================
# base_speed_estimator.py
# ============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from core.schemas import BoundingBox


class BaseSpeedEstimator(ABC):
    """
    Abstract interface for all speed estimation algorithms.
    """

    @abstractmethod
    def estimate(
        self,
        trajectory: list[BoundingBox],
    ) -> float:
        """
        Estimate vehicle speed (km/h).
        """
        raise NotImplementedError