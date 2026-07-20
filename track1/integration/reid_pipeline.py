# ============================================================================
# reid_pipeline.py
# ============================================================================

from __future__ import annotations

import numpy as np

from integration.reid_manager import ReIDManager
from integration.track1_adapter import Track1Adapter
from integration.schemas import ReIDResult
from src.core.schemas import Track


class ReIDPipeline:
    """
    Connects Track 1 outputs to the Vehicle Re-ID pipeline.

    Track1
        ↓
    Track1Adapter
        ↓
    ReIDManager
    """

    def __init__(
        self,
        adapter: Track1Adapter,
        reid_manager: ReIDManager,
    ) -> None:

        self.adapter = adapter
        self.reid_manager = reid_manager

    def process(
        self,
        frame: np.ndarray,
        frame_number: int,
        tracks: list[Track],
    ) -> list[ReIDResult]:
        """
        Process one video frame.

        Returns
        -------
        list[ReIDResult]
            Re-ID results for tracks that finished during this frame.
        """

        finished_tracks = self.adapter.process(
            frame=frame,
            frame_number=frame_number,
            tracks=tracks,
        )

        results: list[ReIDResult] = []

        for track_id in finished_tracks:

            crop = self.adapter.get_representative_crop(track_id)

            if crop is None:
                continue

            result = self.reid_manager.process(
                track_id=track_id,
                crop=crop,
            )

            results.append(result)

            self.adapter.remove_track(track_id)

        return results
