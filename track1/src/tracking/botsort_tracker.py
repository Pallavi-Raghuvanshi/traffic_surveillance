# ============================================================================
# botsort_tracker.py
# ============================================================================

from __future__ import annotations

import numpy as np

from core.config import Config
from core.schemas import Detection
from core.schemas import Track

from tracking.base_tracker import BaseTracker


class BoTSORTTracker(BaseTracker):
    """
    Wrapper for BoT-SORT.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        tracking_cfg = config["tracking"]["botsort"]

        self.cfg = tracking_cfg

        self._active_tracks: list[Track] = []

        # TODO
        # Initialize BoT-SORT

    @property
    def active_tracks(
        self,
    ) -> list[Track]:

        return self._active_tracks

    def update(
        self,
        detections: list[Detection],
        frame: np.ndarray | None = None,
    ) -> list[Track]:

        # TODO

        return []

    def reset(
        self,
    ) -> None:

        self._active_tracks.clear()