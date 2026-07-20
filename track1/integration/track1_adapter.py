from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from integration.representative_crop_manager import RepresentativeCropManager
from src.core.schemas import Track
from integration.base_post_processor import BasePostProcessor


@dataclass(slots=True)
class TrackState:
    """Runtime state maintained for each active track."""

    missing_frames: int = 0


class Track1Adapter(BasePostProcessor):
    """
    Bridges Track 1 with downstream modules (Track 2, Track 3, etc.).

    Responsibilities
    ----------------
    1. Update representative crops.
    2. Track active/missing vehicle IDs.
    3. Return track IDs that have permanently disappeared.

    This class deliberately does NOT perform Re-ID.
    """

    def __init__(
        self,
        lost_threshold: int = 5,
    ) -> None:

        self.crop_manager = RepresentativeCropManager()

        self.lost_threshold = lost_threshold

        self.track_states: dict[int, TrackState] = {}

    def process(
        self,
        frame: np.ndarray,
        frame_number: int,
        tracks: list[Track],
    ) -> list[int]:
        """
        Process one video frame.

        Parameters
        ----------
        frame
            Original video frame.
        frame_number
            Current frame number.
        tracks
            Active tracks returned by Track 1.

        Returns
        -------
        list[int]
            Track IDs that are considered finished.
        """

        # Update representative crops
        self.crop_manager.update(
            frame=frame,
            frame_number=frame_number,
            tracks=tracks,
        )

        current_ids = {track.track_id for track in tracks}

        # Reset missing counter for visible tracks
        for track_id in current_ids:

            state = self.track_states.setdefault(
                track_id,
                TrackState(),
            )

            state.missing_frames = 0

        finished_tracks: list[int] = []

        # Check tracks that disappeared
        for track_id in list(self.track_states.keys()):

            if track_id in current_ids:
                continue

            state = self.track_states[track_id]

            state.missing_frames += 1

            if state.missing_frames >= self.lost_threshold:

                finished_tracks.append(track_id)
                if state.missing_frames >= self.lost_threshold:

                    print(f"Finished track {track_id} at frame {frame_number}")

                    finished_tracks.append(track_id)
                    del self.track_states[track_id]

        return finished_tracks

    def get_representative_crop(
        self,
        track_id: int,
    ) -> np.ndarray | None:
        """
        Return the representative crop for a finished track.
        """

        record = self.crop_manager.records.get(track_id)

        if record is None:
            return None

        return record.crop

    def remove_track(
        self,
        track_id: int,
    ) -> None:
        """
        Remove cached data after downstream processing completes.
        """

        self.crop_manager.records.pop(track_id, None)