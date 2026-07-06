# ============================================================================
# base_tracker.py
# ============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
import numpy as np

from core.schemas import Detection, Track


class BaseTracker(ABC):
    """
    Abstract interface for all multi-object trackers.

    Every tracker implementation must inherit from this class.

    Examples
    --------
    ByteTrack

    DeepSORT

    BoT-SORT

    OC-SORT
    """

    @abstractmethod
    def update(
        self,
        detections: list[Detection],
        frame: np.ndarray | None = None,
    ) -> list[Track]:
        """
        Update tracker using current detections.

        Parameters
        ----------
        detections: list[Detection]
            Vehicle detections from detector.

        frame: np.ndarray
            Current video frame.

        Returns
        -------
        list[Track]

            Active tracked vehicles.
        """

        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """
        Reset tracker state.
        Useful when processing another video.
        """

        raise NotImplementedError

    @property
    @abstractmethod
    def active_tracks(
        self,
    ) -> list[Track]:
        """
        Return all currently active tracks.
        """

        raise NotImplementedError