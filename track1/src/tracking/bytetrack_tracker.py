# bytetrack_tracker.py

from __future__ import annotations

import numpy as np
import supervision as sv

from core.config import Config
from core.schemas import BoundingBox
from core.schemas import Detection
from core.schemas import Track

from tracking.base_tracker import BaseTracker


class ByteTrackTracker(BaseTracker):
    """
    Wrapper around Supervision's ByteTrack implementation.

    This class converts our project schemas into ByteTrack inputs
    and converts ByteTrack outputs back into Track objects.
    """

    def __init__(self, config: Config):

        tracking_cfg = config["tracking"]

        self._tracker = sv.ByteTrack(

            track_activation_threshold=
            tracking_cfg["track_activation_threshold"],

            lost_track_buffer=
            tracking_cfg["lost_track_buffer"],

            minimum_matching_threshold=
            tracking_cfg["minimum_matching_threshold"],

            frame_rate=
            tracking_cfg["frame_rate"],
        )

        self._active_tracks: list[Track] = []

    @property
    def active_tracks(self) -> list[Track]:

        return self._active_tracks

    def reset(self) -> None:

        self._tracker.reset()

        self._active_tracks = []

    def update(
        self,
        detections: list[Detection],
        frame: np.ndarray,
    ) -> list[Track]:

        if not detections:

            self._active_tracks = []

            return []

        xyxy = np.array(
            [
                [
                    d.bbox.x1,
                    d.bbox.y1,
                    d.bbox.x2,
                    d.bbox.y2,
                ]
                for d in detections
            ],
            dtype=np.float32,
        )

        confidence = np.array(
            [
                d.confidence
                for d in detections
            ],
            dtype=np.float32,
        )

        class_id = np.array(
            [
                d.class_id
                for d in detections
            ],
            dtype=np.int32,
        )

        sv_detections = sv.Detections(
            xyxy=xyxy,
            confidence=confidence,
            class_id=class_id,
        )

        tracked = self._tracker.update_with_detections(
            sv_detections
        )

        tracks: list[Track] = []

        for i in range(len(tracked)):

            box = BoundingBox(
                x1=float(tracked.xyxy[i][0]),
                y1=float(tracked.xyxy[i][1]),
                x2=float(tracked.xyxy[i][2]),
                y2=float(tracked.xyxy[i][3]),
            )

            track = Track(

                bbox=box,

                confidence=float(
                    tracked.confidence[i]
                ),

                class_id=int(
                    tracked.class_id[i]
                ),

                class_name=str(
                    tracked.data["class_name"][i]
                ),

                track_id=int(
                    tracked.tracker_id[i]
                ),

                frame_index=0,

                is_confirmed=True,

                age=1,

                lost_frames=0,

                history=(box,),
            )

            tracks.append(track)

        self._active_tracks = tracks

        return tracks