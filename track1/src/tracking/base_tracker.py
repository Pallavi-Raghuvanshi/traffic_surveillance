# ============================================================================
# base_tracker.py
# ============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import numpy as np

from core.schemas import Detection
from core.schemas import Track


class BaseTracker(ABC):
    """
    Abstract interface for all multi-object trackers.

    Every tracker implementation must convert detector outputs
    into standardized Track objects.

    Examples
    --------
    - ByteTrack
    - DeepSORT
    - BoT-SORT
    - OC-SORT
    """

    # ------------------------------------------------------------------ #
    # Tracking
    # ------------------------------------------------------------------ #

    @abstractmethod
    def update(
        self,
        detections: list[Detection],
        frame: np.ndarray | None = None,
    ) -> list[Track]:
        """
        Update the tracker using detections from the current frame.

        Parameters
        ----------
        detections
            Detector output for the current frame.

        frame
            Current video frame. Some trackers
            (e.g. DeepSORT, BoT-SORT) require image
            information for appearance features.

        Returns
        -------
        list[Track]
            Active tracks after the update.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------ #
    # State Management
    # ------------------------------------------------------------------ #

    @abstractmethod
    def reset(
        self,
    ) -> None:
        """
        Reset the tracker before processing
        a new video sequence.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    @abstractmethod
    def active_tracks(
        self,
    ) -> list[Track]:
        """
        Currently active tracks maintained
        by the tracker.
        """

        raise NotImplementedError