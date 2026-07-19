# base_tracker.py
# ============================================================================

from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np

from src.core.schemas import Detection
from src.core.schemas import Track

class BaseTracker(ABC):

    @abstractmethod
    def update(self, detections: list[Detection], frame: np.ndarray | None = None) -> list[Track]:
        """Update tracker using current frame's detections."""

    @abstractmethod
    def reset(self) -> None:
        """Reset the tracker before processing a new video sequence."""
        pass

    @property
    @abstractmethod
    def active_tracks(self) -> list[Track]:
        """Currently active tracks maintained by the tracker."""