# ============================================================================
# pipeline.py (Part 1/3)
# ============================================================================

from __future__ import annotations

import time

from core.logger import get_logger

from evaluation.metrics import Metrics


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
    Metrics
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
        *,
        benchmark_config: dict | None = None,
    ) -> None:

        self.video_loader = video_loader

        self.detector = detector

        self.tracker = tracker

        self.trajectory_manager = trajectory_manager

        self.speed_estimator = speed_estimator

        self.evaluator = evaluator

        self.visualizer = visualizer

        self.metrics = Metrics()

        benchmark_config = (
            benchmark_config
            if benchmark_config is not None
            else {}
        )

        self.benchmark_enabled = (
            benchmark_config.get(
                "enabled",
                False,
            )
        )

        self.save_video = (
            benchmark_config.get(
                "save_video",
                False,
            )
        )

        self.save_csv = (
            benchmark_config.get(
                "save_csv",
                False,
            )
        )

        self.save_json = (
            benchmark_config.get(
                "save_json",
                False,
            )
        )

        self.csv_output_path = (
            benchmark_config.get(
                "csv_output_path"
            )
        )

        self.json_output_path = (
            benchmark_config.get(
                "json_output_path"
            )
        )

    # ------------------------------------------------------------------ #
    # Run
    # ------------------------------------------------------------------ #

    def run(
        self,
    ) -> dict | None:

        logger.info(
            "Pipeline started."
        )

        for frame_number, frame in self.video_loader:

            start = time.perf_counter()

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

            # ----------------------------------------------------------
            # Visualization
            # ----------------------------------------------------------

            processing_time = (
                time.perf_counter()
                - start
            )

            fps = (
                1.0 / processing_time
                if processing_time > 0
                else 0.0
            )

            annotated_frame = (
                self.visualizer.draw_tracks(
                    frame=frame,
                    tracks=tracks,
                    speeds=speed_map,
                    fps=fps,
                    frame_number=frame_number,
                )
            )

            if (
                self.benchmark_enabled
                and self.save_video
            ):
                self.visualizer.write(
                    annotated_frame
                )

                            # ----------------------------------------------------------
            # Evaluation
            # ----------------------------------------------------------

            self.evaluator.update(
                num_detections=len(
                    detections
                ),
                processing_time=processing_time,
                speeds=speeds,
            )

            # ----------------------------------------------------------
            # Metrics
            # ----------------------------------------------------------

            self.metrics.update(
                frame_number=frame_number,
                processing_time=processing_time,
                num_detections=len(
                    detections
                ),
                num_tracks=len(
                    tracks
                ),
                speeds=speeds,
            )

            # --------------------------------------------------------------
            # Pipeline Finished
            # --------------------------------------------------------------

            logger.info(
                "Pipeline finished."
            )

            self.evaluator.print_summary()

            summary = (
                self.metrics.summary()
            )

            if self.benchmark_enabled:

                if (
                    self.save_csv
                    and self.csv_output_path
                ):
                    self.metrics.save_csv(
                        self.csv_output_path
                    )

                if (
                    self.save_json
                    and self.json_output_path
                ):
                    self.metrics.save_json(
                        self.json_output_path
                    )

                self.visualizer.close()

                return summary

            return None