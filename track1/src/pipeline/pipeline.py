# ============================================================================
# pipeline.py
# ============================================================================

from __future__ import annotations

import time

from core.logger import get_logger

logger = get_logger(__name__)


class Pipeline:
    """
    Main processing pipeline.

    Coordinates every module of Track 1.

    Workflow
    --------

    Video

        ↓

    Detection

        ↓

    Tracking

        ↓

    Trajectory

        ↓

    Speed Estimation

        ↓

    Evaluation

        ↓

    Visualization
    """

    def __init__(
        self,
        video_loader,
        detector,
        tracker,
        trajectory_manager,
        speed_estimator,
        evaluator,
    ) -> None:

        self.video_loader = video_loader

        self.detector = detector

        self.tracker = tracker

        self.trajectory_manager = trajectory_manager

        self.speed_estimator = speed_estimator

        self.evaluator = evaluator

    def run(self) -> None:
        """
        Execute complete Track 1 pipeline.
        """

        logger.info(
            "Starting Track 1 pipeline..."
        )

        for frame_number, frame in self.video_loader:

            start = time.perf_counter()

            detections = self.detector.detect(
                frame
            )

            tracks = self.tracker.update(
                detections,
                frame,
            )

            self.trajectory_manager.update(
                tracks
            )

            speeds = []

            for track in tracks:

                trajectory = (
                    self.trajectory_manager.get(
                        track.track_id
                    )
                )

                speed = (
                    self.speed_estimator
                    .estimate(
                        trajectory
                    )
                )

                speeds.append(
                    speed
                )

            elapsed = (
                time.perf_counter()
                - start
            )

            self.evaluator.update(
                len(detections),
                elapsed,
                speeds,
            )

        logger.info(
            "Pipeline finished."
        )

        self.evaluator.print_summary()