# ============================================================================
# botsort_tracker.py
# ============================================================================

from __future__ import annotations

from types import SimpleNamespace

import numpy as np

from ultralytics.trackers.bot_sort import (
    BOTSORT,
)

from core.config import Config
from core.schemas import BoundingBox
from core.schemas import Detection
from core.schemas import Track

from tracking.base_tracker import BaseTracker
from tracking.ultralytics_results_adapter import (
    TrackingResults,
)


class BoTSORTTracker(BaseTracker):
    """
    Wrapper around the official Ultralytics BoT-SORT implementation.
    """

    def __init__(
        self,
        config: Config,
    ) -> None:

        tracking_cfg = config[
            "tracking"
        ][
            "botsort"
        ]

        self.cfg = tracking_cfg

        args = SimpleNamespace(

            # ----------------------------------------------------------
            # Detection thresholds
            # ----------------------------------------------------------

            track_high_thresh=tracking_cfg[
                "track_high_thresh"
            ],

            track_low_thresh=tracking_cfg[
                "track_low_thresh"
            ],

            new_track_thresh=tracking_cfg[
                "new_track_thresh"
            ],

            # ----------------------------------------------------------
            # Association
            # ----------------------------------------------------------

            match_thresh=tracking_cfg[
                "match_thresh"
            ],

            track_buffer=tracking_cfg[
                "track_buffer"
            ],

            fuse_score=tracking_cfg[
                "fuse_score"
            ],

            # ----------------------------------------------------------
            # BoT-SORT
            # ----------------------------------------------------------

            proximity_thresh=tracking_cfg[
                "proximity_thresh"
            ],

            appearance_thresh=tracking_cfg[
                "appearance_thresh"
            ],

            with_reid=tracking_cfg[
                "with_reid"
            ],

            gmc_method=tracking_cfg[
                "gmc_method"
            ],

            model=tracking_cfg[
                "model"
            ],

            # ----------------------------------------------------------
            # Optional
            # ----------------------------------------------------------

            device=None,
        )

        self._tracker = BOTSORT(
            args
        )

        self._active_tracks: list[
            Track
        ] = []

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

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

        if frame is None:

            raise ValueError(
                "BoTSORT requires the current frame."
            )

        results = (
            TrackingResults.from_detections(
                detections
            )
        )

        tracked = self._tracker.update(

            results,

            img=frame,
        )

        if len(tracked) == 0:

            self._active_tracks = []

            return self._active_tracks

        tracks: list[
            Track
        ] = []

        for row in tracked:

            x1 = float(row[0])
            y1 = float(row[1])
            x2 = float(row[2])
            y2 = float(row[3])

            track_id = int(
                row[4]
            )

            score = float(
                row[5]
            )

            class_id = int(
                row[6]
            )

            class_name = str(
                class_id
            )

            for detection in detections:

                if (

                    detection.class_id

                    == class_id

                ):

                    class_name = (
                        detection.class_name
                    )

                    break

            tracks.append(

                Track(

                    track_id=track_id,

                    class_id=class_id,

                    class_name=class_name,

                    confidence=score,

                    bbox=BoundingBox(

                        x1=x1,

                        y1=y1,

                        x2=x2,

                        y2=y2,
                    ),
                )
            )

        self._active_tracks = (
            tracks
        )

        return self._active_tracks