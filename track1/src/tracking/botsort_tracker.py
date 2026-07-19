# botsort_tracker.py
# ============================================================================

from __future__ import annotations
import numpy as np

from ultralytics.trackers.bot_sort import BOTSORT

# Standardized Project Models
from core.config import Config
from core.schemas import BoundingBox, Detection, Track

from tracking.base_tracker import BaseTracker
# from tracking.botsort.config import build_botsort_args
from tracking.ultralytics_results_adapter import TrackingResults

class BoTSORTTracker(BaseTracker):

    def __init__(self, config: Config) -> None:
        self.cfg = config["tracking"]["botsort"]
        args = build_botsort_args(config)
        self._tracker = BOTSORT(args)
        self._active_tracks: list[Track] = []

    @property
    def active_tracks(self) -> list[Track]:
        return self._active_tracks
    
    def update(self, detections: list[Detection], frame: np.ndarray | None = None) -> list[Track]:

        if frame is None:
            raise ValueError("BoTSORT requires the current frame.")

        results = TrackingResults.from_detections(detections)
        tracked = self._tracker.update(results, img=frame) # BoTSORT returns NumPy array

        if len(tracked) == 0:
            self._active_tracks = []
            return self._active_tracks

        tracks = []

        for row in tracked:

            x1 = float(row[0])
            y1 = float(row[1])
            x2 = float(row[2])
            y2 = float(row[3])

            track_id = int(row[4])
            score = float(row[5])
            class_id = int(row[6])
            class_name = str(class_id)

            for detection in detections:
                if detection.class_id == class_id:
                    class_name = detection.class_name
                    break

            tracks.append(
                Track(
                    track_id=track_id,
                    class_id=class_id,
                    class_name=class_name,
                    confidence=score,
                    bbox=BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2)
                )
            )

        self._active_tracks = tracks
        return self._active_tracks

    def reset(self) -> None:
        self._tracker.reset()
        self._active_tracks.clear()