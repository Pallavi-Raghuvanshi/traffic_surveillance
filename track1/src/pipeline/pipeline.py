# ============================================================================
# pipeline.py
# ============================================================================

from __future__ import annotations

import time

from core.logger import get_logger

from evaluation.benchmark_summary import (
    BenchmarkSummary,
)

from evaluation.evaluator import Evaluator
from evaluation.metrics import Metrics


logger = get_logger(__name__)


class Pipeline:
    """
    Executes the complete Track 1 processing pipeline.

    Pipeline owns the ONLY frame-processing loop.

    Responsibilities
    ----------------
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
    Metrics
        ↓
    Evaluation

    Pipeline is intentionally unaware of:

    - benchmarking
    - exporting
    - experiment types
    - output directories
    """

    def __init__(
        self,
        *,
        video_loader,
        detector,
        tracker,
        trajectory_manager,
        speed_estimator,
        metrics: Metrics,
        evaluator: Evaluator,
        visualizer,
    ) -> None:

        self.video_loader = video_loader

        self.detector = detector

        self.tracker = tracker

        self.trajectory_manager = (
            trajectory_manager
        )

        self.speed_estimator = (
            speed_estimator
        )

        self.metrics = metrics

        self.evaluator = evaluator

        self.visualizer = visualizer

    # ------------------------------------------------------------------ #
    # Run
    # ------------------------------------------------------------------ #

    def run(
        self,
    ) -> BenchmarkSummary:

        logger.info(
            "Pipeline started."
        )

        for frame_number, frame in self.video_loader:

            start_time = (
                time.perf_counter()
            )

            # ----------------------------------------------------------
            # Detection
            # ----------------------------------------------------------

            detections = (
                self.detector.detect(
                    frame
                )
            )

            # ----------------------------------------------------------
            # Tracking
            # ----------------------------------------------------------

            tracks = (
                self.tracker.update(
                    detections,
                    frame,
                )
            )

            # ----------------------------------------------------------
            # Trajectory Management
            # ----------------------------------------------------------

            self.trajectory_manager.update(
                tracks
            )

            # ----------------------------------------------------------
            # Speed Estimation
            # ----------------------------------------------------------

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

                speeds.append(
                    speed
                )

                speed_map[
                    track.track_id
                ] = speed

            processing_time = (
                time.perf_counter()
                - start_time
            )

            fps = (
                1.0 / processing_time
                if processing_time > 0
                else 0.0
            )

            # ----------------------------------------------------------
            # Visualization
            # ----------------------------------------------------------

            annotated_frame = (
                self.visualizer.draw_tracks(
                    frame=frame,
                    tracks=tracks,
                    speeds=speed_map,
                    fps=fps,
                    frame_number=frame_number,
                )
            )

            # ----------------------------------------------------------
            # Always write.
            # Visualizer internally performs a no-op when
            # no VideoWriter has been configured.
            # ----------------------------------------------------------

            self.visualizer.write(
                annotated_frame
            )

            # ----------------------------------------------------------
            # Runtime Metrics
            # ----------------------------------------------------------

            self.metrics.update(
                processing_time=processing_time,
                num_detections=len(
                    detections
                ),
                num_tracks=len(
                    tracks
                ),
                speeds=speeds,
            )

            # ----------------------------------------------------------
            # Algorithm Evaluation
            # ----------------------------------------------------------

            self.evaluator.update(
                detections=detections,
                tracks=tracks,
                speeds=speeds,
            )

        # --------------------------------------------------------------
        # Cleanup
        # --------------------------------------------------------------

        self.visualizer.close()

        self.video_loader.release()

        logger.info(
            "Pipeline finished."
        )

        return self.metrics.summary()