# ============================================================================
# deepsort_tracker.py
# ============================================================================

from __future__ import annotations

import numpy as np

from deep_sort_realtime.deepsort_tracker import (
    DeepSort,
)

from core.config import Config
from core.schemas import Detection
from core.schemas import Track

from tracking.base_tracker import BaseTracker


class DeepSORTTracker(BaseTracker):
    """
    Wrapper for DeepSORT.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        tracking_cfg = (
            config["tracking"]["deepsort"]
        )

        self.cfg = tracking_cfg

        self._tracker = DeepSort(

            max_age=tracking_cfg[
                "max_age"
            ],

            n_init=tracking_cfg[
                "n_init"
            ],

            max_iou_distance=tracking_cfg[
                "max_iou_distance"
            ],

            max_cosine_distance=tracking_cfg[
                "max_cosine_distance"
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

        if frame is None:

            raise ValueError(
                "DeepSORT requires the current frame."
            )

        ds_detections = []

        for detection in detections:

            bbox = detection.bbox

            ds_detections.append(

                (

                    [

                        bbox.x1,
                        bbox.y1,
                        bbox.x2 - bbox.x1,
                        bbox.y2 - bbox.y1,
                    ],

                    detection.confidence,

                    detection.class_name,
                )
            )

        tracked = self._tracker.update_tracks(

            ds_detections,

            frame=frame,
        )

        tracks: list[Track] = []

        for track in tracked:

            if not track.is_confirmed():

                continue

            ltrb = track.to_ltrb()

            class_name = getattr(
                track,
                "det_class",
                "vehicle",
            )

            class_id = 0

            for detection in detections:

                if (
                    detection.class_name
                    == class_name
                ):

                    class_id = (
                        detection.class_id
                    )

                    break

            tracks.append(

                Track(

                    track_id=int(
                        track.track_id
                    ),

                    class_id=class_id,

                    class_name=class_name,

                    confidence=1.0,

                    bbox=detections[0].bbox.__class__(

                        x1=float(ltrb[0]),
                        y1=float(ltrb[1]),
                        x2=float(ltrb[2]),
                        y2=float(ltrb[3]),
                    ),
                )
            )

        self._active_tracks = tracks

        return self._active_tracks

    def reset(
        self,
    ) -> None:

        self._tracker.delete_all_tracks()

        self._active_tracks.clear()