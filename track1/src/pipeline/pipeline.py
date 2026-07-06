# ============================================================================
# pipeline.py
# ============================================================================

from __future__ import annotations

import time

from core.logger import get_logger

logger = get_logger(__name__)


class Pipeline:
    """
    Executes the complete Track 1 processing pipeline.

    Workflow
    --------
    Video
        ↓
    Detection
        ↓
    Tracking
        ↓
    Trajectory Update
        ↓
    Speed Estimation
        ↓
    Visualization
        ↓
    Evaluation
    """

    def __init__(
        self,
        video_loader,
        detector,
        tracker,
        trajectory_manager,
        speed_estimator,
        evaluator,
        visualizer,
    ) -> None:

        self.video_loader = video_loader
        self.detector = detector
        self.tracker = tracker
        self.trajectory_manager = trajectory_manager
        self.speed_estimator = speed_estimator
        self.evaluator = evaluator
        self.visualizer = visualizer

    def run(
        self,
    ) -> None:

        logger.info("Pipeline started.")

        for frame_number, frame in self.video_loader:

            start = time.perf_counter()

            # ---------------------------------------------------------
            # Detection
            # ---------------------------------------------------------

            detections = self.detector.detect(
                frame
            )

            # ---------------------------------------------------------
            # Tracking
            # ---------------------------------------------------------

            tracks = self.tracker.update(
                detections,
                frame,
            )

            # ---------------------------------------------------------
            # Trajectory Management
            # ---------------------------------------------------------

            self.trajectory_manager.update(
                tracks
            )

            # ---------------------------------------------------------
            # Speed Estimation
            # ---------------------------------------------------------

            speeds: list[float] = []
            speed_map: dict[int, float] = {}

            for track in tracks:

                trajectory = (
                    self.trajectory_manager.get(
                        track.track_id
                    )
                )

                speed = (
                    self.speed_estimator.estimate(
                        trajectory
                    )
                )

                speeds.append(speed)

                speed_map[
                    track.track_id
                ] = speed

            # ---------------------------------------------------------
            # Visualization
            # ---------------------------------------------------------

            frame = self.visualizer.draw_tracks(
                frame,
                tracks,
                speed_map,
            )

            # ---------------------------------------------------------
            # Evaluation
            # ---------------------------------------------------------

            elapsed = (
                time.perf_counter()
                - start
            )

            self.evaluator.update(
                num_detections=len(
                    detections
                ),
                processing_time=elapsed,
                speeds=speeds,
            )

        logger.info("Pipeline finished.")

        self.evaluator.print_summary()