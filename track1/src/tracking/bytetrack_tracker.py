# ============================================================================
# bytetrack_tracker.py
# ============================================================================

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
    Wrapper for Supervision ByteTrack.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        tracking_cfg = (
            config["tracking"]["bytetrack"]
        )

        self.cfg = tracking_cfg

        self._tracker = sv.ByteTrack(

            track_activation_threshold=tracking_cfg[
                "track_activation_threshold"
            ],

            lost_track_buffer=tracking_cfg[
                "lost_track_buffer"
            ],

            minimum_matching_threshold=tracking_cfg[
                "minimum_matching_threshold"
            ],

            frame_rate=tracking_cfg[
                "frame_rate"
            ],
        )

        self._active_tracks: list[
            Track
        ] = []

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

        if not detections:

            self._active_tracks.clear()

            return self._active_tracks

        sv_detections = sv.Detections(

            xyxy=np.asarray(

                [

                    [

                        detection.bbox.x1,
                        detection.bbox.y1,
                        detection.bbox.x2,
                        detection.bbox.y2,
                    ]

                    for detection in detections

                ],

                dtype=np.float32,
            ),

            confidence=np.asarray(

                [

                    detection.confidence

                    for detection in detections

                ],

                dtype=np.float32,
            ),

            class_id=np.asarray(

                [

                    detection.class_id

                    for detection in detections

                ],

                dtype=np.int32,
            ),
        )

        tracked = self._tracker.update_with_detections(
            sv_detections
        )

        tracks: list[
            Track
        ] = []

        for xyxy, confidence, class_id, tracker_id in zip(

            tracked.xyxy,

            tracked.confidence,

            tracked.class_id,

            tracked.tracker_id,
        ):

            if tracker_id is None:

                continue

            x1, y1, x2, y2 = xyxy

            tracks.append(

                Track(

                    track_id=int(
                        tracker_id
                    ),

                    class_id=int(
                        class_id
                    ),

                    class_name=str(
                        class_id
                    ),

                    confidence=float(
                        confidence
                    ),

                    bbox=BoundingBox(

                        x1=float(x1),

                        y1=float(y1),

                        x2=float(x2),

                        y2=float(y2),
                    ),
                )
            )

        self._active_tracks = tracks

        return self._active_tracks

    def reset(
        self,
    ) -> None:

        self._tracker.reset()

        self._active_tracks.clear()