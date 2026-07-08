# ============================================================================
# ultralytics_results_adapter.py
# ============================================================================
#
# Converts the project's Detection objects into the minimal Results-like
# object expected by the official Ultralytics BYTETracker / BoTSORT.
# ============================================================================

from __future__ import annotations

import numpy as np


class TrackingResults:
    """
    Minimal Results object compatible with Ultralytics trackers.

    Required attributes
    -------------------
    xyxy
    conf
    cls

    Required behaviour
    ------------------
    Boolean indexing

        results[mask]

    Integer indexing

        results[index]
    """

    def __init__(
        self,
        xyxy: np.ndarray,
        conf: np.ndarray,
        cls: np.ndarray,
    ) -> None:

        self.xyxy = np.asarray(
            xyxy,
            dtype=np.float32,
        )

        self.conf = np.asarray(
            conf,
            dtype=np.float32,
        )

        self.cls = np.asarray(
            cls,
            dtype=np.float32,
        )

    # ------------------------------------------------------------------ #
    # Ultralytics Tracker Requirements
    # ------------------------------------------------------------------ #

    @property
    def xywh(
        self,
    ) -> np.ndarray:
        """
        Bounding boxes in (center x, center y, width, height) format.

        Required by ``ultralytics.trackers.utils.stracks.parse_bboxes``,
        which every Ultralytics tracker (BYTETracker, BOTSORT) uses to
        initialize tracks.
        """

        if len(self.xyxy) == 0:

            return np.empty(
                (0, 4),
                dtype=np.float32,
            )

        x1 = self.xyxy[:, 0]
        y1 = self.xyxy[:, 1]
        x2 = self.xyxy[:, 2]
        y2 = self.xyxy[:, 3]

        width = x2 - x1
        height = y2 - y1

        return np.stack(

            [

                x1 + width / 2,

                y1 + height / 2,

                width,

                height,

            ],

            axis=-1,

        ).astype(np.float32)

    # ------------------------------------------------------------------ #
    # Container Protocol
    # ------------------------------------------------------------------ #

    def __len__(
        self,
    ) -> int:

        return len(
            self.conf
        )

    def __getitem__(
        self,
        index,
    ) -> "TrackingResults":

        return TrackingResults(

            xyxy=self.xyxy[index],

            conf=self.conf[index],

            cls=self.cls[index],
        )

    # ------------------------------------------------------------------ #
    # Factory
    # ------------------------------------------------------------------ #

    @classmethod
    def from_detections(
        cls,
        detections,
    ) -> "TrackingResults":

        if not detections:

            return cls(

                xyxy=np.empty(
                    (0, 4),
                    dtype=np.float32,
                ),

                conf=np.empty(
                    0,
                    dtype=np.float32,
                ),

                cls=np.empty(
                    0,
                    dtype=np.float32,
                ),
            )

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

            dtype=np.float32,
        )

        return cls(

            xyxy=xyxy,

            conf=confidence,

            cls=class_id,
        )