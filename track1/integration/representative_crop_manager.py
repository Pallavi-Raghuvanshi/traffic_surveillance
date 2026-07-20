from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from src.core.schemas import Track


@dataclass
class CropRecord:
    track_id: int
    crop: np.ndarray
    score: float
    last_seen_frame: int


class RepresentativeCropManager:

    def __init__(self):

        self.records: dict[int, CropRecord] = {}

    @staticmethod
    def score(crop: np.ndarray) -> float:
        """
        Larger crops usually contain more discriminative details.
        """

        h, w = crop.shape[:2]
        return float(h * w)

    def update(
        self,
        frame: np.ndarray,
        frame_number: int,
        tracks: list[Track],
    ):

        frame_h, frame_w = frame.shape[:2]

        for track in tracks:

            bbox = track.bbox

            x1 = max(0, int(bbox.x1))
            y1 = max(0, int(bbox.y1))
            x2 = min(frame_w, int(bbox.x2))
            y2 = min(frame_h, int(bbox.y2))

            if x2 <= x1 or y2 <= y1:
                continue

            crop = frame[y1:y2, x1:x2].copy()

            score = self.score(crop)

            record = self.records.get(track.track_id)

            if record is None or score > record.score:

                self.records[track.track_id] = CropRecord(
                    track_id=track.track_id,
                    crop=crop,
                    score=score,
                    last_seen_frame=frame_number,
                )

            else:
                record.last_seen_frame = frame_number