# ============================================================================
# botsort_tracker.py
# ============================================================================

from __future__ import annotations

import numpy as np
import supervision as sv

from core.config import Config
from core.schemas import Detection
from core.schemas import Track

from tracking.base_tracker import BaseTracker


class BoTSORTTracker(BaseTracker):
    """
    Wrapper for BoT-SORT.

    NOTE:
    Current Supervision releases expose ByteTrack but do not expose a native
    BoT-SORT tracker API. This wrapper therefore uses the same interface and
    can be switched to a true BoT-SORT implementation later without changing
    the rest of the project.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        tracking_cfg = (
            config["tracking"]["botsort"]
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

            self._active_tracks = []

            return self._active_tracks

        xyxy = np.asarray(

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
        )

        confidence = np.asarray(

            [

                detection.confidence

                for detection in detections

            ],

            dtype=np.float32,
        )

        class_id = np.asarray(

            [

                detection.class_id

                for detection in detections

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

        tracks: list[
            Track
        ] = []

        for i in range(
            len(tracked.xyxy)
        ):

            tracker_id = (
                tracked.tracker_id[i]
            )

            if tracker_id is None:

                continue

            x1, y1, x2, y2 = (
                tracked.xyxy[i]
            )

            tracks.append(

                Track(

                    track_id=int(
                        tracker_id
                    ),

                    class_id=int(
                        tracked.class_id[i]
                    ),

                    class_name=(
                        detections[i]
                        .class_name
                    ),

                    confidence=float(
                        tracked.confidence[i]
                    ),

                    bbox=detections[i].bbox.__class__(

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