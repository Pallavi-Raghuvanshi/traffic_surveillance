# bytetrack_tracker.py
# ============================================================================

from __future__ import annotations
import numpy as np
import supervision as sv

from core.config import Config
from core.schemas import BoundingBox, Detection, Track

from tracking.base_tracker import BaseTracker

class ByteTrackTracker(BaseTracker):

    def __init__(self, config: Config) -> None:

        tracking_cfg = (config["tracking"]["bytetrack"])
        self.cfg = tracking_cfg
        self._active_tracks = []

        self._tracker = sv.ByteTrack(
            track_activation_threshold=tracking_cfg["track_activation_threshold"],
            lost_track_buffer=tracking_cfg["lost_track_buffer"],
            minimum_matching_threshold=tracking_cfg["minimum_matching_threshold"],
            frame_rate=tracking_cfg["frame_rate"]
        )

    @property
    def active_tracks(self) -> list[Track]:
        return self._active_tracks

    def update(self, detections: list[Detection], frame: np.ndarray | None = None) -> list[Track]:

        if not detections:
            self._active_tracks.clear()
            return self._active_tracks

        class_lookup = {detection.class_id: detection.class_name for detection in detections}

        sv_detections = sv.Detections(
            xyxy=np.asarray(
                [

                    [
                        detection.bbox.x1,
                        detection.bbox.y1,
                        detection.bbox.x2,
                        detection.bbox.y2,
                    ] for detection in detections
                ], dtype=np.float32),

            confidence=np.asarray(
                [detection.confidence for detection in detections],
                dtype=np.float32,
            ),

            class_id=np.asarray(
                [detection.class_id for detection in detections],
                dtype=np.int32,
            ),
        )

        tracked = self._tracker.update_with_detections(sv_detections)
        tracks = []
        tracker_ids = tracked.tracker_id

        if tracker_ids is None:
            self._active_tracks = tracks
            return tracks

        for (
            xyxy,
            confidence,
            class_id,
            tracker_id,
        ) in zip(
            tracked.xyxy,
            tracked.confidence,
            tracked.class_id,
            tracker_ids,
        ):

            if tracker_id is None:
                continue

            tracks.append(
                Track(
                    track_id=int(tracker_id),
                    bbox=BoundingBox(
                        x1=float(xyxy[0]),
                        y1=float(xyxy[1]),
                        x2=float(xyxy[2]),
                        y2=float(xyxy[3]),
                    ),
                    confidence=float(confidence),
                    class_id=int(class_id),
                    class_name=class_lookup.get(int(class_id), str(class_id)),
                )
            )
        self._active_tracks = tracks
        return self._active_tracks

    def reset(self) -> None:
        self._tracker.reset()
        self._active_tracks.clear()
        