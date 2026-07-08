# ============================================================================
# deepsort_tracker.py
# ============================================================================

from __future__ import annotations

import numpy as np

from deep_sort_realtime.deepsort_tracker import (
    DeepSort,
)

from core.config import Config
from core.schemas import BoundingBox
from core.schemas import Detection
from core.schemas import Track

from tracking.base_tracker import BaseTracker


class DeepSORTTracker(BaseTracker):
    """
    Wrapper around DeepSORT.
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

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #

    def update(
        self,
        detections: list[Detection],
        frame: np.ndarray | None = None,
    ) -> list[Track]:

        if not detections:

            self._active_tracks.clear()

            return self._active_tracks

        if frame is None:

            raise ValueError(
                "DeepSORT requires the current frame."
            )

        class_lookup = {

            detection.class_name: detection

            for detection in detections
        }

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

        tracked_objects = (
            self._tracker.update_tracks(
                ds_detections,
                frame=frame,
            )
        )

        tracks: list[
            Track
        ] = []

        for tracked in tracked_objects:

            if not tracked.is_confirmed():

                continue

            if tracked.time_since_update > 0:

                continue

            x1, y1, x2, y2 = (
                tracked.to_ltrb()
            )

            class_name = getattr(

                tracked,

                "det_class",

                "unknown",
            )

            detection = class_lookup.get(
                class_name
            )

            class_id = (

                detection.class_id

                if detection is not None

                else -1
            )

            confidence = (

                detection.confidence

                if detection is not None

                else 1.0
            )

            tracks.append(

                Track(

                    track_id=int(
                        tracked.track_id
                    ),

                    bbox=BoundingBox(

                        x1=float(x1),

                        y1=float(y1),

                        x2=float(x2),

                        y2=float(y2),
                    ),

                    confidence=float(
                        confidence
                    ),

                    class_id=int(
                        class_id
                    ),

                    class_name=class_name,
                )
            )

        self._active_tracks = tracks

        return self._active_tracks

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #

    def reset(
        self,
    ) -> None:

        self._tracker.delete_all_tracks()

        self._active_tracks.clear()