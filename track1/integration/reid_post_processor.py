# ============================================================================
# reid_post_processor.py
# ============================================================================

from __future__ import annotations

import numpy as np

from track1.integration.base_post_processor import BasePostProcessor
from track1.integration.reid_manager import ReIDManager
from track1.integration.track1_adapter import Track1Adapter
from track1.integration.schemas import ReIDResult
from track1.src.core.schemas import Track
from dataclasses import dataclass


@dataclass(slots=True)
class GalleryRecord:
    result: ReIDResult
    crop: np.ndarray


class ReIDPostProcessor(BasePostProcessor):
    """
    Post-processing stage that performs Vehicle Re-ID.

    Pipeline
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
        self.results: list[ReIDResult] = []
        self.gallery_records: list[GalleryRecord] = []

    def process(
        self,
        frame: np.ndarray,
        frame_number: int,
        tracks: list[Track],
    ) -> None:

        finished_tracks = self.adapter.process(
            frame=frame,
            frame_number=frame_number,
            tracks=tracks,
        )

        for track_id in finished_tracks:

            crop = self.adapter.get_representative_crop(track_id)

            if crop is None:
                continue

            result = self.reid_manager.process(
                track_id=track_id,
                crop=crop,
                frame_number=frame_number,
            )
            self.gallery_records.append(
                GalleryRecord(
                    result=result,
                    crop=crop.copy(),
                )
            )
            print(result)
            self.results.append(result)

            self.adapter.remove_track(track_id)
